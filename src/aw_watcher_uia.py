# aw_watcher_uia.py
# Captura eventos de UI no Windows (cliques + foco/keypress como sinal) e publica no ActivityWatch
# Licença: MIT

import argparse
import json
import os
import queue
import threading
import time
from datetime import datetime, timezone

import psutil
import uiautomation as uia
from pynput import mouse, keyboard
from tzlocal import get_localzone

try:
    from aw_client import ActivityWatchClient
except Exception as e:
    raise SystemExit("aw-client não encontrado. pip install aw-client")

LOCAL_TZ = get_localzone()

# -------- Utilidades --------

def now_iso():
    return datetime.now(timezone.utc).astimezone(LOCAL_TZ).isoformat()


def bbox_to_dict(rect):
    # rect: uia.Rect(left, top, right, bottom)
    try:
        return {
            "left": int(rect.left),
            "top": int(rect.top),
            "right": int(rect.right),
            "bottom": int(rect.bottom),
        }
    except Exception:
        return None


def control_path(ctrl, depth=4):
    """Constrói um caminho curto na árvore de controles para contexto."""
    parts = []
    try:
        cur = ctrl
        for _ in range(depth):
            if not cur:
                break
            parts.append(f"{cur.ControlTypeName}:{(cur.Name or '').strip()[:30]}")
            cur = cur.GetParentControl()
    except Exception:
        pass
    return list(reversed(parts))


def proc_name(pid):
    try:
        return psutil.Process(pid).name()
    except Exception:
        return None


# -------- Captura de contexto --------
def context_from_point(x, y):
    """Extrai metadados do controle sob o cursor (x,y)."""
    try:
        ctrl = uia.ControlFromPoint((int(x), int(y)))
        if not ctrl:
            return None
        top = ctrl.GetTopWindowControl() or ctrl
        data = {
            "app": proc_name(ctrl.ProcessId),
            "pid": ctrl.ProcessId,
            "window_title": (top.Name or "").strip(),
            "control_type": ctrl.ControlTypeName,
            "control_name": (ctrl.Name or "").strip(),
            "automation_id": (ctrl.AutomationId or "").strip(),
            "bbox": bbox_to_dict(ctrl.BoundingRectangle),
            "path": control_path(ctrl),
        }
        return data
    except Exception:
        return None


def context_from_focus():
    """Extrai metadados do controle com foco atual (para keypress)."""
    try:
        ctrl = uia.GetFocusedControl()
        if not ctrl:
            return None
        top = ctrl.GetTopWindowControl() or ctrl
        data = {
            "app": proc_name(ctrl.ProcessId),
            "pid": ctrl.ProcessId,
            "window_title": (top.Name or "").strip(),
            "control_type": ctrl.ControlTypeName,
            "control_name": (ctrl.Name or "").strip(),
            "automation_id": (ctrl.AutomationId or "").strip(),
            "bbox": bbox_to_dict(ctrl.BoundingRectangle),
            "path": control_path(ctrl),
        }
        return data
    except Exception:
        return None


# -------- Worker de envio para ActivityWatch --------
class AWPublisher:
    def __init__(self, bucket_id, bucket_type="uia.event", host="127.0.0.1", port=5600):
        self.client = ActivityWatchClient("aw-watcher-uia", host=host, port=port)
        self.bucket_id = bucket_id
        self.bucket_type = bucket_type
        self.queue = queue.Queue(maxsize=10000)
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self.client.connect()
        try:
            self.client.create_bucket(self.bucket_id, self.bucket_type, event_schema={})
        except Exception:
            # bucket já existe
            pass
        self.thread.start()

    def _run(self):
        batch = []
        last_flush = time.time()
        while not self.stop_event.is_set():
            try:
                item = self.queue.get(timeout=0.5)
                batch.append(item)
            except queue.Empty:
                pass
            # flush a cada 1s ou 200 eventos
            if batch and (time.time() - last_flush > 1.0 or len(batch) >= 200):
                try:
                    self.client.insert_events(self.bucket_id, batch)
                except Exception as e:
                    # opcional: logar e re-enfileirar
                    pass
                batch = []
                last_flush = time.time()
        # flush final
        if batch:
            try:
                self.client.insert_events(self.bucket_id, batch)
            except Exception:
                pass

    def publish(self, event):
        try:
            self.queue.put_nowait(event)
        except queue.Full:
            pass

    def stop(self):
        self.stop_event.set()
        self.thread.join(timeout=2)


# -------- Main listener --------

def main():
    parser = argparse.ArgumentParser(description="ActivityWatch UIA watcher (desktop)")
    parser.add_argument("--allow", type=str, default="",
                        help="Lista separada por ; com nomes de processos permitidos (ex: EXCEL.EXE;chrome.exe)")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5600)
    parser.add_argument("--bucket", type=str, default=None, help="Bucket ID opcional. Padrão: aw-watcher-uia_<HOST>")
    parser.add_argument("--pausefile", type=str, default="aw_uia.PAUSE",
                        help="Arquivo sentinela para pausar a captura se existir")
    args = parser.parse_args()

    allowlist = [p.strip().lower() for p in args.allow.split(";") if p.strip()] if args.allow else []

    host_name = os.environ.get("COMPUTERNAME", "host").lower()
    bucket_id = args.bucket or f"aw-watcher-uia_{host_name}"

    pub = AWPublisher(bucket_id=bucket_id, host=args.host, port=args.port)
    pub.start()

    def allowed(app_name):
        if not app_name:
            return False
        if not allowlist:
            return True
        return app_name.lower() in allowlist

    def now_event(data):
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "duration": 0,
            "data": data,
        }

    def on_click(x, y, button, pressed):
        if not pressed:
            return
        if os.path.exists(args.pausefile):
            return
        ctx = context_from_point(x, y)
        if not ctx or not allowed(ctx.get("app")):
            return
        ev = now_event({
            "etype": "mouse_click",
            "button": str(button),
            **ctx,
        })
        pub.publish(ev)

    def on_press(key):
        if os.path.exists(args.pausefile):
            return
        ctx = context_from_focus()
        if not ctx or not allowed(ctx.get("app")):
            return
        # Não gravamos a tecla; apenas tipo/categoria
        etype = "key_press"
        try:
            vk = key.vk  # pode não existir em algumas plataformas
        except AttributeError:
            vk = None
        category = "control" if vk in (9, 13, 27) else "alpha"
        ev = now_event({
            "etype": etype,
            "key_category": category,
            **ctx,
        })
        pub.publish(ev)

    mlistener = mouse.Listener(on_click=on_click)
    klistener = keyboard.Listener(on_press=on_press)

    mlistener.start()
    klistener.start()

    print(f"[uia-watcher] Rodando. Bucket: {bucket_id}. Allowlist: {allowlist or 'TODOS'}")
    print("Crie o arquivo 'aw_uia.PAUSE' na pasta atual para pausar.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        mlistener.stop()
        klistener.stop()
        pub.stop()


if __name__ == "__main__":
    main()
