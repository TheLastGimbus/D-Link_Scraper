import pathlib
import random
import string
import traceback
import urllib.parse

import requests
from bs4 import BeautifulSoup
from py_mini_racer import py_mini_racer


class DLink:
    """
    D-Link router

    At init, it contains empty values, that you can fill by getting corresponding sites.
    Before you access any of those sites, you need to successfully login()

    :param base_url: Default URL to your router, usually 'http://192.168.1.1'
    """

    def __init__(self, base_url):
        self._url = base_url
        self._session = requests.session()
        self.network_signal_strength = None
        self.internet_available = False
        self.network_name = None
        self.network_type = None
        self.isp_name = None
        self.public_ip = None

    def login(self, login, password):
        """
        Login to your router - you need to do this before you get any other site

        :param login: Your login. It can't be anything else than 'admin' so...
        :param password: Password to your admin
        """

        # Get main site to get public RSA key
        login_r = self._session.get(self._url + '/loginpage.htm')
        if not login_r.ok:
            raise IOError
        # Scrape the key
        login_soup = BeautifulSoup(login_r.content, features='html.parser')
        pub_key_txt = login_soup.find(id='divpem').text
        pub_key_txt = pub_key_txt.replace('\n', '').strip()

        # This is what the site does (in aes.js) before sending password
        # Why does it generate 16 random digits before password?
        # ¯\_(ツ)_/¯
        pwdv = password + ':' + ''.join(random.choice(string.digits) for i in range(16))

        # We need to use JavaScript engine
        ctx = py_mini_racer.MiniRacer()
        # ...to execute code that encrypts password before sending.
        # I couldn't get it working in Python, so I just stole all required JS
        # and execute it :)
        ctx.eval((pathlib.Path(__file__).parent / 'stolen_javascript.js').read_text())
        pwd_hash = ctx.eval(f"""
        var key = RSA.getPublicKey("{pub_key_txt}");
        RSA.encrypt("{pwdv}", key);
        """)

        # Get cookies by logging in
        auth_r = self._session.post(
            self._url +
            f'/log/in?un={urllib.parse.quote(login)}&pw={urllib.parse.quote(pwd_hash)}'
            f'&rd=%2Fuir%2Fdwrhome.htm&rd2=%2Fuir%2Floginpage.htm&Nrd=1&Nlmb='
        )
        if not auth_r.ok:
            raise IOError

    def logout(self):
        """
        Log out of current session

        You should always do this if you don' want to get
        "admin is currently logged in" all the times
        """
        self._session.get(self._url + '/log/out')

    def get_main_site(self):
        """
        Loads main site on router

        Gives you (if no problems occurred):

        network_signal_strength

        internet_available

        network_type

        isp_name

        public_ip
        """
        main_r = self._session.get('http://192.168.1.1/uir/dwrhome.htm')
        # If there was a redirect then we didn't log in successfully
        if not main_r.ok or len(main_r.history) > 0:
            raise IOError
        main_soup = BeautifulSoup(main_r.content, features='html.parser')

        # network_signal_strength
        try:
            signal_text = main_soup.find(id='_3g_signal').text
            self.network_signal_strength = int(signal_text[signal_text.index('-'): -4])
        except:
            print("Can't scrape network_signal_strength! Error:")
            traceback.print_exc()

        # internet_available
        try:
            self.internet_available = main_soup.find(id='connect_light').img.get(
                'src') == 'Home_Internet_GreenCircle.png'
        except:
            print("Can't scrape internet_available! Error:")
            traceback.print_exc()

        # network_type
        try:
            self.network_type = main_soup.find(id='_3g_service').text.lower()
        except:
            print("Can't scrape network_type! Error:")
            traceback.print_exc()

        # isp_name
        try:
            network_script = main_soup.find(id='networks').script.contents[0]
            variable_index = network_script.index('networknm="') + 11
            end_index = network_script.index('"', variable_index)
            self.isp_name = network_script[variable_index:end_index]
        except:
            print("Can't scrape isp_name! Error:")
            traceback.print_exc()

        # public_ip
        try:
            self.public_ip = main_soup.find(id='_3g_ip').text.strip()
        except:
            print("Can't scrape public_ip! Error:")
            traceback.print_exc()
