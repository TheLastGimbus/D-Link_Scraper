# D-Link_Scraper
## Web scraper to obtain information from D-Link DWR-921 router 

This repo contains a library `dlinkscraper.py` - which you can use to scrape data from D-Link DWR-921 router 
(I don't know if it will work on others, I have only this one :P)

...AND a script `duckdns-update.py`, which is an example on how you can use the library 
(and also the reason why I created it :D)

### Library
As always, before using, you need to `pip3 install -r requirements.txt`

To scrape the data from you router, you will need a RSA hash of your password - I wasn't smart enough to 
reverse-engineer on how the router hashes it on login site, so you will need to obtain it yourself:
1. Open router website
2. Enable Dev Tools in your browser (usually Ctrl + Shift + i )
3. Log into your router
4. Look at Dev Tools 'Network' tab
5. Search for POST request on /log/in
6. 'Request' tab -> 'pw' parameter <= this is what you need

Then using it is simple:
```python
from dlinkscraper import DLink
dl = DLink('http://192.168.1.1')  # Change this if yours has different IP
dl.login('admin', <YOUR_PASSWORD_HASH>)
dl.get_main_site()
print(dl.isp_name)
```

### DuckDNS update script
This script is also simple, you just need to supply
 - your DuckDNS token
 - your DuckDNS domain
 - password hash
 
Optionally you can specify:
 - base URL to your router (default is 'http://192.168.1.1')
 - login

All options are in `--help`
