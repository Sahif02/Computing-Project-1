# Computing-Project-1
# YoInspector 🔍
**A Command-Line Penetration Testing Automation Tool**  
*Automate Android Reverse_TCP and Windows EternalBlue Exploits with Metasploit Integration*

---

## 📖 Overview
YoInspector is a lightweight, command-line tool designed to simplify penetration testing for two critical vulnerabilities:  
- **Android Meterpreter Reverse_TCP** (APK payload generation)  
- **Windows SMB MS17-010 (EternalBlue)**  

Built for cybersecurity students, professionals, and small businesses, YoInspector automates Metasploit workflows, reducing manual configuration and technical barriers.

---

## ✨ Features
- **Automated Payload Generation**: Create Android APK and EternalBlue payloads in seconds.
- **LHOST Auto-Detection**: Automatically detects your IP address for listener setup.
- **Ethical Safeguards**: Legal disclaimer and usage restrictions to enforce responsible testing.
- **Input Validation**: Ensures valid IPs, ports, and filenames.
- **Logging**: Tracks all actions in `yoinspector.log`.
- **Kali Linux Compatibility**: Optimized for penetration testing environments.

---

## ⚙️ Installation

### Prerequisites
- **Kali Linux** (recommended) or Debian-based OS
- **Python 3.7+**
- **Metasploit Framework**
- **Run as Root** (recommended)

### Steps
1. Clone the repository:
   - git clone https://github.com/Sahif02/Computing-Project-1.git
   - cd Computing-Project-1

2. Install dependencies:
   sudo apt update && sudo apt install metasploit-framework python3-pip

3. Run the tool:
   python3 yoinspector.py

## 🚀 Usage
### Android Exploitation (Reverse_TCP)
1. Generate a malicious APK and start a listener:
   - Choose option 1
   - Enter APK filename (e.g., evil.apk)
   - Enter LPORT (e.g., 4444)
   YoInspector will auto-detect your IP and generate the payload.

### Windows Exploitation (EternalBlue)
1. Exploit a vulnerable Windows machine:
   - Choose option 2
   - Enter target IP (RHOST)
   - Enter LPORT (e.g., 5555)
   The tool auto-configures Metasploit for EternalBlue.

## ⚠️ Ethical Guidelines
- Legal Disclaimer: YoInspector displays a mandatory ethical agreement before execution.
- Authorized Use Only: Test only systems you own or have explicit permission to assess.
- Isolated Labs: Use virtual machines (e.g., VirtualBox) in isolated networks.
