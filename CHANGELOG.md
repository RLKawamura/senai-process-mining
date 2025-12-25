# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [1.0.0] - 2025-12-25

### 🎉 Lançamento Inicial

Primeira versão estável do SENAI PR Process Mining Suite.

### ✨ Adicionado

#### Workbench (Coleta)
- Gravação automática de eventos via ActivityWatch (aw_watcher_uia)
- Captura de interações: window, input, UI Automation
- Exportação de eventos para CSV no formato PM4Py
- Fallback automático para diferentes janelas de tempo
- Interface gráfica simples e intuitiva
- Log de atividades em tempo real

#### Analysis (Análise)
- **KPIs do Processo**:
  - Tempo total observado
  - Número de eventos e casos
  - Variantes únicas
  - Aderência ao processo padrão
  - Quantidade de usuários e aplicações
  - Classificação de apps (Business/Pessoal/Outros)
  - Timeline por hora do dia

- **Variantes**:
  - Geração de todas as variantes
  - Top N variantes com percentuais
  - Exportação em TXT e CSV

- **Visualizações**:
  - DFG (Directly-Follows Graph) com frequências
  - Modelo Petri Net via Inductive Miner
  - Exportação em PNG e SVG
  - Graphviz portátil integrado

- **Process Description Document (PDD)**:
  - Geração automática de PDF profissional
  - Inclui: KPIs, variantes, top atividades, timeline
  - Tabelas e gráficos formatados
  - Metadados customizáveis (cliente, área, responsável, etc.)

- **Baseline & Conformance**:
  - Salvamento de processo padrão (baseline)
  - Comparação de amostras com baseline
  - Análise de conformidade via alignment-based fitness
  - Relatório PDF com gráficos comparativos
  - Detecção de melhorias/pioras em KPIs

#### Launcher
- Interface única para acessar Workbench e Analysis
- Ícone SENAI PR em todas as janelas
- Design profissional e intuitivo

#### Infraestrutura
- Build automatizado com PyInstaller
- Executável standalone (não requer instalação)
- Graphviz portátil incluído
- Monkey-patch para compatibilidade hashlib
- Configuração automática de diretórios
- Suporte a executável e modo desenvolvimento

### 🔧 Técnico

- Python 3.8+
- PM4Py 2.7.0+
- ActivityWatch Client/Core
- ReportLab para PDFs
- Tkinter para GUI
- PyInstaller para build

### 📦 Distribuição

- Executável Windows standalone
- Tamanho: ~150MB (com Graphviz)
- Sem necessidade de Python instalado
- Sem configuração necessária

---

## [Unreleased]

### 🔮 Planejado para Próximas Versões

#### v1.1.0 (Q1 2026)
- [ ] Dashboard web interativo
- [ ] Análise de múltiplos usuários
- [ ] Exportação para Excel com gráficos
- [ ] Filtros avançados de dados

#### v1.2.0 (Q2 2026)
- [ ] Integração com ferramentas RPA
- [ ] Machine Learning para detecção de anomalias
- [ ] Sugestões automáticas de otimização
- [ ] API REST para integração

#### v2.0.0 (Q3 2026)
- [ ] Suporte multi-idioma (EN, ES, PT)
- [ ] Modo cloud/servidor
- [ ] Análise colaborativa
- [ ] Mobile app para visualização

---

## [0.9.0] - 2025-12-20 (Beta)

### 🧪 Versão Beta Interna

- Testes iniciais com usuários IST Produtividade
- Validação de fluxos de trabalho
- Ajustes de performance
- Correção de bugs críticos

---

## [0.5.0] - 2025-12-15 (Alpha)

### 🚧 Versão Alpha Interna

- Proof of Concept funcional
- Integração básica PM4Py
- Primeiras análises de processo
- Interface protótipo

---

## Tipos de Mudanças

- `✨ Adicionado` - Novas funcionalidades
- `🔧 Modificado` - Mudanças em funcionalidades existentes
- `🗑️ Depreciado` - Funcionalidades que serão removidas
- `🔥 Removido` - Funcionalidades removidas
- `🐛 Corrigido` - Correção de bugs
- `🔒 Segurança` - Correções de segurança

---

**Formato de Versionamento**: MAJOR.MINOR.PATCH
- **MAJOR**: Mudanças incompatíveis com versões anteriores
- **MINOR**: Novas funcionalidades compatíveis com versões anteriores
- **PATCH**: Correções de bugs compatíveis com versões anteriores

---

**Desenvolvido por:** SENAI PR - IST Produtividade  
**Contato:** ist.produtividade@sistemafiep.org.br  
**Bugs:** rodrigo_kawamura@hotmail.com
