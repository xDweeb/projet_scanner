import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from tkinter.ttk import Progressbar
from scanner_functions import port_scan, system_info, ip_lookup
import threading

# ====== FONCTIONS ======
def gui_port_scan():
    ip = entry_ip.get()
    output.delete(1.0, tk.END)
    
    try:
        start_port = int(entry_start.get())
        end_port = int(entry_end.get())
    except:
        messagebox.showerror("Erreur", "Entrez un range valide")
        return

    output.insert(tk.END, f"Scanning {ip} ports {start_port}-{end_port}...\n")
    
    progress['value'] = 0
    window.update_idletasks()
    
    def scan_thread():
        open_ports = []
        total = end_port - start_port + 1
        for i, port in enumerate(range(start_port, end_port+1)):
            if port_scan(ip, port):
                output.insert(tk.END, f"Port {port} ouvert\n")
                open_ports.append(port)
            progress['value'] = (i+1)/total*100
            window.update_idletasks()
        output.insert(tk.END, "\nScan terminé.\n")
        save_results(ip, open_ports)
    
    threading.Thread(target=scan_thread).start()

def save_results(ip, open_ports):
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files","*.txt")],
                                            title="Sauvegarder résultats")
    if filename:
        with open(filename, "w") as f:
            f.write(f"Scan IP: {ip}\n")
            f.write("Open Ports:\n")
            for port in open_ports:
                f.write(f"{port}\n")
        messagebox.showinfo("Sauvegarde", f"Résultats sauvegardés dans {filename}")

def gui_system_info():
    output.delete(1.0, tk.END)
    system_info()

def gui_ip_lookup():
    ip = entry_ip.get()
    output.delete(1.0, tk.END)
    ip_lookup(ip)

# ====== INTERFACE ======
# ====== WINDOW VERIFICATION ======
verify = tk.Tk()
verify.title("Verification")
verify.geometry("350x250")
verify.config(bg="#1e1e2f")

tk.Label(verify, text="Entrez votre nom :", bg="#1e1e2f", fg="white", font=("Arial", 12)).pack(pady=5)
entry_name = tk.Entry(verify, font=("Arial", 12))
entry_name.pack(pady=5)

tk.Label(verify, text="Votre âge :", bg="#1e1e2f", fg="white", font=("Arial", 12)).pack(pady=5)
entry_age = tk.Entry(verify, font=("Arial", 12))
entry_age.pack(pady=5)

def check_age():
    try:
        age = int(entry_age.get())
        name = entry_name.get()

        if name == "":
            messagebox.showerror("Erreur", "Veuillez entrer votre nom")
            return

        if age < 18:
            messagebox.showerror("Accès refusé", "Il faut avoir plus de 18 ans pour utiliser ce logiciel.")
            return
        
        verify.destroy()  # ferme la fenêtre de vérification

    except:
        messagebox.showerror("Erreur", "Entrez un âge valide")

btn_ok = tk.Button(verify, text="Entrer", bg="#4caf50", fg="white", font=("Arial", 12), command=check_age)
btn_ok.pack(pady=20)

verify.mainloop()

window = tk.Tk()
window.title("🔥 Cyber Scanner PRO 🔥")
window.geometry("700x600")
window.configure(bg="#1e1e2f")

# Label IP
label_ip = tk.Label(window, text="Adresse IP / Domain:", bg="#1e1e2f", fg="#ffffff", font=("Arial", 12))
label_ip.pack(pady=5)

# Entry IP
entry_ip = tk.Entry(window, width=30, font=("Arial", 12))
entry_ip.pack(pady=5)

# Port Range
frame_range = tk.Frame(window, bg="#1e1e2f")
frame_range.pack(pady=5)
tk.Label(frame_range, text="Start Port:", bg="#1e1e2f", fg="white").grid(row=0,column=0,padx=5)
entry_start = tk.Entry(frame_range, width=6)
entry_start.grid(row=0,column=1,padx=5)
tk.Label(frame_range, text="End Port:", bg="#1e1e2f", fg="white").grid(row=0,column=2,padx=5)
entry_end = tk.Entry(frame_range, width=6)
entry_end.grid(row=0,column=3,padx=5)
entry_start.insert(0,"1")
entry_end.insert(0,"1024")

# Buttons frame
frame_btn = tk.Frame(window, bg="#1e1e2f")
frame_btn.pack(pady=10)

btn_scan = tk.Button(frame_btn, text="Scan Ports", width=15, command=gui_port_scan, bg="#4caf50", fg="white", font=("Arial", 10, "bold"))
btn_scan.grid(row=0, column=0, padx=5, pady=5)

btn_lookup = tk.Button(frame_btn, text="IP Lookup", width=15, command=gui_ip_lookup, bg="#2196f3", fg="white", font=("Arial", 10, "bold"))
btn_lookup.grid(row=0, column=1, padx=5, pady=5)

btn_sys = tk.Button(frame_btn, text="System Info", width=15, command=gui_system_info, bg="#ff9800", fg="white", font=("Arial", 10, "bold"))
btn_sys.grid(row=0, column=2, padx=5, pady=5)

# Progress Bar
progress = Progressbar(window, orient=tk.HORIZONTAL, length=600, mode='determinate')
progress.pack(pady=10)

# Scrolled Text output
output = scrolledtext.ScrolledText(window, width=80, height=25, font=("Consolas", 10))
output.pack(pady=10)

window.mainloop()
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
from scanner_functions import port_scan, system_info, ip_lookup
import threading

# ====== FONCTIONS ======
def gui_port_scan():
    ip = entry_ip.get()
    output.delete(1.0, tk.END)
    
    try:
        start_port = int(entry_start.get())
        end_port = int(entry_end.get())
    except:
        messagebox.showerror("Erreur", "Entrez un range valide")
        return

    output.insert(tk.END, f"Scanning {ip} ports {start_port}-{end_port}...\n")
    
    progress['value'] = 0
    window.update_idletasks()
    
    def scan_thread():
        open_ports = []
        total = end_port - start_port + 1
        for i, port in enumerate(range(start_port, end_port+1)):
            if port_scan(ip, port):
                output.insert(tk.END, f"Port {port} ouvert\n")
                open_ports.append(port)
            progress['value'] = (i+1)/total*100
            window.update_idletasks()
        output.insert(tk.END, "\nScan terminé.\n")
        save_results(ip, open_ports)
    
    threading.Thread(target=scan_thread).start()

def save_results(ip, open_ports):
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files","*.txt")],
                                            title="Sauvegarder résultats")
    if filename:
        with open(filename, "w") as f:
            f.write(f"Scan IP: {ip}\n")
            f.write("Open Ports:\n")
            for port in open_ports:
                f.write(f"{port}\n")
        messagebox.showinfo("Sauvegarde", f"Résultats sauvegardés dans {filename}")

def gui_system_info():
    output.delete(1.0, tk.END)
    system_info()

def gui_ip_lookup():
    ip = entry_ip.get()
    output.delete(1.0, tk.END)
    ip_lookup(ip)

# ====== INTERFACE ======
window = tk.Tk()
window.title("🔥 Cyber Scanner PRO 🔥")
window.geometry("750x650")
window.configure(bg="#1e1e2f")

# ====== Logo ======
try:
    logo_img = Image.open("resources/logo.png")
    logo_img = logo_img.resize((120,120))
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(window, image=logo, bg="#1e1e2f")
    logo_label.pack(pady=10)
except:
    print("Logo non trouvé, l'interface continue sans logo")

# ====== IP Entry ======
label_ip = tk.Label(window, text="Adresse IP / Domain:", bg="#1e1e2f", fg="#ffffff", font=("Arial", 12))
label_ip.pack(pady=5)
entry_ip = tk.Entry(window, width=30, font=("Arial", 12))
entry_ip.pack(pady=5)

# ====== Port Range ======
frame_range = tk.Frame(window, bg="#1e1e2f")
frame_range.pack(pady=5)
tk.Label(frame_range, text="Start Port:", bg="#1e1e2f", fg="white").grid(row=0,column=0,padx=5)
entry_start = tk.Entry(frame_range, width=6)
entry_start.grid(row=0,column=1,padx=5)
tk.Label(frame_range, text="End Port:", bg="#1e1e2f", fg="white").grid(row=0,column=2,padx=5)
entry_end = tk.Entry(frame_range, width=6)
entry_end.grid(row=0,column=3,padx=5)
entry_start.insert(0,"1")
entry_end.insert(0,"1024")

# ====== Buttons avec Icons ======
frame_btn = tk.Frame(window, bg="#1e1e2f")
frame_btn.pack(pady=10)

def load_icon(path, size=(30,30)):
    try:
        img = Image.open(path)
        img = img.resize(size)
        return ImageTk.PhotoImage(img)
    except:
        return None

icon_scan = load_icon("resources/icons/scan.png")
icon_lookup = load_icon("resources/icons/lookup.png")
icon_sys = load_icon("resources/icons/sys.png")

btn_scan = tk.Button(frame_btn, text="Scan Ports", width=15, command=gui_port_scan,
                     bg="#4caf50", fg="white", font=("Arial", 10, "bold"), image=icon_scan, compound="left")
btn_scan.grid(row=0, column=0, padx=5, pady=5)

btn_lookup = tk.Button(frame_btn, text="IP Lookup", width=15, command=gui_ip_lookup,
                       bg="#2196f3", fg="white", font=("Arial", 10, "bold"), image=icon_lookup, compound="left")
btn_lookup.grid(row=0, column=1, padx=5, pady=5)

btn_sys = tk.Button(frame_btn, text="System Info", width=15, command=gui_system_info,
                    bg="#ff9800", fg="white", font=("Arial", 10, "bold"), image=icon_sys, compound="left")
btn_sys.grid(row=0, column=2, padx=5, pady=5)

# ====== Progress Bar ======
progress = Progressbar(window, orient=tk.HORIZONTAL, length=700, mode='determinate')
progress.pack(pady=10)

# ====== Scrolled Text output ======
output = scrolledtext.ScrolledText(window, width=90, height=25, font=("Consolas", 10))
output.pack(pady=10)

window.mainloop()
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
from scanner_functions import port_scan, system_info, ip_lookup
import threading

# ====== FONCTIONS ======
def gui_port_scan():
    ip = entry_ip.get()
    output.delete(1.0, tk.END)
    
    try:
        start_port = int(entry_start.get())
        end_port = int(entry_end.get())
    except:
        messagebox.showerror("Erreur", "Entrez un range valide")
        return

    output.insert(tk.END, f"Scanning {ip} ports {start_port}-{end_port}...\n")
    
    progress['value'] = 0
    window.update_idletasks()
    
    def scan_thread():
        open_ports = []
        total = end_port - start_port + 1
        for i, port in enumerate(range(start_port, end_port+1)):
            if port_scan(ip, port):
                output.insert(tk.END, f"Port {port} ouvert\n")
                open_ports.append(port)
            progress['value'] = (i+1)/total*100
            window.update_idletasks()
        output.insert(tk.END, "\nScan terminé.\n")
        save_results(ip, open_ports)
    
    threading.Thread(target=scan_thread).start()

def save_results(ip, open_ports):
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files","*.txt")],
                                            title="Sauvegarder résultats")
    if filename:
        with open(filename, "w") as f:
            f.write(f"Scan IP: {ip}\n")
            f.write("Open Ports:\n")
            for port in open_ports:
                f.write(f"{port}\n")
        messagebox.showinfo("Sauvegarde", f"Résultats sauvegardés dans {filename}")

def gui_system_info():
    output.delete(1.0, tk.END)
    system_info()

def gui_ip_lookup():
    ip = entry_ip.get()
    output.delete(1.0, tk.END)
    ip_lookup(ip)

# ====== INTERFACE ======
window = tk.Tk()
window.title("🔥 Cyber Scanner PRO 🔥")
window.geometry("750x650")
window.configure(bg="#1e1e2f")

# ====== Logo ======
try:
    logo_img = Image.open("resources/logo.png")
    logo_img = logo_img.resize((120,120))
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(window, image=logo, bg="#1e1e2f")
    logo_label.pack(pady=10)
except:
    print("Logo non trouvé, l'interface continue sans logo")

# ====== IP Entry ======
label_ip = tk.Label(window, text="Adresse IP / Domain:", bg="#1e1e2f", fg="#ffffff", font=("Arial", 12))
label_ip.pack(pady=5)
entry_ip = tk.Entry(window, width=30, font=("Arial", 12))
entry_ip.pack(pady=5)

# ====== Port Range ======
frame_range = tk.Frame(window, bg="#1e1e2f")
frame_range.pack(pady=5)
tk.Label(frame_range, text="Start Port:", bg="#1e1e2f", fg="white").grid(row=0,column=0,padx=5)
entry_start = tk.Entry(frame_range, width=6)
entry_start.grid(row=0,column=1,padx=5)
tk.Label(frame_range, text="End Port:", bg="#1e1e2f", fg="white").grid(row=0,column=2,padx=5)
entry_end = tk.Entry(frame_range, width=6)
entry_end.grid(row=0,column=3,padx=5)
entry_start.insert(0,"1")
entry_end.insert(0,"1024")

# ====== Buttons avec Icons ======
frame_btn = tk.Frame(window, bg="#1e1e2f")
frame_btn.pack(pady=10)

def load_icon(path, size=(30,30)):
    try:
        img = Image.open(path)
        img = img.resize(size)
        return ImageTk.PhotoImage(img)
    except:
        return None

icon_scan = load_icon("resources/icons/scan.png")
icon_lookup = load_icon("resources/icons/lookup.png")
icon_sys = load_icon("resources/icons/sys.png")

btn_scan = tk.Button(frame_btn, text="Scan Ports", width=15, command=gui_port_scan,
                     bg="#4caf50", fg="white", font=("Arial", 10, "bold"), image=icon_scan, compound="left")
btn_scan.grid(row=0, column=0, padx=5, pady=5)

btn_lookup = tk.Button(frame_btn, text="IP Lookup", width=15, command=gui_ip_lookup,
                       bg="#2196f3", fg="white", font=("Arial", 10, "bold"), image=icon_lookup, compound="left")
btn_lookup.grid(row=0, column=1, padx=5, pady=5)

btn_sys = tk.Button(frame_btn, text="System Info", width=15, command=gui_system_info,
                    bg="#ff9800", fg="white", font=("Arial", 10, "bold"), image=icon_sys, compound="left")
btn_sys.grid(row=0, column=2, padx=5, pady=5)

# ====== Progress Bar ======
progress = Progressbar(window, orient=tk.HORIZONTAL, length=700, mode='determinate')
progress.pack(pady=10)

# ====== Scrolled Text output ======
output = scrolledtext.ScrolledText(window, width=90, height=25, font=("Consolas", 10))
output.pack(pady=10)

window.mainloop()
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
from scanner_functions import port_scan, ip_lookup, system_info

# -------------------------
# Interface principale
# -------------------------

window = tk.Tk()
window.title("Cyber Scanner PRO")
window.geometry("800x650")
window.config(bg="#1c1c28")

# ====== Charger LOGO ======
try:
    logo_img = Image.open("resources/logo.png")
    logo_img = logo_img.resize((200, 200))
    logo_photo = ImageTk.PhotoImage(logo_img)
    tk.Label(window, image=logo_photo, bg="#1c1c28").pack(pady=10)
except:
    tk.Label(window, text="Cyber Scanner PRO", fg="white", bg="#1c1c28",
             font=("Arial", 22, "bold")).pack(pady=10)

# ====== Input IP ======
frame_input = tk.Frame(window, bg="#1c1c28")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Adresse IP :", fg="white", bg="#1c1c28",
         font=("Arial", 14)).grid(row=0, column=0, padx=10)

entry_ip = tk.Entry(frame_input, font=("Arial", 14), width=25)
entry_ip.grid(row=0, column=1, padx=10)

# ====== Charger ICONS ======
def load_icon(path, size=(30, 30)):
    try:
        img = Image.open(path)
        img = img.resize(size)
        return ImageTk.PhotoImage(img)
    except:
        return None

icon_scan = load_icon("resources/scan.png")
icon_lookup = load_icon("resources/lookup.png")
icon_sys = load_icon("resources/sys.png")

# ====== Zone résultat ======
output = tk.Text(window, height=15, width=90, font=("Consolas", 11),
                 bg="#0f0f17", fg="white")
output.pack(pady=15)

# ====== Progress Bar ======
progress = tk.DoubleVar()
progress_bar = tk.Scale(window, variable=progress, from_=0, to=100,
                         length=600, orient="horizontal",
                         bg="#1c1c28", fg="white")
progress_bar.pack()


# -------------------------
# Fonctions de Scan
# -------------------------

def run_port_scan():
    output.delete(1.0, tk.END)
    ip = entry_ip.get()

    output.insert(tk.END, f"Scanning {ip}...\n")

    open_ports = []
    total_ports = 100
    for port in range(1, total_ports+1):
        if port_scan(ip, port):
            open_ports.append(port)
            output.insert(tk.END, f"Port ouvert: {port}\n")
        progress.set((port/total_ports)*100)
        window.update_idletasks()

    if not open_ports:
        output.insert(tk.END, "\nAucun port ouvert trouvé.")
    else:
        output.insert(tk.END, f"\nPorts ouverts: {open_ports}")


def start_port_scan():
    threading.Thread(target=run_port_scan).start()


def start_lookup():
    ip = entry_ip.get()
    result = ip_lookup(ip)
    output.delete(1.0, tk.END)
    output.insert(tk.END, result)


def show_system_info():
    info = system_info()
    output.delete(1.0, tk.END)
    output.insert(tk.END, info)


# ------------------------
# Boutons avec ICONS
# ------------------------

frame_btn = tk.Frame(window, bg="#1c1c28")
frame_btn.pack(pady=10)

btn_scan = tk.Button(frame_btn, text=" Scanner Ports",
                     image=icon_scan, compound="left",
                     font=("Arial", 13), command=start_port_scan,
                     bg="#29293d", fg="white", width=200)
btn_scan.grid(row=0, column=0, padx=15)

btn_lookup = tk.Button(frame_btn, text=" IP Lookup",
                       image=icon_lookup, compound="left",
                       font=("Arial", 13), command=start_lookup,
                       bg="#29293d", fg="white", width=200)
btn_lookup.grid(row=0, column=1, padx=15)

btn_sysinfo = tk.Button(frame_btn, text=" Info Système",
                        image=icon_sys, compound="left",
                        font=("Arial", 13), command=show_system_info,
                        bg="#29293d", fg="white", width=200)
btn_sysinfo.grid(row=0, column=2, padx=15)


window.mainloop()
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Scanner Pro GUI")

# تحميل الصورة
img = Image.open("gui.png")
img = img.resize((350, 250))
photo = ImageTk.PhotoImage(img)

# عرض الصورة
label = tk.Label(root, image=photo)
label.pack()

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

