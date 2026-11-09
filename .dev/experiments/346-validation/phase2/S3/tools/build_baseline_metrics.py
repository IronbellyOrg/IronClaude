"""Build baseline-metrics.json (DECISIONS.md D5, M1 to M5) for scenario S3 from the package files.

Usage: uv run python -I build_baseline_metrics.py <S3 package dir>
Numbers marked "read" come from evidence files; "derived" were computed or re-derived here.
"""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

P = Path(sys.argv[1])
costs = json.loads((P / "baseline/agent-costs.json").read_text())


def doc(ver):
    b = (P / f"baseline/plans/refactor-plan.{ver}.md").read_bytes()
    return {"bytes": len(b), "lines": b.count(b"\n") + (0 if b.endswith(b"\n") else 1),
            "sha256": hashlib.sha256(b).hexdigest()}


V = {v: doc(v) for v in ("v0", "v1", "v2")}


def pct(a, b):
    return round(100.0 * (b - a) / a, 2)


def secs(role):
    f = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
    return int((f(costs[role]["last_ts"]) - f(costs[role]["first_ts"])).total_seconds())


def cost(role):
    c = costs[role]
    return {"agent_log": f"H4/subagents/agent-{c['agent_id']}.jsonl", "model": c["model"],
            "api_messages": c["api_messages"], "tool_calls": c["tool_calls"],
            "tool_calls_by_name": c["tool_calls_by_name"], "wall_seconds": secs(role),
            "output_tokens": c["output_tokens"], "input_tokens_uncached": c["input_tokens"],
            "cache_read_tokens": c["cache_read_tokens"], "cache_creation_tokens": c["cache_creation_tokens"]}


SEV = ("Blocking = wrong behaviour, a false claim, a missing required item, a security or acceptance-criterion "
       "hole (reviewer briefs name a leak to main/master as blocking). Minor = wording, format. Binary verdict: "
       "PASS only with no blocking finding. Cap: 2 fix cycles, 3 reviews, then escalate (output-style rule, "
       "inputs/owner/output-style-pragmatic-L15.md, restated in the briefs).")

rounds = [
    {"round": 1, "reviewed_version": "v0", "verdict": "FAIL",
     "review_file": "baseline/reviews/plan-review.md",
     "M2": {"blocking": 8, "minor": 14, "basis": "read: plan-review.md:7-8; ids B-1..B-8 and M-1..M-14 re-counted by script (derived), match"},
     "M3": {"reviewer_origin_tag": None, "reviewer_origin_tag_reason": "the review files carry no origin tags",
            "analyst_rederivation": None, "reason": "first review; no previous fix"},
     "M4": {"document_at_start": V["v0"], "document_after_fix": V["v1"],
            "growth_pct_bytes_during_fix": pct(V["v0"]["bytes"], V["v1"]["bytes"]),
            "growth_pct_lines_during_fix": pct(V["v0"]["lines"], V["v1"]["lines"]),
            "basis": "derived: replay of the recorded Write+Edit calls (tools/replay_plan.py); line counts equal what the reviewers' own Read calls returned (tools/crosscheck_reads.py); bytes are derived, v2 bytes equal the file on disk"},
     "M5": {"review": cost("R1_review"), "fix_after_review": cost("R1_fix"),
            "basis": "derived: tools/agent_costs.py over the subagent logs (unique API messages and tool_use ids; usage from the last record of each message id)"}},
    {"round": 2, "reviewed_version": "v1", "verdict": "FAIL",
     "review_file": "baseline/reviews/plan-review-2.md",
     "M2": {"blocking": 8, "minor": 12, "basis": "read: plan-review-2.md:7-8; ids F-1..F-8, m-1..m-12 re-counted (derived), match"},
     "M3": {"reviewer_origin_tag": None, "reviewer_origin_tag_reason": "no origin tags; the review says which round-1 findings were closed (plan-review-2.md:12-25) but not which new ones the fix caused",
            "analyst_rederivation": {"of": 8,
                                     "fix_induced_ids": ["F-2", "F-3", "F-4"],
                                     "partly_fix_induced_ids": ["F-1", "F-8"],
                                     "latent_in_v0_ids": ["F-5", "F-6", "F-7"],
                                     "share_lower": 0.375, "share_upper": 0.625,
                                     "evidence": "F-2 canonical push form, F-3 GET-only gh api form and F-4 the O-16 justification do not exist in v0 (rg counts 0) and appear in v1. F-1: the later-git-word exemption (G4) is already in v0 line 218; only the NM2 line join is new in v1 (partly). F-8: the over-block of a one-line PR title that mentions git comes from the v0 first-git-word UNKNOWN rule, but the false sentence 'one-line commit messages and PR titles that mention git are not blocked' (the mention of PR titles) first appears in v1 line 234, written by fix cycle 1 for B-8 (partly). F-5: v0 decision-table row 33 pins `$GIT push origin main` (v0 line 421). F-6 and F-7: v0 N2 already deletes every quote and backslash and v0 N4 already removes a redirection together with the next word (v0 lines 192, 194).",
                                     "method": "derived: replay of the plan versions, rg over v0, v1, v2 text; reading of the rule text only, nothing was executed; the review itself gives no origin tag",
                                     "discrepancy_with_phase1": "phase-1 REPORT.md (I3 table) says 7 of 8 trace to fix cycle 1 and names NM4 as added by fix cycle 1; v0 already had the same redirection step (called N4), so that count is not supported. Use share_lower to share_upper."}},
     "M4": {"document_at_start": V["v1"], "document_after_fix": V["v2"],
            "growth_pct_bytes_during_fix": pct(V["v1"]["bytes"], V["v2"]["bytes"]),
            "growth_pct_lines_during_fix": pct(V["v1"]["lines"], V["v2"]["lines"]),
            "basis": "derived, as round 1"},
     "M5": {"review": cost("R2_review"), "fix_after_review": cost("R2_fix"), "basis": "derived, as round 1"}},
    {"round": 3, "reviewed_version": "v2", "verdict": "FAIL",
     "review_file": "baseline/reviews/plan-review-3.md",
     "M2": {"blocking": 10, "minor": 11, "basis": "read: plan-review-3.md:7-8; ids B-1..B-10, m-1..m-11 re-counted (derived), match"},
     "M3": {"reviewer_origin_tag": None, "reviewer_origin_tag_reason": "no origin tags",
            "analyst_rederivation": {"of": 10,
                                     "fix_induced_ids": ["B-6"],
                                     "partly_fix_induced_ids": ["B-3", "B-4"],
                                     "latent_in_earlier_versions_ids": ["B-1", "B-2", "B-5", "B-7", "B-8", "B-9"],
                                     "unclassified_ids": ["B-10"],
                                     "share_lower": 0.1, "share_upper": 0.3,
                                     "evidence": "B-6: the rule 'segment split runs only when W contains git, gh, orca, superclaude or repos/' exists only in v2 (v2 line 209). B-3: v2 replaces 'first git word per segment' by command position and adds the position-free global rule, so the wrapper and keyword routes are new in shape. B-4: a git config file outside the tamper list was an open hole since v0 (v0 tamper list has only .gitconfig and .git/config, v0 line 321), but the contradiction the review cites (R11 'the agent cannot set one' against R17 naming ~/.config/git/config and GIT_CONFIG_GLOBAL) exists only in v2 (R17 first appears in v2 line 994). B-1 and B-2: v1 NM2 already joined continuation lines with a space and deleted every quote (v1 line 197), so `gi\\<newline>t` and `$'git'` were already hidden in v1. B-5, B-7, B-8, B-9: glob and brace gaps, R10 (curl), npx and the `superclaude install` rule are in v0 (v0 lines 321-322, R10 and npx present in v0). B-10: the 'No S, UNKNOWN for a first word' rule is in v0 and v1 (v0 line 210), so it probably existed in v1 too, but I did not run it.",
                                     "method": "derived: replay of the plan versions, rg over v0, v1, v2 text; reading of the rule text only, nothing was executed; the review itself gives no origin tag"}},
     "M4": {"document_at_start": V["v2"], "document_after_fix": None,
            "growth_pct_bytes_during_fix": None, "growth_pct_lines_during_fix": None,
            "basis": "no fix cycle after review 3 (cap reached, owner stop at H4.jsonl L1082); the later merge executor output is not part of this loop"},
     "M5": {"review": cost("R3_review"), "fix_after_review": None, "basis": "derived, as round 1"}},
]

out = {
    "scenario": "S3", "incident": "I3",
    "incident_name": "Launch-level hook refactoring plan (issue 394), three adversarial plan reviews",
    "definitions": "346-validation/DECISIONS.md D5 (M1 to M5)",
    "document_under_review": "adversarial/adversarial/refactor-plan.md of brainstorm 20261105-170229-launch-level-hook",
    "baseline_environment": {"repo_commit": "8b4858f7", "claude_code_version": "2.1.318",
                             "orchestrator_model": "claude-sonnet-5-5 for H4.jsonl lines 880-1060 (the session later also ran 1,022 messages on model gpt-6.1-sol)",
                             "subagent_models": {"drafter_and_revisers": "claude-opus-5-5", "review_1_and_2": "claude-sonnet-5-5", "review_3": "claude-opus-5-5"},
                             "log": "H4.jsonl (42ae46e0-b8b8-4840-aafe-9b182be079c9)"},
    "severity_rule": SEV,
    "M1": {"rounds_until_clean_pass": None,
           "reason": "no review passed; the loop stopped at the cap of 3 reviews after 2 fix cycles, then the owner confirmed no further review (H4.jsonl L1059, L1082)",
           "rounds_run": 3, "fix_cycles_run": 2, "final_verdict": "FAIL",
           "basis": "read: parent summaries H4.jsonl L946, L999, L1059; verdict lines of the three review files"},
    "rounds": rounds,
    "loop_totals": {
        "blocking_findings_all_rounds": 26, "minor_findings_all_rounds": 37,
        "blocking_per_round": [8, 8, 10], "last_round_blocking": 10,
        "document_growth_over_loop": {"bytes_pct": pct(V["v0"]["bytes"], V["v2"]["bytes"]),
                                      "lines_pct": pct(V["v0"]["lines"], V["v2"]["lines"]),
                                      "from": "v0 (draft, start of review 1)", "to": "v2 (after fix cycle 2)"},
        "draft_step_cost_not_part_of_loop": cost("R0_draft"),
        "tokens_and_calls_review_and_fix_agents_only": {
            "tool_calls": sum(costs[r]["tool_calls"] for r in costs if r != "R0_draft"),
            "output_tokens": sum(costs[r]["output_tokens"] for r in costs if r != "R0_draft")},
        "wall_seconds_first_review_start_to_last_review_end": int(
            (datetime.fromisoformat(costs["R3_review"]["last_ts"].replace("Z", "+00:00"))
             - datetime.fromisoformat(costs["R1_review"]["first_ts"].replace("Z", "+00:00"))).total_seconds())},
    "line_count_note": "Phase-1 report quotes 1,054 / 1,139 / 1,314 lines: that is the last line number a Read returned, one past the final line (an empty trailing row). Actual line counts are 1,053 / 1,138 / 1,313.",
    "token_caveat": "cache_read and cache_creation tokens count the repeated context of every turn; compare output_tokens, api_messages and tool_calls between runs, not cache totals.",
}
(P / "baseline-metrics.json").write_text(json.dumps(out, indent=1) + "\n")
print("ok", json.dumps(out["loop_totals"]["document_growth_over_loop"]))
