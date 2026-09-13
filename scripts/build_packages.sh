#!/usr/bin/env bash
set -euo pipefail
rm -rf arxiv iclr2027 submission-zips .build/iclr-style
mkdir -p arxiv iclr2027 submission-zips .build/iclr-style
cp -R source/sections source/appendices arxiv/
cp source/references.bib source/arxiv_main.tex arxiv/
mv arxiv/arxiv_main.tex arxiv/main.tex
cp source/package.mk arxiv/Makefile
cp -R source/sections source/appendices iclr2027/
cp source/references.bib source/iclr_main.tex iclr2027/
mv iclr2027/iclr_main.tex iclr2027/main.tex
cp source/package.mk iclr2027/Makefile
curl -fsSL https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip -o .build/iclr-style.zip
unzip -q .build/iclr-style.zip -d .build/iclr-style
find .build/iclr-style -name iclr2027_conference.sty -exec cp {} iclr2027/ \;
find .build/iclr-style -name iclr2027_conference.bst -exec cp {} iclr2027/ \;
printf '# arXiv package\n\nIdentified standalone source package.\n' > arxiv/README.md
printf '# ICLR 2027 package\n\nAnonymous standalone source package.\n' > iclr2027/README.md
(cd arxiv && zip -qr ../submission-zips/mldr_arxiv.zip . -x 'main.pdf')
(cd iclr2027 && zip -qr ../submission-zips/mldr_iclr2027.zip . -x 'main.pdf')
echo 'submission packages: BUILT'
