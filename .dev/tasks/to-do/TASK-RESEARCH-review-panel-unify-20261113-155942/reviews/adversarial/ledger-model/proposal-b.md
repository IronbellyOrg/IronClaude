# Proposal B: Find once, then verify-only for C13

Side: B. Option: Option B of C-13 (`synthesis/synth-04-options-conflicts.md:851-863`): one panel finds at review 1; later reviews answer the plan of existing rows and report new defects only inside changed text. Prepared 2026-11-14 for the adversarial round on conflict C13 (slug `ledger-model`).

**Citation key.** Paths are relative to `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` unless they start with `src/`, `tests/`, `~/.claude/` or `.dev/experiments/`. `01 §n` ... `13 §n` mean `research/NN-*.md` section n; `web-01 §n` means `research/web-01-panel-aggregation.md`; `S4` means `synthesis/synth-04-options-conflicts.md`. `[CODE-VERIFIED]` means I read the cited lines in this pass on branch `ironbelly/shadow-runs`. `[DOC-SOURCED]` means the number comes from a report, not from re-running anything. `[inference]` means my own reading of code, not run. `[ext]` means an external source, always with its URL. E1 = this session's reflect panel work, E2 = the other session's study read only at commit `4a22d74213f93837d00c2c314075dd967b9a98e3` (written `E2@4a22d74`), E3 = the #346 loop on master and its experiment variants.

## Design

### Position in one paragraph

C13 decides what a review round after the first one is. Option B says: only round 1 searches the whole candidate for defects. Rounds 2 and 3 answer one question per existing blocking row ("is it fixed, still open, or regressed, and here is the quote from the new text") and look for new defects only in the text the reviser changed. Everything that decides the loop (row state, frozen fields, the round counter, the cap, clearing, the verdict) is computed by a script that is the only writer of the ledger. The experiment ledger already implements this design in 2,668 lines with 77 test functions (`~/.claude/skills/sc-review-ledger/scripts/review_ledger.py`; byte-identical to the git-tracked copy under `.dev/experiments/346-validation/phase5/final-bundle/builds/ledger/repo-files/` by `cmp`; test file `tests/skills/test_review_ledger_script.py` in the same folder, 1,578 lines) [CODE-VERIFIED]. B moves that design into the shared core and gives it a first-round merge from pieces other conflicts already decided.

### What B decides and what it leaves alone

B decides the round model: how rows are created, how they change, who may clear them, what a later round may report, and how the loop ends. It does not decide who judges blocking at round 1 (C05), how findings are clustered (C12, decided: one v2 clusterer with complete-link admission), the finding container (C01, decided: v2 container, v1 a strict subset) or bad-line policy (C15, decided: keep valid lines, mark the reviewer partial). B consumes those. Option C of C-13 is B plus an explicit round-1 merge; this proposal gets the same round-1 merge by reference to C05, C12 and C15. A reader who finds B and C indistinguishable is right about everything except one point: B carries no A-style "re-find and cluster" mode as a fallback for rounds 2 and 3, and I argue it should not.

### Core (shared module code)

1. **A ledger state machine, schema `review-ledger/2`, ported from `review_ledger.py`.** Phases `find`, `revise`, `verify`, `terminal`, `swept` (`review_ledger.py:61`); the script is the only writer and models hand over small inputs (`:2-8`); each mutation takes a lock and checks a body hash (`:104`, `body_digest`; `E-TAMPERED` per `SKILL.md:40`); snapshots of the text each review saw are hashed and checked (`:482-487`). The master ledger has none of these: `load` checks only the `schema` string (`src/superclaude/cli/review/ledger.py:41-49`) [CODE-VERIFIED].
2. **Rows frozen at creation.** `id, label, round_found, grade, rule, wrong_outcome, blocking, anchor, at, origin, scope, caused_by, finding` cannot change (`review_ledger.py:1592-1606`, refusal `E-FROZEN` at `:1669-1675`). `blocking` is computed by the lens profile from grade, rule and wrong outcome, never taken from a reviewer (`:41-49`, `:64`, `:889`).
3. **A round-1 find path in `superclaude review merge --round 1`.** Parse each reviewer block keeping valid lines (C15); record every rejected line with id, reason and blocking flag in the round entry (closes D1, which E2 had to replay the parser to count: `E2@4a22d74` `AD/summary.md:19`); flag partial reviewers; require a quorum of valid blocks before a round-1 PASS can be written (D3, `ledger.py:150-157`); annotate each finding to a citation (`cluster.annotate`, `cluster.py:126-154`, cited from 02 §5.2 and not re-read by me, plus the anchor-to-citation step that 02 §5.3 item 5 says no code provides); cluster with the C12 clusterer; run the C05 decider hook; hand the resulting rows to `find`. B does not choose the decider: if C05 stays on the provisional answer, the single-reviewer flag is only a candidate filter and the lens predicate plus the decider fix `blocking` once, at creation.
3a. **No second find.** `find` refuses to run twice for review 1 (`review_ledger.py:918-924`, `E-PHASE`). `review merge --round k` for k of 2 or more is refused with a message that names `ledger verify` (proposed; this is the code mode D16c says is missing, S4 D16 row).
4. **A verify step.** `ledger begin --doc D` snapshots the new text, diffs it against the last snapshot and writes `plan-r<k>.md`: every live blocking row, its frozen grade and wrong outcome, its old anchor and the hunks that touched it (`review_ledger.py:1286-1325`, `check_verify` plan at `:1654-1658`). `ledger verify` takes one answer per plan row plus any new rows, validates everything first, and writes nothing if anything is wrong (`:1790-1794`). An answer carries `result` (`resolved`, `open`, `regressed`, `cannot-verify`), an `evidence` quote that must occur in the new snapshot, and `touched_ok` (`:1591`, `:1607`, `:1711-1722`).
5. **Positive clearing only.** A row becomes `verified` only when a hunk touched it, the verifier answered `resolved`, the evidence quote occurs in the new text and the anchor still maps (`:1723-1737`). A row no hunk touched cannot be re-attacked (`E-NOT-CHANGED`, `:1699-1704`). A plan row with no answer is `E-INCOMPLETE` (`:1752-1754`). Silence never clears and never passes.
6. **New rows only where the text changed.** A new row whose anchor sits inside a changed hunk is `scope=in`, can block, and records `caused_by` (the rows that claimed that hunk); anywhere else it is stored `scope=outside`, `deferred` (`:1856-1881`).
7. **Cap and decision by refusal and by formula.** `begin` refuses a fourth review or a third fix cycle with `E-CAP` (`:1300-1311`). `decide` is: ESCALATE if snapshots are not intact, the plan was not answered, or any item could not be verified; PASS if no live blocking in-scope row is left; CONTINUE below the cap; else ESCALATE (`:1900-1914`).
8. **One sweep after the loop.** `sweep --prepare` copies the accepted text to a folder outside the ledger; a fresh context critiques it; sweep rows are stored `deferred` but recorded with `would_block` and `challenges` (a verified row); the delivery outcome is ESCALATE if the loop escalated, any sweep row would block or challenges a verified row, or tails are not intact (`:2139-2278`, outcome at `:2263-2267`). `verdict` exits 12 PENDING until the sweep has run (`:63`, `:2459-2477`). A profile switch (`sweep: required | none`) lets single-pass consumers skip this step.
9. **A lens profile registry.** The single `PROFILES` entry (`:52-59`: grades, blocking predicate, cap) becomes one table row per lens, adding location kind, id grammar and the sweep switch. This is the extension point 02 §6.2 names and it is the "predicate per lens in data" that C16 already decided.
10. **No new panel kind.** `panel resolve --kind re-review` already resolves only the fixed anchor reviewer (`src/superclaude/cli/review/panel.py:600-605`), and all eight packaged templates have `apply_to: ["first"]` (`src/superclaude/cli/review/data/review-panel.*.json:7`) [CODE-VERIFIED]. B answers the open question in 04 Q13 ("should `kind` gain `verify-only`") with no: `kind` stays the round position.
11. **One re-review protocol.** The v1 `prior` line (`{"prior":"L3","status":"resolved"}`, `findings.py:175-187`) and the experiment's `answers` (`review_ledger.py:65`, `:1591`) use the same three status words. B keeps the `prior` line as the carrier syntax and adds `evidence`, `touched_ok` and the status `cannot-verify`, so the unified v2 container (C01) must accept `prior` lines, which v2 rejects today (`findings_v2.py:279-283`, 01 §2.4, §18 item 9). This resolves item 9 of 01 §18 and the "one re-review protocol" clause in S4 C-13 Option C.
12. **Verdict vocabulary.** The ledger's CONTINUE is exposed as REVISE so the shipped exit codes stay 0/10/11 (`ledger_cmd.py:13`), plus 12 PENDING only for lenses that require a sweep (C19 Option A, decided).

### Consumer modules

| Module | What it does under B | Gate | Change needed |
|---|---|---|---|
| Spec and document review (`/sc:spec-panel` loop) | Rounds 1-3 and one sweep. It is the only in-repo caller of `review merge` and the ledger CLI today (`src/superclaude/rules/prompts/document_review_loop_prompts.md:70`, 09 §7) | Blocking: the CLI exit code | Rules prompt and CLI; the design is already written and built as `/sc:spec-panel-ledger` |
| rf-qa replacement | Lens agents find once; one fix agent; the verification round is `verify`. Its fix-cycle text already says: verify each previous blocking issue, do not recheck minor ones, grade new issues caused by fixes (`~/.claude/agents/rf-qa.md:386-398`) | Blocking | Row locations as `file:section`; monotonicity and regression halts (`rf-qa.md:403-418`) can be computed from row history if C19 Option B is later adopted |
| PR code review | Rows keyed by path and line; `scope=in` is the existing `in_diff` flag; the S2b verifier fits `verify` (10 §1.2 seam B, `fsm.py:941`). Later consumer, fit shown, not designed here | Advisory or route | Multi-path snapshots and per-path diffs (02 §5.3 item 3) |
| Reflect pre and post | Round 1 only: panel resolver, clusterer, citation checks; keeps the debate and contract 1.8.0 (C11, decided). No ledger, as E1 decided (S4 C-13 E1 row, scope/04 line 21) | Per C11 | None |
| Workflow and tasklist | Advisory single pass through reflect (09 §3-4) | Advisory | None |

## How it works

### Data flow

```
ROUND 1 (the only find)
  panel resolve --kind first  ->  N reviewers, fresh context, same code-rendered brief (C10)
  each reviewer report  ->  findings block (v2 container, v1 lines accepted)
  review merge --round 1:
      keep valid lines; record every rejected line (id, reason, blocking flag)   [C15, D1]
      partial reviewers flagged; first-review PASS needs a quorum of valid blocks [D3]
      anchor -> citation; cluster (C12); decider hook (C05)
      rows[] = {grade, rule, wrong_outcome, anchor/citations, finding, label}
  ledger find   ->  profile predicate computes blocking; rows frozen; non-blocking rows stored deferred
  ledger close  ->  decision: PASS | REVISE | ESCALATE (cap 1 of 3 reached only by count)

REVISE (reviewer role, no panel)
  reviser edits the candidate from the Reviser brief
  ledger answer   <- fix map (applied | rejected, reason); applied rows -> fixed only if a hunk touches them

ROUND k = 2, 3 (verify-only)
  ledger begin --doc D   ->  snapshot r<k>, diff against r<k-1>, plan-r<k>.md; refuses past the cap (E-CAP)
  panel resolve --kind re-review  ->  ONE anchor reviewer (panel.py:600-605)
  reviewer answers every plan row + reports new defects in changed hunks
  ledger verify   ->  validate all, then write; any problem writes nothing (E-SCHEMA, E-FROZEN, E-ILLEGAL,
                      E-NOT-CHANGED, E-ANCHOR, E-ANCHOR-AMBIGUOUS, E-INCOMPLETE; order at review_ledger.py:1609-1617)
  ledger close   ->  decision from U, X, I (formula below)

AFTER THE LOOP (profiles with sweep: required)
  ledger sweep --prepare  ->  copy of accepted text; fresh context critiques it
  ledger sweep --input    ->  rows stored deferred with would_block / challenges; delivery outcome computed
  ledger verdict          ->  exit 0 PASS, 10 REVISE, 11 ESCALATE, 12 PENDING (until the sweep ran)
```

The decision formula is the experiment's, unchanged (`review_ledger.py:1900-1914`; written out in the build's design document, `.dev/experiments/346-validation/phase5/final-bundle/builds/ledger/repo-files/docs/designs/spec-panel-ledger.md:59-71`):

```
U = rows with blocking and scope == in and status in {open, fixed, reopened}
X = cannot-verify answers + unmappable anchors + failed revert preimages, this round
I = ledger hash valid and snapshots intact and every plan row answered
decision = ESCALATE if not I or X > 0 | PASS if U == 0 | REVISE if k < cap | ESCALATE
delivery outcome (after the sweep) = ESCALATE if decision == ESCALATE or any sweep row would block
             or challenges a verified row, else PASS
```

The brief for a round k reviewer changes in one clause. Today's RE-REVIEW prompt ends with "Record a severe defect you newly discover even if it is older, and say where it came from" (`src/superclaude/rules/prompts/document_review_loop_prompts.md:48`). Under B the reviewer reports new defects only in changed text; an older defect it happens to notice goes in a new row that the script stores `scope=outside`, `deferred`, and is counted by the sweep step. This is a real policy change and Risks names it.

### Contract fields

| Object | Fields | Source |
|---|---|---|
| Row, frozen at creation | `id, label, round_found, grade, rule, wrong_outcome, blocking, anchor, at, origin (find, changed, outside, sweep), scope (in, outside, sweep), caused_by, finding` | `review_ledger.py:1592-1606`, `SKILL.md:42` [CODE-VERIFIED] |
| Row, mutable (script only) | `status` (open, fixed, verified, reopened, deferred), `mappings, claims, history` | `SKILL.md:42-44, 63-80` |
| Row, proposed additions | `citations[]` (role, path, line range) beside `anchor`; `lens`; `would_block` also on `scope=outside` rows from verify, not only on sweep rows (`:2253`) | proposed; the first is 02 §5.3 item 3 |
| Answer (one per plan row) | `row, result, evidence, touched_ok, reason, dispute_ruling` | `review_ledger.py:1607` |
| New row (verify) | `grade, rule, wrong_outcome, anchor, finding, label, side, parent`; no `id`, no `blocking` | `:1608`, `:64`, `:1760-1761` |
| Round decision | `kind, round, loop_decision, U, X, I, report, tail, tail_sha256, seq` | `:1991-2000` |
| Round reviewer entry, proposed | `reviewer_id, requested_model, launch, served_model, block_ok, partial, rejected[] {fid, reason, blocking}, report_sha256` | today only `reviewer_id, model, report, report_sha256, block_ok` (`ledger.py:141-149`); `served_model` per C08 |
| Lens profile | `grades, blocking predicate, cap_reviews, location kind, id grammar, sweep` | `review_ledger.py:52-59` plus the additions in Core item 9 |

### CLI surface

| Command | Status | What it does | Exit |
|---|---|---|---|
| `review panel resolve --kind first\|re-review` | unchanged | Round 1 panel, round k anchor reviewer | as today |
| `review merge --round 1 ...` | changed | Round-1 parse, annotate, cluster, decide, hand rows to `find`; writes the merged report. `--round` of 2 or more refused, naming `ledger verify` | 0 on success |
| `review ledger begin` | new (ported) | Snapshot, diff, plan; `E-CAP` past the cap | 0, or 3 on refusal |
| `review ledger answer` | new (ported) | Reviser claims from the fix map | 0 / 2 / 3 |
| `review ledger revise` | kept as a shim | Reads `fixmap-v1` (`applied`, `rejected`) and calls `answer` and `begin`, so the loop prompt at `document_review_loop_prompts.md:70` keeps working during the move | 0 |
| `review ledger verify` | new (ported) | Validate all answers and new rows, then write | 0 / 2 / 3 |
| `review ledger close` | new (ported) | Append the script tail to the report, compute the decision | 0 |
| `review ledger sweep --prepare \| --input` | new (ported) | One sweep per loop | 0 / 2 / 3 |
| `review ledger status` | new (ported) | Counts U, X, I, status totals | 0 |
| `review ledger verdict` | changed | Print verdict | 0 PASS, 10 REVISE, 11 ESCALATE, 12 PENDING |
| `review ledger defer`, `capture` | kept | Human park of a row; export | as today |

Refusal exit codes are the experiment's: 1 usage, 2 row-level input refused, 3 state refused, 4 lock or sequence conflict (`review_ledger.py:13-16`, `:62`). Every committed mutation exits 0 whatever the decision, as `review merge` does today (`merge_cmd.py:111-118`).

## Evidence

Nothing below is a measurement that B converges faster or finds more real defects than A. Section D says what was measured and where it stops. The case for B rests on the code (sections A and B), on how the shipped loop and the consumers already work (section C) and on one measured fact about where later findings sit (E-19).

### A. What the master re-find ledger does (what B replaces)

- **E-1. Every round re-finds.** `merge_round` re-parses every reviewer report, annotates every finding against the new text, re-clusters all of them and matches each cluster to an existing row (`src/superclaude/cli/review/ledger.py:127-171`). Source: 02 §1.2. [CODE-VERIFIED]
- **E-2. Clearing is by silence, and a reviewer's explicit answer is not used.** A row in `resolved_check` becomes `resolved` whenever no cluster re-reports it (`ledger.py:254-258`); `block_ok` is never read after `:150`, so an invalid reviewer cannot stop the clearing, and the docstring at `:112` says the opposite. The reviewer's own `prior` lines ("resolved", "open", "regressed") are written to history as `prior_note` events and change nothing (`ledger.py:1-5`, `:259-272`); `test_prior_lines_never_change_a_status` pins that (`tests/review/test_review_ledger.py:318`). Sources: 02 §1.1, §1.4 (D2), 12 §3.1. [CODE-VERIFIED]
- **E-3. Blocking is recomputed from the current round.** A matched row takes `blocking = any(current group)` (`ledger.py:213-218`), so one non-blocking re-report un-blocks a row; pinned by `test_refound_as_nonblocking_stops_failing_the_review` (`test_review_ledger.py:518-544`). Source: 02 §1.4 (D4). [CODE-VERIFIED]
- **E-4. Row matching cannot tell "came back" from "new nearby".** A cluster matches the first existing row for which any member passes `same_defect` (`ledger.py:166-171`), which accepts spans within three lines when requirement refs intersect or are both empty (`src/superclaude/cli/review/findings.py:367-379`); row spans are mapped through the revision diff (`ledger.py:343-346`); a matched row in `resolved_check` or `resolved` becomes `regressed` (`ledger.py:235-238`). [inference, not run]: a defect the reviser's own edit creates within three lines of a fixed row's span matches that row and is booked as a regression of it, with nothing recording that the edit caused it. In E2's round-1 data the same matching rule produced 195 chained rows and 83 rows with 8 or more members or 4 or more sections (`E2@4a22d74` `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/analysis/audits/audit-D/summary.md:29`; the "of 1,398" wording is corrected in 02 §4.4). A re-find model runs that matcher again every round. [DOC-SOURCED for the E2 numbers]
- **E-5. Cap and mode are labels.** `_decision` only picks a label (`ledger.py:93-96`); `merge_round` accepts any next round (`:114-118`); `--cap` reaches the ledger only on round 1 (`merge_cmd.py:101-104`); the `--round` help says "1, 2 or 3" over `IntRange(min=1)` (`merge_cmd.py:36-42`); `merge_round` has no mode argument (`:107`). Source: 02 §1.4 (D16a-c). [CODE-VERIFIED]
- **E-6. The master ledger has no integrity check.** `load` checks only the `schema` string and `save` is an atomic write (`ledger.py:41-67`). [CODE-VERIFIED]

### B. What the experiment ledger does (what B ports)

- **E-7. Find once.** `cmd_find` runs only in phase `find` and refuses a second find for review 1 (`~/.claude/skills/sc-review-ledger/scripts/review_ledger.py:912-924`); rows come from one input and `blocking` is computed by the profile, not reported (`:41-49`, `:64`, `:884-909`). Source: 02 §6.1. [CODE-VERIFIED]
- **E-8. Verify-only is a code mode, with refusals.** `check_verify` accepts only `answers` and `new_rows`; frozen fields cannot change (`:1669-1675`); a verified row no hunk touched cannot be reopened (`:1699-1704`); evidence must occur in the new snapshot (`:1711-1722`); `resolved` needs a row in `fixed` and a mappable anchor (`:1723-1737`); `regressed` needs a once-verified row (`:1738-1742`); every plan row must be answered (`:1752-1754`); new-row anchors must occur exactly once (`:1778-1788`); any problem refuses the whole input and writes nothing (`:1790-1794`). [CODE-VERIFIED]
- **E-9. New rows are scoped by the diff.** A new row inside a changed hunk is `scope=in` with `caused_by` set to the rows that claimed the hunk; otherwise `scope=outside`, stored `deferred` (`:1856-1881`). [CODE-VERIFIED]
- **E-10. Cap by refusal and a computed decision.** `begin` refuses past the cap (`:1300-1311`); `decide` is a formula over U, X, I (`:1900-1914`); `verdict` exits 0/10/11/12 (`:63`, `:2459-2477`). The master ledger refuses nothing of this kind. [CODE-VERIFIED]
- **E-11. A sweep recovers what verify-only does not look at.** One sweep after a terminal close, over a copy; a sweep row that would block, or that challenges a verified row, makes the delivery outcome ESCALATE (`:2139-2278`, `:2263-2267`). [CODE-VERIFIED]
- **E-12. It exists as built, tested code.** 2,668 lines, byte-identical in three places (`cmp`: installed copy, `builds/ledger/repo-files/src/.../review_ledger.py`, `builds/ledger/source/.../review_ledger.py`); 1,578 lines of tests with 77 test functions in `builds/ledger/repo-files/tests/skills/test_review_ledger_script.py`; a design document with measured causes and its own risks at `builds/ledger/repo-files/docs/designs/spec-panel-ledger.md`. All under `.dev/experiments/346-validation/phase5/final-bundle/` and git-tracked. The synthesis calls it "installed only, not in `src/`" (S4 C-13 Option B) and the hand-off's "only in the bundle" is contradicted (S4 header; gaps log D-15); both are true of `src/` and incomplete about the repository. [CODE-VERIFIED for `cmp`, `wc`, `git ls-files`]

### C. How the shipped loop and the consumers already behave

- **E-13. A re-review already uses one reviewer.** `review_kind` not in `apply_to` resolves only the fixed slots with count forced to 1 (`src/superclaude/cli/review/panel.py:600-605`, `:616`); all eight packaged templates have `apply_to: ["first"]` (`src/superclaude/cli/review/data/review-panel.{default,live7,reflect-pre,reflect-pre-x2,reflect-post,reflect-post-x2,reflect-lite,reflect-enterprise}.json:7`); the loop prompt says "one reviewer for a re-review by default" (`document_review_loop_prompts.md:70`). Sources: 04 line 255, 09 §7. [CODE-VERIFIED] The consequence: the multi-reviewer clustering that Option A keeps in rounds 2 and 3 is exercised, in the shipped configuration, on a single report.
- **E-14. The shipped re-review already asks verify questions.** The RE-REVIEW prompt has the reviewer decide each prior blocking finding as resolved or regressed against the AFTER text (`document_review_loop_prompts.md:44`), re-check each as "resolved, open or regressed" (`:48`) and write one `prior` line per prior blocking finding (`:61`). B turns that prompt text into a checked protocol and adds the evidence quote. [CODE-VERIFIED]
- **E-15. Almost no code depends on the current shape.** The merge and ledger CLI has one in-repo caller, the rules prompt at `document_review_loop_prompts.md:70`; `panel resolve`, `cluster`, `verify-citations` and `manifest` are called only by reflect shadow steps (09 §7; S4 D14 row). The tests that touch the ledger are `tests/review/test_review_ledger.py` and `test_review_cli.py` (02 §3). [CODE-VERIFIED via 02 and 09 greps]
- **E-16. The rf-qa fix cycle is verify-only in prose.** For each blocking issue of the previous report, verify the fix was applied and is correct; flag and grade new issues the fix introduced; "Do not recheck minor findings from the previous report; they stay recorded as notes"; two fix cycles then halt (`~/.claude/agents/rf-qa.md:386-402`). Of 41 rf-* review call sites, 32 depend on an in-place fix step and the common shape is lens agents, consolidate, one fix agent, verify (10 §3). The core exposures X8 (review kinds beyond first and re-review) and X9 (fix-agent hand-off) are the same pieces (10 §5). [CODE-VERIFIED for `rf-qa.md`]
- **E-17. The PR flow has the same scope rule.** The auggie rubric drops a tier only for a pre-existing finding outside the diff (`severity-rubric.md:94-96`); the router has an `in_diff` flag and the S2b verifier is per finding (`fsm.py:806-826`, `:941`) (10 §1.1, §2 row D-a). B's `scope=in` and `scope=outside` are the same split; the fit is shown here, not designed. [CODE-VERIFIED via 10]
- **E-18. Reflect is single-pass and stays off the ledger.** E1's position is that reflect is single-pass, the ledger is path-blind (bare span, one `doc_sha256` per round) and `--cap 1` would record ESCALATE for every blocking round (S4 C-13 E1 row; scope/04 line 21; MR:273 per scope slice, [DOC-SOURCED]). C11 is decided: keep the debate and contract 1.8.0. B changes nothing in reflect.

### D. Measured evidence, and where it stops

- **E-19. Later findings sit in changed text.** In the controlled #346 comparison, 89% of new findings at review 2 and 100% at review 3 in the treatment arm carry `origin=changed`, meaning they sit on lines the previous fix changed; "A fresh whole-document review after a fix keeps finding fix-induced defects whatever the reviser adds" (`.dev/experiments/346-validation/phase4/AB-REPORT.md:30`). Limits stated by that report: n = 2 + 2 on one scenario (`:40`), and the origin tag is read from reports in one arm and re-derived in the other, so the shares are not compared as numbers (`:30`). The ledger design document records the same finding for review-3 blockers in two traced runs (design doc `:75`, [DOC-SOURCED]). [E3, DOC-SOURCED]
- **E-20. No loop reached a clean PASS.** Ten completed loops (the historical incident, two controls, two exact-427, two with flags, diffgate, ponytail, ledger) all ended FAIL or ESCALATE (`.dev/experiments/346-validation/phase5/FINAL-REPORT.md:75`, table `:96-105`). "None of the five proposed variants has a valid, repeated convergence result" (`:75`). The re-find controls ran 11/9/8 and 12/7/4 new CRITICAL+MAJOR labels at reviews 1/2/3 (`:97-98`); the ledger arm ran 13/9/3 (`:105`). By the experiment's own screen the ledger arm's improvement of 3 is smaller than the control spread of 4 (`:135`), so this is not evidence for B. [E3, DOC-SOURCED, dated 2026-11-08/09]
- **E-21. What the ledger arm showed about its own weak spot.** The loop closed with three open blocking rows and ESCALATE; the later sweep found nine MAJOR findings, several challenging text the loop had marked verified; the report's own heading for the arm is "accounting works; restricted verification misses substantive residuals" (`FINAL-REPORT.md:154-158`, counts `:116-120`). The final reviewer's model changed (`:199`) and the sweep had no control sweep (`:158`). [E3, DOC-SOURCED]
- **E-22. The design document names its own risks.** "Apparent convergence by not looking" (design doc `:217`); frozen first-pass grades (`:218`); an answer with a quote "proves the text was opened, not that it was judged well" (`:233`); the sweep costs about 10 to 15 minutes more per loop and a loop is 13 to 17 script calls, both stated as estimates, not measured (`:211-213`). [E3, DOC-SOURCED]
- **E-23. E2 measured round 1 only.** All 264 merged packages use ledger round 1 only (`E2@4a22d74` `AD/summary.md:3`); the "current call only" re-merge rule "was irrelevant at round 1" (`:34`); row blocking equals any member blocking with 0 violations over 264 merges, so the master ledger implements its rules faithfully (`:33`). E2 therefore gives no evidence about rounds 2 and 3, D2 or D16 for either option. What it does show for B's round-1 path: 49 blocking findings were dropped by length and refs limits and the loss was silent (`:8`, `:19-20`; 02 §4.2), which is why Core item 3 records every rejected line. [E2@4a22d74, DOC-SOURCED]
- **E-24. E1's shadow runs show what agent-written state costs.** Stage 2 failures were orchestrator contract-writing and file-placement lapses: three unparseable contracts, a header copied from the harness, `merged-verdict.yaml` at the nested path, extra top-level keys (S4 C-20 evidence bullet 3, citing 07 §5.1). That is an analogy for why B has the script, not the model, write ledger state; it is not a test of B. [E1, DOC-SOURCED]

### E. External context (not re-fetched in this pass; as recorded and graded in `research/web-01-panel-aggregation.md`)

- **E-25. A missing vote must not default to an answer.** 366 incorrect programs, 14 validators: true-positive rate above 96%, true-negative rate typically below 25%; a super-majority rule that defaults to "invalid" on a missing vote did slightly worse (arXiv 2510.11822v2, https://arxiv.org/html/2510.11822v2; web-01 §1.4; preprint). It maps to D2 and D3 and to B's `E-INCOMPLETE`. [ext]
- **E-26. One run of one model misses a lot, so absence is weak evidence of a fix.** 294 human-confirmed issues across 33 artifacts: no model exceeded about 61% code recall, 56.8% of confirmed defects were found by exactly one model, and the second reviewer was the largest coverage step (https://zenodo.org/records/21328807; web-01 §3.4; self-published, reliability LOW to MEDIUM, code artifacts not specifications). It supports a multi-reviewer round 1 and makes "the reviewer did not re-report it" a poor clearing rule. [ext]
- **E-27. A panel of N is fewer than N votes.** Nine judges gave about two effective votes and the best single judge matched or beat the panel (https://arxiv.org/html/2605.29800v1; web-01 §2.2; preprint). It argues against paying for a panel on rounds 2 and 3. [ext]
- **E-28. Production systems carry findings across runs and verify singletons.** Cursor Bugbot dedupes against bugs posted in earlier runs (https://cursor.com/blog/building-bugbot; web-01 §3.1); LinkedIn passes single-model findings back for verification instead of dropping them (https://www.linkedin.com/blog/engineering/ai/high-signal-ai-code-review-that-adapts-to-your-codebase-at-scale; web-01 §3.3). These support carrying rows across rounds and verifying them; they do not choose between A, B and C (S4 C-13 evidence, last bullet). [ext]

## Correctness argument

Correctness here means: the loop stops, it never reports PASS on a review that did not happen or on a row nobody checked, a row's blocking status cannot change by accident, and what the loop did not look at is recorded. Each property below names the evidence it rests on.

**P1. No silent pass, and a stop that is computed.** PASS requires I (hash and snapshots intact, every plan row answered), X = 0 and U = 0, all computed by the script (E-8, E-10). An invalid answer set is refused and nothing is written (`review_ledger.py:1790-1794`), so a round that did not produce a valid answer set stays in `verify`; it cannot become PASS. The master ledger can PASS on one valid reviewer while another reviewer's block was invalid (D3, `ledger.py:150-157`, `:273-274`, E-2) and writes a verdict that is only a label at the cap (E-5). External support for refusing instead of defaulting: E-25.

**P2. Identity and blocking are stable after round 1.** After `find`, no clustering step touches a row: its id and the thirteen frozen fields cannot change (E-8), and only `status` moves, through the script's transition table (`SKILL.md:63-80`). Two defects of the re-find model cannot occur by construction: one reviewer's non-blocking re-report un-blocking a row (E-3), and a nearby new defect being matched to an old row by the three-line rule (E-4). A new defect in a changed hunk gets its own row with `caused_by` naming the rows that claimed the hunk (E-9); it is a fix-induced defect and is recorded as one.

**P3. Clearing needs evidence about the new text.** A row leaves the blocking set only if (a) a hunk touched its span, (b) the reviser's claim moved it to `fixed`, (c) the verifier answered `resolved` with a quote that occurs in the new snapshot, and (d) the anchor still maps (E-8), or a human defers it. Silence is `E-INCOMPLETE`. This is the fix the synthesis itself proposes for D2: "clearing needs a positive answer in the verify-only protocol" (S4 D2 row, line 1357). Option A's minimum fix (an invalid reviewer cannot clear) leaves clearing by the silence of a valid reviewer, and a single run of one model misses a large share of defects (E-26), so that rule clears rows that were never checked. B's evidence rule does not prove the verifier judged well (E-22), but it proves the verifier was shown the touched text and had to quote it, and the quote is stored.

**P4. The surface a later round may widen is bounded, and the rest is recorded.** Later rounds may add blocking rows only inside changed hunks. Everything else is stored `scope=outside`, `deferred`, and one sweep over the accepted text can still escalate the delivery outcome (E-9, E-11). How much this gives up depends on where later findings sit: in the treatment arm of the controlled comparison, 89% of new findings at review 2 and 100% at review 3 were on lines the previous fix changed (E-19). B does not rely on that number for safety (n = 2 + 2, tags read from reports); it relies on it only for how little the restriction costs.

**P5. Fail closed on bad input.** A refusal costs a retry, not a wrong state. Proposed rule, not in the experiment script: a refused answer set gets the refusal list back and one re-ask; a second refusal is recorded as an X item, which makes the decision ESCALATE (`review_ledger.py:1906-1907`). Two code paths already behave this way for related cases: `cannot-verify` becomes an X item (`:1848-1850`), and stoprule repairs once and then stops (`stoprule.py` per 02 §7.1; not re-read).

**P6. It composes with what is already decided.**
- C01: the `prior` line is the carrier for answers, so v1 stays a strict subset of the v2 container (Core item 11).
- C02 and C15: round 1 keeps valid lines and records every rejected one. The all-or-nothing refusal in B applies to verify answers, not to finding lines, because a missing plan answer is silence while a bad finding line is one lost finding. These are different cases and the decided policy for lines is untouched.
- C16: the blocking predicate per lens is the `PROFILES` row (`review_ledger.py:41-59`).
- C19: one machine verdict in the core, 0/10/11 plus 12 only where a sweep is required; each module maps it to advisory or blocking.
- C11 and E1: reflect stays on the debate and 1.8.0 and does not call the ledger (E-18).

**Comparison with Option A after its fixes (S4 C-13 Option A: D2, D3, D16 fixed).**

| Property | A, fixed | B |
|---|---|---|
| Clearing a fixed row | Absence of a re-report by valid reviewers | Positive answer with a quote in the new text; silence refused |
| Row identity across rounds | Re-clustered and re-matched every round | Frozen ids; new rows only from changed hunks, with `caused_by` |
| Blocking bit | Recomputed from the current group each round | Frozen at creation by the lens predicate |
| Cap and round order | Refusal added by the A fixes | Refusal by construction (`E-CAP`) |
| Verify-only | Prompt text (D16c) | Code mode |
| Late finding | New row in any round, may keep the loop open | In a changed hunk: may block. Elsewhere: deferred and swept |
| Whole-candidate recall in rounds 2-3 | Yes, every round | No; one sweep after the loop |
| Several reviewers in rounds 2-3 | Supported by the merge | Not supported (one answer set per round); the shipped config uses one reviewer (E-13) |
| Reuse | `ledger.py`, `merge_cmd.py`, `ledger_cmd.py`, 24 tests | Built script and 77 tests, but a new ledger schema and a port |
| Effort | M | XL |

### The weakest point

B gives up whole-document recall in rounds 2 and 3 to buy a loop that can end, and I have no measurement that the trade is good. The only run of this design (E-21) ended with three open blocking rows and ESCALATE, and its sweep then found nine MAJOR findings, several against text the loop had marked `verified`. So `verified` means "the verifier was shown the touched text and quoted it", not "the text is correct", and a first-pass blocking grade that is wrong is frozen (E-22). The ledger arm's improvement over the controls did not pass the experiment's own screen (E-20), the final review changed models, and the sweep that compensates for the blind spot has no control sweep. What B offers instead of better measured outcomes is that its failure modes are visible and bounded (U, X, I, deferred rows, a sweep outcome) where A's are silent (clearing by silence, un-blocking by one reviewer, a fourth round). Visible and bounded is not the same as better, and B should be adopted as the default only if the test below does not show it worse.

**A falsifier, stated before the run.** On the E2 ground-truth packages (the quality regression set that C20 Option C already proposes), with the same models, the same reviser and the same cap, compare A (with D2, D3 and D16 fixed) with B: known blocking defects still open at delivery, fix-induced defects found, outside-hunk findings that only the sweep found, review rounds used, refusals and retries, and tokens. Apply the experiment's own screen: an effect counts only if it exceeds the larger within-arm spread (`FINAL-REPORT.md:87`). If B leaves more known blocking defects open at delivery than A, the remedy I would propose is a profile switch that lets outside-hunk rows that would block count toward the decision. That is a change inside B, not a return to re-find. It is unmeasured and I do not claim it works.

## Risks and mitigations

| # | Risk | Why it is real | Mitigation | Residual |
|---|---|---|---|---|
| 1 | Recall lost in rounds 2-3; a wrong first-pass grade is frozen; a "verified" row is not a correct row | E-21 (nine sweep MAJORs, some against verified rows), E-22 (design doc `:217-218`, `:233`) | The sweep is mandatory for blocking consumers (the build's owner decision 6: "The sweep is never skipped", design doc `:18`); the reviser dispute and verifier ruling path lets a frozen grade be challenged inside the loop (`review_ledger.py:1624-1630`, `:1825-1827`); proposed: record `would_block` on outside rows found during verify, as sweep rows already do (`:2253`), and report them in the merged report; the falsifier above | Real. This is the weakest point and the test, not the argument, has to settle it |
| 2 | The older-defect clause changes: today's RE-REVIEW prompt says to record a severe defect found even if older (`document_review_loop_prompts.md:48`) | A defect noticed outside the changed text is stored deferred, not blocking | Owner decision, named in the prompt; deferred rows listed in the merged report; the sweep scores them. The policy origin is the build's measured cause "fresh whole-document re-review after each fix" (design doc `:81`) | A severe old defect surfaces at the sweep, with no fix cycle left; design doc open question 6 recommends a second ledger only on the user's word (`:251`) |
| 3 | Reviewers fail the answer protocol and the loop stalls on refusals | The design doc lists "stalls on refusals" (`:222`); the protocol has seven refusal codes (`review_ledger.py:1609-1617`); only one loop of this design has run (E-21), with a changed final model (`FINAL-REPORT.md:199`); long anchors are common for some models (luna 27, ember 24, wonder 5 anchors over 200 in E2's dropped lines, `E2@4a22d74` `AD/summary.md:17`) | `--dry-run` lets the reviewer check an input without writing (`review_ledger.py:18-20`); the refusal detail lists every line where an ambiguous anchor occurs (`:864`); one re-ask, then ESCALATE (P5, proposed); at round 1 long anchors are truncated at the merge boundary under the decided C02 rule, so `find` never sees the 200-character problem | Compliance at scale with several model families is untested. Whether the E2 long-anchor models would comply with a re-ask is unknown (02 gaps item 9) |
| 4 | Round 1 depends on C05 and C12, and B freezes whatever round 1 decides | `blocking` is frozen at creation (`:1592-1606`); S4 C-05 cites E2 for 65 judge-blocking against 38 real for the single-reviewer veto (I did not re-read that figure at the E2 commit; 02 gaps item 7 marks it UNVERIFIED) | The decider hook runs before `find`, so a better decider needs no ledger change; the human `defer` and the dispute path remain; until C05 is decided the veto is a candidate filter and the lens predicate is the only blocking rule | A wrong round-1 decision is expensive to undo inside the loop |
| 5 | XL port and a single-document design | 02 §6.2: no multi-reviewer merge and one document per ledger; 02 §5.3 item 3: per-path diffs do not exist | First consumer is the single-document spec loop, the only in-repo caller (E-15); schema 2 keys snapshots by path from the start; PR and rf-qa modules wait for multi-path support | The multi-file part is new work that A also needs (02 §5.3) |
| 6 | Reviser-side machinery is document-specific: claims, auto-claim by paragraph, `--revert-unclaimed` | `cmd_answer` and its checks span `review_ledger.py:940-1285` and `cmd_begin` `:1286-1590`, about 650 lines; reverting text needs consent (design doc `:15`, open question 2 at `:247`) | Port `answer` and `begin` for the document lens only; `revert-unclaimed` stays off unless the invocation carries the consent flag; other lenses take claims from the fix map only | The auto-claim leak (a minor edit inside a blocking paragraph is admitted, design doc `:220`) comes along |
| 7 | Schema change breaks old ledgers and prompt pins | `load` rejects any other `schema` string (`ledger.py:47-48`); text pins in `test_review_rules_text.py:34-42, 65-73` and `test_review_loop_extension.py:49-55` | New schema `review-ledger/2` fails loudly on old files; `ledger revise` shim; keep the `prior` example line in the rules file so the token pins hold (Test coverage) | [UNVERIFIED] whether any ledger files exist outside the repository |
| 8 | A consumer wants a panel at round k | A second `verify` for the same round is refused `E-PHASE` (`review_ledger.py:1804-1810`); the code has no merge of several answer sets | The coordinator concatenates disjoint answer sets before `verify` (the rf-qa 1+1 verification case: each verifier answers the rows of its lens); proposed conflict rule: any `open` or `regressed` wins. Untested, and the first consumer does not need it | If a consumer needs overlapping verifiers, B needs new design |
| 9 | Served-model drift inside a loop | E-21: ponytail's and the ledger arm's final reviewer ran on a different model than requested (`FINAL-REPORT.md:199`); the same drift was seen in E1 (11 §11) | Record requested, launch and served model per round (C08, decided); flag a round whose served model differs from the anchor | Detection, not prevention |
| 10 | B and C are close, so the decision may be argued over a name | S4 C-13 Option C = B plus a round-1 unified merge | State it: B does not keep a re-find fallback. If the adversarial round prefers C's wording, the code is the same | None for the design; a naming point for the synthesis |

## Test coverage needed

### Existing tests that change on purpose

`tests/review/test_review_ledger.py` has 24 tests (names and lines read in this pass). Nine pin the re-find model and are replaced; fifteen are kept with the status vocabulary renamed (`resolved_check` to `fixed`, `resolved` to `verified`, `regressed` to `reopened`; 16 lines in the file contain the old strings by grep count).

| Test | Pins today | Under B |
|---|---|---|
| `test_review_ledger.py:193` `test_cleared_after_the_next_round_and_refound_stays_open` | Clearing by silence, then a re-find reopens | Replace: a row clears only through `verify` `resolved` with a quote in the new text; silence is refused |
| `:220` `test_refound_resolved_row_becomes_regressed_and_fails`, `:255` `test_regressed_row_re_resolves_through_the_same_path` | Regression by re-find | Replace: a `regressed` answer on a once-verified row gives `reopened`; then fix and verify again |
| `:318` `test_prior_lines_never_change_a_status` | A prior line is inert | Reverse for round 2 or later: a `prior` line with an evidence quote is an answer and changes status through the script; a prior line with no evidence, or naming a row not in the plan, is refused |
| `:376-385` `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` | D3 and D2 together (12 §3.1) | Split into a round-1 quorum test (D3) and a round-k "silence is refused" test (D2) |
| `:408-417` `test_missing_anchor_is_kept_without_a_span` | D5: a missing anchor becomes an open blocking row | The merge step demotes it to a deferred row with a warning naming the finding id (C02); `find` never receives an unresolved anchor |
| `:493` `test_refound_row_takes_the_current_finding_span` | Re-anchor on a re-find | Replace by span mapping through the diff in `begin` |
| `:518-544` `test_refound_as_nonblocking_stops_failing_the_review` | One reviewer un-blocks (D4) | Replace: `blocking` is frozen; an answer or row carrying `blocking` is `E-FROZEN` |
| `:547-566` `test_a_late_nonblocking_cluster_cannot_mask_a_blocking_one` | The same-round `refound` combine rule | Retire; there is no re-match after round 1 |
| Kept, vocabulary renamed: `:116, :139, :153, :184, :277, :307, :345, :364, :388, :396, :420, :432, :442, :476, :505` | Round 1 rows, membership, revision guards, verdict at rounds 1-3, no-valid-block refusal, order, defer, capture, atomic save, merged report, escalate render | `:277-304` keeps FAIL/REVISE/ESCALATE and the exit codes (C19) |

Other files:
- `tests/review/test_review_cli.py:196` (merge, revise, verdict round trip) and `:328` (verdict exit codes) change: round 1 through `merge`, later rounds through `ledger begin`, `verify`, `close`; exit 12 appears for sweep lenses. `:425` (no valid block refuses and writes nothing) is kept.
- `tests/review/test_review_rules_text.py:34-42` and `:65-73`: keep by leaving the `INS_B` line and the example `{"prior": "L3", "status": "resolved"}` in the rules file and adding a second example line that carries `evidence` and `touched_ok`. If the example line moves, these pins change in lockstep.
- `tests/skills/test_review_loop_extension.py:49-55` pins the fail-closed bullet ("a re-review report with no prior-findings table", "cites a finding id absent from its table"); keep it true by defining the prior-findings table as the answers to `plan-r<k>.md`. `:120-127` forbids the words parser, script, state machine, transcript and asynchronous in the command's `## Review Loop` section: the protocol text goes in `document_review_loop_prompts.md` and the CLI, not in that section.
- Unchanged and used as the regression gate: the panel tests and goldens (the `re-review` kind and `apply_to` do not change), and the 271 legacy reflect tests that 12 says no unification should change (12 §8 key takeaway).

### New tests

1. **Port** `test_review_ledger_script.py` (77 functions) to the package module: tamper and lock (`:290-344`), replay (`:319`, `:837`), the three-review loop and cap (`:1126`), verify refusals (`:948`, `:1289`), sweep (`:1359-1425`), help and refusal-code documentation checks (`:1529-1575`, adapted to the CLI).
2. **Round-model guards:** `review merge --round 2` is refused naming `ledger verify`; a second `find` is `E-PHASE`; `begin` after review 3 is `E-CAP`; `--cap` on an existing ledger is an error (closes D16a and D16b, which no test covers today, 12 §4).
3. **D2 both ways:** a silent valid reviewer leaves the row `fixed` and the round is refused `E-INCOMPLETE`; `resolved` with a quote that occurs in the new snapshot gives `verified`; a quote that does not occur gives `E-ANCHOR`.
4. **Frozen fields:** an answer carrying `grade`, `blocking` or `anchor` is `E-FROZEN`; a new row carrying `id` is `E-FROZEN`.
5. **The E-4 scenario as a characterization pair:** on `tests/review/fixtures/seeded.md`, fix a row, then have the reviser's edit introduce a defect two lines from the fixed row's span. First pin what `merge_round` does today (the row is booked `regressed`); then assert that B stores a new row with `caused_by` naming the fixed row. This turns an [inference] into a test result before the synthesis relies on it.
6. **Round-1 hand-off:** clusterer output becomes `find` rows; the round entry lists every rejected line (id, reason, blocking flag) for an over-length anchor and a bad severity; a partial reviewer is flagged; the quorum boundary (k-1 valid blocks cannot write PASS, k can).
7. **Container compatibility:** the v2 parser accepts a `prior` line, with and without `evidence` and `touched_ok` and with `cannot-verify`; a v1-to-v2 round trip of one report gives the same rows (C01; today v2 rejects `prior` lines, `findings_v2.py:279-283`).
8. **Profiles:** a lens with `sweep: none` never reaches PENDING; verdict exit codes 0/10/11/12 per profile; an unknown lens is refused.
9. **Outside rows (proposed):** `would_block` is recorded for outside rows found at verify and appears in the merged report and the sweep outcome.
10. **Re-ask rule (proposed):** the first refusal returns its list; a second refusal is an X item and the decision is ESCALATE.
11. **Answer-set concatenation (only if adopted):** disjoint sets are accepted, overlapping sets refused, `open` or `regressed` wins.
12. **Provenance:** requested, launch and served model recorded per round (C08); a mismatch against the anchor is flagged.
13. **Migration:** `load` refuses `review-ledger/1` with a message that names the migration; the `ledger revise` shim yields the same row states as `answer` plus `begin` on a fix-map fixture.
14. **Text tests:** the rules file's RE-REVIEW prompt names the plan answers, the evidence quote and the changed-text-only clause; the command's Review Loop section still contains none of the five banned words; a guard that no reflect module imports the ledger (E-18).
15. **The falsifier run** (not a unit test): the A-versus-B comparison on the ground-truth packages described under Correctness argument. It needs the portable runner that C20 Option C already asks for (committed `source.md`, no `/tmp` paths); until that runner exists the run cannot be done and B's adoption as the default stays conditional.

## Cost

**Engineering.** The synthesis rates Option B XL and High risk (S4 C-13 Option B); Option A is M and Medium. I do not dispute either rating. What is different from the synthesis's reading is that B is mostly a port, not a new build.

| Item | Size | Source |
|---|---|---|
| Existing and built: the ledger script | 2,668 lines; about 650 of them (`:940-1590`) are reviser-side claim, admission and revert logic that only the document lens needs | `review_ledger.py` function starts [CODE-VERIFIED] |
| Existing and built: tests | 1,578 lines, 77 functions, plus fixtures under `tests/skills/fixtures/review-ledger/` | `builds/ledger/repo-files/tests/skills/` [CODE-VERIFIED] |
| Existing and built: design document, SKILL.md, `/sc:spec-panel-ledger` command | design doc 256 lines; command 475 lines (09 §2.4) | bundle; `~/.claude/commands/sc/` |
| Master code B replaces for rounds 2 and later | `ledger.py` 494, `merge_cmd.py` 118, `ledger_cmd.py` 137 lines; `test_review_ledger.py` 566 lines, 24 tests | `wc -l` [CODE-VERIFIED] |
| New work 1: multi-path snapshots and per-path diffs | Not in the script; also needed by A (02 §5.3 item 3) | 02 §5.3 |
| New work 2: round-1 hand-off from clusterer and decider into `find` | Depends on C05 and C12 | S4 |
| New work 3: lens registry, replacing the single `PROFILES` row | Small | `review_ledger.py:52-59` |
| New work 4: move from a skill script (`uv run --no-project python <skill base>/scripts/review_ledger.py`, `SKILL.md:16`) into click commands under `superclaude review`, so installed primitives reach it through the CLI as the project rules require | Medium | `SKILL.md:13-19`; project CLAUDE.md rule on installed primitives |
| New work 5: `ledger revise` shim, rules-prompt edits, command text, docs | Small to medium | Test coverage above |
| New work 6: test migration | 9 replaced, 15 adapted, 77 ported, 14 new groups | Test coverage above |

**What B costs that A does not.** A larger port; a schema break with a shim; two owner decisions (the changed-text-only rule for rounds 2 and 3, and the consent flag for reverts); a sweep session on every loop (about 10 to 15 minutes more, estimated by the build's author and not measured, design doc `:213`); and about 13 to 17 script calls per loop (also an estimate, `:212`).

**What B saves.** No clustering after round 1. The reviewer's task in rounds 2 and 3 is narrower (plan rows and hunks, not the whole candidate), which should reduce tokens per round. It does not reduce reviewer count, because the shipped re-review already uses one reviewer (E-13). No token or time measurement exists for either option, so none of this is counted as evidence.

**Order of work, as dependencies and not a roadmap.** The round-1 fixes that both options need (record rejected lines, keep valid lines, a quorum for the first review) come first. Then port the verify path for the document lens only, the one in-repo caller. Then switch the loop prompt. Then run the falsifier. Multi-path support, the rf-qa module and the PR module come after that, in that order of need (design doc `:253` gives the same order: rf-qa after spec-panel, reflect later).

**Decisions this proposal asks of the owner.** (1) Accept that rounds 2 and 3 report new blocking defects only in changed text. (2) Accept a mandatory sweep for blocking consumers. (3) Authorize the falsifier run and treat its result as binding on whether B stays the default.

