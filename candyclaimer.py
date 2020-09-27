import sys
import requests
import os

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

def make_request(email, password):
    req = requests.post('https://realmofthemadgod.appspot.com/account/purchasePackage', data={
        'guid': email,
        'password': password,
        'boxId': 23238,
        'quantity': 1,
        'price': 0,
        'currency': 0,
        'guid': email,
        'password': password,
        'game_net': 'Unity',
        'play_platform': 'Unity',
        'game_net_user_id': ''
    }, headers={
        'User-Agent': 'UnityPlayer/2019.4.9f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
        'X-Unity-Version': '2019.4.9f1'
    })
    return req

count = 0
success = 0
fail = []

for account in accounts:
    count = count +1
    account_info = account.strip('\n').split(':')
    if len(account_info) != 2:
        print(f"{bcolors.FAIL}Your accounts file is in the wrong format on line {str(count)}")
        print(f"Each line should have format{bcolors.ENDC} {bcolors.OKBLUE}email@mail.com:password{bcolors.ENDC}")
        continue

    email = account_info[0]
    password = account_info[1]

    result = make_request(email, password)
    print(f"\nClaiming on {email}")

    if result.text == '<Error>Account not found</Error>':
        print(f"{bcolors.FAIL}ERROR: Incorrect username or password{bcolors.ENDC}")
    elif result.text == '<Error>MysteryBoxError.maxPurchase|0</Error>':
        print(f"{bcolors.WARNING}ERROR: Pack is already claimed on this account{bcolors.ENDC}")
    
    elif result.text[0:9] == '<Success>':
        print(f"{bcolors.OKGREEN}SUCCESS{bcolors.ENDC}")
        success = success + 1
        continue
    else:
        print(f"{bcolors.FAIL}ERROR: Failed to make request, try again later{bcolors.ENDC}")
    fail.append(f"{email}:{password}")

print(f"\n{bcolors.OKGREEN}Successfuly claimed packs on {str(success)} accounts{bcolors.ENDC}")

if len(fail) > 0:
    print(f"\n{bcolors.FAIL}Failed to claim packs on {len(fail)} accounts.. saved the list to failed.txt{bcolors.ENDC}")

    with open('failed.txt', 'w') as failfile:
        for failure in fail:
            failfile.write("{}\n".format(failure))
    failfile.close()