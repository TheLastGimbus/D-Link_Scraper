# D-Link_Scraper
## Web scraper to obtain information from D-Link DWR-921 router 

This repo contains a library `dlinkscraper.py` - which you can use to scrape data from D-Link DWR-921 router 
(I don't know if it will work on others, I have only this one :P)

...AND a script `duckdns-update.py`, which is an example on how you can use the library 
(and also the reason why I created it :D)

### Library
As always, before using, you need to `pip3 install -r requirements.txt`

Then using it is simple:
```python
from dlinkscraper import DLink
dl = DLink('http://192.168.1.1')  # Change this if yours has different IP
dl.login('admin', <PASSWORD>)
dl.get_main_site()
print(dl.isp_name)

# You should always log out if you don't want to get "admin is already logged in" later
dl.logout()
```

Because it executes some JS that I stole from login page, it needs to access `stolen_javascript.js`

If you want to use this without `cd`'ing to it's folder, you need to specify path to it:
```python
dl.login('admin', 'pass', '/path/to/stolen_javascript.js')
```

### DuckDNS update script
This script is also simple, you just need to supply
 - your DuckDNS token
 - your DuckDNS domain
 - password to router
 
Optionally you can specify:
 - base URL to your router (default is 'http://192.168.1.1')
 - login

All options are in `--help`
