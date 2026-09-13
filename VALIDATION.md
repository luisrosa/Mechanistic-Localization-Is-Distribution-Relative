# Validation Record

This repository separates three kinds of evidence:

1. mathematical arguments in the manuscript;
2. executable finite regressions for examples and finite structural claims;
3. release engineering checks for the two submission packages and compiled PDFs.

The finite suite is not a proof assistant and does not replace peer review. General theorems remain mathematical proofs in the paper.

## Mathematical regression suite

Run:

```bash
make check
```

The current suite checks finite instances of the following claims and examples:

- state-relative presentation equivalence;
- the same-support / opposite-Bayes-rule construction from the introduction;
- zero receiver Bayes risk versus exact support factorization;
- passive receiver-refinement monotonicity;
- independent finite Bayes-risk formulas;
- total-variation stability, including sharp finite cases;
- mixture concavity and the common-optimum criterion;
- the log-loss context-value identity on finite distributions;
- positive and negative examples for the receiver-increment formula;
- exact factorization versus the hitting-family characterization;
- double hitting for upward-closed families;
- fixed-OR support universality on small finite receiver sets;
- access-image compatibility / exact descent examples.

The theorem-development pass used an additional adversarial check of the two load-bearing results: the log-loss receiver increment was independently rederived from the two chain-rule decompositions of `I(Y;C,W|Z)`, and fixed-OR universality was exhaustively enumerated for every nonempty upward-closed family through four receivers.

## Manuscript variants

The canonical scientific body lives under `source/`. Two wrappers produce two release surfaces:

- `arxiv/` — identified manuscript source;
- `iclr2027/` — anonymous ICLR 2027 source.

The scientific section files, appendices, and bibliography are copied from one canonical source into both packages during construction. The wrappers differ only where the release surface requires it: author identification, venue style, and associated front matter.

The ICLR main text preserves the five-section theorem spine:

1. Introduction;
2. Realized localization and predictive refinement;
3. Context-invariant realization;
4. Exact support shadow and fixed-network non-canonicity;
5. Implications for mechanistic localization.

The two load-bearing results remain fully stated and proved in the counted main text:

- the log-loss receiver-increment theorem;
- fixed-network support universality for the Boolean OR network.

Blackwell monotonicity, bounded-loss TV stability, the common-optimum criterion, measure-class invariance, and the finite exact-support characterization remain in the main text because they are direct bridges in the argument. Longer categorical bookkeeping, finite selection geometry, blocker details, stronger OR consequences, and access-image descent remain in appendices.

## Package construction

Run:

```bash
make packages
```

This regenerates the standalone `arxiv/` and `iclr2027/` directories and then creates:

```text
submission-zips/mldr_arxiv.zip
submission-zips/mldr_iclr2027.zip
```

The ZIPs are generated directly from the corresponding standalone directories. No submission package is hand-assembled.

## Package verification

Run:

```bash
make verify
```

Verification checks that:

- the required source, bibliography, appendix, and venue files are present;
- the ICLR package is anonymous;
- the arXiv package is identified;
- neither package contains references back to the private development repository;
- the ZIP file manifests match the standalone directories from which they were generated.

The intended release invariant is stronger than ordinary source sharing: either submission directory should remain independently compilable after being copied out of this repository.

## Compilation and page gate

Run:

```bash
make iclr
make arxiv
make pdf
```

The release workflow compiles both variants with `latexmk`, rejects unresolved references and citations, and preflights the resulting PDFs. The ICLR wrapper places a page label immediately after Section 5; CI rejects a build whose counted main text ends after page 9.

The final ICLR edition used to populate this repository was also rendered and inspected page by page during manuscript validation. That pass checked title balance, theorem/equation blocks, the argument table, reference transitions, appendix ordering, theorem labels, mathematical glyphs, clipping, overlap, and whitespace. The inspected final manuscript was 18 pages total with the counted scientific main text within the ICLR limit.

## Root PDF

`mechanistic_localization_is_distribution_relative.pdf` is the stable human-facing identified manuscript path used by external links. `make pdf` rebuilds it from the identified release source.

The purpose of the stable path is practical: application materials and external references can point to one file even when submission packages are regenerated.

## Provenance

`releases/v1.0/` records the first public-artifact release. The release is intended to freeze together:

- the canonical scientific source;
- the identified manuscript PDF;
- the standalone arXiv directory and ZIP;
- the standalone ICLR 2027 directory and ZIP;
- the finite regression suite;
- the claim and validation ledgers.

Scientific changes after a frozen release should produce a new provenance record rather than silently replacing the meaning of the existing release.

## What validation does not establish

Passing the release suite does not establish empirical correctness on a language model, causal necessity of a reported circuit, uniqueness of mechanistic interpretation, or correctness beyond the theorem assumptions recorded in `CLAIMS.md`. Those are separate scientific questions.
