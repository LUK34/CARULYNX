import socket
import concurrent.futures
import sys

RED="\033[91m"
GREEN="\033[92m"
RESET="\033[0m"

def format_port_results(results):
    formatted_results = "Port Scan Results:\n"

    # Left-align the text in a field 8 characters wide ......
    formatted_results += "{:<8} {:<15} {:<10}\n".format("Port", "Service", "Status")

    # This just adds a line of dashes to separate the headers from the actual results — like a table border.
    formatted_results += '-' * 85 + "\n"
    for port, service, banner, status in results:
        if status:
            formatted_results += f"{RED}{port:<8} {service:<15} {'Open':<10}{RESET}\n"
            if banner:
                banner_lines = banner.split('\n')
                for line in banner_lines:
                    formatted_results += f"{GREEN}{'':<8}{line}{RESET}\n"
    return formatted_results

def get_banner(sock):
    try:
        # we need to give timeout of 1 second so that it will get the result from the port
        sock.settimeout(1)
        banner =sock.recv(1024).decode().strip()
        return banner
    except:
        return " "


def scan_port(target_ip, port):
    try:
        # This line creates a socket object:
        # AF_INET: Specifies IPv4 addressing.
        # SOCK_STREAM: Specifies TCP connection (as opposed to UDP).
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # we need to give timeout of 1 second so that it will get the result from the port
        sock.settimeout(1)

        # Attempts to connect to the target IP and port.
        # connect_ex() is similar to connect(), but instead of raising an exception on error, it returns an error code:
        # 0 means the connection was successful (i.e., the port is open).
        # Any other value means the connection failed (i.e., port is closed or filtered).
        result=sock.connect_ex((target_ip,port))
        if result ==0:
            try:
                # Tries to get the standard service name associated with the port (e.g., port 80 → http, port 443 → https).
                service=socket.getservbyport(port, 'tcp')
            except:
                service='Unknown'
            banner=get_banner(sock)
            #here True -> means that the port is open
            return port,service,banner,True
        else:
            return port,"","",False
    except:
        return port, "", "", False
    finally:
        sock.close()

def port_scan(target_host,start_port,end_port):
    target_ip = socket.gethostbyname(target_host)
    print(f"Starting scan on host: {target_ip}")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=400) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in range(start_port, end_port + 1)}
        total_ports = end_port - start_port + 1
        for i, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            port, service, banner, status = future.result()
            results.append((port, service, banner, status))
            sys.stdout.write(f"\rProgress: {i}/total_ports ports scanned")
            sys.stdout.flush()

    sys.stdout.write("\n")
    print(format_port_results(results))


if __name__ == '__main__':
    target_host = input("Enter your target ip: ") #192.168.150.11
    start_port = int(input("Enter the start port: ")) #1
    end_port = int(input("Enter end port: ")) #1000

    port_scan(target_host, start_port, end_port)

# -----------------------------------------------------------------------------
#A port scanner helps identify open ports and associated services, giving clues about what software is in use (e.g., SSH, FTP, HTTP).

# 🛠️ Vulnerability Assessment:
# Once open ports are known, you can match them against known vulnerabilities (e.g., port 21 for FTP might be vulnerable if misconfigured).
# Helps determine if there’s a weak point in the network to exploit.

# 🚀 Automation:
# With Python, you can automate scanning multiple IPs and ports quickly.

# Easily extend your scanner to do banner grabbing, service detection, or even custom exploits after scanning.
# -----------------------------------------------------------------------------

# Banner Grabbing is a technique used by hackers, penetration testers, and network administrators to collect information about a service running on an open port.
# When you connect to certain network services (like a web server, FTP, or SSH), they often respond with a "banner" – a text message that includes:
# Service name
# Version number
# Sometimes even the OS or server configuration

