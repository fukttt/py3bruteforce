import requests
import sys 
import os 


#from mechanic.ivi import Brute
from mechanic.porn import Brute



if __name__ == '__main__':
    b = Brute()
    print("Project name is : " + b.projectFullName)
    print("Project description is : "+ b.description)
    print("Threads count : " + str(b.thread_count))
    b.mult()
