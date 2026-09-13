# Mechanistic Localization Is Distribution-Relative

**Receiver Sufficiency, Context Invariance, and the Support Shadow**  
Luis F. Rosario Freytes — University of Michigan

**[Read the paper](mechanistic_localization_is_distribution_relative.pdf)** · **[LaTeX source](source/)**

Mechanistic interpretability often talks as if a circuit were a property of the network alone: find the right heads, neurons, features, or edges and you have found where the mechanism is.

This paper asks a more basic question. Suppose the network is fixed. Suppose the receiver, target phenomenon, and even the literal support of the inputs are fixed. Is the receiver-level mechanism now fixed?

No.

## Same network, same support, different rule

Take

$$
X=\{0,1\}^2,\qquad \Phi(x_1,x_2)=x_1,\qquad Q_2(x_1,x_2)=x_2.
$$

Put most probability mass on the diagonal states `00,11`. Through the receiver $Q_2$, the Bayes-optimal rule is

$$
h_\mu(z)=z.
$$

Now reverse the diagonal and off-diagonal weights while keeping the support equal to all of $X$. The optimal rule through the **same receiver in the same network** becomes

$$
h_\nu(z)=1-z.
$$

Nothing structural changed. Only the realized probability law changed.

That is the central point of the paper: a component set does not by itself determine the rule realized through the state it exposes. The localization problem has to distinguish

$$
K\longrightarrow (K,h)\longrightarrow [hQ_K]_\mu,
$$

where $K$ says where we read, $(K,h)$ says how the exposed state is used, and $[hQ_K]_\mu$ is the action actually induced on the realized population.

## Two different questions appear

Once those objects are separated, two things that look similar at first behave very differently.

For **predictive adequacy**, more passive receiver access can only help. If $K\subseteq K'$, the larger receiver can always ignore its extra coordinates, so

$$
\delta_\mu(K')\le \delta_\mu(K).
$$

For **context invariance**, there is no corresponding monotonicity law. Under log loss, the value of revealing context is

$$
\Gamma_K^{\log}=I(Y_\Phi;C\mid Q_K(X)),
$$

and adding one receiver changes it by

$$
I(Y_\Phi;Q_j\mid Q_K,C)-I(Y_\Phi;Q_j\mid Q_K).
$$

That quantity can be positive or negative. More internal information can make one rule easier to reuse across contexts or harder to reuse.

So “this receiver predicts the phenomenon” and “this receiver supports the same mechanism across distributions” are different claims.

## Why support still shows up

The earlier support-relative picture is not thrown away. It appears as the exact, zero-loss shadow of the richer distribution-relative problem.

In finite $0$–$1$ settings,

$$
\delta_\mu(K)=0
\iff
\Phi|_S\text{ factors through }Q_K|_S
\iff
\mathrm{Eq}(Q_K|_S)\subseteq\mathrm{Eq}(\Phi|_S).
$$

At zero loss, probability weights disappear and the problem collapses to which target-relevant distinctions survive on the support. That is where the functional-dependency and hitting-set structure comes from.

The paper calls this the **support shadow**: exact localization is a coarse-graining of the distribution-relative problem, not a competing theory.

## One fixed network can realize every admissible exact localization family

The strongest structural example fixes a Boolean OR network and its coordinate receivers. By varying support alone, that one network realizes every nonempty upward-closed exact localization family.

So even at the exact support level, fixing the architecture does not select one canonical circuit. The realized population is part of the localization claim.

## What is in this repository

The maintained manuscript is in [`source/`](source/). The small finite checks used while developing the examples are in [`scripts/check_examples.py`](scripts/check_examples.py).

The standalone identified preprint package is tracked in [`arxiv/`](arxiv/), and the anonymous ICLR 2027 package is tracked in [`iclr2027/`](iclr2027/). The exact anonymous upload ZIP is preserved at [`submission-zips/mldr_iclr2027.zip`](submission-zips/mldr_iclr2027.zip). The package script can regenerate both submission ZIPs from the maintained scientific source.

To build the identified paper:

```bash
make paper
```

To run the finite checks:

```bash
make check
```

## Citation

```bibtex
@article{rosariofreytes2026mechanistic,
  title  = {Mechanistic Localization Is Distribution-Relative: Receiver Sufficiency, Context Invariance, and the Support Shadow},
  author = {Rosario Freytes, Luis F.},
  year   = {2026}
}
```

Citation metadata are also available in [`CITATION.cff`](CITATION.cff).
