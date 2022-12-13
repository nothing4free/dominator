import sqlite3
import dns
import dns.resolver
import sys

"""
    This script will resolve a hostname to an IP address and print it to the screen.
    If no hostname is specified, the script will uexit.

    This script saves the daily data on a sqlite3 database with the following structure:
    - DNS entry type (A, MX, CNAME, etc)
    - hostname
    - IP address
    - redirects (if any)
    - date

    Every day it will check if anything at all changes, and if so, it will save the new data and notify via email.
    Also it will send a daily report with the results.




    DATABASE STRUCTURE: 
    
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


try:
    # set the hostname to the argument passed on the script call
    hostname = sys.argv[1]
except:
    # if no argument is passed, set the hostname to the local hostname
    print(" [!] No hostname specified, please call the script with a hostname as argument")
    exit()


def get_dns_records(hostname):
    a_records = dns.resolver.query(hostname, 'A')
    aaaa_records = dns.resolver.query(hostname, 'AAAA')
    cname_records = dns.resolver.query(hostname, 'CNAME')
    mx_records = dns.resolver.query(hostname, 'MX')
    ns_records = dns.resolver.query(hostname, 'NS')
    txt_records = dns.resolver.query(hostname, 'TXT')
    soa_records = dns.resolver.query(hostname, 'SOA')
    ptr_records = dns.resolver.query(hostname, 'PTR')
    srv_records = dns.resolver.query(hostname, 'SRV')
    
