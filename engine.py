import sqlite3
import dns
import dns.resolver
import sys
import datetime
import requests
import traceback

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


def check_for_redirects(hostname):
    try:
        r = requests.get("http://" + hostname, allow_redirects=False)
        if r.status_code == 200:
            return "no"
        else:
            # return the whole URL
            return r.headers["Location"]
    except:
        return "no"


def get_dns_records(hostname):
    scan_date = datetime.datetime.now().strftime("%Y-%m-%d")

    try:
        a_result = dns.resolver.resolve(hostname, 'A')
        a_records = []
        for rdata in a_result:
            a_records.append(rdata.address)
    except:
        a_records = ""
    
    try:
        aaaa_result= dns.resolver.resolve(hostname, 'AAAA')
        aaaa_records = []
        for rdata in aaaa_result:
            aaaa_records.append(rdata.address)
    except:
        aaaa_records = ""
    
    try:
        cname_result = dns.resolver.resolve(hostname, 'CNAME')
        cname_records = []
        for rdata in cname_result:
            cname_records.append(rdata.target.to_text())
    except:
        # print stack trace
        #traceback.print_exc()
        cname_records = ""
    
    try:
        mx_result = dns.resolver.resolve(hostname, 'MX')
        mx_records = []
        for rdata in mx_result:
            mx_records.append(rdata.exchange.to_text())
    except:
        mx_records = ""
    
    try:
        ns_result = dns.resolver.resolve(hostname, 'NS')
        ns_records = []
        for rdata in ns_result:
            ns_records.append(rdata.target.to_text())
    except:
        ns_records = ""
    
    try:
        txt_result = dns.resolver.resolve(hostname, 'TXT')
        txt_records_pre = []
        for rdata in txt_result:
            txt_records_pre.append(rdata.strings)
        txt_records = []
        # remove the b' from the strings in the tuple
        for x in txt_records_pre:
            for y in x:
                y = y.decode("utf-8")
                txt_records.append(y)

    except:
        txt_records = ""
    
    try:
        soa_result = dns.resolver.resolve(hostname, 'SOA')
        soa_records = []
        for x in soa_result:
            soa_records.append(x.to_text())
    except:
        # print stack trace
        traceback.print_exc()
        soa_records = ""
    
    try:
        ptr_result = dns.resolver.resolve(hostname, 'PTR')
        ptr_records = []
        for rdata in ptr_result:
            ptr_records.append(rdata.target.to_text())
    except:
        ptr_records = ""
    
    try:
        srv_result = dns.resolver.resolve(hostname, 'SRV')
        srv_records = []
        for rdata in srv_result:
            srv_records.append(rdata.target)
    except:
        srv_records = ""

    redirect = check_for_redirects(hostname)

    """conn = sqlite3.connect('./databases/intel.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO dns_records(scan_date, target, a, aaaa, cname, mx, ns, txt, soa, ptr, srv, redirect) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", 
        (scan_date, 
        hostname, 
        a_records, 
        aaaa_records, 
        cname_records, 
        mx_records, 
        ns_records, 
        txt_records, 
        soa_records, 
        ptr_records, 
        srv_records, 
        redirect)
    )
    
    conn.commit()
    conn.close()"""

    print(" [+] Scan date: " + scan_date)
    print(" [+] Target: " + hostname)
    print(" [+] A records: " + str(a_records))
    print(" [+] AAAA records: " + str(aaaa_records))
    print(" [+] CNAME records: " + str(cname_records))
    print(" [+] MX records: " + str(mx_records))
    print(" [+] NS records: " + str(ns_records))
    print(" [+] TXT records: " + str(txt_records))
    print(" [+] SOA records: " + str(soa_records))
    print(" [+] PTR records: " + str(ptr_records))
    print(" [+] SRV records: " + str(srv_records))
    print(" [+] Redirect: " + redirect)
    print(       )
    print(str(txt_records)) # a way to save this thing



def main():
    try:
        # set the hostname to the argument passed on the script call
        hostname = sys.argv[1]
        get_dns_records(hostname)
    except Exception as e:
        # print error traceback
        traceback.print_exc()
        print(" [!] Error: " + str(e))
        # print(" [!] No hostname specified, please call the script with a hostname as argument")
        exit()
    
if __name__ == "__main__":
    main()