from stegano import lsb
import argparse
import sys
import random
import re
import os

# Argument parsing for embedding and extracting messages
parser = argparse.ArgumentParser(description="Image Steganography\n[+] Use .png files only")
parser.add_argument('-e', type=str, help="To embed a message in the image")
parser.add_argument('-f', help="To pass .png (Image) file")
parser.add_argument('-x', help="To extract the message from the image.", action="store_true")
parser.add_argument('-p', help="To put in a password.", nargs="?", const="no_password_given")
args = parser.parse_args()

# Embedding and extraction instructions
# ./stego -f <filename.png> -e "secret_message" -p <Password (Optional)>" -> To embed a secret message.
# ./stego -f <secretfile.png> -x -p <Password supplied> -> To extract the secret message.

try:
    if not args.f:
        print("Please enter a file name.")
        print("[*] Type -h for help.")
        sys.exit(1)

    # Ensure the image file is a .png
    elif not args.f.lower().endswith('.png'):
        print("[-] Enter a .png file")
        sys.exit(1)

    # Handling embedding the message
    if args.f and args.e:
        if args.p is None:
            args.p = "no_password_given"  # Default password if not provided

        # Combine the password (if any) and the secret message
        embed = args.p + " " + args.e
        
        try:
            secret = lsb.hide(args.f, embed)
            random_number = random.randint(0, 100)
            filename = f"secret{random_number}.png"  # Save with random filename
            secret.save(filename)
            print(f"File Saved as {filename}")
        except FileNotFoundError:
            print(f"[-] The file '{args.f}' was not found.")
            sys.exit(1)

    # Handling message extraction
    elif args.f and args.x:
        if not args.p:
            print("[-] Enter a password.")
            print("[*] If you don't want to supply the password, just type -p at the end of the query.")
            sys.exit(1)
        
        try:
            message = lsb.reveal(args.f)
            if message:
                # Check if the password matches
                if args.p in message:
                    message = message.replace(args.p, "")  # Remove the password if it matches
                    print("The secret message is:", message)
                else:
                    print("[-] Couldn't reveal the message with the passcode.")
            else:
                print("[-] No hidden message found.")
        except FileNotFoundError:
            print(f"[-] The file '{args.f}' was not found.")
            sys.exit(1)

    else:
        print("[-] Error occurred")
        print("[*] Try again with the correct syntax.")
        print("[*] If you are trying to embed a message, try -e flag.")
        print("[*] If you are trying to extract a message, try -x flag")
        sys.exit(1)

except KeyboardInterrupt:
    print("[-] Process interrupted by user.")
    sys.exit(1)
