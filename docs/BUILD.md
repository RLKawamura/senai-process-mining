# 🏗️ Guia de Build - SENAI Process Mining Suite

Este documento descreve como compilar o executável standalone do SENAI Process Mining Suite a partir do código-fonte.

---

## 📋 Pré-requisitos

### Software Necessário

1. **Python 3.8 ou superior**
   - Download: https://www.python.org/downloads/
   - Certifique-se de marcar "Add Python to PATH" durante instalação

2. **Git** (opcional, para clonar repositório)
   - Download: https://git-scm.com/downloads

3. **Visual C++ Redistributable** (Windows)
   - Geralmente já instalado
   - Se necessário: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Espaço em Disco

- **Código-fonte**: ~50 MB
- **Ambiente virtual + dependências**: ~1.5 GB
- **Build final**: ~150 MB
- **Total recomendado**: ~2 GB livres

---

## 🚀 Processo de Build

### 1️⃣ Obter o Código-Fonte

#### Opção A: Clone do Git

```bash
git clone https://github.com/seu-usuario/senai-process-mining.git
cd senai-process-mining
```

#### Opção B: Download ZIP

1. Baixe o código em [GitHub](https://github.com/seu-usuario/senai-process-mining)
2. Extraia o ZIP
3. Abra terminal na pasta extraída

---

### 2️⃣ Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

# Verificar ativação (deve mostrar (.venv) no início da linha)
```

---

### 3️⃣ Instalar Dependências

```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar todas as dependências
pip install -r requirements.txt

# Verificar instalação
pip list
```

**Dependências Principais:**
- pm4py>=2.7.0
- pandas>=1.5.0
- pyinstaller>=5.0.0
- reportlab>=3.6.0
- aw-client>=0.5.0
- graphviz>=0.20.0

---

### 4️⃣ Verificar Estrutura de Arquivos

Certifique-se de que a estrutura está correta:

```
SENAI_Process_Mining/
├── pm_suite_entry.py          ✓ Script principal
├── pm_suite_entry.spec        ✓ Configuração PyInstaller
├── requirements.txt           ✓ Dependências
├── assets/
│   └── senai.ico              ✓ Ícone do aplicativo
├── src/
│   ├── pm_analysis_gui.py     ✓ Interface Analysis
│   ├── pm_workbench_gui.py    ✓ Interface Workbench
│   └── aw_watcher_uia.py      ✓ Watcher ActivityWatch
└── vendor/
    └── graphviz/              ✓ Graphviz portátil
        ├── bin/
        └── lib/
```

---

### 5️⃣ Limpar Builds Anteriores (se existirem)

```bash
# Remover builds antigos
rmdir /s /q build      # Windows
rmdir /s /q dist       # Windows

# Ou no Linux/Mac:
rm -rf build dist
```

---

### 6️⃣ Executar Build com PyInstaller

```bash
# Build completo (recomendado)
pyinstaller pm_suite_entry.spec --clean --noconfirm

# OU build rápido (sem limpeza, mais rápido em rebuilds)
pyinstaller pm_suite_entry.spec --noconfirm
```

**Opções do PyInstaller:**
- `--clean`: Remove cache antes de buildar (garante build limpo)
- `--noconfirm`: Sobrescreve sem perguntar
- `--log-level=INFO`: Mostra logs detalhados (debug)

**Tempo esperado:** 2-5 minutos (depende do hardware)

---

### 7️⃣ Verificar Build

```bash
# Navegar para pasta do executável
cd dist\SENAI_Mineracao_Processos

# Verificar arquivos gerados
dir

# Testar executável
SENAI_Mineracao_Processos.exe
```

**Arquivos esperados em `dist\SENAI_Mineracao_Processos\`:**

```
SENAI_Mineracao_Processos.exe    # Executável principal (~20 MB)
_internal/                        # Bibliotecas e dependências
├── app/                          # Scripts Python
│   ├── pm_analysis_gui.py
│   ├── pm_workbench_gui.py
│   └── aw_watcher_uia.py
├── assets/                       # Recursos
│   └── senai.ico
├── vendor/                       # Ferramentas portáteis
│   └── graphviz/
└── [diversos DLLs e PYDs]
```

---

## 🎯 Build Otimizado

### Reduzir Tamanho do Executável

1. **Excluir módulos não usados** (edite `pm_suite_entry.spec`):

```python
excludes=[
    'pandas.tests', 
    'numpy.tests', 
    'pytest', 
    'IPython', 
    'jupyter',
    'tkinter.test',
    'matplotlib.tests',
]
```

2. **Usar UPX** (compressão de executável):

```bash
# Download UPX: https://upx.github.io/
# Extrair upx.exe para pasta do projeto

# Editar pm_suite_entry.spec:
exe = EXE(
    ...
    upx=True,  # Ativar compressão UPX
    ...
)
```

---

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError"

**Problema:** Alguma dependência não foi instalada

**Solução:**
```bash
pip install -r requirements.txt --force-reinstall
```

---

### Erro: "graphviz not found"

**Problema:** Graphviz portátil não está na pasta `vendor/`

**Solução:**
1. Baixe Graphviz: https://graphviz.org/download/
2. Extraia para `vendor/graphviz/`
3. Verifique estrutura:
   ```
   vendor/graphviz/
   ├── bin/
   │   └── dot.exe
   └── lib/
   ```

---

### Erro: "Permission denied" ao deletar build/

**Problema:** Arquivos bloqueados pelo Windows

**Solução:**
1. Feche todos os programas
2. Use PowerShell como Administrador:
   ```powershell
   Remove-Item -Path build,dist -Recurse -Force
   ```

---

### Build muito lento

**Problema:** PyInstaller analisando muitos arquivos

**Solução:**
1. Exclua mais módulos não usados
2. Use `--log-level=WARN` (menos verbose)
3. Não use `--clean` em rebuilds

---

### Executável não abre

**Problema:** Pode ser antivírus bloqueando

**Solução:**
1. Adicione exceção no antivírus para a pasta `dist/`
2. Execute via linha de comando para ver erros:
   ```bash
   cd dist\SENAI_Mineracao_Processos
   SENAI_Mineracao_Processos.exe
   ```

---

## 📦 Distribuição

### Criar Pacote ZIP para Distribuição

```bash
# Navegar para pasta dist
cd dist

# Criar ZIP (Windows)
powershell Compress-Archive -Path SENAI_Mineracao_Processos -DestinationPath SENAI_Process_Mining_v1.0.0.zip

# Ou usar 7-Zip / WinRAR manualmente
```

### Checklist de Distribuição

- [ ] Executável funciona sem erros
- [ ] Ícone SENAI aparece em todas as janelas
- [ ] Análises geram outputs corretamente
- [ ] PDFs são criados sem erros
- [ ] Tamanho do ZIP é aceitável (<200 MB)
- [ ] README.md incluído
- [ ] LICENSE incluído
- [ ] CHANGELOG.md atualizado

---

## 🔄 Rebuild Rápido (Desenvolvimento)

Para rebuilds durante desenvolvimento:

```bash
# Ativar venv
.venv\Scripts\activate

# Build rápido (sem --clean)
pyinstaller pm_suite_entry.spec --noconfirm

# Testar
dist\SENAI_Mineracao_Processos\SENAI_Mineracao_Processos.exe
```

---

## 🎓 Referências

- [Documentação PyInstaller](https://pyinstaller.org/en/stable/)
- [PM4Py Documentation](https://pm4py.fit.fraunhofer.de/)
- [Python Packaging Guide](https://packaging.python.org/)

---

## 📞 Suporte

Problemas durante o build? Abra uma [Issue no GitHub](../../issues) com:

- Saída completa do erro
- Versão do Python (`python --version`)
- Sistema operacional
- Conteúdo de `pm_suite_entry.spec`

---

**Última atualização:** Dezembro 2024  
**Versão do Guia:** 1.0
