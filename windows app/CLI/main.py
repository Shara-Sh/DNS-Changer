import os, sys
import re
import json
import ctypes
import requests
import pyfiglet
import subprocess
import pyfiglet.fonts
from colorama import Fore, Style

def set_console_title(cli_title):
    ctypes.windll.kernel32.SetConsoleTitleW(cli_title)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# CLI Title
cli_title = "DNS Changer"
set_console_title(cli_title)

# Menu Title
menu_title = "DNS Changer"

clear()

dns_server_url = "https://shara-sh.github.io/DNS-Changer/DNS-Server.json"

def fetch_dns_servers():
    try:
        response = requests.get(dns_server_url)
        if response.status_code == 200:
            dns_servers = json.loads(response.text)
            return dns_servers
        else:
            print(f"Failed to fetch DNS server data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching DNS server data: {str(e)}")
    return None

def find_server_by_ip(ip_address, dns_servers):
    for server, server_data in dns_servers.items():
        if ip_address in [server_data['DNS']['Primary'], server_data['DNS']['Secondary']]:
            return server
    return "Custom"


def getdns():
    output_bytes = subprocess.check_output(['wmic', 'nicconfig', 'get', 'dnsserversearchorder'])
    
    # Convert the bytes to a string
    output_str = output_bytes.decode('utf-8')

    # Use regular expressions to extract IP addresses
    dns_addresses = re.findall(r'\d+\.\d+\.\d+\.\d+', output_str)
    return dns_addresses

def server_list_connect(choice, dns_servers):
    index = int(choice) - 1
    server_names = list(dns_servers.keys())
    
    if 0 <= index < len(server_names):
        selected_server = server_names[index]
        primary_dns = dns_servers[selected_server]['DNS']['Primary']
        secondary_dns = dns_servers[selected_server]['DNS']['Secondary']
        
        subprocess.call(['netsh', 'interface', 'ipv4', 'set', 'dns', '"Wi-Fi"', 'static', primary_dns])
        subprocess.call(['netsh', 'interface', 'ipv4', 'add', 'dns', '"Wi-Fi"', secondary_dns, 'index', '=', '2'])
        
        return selected_server
    else:
        print("Invalid choice. Please select a valid server.")
        return None

def connect(dns_servers):
        clear()
        print(pyfiglet.figlet_format(menu_title))
        print("\nChoose option : ")
        print("")
        
        for i, dns in enumerate(dns_servers, start=1):
            print(f"        {i} : {dns}")
        print(f"        C : Custom")
        print(f"        0 : Back")
            
        choice = input("\nEnter the selected number : ")
        if choice.isdigit() and int(choice) > 0:
            server_list_connect(choice, dns_servers)
        elif choice == 'C' or choice == "c" :
            custom()
        elif choice == '0':
            return
    
def disconnect():
    subprocess.call(['netsh', 'interface', 'ipv4', 'set', 'dns', '"Wi-Fi"', 'source', '=', 'dhcp'])

def custom():
    clear()
    print(pyfiglet.figlet_format(menu_title))
    
    primary = input("Set Primary DNS : ")
    secondary = input("Set Secondary DNS : ")
    subprocess.call(['netsh', 'interface', 'ipv4', 'set', 'dns', '"Wi-Fi"', 'static', f'{primary}'])
    subprocess.call(['netsh', 'interface', 'ipv4', 'add', 'dns', '"Wi-Fi"', f'{secondary}', 'index', '=', '2'])

dns_servers = fetch_dns_servers()

while True:
    clear()
    print(pyfiglet.figlet_format(menu_title))
    dns_addresses = getdns()
    if dns_addresses[0] == "192.168.1.1":
        primarydns = "None"
        secondarydns = "None"
        key = "No"
    elif len(dns_addresses) == 1:
        primarydns = dns_addresses[0]
        secondarydns = "None"
        ip_to_find = primarydns
        key = find_server_by_ip(ip_to_find, dns_servers)
    else:
        primarydns = dns_addresses[0]
        secondarydns = dns_addresses[1]
        ip_to_find = primarydns
        key = find_server_by_ip(ip_to_find, dns_servers)
        
    print("\nCurrent DNS Servers : ")
    print(f"""
        {key} DNS
        Primary DNS : {primarydns}
        Secondary DNS : {secondarydns}
        """
          )
    print("\nChoose option : ")
    print("""
        1 : Connect
        2 : Disconnect
        0 : Exit"""
          )
    choice = input("\nEnter the selected number : ")
    if choice == '1':
        connect(dns_servers)
    elif choice == '2' :
        disconnect()
    elif choice == '0':
        sys.exit()