# Standard Library Imports
import os, sys
import time
import requests
import subprocess

# Third-party Library Imports
import ctypes
from colorama import Fore, Style

def set_console_title(new_title):
    ctypes.windll.kernel32.SetConsoleTitleW(new_title)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

appName = "DNS Changer.exe"
updaterName = "Updater.exe"

def download_updater():
    updater_app = "https://shara-sh.github.io/DNS-Changer/windows%20app/Updater/CLI-Updater.exe"
    download_successful = False

    while not download_successful:
        try:
            response = requests.get(updater_app)

            if response.status_code == 200:
                with open(updaterName, "wb") as file:
                    file.write(response.content)
                print(f"{Fore.GREEN}Updater downloaded successfully.{Style.RESET_ALL}")
                time.sleep(2)
                download_successful = True
                subprocess.Popen([updaterName], shell=True)
                sys.exit()
            else:
                print(f"{Fore.RED}\nFailed to download updater file. Status code: {response.status_code}. Try again later.{Style.RESET_ALL}")
                time.sleep(2)
                subprocess.Popen([appName], shell=True)
                sys.exit()
        except requests.RequestException:
            print(f"{Fore.RED}\nAn error occurred while downloading the updater file. Try again later.{Style.RESET_ALL}")
            time.sleep(2)
            subprocess.Popen([appName], shell=True)
            sys.exit()

def check_for_updates(current_version):
    # Replace 'update_server_url' with the URL where you store the latest version information.
    update_server_url = "https://shara-sh.github.io/DNS-Changer/version.txt"
    
    response = requests.get(update_server_url)
    latest_version = response.text.strip()
    if latest_version > current_version:
        print(f"A new update {Fore.GREEN}(version {latest_version}){Style.RESET_ALL} is available. Please update your app.")
        user = input("Do you want to update now? (Y/N) ")
        if user == "y" or user =="Y":
            download_updater()
            sys.exit()
        else:
            clear()
    else:
        print(f"{Fore.GREEN}You have the latest version of the app.{Style.RESET_ALL}")
        if os.path.isfile(updaterName):
            os.remove(updaterName)
            time.sleep(2)
            clear()
        else:
            time.sleep(2)
            clear()