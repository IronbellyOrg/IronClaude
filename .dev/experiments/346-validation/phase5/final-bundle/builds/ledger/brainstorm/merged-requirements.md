---
topic: "Issue #346 theme LEDGER: finding ledger with separate find and verify phases"
domain: architecture
adversarial_status: partial
adversarial_status_reason: "diff-point convergence 1.00, but the Round 2.5 invariant gate was BLOCKED by 9 HIGH items (depth standard has no Round 3); the refactor plan maps each to an applied change, and the merged text was not re-probed"
convergence_score: 1.0
base_variant: "sonnet:analyzer"
source: nested/adversarial-1/merged-output.md
---

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (sonnet:analyzer) -->
<!-- Merge date: 2026-11-08T15:53:25Z -->
<!-- Source tags: "Change #N" refers to adversarial/refactor-plan.md; INV ids refer to adversarial/invariant-probe.md; orchestrator decision ids (D1 to D11) named in Source tags are the refactor plan's binding inputs. All three are external to this spec. -->

# Spec: finding ledger with separate FIND and VERIFY phases (issue 346, theme LEDGER, merged)

<!-- Source: Base (original, modified): title says "merged" instead of "variant 2, analyzer" because this document combines three variants -->
Design only. Nothing here is implemented. Variant command: `/sc:spec-panel-ledger`, additive next to the unchanged `/sc:spec-panel`.

<!-- Source: Base (original, modified): alias BR added per Change #2; the notes on merged citations and on decision numbers added so every reference in this spec resolves or is marked external -->
Citation aliases (all read in this session; `W` = `/home/coder/workspaces/worktrees/IronClaude`): `SP` = `W/bs346-ledger/src/superclaude/commands/spec-panel.md`; `DES` = `W/bs346-ledger/docs/designs/spec-panel-review-loop.md`; `QA` = `W/bs346-ledger/src/superclaude/skills/sc-implement-protocol/refs/qa.md`; `RFQA` = `W/bs346-ledger/src/superclaude/agents/rf-qa.md`; `AB`, `ARMB`, `DEC` = `AB-REPORT.md`, `ARMB-REPORT.md`, `DECISIONS.md` under `W/exp346-p1-logs/.dev/experiments/346-validation/` (`phase4/` for the first two); `F2R2`, `F2R3`, `F2D1`, `F2D2` = `spec-panel-round2.md`, `spec-panel-round3.md`, `disposition.md`, `disposition-round2.md` under `W/exp346-ab-flg-r2/.dev/orca-command-refactor/review/`; `C1R2`, `C1R3` = the same round reports under `W/exp346-ab-ctl-r1/.dev/orca-command-refactor/review/`; `HIST` = `W/exp346-ab-flg-r2/.dev/orca-command-refactor/specs/history/`; `BR` = `W/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/task-text/` (the S1 brief texts, opened read-only by the invariant probe). Anything I did not open is marked UNVERIFIED. Citations merged in from the other two variants and from the debate keep their authors' readings and were not re-opened for this merge. Decision numbers `D5`, `D6`, `D9`, `D10` and `D11` always mean the experiment's decisions recorded in `DEC` (external); this spec defines no D-numbers of its own. The alias `SPEC` (section 10) and the label `C-R3-10` (section 3) are carried from the base variant, which does not define them: UNVERIFIED, external.

## 1. Problem and evidence

<!-- Source: Base (original) -->
- 427 halves growth (63.5% to 29.7%, `AB:19`) but no run of any arm passed; 89% (R2) and 100% (R3) of new findings sit on lines the previous fix changed (`AB:30`); the R3 proxy is 5.5 and 3.5 against a bar of 3 (`ARMB:20`, `ARMB:23`).
- Root cause by trace (flg-r2): non-blocking F22 was applied (`F2D1:37`) although 427 says minor findings never trigger a revision (`SP:259`), because the coordinator brief said "apply confirmed findings" (`F2D1:10`); the F22 fix added the WC-1 proof to AC-0.4 (lines naming AC-0.4 and WC-1: 0 in `HIST/spec-v1-draft.md`, 2 in `HIST/spec-v2-after-round1.md`), which became blocking N5 (`F2R2:119`), whose fix became blocking N12 at review 3 (`F2R3:84`). A prose rule lost to a brief.
- The verdict, the review count, the saved copy and the scope rule are prose ("every rule here is prose read by a model", `DES:143`; "nothing enforces the count", `DES:162`); the round-3 report still grades FAIL on the brief's "any finding of any severity" (`F2R3:15`).
- Claim of this spec: a script, not a model, can hold row states, the scope of each later review, the review counter and the verdict. It cannot stop a reviser from creating fix-induced defects (section 10).

<!-- Source: Invariant probe INV-027 recommended resolution and Base s10, merged per Change #1 -->
- What this spec does not claim: the ledger is not claimed to change r, the share of blocking fixes that create new blocking defects (section 10). The claim "the ledger alone meets the bar" is falsified if the measured B1 x r1 x r2 exceeds 3 in either replicate; the three quantities are pre-registered in section 9.

## 2. Mechanism

<!-- Source: Variant A s2 component table, merged per Change #3 -->
Three components, each with one job, so later adopters reuse the first two unchanged:

| Component | Job | Ships as |
|---|---|---|
| Ledger kernel | The only writer of ledger state: snapshots, diffs, anchors, transitions, decisions | `scripts/review_ledger.py` inside skill `sc-review-ledger` |
| Ledger contract | File layout, input schemas, `PROFILES`, CLI, how to add a profile | `sc-review-ledger/SKILL.md` (delegate-only, like `sc-bare-review`) |
| Adapter | Tool-specific review behaviour plus a profile name | `/sc:spec-panel-ledger` (profile `spec-panel`); later reflect, rf-qa (section 7) |

<!-- Source: Base (original, modified): ledger path, layout and actor rule replaced per Change #5 (Variant A s3 Location and Layout) and Change #4 (no role flag) -->
Names used below. `LEDGER` = `uv run --no-project python "<skill base>/scripts/review_ledger.py"` (same call shape as the archive helper, `W/bs346-ledger/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:54`); `<skill base>` is `~/.claude/skills/sc-review-ledger` first, else the project `.claude/skills/sc-review-ledger`. S1 paths: `DOC` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `L` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger/` (the default `<doc dir>/<doc stem>.review-ledger/`, overridable by `--ledger <dir>`; section 3, Location). The reports stay in `.dev/orca-command-refactor/review/`. Layout of `L`:

```text
<stem>.review-ledger/
  ledger.json                    state; written only by review_ledger.py
  snapshots/r1.md r2.md r3.md    the text each review saw (sha256 in ledger.json)
  diffs/c1.json c2.json          the hunks of each fix cycle (section 3, Diffs)
  inputs/r1-find.json c1-answers.json r2-verify.json c2-answers.json r3-verify.json
  plan-r2.md plan-r3.md          verify plans, written by begin, read by the verifier
  .lock                          the lock file (section 6, Transaction, crash and rerun)
```

Actors: coordinator (Orca worker, human or script), reviewer (a fresh session per step, running `/sc:spec-panel-ledger`), reviser (a separate session, as in S1 today). There is no role flag: the actor follows from the subcommand. Models write only small JSON input files under `L/inputs/` and their own reports; one script call per input file keeps the call count low. Snapshots, diffs, plans and `ledger.json` are written by the script, never by a model.

<!-- Source: Base (original, modified): "Script calls" column restructured to the merged subcommand set per Change #4; Final sweep row replaced per Change #13 -->
| Step | Who | Reads | Writes | Script calls (in order) |
|---|---|---|---|---|
| Review 1 (FIND, the only full find pass) | reviewer, fresh | `DOC`, the command | report `spec-panel.md`, `L/inputs/r1-find.json` | `init --doc DOC --profile spec-panel`; `find --input L/inputs/r1-find.json`; `close --report spec-panel.md` |
| Revise 1 | reviser, separate session | report (its Reviser brief), `DOC` | `DOC`, disposition file as the brief asks; optionally `L/inputs/c1-answers.json` | none required (the S1 reviser briefs run none); optional `answer --input L/inputs/c1-answers.json` and `revert-unclaimed` on its own hunks |
| Review 2 (VERIFY) | reviewer, fresh | `L/plan-r2.md`, `DOC` around each hunk | report `spec-panel-round2.md`, `L/inputs/r2-verify.json` | `status`; `begin --doc DOC [--revert-unclaimed]`; `verify --input L/inputs/r2-verify.json`; `close --report spec-panel-round2.md` |
| Revise 2 | reviser | as Revise 1 (`c2-answers.json`) | as Revise 1 | as Revise 1 |
| Review 3 (VERIFY, last review) | reviewer, fresh | `L/plan-r3.md`, `DOC` around each hunk | report `spec-panel-round3.md`, `L/inputs/r3-verify.json` | as Review 2; `close` computes PASS or ESCALATE, never CONTINUE |
| Final sweep (not a review, no reviser) | a fresh context that has not read `L`: a subagent of the terminal review session, or a sixth dispatch | only the copy that `sweep --prepare` printed, the command | report `spec-panel-sweep.md`, a sweep input file beside the copy | `sweep --prepare`; `sweep --input <file> --report spec-panel-sweep.md` (run by the session that holds the ledger path) |

What each reviewer step does, in order:

<!-- Source: Base (original, modified): blocking now computed by the profile per Change #17; anchor rule replaced per Change #22 -->
1. **Review 1** is today's panel unchanged (experts, Guard Condition Boundary Table, Whittaker, `SP:305-339`), except that its findings leave the chat as rows. For each row the reviewer supplies `grade`, `rule`, `wrong_outcome`, the finding text and an `anchor` quote; `find` checks each anchor by the anchor rules of section 3 (`E-ANCHOR` if absent, `E-ANCHOR-AMBIGUOUS` if repeated, `--at <line>` disambiguates), and the profile computes `blocking` (section 3, Computed fields). So `rule=FR-8` or `FR-9` blocks at any grade, and a MAJOR blocks only with a non-empty `wrong_outcome` (the 427 "concrete wrong outcome" test, `SP:259`, turned into a required field). A non-blocking row is stored `deferred` by the script, so minor rows can never be answered or revised.

<!-- Source: Base (original, modified): the revise-check exit 7 loop and the revert sentence replaced per Change #8; optional reviser call per Change #7 -->
2. **Revise** works on the text the report's Reviser brief lists. The S1 reviser briefs ask the reviser to "apply confirmed findings" and run no script (`BR/T06-R1-reviser-L10-3bb70411.txt`), so a reviser call is optional: a reviser that runs `answer` claims hunks for blocking rows that are `open` or `reopened` (section 3, T3), and one that does not is covered by the admission step below. Unclaimed hunks never stall the loop: there is no "repeat until exit 0" check. A reviser may still run `revert-unclaimed` on its own hunks. This replaces "the reviser reports the byte size before and after" (`SP:263`) by numbers the script prints, and it is the mechanical form of "revise only text a blocking finding names".

<!-- Source: Orchestrator decisions D1 and D2, invariant probe INV-006 (option 2), INV-007 and INV-030, merged per Change #7 and Change #8 -->
3. **Admission at `begin`** (reviews 2 and 3). Reviser answers, when present, are applied first. Then `begin` auto-claims, with `claimed_by=script-location`, every remaining hunk that overlaps the mapped span of an `open` or `reopened` blocking row, widened to its enclosing paragraph; a hunk overlapping two rows is claimed by both; a row with a claimed hunk moves to `fixed` (T4). The S1 reviser briefs stay verbatim; this rule is what lets a cycle make progress when the reviser never runs `answer`. The auto-claim count is reported per cycle as a compliance number (section 9). A hunk that overlaps no blocking row is unclaimed. By default `begin` reports unclaimed hunks, counts their bytes, lists them in the plan and never reverts them. Only when the invocation line carries `--revert-unclaimed` does `begin` restore the snapshot text for those hunks, each after a preimage check, and log every revert with the bytes discarded; the flag is the consent that `SP:475` requires ("Modify specifications without explicit user consent and validation", under "Will Not"). If a preimage check fails, that hunk is not reverted and the round records `cannot-verify` for it, which escalates (section 4) instead of stalling. `begin` never stalls on unclaimed hunks. Reverted bytes feed the growth report (section 9). Known leak: a minor fix written in the same paragraph as a blocking row's span is admitted as part of that row's fix; it is measured as `minor_touched`, split by admission path (section 9).

<!-- Source: Base (original, modified): hunk sentence and per-row answers replaced per Change #6 (Variant A plan file), Change #9 (paragraph admission), Change #10 (four results, Variant C VERIFY schema) and Change #25 (Variant C diffs) -->
4. **Verify** (reviews 2 and 3). `begin` computes the changed hunks of `DOC` against the previous snapshot (Python `difflib` with autojunk disabled, the same intent as `git diff --no-index -w -U0` that the real round-3 reviewer ran, `F2R3:25`; no git call, so no git state is needed), saves them with old and new ranges and deletion tombstones (section 3, Diffs), and writes `L/plan-r<k>.md`. For admission only, the script compares paragraphs (runs of non-blank lines joined with single spaces), so a pure rewrap is not an unclaimed hunk; raw line hunks are kept for evidence and for `HUNKS_LARGE`. The plan lists: every blocking row in `open`, `fixed` or `reopened` with its frozen grade, wrong outcome, old anchor and its hunks (old and new text, 3 lines of context); every `verified` row whose span a hunk touched; every unclaimed hunk with its bytes; every reviser `gap` entry (section 3); the auto-claim list. The reviewer answers every plan row with exactly one result, `resolved`, `open`, `regressed` or `cannot-verify`, with an evidence quote present in the new snapshot (a deletion cites the old span and the new boundary) and `touched_ok` (is the sentence the change touched itself correct); `touched_ok=no` requires a child row in the same batch (T7). `verify` refuses a missing answer (`E-INCOMPLETE`). A `cannot-verify` answer enters the escalation term of section 4. Then the reviewer runs the single new-defect check (below). It does NOT re-run the whole panel.

<!-- Source: Base (original, modified): replaced per Change #11 (both diff sides, no cap) and Change #12 (scope=outside rows, invariant probe INV-022 option 2) -->
5. **New-defect check (one per verify round, over both diff sides)**: panel critique restricted to this round's hunks, old and new sides, deletion tombstones included, with FR-8/FR-9/FR-10 on guards inside hunks (same limit as `SP:262`). Reviews 2 and 3 both run it, and there is no row-count cap. A new row gets `scope=in` when its `anchor` lies inside a hunk (`origin=changed`) or it carries `depends_on` quoting a changed line (`origin=depends`, the 427 exception for an unchanged line that depends on a changed one, `SP:262`); the script sets `origin` itself. A verifier that cannot cover every hunk answers `cannot-verify`, which escalates; oversize hunks only warn (`HUNKS_LARGE`). An allegation outside the hunks is not refused: `verify` stores it as a row with `scope=outside` and `origin=outside`, status `deferred`. Such rows never count toward `U` and never block the loop, but they are counted in the headline with the sweep rows (`O`, section 9), so nothing found in a verify pass lives only in report prose. The unchanged review-3 brief says "assume defects remain and look for them" (`BR/T09-R3-reviewer-L11-1c9a7ec8.txt`), so such allegations are expected.

<!-- Source: Base (original, modified): replaced per Change #13 (orchestrator decision D5; invariant probe INV-002, INV-003; Variant C s4 sweep challenges; Variant A s2 dup_of) and Change #21 (no late row kind) -->
6. **Sweep**: one whole-document critique, exactly like review 1, by a context that has not read the ledger. It runs on a copy of the accepted snapshot placed in a fresh temporary directory with no ledger: `sweep --prepare` makes the copy and prints only its path, and the sweep prompt names only that copy. `sweep --input` ingests the rows and prints counts only. Preferred route: a subagent spawned by the terminal review session, used only if a pre-run smoke check (section 9) shows that a dispatched Orca worker can spawn one, and only with a heartbeat sent before and after the Agent call; otherwise a sixth dispatch, declared as a deviation. Sweep rows get `round_found=sweep`, status `deferred`, and a `location` class by where the anchor falls: `in_claimed_span` (a verify pass said "ok" over this text), `in_unclaimed_hunk`, `outside_hunks` (review 1 missed it). The script proposes `dup_of` candidates against existing rows and does not rule on them (section 9). A blocking sweep row, or a sweep challenge to a `verified` row, makes `delivery_outcome = ESCALATE` (section 4), never a new cycle. Nothing is revised afterwards. After a review-1 PASS, with no revision and an unchanged document hash, the sweep is skipped and recorded `sweep_skipped=review1_pass`. `sweep` records the live `DOC` hash against the snapshot hash and reports a mismatch as post-terminal edits, not as a loop integrity failure.

<!-- Source: Base (original, modified): counter rule replaced per Change #15 (invariant probe INV-018, INV-025 in part); last sentence replaced per Change #33 (orchestrator decision D3) -->
7. **Counting**: the review counter (`round`) is set to 1 by `init` and advances only on a committed `begin`. The fix-cycle counter (`fix_cycles`) advances only on a committed `begin` that admitted at least one claimed hunk (answered or auto-claimed). A zero-hunk round still counts as a review; its new-defect check is recorded `complete-empty` (never `cannot-verify`), and the round result lists "no edits admitted". A crashed reviser's edits are handled by the auto-claim at the next `begin`; no refusal is added. Review 3 is the last `begin` that can start a verify pass; a fourth is refused `E-CAP` (section 4). The reviewer writes what its brief asks, its own verdict included, and `close` never refuses it; `close` appends the script tail (section 4), so the report's last line is script output, not reviewer prose.

<!-- Source: Orchestrator decision D6 and invariant probe INV-004, merged per Change #14 -->
8. **Terminal phase**: after any terminal loop decision (PASS or ESCALATE), the phase is `terminal`, and `begin`, `answer`, `find` and `verify` refuse `E-TERMINAL` with a JSON body naming the decision and "do nothing further". The S1 dispatch list is fixed, so without this a review-3 `begin` after a review-2 PASS could open a new round over post-terminal edits and change a recorded outcome. `status` reports post-terminal edits by document hash. The coordinator runs `status` before each dispatch (PROSE; in S1 the experiment coordinator does it). After a terminal decision the only writes are the single sweep and `defer` (T12); `status` and `verdict` are read-only.

## 3. Ledger file

<!-- Source: Variant A s3 Format and Integrity, merged per Change #16 and Change #30; Base (original, modified): stdlib-only reason kept, JSON Lines replaced, LEDGER_TAMPERED renamed E-TAMPERED -->
**Format**: one JSON object, UTF-8, pretty-printed, `schema: 1`, with the keys `schema`, `profile`, `doc`, `cap_reviews`, `round`, `fix_cycles`, `phase`, `seq`, `snapshots`, `decisions`, `ops` (saved operation results by request digest, section 6), `rows` and `body_sha256`. Each row carries its own `history`, which gives the audit trail without an event log or a reducer. Chosen over Markdown or YAML because the script parses it with stdlib `json` (no PyYAML dependency inside an installed skill), because anchor quotes hold pipes, backticks and quotes that break a table parser, and because the human-readable table is generated into the report by `close` and `status` instead of being parsed back out of prose. `body_sha256` is the sha256 of the canonical JSON without that key; every command recomputes it first, so a hand edit is refused `E-TAMPERED` (exit 3) and nothing is written. It detects hand edits; it is not a security boundary. Writes are all-or-nothing (section 6, Transaction, crash and rerun).

<!-- Source: Base (original, modified): example rebuilt as one state object with renamed fields per Change #16, on the base's real-shape rows -->
Example after the review 2 `close` (illustrative rows built on the real shapes F10, F22 and N12; the ids and wording are invented for the example; `c1#2` means hunk 2 of `diffs/c1.json`):

```json
{
  "schema": 1, "profile": "spec-panel",
  "doc": ".dev/orca-command-refactor/specs/orca-worker-contract-spec.md",
  "cap_reviews": 3, "round": 2, "fix_cycles": 1, "phase": "revise", "seq": 7,
  "snapshots": {"r1": {"sha256": "9f2c...", "bytes": 57763}, "r2": {"sha256": "4be0...", "bytes": 61210}},
  "decisions": [{"round": 1, "U": 1, "loop_decision": "CONTINUE"},
                {"round": 2, "U": 1, "loop_decision": "CONTINUE"}],
  "ops": {"3d1a...": {"op": "r2-verify", "seq": 6, "result": "ok"}},
  "rows": [
    {"id": "L1", "label": "F10", "round_found": 1, "origin": "find", "scope": "in", "caused_by": [],
     "grade": "MAJOR", "rule": null, "blocking": true,
     "finding": "WC-7 lets a worker load the protocol skill without the command file",
     "wrong_outcome": "a worker calls the protocol skill and skips the command file that holds Unattended mode",
     "anchor": "WC-7 requires a Skill-tool call for the command's skill", "at": "r1:[118,119)",
     "status": "verified",
     "mappings": [{"snapshot": "r2", "span": "r2:[118,121)", "method": "rewritten-in-hunk"}],
     "claims": [{"cycle": 1, "action": "fixed", "claimed_by": "reviser", "span": "r2:[118,121)", "hunks": ["c1#2"], "bytes_added": 212}],
     "history": [{"seq": 2, "via": "find", "to": "open"},
                 {"seq": 4, "via": "answer", "from": "open", "to": "fixed"},
                 {"seq": 6, "via": "verify", "from": "fixed", "to": "verified", "result": "resolved",
                  "touched_ok": false, "evidence": "`Skill sc:<name>` for the command itself"}]},
    {"id": "L2", "label": "F22", "round_found": 1, "origin": "find", "scope": "in", "caused_by": [],
     "grade": "MINOR", "rule": null, "blocking": false,
     "finding": "the timeout wording is vague", "wrong_outcome": "",
     "anchor": "well inside its own timeout", "at": "r1:[62,63)",
     "status": "deferred", "mappings": [], "claims": [],
     "history": [{"seq": 2, "via": "find", "to": "deferred", "reason": "non-blocking under profile spec-panel"}]},
    {"id": "L3", "label": "N12", "round_found": 2, "origin": "changed", "scope": "in", "caused_by": ["L1"],
     "grade": "MAJOR", "rule": null, "blocking": true,
     "finding": "the new WC-7 wording names the command but no check reads it",
     "wrong_outcome": "step 5 passes a run that never loaded the command file",
     "anchor": "WC-7 names `sc:<name>` (the command)", "at": "r2:[119,120)",
     "status": "open", "mappings": [], "claims": [],
     "history": [{"seq": 6, "via": "verify", "to": "open", "hunk": "c1#2"}]}
  ],
  "body_sha256": "c41e..."
}
```

<!-- Source: Variant A s3 Location, merged per Change #5; Base (original, modified): reasons (a) to (e) kept, reason (e) rewritten because the ledger no longer sits next to the reports -->
**Location**: `L = <doc dir>/<doc stem>.review-ledger/`, overridable with `--ledger <dir>`; in S1 `.dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger/`. Why this path: (a) it is derivable from the document path alone, so every session (reviewer, reviser, a resumed coordinator) finds the same ledger without being told; 427 drops to a first review when the coordinator loses the prior-findings file and the saved copy (`DES:162`), while here `init` refuses an existing ledger (`E-EXISTS`; reruns use `init --archive-existing`, section 6); (b) a plain folder in the worktree, because fresh sessions of different workers read the same worktree by default (placement guide quoted at `F2R3:66`, C-R3-10), where `/tmp` or a session's memory would not survive a reboot or a new worker; (c) outside `DOC`, so the reviser's edits and the baseline diff never touch it; (d) not under `.claude/`, which is gitignored sync-dev output (project `CLAUDE.md`); (e) snapshots are copies, not git refs, because `DOC` may be untracked (`DES:50`, `DES:174`); (f) next to the document, so it has the document's tracking state; the reports stay in `review/`, so the analyst collects two folders instead of one. A command file cannot carry the file or the script; see section 6.

<!-- Source: Variant A s3 Computed fields and s6 PROFILES seam, merged per Change #17 (fixes X-016) -->
**Computed fields**: `blocking` comes from the profile, never from the model. The reviewer supplies `grade`, `rule` and `wrong_outcome`; profile `spec-panel` computes `blocking = grade == CRITICAL or rule in {FR-8, FR-9} or (grade == MAJOR and wrong_outcome non-empty)`, copying 427's grading (`SP:259`). There is no reviewer-supplied severity field. The script stores every non-blocking row as `deferred`, so a row with `rule=FR-8, grade=MINOR` is blocking, not deferred. `PROFILES` in the script maps a profile name to its grade vocabulary, its blocking predicate, its cap and optional ordered guards (section 4); this change ships only `spec-panel`. `at`, `scope`, `origin`, `caused_by`, claimed spans and location classes are computed from anchors and diffs, mirroring implement, where the parent, not the reviewer, writes `origin=` (`QA:141,150`).

<!-- Source: Variant A s3 frozen list plus Variant C s3 frozen original issue text, merged per Change #18; Base (original, modified): the no-upward-drift argument kept -->
**Frozen at creation** (any later input that carries one of these keys for an existing id is refused `E-FROZEN`, exit 2): `id`, `label`, `round_found`, `origin`, `scope`, `caused_by`, `grade`, `rule`, `wrong_outcome`, `blocking`, `anchor`, `at` and the original finding text. Grade is frozen per row, which stops a verifier from lifting a row from MINOR to MAJOR or from MAJOR to CRITICAL between rounds. Relocation mappings and later evidence are separate records appended to the row, never replacements. Mutable only by script-run transitions: `status`, `claims`, `mappings`, `anchor_state`, `history`. There is no grade edit at all; `defer` (T12) records the user's words and changes no status.

<!-- Source: Variant A s3 Anchor rules, merged per Change #22; Base s11 risk 1 (candidate lines in the error text) -->
**Anchor rules**: the quote is whitespace-normalized (`" ".join(text.split())`, the same flatten the 427 tests use, `DES:126`) and must occur exactly once in the named snapshot: `E-ANCHOR` if absent, `E-ANCHOR-AMBIGUOUS` if repeated; `--at <line>` disambiguates, and the error text lists the candidate lines. A quote should be at least 12 characters; a shorter or generic quote is accepted with a warning, not refused, because a refusal that stalls a run costs more than a weak anchor. Absence and ambiguity stay refusals because a row without a location cannot be verified.

<!-- Source: Variant C s3 "Anchor relocation and edit ownership", merged per Change #23 -->
**Anchor relocation**: the frozen quote and line are kept forever. Each `begin` appends a mapping record to the row (snapshot hash, current span, method): unchanged-block line mapping first, then a unique exact quote with its context. A rewritten quote maps to the replacement span only when the old span contains it and the new span lies in the computed hunk. Line numbers are hints, never proof; a repeated quote needs unique context, and the script never picks the nearest match silently. A row that cannot be mapped gets `anchor_state=missing` or `anchor_state=ambiguous`, cannot become `verified`, and enters the escalation term `X` (section 4). An empty replacement is a tombstone, not proof of resolution; whether a deletion removed a requirement improperly is the verifier's judgement (PROSE).

<!-- Source: Invariant probe INV-014 recommended resolution and Variant C s6 half-open ranges, merged per Change #24 -->
**Coordinates**: all spans and hunk ranges are half-open `[start, end)` line ranges on a named snapshot, written like `r2:[220,221)`. A zero-width deletion at position p overlaps `[s, e)` when `s <= p <= e`. A span is relocated into the old-side snapshot of a diff before any overlap test. One fixture covers each edge (section 6).

<!-- Source: Variant C s6 diff paragraph, merged per Change #25 -->
**Diffs**: each `begin` saves `L/diffs/c1.json` (at review 2) or `L/diffs/c2.json` (at review 3) with raw old and new ranges, insertion and deletion boundaries and content digests, computed by `difflib` with autojunk disabled; there is no git call. Hunks are numbered within each file. Raw hunks drive ownership and hashes; whitespace-normalized hunks drive the new-defect scope and the admission paragraphs (section 2, item 4).

<!-- Source: Base s3 T1 to T11 restructured per Change #20, with Variant A error codes and requested-by column, Variant C history-derived reopen; statuses per Change #19 (fixes X-017); late row kind removed per Change #21 -->
**Status transitions.** Five statuses: `open`, `deferred`, `fixed`, `verified`, `reopened`. A dispute is a claim flag (`claim.action=disputed`) on an `open` or `reopened` row, not a status. The script is the only writer; "Requested by" names the subcommand whose input may request the move, and the actor follows from it. Every refusal is atomic: nothing is written.

| # | From | To | Requested by (subcommand) | Phase | Script check; refusal code |
|---|---|---|---|---|---|
| T1 | none | `open` | `find` (review 1); `verify` new row (reviews 2 and 3) | find, verify | anchor rules (`E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`); profile says blocking; a verify-time row is `scope=in` only when its anchor lies in a hunk of this round (old or new side) or its `depends_on` quotes a changed line, else it is stored by T2 as `scope=outside` |
| T2 | none | `deferred` | script, at `find`, `verify` or `sweep --input` | find, verify, terminal | the profile says non-blocking; or the row is `scope=outside` (including `origin=reviser-gap`); or the row came from the sweep (`round_found=sweep`); nobody chooses it |
| T3 | `open`, `reopened` | `fixed` | `answer` action `fixed` | revise | row is blocking, `scope=in` and listed; the answer names at least one hunk that changes or deletes text inside the row's mapped span, else `E-FIXED-NO-EDIT`; the claim span is no wider than the mapped span widened to its enclosing paragraph, else `E-CLAIM-WIDE` |
| T4 | `open`, `reopened` | `fixed` | script, auto-claim at `begin` | verify | an unclaimed hunk overlaps the row's mapped span widened to its enclosing paragraph; recorded `claimed_by=script-location` |
| T5 | `open`, `reopened` | (unchanged) | `answer` action `not-fixed` or `disputed` | revise | non-empty `reason`; `disputed` sets `claim.action=disputed`, on which the verifier must rule (T11) |
| T6 | `fixed` | `verified` | `verify` result `resolved` with `touched_ok=yes` | verify | the row has a claim; evidence quote present in the new snapshot (`E-ANCHOR`); the row is not `anchor_state=missing` or `ambiguous` |
| T7 | `fixed` | `verified` plus a child row | `verify` result `resolved` with `touched_ok=no` | verify | a child row whose `caused_by` names this row exists in the same batch or already, else `E-INCOMPLETE` |
| T8 | `fixed` | `open` or `reopened` | `verify` result `open` | verify | reason plus a quote present in the new snapshot; `open` when the row's history holds no earlier verification, else `reopened` (history, not last status, decides) |
| T9 | `verified` | `fixed` | script, at `begin` | verify | a hunk of this round overlaps the row's mapped span (half-open test, Coordinates), so a later edit cannot silently break a verified row |
| T10 | `fixed` (reset by T9 this round) | `reopened` | `verify` result `regressed` | verify | `regressed` on a `verified` row that no hunk touched is refused `E-NOT-CHANGED` (accepted text cannot be re-attacked) |
| T11 | `open` or `reopened` with `claim.action=disputed` | `verified`, or unchanged | `verify` with `dispute=accepted` or `dispute=rejected` | verify | evidence about the original harm; `accepted` moves the row to `verified`; `rejected` leaves it `open` or `reopened`; an unruled, rejected or uncertain dispute at the cap counts as an open blocker |
| T12 | any | (unchanged; a `user_deferred` record) | `defer --id <id> --quote "<user words>"` | terminal | non-empty quote; appends a `user_deferred` record to the row's history; the status, the recorded `loop_decision`, `delivery_outcome` and every headline count stay unchanged; that the user said it is PROSE |

A `cannot-verify` result leaves the status unchanged and counts in `X` (section 4). A `verified` row that no hunk touched stays `verified`. A lexical cross-check runs at `begin`: when an identifier named in a verified row's claim appears in a hunk of this round, the plan prints a warning line; it is not a status change.

<!-- Source: Invariant probe INV-008 and orchestrator decision D1, merged per Change #26; Variant C-R2 C-023 row (location, not causation) -->
**Claim width and attribution (under T3 and T4).** A claim span may not exceed the row's mapped span widened to its enclosing paragraph, which is the auto-claim unit of T4; a wider claim is refused `E-CLAIM-WIDE`. A child row's `caused_by` lists every row that claimed its hunk, so a hunk claimed by two rows attributes the child to both. The script records location attribution only; the analyst adjudicates causation for M3 (section 9).

<!-- Source: Invariant probe INV-009, merged per Change #27; Variant A s3 (deleted: true) -->
**A `fixed` answer must name an edit.** `answer` with action `fixed` must name at least one hunk that changes or deletes text inside the row's mapped span (a deletion is given as `deleted: true`), else it is refused `E-FIXED-NO-EDIT`. A reviser who changed nothing answers `not-fixed` or `disputed`. Auto-claimed rows (T4) satisfy this by construction.

<!-- Source: Invariant probe INV-010, adapted to orchestrator decision D4, merged per Change #28 -->
**Reviser gap entries.** A reviser that runs `answer` may add `gap` entries (an anchor on unchanged text plus a reason). The next plan lists them, and the verifier may file each as a row with `origin=reviser-gap`, which is stored `scope=outside` (T2): never blocking, counted in `O` of the headline and separately in M3 (section 9). This is active only when the reviser runs `answer`, which the S1 reviser briefs do not ask for.

<!-- Source: Base (original, modified): adjusted per Change #19 (no disputed status), Change #14 (terminal phase) and Change #20 (fixed to open allowed by T8) -->
Forbidden and refused: any move into `open` from `verified` or `deferred` (T8 is the only move into `open`, and only from `fixed`); any move out of `deferred` (`E-ILLEGAL`); `answer` on a `deferred` or `verified` row (`E-ILLEGAL`, so a minor row cannot be revised, whatever the brief says); a `verify` answer for a row that is not in the plan (`E-ILLEGAL`); `regressed` on an untouched row (`E-NOT-CHANGED`); any frozen key (`E-FROZEN`); `begin`, `answer`, `find` or `verify` in phase `terminal` (`E-TERMINAL`); a fourth review or a third fix cycle (`E-CAP`). An unanswered blocking row is not a transition: it stays `open` and counts as unresolved.

## 4. Termination rule

<!-- Source: Base (original, modified): computed from the ledger only; the read-only verdict subcommand kept -->
Computed by `close` (the loop decision), by `sweep --input` (the delivery outcome) and reported by the read-only `verdict` subcommand, from the ledger only. No model writes a decision.

<!-- Source: Variant C s4 (loop_decision, delivery_outcome, S, X, I), merged per Change #31 and Change #32; Base (original, modified): U restricted to scope=in, late rows and Lt removed per Change #21 -->
```text
n  = state.round       # 1, 2 or 3; set to 1 by init, advanced only by a committed begin
U  = count(rows: blocking and scope == in and status in {open, fixed, reopened})
     # includes child rows; excludes deferred rows, scope=outside rows and sweep rows
X  = count(cannot-verify answers this round) + count(rows: anchor_state in {missing, ambiguous})
     + count(failed revert preimages this round) + coverage overflow
I  = valid state object (body hash) and intact snapshots (sha256) and complete row answers
at close of review n (n = 1, 2, 3):
    if not I or X > 0:  loop_decision = ESCALATE    phase -> terminal
    elif U == 0:        loop_decision = PASS        phase -> terminal
    elif n < 3:         loop_decision = CONTINUE    phase -> revise
    else:               loop_decision = ESCALATE    phase -> terminal
at sweep --input:
    S = count(sweep rows with blocking) + count(blocking sweep challenges to verified rows)
        + (1 if the sweep is incomplete else 0)
    delivery_outcome = ESCALATE if loop_decision == ESCALATE or S > 0 else PASS
at close of review 1 with PASS, no revision and an unchanged document hash:
    sweep skipped (sweep_skipped=review1_pass); delivery_outcome = PASS
```

`loop_decision` is never CONTINUE at review 3, and before the sweep has run a PASS is only a `loop_decision`, never a `delivery_outcome`. `delivery_outcome` is set only by `sweep --input`, or by the review-1 `close` when the sweep is skipped. `S` counts by `blocking` and drives the delivery outcome; the measurement set `W` of section 9 counts the same sweep rows by grade. One `cannot-verify` ends the loop, so the `X` count is reported per replicate (section 9).

<!-- Source: Orchestrator decision D3 and invariant probe INV-021 (option 2), merged per Change #33; Variant A s2 step 4 -->
**Report tail.** The reviewer writes what its brief asks, including a findings table and its own PASS or FAIL verdict (the review-1 brief asks for "a numbered findings list ... and a PASS or FAIL verdict", `BR/T05-R1-reviewer-L11-699ae853.txt`; the review-3 brief says "any finding of any severity is FAIL", `BR/T09-R3-reviewer-L11-1c9a7ec8.txt`). `close` never refuses that text. It appends, in order: `## Ledger` (the rendered rows), the `## Reviser brief` (CONTINUE only), the line `ledger-verdict: <loop_decision> U=<U> S=<S> review: <n> of 3` (`S` reads `pending` until the sweep has run), and, as the very last line, the script verdict. The analyst records every disagreement between the reviewer's verdict and the script's (section 9).

<!-- Source: Orchestrator decision D3, invariant probe INV-024 and Variant C s4 (CONTINUE renders verdict: FAIL), merged per Change #34 -->
**Last-line strings.** A CONTINUE report ends `verdict: FAIL`. A loop-terminal report written before the sweep ends `loop: PASS (sweep pending)` or `loop: ESCALATE (sweep pending)`, with no `verdict:` line from the script. The sweep report ends `verdict: PASS` or `verdict: FAIL` from `delivery_outcome`, where ESCALATE maps to FAIL. A review-1 report with the sweep skipped ends `verdict: PASS`.

<!-- Source: Base (original, modified): Result column split into loop_decision and delivery_outcome per Change #31; Next column replaced per Change #34; zero-finding row added per Change #38 -->
| n | Ledger state after the pass | `loop_decision` | `delivery_outcome` | Last line of this report | Next |
|---|---|---|---|---|---|
| 1 | zero findings (`find` accepted `[]`), or U = 0 and X = 0, document unchanged | PASS | PASS (sweep skipped) | `verdict: PASS` | done |
| 1 or 2 | U > 0, X = 0, I holds | CONTINUE | not set | `verdict: FAIL` | revise, then verify |
| 2 or 3 | U = 0, X = 0, I holds | PASS | set by the sweep | `loop: PASS (sweep pending)` | sweep |
| 3 | U > 0 | ESCALATE | ESCALATE | `loop: ESCALATE (sweep pending)` | sweep, then the user decides on the open blocking rows plus the sweep rows |
| any | X > 0 or I fails | ESCALATE | ESCALATE | `loop: ESCALATE (sweep pending)` | sweep, then the user decides |

<!-- Source: Base (original, modified): renamed to loop_decision; ESCALATE now followed by the sweep -->
Worked on the real flg-r2 counts: review 1 left 13 blocking rows (`F2D1:39`, 13 blocking applied) so CONTINUE; review 2 found 6 new blocking (`F2R2:13`) so U = 6, CONTINUE; review 3 found 1 (N12, `F2R3:15`) so U = 1 at n = 3, `loop_decision` ESCALATE, and therefore `delivery_outcome` ESCALATE after the sweep. That matches what happened (FAIL at review 3, escalated, `F2R3:19`), but the counter and the decision were computed, not typed.

<!-- Source: Variant A s4 (E-REPORT-EDITED), orchestrator decision D3 and invariant probe INV-011, merged per Change #35 -->
**Tail protection.** `close` records a digest of every tail it appends. `begin` refuses `E-REPORT-EDITED` when the prior report's script tail differs from the recorded digest. The last loop report and the sweep report have no next `begin`, so `sweep --input` (or, when the sweep is skipped, the review-1 `close`) re-checks the tail of every prior report against the recorded decisions, and the V1-ledger analyst step runs `status` once after the last dispatch and records the result (section 9). After a crash the tail is regenerated idempotently.

<!-- Source: Base (original, modified): pinned strings kept verbatim; enforcement sentences replaced per Change #36 (Variant A CAP_REVIEWS, Variant C refusals under a new op id) -->
**Cap text and the sweep.** The variant command's cap bullet carries the pinned sentence verbatim: `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` (`CANONICAL_CAP_TEXT`, `W/bs346-ledger/tests/skills/test_review_severity_rule.py:215`) and the at-cap clause `HALT and escalate to the user with the open blocking findings` (`:216-219`). The cap is enforced, not just stated: the script constant `CAP_REVIEWS = 3` implements it, and a test ties the constant to the text. The script refuses a fourth review (`E-CAP`), a third fix cycle (`E-CAP`), a second sweep (`E-SWEEP-DONE`) and a second `init` or `find` on an existing ledger (`E-EXISTS`, `E-PHASE`), even under a new op id; an identical retry returns the committed result instead of using a slot (section 6). Fix cycles therefore stay at most 2.

<!-- Source: Base (original, modified): reason (a) and the cost sentence updated for deferred sweep rows (Change #21) and the sweep route (Change #13) -->
**The final sweep is outside the 3-review cap.** Reasons: (a) the cap counts reviews that can start a fix cycle; the sweep cannot, its rows are `deferred` with `round_found=sweep` and are never revised; (b) putting it inside review 3 would make the same context verify and then sweep, so the sweep would be anchored on the rows it just read, and the sweep is the only part of the design that can expose defects the verify scope hid (section 10); (c) the report header for it is `sweep`, never `review: 4 of 3`, so no text says four reviews. Cost is stated plainly: one extra fresh context (a subagent of the terminal review session, or a sixth dispatch) and a second full read of `DOC`. Full-document reads per loop become 2 (review 1 and the sweep) instead of 3 (reviews 1 to 3 of the control, `AB:6`).

<!-- Source: Base (original, modified): final renamed delivery_outcome, late rows renamed sweep rows per Change #21 and Change #31 -->
**PASS means the ledger is clean, not that the document is clean.** The `loop_decision` can be PASS at review 2 and the sweep can still find blocking rows; `delivery_outcome` is then ESCALATE with those rows listed. That is deliberate: the sweep rows are reported and not looped on, so the user, not a third fix cycle, decides.

<!-- Source: Base (original, modified): last sentence replaced per Change #37 (rf-qa order RFQA:407 from the Round 2 rebuttals) -->
**No second computed stop.** rf-qa halts when the blocking count does not shrink (`RFQA:401`) and 427 chose not to (`DES:154`). Measured data supports skipping it: the critique proxy fell from review 1 to review 2 in all six S1 runs (11 to 9, 12 to 7, 9 to 5, 9 to 7, 16 to 5, 17 to 6; `AB:13`, `ARMB:13`), so a halt at n = 2 would never have fired, and at n = 3 the cap already fires. Profile `spec-panel` has no monotonicity halt. A `PROFILES` row may list ordered guards; a later `rf-qa` profile would carry regression, then monotonicity, then cap, with rf-qa's existing halt messages, in rf-qa's own order (regression first, `RFQA:407`). A guard set by profile, not by flag, cannot be switched on by a brief.

## 5. Difference from PR 427 `--re-review --baseline`

<!-- Source: Base (original) -->
427 re-reviews the changed document: its review 2 and 3 run the full panel on "lines changed against the baseline" and build the boundary table on changed guards (`SP:262`). The ledger changes the unit of review from "changed lines" to "answered rows", and moves five duties from a model to a script. Concretely:

<!-- Source: Base (original, modified): Ledger variant and What is removed cells updated per Change #39 (consequential to Changes #4, #7, #8, #12, #13, #33); row "Out-of-hunk findings" added; "Late findings" renamed "Sweep findings" per Change #21 -->
| Duty | 427 (`SP:258-264`) | Ledger variant | What is removed |
|---|---|---|---|
| Prior findings input | a prose report, parsed by a model; stop if the `review: N of 3` header is missing (`SP:258`) | rows with ids and statuses in `ledger.json`, parsed by `json`, handed to the verifier as `plan-r<k>.md` | the model re-reading and re-tabulating the prior report each round (the 15-row Part 1 table at `F2R3:29-45` becomes the `## Ledger` table that `close` appends) |
| `origin=` tag | written by the reviewer (`SP:262`; "treatment reads a tag", `AB:30`) | computed from hunks; `verify` stores an allegation outside the hunks as a `scope=outside` row instead of a tag | a mislabelled origin; the `origin=unchanged` note class in verify |
| Saved copy and baseline | kept by the coordinator, prose (`SP:261`, `DES:162`) | `init` and `begin` write `snapshots/r<n>.md` themselves; the ledger path is derivable from the document | the failure "coordinator drops the saved copy, run becomes a first review" (`DES:162`) |
| Minor rows never revised | prose (`SP:259`, `SP:263`), overridden by the brief in flg-r2 (`F2D1:10`, `F2D1:37`) | `answer` on a deferred row is refused `E-ILLEGAL`; `begin` auto-claims only hunks inside a blocking row's paragraph and reports the rest, restoring them with `--revert-unclaimed` | a minor fix outside every blocking paragraph as a source of new blocking findings (the F22 to N5 to N12 chain); a minor fix inside a blocking paragraph is admitted and measured (section 9) |
| Review count and verdict | the reviewer's `review: N of 3` header and last line (`SP:260`, `SP:261`) | `begin` advances the counter; `close` computes the decision and appends the tail, with the script verdict as the last line below the reviewer's own verdict | a reviewer, or a brief saying "any finding of any severity" (`F2R3:15`), deciding PASS or FAIL |
| Reviser size report | "reports the byte size before and after" (`SP:263`) | bytes per hunk, per claim and per revert from `begin` | an unchecked self-report |
| Per-fix check | the whole changed-line set gets a full panel pass | one answer per plan row (`resolved`, `open`, `regressed` or `cannot-verify`, plus `touched_ok`), then one new-defect check over both diff sides | the open-ended "find anything on changed lines" framing; the reviewer must answer every plan row (`verify` refuses `E-INCOMPLETE`) |
| Sweep findings | none; every review may raise anything on changed lines | one sweep on a copy of the accepted snapshot, outside the cap, classified by where the defect sits | looping on them |
| Out-of-hunk findings | `origin=unchanged` minor notes (`SP:262`) | `scope=outside` rows, counted in the headline, never blocking | findings that live only in report prose |

<!-- Source: Base (original) -->
What the ledger does NOT remove, stated first because it matters most: the review surface does not shrink much. In flg-r2 review 3 the changed lines were 25 of 317 (7.9%, computed from `F2R3:25`), in ctl-r1 review 3 88 of 364 (24.2%, from `C1R3:11`), so 427 with its flags already restricted the surface to hunks. All 8 blocking findings of ctl-r1 review 3 (`C1R3:181-189`) have at least one anchor inside those changed lines (checked line by line against `C1R3:11`), and so does N12 (`F2R3:85`, lines 60, 210, 220, 317 are all in `F2R3:25`). A hunk-anchored verify therefore finds the same blocking rows 427 found. What changes is who holds the counts, the scope and the verdict, and that minor edits can be stopped mechanically. If the idea works on S1 it works mostly through the minor-row rule and the computed stop, not through a smaller read.

## 6. Exact changes, file by file

<!-- Source: Base (original) -->
**Where the script lives and why.** A command file is one `.md` and `install_commands` copies only the top-level `*.md` files with `shutil.copy2` (`W/bs346-ledger/src/superclaude/cli/install_commands.py:38-41`, `:59-61`); a skill folder is copied whole by `shutil.copytree` (`W/bs346-ledger/src/superclaude/cli/install_skill.py:52`), and the wheel force-includes all of `src/` (`W/bs346-ledger/pyproject.toml:85-87`). So the script goes in a new skill folder and reaches `~/.claude/skills/sc-review-ledger/scripts/`. **Naming trap**: the skill must NOT be named `sc-spec-panel-ledger`. `install_all_skills` treats an `sc-<x>` skill with a `commands/<x>.md` file as "served by the command", skips it and deletes a stale installed copy, unless the command activates it with a `Skill sc-<x>` line (`W/bs346-ledger/src/superclaude/cli/install_skills.py:40-59`, `:88-98`). `sc-review-ledger` has no `commands/review-ledger.md`, so it installs standalone, like `sc-bare-review` (a skill with no slash command, `W/bs346-ledger/src/superclaude/skills/sc-bare-review/SKILL.md:3`). A python CLI subcommand (`superclaude ledger`) was rejected for the experiment: the machine's `superclaude` binary is the owner's install, not this worktree (cf. D9, `DEC:46`), so a changed CLI could not be tested without a machine-wide reinstall.

<!-- Source: Base (original, modified): fixtures row added and SKILL.md row extended per Change #47 (Variant C s6 fixtures folder, Variant A contract) -->
**New files**

| Path | Content |
|---|---|
| `src/superclaude/commands/spec-panel-ledger.md` | The variant command (outline below). |
| `src/superclaude/skills/sc-review-ledger/SKILL.md` | Frontmatter `name: sc-review-ledger`, delegate-only (no slash command), `allowed-tools: Read, Bash`; the contract: layout, input schemas, `PROFILES`, the transition table, the CLI and how to add a profile, so other commands can cite it (section 7). |
| `src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py` | The kernel, stdlib only (`argparse`, `json`, `hashlib`, `difflib`, `fcntl`, `os`, `pathlib`, `re`, `sys`); run as `uv run --no-project python "<skill base>/scripts/review_ledger.py" <subcommand> ...`. |
| `tests/skills/test_review_ledger_script.py` | Executable tests, loading the script with `importlib` like `W/bs346-ledger/tests/skills/test_workflow_archive.py:22-28`. |
| `tests/skills/test_spec_panel_ledger_command.py` | Text pins and the drift test (below). |
| `tests/skills/fixtures/review-ledger/` | Tiny documents and input JSON for the edge cases listed under Tests. |
| `docs/designs/spec-panel-ledger-loop.md` | This design, trimmed, once approved. |

<!-- Source: Base (original) -->
**Edited files**: none in the original loop. `spec-panel.md`, its `plugins/` copy, `HOW-WE-WORK.md` and the routing tests stay untouched (additive variant; promotion would be a separate change). No `UNATTENDED_COMMANDS` edit is needed because the variant omits `## Unattended mode` (the set-equality check is at `W/bs346-ledger/tests/skills/test_worker_contract.py:831-839`; `spec-panel` is in the set because of `SP:451`). `tests/unit/test_cli_install.py` needs no edit: its lists are baseline-member presence checks (`_assert_present`, `:501-505`). The plugin command list there is a strict subset of `src` (`:399-404`), so no plugin mirror is required.

<!-- Source: Base (original, modified): Usage sentence and the eight bullets replaced per Change #40 (Variant A s6 Setup bullet); refusal line added per Change #41 (invariant probe INV-026) -->
**`spec-panel-ledger.md` outline.** Body = `SP:1-450` and `SP:463-486` unchanged, except: frontmatter `name: spec-panel-ledger`; Usage keeps `SP:22` minus `--re-review ... --baseline ...` plus `[--ledger <dir>] [--revert-unclaimed] [--sweep]`, and drops the `--unattended` usage line `SP:23`; `## Unattended mode` (`SP:451-461`) is omitted; `## Review Loop` (`SP:256-264`) is replaced by `## Review Ledger Loop`. That section opens with one refusal line: when `--unattended` appears as a standalone token, print "spec-panel-ledger has no unattended mode" and stop. This is not a `## Unattended mode` heading, so the set-equality test stays green, and a later brief that passes `--unattended` is refused instead of silently ignored. Then come eight one-line bullets (one line each, as 427 does, so line matchers see each whole):
1. **Setup**: critique only; invoke `Skill sc-review-ledger` (dual lookup, `~/.claude/skills/` first, then the project `.claude/skills/`); the ledger is `--ledger` or `<doc dir>/<doc stem>.review-ledger/`; run `init` if it is absent, else `begin`; a refusal stops the run and never falls back to a first review.
2. **Find**: the full panel; each finding becomes a row with `grade`, `rule`, `wrong_outcome` and an anchor quote; the script decides what is blocking.
3. **Verify**: answer every row in `plan-r<k>.md`; run one new-defect check on this round's hunks; anything else is filed `scope=outside`.
4. **Sweep**: run only on the copy that `sweep --prepare` prints; never open the ledger folder.
5. **Report**: write what the brief asks; never edit the lines that `close` appends.
6. **Cap**: the canonical sentence verbatim, then the at-cap clause `HALT and escalate to the user with the open blocking findings`; `review: N of 3` comes from the script; do not type it.
7. **Reviser contract**: revise only text a listed blocking row names; minor rows are not answerable; unclaimed edits are reported and, with `--revert-unclaimed`, restored.
8. **Precedence**: a brief may narrow this scope, not widen it, and cannot change a grade or a script verdict.

<!-- Source: Variant A s6 CLI table and Variant C s6 exit-code rule, merged per Change #42 (orchestrator decision D9); Base (original, modified): role column replaced by inferred caller, close exit codes moved to verdict; init row extended per Change #45; find row per Change #38 -->
**Script CLI.** Every subcommand takes `--ledger <dir>` (or `--doc`, from which the path is derived). Every mutation also takes `--op <id>` and `--expect-seq <n>` (section 6, Transaction, crash and rerun). Every committed operation exits 0, whatever the decision; refusals use distinct non-zero codes: 1 usage; 2 input refused (row level: `E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`, `E-FROZEN`, `E-ILLEGAL`, `E-INCOMPLETE`, `E-NOT-CHANGED`, `E-CLAIM-WIDE`, `E-FIXED-NO-EDIT`, `E-SCHEMA`, and an input whose binding is stale); 3 state refused (`E-EXISTS`, `E-TAMPERED`, `E-PHASE`, `E-TERMINAL`, `E-CAP`, `E-REPORT-EDITED`, `E-SWEEP-DONE`); 4 lock or sequence conflict. Only `verdict` maps PASS, CONTINUE and ESCALATE to 0, 10 and 11. A retry may return an older committed result, so callers read a fresh `status` before acting.

| Subcommand | Caller (inferred) | Inputs | Writes | Output | Checks | Exit |
|---|---|---|---|---|---|---|
| `init --doc D --profile spec-panel [--archive-existing]` | reviewer, review 1 | the document | `ledger.json`, `snapshots/r1.md` | `review: 1 of 3`, ledger path | profile known; no existing ledger (`E-EXISTS`), unless `--archive-existing` renames it first | 0; 1; 3 |
| `find --input F` | reviewer, review 1 | `inputs/r1-find.json` (rows: `grade`, `rule`, `wrong_outcome`, `anchor`, finding text, optional `at`); accepts an empty rows array | rows, `open` or `deferred` | counts, decision preview | phase `find`; schema; anchor rules; blocking from the profile; a second `find` refused (`E-PHASE`) | 0; 2; 3 |
| `answer --input F` | reviser | `inputs/c<k>-answers.json` (per row: `id`, action `fixed`, `not-fixed` or `disputed`, claim span or `deleted: true`, `reason`; optional `gap` entries) | claims, gap entries | per-row result, unclaimed hunks with bytes | phase `revise`; listed blocking rows only (`E-ILLEGAL`); `E-FIXED-NO-EDIT`; `E-CLAIM-WIDE`; `E-TERMINAL` | 0; 2; 3 |
| `begin --doc D [--revert-unclaimed]` | reviewer, reviews 2 and 3 | current `D`, the prior report | `snapshots/r<k>.md`, `diffs/c<k-1>.json`, `plan-r<k>.md`, auto-claims, reverts | `review: k of 3`, plan path, auto-claim count, unclaimed and reverted bytes | integrity (`E-TAMPERED`); prior report tail (`E-REPORT-EDITED`); round within the cap (`E-CAP`); `E-TERMINAL`; one `begin` per round | 0; 2; 3; 4 |
| `verify --input F` | reviewer, reviews 2 and 3 | `inputs/r<k>-verify.json` | transitions, new rows (`scope=in` or `scope=outside`), relocation records | counts, decision preview | every plan row answered once (`E-INCOMPLETE`); evidence quotes present in the new snapshot (`E-ANCHOR`); no frozen keys (`E-FROZEN`); `regressed` only on touched spans (`E-NOT-CHANGED`); `E-TERMINAL` | 0; 2; 3 |
| `close --report R` | reviewer | the report | `decisions`, the report tail and its digest | the decision | header `review: n of 3` present; tail appended once | 0; 3 |
| `sweep --prepare` | the session that holds the ledger path, at the sweep | the ledger | a copy of the accepted snapshot in a fresh temporary directory | only the copy's path | phase `terminal`; one sweep per loop (`E-SWEEP-DONE`) | 0; 3 |
| `sweep --input F --report R` | the same session | sweep rows | rows (`deferred`, `round_found=sweep`), `dup_of` candidates, `delivery_outcome`, the sweep report tail | counts only | phase `terminal`; once per loop (`E-SWEEP-DONE`); re-checks every prior report tail; live `DOC` hash against the snapshot | 0; 2; 3 |
| `status` | any (coordinator before each dispatch; analyst after the last) | the ledger | nothing | phase, counts, post-terminal edits by document hash, the metrics of section 9 | integrity | 0; 3 |
| `revert-unclaimed [--hunk k]` | reviser | its own unclaimed hunks | `D` | restored bytes | preimage check; phase `revise` | 0; 2; 3 |
| `defer --id <id> --quote "<user words>"` | coordinator | the user's words | a `user_deferred` record (T12) | the record | phase `terminal`; non-empty quote | 0; 2; 3 |
| `verdict` | any | the ledger | nothing | `{loop_decision, delivery_outcome, U, S, review}`, read-only | none | 0 PASS; 10 CONTINUE; 11 ESCALATE |

<!-- Source: Variant C s6 stdout object and actor input envelope, merged per Change #43 -->
**Output and input binding.** Success stdout is one JSON object `{ok, seq, phase, review, fix_cycles, counts, loop_decision, delivery_outcome, next_action, artifact_paths}`, with unset decisions as null; errors are `{error, detail, next_action}`; diagnostics go to stderr. Every input file carries `round`, `document_sha256` and `ledger_seq`; a stale binding is refused (exit 2), so resumed or cached output from an older round cannot be ingested.

<!-- Source: Variant C s6 "Transaction, crash and rerun contract", reduced per the C-R2 machinery table and orchestrator decision D8, merged per Change #44 (invariant probe INV-005) and Change #45 (invariant probe INV-001) -->
**Transaction, crash and rerun.** Every mutation runs under a nonblocking `fcntl.flock` on the stable lock file `L/.lock`; a second writer is refused at once (exit 4). Under the lock the script validates the request, writes snapshots and diffs by temp file plus fsync plus `os.replace`, then replaces `ledger.json` the same way. Every mutation takes `--op` and `--expect-seq`. Idempotency is by request digest within the same phase and round, independent of op id: a new op id carrying a payload already committed returns the original result from `ops` with `replayed: true`; only a different payload under a stale `--expect-seq` is refused (exit 4). There is no event replay, no hard-link publish and no directory sync. A reviser crash leaves `D` edited and uncommitted; the next `begin` treats it as input (section 2, item 7). Reruns: with a derivable path, an aborted replicate leaves a ledger that blocks `init` (`E-EXISTS`); `init --archive-existing` renames the old folder to `<stem>.review-ledger.aborted-<UTC timestamp>/` and records the rename in the new state object. The experiment protocol requires it, never a manual delete (section 9).

<!-- Source: Variant A s6 Tests, Variant C s6 fixtures folder and Base s6 text pins and drift test, merged per Change #46; Base "Checks the script owns" list folded in because its role gate and close exit codes no longer exist -->
**Tests.**
- **Script cases** (`test_review_ledger_script.py`, fixtures in `tests/skills/fixtures/review-ledger/`): every transition edge T1 to T12 and every refusal code; profile blocking for CRITICAL, FR-8 with MINOR, MAJOR with and without a wrong outcome, and MINOR; auto-claim with one row, two rows and no row; `E-CLAIM-WIDE`; `E-FIXED-NO-EDIT`; paragraph admission on a pure rewrap; unclaimed hunks reported without the flag and reverted with it; a failed preimage; `scope=outside` rows; `E-TERMINAL`; a zero-hunk round recorded `complete-empty`; an empty `find`; half-open overlap and deletion edges; relocation ending `missing` and `ambiguous`; an identical payload under a new op id; a stale sequence; two writers; `E-TAMPERED`; `E-REPORT-EDITED`; `CAP_REVIEWS == 3` tied to `CANONICAL_CAP_TEXT`.
- **Command pins** (`test_spec_panel_ledger_command.py`): both `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` (imported as `tests/skills/test_spec_panel_review_loop.py` does, `DES:126`) appear in the variant; eight one-line bullets in order; the subcommand names `init`, `find`, `answer`, `begin`, `verify`, `sweep`, `close`, `status`, `revert-unclaimed`, `defer`, `verdict` and the flags `--ledger`, `--revert-unclaimed`, `--sweep` appear; the `--unattended` refusal line exists; no `src/superclaude` path (in the style of test T9 of the 427 design `DES`, external, not transition T9 of this spec); the dual lookup text names `~/.claude/skills/sc-review-ledger` before the project `.claude/skills/sc-review-ledger`; no `## Unattended mode`; none of `BANNED_SEVERITY_PHRASES` (`test_review_severity_rule.py:112-117`); no cap number above 2 (`CAP_REGRESSION`, `:288-293`).
- **Drift test**: after removing frontmatter `name` and `description`, the Usage block, `## Review Loop`/`## Review Ledger Loop` and `## Unattended mode`, the variant equals `spec-panel.md`, so the 486-line panel cannot silently diverge. Run `uv run pytest tests/skills/test_review_severity_rule.py` first, as `DES:141` advises for 427, because its matchers scan every file under `src/` and `plugins/`.

<!-- Source: Base (original, modified): brief sentence replaced per Change #48 (orchestrator decisions D1 and D5) -->
**Experiment install (not a repo change).** As in D9 (`DEC:47`): the owner copies `spec-panel-ledger.md` to `~/.claude/commands/sc/` and the folder `sc-review-ledger/` to `~/.claude/skills/`; only the three review briefs change, by one line: `/sc:spec-panel` becomes `/sc:spec-panel-ledger --ledger <path> --revert-unclaimed`; the reviser briefs stay verbatim. The sweep route is described in section 9. A personal command beats a project one (`DEC:46`), and a different command NAME lets an arm run beside others (`AB:47`). Then `make sync-dev`, `make verify-sync`; never stage `.claude/`.

## 7. Adoption by `/sc:reflect`, rf-qa and the `/sc:implement` final review

<!-- Source: Base (original, modified): title names the real commands and the opening paragraph uses the PROFILES seam per Change #49 (Variant A s6 extension seam and s7, narrowed in A-R2); concurrent-writer limit removed because the lock is now in the kernel (Change #44) -->
Adoption is future work: nothing in this change edits an adopter, and each adopter is a later, separate change gated on the S1 result. What makes the core reusable is the `PROFILES` seam: an adopter adds one `PROFILES` row (its grade vocabulary, blocking predicate, cap and ordered guards) and an adapter section; a new guard needs kernel work and tests. `grade` takes the caller's vocabulary and `anchor` is a quote from one `--doc` file. One thing the first version does NOT do and adopters need: several files per ledger (v1 is single-file; a per-file snapshot and per-file hunks are the extension). Concurrent writers are handled by the kernel's lock (section 6).

<!-- Source: Base (original, modified): table cells updated per Change #49 (C-R2 C-031, C-032, C-033 rows; Variant C s7) -->
| Adopter | Rows come from | Needs | What stays different |
|---|---|---|---|
| `/sc:reflect` (`W/bs346-ledger/src/superclaude/skills/sc-reflect-protocol/SKILL.md`) | the merged Wave 5 findings after the evidence-validator, the "non-negotiable final gate" that drops unfounded items (`SKILL.md:587`), so rows are created only after that gate | a `--ledger` flag; a `reflect` `PROFILES` row for its deviation taxonomy (Authorized expansion, Necessary deviation, Drift, Regression, per the skill's own description); multi-file `--doc` for code or plan trees; the caller (implement or workflow) owns the loop, because reflect has no loop input in the lines I read (two long lines, `SKILL.md:3` and `:35`, were not opened: UNVERIFIED) | the Tier 2 heterogeneous fan-out and adversarial merge stay for the find pass only; verify rounds can use one Tier 1 reviewer, which is the cost saving; the taxonomy, not CRITICAL/MAJOR/MINOR, decides what is blocking; a ledger PASS cannot authorize promotion |
| rf-qa agents (`RFQA:379-416`) | the gate's findings | the Fix Cycle steps 1 to 5 (`RFQA:386-396`) already say "verify the blocking issues, do not recheck minor findings" in prose; the change is to replace "the previous QA report" by the ledger, step 2 by `verify`, step 4 by child rows, step 5 by `verdict`; an `rf-qa` profile with the ordered guards regression, then monotonicity (`RFQA:401`), then cap, keeping rf-qa's existing halt messages, its regression-first order (`RFQA:407`) and its dedup identity (`RFQA:414`); one paragraph in the agent file pointing to `~/.claude/skills/sc-review-ledger` | rf-qa grades CRITICAL/IMPORTANT/MINOR (`DES:72`); QA instances run partitioned and in parallel, which the lock serializes (or one ledger per partition); rf-qa "fixes issues in-place when authorized" (agent description), so finder and reviser can be one agent, and the actor that follows from the subcommand does not prove two sessions |
| `/sc:implement` final review (`W/bs346-ledger/src/superclaude/skills/sc-implement-protocol/refs/qa.md`, `managed-workspace.md:55`) | FINAL `issues` with `path:line` per AC | a ledger per archive attempt, a mapping from `F<k>.<j>` ids (`QA:137`) and status words `resolved|open|regressed` (`QA:143`) to `verified|reopened`, `origin=inherited` (`QA:166`) as the hunk rule | implement already splits "reviewer reports, orchestrator computes" (`QA:334`) and parent-written `sev=`/`origin=` (`QA:141`), so it is ahead of spec-panel on that point. But `QA:186` lets every re-review raise a new blocker anywhere in task-owned text, the opposite of verify-only, and every archive attempt keeps a fresh full FINAL. Recommendation: not adopted; do not adopt there until an implement incident shows the same fix-induced pattern (S5 is outside the S1 data, `AB:43`). |

<!-- Source: Base (original) -->
Order of adoption: spec-panel (this experiment), then rf-qa (the prose it already has maps one to one), then reflect; implement last or never.

## 8. Stateful reviewer session versus file ledger

<!-- Source: Base (original) -->
A stateful design keeps one reviewer session alive across the rounds (same Orca terminal, or `SendMessage` to the same agent), so "the ledger" is its own context.

<!-- Source: Base (original, modified): "hist" renamed "history" (Change #16); cost cell updated to the recounted calls and sessions (Change #62) -->
| Axis | Stateful session | File ledger with fresh sessions |
|---|---|---|
| Independence | the finder verifies its own findings; a fix is judged by the mind that wanted it | each verify is a new session; the round-3 reviewer of flg-r2 re-read live `worker-read --help` and the e2e evidence and found that the N5 fix was wrong in a way the "as asked" check passes (`F2R3:35`, `F2R3:86`); I infer a finder-verifier would more often stop at "resolved as asked" (inference, not measured) |
| Mechanical stop, cap, scope | none; every rule stays prose, which is the measured failure (`DES:143`, `F2D1:10`) | refusal codes, a counter, a hunk check |
| Survives crash, compaction, a new worker | no; the report is the only record | yes; the file is the record and the audit trail (`history`) |
| Cost | cheapest: no script, no row parsing, no extra calls | about 15 to 20 script calls per loop and up to one extra session (section 11) |
| Fits the other tools | no: rf-qa and implement spawn fresh subagents by design (`managed-workspace.md:55` "always a Task subagent, even N=1") | yes: the ledger is the only thing that crosses the fresh-session boundary |
| Fits the S1 test | changes the experimental variable (S1 uses a fresh reviewer per review, `F2R3:3`) | keeps it |

<!-- Source: Base (original, modified): "severity" read as grade; one sentence appended per Change #50 (Variant C-R2 C-034 row) -->
**Recommendation: the file ledger, with fresh sessions.** The state worth keeping is small (id, anchor, grade, status, claim); a file carries it exactly and lets a script, not a model, enforce it. A stateful session is the cheap fallback experiment if the ledger does not beat 427: same briefs, one reviewer kept alive, no script. It cannot be adopted by implement or rf-qa without breaking their fresh-reviewer rule. The file ledger is authoritative: output from a resumed or cached session must carry the current round, document hash and ledger sequence (section 6, Output and input binding) or it is refused; a stateful-session arm stays a cheap later experiment, outside this change.

## 9. Measurement plan on scenario S1

<!-- Source: Base (original, modified): changes (1) and (3) replaced and (4), (5) added per Change #51 (orchestrator decisions D1 and D5; smoke check from B-R2 New evidence 1) -->
**Arm "led"** (two fresh worktrees, for example `exp346-ab-led-r1` and `-r2`), identical to Arm B in everything D11 fixes: scenario S1, base commit 2cb683f5, overlay, verbatim briefs T05 to T09, model claude-opus-5-5, `WORKER-CONTRACT.md` moved aside, watcher on the installed command sha256 (`DEC:59`, `DEC:64`). Changes, all recorded: (1) in the three review briefs only, `/sc:spec-panel` becomes `/sc:spec-panel-ledger --ledger <L> --revert-unclaimed` (no `--re-review`, no `--baseline`); the flag is the consent that unclaimed-hunk reverts require (section 2, item 3), given by whoever wrote the invocation line. Reviser briefs are unchanged: they read the report, and the report carries the script-written Reviser brief. (2) The owner installs the command and the `sc-review-ledger` folder by hand (section 6). (3) Before replicate 1, one throwaway dispatched worker with the T09 wrapper spawns one subagent that reads a file and prints its hash. Yes means the sweep is a subagent of the terminal review session, with a heartbeat before and after the Agent call (the wrapper requires "Send a heartbeat every 5 minutes", `W/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/T09-R3-reviewer-L11-1c9a7ec8.md:31`, as quoted in the Round 2 debate). No means a sixth dispatch, `/sc:spec-panel-ledger @<spec> --mode critique --focus requirements,architecture --ledger <L> --sweep`, which reviews only the copy that `sweep --prepare` prints, declared as a deviation. (4) Reruns use `init --archive-existing` (section 6). (5) The coordinator runs `status` before each dispatch (section 2, item 8). The arm differs from Arm B in three recorded ways: the command name, the `--revert-unclaimed` flag and the sweep route.

<!-- Source: Base (original, modified): ordering and decision rule added per Change #55 (invariant probe INV-028); the procedure follows section 2, item 6 -->
**Baseline sweeps, run first** (so "hiding" can be measured, not argued). Before any ledger replicate, run the same sweep procedure (a copy in a fresh temporary folder, one whole-document critique with the same focus), as a plain `/sc:spec-panel` critique, on the FINAL spec of each existing replicate: ctl-r1, ctl-r2, trt-r1, trt-r2, flg-r1, flg-r2 (copies made read-only first; the worktrees hold them under `.dev/orca-command-refactor/specs/`). That gives how many CRITICAL or MAJOR findings a whole-document pass still finds in a 427-loop document, the number the ledger's sweep is compared with. Decision rule, declared before replicate 1: if the mean CRITICAL or MAJOR count of the six baseline sweeps is 3 or more, the combined bar cannot be met by the ledger alone, and U3 and the sweep are reported separately as the primary result. Reason: pre-existing defects that review 1 missed are relabelled, not prevented (section 10), so such a baseline breaks the combined headline even when U3 is 0.

<!-- Source: Variant A s9 V1-ledger and orchestrator decision D11, merged per Change #57 (invariant probe INV-023, INV-006, INV-002, INV-011; D3; C-R2 C-040 row; A-007 row) -->
**Validity checks (mandatory, per replicate).**
1. **V1-ledger**: the ledger shows rounds 1 to 3 or an earlier terminal decision, the snapshots, a sweep record or `sweep_skipped`, and no `E-TAMPERED`; a replicate whose sessions never ran the script is "ledger not honoured" (the same rule `DEC:64` applies to Arm B as "flags not honoured"). A sweep report that cites any ledger row id fails V1-ledger.
2. **Blinded `wrong_outcome` audit**: if more than 30% of MAJOR-blocking rows are judged filler, the replicate is "grading not honoured"; the cut-off is pre-registered; the review-1 grade distribution is recorded.
3. **Install record**: command, skill and script hashes, and any live-document-versus-snapshot mismatch.
4. **Auto-claim count** per cycle (section 2, item 3).
5. **Verdict disagreements**: every case where the reviewer's own verdict and the script's last line differ (section 4, Report tail).
6. **Final status**: one `status` after the last dispatch, recorded (section 4, Tail protection).
7. **M3 causation**: adjudicated by the analyst from the script's location attribution (section 3, Claim width and attribution).

<!-- Source: Base (original, modified): P3 and P3s replaced by the headline per Change #52 (orchestrator decision D11, invariant probe INV-015, Variant C s9 U3 and W); P3 kept as U3; deferred floor added per Change #53; Growth and Scope bullets replaced per Change #58 -->
**Metrics** (D5 M1 to M5 as before, `DEC:23`, plus these, all read from `L` or the script, not from report prose):
- **Headline** = `|U3 union W union O|`:
  - `U3` = rows of grade CRITICAL or MAJOR whose status after the review-3 `close` is not `verified`, deferred rows included. Grade, not `blocking`, so that MAJOR rows 427 relabels as minor are counted exactly as the Arm B proxy counted them (`ARMB:37`). A `reopened` row is the ledger name for what the control reports call "Partly" (`C1R3:17`), so the two are comparable. `U` (blocking only) is reported beside it. `U3` alone (the base's P3) is the analogue of Arm B's hunk-scoped review 3 and stays a secondary number.
  - `W` = deduplicated sweep CRITICAL or MAJOR rows plus sweep challenges to verified rows.
  - `O` = `scope=outside` CRITICAL or MAJOR rows (verify-time allegations outside the hunks and reviser-gap rows). The union counts a row once, whichever sets it falls in.
  - Duplicates: the script only proposes `dup_of` candidates; a blinded analyst rules each one duplicate, child or challenge (N5 and N12 overlap in AC-0.4 but are distinct harms). The headline uses the ruled count and publishes the raw count and the auto-matched count as bounds; until the ruling exists, only the two bounds exist.
  - A run that ends early is counted at its terminal review and carried to the R3 horizon without inventing a review.
  - The headline replaces the base's P3s (P3 plus the sweep's CRITICAL or MAJOR rows), which was the pre-registered conservative metric because the control's review 3 was a whole-document pass (`AB:30`).
- **Deferred floor**: a deferred MAJOR row (no `wrong_outcome`) can never become `verified`, so it is a permanent floor on `U3`; with four such rows the bar is unreachable whatever the loop does. Publish the deferred CRITICAL or MAJOR count as its own number, pre-register whether the bar is applied with or without it, and compute the control's comparable number (control MAJOR findings with no concrete wrong outcome, read by the same rubric) so both arms are measured on the same population.
- **H, hidden-defect share** = sweep CRITICAL/MAJOR rows / (U3 + sweep CRITICAL/MAJOR rows), split by the script into `in_claimed_span`, `in_unclaimed_hunk`, `outside_hunks`.
- **Growth after 2 fix cycles** = size of the accepted snapshot after revise 2 against 57,763 bytes, as in `AB` and `ARMB` (flg-r2: 76,328 / 57,763 = +32.1%, `ARMB:16`). Beside it: bytes discarded by reverts, bytes of unclaimed hunks left in place, and bytes inside deferred-row spans. A growth gain explained mostly by discarded bytes is reported "not attributable to better fixes".
- **Scope metrics**: `minor_touched` (hunks overlapping the anchor span of a deferred row), split into hunks admitted by an answer and hunks admitted by paragraph auto-claim; unclaimed bytes; revert count; `E-CLAIM-WIDE` count; `scope=outside` count; the `X` count (section 4).
- **Cost**: script calls, sessions, wall time per step, report bytes per review (flg-r2 baseline: 50,563, 48,693, 39,100 bytes for reviews 1 to 3, from `ls -la`).

<!-- Source: Invariant probe INV-027 and the A-012 row, merged per Change #54 -->
**Pre-registered quantities.** B1 (blocking rows after review 1), r1 and r2 (new blocking rows per blocking fix in cycles 1 and 2) are measured per replicate, and U3 is reported against B1 x r1 x r2. With B1 = 13 and r = 0.46 twice the product is 2.7 before any sweep or deferred row; B1 of 39 or more at the measured 0.46 then 0.17 exceeds 3. The claim "the ledger alone meets the bar" is falsified if the measured product exceeds 3 in either replicate (section 1).

<!-- Source: Base (original, modified): restructured into two claims per Change #56 (orchestrator decision D11, invariant probe INV-029); P3s replaced by the headline per Change #52 -->
**Bar (set now, same shape as D10 and D11).** Two claims, each with its own comparator.
- (a) **Ledger plus 427, against control.** The ledger arm counts as better than control only if: the headline mean is at most 3 (50% of control mean 6.0, `AB:19`), or a clean pass in fewer rounds; growth is at most 44.4%; the effect exceeds the larger within-arm spread; and every ledger replicate is on the better side of both control replicates for the headline and growth (R3 proxy 8 and 4, so each replicate at most 3; growth below 57.7%).
- (b) **The ledger's own effect, against Arm B** (427 plus flags, the second comparator): headline mean below 3.5 and growth at most 30.0% (`ARMB:20`). The ledger arm carries 427 grading through the profile, so a win against control credits both; only (b) isolates the ledger.

<!-- Source: Base (original, modified): trace rows kept; forecasts relabelled planning aids; flg-r2 row mechanism replaced per Change #59 (orchestrator decision D1, A-012 row); P3 renamed U3 per Change #52 -->
**Predictions, grounded in traced rows.** The numeric forecasts below are planning aids, not calibrated predictions; each is recomputed from the replicate's measured B1 (Pre-registered quantities).

| Trace | What the ledger loop would have done | U3 |
|---|---|---|
| flg-r2, review 3 (`F2R3`) | F22 stays deferred (`answer` is refused on it). Its hunk is admitted only if it falls inside a blocking row's enclosing paragraph; otherwise `begin` reverts it (the arm passes `--revert-unclaimed`), so the AC-0.4 WC-1 proof never reaches review 2 and N5 and N12 never exist; the other five blocking N-rows were resolved at review 3 (`F2R3:31-36`). This holds only if the F22 hunk falls outside every blocking row's enclosing paragraph in AC-0.4; the condition is checked on `HIST/spec-v2-after-round1.md` before the run and printed here. If a blocking row shares that paragraph, auto-claim admits the F22 edit and the N5 and N12 chain can recur. | 0 to 1 (1 if a different child appears), when the condition holds |
| ctl-r1, review 3 (`C1R3:181-189`) | 8 blocking findings; every one has an anchor inside the changed lines, so verify finds all 8; R3-9 may trace to minor row M2 (`C1R3:196` "M2 resolved for the named instance with a separate defect"), which the ledger would not have edited | 7 to 8 |
| ctl-r1, sweep share | R3-4, R3-8, R3-9 predate the revision and were missed in round 2 (`C1R3:205`); verify-only would leave them to the sweep | sweep 3 or more |

- **U3 (verify only, the base's P3)**: mean 3.0, plausible range 0 to 7; chance that both replicates are at most 3: about 30%. The shape is bimodal: a clean-ish run when the damage chain starts from a minor row, an unchanged run when it starts from blocking rows.
- **Sweep (CRITICAL/MAJOR)**: mean 3, range 1 to 6 (UNVERIFIED; anchored only on ctl-r1's three pre-existing blockers and on R1 counts of 9 to 17 for a whole-document pass, `AB:13`, `ARMB:13`).
- **U3 plus sweep (the base's P3s)**: mean about 5.5, so bar (a) is probably NOT met on the conservative metric. The headline also adds the deferred floor and `O`, so 5.5 is a lower estimate for the headline.
- **Growth**: mean 23% (range 17 to 30). Derivation: Arm B cycle-1 growth 17.5% and 21.6% times (1 - 0.15), plus the cycle-2 increments 10.3 and 10.5 points times (1 - 0.38), where 0.15 and 0.38 are the shares of changed-line bytes carrying only a minor finding id in flg-r2 (3,920 of 26,768 for revise 1; 7,212 of 19,205 for revise 2; my `diff -w` attribution of whole lines, one replicate, so an upper bound on the saving). Gives 21.3% and 24.9%. The 44.4% growth bar of claim (a) passes, but 427 already passes it (`ARMB:24`), so growth cannot show the ledger is better.

<!-- Source: refactor-plan.md "Changes NOT Being Made" rows C-036 (Variant A and Variant C forecasts), recorded here so section 9 says which forecasts were withdrawn -->
**Forecasts withdrawn in the debate.** Variant A's forecast of 2.5 (range 1 to 4) for the R3 count was withdrawn by its author: its basis used the wrong row (R1 blocking in flg-r2 was 13, not 5 to 6; `ARMB:13`, `F2D1:39`). Variant C's forecast of 1.5 for the R3 count had no stated basis and was conceded unsupported by its author. Neither is used here.

<!-- Source: Base (original, modified): failure list replaced per Change #60 (orchestrator decision D11, Changes #52 to #58) -->
**What result would mean the idea failed.** Any of: (1) headline mean 4 or more, or, for the ledger's own effect, a headline mean not below Arm B's 3.5; (2) the ledger sweep finds at least 2 more CRITICAL/MAJOR rows on average than the baseline sweeps find (the loop hid defects instead of preventing them); (3) `minor_touched` above 0 in either replicate with `--revert-unclaimed` on, reported by admission path; (4) a stalled loop caused by the script (a refused call with no recovery path) in either replicate; (5) growth above 30.0% after the discarded bytes are shown; (6) V1-ledger or the `wrong_outcome` audit failing in either replicate (that replicate is then not treatment, not a failure of the idea, and is rerun with `init --archive-existing`); (7) measured B1 x r1 x r2 above 3, which falsifies "the ledger alone meets the bar" (Pre-registered quantities). A result inside the spread of both arms is "not significant", as D6 says.

## 10. Which measured causes the mechanism removes and which it leaves

<!-- Source: Base (original, modified): rows 2 and 6 updated per Change #61 (orchestrator decisions D1, D2, D4; invariant probe INV-008); rows 4 and 5 renamed for the removed sev field (Change #17) and the new refusal codes (Change #42); other rows unchanged -->
| Cause | Measured evidence | Verdict | How, and what remains |
|---|---|---|---|
| Fix-induced defects on changed lines | 89% (R2) and 100% (R3) of new findings are `origin=changed` (`AB:30`); flg-r2: 13 blocking fixes gave 6 new blocking (0.46 per fix), 6 gave 1 (0.17) (`F2R2:13`, `F2R3:15`) | **LEFT** | The reviser still writes the defects. The ledger finds them as child rows and names the fixes that claimed each hunk (`caused_by`), which helps the next reviser, nothing more. |
| Reviser applies minor rows and "related defects" | 9 of the 15 rows applied in revise 2 were non-blocking (N7 to N11, C9, C12 to C14; `F2D2:35`); the F22 chain (`F2D1:37`); E5 and AC-1.2 fixed "while applying" (`F2D2:13`) | **REMOVED for minor rows, PARTLY for scope** | `answer` refuses deferred rows; `begin` auto-claims only hunks inside a blocking row's paragraph; unclaimed hunks are reported, and reverted with `--revert-unclaimed`. The remaining leak is a minor edit inside a blocking row's paragraph, and a claim no wider than `E-CLAIM-WIDE` allows (E5 was the same false claim as N4's, so it was claimable). Bytes per claim and per revert are recorded. |
| Reviser adds a mechanism inside a blocking fix | N12 came from the N5 fix adding a new "record the agent command" step (`F2R3:15`, `F2R3:35`) | **LEFT** | Nothing in a script can tell a needed step from an extra one. Per-row byte budgets belong to the minfix theme. |
| Severity drift between rounds | thin: the one traced case is a panel disagreement on a NEW row, resolved upward (`F2R3:144`); 427 grading relabels MAJOR as minor in flg-r1 (`ARMB:37`) | **REMOVED for existing rows, LEFT for new rows** | `grade`, `rule` and the computed `blocking` are frozen, and a verifier cannot raise a row. A child row still gets a fresh grade from the verifier; `wrong_outcome` is required for MAJOR-blocking so the grade is auditable, but who judges it is a model. |
| No mechanical stop, verdict by judgement, brief overriding the command | "any finding of any severity is FAIL" in the brief (`F2R3:15`); count kept by prose (`DES:162`) | **REMOVED** for the reviewer session | counter, cap (`E-CAP`), terminal phase (`E-TERMINAL`), computed decision, last line written by the script. A coordinator that loops anyway is not stopped (PROSE). |
| Pre-existing defects found late | 3 of the 8 ctl-r1 review-3 blockers predate the revision (`C1R3:205`) | **RELABELLED, not prevented** | they surface in the sweep and are reported, not fixed; verify-time allegations outside the hunks are now counted as `scope=outside` rows. |

<!-- Source: Base (original) -->
**Why two fix cycles cannot be promised to converge, with or without the ledger.** If each cycle leaves a fraction r of its blocking fixes as new blocking defects, the expected count at review 3 is about B1 x r x r. With B1 = 13 and the two measured ratios 0.46 then 0.17 it is 1.0 (flg-r2's actual 1); with r = 0.46 twice it is 2.7; with r = 0.17 twice it is 0.4. PASS inside the cap needs B1 x r x r below 1, so the mechanism's honest ceiling is "escalate with 0 to 3 rows", not "always PASS". Only a lower r (a better reviser) or a lower B1 (a better find pass) changes that; the ledger changes neither directly. Its only lever on r is fewer edits (minor rows) and visible bytes per claim.

<!-- Source: Base (original, modified): items 1 and 5 updated per Change #61; item 2 and the data paragraph renamed for the verify subcommand (Change #4) -->
**The strongest argument that a verify-only pass hides defects instead of preventing them** (I tried to make it as hard as I can):
1. U3 is lower than a whole-document R3 by construction. Anything outside a hunk cannot become a blocking row in verify, so the number of loop rows can only fall; if I report U3 and not the rest, the idea looks better while the document is no better. The ctl-r1 trace shows the size of that effect (3 of 8, `C1R3:205`). That is why `O` and `W` enter the headline (section 9).
2. Interaction defects are the likely casualties. N15 in flg-r2 (step 1 unchanged, contradicted by 2.3, `F2R3:99-101`) is exactly an `origin=unchanged` finding; the ledger counts it only as a never-blocking `scope=outside` row unless the reviewer finds the right `depends_on` quote. So the reviewer is now paid to find a changed line to hang the defect on.
3. Two tick-box answers per row invite "yes, yes". The real round-3 reviewer did far more than tick: it re-ran greps and read live help (`F2R3:51`, `F2R3:86`). A satisficing verifier passes fixes that deserve N12.
4. The sweep is the only guard, and by design nothing it finds is fixed. A PASS at review 2 with a sweep that returns 4 blocking rows is a hollow PASS that the user sees only at the end.
5. A model that cannot add a row anywhere may add it nowhere. `verify` no longer refuses out-of-scope allegations, so the incentive to file nothing is reduced, and the `scope=outside` count is the new early-warning number next to `outside_hunks`.

<!-- Source: Base (original, modified): "mark resolved=yes" renamed to the verify result per Change #4 and Change #10; item (5) counter updated per Change #61 -->
**What the data say about it, and what they do not.** For (1): the three pre-existing ctl-r1 blockers still have an anchor inside a changed line (R3-4 at `SPEC:245`, R3-8 at `SPEC:207,210`, R3-9 at `SPEC:224,238`, all in the changed list at `C1R3:11`), and all eight blockers do; so in the two traces hunk-anchoring lost nothing. That is two documents, one reviewer model. It does not exclude far-from-hunk defects, which only the baseline sweeps (section 9) can measure. For (3) I add one mechanical counter: a `resolved` result requires an evidence quote that must be present in the new snapshot (it proves the reviewer opened the text, not that it judged well). For (5) the counters are the sweep's `outside_hunks` count and the `scope=outside` count. Items (2) and (4) stay open risks.

## 11. Risks and costs

<!-- Source: Base (original, modified): sessions and script-call bullets replaced per Change #62 (orchestrator decision D5, B-R2 New evidence 1); wall-time and token bullets kept with renamed subcommands -->
**Costs per loop** (counts are from the section 2 table; times are estimates, UNVERIFIED):
- Sessions: 5 if the smoke check passes (the sweep is a subagent of the terminal review session), else 6 (reviews 1 to 3, two revisers, one sweep dispatch). The experiment adds the smoke-check worker and up to 6 more sessions for the baseline sweeps (section 9). The subagent route costs a heartbeat before and after the Agent call (the T09 wrapper rule, section 9).
- Script calls: about 3 in review 1 (`init`, `find`, `close`), 0 to 2 per revise (the S1 reviser runs none), 4 per verify (`status`, `begin`, `verify`, `close`), 2 in the sweep (`sweep --prepare`, `sweep --input`). That is 13 to 17 per loop from the steps alone and about 15 to 20 with retries and the coordinator's `status` checks, below the base design's 20 to 31; each one is a `uv run --no-project python` start (well under a second each, not measured).
- Wall time: the sweep is a full review. File times in both worktrees show 9 to 16 minutes between a disposition and the next review report (flg-r2: disposition 13:14, round 2 at 13:26; disposition 13:32, round 3 at 13:41; `ls -la` of `W/exp346-ab-flg-r2/.dev/orca-command-refactor/review/`), so expect about +10 to +15 minutes per loop minus whatever the shorter verify reports save. Verify reports (48.7 KB and 39.1 KB for reviews 2 and 3 in flg-r2, `ls -la`) may shrink because the `## Ledger` table that `close` appends replaces the hand-built Part 1 table; not measured.
- Tokens: findings are written once as JSON input rows and the report narrative refers to ids, instead of the report holding them alone. If the reviewer writes both in full, output tokens rise. The Find bullet asks for each finding as a row.

<!-- Source: Base (original, modified): items 1, 7 and 8 modified and items 9 and 10 appended per Change #63 (orchestrator decisions D1, D2, D6; invariant probe INV-007, INV-019); items 5 and 6 renamed for T12 and E-TAMPERED -->
**Ways the ledger could make the loop worse**
1. The refusal paths stall a loop. Unclaimed hunks no longer refuse, and a failed revert preimage becomes `cannot-verify` instead of a stall; the residual stall paths are an anchor that is absent or repeated (`E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`) and `E-CLAIM-WIDE`. Mitigations: the error text lists candidate lines; `--at`; auto-claim needs no reviser call. Residual: MEDIUM until the script has run on three real documents.
2. Hidden defects (section 10, items 1, 2, 4, 5). The baseline sweeps are how this is measured.
3. A moved section turns every line into a hunk, so verify degrades to a full review. The script prints `HUNKS_LARGE` when changed lines exceed 40% of `DOC` (my threshold, UNVERIFIED as right) and the report tail repeats it.
4. Deferred minor rows stay unfixed; a minor ambiguity can later be an implementer's wrong outcome. S1 cannot show this because it ends at review 3.
5. A wrongly graded first row forces a fix cycle and cannot be demoted; the user's `defer` (T12) records their words but changes no recorded outcome.
6. A harmless reformat of `ledger.json` by a person fails the hash (`E-TAMPERED`) and stops every command. A `reseal --reason` command is needed (open question 3).
7. Experiment confounds: the name change, the hand install, the sweep route (subagent or sixth dispatch), the `--revert-unclaimed` flag, and a sweep context that reads `L` anyway; the last is now detectable when a sweep report cites a ledger row id (V1-ledger, section 9).
8. An unattended coordinator told to "re-review until PASS" meets `E-TERMINAL` after a terminal decision and `verdict` exit 11 at ESCALATE, and may hang or retry. The command's Cap bullet says HALT, and the `E-TERMINAL` body says "do nothing further".
9. Auto-claim admits a minor edit written in a blocking row's paragraph (section 2, item 3). It is measured by `minor_touched` split by admission path, not prevented.
10. Two verdicts in one report (the reviewer's own and the script's last line) can mislead a reader who stops before the last line (section 4, Report tail). The analyst records every disagreement.

<!-- Source: Base (original, modified): rows for the role flag, unclaimed hunks, claims in hunks, sweep independence and verdict replaced, and rows for auto-claim, --revert-unclaimed, scope=outside, terminal phase, report tail and request-digest idempotency added per Change #64 (S-012 row; C-R2 S-012 row) -->
**Rule by rule: MECHANICAL (script-enforced) or PROSE (a model is asked), and the residual risk**

| Rule | Kind | Residual risk |
|---|---|---|
| Row ids, anchor exists, MAJOR-blocking has `wrong_outcome`, `blocking` computed by the profile, non-blocking rows auto-deferred | MECHANICAL | a quote proves presence, not relevance; `wrong_outcome` can be filler (audited, section 9) |
| Phase order (`init`, `find`, `close`, `begin`, `verify`, `sweep`) | MECHANICAL | none beyond bugs |
| Who may call what | PHASE is MECHANICAL; IDENTITY is PROSE | the actor follows from the subcommand, but any session can run any subcommand |
| Frozen `grade`, `rule`, `wrong_outcome`, `blocking`, `anchor` | MECHANICAL | the first grade is a model's judgement |
| Illegal transitions refused (T1 to T12, forbidden moves) | MECHANICAL | none beyond bugs |
| Minor rows unanswerable | MECHANICAL | the reviser can still edit the text; the edit is admitted only inside a blocking row's paragraph |
| Auto-claim at `begin` | MECHANICAL | a minor edit in a blocking paragraph is admitted |
| Unclaimed hunks reported; reverted only with `--revert-unclaimed` | MECHANICAL detection and revert; the consent is the invocation line, written by a person or a brief | without the flag, unclaimed minor edits survive; a failed preimage becomes `cannot-verify` |
| A `fixed` claim names an edit in the row's span, no wider than its paragraph | MECHANICAL (`E-FIXED-NO-EDIT`, `E-CLAIM-WIDE`) | a long paragraph is a wide unit; text added inside a claimed span is invisible to the check |
| Every plan row answered once; `verify` refuses a missing answer | MECHANICAL (`E-INCOMPLETE`) | answer quality, yes-yes bias; evidence only proves the text was opened |
| New rows `scope=in` only in hunks or with `depends_on` in a hunk; anything else `scope=outside` | MECHANICAL | interaction defects stay non-blocking; honesty of `depends_on` |
| `scope=outside` rows counted, never blocking | MECHANICAL | a verifier that runs a whole-document panel swells `O`; the count is then visible rather than hidden |
| No whole-document panel during verify | PROSE | a reviewer may run it anyway, costing time; its rows become `scope=outside` rows |
| Review counter, cap, loop decision | MECHANICAL | a coordinator that ignores refusal codes |
| The verdict line | MECHANICAL for the last line; PROSE for the reviewer's own verdict above it | a reader who stops before the last line |
| Terminal phase refuses further loop work (`E-TERMINAL`) | MECHANICAL | a coordinator that dispatches anyway gets refusals, which it must read |
| Report tail protected (`E-REPORT-EDITED`, the sweep re-check, one final `status`) | MECHANICAL, except that the analyst runs the final `status` (PROSE) | an edit made after the final `status` |
| Retries idempotent by request digest; stale sequence or binding refused | MECHANICAL | a lost input file or a changed `D` needs manual recovery |
| Sweep feeds no reviser; the terminal phase refuses `verify` and `answer` | MECHANICAL | a person may start a new ledger from the sweep rows (a decision, not a leak) |
| Sweep independence | MECHANICAL for the copy and the row-id check; PROSE for not opening the ledger folder | anchoring; shows up as an `in_claimed_span` count of 0 or a cited row id |
| Brief may narrow, not widen | PROSE text, but its main effects (no answer to deferred rows, no verdict from a brief) are MECHANICAL | a brief can still direct edits outside any row; they are reported, or reverted with the flag |
| Variant equals `spec-panel.md` outside the replaced sections | MECHANICAL (drift test) | none |
| Dual lookup of the script path | PROSE; the test pins the text only | a host with neither copy fails at the first call, loudly (exit not 0) |

## 12. Open questions

<!-- Source: Base (original, modified): restructured per Change #65 (orchestrator decisions D1, D2, D5, D8; invariant probe brief readings); kept questions renumbered, three questions added, UNVERIFIED list narrowed -->
1. **Sweep findings with cycles left.** If the loop decision is PASS with fix cycles left and the sweep finds blocking rows, this design only reports them (as the theme says). Should a second ledger be started from them, by default or only by the user? Recommendation: only by the user.
2. **Several files.** v1 is one `--doc`. reflect and rf-qa need per-file snapshots and per-file hunks (section 7). Build now or at adoption?
3. **`reseal --reason`.** The body hash catches hand edits but also harmless reformatting. Add a logged reseal command, or drop the hash and rely on schema and phase validation?
4. **Per-row byte budget.** Bytes per claim are reported, not limited. A limit is the minfix theme; should this script carry the field so both themes share one checker?
5. **Who grades child rows.** The freeze covers existing rows only. A frozen rubric or an independent confirmation of each new blocking row belongs to the stoprule theme; the two could share the `wrong_outcome` field.
6. **Hunk computation parity.** `difflib` on raw and whitespace-normalized lines versus `git diff --no-index -w -U0` (`F2R3:25`): they can differ on moved text. Test on the three S1 history pairs (`HIST/spec-v1-draft.md`, `spec-v2-after-round1.md`, `spec-v3-after-round2.md`) before the first run, pick the `HUNKS_LARGE` threshold from them, and calibrate the paragraph admission unit on the same pairs.
7. **Smoke-check result.** Whether a dispatched Orca worker can spawn a sweep subagent and keep its heartbeats decides the sweep route (section 9); until the check runs, the subagent route is UNVERIFIED.
8. **`E-CLAIM-WIDE` and auto-claim frequency.** How often a real document's paragraphs make the claim unit too wide, and how many hunks auto-claim admits per cycle, is unknown until the script runs on real documents.
9. **Blinded rulings.** Whether the blinded analyst steps (the duplicate ruling, the deferred-floor reading of the control reports and the `wrong_outcome` audit, section 9) can be staffed before replicate 1; without them only the raw and auto-matched bounds exist.
10. **UNVERIFIED in this spec**: that every worker environment has `uv` (the `managed-workspace.md:54` pattern assumes it); that no S1 brief passes `--unattended` (the round-3 run line shows none, `F2R3:80`, and the invariant probe found no `--unattended` token in `BR/T05-R1-reviewer-L11-699ae853.txt`; the probe also opened `BR/T06-R1-reviser-L10-3bb70411.txt` and `BR/T09-R3-reviewer-L11-1c9a7ec8.txt`, so only the S1 briefs other than those three remain unopened); the size of any token or wall-time saving; whether `reflect`'s two unopened long lines (`SKILL.md:3`, `:35`) describe a loop input; the yes-yes rate of a verify reviewer; whether `plugins/` tests would need a mirror (the plugin command list in `tests/unit/test_cli_install.py:399-404` suggests not).

<!-- Source: Change #65 (closed questions) -->
**Closed by this merge** (base question numbers): base 2, unclaimed hunks (reported by default, reverted only with `--revert-unclaimed`, section 2, item 3); base 3 in part, parallel writers (the lock is in v1, section 6; several files stays open as question 2); base 6, sweep independence (a copy in a fresh temporary directory, section 2, item 6); base 9, the coordinator brief (kept verbatim; auto-claim at `begin` lets the loop run without a brief edit, section 2, item 3).
