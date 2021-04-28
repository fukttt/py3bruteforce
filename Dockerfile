FROM ubuntu:21.04
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y git

RUN git clone https://github.com/fukttt/py3bruteforce.git
 
WORKDIR /py3bruteforce
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["python3", "app.py"]