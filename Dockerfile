FROM ubuntu:saucy
MAINTAINER Tutum <info@tutum.co>

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python python-pip
RUN pip install tutum

ENTRYPOINT ["tutum"]
