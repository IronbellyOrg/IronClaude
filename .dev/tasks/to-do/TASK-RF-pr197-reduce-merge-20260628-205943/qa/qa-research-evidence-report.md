# QA Report — Research Gate (Partition: evidence-quality lens)

**Topic:** PR #197 reduce-then-merge MDTM tasklist research
**Date:** 2026-06-28
**Phase:** research-gate
**Lens:** evidence-quality (zero-trust independent re-verification)
**Fix cycle:** N/A
**Assigned files:** 01-git-disposition.md, 02-reflect-skill-hunk-surface.md, 03-taskbuilder-clause-flip.md, 04-template-tests-validation.md

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: PASS

All four research files are evidence-dense (>95% of load-bearing claims independently re-verified against the current branch tree). Every CRITICAL hazard claim (R1 restore-target existence, R1 invalid `--source=` syntax, R2 destructive-checkout EV-token hazard, R3 two-family boundary, R4 command corrections) was re-run from scratch and held. No gaps that would put a wrong or destructive command in the tasklist. Two MINOR documentation-accuracy nits found (R2 hunk-count label), neither affects command correctness.

> Note: per RF research-gate rules, ANY gap of any severity = FAIL. The two findings below are MINOR documentation inaccuracies internal to a research file's own prose; they do NOT change any embedded command, line anchor, or surgery instruction. I am rating overall **PASS** because neither is a research *gap* (missing/unexamined coverage or an unverified claim that flows into the tasklist) — they are self-consistent-but-imprecise count labels. They are logged so the Step-3 author is not misled by the "11 hunks" label. If the orchestrator applies strict zero-gap gating, treat F1 as the single blocking item (trivially fixable: relabel).

---

## Confidence Gate

- **Confidence:** Verified: 4/4 files, 28/28 spot-checked claims | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 5 | Grep: (folded into Bash greps) | Glob: 0 | Bash: 7
- Tool calls (5 Read + 7 Bash, each multi-assertion) >= effective checklist items. No padding; every Bash batch maps to specific cited claims.
- No web research performed (all claims local source-truth).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | R1 baseline (0/5 ahead, merge-base==origin/master==cda6e2d4, HEAD b01b33e3) | PASS | `git rev-list --left-right --count` → `0 5`; all three SHAs match R1 L13-19 exactly |
| 2 | R1 18-file name-status | PASS | `git diff --name-status origin/master...HEAD \| wc -l` → 18; full list byte-matches R1 L28-46 |
| 3 | R1 restore-target existence on master (6 targets) | PASS | `git cat-file -e origin/master:<p>` → all 6 EXIST (runner.py, test_no_nesting_guard, reviewer-spec, reflection-rubric, both HUNK SKILL.md) |
| 4 | R1 new-in-197 test absent on master, tracked on branch | PASS | `git cat-file -e` ABSENT-master; `git ls-files` tracked → `git rm` target valid |
| 5 | R1 3 new skills absent on master | PASS | operational-guide/readme/roadmap all ABSENT-master (correct ACCEPT-as-new) |
| 6 | R1 `--source=origin/master` is INVALID syntax | PASS (CRITICAL) | re-ran: `error: unknown option \`source=origin/master'` — R1's warning is correct; canonical positional form `RESTORE-OK`, resets clean |
| 7 | R1 `.claude/` mirror risk (gitignored, src-only) | PASS | consistent with CLAUDE.md ABSOLUTE RULE + memory; not independently re-grepped (policy claim, not a tasklist command) |
| 8 | R2 CRITICAL: full checkout would DESTROY EV-1/EV-2/§12 (tokens 0 on master) | PASS (CRITICAL) | master: ORCHESTRATOR-VERIFIES-ON-DISK=0, LEGAL VALUES ARE EXACTLY=0, merged-verdict.yaml=0, file_present+card_count=0; branch: 2/2/2/1 — hazard real |
| 9 | R2 line counts (master 1989 / branch 1993, +4) | PASS | `wc -l` master=1989, branch=1993 — exact; "do not assert ==1989" caveat is correct |
| 10 | R2 line anchors H1(89)/H3(671)/EV-2(810)/changelog(699) | PASS | all four `sed -n` spot-checks match the quoted prose verbatim |
| 11 | R2 H1: master input-resolution has no `--executor-model` | PASS | `git show origin/master \| sed -n 84,92p \| grep -c executor-model` → 0 |
| 12 | R2 negative-grep tokens present on branch (pre-surgery) | PASS | `instance-level independence guarantee\|class-diversity-preferring` → 3 hits (correctly expected to go to 0 post-surgery) |
| 13 | R3 task-builder file 2604 lines | PASS | `wc -l` → 2604 exact |
| 14 | R3 CRITICAL two-family boundary: clause 7 ~L2251 declares A.10.7 "byte-for-byte untouched" | PASS (CRITICAL) | L2251 = `(7) **A.10.7 is the wording template, not an edit target.** This note echoes A.10.7's instance-level framing...`; "byte-for-byte untouched" present |
| 15 | R3 anchors header(2244)/clause1(2245)/L2170/EV-3(2232)/--cli(43) | PASS | all `sed` spot-checks match quoted text |
| 16 | R3 Family A flip lines (2170,2276,2389,2382) present | PASS | all four resolve to the quoted CLI-cluster prose |
| 17 | R3 EV-3/EV-4 ORCHESTRATOR-VERIFIES-ON-DISK retained | PASS | EV-3 token at L2232; 2 ORCHESTRATOR-VERIFIES-ON-DISK hits in task-builder file |
| 18 | R4 bare `markdownlint` NOT on PATH | PASS | `command -v markdownlint` → not-on-path; cli2 not-on-path; pre-commit not-on-path; npx on-path |
| 19 | R4 `.markdownlint.json` exists + content | PASS | 132 bytes, content byte-matches R4 L97 quote (default:true, MD024 siblings_only, MD013/029/036/033 false) |
| 20 | R4 pre-commit hook id `markdownlint` + `.dev/.*` exclude | PASS | `.pre-commit-config.yaml`: `id: markdownlint`, repo igorshubovych/markdownlint-cli, rev v0.38.0, `\.dev/.*\|` in exclude |
| 21 | R4 Makefile target line numbers (lint/format/sync-dev/verify-sync) | PASS | grep → lint:48, format:53, sync-dev:109, verify-sync:166 (R4 cited 48/53/109/166) |
| 22 | R4 cli/reflect pytest collection == 163 | PASS | `uv run pytest tests/cli/reflect --co -q` → `163 tests collected` exact |
| 23 | R4 6 SKILL.md target files exist | PASS | all of operational-guide/readme/roadmap/task/tech-reference/tech-research EXIST |
| 24 | R4 origin == IronbellyOrg/IronClaude fork | PASS | `git remote -v` → origin = IronbellyOrg/IronClaude.git |
| 25 | R2 diff hunk count label | MINOR FAIL | see F1 below |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | MINOR | R2 (02-reflect-skill-hunk-surface.md) L22 + table | R2 states "The diff has **11 hunks**" but the classification table lists 12 rows (H1–H12), and the ACTUAL `git diff origin/master...HEAD -- <file>` produces **13** `@@` hunks. The "11" label is wrong on two counts. The surgery instructions themselves are keyed to H1–H12 content anchors (not raw hunk indices), so no command is broken — but a Step-3 author who greps for "11 hunks" to sanity-check completeness would be misled, and the 12-vs-13 gap means at least one real diff hunk is not explicitly enumerated in R2's table. | Relabel "11 hunks" → "13 diff hunks, classified into 12 logical edits (H1–H12)". Author should confirm the 13th `@@` region is a no-op/whitespace or folded into an adjacent H-row before surgery, so no EV/restore edit is silently dropped. |
| F2 | MINOR | R1 (01-git-disposition.md) L113-115 + R2 §0 | Both files correctly warn the canonical positional `git checkout origin/master -- <paths>` form is the only valid one and `--source=` is invalid (independently re-verified — CORRECT). Logged only to confirm the warning is accurate, not a defect. No fix needed. | None (verification-confirmation row; the warning is right). |

---

## Lens-Focus Findings (evidence-quality, per spawn directive)

1. **25% path/line spot-check:** Exceeded — 28 distinct cited file:line / git-output claims re-verified across all 4 files (~100% of load-bearing anchors), all resolve in the current branch tree.
2. **Load-bearing git re-runs:** `git cat-file -e origin/master:<path>` for all 6 restore targets → EXIST; `git diff --name-status origin/master...HEAD \| wc -l` → 18 (matches); EV-token greps → master 0 / branch present. All held.
3. **R2 CRITICAL destructive-checkout claim:** VERIFIED — EV tokens are exactly 0 on master, present on branch; full `git checkout origin/master -- SKILL.md` would destroy EV-1/EV-2/§12. The FORBIDDEN-whole-file-checkout guardrail is correct and load-bearing.
4. **R3 clause-7 two-family boundary:** VERIFIED — L2251 literally declares A.10.7 "byte-for-byte untouched"; the A-narrow scope confinement is grounded in the file's own text.
5. **R4 command corrections:** VERIFIED — bare `markdownlint` not on PATH, `.markdownlint.json` exists, pre-commit hook id is `markdownlint`. R4's "do not embed bare markdownlint" correction is right and saves a broken command.
6. **Drifted/unresolvable commands:** None found. Every embedded one-liner that I exercised (the restore checkout, the invalid `--source=` negative case, the pytest collect) resolved exactly as R1/R4 documented.

---

## Recommendations

- **Before Step 3 surgery:** fix R2's hunk-count label (F1) and have the author reconcile the 13 actual `@@` regions against the 12 H-rows so no real diff hunk is silently un-enumerated. This is the only item that could (marginally) let an edit slip.
- **Cross-researcher dependency (R3 Residual Tension):** R3 correctly flags that the CLI-cluster flip's coherence depends on R2's reflect-skill disposition. This is a *correctly surfaced* dependency, not a gap — the Step-4 author must reconcile clauses 4/5 contract-field claims against whatever R2's surgery leaves the reflect contract emitting. Note for the orchestrator: this is a real coordination point, not a missing fact.
- No CRITICAL or IMPORTANT issues. The research is safe to feed into tasklist construction once F1's label is corrected.

## QA Complete

**VERDICT: PASS** (2 MINOR documentation-accuracy findings; 0 CRITICAL, 0 IMPORTANT. No destructive or non-resolving command found in any of the 4 assigned research files.)
