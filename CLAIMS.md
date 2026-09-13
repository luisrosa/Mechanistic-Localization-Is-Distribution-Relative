# Claim Ledger

This file records the public theorem regime of *Mechanistic Localization Is Distribution-Relative*. It is intentionally stricter than the README: the README tells the argument as a story; this file fixes the assumptions under which each claim is made.

## Core declarations

1. A mechanistic-localization problem is relative to a realized probability state `μ`, receiver family `Q`, phenomenon `Φ`, admissible decoder class `H`, action space, and loss `ℓ`.
2. A receiver set `K`, a receiver-level presentation `(K,h)`, and the realized action `[hQ_K]_μ` are distinct mathematical objects.
3. The receiver map determines what information is exposed. The decoder class determines which functions of that exposed state are admissible downstream uses.
4. The maximal measurable decoder class isolates receiver sufficiency. Architecture-specific localization is obtained by restricting the decoder class; the paper does not identify the maximal class with the computation implemented by an arbitrary concrete neural continuation.

## Realized process

5. The ambient network is deterministic in the main process model. A source law is transported through the fixed network by pushforward to produce a state-decorated realized process.
6. An internal intervention may instead provide a new law at a represented cut; once that boundary law is fixed, the same downstream receiver analysis applies to the rebased suffix. The paper does not formalize every possible intervention protocol as part of one universal process object.
7. Source laws in the same measure class remain in the same measure class after deterministic pushforward.

## Receiver Bayes risk and refinement

8. Receiver Bayes risk is

   `δ_{μ,H}(K) = inf_{h in H_K} E_μ[ℓ(Φ(X), h(Q_K(X)))]`.

9. In the maximal receiver-sufficiency problem, `H_K` is the set of measurable decoders from the receiver state to the action space.
10. Passive receiver refinement means that `K'` exposes extra receiver coordinates from the same realized computation and the smaller state is recovered by coordinate projection.
11. Under passive refinement, `K ⊆ K'` implies `δ_μ(K') ≤ δ_μ(K)`.
12. The same monotonicity holds for restricted decoder families when they are closed under ignoring newly exposed coordinates.
13. Structural inclusion of ablation, patching, retention, or rerun sets does not by itself imply Blackwell refinement, because those protocols may change the state entering the continuation.
14. For losses taking values in `[0,1]`, the full maximal receiver-risk profile is 1-Lipschitz in total variation:

   `sup_K |δ_μ(K)-δ_ν(K)| ≤ d_TV(μ,ν)`.

15. Optimizer identity and a thresholded reported circuit family may nevertheless change discontinuously at a decision boundary.

## Context-invariant realization

16. For a finite mixture of contexts with positive weights, context value is the excess Bayes risk incurred when the context label is hidden and one decoder must serve the pooled law.
17. When the relevant minima are attained, zero context value is equivalent to the existence of a decoder that is optimal in every context.
18. Under log loss with finite target/context variables and finite displayed information quantities,

   `Γ_K^log = I(Y_Φ; C | Q_K(X))`.

19. Adding receiver `j` changes the log-loss context value by

   `I(Y_Φ; Q_j | Q_K,C) - I(Y_Φ; Q_j | Q_K)`.

20. The increment can be positive or negative. Receiver refinement therefore orders predictive adequacy but does not generally order context invariance.

## Exact support shadow

21. Almost-sure exact localization depends only on measure class.
22. In finite 0-1 problems, zero receiver Bayes risk depends only on support.
23. On finite support `S`, exact realization through `Q_K` is equivalent to target factorization through the receiver state and to the equivalence-relation condition

   `Eq(Q_K|_S) ⊆ Eq(Φ|_S)`.

24. The same finite exact problem has an equivalent hitting-set representation: a receiver family realizes the phenomenon exactly iff it separates every support-state pair that the phenomenon distinguishes.
25. The resulting exact finite structure coincides with classical functional-dependency / decision-reduct / transversal structure in the stated correspondence.
26. Support restriction is antitone for exact realization: if `S ⊆ T`, then every exact receiver family valid on `T` remains valid on `S`.
27. Inclusion-minimal exact localization families can contain multiple incomparable members; minimality alone does not provide a unique circuit.

## Fixed-network universality

28. Fix the Boolean OR network on `{0,1}^J`, fixed coordinate receivers, and the OR target.
29. For every nonempty upward-closed family `F ⊆ 2^J`, there exists a support of this one fixed network whose maximal exact receiver-sufficiency family is exactly `F`.
30. Consequently every nonempty antichain occurs as the inclusion-minimal exact localization family for some support of the same fixed network.
31. This theorem is about the maximal receiver-sufficiency layer. A restricted decoder class may impose additional architecture-specific implementation constraints after the receiver state has been exposed.

## Exact context compatibility

32. When each context separately admits an exact decoder through one fixed access, a global exact decoder exists on the union exactly when the context-local decoders agree on every overlap of their receiver images.
33. The relevant overlap is created after the access map: `Q_K(S_i) ∩ Q_K(S_j)`, which may be larger than the image of the source-context intersection when access is noninjective.
34. In the finite zero-loss setting, this exact descent condition is the local-to-global endpoint of the context-value problem.

## Explicit nonclaims

The paper does **not** claim that receiver-level sufficiency is equivalent to any of the following without additional structure:

- causal necessity;
- causal sufficiency under arbitrary interventions;
- a unique mechanistic circuit;
- algorithmic abstraction;
- human interpretability;
- representation identity across reparameterizations or networks;
- equivalence of different mediator vocabularies;
- a guarantee that an arbitrary measurable decoder is implemented by the network's actual continuation.

The paper also does not claim that every mechanistic-interpretability method should be reformulated in this notation. The formalism isolates one precise problem: what a declared receiver interface makes realizable under a declared probability state, decoder class, phenomenon, and adequacy criterion.
