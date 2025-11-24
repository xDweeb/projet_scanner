"""
Modern GUI interface for Cyber Scanner PRO
Main application window with all scanning features
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import time
from PIL import Image, ImageTk

from src.core.scanner_engine import (port_scan, system_info, ip_lookup, ping_host, 
                                   wifi_scan, get_my_ip, whois_lookup, detect_service, 
                                   fast_ping)
from src.database.db_manager import ScanDatabase

class CyberScannerPRO:
    def __init__(self):
        # Initialize database
        self.db = ScanDatabase()
        
        # Load theme preference (force dark mode)
        self.current_theme = 'dark'
        
        # Theme definitions
        self.themes = {
            'dark': {
                'bg': '#0f1419',
                'secondary_bg': '#1a1f2e', 
                'text': '#ffffff',
                'text_secondary': '#9ca3af',
                'text_muted': '#6b7280',
                'accent': '#4a9eff',
                'output_bg': '#0a0e14',
                'button_bg': '#1a1f2e'
            },
            'light': {
                'bg': '#ffffff',
                'secondary_bg': '#f8fafc',
                'text': '#1f2937',
                'text_secondary': '#4b5563',
                'text_muted': '#6b7280',
                'accent': '#3b82f6',
                'output_bg': '#f9fafb',
                'button_bg': '#e5e7eb'
            }
        }
        
        self.show_splash_screen()
    
    def get_theme_color(self, color_key):
        """Get color for current theme"""
        return self.themes[self.current_theme][color_key]
    
    def show_splash_screen(self):
        """Show splash screen with logo for 3 seconds"""
        self.splash = tk.Tk()
        self.splash.title("Cyber Scanner PRO")
        self.splash.geometry("500x400")
        self.splash.configure(bg=self.get_theme_color('bg'))
        self.splash.resizable(False, False)
        self.splash.overrideredirect(True)  # Remove title bar
        
        # Center the splash screen
        self.splash.eval('tk::PlaceWindow . center')
        
        # Main container
        container = tk.Frame(self.splash, bg=self.get_theme_color('bg'))
        container.pack(fill="both", expand=True, padx=50, pady=50)
        
        try:
            # Try to load the logo image
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "logo.png")
            
            # Also try the old path for compatibility
            if not os.path.exists(logo_path):
                logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logo.png")
            
            if os.path.exists(logo_path):
                # Load and resize logo
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((300, 200), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                
                # Display logo
                logo_label = tk.Label(container, image=self.logo_photo, bg=self.get_theme_color('bg'))
                logo_label.pack(pady=(20, 30))
            else:
                # Fallback if logo not found - show text logo
                logo_label = tk.Label(container, text="🛡️", font=("Segoe UI", 60), 
                                     bg=self.get_theme_color('bg'), fg=self.get_theme_color('accent'))
                logo_label.pack(pady=(20, 10))
                
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback logo
            logo_label = tk.Label(container, text="🛡️", font=("Segoe UI", 60), 
                                 bg=self.get_theme_color('bg'), fg=self.get_theme_color('accent'))
            logo_label.pack(pady=(20, 10))
        
        # App title
        title_label = tk.Label(container, text="Cyber Scanner PRO", 
                              font=("Segoe UI", 24, "bold"), 
                              fg=self.get_theme_color('text'), bg=self.get_theme_color('bg'))
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(container, text="Professional Network Security Scanner", 
                                 font=("Segoe UI", 12), 
                                 fg=self.get_theme_color('text_muted'), bg=self.get_theme_color('bg'))
        subtitle_label.pack(pady=(0, 30))
        
        # Loading animation
        self.loading_label = tk.Label(container, text="Chargement", 
                                     font=("Segoe UI", 11), 
                                     fg=self.get_theme_color('accent'), bg=self.get_theme_color('bg'))
        self.loading_label.pack(pady=(0, 20))
        
        # Start loading animation
        self.animate_loading()
        
        # Close splash and show verification after 3 seconds
        self.splash.after(3000, self.close_splash)
        
        self.splash.mainloop()
    
    def animate_loading(self):
        """Animate loading text with dots"""
        texts = ["Chargement", "Chargement.", "Chargement..", "Chargement..."]
        
        def update_text(index=0):
            try:
                if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
                    self.loading_label.config(text=texts[index % len(texts)])
                    if hasattr(self, 'splash') and self.splash.winfo_exists():
                        next_index = (index + 1) % len(texts)
                        self.splash.after(300, update_text, next_index)
            except:
                pass
        
        update_text()
    
    def close_splash(self):
        """Close splash screen and show verification window"""
        try:
            self.splash.destroy()
        except:
            pass
        self.setup_verification_window()
        
    def setup_verification_window(self):
        """Age verification window"""
        self.verify_window = tk.Tk()
        self.verify_window.title("Vérification d'âge")
        self.verify_window.geometry("450x500")
        self.verify_window.configure(bg=self.get_theme_color('bg'))
        self.verify_window.resizable(False, False)
        
        # Center the window
        self.verify_window.eval('tk::PlaceWindow . center')
        
        # Main container with padding
        container = tk.Frame(self.verify_window, bg=self.get_theme_color('bg'))
        container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Shield icon
        shield_label = tk.Label(container, text="🔒", font=("Segoe UI", 40), 
                               bg=self.get_theme_color('bg'), fg=self.get_theme_color('accent'))
        shield_label.pack(pady=(0, 10))
        
        # Title
        title_label = tk.Label(container, text="Cyber Scanner PRO", 
                              font=("Segoe UI", 22, "bold"), 
                              fg=self.get_theme_color('text'), bg=self.get_theme_color('bg'))
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(container, text="Vérification d'accès", 
                                 font=("Segoe UI", 11), 
                                 fg=self.get_theme_color('text_muted'), bg=self.get_theme_color('bg'))
        subtitle_label.pack(pady=(0, 30))
        
        # Name input
        tk.Label(container, text="Nom d'utilisateur", 
                font=("Segoe UI", 10), fg=self.get_theme_color('text_secondary'), bg=self.get_theme_color('bg')).pack(anchor="w", pady=(0, 5))
        
        self.name_entry = tk.Entry(container, font=("Segoe UI", 11), 
                                  bg=self.get_theme_color('secondary_bg'), fg=self.get_theme_color('text'), 
                                  insertbackground=self.get_theme_color('accent'), bd=0, relief="flat")
        self.name_entry.pack(fill="x", ipady=10)
        
        # Age input
        tk.Label(container, text="Âge", 
                font=("Segoe UI", 10), fg=self.get_theme_color('text_secondary'), bg=self.get_theme_color('bg')).pack(anchor="w", pady=(15, 5))
        
        self.age_entry = tk.Entry(container, font=("Segoe UI", 11), 
                                 bg=self.get_theme_color('secondary_bg'), fg=self.get_theme_color('text'), 
                                 insertbackground=self.get_theme_color('accent'), bd=0, relief="flat")
        self.age_entry.pack(fill="x", ipady=10)
        
        # Verify button
        verify_btn = tk.Button(container, text="✅ Accéder à l'application", 
                              font=("Segoe UI", 12, "bold"), 
                              bg=self.get_theme_color('accent'), fg="white", 
                              command=self.verify_access, 
                              bd=0, relief="flat", cursor="hand2",
                              activebackground=self.darken_color(self.get_theme_color('accent')),
                              activeforeground="white")
        verify_btn.pack(fill="x", pady=(30, 10), ipady=15)
        
        # Status label
        self.status_label = tk.Label(container, text="Entrez vos informations pour continuer", 
                                    font=("Segoe UI", 9), fg=self.get_theme_color('text_muted'), bg=self.get_theme_color('bg'))
        self.status_label.pack(pady=(10, 0))
        
        # Bind Enter key to both entry fields and button
        self.name_entry.bind("<Return>", lambda e: self.age_entry.focus())
        self.age_entry.bind("<Return>", lambda e: self.verify_access())
        
        # Focus on name entry initially
        self.name_entry.focus()
        
        # Bind key events to update status
        self.name_entry.bind("<KeyRelease>", self.update_status)
        self.age_entry.bind("<KeyRelease>", self.update_status)
        
        self.verify_window.mainloop()
    
    def update_status(self, event=None):
        """Update status based on input"""
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        
        if not name:
            self.status_label.config(text="Entrez votre nom", fg="#ef4444")
        elif not age:
            self.status_label.config(text="Entrez votre âge", fg="#f59e0b")
        else:
            try:
                age_num = int(age)
                if age_num < 18:
                    self.status_label.config(text="Âge minimum: 18 ans", fg="#ef4444")
                else:
                    self.status_label.config(text="✅ Prêt à continuer", fg="#22c55e")
            except:
                self.status_label.config(text="Âge invalide", fg="#ef4444")
    
    def verify_access(self):
        """Verify user age and name"""
        name = self.name_entry.get().strip()
        age_text = self.age_entry.get().strip()
        
        print(f"Debug: Name='{name}', Age='{age_text}'")  # Debug line
        
        if not name:
            messagebox.showerror("Erreur", "Veuillez entrer votre nom")
            return
            
        if not age_text:
            messagebox.showerror("Erreur", "Veuillez entrer votre âge")
            return
            
        try:
            age = int(age_text)
            if age < 18:
                messagebox.showerror("Accès refusé", "Vous devez avoir au moins 18 ans")
                return
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un âge valide (nombre seulement)")
            return
        
        # Success
        self.user_name = name
        self.verify_window.destroy()
        self.setup_main_window()
        
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            "#4a9eff": "#3a7ed8",
            "#22c55e": "#16a34a", 
            "#f59e0b": "#d97706",
            "#8b5cf6": "#7c3aed",
            "#ef4444": "#dc2626",
            "#6b7280": "#4b5563",
            "#f97316": "#ea580c"
        }
        return color_map.get(color, "#374151")
    
    def setup_main_window(self):
        """Setup the main scanner interface"""
        self.root = tk.Tk()
        self.root.title("Cyber Scanner PRO")
        self.root.geometry("1000x800")
        self.root.configure(bg=self.get_theme_color('bg'))
        self.root.resizable(True, True)
        
        # Configure style for modern look
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Modern.TFrame', background=self.get_theme_color('bg'))
        style.configure('Modern.TLabel', background=self.get_theme_color('bg'), foreground=self.get_theme_color('text'))
        
        self.setup_header()
        self.setup_main_content()
        self.setup_progress_bar()
        self.setup_output_area()
        self.setup_save_section()
        
        self.root.mainloop()
    
    def setup_header(self):
        """Setup header with logo and user info"""
        header_frame = tk.Frame(self.root, bg=self.get_theme_color('bg'))
        header_frame.pack(fill="x", padx=30, pady=(20, 15))
        
        # Logo and title container
        logo_container = tk.Frame(header_frame, bg=self.get_theme_color('bg'))
        logo_container.pack(side="left")
        
        # Shield icon
        shield_label = tk.Label(logo_container, text="🛡️", font=("Segoe UI", 32), 
                               bg=self.get_theme_color('bg'), fg=self.get_theme_color('accent'))
        shield_label.pack(side="left", padx=(0, 12))
        
        # Title
        title_label = tk.Label(logo_container, text="Cyber Scanner PRO", 
                              font=("Segoe UI", 20, "bold"), 
                              bg=self.get_theme_color('bg'), fg=self.get_theme_color('text'))
        title_label.pack(side="left", anchor="w")
        
        # Right side container for user info and buttons
        right_container = tk.Frame(header_frame, bg=self.get_theme_color('bg'))
        right_container.pack(side="right")
        
        # Theme info (dark mode only)
        theme_label = tk.Label(right_container, text="🌙 Dark Mode", 
                              font=("Segoe UI", 9), 
                              bg=self.get_theme_color('bg'), fg=self.get_theme_color('text_muted'))
        theme_label.pack(side="right", padx=(5, 0), pady=8)
        
        # Get My IP button
        ip_btn = tk.Button(right_container, text="🌐 Mon IP", 
                          command=self.get_my_ip,
                          font=("Segoe UI", 9, "bold"), 
                          bg=self.get_theme_color('button_bg'), fg=self.get_theme_color('text'),
                          bd=0, relief="flat", cursor="hand2",
                          width=10,
                          activebackground=self.get_theme_color('secondary_bg'))
        ip_btn.pack(side="right", padx=(10, 5), ipady=4)
        self.ip_btn = ip_btn
        
        # User info
        user_label = tk.Label(right_container, text=f"Utilisateur: {self.user_name}", 
                             font=("Segoe UI", 10), 
                             bg=self.get_theme_color('bg'), fg=self.get_theme_color('text_muted'))
        user_label.pack(side="right", anchor="ne", pady=8, padx=(0, 10))
        self.user_label = user_label
    
    def setup_main_content(self):
        """Setup main content area"""
        content_frame = tk.Frame(self.root, bg=self.get_theme_color('bg'))
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))
        
        # IP/Domain input
        input_frame = tk.Frame(content_frame, bg=self.get_theme_color('bg'))
        input_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(input_frame, text="Adresse IP / Domain :", 
                font=("Segoe UI", 10), bg=self.get_theme_color('bg'), fg=self.get_theme_color('text_secondary')).pack(anchor="w", pady=(0, 6))
        
        self.ip_entry = tk.Entry(input_frame, font=("Segoe UI", 11), 
                                bg=self.get_theme_color('secondary_bg'), fg=self.get_theme_color('text'), 
                                insertbackground=self.get_theme_color('accent'), bd=0, relief="flat")
        self.ip_entry.pack(fill="x", ipady=10)
        
        # Ports input
        ports_frame = tk.Frame(content_frame, bg=self.get_theme_color('bg'))
        ports_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(ports_frame, text="Ports (start-end ou liste, ex: 1-1024 ou 22,80,443):", 
                font=("Segoe UI", 10), bg=self.get_theme_color('bg'), fg=self.get_theme_color('text_secondary')).pack(anchor="w", pady=(0, 6))
        
        self.ports_entry = tk.Entry(ports_frame, font=("Segoe UI", 11), 
                                   bg=self.get_theme_color('secondary_bg'), fg=self.get_theme_color('text'), 
                                   insertbackground=self.get_theme_color('accent'), bd=0, relief="flat")
        self.ports_entry.insert(0, "1-1024")
        self.ports_entry.pack(fill="x", ipady=10)
        
        # Action buttons
        self.setup_action_buttons(content_frame)
        
        # Control buttons (Stop, Clear, etc.)
        self.setup_control_buttons(content_frame)
    
    def setup_action_buttons(self, parent):
        """Setup main action buttons"""
        buttons_frame = tk.Frame(parent, bg=self.get_theme_color('bg'))
        buttons_frame.pack(fill="x", pady=(15, 10))
        
        # Scan speed selection
        speed_frame = tk.Frame(buttons_frame, bg=self.get_theme_color('bg'))
        speed_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(speed_frame, text="Vitesse de scan:", 
                font=("Segoe UI", 9), bg=self.get_theme_color('bg'), fg=self.get_theme_color('text_secondary')).pack(side="left", padx=(0, 10))
        
        self.speed_var = tk.StringVar(value="Normal")
        speed_options = ["Rapide (0.1s)", "Normal (0.5s)", "Lent (1.0s)", "Très Lent (2.0s)"]
        speed_combo = ttk.Combobox(speed_frame, textvariable=self.speed_var, 
                                  values=speed_options, state="readonly", width=15)
        speed_combo.pack(side="left")
        
        # Main action buttons
        main_buttons_frame = tk.Frame(buttons_frame, bg=self.get_theme_color('bg'))
        main_buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Configuration des boutons
        buttons = [
            ("🔍 Scanner Ports", self.start_port_scan, "#4a9eff"),
            (" Test Ping", self.start_ping, "#f59e0b"),
            ("🌐 Géolocalisation IP", self.start_ip_lookup, "#8b5cf6"),
            ("📋 Recherche WHOIS", self.start_whois_lookup, "#f97316"),
            ("📶 Analyse WiFi", self.start_wifi_scan, "#9333ea"),
            ("💻 Infos Système", self.show_system_info, "#ef4444")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(main_buttons_frame, text=text,
                          font=("Segoe UI", 9, "bold"),
                          bg=color, fg="white",
                          bd=0, relief="flat",
                          width=16, height=2,
                          cursor="hand2",
                          command=command,
                          activebackground=self.darken_color(color),
                          activeforeground="white")
            btn.pack(side="left", padx=(0, 8))
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.darken_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
    
    def setup_control_buttons(self, parent):
        """Setup control buttons (Stop, Clear, Export)"""
        control_frame = tk.Frame(parent, bg=self.get_theme_color('bg'))
        control_frame.pack(fill="x", pady=(5, 15))
        
        # Scan control variables
        self.is_scanning = False
        self.stop_scan = False
        
        # Boutons de contrôle
        control_buttons = [
            ("⏹️ Arrêter Scan", self.stop_current_scan, "#ef4444"),
            ("🗑️ Effacer Sortie", self.clear_output, "#6b7280"),
            ("📤 Exporter Résultats", self.export_results, "#22c55e"),
            ("📊 Historique Scans", self.show_scan_history, "#8b5cf6")
        ]
        
        for text, command, color in control_buttons:
            btn = tk.Button(control_frame, text=text,
                          font=("Segoe UI", 9),
                          bg=color, fg="white",
                          bd=0, relief="flat",
                          width=14, height=1,
                          cursor="hand2",
                          command=command,
                          activebackground=self.darken_color(color),
                          activeforeground="white")
            btn.pack(side="left", padx=(0, 8))
            
            # Store stop button reference
            if "Arrêter Scan" in text:
                self.stop_btn = btn
                btn.config(state="disabled")  # Initially disabled
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.darken_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
    
    def setup_progress_bar(self):
        """Setup progress bar"""
        progress_frame = tk.Frame(self.root, bg=self.get_theme_color('bg'))
        progress_frame.pack(fill="x", padx=30, pady=(0, 15))
        
        self.progress = ttk.Progressbar(progress_frame, length=840, mode='determinate',
                                       style='Modern.Horizontal.TProgressbar')
        self.progress.pack(fill="x")
        
        # Style the progress bar
        style = ttk.Style()
        style.configure('Modern.Horizontal.TProgressbar',
                       background='#4a9eff',
                       troughcolor=self.get_theme_color('secondary_bg'),
                       borderwidth=0,
                       thickness=8)
    
    def setup_output_area(self):
        """Setup output text area"""
        output_frame = tk.Frame(self.root, bg=self.get_theme_color('bg'))
        output_frame.pack(fill="both", expand=True, padx=30, pady=(0, 15))
        
        self.output = scrolledtext.ScrolledText(
            output_frame,
            font=("Consolas", 10),
            bg=self.get_theme_color('output_bg'),
            fg=self.get_theme_color('text'),
            insertbackground=self.get_theme_color('accent'),
            selectbackground=self.get_theme_color('secondary_bg'),
            bd=0,
            relief="flat",
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        self.output.pack(fill="both", expand=True)
    
    def setup_save_section(self):
        """Setup save file section"""
        save_frame = tk.Frame(self.root, bg=self.get_theme_color('bg'))
        save_frame.pack(fill="x", padx=30, pady=(0, 25))
        
        # Create inner frame for better layout
        inner_frame = tk.Frame(save_frame, bg=self.get_theme_color('bg'))
        inner_frame.pack(fill="x")
        
        # Étiquette
        tk.Label(inner_frame, text="Fichier de Sauvegarde", 
                font=("Segoe UI", 10), bg=self.get_theme_color('bg'), fg=self.get_theme_color('text_secondary')).pack(side="left", padx=(0, 15))
        
        # Path entry
        self.save_path_var = tk.StringVar()
        # Set default path to output directory
        default_path = os.path.join(os.getcwd(), "output", "scan_results.txt")
        self.save_path_var.set(default_path)
        
        path_entry = tk.Entry(inner_frame, textvariable=self.save_path_var,
                             font=("Segoe UI", 9), bg=self.get_theme_color('secondary_bg'), fg=self.get_theme_color('text_secondary'),
                             state="readonly", bd=0, relief="flat")
        path_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        
        # Browse button
        browse_btn = tk.Button(inner_frame, text="Parcourir", 
                              command=self.browse_save_file,
                              font=("Segoe UI", 9), bg=self.get_theme_color('button_bg'), fg=self.get_theme_color('text'),
                              bd=0, relief="flat", cursor="hand2",
                              width=12,
                              activebackground=self.get_theme_color('secondary_bg'),
                              activeforeground=self.get_theme_color('text'))
        browse_btn.pack(side="right", ipady=8)
    
    def write_output(self, text):
        """Write text to output area"""
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.root.update_idletasks()
    
    def clear_output(self):
        """Clear output area"""
        self.output.delete(1.0, tk.END)
    
    def parse_ports(self, text):
        """Parse ports from text input"""
        text = text.strip()
        if "-" in text:
            try:
                start, end = text.split("-", 1)
                start, end = int(start.strip()), int(end.strip())
                if start > end:
                    start, end = end, start
                return list(range(start, end + 1))
            except:
                return []
        elif "," in text:
            ports = []
            for part in text.split(","):
                try:
                    ports.append(int(part.strip()))
                except:
                    pass
            return ports
        else:
            try:
                return [int(text)]
            except:
                return []
    
    def get_scan_timeout(self):
        """Get timeout based on selected speed"""
        speed = self.speed_var.get()
        if "Rapide" in speed:
            return 0.1
        elif "Normal" in speed:
            return 0.5
        elif "Lent" in speed:
            return 1.0
        else:  # Très lent
            return 2.0
    
    def browse_save_file(self):
        """Browse for save file location"""
        # Set initial directory to output folder
        initial_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(initial_dir, exist_ok=True)
        
        filename = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            initialfile="scan_results.txt",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Choisir l'emplacement du fichier"
        )
        if filename:
            self.save_path_var.set(filename)
    
    def start_port_scan(self):
        """Start port scanning in separate thread"""
        if self.is_scanning:
            messagebox.showwarning("Scan en cours", "Un scan est déjà en cours. Utilisez 'Arrêter Scan' pour l'interrompre.")
            return
            
        target = self.ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Veuillez saisir une adresse IP ou un nom de domaine")
            return
        
        ports_text = self.ports_entry.get().strip()
        ports = self.parse_ports(ports_text)
        if not ports:
            messagebox.showerror("Erreur", "Format de ports non valide")
            return
        
        # Activer le bouton d'arrêt
        self.is_scanning = True
        self.stop_scan = False
        if hasattr(self, 'stop_btn'):
            self.stop_btn.config(state="normal")
        
        self.clear_output()
        timeout = self.get_scan_timeout()
        self.write_output(f"🔍 Analyse des ports en cours sur {target} ({len(ports)} ports)...")
        self.write_output(f"⚙️ Vitesse d'analyse: {self.speed_var.get()} (délai: {timeout}s)")
        self.write_output("=" * 60)
        
        def scan_worker():
            start_time = time.time()
            open_ports = []
            total = len(ports)
            
            for i, port in enumerate(ports):
                # Check for stop request more frequently
                if self.stop_scan:
                    self.write_output("🛑 Analyse interrompue par l'utilisateur")
                    break
                    
                try:
                    if port_scan(target, port, timeout=timeout):
                        service = detect_service(port)
                        self.write_output(f"✅ Port {port:5d} | OUVERT | {service}")
                        open_ports.append((port, service))
                    
                    # Update progress and check for stop again
                    progress_val = (i + 1) / total * 100
                    self.progress['value'] = progress_val
                    
                    # Force GUI update and check stop condition
                    self.root.update_idletasks()
                    if self.stop_scan:
                        self.write_output("🛑 Analyse interrompue par l'utilisateur")
                        break
                    
                except Exception as e:
                    if not self.stop_scan:  # Only show errors if not stopping
                        self.write_output(f"⚠️  Port {port:5d} | Erreur: {str(e)}")
            
            # Résumé des résultats
            self.write_output("=" * 60)
            self.write_output(f"📊 RÉSULTATS DE L'ANALYSE DES PORTS")
            self.write_output(f"   Cible analysée: {target}")
            self.write_output(f"   Ports analysés: {i+1 if not self.stop_scan else len(ports)}")
            self.write_output(f"   Ports ouverts détectés: {len(open_ports)}")
            
            if open_ports:
                self.write_output(f"\n🎯 PORTS OUVERTS DÉTECTÉS:")
                for port, service in open_ports:
                    self.write_output(f"   ✅ Port {port} | {service}")
            
            # Reset scan state
            self.is_scanning = False
            self.stop_scan = False
            if hasattr(self, 'stop_btn'):
                self.stop_btn.config(state="disabled", text="⏹️ Arrêter Scan")
            
            # Sauvegarder dans la base de données
            open_ports_simple = [p[0] for p in open_ports]
            self.db.save_scan(
                scan_type="Analyse de Ports",
                target=target,
                ports_scanned=i+1 if not self.stop_scan else len(ports),
                ports_open=len(open_ports),
                open_ports_list=open_ports_simple,
                duration=time.time() - start_time,
                status="interrompu" if self.stop_scan else "terminé"
            )
            
            # Auto-save results
            self.auto_save_results(target, open_ports, ports_text)
        
        threading.Thread(target=scan_worker, daemon=True).start()
    
    def auto_save_results(self, target, open_ports, ports_text):
        """Auto-save scan results to file"""
        save_path = self.save_path_var.get()
        if save_path:
            try:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(f"Cyber Scanner PRO - Scan Report\n")
                    f.write(f"{'=' * 60}\n\n")
                    f.write(f"Target: {target}\n")
                    f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Ports scannés: {ports_text}\n")
                    f.write(f"Ports ouverts: {len(open_ports)}\n\n")
                    
                    if open_ports:
                        f.write(f"PORTS OUVERTS:\n")
                        for port, service in open_ports:
                            f.write(f"Port {port}: {service}\n")
                    else:
                        f.write(f"Aucun port ouvert trouvé.\n")
                        
                self.write_output(f"\n💾 Résultats sauvegardés: {save_path}")
            except Exception as e:
                self.write_output(f"⚠️  Erreur de sauvegarde: {str(e)}")
    
    def start_ping(self):
        """Démarrer le ping dans un thread séparé"""
        target = self.ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Veuillez saisir une adresse IP ou un nom de domaine")
            return
        
        self.clear_output()
        self.write_output(f"📡 Test de connectivité vers {target}...")
        self.write_output("=" * 60)
        
        def ping_worker():
            try:
                result = ping_host(target, count=4)
                self.write_output(result)
            except Exception as e:
                self.write_output(f"⚠️  Erreur ping: {str(e)}")
        
        threading.Thread(target=ping_worker, daemon=True).start()
    
    def start_ip_lookup(self):
        """Démarrer la recherche IP dans un thread séparé"""
        target = self.ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Veuillez saisir une adresse IP ou un nom de domaine")
            return
        
        self.clear_output()
        self.write_output(f"🌐 Recherche d'informations géographiques pour {target}...")
        self.write_output("=" * 60)
        
        def lookup_worker():
            try:
                result = ip_lookup(target)
                self.write_output(result)
            except Exception as e:
                self.write_output(f"⚠️  Erreur lookup: {str(e)}")
        
        threading.Thread(target=lookup_worker, daemon=True).start()
    
    def start_whois_lookup(self):
        """Démarrer la recherche WHOIS dans un thread séparé"""
        target = self.ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Veuillez saisir un nom de domaine ou une adresse IP")
            return
        
        self.clear_output()
        self.write_output(f"📋 Recherche d'informations WHOIS pour {target}...")
        self.write_output("=" * 60)
        
        def whois_worker():
            try:
                result = whois_lookup(target)
                self.write_output(result)
            except Exception as e:
                self.write_output(f"⚠️  Erreur WHOIS: {str(e)}")
        
        threading.Thread(target=whois_worker, daemon=True).start()
    
    def start_wifi_scan(self):
        """Démarrer l'analyse WiFi dans un thread séparé"""
        self.clear_output()
        self.write_output("📶 Analyse des réseaux WiFi disponibles...")
        self.write_output("=" * 60)
        
        def wifi_worker():
            try:
                result = wifi_scan()
                self.write_output(result)
            except Exception as e:
                self.write_output(f"⚠️  Erreur lors de l'analyse WiFi: {str(e)}")
        
        threading.Thread(target=wifi_worker, daemon=True).start()
    
    def show_system_info(self):
        """Afficher les informations système"""
        self.clear_output()
        self.write_output("💻 Informations du Système")
        self.write_output("=" * 60)
        try:
            result = system_info()
            self.write_output(result)
        except Exception as e:
            self.write_output(f"⚠️  Erreur lors de la récupération: {str(e)}")
    
    def get_my_ip(self):
        """Get public IP and copy to clipboard"""
        def ip_worker():
            try:
                self.write_output("🌐 Récupération de votre IP publique...")
                
                my_ip = get_my_ip()
                
                if my_ip:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(my_ip)
                    self.root.update()
                    
                    self.ip_entry.delete(0, tk.END)
                    self.ip_entry.insert(0, my_ip)
                    
                    self.write_output(f"✅ Votre IP publique: {my_ip}")
                    self.write_output("📋 IP copiée dans le presse-papiers et ajoutée au champ IP")
                    
                    messagebox.showinfo("IP Récupérée", 
                                      f"Votre IP: {my_ip}\n\n✅ Copiée dans le presse-papiers")
                else:
                    self.write_output("❌ Impossible de récupérer votre IP publique")
                    messagebox.showerror("Erreur", "Impossible de récupérer votre IP")
                    
            except Exception as e:
                self.write_output(f"⚠️  Erreur: {str(e)}")
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
        
        threading.Thread(target=ip_worker, daemon=True).start()
    

    def stop_current_scan(self):
        """Arrêter l'analyse en cours"""
        if self.is_scanning:
            self.stop_scan = True
            self.write_output("🛑 Demande d'interruption envoyée... Veuillez patienter.")
            self.write_output("⏳ Arrêt de l'analyse en cours...")
            
            # Désactiver temporairement le bouton d'arrêt pour éviter les clics multiples
            if hasattr(self, 'stop_btn'):
                self.stop_btn.config(state="disabled", text="⏳ Arrêt en cours...")
                # Réactiver après un court délai
                self.root.after(2000, lambda: (
                    self.stop_btn.config(state="normal", text="⏹️ Arrêter Scan") if hasattr(self, 'stop_btn') else None
                ))
        else:
            messagebox.showinfo("Information", "Aucune analyse en cours d'exécution")
    
    def export_results(self):
        """Exporter les résultats actuels vers un fichier"""
        content = self.output.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Attention", "Aucun résultat disponible pour l'exportation")
            return
        
        filename = filedialog.asksaveasfilename(
            initialdir=os.path.join(os.getcwd(), "output"),
            initialfile="cyber_scanner_export.txt",
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
            title="Exporter les résultats d'analyse"
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"Cyber Scanner PRO - Exportation des Résultats\n")
                    f.write(f"{'=' * 50}\n")
                    f.write(f"Date d'exportation: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(content)
                messagebox.showinfo("Exportation Réussie", f"Résultats exportés avec succès vers:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erreur d'Exportation", f"Impossible d'exporter les résultats: {e}")
    
    def show_scan_history(self):
        """Show scan history from database"""
        history_window = tk.Toplevel(self.root)
        history_window.title("📊 Historique des scans - Cyber Scanner PRO")
        history_window.geometry("1000x700")
        history_window.configure(bg=self.get_theme_color('bg'))
        history_window.resizable(True, True)
        
        # Header with statistics
        header_frame = tk.Frame(history_window, bg=self.get_theme_color('bg'))
        header_frame.pack(fill="x", padx=20, pady=15)
        
        # Title
        title_frame = tk.Frame(header_frame, bg=self.get_theme_color('bg'))
        title_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(title_frame, text="📊 Historique des scans", 
                font=("Segoe UI", 18, "bold"), 
                bg=self.get_theme_color('bg'), fg=self.get_theme_color('text')).pack(side="left")
        
        # Statistics
        try:
            stats = self.db.get_scan_statistics()
            stats_text = f"Total: {stats.get('total_scans', 0)} scans | Ports scannés: {stats.get('total_ports_scanned', 0)} | Ports ouverts trouvés: {stats.get('total_open_ports', 0)}"
            tk.Label(title_frame, text=stats_text, 
                    font=("Segoe UI", 10), 
                    bg=self.get_theme_color('bg'), fg=self.get_theme_color('text_muted')).pack(side="right")
        except Exception as e:
            print(f"Erreur stats: {e}")
        
        # Control buttons
        control_frame = tk.Frame(header_frame, bg=self.get_theme_color('bg'))
        control_frame.pack(fill="x", pady=(5, 0))
        
        refresh_btn = tk.Button(control_frame, text="🔄 Actualiser", 
                               command=lambda: self.refresh_history_display(history_text),
                               font=("Segoe UI", 9, "bold"), 
                               bg=self.get_theme_color('accent'), fg="white",
                               bd=0, relief="flat", cursor="hand2",
                               width=12, height=1)
        refresh_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = tk.Button(control_frame, text="🗑️ Vider l'Historique", 
                             command=lambda: self.clear_scan_history_confirm(history_text),
                             font=("Segoe UI", 9, "bold"), 
                             bg="#ef4444", fg="white",
                             bd=0, relief="flat", cursor="hand2",
                             width=15, height=1)
        clear_btn.pack(side="left", padx=(0, 10))
        
        export_btn = tk.Button(control_frame, text="📤 Exporter l'Historique", 
                              command=self.export_scan_history,
                              font=("Segoe UI", 9, "bold"), 
                              bg="#22c55e", fg="white",
                              bd=0, relief="flat", cursor="hand2",
                              width=16, height=1)
        export_btn.pack(side="left")
        
        # History display with improved formatting
        list_frame = tk.Frame(history_window, bg=self.get_theme_color('bg'))
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(list_frame, bg=self.get_theme_color('bg'))
        text_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, bg=self.get_theme_color('secondary_bg'))
        scrollbar.pack(side="right", fill="y")
        
        history_text = tk.Text(text_frame, 
                              font=("Consolas", 9),
                              bg=self.get_theme_color('output_bg'),
                              fg=self.get_theme_color('text'),
                              wrap=tk.WORD,
                              yscrollcommand=scrollbar.set,
                              padx=15, pady=15,
                              bd=0, relief="flat")
        history_text.pack(fill="both", expand=True)
        scrollbar.config(command=history_text.yview)
        
        # Load and display formatted history
        self.load_formatted_history(history_text)
        
        # Store reference for refresh
        self.history_text_widget = history_text
    
    def load_formatted_history(self, text_widget):
        """Load and format scan history"""
        try:
            # Clear existing content
            text_widget.delete(1.0, tk.END)
            
            # En-tête
            text_widget.insert(tk.END, "CYBER SCANNER PRO - HISTORIQUE DES ANALYSES\n")
            text_widget.insert(tk.END, "=" * 80 + "\n\n")
            
            # Charger l'historique depuis la base de données
            history = self.db.get_scan_history(100)
            
            if not history:
                text_widget.insert(tk.END, "📭 Aucune analyse dans l'historique.\n")
                text_widget.insert(tk.END, "💡 Effectuez votre première analyse pour voir les résultats ici!\n")
                return
            
            # Group scans by date
            from datetime import datetime
            current_date = ""
            scan_count = 0
            
            for scan in history:
                try:
                    # Parse timestamp
                    timestamp_str = scan.get('timestamp', '')
                    if 'T' in timestamp_str:
                        dt = datetime.fromisoformat(timestamp_str.replace('T', ' ').split('.')[0])
                        scan_date = dt.strftime('%Y-%m-%d')
                        scan_time = dt.strftime('%H:%M:%S')
                    else:
                        scan_date = "Date inconnue"
                        scan_time = "Heure inconnue"
                    
                    # New date section
                    if scan_date != current_date:
                        if current_date != "":
                            text_widget.insert(tk.END, "\n")
                        
                        current_date = scan_date
                        text_widget.insert(tk.END, f"📅 {scan_date}\n")
                        text_widget.insert(tk.END, "-" * 60 + "\n")
                    
                    scan_count += 1
                    
                    # Détails de l'analyse
                    scan_type = scan.get('scan_type', 'N/A')
                    target = scan.get('target', 'N/A')
                    ports_open = scan.get('ports_open', 0)
                    ports_scanned = scan.get('ports_scanned', 0)
                    duration = scan.get('duration', 0.0)
                    status = scan.get('status', 'terminé')
                    
                    # Icône de statut
                    status_icon = "✅" if status == "terminé" else "⏹️" if status == "interrompu" else "❌"
                    
                    # Format duration
                    if duration > 60:
                        duration_str = f"{duration/60:.1f}m"
                    else:
                        duration_str = f"{duration:.1f}s"
                    
                    # Scan entry
                    text_widget.insert(tk.END, f"{status_icon} {scan_time} | {scan_type:<15} | {target:<25}\n")
                    
                    if "Port" in scan_type:
                        text_widget.insert(tk.END, f"    📊 Résultats: {ports_open}/{ports_scanned} ports ouverts | Durée: {duration_str}\n")
                        
                        # Afficher les ports ouverts si disponibles
                        open_ports_str = scan.get('open_ports', '[]')
                        try:
                            import json
                            open_ports = json.loads(open_ports_str)
                            if open_ports and len(open_ports) > 0:
                                if len(open_ports) <= 10:
                                    ports_display = ', '.join(map(str, open_ports))
                                    text_widget.insert(tk.END, f"    🎯 Ports détectés: {ports_display}\n")
                                else:
                                    text_widget.insert(tk.END, f"    🎯 Ports détectés: {', '.join(map(str, open_ports[:10]))}... (+{len(open_ports)-10} autres)\n")
                        except:
                            pass
                    else:
                        text_widget.insert(tk.END, f"    ⏱️ Durée d'exécution: {duration_str}\n")
                    
                    text_widget.insert(tk.END, "\n")
                    
                except Exception as e:
                    text_widget.insert(tk.END, f"❌ Erreur lors du formatage d'un scan: {e}\n")
                    continue
            
            # Résumé
            text_widget.insert(tk.END, "=" * 80 + "\n")
            text_widget.insert(tk.END, f"📈 Total des analyses affichées: {scan_count}\n")
            text_widget.insert(tk.END, f"🕒 Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
        except Exception as e:
            text_widget.insert(tk.END, f"❌ Erreur lors du chargement de l'historique: {e}\n")
            print(f"Erreur détaillée: {e}")
    
    def refresh_history_display(self, text_widget):
        """Actualiser l'affichage de l'historique"""
        self.load_formatted_history(text_widget)
        messagebox.showinfo("Actualisé", "Historique des analyses mis à jour avec succès!")
    
    def clear_scan_history_confirm(self, text_widget):
        """Confirmer et vider l'historique des analyses"""
        if messagebox.askyesno("Confirmation de Suppression", 
                              "⚠️ Êtes-vous certain de vouloir supprimer TOUT l'historique?\n\n"
                              "Cette action est définitive et irréversible!"):
            try:
                if self.db.clear_history():
                    self.load_formatted_history(text_widget)
                    messagebox.showinfo("Suppression Réussie", "✅ Historique des analyses supprimé avec succès!")
                else:
                    messagebox.showerror("Erreur de Suppression", "❌ Impossible de supprimer l'historique")
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ Erreur lors de la suppression: {e}")
    
    def export_scan_history(self):
        """Export scan history to file"""
        try:
            history = self.db.get_scan_history(1000)  # Export more records
            
            if not history:
                messagebox.showwarning("Attention", "Aucun historique à exporter")
                return
            
            filename = filedialog.asksaveasfilename(
                initialdir=os.path.join(os.getcwd(), "output"),
                initialfile="scan_history_export.txt",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")],
                title="Exporter l'historique"
            )
            
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("CYBER SCANNER PRO - EXPORT HISTORIQUE\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(f"Date d'export: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Nombre de scans: {len(history)}\n\n")
                    
                    for scan in history:
                        f.write(f"Timestamp: {scan.get('timestamp', 'N/A')}\n")
                        f.write(f"Type: {scan.get('scan_type', 'N/A')}\n")
                        f.write(f"Cible: {scan.get('target', 'N/A')}\n")
                        f.write(f"Ports scannés: {scan.get('ports_scanned', 0)}\n")
                        f.write(f"Ports ouverts: {scan.get('ports_open', 0)}\n")
                        f.write(f"Durée: {scan.get('duration', 0.0):.2f}s\n")
                        f.write(f"Statut: {scan.get('status', 'N/A')}\n")
                        f.write("-" * 40 + "\n\n")
                
                messagebox.showinfo("Succès", f"Historique exporté vers:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {e}")
    
    def toggle_theme(self):
        """Theme is locked to dark mode"""
        messagebox.showinfo("Mode sombre", "L'application utilise uniquement le mode sombre pour une expérience optimale.")

if __name__ == "__main__":
    app = CyberScannerPRO()
