# Validation Record

The public artifact preserves four checks: mathematical regression, manuscript compilation, package independence, and release provenance.

The finite regression suite checks presentation equivalence, zero risk versus support factorization, receiver monotonicity, finite Bayes-risk formulas, TV stability, the common-optimum criterion, both signs of the log-loss receiver increment, the same-support/opposite-rule example, hitting-set exact localization, fixed-OR universality on small systems, and exact descent.

`make packages` constructs two standalone directories from the canonical source: identified `arxiv/` and anonymous `iclr2027/`. ZIPs are generated directly from those directories. `make verify` checks required files, rejects references back to the private development repository, and compares ZIP manifests to their source directories.

CI runs the finite checks, regenerates both packages, compiles both variants, rejects unresolved citations/references, verifies the ICLR page gate, and refreshes the root identified PDF and submission ZIPs on `main`.

The regression suite is not a proof assistant or a substitute for peer review. General claims remain mathematical proofs in the manuscript.
