FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 dvipng graphviz imagemagick lilypond source-highlight texlive-latex-base