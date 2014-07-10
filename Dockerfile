FROM ubuntu:trusty
MAINTAINER Tutum <info@tutum.co>

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python python-dev python-pip libyaml-dev
ADD . /app
RUN pip install /app

ENTRYPOINT ["tutum"]
