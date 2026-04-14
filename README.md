# PurpleScan v2.0 - Scanner Profissional de Vulnerabilidades

Ferramenta brasileira de cibersegurança para análise de vulnerabilidades de rede e sistema.

## 🚀 Características

### 🔍 Scanner de Rede
- **Scanner Multi-threaded** - Varredura rápida e concorrente (100+ threads)
- **Identificação de Serviços** - Detecção automática de 25+ serviços comuns
- **Banner Grabbing** - Extração real de banners para fingerprinting
- **Alvos Flexíveis** - IP único, faixas CIDR ou listas de portas customizadas
- **Performance Otimizada** - Timeouts e pools de threads configuráveis

### 🖥️ Análise de Sistema
- **Informações Completas** - Enumeração de SO, hardware e softwares
- **Verificação de Segurança** - Detecção de firewall, antivírus e criptografia de disco
- **Suporte Windows & Linux** - Compatibilidade multiplataforma
- **Inventário de Softwares** - Aplicativos e pacotes instalados

### 📊 Análise de Risco
- **Sistema de Pontuação Ponderada** - Cálculo profissional de risco (0-100)
- **Classificação de Severidade** - Níveis Crítico, Alto, Médio, Baixo
- **Análise Contextual** - Avaliação de vulnerabilidades específicas por serviço
- **Resumo Executivo** - Formato de relatório nível C-level

### 📈 Dashboard Moderno
- **Interface Interativa HTML** - Dashboard estilo SOC com visualizações Chart.js
- **Gráficos em Tempo Real** - Métricas de risco e distribuição de serviços
- **Design Responsivo** - Interface amigável para dispositivos móveis
- **Capacidades de Exportação** - Relatórios JSON e HTML
- **Estilo Profissional** - Visual moderno com gradientes e animações

## 🛠️ Instalação

### Requisitos
- Python 3.7+
- Windows/Linux/Mac

### Instalação Rápida
```bash
# 1. Clonar ou baixar os arquivos
git clone https://github.com/purplescan/purplescan.git
cd purplescan

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Pronto para usar!
```

### Dependências
```bash
pip install colorama requests
```

## 🎯 Como Usar

### **1. Script Único (Recomendado)**
```bash
python scanner.py
```

**Menu Interativo em Português:**
```
PURPLESCAN v2.0 - Menu Principal
============================================
1. Scan Rápido (localhost)
2. Scan Personalizado
3. Scan de Rede Completa
4. Apenas Relatório do Sistema
5. Scan Completo (Tudo em Um)
6. Sair
============================================
```

### **2. Linha de Comando (Avançado)**
```bash
# Scan rápido
python main.py --quick-scan

# Scan personalizado
python main.py --scan 192.168.1.1 --ports 80,443,3389

# Scan de rede
python main.py --scan 192.168.1.0/24 --threads 200

# Apenas relatório do sistema
python main.py --report-only

# Exportar JSON customizado
python main.py --scan 127.0.0.1 --export-json meu_relatorio.json
```

## 📋 Opções do Menu

### **1. Scan Rápido**
- **Alvo**: localhost (127.0.0.1)
- **Portas**: Principais (HTTP, SSH, RDP, FTP, etc.)
- **Tempo**: ~30 segundos
- **Ideal**: Verificação rápida do próprio PC

### **2. Scan Personalizado**
- **Alvo**: Qualquer IP ou rede
- **Portas**: Customizáveis (faixa ou lista)
- **Threads**: Configurável (1-500)
- **Ideal**: Scan específico de servidor/alvo

### **3. Scan de Rede Completa**
- **Alvo**: Rede inteira (CIDR)
- **Portas**: Principais + customizáveis
- **Threads**: 200 (otimizado para performance)
- **Ideal**: Descobrir dispositivos na rede

### **4. Relatório do Sistema**
- **Escopo**: Apenas análise local
- **Sem scan**: Apenas configurações do sistema
- **Tempo**: ~10 segundos
- **Ideal**: Verificar segurança do próprio PC

### **5. Scan Completo (Tudo em Um)**
- **Abrangência**: Sistema + Rede + Risco + Relatório
- **Flexibilidade**: Alvo principal + rede adicional
- **Completo**: Análise 360° de segurança
- **Ideal**: Auditoria completa de segurança

## 📊 Arquivos Gerados

Após executar, você terá:

- **`purplescan_dashboard.html`** - Dashboard interativo completo
- **`purplescan_report.json`** - Relatório detalhado em JSON
- **Arquivos customizados** - Se especificar nomes diferentes

## 🎨 Dashboard HTML

O dashboard abre automaticamente no navegador com:

### **Métricas Principais**
- **Score de Risco** (0-100) com visualização gráfica
- **Status do Sistema** - Windows/Linux, firewall, antivírus
- **Portas Abertas** - Com banners e serviços identificados
- **Gráficos Interativos** - Distribuição de risco e serviços

### **Seções do Dashboard**
- **Informações do Sistema** - SO, hostname, arquitetura
- **Status de Segurança** - Firewall, antivírus, criptografia
- **Análise de Risco** - Classificação por severidade
- **Resumo da Rede** - Hosts, portas, serviços
- **Detalhes da Rede** - Portas específicas com banners

### **Funcionalidades**
- **Exportação JSON** - Download dos dados brutos
- **Impressão** - Versão para impressão
- **Responsivo** - Funciona em celulares e tablets
- **Atualização** - Recarregar dados facilmente

## ⚙️ Configurações Avançadas

### Performance
```bash
# Alta performance (rede local)
python main.py --scan 192.168.1.0/24 --threads 300 --timeout 0.5

# Balanceado (rede corporativa)
python main.py --scan 10.0.0.0/24 --threads 150 --timeout 1.0

# Conservador (internet)
python main.py --scan 203.0.113.0/24 --threads 50 --timeout 2.0
```

### Portas Customizadas
```bash
# Portas específicas
python main.py --scan 192.168.1.1 --ports 80,443,3389,22,21

# Faixa de portas
python main.py --scan 192.168.1.1 --ports 1-1000

# Portas comuns + customizadas
python main.py --scan 192.168.1.1 --ports 21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,3389,5432,3306
```

## 🎯 Exemplos Práticos

### Descoberta de Rede
```bash
# Descobrir todos os dispositivos na rede local
python scanner.py
# Escolha opção 3
# Digite: 192.168.1.0/24
```

### Auditoria de Servidor
```bash
# Scan completo de servidor web
python scanner.py
# Escolha opção 2
# Alvo: 192.168.1.100
# Portas: 80,443,22,3389,21
```

### Verificação de Segurança
```bash
# Análise completa de segurança do PC
python scanner.py
# Escolha opção 5 (Scan Completo)
# Configure conforme necessário
```

### Relatório Executivo
```bash
# Gerar relatório para apresentação
python main.py --scan 192.168.1.0/24 --report-only --export-json auditoria_2024.json
```

## 📈 Sistema de Risco

### Pontuação
```
Score = (Críticos × 25) + (Altos × 15) + (Médios × 8) + (Baixos × 3)
Máximo: 100 pontos
```

### Níveis de Risco
- **0-10**: Mínimo ✅
- **11-25**: Baixo ⚠️
- **26-50**: Médio 🔶
- **51-75**: Alto 🔴
- **76-100**: Crítico 🚨

### Fatores de Risco
- **Crítico (25 pts)**: Firewall desativado, sem antivírus, RDP exposto
- **Alto (15 pts)**: Serviços não criptografados, portas de alto risco
- **Médio (8 pts)**: Múltiplas portas abertas, sem criptografia
- **Baixo (3 pts)**: Configurações menores de segurança

## 🔧 Solução de Problemas

### Problemas Comuns

**"Permissão negada"**
```bash
# Windows: Execute como Administrador
# Linux/Mac: sudo python scanner.py
```

**"Windows não detectado"**
```bash
# Execute como Administrador
# Verifique se os comandos systeminfo e reg estão disponíveis
```

**"Scan lento"**
```bash
# Reduza o número de threads
python scanner.py
# Use timeout maior para redes lentas
```

**"Módulo não encontrado"**
```bash
# Instale dependências
pip install colorama requests
```

### Dicas de Performance

1. **Rede Local**: Use 100-200 threads, timeout 0.5s
2. **Rede Corporativa**: Use 50-150 threads, timeout 1.0s
3. **Internet**: Use 20-50 threads, timeout 2.0s
4. **Portas Específicas**: Scan apenas portas necessárias

## 🔒 Considerações de Segurança

### Uso Autorizado
- **Apenas redes autorizadas** - Scan apenas redes que você possui ou tem permissão
- **Impacto na rede** - High thread counts podem afetar performance
- **Regras de firewall** - Scans podem trigger alertas de segurança
- **Privacidade de dados** - Relatórios contêm informações sensíveis

### Boas Práticas
- Use responsavelmente
- Respeite políticas de segurança
- Não use em redes de terceiros sem permissão
- Mantenha relatórios seguros

## 📁 Estrutura de Arquivos

```
PurpleScan/
├── scanner.py              # Script único em português
├── main.py                # CLI avançada (inglês)
├── network.py             # Módulo de scanner de rede
├── system.py              # Módulo de análise do sistema
├── report.py             # Módulo de geração de relatórios
├── requirements.txt       # Dependências Python
├── README.md            # Versão original (inglês)
├── README_BR.md         # Este arquivo (português)
├── COMO_USAR.md        # Guia rápido em português
└── PurpleScan.py        # Versão original (mantida)
```

## 🚀 Comandos Úteis

### Verificação
```bash
# Verificar dependências
pip list | grep -E "(colorama|requests)"

# Verificar arquivos gerados
ls -la *.html *.json

# Testar módulos
python -c "import network, system, report; print('OK')"
```

### Execução
```bash
# Abrir dashboard manualmente
start purplescan_dashboard.html     # Windows
open purplescan_dashboard.html       # Mac
xdg-open purplescan_dashboard.html  # Linux

# Executar com Python específico
python3 scanner.py
```

## 📝 Logs e Saída

### Formato de Saída
```
[VERIFICAÇÃO] Verificando dependências...
[OK] Todas as dependências verificadas
[SISTEMA] Analisando sistema local...
[REDE] Iniciando scan de rede...
[RELATÓRIO] Gerando relatórios de segurança...
[CONCLUÍDO] PurpleScan finalizado com sucesso!
```

### Arquivos de Log
- **Console**: Saída em tempo real com cores
- **HTML**: Dashboard interativo com gráficos
- **JSON**: Dados estruturados para automação

## 🤝 Contribuição

### Como Contribuir
1. Fork do repositório
2. Criar branch de feature
3. Submit de pull request
4. Seguir padrões de código

### Relatórios de Issues
- Bugs e erros
- Sugestões de melhorias
- Novas funcionalidades
- Problemas de documentação

## 📄 Licença

MIT License - Uso livre para fins educacionais e profissionais

## 🆘 Suporte

### Recursos
- **Documentação**: README_BR.md e COMO_USAR.md
- **Issues**: GitHub Issues para problemas
- **Comunidade**: Fórum e discussões

### Contato
- **GitHub**: Issues e pull requests
- **Documentação**: Arquivos .md no repositório

---

## 🎉 PurpleScan v2.0

**Scanner • Análise • Risco • Dashboard - Tudo em Português!** 🚀
