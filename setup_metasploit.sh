#!/bin/bash

echo "========================================="
echo "         Setting Up Metasploit          "
echo "========================================="

# Initialize Metasploit database
sudo msfdb init

# Check database status
sudo msfdb status

# Launch Metasploit console to verify
echo "Launching Metasploit to verify installation..."
msfconsole -q -x "version; exit"

