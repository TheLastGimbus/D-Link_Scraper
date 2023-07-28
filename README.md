# D-Link Scraper
### This is a library that gets information from your D-Link DWR-921 (and possible others) LTE router admin page using web scraping

This package contains 
 - library `dlinkscraper` - which you can use to scrape data from D-Link DWR-921 LTE router 
(I don't know if it will work on others, I have only this one :P)
 - CLI tool `dlinkscraper` that you can use to get info from console
 - `dlinkscraper-duckdns-update` script, which updates your DuckDNS IP
(and it's also the reason why I created this package :D)

#### Library usage example
```python
from dlinkscraper import DLink
dl = DLink('http://192.168.1.1')  # Change this if yours has different IP
dl.login('admin', <PASSWORD>)
dl.get_main_site()
print(dl.isp_name)

# to get some LTE stats:
dl.get_lte_info()
print(dl.rssi, dl.rscp, dl.rsrp, dl.sinr)

# You should always log out if you don't want to get "admin is already logged in" later
dl.logout()
```

#### CLI usage
Just run `dlinkscraper` from terminal and follow the instructions

#### DuckDNS script usage
Provide all required variables listed in `--help`. Example:
```shell script
dlinkscraper-duckdns-update --token <YOUR_DUCKDNS_TOKEN> --domain <YOUR_DOMAIN> -p <ROUTER_PASSWORD>
```
