# See README for how to use this.

FROM ubuntu:jammy
LABEL maintainer="Michael Halstead <mhalstead@linuxfoundation.org>"

ENV PYTHONUNBUFFERED=1 \
    LANGUAGE=en_US \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LC_CTYPE=en_US.UTF-8
## Uncomment to set proxy ENVVARS within container
#ENV http_proxy http://your.proxy.server:port
#ENV https_proxy https://your.proxy.server:port
#ENV no_proxy localhost,127.0.0.0/8

# NOTE: we don't purge gcc below as we have some places in the OE metadata that look for it

COPY requirements.txt /
RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
        && locale-gen en_US.UTF-8 \
        && update-locale \
    && apt-get install -y --no-install-recommends \
	autoconf \
	cpio \
	curl \
	g++ \
	gcc \
	git \
	libfreetype6-dev \
	libjpeg-dev \
	default-libmysqlclient-dev \
	make \
	netcat-openbsd \
	pkg-config \
	python2 \
	python3-dev \
	python3-pip \
	python3-wheel \
	rpm \
	rpm2cpio \
	vim \
	wget \
	zlib1g-dev \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
	&& locale-gen en_US.UTF-8 \
	&& update-locale \
    && pip3 install pip --upgrade \
    && pip3 install setuptools --upgrade \
    && pip3 install gunicorn \
    && pip3 install -r /requirements.txt \
    && apt-get purge -y autoconf g++ make python3-dev pkg-config libjpeg-dev \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt-get clean

COPY . /opt/layerindex
RUN rm -rf /opt/layerindex/docker
COPY docker/settings.py /opt/layerindex/settings.py
COPY docker/refreshlayers.sh /opt/refreshlayers.sh
COPY docker/updatelayers.sh /opt/updatelayers.sh
COPY docker/migrate.sh /opt/migrate.sh
COPY docker/connectivity_check.sh /opt/connectivity_check.sh

RUN mkdir /opt/workdir \
	&& adduser --system --uid=500 layers \
	&& chown -R layers /opt/workdir
USER layers

# Always copy in .gitconfig and proxy helper script (they need editing to be active)
COPY docker/.gitconfig /home/layers/.gitconfig
COPY docker/git-proxy /opt/bin/git-proxy

# Start Gunicorn
CMD ["/usr/local/bin/gunicorn", "wsgi:application", "--workers=4", "--bind=:5000", "--timeout=60", "--log-level=debug", "--chdir=/opt/layerindex"]
