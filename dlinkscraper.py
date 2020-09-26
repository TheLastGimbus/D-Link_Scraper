import traceback

import requests
from bs4 import BeautifulSoup


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

    def login(self, login, password_hash):
        """
        Login to your router - you need to do this before you get any other site

        To obtain password hash, you need to use Dev Tools in your browser to "sniff"
        what you browser sends when you log into router and it makes a POST request to /log/in:

        Open router website -> enable Dev Tools -> Log into your router ->
        Dev Tools 'Network' tab -> search for POST on /log/in -> Request ->
        'pw' parameter <= this is what you need

        :param login: Your login. It can't be anything else than 'admin' so...
        :param password_hash: RSA hash of your password
        """
        # Get cookies
        login_r = self._session.post(
            self._url +
            f'/log/in?un={login}&pw={password_hash}'
            f'&rd=%2Fuir%2Fdwrhome.htm&rd2=%2Fuir%2Floginpage.htm&Nrd=1&Nlmb='
        )
        if not login_r.ok:
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
