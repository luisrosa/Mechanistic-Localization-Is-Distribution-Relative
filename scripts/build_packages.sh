#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

rm -rf arxiv iclr2027 submission-zips .build/iclr-style .build/iclr-style.zip
mkdir -p arxiv iclr2027 submission-zips .build/iclr-style

# One canonical scientific body is copied into both release surfaces.
cp -R source/sections source/appendices arxiv/
cp source/references.bib source/arxiv_main.tex arxiv/
mv arxiv/arxiv_main.tex arxiv/main.tex
cp source/package.mk arxiv/Makefile

cp -R source/sections source/appendices iclr2027/
cp source/references.bib source/iclr_main.tex iclr2027/
mv iclr2027/iclr_main.tex iclr2027/main.tex
cp source/package.mk iclr2027/Makefile

# Pull the official ICLR 2027 style bundle used by the anonymous submission.
curl -fsSL https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip -o .build/iclr-style.zip
unzip -q .build/iclr-style.zip -d .build/iclr-style
find .build/iclr-style -name iclr2027_conference.sty -exec cp {} iclr2027/ \;
find .build/iclr-style -name iclr2027_conference.bst -exec cp {} iclr2027/ \;
test -s iclr2027/iclr2027_conference.sty
test -s iclr2027/iclr2027_conference.bst

cat > arxiv/README.md <<'EOF'
# arXiv package

Standalone identified source package for *Mechanistic Localization Is Distribution-Relative: Receiver Sufficiency, Context Invariance, and the Support Shadow*.

This directory is generated from the repository's canonical `source/` tree. It contains all scientific section files, appendices, bibliography data, and the identified manuscript wrapper required to compile the preprint independently.

Build with:

```bash
make
```

The corresponding upload archive is `../submission-zips/mldr_arxiv.zip`.
EOF

cat > iclr2027/README.md <<'EOF'
# ICLR 2027 package

Standalone anonymous ICLR 2027 source package for *Mechanistic Localization Is Distribution-Relative: Receiver Sufficiency, Context Invariance, and the Support Shadow*.

This directory is generated from the repository's canonical `source/` tree and includes the official ICLR 2027 style and bibliography files. The wrapper is anonymous; the scientific sections, appendices, and bibliography are synchronized with the identified package.

Build with:

```bash
make
```

The corresponding upload archive is `../submission-zips/mldr_iclr2027.zip`.
EOF

# The upload ZIPs are generated directly from their standalone directories.
# Compiled PDFs are excluded because both arXiv/OpenReview compile the source.
(cd arxiv && zip -qr ../submission-zips/mldr_arxiv.zip . -x 'main.pdf')
(cd iclr2027 && zip -qr ../submission-zips/mldr_iclr2027.zip . -x 'main.pdf')

echo 'submission packages: BUILT'
