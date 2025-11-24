import socket
import platform
import requests

def port_scan(target):
    print(f"\nScanning {target} ...")
    try:
        for port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"Port {port} ouvert")
            sock.close()
    except Exception as e:
        print(f"Erreur : {e}")

def system_info():
    print("\n=== Informations système ===")
    print("Nom de la machine :", platform.node())
    print("Système :", platform.system())
    print("Version :", platform.version())
    print("Processeur :", platform.processor())

def ip_lookup(target):
    print("\nRecherche d'informations...")
    try:
        response = requests.get(f"http://ip-api.com/json/{target}").json()
        if response["status"] == "success":
            print("IP :", response["query"])
            print("Pays :", response["country"])
            print("Ville :", response["city"])
            print("ISP :", response["isp"])
        else:
            print("Impossible de trouver cette IP.")
    except Exception as e:
        print("Erreur :", e)
import socket
import platform
import requests

# ----------------------
# Port Scanner Function
# ----------------------
def port_scan(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except Exception as e:
        print("Erreur:", e)
        return False

# ----------------------
# System Info
# ----------------------
def system_info():
    info = f"""
System: {platform.system()}
Version: {platform.version()}
Machine: {platform.machine()}
"""
    print(info)
    return info

# ----------------------
# IP Lookup (Geo)
# ----------------------
def ip_lookup(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        r = requests.get(url).json()
        info = f"""
IP: {ip}
Country: {r['country']}
City: {r['city']}
ISP: {r['isp']}
Latitude: {r['lat']}
Longitude: {r['lon']}
"""
        print(info)
        return info
    except:
        return "Erreur lookup"
    # scanner_functions.py
import socket
import platform
import subprocess
import requests

# ----------------------
# Port Scanner Function
# ----------------------
def port_scan(ip, port, timeout=0.5):
    """
    Retourne True si port ouvert, False sinon.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except Exception as e:
        # print("port_scan error:", e)
        return False

# ----------------------
# System Info
# ----------------------
def system_info():
    """
    Retourne une string avec infos système (également imprimable).
    """
    try:
        info = []
        info.append(f"Système : {platform.system()}")
        info.append(f"Node : {platform.node()}")
        info.append(f"Release : {platform.release()}")
        info.append(f"Version : {platform.version()}")
        info.append(f"Machine : {platform.machine()}")
        info.append(f"Processor : {platform.processor()}")
        text = "\n".join(info)
        # print(text)
        return text
    except Exception as e:
        return f"Erreur system_info: {e}"

# ----------------------
# IP Lookup (Geo)
# ----------------------
def ip_lookup(target):
    """
    Utilise ip-api.com pour obtenir geo info.
    Retourne string.
    """
    try:
        # si user donne un domain, ip-api accepte aussi domain
        url = f"http://ip-api.com/json/{target}"
        r = requests.get(url, timeout=8).json()
        if r.get("status") == "success":
            parts = [
                f"Query: {r.get('query')}",
                f"Pays: {r.get('country')} ({r.get('countryCode')})",
                f"Region: {r.get('regionName')}",
                f"City: {r.get('city')}",
                f"ISP: {r.get('isp')}",
                f"Lat/Lon: {r.get('lat')},{r.get('lon')}"
            ]
            return "\n".join(parts)
        else:
            return f"Lookup failed: {r.get('message', 'unknown')}"
    except Exception as e:
        return f"Erreur ip_lookup: {e}"

# ----------------------
# Ping function
# ----------------------
def ping_host(target, count=4):
    """
    Retourne la sortie du ping en string.
    Fonctionne sur Windows et Unix.
    """
    try:
        system = platform.system()
        if system == "Windows":
            cmd = ["ping", "-n", str(count), target]
        else:
            cmd = ["ping", "-c", str(count), target]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return proc.stdout
    except Exception as e:
        return f"Erreur ping: {e}"

# ----------------------
# WiFi scan (basic)
# ----------------------
def wifi_scan():
    """
    Essaie d'obtenir liste des réseaux Wi-Fi.
    Sous Windows: utilise 'netsh wlan show networks mode=Bssid'
    Sous Linux (NetworkManager): utilise 'nmcli -f SSID,SIGNAL dev wifi'
    Retourne string résultat ou message d'erreur.
    """
    try:
        system = platform.system()
        if system == "Windows":
            cmd = ["netsh", "wlan", "show", "networks", "mode=Bssid"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return proc.stdout
        else:
            # linux
            cmd = ["nmcli", "-f", "SSID,SIGNAL,SECURITY", "dev", "wifi"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return proc.stdout
    except Exception as e:
        return f"Erreur wifi_scan: {e}"

