import json, sys
B = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/"
S = B + "source.md"; P = B + "TASK-WF-designSpec-20261107-075614.md"
sl = open(S).read().split("\n"); pl = open(P).read().split("\n")
def c(role, a, b, q=None): return {"role": role, "path": S if role == "spec" else P, "line_start": a, "line_end": b, **({"quote": q} if q else {})}
F = [
 ("M-001", "MAJOR", False, "missing-requirement",
  "Resume row 4 and RETRY_RELEASE re-enter release_decision, which needs target_sha and applied_edits, but resume_decision's signature has neither and Task 4 AC does not say where they come from; outcome is fail-safe (HOLD or a completed push), so under-specified, not forced-wrong.",
  ["V1-F2", "V1-F13"],
  [c("spec", 107, 107, "`release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)`"),
   c("spec", 109, 109, "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"),
   c("spec", 166, 166, "re-enter `release_decision` with `push_completed=True`"),
   c("plan", 77, 77, "each re-enter `release_decision` with `push_completed=True`")]),
 ("M-002", "MAJOR", False, "missing-requirement",
  "After a failed engage the fold leaves RELEASE_PENDING with owned_draft false, engage row 6 returns HOLD(ownership_unproven) and never ENGAGE, and neither spec nor plan says what the SKILL does with HOLD at engage; a literal reading could edit on a ready PR. Spec hole the plan copies.",
  ["PROBE-INV-002"],
  [c("spec", 68, 68, "Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`."),
   c("spec", 138, 138, "`HOLD(ownership_unproven)`"),
   c("spec", 199, 199, "`phase = RELEASE_PENDING`, `failed_mutations += 1`, `owned_draft` unchanged"),
   c("plan", 70, 70, "`engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows")]),
 ("M-003", "MINOR", False, "missing-requirement",
  "One minted fix or ci id must be reused by the push triad and rereview_requested; the plan states it in Task 8 prose but its AC only names the mint place, and the fold lists a cycle_id field no effect row sets. Weak AC, not a missing requirement.",
  ["V1-F1", "V3-F1", "V1-F9", "PROBE-INV-003"],
  [c("spec", 251, 251, "uses the same id as the `cycle_id` of the push triad"),
   c("plan", 124, 124, "reuses it as the `cycle_id` of the push triad and of `rereview_requested`"),
   c("plan", 127, 127, "states the single place where the guard-enabled cycle id is minted"),
   c("spec", 190, 190, "phase, phase_before_request, cycle_id, original_is_draft, baseline, run_toggles,")]),
 ("M-004", "MINOR", False, "unpassable-check",
  "A ready not_applied may restore RELEASE_PENDING, but Task 3 AC tests only the HELD outcome, and no effect row says when phase_before_request is set; an always-HELD fold passes the AC.",
  ["V1-F3"],
  [c("spec", 201, 201, "the phase returns to `phase_before_request`"),
   c("plan", 60, 60, "a ready request followed by `not_applied` gives phase `HELD` with `unsettled == 0`")]),
 ("M-005", "MINOR", False, "unpassable-check",
  "Task 11 AC requires the twelve test names; its prose and ACs assert nothing for the release-failure retry, the unreadable-timeline-never-readies case or the moved-head case, so a test with that name that asserts nothing passes.",
  ["V2-F1", "PROBE-INV-005"],
  [c("spec", 315, 315, "one retry, `already_in_state` counts as confirmed, `release_pending` (FR-16)"),
   c("plan", 166, 166, "Cover the cases of the section 5 table"),
   c("plan", 169, 169, "The test file defines `test_guard_modes_ordinals_and_resume_authority`")]),
 ("M-006", "MINOR", False, "missing-requirement",
  "The fold row for a user_override skip sets no disabled_cause while guard_status reads cause user_override; a log built by the real fold matches no mapping row, and Task 3 tests the cause only for already_draft.",
  ["PROBE-INV-001"],
  [c("spec", 206, 206, "`settled(any, skipped, user_override)` | `phase = DISABLED`, `owned_draft = False`"),
   c("spec", 112, 112, "phase `DISABLED` with cause `user_override` gives `user_override`"),
   c("plan", 61, 61, "A `guard_status` test covers every phase and cause of the first-match mapping")]),
 ("M-007", "MINOR", False, "missing-requirement",
  "No pure function owns the request-key a<k> count or the --read JSON to GuardRead mapping, and the script JSON to settle outcome mapping is unstated; Task 3 AC tests only suffix matching.",
  ["V1-F4", "V1-F6"],
  [c("spec", 184, 184, "`idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>`"),
   c("spec", 90, 90, "auto_merge_armed: bool; transitions: int | None; complete: bool"),
   c("plan", 62, 62, "with retries distinguished by the `:a<k>` suffix")]),
 ("M-008", "MINOR", False, "contradiction",
  "The Wave 0 row promises unsettled requests are reconciled before any edit, but resume row 2 returns REPORT_HELD with no mutation at ordinal below 3 or mode off, ahead of RECONCILE; the plan codifies row 2 deliberately.",
  ["V1-F5"],
  [c("spec", 58, 58, "unsettled requests are reconciled before any edit, release or re-trigger"),
   c("spec", 164, 164, "`REPORT_HELD` (no mutation; prints the clear command)"),
   c("plan", 76, 76, "row 2 wins over row 3")]),
 ("M-009", "MINOR", False, "missing-requirement",
  "The CI-fix engage trigger has no severity: the spec lists the CI-fix cycle under the Medium-or-higher routed-finding row, and the Wave 8 bullet engages it with kind ci; the plan copies this.",
  ["V1-F7"],
  [c("spec", 61, 61, "or CI-fix cycle from Wave 8"),
   c("spec", 241, 241, "a CI-fix cycle engages with kind `ci`"),
   c("plan", 150, 150, "a CI-fix cycle engages with kind `ci`")]),
 ("M-010", "MINOR", False, "unpassable-check",
  "Task 7 AC lists the autoMergeRequest key but not its type; the spec example prints a boolean while gh returns an object or null, so a pass-through script satisfies the AC.",
  ["V2-F2"],
  [c("spec", 230, 230, "\"autoMergeRequest\":false"),
   c("plan", 111, 111, "`headRefOid`, `autoMergeRequest`, `transitions`, `complete`")]),
 ("M-011", "MINOR", False, "missing-requirement",
  "The constraint that protocol prose carries no file:NNN pointers is stated in the Constraints block and Task 8 prose, but Task 8 ACs test only src/superclaude, fences and gh scope.",
  ["V2-F3"],
  [c("plan", 23, 23, "Protocol prose carries no `file:NNN` pointers."),
   c("plan", 128, 128, "the ref does not contain `src/superclaude`")]),
 ("M-012", "MINOR", False, "other",
  "Task 7 makes adding the script to _RESOLUTION_SCRIPTS conditional on reading the list's purpose, while its AC states the script passes the _RESOLUTION_SCRIPTS origin-URL resolution tests.",
  ["V3-F2"],
  [c("plan", 108, 108, "only after reading the purpose of that list"),
   c("plan", 113, 113, "the script passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests")]),
 ("M-013", "MINOR", False, "contradiction",
  "Task 9 requires the Wave 0 bullet to carry no L3 or draft condition yet to say 'at L3 with --merge-guard off'; its AC fails the bullet when it names an L3 or draft condition, so literal text can fail its own test.",
  ["PROBE-INV-007"],
  [c("plan", 137, 137, "carries no L3 or `draft` condition"),
   c("plan", 140, 140, "when it names an L3 or `draft` condition")]),
 ("M-014", "MINOR", False, "other",
  "Small spec gaps the plan copies: Phase members have no string values while Task 5 asserts engage_pending; the timeline-failure ok value is unstated; no row checks unsettled requests at engage.",
  ["V1-F10", "V1-F14", "V1-F8"],
  [c("spec", 80, 80, "ENGAGE_PENDING; HELD; RELEASE_PENDING; RELEASED; DISABLED"),
   c("spec", 234, 234, "`gh` failure or failed verification (the JSON line is still printed with `ok:false`)"),
   c("plan", 90, 90, "returns `unsettled == 1` and phase `engage_pending`")]),
]
bad = []
out = []
for fid, sev, blk, cat, claim, src, cits in F:
    assert len(claim) <= 300, (fid, len(claim))
    for ct in cits:
        lines = sl if ct["role"] == "spec" else pl
        seg = "\n".join(lines[ct["line_start"] - 1: ct["line_end"]])
        if "quote" in ct and ct["quote"] not in seg: bad.append((fid, ct["line_start"], ct["quote"][:60]))
        assert len(ct.get("quote", "")) <= 200, (fid, "quote length")
    out.append({"id": fid, "severity": sev, "blocking": blk, "category": cat, "lens": "reflect-pre", "claim": claim, "refs": src, "citations": cits})
if bad: print("QUOTE MISMATCH", bad); sys.exit(1)
d = sys.argv[1]
open(d + "/artifacts/merged-findings.jsonl", "w").write("\n".join(json.dumps(o, ensure_ascii=False) for o in out) + "\n")
print(len(out), "findings; all quotes verified; max claim", max(len(o["claim"]) for o in out))
