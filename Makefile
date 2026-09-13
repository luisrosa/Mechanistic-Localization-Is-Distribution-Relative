.PHONY: all paper check packages iclr arxiv submission verify clean

PDF := mechanistic_localization_is_distribution_relative.pdf

all: paper check

paper: arxiv
	cp arxiv/main.pdf $(PDF)

check:
	python3 scripts/check_examples.py

packages:
	bash scripts/build_packages.sh

iclr: packages
	$(MAKE) -C iclr2027

arxiv: packages
	$(MAKE) -C arxiv

submission: check iclr arxiv verify

verify: packages
	python3 scripts/verify_packages.py

clean:
	rm -rf arxiv iclr2027 submission-zips .build $(PDF)
