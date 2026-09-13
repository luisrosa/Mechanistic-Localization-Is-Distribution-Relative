#!/usr/bin/env python3
"""Adversarial finite regressions for the distribution-relative mechanism draft.

The suite intentionally computes several results in two independent ways. In
particular, optimizer sets are represented on one declared receiver domain,
not on context-specific realized images; otherwise intersections of optimizer
sets are not meaningful.
"""

from collections import Counter
from itertools import combinations, product
from math import log2


def all_subsets(n):
    return {
        frozenset(c)
        for r in range(n + 1)
        for c in combinations(range(n), r)
    }


def minimal_elements(family):
    return {k for k in family if not any(j < k for j in family)}


def is_upward_closed(family, n):
    universe = all_subsets(n)
    return all(not (k <= kp) or kp in family for k in family for kp in universe)


def hitting_family(hypergraph, n):
    universe = all_subsets(n)
    return {k for k in universe if all(k & edge for edge in hypergraph)}


def kernel(domain, fn):
    return {(x, y) for x in domain for y in domain if fn(x) == fn(y)}


def factors_through(domain, access, target):
    return kernel(domain, access) <= kernel(domain, target)


def realizing_families(domain, receivers, target):
    out = set()
    for k in all_subsets(len(receivers)):
        access = lambda x, k=k: tuple(receivers[j](x) for j in sorted(k))
        if factors_through(domain, access, target):
            out.add(k)
    return out


def distinction_hypergraph(domain, receivers, target):
    return {
        frozenset(
            j for j, receiver in enumerate(receivers) if receiver(x) != receiver(y)
        )
        for x in domain
        for y in domain
        if target(x) != target(y)
    }


def support_from_hypergraph(hypergraph, n, with_bit=True):
    if with_bit:
        anchor = ((0,) * n, 0)
        return {anchor} | {
            (tuple(int(j in edge) for j in range(n)), 1) for edge in hypergraph
        }
    anchor = (0,) * n
    return {anchor} | {
        tuple(int(j in edge) for j in range(n)) for edge in hypergraph
    }


def canonical_support_from_upward(family, n, with_bit=True):
    return support_from_hypergraph(hitting_family(family, n), n, with_bit=with_bit)


def tv_distance(mu, nu):
    states = set(mu) | set(nu)
    return 0.5 * sum(abs(mu.get(x, 0.0) - nu.get(x, 0.0)) for x in states)


def access_value(x, receivers, k):
    return tuple(receivers[j](x) for j in sorted(k))


def decoder_risks(mu, receivers, target, k, y_values, declared_domain=None):
    """Enumerate full decision rules on one common declared receiver domain."""
    if declared_domain is None:
        declared_domain = tuple(mu)
    z_values = sorted({access_value(x, receivers, k) for x in declared_domain})
    risks = {}
    for outputs in product(y_values, repeat=len(z_values)):
        decoder = dict(zip(z_values, outputs))
        risk = sum(
            p * (decoder[access_value(x, receivers, k)] != target(x))
            for x, p in mu.items()
        )
        risks[tuple(outputs)] = risk
    return z_values, risks


def defect_and_optimizers(
    mu,
    receivers,
    target,
    k,
    y_values=(0, 1),
    declared_domain=None,
):
    _, risks = decoder_risks(
        mu,
        receivers,
        target,
        k,
        y_values,
        declared_domain=declared_domain,
    )
    optimum = min(risks.values())
    optimizers = {h for h, r in risks.items() if abs(r - optimum) < 1e-12}
    return optimum, optimizers


def bayes_defect(mu, receivers, target, k):
    """Independent cell-majority formula for finite 0-1 Bayes risk."""
    masses = {}
    for x, p in mu.items():
        if p <= 0:
            continue
        z = access_value(x, receivers, k)
        y = target(x)
        masses[(z, y)] = masses.get((z, y), 0.0) + p
    if not masses:
        return 0.0
    z_values = {z for z, _ in masses}
    y_values = {target(x) for x, p in mu.items() if p > 0}
    correct = sum(max(masses.get((z, y), 0.0) for y in y_values) for z in z_values)
    return 1.0 - correct


def g3_deletion_error(domain, receivers, target, k):
    """Minimum fraction of rows deleted to make the empirical FD exact."""
    groups = {}
    for x in domain:
        z = access_value(x, receivers, k)
        groups.setdefault(z, []).append(target(x))
    kept = sum(max(Counter(values).values()) for values in groups.values())
    return 1.0 - kept / len(domain)


def conditional_entropy(mu, target, condition):
    joint = {}
    cond_mass = {}
    for x, p in mu.items():
        if p <= 0:
            continue
        y = target(x)
        z = condition(x)
        joint[(z, y)] = joint.get((z, y), 0.0) + p
        cond_mass[z] = cond_mass.get(z, 0.0) + p
    out = 0.0
    for (z, _y), p in joint.items():
        out -= p * log2(p / cond_mass[z])
    return out


def conditional_mutual_information(mu, y_fn, c_fn, z_fn):
    return conditional_entropy(mu, y_fn, z_fn) - conditional_entropy(
        mu, y_fn, lambda x: (z_fn(x), c_fn(x))
    )


def conditional_information_of_added_receiver(mu, y_fn, c_fn, z_fn, w_fn):
    i_y_w_given_zc = conditional_entropy(
        mu, y_fn, lambda x: (z_fn(x), c_fn(x))
    ) - conditional_entropy(
        mu, y_fn, lambda x: (z_fn(x), c_fn(x), w_fn(x))
    )
    i_y_w_given_z = conditional_entropy(mu, y_fn, z_fn) - conditional_entropy(
        mu, y_fn, lambda x: (z_fn(x), w_fn(x))
    )
    return i_y_w_given_zc - i_y_w_given_z


def mix(mu, nu, lam):
    states = set(mu) | set(nu)
    return {
        x: lam * mu.get(x, 0.0) + (1.0 - lam) * nu.get(x, 0.0)
        for x in states
    }


def equivalent_actions(mu, f, g):
    return all(p <= 0 or f(x) == g(x) for x, p in mu.items())


def rational_simplex(states, denominator):
    n = len(states)

    def comps(total, slots):
        if slots == 1:
            yield (total,)
            return
        for first in range(total + 1):
            for rest in comps(total - first, slots - 1):
                yield (first,) + rest

    for counts in comps(denominator, n):
        yield {x: c / denominator for x, c in zip(states, counts)}


def test_state_relative_presentation_equivalence():
    mu = {0: 0.4, 1: 0.6}
    nu = {0: 0.8, 1: 0.2}
    q1 = lambda x: x
    q2 = lambda x: 1 - x
    h1 = lambda z: z
    h2 = lambda z: 1 - z
    f = lambda x: h1(q1(x))
    g = lambda x: h2(q2(x))
    assert equivalent_actions(mu, f, g)
    assert equivalent_actions(nu, f, g)
    flip = lambda x: 1 - h1(q1(x))
    assert not equivalent_actions(mu, f, flip)

    states = list(product([0, 1], repeat=2))
    coarse = lambda x: x[0]
    refined = lambda x: (x[0], x[1])
    h_coarse = lambda z: z
    h_refined = lambda z: z[0]
    full = {x: 1.0 / len(states) for x in states}
    assert equivalent_actions(full, lambda x: h_coarse(coarse(x)), lambda x: h_refined(refined(x)))

    mu0 = {0: 1.0, 1: 0.0}
    mu1 = {0: 0.0, 1: 1.0}
    mixed = mix(mu0, mu1, 0.5)
    same = lambda x: x
    assert equivalent_actions(mu0, same, same)
    assert equivalent_actions(mu1, same, same)
    assert equivalent_actions(mixed, same, same)
    disagree_at_one = lambda x: 0
    assert equivalent_actions(mu0, same, disagree_at_one)
    assert not equivalent_actions(mu1, same, disagree_at_one)
    assert not equivalent_actions(mixed, same, disagree_at_one)


def test_zero_defect_equals_support_factorization():
    states = list(product([0, 1], repeat=2))
    receivers = [lambda x: x[0], lambda x: x[1]]
    target = lambda x: x[0] ^ x[1]
    for mu in rational_simplex(states, 3):
        support = [x for x, p in mu.items() if p > 0]
        if not support:
            continue
        for k in all_subsets(2):
            defect, _ = defect_and_optimizers(mu, receivers, target, k, declared_domain=states)
            access = lambda x, k=k: access_value(x, receivers, k)
            assert (abs(defect) < 1e-12) == factors_through(support, access, target)


def test_receiver_monotonicity_and_bayes_formula():
    states = list(product([0, 1], repeat=2))
    receivers = [lambda x: x[0], lambda x: x[1]]
    target = lambda x: x[0] ^ x[1]
    for mu in rational_simplex(states, 4):
        defects = {}
        for k in all_subsets(2):
            d, _ = defect_and_optimizers(mu, receivers, target, k, declared_domain=states)
            defects[k] = d
            assert abs(d - bayes_defect(mu, receivers, target, k)) < 1e-12
        for k in defects:
            for kp in defects:
                if k <= kp:
                    assert defects[kp] <= defects[k] + 1e-12


def test_tv_nonexpansiveness_exhaustively_and_sharpness():
    states = list(product([0, 1], repeat=2))
    receivers = [lambda x: x[0], lambda x: x[1]]
    target = lambda x: x[0]
    distributions = list(rational_simplex(states, 3))
    for mu in distributions:
        for nu in distributions:
            tv = tv_distance(mu, nu)
            for k in all_subsets(2):
                dmu, _ = defect_and_optimizers(mu, receivers, target, k, declared_domain=states)
                dnu, _ = defect_and_optimizers(nu, receivers, target, k, declared_domain=states)
                assert abs(dmu - dnu) <= tv + 1e-12
    t = 0.37
    mu = {0: 1.0, 1: 0.0}
    nu = {0: 1.0 - t, 1: t}
    assert abs(abs(mu[1] - nu[1]) - tv_distance(mu, nu)) < 1e-12


def test_mixture_concavity_and_shared_optimizer_on_common_domain():
    states = list(product([0, 1], repeat=2))
    receivers = [lambda x: x[1]]
    target = lambda x: x[0]
    distributions = list(rational_simplex(states, 3))
    k = frozenset({0})
    for mu in distributions:
        for nu in distributions:
            for lam in (0.25, 0.5, 0.75):
                mixed = mix(mu, nu, lam)
                dmu, omu = defect_and_optimizers(mu, receivers, target, k, declared_domain=states)
                dnu, onu = defect_and_optimizers(nu, receivers, target, k, declared_domain=states)
                dmix, _ = defect_and_optimizers(mixed, receivers, target, k, declared_domain=states)
                lower = lam * dmu + (1.0 - lam) * dnu
                assert dmix + 1e-12 >= lower
                assert (abs(dmix - lower) < 1e-12) == bool(omu & onu)


def test_log_loss_contextuality_increment_and_both_refinement_directions():
    p = 0.2
    mu = {}
    for c, y, n in product([0, 1], repeat=3):
        prob_n = p if n else 1.0 - p
        mu[(c, y, n)] = 0.25 * prob_n
    y_fn = lambda x: x[1]
    c_fn = lambda x: x[0]
    z1_fn = lambda x: x[1] ^ x[2]
    z2_fn = lambda x: x[1] ^ x[0]
    z12_fn = lambda x: (z1_fn(x), z2_fn(x))
    h_y_z1 = conditional_entropy(mu, y_fn, z1_fn)
    h_y_z12 = conditional_entropy(mu, y_fn, z12_fn)
    i_y_c_z1 = conditional_mutual_information(mu, y_fn, c_fn, z1_fn)
    i_y_c_z12 = conditional_mutual_information(mu, y_fn, c_fn, z12_fn)
    increment = conditional_information_of_added_receiver(mu, y_fn, c_fn, z1_fn, z2_fn)
    h2p = -(p * log2(p) + (1.0 - p) * log2(1.0 - p))
    assert abs(h_y_z1 - h2p) < 1e-12
    assert abs(h_y_z12 - h_y_z1) < 1e-12
    assert abs(i_y_c_z1) < 1e-12
    assert abs(i_y_c_z12 - h2p) < 1e-12
    assert abs((i_y_c_z12 - i_y_c_z1) - increment) < 1e-12

    mu_down = {(0, 0): 0.5, (1, 1): 0.5}
    y_down = lambda x: x[1]
    c_down = lambda x: x[0]
    gamma_empty = conditional_mutual_information(mu_down, y_down, c_down, lambda x: ())
    gamma_y = conditional_mutual_information(mu_down, y_down, c_down, lambda x: x[1])
    assert abs(gamma_empty - 1.0) < 1e-12
    assert abs(gamma_y) < 1e-12


def test_same_support_opposite_decoder_example():
    eta = 0.1
    mu = {(0, 0): (1 - eta) / 2, (1, 1): (1 - eta) / 2, (0, 1): eta / 2, (1, 0): eta / 2}
    nu = {(0, 1): (1 - eta) / 2, (1, 0): (1 - eta) / 2, (0, 0): eta / 2, (1, 1): eta / 2}
    states = list(mu)
    receivers = [lambda x: x[1]]
    target = lambda x: x[0]
    k = frozenset({0})
    dmu, omu = defect_and_optimizers(mu, receivers, target, k, declared_domain=states)
    dnu, onu = defect_and_optimizers(nu, receivers, target, k, declared_domain=states)
    dmix, _ = defect_and_optimizers(mix(mu, nu, 0.5), receivers, target, k, declared_domain=states)
    assert set(mu) == set(nu)
    assert abs(dmu - eta) < 1e-12
    assert abs(dnu - eta) < 1e-12
    assert not (omu & onu)
    assert abs(dmix - 0.5) < 1e-12
    assert abs((dmix - 0.5 * dmu - 0.5 * dnu) - (0.5 - eta)) < 1e-12


def test_uniform_empirical_defect_equals_g3_deletion_error():
    states = list(product([0, 1], repeat=3))
    receivers = [lambda x: x[0], lambda x: x[1]]
    target = lambda x: x[2]
    mu = {x: 1.0 / len(states) for x in states}
    for k in all_subsets(2):
        assert abs(bayes_defect(mu, receivers, target, k) - g3_deletion_error(states, receivers, target, k)) < 1e-12


def test_discernibility_shadow():
    states = list(product([0, 1], repeat=2))
    receivers = [lambda x: x[0], lambda x: x[1]]
    target = lambda x: x[0] ^ x[1]
    assert realizing_families(states, receivers, target) == hitting_family(distinction_hypergraph(states, receivers, target), 2)


def test_double_hitting_for_all_upward_families_including_empty_receiver_set():
    for n in range(0, 5):
        subsets = sorted(all_subsets(n), key=lambda s: (len(s), tuple(s)))
        for mask in product([False, True], repeat=len(subsets)):
            family = {s for s, keep in zip(subsets, mask) if keep}
            if is_upward_closed(family, n):
                assert hitting_family(hitting_family(family, n), n) == family


def test_canonical_support_section_and_fixed_or_universality():
    n = 3
    subsets = sorted(all_subsets(n), key=lambda s: (len(s), tuple(s)))
    upward = []
    for mask in product([False, True], repeat=len(subsets)):
        family = {s for s, keep in zip(subsets, mask) if keep}
        if is_upward_closed(family, n):
            upward.append(family)
    interface_receivers = [lambda x, j=j: x[0][j] for j in range(n)]
    interface_target = lambda x: x[1]
    or_receivers = [lambda x, j=j: x[j] for j in range(n)]
    or_target = lambda x: int(any(x))
    full = frozenset(range(n))
    for f in upward:
        s = canonical_support_from_upward(f, n, with_bit=True)
        assert realizing_families(s, interface_receivers, interface_target) == f
        if f:
            assert full in f
            s_or = canonical_support_from_upward(f, n, with_bit=False)
            assert realizing_families(s_or, or_receivers, or_target) == f
    for f in upward:
        for g in upward:
            sf = canonical_support_from_upward(f, n, with_bit=True)
            sg = canonical_support_from_upward(g, n, with_bit=True)
            assert (f <= g) == (sg <= sf)


def local_exact_decoder(domain, access, target):
    decoder = {}
    for x in domain:
        z = access(x)
        y = target(x)
        if z in decoder and decoder[z] != y:
            return None
        decoder[z] = y
    return decoder


def test_exact_descent_multiple_contexts():
    s1 = [(0, 0), (1, 1)]
    s2 = [(0, 0), (2, 1)]
    target = lambda x: x[0]
    access = lambda x: x[1]
    union = sorted(set(s1) | set(s2))
    assert factors_through(s1, access, target)
    assert factors_through(s2, access, target)
    assert not factors_through(union, access, target)

    t1 = [(0, 0), (1, 1)]
    t2 = [(2, 0), (1, 1)]
    t3 = [(0, 0), (3, 2)]
    target2 = lambda x: {0: 0, 1: 1, 2: 0, 3: 2}[x[0]]
    access2 = lambda x: x[1]
    decoders = [local_exact_decoder(t, access2, target2) for t in (t1, t2, t3)]
    assert all(h is not None for h in decoders)
    for h1, h2 in combinations(decoders, 2):
        for z in set(h1) & set(h2):
            assert h1[z] == h2[z]
    assert local_exact_decoder(set(t1) | set(t2) | set(t3), access2, target2) is not None


def main():
    test_state_relative_presentation_equivalence()
    test_zero_defect_equals_support_factorization()
    test_receiver_monotonicity_and_bayes_formula()
    test_tv_nonexpansiveness_exhaustively_and_sharpness()
    test_mixture_concavity_and_shared_optimizer_on_common_domain()
    test_log_loss_contextuality_increment_and_both_refinement_directions()
    test_same_support_opposite_decoder_example()
    test_uniform_empirical_defect_equals_g3_deletion_error()
    test_discernibility_shadow()
    test_double_hitting_for_all_upward_families_including_empty_receiver_set()
    test_canonical_support_section_and_fixed_or_universality()
    test_exact_descent_multiple_contexts()
    print("adversarial distributional mechanism and support-shadow regressions: PASS")


if __name__ == "__main__":
    main()
