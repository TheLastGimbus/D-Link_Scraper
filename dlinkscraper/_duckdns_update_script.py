def main():
    import argparse
    import re
    import traceback

    import requests

    from dlinkscraper import DLink

    parser = argparse.ArgumentParser(
        'DuckDNS Updater',
        description=
        """This script updates your DuckDNS IPv4 address to scraped address 
        from your D-Link router. Because in LTE routers, your visible public 
        IP doesn't always match with IP that is needed to access you, 
        we need to scrape it from router's admin page"""
    )
    parser.add_argument('--token', '-t', type=str, required=True, help='Your DuckDNS token')
    parser.add_argument('--domain', '-d', type=str, required=True, help='Your DuckDNS domain')
    parser.add_argument(
        '--login', '-l', type=str, required=False, default='admin',
        help="Login to your router. It's always 'admin', so, yeah, "
             "you don't need to specify it...")
    parser.add_argument(
        '--password', '-p', type=str, required=True,
        help="Password to your router's admin"
    )
    parser.add_argument(
        '--router-url', '-u', type=str, required=False, default='http://192.168.1.1',
        help="Base URL to you router. Usually something "
             "like 'http://192.168.1.1' (that's default)")
    parser.add_argument(
        '--no-cache', action='store_true',
        help="Don't cache and check last known IP. This is default behaviour, "
             "as it won't ping DuckDNS every time - only when IP changed")
    parser.add_argument(
        '--cache-file', type=str, required=False, default='last_ip.txt',
        help='Path to file where last known IP will be cached')

    args = parser.parse_args()

    dl = DLink(args.router_url)
    print('Logging in to router...')
    dl.login(args.login, args.password)
    print('Getting router main page...')
    dl.get_main_site()
    print('Logging out...')
    dl.logout()

    # Check if it's actually valid IP
    if dl.public_ip is None or not re.match(r'\d+\.\d+\.\d+\.\d+', dl.public_ip):
        print('Got invalid IP from router! Exit!')
        exit(-1)

    print('IP from router: ' + dl.public_ip)

    if not args.no_cache:
        print('Checking last known IP...')
        try:
            with open(args.cache_file, 'r') as f:
                saved_ip = f.read()
                print('Last IP: ' + saved_ip)
        except:
            saved_ip = 'error'
            print(f"Can't open cache file ({args.cache_file})")
            traceback.print_exc()

        if saved_ip == dl.public_ip:
            print('Last IP was the same :) Exit.')
            exit(0)
        else:
            print('IP changed!')

    req = requests.get(
        f'https://www.duckdns.org/update'
        f'?domains={args.domain}'
        f'&token={args.token}'
        f'&ip={dl.public_ip}'
    )
    if req.ok and req.content.decode('utf-8') == 'OK':
        print('Updating IP success :)')
        if not args.no_cache:
            print('Saving current IP for later...')
            try:
                with open(args.cache_file, 'w') as f:
                    f.write(dl.public_ip)
            except:
                print("Can't write cache file!")
                traceback.print_exc()

            print('Saving current IP success :)')
        exit(0)
    else:
        print('Updating IP failed!')
        exit(-1)


if __name__ == '__main__':
    main()
