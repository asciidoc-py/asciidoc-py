FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3 autoconf make wget unzip libxml2-utils xsltproc && \
    apt-get install -y dvipng graphviz imagemagick lilypond source-highlight texlive-latex-base docbook-xsl

COPY . "/srv/asciidoc"
WORKDIR "/srv/asciidoc"
