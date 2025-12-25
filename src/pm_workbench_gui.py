#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SENAI TASK MINING - Gravador e exportador
-----------------------------------------
GUI simples para:
- Iniciar/parar o aw_watcher_uia.py
- Exportar os eventos da sessão (window + input + uia) para CSV
  compatível com o pm_analysis_gui.py (colunas:
  case:concept:name, concept:name, time:timestamp, ...)

Pré-requisitos no .venv:
    pip install aw-client pandas

O ActivityWatch (aw-server) precisa estar rodando.
"""

import sys
import os
import csv
import logging
import subprocess
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox

try:
    from aw_client import ActivityWatchClient
except ImportError:
    ActivityWatchClient = None

# ---------------------------------------------------------------------
# Caminhos básicos
# ---------------------------------------------------------------------
from pathlib import Path

# Diretório de recursos (onde ficam .ico e outros arquivos empacotados)
if getattr(sys, 'frozen', False):
    # Executável PyInstaller
    RESOURCE_DIR = Path(sys._MEIPASS)
else:
    # Desenvolvimento: subir um nível da pasta src para a raiz do projeto
    RESOURCE_DIR = Path(__file__).resolve().parent.parent

# Diretório de dados (gravável) - evita problemas em Program Files / pastas protegidas
DATA_DIR = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'SENAI_Process_Mining_Suite'
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR = DATA_DIR / 'outputs'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_PATH = DATA_DIR / 'pm_workbench_gui.log'

# Ajuste este caminho se mudar a pasta do watcher
AW_UIA_DIR = RESOURCE_DIR  # modo frozen usa o próprio EXE para rodar o watcher
AW_UIA_SCRIPT = AW_UIA_DIR / "aw_watcher_uia.py"

def _watcher_cmd():
    """No executável, o watcher roda chamando o próprio EXE com --uia-watcher."""
    if getattr(sys, 'frozen', False):
        return [sys.executable, '--uia-watcher']
    return [sys.executable, str(AW_UIA_SCRIPT)]

logger = logging.getLogger("pm_workbench_gui")


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


# ---------------------------------------------------------------------
# Lógica de exportação ActivityWatch → CSV
# ---------------------------------------------------------------------
def _collect_events_between(start_utc, end_utc):
    """
    Coleta eventos dos buckets aw-watcher-window / aw-watcher-input / aw-watcher-uia
    entre start_utc e end_utc usando aw_client.
    Retorna lista de tuplas (timestamp, data_dict, source_label, bucket_id).
    """
    if ActivityWatchClient is None:
        raise RuntimeError(
            "Biblioteca 'aw_client' não encontrada no .venv.\n"
            "Instale com: pip install aw-client"
        )

    client = ActivityWatchClient("senai-taskmining-export")
    client.connect()

    buckets = client.get_buckets()  # dict: bucket_id -> metadata
    window_ids = [bid for bid in buckets.keys() if "aw-watcher-window" in bid]
    input_ids = [bid for bid in buckets.keys() if "aw-watcher-input" in bid]
    uia_ids = [bid for bid in buckets.keys() if "aw-watcher-uia" in bid]

    all_events = []

    def _grab(bid_list, label):
        nonlocal all_events
        for bid in bid_list:
            try:
                evs = client.get_events(bid, start=start_utc, end=end_utc)
                for ev in evs:
                    # ev pode ser dict ou um objeto Event
                    if isinstance(ev, dict):
                        ts = ev.get("timestamp")
                        data = ev.get("data", {}) or {}
                    else:
                        ts = getattr(ev, "timestamp", None)
                        data = getattr(ev, "data", {}) or {}
                    all_events.append((ts, data, label, bid))
            except Exception as e:
                logger.warning("Falha ao ler bucket %s: %s", bid, e)

    _grab(window_ids, "window")
    _grab(input_ids, "input")
    _grab(uia_ids, "uia")

    if not all_events:
        raise RuntimeError("Janela sem eventos (curta demais?).")

    # Ordena por horário
    all_events.sort(key=lambda x: x[0] or datetime.min.replace(tzinfo=timezone.utc))
    return all_events


def export_aw_between_to_csv(start_utc, end_utc, out_dir: Path) -> str:
    """
    Exporta eventos AW em uma janela [start_utc, end_utc] para um CSV COMBINED.
    Retorna o caminho do CSV.
    Lança RuntimeError se não houver eventos.
    """
    events = _collect_events_between(start_utc, end_utc)
    if not events:
        raise RuntimeError("Janela sem eventos (curta demais?).")

    rows = []
    case_id = "1"

    for ts, data, source_label, bucket_id in events:
        if ts is None:
            continue
        if not isinstance(ts, datetime):
            try:
                ts = datetime.fromisoformat(str(ts))
            except Exception:
                continue
        ts_utc = ts.astimezone(timezone.utc)

        app = data.get("app") or data.get("exe") or ""
        title = data.get("title") or data.get("window_title") or data.get("name") or ""
        etype = data.get("etype") or data.get("event_type") or data.get("key_category") or source_label

        parts = [p for p in [etype, app, title] if p]
        activity = " | ".join(parts) if parts else "EVENTO"

        rows.append(
            {
                "case:concept:name": case_id,
                "concept:name": activity,
                "time:timestamp": ts_utc.isoformat(),
                "aw:bucket": bucket_id,
                "aw:source": source_label,
                "aw:app": app,
                "aw:title": title,
                "aw:etype": etype,
            }
        )

    if not rows:
        raise RuntimeError("Sem linhas após o processamento dos eventos.")

    # Nome com data + hora início/fim (local)
    start_local = start_utc.astimezone()
    end_local = end_utc.astimezone()
    date_str = start_local.strftime("%d%m%Y")
    start_str = start_local.strftime("%H-%M")
    end_str = end_local.strftime("%H-%M")
    fname = f"event_log_COMBINED_{date_str}_{start_str}_{end_str}.csv"
    out_path = out_dir / fname

    fieldnames = list(rows[0].keys())
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return str(out_path)


# ---------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------
class WorkbenchApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SENAI TASK MINING - Gravador e exportador")
        self._config_icon()
        self.geometry("650x350")

        self.watcher_proc = None
        self.session_start_utc = None

        self._build_gui()

    # ------------------------------------------------------------- GUI
    def _config_icon(self):
        ico = RESOURCE_DIR / "assets" / "senai.ico"
        if not ico.exists():
        	ico = RESOURCE_DIR / "senai.ico"
        if ico.exists():
            try:
                self.iconbitmap(str(ico))
            except Exception:
                pass

    def _build_gui(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill="both", expand=True)

        status_frame = ttk.LabelFrame(frm, text="Status do gravador")
        status_frame.pack(fill="x", pady=5)

        self.status_var = tk.StringVar(value="Parado")
        ttk.Label(status_frame, textvariable=self.status_var).pack(anchor="w")

        self.pid_var = tk.StringVar(value="PID: -")
        ttk.Label(status_frame, textvariable=self.pid_var).pack(anchor="w")

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill="x", pady=10)

        self.btn_start = ttk.Button(btn_frame, text="Iniciar gravação", command=self.on_start)
        self.btn_start.grid(row=0, column=0, padx=5)

        self.btn_stop_export = ttk.Button(
            btn_frame,
            text="Parar e exportar sessão",
            command=self.on_stop_and_export,
            state="disabled",
        )
        self.btn_stop_export.grid(row=0, column=1, padx=5)

        info = (
            "• Ao clicar em 'Iniciar gravação', o aw_watcher_uia.py será iniciado.\n"
            "• Ao clicar em 'Parar e exportar sessão', o watcher será encerrado e\n"
            "  um CSV COMBINED será gerado na pasta 'outputs'.\n\n"
            "Depois, abra o arquivo no 'SENAI TASK MINING - Análises' para gerar\n"
            "DFG, estatísticas e variantes."
        )
        ttk.Label(frm, text=info, justify="left").pack(fill="x", pady=5)

        log_frame = ttk.LabelFrame(frm, text="Log")
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(log_frame, height=8, wrap="word", state="disabled")
        self.log_text.pack(fill="both", expand=True)

    def _append_log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        full = f"[{ts}] {msg}\n"
        logger.info(msg)
        self.log_text.configure(state="normal")
        self.log_text.insert("end", full)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    # ----------------------------------------------------- Controle watcher
    def on_start(self):
        if self.watcher_proc and self.watcher_proc.poll() is None:
            messagebox.showinfo("Já está rodando", "O gravador já está em execução.")
            return

        if (not getattr(sys, 'frozen', False)) and (not AW_UIA_SCRIPT.exists()):
            messagebox.showerror(
                "Erro",
                f"Script aw_watcher_uia.py não encontrado em:\n{AW_UIA_SCRIPT}",
            )
            return

        try:
            python_exe = sys.executable
            self.session_start_utc = datetime.now(timezone.utc)

            self.watcher_proc = subprocess.Popen(
                _watcher_cmd(),
                cwd=str(AW_UIA_DIR),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )

            pid = self.watcher_proc.pid
            self.status_var.set("Gravando")
            self.pid_var.set(f"PID: {pid}")
            self.btn_start.configure(state="disabled")
            self.btn_stop_export.configure(state="normal")
            self._append_log(f"Watcher iniciado. PID={pid}")
        except Exception as e:
            self._append_log(f"[ERRO] Falha ao iniciar watcher: {e}")
            messagebox.showerror("Erro", f"Falha ao iniciar watcher:\n{e}")

    def on_stop_and_export(self):
        if not self.watcher_proc:
            return

        # Para o watcher
        try:
            if self.watcher_proc.poll() is None:
                self.watcher_proc.terminate()
                try:
                    self.watcher_proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.watcher_proc.kill()
            self._append_log("Watcher parado.")
        except Exception as e:
            self._append_log(f"[ERRO] Ao parar watcher: {e}")
        finally:
            self.watcher_proc = None
            self.status_var.set("Parado")
            self.pid_var.set("PID: -")
            self.btn_start.configure(state="normal")
            self.btn_stop_export.configure(state="disabled")

        if not self.session_start_utc:
            messagebox.showwarning(
                "Sessão desconhecida",
                "Hora de início da sessão não registrada. Não é possível exportar.",
            )
            return

        end_utc = datetime.now(timezone.utc)

        # Exporta em thread para não travar a UI
        t = threading.Thread(
            target=self._export_session_thread,
            args=(self.session_start_utc, end_utc),
            daemon=True,
        )
        t.start()

    def _export_session_thread(self, start_utc, end_utc):
        try:
            out_csv = self._export_with_fallback(start_utc, end_utc)
            self._append_log(f"Event log exportado: {out_csv}")
            messagebox.showinfo("Sucesso", f"Event log exportado para:\n{out_csv}")
        except Exception as e:
            self._append_log(f"[ERRO] Exportar sessão: {e}")
            messagebox.showerror("Erro", f"Falha ao exportar sessão:\n{e}")

    def _export_with_fallback(self, start_utc, end_utc) -> str:
        """
        Tenta exportar em algumas janelas diferentes para reduzir o problema
        de "sem eventos" se o relógio estiver um pouco desalinhado.
        """
        testes = [
            ("Sessão Start→Agora (janela solicitada)", start_utc, end_utc),
            (
                "Sessão Start→Agora (±60s/5s)",
                start_utc - timedelta(seconds=60),
                end_utc + timedelta(seconds=5),
            ),
            ("Fallback: últimos 15 min", end_utc - timedelta(minutes=15), end_utc),
            ("Fallback: últimos 60 min", end_utc - timedelta(minutes=60), end_utc),
        ]

        last_err = None
        for label, s, e in testes:
            self._append_log(
                f"Tentando exportar: {label} | {s.isoformat()} → {e.isoformat()}"
            )
            try:
                csv_path = export_aw_between_to_csv(s, e, OUTPUT_DIR)
                return csv_path
            except RuntimeError as re:
                self._append_log("Sem eventos nessa janela.")
                last_err = re
            except Exception as e:
                self._append_log(f"[ERRO] Janela '{label}': {e}")
                last_err = e

        raise RuntimeError(
            "Não há eventos nas janelas testadas. "
            "Faça algumas ações (ALT+TAB, digitação) por ~15s e tente de novo."
        ) from last_err


def main():
    setup_logging()
    app = WorkbenchApp()
    app.mainloop()


if __name__ == "__main__":
    main()