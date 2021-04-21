import os
import importlib
import sys
import psutil
from flask import Flask, request, render_template

app = Flask(__name__)
bruteList = []

@app.route('/')
def index():
    return render_template("index.html",
        title = 'Web-Bruteforce',
        modules = getModules(),
        aval = bruteList)

@app.route('/module/<string:module>')
def mod(module):
    b = importlib.import_module('mechanic.' + module).Brute()
    return render_template("module.html",
        mod = b,
        module = module,
        modules = getModules(),
        files = getText())


@app.route('/sysinfo')
def sysinfp():
    a = psutil
    return render_template("sysinfo.html",
        sys = a,
        modules = getModules(),
        files = getText())

@app.route('/wiki')
def wiki():
    return render_template("wiki.html",
        modules = getModules(),
        files = getText())

@app.route('/api', methods=['POST']) 
def foo():
    data = request.json
    if data['method'] == "start":
        try:
            b = importlib.import_module('mechanic.' + data['module']).Brute()
            b.basename = data['base']
            b.proxyname = data['proxy']
            b.proxytype = data['proxytype']
            b.proxylink = data['proxylink']
            b.projid = len(bruteList) + 1
            b.thread_count = int(data['threads'])
            b.timeout = (int(data['timeout']),int(data['timeout']))
            b.mult()
            bruteList.append(b)
            return "Started succesfully"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error while starting module " + data['module'] + " [" + str(e) + "] " + fname + " " + str(exc_tb.tb_lineno)
    if data['method'] == "get":
        return str(bruteList[int(data['id'])].good) + "/" + str(bruteList[int(data['id'])].bad) + "/" + str(bruteList[int(data['id'])].error) + "/" + str(bruteList[int(data['id'])].projerror) + "/" + str(bruteList[int(data['id'])].captcha)
    if data['method'] == "stop":
        for a in bruteList:
            if a.projid == int(data['id']):
                a.running = False
                bruteList.remove(a)
                return "Stopped succesfully!"
            else:
                return "Can't stop! Id didn't found!"




def getModules():
    a = []
    for filename in os.listdir('mechanic'):
        if ".py" in filename:
            a.append(filename.replace('.py', ''))
    return a

def getText():
    a = []
    for filename in os.listdir('sources'):
        if ".txt" in filename:
            a.append(filename)
    return a

app.run(host="0.0.0.0", debug = True)