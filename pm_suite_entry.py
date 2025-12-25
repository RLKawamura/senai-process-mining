# -*- coding: utf-8 -*-
"""
SENAI - Mineração de Processos: Mapeamento Digital de Rotinas de Trabalho
Launcher para Workbench e Analysis
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import subprocess
import importlib.util

def get_base_path():
    """Retorna o diretório base do executável ou script"""
    if getattr(sys, 'frozen', False):
        # Executável PyInstaller
        base = sys._MEIPASS
    else:
        # Desenvolvimento
        base = os.path.dirname(os.path.abspath(__file__))
    return base

def get_app_path():
    """Retorna o diretório onde estão os scripts da aplicação"""
    base = get_base_path()
    # Em produção: _internal/app/
    app_path = os.path.join(base, '_internal', 'app')
    if os.path.exists(app_path):
        return app_path
    # Fallback desenvolvimento
    app_path = os.path.join(base, 'src')
    if os.path.exists(app_path):
        return app_path
    # Último fallback
    return base

def get_icon_path():
    """Retorna o caminho do ícone"""
    base = get_base_path()
    icon_path = os.path.join(base, '_internal', 'assets', 'senai.ico')
    if os.path.exists(icon_path):
        return icon_path
    # Fallback desenvolvimento
    icon_path = os.path.join(base, 'assets', 'senai.ico')
    if os.path.exists(icon_path):
        return icon_path
    return None

def run_module(module_name, root_window):
    """Executa um módulo Python"""
    app_path = get_app_path()
    script_path = os.path.join(app_path, f"{module_name}.py")
    
    if not os.path.exists(script_path):
        messagebox.showerror(
            "Erro",
            f"Script não encontrado:\n{script_path}\n\n"
            f"Diretório app: {app_path}\n"
            f"Conteúdo: {os.listdir(app_path) if os.path.exists(app_path) else 'N/A'}"
        )
        return
    
    try:
        # Adicionar app_path ao sys.path
        if app_path not in sys.path:
            sys.path.insert(0, app_path)
        
        if getattr(sys, 'frozen', False):
            # EXECUTÁVEL PyInstaller - Importar e executar diretamente
            # Fechar a janela do launcher
            root_window.destroy()
            
            # Importar o módulo
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, script_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # Executar a função main() se existir
            if hasattr(module, 'main'):
                module.main()
            
        else:
            # DESENVOLVIMENTO - Usar subprocess
            root_window.withdraw()  # Esconder janela
            root_window.update()
            
            # Executar em processo separado
            result = subprocess.run(
                [sys.executable, script_path],
                cwd=os.path.dirname(script_path),
                env={**os.environ, 'PYTHONPATH': app_path}
            )
            
            # Reabrir janela do launcher
            root_window.deiconify()
        
    except Exception as e:
        if not getattr(sys, 'frozen', False):
            root_window.deiconify()  # Garantir que janela volte no desenvolvimento
        
        messagebox.showerror(
            "Erro ao executar módulo",
            f"Módulo: {module_name}\n"
            f"Erro: {str(e)}\n"
            f"Tipo: {type(e).__name__}"
        )
        import traceback
        traceback.print_exc()

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SENAI - Mineração de Processos")
        self.root.geometry("550x550")
        self.root.resizable(False, False)
        
        # Ícone
        icon_path = get_icon_path()
        if icon_path:
            try:
                self.root.iconbitmap(icon_path)
            except:
                pass
        
        # Centralizar janela
        self.center_window()
        
        # Título
        title_label = tk.Label(
            root,
            text="SENAI - Mineração de Processos",
            font=("Arial", 16, "bold"),
            fg="#003366"
        )
        title_label.pack(pady=20)
        
        # Subtítulo
        subtitle_label = tk.Label(
            root,
            text="Mapeamento Digital de Rotinas de Trabalho",
            font=("Arial", 11),
            fg="#666666"
        )
        subtitle_label.pack(pady=5)
        
        # Linha separadora
        separator = tk.Frame(root, height=2, bg="#cccccc")
        separator.pack(fill="x", padx=40, pady=15)
        
        # Instrução
        instruction_label = tk.Label(
            root,
            text="Selecione o módulo que deseja executar:",
            font=("Arial", 10)
        )
        instruction_label.pack(pady=10)
        
        # Frame para botões
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        # Botão Workbench
        btn_workbench = tk.Button(
            button_frame,
            text="📊 Workbench\nColeta e Exportação de Dados",
            font=("Arial", 11, "bold"),
            width=35,
            height=3,
            bg="#0066cc",
            fg="white",
            cursor="hand2",
            command=lambda: run_module("pm_workbench_gui", self.root)
        )
        btn_workbench.pack(pady=8)
        
        # Botão Analysis
        btn_analysis = tk.Button(
            button_frame,
            text="📈 Analysis\nVisualização e Análise de Processos",
            font=("Arial", 11, "bold"),
            width=35,
            height=3,
            bg="#00aa66",
            fg="white",
            cursor="hand2",
            command=lambda: run_module("pm_analysis_gui", self.root)
        )
        btn_analysis.pack(pady=8)
        
        # Rodapé
        footer_label = tk.Label(
            root,
            text="© 2025 Instituto SENAI de tecnologia em Produtividade - Todos os direitos reservados",
            font=("Arial", 8),
            fg="#999999"
        )
        footer_label.pack(side="bottom", pady=10)
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

def main():
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()