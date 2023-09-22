# Standard Library Imports
import os, sys
import time
import requests

# Third-party Library Imports
import ctypes
import subprocess
from colorama import Fore, Style

def set_console_title(cli_title):
    ctypes.windll.kernel32.SetConsoleTitleW(cli_title)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# CLI Title
cli_title = "Updater"
set_console_title(cli_title)

clear()

updated_app = "https://shara-sh.github.io/DNS-Changer/windows%20app/CLI/DNS%20Changer.exe"
appName = "DNS Changer.exe"
download_successful = False

while not download_successful:
    try:
        response = requests.get(updated_app)

        if response.status_code == 200:
            with open(appName, "wb") as file:
                file.write(response.content)
            print(f"{Fore.GREEN}Updater downloaded successfully.{Style.RESET_ALL}")
            time.sleep(2)
            download_successful = True
            subprocess.Popen([appName], shell=True)
            sys.exit()
        else:
            print(f"{Fore.RED}\nFailed to download file. Status code: {response.status_code}. Try again later.{Style.RESET_ALL}")
            time.sleep(2)
            subprocess.Popen([appName], shell=True)
            sys.exit()
    except requests.RequestException:
        print(f"{Fore.RED}\nAn error occurred while downloading the file. Try again later.{Style.RESET_ALL}")
        time.sleep(2)
        subprocess.Popen([appName], shell=True)
        sys.exit()