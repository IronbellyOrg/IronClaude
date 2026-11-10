# SPEC: finding ledger for document review loops (issue 346, theme "ledger")

Status: design only, nothing implemented. Variant command: `/sc:spec-panel-ledger`.

Built from `/sc:brainstorm --unattended` (3 proposals, 2 debate rounds, an invariant probe, a merge). `merged-requirements.md` in this folder is the full merged design (531 lines); `nested/adversarial-1/adversarial/` holds every debate artifact. This file stands alone; "merged sN" points into `merged-requirements.md` for detail only. Paths starting `exp346-` are other worktrees under `/home/coder/workspaces/worktrees/IronClaude/`, read-only.

## 1. Problem and evidence

- PR 427 halves spec growth on S1 (control +63.5%, 427 +29.7%, 427 plus flags +30.0% after two fix cycles) but no run of any arm reached PASS; review-3 critical+major was control 8 and 4, 427 6 and 5, 427 plus flags 6 and 1 (`exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md:13-19`, `ARMB-REPORT.md:13-20`).
- 89% (review 2) and 100% (review 3) of new findings sit on lines the previous fix changed (`AB-REPORT.md:30`): each later whole-document look finds defects the last fix made or exposed.
- Revisers apply minor findings when the brief says "apply confirmed findings": flg-r2 applied 8 of 9 non-blocking findings in cycle 1 and 15 of 15 rows (9 non-blocking) in cycle 2 (`exp346-ab-flg-r2/.dev/orca-command-refactor/review/disposition.md:39`, `disposition-round2.md:35`).
- Verdict, review count, baseline and scope are prose: "every rule here is prose read by a model" (`docs/designs/spec-panel-review-loop.md:143`), "nothing enforces the count" (`:162`).
- Theme: find once (review 1), then only verify ledger rows, with a script that owns the rows, the counters and the verdict.

## 2. Mechanism

**Parts.** One stdlib Python script, `review_ledger.py`, is the only writer of the ledger. Models never edit ledger state: they write small JSON input files and their own reports, and the script validates and ingests them atomically. Every call is `uv run --no-project python "<skill base>/scripts/review_ledger.py" <subcommand> ...` (the call shape `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:54` already uses). The actor is implied by the subcommand; there is no role flag.

**Where the ledger lives.** `<doc dir>/<doc stem>.review-ledger/` by default (overridable with `--ledger <dir>`), holding `ledger.json`, `snapshots/r1.md r2.md r3.md` (the exact text each review saw), `diffs/c1.json c2.json`, `inputs/*.json`, `plan-r2.md plan-r3.md` and `.lock`. The path is derivable from the document alone, so a session that loses a flag still finds the ledger, and `init` refuses when one exists (`E-EXISTS`): a lost flag can never restart a first review, which is the 427 failure "without them the run is a first review" (`src/superclaude/commands/spec-panel.md:261`). For S1: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger/`.

**The loop, step by step.**

1. **Review 1 (FIND, the only full find pass).** Fresh reviewer session. `init --doc D --profile spec-panel` snapshots `D` as `r1.md` and prints `review: 1 of 3`. The panel runs unchanged over the whole document. Each finding becomes a row in `inputs/r1-find.json` with `grade` (CRITICAL/MAJOR/MINOR), `rule` (for example FR-8), `wrong_outcome` and an exact anchor quote; `find` checks each anchor is present once (`E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`), and the profile, not the model, computes `blocking = grade == CRITICAL or rule in {FR-8, FR-9} or (grade == MAJOR and wrong_outcome non-empty)`, which is 427's grading rule (`spec-panel.md:259`) made a formula. Non-blocking rows are stored `deferred`. `close --report R1` appends the script tail (rendered ledger, Reviser brief, decision line) to the report.
2. **Revise 1.** Separate reviser session, brief unchanged. It edits `D` from the Reviser brief in the report. Running `answer` (claim hunks per blocking row) is optional, because the S1 reviser briefs run no script. Answers on a `deferred` row are refused (`E-ILLEGAL`), so a minor row can never be "fixed" through the ledger.
3. **Review 2 (VERIFY).** Fresh reviewer session. `begin --doc D` snapshots `r2.md`, diffs it against `r1.md` (difflib, whitespace-insensitive, old and new ranges, deletion tombstones), applies reviser answers, then **auto-claims** every remaining hunk that overlaps an open blocking row's anchor span widened to its enclosing paragraph (this is what lets a cycle progress when the reviser never ran `answer`). Hunks no blocking row claims are **unclaimed**: reported with their bytes, and restored to the snapshot text only when the invocation carries `--revert-unclaimed` (spec-panel's own rule is never to "Modify specifications without explicit user consent", `spec-panel.md:475`; the flag is that consent). `begin` writes `plan-r2.md`: every blocking row still open, its frozen grade and wrong outcome, its old anchor and the old and new text of its hunks, plus the unclaimed hunks. The verifier answers every plan row once with `resolved`, `open`, `regressed` or `cannot-verify`, an evidence quote that must exist in the new snapshot, and `touched_ok` (did the change break the sentence it touched; `no` requires a child row). Then one **new-defect check** over this round's hunks only, both diff sides. A new row anchored inside a hunk is `scope=in` and can block (`origin=changed`, `caused_by` = the rows that claimed the hunk). An allegation outside the hunks is not refused: it is stored `scope=outside`, never blocks, and is counted in the measurement headline, so nothing lives only in report prose. `verify` refuses a missing plan answer (`E-INCOMPLETE`). `close` computes the decision.
4. **Revise 2.** As revise 1.
5. **Review 3 (VERIFY, last).** As review 2 against `r2.md`; the decision can only be PASS or ESCALATE.
6. **Final sweep (once, not a review, never looped).** A fresh context that has not read the ledger critiques the whole accepted snapshot, given as a copy in a temporary folder by `sweep --prepare`. Its rows are stored `deferred` with `round_found=sweep` and a location class (`in_claimed_span`, `in_unclaimed_hunk`, `outside_hunks`). A blocking sweep row, or a sweep challenge to a verified row, makes the **delivery outcome** ESCALATE; it never opens a cycle. The sweep is skipped only after a review-1 PASS with the document unchanged.

**Status transitions (only the script writes; merged s3 has the full T1 to T12 table).**

| From | To | Requested by | Refused when |
|---|---|---|---|
| none | `open` / `deferred` | `find` (review 1), `verify` new row (reviews 2, 3), `sweep` (always `deferred`) | anchor absent or repeated; a verify row outside the hunks becomes `scope=outside`, `deferred` |
| `open`, `reopened` | `fixed` | reviser `answer`, or the script's auto-claim at `begin` | row not blocking or not listed; claim wider than the row's paragraph (`E-CLAIM-WIDE`); a `fixed` answer with no edit in the span (`E-FIXED-NO-EDIT`) |
| `fixed` | `verified` | verifier `resolved` | evidence quote not in the new snapshot; anchor unmappable |
| `fixed` | `open` or `reopened` | verifier `open` (`reopened` if the row was ever verified, from history) | no reason or quote |
| `verified` | `fixed` | script at `begin`, when this round's hunk touches the row's span | never; then `regressed` is allowed |
| `verified` (untouched) | `reopened` | nobody | `E-NOT-CHANGED`: accepted text cannot be re-attacked |
| `deferred` | anything | nobody | `E-ILLEGAL` |
| any frozen field | changed | nobody | `E-FROZEN` (frozen at creation: id, grade, rule, wrong_outcome, blocking, anchor, origin, scope, caused_by, finding text) |
| any loop step after a terminal decision | | nobody | `E-TERMINAL` (only the single sweep and `status` run after it) |

A dispute is a flag on a claim, not a status; the verifier rules on it, and an unruled dispute at the cap counts as open. `ledger.json` carries `body_sha256`; a hand edit is refused `E-TAMPERED`. Mutations hold a nonblocking per-ledger lock and take `--op` and `--expect-seq`; an identical retry returns the committed result instead of using a slot.

**Termination, computed by the script after each review k (k = 1, 2, 3):**

```text
U = rows with blocking and scope == in and status in {open, fixed, reopened}   # child rows included
X = cannot-verify answers this round + unmappable anchors + failed revert preimages
I = ledger hash valid and snapshots intact and every plan row answered
loop_decision = ESCALATE  if not I or X > 0
                PASS      if U == 0
                CONTINUE  if k < 3
                ESCALATE  otherwise                      # k == 3 with U > 0
after the sweep: S = blocking sweep rows + blocking sweep challenges to verified rows
delivery_outcome = ESCALATE if loop_decision == ESCALATE or S > 0, else PASS
```

The review counter advances only on a committed `begin`; a fourth review or a third fix cycle is refused (`E-CAP`, constant `CAP_REVIEWS = 3` tied by a test to the pinned text `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`, `tests/skills/test_review_severity_rule.py:215`). The sweep is outside the 3-review cap: it cannot start a fix cycle and its report header is `sweep`, never `review: 4 of 3`. There is no second computed stop (no "count did not shrink" halt): blocking counts fell from review 1 to review 2 in all six S1 runs (`AB-REPORT.md:13`, `ARMB-REPORT.md:13`), so it would never have fired. The reviewer may write its own verdict (the S1 briefs ask for one); the script's tail is always the report's last lines: CONTINUE ends `verdict: FAIL`, a terminal review before the sweep ends `loop: PASS (sweep pending)` or `loop: ESCALATE (sweep pending)`, and the sweep report ends `verdict: PASS` or `verdict: FAIL` from the delivery outcome. `begin` refuses an edited tail (`E-REPORT-EDITED`). The read-only `verdict` subcommand exits 0 PASS, 10 CONTINUE, 11 ESCALATE and, settled here (the merge left it open), **12 PENDING** while the loop is terminal but the sweep has not run, so no caller can read an early loop PASS as a delivery PASS. Every other committed operation exits 0 whatever the decision.

**How this differs from PR 427's `--re-review`.** 427's reviews 2 and 3 still re-review the changed document: the reviewer reads the whole revised spec and the prior report, rebuilds the resolution table in prose, may raise any finding on changed lines, re-grades what it writes, writes its own verdict, and depends on the coordinator keeping the baseline copy and the count (`spec-panel.md:258-264`). The ledger moves five duties to the script: the row list and statuses (a plan file instead of a re-read report), the origin tag (computed from hunks), the baseline and counter (script snapshots), the scope (rows outside hunks cannot block), and the verdict (computed, last line). Grade is frozen per row, so it cannot drift upward between rounds. What does NOT change much is the reading surface: 427 with flags already confined review 3 to hunks (25 of 317 lines in flg-r2), and every review-3 blocker in two traced runs had an anchor in changed lines (merged s5), so the ledger would have found the same blockers. Its gain, if any, comes from the minor-row rule, the frozen grade and the computed stop, not from reading less.

**Measured causes: removed and left.**

| Cause (measured) | Effect | Kind |
|---|---|---|
| Fresh whole-document re-review after each fix | removed for reviews 2 and 3; replaced by one sweep that cannot loop | MECHANICAL |
| Fix-induced defects on changed lines (89% / 100%) | LEFT: fixes still create defects; the ledger finds them as child rows with `caused_by` | not addressed |
| Severity drift between rounds | removed for existing rows (`E-FROZEN`); left for new rows, graded once by a model | MECHANICAL / PROSE |
| Reviser applies minor findings | removed outside blocking paragraphs (unclaimed, reverted with the flag); LEFT inside a blocking row's paragraph (auto-claim admits it) | MECHANICAL, with a leak |
| Reviser adds mechanisms inside a blocking fix | LEFT; bytes per claim are only measured | not addressed |
| No mechanical stop; verdict is reviewer judgement | removed: counter, cap, terminal phase, computed last line | MECHANICAL |

**Stateful single reviewer vs file ledger: file ledger, recommended.** A reviewer session kept alive across rounds is cheapest (no script calls) but has no mechanical rule at all, lets the finder judge its own findings, does not survive a crash or a new worker, and does not fit S1 (a fresh worker per review) or rf-qa and `/sc:implement`, which use fresh subagents by design. The file ledger carries the small state that matters (id, anchor, grade, status, claim) exactly, survives any session, and lets a script enforce it. A stateful arm stays a cheap later experiment if the ledger fails.

## 3. Exact changes

All additive. Nothing existing is edited: `src/superclaude/commands/spec-panel.md`, its `plugins/` copy, `HOW-WE-WORK.md`, the severity pins and routing stay as they are until S1 proves the variant.

| File | Change |
|---|---|
| `src/superclaude/commands/spec-panel-ledger.md` (new) | Copy of `spec-panel.md` with three blocks changed (below). |
| `src/superclaude/skills/sc-review-ledger/SKILL.md` (new) | Delegate-only skill (no slash command, like `sc-bare-review`): ledger layout, input schemas, `PROFILES`, transition table, CLI, how to add a profile. |
| `src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py` (new) | The kernel. Stdlib only (`argparse`, `json`, `hashlib`, `difflib`, `fcntl`, `os`, `pathlib`, `re`). |
| `tests/skills/test_review_ledger_script.py` (new) | Behaviour tests, loading the script by path as `tests/skills/test_workflow_archive.py` does. |
| `tests/skills/fixtures/review-ledger/` (new) | Tiny documents and input JSON for the edge cases. |
| `tests/skills/test_spec_panel_ledger_command.py` (new) | Text pins and the drift test. |
| `docs/designs/spec-panel-ledger.md` (new, after approval) | This design. |

**Why a skill folder for the script.** The command installer copies only top-level `*.md` files (`src/superclaude/cli/install_commands.py`), while a skill folder is copied whole (`src/superclaude/cli/install_skill.py:52`, `shutil.copytree`), so the script reaches `~/.claude/skills/sc-review-ledger/scripts/`. The skill must not be named `sc-spec-panel-ledger`: the skill installer treats an `sc-<x>` skill with a `commands/<x>.md` file as served by that command and skips it unless the command activates it (`src/superclaude/cli/install_skills.py`, debate finding U-009, not re-read here).

**Command file `spec-panel-ledger.md`: the three changed blocks.**
1. Frontmatter `name: spec-panel-ledger`, description "... with a script-kept finding ledger (find once, then verify)".
2. Usage line: drop `[--re-review <prior-findings-file> --baseline <saved-copy>]`, add `[--ledger <dir>] [--revert-unclaimed] [--sweep]`; drop the `--unattended` usage line. `## Unattended mode` is omitted, because `tests/skills/test_worker_contract.py:831-839` requires the set of commands with that heading to equal `UNATTENDED_COMMANDS`; instead the new section's first line refuses a standalone `--unattended` token ("spec-panel-ledger has no unattended mode") so it is never silently ignored.
3. `## Review Loop` replaced by `## Review Ledger Loop`, one line per bullet so the repo's line matchers see each whole:
   1. **Setup**: critique only; invoke `Skill sc-review-ledger` (`~/.claude/skills/` first, then the project `.claude/skills/`); the ledger is `--ledger` or `<doc dir>/<doc stem>.review-ledger/`; run `init` if absent, else `begin`; a refusal stops the run and never falls back to a first review.
   2. **Find**: the full panel; each finding becomes a row with grade, rule, wrong outcome and an exact anchor quote; the script decides what blocks.
   3. **Verify**: answer every row in `plan-r<k>.md`; run one new-defect check on this round's hunks; anything else is filed `scope=outside`.
   4. **Sweep**: run only on the copy that `sweep --prepare` prints; never open the ledger folder.
   5. **Report**: write what the brief asks; never edit the lines `close` appends.
   6. **Cap**: `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`, then `HALT and escalate to the user with the open blocking findings` (both verbatim); `review: N of 3` comes from the script.
   7. **Reviser contract**: revise only text a listed blocking row names; minor rows are not answerable; unclaimed edits are reported and, with `--revert-unclaimed`, restored.
   8. **Precedence**: a brief may narrow this scope, not widen it, and cannot change a grade or a script verdict.

**Script CLI outline (`review_ledger.py`).** Output is one JSON object on stdout (`{ok, seq, phase, review, fix_cycles, counts, loop_decision, delivery_outcome, next_action}` or `{error, detail, next_action}`). Exit codes: 0 committed (whatever the decision); 1 usage; 2 input refused (row level); 3 state refused; 4 lock or sequence conflict; `verdict` alone uses 0/10/11/12 (PASS/CONTINUE/ESCALATE/PENDING).

| Subcommand | Run by | Does | Main refusals |
|---|---|---|---|
| `init --doc D --profile spec-panel [--archive-existing]` | review 1 | creates ledger, `r1.md` | `E-EXISTS` (rerun needs `--archive-existing`, which renames the old folder) |
| `find --input F` | review 1 | adds rows, computes `blocking`, defers the rest; accepts `[]` | `E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`, `E-SCHEMA`, `E-PHASE` |
| `answer --input F` | reviser (optional) | claims hunks per blocking row; optional `gap` entries | `E-ILLEGAL`, `E-CLAIM-WIDE`, `E-FIXED-NO-EDIT`, `E-TERMINAL` |
| `begin --doc D [--revert-unclaimed]` | reviews 2, 3 | snapshot, diff, auto-claim, optional revert, writes `plan-r<k>.md` | `E-TAMPERED`, `E-REPORT-EDITED`, `E-CAP`, `E-TERMINAL` |
| `verify --input F` | reviews 2, 3 | applies answers, adds `scope=in` and `scope=outside` rows | `E-INCOMPLETE`, `E-ANCHOR`, `E-FROZEN`, `E-NOT-CHANGED` |
| `close --report R` | each review | computes `loop_decision`, appends the tail and its digest | `E-PHASE` |
| `sweep --prepare` / `sweep --input F --report R` | session holding the ledger | copy for the sweep; ingests sweep rows, sets `delivery_outcome`, re-checks every prior tail | `E-SWEEP-DONE`, `E-PHASE` |
| `status`, `verdict` | anyone | read-only counts, metrics, post-terminal edits by hash | none |
| `revert-unclaimed [--hunk k]`, `defer --id --quote` | reviser; coordinator | restore own unclaimed hunk (preimage-checked); record a user's words (no status change) | `E-PHASE` |

Writes: temp file, fsync, `os.replace`, under `fcntl.flock` on `.lock`; idempotency by request digest within phase and round. No event log, no git calls (snapshots are copies because a `.dev/` document may be untracked, `docs/designs/spec-panel-review-loop.md:50`).

**Tests.**
- Script: every transition and refusal code; the blocking formula for CRITICAL, FR-8 with MINOR, MAJOR with and without wrong outcome, MINOR; auto-claim with zero, one and two rows; paragraph admission on a pure rewrap; unclaimed hunks kept without the flag and restored with it; failed preimage gives `cannot-verify`; `scope=outside`; `E-TERMINAL`; empty `find`; zero-hunk round; half-open range and deletion edges; anchor relocation ending missing or ambiguous; identical retry under a new op id; stale sequence; two writers; `E-TAMPERED`; `E-REPORT-EDITED`; `verdict` exit 12 before the sweep; `CAP_REVIEWS == 3` tied to `CANONICAL_CAP_TEXT`.
- Command: `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` present (imported from `tests/skills/test_review_severity_rule.py`); eight one-line bullets in order; subcommand and flag names present; the `--unattended` refusal line present; no `## Unattended mode`; no `src/superclaude` path; dual lookup order; none of the banned severity phrases and no cap number above 2 (that test scans all of `src/`).
- Drift test: the variant equals `spec-panel.md` outside the frontmatter name and description, the Usage block, the loop section and `## Unattended mode`, so the copied panel cannot silently diverge.

**Later adopters (not in this change; each a separate change gated on S1).** The kernel knows no spec-panel words: an adopter adds one `PROFILES` row (grade vocabulary, blocking predicate, cap, ordered stop guards) and a short adapter section.
- **rf-qa agents** (`src/superclaude/agents/rf-qa.md:379-416`): first adopter after spec-panel. Its Fix Cycle steps 1 to 5 already say "verify the blocking issues, do not recheck minor findings"; the ledger replaces "the previous QA report" with `plan-r<k>.md`, step 5's verdict with `verdict`, and its prose monotonicity halt `|F_{n+1}| < |F_n|` (`:401`) with a profile guard run in rf-qa's own order (regression first, `:407`). Differences: CRITICAL/IMPORTANT/MINOR grades; partitioned parallel instances (the lock serializes them, or one ledger per partition); rf-qa may fix in place, so finder and reviser can be one agent.
- **`/sc:reflect`**: rows created only from findings that pass its evidence-validator gate; a `reflect` profile mapping its deviation classes to blocking (which classes block is UNVERIFIED); multi-file ledgers (v1 is one document); its caller owns the loop. A ledger PASS never authorizes promotion.
- **`/sc:implement` final review**: not adopted. Implement already computes the verdict in the orchestrator (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:334`), but every re-review may raise a blocker anywhere in task-owned text (`:186`) and each archive attempt needs a fresh full FINAL; a per-task repair ledger between FINALs is the most it could take, and only after an implement incident shows the same fix-induced pattern.

## 4. Variant command name and install note

- **Name**: `spec-panel-ledger`, invoked as `/sc:spec-panel-ledger`; source `src/superclaude/commands/spec-panel-ledger.md`; installed copy `~/.claude/commands/sc/spec-panel-ledger.md`, next to the unchanged `~/.claude/commands/sc/spec-panel.md`. Its skill installs to `~/.claude/skills/sc-review-ledger/` (with `scripts/review_ledger.py`).
- **Why a new name**: a worker loads `/sc:spec-panel` from the user-level file, and a personal command beats a project command of the same name (`exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md:46`), so a worktree-only change is inert and parallel arms need different names (`AB-REPORT.md:47`). The original file is never edited by the experiment.
- **Experiment install (owner, by hand, not a repo change)**: copy `spec-panel-ledger.md` into `~/.claude/commands/sc/` and the `sc-review-ledger/` folder into `~/.claude/skills/`; record their sha256 in the install watcher. Nothing else in `~/.claude/` changes; no `superclaude install`.
- **The one-line substitution** (in the three S1 review briefs only; reviser briefs stay verbatim):

```text
/sc:spec-panel        ->  /sc:spec-panel-ledger --ledger .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger --revert-unclaimed
```

  All other flags on the line (`@<spec> --mode critique --focus requirements,architecture`) stay. No `--re-review`, no `--baseline`. `--revert-unclaimed` is the consent that lets `begin` restore edits no blocking row claims; it is part of the treatment and is recorded as such.
- **Sweep route** (needs one check before replicate 1): if a throwaway dispatched worker with the T09 wrapper can spawn an Agent-tool subagent and keep its 5-minute heartbeat, the sweep is a subagent of the terminal review session (still 5 dispatches). Otherwise it is a sixth dispatch, `/sc:spec-panel-ledger @<spec> --mode critique --focus requirements,architecture --ledger <same path> --sweep`, declared as a deviation. Whether an S1 worker can spawn a subagent is UNVERIFIED today (no S1 brief or report shows it either way, `nested/adversarial-1/adversarial/round2-rebuttal-B.md`, New evidence 1).

## 5. Measurement plan and predicted numbers

**Arm "led"** (two fresh worktrees, for example `exp346-ab-led-r1`, `-r2`): identical to Arm B as fixed in `DECISIONS.md` D11 (S1, base commit 2cb683f5, overlay, verbatim briefs T05 to T09, model claude-opus-5-5, `WORKER-CONTRACT.md` moved aside, install watcher), except the three recorded differences: the one-line substitution of section 4, the `--revert-unclaimed` flag inside it, and the sweep route. Comparators, reused: control ctl-r1/ctl-r2 and Arm B flg-r1/flg-r2. Reruns of an aborted replicate use `init --archive-existing`, never a manual delete.

**Before replicate 1 (pre-registered).**
1. Smoke check for the sweep route (section 4).
2. Baseline sweeps: run the same sweep (a whole-document `/sc:spec-panel` critique on a copy) on the FINAL spec of all six existing replicates. Their mean CRITICAL+MAJOR count is what a whole-document look still finds after a 427 loop. If it is 3 or more, the combined bar cannot be met by the ledger alone, and the loop number and the sweep number are reported separately as the primary result.
3. Hunk parity: run the script's diff on the three S1 history pairs (`exp346-ab-flg-r2/.dev/orca-command-refactor/specs/history/`) and fix the paragraph unit and the `HUNKS_LARGE` threshold from them.

**Validity checks per replicate.** V1-ledger: `ledger.json` shows rounds 1 to 3 (or an earlier terminal decision), the snapshots, and a sweep record; a replicate whose sessions never ran the script is "ledger not honoured" and is not treatment (the rule D11 applies to Arm B as "flags not honoured"). A sweep report that cites a ledger row id fails V1-ledger (the sweep read the ledger). A blinded audit of `wrong_outcome` texts: more than 30% judged filler marks the replicate "grading not honoured". Also recorded: command, skill and script sha256; auto-claim count per cycle; every reviewer-vs-script verdict disagreement; one `status` after the last dispatch.

**Metrics.** D5 M1 to M5 (`DECISIONS.md:23`), read from the ledger, not from report prose (M3, the fix-induced share, is computed from hunk attribution, then the causation is ruled by the analyst). Plus: unclaimed and reverted bytes per cycle, `minor_touched` (edits inside a deferred row's span, split by "answered" and "auto-claimed"), `scope=outside` count, `X` count, script calls, sessions and wall time per step.

**How "review 3 critical+major" is counted in a ledger loop.** A ledger loop's review 3 looks only at rows and hunks, so counting its open rows alone would let the ledger win by not looking. The headline is therefore the union, each defect counted once:
- `U3`: CRITICAL or MAJOR rows (by grade, as Arm B's proxy counted by grade, `ARMB-REPORT.md:37`) not `verified` after review 3, child rows included;
- `W`: sweep CRITICAL or MAJOR rows plus sweep challenges to verified rows;
- `O`: `scope=outside` CRITICAL or MAJOR rows (verify-time allegations outside the hunks).
Duplicates between sets are ruled by a blinded analyst; the raw and auto-matched counts are published as bounds. MAJOR rows deferred at review 1 (no wrong outcome) can never be verified, so they form a permanent floor: that **deferred floor** is published separately, the bar is applied to the headline without it, and the control's comparable number (control MAJOR findings without a concrete wrong outcome) is computed by the same rubric. A run that ends early is counted at its terminal review. `U3` alone is the analogue of Arm B's hunk-scoped review 3 and is reported beside the headline.

**Bars (fixed now, same shape as D10/D11).**
- (a) **Ledger plus 427 vs control**: headline mean at most 3 (half the control's 6.0), growth after two fix cycles at most 44.4%, effect larger than the larger within-arm spread, and every ledger replicate better than both control replicates on both.
- (b) **The ledger's own effect vs Arm B** (the ledger carries 427's grading, so (a) credits both): headline mean below Arm B's 3.5 and growth at most 30.0%.
- Pre-registered per replicate: B1 (blocking rows after review 1) and r1, r2 (new blocking rows per blocking fix in cycles 1 and 2). The ledger does not claim to change r. Expected review-3 blockers are about B1 x r1 x r2 (with B1 = 13: 2.7 at r = 0.46 twice, 1.0 at flg-r2's measured 0.46 then 0.17, merged s10); a measured product above 3 means no loop change of this kind can meet the bar on that run.

**Predicted numbers (n = 2, a screen, planning estimates only).**

| Metric | Control mean | Arm B mean | Ledger predicted | Bar |
|---|---|---|---|---|
| Headline review-3 critical+major (`U3` + `W` + `O`, deduplicated, without deferred floor) | 6.0 | 3.5 (whole-document sweep not counted) | **5.5** (range 3 to 9) | at most 3 |
| `U3` alone (loop rows open after review 3) | n/a | 3.5 | **3** (range 1 to 6) | none |
| `W` sweep critical+major | n/a | n/a | 2.5 (range 1 to 5) | none |
| Deferred floor | n/a | n/a | 1 to 3 | reported only |
| Growth after 2 fix cycles | 63.5% | 30.0% | **26%** (range 18% to 33%) | at most 44.4% |
| Clean delivery PASS within 3 reviews | 0 of 2 | 0 of 2 | 0 of 2 (a loop PASS in 1 of 2 is plausible; the sweep then escalates) | none |

Basis. `U3` follows Arm B, because the ledger reads the same hunks 427 with flags read, and every review-3 blocker in the two traced runs had an anchor in changed lines (merged s5). The base proposal predicted that the ledger breaks the flg-r2 chain "minor F22 applied, then blocking N5, then blocking N12" because `answer` refuses minor rows. I checked that claim and it does not hold: F22 was graded "MAJOR (FR-8 GAP minimum), non-blocking" (`exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel.md:63`), and the profile makes any FR-8 row blocking, so F22 would be a blocker and be fixed; and F22's edit to the AC-0.4 row shares that one-line table row with the edit of blocking F10 (`disposition.md:25`, `:37`), so paragraph auto-claim would admit it anyway. So no traced chain is removed, and `U3` is predicted near Arm B, not near 0. `W` is the pre-existing defects review 1 missed: 3 of the 8 ctl-r1 review-3 blockers predated the revision (merged s10). Growth: the ledger stops minor edits outside blocking paragraphs (in flg-r2, 15% of cycle-1 and 38% of cycle-2 changed-line bytes carried only a minor finding id, merged s9, one replicate, an upper bound on the saving), but the profile grades every FR-8 or FR-9 row blocking, which the flg-r2 reviewer did not do, so B1 and fix volume can rise; the two roughly cancel against Arm B's 30%.

**Honest forecast.** The ledger is predicted to **meet the growth bar (a)** and **miss the review-3 bar (a)**, and to be only marginally better than Arm B on (b). It removes the prose-only stop and makes the count honest, but the dominant measured cause (fixes create new defects at rate r) is untouched.

**What result means the idea failed.**
1. Headline mean 4 or more, or not below Arm B's 3.5: the ledger adds nothing over 427 with flags on convergence.
2. The ledger sweep finds on average 2 or more CRITICAL+MAJOR rows more than the baseline sweeps: verify-only hid defects instead of preventing them.
3. Growth above 30.0% after reverted bytes are shown: the minor-row rule did not cut text.
4. `minor_touched` above 0 through answered claims with `--revert-unclaimed` on: the scope rule leaked mechanically.
5. A loop stalled by a script refusal with no recovery path in either replicate.
A replicate that fails V1-ledger or the wrong-outcome audit is not treatment (it is rerun), not a failure. Results inside both arms' spreads are "not significant" (D6).

**What would show the idea worked even if the bar is missed.** `U3` below 3.5 in both replicates with growth at most 30%, the sweep no larger than the baseline sweeps, zero `minor_touched` through answers, and zero verdict computed by a model. That would justify keeping the ledger as the carrier for a second theme that lowers r (for example a bounded-fix reviser), whose effect the ledger would then measure exactly.

## 6. Risks, costs and what would falsify it

**Cost per loop (estimates; measure as M5).**
- Sessions: 5 if the sweep runs as a subagent of the terminal review session; 6 if it needs its own dispatch. The experiment also adds one smoke-check worker and up to six baseline-sweep sessions, once.
- Script calls: about 3 in review 1, 0 to 2 per revise, 4 per verify, 2 for the sweep: 13 to 17 per loop, about 15 to 20 with retries and the coordinator's `status` checks. Each is a `uv run` start of well under a second (not measured).
- Wall time: the sweep is one more whole-document critique, about +10 to +15 minutes per loop (flg-r2 file times show 9 to 16 minutes per review step); shorter verify reports may give some back (not measured).
- Maintenance: a 480-line copied command kept in step by a drift test, plus a script with its own test suite and fixtures.

**Ways it could make the loop worse.**
1. **Apparent convergence by not looking.** Verify-only reviews cannot add blocking rows outside the hunks, so the loop count falls by construction while the document may be no better. Mitigation: `scope=outside` rows and the sweep enter the headline; baseline sweeps measure the hidden share. Residual: a "PASS" loop next to a sweep that escalates.
2. **Frozen first-pass grades.** A wrong review-1 grade is locked for the whole loop: a real blocker filed MINOR is never fixed in-loop; an inflated grade forces a fix cycle. The S1 briefs still say "any finding of any severity is FAIL", which may push review-1 grades up now that review 1 is the only grading moment. Measured by the wrong-outcome audit, not prevented.
3. **The profile is stricter than practice.** It makes every FR-8 or FR-9 row blocking, as 427's text says; the flg-r2 reviewer graded an FR-8 GAP finding non-blocking (F22). More blocking rows mean more fixes and more fix-induced defects.
4. **Auto-claim leak.** A minor edit written in the same paragraph as a blocking row's anchor is admitted as part of that fix (the F22/F10 case). A paragraph that is a long table row is a wide unit.
5. **Reverting text.** With `--revert-unclaimed`, an edit the reviser needed but did not tie to a blocking row is undone; the gap then surfaces only in the sweep, with no cycle left.
6. **Stalls on refusals.** Absent or repeated anchors and over-wide claims refuse a call; an unattended session may not recover. Unclaimed hunks and failed reverts never stall (they report or become `cannot-verify`), but one `cannot-verify` ends the loop as ESCALATE.
7. **Two verdicts in one report.** The reviewer's own verdict (the briefs ask for one) sits above the script's last line; a reader who stops early can misread it. Every disagreement is recorded.
8. **Interaction defects.** A defect on unchanged text caused by a change elsewhere (for example flg-r2 N15) can block only if the verifier quotes the changed line it depends on; otherwise it is a non-blocking `scope=outside` row.

**What is mechanical and what is still prose.**

| Rule | Kind | Residual risk |
|---|---|---|
| Ledger written only by the script; hash refuses hand edits | MECHANICAL | detects, does not prevent, a determined editor |
| Blocking computed from grade, rule and wrong outcome; non-blocking rows deferred and unanswerable | MECHANICAL | the grade and the wrong-outcome text are still model judgement |
| Grade and anchor frozen | MECHANICAL | locks first-pass errors |
| Every plan row answered; evidence quote present in the snapshot | MECHANICAL | proves the text was opened, not that it was judged well ("yes, yes" answers) |
| New blocking rows only inside this round's hunks | MECHANICAL | interaction defects become non-blocking |
| Unclaimed edits reported; reverted with the flag | MECHANICAL | edits inside a blocking paragraph are admitted |
| Counter, cap, terminal phase, computed last line | MECHANICAL | a coordinator that ignores refusals and dispatches anyway |
| Verifier does not run a whole-document panel | PROSE | it may anyway; its out-of-hunk rows are then counted, not hidden |
| Sweep context does not open the ledger | PROSE, partly checked | detected only when the sweep report cites a row id |
| Reviewer, reviser and sweep are different sessions | PROSE | the script knows the subcommand, not the session |
| Reviser adds no mechanism inside a blocking fix | PROSE | the main remaining cause; bytes per claim are only measured |

**What would falsify it.** The five failure results in section 5. The cleanest single test: if `U3` (the loop's own count) is not below Arm B's 3.5 in both replicates, the ledger adds nothing to convergence beyond what 427 with flags already does, and only its mechanical stop and honest counting remain as reasons to keep it.

## 7. Open questions

1. **Sweep route.** Can a dispatched Orca worker spawn an Agent-tool subagent and keep its heartbeat? Decides 5 or 6 sessions and whether S1's dispatch list changes (UNVERIFIED; one smoke check settles it).
2. **Consent for reverts.** Is a flag on the invocation line, written by a coordinator's brief, enough to count as "explicit user consent" under `spec-panel.md:475`, or must a person approve each revert? The default without the flag only reports.
3. **Deferred floor in the bar.** Should the review-3 bar be applied with or without the deferred MAJOR floor? This design applies it without, and publishes the floor beside it; this must be fixed before replicate 1.
4. **FR-8/FR-9 strictness.** Keep 427's rule that every FR-8/FR-9 row blocks (as written) or follow what reviewers did in practice (some FR-8 GAP rows graded non-blocking)? The choice moves B1 and growth.
5. **Paragraph unit.** Is "enclosing paragraph" the right auto-claim and admission unit for a spec made of long one-line table rows? Calibrate on the S1 history pairs.
6. **Sweep findings with cycles left.** When the loop passes early and the sweep finds blockers, should a second ledger start automatically or only on the user's word? Recommended: only on the user's word.
7. **Blinded rulings.** Can the duplicate ruling, the deferred-floor reading of the control reports and the wrong-outcome audit be staffed before replicate 1? Without them only raw bounds exist.
8. **Order of adoption.** rf-qa first after spec-panel (its Fix Cycle maps one to one), then `/sc:reflect` (needs multi-file ledgers), `/sc:implement` last or never. Confirm before any adopter work.
9. **Pairing with another theme.** Because r (fix-induced defects per fix) is the dominant cause and the ledger leaves it, should the S1 arm run the ledger together with a bounded-fix reviser theme, with the ledger as the measuring frame? That changes what the arm tests and must be decided before it runs.

Not checked in this spec: the skill installer's naming rule (cited from the debate, `src/superclaude/cli/install_skills.py` not re-read); whether every worker host has `uv`; how `/sc:reflect` grades blocking; any timing or token number marked as an estimate.
