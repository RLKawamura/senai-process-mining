# 📥 Guia de Instalação - SENAI Process Mining Suite

Guia completo de instalação para usuários finais.

---

## 🎯 Visão Geral

O SENAI Process Mining Suite vem em **executável standalone** - não requer instalação tradicional. Basta extrair e executar!

**Tempo estimado:** 5 minutos

---

## 📋 Requisitos do Sistema

### Mínimos

| Item | Requisito |
|------|-----------|
| **Sistema Operacional** | Windows 10 (64-bit) ou superior |
| **Processador** | Intel Core i3 ou equivalente |
| **Memória RAM** | 4 GB |
| **Espaço em Disco** | 1 GB livre |
| **Resolução de Tela** | 1366x768 |

### Recomendados

| Item | Requisito |
|------|-----------|
| **Sistema Operacional** | Windows 11 (64-bit) |
| **Processador** | Intel Core i5 ou superior |
| **Memória RAM** | 8 GB ou mais |
| **Espaço em Disco** | 5 GB livre |
| **Resolução de Tela** | 1920x1080 ou superior |

---

## 🚀 Instalação Passo a Passo

### Passo 1: Download

1. Acesse a página de [Releases](https://github.com/seu-usuario/senai-process-mining/releases)
2. Baixe a última versão: `SENAI_Process_Mining_v1.0.0.zip`
3. Tamanho aproximado: ~150 MB

### Passo 2: Extração

1. Localize o arquivo ZIP baixado (geralmente em `Downloads`)
2. **Clique com botão direito** → **Extrair tudo...**
3. Escolha um local permanente (recomendado: `C:\SENAI_ProcessMining`)
4. Clique em **Extrair**

⚠️ **IMPORTANTE:** Não execute direto do ZIP! Extraia primeiro.

### Passo 3: Primeira Execução

1. Abra a pasta extraída: `SENAI_Mineracao_Processos`
2. **Duplo-clique** em `SENAI_Mineracao_Processos.exe`
3. Se o Windows perguntar, clique em **"Executar mesmo assim"**

**Pronto!** 🎉 O launcher deve abrir.

---

## 🔒 Alerta do Windows Defender

### Por que aparece?

O Windows pode mostrar um alerta porque o executável não possui assinatura digital (certificado pago).

### Como prosseguir com segurança?

1. Quando aparecer **"Windows protegeu seu computador"**:
   - Clique em **"Mais informações"**
   - Clique em **"Executar assim mesmo"**

2. **Ou** adicione exceção permanente no Windows Defender:
   - Abra **Configurações** → **Atualização e Segurança** → **Segurança do Windows**
   - Clique em **Proteção contra vírus e ameaças**
   - Em **Configurações de proteção**, clique em **Gerenciar configurações**
   - Role até **Exclusões** e clique em **Adicionar ou remover exclusões**
   - Clique em **Adicionar uma exclusão** → **Pasta**
   - Selecione a pasta `SENAI_Mineracao_Processos`

---

## 📦 Estrutura de Pastas

Após extração, você terá:

```
📁 SENAI_Mineracao_Processos/
├── 📄 SENAI_Mineracao_Processos.exe    # Executável principal
├── 📁 _internal/                        # Arquivos do sistema (NÃO MODIFICAR)
│   ├── 📁 app/                          # Scripts Python
│   ├── 📁 assets/                       # Ícones e recursos
│   └── 📁 vendor/                       # Ferramentas auxiliares
└── 📄 README.txt (opcional)
```

---

## 🎮 Primeiro Uso

### Configuração Inicial

1. **Instale o ActivityWatch** (necessário para coleta):
   - Download: https://activitywatch.net/downloads/
   - Instale e inicie o `aw-qt`
   - O ícone deve aparecer na bandeja do sistema

2. **Abra o SENAI Process Mining Suite**
   - Duplo-clique no executável
   - Escolha **Workbench** ou **Analysis**

### Teste Rápido (5 minutos)

#### 1. Testar Workbench (Coleta)

1. No launcher, clique em **"Workbench"**
2. Clique em **"Iniciar gravação"**
3. Realize algumas atividades no computador (abrir apps, navegar)
4. Aguarde 2-3 minutos
5. Clique em **"Parar e exportar sessão"**
6. Um CSV será salvo em `Documentos\SENAI_ProcessMining\outputs`

#### 2. Testar Analysis (Análise)

1. Volte ao launcher e clique em **"Analysis"**
2. Clique em **"Procurar..."** e selecione o CSV gerado
3. Preencha os campos (opcional)
4. Clique em **"Gerar KPIs / Top atividades"**
5. Uma janela com estatísticas deve abrir

✅ Se funcionou, a instalação foi bem-sucedida!

---

## 📁 Onde os Dados São Salvos?

### Outputs do Sistema

**Localização padrão:**
```
C:\Users\[SeuUsuário]\Documents\SENAI_ProcessMining\outputs\
```

**Tipos de arquivos gerados:**
- `event_log_COMBINED_*.csv` - Logs de eventos coletados
- `*__kpis_resumo.txt` - Relatórios de KPIs
- `*__dfg_frequency.png` - Grafos de processo
- `*__process_description_document.pdf` - PDFs profissionais
- `*__baseline.pkl` - Modelos salvos

### Logs do Sistema

**Localização:**
```
C:\Users\[SeuUsuário]\AppData\Local\SENAI_Process_Mining_Suite\
```

Contém logs de execução para diagnóstico de problemas.

---

## 🔄 Atualização

### Como Atualizar para Nova Versão

1. **Faça backup** dos seus dados:
   - Copie `Documentos\SENAI_ProcessMining\outputs\` para local seguro

2. **Baixe** a nova versão do GitHub Releases

3. **Extraia** a nova versão em nova pasta

4. **Execute** o novo executável

5. Seus dados anteriores continuam disponíveis em `Documentos`

⚠️ **Não é necessário** desinstalar a versão antiga - basta não usá-la mais.

---

## 🗑️ Desinstalação

### Remover o Software

1. **Delete a pasta** `SENAI_Mineracao_Processos` (onde você extraiu)

2. **(Opcional)** Delete os dados gerados:
   - `Documentos\SENAI_ProcessMining\`

3. **(Opcional)** Delete os logs:
   - `%LOCALAPPDATA%\SENAI_Process_Mining_Suite\`

**Pronto!** Software removido.

---

## 🐛 Solução de Problemas

### Problema: "Executável não abre"

**Soluções:**

1. **Verifique se extraiu** (não rode do ZIP)
2. **Execute como Administrador**:
   - Clique direito → "Executar como administrador"
3. **Verifique antivírus** (pode estar bloqueando)
4. **Reinstale o Visual C++ Redistributable**:
   - https://aka.ms/vs/17/release/vc_redist.x64.exe

---

### Problema: "ActivityWatch não está rodando"

**Sintoma:** Workbench não consegue coletar eventos

**Solução:**

1. Baixe ActivityWatch: https://activitywatch.net/
2. Instale e execute `aw-qt.exe`
3. Verifique ícone na bandeja do sistema
4. Reinicie o Workbench

---

### Problema: "Gráficos não são gerados" (DFG, Inductive)

**Sintoma:** Erro ao gerar DFG ou Petri Net

**Causa:** Graphviz não configurado corretamente

**Solução:**

1. Verifique se `_internal\vendor\graphviz\bin\dot.exe` existe
2. Se não existir, extraia novamente o ZIP completo
3. Ou baixe Graphviz: https://graphviz.org/download/

---

### Problema: "Erro ao gerar PDF"

**Sintoma:** Erro ao criar Process Description Document

**Solução:**

1. Verifique se há espaço em disco
2. Verifique permissões na pasta `Documentos`
3. Tente executar como Administrador

---

### Problema: "CSV muito grande / Análise lenta"

**Sintoma:** Analysis demora muito ou trava

**Solução:**

1. Use períodos de coleta menores (15-30 min)
2. Filtre eventos desnecessários
3. Considere analisar por partes

---

## 🆘 Suporte Técnico

### Antes de Reportar Problema

Colete estas informações:

1. **Versão do software**: Ver no launcher ou arquivo README
2. **Sistema operacional**: Windows 10/11, versão
3. **Mensagem de erro completa** (screenshot)
4. **Arquivo de log**: `%LOCALAPPDATA%\SENAI_Process_Mining_Suite\pm_*.log`

### Como Reportar

1. Abra uma [Issue no GitHub](https://github.com/seu-usuario/senai-process-mining/issues)
2. Use o template de bug report
3. Anexe informações coletadas acima

### Contato SENAI

- **Website**: www.senai.br
- **Email**: suporte@senai.br
- **Telefone**: 0800-XXX-XXXX

---

## 📚 Próximos Passos

Após instalação bem-sucedida:

1. 📖 Leia o [Manual do Usuário](MANUAL_USUARIO.md)
2. 🎥 Assista aos tutoriais em vídeo (em breve)
3. 💡 Experimente os casos de uso de exemplo
4. 🤝 Participe da comunidade no GitHub Discussions

---

## ✅ Checklist de Instalação

- [ ] Download do ZIP completo
- [ ] Extração para pasta permanente
- [ ] Executável abre sem erros
- [ ] ActivityWatch instalado e rodando
- [ ] Teste de coleta realizado com sucesso
- [ ] Teste de análise realizado com sucesso
- [ ] Localização dos outputs identificada

---

**Instalação concluída com sucesso?** Aproveite o SENAI Process Mining Suite! 🎉

---

**Última atualização:** Dezembro 2024  
**Versão do Guia:** 1.0
