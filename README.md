misc badly written scripts for realm of the mad god. most likely need python 3+ installed

use `pip install -r requirements.txt` to install all dependencies

## pack_claimer.py  

python script to claim certain or all available free packs with a large account list  
by default, it will look for `accounts.txt` in the same folder  
for each account, use the format `email:password` on a new line
# 
`--file file.txt` *use another account list file*    
  
## reward_claimer.py  

python script to login to an account list and log the daily reward. this script *cannot* actually claim the items, just acknowledge that you logged in. by default it will look for `accounts.txt` but you can pass the below argument:  
# 
`--file file.txt` *the account list to use with format email:password*  
 
  
## mass_changer.py  

python script to mass change passwords with an account list
# 
`--password newpass` *the new password to use, otherwise it's a random string*   
`--proxyfile file.txt` *use your own proxy list with format ip:port*  
`--out file.txt` *the file to save the new accounts to, by default it's new_accounts.txt*

## create_null.py  

python script to spam the register endpoint and create an account with no username (null)  
they can't be kicked from dungeons, private messaged and their chat messages are yellow

**THIS IS PATCHED NOW**
# 
`--proxyfile list.txt` *optional - use your own proxy list instead of the scraped proxyscape one* 
  
  
   