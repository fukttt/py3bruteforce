import os
import importlib
import jsons
import sys
import datetime
import psutil
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
bruteList = []
hiddenList = []

@app.route('/')
def index():
    return render_template("index.html",
        title = 'Dashboard',
        modules = getModules(),
        aval = bruteList)

@app.route('/module/<string:module>')
def mod(module):
    b = importlib.import_module('mechanic.' + module).Brute()
    return render_template("module.html",
        mod = b,
        module = module,
        modules = getModules(),
        files = getText(), 
        title=b.projectFullName)


@app.route('/sysinfo')
def sysinfp():
    return render_template("sysinfo.html",
        modules = getModules(),
        title = "System monitoring")

@app.route('/logs')
def logs():
    return render_template("logs.html",
        log = getLogs(),
        title = "Watch logs")

@app.route('/wiki')
def wiki():
    return render_template("wiki.html",
        modules = getModules(),
        files = getText(),
        title="Wiki")
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("file")
        for file in files:
            if file.filename != '' and ".txt" in file.filename:
                file.save(os.path.join('sources', file.filename))
    return redirect(url_for('index'))

@app.route('/uploadmodule', methods=['GET', 'POST'])
def upload_module():
    if request.method == "POST":
        files = request.files.getlist("file")
        for file in files:
            if file.filename != '' and ".py" in file.filename:
                file.save(os.path.join('mechanic', file.filename))
    return redirect(url_for('index'))

@app.route('/uploadfile', methods=['GET'])
def uploadfile():
    return render_template("uploadfile.html",
        modules = getModules(),
        title="Upload file")
@app.route('/api', methods=['POST']) 
def foo():
    data = request.json
    if data['method'] == "start":
        try:
            b = importlib.import_module('utils.Core').Core(data['module'])
            bruteList.append(b)
            b.basename = data['base']
            b.proxyname = data['proxy']
            b.proxytype = data['proxytype']
            b.proxylink = data['proxylink']
            b.projid = len(bruteList) + 1
            b.thread_count = int(data['threads'])
            b.timeout = (int(data['timeout']),int(data['timeout']))
            b.mainPoint()
            return "Started succesfully"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error while starting module " + data['module'] + " [" + str(e) + "] " + fname + " " + str(exc_tb.tb_lineno))
    if data['method'] == "get":
        try:
            
            proj = ""
            if len(bruteList) == 0:
                return "No projs"
            elif len(bruteList) == 1:
                for it in bruteList:
                    proj += it.projectName + " (" + str(it.lines.qsize()) + ") | " + \
                        str(it.good) + " | " + \
                        str(it.bad) + " | " + \
                        str(it.error) + " | " + \
                        str(it.projerror) + " | " + \
                        str(it.captcha) + " | " + \
                        it.basename + " | " + \
                        str(len(it.prlines)) + " | " + \
                        str(it.thread_count) + " | " + \
                        it.proxytype + " | " + \
                        str(it.projid) + " | "
                return '{}'.format(proj)
            else :
                for it in bruteList:
                    proj += it.projectName + " (" + str(it.lines.qsize()) +  ") | " + \
                        str(it.good) + " | " + \
                        str(it.bad) + " | " + \
                        str(it.error) + " | " + \
                        str(it.projerror) + " | " + \
                        str(it.captcha) + " | " + \
                        it.basename + " | " + \
                        str(len(it.prlines)) + " | " + \
                        str(it.thread_count) + " | " + \
                        it.proxytype + " | " + \
                        str(it.projid) + "||"
                return '{}'.format(proj)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return exc_type, fname, exc_tb.tb_lineno
    if data['method'] == "getlog":
        return '{}'.format(getLog(data["dir"]))
    if data['method'] == "getcpu":
        
        stat = str(psutil.cpu_percent(interval=0)) + "|" + datetime.datetime.today().strftime("%H.%M.%S")
        return '{}'.format(stat)
    if data['method'] == "stop":
        for a in bruteList:
            if a.projid == int(data['id']):
                a.stop()
                bruteList.remove(a)
                return "Stopped succesfully!"
                break
            
        return "Project no found"


def hidden(path):

    for i in hiddenList:
        if i != '' and i in path:
            return True
    
    return False


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
def getLogs():
    dirs = []
    directory = 'logs/'
    for filename in os.listdir(directory):
        a = os.path.join(directory, filename)
        for filename in os.listdir(os.path.join(directory, filename)):
            b = a + "/" + filename
            for filename in os.listdir(os.path.join(a, filename)):
                dirs.append( b + "/" + filename)
    return dirs

def getLog(fr):
    f = open(fr, "r")
    return f.read()
if __name__=="__main__":
    try:
        app.run("0.0.0.0",5000,True)
    except (KeyboardInterrupt, SystemExit):
        for it in bruteList:
            it.running = False
