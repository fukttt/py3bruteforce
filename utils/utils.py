import datetime
import os
import random

today = datetime.datetime.today()
class Help(object):
    def writelog(projectName, file, log):
        dirr = "logs/" + projectName + "/" + str(today.strftime("%H.%M.%S")) + "/" +file
        os.makedirs(os.path.dirname(dirr), exist_ok=True)
        with open(dirr, 'a') as the_file:
            the_file.write(log + '\n')
    def getRandomUa():
        lines = open('utils/ua.txt').read().splitlines()
        line = random.choice(lines)
        return line