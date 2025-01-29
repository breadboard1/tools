#!/usr/bin/ python

import scapy.all as scapy
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Give a target / IP range.")
    options, _ = parser.parse_args()
    return options
    
def scan(ip):
    # scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # print(answered.summary())[1]
    # arp_request_broadcast.show()
    # scapy.ls(scapy.Ether())
    clients_list = []
    for e in answered:
        client = {"ip" : e[1].psrc, "mac" : e[1].hwsrc}
        clients_list.append(client)
    return clients_list    

def print_result(result_list):
    print("IP\t\t\tMAC address\n-----------------------------------------")
    for client in result_list:
        print(f"{client["ip"]}\t\t{client["mac"]}")
    

if __name__ == "__main__":
    options =  get_arguments()  
    scan_result = scan(options.target)
    print_result(scan_result)
