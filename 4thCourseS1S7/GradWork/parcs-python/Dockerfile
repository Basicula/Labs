FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install python3.7 python3-pip

WORKDIR /parcs

COPY . /parcs

RUN pip3 install -r requirements.txt

CMD ["./run.sh"]
