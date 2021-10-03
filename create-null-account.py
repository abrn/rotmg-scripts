"""
-- THIS METHOD IS PATCHED NOW --
It worked via spamming account register requests and omitting the username
field. Every 24 hours a null account would become available and a lucky person
running a script could register it.
"""
import time
import requests
import sys
from random import randint

# replace this email and password with the one to register the null account
REGISTER_EMAIL = 'replace@gmail.com'
REGISTER_PASS = 'yourpass'

# the SOCKS type to use (4 or 5), keep at 4 unless you have issues
SOCKS_VERSION = 4


# takes a --proxyfile arg or just scrapes some from proxyscape
if '--proxyfile' in sys.argv:
    p = open('proxies.txt')
    proxyList = p.readlines()
else:
    proxyReq = requests.get(
        'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=3000&country=all&ssl=all&anonymity=all')
    if proxyReq.status_code == 200:
        proxyList = proxyReq.text.splitlines()
    else:
        print('Failed to retreive proxies via URL.. please load from file')
        sys.exit(-1)


def make_req():
    if len(proxyList) == 0:
        return 'No available stable proxies remaining.. Try run the script again with the accounts it missed before'
        sys.exit(-1)
    proxy = get_proxy(proxyList)

    req = None
    while req is not None:
        url = 'https://www.realmofthemadgod.com/account/register?g={}'.format(REGISTER_EMAIL)
        try:
            req = requests.post(url, data={
                'newGUID': REGISTER_EMAIL,
                'newPassword': REGISTER_PASS,
                'gameClientVersion': '2.0.3.1.0',
                'ignore': '123456',
                'entrytag': '',
                'name': '',
                'isAgeVerified': '1',
                'signedUpKabamEmail': '0'
            }, proxies=proxy)
            return req.text
        except Exception as e:
            print('\nProxy failed... switching')
            print(e)
            if len(proxyList) == 0:
                return 'No proxies remaining'
            else:
                proxy = get_proxy(proxyList)


def get_proxy(fromList):
    proxyCount = len(fromList)
    proxyIndex = randint(0, proxyCount - 1)
    newProxy = fromList[proxyIndex].split(':')
    proxy = {
        'http': f'socks{SOCKS_VERSION}://{newProxy[0]}:{newProxy[1]}',
        'https': f'socks{SOCKS_VERSION}://{newProxy[0]}:{newProxy[1]}'
    }
    return proxy


def main():
    try_count = 0
    result = None

    while result is None:
        req = make_req()
        try_count += 1

        if req == 'No proxies remaining':
            print('\n' + req)
            sys.exit(0)
        if req == '<Error>Error.nameAlreadyInUse</Error>':
            print('Failed to create, attempt: {}'.format(try_count))
        elif req[0:6] == '<Error>':
            print('Failed to create with error: {} - attempt: {}'.format(req, try_count))
        elif req is None:
            print('Failed to create, connection failed - attempt: {}'.format(try_count))
        elif req[0:8] == '<Success>':
            print(
                'SUCCESS at time {} with attempt {}\n\nEmail: {}\nPassword: {}'.format(time.time(), try_count, REGISTER_EMAIL, REGISTER_PASS))
            result = True
            break
        else:
            print('Failed to create with error: {} - attempt: {}'.format(req, try_count))


if __name__ == "__main__":
    main()
