FROM python:3.7-slim-buster
MAINTAINER Aituglo <contact@aituglo.com>

RUN apt-get update && apt-get install -y git wget
RUN git clone https://github.com/OnyxProject/onyx

RUN bash onyx/install_debian_script.sh
RUN bash onyx/setup.sh

WORKDIR /onyx

EXPOSE 8080
ENTRYPOINT ["./onyx.sh start"]
CMD ["./onyx.sh start"]