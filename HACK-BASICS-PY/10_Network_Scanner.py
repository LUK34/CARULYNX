import scapy.all as scapy
import socket
import threading
from queue import Queue
import ipaddress

# scapy: Used for low-level packet crafting, sending, and receiving (e.g., ARP packets).
# socket: Used to resolve IP addresses to hostnames.
# threading: Enables concurrent scanning of multiple IPs.
# Queue: Thread-safe queue to store results.
# ipaddress: Helps in parsing and handling IP networks.

# This function sends an ARP request to a given IP address and captures the response.
def scan(ip, result_queue):
    # Creates an ARP request packet where pdst is the target IP or IP range (e.g., "192.168.1.1/24").
    arp_request=scapy.ARP(pdst=ip)

    # Creates a broadcast Ethernet frame.
    # It’s like yelling in the network: "Hey everyone, who owns this IP?"
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # Combines the Ethernet and ARP request into a single packet.
    packet=broadcast/arp_request

    # srp() sends the packet and receives replies at Layer 2 (Ethernet).
    # timeout=1 waits for 1 second.
    # verbose=False disables output.
    # The result is a list of answered packets.
    # If one machine does'nt have what we are searching for, we jump to the next machine. That is why we have 1 second delay.
    answer=scapy.srp(packet,timeout=1,verbose=False)[0] #Takes only the first line

    clients=[]
    for client in answer:
        client_info={'IP':client[1].psrc,'MAC': client[1].hwsrc}
        try: # If client Hostname exists then execute this
            hostname = socket.gethostbyaddr(client_info['IP'])[0]
            client_info['Hostname']=hostname
        except socket.herror: # If client hostname does not exist then execute.
            client_info['Hostname'] = 'Unknown'
        clients.append(client_info)
    result_queue.put(clients)


def print_result(result):
    print('IP' + " "*20 +'MAC'+ " "*20 + 'Hostname')
    print('-'*80)
    for client in result:
        print(client['IP']+'\t\t'+client['MAC']+'\t\t'+client['Hostname'])

# Main driver function for the script. It takes a CIDR range (like 192.168.1.0/24) and performs the following
def main(cidr):
    results_queue=Queue()
    threads=[]
    network=ipaddress.ip_network(cidr, strict=False)

    # Start Threads for Each Host IP
    for ip in network.hosts():
        # Creates and starts a thread per IP to scan them in parallel.
        # Each thread runs the scan() function.
        thread=threading.Thread(target=scan, args=(str(ip), results_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    all_clients=[]
    while not results_queue.empty():
        all_clients.extend(results_queue.get())

    print_result(all_clients)

if __name__ == '__main__':
    cidr=input("Enter network IP Address:")
    main(cidr)


# python .\10_Network_Scanner.py
#192.168.1.0/24