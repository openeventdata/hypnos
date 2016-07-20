FROM ubuntu:14.04

MAINTAINER John Beieler <johnb30@gmail.com>

RUN apt-get update && apt-get install -y git python-dev python-pip

RUN pip install git+https://github.com/openeventdata/petrarch2.git

ADD . /src

RUN cd /src; pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "/src/petrarch_app.py"]
