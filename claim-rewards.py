import sys
import requests
import os
import time

from lib.req import *
from lib.log import color, log

# switch os terminal color mode
os.system('color')


if len(sys.argv) >= 2 and sys.argv[1] == '-i' or sys.argv[1] == '--file':
    if len(sys.argv) < 3:
        log(f'enter a filename to read e.g:\n {color.WARN}python {sys.argv[0]} {sys.argv[1]} accounts.txt{color.EOF}', 'FILES', color.FAIL)
        sys.exit(0)
    else:
        filename = sys.argv[2]
else:
    filename = 'accounts.txt'

try:
    file = open(filename, 'r')
    accounts = file.readlines()
except FileNotFoundError:
    log('enter a filename to read e.g:\n\n python {} --file accountlist.txt'.format(sys.argv[0]), "FILES", color.FAIL)
    print(f"{color.FAIL}Could not find the{color.EOF} {color.INFO}{filename}{color.EOF}{color.FAIL} file{color.EOF}")
    sys.exit(0)




count = 0
success = 0

for account in accounts:
    count = count + 1
    account_info = account.strip('\n').split(':')
    if len(account_info) != 2:
        print(f"{color.FAIL}Your accounts file is in the wrong format on line {str(count)}")
        print(f"Each line should have format{color.EOF} {color.INFO}email@mail.com:password{color.EOF}")
        continue

    email = account_info[0]
    password = account_info[1]

    print(f"\nClaiming on {email}")
    response = do_login(email, password)
    parse_request(response)

print(f"\n{color.OK}Successfuly logged in on {str(success)}/{str(count)} accounts{color.EOF}")
print(f"\n{color.FAIL}WARNING:{color.EOF} Your logins have been counted, but the items still need to be claimed ingame")