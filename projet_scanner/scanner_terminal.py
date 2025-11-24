from scanner_functions import port_scan, system_info, ip_lookup

def main():
    while True:
        print("\n===== Scanner Terminal =====")
        print("1. Scanner ports")
        print("2. Afficher informations système")
        print("3. Recherche IP (géolocalisation)")
        print("4. Quitter")

        choice = input("Choisissez une option : ")

        if choice == "1":
            target = input("Entrez l'adresse IP à scanner : ")
            port_scan(target)

        elif choice == "2":
            system_info()

        elif choice == "3":
            target = input("Entrez IP/domain : ")
            ip_lookup(target)

        elif choice == "4":
            print("Au revoir !")
            break

        else:
            print("Option invalide !")


if __name__ == "__main__":
    main()
