import tkinter as tk
from tkinter import scrolledtext
from scanner_functions import port_scan, system_info, ip_lookup

# ====== FONCTIONS ======
def gui_port_scan():
    ip = entry_ip.get()
    output.delete(1.0, tk.END)
    output.insert(tk.END, f"Scanning {ip}...\n")
    port_scan(ip)
    output.insert(tk.END, "\nScan terminé.\n")

def gui_system_info():
    output.delete(1.0, tk.END)
    system_info()

def gui_ip_lookup():
    ip = entry_ip.get()
    output.delete(1.0, tk.END)
    ip_lookup(ip)

# ====== INTERFACE ======
window = tk.Tk()
window.title("🔥 Cyber Scanner GUI 🔥")
window.geometry("600x550")
window.configure(bg="#1e1e2f")  # dark background

# Label IP
label_ip = tk.Label(window, text="Adresse IP / Domain:", bg="#1e1e2f", fg="#ffffff", font=("Arial", 12))
label_ip.pack(pady=10)

# Entry IP
entry_ip = tk.Entry(window, width=30, font=("Arial", 12))
entry_ip.pack(pady=5)

# Buttons frame
frame_btn = tk.Frame(window, bg="#1e1e2f")
frame_btn.pack(pady=10)

btn_scan = tk.Button(frame_btn, text="Scan Ports", width=15, command=gui_port_scan, bg="#4caf50", fg="white", font=("Arial", 10, "bold"))
btn_scan.grid(row=0, column=0, padx=5, pady=5)

btn_lookup = tk.Button(frame_btn, text="IP Lookup", width=15, command=gui_ip_lookup, bg="#2196f3", fg="white", font=("Arial", 10, "bold"))
btn_lookup.grid(row=0, column=1, padx=5, pady=5)

btn_sys = tk.Button(frame_btn, text="System Info", width=15, command=gui_system_info, bg="#ff9800", fg="white", font=("Arial", 10, "bold"))
btn_sys.grid(row=0, column=2, padx=5, pady=5)

# Scrolled Text output
output = scrolledtext.ScrolledText(window, width=70, height=20, font=("Consolas", 10))
output.pack(pady=10)

window.mainloop()

