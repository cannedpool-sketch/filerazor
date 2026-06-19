import glob
import os
import readline
import readchar
import sys
import time
from colorama import init, Fore, Back, Style
init()

deletefolders = False

def print_top_right(text):
    cols = os.get_terminal_size().columns
    padded = text[:cols]
    sys.stdout.write(f"\033[s\033[1;{cols - len(padded)}H{Fore.MAGENTA}{padded}\033[u")
    sys.stdout.flush()

def print_top_right_sub(text):
    if not text:
        return
    cols = os.get_terminal_size().columns
    lines = text.split('\n')
    col_start = cols - max(len(l) for l in lines if l)
    col_start = max(col_start, 0)
    row = 3
    for line in lines:
        chunks = [line[i:i + cols] for i in range(0, max(len(line), 1), cols)]
        for chunk in chunks:
            sys.stdout.write(f"\033[s\033[{row};{col_start}H{chunk}\033[u")
            sys.stdout.flush()
            row += 1

def clear_screen():
    os.system('clear')

def path_completer(text, state):
    expanded_text = os.path.expanduser(text)
    matches = glob.glob(expanded_text + '*')
    processed_matches = []
    for match in matches:
        if os.path.isdir(match):
            processed_matches.append(match + '/')
        else:
            processed_matches.append(match)
    return processed_matches[state]

def forced_prefix_input(prefix="/", prompt=""):
    readline.set_completer_delims(' \t\n=')
    readline.set_completer(path_completer)
    readline.parse_and_bind("tab: complete")
    sys.stdout.write(prompt + prefix)
    sys.stdout.flush()
    result = prefix
    while True:
        ch = readchar.readchar()
        if ch in (readchar.key.ENTER, '\r', '\n'):
            print()
            return result
        elif ch in (readchar.key.BACKSPACE, '\x7f'):
            if len(result) > len(prefix):
                result = result[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        elif ch == '\t':
            matches = glob.glob(os.path.expanduser(result) + '*')
            if len(matches) == 1:
                match = matches[0]
                if os.path.isdir(match):
                    match += '/'
                sys.stdout.write(match[len(result):])
                sys.stdout.flush()
                result = match
            elif len(matches) > 1:
                print()
                print('  '.join(matches))
                sys.stdout.write(prompt + result)
                sys.stdout.flush()
        else:
            result += ch
            sys.stdout.write(ch)
            sys.stdout.flush()

targetdir = forced_prefix_input("/", "Enter path: ")
while True:
    userinput = input("Would you like to delete folders? y/n: ").lower().strip()
    if userinput == 'y':
        deletefolders = True
        break
    elif userinput in 'n':
        deletefolders = False
        break
    print("Please choose y or n \n")

os.chdir(targetdir)
filecount = len(os.listdir(targetdir))

if filecount > 0:
    if deletefolders == True:
        file_iter = iter(sorted(os.listdir(targetdir)))
        filename = next(file_iter, None)
        last_output = ""
        while filename is not None:
            filepath = os.path.join(targetdir, filename)
            clear_screen()
            print_top_right(f"Current: {filename}")
            print_top_right_sub(last_output)
            print(f"{Fore.CYAN} Working Directory: {targetdir}")
            userinput = input(f"{Fore.YELLOW}Would you like to delete '{filepath}'? y/n/o : " + Fore.CYAN)
            if userinput.lower() == 'y':
                os.remove(filepath)
                last_output = Fore.RED + f"[-] DELETED {filename}"
            if userinput.lower() == 'n':
                last_output = Fore.GREEN + f"Skipping {filename}"
            elif userinput.lower() == 'o':
                with open(filepath, 'r', errors='replace') as file:
                    content = file.read()
                last_output = Fore.WHITE + content.strip()
                continue
            elif userinput.lower() not in ('y', 'n', 'o'):
                print_top_right_sub(Fore.RED + "Invalid input! Please enter y/n/o")
                continue
            filename = next(file_iter, None)
    elif deletefolders == False:
        file_iter = iter(sorted(os.listdir(targetdir)))
        filename = next(file_iter, None)
        last_output = ""
        while filename is not None:
            filepath = os.path.join(targetdir, filename)
            if os.path.isdir(filepath):
                filename = next(file_iter, None)
                continue
            else:
                clear_screen()
                print_top_right(f"Current: {filename}")
                print_top_right_sub(last_output)
                print(f"{Fore.CYAN} Working Directory: {targetdir}")
                userinput = input(f"{Fore.YELLOW}Would you like to delete '{filepath}'? y/n/o : " + Fore.CYAN)
                if userinput.lower() == 'y':
                    os.remove(filepath)
                    last_output = Fore.RED + f"[-] DELETED {filename}"
                if userinput.lower() == 'n':
                    last_output = Fore.GREEN + f"Skipping {filename}"
                elif userinput.lower() == 'o':
                    with open(filepath, 'r', errors='replace') as file:
                        content = file.read()
                    last_output = Fore.WHITE + content.strip()
                    continue
                elif userinput.lower() not in ('y', 'n', 'o'):
                    print_top_right_sub(Fore.RED + "Invalid input! Please enter y/n/o")
                    continue
                filename = next(file_iter, None)

print(f"{Fore.CYAN}No files to delete!")