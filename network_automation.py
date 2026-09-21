from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException

# 1. Define the network device parameters (Matches CCNA topologies)
cisco_switch = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.5',        # The IP address of the switch/router
    'username': 'admin',          # SSH Username
    'password': 'SuperSecurePassword123',  # SSH Password
    'secret': 'EnablePassword123',        # Cisco Enable Password
    'port': 22,                   # Standard SSH Port
}

# 2. Define the configuration changes to apply (Creating a VLAN)
vlan_commands = [
    'vlan 10',
    'name Sales_Network',
    'exit'
]

def deploy_network_changes():
    print(f"🔄 Connecting to network device at {cisco_switch['host']} via SSH...")
    
    try:
        # Establish SSH connection using Netmiko
        connection = ConnectHandler(**cisco_switch)
        connection.enable()  # Enter Cisco privileged EXEC mode
        
        print("⚙️ Connection successful. Deploying VLAN configuration...")
        output = connection.send_config_set(vlan_commands)
        
        print("\n--- Execution Output ---")
        print(output)
        print("------------------------")
        
        # Save configuration to NVRAM (copy running-config startup-config)
        connection.send_command("write memory")
        print("💾 Configuration saved successfully.")
        
        # Close the SSH session safely
        connection.disconnect()
        print("🔌 Disconnected cleanly from device.")

    except NetMikoTimeoutException:
        print("❌ Error: Connection timed out. Check network routing and reachability.")
    except NetMikoAuthenticationException:
        print("❌ Error: Authentication failed. Please check your SSH credentials.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    deploy_network_changes()
