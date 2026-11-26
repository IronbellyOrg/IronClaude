from fractions import Fraction

import pytest
from harness import scorer
from harness.scorer import (
    jev_answer,
    latency_stats,
    median,
    percentile_nearest_rank,
    right,
    sign_test_passes,
)

# ---- right (T-07)

def test_right_for_a_typed_label():
    assert right("bug", "bug") is True
    assert right("bug", "test") is False
    assert right("bug", None) is False                 # an unset answer on a typed label is not right


@pytest.mark.parametrize("label", ["ambiguous", "none-fit"])
def test_right_for_an_unset_label_needs_an_unset_answer(label):
    assert right(label, None) is True
    assert right(label, "bug") is False


def test_right_refuses_an_unknown_label():
    with pytest.raises(ValueError):
        right("urgent", None)


# ---- sign test (T-12, T-15)

@pytest.mark.parametrize("b,c", [(5, 0), (7, 1), (9, 2)])
def test_sign_test_passes_for_the_agreed_cases(b, c):
    assert sign_test_passes(b, c) is True


@pytest.mark.parametrize("b,c", [(4, 0), (6, 1), (8, 2), (0, 0), (0, 7), (3, 9)])
def test_sign_test_fails_for_the_agreed_cases(b, c):
    assert sign_test_passes(b, c) is False


def test_smallest_passing_b_for_each_c_from_0_to_6():
    smallest = [next(b for b in range(0, 40) if sign_test_passes(b, c)) for c in range(7)]
    assert smallest == [5, 7, 9, 10, 12, 13, 15]


def test_sign_test_agrees_with_an_exact_fraction_reference_up_to_30():
    from math import comb
    for b in range(31):
        for c in range(31):
            n = b + c
            expected = n > 0 and Fraction(sum(comb(n, k) for k in range(b, n + 1)), 2 ** n) < Fraction(1, 20)
            assert sign_test_passes(b, c) is expected, (b, c)


def test_sign_test_reads_the_factor_from_the_rule():
    assert sign_test_passes(4, 0, alpha_inverse=10) is True      # 1/16 is below 1/10 but not below 1/20
    assert sign_test_passes(4, 0, alpha_inverse=20) is False


# ---- jev_answer (T-05)

def _rule(low_op, high_op):
    return {"noul_low": 0.3, "noul_high": 0.7, "noul_low_operator": low_op, "noul_high_operator": high_op}


@pytest.mark.parametrize("low_op", ["lt", "le"])
@pytest.mark.parametrize("high_op", ["gt", "ge"])
def test_jev_answer_at_and_around_both_edges(low_op, high_op):
    rule = _rule(low_op, high_op)
    assert jev_answer(0.2999999, "bug", rule) == (None, "none-fit")
    assert jev_answer(0.3, "bug", rule) == ((None, "none-fit") if low_op == "le" else (None, "not-settled"))
    assert jev_answer(0.3000001, "bug", rule) == (None, "not-settled")
    assert jev_answer(0.5, "bug", rule) == (None, "not-settled")
    assert jev_answer(0.6999999, "bug", rule) == (None, "not-settled")
    assert jev_answer(0.7, "bug", rule) == (("bug", None) if high_op == "ge" else (None, "not-settled"))
    assert jev_answer(0.7000001, "bug", rule) == ("bug", None)


@pytest.mark.parametrize("low_op,high_op", [("UNSET", "ge"), ("le", "UNSET"), ("gt", "ge"), ("le", "lt")])
def test_jev_answer_refuses_an_unset_or_misplaced_operator(low_op, high_op):
    with pytest.raises(ValueError):
        jev_answer(0.5, "bug", _rule(low_op, high_op))


# ---- median, percentile, latency (T-08)

def test_median_of_odd_and_even_counts_and_empty():
    assert median([3, 1, 2]) == 2
    assert median([4, 1, 3, 2]) == 2.5
    assert median([]) is None


def test_nearest_rank_percentile():
    assert percentile_nearest_rank(list(range(1, 11)), 0.9) == 9          # ceil(9) - 1 = index 8
    assert percentile_nearest_rank(list(range(1, 31)), 0.9) == 27
    assert percentile_nearest_rank(list(range(1, 12)), 0.9) == 10         # ceil(9.9) - 1 = index 9
    assert percentile_nearest_rank([5], 0.9) == 5
    assert percentile_nearest_rank([], 0.9) is None


def _a(pid, latency, timed_out=False, answered=True):
    return {"prompt_id": pid, "latency_s": latency, "timed_out": timed_out, "answered": answered}


RULE = {"attempt_timeout_s": 10.0, "median_population": "answered_only"}


def test_timeout_counts_at_the_cap_in_the_slowest_and_is_left_out_of_the_median():
    attempts = [_a("p1", 10.4, timed_out=True, answered=False), _a("p1", 1.0), _a("p2", 3.0)]
    s = latency_stats(attempts, RULE)
    assert s["slowest"] == 10.0 and s["median"] == 2.0 and s["p90"] == 3.0 and s["n"] == 2


def test_a_prompt_that_never_answered_is_not_in_the_answered_only_population():
    s = latency_stats([_a("p1", 0.5), _a("p2", 2.0, answered=False)], RULE)
    assert s["n"] == 1 and s["median"] == 0.5 and s["slowest"] == 2.0


def test_the_include_timeouts_population_counts_a_timeout_at_the_cap():
    rule = dict(RULE, median_population="include_timeouts_at_cap")
    s = latency_stats([_a("p1", 1.0), _a("p2", 10.2, timed_out=True, answered=False)], rule)
    assert s["n"] == 2 and s["median"] == 5.5 and s["slowest"] == 10.0


def test_latency_stats_on_no_attempts_are_none_and_an_unknown_population_is_refused():
    assert latency_stats([], RULE) == {"median": None, "slowest": None, "p90": None, "n": 0}
    with pytest.raises(ValueError):
        latency_stats([_a("p1", 1.0)], dict(RULE, median_population="all"))


def test_scorer_has_no_floating_point_comparison_at_the_agreed_line():
    text = open(scorer.__file__, encoding="utf-8").read()
    assert "0.05" not in text and "0.95" not in text
