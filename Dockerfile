FROM ubuntu:20.04
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY . /app
 
WORKDIR /app
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["python3", "app.py"]
