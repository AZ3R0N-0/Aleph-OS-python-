try:
    import time
    import os
    from pathlib import Path
    import platform
    import sys
    import random
    import subprocess
    import shlex
    import requests #ATTENTION!!! you'll need to install this library manually
except ModuleNotFoundError as e:
    print(f'[FATAL]: {e}')

project_dir = Path(__file__).resolve().parent #main Aleph OS directory

version = '5.0.4' #OS version

def ping_host(host): #'ping' command (like in other systems)
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    subprocess.run(['ping', param, '4', host])

def progress(percent=0, width=30):
    left = width * percent // 100
    right = width - left
    tags = '>' * left
    spaces = '_' * right
    percents = f'{percent:.0f}%'
    print('\r[', tags, spaces, ']', percents, sep='', end='', flush=True)

def logo(): #logo
    print(r'    _    _            _        ___  ____  ')
    print(r'   / \  | | ___ _ __ | |__    / _ \/ ___| ')
    print(r"  / _ \ | |/ _ \ '_ \| '_ \  | | | \___ \ ")
    print(r' / ___ \| |  __/ |_) | | | | | |_| |___) |')
    print(r'/_/   \_\_|\___| .__/|_| |_|  \___/|____/ ')
    print(r'               |_|                        ')
    print()
    print(f'~ Welcome to Aleph OS {version}! ~')
    print("Type 'help' to view avaiable commands")
    print()

os.system('cls' if os.name == 'nt' else 'clear') #bugfix for windows (makes ANSI color codes work correctly)

REPO_NAME = 'Aleph-OS-spm-repository' #official repository

try: #gets your system username
    user = os.getlogin()
except OSError:
    print("[ERROR]: I can't find your name. I'll call you 'user'.")
    user = 'user'

logo()
while True:
    try:
        try:
            user_input = input(f'[\033[91m{user}\033[0m@alephos]% ').strip()
        except EOFError:
            print('\n[ERROR]: End-Of-File! Ending session.')
            break

        if not user_input:
            continue #skips the entire iteration to prevent error: '[ERROR]: no such command ""'

        parts = shlex.split(user_input)
        command = parts[0]
        args = parts[1:]
        #print(args)

        if user_input == 'exit': #exit Aleph OS #DON'T HAVE ARGUMENTS
            print('#~ Exiting...')
            break #can be changed to 'exit()'

        elif user_input == 'clear': #clear terminal #DON'T HAVE ARGUMENTS
            os.system('cls' if os.name == 'nt' else 'clear')

        elif command == 'list': #imitation of 'ls' or 'dir' command
            if args != []:
                if args[0] == '-f':
                    if len(args) >= 2:
                        for item in os.listdir(project_dir):
                            item_path = Path(item)
                            if item_path.suffix == args[1]:
                                print(f' |> {item}  ')
                    else:
                        raise SyntaxError('no file extension.')
            else:
                for item in os.listdir(project_dir):
                    print(f' |> {item}  ')

        elif command == 'ping': #'ping' command (like in other systems)
            while True:
                try:
                    ping_host(args[0])
                    time.sleep(0.2)
                except KeyboardInterrupt:
                    break

        elif user_input == 'help': #list of avaiable commands #DON'T HAVE ARGUMENTS
            print('Avaiable commands:')
            print('ping - checks your internet connection.')
            print('exit - exits Aleph OS.')
            print('list - shows all files and directories in main Aleph OS directory.')
            print('exec - executes a file.')
            print('clear - clears screen.')
            print('spm - downloads a file from GitHub repository.')
            print('chrep - changes current GitHub repository.')

        elif command == 'exec': #executes files (!!!ATTENTION: THIS COMMAND WON'T EXECUTE A FILE IF IT'S NOT IN A MAIN DIRECTORY)
            if args != []:
                path = project_dir / args[0]
                time.sleep(0.1)
                if not path.is_file(): #checks if it's a file or a directory (also checks existence of a file)
                    raise FileNotFoundError('so such file.')
                else:
                    try:
                        subprocess.run([sys.executable,'-u', path])
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print('[SUCCESS]: file was successfully terminated.')
                    except KeyboardInterrupt: #preventing system shutdown after 'Ctrl + C'
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f'[ERROR]: file was terminated with error: keyboard interruption.')
            else:
                raise SyntaxError('no arguments.')

        elif command == 'spm': #fetches file from GitHub repository
            if args != []:
                if len(args) >= 2:
                    REPO_NAME = args[1]
                try:
                    #This variables can be changed if you're going to use another repository
                    USERNAME = 'AZ3R0N-0'
                    BRANCH = 'main'
                    #
                    timestamp = int(time.time())
                    url = f'https://raw.githubusercontent.com/{USERNAME}/{REPO_NAME}/{BRANCH}/{args[0]}?t={timestamp}' #full link to a repository
                    args[0] = os.path.basename(args[0]) #leaves only a name with an extension
                    full_path = os.path.join(project_dir, args[0]) #fix for linux to prevent files to be installed in home directory
                    print(f'Fetching file from {REPO_NAME}...')
                    time.sleep(0.8)
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    total_bytes = response.headers.get('content-length')
                    if total_bytes is not None: #checks if 'Content-lenght' header is received
                        total_bytes = int(total_bytes)
                        if total_bytes >= 1024 ** 2:
                            size_formatted = f'{total_bytes / (1024 ** 2):.2f} Mb'
                        else:
                            size_formatted = f'{total_bytes / 1024:.2f} Kb'
                    else:
                        size_formatted = '??? b'
                    print('File to install:')
                    print(f'{REPO_NAME}/{BRANCH}/{args[0]}      File size: {size_formatted}')
                    print()
                    input("Press 'Enter' to continue installation or press '^C' to cancel installation: ")
                    print(f'Installing {args[0]}...')
                    for i in range(101): #progressbar
                        progress(i)
                        time.sleep(0.01)
                    print()
                    with open(full_path, 'wb') as f:
                        f.write(response.content)
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 404:
                        raise FileNotFoundError(f"Cannot find '{args[0]}' in {REPO_NAME}.")
                    else:
                        print(f'HTTP error: {e}')
            else:
                raise SyntaxError('no arguments.')

        elif command == 'chrep': #changes repository
            if args != []:
                if args[0] == '-show':
                    print(REPO_NAME)
                else:
                    REPO_NAME = args[0]
            else:
                raise SyntaxError('no arguments.')
        else:
            raise SyntaxError(f'no such command: {command}.')
        print('\033[2m~\033[0m')
    except KeyboardInterrupt:
        print('\n[ERROR]: Keyboard Interruption!')
        print('\033[2m~\033[0m')
    except Exception as e:
        print(f'[ERROR]: {e}')
        print('\033[2m~\033[0m')