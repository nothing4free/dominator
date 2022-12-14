"""    
    dns_records (main table, scan results go here)
    +---------+-----------+--------+---+------+-------+-----+----+----+----+------+-----+----------+
    | scan_id | scan_date | target | a | aaaa | cname | mx | ns | txt | soa | ptr | srv | redirect |
    +---------+-----------+--------+---+------+-------+-----+----+----+----+------+-----+----------+
    |   1     | YYYY-MM-DD| domain | a | aaaa | cname | mx | ns | txt | soa | ptr | srv | url / no |
    +---------+-----------+--------+---+------+-------+-----+----+----+----+------+-----+----------+

    targets (scan sources go here)
    +---------+
    | target  |
    +---------+
    | domain  |
    +---------+
"""

from simple_term_menu import TerminalMenu
import sqlite3
import os
import time

def new_screen():
    os.system("clear")
    print("        __                _             __            ")
    print("   ____/ /___  ____ ___  (_)___  ____ _/ /_____  _____")
    print("  / __  / __ \/ __ `__ \/ / __ \/ __ `/ __/ __ \/ ___/")
    print(" / /_/ / /_/ / / / / / / / / / / /_/ / /_/ /_/ / /    ")
    print(" \__,_/\____/_/ /_/ /_/_/_/ /_/\__,_/\__/\____/_/     [dev]")
    print(" ──────────────────────────────────────────────────────────")
    print("")


def add_target():

    new_screen()
    try:
        conn = sqlite3.connect('./databases/intel.db')
        c = conn.cursor()
        target = input(" [i] Enter the target domain: ")
        c.execute("INSERT INTO targets VALUES (?)", (target,))
        conn.commit()
        conn.close()
        print(" [i] Target added successfully")
    except:
        print(" [!] Error adding target")

def remove_target():
    new_screen()
    try:
        conn = sqlite3.connect('./databases/intel.db')
        c = conn.cursor()
        c.execute("SELECT * FROM targets")
        targets = c.fetchall()

        target_list = []
        for target in targets:
            target_list.append(target[0])
        menu = TerminalMenu(target_list, title=" [i] Select a target to remove")
        menu_entry_index = menu.show()

        c.execute("DELETE FROM targets WHERE target = ?", (target_list[menu_entry_index],))
        conn.commit()

        options = ["Yes", "No"]
        menu = TerminalMenu(options, title=" [i] Remove all records on history for this target?")
        menu_entry_index = menu.show()

        if menu_entry_index == 0:
            c.execute("DELETE FROM dns_records WHERE target = ?", (target_list[menu_entry_index],))
            conn.commit()
            print(" [i] All records removed successfully")
        else:
            print(" [i] Records not removed")

        conn.close()
    
    except:
        print(" [!] Error removing target")

def list_targets_and_records():
    new_screen()
    try:
        conn = sqlite3.connect('./databases/intel.db')
        c = conn.cursor()
        c.execute("SELECT * FROM targets")
        targets = c.fetchall()

        target_list = []
        for target in targets:
            target_list.append(target[0])
        menu = TerminalMenu(target_list, title=" [i] Select a target to view its historical records")
        menu_entry_index = menu.show()

        c.execute("SELECT * FROM dns_records WHERE target = ?", (target_list[menu_entry_index],))
        records = c.fetchall()

        print(" [i] Records for target: " + target_list[menu_entry_index])
        print("───────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        print("")

        for record in records:
            print(" [i] Scan ID: " + str(record[0]))
            print(" [i] Scan Date: " + str(record[1]))
            print(" [i] Target: " + str(record[2]))
            print(" [i] A: " + str(record[3]))
            print(" [i] AAAA: " + str(record[4]))
            print(" [i] CNAME: " + str(record[5]))
            print(" [i] MX: " + str(record[6]))
            print(" [i] NS: " + str(record[7]))
            print(" [i] TXT: " + str(record[8]))
            print(" [i] SOA: " + str(record[9]))
            print(" [i] PTR: " + str(record[10]))
            print(" [i] SRV: " + str(record[11]))
            print(" [i] Redirect: " + str(record[12]))
            print("───────────────────────────────────────────────────────────────────────────────────────────────────────────────")
            print("")
        
        time.sleep(10)

        conn.close()
    except:
        print(" [!] Error listing targets and records")

def main():
    new_screen()
    options = ["Add Target", "Remove Target", "List Targets and Records", "Exit"]
    menu = TerminalMenu(options, title=" [i] Select an option")
    menu_entry_index = menu.show()

    if menu_entry_index == 0:
        add_target()
    elif menu_entry_index == 1:
        remove_target()
    elif menu_entry_index == 2:
        list_targets_and_records()
    elif menu_entry_index == 3:
        exit()

if __name__ == "__main__":
    while True:
        main()