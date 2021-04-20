import os
import importlib
import sys
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

@app.route('/wiki')
def wiki():
    return '<h1>Will be soon</h1><a href="/"><- back</a>'

@app.route('/api', methods=['POST']) 
def foo():
    data = request.json
    if data['method'] == "start":
        try:
            b = importlib.import_module('mechanic.' + data['module']).Brute()
            b.basename = data['base']
            b.proxyname = data['proxy']
            b.proxytype = data['proxytype']
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

app.run(debug = True)