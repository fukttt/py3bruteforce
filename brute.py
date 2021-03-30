import requests
import sys 
import os 
import argparse
import importlib
from helpers.colors import bcolors

#from mechanic.ivi import Brute
#from mechanic.porn import Brute



if __name__ == '__main__':

   

    parser = argparse.ArgumentParser(description='How to use it :')
    parser.add_argument ('-p', '--proxy', help='example of use : python3 brute.py -p proxy.txt')
    parser.add_argument ('-b', '--base', help='example of use : python3 brute.py -b log.txt')
    parser.add_argument ('-t', '--threads', type=int, help='example of use : python3 brute.py -t 150')
    parser.add_argument ('-m', '--module', help='example of use : python3 brute.py -m ivi')
    parser.add_argument ('-pt', '--proxytype', help='example of use : python3 brute.py -pt https (https, socks4, socks5, burp)')
    parser.add_argument ('-ls', '--list', help='example of use : python3 brute.py -ls', action='store_true')

    namespace = parser.parse_args()

    b = importlib.import_module('mechanic.ivi').Brute()

    if (namespace.list == True):
        print(bcolors.OKGREEN + '[+] List of all modules' + bcolors.ENDC)
        count = 1
        for filename in os.listdir('mechanic'):
            if filename.endswith(".py"): 
                m = importlib.import_module('mechanic.' + filename.replace('.py', '')).Brute()
                print("["+str(count)+"] " + "["+filename.replace('.py', '')+"] " +m.projectFullName +  " " + bcolors.OKGREEN + m.description + bcolors.ENDC)
                count += 1
        sys.exit()

    if (namespace.module != None):
        print(bcolors.OKGREEN + '[+] Selected module is : ' + str(namespace.module) + bcolors.ENDC)
        b = importlib.import_module('mechanic.' + namespace.module).Brute()
        
    else:
        print(bcolors.FAIL + '[+] No module name in -m. Exiting. Bye!' + bcolors.ENDC)
        sys.exit()
    
    if (namespace.base != None):
        print(bcolors.OKGREEN + '[+] Selected base file : ' + namespace.base + bcolors.ENDC)
        b.basename = namespace.base
    else:
        print(bcolors.WARNING + '[+] Basename didnt selected. Using as default log.txt.' + bcolors.ENDC)
        
    if (namespace.proxytype != None):
        print(bcolors.OKGREEN + '[+] Selected proxy type : ' + namespace.proxytype + bcolors.ENDC)
        b.proxytype = namespace.proxytype
    else:
        print(bcolors.WARNING + '[+] Proxytype didnt selected. Using as default https.' + bcolors.ENDC)
    
    if (namespace.proxy != None):
        print(bcolors.OKGREEN + '[+] Selected proxy file : ' + namespace.proxy + bcolors.ENDC)
        b.proxyname = namespace.proxy
    else:
        print(bcolors.WARNING + '[+] Proxyfile didnt selected. Using as default proxy.txt.' + bcolors.ENDC)

    if (namespace.threads != None):
        print(bcolors.OKGREEN + '[+] Selected threads count : ' + str(namespace.threads) + bcolors.ENDC)
        b.thread_count = namespace.threads
    else:
        print(bcolors.WARNING + '[+] Threads count didnt selected. Using as default 150.' + bcolors.ENDC)
    
    
    
    print("[+] Module name is : " + bcolors.UNDERLINE + b.projectFullName+ bcolors.ENDC)
    print("[+] Module description is : "+ bcolors.UNDERLINE+ b.description+ bcolors.ENDC)
    print("[+] Threads count : "+ bcolors.UNDERLINE + str(b.thread_count)+ bcolors.ENDC)
    b.mult()
    
