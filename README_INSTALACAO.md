# SENAI - Mineração de Processos
## Mapeamento Digital de Rotinas de Trabalho

---

## 📋 Requisitos do Sistema

- **Sistema Operacional**: Windows 10 ou Windows 11 (64-bit)
- **Memória RAM**: Mínimo 4 GB (recomendado 8 GB)
- **Espaço em Disco**: 500 MB livres
- **Permissões**: Usuário padrão (não requer administrador)
- **Python**: **NÃO É NECESSÁRIO** (aplicação standalone)

---

## 🚀 Instalação Rápida

### Opção 1: Extração Simples (Recomendado)

1. Extraia o arquivo `SENAI_Mineracao_Processos_v1.0.zip`
2. Mova a pasta extraída para um local de sua preferência:
   - `C:\Programas\SENAI_Mineracao_Processos`
   - `C:\Users\SeuUsuario\SENAI_Mineracao_Processos`
3. Entre na pasta
4. Dê duplo clique em `SENAI_Mineracao_Processos.exe`

### Opção 2: Instalação em Rede

Se for instalar em um servidor de rede para múltiplos usuários:

1. Extraia para: `\\ServidorRede\Apps\SENAI_Mineracao_Processos`
2. Crie um atalho do executável na área de trabalho de cada usuário
3. Cada usuário pode executar normalmente

---

## 📦 Estrutura de Pastas

```
SENAI_Mineracao_Processos/
├── SENAI_Mineracao_Processos.exe  ← Execute este arquivo
├── _internal/                      ← Arquivos do sistema (NÃO MEXER)
│   ├── app/                        ← Scripts Python internos
│   ├── assets/                     ← Ícones e recursos
│   └── [bibliotecas...]            ← Dependências
└── LEIA-ME.txt                     ← Este arquivo
```

⚠️ **IMPORTANTE**: Não delete, mova ou renomeie a pasta `_internal`. O executável precisa dela para funcionar.

---

## 🎯 Módulos Disponíveis

Ao executar `SENAI_Mineracao_Processos.exe`, você verá dois módulos:

### 📊 Workbench - Coleta e Exportação de Dados
- Importa logs do ActivityWatch
- Processa eventos de aplicações e janelas
- Exporta dados em formato CSV para análise

### 📈 Analysis - Visualização e Análise de Processos
- Visualiza DFG (Directly-Follows Graph)
- Executa algoritmos de mineração de processos
- Analisa variantes de processos
- Gera KPIs (indicadores de desempenho)

---

## 🔧 ActivityWatch - Pré-Requisito Obrigatório

### O que é?
O **ActivityWatch** é um software de monitoramento de atividades que registra quais aplicações e janelas você usa ao longo do dia. É essencial para a mineração de processos.

### Onde Baixar?
🔗 **Site Oficial**: https://activitywatch.net/downloads/

Escolha a versão para Windows (64-bit).

### Como Instalar?

1. **Baixe o instalador**:
   - Acesse: https://activitywatch.net/downloads/
   - Baixe: `activitywatch-v0.X.X-windows-x86_64.exe`

2. **Execute o instalador**:
   - Dê duplo clique no arquivo baixado
   - Siga as instruções na tela
   - Aceite o local de instalação padrão

3. **Inicie o ActivityWatch**:
   - Após instalar, abra o ActivityWatch
   - Ele aparecerá na bandeja do sistema (ícone próximo ao relógio)
   - **Deixe-o rodando em segundo plano**

4. **Configure para iniciar automaticamente**:
   - Clique com botão direito no ícone do ActivityWatch na bandeja
   - Selecione "Settings" ou "Configurações"
   - Marque "Start on boot" ou "Iniciar com o Windows"

### Por Que Preciso do ActivityWatch?

O módulo **Workbench** precisa dos dados coletados pelo ActivityWatch para funcionar. Sem o ActivityWatch rodando:
- ❌ Não haverá dados para importar
- ❌ O Workbench não conseguirá processar eventos
- ❌ A análise de processos ficará incompleta

### Verificando se está Funcionando

1. Olhe na bandeja do sistema (próximo ao relógio)
2. Você deve ver o ícone do ActivityWatch (geralmente um olho 👁️)
3. Clique nele e selecione "Open Dashboard"
4. No navegador, verifique se há dados sendo coletados

---

## 🐛 Solução de Problemas

### Erro: "VCRUNTIME140.dll ausente"

**Causa**: Falta o Visual C++ Redistributable

**Solução**:
1. Baixe em: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Execute o instalador
3. Reinicie o computador
4. Tente executar novamente

### Erro: "Windows protegeu seu computador"

**Causa**: Windows SmartScreen bloqueando aplicativo desconhecido

**Solução**:
1. Clique em "Mais informações"
2. Clique em "Executar assim mesmo"

**OU**:
1. Clique com botão direito no executável
2. Selecione "Propriedades"
3. Na aba "Geral", marque "Desbloquear"
4. Clique "OK"
5. Execute novamente

### Workbench não encontra dados

**Causa**: ActivityWatch não está rodando ou não coletou dados ainda

**Solução**:
1. Verifique se o ActivityWatch está na bandeja do sistema
2. Se não estiver, abra o ActivityWatch
3. Use o computador normalmente por alguns minutos
4. Tente importar os dados novamente no Workbench

### Janelas do programa não aparecem

**Causa**: Pode estar abrindo em outro monitor ou minimizado

**Solução**:
1. Pressione `Alt + Tab` para alternar entre janelas
2. Verifique se não está em outro monitor
3. Reinicie o aplicativo

---

## 📞 Suporte Técnico

Para questões técnicas ou problemas:

- **E-mail**: suporte.ti@senai.br
- **Telefone**: (XX) XXXX-XXXX
- **Horário**: Segunda a Sexta, 8h às 18h

---

## 📝 Notas Importantes

### Segurança e Privacidade

- ✅ Todos os dados processados ficam no seu computador
- ✅ Nenhuma informação é enviada para servidores externos
- ✅ O ActivityWatch armazena dados localmente
- ✅ Você tem controle total sobre seus dados

### Atualizações

Para atualizar o software:
1. Baixe a nova versão
2. Substitua a pasta antiga pela nova
3. Seus dados do ActivityWatch são preservados

### Desinstalação

Para remover o software:
1. Feche o aplicativo se estiver aberto
2. Delete a pasta `SENAI_Mineracao_Processos`
3. Para remover o ActivityWatch, use o desinstalador do Windows:
   - Painel de Controle > Programas > Desinstalar um programa
   - Procure "ActivityWatch" e desinstale

---

## 📄 Licença e Direitos

© 2024 SENAI - Serviço Nacional de Aprendizagem Industrial  
Todos os direitos reservados.

Este software é de uso interno e corporativo. Distribuição não autorizada é proibida.

---

## 🎓 Treinamento e Documentação

Para aprender a usar o sistema:

1. **Vídeos tutoriais**: Disponíveis no portal interno do SENAI
2. **Documentação técnica**: Consulte o manual do usuário
3. **Treinamentos presenciais**: Consulte o RH sobre próximas turmas

---

**Versão**: 1.0.0  
**Data de Lançamento**: Dezembro 2024  
**Última Atualização**: 22/12/2024