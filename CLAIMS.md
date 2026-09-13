# Claim Ledger

This file records the manuscript's public theorem regime.

1. Localization is relative to a realized probability state `μ`, receiver family `Q`, phenomenon `Φ`, decoder class `H`, and loss `ℓ`.
2. `K`, `(K,h)`, and `[hQ_K]_μ` are distinct: location, receiver-level presentation, and realized action.
3. The maximal measurable decoder class isolates receiver sufficiency; architecture-specific localization restricts that class.
4. Passive receiver refinement is monotone: `K ⊆ K'` implies `δ_μ(K') ≤ δ_μ(K)`.
5. For loss in `[0,1]`, the receiver-risk profile is 1-Lipschitz in total variation.
6. Under log loss, `Γ_K = I(Y_Φ;C | Q_K(X))`.
7. Adding receiver `j` changes context value by `I(Y_Φ;Q_j | Q_K,C) - I(Y_Φ;Q_j | Q_K)`; either sign occurs.
8. Almost-sure exact localization depends only on measure class.
9. In finite 0–1 problems, zero risk depends only on support and is equivalent to factorization through the receiver state.
10. The finite exact problem has an equivalent hitting-set / decision-reduct form.
11. Support restriction can enlarge the exact realization family.
12. One fixed Boolean OR network with fixed coordinate receivers and fixed OR target realizes every nonempty upward-closed exact localization family by support variation alone.

The paper keeps receiver sufficiency separate from stronger notions of causal, algorithmic, representational, or cross-network mechanism identity.
