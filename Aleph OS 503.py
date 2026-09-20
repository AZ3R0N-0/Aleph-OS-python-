import time
import os
from pathlib import Path
import platform
import socket
import sys
import json
import random
import subprocess
import requests

version = '5.0.3'

def ping_host(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', host]
    subprocess.run(command)

def openf(name):
    folder_name = Path(__file__).resolve().parent
    file_name = name
    file_path = folder_name / file_name

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f'[ERROR]: {e}')

'''
def writew(name, data):
    folder_name = Path(__file__).resolve().parent
    file_name = name
    file_path = folder_name / file_name

    try:
        with open(file_path, 'r+', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'[ERROR]: {e}')

def writem(name, data):
    folder_name = Path(__file__).resolve().parent
    file_name = name
    file_path = folder_name / file_name

    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f'{data}\n')


def reset(name):
    folder_name = Path(__file__).resolve().parent
    file_name = name
    file_path = folder_name / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('')
'''

def progress(percent=0, width=30):
    left = width * percent // 100
    right = width - left
    tags = '#' * left
    spaces = '' * right
    percents = f'{percent:.0f}%'
    print('\r[', tags, spaces, ']', percents, sep='', end='', flush=True)

#⎿

project_dir = Path(__file__).resolve().parent

try:
    user = os.getlogin()
except OSError:
    print('[ERROR]: cannot find username.')
    user = 'user'

print(r'    _    _            _        ___  ____  ')
print(r'   / \  | | ___ _ __ | |__    / _ \/ ___| ')
print(r"  / _ \ | |/ _ \ '_ \| '_ \  | | | \___ \ ")
print(r' / ___ \| |  __/ |_) | | | | | |_| |___) |')
print(r'/_/   \_\_|\___| .__/|_| |_|  \___/|____/ ')
print(r'               |_|                        ')
print()
print(f'~ Welcome to Aleph OS {version} (tty)! ~')
print("Type 'help' to view avaiable commands")
print()
while True:
    try:
        try:
            user_input = input(f'[\033[91m{user}\033[0m@alephos]% ').strip()
        except KeyboardInterrupt:
            print('\n[ERROR]: Keyboard interruption! Ending session.')
            break
        except EOFError:
            print('\n[ERROR]: End-Of-File! Ending session.')
            break

        if not user_input:
            continue

        parts = user_input.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if user_input == 'exit':
            print('#~ Exiting...')
            break

        elif user_input == 'clear':
            if not args or args == '':
                os.system('cls' if os.name == 'nt' else 'clear')

        elif user_input == 'list':
            print('\033[2m~\033[0m')
            for item in os.listdir(project_dir):
                print(f' ⎿{item}  ')

        elif command == 'ping':
            print('~')
            while True:
                try:
                    ping_host(args)
                    time.sleep(0.2)
                except KeyboardInterrupt:
                    break
        elif user_input == 'help':
            print('\033[2m~\033[0m')
            print('Avaiable commands:')
            print('ping - checks your internet connection. Syntax: ping <url>')
            print('exit - exits Aleph OS. Syntax: exit')
            print('list - shows all files and directories in main Aleph OS directory. Syntax: list')
            print('exec - executes a file. Syntax: exec <file (without extension)>')
            print('clear - clears screen. Syntax: clear')
            print('sysinfo - shows information about system (OS name, OS version, python compiler, python version). Syntax: sysinfo')
            print('spm - downloads a file from oficial Aleph OS repository. Syntax: spm <file (with extension)>')

        elif command == 'exec':
            print('\033[2m~\033[0m')
            args += '.py'
            path = project_dir / args
            time.sleep(0.1)
            if not path.is_file():
                raise FileNotFoundError('so such file.')
            else:
                try:
                    subprocess.run([sys.executable,'-u', path])
                except KeyboardInterrupt:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('[ERROR]: keyboard interruption.')

        elif user_input == 'sysinfo':
            print('\033[2m~\033[0m')
            print('OS: Aleph OS')
            print(f'Version: {version} (beta release)')
            print(f'Python compiler: {platform.python_compiler()}')
            print(f'Python version: {platform.python_version()}')
        elif command == 'spm':
            if args != '':
                try:
                    USERNAME = 'AZ3R0N-0'
                    REPO_NAME = 'Aleph-OS-spm-repository'
                    BRANCH = 'main'
                    timestamp = int(time.time())
                    url = f'https://raw.githubusercontent.com/{USERNAME}/{REPO_NAME}/{BRANCH}/{args}?t={timestamp}'
                    args = os.path.basename(args)
                    full_path = os.path.join(project_dir, args)
                    print("Downloading...")
                    response = requests.get(url)
                    response.raise_for_status()
                    with open(full_path, 'wb') as f:
                        f.write(response.content)
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 404:
                        raise FileNotFoundError(f"Cannot find '{args}' in Aleph OS repository.")
                    else:
                        print(f'HTTP error: {e}')
        else:
            raise SyntaxError(f'no such command: {command}.')
        print('\033[2m~\033[0m')
    except Exception as e:
        print(f'[ERROR]: {e}')
        print('\033[2m~\033[0m')