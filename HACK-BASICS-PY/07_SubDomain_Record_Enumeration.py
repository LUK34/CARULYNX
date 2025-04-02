# Used to send http request
import requests
# Used to run multiple threads concurrently for faster scanning.
import threading

# -----------------------------------------------------------------------------------------
domain='youtube.com'
# -----------------------------------------------------------------------------------------
with open('subdomains_prime.txt') as file:
    subdomains= file.read().splitlines()

discovered_subdomains=[]
# Ensures thread-safe writing to the shared list (to prevent race conditions).
lock = threading.Lock()

# -----------------------------------------------------------------------------------------
def check_subdomain(subdomain):
    url= f'http://{subdomain}.{domain}'
    try:
        response = requests.get(url, timeout=3)
        if response.status_code < 400:  # Optional: only consider successful or redirected responses
            print("[+] Discovered subdomain:", url)
            with lock:
                discovered_subdomains.append(url)
    except requests.ConnectionError:
        pass
    except requests.Timeout:
        pass
# -----------------------------------------------------------------------------------------
threads=[]
# -----------------------------------------------------------------------------------------
# For every subdomains discovered append it to the list-> threads
# Creates a thread for each subdomain and starts it.
# Appends each thread to a list to keep track of them.
for subdomain in subdomains:
    thread=threading.Thread(target=check_subdomain,args=(subdomain,))
    thread.start()
    threads.append(thread)
# -----------------------------------------------------------------------------------------
# Below lines of code to make sure that the thread execution finish its processes.
# Wait for All Threads to Finish
# Ensures that the main thread waits until all subdomain-checking threads are done.
for thread in threads:
    thread.join()
# -----------------------------------------------------------------------------------------
# Save Discovered Subdomains to a File
# Writes all discovered (working) subdomains into discovered_subdomains.txt.
with open("discovered_subdomains.txt",'w') as f:
    for subdomain in discovered_subdomains:
        print(subdomain,file=f)
# -----------------------------------------------------------------------------------------




























