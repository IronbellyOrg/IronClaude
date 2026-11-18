# Research: Ledger, merge and verdict mechanics

**Investigation type:** Code Tracer
**Scope:** `src/superclaude/cli/review/ledger.py`, `src/superclaude/cli/review/merge_cmd.py`, `src/superclaude/cli/review/ledger_cmd.py`, `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py`, `~/.claude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py`, `~/.claude/agents/finding-grader.md`, `.dev/experiments/346-validation/phase5/final-bundle/SNAPSHOT-STATE.txt`, E2 audit D (`git show 4a22d742...:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/analysis/audits/audit-D/*`), `tests/review/test_review_ledger.py`
**Status:** Complete
**Date:** 2026-11-14

---

Read first (per task rules): `research/scope/00-handoff-copy.md` sections 2.4 and 2.6, `research/scope/01-other-branch-study.md` section 2, `research/scope/02-review-cli-code.md` sections 5 and 6. Every line number below was re-read in this pass on branch `ironbelly/shadow-runs` (HEAD 792cf8c52); the scope slices are cited only for context.

## 1. `src/superclaude/cli/review/ledger.py` (494 lines) [E3]

### 1.1 What the module is

- Docstring :1-5: "Typed finding ledger (review-ledger/1): rows, statuses and the verdict. Only this module changes a finding's status; a reviewer's own prior lines are recorded as notes and never change one." [E3]
- Imports only the v1 contract: `from superclaude.cli.review import findings as fnd` (:15). No import of `findings_v2` or `cluster` (the reflect v2 stack, [E1]). [E3]
- Constants: `SCHEMA = "review-ledger/1"` (:17), `CAPTURE_SCHEMA = "review-capture/1"` (:18), `STATUSES = ("open", "resolved_check", "resolved", "regressed", "deferred")` (:19), `_SEV_RANK` (:20), `REVISER_RULES` text (:22-26). [E3]
- `new_ledger(doc, cap=3)` (:37-38) is the only place `cap_reviews` is set. `load` (:41-49) checks only `schema`. `save` (:52-67) is atomic (temp file + `os.replace`, fsync). [E3]

### 1.2 Data flow of `merge_round` (:107-298)

1. Round check :114-118: `expected = len(ledger["rounds"]) + 1`; raise if `n != expected`. No comparison with `ledger["cap_reviews"]`. [E3]
2. Duplicate reviewer id check :119-121. [E3]
3. Per reviewer (:127-149): `fnd.parse_block(rv["text"])` (:128); `block_ok[id] = parsed["ok"]` (:129); if not ok, ONE warning with the error count and only `errors[0]["msg"]` (:130-134); every parsable finding is annotated with `fnd.annotate(f, doc_text)` and tagged `_reviewer` (:135-138) — this runs whether or not the block is ok; priors collected (:139-140); `entries` record `reviewer_id, model, report, report_sha256, block_ok` only (:141-149). The rejected lines' ids, reasons and count are not stored in the entry. [E3]
4. No-valid-block refusal :150-157: raises `LedgerError` only when `not any(block_ok.values())`. [E3]
5. Clustering :165: `fnd.cluster(all_findings)` (v1 union-find, `findings.py:382-407`). [E3]
6. Row match :166-171: a group matches the first existing row for which `fnd.same_defect(m, _view(row))` is true for any member. [E3]
7. New row :181-206: `blocking = any(m["blocking"] for m in group)` (:187); `category`, `anchor`, `anchor2`, `span`, `claim`, `fp` all from `group[0]` (:182-199); `confidence` set by `_confidence(row)` (:203). [E3]
8. Matched row :207-238: `current = any(m["blocking"] for m in group)` (:213); `row["blocking"] = (row["blocking"] or current) if row["lid"] in refound else current` (:216-218) — the current round's members overwrite the stored blocking flag; re-anchor on the first member with a span (:226-231); status `resolved_check`/`resolved` -> `regressed` (:235-238). [E3]
9. Clearing loop :254-258: every row with `status == "resolved_check"` and `lid not in members_by_lid` becomes `resolved`. [E3]
10. Prior lines become `prior_note` history events (:259-272); unknown prior id is a warning (:262-264). [E3]
11. Verdict :273-275: `brief = _brief_ids(ledger)`; `verdict = "FAIL" if brief else "PASS"`; `decision = _decision(ledger, verdict, n)`. [E3]
12. Round record :276-285 (`n, doc_sha256, reviewers, verdict, decision, brief_ids`) and result dict :286-298 (includes `block_ok` and `warnings`, plus private `_members`). [E3]

### 1.3 Helper functions

- `_confidence` :86-90 returns `"overlap"` when any single round has 2+ distinct reviewer ids among the row's members, else `"single"`. [E3]
- `_decision` :93-96: PASS -> PASS; otherwise `REVISE if n < cap_reviews else ESCALATE`. [E3]
- `_brief_ids` :99-104: rows with `blocking` true and status `open` or `regressed`. `confidence` is not read. [E3]
- `verdict` :363-372 returns the stored verdict of the last round; it never recomputes. [E3]
- `apply_revision` :301-347: refuses if `--old` sha differs from the last round's `doc_sha256` (:308-314); a fix-map item `applied` whose row span is touched by a diff hunk moves `open`/`regressed` -> `resolved_check` (:330-336), else `named_not_touched` (:337-339); any other action is `rejected_by_reviser` (:340-342); all spans are mapped through the diff (:343-346). [E3]
- `defer` :350-360: sets `deferred`, removes the lid from the last round's `brief_ids`, and if empty rewrites the stored verdict and decision to PASS (:359-360). [E3]
- `capture` :375-401: `review-capture/1` matrix per round, `blocking = any(member blocking)` (:390). [E3]
- `render_merged_report` :408-494: header `review: n of cap` (:416), one line per reviewer with `block ok` (:421-424), ledger table that DOES print `confidence` (:429-437), blocking findings show each current member's claim and anchor (:439-466), `## Escalation` instead of the Reviser brief when decision is ESCALATE (:475-486), else `## Reviser brief` + `REVISER_RULES` (:487-493). [E3]

### 1.4 Defects D2, D3, D4, D16 against current lines

| ID | Claim | Current code (re-read 2026-11-14) | Verdict |
|---|---|---|---|
| D2 | Clearing ignores `block_ok`, contradicting the docstring | Docstring :112 "A reviewer with an invalid block is skipped for clearing but its parsable findings are kept." Clearing loop :254-258 tests only `row["status"] == "resolved_check" and row["lid"] not in members_by_lid`; `block_ok` (built :123, :129) is never consulted after :150. So a `resolved_check` row is cleared to `resolved` when the only reviewer who would have re-reported it had a truncated or invalid block (or when its re-report line itself was rejected by `_check_finding`). | hand-off claim [CODE-VERIFIED] [E3]; the docstring :112 is [CODE-CONTRADICTED] by :254-258 |
| D3 | A round can PASS on one valid reviewer | :150-157 raises only when no reviewer is ok; with one ok reviewer and N-1 invalid ones, clustering runs over whatever parsed (:135-138) and :273-274 computes PASS when no open/regressed blocking row exists. Pinned by `tests/review/test_review_ledger.py:376` (see section 3). | [CODE-VERIFIED] [E3] |
| D4 | One reviewer's `blocking` decides; `confidence` unused | New row :187 `any(...)`; matched row :213-218 `any(...)` of the current round's group; `_brief_ids` :99-104 reads only `blocking` and `status`; verdict :274. `_confidence` (:86-90) is stored (:192, :203, :223) and printed in the merged report (:435, :473) but no decision reads it. Precision: "computed but unused" is true for the verdict/decision; it is used for display. Also an asymmetry: on a matched row a single nonblocking re-report by any reviewer (with no blocking member in that group) sets `blocking = False` (:216-218), so one reviewer can also UN-block a row. | blocking half [CODE-VERIFIED]; "confidence never used" [CODE-CONTRADICTED] in part (used for display only) [E3] |
| D16a | Round 4 accepted | :114-118 only requires `n == len(rounds)+1`. `_decision` :96 returns ESCALATE at `n >= cap_reviews`, but the merge still runs and appends round 4 (:276-285). `merge_cmd.py:40-41` help says "Review number (1, 2 or 3)" while the type is `click.IntRange(min=1)` with no max. | [CODE-VERIFIED] [E3]; help text **[STALE DOC]** vs :40 |
| D16b | `--cap` ignored on an existing ledger | `merge_cmd.py:101-104`: an existing file is `led.load`ed; `led.new_ledger(doc, cap)` only when the file is absent and `round_n == 1`. The `--cap` help says so explicitly (`merge_cmd.py:69` "Review cap used when round 1 creates the ledger."). So it is documented, but silent: no warning when a different `--cap` is passed. | [CODE-VERIFIED] [E3] |
| D16c | Verify-only is not a code mode | `merge_round` signature :107 has no mode argument; every round re-parses full findings and re-clusters (:127-171). No `verify` symbol exists in `ledger.py` (whole file read). The only verify-only implementation is the installed experiment script (section 6). | [CODE-VERIFIED] [E3] |

Additional observations:
- `merge_round` mutates `ledger["rows"]` in place (:204, :209, :236, :256) before the round record is appended; `merge_cmd` saves only after rendering (`merge_cmd.py:109-116`), so a failure between is safe on disk but not in memory. [E3]
- `members_by_lid` (:164, :239) includes members whose own line was valid even if their reviewer's block was not ok, so an invalid reviewer CAN prevent clearing (by re-reporting) but its absence never blocks clearing (D2). [E3]
- `render_merged_report` prints `review: {n} of {cap}` (:416); at round 4 with cap 3 it would print "review: 4 of 3". Inference from :413/:416, not run. [E3]

Key Takeaways
- The v1 ledger is a deterministic, any-reviewer-blocks model: one reviewer opens a blocking row, one reviewer's nonblocking re-report un-blocks it, and absence of a re-report clears a `resolved_check` row, regardless of reviewer validity. [E3]
- `confidence` is a display field, not a decision input. [E3]
- Cap and round limits are enforced only by the decision label, not by refusing the merge. [E3]
- Adopting this ledger as the shared core would import D2/D3/D4/D16 into reflect, which today avoids them because the v2 stack has no ledger or verdict (`02-review-cli-code.md` section 5 summary). [E1][E3]

## 2. `merge_cmd.py` (118 lines) and `ledger_cmd.py` (137 lines) [E3]

### 2.1 `superclaude review merge` (`merge_cmd.py`)

- Options :22-70: `--ledger`, `--doc` (must exist), `--round` (`IntRange(min=1)`, :40), `--report REVIEWER_ID=PATH` repeated (:43-49), `--resolution` (panel resolution JSON, used only to look up `model` per reviewer, :74-83), `--out`, `--cap` (default 3, :64-70). [E3]
- Flow :71-118: parse `--report` pairs (:85-98) -> read doc -> load ledger if the file exists, else create it only on round 1 with `cap` (:101-108) -> `led.merge_round` (:109) -> `led.render_merged_report` (:110) -> write merged report (:113-115) -> `led.save` (:116) -> print the result JSON without private keys (:117-118). [E3]
- Cap use :102-104: `cap` reaches the ledger only through `new_ledger` on round 1 (D16b). [E3]
- Exit code: the command always exits 0 on a successful merge, including FAIL/ESCALATE; only `LedgerError` becomes a `ClickException` (:111-112). The verdict exit codes live in `ledger verdict`. [E3]
- No telemetry call anywhere in the file (consistent with hand-off D15). [E3]

### 2.2 `superclaude review ledger` (`ledger_cmd.py`)

- `EXIT_BY_DECISION = {"PASS": 0, "REVISE": 10, "ESCALATE": 11}` (:13). [E3]
- `revise` (:36-71): `fnd.parse_fixmap` then `led.apply_revision`; adds `fixmap_ok` to the output (:70). [E3]
- `defer` (:74-91): human command; prints the (possibly rewritten) stored verdict. [E3]
- `verdict` (:94-109): prints `led.verdict` and `sys.exit(EXIT_BY_DECISION[decision])` (:109). [E3]
- `capture` (:112-137): exports `review-capture/1`. [E3]

Key Takeaways
- The CLI is a thin wrapper; all decision logic is in `ledger.py`. A unified panel can keep the CLI shape (merge, revise, defer, verdict, capture, exit 0/10/11) while replacing the merge core. [E3]
- `--resolution` already couples merge to the panel resolution file (model per reviewer); the E2 study reused the product `review-panel-resolution/1` schema for its resolution files (`01-other-branch-study.md` section 2.2), so the panel-to-merge seam exists. [E2][E3]

## 3. Tests that pin current behaviour (`tests/review/test_review_ledger.py`, 566 lines, 24 tests) [E3]

| Test (line) | What it asserts (re-read) | Defect it pins | Must change on purpose if fixed |
|---|---|---|---|
| `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (:376-385) | Round 2 with `rev("t1b-1")` (valid, no findings) and `_broken("t2-1")` (no findings block): `block_ok == {"t1b-1": True, "t2-1": False}` (:383), `warnings` non-empty (:384), and **`status(led)["L1"] == "resolved"` (:385)** | D3 (one valid reviewer is enough) AND D2 (L1 is cleared from `resolved_check` to `resolved` while reviewer t2-1 was invalid). The scope slice lists this test only under D3; the assertion at :385 is the D2 behaviour too. | Yes, both a quorum rule and a D2 fix change :385 (L1 should stay `resolved_check` when an invalid reviewer could have re-found it). |
| `test_missing_anchor_is_kept_without_a_span` (:408-417) | A finding whose anchor is not in the document becomes a row with `span is None`, `status == "open"`, `blocking is True` (:417) | D5 (missing anchor kept silently, can block) | Yes, if missing anchors are demoted, dropped or flagged for re-read. |
| `test_refound_as_nonblocking_stops_failing_the_review` (:518-544) | A single reviewer's nonblocking MINOR re-report sets `row["blocking"] is False` and removes it from `brief_ids` (:544) | D4 un-blocking side (one reviewer un-blocks) | Yes, if blocking becomes a quorum/grader decision. |
| `test_a_late_nonblocking_cluster_cannot_mask_a_blocking_one` (:547-566) | Two clusters of one round match the same row; the row stays blocking (:565) | the `refound` combine rule at `ledger.py:216-218` | Keep (it is a correct invariant). |
| `test_verdict_and_decision_at_rounds_1_to_3` (:277-304) | FAIL/REVISE at rounds 1-2, FAIL/ESCALATE at 3, PASS/PASS on clean doc | `_decision` cap semantics | Keep; add a round-4 refusal test if D16a is fixed. |
| `test_escalate_still_prints_verdict_fail` (:476-490) | At round 3 of 3 the report first line is `review: 3 of 3`, last line `verdict: FAIL`, no Reviser brief, has `## Escalation` | render contract | Keep. |
| `test_round_with_no_valid_block_is_refused_and_changes_nothing` (:345-361) and `test_first_round_with_no_valid_block_is_refused_not_pass` (:364-373) | zero valid blocks -> `LedgerError`, ledger unchanged | the only validity gate today | Keep; a quorum rule generalises it. |
| `test_round_cannot_be_merged_twice_or_out_of_order` (:388-393) | round 1 twice and round 3 after 1 both raise | round sequencing | Keep; there is no test for round 4 after 3 (D16a not pinned). |
| `test_review_cli.py:236` | CLI merge summary `block_ok == {"t1b-1": True, "t2-1": True}` | output shape | Keep if `block_ok` stays in the result. |

No test outside `tests/review/test_review_ledger.py` and `tests/review/test_review_cli.py` references `merge_round`, `review merge`, `review_ledger` or `ledger verdict` (grep over `tests/**/*.py`). No test covers `--cap` on an existing ledger or round 4 (grep of `test_review_cli.py` for `--cap` returned nothing). [E3]

Key Takeaways
- `test_review_ledger.py:385` pins D2 as well as D3; the scope slice missed that. A fix to either defect must rewrite that assertion deliberately. [E3]
- Three tests (:376, :408, :518) encode the "one reviewer decides" model and must change if the unified panel adopts quorum, calibration or a grader. [E3]
- D16 (round 4, cap on existing ledger) has no test either way; a fix adds tests rather than changing any. [E3]

## 4. E2 audit D: the 49 blocking findings lost at merge, and D1 [E2][E3]

Source: `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/analysis/audits/audit-D/<file>` (abbreviated `AD/<file>`). `git ls-tree` lists: `anch.py`, `audit.py`, `audit2.json`, `audit2.py`, `bok.py`, `exclude-list.txt`, `extra.json`, `flags.tsv`, `mk.py`, `run1.txt`, `summary.md`. Evidence date: the study ran 2026-11-11 to 2026-11-13 (row names and SPEC per `01-other-branch-study.md`); model behaviour below is that period's gateway models.

### 4.1 What each script does

- `AD/audit.py` (239 lines): per merged row (`merged-1.md`, `ledger.json`, `resolution.json`) checks panel equality (:54-62), report path and staleness by mtime and `report_sha256` (:70-84), parses the block with its own lenient regex (:17-31, closed fence only, no field validation) and compares raw finding count with ledger members per reviewer (:89-103), blocking consistency member vs raw (:110-118) and row vs members and md table (:134-156), doc sha and round count (:157-168), plus extras (mixed categories, rows without span) (:171-201). Writes `/tmp/audit-D/flags.tsv` (:226-229). [E2]
- `AD/audit2.py` (179 lines): re-implements the product rules. `check` (:8-30) is a copy of `findings._check_finding` returning short reason codes (`anchor>200`, `anchor2>200`, `claim>300`, `refs-bad`, ...); the copy flattens whitespace before measuring (:6, :18-29), matching `findings.py:79-87` (`_check_flat` uses `len(flat(value))`). It copies `locate`, `refs_norm`, `section_of`, the fingerprint and `same_defect` (:40-94) from `findings.py`. For each merge it collects rejected lines with `blocking is True` into `dropped_blk` (:126-129) and records a **verdict flip** when the row-package has dropped blocking findings AND `not any(r["blocking"] for r in led["rows"])` (:113, :133-136). Appends `3-dropped-blocking` flags, EXCLUDE when the merge is a flip (:167-172). It also measures chaining (:139-155). [E2]
- `AD/anch.py` (31 lines): tabulates `(block_ok, kept, anchor1_in_candidate, anchor2_in_candidate)` per raw finding using a raw substring test (:23-26). [E2]
- `AD/bok.py` (44 lines): for every reviewer with `block_ok` false, lists which raw findings are missing from the ledger and their categories (:16-32), to test the old "unpassable-ac category" hypothesis. [E2]

### 4.2 The numbers, re-derived from the committed outputs

- `AD/summary.md:8`: "49 dropped findings were BLOCKING." [E2]
- `AD/flags.tsv` has exactly 49 `3-dropped-blocking` lines (count re-run 2026-11-14). By reason: `anchor>200` 24, `anchor2>200` 14, `claim>300` 10, `refs-bad` 1. So **48 of 49 are the over-length limits of D1 and the last one is the refs limit (`len(refs) > 8` or non-string, `findings.py:111-117`), also listed under D1**. None is a category or severity reject. [E2][E3]
- All dropped findings (blocking or not), `AD/summary.md:16`: anchor >200 56, anchor2 >200 18, claim >300 14, bad severity 3, refs-bad 1 (= 92). Per model (`AD/summary.md:17` and `AD/audit2.json` `drop_model`): luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet/terra/sol 0. These per-model counts are **all** drops, not blocking drops (agrees with `01-other-branch-study.md` H14). [E2]
- Verdict flips: `AD/summary.md:20` names **three**: `g3-sonnet-luna-ember-r3/alias t4-1 F1`, `g5-ember2-luna-r2/alias t4-1 F1`, `n5-sonnet-ember/design t4-1 F1+F2`, all `anchor >200`. `AD/audit2.json` `verdict_flip` has the same three entries. `AD/flags.tsv` has 4 EXCLUDE `3-dropped-blocking` lines because `n5-sonnet-ember` contributes two (F1 and F2). That is the most likely source of the "4 verdicts flipped" in the hand-off and CR:292: 4 dropped-blocking flag lines over 3 flipped merges. The count of flipped verdicts is **3**. [E2]
- Total-loss merges listed separately (`AD/summary.md:20`): 5 reviewer-level cases (`g1-ember-luna2-r4/alias t3-1`, `g7-haiku-luna2-r4/designSpec t4-1` 6/6, `n4-sonnet-ember/design t4-1` 8/8, `h1-...-r2/designSpec t4-2`, `h1-...-r3/designSpec t4-1`). These are not verdict flips because other reviewers in the same merge still had a blocking row. [E2]
- `AD/summary.md:15`: "the merge keeps the parsable lines and drops the invalid ones" — consistent with `findings.py:188-192` (invalid line `continue`s; `ok = False`) and `ledger.py:135-138` (findings kept regardless of `ok`). [E2][E3]
- Unexplained discrepancy: `AD/summary.md:18` kept/raw per model gives haiku 1085/1108 (23 missing) and grok 205/207 (2 missing), while the reason tally gives haiku 7 and grok 1. `AD/summary.md:18` says those counts include stale reports, which may explain it; not resolved here. [E2]

### 4.3 How the loss happens in the product code (trace)

1. Reviewer emits a `findings-v1` line with a quoted anchor longer than 200 flattened characters. [E2]
2. `findings._check_finding` returns "anchor must have at most 200 characters" (`findings.py:104-106` via `_check_flat` :85-86); `parse_block` marks `ok = False`, appends `{line, msg}`, and skips the line (`findings.py:188-192`). [E3]
3. `merge_round` stores `block_ok = False` (`ledger.py:129`), emits one warning with the count and the FIRST message only (`ledger.py:130-134`), and adds no record of which ids were rejected (`ledger.py:141-149`). [E3]
4. If any other reviewer is valid, the merge proceeds (`ledger.py:150`), so the blocking finding never reaches `fnd.cluster` (`ledger.py:165`) and never becomes a row; if no other row is blocking, `_brief_ids` is empty and the verdict is PASS (`ledger.py:273-274`). That is the verdict-flip path. [E3]
5. Even where the merge's stdout was kept, the warning says only the first reason; for 45 merges `merge-stdout.txt` was not kept at all (`AD/summary.md:26`), so the study had to replay the parser to count losses. [E2]

Relation to other defects: the loss is D1 (limit + drop), made verdict-changing by D3 (one valid reviewer is enough) and by the absence of any record of rejected blocking lines; D4 (one reviewer decides) means a surviving single blocker would have been enough to keep FAIL. The 13 blocking rows with null span (`AD/summary.md:30`) are the opposite case (D5): an anchor that does NOT resolve is kept and can block. So length is punished by deletion while non-existence is tolerated. [E2][E3]

### 4.4 Other audit-D results relevant to merge design

- `AD/summary.md:29` (X1): replayed `cluster()` shows 195 chained rows among 1398 ledger rows in total (`audit2.py:139-155`: `rows_total` is incremented at :140 for every row, before the `< 3 members` filter at :145, so 1398 is all rows, not rows with 3+ members; `summary.md:29` wording is [CODE-CONTRADICTED], see file 03 :288), 83 rows have 8+ members or 4+ sections; row anchor/claim = first member only, so one mega row counts as one blocking row and `overlap` confidence is inflated. Hand-off D6. [E2][E3]
- `AD/summary.md:33` (X5): row blocking == any member blocking and verdict FAIL iff a blocking row, 0 violations over 264 merges. The ledger implements its rules faithfully; the defects are in the rules. [E2][E3]
- `AD/summary.md:34` (X6): the "current call only" re-merge rule (`ledger.py:213-218`) was irrelevant at round 1, so E2 gives no evidence about rounds 2-3, D2 or D16. [E2]
- `AD/summary.md:10` (C5): `report_sha256` in the ledger let the audit detect 16 stale merges (report re-run after merge). This field is a reusable integrity check for a unified run manifest. [E2][E3]

Key Takeaways
- All 49 lost blocking findings were rejected by D1 limits (48 length, 1 refs); none by category or severity. [E2][E3]
- Audit D names 3 verdict flips; "4" comes from counting 4 flag lines (n5-sonnet-ember has two). [E2]
- The fix is not only "raise the limit": the merge must record every rejected line (id, reason, blocking flag) in the round entry and must not compute PASS while a rejected line was blocking. [E2][E3]
- `report_sha256` and doc sha checks made the audit possible and should carry into the shared run manifest. [E2][E3]

## 5. Can `merge_round` accept findings-v2 citations? What replaces `annotate(f, doc_text)`? [E1][E3]

### 5.1 Why it cannot today (code facts)

- `merge_round` parses with `fnd.parse_block` (`ledger.py:128`), which looks only for a fence with info string `findings-v1` (`findings.py:124-126`). A findings-v2 report (fence `findings-v2`, `findings_v2.py:24`) yields "no fenced block with info string findings-v1 after the heading" (`findings.py:134-142`), so every v2 reviewer is `block_ok False` and the round raises `LedgerError` (`ledger.py:150-157`). [E1][E3]
- Even if the parse were swapped, `fnd.annotate` dereferences `finding["anchor"]` (`findings.py:349`) while findings-v2 makes `anchor` optional when `citations` is present (`findings_v2.py:122-134`): a citation-only finding would raise `KeyError`. [E1][E3]
- The ledger row view `_view` (`ledger.py:77-83`) carries one `fp`, one `span`, one `span2` and `refs_norm`; `apply_revision` maps those spans through ONE document diff (`ledger.py:315`, `:343-346`, `fnd.opcodes(old_text, new_text)`). There is no per-path structure. [E3]

### 5.2 What the v2 stack already provides in place of `annotate(f, doc_text)` [E1]

- `cluster.annotate(finding, snapshot)` (`cluster.py:126-154`) returns `citations` (each with `role, path, line_start, line_end, status` resolved/unresolved/malformed, `cluster.py:104-116`), a `primary_citation` chosen by lens role (`PRIMARY_ROLES` `cluster.py:67-71`, selection :133-134), `refs_norm` (reusing v1 `refs_norm`, :135-141), `deviation_class`, and a path-aware fingerprint `sha256("v2|role|path||refs|class")` (:119-123, :143-147). Section is always empty because no document text is given (docstring :26-29). [E1]
- `same_defect_v2` (`cluster.py:161-181`): equal fp with non-empty refs, or compatible deviation classes AND intersecting/both-empty refs AND any pair of resolved citations on the same `path` with spans within `SPAN_TOLERANCE = 3` (:72). This is the direct multi-file replacement for v1 `same_defect` (`findings.py:367-379`): it compares across the up-to-8 citations of each finding (`findings_v2.py:128-129`), not one span per document. [E1]
- Missing-anchor analogue: a citation whose path is not in the snapshot is `unresolved` and does not take part in matching (`cluster.py:115`, docstring :21-23); malformed citations are counted (`cluster.py:413`, :429-431). Findings are not dropped. [E1]
- Calibration and support: `cluster_v2` computes `support`, `disputed`, `representative` by highest calibrated confidence, `blocking_any`/`blocking_all`, `chained` (`cluster.py:323-378`) and `cluster_agreement` (:403-412). This answers D4/D6 partly: the representative is the most confident member (not the first), chains are flagged, and disagreement is marked `disputed`. Nothing consumes these for a verdict today (`02-review-cli-code.md` D4 row). [E1]

### 5.3 What a v2-capable merge would need (derived from the code above, not an existing design)

1. Parse with `findings_v2.parse_block` (`findings_v2.py:215-304`) and keep its per-line `errors` in the round entry. [E1][E3]
2. Replace `fnd.annotate(f, doc_text)` with `cluster.annotate(f, snapshot)` plus, for each citation on the reviewed artifact, a line-range existence check against that file's text (cluster.py does not open files; `verify-citations` is the existing command that re-reads cited lines per `02-review-cli-code.md`; its line-existence check is [UNVERIFIED] there). [E1]
3. Ledger rows keyed by citation set: replace `span/span2` with a `citations` list, and `apply_revision` must take a per-path diff map (old/new text per changed path) instead of one `old_text/new_text`. [E1][E3]
4. Row match against existing rows must use `same_defect_v2` over row views that hold citations (today `_view` cannot express that). [E1][E3]
5. A v1 report remains acceptable as a v2 line set with anchor only (`findings_v2.py:3` "A line that findings-v1 accepts and whose keys are all in V1_FIELDS passes check_finding unchanged"), but such a finding has no citations, so `cluster.annotate` gives it no fp and no spans: it can only be a singleton cluster. A unified merge needs an anchor-to-citation step (locate the anchor in the reviewed document and synthesise a citation with role = the lens's primary role) to keep v1 clustering power. The scope slice records no test for anchor-only findings through `cluster_v2` (`02-review-cli-code.md` section 6). [E1][E3]

### 5.4 A stricter loss mode in v2 (important for the D1 fix)

- v2 `parse_block` sets `state = "invalid"` on ANY line error and `ok = (state == "complete")` (`findings_v2.py:299-303`). `cluster._records` treats a dict block as valid only when `state == "complete"` (`cluster.py:220-221`) and `_members` skips every finding of an invalid record (`cluster.py:255-257`). So under v2 a single over-length anchor removes **all** of that reviewer's findings from clustering, not just the bad line. The v1 merge keeps the good lines (`ledger.py:135-138`). Applied to E2's data, the 80 `block ok false` reviewer cases (`AD/summary.md:7`) would all become total-loss reviewers. [E1][E2][E3]
- v2 keeps the same length literals as v1 (`findings_v2.py:111` claim 300, :126/:132 anchor 12-200, :136 anchor2, :80 citation quote 12-200). [E1]

Key Takeaways
- `merge_round` is v1-only at three points: the parser (`ledger.py:128`), `annotate` (`findings.py:349` needs `anchor`), and the single-span row view and single-document revision mapping (`ledger.py:77-83`, `:315`). [E3]
- The replacement for `annotate(f, doc_text)` exists: `cluster.annotate(f, snapshot)` + `same_defect_v2`, which are multi-file by design; what is missing is persistence (ledger rows with citations) and per-path revision mapping. [E1]
- Moving the merge to v2 without changing its block-validity rule would make the E2 loss worse (whole reviewer dropped instead of one line). The unified merge should keep valid lines from an invalid block and record rejected lines. [E1][E2][E3]

## 6. Experiment ledger (installed only): `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py` (2668 lines) [E3-experiment]

Read by ranges only: :1-70 (header, `PROFILES`, constants), :440-530 (state), :794-937 (row schema, anchors, `make_row`, `find`), :1286-1325 (`begin` cap), :1591-1915 (verify, `decide`), :2139-2278 (sweep), :2459-2477 (verdict). Not in `src/`; this is one of the experiment variants installed only in `~/.claude/` (hand-off D14; `02-review-cli-code.md` D14). [E3]

### 6.1 Model: find once, then verify-only

- Module docstring :2-20: "the script-kept finding ledger"; the script is the only writer; models write small JSON inputs or a report with one fenced `ledger-input` block. Exit codes 0 committed / 1 usage / 2 row input refused / 3 state refused / 4 lock conflict; `verdict` exits 0 PASS, 10 CONTINUE, 11 ESCALATE, 12 PENDING (:13-16, `VERDICT_EXIT` :63). [E3]
- Phases `("find", "revise", "verify", "terminal", "swept")` (:61). State keys (:443-458): `profile`, `cap_reviews` from the profile, `round`, `fix_cycles`, `phase`, `seq`, `snapshots`, `decisions`, `ops`, `rows`, `body_sha256`. [E3]
- **Find once**: `cmd_find` (:912-937) runs only in phase `find` and refuses a second find for review 1 (:918-924, `E-PHASE`). Rows come from ONE input (one report's `ledger-input` block), not from several reviewer reports; there is no clustering in this script (grep for `union`, `cluster` and `reviewer` finds only one comment at :1964; rows are appended one-to-one, :928-933). The installed command `~/.claude/commands/sc/spec-panel-ledger.md:259` says "Find: run the full panel over the whole document; each finding becomes one row ... the script, not this session, decides which rows block" — "panel" there is the spec-panel expert personas in one session (`spec-panel-ledger.md:99` "Each expert builds on the context established by previous reviewers"). [CODE-VERIFIED] for one input per find (:912-937). [E3]
- **Verify-only at reviews 2-3**: `check_verify` (:1633-1795) accepts only `{"answers": [...], "new_rows": [...]}` (:1636-1647). Every answer names an existing row; `FROZEN_FIELDS` (:1592-1606: id, grade, rule, wrong_outcome, blocking, anchor, at, finding, ...) cannot be changed (:1669-1675); a row not in this round's plan is `E-ILLEGAL` (:1706-1708); every plan row must be answered (:1752-1754, `E-INCOMPLETE`); evidence must be a quote that occurs in the new snapshot (:1711-1722); `resolved` only for a `fixed` row whose anchor still maps (:1723-1737). New rows must carry a single-occurrence anchor on the new or old side (:1756-1789); a new row inside a changed hunk is `in` scope with `caused_by` the rows that claimed that hunk, otherwise `outside` scope stored `deferred` (:1856-1881). So reviewers at rounds 2-3 do not re-find; they answer the plan and report new defects only in changed text. [E3]
- **Blocking is computed, not reported**: `make_row` (:884-909) sets `blocking = profile["blocking"](row) and scope == "in" and rnd != "sweep"` (:889); non-blocking rows are stored `deferred` (:905). The reviewer's input has no `blocking` key (`ROW_INPUT_KEYS = {"grade", "rule", "wrong_outcome", "anchor", "finding", "label"}`, :64). [E3]
- **`PROFILES`** (:52-59) has exactly one entry, `spec-panel`: grades CRITICAL/MAJOR/MINOR (:38), blocking predicate `_blocking_spec_panel` = `grade == "CRITICAL" or rule in {"FR-8","FR-9"} or (grade == "MAJOR" and wrong_outcome non-empty)` (:41-49), `cap_reviews = CAP_REVIEWS = 3` (:35). The skill doc table agrees (`SKILL.md:46-52`) [CODE-VERIFIED]; it also says two places outside `PROFILES` still name grades (`SKILL.md:52`), consistent with `CM = {"CRITICAL", "MAJOR"}` at :2101 [CODE-VERIFIED]. [E3]
- **Row schema validation** (`validate_rows` :794-848): unknown keys, bad grade, empty `anchor`/`finding`, non-string `rule`/`wrong_outcome`/`label` are refused. There is **no length limit** on anchor or finding. ANY bad row refuses the whole input ("nothing was written", :844-847). `check_anchors` (:851-881) refuses the whole input if any anchor is not found (`E-ANCHOR`) or occurs more than once (`E-ANCHOR-AMBIGUOUS`). [E3]
- **Cap enforced by refusal**: `cmd_begin` (:1300-1311) refuses `E-CAP` when `round >= cap_reviews` or `fix_cycles >= cap_reviews - 1` ("no fourth review and no third fix cycle"). This is the code-level fix for D16a that the master ledger lacks. [E3]
- **Decision** (`decide` :1900-1914): ESCALATE if snapshots are not intact, the plan was not answered, or there are X items (cannot-verify answers, unmappable anchors, failed revert preimages, :490-497); else PASS if `U == 0` (U = blocking, in-scope, status in `open/fixed/reopened`, :474-479); else CONTINUE below the cap; else ESCALATE. [E3]
- **Sweep** (:2139-2278): after a terminal close, one sweep over a prepared copy; sweep rows are always `deferred` (:2251) but record `would_block` (:2253) and `challenges` (a verified row) (:2254); delivery outcome is ESCALATE if the loop escalated, any sweep row would block or challenges a verified row, or tails are not intact; else PASS (:2263-2267). [E3]
- **Verdict** (`verdict_of` :2459-2464): CONTINUE in find/revise/verify, PENDING when terminal before the sweep, else the sweep's delivery outcome. [E3]
- Integrity: `body_sha256` tamper check (`SKILL.md:40` says a hand edit is refused `E-TAMPERED`; [CODE-VERIFIED]: `body_digest` :104, `E-TAMPERED` raised at :342 and :351, checked first at :618), snapshots with sha (:482-487), lock file and `--dry-run` (:18-20, `_DRY` :69). [E3]

### 6.2 Comparison with the master re-find-and-cluster model

| Aspect | Master `ledger.py` [E3] | Experiment `review_ledger.py` [E3] | Reflect v2 [E1] |
|---|---|---|---|
| Rounds 2-3 | full re-review, re-parse, re-cluster, match rows by `same_defect` (`ledger.py:127-171`) | answer plan rows + new rows in changed hunks only (:1633-1795) | no rounds |
| Multi-reviewer | yes, union-find clustering (`ledger.py:165`) | no; one input per find/verify (:912-937) | yes, `cluster_v2` with support (`cluster.py:381-433`) |
| Who decides blocking | any one reviewer's `blocking` flag (`ledger.py:187`, :213-218) | profile predicate over grade/rule/wrong_outcome (:41-49, :889) | `blocking_any` reported; `support`/`disputed` computed, not used for a verdict |
| Bad line | that line dropped, others kept, `block_ok` false (`findings.py:188-192`) | whole input refused, nothing written (:844-847, :1790-1794) | whole block invalid, no findings clustered (`findings_v2.py:299-303`, `cluster.py:255-257`) |
| Anchor not found | kept, span None, may block (`findings.py:349-358`) | input refused `E-ANCHOR` (:855-857) | citation `unresolved`, kept (`cluster.py:115`) |
| Anchor length | 12-200 (`findings.py:104`) | non-empty only (:826-834) | 12-200 (`findings_v2.py:126`) |
| Cap | label only; round 4 merges (`ledger.py:114-118`, :93-96) | refused `E-CAP` (:1301-1311) | n/a |
| Clearing | absence of re-report (`ledger.py:254-258`) | explicit `resolved` answer with evidence quote in new text (:1711-1737) | n/a |
| Exit codes | merge 0; `ledger verdict` 0/10/11 (`ledger_cmd.py:13`) | 0/1/2/3/4 per call; `verdict` 0/10/11/12 (:63) | n/a |

Key Takeaways
- The experiment fixes D2 (clearing needs a positive, evidenced answer), D4 (blocking is a rule over grade/rule/wrong_outcome, not a reviewer flag), D16a (E-CAP) and D16c (verify-only is a code mode), but it has no multi-reviewer merge at all, so it does not address D3 or clustering. [E3]
- Its all-or-nothing input refusal is safe against silent loss (nothing half-written) but requires a retry loop with the model; the E2 study shows long anchors are common (luna, ember, wonder), so a strict refusal would have forced re-asks rather than drops. Whether the E2 models would comply on re-ask is [UNVERIFIED]. [E2][E3]
- `PROFILES` is the right extension point for per-consumer blocking rules (spec, tasklist, reflect, PR review): one entry per profile with grades, a blocking predicate and a cap. Only `spec-panel` exists today. [E3]

## 7. Stoprule computed verdict and the blind finding-grader (installed only) [E3-experiment]

Files: `~/.claude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py` (2050 lines; read :1-22, :401-440, :560-629, :631-960, :1148-1237, grep for `--cap`, exit codes), `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` (15 lines, read whole), `~/.claude/agents/finding-grader.md` (35 lines, read whole). Not in `src/`. [E3]

### 7.1 Data model and flow

- Docstring :2-11: "computed stop rule for the /sc:spec-panel-stoprule review loop"; standard library only; the claim ledger is a fenced ```` ```stoprule-ledger ```` block of JSON lines inside the review report; reviewer lines are `claim`, `prior`, `checked`; every other kind is script-appended (`REVIEWER_KINDS` :29). Exit codes 0 ok, 3 repairable once, 4 HALT at cap, 5 stop on bad input, 6 ledger tampered (:8, :23). [E3]
- `begin` (:401-...): once per report (:406-410); with `--re-review` it requires a valid sentinel from the prior report (:415-420) and refuses with EXIT_HALT when `prior_n >= args.cap` (:423-429) — cap enforced by refusal, `--cap` default 3 (:1940). It also requires `--baseline` (saved copy of the spec the prior review saw) and checks its sha against the sentinel (:432-440). [E3]
- `seal` (:517-628): checks each claim's form (quote occurs, evidence, :303 `claim_issues`); first pass with defects returns EXIT_REPAIR "Fix the listed claims once, then run seal again; the second seal is final" (:579-587). On the final seal each claim gets a `mark` with `form_ok`, `late`, `anchor` (`changed` if the quote touches changed lines, `prior` if linked to a valid prior, else `none` and `late = True` when the ratchet is on, :589-599), plus quote/outcome hashes (:600-613); uncovered hunks are recorded (:614-615). [E3]
- `grade-prep` / `build_batches` (:657-681, :769-786): deterministic batches seeded by `sha256(nonce|review|seal)`; at most 6 form-valid claims per batch plus one blocking and one minor **canary** (:663-674), shuffled; `render_batch` (:721-766) gives the grader the frozen rubric, each claim's `quote`, `span`, `outcome`, evidence tagged `[verified]`/`[unverified]` (:694-705), and in a re-review the baseline text (:708-718). The grader never sees the reviewer's grade label. [E3]
- `apply-grades` (:833-899): `parse_grader_reply` requires exactly the keys `cid, blocking, q2, why` with `why` <= 25 words and a line for every cid (:789-816); `evaluate_reply` rejects the whole batch if any canary is graded wrong (:819-830). First reject -> EXIT_REPAIR, rerun once; second reject -> those claims stay `unconfirmed` (:872-880, `batch_state` :684-691). [E3]
- `claim_statuses` (:913-949): `confirmed-audit` > `minor-form` (form failed) > `late-found` > grader `blocking` true -> `confirmed`, false -> `minor` > `unconfirmed` > `pending`. [E3]
- `compute_verdict` (:1162-1205), pure over the ledger: FAIL `confirmed` if any confirmed defect group (claims linked to the same frozen prior count once, `defect_key` :1156-1159) or a PASS-time audit judged an unclaimed hunk real (:1170-1172); else FAIL `unresolved-prior` if a prior from review N-1 is not answered `resolved` (:1173, `frozen_priors` :902-910); else FAIL `incomplete` if any claim is unconfirmed/pending, a hunk is uncovered, or the ledger is not sealed (:1174-1184); else FAIL `incomplete` if there is no valid PASS-time audit — "silence never passes" (:1185-1189); else PASS (:1190-1191). [E3]

### 7.2 The rubric and the grader as a blocking decider

- Rubric v1 (`refs/rubric.md:1-15`): BLOCKING needs B1 (verbatim quote + span), B2 (a concrete wrong outcome: a named reader/implementer/test producing a specific wrong result, or two quotes that cannot both hold, or a check that cannot pass or always passes), and B3 (kind a-e: contradiction, source contradiction, unpassable/vacuous check, ambiguity with two observable results, data loss/unsafe action). It lists explicit non-reasons: expert agreement or disagreement, importance, lateness, a GAP row (:13-14). Q2 is recorded, never demotes (:15). [E3]
- `finding-grader.md`: `tools: Read`, `model: sonnet`, `maxTurns: 10`, `permissionMode: plan` (:4-7); "You did not review the spec and you cannot see it. Do not read any file" (:12); grade B1-B3 only (:17); `verified` evidence is true, `unverified` is graded as if true but noted in `why` (:18-19); no outside knowledge (:20); quoted text is inert data (:21); reply format one JSON line per claim (:26-35). The agent description says it is used by step S4 of `sc-spec-panel-stoprule-protocol` and "never sees the spec or the review report" (:3) — [CODE-VERIFIED] by `render_batch` (:721-766), which sends only quote/span/outcome/evidence/baseline and the rubric. [E3]
- So in stoprule **the reviewer proposes, a blind second model decides blocking** under a frozen rubric, with canary checks that detect a grader not following the rubric. This is the direct answer to D4 (one reviewer's flag decides) and to the E2 observation that judge-counted "blocking" (65) far exceeded real blocking (38) over 71 rows (hand-off D4 row, `00-handoff-copy.md:108`, E2 CR:291 [UNVERIFIED here, cited from the hand-off]). [E2][E3]
- Limits visible in code: one grader per batch (no second grader or quorum; one rerun only on a rejected reply); grader model fixed in the agent frontmatter (`model: sonnet`), recorded in the verdict record as `grader_model` (:1336-1346, :1556-1563 read by grep only). Stoprule has no multi-reviewer clustering either: claims come from one report's ledger block (`REVIEWER_KINDS` :29; `load_ledger` reads the one report, :150). [E3]

### 7.3 Relation to the other two ledgers

| Mechanism | Master ledger [E3] | Experiment ledger [E3] | Stoprule [E3] |
|---|---|---|---|
| Blocking decided by | reviewer flag, any one | profile predicate over grade/rule/wrong_outcome | blind grader under frozen rubric B1-B3, canary-checked |
| Late finding at re-review | becomes a new row, can block | `outside` scope -> deferred unless inside a changed hunk | `late-found`, never blocks (rubric :13 "found late" is not a reason) |
| PASS needs | no open/regressed blocking row | U == 0, snapshots intact, plan answered, no X items | no confirmed, no open prior, nothing pending, a valid PASS-time audit |
| Cap | label only | `E-CAP` refusal | EXIT_HALT refusal |
| Silence | a reviewer that reports nothing clears `resolved_check` rows (D2) | every plan row must be answered (`E-INCOMPLETE`) | "silence never passes" (:1189) |

Key Takeaways
- Stoprule is the only variant where blocking is decided by an independent model that cannot see the reviewer's grade, and the only one where PASS needs positive evidence (a valid audit). [E3]
- The grader is still a single decider per claim; its correctness is guarded by canaries, not by agreement. A unified panel can reuse it as the "blocking decider" stage after clustering, replacing `any(m["blocking"])`. [E3]
- None of the three ledgers combines multi-reviewer clustering with an independent blocking decision; that combination is what the unified merge would add. [E1][E2][E3]

## 8. Phase-5 bundle caveat: no valid-success verdict exists [E3]

- `.dev/experiments/346-validation/phase5/final-bundle/SNAPSHOT-STATE.txt:1`: "Initial capture at 2026-11-09T02:43:39Z ... This is a preservation bundle in progress, not a final success report." [E3]
- `SNAPSHOT-STATE.txt:3`: diffgate/ponytail repeats are PAUSED for missing owner authorization; four first reviews delivered; "No valid-success verdict is implied."; "A complete program-final design and final design QA remain pending." [E3]
- `.dev/experiments/346-validation/phase5/FINAL-REPORT.md:42` "Convergence not proven; no validated winner"; :75 "None of the completed, measured loops reached a clean PASS. None of the five proposed variants has a valid, repeated convergence result." [E3]
- Per variant (`FINAL-REPORT.md:103-107`, evidence dated 2026-11-08/09 per :40): Ledger 1 loop, new CRITICAL+MAJOR labels 13 / 9 / 3, growth 22.16%, outcome "ESCALATE; sweep FAIL" (:105), and :79 "Ledger's restricted final review listed three new MAJOR findings, with three prior MAJOR labels unresolved; its separate sweep found nine MAJOR findings". Stoprule: 0 completed loops, review 1 only, "6 machine-confirmed blockers from 8 sealed claims", "Invalid provenance check; stopped" (:106). [E3]
- `FINAL-REPORT.md:109`: one flagged-427 final review had "six MAJOR labels but four blocking grades, demonstrating why the two measures must not be substituted for one another" — direct evidence that grade label and blocking decision diverge, which supports a separate blocking decider (section 7). [E3]
- Consequence for this research: the experiment ledger (section 6) and stoprule (section 7) are **designs with partial runs**, not validated mechanisms. Their code properties (refusal on cap, positive clearing, blind grader) are verified by reading code; their effect on loop outcomes is not established by the bundle. Likewise E2 measured first reviews only (`00-handoff-copy.md:144`), so no effort has evidence about rounds 2-3 under a multi-reviewer ledger. [E2][E3]

Key Takeaways
- Treat ledger and stoprule as candidate designs; carry their verified invariants, not claimed outcomes. [E3]
- The only loop-level evidence (FINAL-REPORT.md) shows every variant ended FAIL/ESCALATE; no variant can be cited as the proven verdict model. [E3]

## 9. Synthesis for the unified merge and verdict (derived from the sections above) [E1][E2][E3]

Ownership of each mechanism and where the evidence sits:

| Concern | Best existing piece | Effort | Evidence |
|---|---|---|---|
| Finding contract with multi-file citations | findings-v2 (`findings_v2.py:59-187`) | [E1] | code |
| Cluster with chain flag, calibrated support, representative | `cluster_v2` (`cluster.py:381-433`) | [E1] | code; replay of v1 chaining in E2 audit D X1 [E2] |
| Keep valid lines of an invalid block | v1 `parse_block` + `merge_round` (`findings.py:188-192`, `ledger.py:135-138`) | [E3] | code |
| Record every rejected line | none today (gap) | - | E2 audit D had to replay the parser [E2] |
| Blocking decision independent of reviewer label | stoprule grader + rubric (`stoprule.py:657-899`, `rubric.md`) or profile predicate (`review_ledger.py:41-59`) | [E3] | code; FINAL-REPORT :109 label vs grade divergence |
| Verify-only re-review and positive clearing | `review_ledger.py` verify (:1633-1892) | [E3] | code |
| Cap by refusal | `review_ledger.py:1300-1311`, `stoprule.py:423-429` | [E3] | code |
| Silence never passes | `stoprule.py:1185-1189`, `review_ledger.py:1752-1754` | [E3] | code |
| Integrity (report sha, doc sha, tamper) | `ledger.py:146`, :279; `review_ledger.py:104`, :342-351 | [E3] | E2 audit D C5 used `report_sha256` [E2] |
| Exit-code contract for verdict | `ledger_cmd.py:13` (0/10/11) and `review_ledger.py:63` (0/10/11/12) | [E3] | code |

Conflicts to log (not resolved here):
1. **Bad-line policy**: v1 drops the line and keeps the rest (`findings.py:188-192`); v2 invalidates the whole reviewer (`findings_v2.py:299-303`, `cluster.py:255-257`); the experiment ledger refuses the whole input (`review_ledger.py:844-847`). [E1][E3]
2. **Missing anchor**: kept and can block (v1, `findings.py:349-358`, pinned by `test_review_ledger.py:408-417`); kept as unresolved citation (v2, `cluster.py:115`); refused (`review_ledger.py:855-857`). [E1][E3]
3. **Blocking decider**: reviewer flag (v1); reported but annotated with support/disputed (v2); profile predicate (experiment ledger); blind grader (stoprule). [E1][E3]
4. **Round model**: re-find and cluster every round (master) vs find once then verify-only (experiment ledger, stoprule claims with priors and baseline). [E3]
5. **Exit-code vocabularies**: REVISE (master, `ledger_cmd.py:13`) vs CONTINUE (+ PENDING) (experiment, `review_ledger.py:63`) vs stoprule's 0/3/4/5/6 process codes (`stoprule.py:8`). [E3]

Key Takeaways
- No single existing ledger can be the shared core unchanged; the unified merge needs v2 clustering [E1], v1's partial-keep plus a new rejected-line record [E2][E3], an independent blocking decider [E3], and refusal-based caps and positive clearing [E3].

## Gaps and Questions

1. [CODE-CONTRADICTED] `ledger.py:112` docstring ("A reviewer with an invalid block is skipped for clearing") vs the clearing loop `ledger.py:254-258`, which never reads `block_ok`. Decide which is intended; the test at `tests/review/test_review_ledger.py:385` pins the code, not the docstring. [E3]
2. [CODE-CONTRADICTED] in part: hand-off D4 "`confidence` ... computed but never used". It is not used by any decision, but it is printed in the merged report (`ledger.py:435`, `:473`). [E3]
3. [CODE-CONTRADICTED] by E2 data: hand-off D1 and CR:292 "4 verdicts flipped FAIL to PASS". Audit D (`AD/summary.md:20`, `AD/audit2.json` `verdict_flip`) names 3 flipped merges; `AD/flags.tsv` has 4 EXCLUDE dropped-blocking lines because one merge lost two blocking findings. [E2]
4. Scope slice `02-review-cli-code.md` section 6 lists `test_review_ledger.py:376` as pinning D3 only; its assertion at :385 also pins D2. [E3]
5. Unexplained count gap in E2 audit D: kept/raw per model (`AD/summary.md:18`) implies 23 haiku and 2 grok findings missing, while the reason tally (`AD/summary.md:17`) gives 7 and 1. The summary says kept/raw includes stale reports; not resolved here. [E2]
6. Audit D's "verdict flip" test (`AD/audit2.py:133-136`) infers the reviewer said FAIL from a dropped blocking line; it does not read the reviewer report's own verdict line. Treat "flip" as "the merged verdict would have been FAIL", which is what matters for the ledger. [E2]
7. [UNVERIFIED] E2 "judge 65 blocking vs real 38 over 71 rows" (CR:291) is cited here only through `00-handoff-copy.md:108`; not re-read from the E2 report. [E2]
8. [UNVERIFIED] whether `superclaude review verify-citations` checks that a cited line range exists in the file (needed to replace v1 anchor location in a v2 merge); taken from `02-review-cli-code.md` D5 row, not re-read here. [E1]
9. [UNVERIFIED] whether the long-anchor models of E2 (luna, ember, wonder) would comply with a re-ask if the merge refused over-length lines instead of dropping them (the experiment ledger's all-or-nothing policy). No data in any effort. [E2][E3]
10. No effort has evidence for rounds 2-3 with a multi-reviewer ledger: E2 ran round 1 only (`AD/summary.md:3`, `:34`), the bundle's ledger and stoprule loops were single-session (sections 6-8). D2 and the verify-only design are therefore untested in a panel setting. [E2][E3]
11. Stoprule's `grader_model` recording (`stoprule.py:1336-1346`, `:1556-1563`) was located by grep and outline, not read in full. [E3]
12. Design question for synthesis: which blocking decider should the unified panel use per consumer (rule predicate per `PROFILES`, blind grader, or calibrated support from `cluster_v2`)? The code supports all three; no effort compared them on the same data. [E1][E3]
13. Design question: anchor-only (v1-shaped) findings through `cluster_v2` become singletons (no citations, no fp; `cluster.py:126-154`). A unified merge needs an anchor-to-citation step; no code exists for it. [E1][E3]

## Stale Documentation Found

- **[STALE DOC]** `src/superclaude/cli/review/merge_cmd.py:41` `--round` help "Review number (1, 2 or 3)" while the type is `click.IntRange(min=1)` (:40) and `merge_round` accepts any next round (`ledger.py:114-118`). [E3]
- **[STALE DOC]** `src/superclaude/cli/review/ledger.py:112` docstring on clearing (see Gaps 1). [E3]
- **[STALE DOC]** hand-off `00-handoff-copy.md:105` (D1 row) "4 verdicts flipped FAIL to PASS" — audit D says 3 (see Gaps 3). [E2]
- **[STALE DOC]** `AD/summary.md:2` names `/tmp/audit-D/...` script and flag paths rather than the committed location (also recorded in `01-other-branch-study.md` H21). [E2]
- Hand-off D14 says the ledger skill, `spec-panel-ledger/-stoprule` commands and `finding-grader` agent exist "only as experiment copies under `.dev/experiments/346-validation/phase5/final-bundle/builds/`" (`00-handoff-copy.md:118`); they are also installed and readable at `~/.claude/skills/sc-review-ledger/`, `~/.claude/skills/sc-spec-panel-stoprule-protocol/`, `~/.claude/commands/sc/spec-panel-ledger.md` and `~/.claude/agents/finding-grader.md` (read in sections 6-7). Not wrong about `src/`, but incomplete about where they live. [E3]

## Summary

The master ledger (`ledger.py`) is a faithful implementation of a weak rule set: any one reviewer's flag opens or closes a blocking row, a round passes with one valid reviewer, absence of a re-report clears a fixed row even when the reviewer's block was invalid, and the cap is a label rather than a refusal (D2, D3, D4, D16 all confirmed at current lines; `tests/review/test_review_ledger.py:376-385`, :408 and :518 pin this behaviour, :385 pinning D2 as well as D3). [E3] E2 audit D shows all 49 lost blocking findings were rejected by the D1 length and refs limits (24 anchor, 14 anchor2, 10 claim, 1 refs) and that 3, not 4, merged verdicts flipped to PASS; the loss is silent because the round entry stores only `block_ok`, not the rejected lines. [E2][E3] `merge_round` cannot take findings-v2 today (v1-only parser, `annotate` needs `anchor`, single-span rows, single-document revision mapping); reflect's `cluster.annotate` + `same_defect_v2` are the multi-file replacement, but v2 invalidates a whole reviewer on one bad line, which would worsen the E2 loss. [E1][E3] The installed experiments supply the missing invariants — find-once/verify-only with evidenced clearing and refusal caps (`review_ledger.py`), and a blind, canary-checked grader deciding blocking under a frozen rubric with "silence never passes" (`stoprule.py`, `finding-grader.md`) — but neither merges multiple reviewers, and the phase-5 bundle states no valid-success verdict exists for any variant. [E3]
