FROM mono:3.12.1

LABEL maintainer="Philip Gisella <philip.gisella@theclonker.de>"

RUN apt-get update && \
    apt-get install git python3 -y && \
    apt-get clean && \
    git clone https://github.com/chocolatey/choco/ /usr/local/src/choco/

WORKDIR /usr/local/src/choco
RUN chmod +x build.sh && \
    chmod +x zip.sh && \
    ./build.sh && \
    ln -s /usr/local/src/choco/build_output/chocolatey /usr/local/bin/chocolatey && \
    cp /usr/local/src/choco/docker/choco_wrapper /usr/local/bin/choco

WORKDIR /
COPY buildbox.py /usr/local/bin/buildbox