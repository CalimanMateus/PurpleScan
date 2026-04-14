# PurpleScan v2.0 - Como Usar

## Instalação Rápida

```bash
# 1. Instalar dependências
pip install colorama requests

# 2. Pronto! Já pode usar
```

## Formas de Usar

### **1. Script Único (Recomendado)**

```bash
# Menu interativo em português
python scanner.py
```

**Opções do Menu:**
- **1. Scan Rápido** - Scan localhost automático
- **2. Scan Personalizado** - Configure alvo, portas, threads
- **3. Scan de Rede** - Scan completo de rede (ex: 192.168.1.0/24)
- **4. Relatório do Sistema** - Apenas análise do sistema
- **5. Sair** - Fechar o programa

### **2. Linha de Comando (Avançado)**

```bash
# Scan rápido
python main.py --quick-scan

# Scan personalizado
python main.py --scan 192.168.1.1 --ports 80,443,3389

# Scan de rede
python main.py --scan 192.168.1.0/24 --threads 200

# Apenas relatório
python main.py --report-only

# Exportar JSON customizado
python main.py --scan 127.0.0.1 --export-json meu_relatorio.json
```

### **3. Exemplos Práticos**

```bash
# Scan da minha rede local
python scanner.py
# Escolha opção 3
# Digite: 192.168.1.0/24

# Scan rápido do meu PC
python scanner.py
# Escolha opção 1

# Scan de servidor específico
python scanner.py
# Escolha opção 2
# Alvo: 192.168.1.100
# Portas: 21,22,80,443,3389

# Verificar segurança do meu PC
python scanner.py
# Escolha opção 4
```

## Arquivos Gerados

Após executar, você terá:

- **`purplescan_dashboard.html`** - Dashboard interativo
- **`purplescan_report.json`** - Relatório completo em JSON
- **Arquivos customizados** - Se especificar nome diferente

## O que cada opção faz

### **Scan Rápido (Opção 1)**
- Alvo: localhost (127.0.0.1)
- Portas: Principais (HTTP, SSH, RDP, etc.)
- Tempo: ~30 segundos
- Ideal: Verificação rápida do próprio PC

### **Scan Personalizado (Opção 2)**
- Alvo: Qualquer IP ou rede
- Portas: Customizáveis
- Threads: Configurável
- Ideal: Scan específico de servidor/alvo

### **Scan de Rede (Opção 3)**
- Alvo: Rede inteira (CIDR)
- Portas: Principais
- Threads: 200 (rápido)
- Ideal: Descobrir dispositivos na rede

### **Relatório do Sistema (Opção 4)**
- Apenas análise local
- Sem scan de rede
- Tempo: ~10 segundos
- Ideal: Verificar configurações de segurança

## Dashboard HTML

O dashboard automaticamente abre no navegador com:

- **Score de Risco** (0-100)
- **Status do Sistema** - Windows, firewall, antivírus
- **Portas Abertas** - Com banners e serviços
- **Gráficos** - Distribuição de risco e serviços
- **Recomendações** - Baseadas nos riscos encontrados

## Problemas Comuns

### **"Windows 10 não detectado"**
- **Solução**: Execute como Administrador
- **Comando**: `python scanner.py` (corrigido na v2.0)

### **"Network Summary zerado"**
- **Solução**: Verifique se há portas abertas
- **Teste**: `python scanner.py` opção 1 (localhost)

### **"Permissão negada"**
- **Windows**: Execute como Administrador
- **Linux/Mac**: `sudo python scanner.py`

### **"Módulo não encontrado"**
- **Instale**: `pip install colorama requests`
- **Verifique**: Todos os arquivos estão na mesma pasta

## Dicos de Uso

### **Performance**
- **Rede local**: Use 100-200 threads
- **Internet**: Use 50-100 threads, timeout 2.0s
- **Scan rápido**: Use portas específicas

### **Segurança**
- **Apenas redes autorizadas**
- **Scan pode trigger firewalls**
- **Use com responsabilidade**

### **Resultados**
- **Score 0-25**: Seguro
- **Score 26-50**: Atenção
- **Score 51-75**: Risco alto
- **Score 76-100**: Crítico

## Comandos Úteis

```bash
# Verificar arquivos gerados
ls -la *.html *.json

# Abrir dashboard manualmente
start purplescan_dashboard.html  # Windows
open purplescan_dashboard.html    # Mac
xdg-open purplescan_dashboard.html # Linux

# Verificar dependências
pip list | grep colorama
```

## Suporte

- **Erros**: Execute como Administrador
- **Performance**: Ajuste threads e timeout
- **Permissões**: Scan apenas redes autorizadas

---

**PurpleScan v2.0** - Ferramenta brasileira de segurança!
