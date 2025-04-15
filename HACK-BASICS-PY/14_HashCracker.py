import hashlib
import itertools
import string
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import argparse
# -------------------------------------------------------------------------------------------
# The below specifies the list of hashes the programme will use
# to crack the password
hash_name = [
    'md5',
    'sha1',
    'sha224',
    'sha256',
    'sha384',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'sha512'
]
# -------------------------------------------------------------------------------------------
# This will generate passwords on the fly.
def generate_passwords(min_length, max_length, charcaters):
    for length in range(min_length, max_length + 1):
        # It uses itertools.product to generate all possible combinations with repetition.
        for pwd in itertools.product(charcaters, repeat=length):
            # yield is used in generators.
            # A generator is a special type of function that returns values one at a time, pausing after each one until the next is requested.
            #  yield ''.join(pwd) is returning each possible password one by one instead of all at once
            yield ''.join(pwd)
# -------------------------------------------------------------------------------------------
def check_hash(hash_fn, password, target_hash):
    # Encode the password in Hexadecimal. And the encoded password should be verified with target_hash
    # So we take the password from either wordlist or generate_password
    # We encode the password into hexi digit and refine this hexidigit password with target_hash
    return hash_fn(password.encode()).hexdigest() == target_hash

# -------------------------------------------------------------------------------------------
def crack_hash(hash, wordlist=None,
               hash_type='md5',
               min_length=0,
               max_length=0,
               characters=string.ascii_letters + string.digits,
               max_workers=4):

    # getattr() is a Python function used to dynamically get an attribute (like a function or variable) from a module or class.
    # hashlib is a module that contains hashing functions like md5, sha1, sha256, etc.
    # hash_type is a string like 'md5' or 'sha256'.
    # Line: “Give me the hash function from hashlib that matches the name hash_type, or None if it doesn’t exist.”
    hash_fn = getattr(hashlib, hash_type, None)
    if hash_fn is None or hash_type not in hash_name:
        raise ValueError(f'[!] Invalid hash type: {hash_type} supported are {hash_name}')

    # If the password is from the `wordlist`
    if wordlist:
        # Read the `wordlist` file in read mode
        with open(wordlist, 'r') as f:
            lines = f.readlines()
            total_lines = len(lines)
            print(f"[*] Cracking hash {hash} using {hash_type} with a list of {total_lines} passwords.")

            # Multi threading -> Execute 4 threads at a time to speed up execution
            # ThreadPoolExecutor allows you to run functions in parallel threads.
            # The with block ensures resources are cleaned up when done (no need to manually shutdown the pool).
            # Creates a dictionary called futures.
            # Each key is a Future object, which represents a thread executing check_hash().
            # executor.submit(...) starts the function check_hash() in a separate thread for each line in lines.
            # check_hash(hash_fn, line.strip(), hash) — you're calling a function that checks if line.strip() hashes to the given target hash.
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(check_hash, hash_fn, line.strip(), hash): line for line in lines} #dictionary comprehension
                # Iterates over all the futures.
                # tqdm() adds a progress bar for visual feedback.
                for future in tqdm(futures, total=total_lines, desc="Cracking hash"):
                    # Returns the original line (word) associated with the Future that returned True.
                    # .strip() removes any leading/trailing whitespaces.
                    if future.result():
                        return futures[future].strip()

    # If the password is generated.
    elif min_length > 0 and max_length > 0:
        total_combinations = sum(len(characters) ** length for length in range(min_length, max_length + 1))
        print(f'[*] Cracking hash {hash} using {hash_type} with generated passwords of lengths from {min_length} to {max_length}. Total combinations: {total_combinations}.')

        # Multi threading -> Execute 4 threads at a time to speed up execution
        # ThreadPoolExecutor allows you to run functions in parallel threads.
        # The with block ensures resources are cleaned up when done (no need to manually shutdown the pool).
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            with tqdm(total=total_combinations, desc='Generating and cracking hash') as pbar:
                for pwd in generate_passwords(min_length, max_length, characters):
                    future = executor.submit(check_hash, hash_fn, pwd, hash) # No dictionary comprehension used here
                    futures.append(future)
                    pbar.update(1) #Progress bar will be updated by 1 password
                    if future.result():
                        # If we got the result we will return the password
                        return pwd
    # If we did not get the password it will return none
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hash cracker')
    parser.add_argument('hash', help='The hash to crack.')
    parser.add_argument('-w','--wordlist', help='The path to the wordlist.')
    parser.add_argument('--hash_type', help='The hash to use', default='md5')
    parser.add_argument('--min_length', type=int, help='The minimum length of password to generate.')
    parser.add_argument('--max_length', type=int, help='The maximum length of password to generate.')
    parser.add_argument('-c', '--characters', help='The characters to use for password generation.')
    parser.add_argument('--max_workers', type=int, help='The maximum number of threads.')

    args = parser.parse_args()

    cracked_password = crack_hash(args.hash, args.wordlist, args.hash_type, args.min_length, args.max_length, args.characters, args.max_workers)

    if cracked_password:
         print(f"[+] Found password: {cracked_password}")
    else:
        print("[!] Password not found.")


# ------------------------------------------------------------------------------
# Why use yield here?
# If the character set is large and the password length is high, the number of combinations becomes massive.
# Instead of storing all passwords in memory, yield allows generating them on-the-fly, one at a time.

# Plain Text: 24339
# SHA512: f3b01e6a20694556304f9057582e33356b44244eab302ae5352217d231f4cbd5720a21bab894c903e01a48d0c43509cd9e2d3dce9b91a2e3eb6c9eca07ef978c

# CMDS to execute in terminal
# python .\14_HashCracker.py f3b01e6a20694556304f9057582e33356b44244eab302ae5352217d231f4cbd5720a21bab894c903e01a48d0c43509cd9e2d3dce9b91a2e3eb6c9eca07ef978c --min_length 4 --max_length 7 -c 1234567890 --hash_type sha512



