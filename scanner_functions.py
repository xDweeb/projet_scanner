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
