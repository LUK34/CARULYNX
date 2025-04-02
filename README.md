# HACK-BASICS-PY

## 01_ErrorHandling.PY
- Teaches you how to handle error using try and except block

## 02_Threading.py
- This program demonstrates multithreading using Python's threading module.
- Two functions are executed concurrently using separate threads.
- 🔧 Function Definitions:
- print_number()
- Prints numbers from 1 to 5
- Waits 1 second between each print using time.sleep(1)
- print_letters()
- Prints letters from A to E
- Waits 1 second between each print using time.sleep(1)
- 🧵 Thread Creation:
- thread1 is created to run the print_number() function.
- thread2 is created to run the print_letters() function.
- ▶️ Thread Execution:
- Both threads are started using the .start() method.
- Since threads run simultaneously, the output is interleaved, showing both numbers and letters printed in a mixed order depending on the thread scheduler.

## 03_File_Write_Read.py
- This programme teaches you how to write the contexts to a file name `data.txt`.
- After writing the contents in that file, this programme will teach how to read the contents from that file.

## 04_ThreadExecutionPool.py
- concurrent.futures: Helps run tasks in parallel using threads or processes.
- time: Used to pause/sleep the program for a few seconds.
- random: Used to pick a random number (for sleep duration).
- threading: Lets you find the name of the current thread (worker).

- def task(name): The Task Function
- Defines a function called task that simulates some work.
- It gets the name of the current thread (worker) using threading.current_thread().name.
- It prints that the task has started and on which thread.
- Sleeps for 1 to 5 random seconds (to simulate work).
- Prints that the task is complete.
- Returns the number of seconds it slept.

- with concurrent.futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix="Soldier") as executor:
- This is a Thread Pool Executor block
- Creates a pool of 3 threads (workers) that can run tasks in parallel.
- Each thread will be named like "Soldier_0", "Soldier_1", etc.
- executor is used to assign tasks to those threads.
- The with block makes sure threads are cleaned up after use.

- future_to_task = {executor.submit(task, i): i for i in range(1, 5)}
- This is a Dictionary Comprehension for submitting tasks
- Submits tasks task(1) to task(4) to the executor.
- executor.submit(task, i) sends the task to a worker thread and returns a future.
- future_to_task is a dictionary mapping each future to its task number i.
- This helps keep track of which result belongs to which task.

- for future in concurrent.futures.as_completed(future_to_task):
- Handling Completed Tasks
- Waits for the tasks to finish one by one, in the order they complete, not start.
- future is like a box that will contain the result of a task once it finishes.

- Getting the Result or Handling Exceptions
- task_name = future_to_task[future]: Gets the task number for that future.
- future.result():
- Returns the result of the task (i.e., how many seconds it slept).
- If the task raised an error, this will raise an exception.
- The result is printed, or the error is shown if there was one.



## 05_ProgressBar.py
- This imports the tqdm library, which is used to display a progress bar in the console for loops.
- It's especially helpful when running tasks that take time, like processing files, downloads, etc.

## 06_DNS_Record_Enumeration.py
- Programme to help you identiy the different record types of DNS based on the given url.
### What is DNS??
- DNS (Domain Name System) is like the phonebook of the internet.
- It translates domain names (like google.com) into IP addresses (like 142.250.195.14) that computers use to identify each other on the network.
- **A (Address)**
- Maps a domain name to an IPv4 address
- Example: example.com → 93.184.216.34
- **AAAA (Quad-A)**
- Maps a domain name to an IPv6 address
- Example: example.com → 2606:2800:220:1:248:1893:25c8:1946
- **CNAME (Canonical Name)**
- Points one domain name to another domain name
- Example: www.example.com → example.com
- **MX (Mail Exchange)**
- Defines email servers for the domain
- Example: email for example.com goes to mail.example.com
- **TXT (Text)**
- Stores text data for the domain
- Often used for SPF records, domain verification, etc.
- **SOA (Start of Authority)**
- Contains administrative info about the domain
- Includes: primary name server, admin email, domain serial number, refresh/retry/expiry settings


## 07_SubDomain_Record_Enumeration.py
- Programme to help you identify the different sub domain associated with a given url.
### What is sub domain??
- A subdomain is a subdivision of a main domain.
- It is used to organize or separate content on a website.
- Format: subdomain.domain.com (e.g., blog.example.com).
- It is treated as a separate entity by search engines.
- Can point to a different IP address or server.
- Useful for hosting different web apps (e.g., support, store).
- Does not require purchasing a new domain.
- Commonly used for testing environments (dev.example.com).
- Configured via DNS settings.
- Helps improve site structure and user experience.


## 08_PDF_Protector.py
- Opens the input file in binary read mode ('rb').
- with ensures the file is properly closed afterward.
- Creates a PdfReader object to read the pages of the PDF.
- Creates a PdfWriter object to write new PDF content.
- Loops through all pages of the input PDF and adds them to the writer object one by one.
- Applies password protection using the given password.
- Opens the output file in binary write mode ('wb').
- Writes the encrypted PDF to disk.
- sys.exit(1) exits the program with a status code 1 (which typically indicates an error).

## 09_PDF_cracker.PY
### imports
- import itertools: Provides functions for creating iterators for efficient looping, used for password generation.
- import pikepdf: Library to handle PDF files, specifically used here to open password-protected PDFs.
- from tqdm import tqdm: Provides a progress bar while cracking the PDF.
- import string: Contains useful character sets like letters, digits, and punctuation.
- from concurrent.futures import ThreadPoolExecutor, as_completed: For running password trials concurrently (multi-threaded).
- import argparse: For parsing command-line arguments.
- from itertools import tee: Used to create multiple independent iterators from a single iterable (not used in the final code though).
### Password Generator
- Generates all combinations of passwords with lengths from min_length to max_length.
- Uses itertools.product(chars, repeat=length) to generate all permutations of given characters for each length.
- Yields passwords one by one using a generator (saves memory).
### Wordlist Loader -> def load_wordlist(wordlist_file):
- Opens a file containing passwords (wordlist).
- Yields each password after stripping whitespace/newlines.
### Try Opening PDF with Password -> def try_password(pdf_file, password):
- Tries to open the PDF using the current password.
- If correct, returns the password.
- If incorrect (i.e., raises PasswordError), returns None.
###  Main Decryption Logic
- Sets up a progress bar (tqdm) for visual tracking.
- Uses ThreadPoolExecutor to run password checks in parallel.
- Submits each password attempt to the thread pool.
- future_to_passwords: Dictionary mapping each future (task) to its password.
- As each future completes:
- If a password is correct → print and return it.
- Else → update the progress bar.
- If no password worked → prints failure message.
### Main Execution Block
- Sets up argparse to allow command-line execution with different modes:
- pdf_file: Required. Path to the password-protected PDF.
- -w/--wordlist: Optional. Use a wordlist file.
- -g/--generate: Optional. Enable brute-force password generation.
- --min_length & --max_length: Min and max length for generated passwords.
- --charset: Characters used for generation (default = letters + digits + punctuation).
- --max_workers: Number of parallel threads.

- python 09_PDF_cracker.py "Hello Worldv3.pdf" -g -min 1 -max 4 -c 1234567890
- python 09_PDF_cracker.py "Hello Worldv3.pdf" -w wordlist.txt





