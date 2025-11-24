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
            "=== INFORMATIONS DU SYSTÈME ===",
            f"Nom de l'ordinateur: {platform.node()}",
            f"Système d'exploitation: {platform.system()}",
            f"Version du système: {platform.release()}",
            f"Détails de la version: {platform.version()}",
            f"Architecture processeur: {platform.machine()}",
            f"Type de processeur: {platform.processor()}",
            f"Version Python: {platform.python_version()}"
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
                "=== INFORMATIONS IP ET GÉOLOCALISATION ===",
                f"Adresse IP: {data.get('query', 'Non disponible')}",
                f"Pays: {data.get('country', 'Non disponible')} ({data.get('countryCode', 'N/A')})",
                f"Région/Province: {data.get('regionName', 'Non disponible')}",
                f"Ville: {data.get('city', 'Non disponible')}",
                f"Code postal: {data.get('zip', 'Non disponible')}",
                f"Fournisseur Internet: {data.get('isp', 'Non disponible')}",
                f"Organisation: {data.get('org', 'Non disponible')}",
                f"Latitude: {data.get('lat', 'Non disponible')}",
                f"Longitude: {data.get('lon', 'Non disponible')}",
                f"Fuseau horaire: {data.get('timezone', 'Non disponible')}"
            ]
            return "\n".join(result_lines)
        else:
            return f"Erreur lors de la recherche géographique: {data.get('message', 'Impossible de localiser cette adresse IP')}"
            
    except requests.exceptions.Timeout:
        return "Erreur: Délai d'attente dépassé lors de la requête de géolocalisation"
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion Internet: {e}"
    except Exception as e:
        return f"Erreur inattendue lors de la géolocalisation: {e}"

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
            return f"=== RÉSULTATS DU TEST DE CONNECTIVITÉ ===\n{result.stdout}"
        else:
            return f"=== TEST DE CONNECTIVITÉ ÉCHOUÉ ===\n{result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Erreur: Délai d'attente dépassé lors du test de connectivité"
    except Exception as e:
        return f"Erreur lors du test de connectivité: {e}"

def wifi_scan():
    """
    Analyser les réseaux WiFi disponibles avec plusieurs méthodes.
    """
    try:
        system = platform.system().lower()
        
        if system == "windows":
            output_parts = []
            
            # Method 1: Check WiFi adapter status first
            try:
                cmd_adapter = ["netsh", "wlan", "show", "drivers"]
                result_adapter = subprocess.run(cmd_adapter, capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
                
                if result_adapter.returncode == 0:
                    if "not running" in result_adapter.stdout.lower() or "service is not running" in result_adapter.stdout.lower():
                        return "❌ Service WiFi non démarré. Activez le WiFi dans les paramètres Windows."
                else:
                    return "❌ Aucun adaptateur WiFi détecté sur ce système."
            except Exception:
                pass
            
            # Method 2: Get available networks (live scan)
            try:
                cmd_available = ["netsh", "wlan", "show", "networks", "mode=bssid"]
                result_available = subprocess.run(cmd_available, capture_output=True, text=True, timeout=15, encoding='utf-8', errors='ignore')
                
                if result_available.returncode == 0 and result_available.stdout:
                    if "There is no wireless interface" in result_available.stdout:
                        output_parts.append("❌ Aucune interface WiFi disponible.")
                    elif "networks currently visible" in result_available.stdout or "SSID" in result_available.stdout:
                        output_parts.append("=== 📡 RÉSEAUX WiFi DISPONIBLES ===")
                        output_parts.append(result_available.stdout)
                    else:
                        output_parts.append("⚠️ Aucun réseau WiFi détecté à proximité.")
            except Exception as e:
                output_parts.append(f"⚠️ Erreur lors du scan des réseaux disponibles: {e}")
            
            # Method 3: Get saved profiles
            try:
                cmd_profiles = ["netsh", "wlan", "show", "profiles"]
                result_profiles = subprocess.run(cmd_profiles, capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
                
                if result_profiles.returncode == 0 and result_profiles.stdout:
                    if "User profiles" in result_profiles.stdout or "Profil Utilisateur" in result_profiles.stdout:
                        output_parts.append("\n=== 💾 RÉSEAUX WiFi ENREGISTRÉS ===")
                        output_parts.append(result_profiles.stdout)
            except Exception:
                pass
            
            # Method 4: PowerShell fallback for detailed info
            if not output_parts:
                try:
                    ps_cmd = '''
                    Get-NetAdapter | Where-Object {$_.InterfaceDescription -like "*Wi-Fi*" -or $_.InterfaceDescription -like "*Wireless*"} | 
                    Select-Object Name, InterfaceDescription, Status, LinkSpeed | 
                    Format-Table -AutoSize
                    '''
                    result_ps = subprocess.run(["powershell", "-Command", ps_cmd], 
                                             capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
                    
                    if result_ps.returncode == 0 and result_ps.stdout.strip():
                        output_parts.append("=== 🔧 ADAPTATEURS WiFi DÉTECTÉS ===")
                        output_parts.append(result_ps.stdout)
                    else:
                        output_parts.append("❌ Aucun adaptateur WiFi trouvé avec PowerShell.")
                except Exception:
                    output_parts.append("❌ Impossible d'analyser les adaptateurs WiFi.")
            
            # Return combined results or error message
            if output_parts:
                return "\n".join(output_parts)
            else:
                return "❌ WiFi non disponible: Vérifiez que votre adaptateur WiFi est activé et fonctionne correctement."
                
        else:
            # Linux/Unix systems
            methods = [
                (["nmcli", "-f", "SSID,SIGNAL,SECURITY,CHAN", "dev", "wifi"], "NetworkManager"),
                (["iwlist", "scan"], "iwlist"),
                (["iw", "dev", "wlan0", "scan"], "iw tool")
            ]
            
            for cmd, method_name in methods:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                    if result.returncode == 0 and result.stdout:
                        return f"=== RÉSEAUX WiFi DISPONIBLES ({method_name}) ===\n{result.stdout}"
                except Exception:
                    continue
            
            return "❌ Aucune méthode de scan WiFi disponible sur ce système Linux."
            
    except subprocess.TimeoutExpired:
        return "⏱️ Erreur: Délai d'attente dépassé lors de l'analyse WiFi (réseau lent ou surchargé)"
    except Exception as e:
        return f"❌ Erreur générale lors de l'analyse WiFi: {e}"

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
                "=== INFORMATIONS D'ENREGISTREMENT WHOIS ===",
                f"Nom de domaine: {w.domain_name if w.domain_name else domain}",
                f"Registraire: {w.registrar if w.registrar else 'Non disponible'}",
                f"Date de création: {w.creation_date if w.creation_date else 'Non disponible'}",
                f"Date d'expiration: {w.expiration_date if w.expiration_date else 'Non disponible'}",
                f"Dernière modification: {w.updated_date if w.updated_date else 'Non disponible'}",
                f"Statut du domaine: {w.status if w.status else 'Non disponible'}",
                f"Serveurs de noms DNS: {', '.join(w.name_servers) if w.name_servers else 'Non disponible'}",
                f"Organisation propriétaire: {w.org if w.org else 'Non disponible'}",
                f"Pays d'enregistrement: {w.country if w.country else 'Non disponible'}"
            ]
            return "\n".join(result_lines)
        else:
            return "Aucune information d'enregistrement WHOIS trouvée pour ce domaine"
            
    except ImportError:
        return "Erreur: Module python-whois non installé. Installez-le avec: pip install python-whois"
    except Exception as e:
        return f"Erreur lors de la recherche WHOIS: {e}"

def detect_service(port):
    """Detect common services on ports"""
    services = {
        21: "FTP - Transfert de Fichiers", 22: "SSH - Shell Sécurisé", 23: "Telnet", 25: "SMTP - Courrier Électronique", 53: "DNS - Résolution de Noms",
        80: "HTTP - Web", 110: "POP3 - Courrier Entrant", 143: "IMAP - Courrier Entrant", 443: "HTTPS - Web Sécurisé", 993: "IMAPS - Courrier Sécurisé",
        995: "POP3S - Courrier Sécurisé", 3389: "RDP - Bureau à Distance", 5432: "PostgreSQL - Base de Données", 3306: "MySQL - Base de Données",
        1433: "MSSQL - Base de Données Microsoft", 6379: "Redis - Cache de Données", 27017: "MongoDB - Base de Données NoSQL", 8080: "HTTP Alternatif",
        8443: "HTTPS Alternatif", 2222: "SSH Alternatif", 8888: "Proxy HTTP"
    }
    return services.get(port, "Service Non Identifié")

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
    Découvrir les hôtes actifs dans une plage réseau simple.
    network_range: chaîne comme "192.168.1.1-254"
    progress_callback: fonction à appeler avec (current, total, found_host)
    """
    try:
        if not network_range or '-' not in network_range:
            return []
        
        # Analyser la plage réseau
        base_ip = '.'.join(network_range.split('.')[:-1])
        start_end = network_range.split('.')[-1].split('-')
        start_host = int(start_end[0])
        end_host = int(start_end[1])
        
        alive_hosts = []
        total = end_host - start_host + 1
        
        for i in range(start_host, end_host + 1):
            test_ip = f"{base_ip}.{i}"
            current = i - start_host + 1
            
            if fast_ping(test_ip, timeout=0.5):
                alive_hosts.append(test_ip)
                if progress_callback:
                    progress_callback(current, total, f"✅ Hôte trouvé: {test_ip}")
            elif progress_callback:
                progress_callback(current, total, None)
        
        return alive_hosts
        
    except Exception as e:
        if progress_callback:
            progress_callback(0, 1, f"❌ Erreur: {e}")
        return []

# Fonction simplifiée pour obtenir l'IP locale
def get_local_ip():
    """Obtenir l'IP locale de façon simple"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        try:
            import socket
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "127.0.0.1"
