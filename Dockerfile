# You can specify a specific python version to use by doing
# --build-arg PYTHON_VERSION=<version> on the build command,
# This defaults to 3.6 if nothing is given.
ARG PYTHON_VERSION=3.6

# These images are based off Debian Stretch (slim) using https://hub.docker.com/_/python/ as the "base"
FROM python:${PYTHON_VERSION}-stretch

# Install asciidoc dependencies
# install the necessary stuff for asciidoc now that python has been built
RUN echo "deb http://ftp.debian.org/debian stretch-backports main" >> /etc/apt/sources.list && apt-get update && \
    apt-get install -y --no-install-recommends \
        autoconf \
        docbook-xsl \
        dvipng \
        git \
        graphviz \
        imagemagick \
        libxml2-utils \
        make \
        python3 \
        source-highlight \
        time \
        texlive-latex-base \
        unzip \
        xsltproc \
        && \
    apt-get -t stretch-backports install -y --no-install-recommends lilypond && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . "/srv/asciidoc"
WORKDIR "/srv/asciidoc"
