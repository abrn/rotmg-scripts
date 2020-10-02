import sys
import requests
import os
import time
import xml.etree.ElementTree as ET

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


def get_free_packs(email, password):
    req = requests.post('https://realmofthemadgod.appspot.com/package/getPackages', data={
        'guid': email,
        'password': password,
        'language': 'en',
        'version': 0,
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
        print(f"{bcolors.FAIL}Could not make a request to find free packs as the RotMG API is down - try again later{bcolors.ENDC}")
        sys.exit(0)
    if req.text == '<Error>Account not Found</Error>':
        print(f"{bcolors.FAIL}Could not make a request to find free packs as your first account's details are invalid - replace the account and try again{bcolors.ENDC}")
        sys.exit(0)
    
    root = ET.fromstring(req.text)
    freepacks = []

    for package in root.findall('Package'):
        title = package.attrib['title']
        boxid = package.attrib['id']
        cost = package.find('Price').attrib['amount']
        if cost == '0':
            freepacks.append([title, boxid])
    return freepacks


def make_request(email, password, boxid):
    req = requests.post('https://realmofthemadgod.appspot.com/account/purchasePackage', data={
        'guid': email,
        'password': password,
        'boxId': boxid,
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
    time.sleep(0.1)
    return req.text


def parse_request(packname, response):
    if response == '<Error>Account not found</Error>':
        print(f"{bcolors.FAIL}ERROR: Incorrect username or password - {packname}{bcolors.ENDC}")
    elif response == '<Error>MysteryBoxError.maxPurchase|0</Error>':
        print(f"{bcolors.WARNING}ERROR: Pack is already claimed on this account - {packname}{bcolors.ENDC}")
    elif response[0:9] == '<Success>':
        print(f"{bcolors.OKGREEN}SUCCESS - {packname}{bcolors.ENDC}")
        global success
        success = success + 1
    else:
        print(f"{bcolors.FAIL}ERROR: Failed to make request, try again later - {packname}{bcolors.ENDC}")


count = 0
success = 0
fail = []
chosenpacks = None


for account in accounts:
    count = count + 1
    account_info = account.strip('\n').split(':')
    if len(account_info) != 2:
        print(f"{bcolors.FAIL}Your accounts file is in the wrong format on line {str(count)}")
        print(f"Each line should have format{bcolors.ENDC} {bcolors.OKBLUE}email@mail.com:password{bcolors.ENDC}")
        continue

    email = account_info[0]
    password = account_info[1]

    if chosenpacks is None:
        freepacks = get_free_packs(email, password)
        packamount = len(freepacks)
        print(f"{bcolors.OKGREEN}\nFound {packamount} available free packs:{bcolors.ENDC}\n")

        for x in range(0,packamount):
            print(f"\t[{x}] {freepacks[x][0]}")
        print(f"\t[{packamount}] Claim all packs\n")

        chosenpacks = input(f"{bcolors.OKGREEN}Enter your choice as a number: ")
        print(f"{bcolors.ENDC}")
        if chosenpacks == str(packamount):
            chosenpacks = 'all'
    
    if chosenpacks == 'all':
        print(f"\nClaiming all on {email}")
        for pack in freepacks:
            response = make_request(email, password, pack[1])
            parse_request(pack[0], response)
    elif chosenpacks is not None:
        if int(chosenpacks) > len(freepacks) or int(chosenpacks) < 0:
            print(f"{bcolors.FAIL}Invalid pack choice - try again{bcolors.ENDC}")
            sys.exit(0)
        print(f"\nClaiming on {email}")
        response = make_request(email, password, freepacks[int(chosenpacks)][1])
        parse_request(freepacks[int(chosenpacks)][0], response)


print(f"\n{bcolors.OKGREEN}Successfuly claimed {str(success)} packs{bcolors.ENDC}")
