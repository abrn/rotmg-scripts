import sys
import requests
import os
import time
import hashlib
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


def get_free_packs(token):
    req = requests.post('https://realmofthemadgod.appspot.com/package/getPackages', data={
        'language': 'en',
        'version': 0,
        'accessToken': token,
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
        print(f"{bcolors.FAIL}Could not request the pack list as your first account's details are invalid - replace the account and try again{bcolors.ENDC}")
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


def get_access_token(email, password):
    clientToken = hashlib.md5(email.encode('utf-8') + password.encode('utf-8'))

    req = requests.post('https://realmofthemadgod.appspot.com/account/verify', data={
        'game_net': 'Unity',
        'play_platform': 'Unity',
        'game_net_user_id': '',
        'guid': email,
        'password': password,
        'clientToken': clientToken
    }, headers={
        'User-Agent': 'UnityPlayer/2019.4.9f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
        'X-Unity-Version': '2019.4.9f1'
    })

    if req.text == "<Error>Internal error, please wait 5 minutes to try again!</Error>":
        print(f"{bcolors.FAIL}ERROR - Rate limited while grabbing token.. waiting 5 minutes before retrying..{bcolors.ENDC}")
        time.sleep(310)
        token = get_access_token(email, password)
        return token

    try:
        root = ET.fromstring(req.text)
    except:
        return None

    token = root.findall('AccessToken')
    if token is None:
        return None
    else:
        try:
            token = token[0].text
            return token
        except IndexError:
            return None


def do_login(token):
    req = requests.post('https://realmofthemadgod.appspot.com/char/list?muledump=true', data={
        'game_net': 'Unity',
        'play_platform': 'Unity',
        'game_net_user_id': '',
        'do_login': 'true',
        'accessToken': token
    }, headers={
        'User-Agent': 'UnityPlayer/2019.4.9f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
        'X-Unity-Version': '2019.4.9f1'
    })


def make_request(token, boxid):
    req = requests.post('https://realmofthemadgod.appspot.com/account/purchasePackage', data={
        'boxId': boxid,
        'quantity': 1,
        'price': 0,
        'currency': 0,
        'accessToken': token,
        'game_net': 'Unity',
        'play_platform': 'Unity',
        'game_net_user_id': ''
    }, headers={
        'User-Agent': 'UnityPlayer/2019.4.9f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
        'X-Unity-Version': '2019.4.9f1'
    })
    if req.text == "'NoneType' object has no attribute 'put'":
        print(f"{bcolors.WARNING}SUCCESS - Login required, logging in...")
        do_login(token)
        response = make_request(token, boxid)
        return response

    return req.text


def parse_request(packname, response):
    if response == '<Error>Account not found</Error>':
        print(f"{bcolors.FAIL}ERROR - Incorrect username or password - {packname}{bcolors.ENDC}")
    elif response == '<Error>MysteryBoxError.maxPurchase|0</Error>':
        print(f"{bcolors.WARNING}ERROR - Pack is already claimed on this account - {packname}{bcolors.ENDC}")  
    elif response[0:9] == '<Success>':
        print(f"{bcolors.OKGREEN}SUCCESS - {packname}{bcolors.ENDC}")
        global success
        success = success + 1
    else:
        print(f"{bcolors.FAIL}ERROR - Failed to make request: {response}{bcolors.ENDC}")


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
    token = get_access_token(email, password)

    if token is None:
        print(f"{bcolors.FAIL}ERROR - Could not get token for account {email}.. incorrect username or password{bcolors.ENDC}")
        continue

    if chosenpacks is None:
        freepacks = get_free_packs(token)
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
        print(f"\nClaiming all packs on {email}")
        for pack in freepacks:
            response = make_request(token, pack[1])
            parse_request(pack[0], response)
            time.sleep(5)
    elif chosenpacks is not None:
        if int(chosenpacks) > len(freepacks) or int(chosenpacks) < 0:
            print(f"{bcolors.FAIL}Invalid pack choice - try again{bcolors.ENDC}")
            sys.exit(0)
        print(f"\nClaiming on {email}")
        response = make_request(token, freepacks[int(chosenpacks)][1])
        parse_request(freepacks[int(chosenpacks)][0], response)
        time.sleep(5)


print(f"\n{bcolors.OKGREEN}Successfuly claimed {str(success)} packs{bcolors.ENDC}")
