# rotmg-scripts
misc badly written scripts for realm of the mad god
most python scripts require the `requests` library

## pack_claimer.py

interactive python script to claim certain or all available free packs with a given account list

it will look for an `accounts.txt` file by default but you can supply a `--file` argument to change it


## mass_changer.py

python script to mass change passwords with an account list, available args:

`--password newpass`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *the new password to use, otherwise it's a random string*   
`--proxyfile file.txt`&nbsp;&nbsp;&nbsp; *use your own proxy list with format ip:port*  
`--out file.txt`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *the file to save the new accounts to, by default it's new_accounts.txt*
