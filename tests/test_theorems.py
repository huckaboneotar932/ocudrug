from ocudrug_graphrag.proceedings.theorems import (
    pareto_dominance_check,
    tier3_lower_bound,
    variance_reduction_bound,
)


def test_tier3_lower_bound_value() -> None:
    bound = tier3_lower_bound(0.65, 0.18)
    assert abs(bound.lower_bound - 0.938) < 0.002
    assert abs(bound.fpr_suppression - 31.0) < 1.0


def test_variance_reduction_below_min() -> None:
    vb = variance_reduction_bound(0.05)
    assert vb.reduced_upper_bound < 0.05
    assert 0.0 < vb.coefficient < 1.0


def test_pareto_operating_point_dominates() -> None:
    operating = (0.495, 0.873)
    alternatives = {
        "hard_filter": (0.470, 0.401),
        "learned_leak": (0.452, 0.55),
        "text_only": (0.421, 0.606),
    }
    assert pareto_dominance_check(operating, alternatives) is True
