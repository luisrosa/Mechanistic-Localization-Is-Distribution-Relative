# Mechanistic Localization Is Distribution-Relative

**Receiver sufficiency, context invariance, and the support shadow**  
Luis F. Rosario Freytes — University of Michigan

This repository is the public research artifact for the current paper. It is designed to do four things at once: explain the argument to a human reader, provide the paper in one click, expose the exact theorem regime and validation record, and preserve the source packages used for arXiv and ICLR 2027.

## Read the paper

- **[Current identified manuscript PDF](mechanistic_localization_is_distribution_relative.pdf)**
- [identified arXiv source package](arxiv/)
- [anonymous ICLR 2027 source package](iclr2027/)
- [submission ZIPs](submission-zips/)
- [claim ledger](CLAIMS.md)
- [validation record](VALIDATION.md)

## The story

Mechanistic interpretability often asks where a computation is located inside a neural network. A common answer is a component set: a collection of neurons, heads, features, edges, or other internal variables that suffices for some phenomenon.

The paper asks what has to be fixed before that statement has a definite meaning.

Suppose the network is fixed. Fix the receiver being read, the target phenomenon, and even the literal set of possible states. Is the receiver-level realization now fixed?

No.

### Same support, opposite optimal rule

Let

```math
X=\{0,1\}^2,\qquad \Phi(x_1,x_2)=x_1,\qquad Q_2(x_1,x_2)=x_2.
```

For `0 < eta < 1/2`, put most probability mass on the diagonal states `00,11`. Through receiver `Q_2`, the Bayes-optimal 0-1 rule is then

```math
h_{\mu_\eta}(z)=z.
```

Reverse the diagonal and off-diagonal weights while leaving the support equal to all of `X`. The Bayes-optimal rule through the same receiver becomes

```math
h_{\nu_\eta}(z)=1-z.
```

Nothing about the network, target, receiver, or literal support changed. Only the probability weights changed. Passing from a realized probability law to its support therefore discards exactly the information that selected the receiver-level rule.

That forces a distinction between three objects:

```math
K\longrightarrow (K,h)\longrightarrow [hQ_K]_\mu.
```

They record, respectively,

```text
where the analysis reads
→ how the exposed state is used
→ what action is induced on the realized population.
```

A component set is therefore not a complete localization specification.

## What has to be declared

The paper treats a mechanistic-localization claim as relative to a realized probability state, a receiver interface, an admissible downstream-use class, a target phenomenon, and an adequacy criterion:

```text
realized state μ
+ receiver access Q
+ admissible decoder class H
+ phenomenon Φ
+ loss / adequacy criterion ℓ
(+ threshold ε when a discrete circuit family is reported)
-----------------------------------------------------------
mechanistic-localization claim
```

The receiver map says what internal state is exposed. The decoder class says what may be done with that state. The maximal measurable decoder class isolates receiver sufficiency itself; restricting that class specializes the construction to a concrete downstream architecture or continuation protocol.

## Two laws separate

Once the objects are separated, passive receiver refinement has a clean monotonicity law. If `K ⊆ K'`, the larger receiver state can ignore its extra coordinates and reproduce every rule available through the smaller one, so

```math
\delta_\mu(K')\le \delta_\mu(K).
```

More exposed receiver information cannot worsen optimal predictive adequacy.

Context invariance behaves differently. Let `C` index contexts and let `Gamma_K` be the excess Bayes risk incurred when one decoder must serve the pooled population instead of allowing a context-specific optimum. Under log loss,

```math
\Gamma_K^{\log}=I(Y_\Phi;C\mid Q_K(X)).
```

Adding receiver `j` changes this quantity by

```math
I(Y_\Phi;Q_j\mid Q_K,C)-I(Y_\Phi;Q_j\mid Q_K).
```

Either sign occurs. More receiver information can make one common rule easier to sustain across distributions or harder to sustain.

So the same refinement order produces two different behaviors:

```text
predictive adequacy: monotone under passive receiver refinement
context invariance: no general monotonicity law
```

## The support shadow

Exact zero-loss localization is a coarser problem. Almost-sure exact realization forgets probability weights inside a measure class; in finite discrete settings that coarse-graining reduces to support.

```math
\text{probability state}
\longrightarrow
\text{measure class}
\longrightarrow
\text{support}
\longrightarrow
\text{functional dependency / reduct structure}.
```

For finite 0-1 problems,

```math
\delta_\mu(K)=0
\iff
\Phi|_S\text{ factors through }Q_K|_S
\iff
\operatorname{Eq}(Q_K|_S)\subseteq\operatorname{Eq}(\Phi|_S).
```

Equivalently, the selected receivers must hit every target-relevant state pair that needs to be distinguished. This is the exact support shadow of the distribution-relative problem.

This also explains the relation to the earlier support-relative project: support-relative localization is not discarded here; it appears as the zero-loss coarse-graining of the richer distributional theory. The earlier public artifact is preserved separately at [mechanistic-localization-is-support-relative](https://github.com/luisrosa/mechanistic-localization-is-support-relative).

## Fixing the network still does not fix the exact circuit

The final structural result freezes the architecture, target, and receiver granularity and varies support alone.

Consider one Boolean OR network

```math
\{0,1\}^J\xrightarrow{\mathrm{id}}\{0,1\}^J\xrightarrow{\mathrm{OR}}\{0,1\}
```

with fixed coordinate receivers. Every nonempty upward-closed exact localization family can be realized in this one network by choosing an appropriate support.

Upward closure is the constraint already forced by passive receiver inclusion. Within that constraint, support variation alone exhausts the admissible exact-localization families. Architecture therefore does not select a canonical exact circuit at the receiver-sufficiency level.

## What different experimental choices change

| Experimental choice | Formal argument | What may change |
| --- | --- | --- |
| input / prompt distribution | `μ` | optimal rule, receiver risk, context value, selected circuit |
| mediator / representation granularity | `Q` | the localization problem itself |
| downstream architecture or continuation class | `H` | realizable receiver-level rules and optimal risk |
| target behavior | `Φ` | which distinctions receivers must preserve |
| adequacy criterion | `ℓ` | optimal action and receiver risk |
| selection threshold | `ε` | reported discrete circuit family |
| passive receiver set | `K` | predictive risk, monotonically under refinement |
| ablation / patch / rerun protocol | realized process | the induced experiment; passive Blackwell order need not apply |

This is the practical reading of the theory: two papers that report different component subsets may have changed different arguments of the mechanistic claim, while two papers that report the same subset may still realize different receiver-level rules on different populations.

## Repository organization

```text
source/             canonical scientific source and the two wrappers
arxiv/              standalone identified source package
iclr2027/           standalone anonymous ICLR 2027 package
submission-zips/    upload-ready ZIPs generated from those directories
scripts/            finite checks and package verification
releases/           frozen release provenance
```

The two submission directories are intentionally standalone. Each can be copied out of the repository, compiled independently, and zipped without depending on the other package or on the private development repository.

### Rebuild everything

```bash
make all
```

The release pipeline runs the finite regression suite, constructs both submission directories and ZIPs, compiles both manuscript variants, verifies the package manifests and anonymity/identity invariants, and builds the stable identified PDF at repository root.

For the exact theorem regime and explicit nonclaims, see [`CLAIMS.md`](CLAIMS.md). For what was checked computationally and what remains a mathematical proof in the manuscript, see [`VALIDATION.md`](VALIDATION.md).
