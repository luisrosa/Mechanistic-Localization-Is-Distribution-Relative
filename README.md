# Mechanistic Localization Is Distribution-Relative

**Receiver sufficiency, context invariance, and the support shadow**  
Luis F. Rosario Freytes — University of Michigan

This repository is the public research artifact for the current paper. It contains the identified preprint, the anonymous ICLR 2027 package, submission ZIPs, finite regression checks, and release provenance.

## Read the paper

- [Current identified PDF](mechanistic_localization_is_distribution_relative.pdf)
- [arXiv package](arxiv/)
- [ICLR 2027 package](iclr2027/)
- [submission ZIPs](submission-zips/)
- [claim ledger](CLAIMS.md)
- [validation record](VALIDATION.md)

## The story

A component set does not determine the receiver-level realization by itself. Fix the network, receiver, target, and literal support. Changing only probability weights can still reverse the Bayes-optimal rule through the same receiver.

For the two-bit example

```math
X=\{0,1\}^2,\quad \Phi(x_1,x_2)=x_1,\quad Q_2(x)=x_2,
```

diagonal-heavy and off-diagonal-heavy full-support laws produce opposite optimal rules. Passing from the probability law to its support therefore discards information that selects the receiver-level rule.

The paper separates

```math
K\longrightarrow(K,h)\longrightarrow[hQ_K]_\mu,
```

or: where we read, how the exposed state is used, and what action is induced on the realized population.

Passive receiver refinement orders predictive adequacy:

```math
K\subseteq K'\Longrightarrow\delta_\mu(K')\le\delta_\mu(K).
```

Context invariance does not obey the same order. Under log loss,

```math
\Gamma_K^{\log}=I(Y_\Phi;C\mid Q_K(X)),
```

and adding receiver `j` changes it by

```math
I(Y_\Phi;Q_j\mid Q_K,C)-I(Y_\Phi;Q_j\mid Q_K),
```

which can have either sign.

At zero loss the theory coarse-grains to measure class and, in finite problems, to support. Exact localization becomes factorization / functional-dependency / hitting-set structure. One fixed Boolean OR network with fixed coordinate receivers then realizes every nonempty upward-closed exact localization family by varying support alone.

## Repository layout

- `source/` — canonical manuscript source
- `arxiv/` — standalone identified package
- `iclr2027/` — standalone anonymous package
- `submission-zips/` — upload-ready ZIPs
- `scripts/` — package construction, verification, and finite checks
- `releases/` — frozen provenance records

Run `make all` to rebuild and verify the complete artifact.
