from conftest import (
    CONTROL,
    candidate,
    default_rules,
    finding,
    jload,
    launch,
    mini_sandbox,
    write_plan,
    write_values,
)

from r3lib import metrics

CAND = candidate()

R23 = [
    "msgs_sent",
    "msgs_received",
    "seal_t",
    "resume_fallback",
    "phase2_s",
    "reask_s",
    "p2reask_s",
    "attempts",
    "retry_s",
    "retry_isolated",
    "phase2_timeout",
    "p2_lines_salvaged",
    "n_planned",
    "n_launched",
    "hang_kill",
    "no_launch_reason",
    "output_tokens_all",
] + metrics.MIDRUN_NULL
PANEL = [
    "T0",
    "elapsed_s",
    "baseline_elapsed_s",
    "overhead_pct",
    "k",
    "panel_finish_at",
    "finish_would_fire",
    "slo_breach",
    "own_line_jaccard",
    "pairwise_task_jaccard",
    "echo_rate",
    "ledger_rows",
    "challenges_real",
    "challenges_gap",
    "gt_anchor_overlap",
]


def test_collab_json_keys(env):
    write_values(env)
    mini_sandbox(env)
    write_plan(env, default_rules(env))
    r, rd = launch(env, extra=["--no-judge"])
    cj = jload(rd / CONTROL / "collab.json")
    for k in (
        "arm",
        "panel",
        "run_id",
        "pkg",
        "values_sha256",
        "values_status",
        "reviewers",
        "slots",
    ):
        assert k in cj
    for rv in cj["reviewers"].values():
        assert all(k in rv for k in R23)
    assert all(k in cj["panel"] for k in PANEL)
    for s in cj["slots"]:
        assert {
            "rid",
            "j",
            "slot_type",
            "move",
            "source_rid",
            "source_finding_id",
            "deal_r",
            "card_form",
            "deal_c",
        } <= set(s)


def test_own_line_jaccard_ignores_peer_lines():
    own = {"a": [finding("F1", "every")], "b": [finding("F1", "cmd")]}
    j0 = metrics.own_line_jaccard(own, CAND)
    assert j0 == 0.0
    withpeer = {
        "a": own["a"] + [dict(finding("P2-F1", "cmd"), origin="peer")],
        "b": own["b"],
    }
    assert metrics.own_line_jaccard(withpeer, CAND) == j0
    assert metrics.all_line_jaccard(withpeer, CAND) > metrics.all_line_jaccard(
        own, CAND
    )


def test_echo():
    slots = {
        "t4-1": [
            {
                "slot_type": "real",
                "anchor": finding("x", "only")["anchor"],
                "source_rid": "t2b-1",
                "source_finding_id": "F1",
            }
        ]
    }
    claims = {
        ("t2b-1", "F1"): "The edit roots exclude the artifacts folder entirely here"
    }
    p2 = {
        "t4-1": [
            finding(
                "P2-F1",
                "only",
                claim="The edit roots exclude the artifacts folder entirely here",
            )
        ]
    }
    assert metrics.echo_rate(p2, slots, claims) == 1.0
    assert (
        metrics.echo_rate(
            p2, {"t4-1": [dict(slots["t4-1"][0], slot_type="gap")]}, claims
        )
        == "n/a"
    )


def test_task_of():
    c = "# Plan\n\n## Task 3: Do x\n\nThe worker must keep every rule here.\n"
    assert metrics.task_of(c, "The worker must keep every rule") == "T3"
