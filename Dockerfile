FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3 autoconf make wget unzip libxml2-utils xsltproc && \
    apt-get install -y dvipng graphviz imagemagick lilypond source-highlight texlive-latex-base

RUN wget http://www.docbook.org/xml/4.5/docbook-xml-4.5.zip -O /tmp/docbook-xml-4.5.zip && \
    unzip /tmp/docbook-xml-4.5.zip -d /tmp/docbook-xml-4.5

RUN cd /tmp/docbook-xml-4.5 && \
    install -v -d -m755 /usr/share/xml/docbook/xml-dtd-4.5 && \
    install -v -d -m755 /etc/xml && \
    chown -R root:root . && \
    cp -v -af docbook.cat *.dtd ent/ *.mod /usr/share/xml/docbook/xml-dtd-4.5

RUN if [ ! -e /etc/xml/docbook ]; then \
        xmlcatalog --noout --create /etc/xml/docbook; \
    fi

RUN xmlcatalog --noout --add "public" \
        "-//OASIS//DTD DocBook XML V4.5//EN" \
        "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" \
        /etc/xml/docbook && \
    xmlcatalog --noout --add "public" \
        "-//OASIS//DTD DocBook XML CALS Table Model V4.5//EN" \
        "file:///usr/share/xml/docbook/xml-dtd-4.5/calstblx.dtd" \
        /etc/xml/docbook && \
    xmlcatalog --noout --add "public" \
        "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
        "file:///usr/share/xml/docbook/xml-dtd-4.5/soextblx.dtd" \
        /etc/xml/docbook && \
    xmlcatalog --noout --add "public" \
        "-//OASIS//ELEMENTS DocBook XML Information Pool V4.5//EN" \
        "file:///usr/share/xml/docbook/xml-dtd-4.5/dbpoolx.mod" \
        /etc/xml/docbook && \
    xmlcatalog --noout --add "public" \
        "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.5//EN" \
        "file:///usr/share/xml/docbook/xml-dtd-4.5/dbhierx.mod" \
        /etc/xml/docbook && \
    xmlcatalog --noout --add "public" \
        "-//OASIS//ELEMENTS DocBook XML HTML Tables V4.5//EN" \
        "file:///usr/share/xml/docbook/xml-dtd-4.5/htmltblx.mod" \
        /etc/xml/docbook && \
    xmlcatalog --noout --add "public" \
        "-//OASIS//ENTITIES DocBook XML Notations V4.5//EN" \
        "file:///usr/share/xml/docbook/xml-dtd-4.5/dbnotnx.mod" \
        /etc/xml/docbook && \
    xmlcatalog --noout --add "public" \
        "-//OASIS//ENTITIES DocBook XML Character Entities V4.5//EN" \
        "file:///usr/share/xml/docbook/xml-dtd-4.5/dbcentx.mod" \
        /etc/xml/docbook && \
    xmlcatalog --noout --add "public" \
        "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.5//EN" \
        "file:///usr/share/xml/docbook/xml-dtd-4.5/dbgenent.mod" \
        /etc/xml/docbook && \
    xmlcatalog --noout --add "rewriteSystem" \
        "http://www.oasis-open.org/docbook/xml/4.5" \
        "file:///usr/share/xml/docbook/xml-dtd-4.5" \
        /etc/xml/docbook && \
    xmlcatalog --noout --add "rewriteURI" \
        "http://www.oasis-open.org/docbook/xml/4.5" \
        "file:///usr/share/xml/docbook/xml-dtd-4.5" \
        /etc/xml/docbook

RUN if [ ! -e /etc/xml/catalog ]; then \
        xmlcatalog --noout --create /etc/xml/catalog; \
    fi

RUN xmlcatalog --noout --add "delegatePublic" \
        "-//OASIS//ENTITIES DocBook XML" \
        "file:///etc/xml/docbook" \
        /etc/xml/catalog && \
    xmlcatalog --noout --add "delegatePublic" \
        "-//OASIS//DTD DocBook XML" \
        "file:///etc/xml/docbook" \
        /etc/xml/catalog && \
    xmlcatalog --noout --add "delegateSystem" \
        "http://www.oasis-open.org/docbook/" \
        "file:///etc/xml/docbook" \
        /etc/xml/catalog && \
    xmlcatalog --noout --add "delegateURI" \
        "http://www.oasis-open.org/docbook/" \
        "file:///etc/xml/docbook" \
        /etc/xml/catalog
