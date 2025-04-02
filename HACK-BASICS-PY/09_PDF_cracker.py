import itertools
import pikepdf
from tqdm import tqdm
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from itertools import tee


# -------------------------------------------------------------------------------------------------------------------
def generate_password(chars, min_length, max_length):
    for length in range(min_length,max_length+1):
        # Iterates over each of those combinations, where each password is a tuple of characters like ('a', 'b').
        # This returns a Cartesian product — all possible combinations of the characters in chars, repeated length times.
        # For example:
        # If chars = 'ab' and length = 2, the result would be:
        for password in itertools.product(chars,repeat=length):
            # Instead of returning the value and exiting the function, yield produces a value and pauses the function,
            # allowing it to resume later — this is what makes it a generator.
            # It lets you generate large sequences lazily, one at a time, without consuming lots of memory.
            yield ''.join(password) # Results in 'ab'
# -------------------------------------------------------------------------------------------------------------------
def load_wordlist(wordlist_file):
    with open(wordlist_file,'r') as file:
        for line in file:
            # Removes space in between
            # Hello World -> HelloWorld
            yield line.strip()
# -------------------------------------------------------------------------------------------------------------------
def try_password(pdf_file, password):
    try:
        with pikepdf.open(pdf_file,password=password) as pdf:
            return password
    except pikepdf._core.PasswordError:
        return None
# -------------------------------------------------------------------------------------------------------------------
def decrypt_pdf(pdf_file, passwords, total_passwords, max_workers=4):
    # Creates a progress bar using the tqdm library to visually show how many passwords have been attempted.
    with tqdm(total=total_passwords, desc='Decrypting PDF', unit='password') as progressBar:
        # Starts a thread pool to try multiple passwords at the same time. The number of threads is controlled by max_workers.
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # For each password, a task is submitted to the thread pool using executor.submit(...).
            # This runs the try_password(pdf_file, pwd) function in parallel.
            # A dictionary future_to_passwords is created to map each Future object (asynchronous task) to its corresponding password.
            future_to_passwords = {executor.submit(try_password, pdf_file, pwd): pwd for pwd in passwords}

            # as_completed(...) gives you the results in the order they finish, not the order they were submitted.
            for future in as_completed(future_to_passwords):
                #Get the password corresponding to this future.
                password = future_to_passwords[future]
                try:
                    # Call future.result() to get the result of try_password(...).
                    result = future.result()
                    if result:
                        print(f" Password found: {password}")
                        return result
                except Exception as e:
                    print(f"Decryption Error. Trying with password -> '{password}' .\nBut the error is as follows :\n{e}\n")
                finally:
                    # Whether successful or not, make sure the progress bar updates for each attempted password.
                    progressBar.update(1)

    print("Unable to decrypt PDF. Password not found.")
    return None
# -------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Decrypt a password=protected PDF file.")
    parser.add_argument('pdf_file',help='Path to the password-protected PDF file.')
    parser.add_argument('-w','--wordlist',help='Path to the passwords list file.', default=None)
    parser.add_argument('-g','--generate',action='store_true',help='Generate password on the fly.')
    parser.add_argument('-min','--min_length',type=int, help='Minimum length of the password to generate', default=1)
    parser.add_argument('-max', '--max_length', type=int, help='Maximum length of the password to generate', default=3)
    parser.add_argument('-c', '--charset', type=str, help='Characters to use for password generation', default=string.ascii_letters + string.digits + string.punctuation)
    parser.add_argument('--max_workers',type=int, help='Maximum workers of parallel threads',default=4)

    args=parser.parse_args()

    if args.generate:
        passwords = generate_password(args.charset, args.min_length, args.max_length)
        # for _ in ... — this is a loop that goes through each password in the list,
        # but ignores the actual password by using _ (underscore is a common convention for "I don't care about this value").
        # sum(1 for ...) — this creates a generator expression that yields the number 1 for each password,
        # and then sum() adds all those 1s up.
        total_passwords=sum(1 for _ in generate_password(args.charset, args.min_length, args.max_length))
        # for _ in iterable: Just means: "loop through each item, but I don’t need to use the item itself."
    elif args.wordlist:
        passwords = load_wordlist(args.wordlist)
        # for _ in iterable: Just means: "loop through each item, but I don’t need to use the item itself."
        total_passwords = sum(1 for _ in load_wordlist(args.wordlist))
    else:
        print("Either --wordlist must be provided or --generate must be specified.")

    decrypted_password = decrypt_pdf(args.pdf_file, passwords, total_passwords, args.max_workers)

    if decrypted_password:
        print(f"PDF decrypted successfully with password: {decrypted_password}")
    else:
        print("Unable to decrypt PDF. Password not found.")

# -------------------------------------------------------------------------------------------------------------------
# python 09_PDF_cracker.py -h
# python 09_PDF_cracker.py "Hello Worldv2.pdf" -g -min 1 -max 4 -c 1234567890

# python 09_PDF_cracker.py "Hello Worldv3.pdf" -g -min 1 -max 4 -c 1234567890



































































