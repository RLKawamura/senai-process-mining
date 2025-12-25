# SENAI PR - Process Mining Suite

**Mapeamento Digital de Rotinas de Trabalho**

[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)]()

> ⚠️ **REQUISITO ESSENCIAL**: Este software requer o [ActivityWatch](https://activitywatch.net/) instalado e em execução. Sem o ActivityWatch Server rodando, a coleta de dados **NÃO FUNCIONARÁ**.

> 📄 **AVISO LEGAL**: Este software é propriedade do SENAI PR - IST Produtividade e é de uso EXCLUSIVO para consultorias do instituto. Uso não autorizado é proibido.

---

## 📋 Sobre o Projeto

O **SENAI Process Mining Suite** é uma solução completa para captura, análise e visualização de processos de trabalho através de Task Mining. O sistema utiliza o **ActivityWatch** para monitoramento não-invasivo e o **PM4Py** para análise avançada de processos, gerando insights valiosos para otimização, padronização e automação.

### 🎯 Características Principais

- **📊 Workbench (Coleta)**: Gravação automática via ActivityWatch
- **📈 Analysis (Análise)**: Análise avançada com Process Mining (PM4Py)
- **📄 Relatórios Profissionais**: Geração automática de PDFs
- **🔄 Baseline & Conformance**: Comparação de processos
- **📊 Visualizações**: DFG, Petri Nets, Variantes, Timeline
- **🚀 Zero Configuração**: Executável standalone

---

## 🔌 Pré-Requisitos OBRIGATÓRIOS

### ⚠️ ActivityWatch (ESSENCIAL)

**O SENAI Process Mining Suite NÃO funcionará sem o ActivityWatch!**

#### O que é o ActivityWatch?

ActivityWatch é um software open-source de monitoramento de tempo que captura automaticamente:
- 🪟 Janelas de aplicativos abertas
- 🌐 Sites visitados  
- ⌨️ Eventos de teclado (teclas, não conteúdo)
- 🖱️ Interações com UI

**Privacy-first:** Todos os dados ficam no seu computador, nada é enviado para nuvem.

#### Instalação do ActivityWatch

**1. Download:**
- 🔗 Acesse: https://activitywatch.net/downloads/
- 📥 Baixe a versão **Windows** (última estável)
- 📦 Arquivo: `aw-windows-x86_64-vX.X.X.zip` (~50 MB)

**2. Instalação:**
1. Extraia o ZIP em local permanente (ex: `C:\ActivityWatch`)
2. Execute `aw-qt.exe`
3. Um ícone ⏱️ aparecerá na bandeja do sistema (systray)

**3. Verificação:**
- ✅ Ícone do ActivityWatch visível na bandeja
- ✅ Ao clicar no ícone, mostra "Server running"
- ✅ Acesse http://localhost:5600 (interface web deve abrir)
- ✅ Watchers mostrando status "Running" (verde)

**4. Configuração:**
- ✅ Marque "Start on boot" (iniciar com Windows)
- ✅ Deixe rodando em background (consome ~100 MB RAM)
- ✅ Não requer configuração adicional

**5. Permissões (Importante!):**

No Windows 10/11, dê permissões de acessibilidade:
- Configurações → Privacidade → Acessibilidade
- Permita que ActivityWatch monitore aplicativos

---

### 💻 Requisitos do Sistema (SENAI Process Mining)

| Item | Mínimo | Recomendado |
|------|--------|-------------|
| **SO** | Windows 10 (64-bit) | Windows 11 (64-bit) |
| **Processador** | Intel Core i3 | Intel Core i5+ |
| **RAM** | 4 GB | 8 GB+ |
| **Disco** | 1 GB livre | 5 GB livre |
| **Resolução** | 1366x768 | 1920x1080 |
| **ActivityWatch** | ✅ **OBRIGATÓRIO** | ✅ **OBRIGATÓRIO** |

---

## 📥 Instalação

### ✅ Passo 1: Instalar ActivityWatch (OBRIGATÓRIO)

**Antes de usar o SENAI Process Mining, você DEVE instalar o ActivityWatch:**

1. **Download**: https://activitywatch.net/downloads/
2. **Extrair** o ZIP em `C:\ActivityWatch`
3. **Executar** `aw-qt.exe`
4. **Verificar** ícone ⏱️ na bandeja do sistema

⚠️ **SEM O ACTIVITYWATCH, O WORKBENCH NÃO FUNCIONARÁ!**

---

### ✅ Passo 2: Baixar SENAI Process Mining

**Opção A: Executável Standalone (Recomendado)**

1. Baixe a última versão: [**📥 Releases**](https://github.com/RLKawamura/senai-process-mining/releases/latest)
2. Extraia o arquivo ZIP
3. Execute `SENAI_Mineracao_Processos.exe`
4. Não requer instalação!

**Opção B: Código-Fonte (Desenvolvedores)**

```bash
# Clone o repositório
git clone https://github.com/RLKawamura/senai-process-mining.git
cd senai-process-mining

# Crie ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Execute
python pm_suite_entry.py
```

---

### ✅ Passo 3: Verificar Tudo

**Checklist antes do primeiro uso:**

- [ ] ✅ ActivityWatch instalado
- [ ] ✅ `aw-qt.exe` rodando (ícone na bandeja)
- [ ] ✅ Interface web abre em http://localhost:5600
- [ ] ✅ Watchers mostrando "Running"
- [ ] ✅ SENAI Process Mining executável baixado
- [ ] ✅ SENAI_Mineracao_Processos.exe abre sem erros

---

## 🚀 Uso Rápido

### Fluxo Completo (Primeiro Uso - 10 minutos)

#### 0️⃣ **ANTES DE TUDO: Verifique ActivityWatch**

```bash
# ✅ OBRIGATÓRIO: ActivityWatch deve estar rodando!
# Olhe na bandeja do sistema (systray)
# Deve ter o ícone ⏱️ do ActivityWatch
# Se não tiver, execute: C:\ActivityWatch\aw-qt.exe
```

---

#### 1️⃣ **Workbench - Coleta de Dados** (5-30 min)

1. Abra **SENAI Process Mining Suite** (`SENAI_Mineracao_Processos.exe`)
2. Clique em **"📊 Workbench"**
3. ⚠️ **IMPORTANTE**: Verifique a mensagem de status
   - ✅ Se mostrar "Pronto para gravar" → Tudo OK
   - ❌ Se mostrar erro de conexão → ActivityWatch não está rodando!
4. Clique em **"Iniciar gravação"**
5. **Trabalhe normalmente** por 5-30 minutos:
   - Abra aplicativos
   - Navegue em sites
   - Use o sistema como de costume
6. Clique em **"Parar e exportar sessão"**
7. CSV será salvo em: `Documentos\SENAI_ProcessMining\outputs\`

**Dica:** Quanto mais tempo gravar (15-30 min), melhor a análise!

---

#### 2️⃣ **Analysis - Análise de Processos** (2-5 min)

1. No launcher, clique em **"📈 Analysis"**
2. Clique **"Procurar..."** → selecione o CSV exportado
3. Preencha metadados (opcional mas recomendado):
   - Cliente: Nome da empresa cliente
   - Área: Setor/departamento
   - Responsável: Seu nome (consultor SENAI)
   - Período: Data/hora da coleta
4. **Experimente as análises:**

| Botão | O que faz | Tempo | Output |
|-------|-----------|-------|--------|
| **Gerar KPIs** | Estatísticas do processo | ~10s | TXT + CSV |
| **Gerar Variantes (Top)** | Top 10 caminhos do processo | ~15s | TXT + CSV |
| **Gerar DFG** | Grafo visual de frequência | ~20s | PNG + SVG |
| **Gerar PDF** | Relatório completo profissional | ~30s | PDF |
| **Descobrir modelo** | Petri Net (Inductive Miner) | ~30s | PNG + SVG |
| **Salvar baseline** | Salva processo padrão | ~20s | PKL |

---

## 📊 Tipos de Análises Disponíveis

### 1. KPIs e Estatísticas

**O que gera:**
- Tempo total monitorado
- Número de eventos e casos
- Total de variantes únicas
- Aderência ao processo padrão (%)
- Classificação de apps (Business/Pessoal/Outros)
- Timeline por hora do dia

**Arquivos gerados:**
- `*__kpis_resumo.txt` - Resumo completo
- `*__kpis_top_atividades.csv` - Top atividades
- `*__apps_categories.csv` - Uso por tipo de app

---

### 2. Variantes do Processo

**O que é:** Diferentes sequências de atividades (caminhos)

**Exemplo:**
```
Variante 1 (50%): Abrir Excel → Editar → Salvar → Fechar
Variante 2 (30%): Abrir Excel → Copiar → Colar → Salvar → Fechar
Variante 3 (20%): Abrir Excel → Fechar (sem salvar)
```

**Uso:** Identificar processos padrão vs exceções

---

### 3. DFG (Directly-Follows Graph)

**O que é:** Grafo visual mostrando fluxo de atividades

**Características:**
- Nós = Atividades
- Setas = Transições (com frequências)
- Espessura da seta = Frequência

**Uso:** Visualizar gargalos e caminhos mais comuns

---

### 4. Process Description Document (PDF)

**Relatório profissional contendo:**
- ✅ Capa com metadados do cliente
- ✅ KPIs completos
- ✅ Top variantes (tabela)
- ✅ Top atividades (tabela)
- ✅ Uso por tipo de app (tabela)
- ✅ Timeline de uso (gráfico)
- ✅ Análise de desvios
- ✅ Recomendações

**Uso:** Entrega ao cliente, relatório de consultoria

---

### 5. Baseline e Conformance

**O que é:**
- **Baseline**: Processo padrão/ideal salvo
- **Conformance**: Comparação de nova amostra com baseline

**Fluxo:**
1. Colete processo ideal → **Salvar baseline**
2. Colete nova amostra → **Comparar com baseline**
3. Receba PDF com:
   - Fitness (% de conformidade)
   - KPIs comparados
   - Gráficos de melhoria/piora

**Uso:** Monitorar aderência ao processo padrão, identificar desvios

---

## 📸 Screenshots

### 🚀 Launcher Principal

O ponto de entrada da suite - escolha entre coleta (Workbench) ou análise (Analysis).

![Launcher](docs/images/launcher.png)

---

### 📊 Workbench - Coleta de Dados

Interface simples para gravação de eventos com ActivityWatch.

![Workbench](docs/images/workbench.png)

**Funcionalidades:**
- ✅ Iniciar/parar gravação com um clique
- ✅ Log de atividades em tempo real
- ✅ Exportação automática para CSV
- ✅ Indicador de conexão com ActivityWatch

**⚠️ REQUISITO:** ActivityWatch Server deve estar rodando!

---

### 📈 Analysis - Análise de Processos

Central de análises com 10+ tipos de visualizações e relatórios.

![Analysis](docs/images/analysis.png)

**Recursos:**
- ✅ Carregamento de CSVs exportados
- ✅ Preenchimento de metadados (cliente, área, período)
- ✅ Geração de KPIs, DFG, Variantes, PDFs
- ✅ Baseline e conformance
- ✅ 10+ tipos de análises em um clique

---

## 📂 Estrutura de Outputs

Todos os arquivos gerados são salvos em:

```
C:\Users\[Usuario]\Documents\SENAI_ProcessMining\outputs\
├── event_log_COMBINED_[data]_[hora].csv          ← CSV exportado do Workbench
├── [arquivo]__kpis_resumo.txt                    ← Resumo de KPIs
├── [arquivo]__kpis_top_atividades.csv            ← Top atividades
├── [arquivo]__apps_categories.csv                ← Classificação de apps
├── [arquivo]__variants_all.csv                   ← Todas variantes
├── [arquivo]__variants_top.txt                   ← Top variantes
├── [arquivo]__variants_top_table.csv             ← Top variantes (tabela)
├── [arquivo]__dfg_frequency.png                  ← DFG (imagem)
├── [arquivo]__dfg_frequency.svg                  ← DFG (vetorial)
├── [arquivo]__inductive_petri.png                ← Petri Net
├── [arquivo]__inductive_petri.svg                ← Petri Net (vetorial)
├── [arquivo]__process_description_document.pdf   ← PDF profissional
├── [arquivo]__baseline.pkl                       ← Modelo baseline
└── [arquivo]__baseline_comparison.pdf            ← Comparação com baseline
```

---

## 🐛 Solução de Problemas Comuns

### ❌ "Erro ao conectar com ActivityWatch Server"

**Problema:** Workbench não consegue gravar eventos

**Causa:** ActivityWatch não está rodando

**Solução:**
1. Verifique se `aw-qt.exe` está rodando (ícone ⏱️ na bandeja)
2. Se não estiver, execute `C:\ActivityWatch\aw-qt.exe` manualmente
3. Aguarde 10 segundos até o server iniciar
4. Verifique em http://localhost:5600 se está funcionando
5. Tente novamente no Workbench

---

### ❌ "Nenhum bucket encontrado"

**Problema:** Workbench não encontra watchers do ActivityWatch

**Causa:** ActivityWatch instalado mas watchers não iniciaram

**Solução:**
1. Abra http://localhost:5600
2. Vá em "Activity" → Verifique se há watchers listados
3. Deve ter: `aw-watcher-window`, `aw-watcher-afk`
4. Se não houver, reinicie o ActivityWatch:
   - Clique no ícone → "Quit"
   - Execute `aw-qt.exe` novamente
5. Aguarde 10 segundos e tente novamente

---

### ❌ "Janela sem eventos (curta demais?)"

**Problema:** Ao exportar, diz que não há eventos para exportar

**Causa:** 
- Período de coleta muito curto
- ActivityWatch sem permissões
- Nenhuma atividade foi realizada

**Solução:**
1. Grave por **pelo menos 5 minutos**
2. **Faça atividades** durante a gravação:
   - Abra aplicativos diferentes
   - Navegue em sites
   - Alterne entre janelas (Alt+Tab)
3. Verifique permissões do ActivityWatch no Windows
4. Tente exportar novamente

---

### ❌ "DFG não é gerado" ou "Erro do Graphviz"

**Problema:** Erro ao gerar DFG ou Petri Net

**Causa:** Graphviz não configurado corretamente

**Solução (Executável):**
- Verifique se `_internal\vendor\graphviz\bin\dot.exe` existe
- Se não existir, re-extraia o ZIP completo

**Solução (Código-fonte):**
- O Graphviz portátil já vem no repositório
- Se ainda assim falhar, instale: https://graphviz.org/download/

---

### ❌ Windows Defender bloqueia executável

**Problema:** "Windows protegeu seu computador"

**Causa:** Executável não possui assinatura digital

**Solução:**
1. Clique em **"Mais informações"**
2. Clique em **"Executar assim mesmo"**
3. OU adicione exceção no Windows Defender

**Por que isso acontece?**
- Executável não tem certificado digital (certificados custam ~US$ 300/ano)
- É seguro, o código está público no GitHub

---

## 🏗️ Build do Executável

Para compilar do código-fonte:

```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Limpar builds anteriores
rmdir /s /q build dist

# Build com PyInstaller
pyinstaller pm_suite.spec --clean --noconfirm

# Executável em: dist\SENAI_Mineracao_Processos\
```

📖 **Guia completo:** [docs/BUILD.md](docs/BUILD.md)

---

## 📚 Documentação Completa

- 📖 [Manual do Usuário](docs/INSTALACAO.md) - Guia completo de instalação e uso
- 🏗️ [Guia de Build](docs/BUILD.md) - Como compilar o executável
- 📝 [Changelog](CHANGELOG.md) - Histórico de versões
- 🤝 [Como Contribuir](CONTRIBUTING.md) - Guia para colaboradores do IST

---

## 🤝 Contribuindo (IST Produtividade)

Este projeto é de uso interno do IST Produtividade. Colaboradores do SENAI/IST podem:

1. **Fork** o repositório
2. **Criar branch** para sua feature
3. **Fazer mudanças**
4. **Abrir Pull Request**

📖 Ver [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes

---

## 📄 Licença

**Licença Proprietária - Todos os Direitos Reservados**

Copyright © 2025 SENAI PR - Instituto SENAI de Tecnologia em Produtividade (IST Produtividade)

Este software é de uso **EXCLUSIVO** do IST Produtividade para consultorias. 
Uso não autorizado é **PROIBIDO**.

Ver [LICENSE](LICENSE) para termos completos.

---

## 🙏 Agradecimentos

Este projeto utiliza as seguintes bibliotecas open-source:

- [PM4Py](https://pm4py.fit.fraunhofer.de/) - Process Mining
- [ActivityWatch](https://activitywatch.net/) - Time Tracking (ESSENCIAL!)
- [Graphviz](https://graphviz.org/) - Visualizações
- [ReportLab](https://www.reportlab.com/) - Geração de PDFs
- [Pandas](https://pandas.pydata.org/) - Análise de dados

---

## 📞 Suporte

**Para colaboradores do IST Produtividade:**

- 🐛 **Bugs/Issues:** rodrigo_kawamura@hotmail.com
- 💡 **Sugestões:** [GitHub Discussions](../../discussions)
- 📧 **Contato IST:** ist.produtividade@sistemafiep.org.br
- 🌐 **Website:** https://www.senaipr.org.br/tecnologiaeinovacao/

---

## ⚠️ Checklist Pré-Uso

Antes de usar em consultoria, verifique:

- [ ] ✅ ActivityWatch instalado e configurado
- [ ] ✅ ActivityWatch rodando (ícone na bandeja)
- [ ] ✅ Watchers mostrando "Running" em http://localhost:5600
- [ ] ✅ SENAI Process Mining executável testado
- [ ] ✅ Workbench conecta com ActivityWatch sem erros
- [ ] ✅ Teste de coleta (5 min) realizado com sucesso
- [ ] ✅ CSV exportado corretamente
- [ ] ✅ Analysis carrega CSV sem erros
- [ ] ✅ Pelo menos 1 análise testada (KPIs ou DFG)

---

**Desenvolvido com ❤️ pelo SENAI PR - IST Produtividade**

**Versão**: 1.0.0 | **Data**: Dezembro 2025 | **Requisito**: ActivityWatch ⏱️
