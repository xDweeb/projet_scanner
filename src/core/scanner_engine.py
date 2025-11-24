"""
Core scanner functions module
Contains all network scanning, system info, and utility functions
"""

import socket
import platform
import requests
import subprocess
import time

def port_scan(target, port, timeout=0.5):
    """
    Scan a single port on the target.
    Returns True if port is open, False otherwise.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def system_info():
    """
    Get system information and return as string.
    """
    try:
        info_lines = [
            "=== Informations système ===",
            f"Nom de la machine: {platform.node()}",
            f"Système: {platform.system()}",
            f"Release: {platform.release()}",
            f"Version: {platform.version()}",
            f"Architecture: {platform.machine()}",
            f"Processeur: {platform.processor()}",
            f"Python: {platform.python_version()}"
        ]
        return "\n".join(info_lines)
    except Exception as e:
        return f"Erreur lors de la récupération des informations système: {e}"

def ip_lookup(target):
    """
    Lookup IP geolocation information.
    Returns formatted string with results.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{target}", timeout=10)
        data = response.json()
        
        if data["status"] == "success":
            result_lines = [
                "=== Informations IP/Géolocalisation ===",
                f"IP: {data.get('query', 'N/A')}",
                f"Pays: {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})",
                f"Région: {data.get('regionName', 'N/A')}",
                f"Ville: {data.get('city', 'N/A')}",
                f"Code postal: {data.get('zip', 'N/A')}",
                f"ISP: {data.get('isp', 'N/A')}",
                f"Organisation: {data.get('org', 'N/A')}",
                f"Latitude: {data.get('lat', 'N/A')}",
                f"Longitude: {data.get('lon', 'N/A')}",
                f"Timezone: {data.get('timezone', 'N/A')}"
            ]
            return "\n".join(result_lines)
        else:
            return f"Erreur lors de la recherche: {data.get('message', 'Impossible de trouver cette IP')}"
            
    except requests.exceptions.Timeout:
        return "Erreur: Timeout lors de la requête"
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion: {e}"
    except Exception as e:
        return f"Erreur inattendue: {e}"

def ping_host(target, count=4):
    """
    Ping a host and return the results.
    """
    try:
        system = platform.system().lower()
        
        if system == "windows":
            cmd = ["ping", "-n", str(count), target]
        else:
            cmd = ["ping", "-c", str(count), target]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return f"=== Résultats Ping ===\n{result.stdout}"
        else:
            return f"=== Ping échoué ===\n{result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Erreur: Timeout lors du ping"
    except Exception as e:
        return f"Erreur ping: {e}"

def wifi_scan():
    """
    Scan for available WiFi networks.
    """
    try:
        system = platform.system().lower()
        
        if system == "windows":
            cmd = ["netsh", "wlan", "show", "networks", "mode=Bssid"]
        else:
            cmd = ["nmcli", "-f", "SSID,SIGNAL,SECURITY", "dev", "wifi"]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            return f"=== Réseaux WiFi disponibles ===\n{result.stdout}"
        else:
            return f"Erreur lors du scan WiFi: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Erreur: Timeout lors du scan WiFi"
    except Exception as e:
        return f"Erreur WiFi scan: {e}"

def get_my_ip():
    """
    Get public IP address using multiple services.
    Returns the IP address as string.
    """
    services = [
        "https://api.ipify.org",
        "https://ipinfo.io/ip",
        "https://icanhazip.com",
        "https://ident.me"
    ]
    
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                ip = response.text.strip()
                # Simple validation for IP format
                parts = ip.split('.')
                if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                    return ip
        except Exception:
            continue
    
    return None

def whois_lookup(domain):
    """
    Perform WHOIS lookup on domain or IP.
    Returns formatted WHOIS information.
    """
    try:
        import whois
        
        # Clean the domain (remove http/https if present)
        if domain.startswith(('http://', 'https://')):
            domain = domain.split('://')[1].split('/')[0]
        
        w = whois.whois(domain)
        
        if w:
            result_lines = [
                "=== Informations WHOIS ===",
                f"Domaine: {w.domain_name if w.domain_name else domain}",
                f"Registrar: {w.registrar if w.registrar else 'N/A'}",
                f"Date de création: {w.creation_date if w.creation_date else 'N/A'}",
                f"Date d'expiration: {w.expiration_date if w.expiration_date else 'N/A'}",
                f"Dernière mise à jour: {w.updated_date if w.updated_date else 'N/A'}",
                f"Statut: {w.status if w.status else 'N/A'}",
                f"Serveurs DNS: {', '.join(w.name_servers) if w.name_servers else 'N/A'}",
                f"Organisation: {w.org if w.org else 'N/A'}",
                f"Pays: {w.country if w.country else 'N/A'}"
            ]
            return "\n".join(result_lines)
        else:
            return "Aucune information WHOIS trouvée"
            
    except ImportError:
        return "Erreur: Module python-whois non installé. Exécutez: pip install python-whois"
    except Exception as e:
        return f"Erreur WHOIS: {e}"

def detect_service(port):
    """Detect common services on ports"""
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
        995: "POP3S", 3389: "RDP", 5432: "PostgreSQL", 3306: "MySQL",
        1433: "MSSQL", 6379: "Redis", 27017: "MongoDB", 8080: "HTTP-Alt",
        8443: "HTTPS-Alt", 2222: "SSH-Alt", 8888: "HTTP-Proxy"
    }
    return services.get(port, "Service inconnu")

def fast_ping(host, timeout=1):
    """
    Fast ping using socket connection for network discovery.
    Returns True if host is reachable, False otherwise.
    """
    try:
        # Try to connect to common ports quickly
        import socket
        
        # Test multiple common ports to increase detection chance
        test_ports = [80, 443, 22, 21, 23, 25, 53, 135, 139, 445]
        
        for port in test_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    return True
            except:
                continue
        
        # If no ports respond, try ICMP ping as fallback
        try:
            system = platform.system().lower()
            if system == "windows":
                cmd = ["ping", "-n", "1", "-w", "1000", host]
            else:
                cmd = ["ping", "-c", "1", "-W", "1", host]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            return result.returncode == 0
        except:
            pass
        
        return False
        
    except Exception:
        return False

def network_discovery(network_range, progress_callback=None):
    """
    Discover active hosts in a network range.
    network_range: string like "192.168.1.1-254"
    progress_callback: function to call with (current, total, found_host)
    """
    try:
        if '-' not in network_range:
            return []
        
        # Parse network range
        base_ip = '.'.join(network_range.split('.')[:-1])
        start_end = network_range.split('.')[-1].split('-')
        start_host = int(start_end[0])
        end_host = int(start_end[1])
        
        alive_hosts = []
        total = end_host - start_host + 1
        
        for i in range(start_host, end_host + 1):
            test_ip = f"{base_ip}.{i}"
            
            if fast_ping(test_ip, timeout=0.5):
                alive_hosts.append(test_ip)
                if progress_callback:
                    progress_callback(i - start_host + 1, total, test_ip)
            elif progress_callback:
                progress_callback(i - start_host + 1, total, None)
        
        return alive_hosts
        
    except Exception as e:
        print(f"Network discovery error: {e}")
        return []
