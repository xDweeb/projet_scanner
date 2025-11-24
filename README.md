# 🛡️ Cyber Scanner PRO

A modern, professional network security scanning tool with a sleek dark-themed GUI interface.

## ✨ Features

- **Modern GUI Interface** - Dark theme with professional styling
- **Port Scanner** - Fast TCP port scanning with progress tracking
- **IP Geolocation** - Detailed IP information and geographic location
- **Ping Tool** - Network connectivity testing
- **System Information** - Comprehensive system details
- **Age Verification** - Secure access control (18+ required)
- **Results Export** - Save scan results to text files
- **Multi-threading** - Non-blocking operations for better performance

## 🚀 Quick Start

### Method 1: Double-click launcher (Windows)
```
Double-click: start_scanner.bat
```

### Method 2: Python command
```bash
python scanner_gui_modern.py
```

### Method 3: Use the launcher script
```bash
python launcher.py
```

## 📋 Requirements

- Python 3.7+
- tkinter (usually included with Python)
- requests
- Pillow (for enhanced UI elements)

## 🔧 Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python scanner_gui_modern.py
   ```

## 🎯 Usage

1. **Age Verification**: Enter your name and age (must be 18+)
2. **Enter Target**: Input IP address or domain name
3. **Configure Ports**: Set port range (e.g., "1-1024") or specific ports (e.g., "22,80,443")
4. **Choose Action**:
   - 🔍 **Scan Ports**: Comprehensive port scanning
   - 📡 **Ping**: Test connectivity
   - 🌐 **IP Lookup**: Geographic and ISP information
   - 💻 **System Info**: Local system details
5. **View Results**: Real-time output in the console area
6. **Save Results**: Automatically saved to specified file path

## 🎨 Interface Features

- **Professional Dark Theme**: Easy on the eyes
- **Real-time Progress**: Visual progress bar during scans
- **Hover Effects**: Interactive button feedback
- **Emoji Icons**: Modern visual indicators
- **Responsive Layout**: Adapts to window resizing
- **Clean Typography**: Segoe UI font for better readability

## 🔒 Security Features

- Age verification system
- Input validation
- Error handling and timeout protection
- Safe file operations

## 📁 File Structure

```
projet_scanner/
├── scanner_gui_modern.py      # Main modern GUI application
├── scanner_functions.py       # Core scanning functions
├── scanner_terminal.py        # Terminal interface (legacy)
├── launcher.py               # Automatic launcher with dependency check
├── start_scanner.bat         # Windows batch launcher
├── requirements.txt          # Python dependencies
└── README.md                # This documentation
```

## 🛠️ Advanced Configuration

### Port Scanning Options
- **Range**: `1-1024` (scans ports 1 to 1024)
- **List**: `22,80,443,8080` (scans specific ports)
- **Single**: `80` (scans only port 80)

### Timeout Settings
The default timeout is 0.5 seconds per port. This can be adjusted in the `port_scan` function for faster or more thorough scanning.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License

This project is for educational purposes only. Use responsibly and only on networks you own or have permission to test.

## ⚠️ Disclaimer

This tool is intended for network administrators and security professionals. Always ensure you have proper authorization before scanning any network or system.

---

**Made with ❤️ for cybersecurity education and network administration**
