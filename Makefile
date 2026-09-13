.PHONY: all check packages iclr arxiv pdf verify hashes clean

all: check packages iclr arxiv pdf verify hashes

check:
	python3 scripts/check_examples.py

packages:
	bash scripts/build_packages.sh

iclr: packages
	$(MAKE) -C iclr2027

arxiv: packages
	$(MAKE) -C arxiv

pdf: arxiv
	cp arxiv/main.pdf mechanistic_localization_is_distribution_relative.pdf

verify: packages
	python3 scripts/verify_packages.py

hashes: pdf verify
	python3 scripts/write_release_hashes.py

clean:
	rm -rf arxiv iclr2027 submission-zips .build mechanistic_localization_is_distribution_relative.pdf
	rm -f releases/v1.0/SHA256SUMS.txt
