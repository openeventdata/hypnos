FROM ubuntu:14.04

MAINTAINER John Beieler <jbeieler@caerusassociates.com>

RUN apt-get update && apt-get install -y git python-dev python-pip 

RUN pip install https://github.com/openeventdata/petrarch/archive/0.3.0.zip

ADD . /src

RUN cd /src; pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "/src/petrarch_app.py"]
