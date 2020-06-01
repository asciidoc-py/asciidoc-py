#!/usr/bin/env bash

# layout1  -  Tables based layout.
# layout2  -  CSS based layout
LAYOUT=layout2

ASCIIDOCVERSION=$(sed -n '1p' configure.ac | grep -o -e "[0-9]*\.[0-9]*\.[a-z0-9]*")
# trying to embed this string with spaces into the command below causes
# sys.argv to get funny, and I cannot figure out why
ASCIIDOCDATE=$(sed -n '3p' configure.ac | grep -o -e "[0-9]* [A-Z][a-z]* [0-9]*")

# execute this as a function so that we do not run afoul of bash's string interpolation / splitting
# when trying to execute commands from variables
asciidoc() {
    python3 ../asciidoc.py -a revnumber="${ASCIIDOCVERSION}" -a revdate="${ASCIIDOCDATE}" "$@"
}

A2X="python3 ../a2x.py"

# Step 0: Initialize the gh-pages folder
if [ ! -d gh-pages ]; then
    git clone https://github.com/asciidoc/asciidoc-py3 gh-pages
    pushd gh-pages
    git checkout gh-pages
    popd
fi
pushd gh-pages
find . -maxdepth 1 -type f -not \( -name '*.md' -o -name '*.md5' -o -name '*.epub' -o -name 'CNAME' -o -name '.nojekyll' \) -exec rm -rf {} \;
rm -rf chunked
rm -rf images
popd


# Step 1: Conslidate all files into the gh-pages directory
files=(
    docbook-xsl/asciidoc-docbook-xsl.txt
    filters/graphviz/asciidoc-graphviz-sample.txt
    stylesheets/asciidoc.css
    javascripts/asciidoc.js
    javascripts/ASCIIMathML.js
    CHANGELOG.txt
    INSTALL.txt
    javascripts/LaTeXMathML.js
    stylesheets/xhtml11-quirks.css
)

for file in ${files[@]}; do
    name=$(basename ${file})
    set -x
    cp ${file} gh-pages/${name}
    set +x
done

set -x
cp README.asciidoc gh-pages/README.txt
cp website/* gh-pages
cp doc/*.txt gh-pages
cp -R images gh-pages

cp doc/asciidoc.1.txt gh-pages/manpage.txt
cp doc/asciidoc.txt gh-pages/userguide.txt
set +x

pushd gh-pages

# Step 2: Build the files
ASCIIDOC="asciidoc -b xhtml11 -f ${LAYOUT}.conf -a icons -a badges -a max-width=70em -a source-highlighter=highlight"
for file in *.txt; do
    name=${file:0:-4}
    opts=""
    if [ "${name}" = "userguide" ] || [ "${name}" = "faq" ]; then
        opts="-a toc -a numbered"
    elif [ "${name}" = "index" ]; then
        opts="-a index-only"
    elif [ "${name}" = "manpage" ] || [ "${name}" = "a2x.1" ] || [ "${name}" = "asciidoc.1" ]; then
        opts="-d manpage"
    elif [ "${name}" = "asciimathml" ]; then
        opts="-a asciimath"
    elif [ "${name}" = "latexmath" ]; then
        opts="-a latexmath"
    fi
    if [ "${name}" = "index" ] || [ "${name}" = "INSTALL" ] || [ "${name}" = "asciidocapi" ] || [ "${name}" = "testasciidoc" ] || [ "${name}" = "publishing-ebooks-with-asciidoc" ]; then
        opts+=" -a toc -a toclevels=1"
    fi
    set -x
    ${ASCIIDOC} ${opts} ${file}
    set +x
done

# Step 3: build out remaining specific files from doc
ASCIIDOC="asciidoc"
# TODO: investigate epub generation (--epubcheck fails)
set -x
${ASCIIDOC} -a data-uri -a icons -a toc -a max-width=55em -o article-standalone.html article.txt
${ASCIIDOC} -b html5 -a icons -a toc2 -a theme=flask -o article-html5-toc2.html article.txt

${ASCIIDOC} -d manpage -b html4 asciidoc.1.txt
${ASCIIDOC} -b xhtml11 -d manpage -o asciidoc.1.css-embedded.html asciidoc.1.txt
${ASCIIDOC} -d manpage -b docbook asciidoc.1.txt
xsltproc --nonet ../docbook-xsl/manpage.xsl asciidoc.1.xml
rm asciidoc.1.xml

${ASCIIDOC} -b xhtml11 -n -a toc -a toclevels=2 -o asciidoc.css-embedded.html asciidoc.txt
${A2X} -f epub -d book --epubcheck --icons asciidoc.txt
${A2X} -f chunked -dbook --icons -D ./ asciidoc.txt
mv asciidoc.chunked chunked

${A2X} -f epub -d book --epubcheck --icons book.txt

${ASCIIDOC} -n -b docbook article.txt
xsltproc --nonet --stringparam admon.textlabel 0 ../docbook-xsl/fo.xsl article.xml > article.fo
fop article.fo article.pdf
set +x
rm article.xml
rm article.fo

set -x
${ASCIIDOC} -b docbook asciidoc.txt
dblatex -p ../dblatex/asciidoc-dblatex.xsl -s ../dblatex/asciidoc-dblatex.sty -o asciidoc.pdf asciidoc.xml
set +x
rm asciidoc.xml

popd
