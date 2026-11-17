# Research: merge, ledger and verdict semantics (unified Review Panel, run 2, item 2.03)
**Investigation type:** Code Tracer
**Scope:** src/superclaude/cli/review/{ledger.py,ledger_cmd.py,merge_cmd.py}, src/superclaude/cli/reflect/contract.py (derive_verdict), installed variants ~/.claude/skills/sc-review-ledger/ and ~/.claude/skills/sc-spec-panel-stoprule-protocol/, tests pinning these behaviours; scope slices 09, 12, 10, 01
**Status:** Complete
**Date:** 2026-11-14
---

## 0. Method, ground state and numbering

- Repo `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`, branch `ironbelly/shadow-runs`, HEAD `50d4d2b9d1f2288afa497830b3049f2fe48f5c75` (`git rev-parse HEAD`, 2026-11-14) [CODE-VERIFIED]. Slices 09, 12, 10, 01 were read first; every kept claim was re-read in source below.
- Defect numbering: D-1 (clearing loop), D-2 (one valid reviewer passes), D-11 (deferred row never re-opens), D-13 (stored, not derived, verdict) are the IDs of scope slice 09 section G. Slice 01 uses a DIFFERENT numbering for the same family (run-2 hand-off "D2 partial-panel invisible", "D3 docstring vs clearing loop", "D11 revise twice"); its crosswalk is slice 01 section 3.5. In this report "D-n" always means slice 09 numbering.
- Reproductions use only read-only `uv run --no-sync python` / `uv run --no-sync superclaude ...` with `PYTHONDONTWRITEBYTECODE=1`; fixtures and outputs live in `/tmp/review-panel-run2-2.03/` (a copy of `tests/review/fixtures/seeded.md` plus hand-written report files). Nothing was written in the repository.

## 1. Reproductions (open item c) [CODE-VERIFIED by execution]

### 1.1 D-1 clearing loop: `src/superclaude/cli/review/ledger.py:254-258` clears by absence

Code (read): `for row in ledger["rows"]: if row["status"] == "resolved_check" and row["lid"] not in members_by_lid: row["status"] = "resolved"` plus a `cleared` history event. `members_by_lid` is filled from every parsable finding of every reviewer of the round (`ledger.py:135-138`, `:239`), including reviewers whose block is invalid. `block_ok` is read only at `ledger.py:150` and returned at `:295` (grep of `block_ok` in ledger.py: lines 123, 129, 147, 150, 295, 423), so the clearing loop never consults it. The docstring "A reviewer with an invalid block is skipped for clearing but its parsable findings are kept" (`ledger.py:112`) has no corresponding code [CODE-CONTRADICTED docstring vs `:254-258`].

Reproduction (`/tmp/review-panel-run2-2.03/d1.py`), quoted output:

```
== D-1 variant A: 3 reviewers found L1 in round 1; round 2 has ONE other reviewer with an empty block
round1: FAIL REVISE ['L1'] confidence= overlap members= 3
revise: {'resolved_check': ['L1'], 'named_not_touched': [], 'rejected': [], 'unknown': []}
status after revise: {'L1': 'resolved_check'} | stored verdict still: {'verdict': 'FAIL', 'decision': 'REVISE', 'brief_ids': ['L1'], 'round': 1}
round2: PASS PASS cleared= ['L1'] block_ok= {'t4-9': True}
status: {'L1': 'resolved'} history L1: ['opened', 'resolved_check', 'cleared']
== D-1 variant B: ... merged against an UNRELATED doc text
round2: PASS PASS cleared= ['L1'] doc_sha256 stored: 054cfe9c55f4
== D-1 variant C: block_ok false reviewer + valid empty block reviewer
round2: PASS PASS cleared= ['L1'] block_ok= {'t1b-1': True, 't2-1': False} warnings= ["t2-1: findings block problem (1 error(s)), first: heading '## Findings block' is missing"]
```

Reading:
- Variant A: a defect found by 3 of 3 round-1 reviewers (`confidence= overlap`) is cleared, and the round PASSes, because ONE reviewer who took no part in round 1 returned an empty block. Nothing ties the clearing reviewer to the original finders and nothing checks that the reviewer read the revised region.
- Variant B: `merge_round` does not check that `doc_text` is the text `apply_revision` produced; it only hashes it into the round record (`ledger.py:279`). `apply_revision` records no hash of the new text (`ledger.py:301-347`; only `--old` is verified, `:308-314`). A round can therefore be merged against any text and still clear rows (slice 01 "D11 revise twice / new text hash not stored" family).
- Variant C: the invalid-block reviewer (`t2-1`) does not prevent clearing; it only adds a `warnings` entry.
- Panel context: the packaged `@default` re-review resolves ONE reviewer. `superclaude review panel resolve --template @default --env anthropic-only --run-id rr --kind re-review` printed `"review_kind": "re-review"` with one reviewer `t1b-1` (model `claude-sonnet-5-5`); the same template with `--kind first` printed 4 reviewer ids. Code: `panel.py:600` (`if review_kind in panel["apply_to"]` else only the fixed slot). All 8 packaged templates carry `"apply_to": ["first"]` at line 7 (Grep of `src/superclaude/cli/review/data`: reflect-enterprise, live7, reflect-post-x2, reflect-post, reflect-pre, default, reflect-lite, reflect-pre-x2) [CODE-VERIFIED]. So in the standard flow the clearing reviewer is by construction a single reviewer.
- Test pins of the behaviour: `tests/review/test_review_ledger.py:193-217` (`test_cleared_after_the_next_round_and_refound_stays_open`: L1 and L2 `resolved` / `cleared` after a round-2 report by `t1b-1` that mentions only L4), and the CLI round trip `tests/review/test_review_cli.py:274-292` (a single reviewer `t1b-1` in round 2 gives `cleared == ["L1"]`) [CODE-VERIFIED by Read].

Key Takeaways (1.1):
- The only evidence the ledger accepts for "fixed" is a revision hunk touching the span (`ledger.py:331-334`) plus silence in the next round; silence is not proof of coverage.
- The installed variant script `review_ledger.py` replaces silence with an explicit per-row `verify` answer (`result: resolved|open|regressed|cannot-verify`, `review_ledger.py:1829-1853`); the CLI ledger has no equivalent (section 3).

### 1.2 D-2 one valid reviewer passes: `ledger.py:150-157` and `:273-275`

Code (read): refusal only when `not any(block_ok.values())` (`ledger.py:150`); otherwise verdict is `FAIL` iff `_brief_ids(ledger)` is non-empty (`:273-275`); `_brief_ids` returns rows with `blocking` AND status in (`open`, `regressed`) (`:99-104`). The stored round record has keys `brief_ids, decision, doc_sha256, n, reviewers, verdict` and nothing else (printed below): no quorum, no requested/resolved count, no completion state. `grep manifest|reviewers_complete` over `ledger.py` returned no match (negative evidence: the ledger never reads the manifest or its `reviewers_complete` count).

Reproduction (`d2.py`), quoted output:

```
== D-2 A: round 1, 4 dispatched reviewers, ONE valid empty block, three broken -> merge result
verdict/decision: PASS PASS brief_ids: []
block_ok: {'t1b-1': True, 't2-1': False, 't3-1': False, 't3-2': False}
ledger.verdict(): {'verdict': 'PASS', 'decision': 'PASS', 'brief_ids': [], 'round': 1}
any quorum/completion field in round record? ['brief_ids', 'decision', 'doc_sha256', 'n', 'reviewers', 'verdict']
== D-2 C: reviewer-typed severity/blocking decides: CRITICAL with blocking=false from the single reviewer
verdict/decision: PASS PASS brief_ids: [] row.blocking: False severity_max: CRITICAL
report text of the reviewer ended with 'verdict: FAIL' but ledger verdict is PASS
== D-2 D: one reviewer of three flags blocking, two say nothing about it -> still FAIL
verdict: FAIL confidence: single (confidence never read by _decision/_brief_ids)
```

CLI reproduction (scratch dir; `r_empty.md` = valid empty `findings-v1` block, `r_broken.md` = `review: 1 of 3` / `verdict: PASS` with no block):

```
review merge --ledger led1.json --doc doc.md --round 1 --report a=r_empty.md --report b=r_broken.md --report c=r_broken.md --out merged1.md
  -> {"block_ok": {"a": true, "b": false, "c": false}, "brief_ids": [], "decision": "PASS", "verdict": "PASS", "warnings": ["b: findings block problem (1 error(s)), first: heading '## Findings block' is missing", "c: ..."]}
merge exit=0
review ledger verdict --ledger led1.json -> {"brief_ids": [], "decision": "PASS", "round": 1, "verdict": "PASS"}   exit=0
(one failing report)  merge exit=0 ; ledger verdict exit=10  {"decision": "REVISE", "verdict": "FAIL"}
(all reports broken)  Error: round 1 cannot be merged: no reviewer produced a valid findings block ... the ledger was not changed.   merge exit=1; led3.json not created
```

Reading:
- 1 valid of 3 is a PASS with script-facing exit 0 (`merge_cmd.py` ends without `sys.exit`; `ledger_cmd.py:13` maps PASS to 0). 0 valid of N is the ONLY refusal.
- Reviewer-typed inputs decide the verdict: severity CRITICAL with `blocking:false` is accepted (`findings.py:100-101` rejects only MINOR+blocking) and yields PASS. The reviewer's own last line `verdict: FAIL` is ignored: grep of `verdict:|block_ok` over `findings.py, ledger.py, ledger_cmd.py, merge_cmd.py` shows `verdict:` only in rendered output (`ledger.py:485,493`), never parsed. One blocking flag from any one reviewer fails the round however many others are silent; `confidence` (`ledger.py:86-90`) is rendered only (`:435`) and never read by `_decision`/`_brief_ids`.
- Test pin: `tests/review/test_review_ledger.py:376-385` `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` asserts `res["block_ok"] == {"t1b-1": True, "t2-1": False}`, non-empty `res["warnings"]`, and `status(led)["L1"] == "resolved"` [CODE-VERIFIED by Read].

Key Takeaways (1.2):
- "No valid block anywhere" is fail-closed (K-3); "some valid block" is fail-open. A shared core needs a quorum and per-reviewer completion state; `findings_v2` already has `COMPLETION_STATES` (complete, truncated, invalid, failed, timed_out) per slice 09, [UNVERIFIED here: not re-read in findings_v2.py].
- Verdict authority sits with the reviewer's typed `blocking` boolean; the typed `verdict:` line is dead input.

### 1.3 D-11 deferred row never re-opens: `ledger.py:99-104, 235-238, 350-360`

Code (read): a re-find transitions only `resolved_check|resolved -> regressed` (`:235-238`); a re-found `deferred` row keeps its status; `_brief_ids` ignores `deferred` (`:99-104`); `defer()` (`:350-360`) has no status guard, records only `reason`, removes the lid from the LAST round's `brief_ids` and, when that list becomes empty, overwrites the stored verdict AND decision with `PASS`.

Reproduction (`d11.py`), quoted output:

```
== D-11 A: deferred row re-found as blocking next round
round1 verdict: FAIL
after defer (stored verdict patched): {'verdict': 'PASS', 'decision': 'PASS', 'brief_ids': [], 'round': 1} {'L1': 'deferred'}
round2: PASS PASS brief_ids: [] refound: ['L1'] status: deferred blocking: True
history: [{'round': 1, 'event': 'opened'}, {'round': 1, 'event': 'deferred', 'reason': 'accepted risk'}, {'round': 2, 'event': 'refound'}]
== D-11 B: defer has no status guard (resolved row) and no owner/expiry fields
status before defer: {'L1': 'resolved'}
status after defer of a resolved row: {'L1': 'deferred'} history tail: {'round': 2, 'event': 'deferred', 'reason': 'x'}
== D-11 C: defer at the cap flips ESCALATE to PASS
round3: {'verdict': 'FAIL', 'decision': 'ESCALATE', 'brief_ids': ['L1'], 'round': 3}
after defer: {'verdict': 'PASS', 'decision': 'PASS', 'brief_ids': [], 'round': 3}
```

Reading: a deferred row re-found as `blocking: True` in a later round yields PASS with `status: deferred, blocking: True`; the `refound` event is in history but nothing surfaces it. A human `defer` at round 3 turns the stored ESCALATE into PASS. The history entry carries no owner and no expiry.
Test pins: `tests/review/test_review_ledger.py:396-405` (`test_defer_turns_a_blocking_row_into_deferred`: after `defer`, `status == "deferred"`, `verdict == "PASS" and decision == "PASS" and brief_ids == []`, unknown lid raises) and `tests/review/test_review_cli.py:298-313` (CLI defer then `ledger verdict` exit 0, decision PASS). `grep deferred tests/review/*.py` returns only `test_review_ledger.py:396,401` and `test_review_cli.py:313`: NO test re-finds a deferred row (negative evidence for the D-11 re-open case) [CODE-VERIFIED].

### 1.4 D-13 stored verdict is not derived

`ledger.verdict()` returns `last["verdict"]`, `last["decision"]`, `brief_ids` and `n` from the stored round (`ledger.py:363-372`) [CODE-VERIFIED]. Reproduction (`d11.py` tail): after `apply_revision` moved L1 to `resolved_check`, `verdict()` still returned `{'verdict': 'FAIL', 'decision': 'REVISE', 'brief_ids': ['L1'], 'round': 1}` while rows were `{'L1': 'resolved_check'}`. The CLI `ledger verdict` exits 10 in that state (`ledger_cmd.py:13`, `:94-109`).

Key Takeaways (1.3-1.4):
- Three ways to leave the loop without a script-verified clean re-review: silence (D-1), a lone valid reviewer (D-2), and a human `defer` (D-11) that rewrites the stored verdict. All are visible to scripts only as PASS / exit 0.
- The stored verdict is correct only immediately after `merge` or `defer`; `revise` leaves it stale.

### 1.5 Further edge cases run read-only (`/tmp/review-panel-run2-2.03/extra.py`), quoted output

```
== X1: round 4 accepted after ESCALATE at round 3 (only n == len(rounds)+1 is checked)
round3: FAIL ESCALATE
round4: FAIL ESCALATE rounds: 4 cap_reviews: 3
== X2: row whose anchor is missing has span None -> cannot reach resolved_check via a hunk (D-4)
apply_revision: {'resolved_check': [], 'named_not_touched': ['L1'], 'rejected': [], 'unknown': []} status: {'L1': 'open'}
== X3: a typed 'prior' line from the reviewer never changes status (K-4)
round2 status: {'L1': 'resolved'} cleared: ['L1'] history: ['opened', 'resolved_check', 'cleared', 'prior_note']
```

- X1: the cap is enforced only by the decision label (`_decision`, `ledger.py:93-96`) and the order check `n == len(rounds)+1` (`ledger.py:114-118`); nothing refuses a round after ESCALATE. [CODE-VERIFIED]
- X2: a row with no span can never be moved by a fix (`ledger.py:331-339`) and stays blocking until escalation (slice 09 D-4 reproduced).
- X3: the `prior` line (`{"prior":"L1","status":"resolved"}`) is recorded only as `prior_note` (`ledger.py:259-272`); the row became `resolved` through the clearing loop (the reviewer reported no finding for it), not through the prior line. So `prior` really is inert (K-4), but silence still clears.

## 2. Tests that encode defects as intended behaviour (open item a)

Method: each test below was read in this session (Read of the cited lines) and compared with the behaviour reproduced in section 1 or with the code line it exercises. Where I did not read the test, the row is marked [UNVERIFIED] and its source is slice 09 section G/H.

| Defect (slice 09 id) | Test pin | What the test asserts | Status |
|---|---|---|---|
| D-1 clearing by absence | `tests/review/test_review_ledger.py:193-217` | after a round-2 report by `t1b-1` that mentions only L4, L1 and L2 are `resolved` with last event `cleared`, `res["cleared"] == ["L1","L2"]` | [CODE-VERIFIED] pins the defect as intended |
| D-1 (CLI level) | `tests/review/test_review_cli.py:274-292` | a single round-2 reviewer `t1b-1` yields `cleared == ["L1"]` | [CODE-VERIFIED] |
| D-1 + D-2 (invalid reviewer does not stop clearing) | `tests/review/test_review_ledger.py:376-385` | `block_ok == {"t1b-1": True, "t2-1": False}`, warnings non-empty, L1 `resolved` | [CODE-VERIFIED] the known anchor; function name literally says "one valid block is enough" |
| D-11 defer semantics | `tests/review/test_review_ledger.py:396-405`; `tests/review/test_review_cli.py:298-313` | defer flips a blocking row to `deferred` and the stored verdict and decision to PASS; CLI exit 0 | [CODE-VERIFIED] pins defer-rewrites-verdict; NO test re-finds a deferred row (grep `deferred` over `tests/review/*.py`: only `test_review_ledger.py:396,401` and `test_review_cli.py:313`) |
| D-3/D-4 missing anchor kept, no span | `tests/review/test_review_ledger.py:408-417` | row with unmatched anchor has `span is None`, `status == "open"`, `blocking is True` | [CODE-VERIFIED] |
| D-3 anchor flags computed, never consumed | `tests/review/test_review_findings.py:219-230` | `anchor_status == "missing"`, `anchor_ambiguous is True`, span = first occurrence `(0, 1)` | [CODE-VERIFIED]; the flags are asserted only here (slice 09 grep: no production reader) |
| D-6 lower-case / hyphenless ids are not refs | `tests/review/test_review_findings.py:201-212` | `assert "FR-9" not in got  # lower-case ids are not matches` | [CODE-VERIFIED] pins the narrow grammar |
| Reviewer re-classification ends a failure (reviewer-controlled verdict) | `tests/review/test_review_ledger.py:518-546` | a round-2 MINOR/non-blocking re-find of L1 sets `row["blocking"] is False` and removes L1 from `brief_ids` | [CODE-VERIFIED] pins "the current report's classification decides" (comment at `ledger.py:210-212`); the later test `:547-566` pins the opposite protection for two clusters of one round |
| D-5 soft distinctness re-admits | `tests/review/test_review_panel.py:204-214`; `tests/review/test_review_panel_exclusion.py:208-213` | `resolve_slot(["a"], "random", "s", "all", [], exclude=("a",))["model"] == "a"`; live7 in anthropic-only has `_models(res).count(HAIKU) == 6` with the in-file comment "live7 in anthropic-only is 1 Sonnet + 6 Haiku today: soft distinctness re-admits Haiku" | [CODE-VERIFIED] (panel side, outside merge/ledger; listed because it is the same fail-open pattern) |
| D-13 stored verdict | none found: no test asserts `verdict()` after `apply_revision` | negative evidence (grep not run for every spelling; reproduction shows the stale value) | gap |
| D-2/D-1 quorum | none found requiring a quorum; the only refusal tests are `test_review_ledger.py:345-373` (no valid block) and `test_review_cli.py` (merge refuses a round with no valid block, per slice 09 H) | [CODE-VERIFIED] for ledger tests; CLI test line range [UNVERIFIED] here |
| D-25/D-26 (cluster side), D-24, D-16, D-17 | `test_review_cluster.py:233-260`, `:361-401`, `test_review_card_convert.py:405`, `test_review_telemetry.py:201-221` | per slice 09 H | [UNVERIFIED] here: outside my topic (merge/ledger/verdict), not read |

Test-pin summary: 6 of the 8 test pins I read assert defect behaviour as intended (D-1 x3 including the CLI, D-2, D-11, D-3/D-4, D-6, reviewer re-classification). Because they are named as ordinary feature tests ("cleared after the next round", "one valid block is enough"), a fix for D-1/D-2/D-11 will break them and they must be rewritten with the fix, not just deleted (consistent with slice 09 section K).

Key Takeaways (2):
- The defects are not accidental regressions: D-1, D-2 and D-11 were each designed in and tested, with explanatory comments (`ledger.py:112` docstring, the Codex P1 refusal comment at `ledger.py:151-153` and `tests/review/test_review_ledger.py:346`).
- The refusal rule (`any(block_ok)`) came from a review finding "an invalid review must never certify PASS" (`tests/review/test_review_ledger.py:346`), i.e. the fail-closed intent exists but stops at the 0-valid boundary.

## 3. Relation of the installed variant scripts to `cli/review/ledger.py` (open item b; slice 09 gap 1, slice 02 gap 9)

Slice 02 gap 9 reads: "The relation between E3's installed ledger/stoprule/diffgate variants (`sc-review-ledger`, `finding-grader`) and `cli/review/ledger.py` was not read" (`scope/02-run-comparison-and-notes.md:618`). Slice 09 section A flagged the same as [UNVERIFIED]. Resolved here.

### 3.1 Evidence: they re-implement, they do not import or share

| Check | Result | Evidence |
|---|---|---|
| Imports of `review_ledger.py` (2668 lines, `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py`) | stdlib only: argparse, difflib, fcntl, hashlib, json, os, re, sys, tempfile, pathlib | Grep of `^\s*(import \|from )` lines 23-32 [CODE-VERIFIED] |
| Imports of `stoprule.py` (2050 lines) | stdlib only: argparse, difflib, hashlib, json, pathlib, random, re, sys | lines 14-21 [CODE-VERIFIED] |
| Imports of `diffgate.py` (1740 lines) | stdlib only (argparse, contextlib, difflib, hashlib, json, os, re, sys, tempfile, collections, pathlib) | lines 11-21 [CODE-VERIFIED] |
| Any reference to `superclaude`, `cli.review`, `cli/review` | none in any of the three scripts (the only `ledger.py` hits are the string `review_ledger.py` itself, lines 2, 1925, 2271, 2495) | Grep, [CODE-VERIFIED] negative |
| Any shared vocabulary string in installed skills (`sc-review-ledger`, `sc-spec-panel-stoprule-protocol`, `sc-diffgate`, `sc-fix-audit`) or in the 5 installed variant commands | no match for `findings-v1`, `fixmap-v1`, `superclaude review`, `review-ledger/1`, `resolved_check`, `review panel` | Grep over `~/.claude/skills/<4 dirs>/**` and `~/.claude/commands/sc/spec-panel-{ledger,stoprule,diffgate,ponytail,armb}.md`: "No matches found" [CODE-VERIFIED] negative |
| Source of truth for the variants | not in `src/superclaude/` (slice 12 section A: installed-only plus frozen `.dev/experiments/346-validation/phase5/final-bundle/builds/*` copies; the installed `review_ledger.py` was `cmp`-identical to the bundle copy per slice 12) | slice 12 A3-A5, [UNVERIFIED] here (I did not re-run `cmp`) |

Conclusion: [CODE-VERIFIED] the three variants are independent re-implementations. They share only the cap constant 3 (`CAP_REVIEWS = 3` at `review_ledger.py:35`, `diffgate.py` constant per slice 12, `--cap` default in stoprule, vs `new_ledger(doc, cap=3)` at `ledger.py:37`) and the conceptual three-review/two-fix-cycle rule. The CLI `ledger.py`, by contrast, imports `findings.py` (`ledger.py:15`).

### 3.2 They differ in schema, grammar, locator, status machine and verdict authority

| Aspect | CLI `cli/review/ledger.py` (`review-ledger/1`) | variant `review_ledger.py` (`schema 1`) | variant `stoprule.py` | variant `diffgate.py` |
|---|---|---|---|---|
| Input grammar | `findings-v1` JSONL in a fenced block + `fixmap-v1` (`findings.py`) | JSON array / `ledger-input` fenced block per subcommand (`SKILL.md:56-61`) | `stoprule-ledger` fenced block, kinds `claim`/`prior`/`checked` (slice 12 C2) | keyword-at-column-1 lines `PRIOR`/`FINDING`/`FINDINGS none` (slice 12 C3) |
| Locator | quoted anchor 12..200 chars, first occurrence, fingerprint (`findings.py:346-360`) | anchor must occur exactly once in `snapshots/r<k>.md`; refused otherwise (`E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`, `SKILL.md:58`) | `quote` 20..300 unique + `span` (slice 12 C2) | `at=<line>` / `hunk=H<k>.<n>` / `via=` (slice 12 C3) |
| Multi-reviewer merge | yes (`merge_round` clusters across reviewers, `ledger.py:165`) | no reviewer concept: `grep reviewer|quorum|panel|cluster|same_defect|fingerprint` over `review_ledger.py` returns only the `_blocking_spec_panel` name and two prose lines (528, 1964) | none (single reviewer + blind grader) | none (single review per round) |
| State store | JSON file, atomic replace, no lock (`ledger.py:52-67`) | folder with `ledger.json`, `snapshots/`, `diffs/`, `.lock`, `body_sha256` tamper check, `fcntl` lock (`SKILL.md:29-40`; `fcntl` import line 25) | sealed claim ledger inside the report, sha256 chain (slice 12 C2) | `ledger.json` replayed against checks (exit 6 on mismatch) (slice 12 C3) |

Key Takeaways (3):
- Open item (b) answer: re-implement, no import, no shared schema string, no shared grammar; slice 02 gap 9 and slice 09 gap 1 are closed for the three scripts.
- None of the variants is a multi-reviewer panel merge. Their value for a core is the verification discipline (explicit per-row verify, computed verdict, tamper checks, replayed ledger), not a competing merge algorithm. The CLI ledger is the only multi-reviewer merge in the codebase.
- A core cannot "adopt" a variant script by import; it would have to port semantics (section 4) into the single package.

## 4. The two ledger status machines and who types or computes the verdict (open item d)

### 4.1 Status machines

CLI ledger (`ledger.py:19`, transitions read at `:235-238`, `:254-258`, `:331-341`, `:353`):

| From | To | Trigger | Code |
|---|---|---|---|
| (new) | `open` | first finding cluster matching no row | `ledger.py:181-206` |
| `open`, `regressed` | `resolved_check` | `ledger revise` fix map says `applied` AND a hunk touches span or span2 | `ledger.py:330-336` |
| `open`, `regressed` | unchanged (`named_not_touched`) | `applied` but no hunk touches the span (including span None) | `ledger.py:337-339` |
| `resolved_check` | `resolved` | next `merge` round in which NO member of this round matched the row | `ledger.py:254-258` |
| `resolved_check`, `resolved` | `regressed` | re-found in a later round | `ledger.py:235-238` |
| any | `deferred` | human `ledger defer` (no guard) | `ledger.py:350-360` |
| `deferred` | (nothing) | no transition out; re-find keeps `deferred` | `ledger.py:235-238` |

Variant `review_ledger.py` (statuses at `review_ledger.py:508`; `LIVE_STATUSES = {"open","fixed","reopened"}` at `:66`; transitions per `SKILL.md:63-78` and read at `review_ledger.py:1829-1853` and `:1439-1472`):

| From | To | Trigger |
|---|---|---|
| (new) | `open` / `deferred` | `find` (review 1), `verify` new row, `sweep` rows always `deferred` |
| `open`, `reopened` | `fixed` | reviser `answer` claim or auto-claim at `begin` (hunk overlaps the row span) |
| `fixed` | `verified` | `verify` answer `resolved` with evidence quoted from the new snapshot (`:1829-1838`); at the cap an unruled dispute keeps it open (`:1830-1836`) |
| `fixed` | `open` / `reopened` | `verify` answer `open` (`reopened` if ever verified) (`:1839-1845`) |
| `fixed` (once verified) | `reopened` | `verify` answer `regressed` (`:1846-1847`) |
| `fixed` | unchanged, counts in X | `verify` answer `cannot-verify` (`:1848-1850`) |
| `verified` | `fixed` | `begin` when the new hunk touches the row's span (`:1458-1472`) |
| `deferred` | anything | nobody (`E-ILLEGAL`, `SKILL.md:76`); `defer` command only records the user's quote, no status change (`review_ledger.py:2376-2384`) |

Differences that matter for a core:
- CLI: clearing evidence is absence (`resolved_check -> resolved`); variant: clearing evidence is a mandatory per-row answer with a quote that must occur in the new snapshot (`SKILL.md:60`), `incomplete` plan (a row left unanswered) forces ESCALATE (`decide`, `review_ledger.py:1903-1907`: `i_ok` requires every plan row answered; ESCALATE if `not i_ok or x_items`).
- CLI `deferred` is a human-writable exit that rewrites the verdict; variant `deferred` is terminal for the machine (only set at creation for non-blocking, outside-scope or sweep rows) and never hides a CRITICAL/MAJOR: owner counting rule `headline_raw = U3 + W + O`, "a deferred, demoted or outside CRITICAL or MAJOR finding stays counted as open" (`SKILL.md:117`; metrics code `review_ledger.py:2394-2405`).
- CLI has `regressed` as a status; variant has `reopened`. CLI has no `fixed`/`verified` split: `resolved_check` is "claimed fixed by hunk + fix map", `resolved` is "not re-found"; variant `fixed` = claimed, `verified` = checked by a verifier.
- Name collision: both are called "ledger"; the CLI schema is the string `review-ledger/1`, the variant schema is the integer `1` (`review_ledger.py:34`), folder `<doc stem>.review-ledger/`. Same job, incompatible vocabularies (slice 12 B15 [CODE-VERIFIED] again here).
- Neither has a status for "reviewer did not examine this" except the variant's `cannot-verify -> X`.

### 4.2 Reviewer-typed versus script-computed verdict

| Mechanism | Who types what | Who computes the verdict | Fail-closed on missing review? | Evidence |
|---|---|---|---|---|
| Master Review Loop (spec-panel prose) | reviewer types `verdict: PASS|FAIL` as the last line (slice 12 B5) | the reviewer (prose), checked only by the host command's rules | prose fail-closed: "a coordinator treats a re-review report with no prior-findings table, any report whose final `verdict:` line is missing or ambiguous, and any report that cites a finding id absent from its table as `verdict: FAIL`" | `src/superclaude/commands/spec-panel.md:260` [CODE-VERIFIED by Read]. Note the contrast: the CLI ledger ignores the typed `verdict:` line entirely, so the prose fail-closed rule and the script's rule are two different verdict authorities for the same loop |
| CLI `review merge` / `ledger` (`ledger.py`) | reviewer types `severity` and `blocking` per finding; typed `verdict:` line is ignored | script: `FAIL` iff any row with `blocking` AND status open/regressed (`ledger.py:99-104, 273-275`), stored (D-13) | only at 0 valid blocks (`ledger.py:150`) | sections 1.2, 1.4 |
| Variant `review_ledger.py` | reviewer proposes grade, rule, `wrong_outcome` | script: blocking predicate `_blocking_spec_panel` = CRITICAL, or rule FR-8/FR-9, or MAJOR with non-empty `wrong_outcome` (`review_ledger.py:41-49`); loop decision by `decide` (`:1900-1914`); verdict read from state by `verdict_of` (`:2459-2464`) = CONTINUE while in find/revise/verify, PENDING when terminal until the sweep, else `delivery_outcome` | yes: unanswered plan row or `cannot-verify` gives ESCALATE (`decide`) | read |
| Variant `stoprule.py` | reviewer types claims only; "reviewer never writes a verdict" (slice 12 C2); a blind grader decides blocking per claim | script: pure function `compute_verdict(records)` (`stoprule.py:1162-1205`): FAIL `confirmed` if any confirmed group; FAIL `unresolved-prior`; FAIL `incomplete` if any claim unconfirmed/pending, any uncovered hunk, no seal, or no valid PASS-time audit ("silence never passes", comment at `stoprule.py:1189`); PASS only otherwise | yes, strongest of the four | read |
| Variant `diffgate.py` | reviewer types `FINDING` / `PRIOR` lines with `sev`, `at`, `outcome`; prior statuses `resolved|open|regressed|withdrawn` each need keys (`diffgate.py:327-345`) | script: `verdict = "FAIL" if open_blocking else "PASS"` (`diffgate.py:796`); a prior blocker with no `PRIOR` line defaults to `open` (`:754-756`), and an empty change surface keeps prior blockers `open` (`:759-760`) | yes for priors: silence keeps open (the inverse of the CLI ledger's clearing rule) | read |
| Reflect `contract.py` `derive_verdict` (`src/superclaude/cli/reflect/contract.py:138-260`) | an orchestrator (or `ensemble.py`) writes contract fields: `status`, `tier_reached`, `merge_method`, `adversarial_convergence_score`, load-bearing booleans (`contract.py:47-57`) | script: first-match order BLOCKED -> DEGRADED -> HALTED -> PASS (`:146-260`), 14 degraded triggers (`:263-358`), halted triggers (`:361-382`) | yes: missing contract, non-zero rc, missing/major-mismatched version, malformed booleans = BLOCKED (`:161-222`) | read |

Findings on reflect `derive_verdict` as a verdict model:
- It computes a 4-state verdict (PASS 0 / HALTED 10 / DEGRADED 11 / BLOCKED 2: `src/superclaude/cli/reflect/models.py:33-48` [CODE-VERIFIED by Grep]; `commands.py:40-42` per slice 10, [UNVERIFIED] here) from CONTRACT fields, i.e. from typed inputs of the orchestrator. It reads neither findings nor ledger rows; it never reads `merged-verdict.yaml`, `reviewer_cards` or `evidence_validator_ran` (slice 10 S7 field list; `contract.py` lines 104-135 and 138-382 read, no such key present in the functions I read) [CODE-VERIFIED for `derive_verdict`/`_degraded_reason`/`_halted_reason`/`_make_result`].
- Its `DEGRADED` concept ("the audit is untrustworthy because the chain lost a component") is exactly what the CLI ledger lacks for partial panels: D-2 (3 of 4 reviewers invalid) would be `degraded-model-diversity`/`degraded-tier1` territory in reflect but a PASS in the ledger. A core could unify them: ledger verdict = PASS only if quorum met AND no blocking row AND all verification answers present; otherwise DEGRADED (exit 11) rather than PASS.
- Threshold inconsistency: SKILL.md routes convergence >= 0.75 PASS (slice 10 S7, [UNVERIFIED here]) while `contract.py:317-326` degrades at < 0.80 ("low-convergence"); a unified verdict function must pick one.
- The code-driven engine hard-codes contract values (`merge_method` set by reviewer COUNT, `verification_ran: False`, deviation counts default CLEAN; slice 10 S6.2 citing `ensemble.py:772-832`) [UNVERIFIED here: `ensemble.py` not re-read]. So `derive_verdict` PASS on the code engine path rests on defaults, not on measured findings.

Key Takeaways (4):
- Spectrum of authority: CLI ledger (reviewer types `blocking`, script derives, fail-open on partial panel) < diffgate (reviewer types, script validates, silence keeps open) < variant ledger (explicit per-row verify, replay) < stoprule (separate grader decides blocking; computed verdict; silence never passes).
- The two things the CLI ledger most needs from the variants are the inverse default (unanswered means open, not resolved) and a verdict derived from rows on read. The two things the variants lack and the CLI has are multi-reviewer clustering and a panel resolution record.
- Reflect's `derive_verdict` supplies the missing "degraded" state; it is a pure function and can be reused as the verdict shell if its inputs come from the ledger (quorum, completion states, verification coverage) rather than from orchestrator-typed contract booleans.

## 5. Design implications for the verdict and ledger axis (derived only from the verified behaviour above)

| # | Implication | Basis |
|---|---|---|
| I-1 | Clearing must be an explicit per-row answer from a reviewer who is recorded as having examined the revised region; unanswered rows stay open (the variant `verify` rule and diffgate's silence-keeps-open rule, not the CLI's silence-clears rule) | 1.1; 4.1; `review_ledger.py:1903-1907`; `diffgate.py:754-760` |
| I-2 | PASS needs a quorum over RECORDED completion states (requested, resolved, complete); a partial panel yields a DEGRADED-style outcome, never PASS | 1.2; `contract.py:263-358`; `ledger.py:150` |
| I-3 | Derive the verdict from rows on every read; do not store it; `defer` must not rewrite a verdict | 1.3; 1.4; `ledger.py:350-372` |
| I-4 | A deferred row needs owner, reason and expiry, must stay counted as open in the headline (owner counting rule), and a blocking re-find must surface rather than be swallowed | 1.3; `SKILL.md:117` of sc-review-ledger |
| I-5 | The reviewer's typed `blocking` boolean should not be the sole authority: either a script predicate over typed fields (variant ledger / diffgate) or a separate grader (stoprule) | 1.2; 4.2 |
| I-6 | Refuse a round after ESCALATE and a round whose document text is not the revision output (store the new-text hash at `revise`) | 1.5 X1; 1.1 variant B |
| I-7 | Rewrite the pinned tests together with the fix; they are named as features (`test_cleared_after_the_next_round...`, `test_one_valid_block_is_enough...`) | section 2 |

These are implications for the report's design axis, not recommendations of one architecture; the choice between porting variant semantics into `cli/review/ledger.py` and keeping the single-package ledger is left to the report.

## Gaps and Questions

1. [UNVERIFIED] Whether the installed variant scripts are byte-identical to the `.dev/experiments/346-validation/phase5/final-bundle/builds/*` copies: I relied on slice 12 (`cmp` results) and did not re-run `cmp`. Searches tried: Read/Grep of the installed scripts only. This does not affect item (b) (relation to `cli/review/ledger.py`), which rests on the installed scripts themselves.
2. [UNVERIFIED] The variants' own tests (`test_review_ledger_script.py` etc.) live only in the frozen bundle (slice 12 A9), not under `tests/`; I did not read them, so which variant behaviours are pinned (versus merely implemented) is unknown. Search tried: none beyond slice 12; `git ls-files tests` per slice 12 shows none.
3. [UNVERIFIED] Whether the fail-closed `stoprule.py` verdict works live: slice 12 C2 records that the transcript-integrity check failed on a real run (`verify-transcript`, `stoprule.py:1754-1793` per slice 12); I read `compute_verdict` (`stoprule.py:1162-1205`) but did not read `verify-transcript` or the grader path.
4. [UNVERIFIED] `ensemble.py:772-832` hard-coded contract values (merge_method by reviewer count, `verification_ran: False`) were taken from slice 10 S6.2 and not re-read; they matter for how strong a `derive_verdict` PASS is on the code-engine path. Likewise `commands.py:40-42` and the SKILL.md convergence routing (>= 0.75 PASS) are from slice 10 only.
5. Open question: should the shared core adopt the CLI ledger's multi-reviewer clustering with the variants' verification discipline, or leave the variants as research archives (slice 12 lesson L6)? The code shows the two do not interoperate (section 3); the decision is not a code fact.
6. Open question: which reviewer count counts as quorum (all dispatched, 2 of 3, majority)? `manifest.reviewers_complete` exists (slice 09 D5, `_recount`) but `ledger.py` never reads the manifest (grep `manifest|reviewers_complete` over `ledger.py`: no match); the code gives no rule.
7. Open question: who may defer, with what expiry (D-11)? The code allows any CLI caller with no owner field (`ledger_cmd.py` `defer --ledger --lid --reason` per slice 09 B4; the reproduction shows history `{'round','event','reason'}` only).
8. Not reproduced here (outside my assigned topic): D-3 silent anchor drops beyond the read-only X2 case, D-4 beyond X2, D-12 (`annotate` `KeyError` on a citation-only finding; slice 09 marks it `[RUN]`), D-28 (cluster matches only the first row), D-30 (single-document ledger). They are taken from slice 09 as [UNVERIFIED] here except where section 1.5 reproduced a part.
9. Not run: the pytest suite (pytest writes caches; the assignment did not authorise it). The test claims in section 2 are from reading the tests and from reproducing the same behaviour by direct calls, not from a test run.
10. Numbering hazard: slice 09 "D-n" and the run-2 hand-off "Dn" (slice 01) number different things (for example slice 01 D11 = revise twice; slice 09 D-11 = deferred never re-opens). Any consumer of this report must say which numbering it uses.

## Stale Documentation Found

- **[STALE DOC] `ledger.py:112` docstring** "A reviewer with an invalid block is skipped for clearing but its parsable findings are kept": [CODE-CONTRADICTED] by `ledger.py:254-258` and by the reproduction variant C (the invalid-block reviewer's presence neither blocks nor skips clearing; `block_ok` is not read in the clearing loop).
- **[STALE DOC] `ledger.py:351` docstring of `defer`** "The stored decision of the last round is recomputed without it": [CODE-CONTRADICTED] in the sense that the code does not recompute the verdict from rows; it filters `brief_ids` and, only when empty, sets verdict and decision to PASS (`ledger.py:356-360`); a non-empty remaining brief leaves `verdict`/`decision` untouched (a REVISE/ESCALATE label is not recomputed). [CODE-VERIFIED by Read]
- **[STALE DOC] `src/superclaude/cli/reflect/contract.py` header comment cites "SKILL.md:754"** for the `needs_human_decision` invariant (slice 10 S7); the grounding-gaps text sits at SKILL.md L761/L858 now: [UNVERIFIED] here (I did not re-read SKILL.md).
- Slice 12 note [CODE-VERIFIED here only in part]: the variant commands copy the PR #427 base and none mentions `findings-v1`, `superclaude review` or `review panel` (Grep over the five installed variant commands: no match), so the installed variants and the master Review Loop (`spec-panel.md:260-264` plus `document_review_loop_prompts.md`) use disjoint contracts today; a doc saying "the variants extend the master loop" is true only at the level of the 3-review rule.
- Slice 09 statement that the installed variants were "NOT read in this slice [UNVERIFIED whether they duplicate ledger.py logic]" and slice 02 gap 9: resolved by section 3 (they re-implement; no import).

## Summary

The CLI ledger (`src/superclaude/cli/review/ledger.py`) fails open in three reproduced ways: it clears a `resolved_check` row by the mere absence of a re-find (D-1, `ledger.py:254-258`, including by a reviewer who never saw the finding), it lets ONE valid reviewer of N produce PASS and exit 0 (D-2, `ledger.py:150`), and a human `defer` rewrites the stored verdict and never lets a blocking re-find reopen the row (D-11), while the stored verdict goes stale after `revise` (D-13). Tests pin D-1, D-2, D-11, missing-anchor rows, the narrow ref grammar and reviewer re-classification as intended behaviour, so each fix needs rewritten tests. The installed variants (`review_ledger.py`, `stoprule.py`, `diffgate.py`) are stdlib-only re-implementations that share nothing with `cli/review/ledger.py` (no import, no schema string, no grammar); they are single-reviewer loops, but they supply the missing discipline: explicit per-row verification, unanswered-means-open, verdicts computed by script (strongest in stoprule: "silence never passes"). Reflect's pure `derive_verdict` (`contract.py:138-260`) supplies a DEGRADED state that fits the partial-panel hole but takes orchestrator-typed contract fields, not ledger rows.

