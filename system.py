import os
import platform
import subprocess
import json
from datetime import datetime
from colorama import Fore, Style

class SystemAnalyzer:
    def __init__(self):
        self.system_info = {}
        self.security_status = {}
        self.installed_software = []

    def run_command(self, command, shell=True):
        """Execute system command safely"""
        try:
            if platform.system() == "Windows":
                result = subprocess.check_output(command, shell=shell, text=True, 
                                               stderr=subprocess.DEVNULL, encoding='utf-8')
            else:
                result = subprocess.check_output(command, shell=shell, text=True, 
                                               stderr=subprocess.DEVNULL)
            return result.strip()
        except subprocess.CalledProcessError:
            return ""
        except Exception as e:
            return f"Error: {str(e)}"

    def get_system_info(self):
        """Collect comprehensive system information"""
        info = {
            'hostname': os.getenv('COMPUTERNAME', 'Unknown'),
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'timestamp': datetime.now().isoformat()
        }

        # Windows-specific information
        if platform.system() == "Windows":
            try:
                # Get OS details - melhor método
                cmd_output = self.run_command('systeminfo')
                for line in cmd_output.split('\n'):
                    if 'OS Name:' in line:
                        info['os_name'] = line.split(':')[1].strip() if ':' in line else 'Windows'
                    elif 'OS Version:' in line:
                        info['os_version'] = line.split(':')[1].strip() if ':' in line else 'Unknown'
                    elif 'System Type:' in line:
                        info['system_type'] = line.split(':')[1].strip() if ':' in line else 'Unknown'

                # Get Windows version via registry (mais confiável)
                reg_output = self.run_command('reg query "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" /v ProductName')
                if 'ProductName' in reg_output:
                    for line in reg_output.split('\n'):
                        if 'ProductName' in line and 'REG_SZ' in line:
                            info['os_name'] = line.split('REG_SZ')[1].strip() if 'REG_SZ' in line else info.get('os_name', 'Windows')
                            break

                # Get system uptime
                uptime = self.run_command('wmic os get lastbootuptime /value')
                if uptime and '=' in uptime:
                    info['last_boot'] = uptime.split('=')[1].strip()

            except Exception as e:
                print(f"{Fore.YELLOW}[AVISO] Não foi possível obter informações detalhadas do Windows: {e}")
                # Fallback para informações básicas
                info['os_name'] = 'Windows'
                info['os_version'] = platform.release()

        # Linux/Mac information
        else:
            try:
                info['kernel'] = self.run_command("uname -r")
                info['distro'] = self.run_command("lsb_release -d 2>/dev/null | cut -f2") or \
                               self.run_command("cat /etc/*release 2>/dev/null | grep PRETTY_NAME | cut -d'=' -f2 | tr -d '\"'")
                
                # System uptime
                uptime = self.run_command("uptime -p 2>/dev/null || uptime")
                if uptime:
                    info['uptime'] = uptime

            except Exception as e:
                print(f"{Fore.YELLOW}[AVISO] Não foi possível obter informações detalhadas do Unix: {e}")

        self.system_info = info
        return info

    def check_firewall_status(self):
        """Check firewall status across platforms"""
        status = {'enabled': False, 'details': 'Unknown'}

        if platform.system() == "Windows":
            try:
                # Check Windows Defender Firewall
                output = self.run_command("netsh advfirewall show allprofiles")
                if "State" in output and "ON" in output:
                    status['enabled'] = True
                    status['details'] = "Windows Defender Firewall"
                
                # Check domain, private, public profiles
                profiles = {}
                for profile in ["Domain", "Private", "Public"]:
                    profile_output = self.run_command(f"netsh advfirewall show {profile.lower()}profile")
                    if "State" in profile_output and "ON" in profile_output:
                        profiles[profile] = "Enabled"
                    else:
                        profiles[profile] = "Disabled"
                
                status['profiles'] = profiles

            except Exception as e:
                status['details'] = f"Erro ao verificar firewall: {e}"

        else:
            # Linux firewall checks
            try:
                # UFW (Ubuntu)
                ufw_status = self.run_command("ufw status")
                if "Status: active" in ufw_status:
                    status['enabled'] = True
                    status['details'] = "UFW Firewall"

                # iptables rules
                iptables = self.run_command("iptables -L 2>/dev/null | wc -l")
                if iptables and int(iptables) > 10:
                    status['enabled'] = True
                    status['details'] = "iptables"

            except Exception:
                pass

        return status

    def check_antivirus_status(self):
        """Check antivirus/antimalware status"""
        status = {'enabled': False, 'name': 'Unknown', 'details': 'No AV detected'}

        if platform.system() == "Windows":
            try:
                # Windows Defender
                defender_output = self.run_command("powershell \"Get-MpComputerStatus | Select-Object AMServiceEnabled, AntispywareEnabled, RealTimeProtectionEnabled\"")
                if "True" in defender_output:
                    status['enabled'] = True
                    status['name'] = "Windows Defender"
                    status['details'] = "Real-time protection enabled"

                # Check for other AV via WMI
                av_products = self.run_command("wmic /namespace:\\\\root\\securitycenter2 path antivirusproduct get displayName /format:list")
                if av_products and "DisplayName=" in av_products:
                    av_names = [line.split('=')[1] for line in av_products.split('\n') if 'DisplayName=' in line]
                    if av_names:
                        status['name'] = ", ".join(av_names[:3])  # Limit to first 3
                        status['enabled'] = True

            except Exception as e:
                status['details'] = f"Erro ao verificar antivírus: {e}"

        else:
            # Linux AV checks
            try:
                # ClamAV
                clamav = self.run_command("clamscan --version 2>/dev/null")
                if clamav:
                    status['enabled'] = True
                    status['name'] = "ClamAV"
                    status['details'] = clamav.split('\n')[0]

                # Check for common Linux AV services
                services = ["clamav-freshclam", "clamav-daemon", "malware-detect"]
                for service in services:
                    service_status = self.run_command(f"systemctl is-active {service} 2>/dev/null")
                    if "active" in service_status:
                        status['enabled'] = True
                        status['name'] = service
                        break

            except Exception:
                pass

        return status

    def check_disk_encryption(self):
        """Check disk encryption status"""
        status = {'enabled': False, 'type': 'None', 'details': 'No encryption detected'}

        if platform.system() == "Windows":
            try:
                # BitLocker
                bitlocker = self.run_command("manage-bde -status")
                if bitlocker and "Protection On" in bitlocker:
                    status['enabled'] = True
                    status['type'] = "BitLocker"
                    
                    # Parse BitLocker details
                    for line in bitlocker.split('\n'):
                        if 'Encryption Percentage:' in line:
                            status['details'] = line.split(':')[1].strip()
                            break

            except Exception:
                pass

        else:
            # Linux encryption checks
            try:
                # LUKS
                luks = self.run_command("lsblk -f | grep crypto_LUKS")
                if luks:
                    status['enabled'] = True
                    status['type'] = "LUKS"
                    status['details'] = f"Found {len(luks.split())} encrypted volumes"

                # Check for encrypted home directories
                ecryptfs = self.run_command("ecryptfs-verify -h 2>/dev/null")
                if ecryptfs and "encrypted" in ecryptfs.lower():
                    status['enabled'] = True
                    status['type'] = "eCryptfs"

            except Exception:
                pass

        return status

    def get_installed_software(self, limit=20):
        """Get list of installed software"""
        software = []

        if platform.system() == "Windows":
            try:
                # Get installed programs via WMI
                programs = self.run_command("wmic product get name,version /format:csv")
                if programs:
                    for line in programs.split('\n')[1:limit+1]:  # Skip header, limit results
                        if line.strip():
                            parts = line.split(',')
                            if len(parts) >= 3 and parts[2].strip():
                                software.append({
                                    'name': parts[2].strip(),
                                    'version': parts[3].strip() if len(parts) > 3 else 'Unknown'
                                })

                # Also check 64-bit programs
                programs64 = self.run_command("wmic product get name,version /format:csv")
                if programs64:
                    for line in programs64.split('\n')[1:limit+1]:
                        if line.strip() and line not in programs:
                            parts = line.split(',')
                            if len(parts) >= 3 and parts[2].strip():
                                software.append({
                                    'name': parts[2].strip(),
                                    'version': parts[3].strip() if len(parts) > 3 else 'Unknown'
                                })

            except Exception as e:
                print(f"{Fore.YELLOW}[AVISO] Não foi possível obter softwares instalados: {e}")

        else:
            # Linux software
            try:
                # Get installed packages (dpkg/rpm)
                if os.path.exists('/usr/bin/dpkg'):
                    packages = self.run_command("dpkg -l | grep '^ii' | head -20")
                    for line in packages.split('\n')[:limit]:
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 3:
                                software.append({
                                    'name': parts[1],
                                    'version': parts[2]
                                })

                elif os.path.exists('/bin/rpm'):
                    packages = self.run_command("rpm -qa | head -20")
                    for line in packages.split('\n')[:limit]:
                        if line.strip():
                            software.append({'name': line, 'version': 'Unknown'})

            except Exception as e:
                print(f"{Fore.YELLOW}[AVISO] Não foi possível obter pacotes Linux: {e}")

        self.installed_software = software[:limit]
        return self.installed_software

    def get_security_summary(self):
        """Get comprehensive security status"""
        return {
            'firewall': self.check_firewall_status(),
            'antivirus': self.check_antivirus_status(),
            'disk_encryption': self.check_disk_encryption(),
            'scan_time': datetime.now().isoformat()
        }

    def analyze_security_risks(self, security_info, network_results):
        """Analyze security risks based on system and network data"""
        risks = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'info': []
        }

        # Firewall risks
        if not security_info['firewall']['enabled']:
            risks['critical'].append("Firewall is disabled - system exposed to network attacks")

        # Antivirus risks
        if not security_info['antivirus']['enabled']:
            risks['critical'].append("No antivirus protection detected")
        else:
            risks['low'].append(f"Antivirus active: {security_info['antivirus']['name']}")

        # Disk encryption risks
        if not security_info['disk_encryption']['enabled']:
            risks['medium'].append("Disk encryption not enabled - data at risk if device lost")

        # Network risks
        high_risk_ports = [21, 23, 135, 139, 445, 3389, 5900]
        for host, ports in network_results.items():
            for port_info in ports:
                port = port_info['port']
                service = port_info['service']
                
                if port in high_risk_ports:
                    risks['high'].append(f"High-risk service exposed: {service} on {host}:{port}")
                
                # Specific service risks
                if service == "Telnet" and port == 23:
                    risks['critical'].append(f"Telnet (unencrypted) exposed on {host}:{port}")
                elif service == "FTP" and port == 21:
                    risks['high'].append(f"FTP (unencrypted credentials) on {host}:{port}")
                elif service == "RDP" and port == 3389:
                    risks['high'].append(f"RDP access exposed on {host}:{port}")

        # System information risks
        if platform.system() == "Windows":
            if "Home" in self.system_info.get('os_name', ''):
                risks['medium'].append("Windows Home edition - limited security features")

        return risks

    def export_system_report(self, filename="system_report.json"):
        """Export complete system analysis"""
        report = {
            'system_info': self.system_info,
            'security_status': self.get_security_summary(),
            'installed_software': self.installed_software,
            'scan_time': datetime.now().isoformat()
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"{Fore.GREEN}[EXPORT] System report saved to {filename}")
        except Exception as e:
            print(f"{Fore.RED}[ERRO] Falha ao exportar relatório do sistema: {e}")

        return report
