FROM python:3.5.2
MAINTAINER Aituglo
WORKDIR /Onyx
ADD . /Onyx

RUN sh install.sh && chmod +x launch.sh
RUN chmod +x ./
RUN pip install -r requirements.txt

EXPOSE 80
CMD ./launch.sh
