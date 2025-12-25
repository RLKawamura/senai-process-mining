# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o **SENAI PR - Process Mining Suite**! Este documento fornece diretrizes para contribuições.

---

## 📋 Código de Conduta

### Nossos Valores

- **Respeito**: Trate todos com respeito e profissionalismo
- **Colaboração**: Trabalhe em conjunto para o bem do projeto
- **Qualidade**: Priorize código limpo e bem documentado
- **Inclusão**: Seja acolhedor com novos contribuidores

---

## 🚀 Como Contribuir

### 1️⃣ Reportar Bugs

**Email para bugs:** rodrigo_kawamura@hotmail.com

**Informações necessárias:**
- Versão do software
- Sistema operacional
- Passos para reproduzir
- Comportamento esperado vs atual
- Screenshots/logs

**Exemplo:**
```markdown
**Versão:** v1.0.0
**SO:** Windows 11 Pro 64-bit
**Problema:** DFG não é gerado

**Passos:**
1. Abrir Analysis
2. Selecionar CSV com 1000+ eventos
3. Clicar em "Gerar DFG"
4. Erro: "dot.exe not found"

**Esperado:** DFG deve ser gerado
**Atual:** Erro de Graphviz
```

---

### 2️⃣ Sugerir Funcionalidades

**Email para sugestões:** rodrigo_kawamura@hotmail.com

**Informações necessárias:**
- Problema que resolve
- Solução proposta
- Alternativas consideradas
- Impacto esperado

---

### 3️⃣ Contribuir com Código

#### Pré-requisitos

- Python 3.8+
- Git
- Conhecimento de PM4Py (recomendado)
- Acesso ao repositório (colaboradores SENAI PR/IST)

#### Processo

1. **Fork** o repositório
2. **Clone** seu fork:
   ```bash
   git clone https://github.com/seu-usuario/senai-process-mining.git
   cd senai-process-mining
   ```

3. **Crie uma branch** para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```

4. **Configure o ambiente:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Faça suas mudanças**

6. **Teste suas mudanças:**
   ```bash
   python pm_suite_entry.py
   ```

7. **Commit** com mensagem descritiva:
   ```bash
   git commit -m "feat: adiciona exportação para Excel"
   ```

8. **Push** para seu fork:
   ```bash
   git push origin feature/minha-feature
   ```

9. **Abra um Pull Request** no repositório original

---

## 📝 Padrões de Código

### Estilo Python

Seguimos **PEP 8** com algumas adaptações:

```python
# ✅ BOM
def calcular_kpis(csv_path: str) -> dict:
    """
    Calcula KPIs do processo.
    
    Args:
        csv_path: Caminho para o CSV de log
        
    Returns:
        Dicionário com KPIs calculados
    """
    # Lógica aqui
    return kpis

# ❌ RUIM
def calc(p):
    # sem docstring
    return x
```

### Commits Convencionais

Use prefixos semânticos:

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Mudanças em documentação
- `style:` - Formatação (sem mudança de lógica)
- `refactor:` - Refatoração de código
- `test:` - Adição/correção de testes
- `chore:` - Tarefas de manutenção

**Exemplos:**
```bash
feat: adiciona análise de bottlenecks
fix: corrige cálculo de tempo médio
docs: atualiza README com novos exemplos
refactor: simplifica lógica de exportação CSV
```

### Estrutura de Código

```python
# 1. Imports padrão
import os
import sys

# 2. Imports de terceiros
import pandas as pd
from pm4py import *

# 3. Imports locais
from utils import helper_function

# 4. Constantes
OUTPUT_DIR = "outputs"
MAX_EVENTS = 10000

# 5. Funções
def minha_funcao():
    pass

# 6. Classes
class MinhaClasse:
    pass

# 7. Main
if __name__ == "__main__":
    main()
```

---

## 🧪 Testes

### Testes Manuais

Antes de submeter PR, teste:

1. **Workbench**:
   - [ ] Iniciar/parar gravação
   - [ ] Exportação de CSV
   - [ ] Conexão com ActivityWatch

2. **Analysis**:
   - [ ] Carregamento de CSV
   - [ ] Geração de KPIs
   - [ ] Geração de variantes
   - [ ] Geração de DFG
   - [ ] Geração de PDF

3. **Build**:
   - [ ] Build com PyInstaller
   - [ ] Executável funciona
   - [ ] Ícones aparecem

### Testes Automatizados (Futuro)

Planejamos adicionar testes unitários com pytest:

```python
# tests/test_kpis.py
def test_calcular_kpis():
    csv_path = "tests/fixtures/sample.csv"
    kpis = compute_kpis(csv_path)
    assert kpis['num_events'] > 0
    assert kpis['num_cases'] > 0
```

---

## 📁 Estrutura do Projeto

```
SENAI_Process_Mining/
├── src/                      # Código-fonte principal
│   ├── pm_analysis_gui.py    # Interface de análise
│   ├── pm_workbench_gui.py   # Interface de coleta
│   └── aw_watcher_uia.py     # Watcher ActivityWatch
├── assets/                   # Recursos (ícones, imagens)
├── vendor/                   # Dependências portáteis
├── docs/                     # Documentação
├── tests/                    # Testes (futuro)
├── pm_suite_entry.py         # Launcher principal
├── pm_suite.spec             # Config PyInstaller
├── requirements.txt          # Dependências Python
└── README.md                 # Documentação principal
```

---

## 🎨 Contribuições de Design

### UI/UX

Melhorias na interface são bem-vindas:

- Mockups no Figma
- Paleta de cores SENAI PR
- Layout responsivo
- Acessibilidade

### Documentação

- Tutoriais em vídeo
- Guias ilustrados
- Traduções
- Screenshots

---

## 📚 Áreas para Contribuição

### 🟢 Iniciante-Friendly

- Corrigir typos na documentação
- Melhorar mensagens de erro
- Adicionar comentários no código
- Traduzir documentação

### 🟡 Intermediário

- Adicionar novos tipos de análise
- Melhorar performance
- Adicionar validações
- Criar testes unitários

### 🔴 Avançado

- Integração com outras ferramentas PM
- Machine Learning para detecção de anomalias
- Dashboard web
- API REST

---

## 🔄 Processo de Review

### O que esperamos em um PR

- [ ] Código segue os padrões do projeto
- [ ] Funcionalidade testada manualmente
- [ ] Documentação atualizada (se aplicável)
- [ ] Commits descritivos
- [ ] Branch atualizada com main

### Timeline de Review

- **Bugs críticos**: Resposta em 24h
- **PRs simples**: Review em 3-5 dias
- **PRs complexos**: Review em 1-2 semanas

### Critérios de Aprovação

✅ **Aprovado se:**
- Funcionalidade funciona corretamente
- Não quebra funcionalidades existentes
- Código está limpo e documentado
- Segue padrões do projeto

❌ **Rejeitado se:**
- Quebra funcionalidades existentes
- Código não segue padrões
- Falta documentação
- Não passa nos testes

---

## 🎓 Recursos para Aprendizado

### Process Mining

- [PM4Py Documentação](https://pm4py.fit.fraunhofer.de/)
- [Process Mining Book](https://www.processmining.org/book/start)
- [Coursera: Process Mining](https://www.coursera.org/learn/process-mining)

### Python

- [Python.org](https://www.python.org/)
- [Real Python](https://realpython.com/)
- [PEP 8 Style Guide](https://pep8.org/)

### ActivityWatch

- [ActivityWatch Docs](https://docs.activitywatch.net/)
- [aw-client Python](https://github.com/ActivityWatch/aw-client)

---

## 🏆 Reconhecimento

### Contribuidores

Todos os contribuidores serão:

- Listados no CONTRIBUTORS.md
- Mencionados no CHANGELOG
- Creditados em releases

### Top Contribuidores

Prêmios especiais para:
- Mais commits
- Maior impacto
- Melhor documentação
- Comunidade mais ativa

---

## 📞 Comunicação

### Canais

- **Bugs:** rodrigo_kawamura@hotmail.com
- **Sugestões:** rodrigo_kawamura@hotmail.com
- **Institucional:** ist.produtividade@sistemafiep.org.br
- **Pull Requests:** Code reviews via GitHub

### Idioma

- **Código**: Inglês (comentários em português OK)
- **Commits**: Português ou inglês
- **Issues/PRs**: Português preferencial
- **Documentação**: Português

---

## ❓ FAQ para Contribuidores

**Q: Posso trabalhar em uma Issue já atribuída?**  
A: Não, a menos que tenha permissão do assignee.

**Q: Como sei em que trabalhar?**  
A: Entre em contato via rodrigo_kawamura@hotmail.com para discutir contribuições.

**Q: Meu PR foi rejeitado, e agora?**  
A: Leia o feedback, faça as correções e resubmeta.

**Q: Posso contribuir sem saber PM4Py?**  
A: Sim! Há contribuições não-técnicas (docs, design, etc).

**Q: Quanto tempo leva para aprovar um PR?**  
A: Depende da complexidade. Simples: ~1 semana. Complexo: ~2 semanas.

---

## 🎯 Prioridades Atuais (2025)

### Alta Prioridade
- [ ] Testes unitários com pytest
- [ ] Documentação de API interna
- [ ] Otimização de performance (CSVs grandes)
- [ ] Exportação para Excel

### Média Prioridade
- [ ] Dashboard web interativo
- [ ] Análise multi-usuário
- [ ] Integração com RPA

### Baixa Prioridade
- [ ] Suporte multi-idioma
- [ ] Modo cloud
- [ ] Mobile app

---

## ✅ Checklist do Contribuidor

Antes de submeter PR:

- [ ] Li o CONTRIBUTING.md
- [ ] Testei localmente
- [ ] ActivityWatch funcionando nos testes
- [ ] Fork e clone do repositório
- [ ] Branch criada com nome descritivo
- [ ] Código segue padrões PEP 8
- [ ] Testei manualmente (Workbench + Analysis)
- [ ] Documentação atualizada
- [ ] Commits descritivos
- [ ] Push para meu fork
- [ ] PR aberto com descrição clara

---

## 🙏 Obrigado!

Sua contribuição faz diferença! Seja código, documentação, design ou feedback - tudo é valioso.

**Juntos construímos um melhor Process Mining Suite!** 💪

---

## 📧 Contatos

**SENAI PR - Instituto SENAI de Tecnologia em Produtividade**

- 📧 **Email Institucional:** ist.produtividade@sistemafiep.org.br
- 🐛 **Bugs/Sugestões:** rodrigo_kawamura@hotmail.com
- 🌐 **Website:** https://www.senaipr.org.br/tecnologiaeinovacao/

---

**Última atualização:** Dezembro 2025  
**Versão do Guia:** 1.0  
**Desenvolvido por:** SENAI PR - IST Produtividade
