misc badly written python scripts for realm of the mad god. you will need likely the most [up-to-date](https://www.python.org/downloads/) version of python 3+ installed

with python installed,   
use `pip3 install -r requirements.txt` to install all dependencies

## claim-packs.py  

this script will run over a list of accounts and claim certain or all available free packs
by default, it will look for `accounts.txt` in the same folder. for each account, use the format `email:password` on a new line  
you can pass the below arguments to customize the script running:  

`-i filename.txt`  `--file filename.txt` (*optional*)
+ use your own account list file. if none is supplied it will default to `accounts.txt` in the script path 
  
## claim-rewards.py  

python script to log in to an account list and log the daily reward. this script *cannot* actually claim the items, just acknowledge that you logged in. by default it will look for `accounts.txt`  
you can pass the below arguments to customize the script running:

`-i filename.txt`  `--file filename.txt` (*optional*)
+ use your own account list file. if none is supplied it will default to `accounts.txt` in the script path

## create-null-account.py  
**THIS IS PATCHED NOW**  

python script to spam the register endpoint and create an account with no username (null)  /
they can't be kicked from dungeons, private messaged and their chat messages are yellow like an Admins
 
`--proxyfile filename.txt` (*optional*)
+ use your own proxy file list. if none is supplied they will be scraped from proxyscrape  
