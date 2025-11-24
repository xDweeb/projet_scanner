# scanner_gui_full.py
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from PIL import Image, ImageTk
import threading
import time
import os

# import functions
from scanner_functions import port_scan, system_info, ip_lookup, ping_host, wifi_scan

# -----------------------
# Helper: load image safely
# -----------------------
def load_image(path, size=None):
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

# -----------------------
# Main window (but we will show verification first)
# -----------------------
root = tk.Tk()
root.withdraw()  # hide main until verification

# ===== Verification window (name + age) =====
ver = tk.Toplevel()
ver.title("Vérification")
ver.geometry("380x260")
ver.configure(bg="#0f1724")
ver.resizable(False, False)

tk.Label(ver, text="Bienvenue", bg="#0f1724", fg="white", font=("Arial", 16, "bold")).pack(pady=8)
tk.Label(ver, text="Entrez votre nom :", bg="#0f1724", fg="white").pack(pady=4)
name_entry = tk.Entry(ver, font=("Arial", 12), width=30)
name_entry.pack()

tk.Label(ver, text="Votre âge :", bg="#0f1724", fg="white").pack(pady=6)
age_entry = tk.Entry(ver, font=("Arial", 12), width=10)
age_entry.pack()

def verify_and_open():
    name = name_entry.get().strip()
    age_text = age_entry.get().strip()
    if not name:
        messagebox.showerror("Erreur", "Entrez votre nom")
        return
    try:
        age = int(age_text)
    except:
        messagebox.showerror("Erreur", "Entrez un âge valide")
        return
    if age < 18:
        messagebox.showerror("Accès refusé", "Il faut avoir au moins 18 ans")
        return
    # success
    ver.destroy()
    open_main_window(name)

tk.Button(ver, text="Entrer", bg="#16a085", fg="white", font=("Arial", 12), command=verify_and_open).pack(pady=12)

def open_main_window(user_name):
    # build main UI
    root.deiconify()
    root.title(f"Cyber Scanner PRO - {user_name}")
    root.geometry("980x700")
    root.configure(bg="#0b1220")

    # Top frame: logo + title
    top = tk.Frame(root, bg="#0b1220")
    top.pack(fill="x", pady=10)

    logo = load_image("resources/logo.png", size=(120,120))
    if logo:
        tk.Label(top, image=logo, bg="#0b1220").pack(side="left", padx=20)
    else:
        tk.Label(top, text="Cyber Scanner PRO", bg="#0b1220", fg="white", font=("Arial", 20, "bold")).pack(side="left", padx=20)

    tk.Label(top, text=f"Utilisateur: {user_name}", bg="#0b1220", fg="#cbd5e1", font=("Arial", 12)).pack(anchor="ne", padx=10)

    # Middle: controls and output
    middle = tk.Frame(root, bg="#0b1220")
    middle.pack(fill="both", expand=True, padx=20, pady=5)

    # Left panel: controls
    left = tk.Frame(middle, bg="#0b1220", width=360)
    left.pack(side="left", fill="y", padx=(0,10))

    # IP entry
    tk.Label(left, text="Adresse IP / Domain:", bg="#0b1220", fg="#cbd5e1").pack(anchor="w", pady=(5,2))
    ip_entry = tk.Entry(left, font=("Arial", 12), width=30)
    ip_entry.pack(pady=(0,8))

    # Ports (start / end or custom list)
    tk.Label(left, text="Ports (start-end ou liste, ex: 1-1024 ou 22,80,443):", bg="#0b1220", fg="#cbd5e1").pack(anchor="w")
    ports_entry = tk.Entry(left, font=("Arial", 11), width=30)
    ports_entry.insert(0, "1-1024")
    ports_entry.pack(pady=(0,8))

    # Buttons (with icons optional)
    def icon(path, size=(22,22)):
        p = load_image(path, size=size)
        return p

    btn_scan_icon = icon("resources/icons/scan.png")
    btn_ping_icon = icon("resources/icons/ping.png")
    btn_lookup_icon = icon("resources/icons/lookup.png")
    btn_sys_icon = icon("resources/icons/sys.png")
    btn_wifi_icon = icon("resources/icons/wifi.png")
    btn_save_icon = icon("resources/icons/save.png")

    btn_frame = tk.Frame(left, bg="#0b1220")
    btn_frame.pack(pady=8)

    # Progressbar widget
    prog = ttk.Progressbar(left, orient="horizontal", length=300, mode="determinate")
    prog.pack(pady=6)

    # Output file path display
    save_path_var = tk.StringVar()
    tk.Entry(left, textvariable=save_path_var, state="readonly", width=30).pack(pady=(6,4))

    # Save button helper
    def ask_save_path():
        f = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
        if f:
            save_path_var.set(f)

    save_btn = ttk.Button(left, text="Choose Save File", command=ask_save_path)
    save_btn.pack(pady=(0,8))

    # Right panel: output
    right = tk.Frame(middle, bg="#0b1220")
    right.pack(side="right", fill="both", expand=True)

    output = scrolledtext.ScrolledText(right, font=("Consolas", 11), bg="#071126", fg="#e6eef6")
    output.pack(fill="both", expand=True, padx=(0,10), pady=5)

    # -------------------------
    # Functionalities
    # -------------------------
    def write_output(text):
        output.insert(tk.END, text + "\n")
        output.see(tk.END)

    def clear_output():
        output.delete(1.0, tk.END)

    # parse ports entry
    def parse_ports(text):
        text = text.strip()
        if "-" in text:
            try:
                s,e = text.split("-",1)
                s = int(s.strip()); e = int(e.strip())
                if s>e: s,e = e,s
                return list(range(s, e+1))
            except:
                return []
        elif "," in text:
            parts = [p.strip() for p in text.split(",")]
            lst = []
            for p in parts:
                try:
                    lst.append(int(p))
                except:
                    pass
            return lst
        else:
            try:
                v = int(text)
                return [v]
            except:
                return []

    # port scan worker
    def worker_port_scan(target, ports, timeout=0.5):
        open_ports = []
        total = len(ports)
        for i, p in enumerate(ports):
            ok = port_scan(target, p, timeout=timeout)
            if ok:
                write_output(f"[OPEN] Port {p}")
                open_ports.append(p)
            else:
                write_output(f"[closed] Port {p}")
            # update progress
            try:
                prog['value'] = (i+1)/total*100
            except:
                prog['value'] = 0
        prog['value'] = 100
        return open_ports

    def start_scan():
        clear_output()
        target = ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Entrez une adresse IP ou domain")
            return
        ports_text = ports_entry.get().strip()
        ports = parse_ports(ports_text)
        if not ports:
            messagebox.showerror("Erreur", "Ports invalides")
            return

        write_output(f"Starting scan {target} - {len(ports)} ports")
        def thread_scan():
            opens = worker_port_scan(target, ports)
            write_output("Scan terminé.")
            # auto save if path is set
            path = save_path_var.get()
            if path:
                with open(path, "w") as f:
                    f.write(f"Scan target: {target}\nOpen ports:\n")
                    for op in opens:
                        f.write(str(op)+"\n")
                write_output(f"Résultats sauvegardés dans {path}")
        threading.Thread(target=thread_scan, daemon=True).start()

    def do_ping():
        clear_output()
        target = ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Entrez une adresse IP ou domain")
            return
        write_output(f"Pinging {target} ...")
        def t():
            res = ping_host(target, count=4)
            write_output(res)
        threading.Thread(target=t, daemon=True).start()

    def do_lookup():
        clear_output()
        target = ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Entrez une adresse IP ou domain")
            return
        write_output("Lookup en cours...")
        def t():
            res = ip_lookup(target)
            write_output(res)
        threading.Thread(target=t, daemon=True).start()

    def do_sysinfo():
        clear_output()
        res = system_info()
        write_output(res)

    def do_wifi_scan():
        clear_output()
        write_output("Scanning Wi-Fi networks ...")
        def t():
            res = wifi_scan()
            write_output(res)
        threading.Thread(target=t, daemon=True).start()

    # Buttons (big)
    b1 = ttk.Button(btn_frame, text="Scan Ports", image=btn_scan_icon, compound="left", command=start_scan)
    b2 = ttk.Button(btn_frame, text="Ping", image=btn_ping_icon, compound="left", command=do_ping)
    b3 = ttk.Button(btn_frame, text="IP Lookup", image=btn_lookup_icon, compound="left", command=do_lookup)
    b4 = ttk.Button(btn_frame, text="System Info", image=btn_sys_icon, compound="left", command=do_sysinfo)
    b5 = ttk.Button(btn_frame, text="Wi-Fi Scan", image=btn_wifi_icon, compound="left", command=do_wifi_scan)

    b1.grid(row=0, column=0, padx=6, pady=6)
    b2.grid(row=0, column=1, padx=6, pady=6)
    b3.grid(row=0, column=2, padx=6, pady=6)
    b4.grid(row=0, column=3, padx=6, pady=6)
    b5.grid(row=0, column=4, padx=6, pady=6)

    # Save output button
    def save_output_file():
        p = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
        if p:
            with open(p, "w", encoding="utf-8") as f:
                f.write(output.get(1.0, tk.END))
            messagebox.showinfo("Saved", f"Saved to {p}")

    save_btn = ttk.Button(root, text="Save Output...", image=btn_save_icon, compound="left", command=save_output_file)
    save_btn.pack(pady=8)

    # keep a reference to images to prevent GC
    root._logo = logo
    root._icons = (btn_scan_icon, btn_ping_icon, btn_lookup_icon, btn_sys_icon, btn_wifi_icon, btn_save_icon)

# start Tk mainloop
root.mainloop()
btn_antivirus = Button(window, text="Petit Antivirus", command=scan_package, bg="#4CAF50", fg="white")
btn_antivirus.pack(pady=10)
import os
from tkinter import filedialog, messagebox

def scan_package():
    folder = filedialog.askdirectory(title="Choisir le dossier à scanner")

    if not folder:
        return messagebox.showwarning("Avertissement", "Aucun dossier choisi !")

    # Signatures simples
    signatures = ["virus", "trojan", "malware", "worm", "hack", "danger"]

    infected_files = []

    # Parcours des fichiers
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", errors="ignore") as f:
                    content = f.read()
                    for sig in signatures:
                        if sig.lower() in content.lower():
                            infected_files.append(file_path)
                            break
            except:
                pass  # ignore les fichiers impossibles à lire

    # Affichage des résultats
    if infected_files:
        result = "\n".join(infected_files)
        messagebox.showerror("Menace trouvée !", f"Fichiers infectés :\n{result}")
    else:
        messagebox.showinfo("Scan terminé", "Aucune menace détectée ! 👍")
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# === Splash Screen ===
def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)  # Hide window frame
    splash.configure(bg="white")

    # Center window
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    width = 400
    height = 300
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    splash.geometry(f"{width}x{height}+{x}+{y}")

    # Load Logo
    img = Image.open("/mnt/data/A_vector-based_logo_design_in_the_image_features_a.png")
    img = img.resize((250, 250))
    logo = ImageTk.PhotoImage(img)

    label = tk.Label(splash, image=logo, bg="white")
    label.image = logo
    label.pack(pady=10)

    # Show 4 seconds then open login
    splash.after(4000, lambda: [splash.destroy(), open_login()])


# === Login Window ===
def open_login():
    login = tk.Toplevel()
    login.title("Authentification - Z-Scanner")
    login.geometry("350x200")

    tk.Label(login, text="Entrez le mot de passe :", font=("Arial", 12)).pack(pady=10)
    password_entry = tk.Entry(login, show="*", width=25)
    password_entry.pack()

    def check_password():
        if password_entry.get() == "1234":   # Change password here
            messagebox.showinfo("Bienvenue", "Mot de passe correct !")
            login.destroy()
            open_main_app()
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect")

    tk.Button(login, text="Valider", command=check_password).pack(pady=15)


# === Main App ===
def open_main_app():
    main = tk.Toplevel()
    main.title("Z-Scanner")
    main.geometry("500x300")
    tk.Label(main, text="Bienvenue dans Z-Scanner", font=("Arial", 14)).pack(pady=50)


# === Program Start ===
root = tk.Tk()
root.withdraw()  # Hide main window first

show_splash()

root.mainloop()
