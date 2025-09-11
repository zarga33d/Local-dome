# Local-dome
Enhanced Honeypot is a security tool that simulates multiple services (SSH, FTP, HTTP, etc.) to detect and log cyber attacks. It collects threat intelligence, blocks malicious IPs automatically, and provides hidden logging with detailed statistics for research, monitoring, and training.


# 1️⃣ Update package lists
sudo apt update

# 2️⃣ Upgrade the system (optional but recommended)
sudo apt upgrade -y

# 3️⃣ Install iptables (required for some security features)
sudo apt install iptables -y

# 4️⃣ Clone the tool from GitHub
git clone https://github.com/zarga33d/Local-dome.git

# 5️⃣ Navigate into the tool's directory
cd Local-dome

# 6️⃣ Install required Python libraries
pip install -r requirements.txt
