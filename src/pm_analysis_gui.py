# ============================================================================
# Configuração do Graphviz Portátil
# ============================================================================
import os
import sys

def setup_graphviz():
    """Adiciona Graphviz portátil ao PATH"""
    if getattr(sys, 'frozen', False):
        # Executável PyInstaller
        base_path = sys._MEIPASS
    else:
        # Desenvolvimento
        base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(base_path)  # Volta para raiz
    
    # Caminho do Graphviz
    graphviz_bin = os.path.join(base_path, 'vendor', 'graphviz', 'bin')
    
    if os.path.exists(graphviz_bin):
        # Adiciona ao PATH em tempo de execução
        os.environ['PATH'] = graphviz_bin + os.pathsep + os.environ.get('PATH', '')
        print(f"[INFO] Graphviz configurado: {graphviz_bin}")
        return True
    else:
        print(f"[WARN] Graphviz não encontrado em: {graphviz_bin}")
        return False

# Configurar Graphviz ao importar o módulo
setup_graphviz()

import os
import sys
import shutil
import datetime
import textwrap
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# Diretório de recursos (onde ficam .ico e outros arquivos empacotados)
if getattr(sys, 'frozen', False):
    # Executável PyInstaller
    RESOURCE_DIR = Path(sys._MEIPASS)
else:
    # Desenvolvimento: subir um nível da pasta src para a raiz do projeto
    RESOURCE_DIR = Path(__file__).resolve().parent.parent

import pandas as pd
import pickle
import hashlib

from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_TIMESTAMP_KEY
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualizer
from pm4py.statistics.variants.log import get as variants_get
try:
    # PM4Py mais novo
    from pm4py.evaluation.replay_fitness.variants import alignment_based as replay_fitness_alignment
except ImportError:
    # PM4Py antigo (seu caso)
    from pm4py.algo.evaluation.replay_fitness.variants import alignment_based as replay_fitness_alignment



# ======================================================
# MONKEY-PATCH HASHLIB (para erro do usedforsecurity)
# ======================================================

_orig_new = hashlib.new
def _hashlib_new(name, data=b"", **kwargs):
    kwargs.pop("usedforsecurity", None)
    return _orig_new(name, data, **kwargs)
hashlib.new = _hashlib_new

_orig_md5 = hashlib.md5
def _hashlib_md5(*args, **kwargs):
    kwargs.pop("usedforsecurity", None)
    return _orig_md5(*args, **kwargs)
hashlib.md5 = _hashlib_md5


# ======================================================
# CATEGORIZAÇÃO DE APLICATIVOS (Business x Pessoal)
# ======================================================

# Ajuste aqui conforme a sua realidade. Use o nome do executável
# exatamente como aparece na coluna "app" do CSV exportado.


# ============================================================================
# CONFIGURAÇÃO DE DIRETÓRIO DE SAÍDA
# ============================================================================
def get_output_directory():
    """
    Retorna o diretório onde os outputs serão salvos.
    Cria a estrutura de pastas se não existir.
    """
    from pathlib import Path
    
    # Documentos do usuário
    base_dir = Path.home() / "Documents" / "SENAI_ProcessMining"
    output_dir = base_dir / "outputs"
    
    # Criar pasta
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return str(output_dir)

# Diretório de saída global
OUTPUT_DIR = get_output_directory()

print("="*70)
print("SENAI Process Mining - Analysis")
print(f"Outputs serão salvos em: {OUTPUT_DIR}")
print("="*70)
print()

# ============================================================================


BUSINESS_APPS = {
    "chrome.exe",
    "firefox.exe",
    "msedge.exe",
    "EXCEL.EXE",
    "POWERPNT.EXE",
    "WINWORD.EXE",
    "totvs.exe",
    "saplogon.exe",
    "sapshcut.exe",
    "code.exe",
    "pycharm64.exe",
}

PERSONAL_APPS = {
    "whatsapp.exe",
    "telegram.exe",
    "discord.exe",
    "spotify.exe",
    "vlc.exe",
    "netflix.exe",
    "instagram.exe",
    "tiktok.exe",
    "youtube.exe",
}

BUSINESS_LOWER = {a.lower() for a in BUSINESS_APPS}
PERSONAL_LOWER = {a.lower() for a in PERSONAL_APPS}


def classificar_app(app_name: str) -> str:
    """Classifica o executável em Business, Pessoal ou Outros."""
    if not isinstance(app_name, str):
        return "Outros"
    name = app_name.lower()
    if name in BUSINESS_LOWER:
        return "Business"
    if name in PERSONAL_LOWER:
        return "Pessoal"
    return "Outros"


# ======================================================
# UTILITÁRIOS DE PROCESSO / LOG
# ======================================================

def _check_graphviz():
    """Verifica se o binário 'dot' do Graphviz está acessível.
    Apenas emite um aviso no console se não encontrar.
    """
    if shutil.which("dot") is None:
        print(
            "[WARN] Binário 'dot' do Graphviz não encontrado no PATH. "
            "Se os gráficos de DFG/Inductive falharem, verifique a instalação do Graphviz."
        )


def _ensure_duration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Garante coluna 'duration' em segundos, calculada por diferença de timestamps
    dentro de cada caso.
    """
    df = df.copy()
    ts_col = "time:timestamp"

    if ts_col not in df.columns:
        raise RuntimeError(f"CSV não contém a coluna '{ts_col}' necessária para calcular duração.")

    if "case:concept:name" not in df.columns:
        df["case:concept:name"] = "CASE_1"

    df[ts_col] = pd.to_datetime(df[ts_col], utc=True, errors="coerce")
    df = df.dropna(subset=[ts_col])

    df = df.sort_values(by=["case:concept:name", ts_col])

    df["__next_ts"] = df.groupby("case:concept:name")[ts_col].shift(-1)
    df["duration"] = (df["__next_ts"] - df[ts_col]).dt.total_seconds()
    df["duration"] = df["duration"].fillna(0).clip(lower=0)
    df = df.drop(columns=["__next_ts"])

    return df


def _csv_to_eventlog(csv_path: str):
    """Lê o CSV exportado pelo gravador e converte em event log do pm4py."""
    df = pd.read_csv(csv_path)

    required = ["case:concept:name", "concept:name", "time:timestamp"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(
            "CSV não contém as colunas obrigatórias: "
            + ", ".join(required)
            + f". Ausentes: {', '.join(missing)}"
        )

    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], utc=True, errors="coerce")
    df = df.dropna(subset=["time:timestamp"])

    df_pm = dataframe_utils.convert_timestamp_columns_in_df(df)

    parameters = {
        "case_id_key": "case:concept:name",
        "activity_key": "concept:name",
        "timestamp_key": "time:timestamp",
    }

    event_log = log_converter.apply(
        df_pm,
        variant=log_converter.Variants.TO_EVENT_LOG,
        parameters=parameters,
    )

    for trace in event_log:
        for event in trace:
            if DEFAULT_NAME_KEY not in event and "concept:name" in event:
                event[DEFAULT_NAME_KEY] = event["concept:name"]
            if DEFAULT_TIMESTAMP_KEY not in event and "time:timestamp" in event:
                event[DEFAULT_TIMESTAMP_KEY] = event["time:timestamp"]

    return event_log, df_pm


# ======================================================
# KPIs, VARIANTES, DFG, IND-MINER, TIMELINE
# ======================================================

def compute_kpis(csv_path: str):
    """Gera KPIs do processo, top atividades e resumo por tipo de app."""
    df = pd.read_csv(csv_path)
    df = _ensure_duration(df)

    # Classificação por tipo de app (Business / Pessoal / Outros)
    # Tornar coluna 'app' opcional
    if "app" in df.columns:
        df["app_category"] = df["app"].apply(classificar_app)
    else:
        df["app_category"] = "Outros"
        df["app"] = "Desconhecido"  # Criar coluna fictícia

    # Tempo total observado (somando durations entre eventos)
    total_seconds_obs = float(df["duration"].sum())
    total_minutes_obs = total_seconds_obs / 60.0
    total_hours_obs = total_minutes_obs / 60.0

    # Eventos e casos
    num_events = len(df)
    num_cases = df["case:concept:name"].nunique() if "case:concept:name" in df.columns else 1

    if "concept:name" not in df.columns:
        raise RuntimeError("CSV não contém a coluna 'concept:name'.")

    # Top atividades por tempo acumulado
    grouped = df.groupby("concept:name", as_index=False).agg(
        num_eventos=("concept:name", "count"),
        tempo_total_segundos=("duration", "sum"),
    )
    grouped["tempo_total_min"] = grouped["tempo_total_segundos"] / 60.0
    grouped = grouped.sort_values(by="tempo_total_segundos", ascending=False)

    # Tempo médio e total de execução por traço
    avg_case_seconds = None
    total_case_seconds = None
    if "case:concept:name" in df.columns and "time:timestamp" in df.columns:
        df_sorted = df.sort_values(["case:concept:name", "time:timestamp"])
        grp_ts = df_sorted.groupby("case:concept:name")["time:timestamp"]
        start = grp_ts.min()
        end = grp_ts.max()
        case_durations = (end - start).dt.total_seconds()
        if len(case_durations) > 0:
            avg_case_seconds = float(case_durations.mean())
            total_case_seconds = float(case_durations.sum())

    # Variantes (traços únicos) + aderência ao processo padrão
    total_unique_variants = None
    adherence = None
    if "case:concept:name" in df.columns and "concept:name" in df.columns:
        df_seq = df.sort_values(["case:concept:name", "time:timestamp"])
        sequences = df_seq.groupby("case:concept:name")["concept:name"].apply(tuple)
        if len(sequences) > 0:
            counts = sequences.value_counts()
            total_unique_variants = counts.shape[0]
            top_count = counts.iloc[0]
            adherence = (top_count / len(sequences)) * 100.0

    # Quantidade de usuários
    if "org:resource" in df.columns:
        num_users = df["org:resource"].nunique()
    else:
        num_users = 0

    # Quantidade de aplicações
    if "app" in df.columns:
        num_apps = df["app"].nunique()
    else:
        num_apps = 0
        if "app" not in df.columns:
            df["app"] = "Desconhecido"

    # Quantidade média de ações por tarefa (eventos por caso)
    actions_per_case = None
    if num_cases > 0:
        actions_per_case = num_events / num_cases

    base_name = os.path.basename(csv_path)


    base, _ = os.path.splitext(base_name)
    resumo_path = os.path.join(OUTPUT_DIR, base + "__kpis_resumo.txt")
    top_ativ_path = os.path.join(OUTPUT_DIR, base + "__kpis_top_atividades.csv")
    apps_cat_path = os.path.join(OUTPUT_DIR, base + "__apps_categories.csv")

    grouped.to_csv(top_ativ_path, index=False)

    # Uso por tipo de aplicação
    # Garantir que app_category existe
    if "app_category" not in df.columns:
        df["app_category"] = "Outros"
    if "app" not in df.columns:
        df["app"] = "Desconhecido"
    
    cat_group = df.groupby("app_category", as_index=False).agg(
        tempo_total_segundos=("duration", "sum"),
        num_eventos=("app", "count"),
        num_apps=("app", "nunique"),
    )
    if total_seconds_obs > 0:
        cat_group["perc_tempo"] = cat_group["tempo_total_segundos"] / total_seconds_obs * 100.0
    else:
        cat_group["perc_tempo"] = 0.0
    cat_group["tempo_total_min"] = cat_group["tempo_total_segundos"] / 60.0
    cat_group.to_csv(apps_cat_path, index=False)

    def fmt_secs(seconds):
        if seconds is None:
            return "n/d"
        seconds = int(seconds)
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        if h > 0:
            return f"{h}h {m}min {s}s"
        elif m > 0:
            return f"{m}min {s}s"
        else:
            return f"{s}s"

    linhas = []
    linhas.append(f"Arquivo de origem: {csv_path}")
    linhas.append("")
    linhas.append(f"Tempo total observado (todos os eventos): {total_minutes_obs:.1f} min ({total_hours_obs:.2f} h)")
    linhas.append(f"Número de eventos: {num_events}")
    linhas.append(f"Número de casos (traços): {num_cases}")

    if total_unique_variants is not None:
        linhas.append(f"Total de traços únicos (variantes): {total_unique_variants}")

    linhas.append(f"Quantidade de usuários: {num_users}")
    linhas.append(f"Quantidade de aplicações: {num_apps}")

    if adherence is not None:
        linhas.append(f"Percentual de aderência ao processo padrão: {adherence:.2f}%")

    linhas.append(f"Tempo médio de execução por traço: {fmt_secs(avg_case_seconds)}")
    linhas.append(f"Tempo total gasto (soma dos tempos de execução dos traços): {fmt_secs(total_case_seconds)}")

    if actions_per_case is not None:
        linhas.append(f"Quantidade média de ações por tarefa (caso): {actions_per_case:.2f}")

    linhas.append("")
    linhas.append("Tempo por tipo de aplicação (Business / Pessoal / Outros):")
    for _, row in cat_group.iterrows():
        linhas.append(
            f"- {row['app_category']}: {row['tempo_total_min']:.1f} min "
            f"({row['perc_tempo']:.1f}% do tempo observado), "
            f"{row['num_eventos']} eventos, {row['num_apps']} app(s)."
        )

    linhas.append("")
    linhas.append("Top atividades por tempo acumulado (Top 10):")
    for _, row in grouped.head(10).iterrows():
        nome = row["concept:name"]
        tmin = row["tempo_total_min"]
        nevt = row["num_eventos"]
        linhas.append(f"- {nome}: {tmin:.1f} min em {nevt} eventos")
    linhas.append("")
    linhas.append(f"Tabela completa de top atividades salva em: {top_ativ_path}")
    linhas.append(f"Tabela de categorias de apps salva em: {apps_cat_path}")

    kpis_text = "\n".join(linhas)

    with open(resumo_path, "w", encoding="utf-8") as f:
        f.write(kpis_text)

    print(kpis_text)
    print(f"Resumo salvo em: {resumo_path}")
    print(f"Top atividades salvo em: {top_ativ_path}")
    print(f"Categorias de apps salvas em: {apps_cat_path}")
    return resumo_path, top_ativ_path


def compute_variants(csv_path: str):
    """Calcula variantes do processo e salva em CSV (todas as variantes)."""
    event_log, df_pm = _csv_to_eventlog(csv_path)

    variants = variants_get.get_variants(event_log)

    rows = []
    for variant_str, traces in variants.items():
        rows.append(
            {
                "variant": variant_str,
                "num_cases": len(traces),
            }
        )

    df_variants = pd.DataFrame(rows).sort_values(by="num_cases", ascending=False)

    base_name = os.path.basename(csv_path)


    base, _ = os.path.splitext(base_name)
    out_path = os.path.join(OUTPUT_DIR, base + "__variants_all.csv")
    df_variants.to_csv(out_path, index=False)

    print(f"Variantes salvas em: {out_path}")
    return out_path


def compute_top_variants(csv_path: str, top_n: int = 10):
    """Calcula Top-N variantes do processo e salva em TXT + CSV para tabela."""
    df = pd.read_csv(csv_path)

    required = ["case:concept:name", "concept:name", "time:timestamp"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(
            "CSV não contém as colunas obrigatórias: "
            + ", ".join(required)
            + f". Ausentes: {', '.join(missing)}"
        )

    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], utc=True, errors="coerce")
    df = df.dropna(subset=["time:timestamp"])
    df = df.sort_values(by=["case:concept:name", "time:timestamp"])

    sequences = df.groupby("case:concept:name")["concept:name"].apply(tuple)
    total_cases = sequences.shape[0]
    if total_cases == 0:
        raise RuntimeError("Não há casos no log para calcular variantes.")

    counts = sequences.value_counts()

    base_name = os.path.basename(csv_path)


    base, _ = os.path.splitext(base_name)
    out_txt_path = os.path.join(OUTPUT_DIR, base + "__variants_top.txt")
    out_csv_table = os.path.join(OUTPUT_DIR, base + "__variants_top_table.csv")

    linhas = []
    linhas.append(f"Arquivo de origem: {csv_path}")
    linhas.append("")
    linhas.append(f"Total de casos: {total_cases}")
    linhas.append(f"Total de variantes únicas: {counts.shape[0]}")
    linhas.append("")

    rows_table = []
    top_n_eff = min(top_n, len(counts))
    linhas.append(f"Top {top_n_eff} variantes:")

    for i, (variant, count) in enumerate(counts.head(top_n).items(), start=1):
        perc = (count / total_cases) * 100.0
        seq_str = " -> ".join(variant)
        linhas.append(f"{i:02d}. {count} casos ({perc:.1f}%) - {seq_str}")

        rows_table.append(
            {
                "rank": i,
                "num_cases": int(count),
                "perc": perc,
                "sequence": seq_str,
            }
        )

    text = "\n".join(linhas)

    with open(out_txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    df_tab = pd.DataFrame(rows_table)
    df_tab.to_csv(out_csv_table, index=False)

    print(text)
    print(f"Top variantes salvas em: {out_txt_path}")
    print(f"Tabela de Top variantes salva em: {out_csv_table}")
    return out_txt_path, text


def discover_inductive_petri(csv_path: str):
    """Descobre modelo de processo com Inductive Miner e salva Petri net em PNG e SVG."""
    _check_graphviz()
    event_log, df_pm = _csv_to_eventlog(csv_path)

    tree = inductive_miner.apply(event_log)
    net, im, fm = pt_converter.apply(tree)

    base_name = os.path.basename(csv_path)


    base, _ = os.path.splitext(base_name)
    out_path = os.path.join(OUTPUT_DIR, base + "__inductive_petri.png")

    gviz = pn_visualizer.apply(net, im, fm)

    gviz.graph_attr["rankdir"] = "TB"
    gviz.graph_attr["ratio"] = "compress"
    gviz.graph_attr["size"] = "8,11!"
    gviz.graph_attr["dpi"] = "200"
    gviz.graph_attr["fontname"] = "Arial"
    gviz.graph_attr["fontsize"] = "12"

    gviz.node_attr["fontname"] = "Arial"
    gviz.node_attr["fontsize"] = "12"

    gviz.edge_attr["fontname"] = "Arial"
    gviz.edge_attr["fontsize"] = "10"

    pn_visualizer.save(gviz, out_path)

    base_no_ext, _ = os.path.splitext(out_path)
    out_svg = base_no_ext + ".svg"
    pn_visualizer.save(gviz, out_svg)

    print(f"Modelo Inductive Miner salvo em: {out_path}")
    return out_path


def build_dfg_frequency(csv_path: str):
    """Gera DFG de frequência a partir do log e salva em PNG e SVG."""
    _check_graphviz()
    event_log, df_pm = _csv_to_eventlog(csv_path)

    dfg = dfg_discovery.apply(event_log)
    parameters = {dfg_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
    gviz = dfg_visualizer.apply(
        dfg,
        log=event_log,
        variant=dfg_visualizer.Variants.FREQUENCY,
        parameters=parameters,
    )

    gviz.graph_attr["rankdir"] = "TB"
    gviz.graph_attr["ratio"] = "compress"
    gviz.graph_attr["size"] = "8,11!"
    gviz.graph_attr["dpi"] = "200"
    gviz.graph_attr["fontname"] = "Arial"
    gviz.graph_attr["fontsize"] = "12"

    gviz.node_attr["fontname"] = "Arial"
    gviz.node_attr["fontsize"] = "12"

    gviz.edge_attr["fontname"] = "Arial"
    gviz.edge_attr["fontsize"] = "10"

    base_name = os.path.basename(csv_path)


    base, _ = os.path.splitext(base_name)
    out_path = os.path.join(OUTPUT_DIR, base + "__dfg_frequency.png")
    dfg_visualizer.save(gviz, out_path)

    base_no_ext, _ = os.path.splitext(out_path)
    out_svg = base_no_ext + ".svg"
    dfg_visualizer.save(gviz, out_svg)

    print(f"DFG (frequência) salvo em: {out_path}")
    return out_path


def compute_timeline_by_hour(csv_path: str):
    """
    Agrega o tempo total de atividade por hora do dia (0..23),
    usando 'time:timestamp' e 'duration'.
    Retorna (lista_horas, lista_valores_em_horas).
    """
    df = pd.read_csv(csv_path)
    df = _ensure_duration(df)

    if "time:timestamp" not in df.columns:
        hours = list(range(24))
        return hours, [0.0] * 24

    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], utc=True, errors="coerce")
    df = df.dropna(subset=["time:timestamp"])

    df["_hour"] = df["time:timestamp"].dt.hour
    grp = df.groupby("_hour")["duration"].sum()

    hours = list(range(24))
    values = []
    for h in hours:
        sec = float(grp.get(h, 0.0))
        values.append(sec / 3600.0)

    return hours, values


# ======================================================
# KPIs ESTRUTURADOS (para baseline)
# ======================================================

def compute_kpis_metrics_from_df(df: pd.DataFrame) -> dict:
    """Versão enxuta do compute_kpis que devolve apenas um dict de métricas."""
    df = _ensure_duration(df)

    metrics = {}

    metrics["num_events"] = len(df)
    metrics["num_cases"] = df["case:concept:name"].nunique() if "case:concept:name" in df.columns else 1

    avg_case_seconds = None
    total_case_seconds = None
    if "case:concept:name" in df.columns and "time:timestamp" in df.columns:
        df_sorted = df.sort_values(["case:concept:name", "time:timestamp"])
        grp_ts = df_sorted.groupby("case:concept:name")["time:timestamp"]
        start = grp_ts.min()
        end = grp_ts.max()
        case_durations = (end - start).dt.total_seconds()
        if len(case_durations) > 0:
            avg_case_seconds = float(case_durations.mean())
            total_case_seconds = float(case_durations.sum())

    metrics["avg_case_seconds"] = avg_case_seconds
    metrics["total_case_seconds"] = total_case_seconds

    if "case:concept:name" in df.columns and "concept:name" in df.columns:
        df_seq = df.sort_values(["case:concept:name", "time:timestamp"])
        sequences = df_seq.groupby("case:concept:name")["concept:name"].apply(tuple)
        if len(sequences) > 0:
            counts = sequences.value_counts()
            metrics["total_unique_variants"] = counts.shape[0]
            top_count = counts.iloc[0]
            metrics["adherence_percent"] = (top_count / len(sequences)) * 100.0
        else:
            metrics["total_unique_variants"] = None
            metrics["adherence_percent"] = None
    else:
        metrics["total_unique_variants"] = None
        metrics["adherence_percent"] = None

    return metrics


def save_baseline(csv_path: str, baseline_path: str = None) -> str:
    """
    Salva um 'padrão' (baseline) a partir de um CSV:
    - modelo Inductive (net, im, fm)
    - KPIs da época
    """
    event_log, df_pm = _csv_to_eventlog(csv_path)

    tree = inductive_miner.apply(event_log)
    net, im, fm = pt_converter.apply(tree)

    kpis = compute_kpis_metrics_from_df(df_pm)

    baseline = {
        "created_at": datetime.datetime.now().isoformat(),
        "source_csv": os.path.abspath(csv_path),
        "net": net,
        "im": im,
        "fm": fm,
        "kpis": kpis,
    }

    if baseline_path is None:
        base_name = os.path.basename(csv_path)

        base, _ = os.path.splitext(base_name)
        baseline_path = os.path.join(OUTPUT_DIR, base + "__baseline.pkl")

    with open(baseline_path, "wb") as f:
        pickle.dump(baseline, f)

    print(f"Baseline salvo em: {baseline_path}")
    return baseline_path


def conformance_against_baseline(csv_sample_path: str, baseline_path: str) -> dict:
    """
    Compara um CSV de amostra contra o modelo do baseline via fitness de alinhamento.
    """
    with open(baseline_path, "rb") as f:
        baseline = pickle.load(f)
    net, im, fm = baseline["net"], baseline["im"], baseline["fm"]

    event_log, df_pm = _csv_to_eventlog(csv_sample_path)

    fitness = replay_fitness_alignment.apply(event_log, net, im, fm)

    perc_fit = fitness.get("percFitTraces") or fitness.get("percentage_of_fitting_traces")
    avg_fit = fitness.get("average_trace_fitness") or fitness.get("averageFitness")
    log_fit = fitness.get("log_fitness") or avg_fit

    return {
        "log_fitness": log_fit,
        "perc_fit_traces": perc_fit,
        "average_trace_fitness": avg_fit,
        "num_traces": len(event_log),
        "raw": fitness,
    }


def compare_kpis_against_baseline(csv_sample_path: str, baseline_path: str) -> dict:
    """
    Compara KPIs do baseline com KPIs da amostra e indica quais métricas melhoraram.
    """
    with open(baseline_path, "rb") as f:
        baseline = pickle.load(f)
    base_kpis = baseline["kpis"]

    event_log, df_pm = _csv_to_eventlog(csv_sample_path)
    sample_kpis = compute_kpis_metrics_from_df(df_pm)

    directions = {
        "avg_case_seconds": "lower_better",
        "total_case_seconds": "lower_better",
        "total_unique_variants": "lower_better",
        "adherence_percent": "higher_better",
    }

    comparacao = []
    for name, direction in directions.items():
        base_val = base_kpis.get(name)
        new_val = sample_kpis.get(name)
        if base_val is None or new_val is None:
            continue

        delta = new_val - base_val
        if direction == "lower_better":
            improved = new_val < base_val
        elif direction == "higher_better":
            improved = new_val > base_val
        else:
            improved = None

        comparacao.append(
            {
                "metric": name,
                "baseline": base_val,
                "sample": new_val,
                "delta": delta,
                "improved": improved,
            }
        )

    return {
        "baseline_kpis": base_kpis,
        "sample_kpis": sample_kpis,
        "comparison": comparacao,
    }

def generate_baseline_comparison_pdf(csv_sample_path: str, baseline_path: str, meta=None) -> str:
    """
    Gera um PDF de comparação entre baseline e amostra, com:
    - Conformance (fitness)
    - Tabela de KPIs baseline x amostra
    - Gráficos de barras comparativos
    """
    if meta is None:
        meta = {}

    # Imports do reportlab (locais para não quebrar o resto se faltar lib)
    try:
        import reportlab
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.pdfgen import canvas
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics.charts.barcharts import VerticalBarChart
        from reportlab.graphics import renderPDF
        from reportlab.platypus import Table, TableStyle
        from reportlab.lib import colors
        print("reportlab (baseline comparison) carregado de:", reportlab.__file__)
    except ImportError as e:
        raise RuntimeError(
            "Biblioteca 'reportlab' não encontrada neste ambiente Python.\n"
            "Instale com: pip install reportlab\n\n"
            f"Detalhe técnico: {e}"
        )

    # ------------------------------------------------------------------
    # Dados de comparação (já usando suas funções existentes)
    # ------------------------------------------------------------------
    conf = conformance_against_baseline(csv_sample_path, baseline_path)
    comp = compare_kpis_against_baseline(csv_sample_path, baseline_path)

    base_kpis = comp["baseline_kpis"]
    sample_kpis = comp["sample_kpis"]
    comparison = comp["comparison"]

    # Nomes bonitinhos para as métricas
    metric_labels = {
        "avg_case_seconds": "Tempo médio por caso (s)",
        "total_case_seconds": "Tempo total (s)",
        "total_unique_variants": "Total de variantes",
        "adherence_percent": "Aderência ao processo padrão (%)",
    }

    def fmt_num(v, decimals=2):
        if v is None:
            return "n/d"
        return f"{v:.{decimals}f}"

    # ------------------------------------------------------------------
    # Criação do PDF
    # ------------------------------------------------------------------
    base, _ = os.path.splitext(csv_sample_path)
    pdf_path = os.path.join(OUTPUT_DIR, base + "__baseline_comparison.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    margin_x = 2 * cm
    margin_y = 2 * cm

    def draw_multiline(text: str, x: float, y: float, max_chars: int = 95, leading: float = 14):
        if not text:
            return y
        lines = []
        for paragraph in text.splitlines():
            if not paragraph.strip():
                lines.append("")
                continue
            wrapped = textwrap.wrap(paragraph, max_chars)
            if not wrapped:
                lines.append("")
            else:
                lines.extend(wrapped)
        text_obj = c.beginText(x, y)
        text_obj.setLeading(leading)
        for line in lines:
            if y < margin_y:
                c.drawText(text_obj)
                c.showPage()
                text_obj = c.beginText(x, height - margin_y)
                text_obj.setLeading(leading)
                y = height - margin_y
            text_obj.textLine(line)
            y -= leading
        c.drawText(text_obj)
        return y

    process_name = meta.get("process_name", "Processo monitorado")
    cliente = meta.get("cliente", "[Cliente]")
    area = meta.get("area", "[Área/Setor]")
    responsavel = meta.get("responsavel", "[Consultor responsável]")
    periodo = meta.get("periodo", "[Período analisado]")
    data_analise = meta.get("data_analise", datetime.date.today().strftime("%d/%m/%Y"))

    # ----------------- CAPA -----------------
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin_x, height - margin_y - 20, "Baseline Comparison – SENAI TASK MINING")
    c.setFont("Helvetica", 11)
    y = height - margin_y - 50

    infos = [
        f"Processo: {process_name}",
        f"Cliente: {cliente}",
        f"Área/Setor: {area}",
        f"Data da análise: {data_analise}",
        f"Responsável: {responsavel}",
        f"Período analisado: {periodo}",
        f"Arquivo baseline: {os.path.basename(baseline_path)}",
        f"Arquivo amostra:  {os.path.basename(csv_sample_path)}",
    ]
    for line in infos:
        c.drawString(margin_x, y, line)
        y -= 14

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "1. Conformance (fitness)")
    y -= 20

    c.setFont("Helvetica", 11)
    conf_txt = (
        f"Fitness médio (log_fitness / average): {conf.get('log_fitness')}\n"
        f"% de traços aderentes (percFitTraces): {conf.get('perc_fit_traces')}\n"
        f"Nº de traços na amostra: {conf.get('num_traces')}"
    )
    y = draw_multiline(conf_txt, margin_x, y)

    # ----------------- PÁGINA 2: TABELA DE KPIs -----------------
    c.showPage()
    y = height - margin_y

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "2. Comparação de KPIs (baseline x amostra)")
    y -= 20

    data_tbl = [["Métrica", "Baseline", "Amostra", "Δ", "Status"]]
    row_styles = []

    for idx, item in enumerate(comparison, start=1):
        metric = item["metric"]
        base_val = item["baseline"]
        new_val = item["sample"]
        delta = item["delta"]
        improved = item["improved"]

        label = metric_labels.get(metric, metric)

        if metric.endswith("_seconds"):
            base_str = fmt_num(base_val, 1)
            new_str = fmt_num(new_val, 1)
            delta_str = fmt_num(delta, 1)
        else:
            base_str = fmt_num(base_val, 2)
            new_str = fmt_num(new_val, 2)
            delta_str = fmt_num(delta, 2)

        if improved is True:
            status = "MELHOROU"
            color = colors.green
        elif improved is False:
            status = "PIOROU"
            color = colors.red
        else:
            status = "N/A"
            color = colors.black

        data_tbl.append([label, base_str, new_str, delta_str, status])
        row_styles.append(("TEXTCOLOR", (0, idx), (-1, idx), color))

    table = Table(
        data_tbl,
        colWidths=[
            (width - 2 * margin_x) * 0.36,
            (width - 2 * margin_x) * 0.16,
            (width - 2 * margin_x) * 0.16,
            (width - 2 * margin_x) * 0.16,
            (width - 2 * margin_x) * 0.16,
        ],
    )

    base_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 1), (-2, -1), "CENTER"),
    ]
    table.setStyle(TableStyle(base_style + row_styles))

    w, h = table.wrapOn(c, width - 2 * margin_x, y - margin_y)
    table.drawOn(c, margin_x, y - h)
    y = y - h - 20

    # ----------------- PÁGINA 3: GRÁFICOS DE TEMPO -----------------
    c.showPage()
    y = height - margin_y

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "3. Gráficos comparativos de tempo")
    y -= 20

    # Tempo médio e total (segundos)
    dur_metrics = ["avg_case_seconds", "total_case_seconds"]
    dur_labels = [metric_labels[m] for m in dur_metrics if m in metric_labels]
    base_dur = []
    sample_dur = []
    for m in dur_metrics:
        base_dur.append(base_kpis.get(m) or 0.0)
        sample_dur.append(sample_kpis.get(m) or 0.0)

    chart_height = 7 * cm
    chart_width = width - 2 * margin_x

    drawing = Drawing(chart_width, chart_height)
    bc = VerticalBarChart()
    bc.x = 40
    bc.y = 40
    bc.height = chart_height - 60
    bc.width = chart_width - 80
    bc.data = [base_dur, sample_dur]
    bc.categoryAxis.categoryNames = dur_labels
    bc.categoryAxis.labels.boxAnchor = "ne"
    bc.categoryAxis.labels.angle = 45
    bc.categoryAxis.labels.dy = -15
    bc.valueAxis.valueMin = 0
    max_val = max(base_dur + sample_dur) if (base_dur + sample_dur) else 1
    bc.valueAxis.valueMax = max_val * 1.1 if max_val > 0 else 1
    bc.valueAxis.valueStep = bc.valueAxis.valueMax / 4 if bc.valueAxis.valueMax > 0 else 1

    drawing.add(bc)
    renderPDF.draw(drawing, c, margin_x, y - chart_height)
    y = y - chart_height - 20

    c.setFont("Helvetica", 9)
    y = draw_multiline(
        "Gráfico 1: comparação de tempo médio por caso e tempo total (em segundos) "
        "entre o baseline e a amostra.",
        margin_x,
        y,
        max_chars=100,
        leading=11,
    )

    # ----------------- PÁGINA 4: VARIANTES E ADERÊNCIA -----------------
    c.showPage()
    y = height - margin_y

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "4. Variantes e aderência ao processo padrão")
    y -= 20

    var_metrics = ["total_unique_variants", "adherence_percent"]
    var_labels = [metric_labels[m] for m in var_metrics if m in metric_labels]
    base_var = []
    sample_var = []
    for m in var_metrics:
        base_var.append(base_kpis.get(m) or 0.0)
        sample_var.append(sample_kpis.get(m) or 0.0)

    drawing2 = Drawing(chart_width, chart_height)
    bc2 = VerticalBarChart()
    bc2.x = 40
    bc2.y = 40
    bc2.height = chart_height - 60
    bc2.width = chart_width - 80
    bc2.data = [base_var, sample_var]
    bc2.categoryAxis.categoryNames = var_labels
    bc2.categoryAxis.labels.boxAnchor = "ne"
    bc2.categoryAxis.labels.angle = 45
    bc2.categoryAxis.labels.dy = -15
    bc2.valueAxis.valueMin = 0
    max_val2 = max(base_var + sample_var) if (base_var + sample_var) else 1
    bc2.valueAxis.valueMax = max_val2 * 1.1 if max_val2 > 0 else 1
    bc2.valueAxis.valueStep = bc2.valueAxis.valueMax / 4 if bc2.valueAxis.valueMax > 0 else 1

    drawing2.add(bc2)
    renderPDF.draw(drawing2, c, margin_x, y - chart_height)
    y = y - chart_height - 20

    c.setFont("Helvetica", 9)
    y = draw_multiline(
        "Gráfico 2: comparação do total de variantes e do percentual de aderência ao processo padrão "
        "entre o baseline e a amostra.",
        margin_x,
        y,
        max_chars=100,
        leading=11,
    )

    # ----------------- RODAPÉ -----------------
    c.showPage()
    y = height - margin_y
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        margin_x,
        y,
        "Relatório automático de comparação de baseline gerado pelo SENAI TASK MINING.",
    )

    c.save()
    print(f"Baseline Comparison PDF gerado em: {pdf_path}")
    return pdf_path


# ======================================================
# PROCESS DESCRIPTION DOCUMENT (PDF)
# ======================================================

def generate_pdd(csv_path: str, meta=None) -> str:
    """
    Gera um Process Description Document em PDF na mesma pasta do CSV, usando:
    - KPIs
    - Variantes (todas e Top)
    - DFG (frequência)
    - Modelo Inductive
    - Timeline por hora
    """
    if meta is None:
        meta = {}

    try:
        import reportlab
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.pdfgen import canvas
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics.charts.barcharts import VerticalBarChart
        from reportlab.graphics import renderPDF
        from reportlab.platypus import Table, TableStyle
        from reportlab.lib import colors
        print("reportlab carregado de:", reportlab.__file__)
    except ImportError as e:
        raise RuntimeError(
            "Biblioteca 'reportlab' não encontrada neste ambiente Python.\n"
            "Verifique se você instalou dentro do mesmo venv usado para rodar o pm_analysis_gui.\n\n"
            f"Detalhe técnico: {e}"
        )

    resumo_path, top_ativ_path = compute_kpis(csv_path)
    variants_all_path = compute_variants(csv_path)
    variants_top_path, variants_text = compute_top_variants(csv_path)
    dfg_path = build_dfg_frequency(csv_path)
    inductive_path = discover_inductive_petri(csv_path)
    hours_tl, values_tl = compute_timeline_by_hour(csv_path)

    base_name = os.path.basename(csv_path)


    base, _ = os.path.splitext(base_name)
    variants_table_path = os.path.join(OUTPUT_DIR, base + "__variants_top_table.csv")
    apps_cat_path = os.path.join(OUTPUT_DIR, base + "__apps_categories.csv")

    with open(resumo_path, "r", encoding="utf-8") as f:
        kpis_text = f.read()

    df_top_ativ = None
    if os.path.isfile(top_ativ_path):
        df_top_ativ = pd.read_csv(top_ativ_path)

    df_top_variants = None
    if os.path.isfile(variants_table_path):
        df_top_variants = pd.read_csv(variants_table_path)

    df_apps_cat = None
    if os.path.isfile(apps_cat_path):
        df_apps_cat = pd.read_csv(apps_cat_path)

    pdf_path = os.path.join(OUTPUT_DIR, base + "__process_description_document.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    from reportlab.lib.units import cm as _cm
    margin_x = 2 * _cm
    margin_y = 2 * _cm

    def draw_multiline(text: str, x: float, y: float, max_chars: int = 95, leading: float = 14):
        if not text:
            return y
        lines = []
        for paragraph in text.splitlines():
            if not paragraph.strip():
                lines.append("")
                continue
            wrapped = textwrap.wrap(paragraph, max_chars)
            if not wrapped:
                lines.append("")
            else:
                lines.extend(wrapped)
        text_obj = c.beginText(x, y)
        text_obj.setLeading(leading)
        for line in lines:
            if y < margin_y:
                c.drawText(text_obj)
                c.showPage()
                text_obj = c.beginText(x, height - margin_y)
                text_obj.setLeading(leading)
                y = height - margin_y
            text_obj.textLine(line)
            y -= leading
        c.drawText(text_obj)
        return y

    process_name = meta.get("process_name", "Processo monitorado")
    cliente = meta.get("cliente", "[Cliente]")
    area = meta.get("area", "[Área/Setor]")
    responsavel = meta.get("responsavel", "[Consultor responsável]")
    periodo = meta.get("periodo", "[Período analisado]")
    data_analise = meta.get("data_analise", datetime.date.today().strftime("%d/%m/%Y"))
    csv_filename = os.path.basename(csv_path)

    logo_path = meta.get("logo_path", "logo_senai_task_mining.png")
    if os.path.isfile(logo_path):
        try:
            logo_w = 4 * _cm
            logo_h = 4 * _cm
            c.drawImage(
                logo_path,
                margin_x,
                height - margin_y - logo_h,
                width=logo_w,
                height=logo_h,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass

    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin_x, height - margin_y - 5.5 * _cm, f"Process Description Document – {process_name}")

    c.setFont("Helvetica", 11)
    y = height - margin_y - 5.5 * _cm - 25

    info_lines = [
        f"Cliente: {cliente}",
        f"Área/Setor: {area}",
        f"Data da análise: {data_analise}",
        f"Responsável: {responsavel}",
        f"Período analisado: {periodo}",
        f"Arquivo de origem: {csv_filename}",
    ]
    for line in info_lines:
        c.drawString(margin_x, y, line)
        y -= 14

    y -= 10

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "1. Objetivo")
    y -= 18

    c.setFont("Helvetica", 11)
    objetivo_txt = (
        "Descrever o processo tal como executado no ambiente digital, com base em dados capturados "
        "automaticamente pelo SENAI TASK MINING (ActivityWatch + PM4Py), identificando o processo padrão "
        "(baseline), variantes, desvios e oportunidades de melhoria e automação."
    )
    y = draw_multiline(objetivo_txt, margin_x, y)

    y -= 6
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "2. Escopo")
    y -= 18

    c.setFont("Helvetica", 11)
    escopo_txt = (
        "Este Process Description Document considera apenas as interações digitais capturadas durante o período informado, "
        "relacionadas ao processo monitorado. Atividades claramente pessoais (entretenimento, redes sociais, "
        "notícias) podem ter sido filtradas ou classificadas como ruído, conforme configuração do ETL."
    )
    y = draw_multiline(escopo_txt, margin_x, y)

    c.showPage()
    y = height - margin_y

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "3. Fonte de dados e método")
    y -= 18

    c.setFont("Helvetica", 11)
    metodo_txt = (
        "Os dados foram coletados por meio do ActivityWatch (aw-watcher-uia e watchers associados) e "
        "convertidos para um event log no padrão PM4Py através de script ETL. O arquivo CSV resultante foi "
        "processado pelo módulo 'SENAI TASK MINING – Análises', que gera KPIs, variantes, DFG (Directly-Follows "
        "Graph) e modelo de processo via Inductive Miner."
    )
    y = draw_multiline(metodo_txt, margin_x, y)

    y -= 6
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "4. KPIs do processo")
    y -= 18

    c.setFont("Helvetica", 11)
    y = draw_multiline(kpis_text, margin_x, y)

    c.showPage()
    y = height - margin_y

    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics import renderPDF

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "5. Top variantes e processo padrão (baseline)")
    y -= 20

    if df_top_variants is not None and not df_top_variants.empty:
        data = [["#", "Casos", "%", "Sequência (início)"]]
        for _, row in df_top_variants.head(10).iterrows():
            seq = row["sequence"]
            if len(seq) > 70:
                seq = seq[:67] + "..."
            data.append(
                [
                    int(row["rank"]),
                    int(row["num_cases"]),
                    f"{row['perc']:.1f}",
                    seq,
                ]
            )
        table = Table(
            data,
            colWidths=[1.2 * _cm, 2 * _cm, 2 * _cm, (width - 2 * margin_x) - 5.2 * _cm],
        )
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("ALIGN", (0, 0), (2, -1), "CENTER"),
                ]
            )
        )
        w, h = table.wrapOn(c, width - 2 * margin_x, y - margin_y)
        table.drawOn(c, margin_x, y - h)
        y = y - h - 20
    else:
        c.setFont("Helvetica", 11)
        y = draw_multiline("Não foi possível montar a tabela de Top variantes.", margin_x, y)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "6. Top atividades por tempo acumulado")
    y -= 20

    if df_top_ativ is not None and not df_top_ativ.empty:
        data = [["Atividade", "Tempo total (min)", "Eventos"]]
        for _, row in df_top_ativ.head(10).iterrows():
            data.append(
                [
                    str(row["concept:name"]),
                    f"{row['tempo_total_min']:.1f}",
                    int(row["num_eventos"]),
                ]
            )
        table = Table(
            data,
            colWidths=[
                (width - 2 * margin_x) * 0.6,
                (width - 2 * margin_x) * 0.2,
                (width - 2 * margin_x) * 0.2,
            ],
        )
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                ]
            )
        )
        w, h = table.wrapOn(c, width - 2 * margin_x, y - margin_y)
        table.drawOn(c, margin_x, y - h)
        y = y - h - 20
    else:
        c.setFont("Helvetica", 11)
        y = draw_multiline("Não foi possível montar a tabela de Top atividades.", margin_x, y)

    c.showPage()
    y = height - margin_y

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "7. Uso por tipo de aplicação (Business / Pessoal / Outros)")
    y -= 20

    if df_apps_cat is not None and not df_apps_cat.empty:
        cols = ["app_category", "tempo_total_min", "perc_tempo", "num_eventos", "num_apps"]
        for col in cols:
            if col not in df_apps_cat.columns:
                df_apps_cat[col] = 0
        data = [["Categoria", "Tempo (min)", "% do tempo", "Eventos", "Apps distintos"]]
        for _, row in df_apps_cat.iterrows():
            data.append(
                [
                    str(row["app_category"]),
                    f"{row['tempo_total_min']:.1f}",
                    f"{row['perc_tempo']:.1f}",
                    int(row["num_eventos"]),
                    int(row["num_apps"]),
                ]
            )
        table = Table(
            data,
            colWidths=[
                (width - 2 * margin_x) * 0.28,
                (width - 2 * margin_x) * 0.18,
                (width - 2 * margin_x) * 0.18,
                (width - 2 * margin_x) * 0.18,
                (width - 2 * margin_x) * 0.18,
            ],
        )
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ]
            )
        )
        w, h = table.wrapOn(c, width - 2 * margin_x, y - margin_y)
        table.drawOn(c, margin_x, y - h)
        y = y - h - 20
    else:
        c.setFont("Helvetica", 11)
        y = draw_multiline("Não foi possível montar a tabela de categorias de aplicação.", margin_x, y)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "8. Timeline de utilização (por hora do dia)")
    y -= 20

    total_tl = sum(values_tl)
    if total_tl <= 0:
        c.setFont("Helvetica", 11)
        y = draw_multiline("Não foi possível calcular a timeline (sem timestamps ou durações válidas).", margin_x, y)
    else:
        c.setFont("Helvetica", 10)
        y = draw_multiline(
            "Gráfico de barras mostrando o total de horas de atividade por hora do dia (0–23h), "
            "considerando todos os eventos do período analisado.",
            margin_x,
            y,
        )
        chart_height = 7 * _cm
        chart_width = width - 2 * margin_x

        drawing = Drawing(chart_width, chart_height)
        bc = VerticalBarChart()
        bc.x = 30
        bc.y = 30
        bc.height = chart_height - 40
        bc.width = chart_width - 60
        bc.data = [values_tl]
        bc.categoryAxis.categoryNames = [str(h) for h in hours_tl]
        bc.valueAxis.valueMin = 0
        max_v = max(values_tl)
        bc.valueAxis.valueMax = max_v * 1.1 if max_v > 0 else 1
        bc.valueAxis.valueStep = bc.valueAxis.valueMax / 4 if bc.valueAxis.valueMax > 0 else 1

        drawing.add(bc)
        renderPDF.draw(drawing, c, margin_x, y - chart_height)
        y = y - chart_height - 10

    c.showPage()
    y = height - margin_y

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "9. Análise de desvios e oportunidades (para preenchimento)")
    y -= 18

    c.setFont("Helvetica", 11)
    bloco_rec = (
        "Esta seção pode ser complementada manualmente pelo consultor SENAI, com base na análise dos gráficos, "
        "das variantes e dos tempos coletados. Sugestão de tópicos:\n"
        "- Desvios relevantes em relação ao processo padrão (baseline);\n"
        "- Desperdícios digitais (motion, waiting, overprocessing);\n"
        "- Diferenças de execução entre usuários ou turnos;\n"
        "- Oportunidades de padronização, treinamento e automação/RPA."
    )
    y = draw_multiline(bloco_rec, margin_x, y)

    y -= 20
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        margin_x,
        y,
        "Documento gerado automaticamente pelo SENAI TASK MINING – Process Description Document (ActivityWatch + PM4Py).",
    )

    c.save()
    print(f"Process Description Document gerado em: {pdf_path}")
    return pdf_path


# ======================================================
# GUI (Tkinter)
# ======================================================

class AnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SENAI TASK MINING - Análises")
        
        # ===== DEBUG: VERIFICAR CAMINHOS DO ÍCONE =====
        print("\n" + "="*70)
        print("DEBUG - Configuração do ícone:")
        print("="*70)
        print(f"RESOURCE_DIR: {RESOURCE_DIR}")
        print(f"RESOURCE_DIR existe? {RESOURCE_DIR.exists()}")
        
        ico1 = RESOURCE_DIR / "assets" / "senai.ico"
        print(f"\nCaminho 1: {ico1}")
        print(f"Existe? {ico1.exists()}")
        
        ico2 = RESOURCE_DIR / "senai.ico"
        print(f"\nCaminho 2: {ico2}")
        print(f"Existe? {ico2.exists()}")
        
        # Listar arquivos no RESOURCE_DIR
        if RESOURCE_DIR.exists():
            print(f"\nArquivos em {RESOURCE_DIR}:")
            try:
                for item in RESOURCE_DIR.iterdir():
                    print(f"  - {item.name}")
            except Exception as e:
                print(f"  Erro ao listar: {e}")
        
        # Verificar se há pasta assets
        assets_dir = RESOURCE_DIR / "assets"
        if assets_dir.exists():
            print(f"\nArquivos em {assets_dir}:")
            try:
                for item in assets_dir.iterdir():
                    print(f"  - {item.name}")
            except Exception as e:
                print(f"  Erro ao listar: {e}")
        
        print("="*70 + "\n")
        # ===== FIM DEBUG =====
        
        # Configurar ícone
        ico = RESOURCE_DIR / "assets" / "senai.ico"
        if not ico.exists():
            ico = RESOURCE_DIR / "senai.ico"
        if ico.exists():
            try:
                self.iconbitmap(str(ico))
            except Exception:
                pass
        
        self.geometry("760x480")
        self.csv_path_var = tk.StringVar()
        self.cliente_var = tk.StringVar()
        self.area_var = tk.StringVar()
        self.data_analise_var = tk.StringVar(value=datetime.date.today().strftime("%d/%m/%Y"))
        self.responsavel_var = tk.StringVar()
        self.periodo_var = tk.StringVar()
        self._build_widgets()

    def _build_widgets(self):
        frm = tk.Frame(self, padx=10, pady=10)
        frm.pack(fill="both", expand=True)

        lbl = tk.Label(frm, text="Arquivo CSV de log (event_log_COMBINED_...csv):")
        lbl.grid(row=0, column=0, columnspan=2, sticky="w")

        ent = tk.Entry(frm, textvariable=self.csv_path_var, width=80)
        ent.grid(row=1, column=0, sticky="we", pady=5)

        btn_browse = tk.Button(frm, text="Procurar...", command=self._on_browse)
        btn_browse.grid(row=1, column=1, padx=5)

        tk.Label(frm, text="Cliente:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        tk.Entry(frm, textvariable=self.cliente_var, width=50).grid(row=2, column=1, sticky="we", pady=(10, 0))

        tk.Label(frm, text="Área/Setor:").grid(row=3, column=0, sticky="w")
        tk.Entry(frm, textvariable=self.area_var, width=50).grid(row=3, column=1, sticky="we")

        tk.Label(frm, text="Data da análise:").grid(row=4, column=0, sticky="w")
        tk.Entry(frm, textvariable=self.data_analise_var, width=20).grid(row=4, column=1, sticky="w")

        tk.Label(frm, text="Responsável:").grid(row=5, column=0, sticky="w")
        tk.Entry(frm, textvariable=self.responsavel_var, width=50).grid(row=5, column=1, sticky="we")

        tk.Label(frm, text="Período analisado:").grid(row=6, column=0, sticky="w")
        tk.Entry(frm, textvariable=self.periodo_var, width=50).grid(row=6, column=1, sticky="we")

        frm.grid_columnconfigure(0, weight=1)
        frm.grid_columnconfigure(1, weight=1)

        btn_kpis = tk.Button(
            frm,
            text="Gerar KPIs / Top atividades",
            command=self._on_kpis,
            width=35,
        )
        btn_kpis.grid(row=7, column=0, sticky="w", pady=5)

        btn_variants_top = tk.Button(
            frm,
            text="Gerar Variantes (Top)",
            command=self._on_variants_top,
            width=35,
        )
        btn_variants_top.grid(row=8, column=0, sticky="w", pady=5)

        btn_variants = tk.Button(
            frm,
            text="Gerar Variantes (todas)",
            command=self._on_variants,
            width=35,
        )
        btn_variants.grid(row=9, column=0, sticky="w", pady=5)

        btn_pdd = tk.Button(
            frm,
            text="Gerar Process Description Document (PDF)",
            command=self._on_pdd,
            width=35,
        )
        btn_pdd.grid(row=10, column=0, sticky="w", pady=5)

        btn_inductive = tk.Button(
            frm,
            text="Descobrir modelo (Inductive Miner)",
            command=self._on_inductive,
            width=35,
        )
        btn_inductive.grid(row=7, column=1, sticky="w", pady=5)

        btn_dfg = tk.Button(
            frm,
            text="Gerar DFG (frequência)",
            command=self._on_dfg,
            width=35,
        )
        btn_dfg.grid(row=8, column=1, sticky="w", pady=5)

        btn_save_baseline = tk.Button(
            frm,
            text="Salvar padrão (baseline)",
            command=self._on_save_baseline,
            width=35,
        )
        btn_save_baseline.grid(row=9, column=1, sticky="w", pady=5)

        btn_compare_baseline = tk.Button(
            frm,
            text="Comparar com padrão (baseline)",
            command=self._on_compare_baseline,
            width=35,
        )
        btn_compare_baseline.grid(row=10, column=1, sticky="w", pady=5)

        lbl_hint = tk.Label(
            frm,
            text=(
                "1) Use o SENAI TASK MINING - Gravador para exportar o CSV.\n"
                "2) Selecione o CSV, preencha os metadados e utilize os botões de análise.\n"
                "3) Para baseline: salve o padrão e depois compare uma amostra com ele."
            ),
            fg="gray",
        )
        lbl_hint.grid(row=11, column=0, columnspan=2, sticky="w", pady=15)

    def _on_browse(self):
        path = filedialog.askopenfilename(
            title="Selecione o CSV de log",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if path:
            self.csv_path_var.set(path)

    def _get_csv_path(self) -> str:
        path = self.csv_path_var.get().strip()
        if not path:
            raise RuntimeError("Nenhum arquivo CSV selecionado.")
        if not os.path.isfile(path):
            raise RuntimeError(f"Arquivo não encontrado: {path}")
        return path

    def _on_kpis(self):
        try:
            csv_path = self._get_csv_path()
            resumo_path, top_ativ_path = compute_kpis(csv_path)

            with open(resumo_path, "r", encoding="utf-8") as f:
                conteudo = f.read()

            win = tk.Toplevel(self)
            win.title("KPIs do processo")
            win.geometry("700x500")
            
            # Configurar ícone
            ico = RESOURCE_DIR / "assets" / "senai.ico"
            if not ico.exists():
                ico = RESOURCE_DIR / "senai.ico"
            if ico.exists():
                try:
                    win.iconbitmap(str(ico))
                except Exception:
                    pass
            
            txt = tk.Text(win, wrap="word")

            messagebox.showinfo(
                "KPIs gerados",
                f"KPIs e Top atividades gerados com sucesso.\n"
                f"Os arquivos foram salvos em:\n{resumo_path}",
            )
        except Exception as e:
            messagebox.showerror("Erro ao gerar KPIs", str(e))

    def _on_variants(self):
        try:
            csv_path = self._get_csv_path()
            out_path = compute_variants(csv_path)
            messagebox.showinfo(
                "Variantes geradas",
                f"Arquivo de variantes salvo em:\n{out_path}",
            )
        except Exception as e:
            messagebox.showerror("Erro ao gerar variantes", str(e))

    def _on_variants_top(self):
        try:
            csv_path = self._get_csv_path()
            out_path, text = compute_top_variants(csv_path)

            win = tk.Toplevel(self)
            win.title("Top variantes do processo")
            win.geometry("900x500")
            
            # Configurar ícone
            ico = RESOURCE_DIR / "assets" / "senai.ico"
            if not ico.exists():
                ico = RESOURCE_DIR / "senai.ico"
            if ico.exists():
                try:
                    win.iconbitmap(str(ico))
                except Exception:
                    pass
            
            txt = tk.Text(win, wrap="word")

            messagebox.showinfo(
                "Variantes (Top) geradas",
                f"Top variantes salvas em:\n{out_path}",
            )
        except Exception as e:
            messagebox.showerror("Erro ao gerar Variantes (Top)", str(e))

    def _on_inductive(self):
        try:
            csv_path = self._get_csv_path()
            out_path = discover_inductive_petri(csv_path)
            messagebox.showinfo(
                "Inductive Miner",
                f"Modelo de processo (Petri net) salvo em:\n{out_path}",
            )
        except Exception as e:
            messagebox.showerror("Erro em Inductive Miner", str(e))

    def _on_dfg(self):
        try:
            csv_path = self._get_csv_path()
            out_path = build_dfg_frequency(csv_path)
            messagebox.showinfo(
                "DFG gerado",
                f"DFG de frequência salvo em:\n{out_path}",
            )
        except Exception as e:
            messagebox.showerror("Erro ao gerar DFG", str(e))

    def _on_pdd(self):
        try:
            csv_path = self._get_csv_path()

            meta = {
                "process_name": "Processo monitorado",
                "cliente": self.cliente_var.get() or "[Cliente]",
                "area": self.area_var.get() or "[Área/Setor]",
                "responsavel": self.responsavel_var.get() or "[Consultor SENAI]",
                "periodo": self.periodo_var.get() or "[Período analisado]",
                "data_analise": self.data_analise_var.get() or datetime.date.today().strftime("%d/%m/%Y"),
                "logo_path": "logo_senai_task_mining.png",
            }

            pdf_path = generate_pdd(csv_path, meta=meta)
            messagebox.showinfo(
                "Process Description Document gerado",
                f"Process Description Document salvo em:\n{pdf_path}",
            )
        except Exception as e:
            messagebox.showerror("Erro ao gerar Process Description Document", str(e))

    def _on_save_baseline(self):
        try:
            csv_path = self._get_csv_path()
            baseline_path = save_baseline(csv_path)
            messagebox.showinfo(
                "Baseline salva",
                f"Padrão (baseline) salvo em:\n{baseline_path}",
            )
        except Exception as e:
            messagebox.showerror("Erro ao salvar baseline", str(e))

    def _on_compare_baseline(self):
        try:
            csv_path = self._get_csv_path()
            baseline_path = filedialog.askopenfilename(
                title="Selecione o arquivo de baseline (.pkl)",
                filetypes=[("Baseline files", "*.pkl"), ("Todos os arquivos", "*.*")],
            )
            if not baseline_path:
                return

            meta = {
                "process_name": "Processo monitorado",
                "cliente": self.cliente_var.get() or "[Cliente]",
                "area": self.area_var.get() or "[Área/Setor]",
                "responsavel": self.responsavel_var.get() or "[Consultor SENAI]",
                "periodo": self.periodo_var.get() or "[Período analisado]",
                "data_analise": self.data_analise_var.get() or datetime.date.today().strftime("%d/%m/%Y"),
            }

            pdf_path = generate_baseline_comparison_pdf(csv_path, baseline_path, meta=meta)

            messagebox.showinfo(
                "Comparação com padrão (baseline)",
                f"PDF de comparação gerado em:\n{pdf_path}",
            )

        except Exception as e:
            messagebox.showerror("Erro ao comparar com baseline", str(e))



def main():
    app = AnalysisApp()
    app.mainloop()


if __name__ == "__main__":
    main()

