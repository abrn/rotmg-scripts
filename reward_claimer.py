import sys
import requests
import os
import time

os.system('color')
class bcolors:
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

if len(sys.argv) >= 2 and sys.argv[1] == '--file':
    if len(sys.argv) < 3:
        print('Please enter a filename to read e.g:\n\n python {} --file accountlist.txt'.format(sys.argv[0]))
        sys.exit(0)
    else:
        filename = sys.argv[2]
else:
    filename = 'accounts.txt'

try:
    f = open(filename, 'r')
    accounts = f.readlines()
except FileNotFoundError:
    print(f"{bcolors.FAIL}Could not find the{bcolors.ENDC} {bcolors.OKBLUE}{filename}{bcolors.ENDC}{bcolors.FAIL} file{bcolors.ENDC}")
    sys.exit(0)


def do_login(email, password):
    req = requests.post('https://realmofthemadgod.appspot.com/char/list', data={
        'do_login': 'true',
        'guid': email,
        'password': password,
        'game_net': 'Unity',
        'play_platform': 'Unity',
        'game_net_user_id': ''
    }, headers={
        'User-Agent': 'UnityPlayer/2019.4.9f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
        'X-Unity-Version': '2019.4.9f1'
    })
    if req.status_code != 200:
        print(f"{bcolors.FAIL}Could not make the login request as the RotMG API is down - try again later{bcolors.ENDC}")
        sys.exit(0)
    return req.text

def parse_request(response):
    if response == '<Error>Account not found</Error>':
        print(f"{bcolors.FAIL}ERROR: Incorrect username or password{bcolors.ENDC}")
    elif response[0:6] == '<Chars':
        print(f"{bcolors.OKGREEN}SUCCESS{bcolors.ENDC}")
        global success
        success = success + 1
    elif response == '<Error>Internal error, please wait 5 minutes to try again!</Error>':
        print(f"{bcolors.WARNING}ERROR: Your IP has been rate limited - try again in 5 minutes{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}ERROR: Failed to make request, try again later{bcolors.ENDC}")

count = 0
success = 0

for account in accounts:
    count = count + 1
    account_info = account.strip('\n').split(':')
    if len(account_info) != 2:
        print(f"{bcolors.FAIL}Your accounts file is in the wrong format on line {str(count)}")
        print(f"Each line should have format{bcolors.ENDC} {bcolors.OKBLUE}email@mail.com:password{bcolors.ENDC}")
        continue

    email = account_info[0]
    password = account_info[1]

    print(f"\nClaiming on {email}")
    response = do_login(email, password)
    parse_request(response)

print(f"\n{bcolors.OKGREEN}Successfuly logged in on {str(success)}/{str(count)} accounts{bcolors.ENDC}")
print(f"\n{bcolors.FAIL}WARNING:{bcolors.ENDC} Your logins have been counted, but the items still need to be claimed ingame")