import os
import importlib
import jsons
import sys
import datetime
import psutil
from flask import Flask, request, render_template

app = Flask(__name__)
UPLOAD_FOLDER = 'sources'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
        modules = getModules())

@app.route('/wiki')
def wiki():
    return render_template("wiki.html",
        modules = getModules(),
        files = getText())
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("file")
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return "Uploaded succesfully<script>document.location.href='/'</script>"
@app.route('/uploadfile', methods=['GET'])
def uploadfile():
    return render_template("uploadfile.html",
        modules = getModules())
@app.route('/api', methods=['POST']) 
def foo():
    data = request.json
    if data['method'] == "start":
        try:
            b = importlib.import_module('mechanic.' + data['module']).Brute()
            bruteList.append(b)
            b.basename = data['base']
            b.proxyname = data['proxy']
            b.proxytype = data['proxytype']
            b.proxylink = data['proxylink']
            b.projid = len(bruteList) + 1
            b.thread_count = int(data['threads'])
            b.timeout = (int(data['timeout']),int(data['timeout']))
            b.mult()
            return "Started succesfully"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error while starting module " + data['module'] + " [" + str(e) + "] " + fname + " " + str(exc_tb.tb_lineno)
    if data['method'] == "get":
        try:
            
            proj = ""
            if len(bruteList) == 0:
                return "No projs"
            elif len(bruteList) == 1:
                for it in bruteList:
                    proj += it.projectName + "#" + str(it.projid) + " | " + \
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
                    proj += it.projectName + "#" + str(it.projid) +  " | " + \
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

    if data['method'] == "getcpu":
        
        stat = str(psutil.cpu_percent(interval=0)) + "|" + datetime.datetime.today().strftime("%H.%M.%S")
        return '{}'.format(stat)
    if data['method'] == "stop":
        for a in bruteList:
            if a.projid == int(data['id']):
                a.running = False
                bruteList.remove(a)
                return "Stopped succesfully!"
                break
            
        return "Project no found"




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