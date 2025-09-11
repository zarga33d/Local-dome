# Local-dome
Zarga Honeypot

Enhanced Honeypot is a security tool that simulates multiple services (SSH, FTP, HTTP, etc.) to detect and log cyber attacks. It collects threat data, blocks malicious IPs automatically, and provides hidden logging with detailed statistics for research, monitoring, and training.

# ⚠️ Key Features:

- When a cyber attack is detected, the tool will trigger a pop-up alert.

- Automatically launches a counterattack using hping3 against the attacking IP.

- After the counterattack, it runs background reconnaissance scans (like nmap and other tools) on the target IP.

All collected data is saved to a root-accessible file named: intel-reports
This file contains detailed information extracted from the attack and subsequent scans.

# 1️⃣ Update package lists
```bash
sudo apt update
```
# 2️⃣ Upgrade the system (optional but recommended)
```bash
sudo apt upgrade -y
```
# 3️⃣ Install iptables (required for some security features)
```bash
sudo apt install iptables -y
```
# 4️⃣ Clone the tool from GitHub
```bash
git clone https://github.com/zarga33d/Local-dome.git
```
# 5️⃣ Navigate into the tool's directory
```bash
cd Local-dome
```
# 6️⃣ Install required Python libraries
```bash
pip install -r requirements.txt
```
# ⚡ Add an alias for easy access
# 7️⃣ Edit your zsh configuration file (if using zsh)
```bash
nano ~/.zshrc
```
Add the following line at the end (replace username with your actual user path):
```bash
alias zhz='python3 /home/username/Local-dome/zhoneypot_enhanced.py'
```
# 8️⃣ Reload zsh configuration
```bash
source ~/.zshrc
```
✅ You can now run the tool with a simple command:
```bash
zhz
```
# Windows Setup
 # 1️⃣ Clone the tool from GitHub
git clone https://github.com/zarga33d/Local-dome.git

# 2️⃣ Navigate into the tool's directory
cd Local-dome

# 3️⃣ Install required Python libraries
pip install -r requirements.txt

⚠️ Note: iptables is not supported on Windows. Its functionality is simulated within the tool.
