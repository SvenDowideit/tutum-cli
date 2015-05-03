FROM alpine
MAINTAINER support@tutum.co

RUN apk --update add python py-pip tar curl
ADD . /app
RUN export SDK_VER=$(cat /app/requirements.txt | grep python-tutum | grep -o '[0-9.]*') && \
    curl -0L https://github.com/tutumcloud/python-tutum/archive/v${SDK_VER}.tar.gz | tar -zxv && \
    pip install python-tutum-${SDK_VER}/. && \
    pip install /app && \
    rm -rf /app python-tutum-${SDK_VER} && \
    tutum -v

ENTRYPOINT ["tutum"]
