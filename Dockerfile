FROM python:3.5.2
MAINTAINER Aituglo
RUN adduser --disabled-password --gecos "" onyx && cd /home/onyx/ && git clone $
WORKDIR /home/onyx/Onyx/
RUN cd /home/onyx/Onyx/ && sh install.sh && chmod +x launch.sh
RUN mv onyx/config_example.py onyx/flask_config.py && chown onyx:onyx ./*
EXPOSE 80
CMD ./launch.sh