import argparse

from dlinkscraper.dlinkscraper import DLink


def main():
    parser = argparse.ArgumentParser("D-Link scraper")
    parser.add_argument('--url', '-u', required=False, help='Base URL to your router')
    parser.add_argument('--login', '-l', required=False, help='Login to your router admin')
    parser.add_argument('--password', '-p', required=False, help='Password to your router admin')
    args = parser.parse_args()
    if args.url is None:
        args.url = input("Input your url (leave blank for 'http://192.168.1.1'):\n")
        if len(args.url.strip()) == 0:
            args.url = 'http://192.168.1.1'
    if args.login is None:
        args.login = input("Input your login (leave blank for 'admin'):\n")
        if len(args.login.strip()) == 0:
            args.login = 'admin'
    if args.password is None:
        args.password = input("Input your password (leave blank for 'admin'):\n")
        if len(args.password.strip()) == 0:
            args.password = 'admin'

    dl = DLink(args.url)
    print('Logging in...')
    try:
        dl.login(args.login, args.password)
    except IOError:
        print("Can't log in!")
        exit(-1)

    print('Scraping all the data I can...')
    try:
        dl.get_main_site()
    except IOError:
        print("Can't scrape main site!")

    print("Network signal strength: " + dl.network_signal_strength)
    print("Is internet available: " + dl.internet_available)
    print("Network name: " + dl.network_name)
    print("Network type: " + dl.network_type)
    print("ISP name: " + dl.isp_name)
    print("Public ip: " + dl.public_ip)


if __name__ == "__main__":
    main()
