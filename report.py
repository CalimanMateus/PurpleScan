import json
import webbrowser
from datetime import datetime
from colorama import Fore, Style
import os

class ReportGenerator:
    def __init__(self):
        self.report_data = {}
        self.html_template = ""
        self.chart_js_included = True

    def generate_risk_score(self, risks):
        """Calculate risk score from risk analysis"""
        score_weights = {
            'critical': 25,
            'high': 15,
            'medium': 8,
            'low': 3,
            'info': 0
        }
        
        total_score = 0
        max_score = 100
        
        for severity, items in risks.items():
            total_score += len(items) * score_weights.get(severity, 0)
        
        return min(total_score, max_score)

    def get_risk_level(self, score):
        """Determine risk level from score"""
        if score >= 75:
            return {"level": "CRITICAL", "color": "#ff4d4d", "bg_color": "#2d0000"}
        elif score >= 50:
            return {"level": "HIGH", "color": "#ff8c00", "bg_color": "#2d1a00"}
        elif score >= 25:
            return {"level": "MEDIUM", "color": "#ffd633", "bg_color": "#2d2d00"}
        elif score >= 10:
            return {"level": "LOW", "color": "#66ff99", "bg_color": "#002d00"}
        else:
            return {"level": "MINIMAL", "color": "#66d9ff", "bg_color": "#001a2d"}

    def prepare_report_data(self, system_info, security_status, network_results, risks):
        """Prepare comprehensive report data"""
        self.report_data = {
            'metadata': {
                'scan_time': datetime.now().isoformat(),
                'scanner': 'PurpleScan v2.0',
                'report_version': '2.0'
            },
            'system': system_info,
            'security': security_status,
            'network': network_results,
            'risks': risks,
            'risk_score': self.generate_risk_score(risks),
            'summary': self._generate_summary(system_info, security_status, network_results, risks)
        }

    def _generate_summary(self, system_info, security_status, network_results, risks):
        """Generate executive summary"""
        total_hosts = len(network_results)
        total_open_ports = sum(len(ports) for ports in network_results.values())
        
        # Count services
        service_counts = {}
        for host, ports in network_results.items():
            for port_info in ports:
                service = port_info['service']
                service_counts[service] = service_counts.get(service, 0) + 1
        
        return {
            'total_hosts_scanned': total_hosts,
            'total_open_ports': total_open_ports,
            'unique_services': len(service_counts),
            'top_services': dict(sorted(service_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            'security_status': {
                'firewall_enabled': security_status['firewall']['enabled'],
                'antivirus_enabled': security_status['antivirus']['enabled'],
                'encryption_enabled': security_status['disk_encryption']['enabled']
            },
            'risk_distribution': {k: len(v) for k, v in risks.items()}
        }

    def generate_html_dashboard(self, output_file="purplescan_dashboard.html"):
        """Generate modern HTML dashboard with Chart.js"""
        if not self.report_data:
            raise ValueError("No report data available. Call prepare_report_data() first.")

        risk_info = self.get_risk_level(self.report_data['risk_score'])
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PurpleScan - Dashboard de Segurança</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a14 0%, #1a1a2e 100%);
            color: #e0e0e0;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(187, 134, 252, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(187, 134, 252, 0.3);
        }}
        
        .header h1 {{
            color: #bb86fc;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(187, 134, 252, 0.5);
        }}
        
        .header p {{
            color: #aaa;
            font-size: 1.1em;
        }}
        
        .risk-score {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .score-display {{
            display: inline-block;
            padding: 30px 50px;
            background: {risk_info['bg_color']};
            border: 2px solid {risk_info['color']};
            border-radius: 20px;
            box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
        }}
        
        .score-number {{
            font-size: 4em;
            font-weight: bold;
            color: {risk_info['color']};
            margin-bottom: 10px;
        }}
        
        .score-label {{
            font-size: 1.5em;
            color: {risk_info['color']};
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: rgba(30, 30, 50, 0.8);
            border: 1px solid rgba(187, 134, 252, 0.2);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        }}
        
        .card h2 {{
            color: #bb86fc;
            margin-bottom: 20px;
            font-size: 1.5em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        
        .status-enabled {{
            background: #66ff99;
            box-shadow: 0 0 10px #66ff99;
        }}
        
        .status-disabled {{
            background: #ff4d4d;
            box-shadow: 0 0 10px #ff4d4d;
        }}
        
        .risk-item {{
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 8px;
            border-left: 4px solid;
        }}
        
        .risk-critical {{
            background: rgba(255, 77, 77, 0.1);
            border-color: #ff4d4d;
        }}
        
        .risk-high {{
            background: rgba(255, 140, 0, 0.1);
            border-color: #ff8c00;
        }}
        
        .risk-medium {{
            background: rgba(255, 214, 51, 0.1);
            border-color: #ffd633;
        }}
        
        .risk-low {{
            background: rgba(102, 255, 153, 0.1);
            border-color: #66ff99;
        }}
        
        .chart-container {{
            position: relative;
            height: 300px;
            margin-top: 20px;
        }}
        
        .network-item {{
            padding: 10px;
            margin: 5px 0;
            background: rgba(187, 134, 252, 0.05);
            border-radius: 8px;
            border-left: 3px solid #bb86fc;
        }}
        
        .port-info {{
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #aaa;
        }}
        
        .summary-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 15px;
            background: rgba(187, 134, 252, 0.1);
            border-radius: 10px;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #bb86fc;
        }}
        
        .stat-label {{
            color: #aaa;
            font-size: 0.9em;
        }}
        
        .export-buttons {{
            text-align: center;
            margin-top: 30px;
        }}
        
        .btn {{
            background: linear-gradient(45deg, #bb86fc, #7b2cbf);
            color: white;
            border: none;
            padding: 12px 25px;
            margin: 0 10px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(187, 134, 252, 0.4);
        }}
        
        .banner {{
            background: linear-gradient(45deg, #ff4d4d, #ff8c00, #ffd633);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: bold;
        }}
        
        @media (max-width: 768px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
            .container {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> PurpleScan Dashboard de Segurança</h1>
            <p>Relatório Avançado de Avaliação de Vulnerabilidades</p>
            <p><small>Gerado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
        </div>

        <div class="risk-score">
            <div class="score-display">
                <div class="score-number">{self.report_data['risk_score']}</div>
                <div class="score-label">{risk_info['level']} RISK</div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h2> Informações do Sistema</h2>
                <p><strong>Hostname:</strong> {self.report_data['system'].get('hostname', 'Desconhecido')}</p>
                <p><strong>Plataforma:</strong> {self.report_data['system'].get('platform', 'Desconhecida')} {self.report_data['system'].get('platform_release', '')}</p>
                <p><strong>Arquitetura:</strong> {self.report_data['system'].get('architecture', 'Desconhecida')}</p>
                <p><strong>Sistema Operacional:</strong> {self.report_data['system'].get('os_name', 'Desconhecido')}</p>
            </div>

            <div class="card">
                <h2> Status de Segurança</h2>
                <p>
                    <span class="status-indicator {'status-enabled' if self.report_data['security']['firewall']['enabled'] else 'status-disabled'}"></span>
                    <strong>Firewall:</strong> {self.report_data['security']['firewall']['details']}
                </p>
                <p>
                    <span class="status-indicator {'status-enabled' if self.report_data['security']['antivirus']['enabled'] else 'status-disabled'}"></span>
                    <strong>Antivírus:</strong> {self.report_data['security']['antivirus']['name']}
                </p>
                <p>
                    <span class="status-indicator {'status-enabled' if self.report_data['security']['disk_encryption']['enabled'] else 'status-disabled'}"></span>
                    <strong>Criptografia:</strong> {self.report_data['security']['disk_encryption']['type']}
                </p>
            </div>

            <div class="card">
                <h2> Análise de Risco</h2>
                <div class="chart-container">
                    <canvas id="riskChart"></canvas>
                </div>
                <div style="margin-top: 20px;">
                    {self._format_risks_html()}
                </div>
            </div>

            <div class="card">
                <h2> Resumo da Rede</h2>
                <div class="summary-stats">
                    <div class="stat-item">
                        <div class="stat-number">{self.report_data['summary']['total_hosts_scanned']}</div>
                        <div class="stat-label">Hosts</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{self.report_data['summary']['total_open_ports']}</div>
                        <div class="stat-label">Portas Abertas</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{self.report_data['summary']['unique_services']}</div>
                        <div class="stat-label">Serviços</div>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="serviceChart"></canvas>
                </div>
            </div>

            <div class="card" style="grid-column: 1 / -1;">
                <h2> Detalhes da Rede</h2>
                {self._format_network_html()}
            </div>
        </div>

        <div class="export-buttons">
            <button class="btn" onclick="exportJSON()">Exportar JSON</button>
            <button class="btn" onclick="window.print()">Imprimir Relatório</button>
            <button class="btn" onclick="location.reload()">Atualizar</button>
        </div>
    </div>

    <script>
        // Risk Distribution Chart
        const riskCtx = document.getElementById('riskChart').getContext('2d');
        const riskChart = new Chart(riskCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Crítico', 'Alto', 'Médio', 'Baixo', 'Info'],
                datasets: [{{
                    data: [
                        {len(self.report_data['risks']['critical'])},
                        {len(self.report_data['risks']['high'])},
                        {len(self.report_data['risks']['medium'])},
                        {len(self.report_data['risks']['low'])},
                        {len(self.report_data['risks']['info'])}
                    ],
                    backgroundColor: ['#ff4d4d', '#ff8c00', '#ffd633', '#66ff99', '#66d9ff'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            color: '#e0e0e0'
                        }}
                    }}
                }}
            }}
        }});

        // Services Chart
        const serviceCtx = document.getElementById('serviceChart').getContext('2d');
        const serviceChart = new Chart(serviceCtx, {{
            type: 'bar',
            data: {{
                labels: {list(self.report_data['summary']['top_services'].keys()) if self.report_data['summary']['top_services'] else ['Nenhum']},
                datasets: [{{
                    label: 'Contagem de Serviços',
                    data: {list(self.report_data['summary']['top_services'].values()) if self.report_data['summary']['top_services'] else [0]},
                    backgroundColor: 'rgba(187, 134, 252, 0.6)',
                    borderColor: '#bb86fc',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            color: '#e0e0e0'
                        }},
                        grid: {{
                            color: 'rgba(255, 255, 255, 0.1)'
                        }}
                    }},
                    x: {{
                        ticks: {{
                            color: '#e0e0e0'
                        }},
                        grid: {{
                            color: 'rgba(255, 255, 255, 0.1)'
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});

        // Export functions
        function exportJSON() {{
            const data = {json.dumps(self.report_data, indent=2)};
            const blob = new Blob([data], {{type: 'application/json'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'purplescan_report.json';
            a.click();
        }}

        // Auto-refresh every 5 minutes
        setTimeout(() => {{
            console.log('Dashboard ready');
        }}, 1000);
    </script>
</body>
</html>
        """

        # Write HTML file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"{Fore.GREEN}[DASHBOARD] Generated: {output_file}")
            return output_file
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to generate dashboard: {e}")
            return None

    def _format_risks_html(self):
        """Format risks for HTML display"""
        html = ""
        
        risk_labels = {
            'critical': 'CRÍTICO',
            'high': 'ALTO', 
            'medium': 'MÉDIO',
            'low': 'BAIXO'
        }
        
        for severity in ['critical', 'high', 'medium', 'low']:
            risks = self.report_data['risks'].get(severity, [])
            if risks:
                html += f"<div class='risk-item risk-{severity}'>"
                html += f"<strong>{risk_labels[severity]} ({len(risks)}):</strong><ul>"
                for risk in risks[:5]:  # Limit to first 5
                    html += f"<li>{risk}</li>"
                if len(risks) > 5:
                    html += f"<li><em>... e mais {len(risks) - 5} riscos</em></li>"
                html += "</ul></div>"
                
        if not any(self.report_data['risks'].values()):
            html = "<div class='risk-item risk-low'><strong>NENHUM RISCO DETECTADO</strong></div>"
            
        return html

    def _format_network_html(self):
        """Format network results for HTML display"""
        html = ""
        
        if not self.report_data['network']:
            html = "<div class='network-item'><strong>Nenhuma porta aberta encontrada</strong></div>"
            return html
            
        for host, ports in self.report_data['network'].items():
            html += f"<div class='network-item'>"
            html += f"<strong>{host}</strong><br>"
            
            if not ports:
                html += f"<div class='port-info'>Nenhuma porta aberta</div>"
            else:
                for port_info in ports[:10]:  # Limit to first 10 ports
                    banner = port_info.get('banner', 'Sem banner')[:50]
                    html += f"<div class='port-info'>{port_info['port']}/{port_info['service']} - {banner}</div>"
                if len(ports) > 10:
                    html += f"<div class='port-info'><em>... e mais {len(ports) - 10} portas</em></div>"
                    
            html += "</div>"
        return html

    def export_json_report(self, filename="purplescan_report.json"):
        """Export complete report as JSON"""
        if not self.report_data:
            raise ValueError("No report data available. Call prepare_report_data() first.")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.report_data, f, indent=2, ensure_ascii=False)
            print(f"{Fore.GREEN}[EXPORT] JSON report saved: {filename}")
            return filename
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to export JSON: {e}")
            return None

    def open_dashboard(self, dashboard_file):
        """Open dashboard in default browser"""
        try:
            webbrowser.open(f'file://{os.path.abspath(dashboard_file)}')
            print(f"{Fore.GREEN}[BROWSER] Dashboard opened: {dashboard_file}")
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Could not open browser: {e}")

    def generate_executive_summary(self):
        """Generate text-based executive summary"""
        if not self.report_data:
            return "No data available"

        summary = f"""
PURPLESCAN SECURITY REPORT
{'='*50}

Scan Date: {self.report_data['metadata']['scan_time']}
Risk Score: {self.report_data['risk_score']}/100 ({self.get_risk_level(self.report_data['risk_score'])['level']})

EXECUTIVE SUMMARY:
- Hosts Scanned: {self.report_data['summary']['total_hosts_scanned']}
- Total Open Ports: {self.report_data['summary']['total_open_ports']}
- Unique Services: {self.report_data['summary']['unique_services']}

SECURITY POSTURE:
- Firewall: {'ENABLED' if self.report_data['summary']['security_status']['firewall_enabled'] else 'DISABLED'}
- Antivirus: {'ACTIVE' if self.report_data['summary']['security_status']['antivirus_enabled'] else 'INACTIVE'}
- Disk Encryption: {'ENABLED' if self.report_data['summary']['security_status']['encryption_enabled'] else 'DISABLED'}

RISK BREAKDOWN:
- Critical: {len(self.report_data['risks']['critical'])} issues
- High: {len(self.report_data['risks']['high'])} issues
- Medium: {len(self.report_data['risks']['medium'])} issues
- Low: {len(self.report_data['risks']['low'])} issues

TOP SERVICES:
{chr(10).join([f"- {k}: {v}" for k, v in list(self.report_data['summary']['top_services'].items())[:5]])}

RECOMMENDATIONS:
{'-'*50}
"""
        
        # Add specific recommendations based on risks
        if not self.report_data['summary']['security_status']['firewall_enabled']:
            summary += "- Enable firewall protection immediately\n"
        
        if not self.report_data['summary']['security_status']['antivirus_enabled']:
            summary += "- Install and configure antivirus software\n"
        
        if not self.report_data['summary']['security_status']['encryption_enabled']:
            summary += "- Consider enabling disk encryption for sensitive data\n"
        
        if len(self.report_data['risks']['critical']) > 0:
            summary += "- Address critical vulnerabilities immediately\n"
        
        return summary
