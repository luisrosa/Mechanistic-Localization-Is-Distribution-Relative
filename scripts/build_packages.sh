#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

rm -rf arxiv iclr2027 submission-zips .build/iclr-style .build/iclr-style.zip
mkdir -p arxiv iclr2027 submission-zips .build/iclr-style

cp -R source/sections source/appendices arxiv/
cp source/references.bib source/arxiv_main.tex arxiv/
mv arxiv/arxiv_main.tex arxiv/main.tex
cp source/package.mk arxiv/Makefile

cp -R source/sections source/appendices iclr2027/
cp source/references.bib source/iclr_main.tex iclr2027/
mv iclr2027/iclr_main.tex iclr2027/main.tex
cp source/package.mk iclr2027/Makefile

# Both manuscript surfaces use the same typography.  The identified preprint
# removes review-only furniture in its wrapper; the anonymous submission does not.
curl -fsSL https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip -o .build/iclr-style.zip
unzip -q .build/iclr-style.zip -d .build/iclr-style
for dir in arxiv iclr2027; do
  find .build/iclr-style -name iclr2027_conference.sty -exec cp {} "$dir/" \;
  find .build/iclr-style -name iclr2027_conference.bst -exec cp {} "$dir/" \;
  test -s "$dir/iclr2027_conference.sty"
  test -s "$dir/iclr2027_conference.bst"
done

printf '# Identified preprint source\n\nBuild with `make`.\n' > arxiv/README.md
printf '# Anonymous ICLR 2027 source\n\nBuild with `make`.\n' > iclr2027/README.md

(cd arxiv && zip -qr ../submission-zips/mldr_arxiv.zip . -x 'main.pdf')
(cd iclr2027 && zip -qr ../submission-zips/mldr_iclr2027.zip . -x 'main.pdf')

echo 'submission packages: BUILT'
