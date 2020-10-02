# rotmg-scripts
misc badly written scripts for realm of the mad god  
most python scripts require the `requests` library

## pack_claimer.py

interactive python script to claim certain or all available free packs with a given account list. by default it will look for `accounts.txt` but you can pass the below argument:  

`--file file.txt`&nbsp;&nbsp;&nbsp;&nbsp; *the account list to use with format email:password*  


## mass_changer.py

python script to mass change passwords with an account list, optional args:

`--password newpass`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *the new password to use, otherwise it's a random string*   
`--proxyfile file.txt`&nbsp;&nbsp;&nbsp; *use your own proxy list with format ip:port*  
`--out file.txt`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *the file to save the new accounts to, by default it's new_accounts.txt*

## create_null.py

python script to spam the /account/register endpoint and create a "null" name account  

**note:** one null name account can be made every 24 hours, which means only one lucky person running this script will get one  
to increase your chances, either multithread the script, use better proxies or run multiple scripts at once  

`--proxyfile file.txt`&nbsp;&nbsp;&nbsp;&nbsp; *optional - use your own proxy list instead of the scraped proxyscape one - format ip:port* 
