#!/usr/bin/env python3
"""
PurpleScan v2.0 - Scanner de Vulnerabilidades
Script único de execução em português
"""

import os
import sys
from datetime import datetime

# Verificar dependências
try:
    import colorama
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("ERRO: Instale colorama com: pip install colorama")
    sys.exit(1)

# Importar módulos
try:
    from network import NetworkScanner
    from system import SystemAnalyzer
    from report import ReportGenerator
except ImportError as e:
    print(f"ERRO: Não foi possível importar módulos: {e}")
    print("Certifique-se de que os arquivos network.py, system.py e report.py existem")
    sys.exit(1)

def menu_principal():
    """Menu principal em português"""
    print(f"""
{Fore.MAGENTA}{'='*50}
{Fore.MAGENTA}    PURPLESCAN v2.0 - Menu Principal
{Fore.MAGENTA}{'='*50}
{Fore.CYAN}1. Scan Rápido (localhost)
{Fore.CYAN}2. Scan Personalizado
{Fore.CYAN}3. Scan de Rede Completa
{Fore.CYAN}4. Apenas Relatório do Sistema
{Fore.CYAN}5. Scan Completo (Tudo em Um)
{Fore.CYAN}6. Sair
{Fore.MAGENTA}{'='*50}{Style.RESET_ALL}
    """)
    
    while True:
        try:
            opcao = input(f"{Fore.YELLOW}[ESCOLHA] Digite uma opção (1-6): {Style.RESET_ALL}").strip()
            if opcao in ['1', '2', '3', '4', '5', '6']:
                return opcao
            else:
                print(f"{Fore.RED}[ERRO] Opção inválida!{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[CANCELADO] Operação cancelada{Style.RESET_ALL}")
            return '6'

def scan_rapido():
    """Scan rápido de localhost"""
    print(f"\n{Fore.CYAN}[SCAN RÁPIDO] Iniciando scan de localhost...{Style.RESET_ALL}")
    
    scanner = NetworkScanner(timeout=0.5, max_threads=50)
    analyzer = SystemAnalyzer()
    reporter = ReportGenerator()
    
    # Análise do sistema
    print(f"{Fore.YELLOW}[SISTEMA] Analisando sistema local...{Style.RESET_ALL}")
    system_info = analyzer.get_system_info()
    security_status = analyzer.get_security_summary()
    
    # Scan de rede
    print(f"{Fore.YELLOW}[REDE] Escaneando localhost...{Style.RESET_ALL}")
    network_results = scanner.network_scan("127.0.0.1/32")
    
    # Gerar relatório
    print(f"{Fore.YELLOW}[RELATÓRIO] Gerando dashboard...{Style.RESET_ALL}")
    risks = analyzer.analyze_security_risks(security_status, network_results)
    reporter.prepare_report_data(system_info, security_status, network_results, risks)
    
    dashboard_file = reporter.generate_html_dashboard()
    json_file = reporter.export_json_report()
    
    # Exibir resumo
    risk_score = reporter.generate_risk_score(risks)
    risk_level = reporter.get_risk_level(risk_score)
    
    print(f"\n{Fore.GREEN}[CONCLUÍDO] Scan rápido finalizado!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[RISCO] Nível: {risk_level['level']} ({risk_score}/100){Style.RESET_ALL}")
    print(f"{Fore.CYAN}[ARQUIVOS] Dashboard: {dashboard_file}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[ARQUIVOS] JSON: {json_file}{Style.RESET_ALL}")
    
    # Abrir dashboard
    try:
        import webbrowser
        webbrowser.open(f'file://{os.path.abspath(dashboard_file)}')
        print(f"{Fore.GREEN}[BROWSER] Dashboard aberto no navegador{Style.RESET_ALL}")
    except:
        print(f"{Fore.YELLOW}[AVISO] Não foi possível abrir o navegador automaticamente{Style.RESET_ALL}")

def scan_personalizado():
    """Scan personalizado"""
    print(f"\n{Fore.CYAN}[SCAN PERSONALIZADO] Configure seu scan{Style.RESET_ALL}")
    
    # Obter alvo
    while True:
        target = input(f"{Fore.YELLOW}[ALVO] Digite o IP/CIDR (ex: 192.168.1.1 ou 192.168.1.0/24): {Style.RESET_ALL}").strip()
        if target:
            break
        print(f"{Fore.RED}[ERRO] Digite um alvo válido{Style.RESET_ALL}")
    
    # Obter portas
    portas_input = input(f"{Fore.YELLOW}[PORTAS] Digite as portas (ex: 80,443,3389 ou 1-1000) [Enter para padrão]: {Style.RESET_ALL}").strip()
    
    if portas_input:
        if '-' in portas_input:
            try:
                start, end = map(int, portas_input.split('-'))
                ports = list(range(start, min(end + 1, 65536)))
            except:
                print(f"{Fore.RED}[ERRO] Faixa inválida, usando portas padrão{Style.RESET_ALL}")
                ports = None
        else:
            try:
                ports = [int(p.strip()) for p in portas_input.split(',')]
            except:
                print(f"{Fore.RED}[ERRO] Lista inválida, usando portas padrão{Style.RESET_ALL}")
                ports = None
    else:
        ports = None
    
    # Obter threads
    try:
        threads = int(input(f"{Fore.YELLOW}[THREADS] Número de threads [Enter para 100]: {Style.RESET_ALL}").strip() or "100")
    except:
        threads = 100
    
    # Obter timeout
    try:
        timeout = float(input(f"{Fore.YELLOW}[TIMEOUT] Timeout em segundos [Enter para 1.0]: {Style.RESET_ALL}").strip() or "1.0")
    except:
        timeout = 1.0
    
    # Executar scan
    print(f"\n{Fore.CYAN}[EXECUTANDO] Iniciando scan personalizado...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[CONFIG] Alvo: {target}, Threads: {threads}, Timeout: {timeout}s{Style.RESET_ALL}")
    
    scanner = NetworkScanner(timeout=timeout, max_threads=threads)
    analyzer = SystemAnalyzer()
    reporter = ReportGenerator()
    
    if ports:
        scanner.common_ports = ports
    
    # Análise do sistema
    print(f"{Fore.YELLOW}[SISTEMA] Analisando sistema...{Style.RESET_ALL}")
    system_info = analyzer.get_system_info()
    security_status = analyzer.get_security_summary()
    
    # Scan de rede
    print(f"{Fore.YELLOW}[REDE] Escaneando {target}...{Style.RESET_ALL}")
    network_results = scanner.network_scan(target, ports)
    
    # Gerar relatório
    print(f"{Fore.YELLOW}[RELATÓRIO] Gerando dashboard...{Style.RESET_ALL}")
    risks = analyzer.analyze_security_risks(security_status, network_results)
    reporter.prepare_report_data(system_info, security_status, network_results, risks)
    
    dashboard_file = reporter.generate_html_dashboard()
    json_file = reporter.export_json_report()
    
    # Exibir resumo
    risk_score = reporter.generate_risk_score(risks)
    risk_level = reporter.get_risk_level(risk_score)
    
    print(f"\n{Fore.GREEN}[CONCLUÍDO] Scan personalizado finalizado!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[RISCO] Nível: {risk_level['level']} ({risk_score}/100){Style.RESET_ALL}")
    print(f"{Fore.CYAN}[ARQUIVOS] Dashboard: {dashboard_file}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[ARQUIVOS] JSON: {json_file}{Style.RESET_ALL}")
    
    # Abrir dashboard
    try:
        import webbrowser
        webbrowser.open(f'file://{os.path.abspath(dashboard_file)}')
        print(f"{Fore.GREEN}[BROWSER] Dashboard aberto no navegador{Style.RESET_ALL}")
    except:
        print(f"{Fore.YELLOW}[AVISO] Não foi possível abrir o navegador automaticamente{Style.RESET_ALL}")

def scan_rede_completa():
    """Scan completo de rede"""
    print(f"\n{Fore.CYAN}[SCAN DE REDE] Scan completo de rede{Style.RESET_ALL}")
    
    # Obter rede
    while True:
        rede = input(f"{Fore.YELLOW}[REDE] Digite a rede (ex: 192.168.1.0/24): {Style.RESET_ALL}").strip()
        if rede:
            break
        print(f"{Fore.RED}[ERRO] Digite uma rede válida{Style.RESET_ALL}")
    
    # Configurações de performance
    try:
        threads = int(input(f"{Fore.YELLOW}[THREADS] Número de threads [Enter para 200]: {Style.RESET_ALL}").strip() or "200")
    except:
        threads = 200
    
    try:
        timeout = float(input(f"{Fore.YELLOW}[TIMEOUT] Timeout em segundos [Enter para 0.5]: {Style.RESET_ALL}").strip() or "0.5")
    except:
        timeout = 0.5
    
    print(f"\n{Fore.YELLOW}[AVISO] Scan de rede pode demorar. Pressione Ctrl+C para cancelar.{Style.RESET_ALL}")
    
    # Executar scan
    scanner = NetworkScanner(timeout=timeout, max_threads=threads)
    analyzer = SystemAnalyzer()
    reporter = ReportGenerator()
    
    # Análise do sistema
    print(f"{Fore.YELLOW}[SISTEMA] Analisando sistema...{Style.RESET_ALL}")
    system_info = analyzer.get_system_info()
    security_status = analyzer.get_security_summary()
    
    # Scan de rede
    print(f"{Fore.YELLOW}[REDE] Escaneando rede {rede}...{Style.RESET_ALL}")
    network_results = scanner.network_scan(rede)
    
    # Gerar relatório
    print(f"{Fore.YELLOW}[RELATÓRIO] Gerando dashboard...{Style.RESET_ALL}")
    risks = analyzer.analyze_security_risks(security_status, network_results)
    reporter.prepare_report_data(system_info, security_status, network_results, risks)
    
    dashboard_file = reporter.generate_html_dashboard()
    json_file = reporter.export_json_report()
    
    # Exibir resumo
    risk_score = reporter.generate_risk_score(risks)
    risk_level = reporter.get_risk_level(risk_score)
    
    print(f"\n{Fore.GREEN}[CONCLUÍDO] Scan de rede finalizado!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[RISCO] Nível: {risk_level['level']} ({risk_score}/100){Style.RESET_ALL}")
    print(f"{Fore.CYAN}[ARQUIVOS] Dashboard: {dashboard_file}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[ARQUIVOS] JSON: {json_file}{Style.RESET_ALL}")
    
    # Abrir dashboard
    try:
        import webbrowser
        webbrowser.open(f'file://{os.path.abspath(dashboard_file)}')
        print(f"{Fore.GREEN}[BROWSER] Dashboard aberto no navegador{Style.RESET_ALL}")
    except:
        print(f"{Fore.YELLOW}[AVISO] Não foi possível abrir o navegador automaticamente{Style.RESET_ALL}")

def relatorio_sistema():
    """Apenas relatório do sistema"""
    print(f"\n{Fore.CYAN}[RELATÓRIO] Gerando relatório do sistema{Style.RESET_ALL}")
    
    analyzer = SystemAnalyzer()
    reporter = ReportGenerator()
    
    # Análise do sistema
    print(f"{Fore.YELLOW}[SISTEMA] Analisando sistema...{Style.RESET_ALL}")
    system_info = analyzer.get_system_info()
    security_status = analyzer.get_security_summary()
    
    # Gerar relatório sem scan de rede
    print(f"{Fore.YELLOW}[RELATÓRIO] Gerando dashboard...{Style.RESET_ALL}")
    risks = analyzer.analyze_security_risks(security_status, {})
    reporter.prepare_report_data(system_info, security_status, {}, risks)
    
    dashboard_file = reporter.generate_html_dashboard()
    json_file = reporter.export_json_report()
    
    # Exibir resumo
    risk_score = reporter.generate_risk_score(risks)
    risk_level = reporter.get_risk_level(risk_score)
    
    print(f"\n{Fore.GREEN}[CONCLUÍDO] Relatório do sistema finalizado!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[RISCO] Nível: {risk_level['level']} ({risk_score}/100){Style.RESET_ALL}")
    print(f"{Fore.CYAN}[ARQUIVOS] Dashboard: {dashboard_file}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[ARQUIVOS] JSON: {json_file}{Style.RESET_ALL}")
    
    # Abrir dashboard
    try:
        import webbrowser
        webbrowser.open(f'file://{os.path.abspath(dashboard_file)}')
        print(f"{Fore.GREEN}[BROWSER] Dashboard aberto no navegador{Style.RESET_ALL}")
    except:
        print(f"{Fore.YELLOW}[AVISO] Não foi possível abrir o navegador automaticamente{Style.RESET_ALL}")

def scan_completo():
    """Scan completo - Combina todas as 4 funcionalidades"""
    print(f"\n{Fore.MAGENTA}[SCAN COMPLETO] Análise de Segurança Completa{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Este scan combina: Sistema + Rede + Risco + Relatório{Style.RESET_ALL}")
    
    # Obter configurações
    print(f"\n{Fore.CYAN}[CONFIGURAÇÃO] Configure o scan completo{Style.RESET_ALL}")
    
    # Alvo principal
    while True:
        alvo_principal = input(f"{Fore.YELLOW}[ALVO PRINCIPAL] IP/CIDR principal [Enter para localhost]: {Style.RESET_ALL}").strip()
        if alvo_principal or alvo_principal == "":
            if alvo_principal == "":
                alvo_principal = "127.0.0.1/32"
            break
        print(f"{Fore.RED}[ERRO] Digite um alvo válido{Style.RESET_ALL}")
    
    # Rede adicional (opcional)
    rede_adicional = input(f"{Fore.YELLOW}[REDE ADICIONAL] Outra rede para scan [Enter para pular]: {Style.RESET_ALL}").strip()
    
    # Portas customizadas
    portas_input = input(f"{Fore.YELLOW}[PORTAS] Portas específicas [Enter para todas principais]: {Style.RESET_ALL}").strip()
    
    if portas_input:
        if '-' in portas_input:
            try:
                start, end = map(int, portas_input.split('-'))
                ports = list(range(start, min(end + 1, 65536)))
            except:
                print(f"{Fore.RED}[ERRO] Faixa inválida, usando portas padrão{Style.RESET_ALL}")
                ports = None
        else:
            try:
                ports = [int(p.strip()) for p in portas_input.split(',')]
            except:
                print(f"{Fore.RED}[ERRO] Lista inválida, usando portas padrão{Style.RESET_ALL}")
                ports = None
    else:
        ports = None
    
    # Performance
    try:
        threads = int(input(f"{Fore.YELLOW}[THREADS] Threads [Enter para 150]: {Style.RESET_ALL}").strip() or "150")
    except:
        threads = 150
    
    try:
        timeout = float(input(f"{Fore.YELLOW}[TIMEOUT] Timeout [Enter para 1.0]: {Style.RESET_ALL}").strip() or "1.0")
    except:
        timeout = 1.0
    
    print(f"\n{Fore.MAGENTA}[INICIANDO] Scan completo em 3...2...1...{Style.RESET_ALL}")
    
    # Inicializar componentes
    scanner = NetworkScanner(timeout=timeout, max_threads=threads)
    analyzer = SystemAnalyzer()
    reporter = ReportGenerator()
    
    if ports:
        scanner.common_ports = ports
    
    # 1. Análise do Sistema
    print(f"\n{Fore.CYAN}[1/4] ANÁLISE DO SISTEMA{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Coletando informações do sistema local...{Style.RESET_ALL}")
    system_info = analyzer.get_system_info()
    security_status = analyzer.get_security_summary()
    installed_software = analyzer.get_installed_software(limit=20)
    print(f"{Fore.GREEN}[OK] Sistema analisado{Style.RESET_ALL}")
    
    # 2. Scan do Alvo Principal
    print(f"\n{Fore.CYAN}[2/4] SCAN DO ALVO PRINCIPAL{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Escaneando {alvo_principal}...{Style.RESET_ALL}")
    network_results = {}
    network_results[alvo_principal] = scanner.scan_host(alvo_principal.split('/')[0], ports)
    
    if network_results[alvo_principal]:
        print(f"{Fore.GREEN}[OK] Encontradas {len(network_results[alvo_principal])} portas abertas{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[INFO] Nenhuma porta aberta em {alvo_principal}{Style.RESET_ALL}")
    
    # 3. Scan de Rede Adicional (se fornecida)
    if rede_adicional:
        print(f"\n{Fore.CYAN}[3/4] SCAN DE REDE ADICIONAL{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Escaneando rede {rede_adicional}...{Style.RESET_ALL}")
        
        try:
            rede_results = scanner.network_scan(rede_adicional, ports)
            network_results.update(rede_results)
            
            total_hosts = len(rede_results)
            total_ports = sum(len(host_ports) for host_ports in rede_results.values())
            print(f"{Fore.GREEN}[OK] Scan concluído: {total_hosts} hosts, {total_ports} portas{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}[ERRO] Falha no scan de rede: {e}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.CYAN}[3/4] SCAN DE REDE ADICIONAL{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[PULADO] Nenhuma rede adicional especificada{Style.RESET_ALL}")
    
    # 4. Análise de Risco e Relatório
    print(f"\n{Fore.CYAN}[4/4] ANÁLISE DE RISCO E RELATÓRIO{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Analisando riscos e gerando relatórios...{Style.RESET_ALL}")
    
    risks = analyzer.analyze_security_risks(security_status, network_results)
    reporter.prepare_report_data(system_info, security_status, network_results, risks)
    
    dashboard_file = reporter.generate_html_dashboard()
    json_file = reporter.export_json_report()
    
    # Relatório executivo
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.MAGENTA}    RELATÓRIO EXECUTIVO - SCAN COMPLETO{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*60}")
    
    summary = reporter.generate_executive_summary()
    print(summary)
    
    # Resumo final
    risk_score = reporter.generate_risk_score(risks)
    risk_level = reporter.get_risk_level(risk_score)
    
    total_hosts = len(network_results)
    total_ports = sum(len(host_ports) for host_ports in network_results.values())
    
    print(f"\n{Fore.GREEN}{'='*60}")
    print(f"{Fore.GREEN}[SCAN COMPLETO FINALIZADO] Todos os objetivos concluídos!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[RESUMO GERAL]")
    print(f"  Sistema: {system_info.get('os_name', 'Desconhecido')}")
    print(f"  Hosts analisados: {total_hosts}")
    print(f"  Portas abertas: {total_ports}")
    print(f"  Risco geral: {risk_level['level']} ({risk_score}/100)")
    print(f"{Fore.CYAN}[ARQUIVOS GERADOS]")
    print(f"  Dashboard: {dashboard_file}")
    print(f"  JSON: {json_file}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    
    # Abrir dashboard
    try:
        import webbrowser
        webbrowser.open(f'file://{os.path.abspath(dashboard_file)}')
        print(f"{Fore.GREEN}[BROWSER] Dashboard completo aberto{Style.RESET_ALL}")
    except:
        print(f"{Fore.YELLOW}[AVISO] Abra manualmente: {dashboard_file}{Style.RESET_ALL}")
    
    # Exportações adicionais
    exportar_extra = input(f"\n{Fore.YELLOW}[EXPORTAR] Salvar cópia extra? [S/N]: {Style.RESET_ALL}").strip().upper()
    if exportar_extra == 'S':
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        extra_json = f"scan_completo_{timestamp}.json"
        reporter.export_json_report(extra_json)
        print(f"{Fore.GREEN}[EXPORT] Cópia salva: {extra_json}{Style.RESET_ALL}")

def main():
    """Função principal"""
    print(f"""
{Fore.MAGENTA}{'='*60}
{Fore.MAGENTA}    PURPLESCAN v2.0
{Fore.MAGENTA}    Scanner Profissional de Vulnerabilidades
{Fore.MAGENTA}{'='*60}
{Fore.CYAN}    Ferramenta de Segurança em Português
{Fore.CYAN}    Análise de Rede | Sistema | Risco
{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}
    """)
    
    while True:
        try:
            opcao = menu_principal()
            
            if opcao == '1':
                scan_rapido()
            elif opcao == '2':
                scan_personalizado()
            elif opcao == '3':
                scan_rede_completa()
            elif opcao == '4':
                relatorio_sistema()
            elif opcao == '5':
                scan_completo()
            elif opcao == '6':
                print(f"{Fore.GREEN}[SAIR] Obrigado por usar PurpleScan!{Style.RESET_ALL}")
                break
            
            # Pausar antes de voltar ao menu
            input(f"\n{Fore.YELLOW}[ENTER] Pressione Enter para voltar ao menu...{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[CANCELADO] Operação cancelada pelo usuário{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}[ERRO] Ocorreu um erro: {e}{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}[ENTER] Pressione Enter para continuar...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
