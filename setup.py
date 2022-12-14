import os
import pwd

os.system("pip install python_crontab==2.6.0")
from crontab import CronTab

username = pwd.getpwuid(os.getuid())[0]
directory = os.getcwd()

def new_screen():
    os.system("clear")
    print("        __                _             __            ")
    print("   ____/ /___  ____ ___  (_)___  ____ _/ /_____  _____")
    print("  / __  / __ \/ __ `__ \/ / __ \/ __ `/ __/ __ \/ ___/")
    print(" / /_/ / /_/ / / / / / / / / / / /_/ / /_/ /_/ / /    ")
    print(" \__,_/\____/_/ /_/ /_/_/_/ /_/\__,_/\__/\____/_/     [dev]")
    print(" ──────────────────────────────────────────────────────────")
    print("")


def install_dependencies():
    print(" [i] Installing dependencies...")
    try:
        os.system("pip install -r requirements.txt")
    except:
        print(" [!] Could not install dependencies. Dominator might not work as expected.")

def set_cron():
    try:
        cron = CronTab(user=username)
        job = cron.new(command='python3 {}/exec.py'.format(directory))
        
        interval = input(" [i] Do you want this script to run every x hours or minutes? (h/m):")
        if interval == "h":
            amt = input(" [i] Run dominator every x hours: ")
            job.hour.every(int(amt))
        elif interval == "m":
            amt = input(" [i] Run dominator every x minutes: ")
            job.hour.every(int(amt))
        cron.write()
    except:
        print(" [!] Cron could not be set up. Dominator won't be ran periodically.")

def main():
    new_screen()
    install_dependencies()
    set_cron()

if __name__ == "__main__":
    main()