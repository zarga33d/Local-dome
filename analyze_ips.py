#!/usr/bin/env python3
import os
import subprocess
import time

REPORTS_DIR = "/root/intel-reports/"
JS_DIR = os.path.expanduser("~/.honeypot.js/")
TOOLS = [
    ("traceroute", "traceroute.txt", lambda ip: ["traceroute", ip]),
    ("whois", "whois.txt", lambda ip: ["whois", ip]),
    ("nmap", "nmap.txt", lambda ip: ["nmap", "-Pn", "-sV", ip]),
    ("dig", "dig.txt", lambda ip: ["dig", "-x", ip]),
    ("zinfo", "zinfo.txt", lambda ip: ["zsh", "-i", "-c", f"zinfo {ip}"]),
]
DEBUG_LOG = os.path.join(REPORTS_DIR, "debug.log")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def log_debug(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(DEBUG_LOG, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def remove_ban(ip):
    for chain, flag, direction in [("INPUT", "-s", ip), ("OUTPUT", "-d", ip), ("FORWARD", "-s", ip)]:
        cmd = ["sudo", "iptables", "-D", chain, flag, direction, "-j", "DROP"]
        # Remove all matching rules (loop until not found)
        while True:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                break
    log_debug(f"[UNBAN] IP {ip}: Ban temporarily removed for analysis.")

def restore_ban(ip):
    for chain, flag, direction in [("INPUT", "-s", ip), ("OUTPUT", "-d", ip), ("FORWARD", "-s", ip)]:
        # Check if already banned
        check_cmd = ["sudo", "iptables", "-C", chain, flag, direction, "-j", "DROP"]
        add_cmd = ["sudo", "iptables", "-A", chain, flag, direction, "-j", "DROP"]
        result = subprocess.run(check_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            subprocess.run(add_cmd)
    log_debug(f"[REBANNED] IP {ip}: Ban restored after analysis.")

def ping_check(ip, duration=5):
    end = time.time() + duration
    while time.time() < end:
        try:
            result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False

def analyze_ip(ip):
    ip_dir = os.path.join(REPORTS_DIR, ip)
    analyzed_flag = os.path.join(ip_dir, "analyzed.flag")
    if os.path.exists(analyzed_flag):
        log_debug(f"[SKIP] IP {ip}: Already analyzed.")
        return
    ensure_dir(ip_dir)
    # إزالة الحظر مؤقتاً
    remove_ban(ip)
    # اختبار ping
    log_debug(f"[PING] IP {ip}: Testing reachability for 5 seconds...")
    if not ping_check(ip, duration=5):
        log_debug(f"[PING-FAIL] IP {ip}: No response. Analysis aborted. Ban restored.")
        restore_ban(ip)
        return
    log_debug(f"[PING-OK] IP {ip}: Host is reachable. Starting full analysis.")
    for tool, out_file, cmd_func in TOOLS:
        out_path = os.path.join(ip_dir, out_file)
        start_time = time.strftime("%Y-%m-%d %H:%M:%S")
        log_debug(f"START: {tool} on {ip} at {start_time}")
        try:
            with open(out_path, "w") as f:
                subprocess.run(cmd_func(ip), stdout=f, stderr=subprocess.STDOUT, timeout=180)
            log_debug(f"SUCCESS: {tool} on {ip}")
        except Exception as e:
            with open(out_path, "a") as f:
                f.write(f"\n[ERROR] {tool} failed: {e}\n")
            log_debug(f"ERROR: {tool} on {ip} - {e}")
        time.sleep(2)
    open(analyzed_flag, "w").close()
    log_debug(f"DONE: {ip} analysis complete.")
    # إعادة الحظر بعد التحليل
    restore_ban(ip)

def main():
    # Restart network directly before analysis
    try:
        subprocess.run(["service", "NetworkManager", "restart"], check=True)
        log_debug("[NETWORK] NetworkManager restarted before analysis.")
        time.sleep(5)  # Give network time to restart
    except Exception as e:
        log_debug(f"[NETWORK-FAIL] Could not restart NetworkManager: {e}")
    ensure_dir(REPORTS_DIR)
    if not os.path.exists(JS_DIR):
        ensure_dir(JS_DIR)  # أنشئ المجلد إذا لم يكن موجوداً
    ips = []
    for fname in os.listdir(JS_DIR):
        if fname.endswith(".js"):
            ip = fname[:-3]  # يحذف فقط .js من النهاية
            ips.append(ip)
    if not ips:
        # لا تطبع أي شيء عند التشغيل في الخلفية
        return
    for ip in ips:
        analyze_ip(ip)

if __name__ == "__main__":
    main() 