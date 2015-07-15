FROM ubuntu:14.04

MAINTAINER John Beieler <jbeieler@caerusassociates.com>

RUN apt-get update && apt-get install -y git python-dev python-pip 

ADD . /src

RUN cd /src; pip install -r requirements.txt

EXPOSE 5002

CMD ["python", "/src/app.py"]
