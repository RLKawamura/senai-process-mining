# 🚀 Release v1.0.0 - SENAI Process Mining Suite

**Data de Lançamento:** 25 de Dezembro de 2024

---

## 🎉 Primeira Versão Estável!

Apresentamos a primeira versão estável do **SENAI Process Mining Suite** - uma solução completa para mapeamento digital de rotinas de trabalho através de Task Mining.

---

## ✨ Destaques desta Versão

### 📊 Workbench - Coleta de Dados
- Gravação automática de eventos (window, input, UI Automation)
- Exportação para CSV compatível com PM4Py
- Interface intuitiva com log em tempo real

### 📈 Analysis - Análise de Processos
- **10+ tipos de análises** incluindo KPIs, Variantes, DFG, Petri Net
- **Geração automática de PDFs** profissionais
- **Baseline e Conformance** para comparação de processos
- **Timeline por hora** do dia

### 🎯 Facilidades
- **Executável standalone** - não requer instalação
- **Graphviz integrado** - visualizações prontas
- **Interface em português** - 100% localizada

---

## 📥 Download

### Windows 64-bit (Recomendado)

**[⬇️ SENAI_Process_Mining_v1.0.0.zip](link-para-o-zip)** (150 MB)

**Checksums:**
- **SHA256:** `[inserir hash aqui]`
- **MD5:** `[inserir hash aqui]`

### Código-Fonte

- **[📦 Source code (zip)](link)**
- **[📦 Source code (tar.gz)](link)**

---

## 📋 Requisitos do Sistema

| Item | Requisito |
|------|-----------|
| **SO** | Windows 10/11 (64-bit) |
| **RAM** | 4 GB mínimo, 8 GB recomendado |
| **Disco** | 1 GB livre |
| **Outros** | ActivityWatch Server |

---

## 🚀 Início Rápido

### 1. Instalação

```bash
# 1. Extrair ZIP
# 2. Executar SENAI_Mineracao_Processos.exe
# 3. Escolher Workbench ou Analysis
```

### 2. Primeiro Uso

```
Workbench → Iniciar gravação → [trabalhe normalmente] → Parar e exportar
Analysis → Procurar CSV → Gerar análises
```

📖 **Documentação completa:** [INSTALACAO.md](INSTALACAO.md)

---

## 📊 O Que Há de Novo

### ✨ Funcionalidades

#### Workbench
- [x] Gravação automática via ActivityWatch
- [x] Exportação para CSV PM4Py
- [x] Fallback automático de janelas de tempo
- [x] Log de atividades em tempo real

#### Analysis
- [x] KPIs completos (tempo, casos, variantes, aderência)
- [x] Classificação de apps (Business/Pessoal/Outros)
- [x] Variantes (todas + top N)
- [x] DFG (Directly-Follows Graph)
- [x] Inductive Miner (Petri Net)
- [x] Process Description Document (PDF profissional)
- [x] Baseline e Conformance
- [x] Timeline por hora do dia

#### Infraestrutura
- [x] Build automatizado com PyInstaller
- [x] Graphviz portátil incluído
- [x] Ícone SENAI em todas as janelas
- [x] Outputs organizados em Documentos

### 🐛 Correções

- Corrigido: Ícone não aparecia em janelas Toplevel
- Corrigido: Mensagem de KPI mostrando caminho incorreto
- Corrigido: RESOURCE_DIR em desenvolvimento vs produção
- Corrigido: Compatibilidade hashlib com PM4Py

### 🔧 Melhorias

- Melhorado: Estrutura de diretórios mais organizada
- Melhorado: Mensagens de erro mais claras
- Melhorado: Performance de geração de PDFs
- Melhorado: Compatibilidade com Python 3.8-3.11

---

## 📈 Estatísticas

| Métrica | Valor |
|---------|-------|
| **Linhas de código** | ~2.500 |
| **Tamanho executável** | 150 MB |
| **Dependências** | 15+ bibliotecas |
| **Formatos de output** | 7 tipos (CSV, TXT, PNG, SVG, PDF, PKL) |
| **Análises disponíveis** | 10+ |

---

## 🔄 Migração de Versão Anterior

Não aplicável - primeira versão estável.

---

## ⚠️ Problemas Conhecidos

### Limitações Atuais

1. **Suporte apenas Windows**: Linux/Mac em desenvolvimento
2. **ActivityWatch obrigatório**: Não funciona sem AW Server
3. **Grande consumo de disco**: Logs grandes (~100MB/dia)
4. **Idioma fixo**: Apenas português (multi-idioma planejado)

### Workarounds

- **Disk Space**: Limpe logs antigos periodicamente
- **Performance**: Use períodos de coleta menores (15-30 min)

---

## 📚 Documentação

- 📖 [README.md](README.md) - Visão geral do projeto
- 📥 [INSTALACAO.md](INSTALACAO.md) - Guia de instalação
- 🏗️ [BUILD.md](BUILD.md) - Como compilar do código
- 📝 [CHANGELOG.md](CHANGELOG.md) - Histórico de mudanças
- 📄 [LICENSE](LICENSE) - Licença MIT

---

## 🐛 Reportar Problemas

Encontrou um bug? [Abra uma Issue](../../issues/new) com:

- Versão do software (v1.0.0)
- Sistema operacional
- Passos para reproduzir
- Screenshot (se aplicável)
- Arquivo de log

---

## 🗺️ Roadmap

### Próximas Versões

**v1.1.0 (Q1 2025)**
- Dashboard web interativo
- Análise multi-usuário
- Exportação para Excel

**v1.2.0 (Q2 2025)**
- Integração com RPA
- Machine Learning para anomalias
- API REST

**v2.0.0 (Q3 2025)**
- Suporte multi-idioma
- Modo cloud
- Mobile app

---

## 🙏 Agradecimentos

Desenvolvido com ❤️ pela equipe SENAI.

**Agradecimentos especiais:**
- Equipe de desenvolvimento SENAI
- Comunidade PM4Py
- Projeto ActivityWatch
- Beta testers internos

---

## 📞 Contato & Suporte

- **Website**: [www.senai.br](https://www.senai.br)
- **GitHub Issues**: [Reportar problema](../../issues)
- **Email**: suporte@senai.br
- **Documentação**: [Wiki do projeto](../../wiki)

---

## ✅ Verificação de Integridade

Após download, verifique a integridade:

```powershell
# PowerShell
Get-FileHash SENAI_Process_Mining_v1.0.0.zip -Algorithm SHA256

# Deve retornar: [hash SHA256 aqui]
```

---

## 🏆 Próximos Passos

1. ⬇️ **Baixe** o executável acima
2. 📖 **Leia** o [guia de instalação](INSTALACAO.md)
3. 🚀 **Execute** seu primeiro mapeamento de processo
4. 💡 **Compartilhe** feedback via Issues
5. ⭐ **Dê uma estrela** no repositório!

---

**Baixar agora:** [SENAI_Process_Mining_v1.0.0.zip](link) | **Código-fonte:** [GitHub](link)

---

*Esta release foi testada em Windows 10/11 com ActivityWatch v0.12+*

**Release criada em:** 25/12/2024  
**Assinado por:** SENAI Development Team
