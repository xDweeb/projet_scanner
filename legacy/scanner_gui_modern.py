import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import time
import os
from PIL import Image, ImageTk
from scanner_functions import port_scan, system_info, ip_lookup, ping_host, wifi_scan, get_my_ip, whois_lookup
from database import ScanDatabase

class CyberScannerPRO:
    def __init__(self):
        # Initialize database
              # Button configuration
        buttons = [
            ("🔍 Scan Ports", self.start_port_scan, "#4a9eff"),
            ("🔍 Network Discovery", self.start_network_discovery, "#22c55e"),
            ("📡 Ping", self.start_ping, "#f59e0b"),
            ("🌐 IP Lookup", self.start_ip_lookup, "#8b5cf6"),
            ("📋 WHOIS Lookup", self.start_whois_lookup, "#f97316"),
            ("💻 System Info", self.show_system_info, "#ef4444")
        ]b = ScanDatabase()
        
        # Load theme preference
        self.current_theme = self.db.get_setting('theme', 'dark')
        
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
    
    def show_splash_screen(self):
        """Show splash screen with logo for 3 seconds"""
        self.splash = tk.Tk()
        self.splash.title("Cyber Scanner PRO")
        self.splash.geometry("500x400")
        self.splash.configure(bg="#0f1419")
        self.splash.resizable(False, False)
        self.splash.overrideredirect(True)  # Remove title bar
        
        # Center the splash screen
        self.splash.eval('tk::PlaceWindow . center')
        
        # Main container
        container = tk.Frame(self.splash, bg="#0f1419")
        container.pack(fill="both", expand=True, padx=50, pady=50)
        
        try:
            # Try to load the logo image
            logo_path = r"C:\Users\xdweb\Downloads\projet_scanner\logo.png"
            if os.path.exists(logo_path):
                # Load and resize logo
                logo_img = Image.open(logo_path)
                # Resize to fit nicely in splash screen
                logo_img = logo_img.resize((300, 200), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                
                # Display logo
                logo_label = tk.Label(container, image=self.logo_photo, bg="#0f1419")
                logo_label.pack(pady=(20, 30))
            else:
                # Fallback if logo not found - show text logo
                logo_label = tk.Label(container, text="🛡️", font=("Segoe UI", 60), 
                                     bg="#0f1419", fg="#4a9eff")
                logo_label.pack(pady=(20, 10))
                
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback logo
            logo_label = tk.Label(container, text="🛡️", font=("Segoe UI", 60), 
                                 bg="#0f1419", fg="#4a9eff")
            logo_label.pack(pady=(20, 10))
        
        # App title
        title_label = tk.Label(container, text="Cyber Scanner PRO", 
                              font=("Segoe UI", 24, "bold"), 
                              fg="#ffffff", bg="#0f1419")
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(container, text="Professional Network Security Scanner", 
                                 font=("Segoe UI", 12), 
                                 fg="#6b7280", bg="#0f1419")
        subtitle_label.pack(pady=(0, 30))
        
        # Loading animation
        self.loading_label = tk.Label(container, text="Chargement", 
                                     font=("Segoe UI", 11), 
                                     fg="#4a9eff", bg="#0f1419")
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
            if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
                self.loading_label.config(text=texts[index % len(texts)])
                self.splash.after(300, lambda: update_text((index + 1) % len(texts)))
        
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
        self.verify_window.configure(bg="#0f1419")
        self.verify_window.resizable(False, False)
        
        # Center the window
        self.verify_window.eval('tk::PlaceWindow . center')
        
        # Main container with padding
        container = tk.Frame(self.verify_window, bg="#0f1419")
        container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Shield icon
        shield_label = tk.Label(container, text="🔒", font=("Segoe UI", 40), 
                               bg="#0f1419", fg="#4a9eff")
        shield_label.pack(pady=(0, 10))
        
        # Title
        title_label = tk.Label(container, text="Cyber Scanner PRO", 
                              font=("Segoe UI", 22, "bold"), 
                              fg="#ffffff", bg="#0f1419")
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(container, text="Vérification d'accès", 
                                 font=("Segoe UI", 11), 
                                 fg="#6b7280", bg="#0f1419")
        subtitle_label.pack(pady=(0, 30))
        
        # Name input
        tk.Label(container, text="Nom d'utilisateur", 
                font=("Segoe UI", 10), fg="#9ca3af", bg="#0f1419").pack(anchor="w", pady=(0, 5))
        
        self.name_entry = tk.Entry(container, font=("Segoe UI", 11), 
                                  bg="#1a1f2e", fg="white", 
                                  insertbackground="#4a9eff", bd=0, relief="flat")
        self.name_entry.pack(fill="x", ipady=10)
        
        # Age input
        tk.Label(container, text="Âge", 
                font=("Segoe UI", 10), fg="#9ca3af", bg="#0f1419").pack(anchor="w", pady=(15, 5))
        
        self.age_entry = tk.Entry(container, font=("Segoe UI", 11), 
                                 bg="#1a1f2e", fg="white", 
                                 insertbackground="#4a9eff", bd=0, relief="flat")
        self.age_entry.pack(fill="x", ipady=10)
        
        # Verify button
        verify_btn = tk.Button(container, text="✅ Accéder à l'application", 
                              font=("Segoe UI", 12, "bold"), 
                              bg="#4a9eff", fg="white", 
                              command=self.verify_access, 
                              bd=0, relief="flat", cursor="hand2",
                              activebackground="#3a7ed8",
                              activeforeground="white")
        verify_btn.pack(fill="x", pady=(30, 10), ipady=15)
        
        # Hover effects
        verify_btn.bind("<Enter>", lambda e: verify_btn.config(bg="#3a7ed8"))
        verify_btn.bind("<Leave>", lambda e: verify_btn.config(bg="#4a9eff"))
        
        # Status label
        self.status_label = tk.Label(container, text="Entrez vos informations pour continuer", 
                                    font=("Segoe UI", 9), fg="#6b7280", bg="#0f1419")
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
    
    def setup_main_window(self):
        """Setup the main scanner interface"""
        self.root = tk.Tk()
        self.root.title("Cyber Scanner PRO")
        self.root.geometry("900x750")
        self.root.configure(bg="#0f1419")
        self.root.resizable(True, True)
        
        # Configure style for modern look
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Modern.TFrame', background='#0f1419')
        style.configure('Modern.TLabel', background='#0f1419', foreground='white')
        
        self.setup_header()
        self.setup_main_content()
        self.setup_progress_bar()
        self.setup_output_area()
        self.setup_save_section()
        
        self.root.mainloop()
    
    def setup_header(self):
        """Setup header with logo and user info"""
        header_frame = tk.Frame(self.root, bg="#0f1419")
        header_frame.pack(fill="x", padx=30, pady=(20, 15))
        
        # Logo and title container
        logo_container = tk.Frame(header_frame, bg="#0f1419")
        logo_container.pack(side="left")
        
        # Shield icon
        shield_label = tk.Label(logo_container, text="🔒", font=("Segoe UI", 32), 
                               bg="#0f1419", fg="#4a9eff")
        shield_label.pack(side="left", padx=(0, 12))
        
        # Title
        title_label = tk.Label(logo_container, text="Cyber Scanner PRO", 
                              font=("Segoe UI", 20, "bold"), 
                              bg="#0f1419", fg="white")
        title_label.pack(side="left", anchor="w")
        
        # Right side container for user info and buttons
        right_container = tk.Frame(header_frame, bg=self.get_theme_color('bg'))
        right_container.pack(side="right")
        
        # Theme toggle button
        theme_btn = tk.Button(right_container, text="�" if self.current_theme == 'dark' else "☀️", 
                             command=self.toggle_theme,
                             font=("Segoe UI", 12), 
                             bg=self.get_theme_color('button_bg'), fg=self.get_theme_color('text'),
                             bd=0, relief="flat", cursor="hand2",
                             width=3,
                             activebackground=self.get_theme_color('secondary_bg'))
        theme_btn.pack(side="right", padx=(5, 0), ipady=4)
        self.theme_btn = theme_btn
        
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
        content_frame = tk.Frame(self.root, bg="#0f1419")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))
        
        # IP/Domain input
        input_frame = tk.Frame(content_frame, bg="#0f1419")
        input_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(input_frame, text="Adresse IP / Domain :", 
                font=("Segoe UI", 10), bg="#0f1419", fg="#9ca3af").pack(anchor="w", pady=(0, 6))
        
        self.ip_entry = tk.Entry(input_frame, font=("Segoe UI", 11), 
                                bg="#1a1f2e", fg="white", 
                                insertbackground="#4a9eff", bd=0, relief="flat")
        self.ip_entry.pack(fill="x", ipady=10)
        
        # Ports input
        ports_frame = tk.Frame(content_frame, bg="#0f1419")
        ports_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(ports_frame, text="Ports (start-end ou liste, ex: 1-1024 ou 22,80,443):", 
                font=("Segoe UI", 10), bg="#0f1419", fg="#9ca3af").pack(anchor="w", pady=(0, 6))
        
        self.ports_entry = tk.Entry(ports_frame, font=("Segoe UI", 11), 
                                   bg="#1a1f2e", fg="white", 
                                   insertbackground="#4a9eff", bd=0, relief="flat")
        self.ports_entry.insert(0, "1-1024")
        self.ports_entry.pack(fill="x", ipady=10)
        
        # Action buttons
        self.setup_action_buttons(content_frame)
        
        # Control buttons (Stop, Clear, etc.)
        self.setup_control_buttons(content_frame)
    
    def setup_action_buttons(self, parent):
        """Setup main action buttons"""
        buttons_frame = tk.Frame(parent, bg="#0f1419")
        buttons_frame.pack(fill="x", pady=(15, 10))
        
        # Scan speed selection
        speed_frame = tk.Frame(buttons_frame, bg="#0f1419")
        speed_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(speed_frame, text="Vitesse de scan:", 
                font=("Segoe UI", 9), bg="#0f1419", fg="#9ca3af").pack(side="left", padx=(0, 10))
        
        self.speed_var = tk.StringVar(value="Normal")
        speed_options = ["Rapide (0.1s)", "Normal (0.5s)", "Lent (1.0s)", "Très lent (2.0s)"]
        speed_combo = ttk.Combobox(speed_frame, textvariable=self.speed_var, 
                                  values=speed_options, state="readonly", width=15)
        speed_combo.pack(side="left")
        
        # Main action buttons
        main_buttons_frame = tk.Frame(buttons_frame, bg="#0f1419")
        main_buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Button configuration
        buttons = [
            ("🔍 Scan Ports", self.start_port_scan, "#4a9eff"),
            ("� Network Discovery", self.start_network_discovery, "#22c55e"),
            ("�📡 Ping", self.start_ping, "#f59e0b"),
            ("🌐 IP Lookup", self.start_ip_lookup, "#8b5cf6"),
            ("💻 System Info", self.show_system_info, "#ef4444")
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
        control_frame = tk.Frame(parent, bg="#0f1419")
        control_frame.pack(fill="x", pady=(5, 15))
        
        # Scan control variables
        self.is_scanning = False
        self.stop_scan = False
        
        # Control buttons
        control_buttons = [
            ("⏹️ Stop Scan", self.stop_current_scan, "#ef4444"),
            ("🗑️ Clear Output", self.clear_output, "#6b7280"),
            ("📤 Export Results", self.export_results, "#22c55e"),
            ("📊 Scan History", self.show_scan_history, "#8b5cf6")
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
            if "Stop" in text:
                self.stop_btn = btn
                btn.config(state="disabled")  # Initially disabled
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.darken_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            "#4a9eff": "#3a7ed8",
            "#22c55e": "#16a34a", 
            "#f59e0b": "#d97706",
            "#8b5cf6": "#7c3aed",
            "#ef4444": "#dc2626",
            "#6b7280": "#4b5563"
        }
        return color_map.get(color, "#374151")
    
    def setup_progress_bar(self):
        """Setup progress bar"""
        progress_frame = tk.Frame(self.root, bg="#0f1419")
        progress_frame.pack(fill="x", padx=30, pady=(0, 15))
        
        self.progress = ttk.Progressbar(progress_frame, length=840, mode='determinate',
                                       style='Modern.Horizontal.TProgressbar')
        self.progress.pack(fill="x")
        
        # Style the progress bar
        style = ttk.Style()
        style.configure('Modern.Horizontal.TProgressbar',
                       background='#4a9eff',
                       troughcolor='#1a1f2e',
                       borderwidth=0,
                       thickness=8)
    
    def setup_output_area(self):
        """Setup output text area"""
        output_frame = tk.Frame(self.root, bg="#0f1419")
        output_frame.pack(fill="both", expand=True, padx=30, pady=(0, 15))
        
        self.output = scrolledtext.ScrolledText(
            output_frame,
            font=("Consolas", 10),
            bg="#0a0e14",
            fg="#e5e5e5",
            insertbackground="#4a9eff",
            selectbackground="#1a1f2e",
            bd=0,
            relief="flat",
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        self.output.pack(fill="both", expand=True)
    
    def setup_save_section(self):
        """Setup save file section"""
        save_frame = tk.Frame(self.root, bg="#0f1419")
        save_frame.pack(fill="x", padx=30, pady=(0, 25))
        
        # Create inner frame for better layout
        inner_frame = tk.Frame(save_frame, bg="#0f1419")
        inner_frame.pack(fill="x")
        
        # Label
        tk.Label(inner_frame, text="Choose Save File", 
                font=("Segoe UI", 10), bg="#0f1419", fg="#9ca3af").pack(side="left", padx=(0, 15))
        
        # Path entry
        self.save_path_var = tk.StringVar()
        # Set default path to current project directory
        default_path = os.path.join(os.getcwd(), "scan_results.txt")
        self.save_path_var.set(default_path)
        
        path_entry = tk.Entry(inner_frame, textvariable=self.save_path_var,
                             font=("Segoe UI", 9), bg="#1a1f2e", fg="#9ca3af",
                             state="readonly", bd=0, relief="flat")
        path_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        
        # Browse button
        browse_btn = tk.Button(inner_frame, text="Parcourir", 
                              command=self.browse_save_file,
                              font=("Segoe UI", 9), bg="#1a1f2e", fg="white",
                              bd=0, relief="flat", cursor="hand2",
                              width=12,
                              activebackground="#252b3b",
                              activeforeground="white")
        browse_btn.pack(side="right", ipady=8)
        
        # Hover effect
        browse_btn.bind("<Enter>", lambda e: browse_btn.config(bg="#252b3b"))
        browse_btn.bind("<Leave>", lambda e: browse_btn.config(bg="#1a1f2e"))
    
    def browse_save_file(self):
        """Browse for save file location"""
        # Set initial directory to current project folder
        initial_dir = os.getcwd()
        filename = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            initialfile="scan_results.txt",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Choisir l'emplacement du fichier"
        )
        if filename:
            self.save_path_var.set(filename)
    
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
    
    def start_port_scan(self):
        """Start port scanning in separate thread"""
        if self.is_scanning:
            messagebox.showwarning("Scan en cours", "Un scan est déjà en cours. Utilisez 'Stop Scan' pour l'arrêter.")
            return
            
        target = self.ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Veuillez entrer une adresse IP ou un domaine")
            return
        
        ports_text = self.ports_entry.get().strip()
        ports = self.parse_ports(ports_text)
        if not ports:
            messagebox.showerror("Erreur", "Format de ports invalide")
            return
        
        # Enable stop button, disable scan button
        self.is_scanning = True
        self.stop_scan = False
        self.stop_btn.config(state="normal")
        
        self.clear_output()
        timeout = self.get_scan_timeout()
        self.write_output(f"🔍 Scan en cours de {target} sur {len(ports)} ports...")
        self.write_output(f"⚙️ Vitesse: {self.speed_var.get()} (timeout: {timeout}s)")
        self.write_output("=" * 60)
        
        def scan_worker():
            start_time = time.time()
            open_ports = []
            total = len(ports)
            
            # Show scan progress every 100 ports or for small scans
            show_interval = max(1, min(100, total // 10)) if total > 50 else 1
            
            for i, port in enumerate(ports):
                # Check for stop request
                if self.stop_scan:
                    self.write_output("🛑 Scan arrêté par l'utilisateur")
                    break
                    
                try:
                    if port_scan(target, port, timeout=timeout):
                        service = self.detect_service(port)
                        self.write_output(f"✅ Port {port:5d} | OUVERT | {service}")
                        open_ports.append((port, service))
                    else:
                        # Only show closed ports for small scans or at intervals
                        if total <= 50 or (i + 1) % show_interval == 0:
                            self.write_output(f"🔍 Progression: {i+1}/{total} ports scannés...")
                except Exception as e:
                    self.write_output(f"⚠️  Port {port:5d} | Erreur: {str(e)}")
                
                # Update progress
                progress_val = (i + 1) / total * 100
                self.progress['value'] = progress_val
                self.root.update_idletasks()
            
            self.write_output("=" * 60)
            self.write_output(f"📊 RÉSULTATS DU SCAN")
            self.write_output(f"   Cible: {target}")
            self.write_output(f"   Ports scannés: {i+1 if not self.stop_scan else len(ports)}")
            self.write_output(f"   Ports ouverts: {len(open_ports)}")
            
            if open_ports:
                self.write_output(f"\n🎯 PORTS OUVERTS TROUVÉS:")
                for port_info in open_ports:
                    if isinstance(port_info, tuple):
                        port, service = port_info
                        self.write_output(f"   ✅ Port {port} | {service}")
                    else:
                        self.write_output(f"   ✅ Port {port_info}")
                port_list = [str(p[0]) if isinstance(p, tuple) else str(p) for p in open_ports]
                self.write_output(f"\n📋 Liste complète: {', '.join(port_list)}")
            else:
                self.write_output(f"   ❌ Aucun port ouvert trouvé")
            
            # Disable stop button, enable scan button
            self.is_scanning = False
            self.stop_scan = False
            self.stop_btn.config(state="disabled")
            
            # Save scan to database
            open_ports_simple = [p[0] if isinstance(p, tuple) else p for p in open_ports]
            self.db.save_scan(
                scan_type="Port Scan",
                target=target,
                ports_scanned=i+1 if not self.stop_scan else len(ports),
                ports_open=len(open_ports),
                open_ports_list=open_ports_simple,
                duration=time.time() - start_time,
                status="stopped" if self.stop_scan else "completed"
            )
            
            # Auto-save if path is set
            save_path = self.save_path_var.get()
            if save_path:
                try:
                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(f"Cyber Scanner PRO - Scan Report\n")
                        f.write(f"{'=' * 60}\n\n")
                        f.write(f"Target: {target}\n")
                        f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Ports scannés: {len(ports)}\n")
                        f.write(f"Ports ouverts: {len(open_ports)}\n\n")
                        
                        if open_ports:
                            f.write(f"PORTS OUVERTS:\n")
                            for port in open_ports:
                                f.write(f"Port {port}: OUVERT\n")
                        else:
                            f.write(f"Aucun port ouvert trouvé.\n")
                            
                        f.write(f"\nRange scanné: {ports_text}\n")
                        
                    self.write_output(f"\n💾 Résultats sauvegardés: {save_path}")
                except Exception as e:
                    self.write_output(f"⚠️  Erreur de sauvegarde: {str(e)}")
                    # Try alternative path in current directory
                    try:
                        alt_path = os.path.join(os.getcwd(), "scan_results_backup.txt")
                        with open(alt_path, "w", encoding="utf-8") as f:
                            f.write(f"Cyber Scanner PRO - Scan Report\n")
                            f.write(f"Target: {target}\n")
                            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(f"Ports ouverts: {len(open_ports)}\n")
                            for port in open_ports:
                                f.write(f"Port {port}: OUVERT\n")
                        self.write_output(f"💾 Sauvegarde alternative: {alt_path}")
                    except:
                        self.write_output(f"❌ Impossible de sauvegarder les résultats")
        
        threading.Thread(target=scan_worker, daemon=True).start()
    
    def start_ping(self):
        """Start ping in separate thread"""
        target = self.ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Veuillez entrer une adresse IP ou un domaine")
            return
        
        self.clear_output()
        self.write_output(f"📡 Ping de {target}...")
        self.write_output("=" * 60)
        
        def ping_worker():
            try:
                result = ping_host(target, count=4)
                self.write_output(result)
            except Exception as e:
                self.write_output(f"⚠️  Erreur ping: {str(e)}")
        
        threading.Thread(target=ping_worker, daemon=True).start()
    
    def start_ip_lookup(self):
        """Start IP lookup in separate thread"""
        target = self.ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Veuillez entrer une adresse IP ou un domaine")
            return
        
        self.clear_output()
        self.write_output(f"🌐 Recherche d'informations pour {target}...")
        self.write_output("=" * 60)
        
        def lookup_worker():
            try:
                result = ip_lookup(target)
                self.write_output(result)
            except Exception as e:
                self.write_output(f"⚠️  Erreur lookup: {str(e)}")
        
        threading.Thread(target=lookup_worker, daemon=True).start()
    
    def show_system_info(self):
        """Show system information"""
        self.clear_output()
        self.write_output("💻 Informations système")
        self.write_output("=" * 60)
        try:
            result = system_info()
            self.write_output(result)
        except Exception as e:
            self.write_output(f"⚠️  Erreur: {str(e)}")
    
    def get_my_ip(self):
        """Get public IP and copy to clipboard"""
        def ip_worker():
            try:
                # Show loading message
                self.write_output("🌐 Récupération de votre IP publique...")
                
                # Get IP
                my_ip = get_my_ip()
                
                if my_ip:
                    # Copy to clipboard
                    self.root.clipboard_clear()
                    self.root.clipboard_append(my_ip)
                    self.root.update()  # Ensure clipboard is updated
                    
                    # Also set in IP entry field
                    self.ip_entry.delete(0, tk.END)
                    self.ip_entry.insert(0, my_ip)
                    
                    # Show success message
                    self.write_output(f"✅ Votre IP publique: {my_ip}")
                    self.write_output("📋 IP copiée dans le presse-papiers et ajoutée au champ IP")
                    
                    # Show success popup
                    messagebox.showinfo("IP Récupérée", 
                                      f"Votre IP: {my_ip}\n\n✅ Copiée dans le presse-papiers\n✅ Ajoutée au champ de saisie")
                else:
                    self.write_output("❌ Impossible de récupérer votre IP publique")
                    messagebox.showerror("Erreur", "Impossible de récupérer votre IP.\nVérifiez votre connexion internet.")
                    
            except Exception as e:
                self.write_output(f"⚠️  Erreur lors de la récupération IP: {str(e)}")
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
        
        # Run in separate thread to avoid blocking UI
        threading.Thread(target=ip_worker, daemon=True).start()
    
    def detect_service(self, port):
        """Detect common services on ports"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
            995: "POP3S", 3389: "RDP", 5432: "PostgreSQL", 3306: "MySQL",
            1433: "MSSQL", 6379: "Redis", 27017: "MongoDB", 8080: "HTTP-Alt",
            8443: "HTTPS-Alt", 2222: "SSH-Alt", 8888: "HTTP-Proxy"
        }
        return services.get(port, "Service inconnu")
    
    def stop_current_scan(self):
        """Stop the current scan"""
        if self.is_scanning:
            self.stop_scan = True
            self.write_output("🛑 Demande d'arrêt envoyée...")
        else:
            messagebox.showinfo("Info", "Aucun scan en cours")
    
    def export_results(self):
        """Export current output to file"""
        content = self.output.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Attention", "Aucun résultat à exporter")
            return
        
        filename = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            initialfile="cyber_scanner_export.txt",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("HTML files", "*.html"), ("All files", "*.*")],
            title="Exporter les résultats"
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"Cyber Scanner PRO - Export\n")
                    f.write(f"{'=' * 50}\n")
                    f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(content)
                messagebox.showinfo("Succès", f"Résultats exportés vers:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'export: {e}")
    
    def show_scan_history(self):
        """Show scan history"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Historique des scans")
        history_window.geometry("600x400")
        history_window.configure(bg="#0f1419")
        
        tk.Label(history_window, text="📊 Historique des scans", 
                font=("Segoe UI", 16, "bold"), 
                bg="#0f1419", fg="white").pack(pady=10)
        
        # For now, show a placeholder
        tk.Label(history_window, text="Fonctionnalité en développement\nL'historique sera disponible prochainement", 
                font=("Segoe UI", 12), 
                bg="#0f1419", fg="#6b7280").pack(pady=50)
    
    def start_network_discovery(self):
        """Start network discovery scan"""
        if self.is_scanning:
            messagebox.showwarning("Scan en cours", "Un scan est déjà en cours")
            return
        
        target = self.ip_entry.get().strip()
        if not target:
            # Try to get local network range
            try:
                import socket
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                # Get network range (assumes /24)
                network_base = '.'.join(local_ip.split('.')[:-1])
                target = f"{network_base}.1-254"
                self.ip_entry.delete(0, tk.END)
                self.ip_entry.insert(0, target)
            except:
                messagebox.showerror("Erreur", "Veuillez entrer une plage d'IPs (ex: 192.168.1.1-254)")
                return
        
        self.is_scanning = True
        self.stop_scan = False
        self.stop_btn.config(state="normal")
        
        self.clear_output()
        self.write_output(f"🔍 Découverte réseau en cours...")
        self.write_output(f"🎯 Cible: {target}")
        self.write_output("=" * 60)
        
        def discovery_worker():
            try:
                # Parse IP range
                if '-' in target:
                    base_ip = '.'.join(target.split('.')[:-1])
                    start_end = target.split('.')[-1].split('-')
                    start_host = int(start_end[0])
                    end_host = int(start_end[1])
                    
                    alive_hosts = []
                    total = end_host - start_host + 1
                    
                    for i in range(start_host, end_host + 1):
                        if self.stop_scan:
                            break
                            
                        test_ip = f"{base_ip}.{i}"
                        # Quick ping test
                        result = ping_host(test_ip, count=1)
                        if "TTL" in result or "ttl" in result:
                            self.write_output(f"✅ {test_ip} | ACTIF")
                            alive_hosts.append(test_ip)
                        
                        progress = ((i - start_host + 1) / total) * 100
                        self.progress['value'] = progress
                        self.root.update_idletasks()
                    
                    self.write_output("=" * 60)
                    self.write_output(f"📊 Découverte terminée")
                    self.write_output(f"   Hôtes testés: {total}")
                    self.write_output(f"   Hôtes actifs: {len(alive_hosts)}")
                    
                    if alive_hosts:
                        self.write_output(f"\n🎯 HÔTES ACTIFS:")
                        for host in alive_hosts:
                            self.write_output(f"   ✅ {host}")
                
            except Exception as e:
                self.write_output(f"⚠️ Erreur: {e}")
            finally:
                self.is_scanning = False
                self.stop_scan = False
                self.stop_btn.config(state="disabled")
        
        threading.Thread(target=discovery_worker, daemon=True).start()
    
    def get_theme_color(self, color_key):
        """Get color for current theme"""
        return self.themes[self.current_theme][color_key]
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.db.set_setting('theme', self.current_theme)
        
        # Show restart message
        messagebox.showinfo("Thème changé", 
                           "Le thème a été changé. Redémarrez l'application pour voir les modifications.")
    
    def start_whois_lookup(self):
        """Start WHOIS lookup in separate thread"""
        target = self.ip_entry.get().strip()
        if not target:
            messagebox.showerror("Erreur", "Veuillez entrer un domaine ou une IP")
            return
        
        self.clear_output()
        self.write_output(f"📋 Recherche WHOIS pour {target}...")
        self.write_output("=" * 60)
        
        def whois_worker():
            try:
                start_time = time.time()
                result = whois_lookup(target)
                duration = time.time() - start_time
                
                self.write_output(result)
                
                # Save to database
                self.db.save_scan(
                    scan_type="WHOIS",
                    target=target,
                    duration=duration,
                    results=result
                )
                
            except Exception as e:
                self.write_output(f"⚠️  Erreur WHOIS: {str(e)}")
        
        threading.Thread(target=whois_worker, daemon=True).start()
    
    def show_scan_history(self):
        """Show scan history from database"""
        history_window = tk.Toplevel(self.root)
        history_window.title("📊 Historique des scans")
        history_window.geometry("800x600")
        history_window.configure(bg=self.get_theme_color('bg'))
        
        # Header
        header_frame = tk.Frame(history_window, bg=self.get_theme_color('bg'))
        header_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(header_frame, text="📊 Historique des scans", 
                font=("Segoe UI", 16, "bold"), 
                bg=self.get_theme_color('bg'), fg=self.get_theme_color('text')).pack(side="left")
        
        # Statistics
        stats = self.db.get_scan_statistics()
        stats_text = f"Total: {stats.get('total_scans', 0)} | Ports scannés: {stats.get('total_ports_scanned', 0)} | Ports ouverts: {stats.get('total_open_ports', 0)}"
        tk.Label(header_frame, text=stats_text, 
                font=("Segoe UI", 10), 
                bg=self.get_theme_color('bg'), fg=self.get_theme_color('text_muted')).pack(side="right")
        
        # History listbox with scrollbar
        list_frame = tk.Frame(history_window, bg=self.get_theme_color('bg'))
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        history_list = tk.Listbox(list_frame, 
                                 font=("Consolas", 10),
                                 bg=self.get_theme_color('output_bg'),
                                 fg=self.get_theme_color('text'),
                                 selectbackground=self.get_theme_color('accent'),
                                 yscrollcommand=scrollbar.set)
        history_list.pack(fill="both", expand=True)
        scrollbar.config(command=history_list.yview)
        
        # Load history
        history = self.db.get_scan_history(100)
        for scan in history:
            timestamp = scan['timestamp'].split('T')[0] + ' ' + scan['timestamp'].split('T')[1][:8]
            line = f"{timestamp} | {scan['scan_type']:12} | {scan['target']:20} | Ports: {scan['ports_open']}/{scan['ports_scanned']}"
            history_list.insert(tk.END, line)
        
        # Buttons
        btn_frame = tk.Frame(history_window, bg=self.get_theme_color('bg'))
        btn_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Button(btn_frame, text="🔄 Actualiser", 
                 command=lambda: self.refresh_history(history_list),
                 bg=self.get_theme_color('accent'), fg="white",
                 font=("Segoe UI", 10), bd=0, cursor="hand2").pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="🗑️ Effacer l'historique", 
                 command=lambda: self.clear_scan_history(history_list),
                 bg="#ef4444", fg="white",
                 font=("Segoe UI", 10), bd=0, cursor="hand2").pack(side="left")
    
    def refresh_history(self, listbox):
        """Refresh history listbox"""
        listbox.delete(0, tk.END)
        history = self.db.get_scan_history(100)
        for scan in history:
            timestamp = scan['timestamp'].split('T')[0] + ' ' + scan['timestamp'].split('T')[1][:8]
            line = f"{timestamp} | {scan['scan_type']:12} | {scan['target']:20} | Ports: {scan['ports_open']}/{scan['ports_scanned']}"
            listbox.insert(tk.END, line)
    
    def clear_scan_history(self, listbox):
        """Clear scan history from database"""
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir effacer tout l'historique?"):
            if self.db.clear_history():
                listbox.delete(0, tk.END)
                messagebox.showinfo("Succès", "Historique effacé avec succès")
            else:
                messagebox.showerror("Erreur", "Impossible d'effacer l'historique")

if __name__ == "__main__":
    app = CyberScannerPRO()