import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from ipaddress import ip_network
from colorama import Fore, Style
import json

class NetworkScanner:
    def __init__(self, timeout=1.0, max_threads=100):
        self.timeout = timeout
        self.max_threads = max_threads
        self.open_ports = {}
        self.service_banners = {}
        
        # Port mapping for service identification
        self.port_services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 143: "IMAP",
            443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
            1433: "MSSQL", 1521: "Oracle", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt",
            8443: "HTTPS-Alt", 9200: "Elasticsearch"
        }
        
        # Common ports to scan (prioritized)
        self.common_ports = list(self.port_services.keys()) + [
            81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
            135, 139, 389, 443, 445, 636, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9200
        ]

    def scan_port(self, ip, port):
        """Scan single port with banner grabbing"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            result = sock.connect_ex((str(ip), port))
            if result == 0:
                service = self.port_services.get(port, "Unknown")
                banner = self.grab_banner(sock, port)
                
                return {
                    'port': port,
                    'service': service,
                    'banner': banner,
                    'status': 'open'
                }
            
        except Exception:
            pass
        finally:
            try:
                sock.close()
            except:
                pass
        
        return None

    def grab_banner(self, sock, port):
        """Grab service banner from open port"""
        try:
            # Send appropriate probes based on port
            if port in [80, 8080, 8000, 8008]:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + str(sock.getpeername()[0]).encode() + b"\r\n\r\n")
            elif port in [21]:
                pass  # FTP servers send banner automatically
            elif port in [22]:
                pass  # SSH servers send banner automatically
            elif port in [25]:
                pass  # SMTP servers send banner automatically
            elif port in [110]:
                pass  # POP3 servers send banner automatically
            elif port in [143]:
                pass  # IMAP servers send banner automatically
            
            # Receive banner
            sock.settimeout(2.0)
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            
            # Clean up banner
            if banner:
                banner = banner[:200]  # Limit banner length
                banner = banner.replace('\r', '').replace('\n', ' | ')
                return banner
                
        except Exception:
            pass
        
        return "No banner"

    def scan_host(self, ip, ports=None):
        """Scan all ports on a host using threads"""
        if ports is None:
            ports = self.common_ports
            
        print(f"{Fore.CYAN}[SCANNING] {ip} - {len(ports)} ports")
        
        results = []
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            # Submit all port scans
            future_to_port = {
                executor.submit(self.scan_port, ip, port): port 
                for port in ports
            }
            
            # Process completed scans
            for future in as_completed(future_to_port):
                result = future.result()
                if result:
                    results.append(result)
                    print(f"{Fore.GREEN}[OPEN] {ip}:{result['port']} ({result['service']})")
        
        return sorted(results, key=lambda x: x['port'])

    def network_scan(self, cidr="127.0.0.1/32", ports=None):
        """Scan multiple hosts in network"""
        results = {}
        
        try:
            network = ip_network(cidr, strict=False)
            hosts = list(network)
            
            if len(hosts) > 254:
                print(f"{Fore.YELLOW}[WARNING] Large network ({len(hosts)} hosts). Scanning first 254...")
                hosts = hosts[:254]
            
            print(f"{Fore.MAGENTA}[NETWORK] Scanning {len(hosts)} hosts")
            
            for i, ip in enumerate(hosts, 1):
                print(f"{Fore.CYAN}[PROGRESS] {i}/{len(hosts)} - {ip}")
                host_results = self.scan_host(ip, ports)
                
                if host_results:
                    results[str(ip)] = host_results
                    
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Network scan failed: {e}")
        
        return results

    def export_results(self, results, filename="network_scan.json"):
        """Export scan results to JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"{Fore.GREEN}[EXPORT] Results saved to {filename}")
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to export: {e}")

    def get_scan_summary(self, results):
        """Generate scan summary statistics"""
        total_hosts = len(results)
        total_ports = sum(len(ports) for ports in results.values())
        
        service_counts = {}
        risk_ports = []
        
        for host, ports in results.items():
            for port_info in ports:
                service = port_info['service']
                service_counts[service] = service_counts.get(service, 0) + 1
                
                # High-risk ports
                if port_info['port'] in [21, 23, 135, 139, 445, 3389]:
                    risk_ports.append(f"{host}:{port_info['port']} ({service})")
        
        return {
            'total_hosts': total_hosts,
            'total_open_ports': total_ports,
            'services': service_counts,
            'high_risk_ports': risk_ports,
            'scan_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
