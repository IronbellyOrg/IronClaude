# Spec: finding ledger with separate FIND and VERIFY phases (issue 346, theme LEDGER, variant 2, analyzer)

Design only. Nothing here is implemented. Variant command: `/sc:spec-panel-ledger`, additive next to the unchanged `/sc:spec-panel`.

Citation aliases (all read in this session; `W` = `/home/coder/workspaces/worktrees/IronClaude`): `SP` = `W/bs346-ledger/src/superclaude/commands/spec-panel.md`; `DES` = `W/bs346-ledger/docs/designs/spec-panel-review-loop.md`; `QA` = `W/bs346-ledger/src/superclaude/skills/sc-implement-protocol/refs/qa.md`; `RFQA` = `W/bs346-ledger/src/superclaude/agents/rf-qa.md`; `AB`, `ARMB`, `DEC` = `AB-REPORT.md`, `ARMB-REPORT.md`, `DECISIONS.md` under `W/exp346-p1-logs/.dev/experiments/346-validation/` (`phase4/` for the first two); `F2R2`, `F2R3`, `F2D1`, `F2D2` = `spec-panel-round2.md`, `spec-panel-round3.md`, `disposition.md`, `disposition-round2.md` under `W/exp346-ab-flg-r2/.dev/orca-command-refactor/review/`; `C1R2`, `C1R3` = the same round reports under `W/exp346-ab-ctl-r1/.dev/orca-command-refactor/review/`; `HIST` = `W/exp346-ab-flg-r2/.dev/orca-command-refactor/specs/history/`. Anything I did not open is marked UNVERIFIED.

## 1. Problem and evidence

- 427 halves growth (63.5% to 29.7%, `AB:19`) but no run of any arm passed; 89% (R2) and 100% (R3) of new findings sit on lines the previous fix changed (`AB:30`); the R3 proxy is 5.5 and 3.5 against a bar of 3 (`ARMB:20`, `ARMB:23`).
- Root cause by trace (flg-r2): non-blocking F22 was applied (`F2D1:37`) although 427 says minor findings never trigger a revision (`SP:259`), because the coordinator brief said "apply confirmed findings" (`F2D1:10`); the F22 fix added the WC-1 proof to AC-0.4 (lines naming AC-0.4 and WC-1: 0 in `HIST/spec-v1-draft.md`, 2 in `HIST/spec-v2-after-round1.md`), which became blocking N5 (`F2R2:119`), whose fix became blocking N12 at review 3 (`F2R3:84`). A prose rule lost to a brief.
- The verdict, the review count, the saved copy and the scope rule are prose ("every rule here is prose read by a model", `DES:143`; "nothing enforces the count", `DES:162`); the round-3 report still grades FAIL on the brief's "any finding of any severity" (`F2R3:15`).
- Claim of this spec: a script, not a model, can hold row states, the scope of each later review, the review counter and the verdict. It cannot stop a reviser from creating fix-induced defects (section 10).

## 2. Mechanism

Names used below. `LEDGER` = `uv run --no-project python "<skill base>/scripts/review_ledger.py"` (same call shape as the archive helper, `W/bs346-ledger/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:54`); `<skill base>` is `~/.claude/skills/sc-review-ledger` first, else the project `.claude/skills/sc-review-ledger`. S1 paths: `DOC` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `L` = `.dev/orca-command-refactor/review/ledger.jsonl`; snapshots `L.snap/r1.md`, `r2.md`, `r3.md`, `final.md` are written by the script, never by a model. Actors: coordinator (Orca worker, human or script), reviewer (a fresh session per step, running `/sc:spec-panel-ledger`), reviser (a separate session, as in S1 today). Scratch files `findings.jsonl`, `marks.jsonl`, `new.jsonl`, `answers.jsonl` sit next to each report and are inputs to `--batch` calls (one call per file keeps the call count low).

| Step | Who | Reads | Writes | Script calls (in order) |
|---|---|---|---|---|
| Review 1 (FIND, the only full find pass) | reviewer, fresh | `DOC`, the command | report `spec-panel.md`, `L`, `L.snap/r1.md` | `init --doc DOC --ledger L --scale CRITICAL,MAJOR,MINOR --needs-outcome MAJOR`; `add --ledger L --batch findings.jsonl`; `close --ledger L --report spec-panel.md` |
| Revise 1 | reviser, separate session | report (its Reviser brief), `L`, `DOC` | `DOC`, `L` (answers), disposition file as the brief asks | `show --ledger L --rows revisable`; `answer --ledger L --batch answers.jsonl`; `revise-check --ledger L` (repeat until exit 0) |
| Review 2 (VERIFY) | reviewer, fresh | `L`, hunks printed by the script, `DOC` | report `spec-panel-round2.md`, `L`, `L.snap/r2.md` | `open --ledger L`; `mark --ledger L --batch marks.jsonl`; `add --ledger L --batch new.jsonl`; `close --ledger L --report spec-panel-round2.md` |
| Revise 2 | reviser | as Revise 1 | as Revise 1 | as Revise 1 |
| Review 3 (VERIFY, last review) | reviewer, fresh | as Review 2 | report `spec-panel-round3.md`, `L`, `L.snap/r3.md` | as Review 2; `close` computes PASS or ESCALATE, never CONTINUE |
| Final sweep (not a review, no reviser) | reviewer, fresh, told not to read `L` | `DOC`, the command | report `spec-panel-sweep.md`, `L` (late rows), `L.snap/final.md` | `open --ledger L --sweep`; `add --ledger L --batch findings.jsonl`; `close --ledger L --report spec-panel-sweep.md --sweep` |

What each reviewer step does, in order:

1. **Review 1** is today's panel unchanged (experts, Guard Condition Boundary Table, Whittaker, `SP:305-339`), except that its findings leave the chat as rows. `add` refuses a row whose `anchor` quote is not byte-present once in `DOC` (or needs `--at`), and refuses `sev=blocking` with grade MAJOR unless a non-empty `wrong_outcome` is given (this is the 427 "concrete wrong outcome" test, `SP:259`, turned into a required field). Grade MINOR is stored `sev=minor`, status `deferred` by the script, so minor rows can never be answered or revised.
2. **Revise** answers rows, not the report. `answer` accepts only blocking rows that are `open` or `reopened`; `edited` must quote the new text, which must lie in a changed hunk against `r1.md`. `revise-check` lists every changed hunk no answer claims (`UNCLAIMED`, exit 7) with its bytes; `revert-unclaimed` restores the `r<n>.md` text for those hunks. This replaces "the reviser reports the byte size before and after" (`SP:263`) by numbers the script prints, and it is the mechanical form of "revise only text a blocking finding names".
3. **Verify** (review 2 and 3). `open` computes the changed hunks of `DOC` against `r<n-1>.md` (whitespace-insensitive, the same intent as `git diff --no-index -w -U0` that the real round-3 reviewer ran, `F2R3:25`; Python `difflib` instead of a git call so no git state is needed) and prints, per `fixed` row, the claimed text plus its hunk with 3 lines of context. The reviewer answers exactly two questions per `fixed` row, as fields the script requires: `resolved` (is the finding gone) and `touched_ok` (is the sentence the change touched itself correct). Then it runs the single bounded new-defect check (below). It does NOT re-run the whole panel.
4. **New-defect check (one, bounded)**: panel critique restricted to hunk text, including FR-8/FR-9/FR-10 on guards inside hunks (same limit as `SP:262`). A new row is accepted only if its `anchor` lies inside a hunk, or it carries `depends_on` quoting a changed line (the 427 exception for an unchanged line that depends on a changed one, `SP:262`). The script sets `origin=changed|depends` itself; there is no `unchanged` row in a verify pass, so 427's "origin=unchanged is a minor note" bookkeeping disappears.
5. **Sweep**: one whole-document critique exactly like review 1, by a session that has not read `L`. `add` in the sweep phase stores rows as `late`. The script classifies each late row by where its anchor falls: `in_claimed_span` (a verify pass said "ok" over this text), `in_unclaimed_hunk`, `outside_hunks` (review 1 missed it). Nothing is revised afterwards.
6. **Counting**: the review counter is a field in `L`, incremented only by `open`. Review 3 is the last `open` that can start a verify pass; a later `open` without `--sweep` exits 11 (cap). `close` appends the computed lines to the report (section 4), so the report's last line is script output, not reviewer prose.

## 3. Ledger file

**Format**: JSON Lines, UTF-8, one header line then one line per row. Chosen over Markdown or YAML because the script parses it with stdlib `json` (no PyYAML dependency inside an installed skill), a row is one atomic line, and the human-readable table is generated by `render` into the report instead of being parsed back out of prose. The header carries `body_sha256`, the hash of every following line; every command recomputes it first, so a hand edit exits 3 `LEDGER_TAMPERED` and nothing is written. All writes are all-or-nothing (temp file, then `os.replace`).

Example after the review 2 `close` (illustrative rows built on the real shapes F10, F22 and N12; the ids and wording are invented for the example):

```json
{"ledger":1,"doc":".dev/orca-command-refactor/specs/orca-worker-contract-spec.md","scale":["CRITICAL","MAJOR","MINOR"],"needs_outcome":["MAJOR"],"phase":"revise","review":2,"cap":3,"body_sha256":"9f2c...e1"}
{"id":"L1","sev":"blocking","grade":"MAJOR","anchor":"WC-7 requires a Skill-tool call for the command's skill","wrong_outcome":"a worker calls the protocol skill and skips the command file that holds Unattended mode","found":1,"origin":"find","parent":null,"status":"verified","claim":{"round":1,"action":"edited","new_text":"`Skill sc:<name>` for the command itself","bytes_added":212},"hist":["r1:add:reviewer","r1:answer:reviser","r2:mark:reviewer"]}
{"id":"L2","sev":"minor","grade":"MINOR","anchor":"well inside its own timeout","wrong_outcome":"","found":1,"origin":"find","parent":null,"status":"deferred","claim":null,"hist":["r1:add:reviewer","r1:auto-deferred:script"]}
{"id":"L3","sev":"blocking","grade":"MAJOR","anchor":"WC-7 names `sc:<name>` (the command)","wrong_outcome":"step 5 passes a run that never loaded the command file","found":2,"origin":"changed","parent":"L1","status":"open","claim":null,"hist":["r2:add:reviewer"]}
```

**Location**: `<report dir>/ledger.jsonl`, passed to the command as `--ledger <path>`; in S1 `.dev/orca-command-refactor/review/ledger.jsonl`, snapshots in `ledger.jsonl.snap/`. Why this path: (a) a plain file in the worktree, because fresh sessions of different workers read the same worktree by default (placement guide quoted at `F2R3:66`, C-R3-10), where `/tmp` or a session's memory would not survive a reboot or a new worker; (b) outside `DOC`, so the reviser's edits and the baseline diff never touch it; (c) not under `.claude/`, which is gitignored sync-dev output (project `CLAUDE.md`); (d) snapshots are copies, not git refs, because `DOC` may be untracked (`DES:50`, `DES:174`); (e) next to the reports, so a coordinator that already collects the review folder collects the ledger. A command file cannot carry the file or the script; see section 6.

**Frozen after `add`** (the script rejects any later change, exit 5 `FROZEN_FIELD`): `id`, `sev`, `grade`, `anchor`, `wrong_outcome`, `found`, `origin`, `parent`. Severity is frozen per row, which stops a verifier from lifting a row from minor to blocking or from MAJOR to CRITICAL between rounds. Mutable only by script-run transitions: `status`, `claim`, `hist`. There is no severity edit at all; the only downward path is T10 below, by the user.

**Status transitions** (every write command needs `--as reviewer|reviser|coordinator`; the script checks the subcommand is in that role's set AND that the phase allows it):

| # | From | To | Who may | Phase | Script check (illegal: exit 5 `ILLEGAL <from>-><to> <id> phase <p>`, no write) |
|---|---|---|---|---|---|
| T1 | none | open | reviewer, `add` | find, verify (new-defect check), sweep | anchor byte-present; MAJOR+blocking needs `wrong_outcome`; in verify the anchor lies in a hunk or `depends_on` quotes a changed line |
| T2 | none | deferred | script, at `add` | any | derived from grade MINOR; nobody chooses it |
| T3 | open or reopened | fixed | reviser, `answer action=edited` | revise | row is blocking; `new_text` found in `DOC` and inside a changed hunk against `r<n>.md` |
| T4 | open or reopened | (stays; `claim.action=disputed`) | reviser, `answer action=disputed` | revise | non-empty `reason`; the verifier must rule on it |
| T5 | fixed | verified | reviewer, `mark resolved=yes touched_ok=yes evidence="<quote>"` | verify | row has a claim; both fields present; `evidence` is byte-present in `DOC` now |
| T6 | fixed | reopened | reviewer, `mark resolved=no` | verify | non-empty `note` |
| T7 | fixed | verified plus a child row | reviewer, `mark resolved=yes touched_ok=no` | verify | a row with `parent=<id>` must exist in the same batch or already; else exit 6 |
| T8 | disputed | verified or reopened | reviewer, `mark dispute=accepted` or `rejected` | verify | non-empty `note` |
| T9 | verified | fixed | script, at `open` | verify | a hunk of this revision overlaps the row's claim span (re-checked, so a later edit cannot silently break a verified row) |
| T10 | blocking, any open state | deferred | coordinator, `defer --accepted-by user --quote "<user words>"` | closed (after ESCALATE) | non-empty quote; that the user said it is PROSE |
| T11 | sweep row | open, immutable | reviewer, `add` in sweep | sweep | every mutating command except `defer` refuses a `late` row |

Forbidden and refused: any move into `open` from `fixed`, `verified` or `deferred`; `answer` on a `deferred` or `verified` row (so a minor row cannot be revised, whatever the brief says); `mark` on a row that is not `fixed` or disputed; any write in phase `closed` except T10; `open` when `review` is already 3 (exit 11, the cap). An unanswered blocking row is not a transition: it stays `open` and counts as unresolved.

## 4. Termination rule

Computed by `close` (and by the read-only `verdict` subcommand) from the ledger only. No model writes a verdict.

```text
n  = header.review                      # 1, 2 or 3; only `open` increments it
U  = count(rows: sev == blocking and status in {open, fixed, reopened})   # includes child rows
at close of review n (n = 1, 2, 3):
    if any row is `fixed` and unmarked:   refuse, exit 6 UNMARKED_ROWS    # a verify pass cannot skip rows
    if U == 0:    PASS      exit 0    phase -> closed
    elif n < 3:   CONTINUE  exit 10   phase -> revise
    else:         ESCALATE  exit 11   phase -> closed
at close of the sweep:
    Lt = count(rows: origin == late and sev == blocking)
    final = PASS if (U == 0 and Lt == 0) else ESCALATE
report footer written by the script: "ledger-verdict: <PASS|CONTINUE|ESCALATE> U=<U> Lt=<Lt> review: <n> of 3"
report last line written by the script: "verdict: PASS" if PASS, else "verdict: FAIL"
```

| n | U after the verify pass | Result | Next |
|---|---|---|---|
| 1 | 0 | PASS | sweep |
| 1 or 2 | > 0 | CONTINUE | revise, then verify |
| 3 | 0 | PASS | sweep |
| 3 | > 0 | ESCALATE | sweep, then the user decides on the open blocking rows plus the late rows |

Worked on the real flg-r2 counts: review 1 left 13 blocking rows (`F2D1:39`, 13 blocking applied) so CONTINUE; review 2 found 6 new blocking (`F2R2:13`) so U = 6, CONTINUE; review 3 found 1 (N12, `F2R3:15`) so U = 1 at n = 3, ESCALATE. That matches what happened (FAIL at review 3, escalated, `F2R3:19`), but the counter and the verdict were computed, not typed.

**Cap text and the sweep.** The variant command's cap bullet carries the pinned sentence verbatim: `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` (`CANONICAL_CAP_TEXT`, `W/bs346-ledger/tests/skills/test_review_severity_rule.py:215`) and the at-cap clause `HALT and escalate to the user with the open blocking findings` (`:216-219`). The cap is enforced, not just stated: `close` never returns CONTINUE at n = 3, so a revise phase cannot follow review 3, and `open` without `--sweep` at n = 3 exits 11. Fix cycles therefore stay at most 2.

**The final sweep is outside the 3-review cap.** Reasons: (a) the cap counts reviews that can start a fix cycle; the sweep cannot, its rows are `late`, immutable and unrevisable; (b) putting it inside review 3 would make the same session verify and then sweep, so the sweep would be anchored on the rows it just read, and the sweep is the only part of the design that can expose defects the verify scope hid (section 10); (c) the report header for it is `sweep`, never `review: 4 of 3`, so no text says four reviews. Cost is stated plainly: one extra fresh session and a second full read of `DOC`. Full-document reads per loop become 2 (review 1 and the sweep) instead of 3 (reviews 1 to 3 of the control, `AB:6`).

**PASS means the ledger is clean, not that the document is clean.** The loop verdict can be PASS at review 2 and the sweep can still find late blocking rows; `final` is then ESCALATE with those rows listed. That is deliberate: the sweep rows are reported and not looped on, so the user, not a third fix cycle, decides.

**No second computed stop.** rf-qa halts when the blocking count does not shrink (`RFQA:401`) and 427 chose not to (`DES:154`). Measured data supports skipping it: the critique proxy fell from review 1 to review 2 in all six S1 runs (11 to 9, 12 to 7, 9 to 5, 9 to 7, 16 to 5, 17 to 6; `AB:13`, `ARMB:13`), so a halt at n = 2 would never have fired, and at n = 3 the cap already fires. The script keeps the check optional (`close --monotonic`, default off) so rf-qa can adopt it (section 7).

## 5. Difference from PR 427 `--re-review --baseline`

427 re-reviews the changed document: its review 2 and 3 run the full panel on "lines changed against the baseline" and build the boundary table on changed guards (`SP:262`). The ledger changes the unit of review from "changed lines" to "answered rows", and moves five duties from a model to a script. Concretely:

| Duty | 427 (`SP:258-264`) | Ledger variant | What is removed |
|---|---|---|---|
| Prior findings input | a prose report, parsed by a model; stop if the `review: N of 3` header is missing (`SP:258`) | rows with ids and statuses, parsed by `json` | the model re-reading and re-tabulating the prior report each round (the 15-row Part 1 table at `F2R3:29-45` becomes `render` output) |
| `origin=` tag | written by the reviewer (`SP:262`; "treatment reads a tag", `AB:30`) | computed from hunks; `add` rejects an anchor outside a hunk | a mislabelled origin; the whole `origin=unchanged` note class in verify |
| Saved copy and baseline | kept by the coordinator, prose (`SP:261`, `DES:162`) | `open` and `close` write `r<n>.md` themselves | the failure "coordinator drops the saved copy, run becomes a first review" (`DES:162`) |
| Minor rows never revised | prose (`SP:259`, `SP:263`), overridden by the brief in flg-r2 (`F2D1:10`, `F2D1:37`) | `answer` on a deferred row exits 5; `revise-check` lists hunks no blocking row claims | a minor fix as a source of new blocking findings (the F22 to N5 to N12 chain) |
| Review count and verdict | the reviewer's `review: N of 3` header and last line (`SP:260`, `SP:261`) | `open` increments, `close` computes, the script writes the footer lines | a reviewer, or a brief saying "any finding of any severity" (`F2R3:15`), deciding PASS or FAIL |
| Reviser size report | "reports the byte size before and after" (`SP:263`) | `bytes_added` per row from `revise-check` | an unchecked self-report |
| Per-fix check | the whole changed-line set gets a full panel pass | two required answers per `fixed` row (`resolved`, `touched_ok`), then one panel pass limited to hunk text | the open-ended "find anything on changed lines" framing; the reviewer must close every row (`close` exits 6 on an unmarked `fixed` row) |
| Late findings | none; every review may raise anything on changed lines | one sweep, outside the cap, classified by where the defect sits | looping on them |

What the ledger does NOT remove, stated first because it matters most: the review surface does not shrink much. In flg-r2 review 3 the changed lines were 25 of 317 (7.9%, computed from `F2R3:25`), in ctl-r1 review 3 88 of 364 (24.2%, from `C1R3:11`), so 427 with its flags already restricted the surface to hunks. All 8 blocking findings of ctl-r1 review 3 (`C1R3:181-189`) have at least one anchor inside those changed lines (checked line by line against `C1R3:11`), and so does N12 (`F2R3:85`, lines 60, 210, 220, 317 are all in `F2R3:25`). A hunk-anchored verify therefore finds the same blocking rows 427 found. What changes is who holds the counts, the scope and the verdict, and that minor edits can be stopped mechanically. If the idea works on S1 it works mostly through the minor-row rule and the computed stop, not through a smaller read.

## 6. Exact changes, file by file

**Where the script lives and why.** A command file is one `.md` and `install_commands` copies only the top-level `*.md` files with `shutil.copy2` (`W/bs346-ledger/src/superclaude/cli/install_commands.py:38-41`, `:59-61`); a skill folder is copied whole by `shutil.copytree` (`W/bs346-ledger/src/superclaude/cli/install_skill.py:52`), and the wheel force-includes all of `src/` (`W/bs346-ledger/pyproject.toml:85-87`). So the script goes in a new skill folder and reaches `~/.claude/skills/sc-review-ledger/scripts/`. **Naming trap**: the skill must NOT be named `sc-spec-panel-ledger`. `install_all_skills` treats an `sc-<x>` skill with a `commands/<x>.md` file as "served by the command", skips it and deletes a stale installed copy, unless the command activates it with a `Skill sc-<x>` line (`W/bs346-ledger/src/superclaude/cli/install_skills.py:40-59`, `:88-98`). `sc-review-ledger` has no `commands/review-ledger.md`, so it installs standalone, like `sc-bare-review` (a skill with no slash command, `W/bs346-ledger/src/superclaude/skills/sc-bare-review/SKILL.md:3`). A python CLI subcommand (`superclaude ledger`) was rejected for the experiment: the machine's `superclaude` binary is the owner's install, not this worktree (cf. D9, `DEC:46`), so a changed CLI could not be tested without a machine-wide reinstall.

**New files**

| Path | Content |
|---|---|
| `src/superclaude/commands/spec-panel-ledger.md` | The variant command (outline below). |
| `src/superclaude/skills/sc-review-ledger/SKILL.md` | Frontmatter `name: sc-review-ledger`, delegate-only (no slash command), `allowed-tools: Read, Bash`; the file format, the transition table and the CLI, so other commands can cite it (section 7). |
| `src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py` | The script, stdlib only (`argparse`, `json`, `hashlib`, `difflib`, `os`, `pathlib`, `re`, `sys`); run as `uv run --no-project python "<skill base>/scripts/review_ledger.py" <subcommand> ...`. |
| `tests/skills/test_review_ledger_script.py` | Executable tests, loading the script with `importlib` like `W/bs346-ledger/tests/skills/test_workflow_archive.py:22-28`. |
| `tests/skills/test_spec_panel_ledger_command.py` | Text pins and the drift test (below). |
| `docs/designs/spec-panel-ledger-loop.md` | This design, trimmed, once approved. |

**Edited files**: none in the original loop. `spec-panel.md`, its `plugins/` copy, `HOW-WE-WORK.md` and the routing tests stay untouched (additive variant; promotion would be a separate change). No `UNATTENDED_COMMANDS` edit is needed because the variant omits `## Unattended mode` (the set-equality check is at `W/bs346-ledger/tests/skills/test_worker_contract.py:831-839`; `spec-panel` is in the set because of `SP:451`). `tests/unit/test_cli_install.py` needs no edit: its lists are baseline-member presence checks (`_assert_present`, `:501-505`). The plugin command list there is a strict subset of `src` (`:399-404`), so no plugin mirror is required.

**`spec-panel-ledger.md` outline.** Body = `SP:1-450` and `SP:463-486` unchanged, except: frontmatter `name: spec-panel-ledger`; Usage keeps `SP:22` minus `--re-review ... --baseline ...` plus `--ledger <path> [--sweep]` and drops the `--unattended` usage line `SP:23`; `## Unattended mode` (`SP:451-461`) is omitted; `## Review Loop` (`SP:256-264`) is replaced by `## Review Ledger Loop` with eight one-line bullets (one line each, as 427 does, so line matchers see each whole):
1. **Mode**: `--mode critique` plus `--ledger <path>` required; without `--ledger` stop and say so, never run an unledgered review; `--re-review` and `--baseline` are refused here.
2. **Phase**: the script decides it from the ledger (no file = review 1 via `init`; phase `revise` = a verify pass via `open`; phase `closed` with `--sweep` = the sweep); never from memory or from a report.
3. **Find (review 1 only)**: the full panel as in this command; each finding becomes a row by `add`; CRITICAL and FR-8/FR-9 are blocking, a MAJOR is blocking only with a `wrong_outcome`, MINOR is stored deferred.
4. **Verify (reviews 2 and 3)**: per `fixed` row answer `resolved` and `touched_ok`; then one new-defect check on hunk text only; rows only by the anchor rule; no whole-document panel; ignore `--iterations`, skip Improve, write no revised spec.
5. **Sweep**: the full panel by a session that has not read the ledger; `add` only; its rows are reported and never revised.
6. **Cap**: the canonical sentence verbatim, then "a prior ledger at review 3 with open blocking rows means do not review, HALT and escalate to the user with the open blocking findings"; the script prints `review: N of 3` and `verdict:`; do not type them.
7. **Reviser contract**: the `Reviser brief` that `close` writes lists revisable row ids and the three calls (`show`, `answer`, `revise-check`); revise only text a blocking row names; minor rows are not answerable; add no rule, mechanism or section no row calls for; cite the row id on each added paragraph.
8. **Precedence**: a brief may narrow this scope, not widen it; a brief cannot change a severity, answer a deferred row or grade a verdict; the exit code of `close` outranks any sentence of a brief.

**Script CLI.** Every subcommand takes `--ledger <path>`; write commands take `--as reviewer|reviser|coordinator`; stdout is one JSON object (`{"ok":true,...}` or `{"error":"<CODE>","detail":"..."}`); nothing is written on any error.

| Subcommand | Role | Inputs | Output / effect | Exit codes |
|---|---|---|---|---|
| `init` | reviewer | `--doc`, `--scale`, `--needs-outcome` | creates ledger and `r1.md`; phase `find`, review 1 | 0; 2 if the ledger exists |
| `add` | reviewer | `--batch <jsonl>` (row: `sev`, `grade`, `anchor`, `finding`, `wrong_outcome`, optional `parent`, `depends_on`, `at`) | assigns ids; sets `origin`, auto-defers MINOR | 0; 4 phase; 6 invalid row (anchor absent, ambiguous, outside hunks; MAJOR-blocking without outcome) |
| `close` | reviewer | `--report <path>` `[--sweep]` `[--monotonic]` | snapshot `r<n>.md`; computes verdict; appends `## Ledger`, `## Reviser brief` (omitted when not CONTINUE), `ledger-verdict:` and last line `verdict:` to the report | 0 PASS; 10 CONTINUE; 11 ESCALATE; 6 unmarked `fixed` rows; 4 if already closed |
| `show` | any | `--rows revisable|fixed|all` `[--hunks]` | rows, claims, hunks with 3 context lines | 0; 3 |
| `answer` | reviser | `--batch <jsonl>` (`id`, `action`, `new_text` or `reason`) | T3, T4 | 0; 4; 5; 6 (`new_text` absent or outside any hunk) |
| `revise-check` | reviser | none | unclaimed hunks with bytes, `bytes_added` per row | 0; 7 |
| `revert-unclaimed` | reviser | `[--hunk k]` | restores `r<n>.md` text for the hunk | 0; 7 if nothing to revert |
| `open` | reviewer | `[--sweep]` | review+1 (cap check), hunks vs `r<n-1>.md`, T9 retouches, unclaimed hunk list | 0; 4; 11 cap |
| `mark` | reviewer | `--batch <jsonl>` (`id`, `resolved`, `touched_ok`, `evidence`, `dispute`, `note`) | T5 to T8 | 0; 4; 5; 6 (T7 without child) |
| `defer` | coordinator | `--id`, `--accepted-by user`, `--quote` | T10 | 0; 4; 5 |
| `verdict` | any | none | `{"verdict","U","Lt","review"}`, read-only | 0 PASS; 10; 11 |
| `render` | any | none | markdown table of rows for a report | 0 |

Checks the script owns (each has a test): body hash; phase gate; role gate; anchor uniqueness (`--at` disambiguates); hunks by `difflib` on whitespace-collapsed lines; frozen fields; claim inside a hunk; child-row link for `touched_ok=no`; retouch detection; sweep classification; cap; atomic batch; idempotent `close` (second call exits 4).

**Tests, beyond the script suite.** `test_spec_panel_ledger_command.py` asserts: both `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` (imported as `tests/skills/test_spec_panel_review_loop.py` does, `DES:126`) appear in the variant; eight single-line bullets in order; `--ledger`, `--sweep`, the six subcommand names appear; no `src/superclaude` path (`DES` T9 style); the dual lookup text names `~/.claude/skills/sc-review-ledger` before the project `.claude/skills/sc-review-ledger`; no `## Unattended mode`; none of `BANNED_SEVERITY_PHRASES` (`test_review_severity_rule.py:112-117`); no cap number above 2 (`CAP_REGRESSION`, `:288-293`). **Drift test**: after removing frontmatter `name` and `description`, the Usage block, `## Review Loop`/`## Review Ledger Loop` and `## Unattended mode`, the variant equals `spec-panel.md`, so the 486-line panel cannot silently diverge. Run `uv run pytest tests/skills/test_review_severity_rule.py` first, as `DES:141` advises for 427, because its matchers scan every file under `src/` and `plugins/`.

**Experiment install (not a repo change).** As in D9 (`DEC:47`): the owner copies `spec-panel-ledger.md` to `~/.claude/commands/sc/` and the folder `sc-review-ledger/` to `~/.claude/skills/`; the briefs get the one-line name change and `--ledger <path>`; a personal command beats a project one (`DEC:46`), and a different command NAME lets an arm run beside others (`AB:47`). Then `make sync-dev`, `make verify-sync`; never stage `.claude/`.

## 7. Adoption by reflect, rf-qa and the implement final review

What makes the core reusable, and is therefore built in from the start: the script knows no spec-panel words. `init --scale <grades> --needs-outcome <grades>` takes the caller's severity vocabulary; `sev` stays `blocking|minor`; `anchor` is a quote from one `--doc` file. Two things the first version does NOT do and adopters need: several files per ledger (v1 is single-file; a per-file snapshot and per-file hunks are the extension) and concurrent writers (v1 writes by temp file plus `os.replace`, so two parallel QA instances on one ledger lose updates; an adopter needs `fcntl.flock` or one ledger per partition).

| Adopter | Rows come from | Needs | What stays different |
|---|---|---|---|
| `/sc:reflect` (`W/bs346-ledger/src/superclaude/skills/sc-reflect-protocol/SKILL.md`) | the merged Wave 5 findings after the evidence-validator, the "non-negotiable final gate" that drops unfounded items (`SKILL.md:587`), so only grounded rows are `add`ed | a `--ledger` flag; `--scale` set to its deviation taxonomy (Authorized expansion, Necessary deviation, Drift, Regression, per the skill's own description); multi-file `--doc` for code or plan trees; the caller (implement or workflow) owns the loop, because reflect has no loop input in the lines I read (two long lines, `SKILL.md:3` and `:35`, were not opened: UNVERIFIED) | the Tier 2 heterogeneous fan-out and adversarial merge stay for the find pass only; verify rounds can use one Tier 1 reviewer, which is the cost saving; the taxonomy, not CRITICAL/MAJOR/MINOR, decides what is blocking |
| rf-qa agents (`RFQA:379-416`) | the gate's findings | the Fix Cycle steps 1 to 5 (`RFQA:386-396`) already say "verify the blocking issues, do not recheck minor findings" in prose; the change is to replace "the previous QA report" by the ledger, step 2 by `mark`, step 4 by child rows, step 5 by `verdict`, and the monotonicity halt `|F_{n+1}| < |F_n|` (`RFQA:401`) by `close --monotonic`; one paragraph in the agent file pointing to `~/.claude/skills/sc-review-ledger` | rf-qa grades CRITICAL/IMPORTANT/MINOR (`DES:72`); QA instances run partitioned and in parallel (locking, above); rf-qa "fixes issues in-place when authorized" (agent description), so finder and reviser can be one agent and the `--as` role split is only advice there |
| `/sc:implement` final review (`W/bs346-ledger/src/superclaude/skills/sc-implement-protocol/refs/qa.md`, `managed-workspace.md:55`) | FINAL `issues` with `path:line` per AC | a ledger per archive attempt, a mapping from `F<k>.<j>` ids (`QA:137`) and status words `resolved|open|regressed` (`QA:143`) to `verified|reopened`, `origin=inherited` (`QA:166`) as the hunk rule | implement already splits "reviewer reports, orchestrator computes" (`QA:334`) and parent-written `sev=`/`origin=` (`QA:141`), so it is ahead of spec-panel on that point. But `QA:186` lets every re-review raise a new blocker anywhere in task-owned text, the opposite of verify-only; adopting means a deliberate policy change plus edits to pinned text. Recommendation: do not adopt there until an implement incident shows the same fix-induced pattern (S5 is outside the S1 data, `AB:43`). |

Order of adoption: spec-panel (this experiment), then rf-qa (the prose it already has maps one to one), then reflect; implement last or never.

## 8. Stateful reviewer session versus file ledger

A stateful design keeps one reviewer session alive across the rounds (same Orca terminal, or `SendMessage` to the same agent), so "the ledger" is its own context.

| Axis | Stateful session | File ledger with fresh sessions |
|---|---|---|
| Independence | the finder verifies its own findings; a fix is judged by the mind that wanted it | each verify is a new session; the round-3 reviewer of flg-r2 re-read live `worker-read --help` and the e2e evidence and found that the N5 fix was wrong in a way the "as asked" check passes (`F2R3:35`, `F2R3:86`); I infer a finder-verifier would more often stop at "resolved as asked" (inference, not measured) |
| Mechanical stop, cap, scope | none; every rule stays prose, which is the measured failure (`DES:143`, `F2D1:10`) | exit codes, a counter, a hunk check |
| Survives crash, compaction, a new worker | no; the report is the only record | yes; the file is the record and the audit trail (`hist`) |
| Cost | cheapest: no script, no row parsing, no extra calls | about 25 to 30 script calls per loop and one extra session (section 11) |
| Fits the other tools | no: rf-qa and implement spawn fresh subagents by design (`managed-workspace.md:55` "always a Task subagent, even N=1") | yes: the ledger is the only thing that crosses the fresh-session boundary |
| Fits the S1 test | changes the experimental variable (S1 uses a fresh reviewer per review, `F2R3:3`) | keeps it |

**Recommendation: the file ledger, with fresh sessions.** The state worth keeping is small (id, anchor, severity, status, claim); a file carries it exactly and lets a script, not a model, enforce it. A stateful session is the cheap fallback experiment if the ledger does not beat 427: same briefs, one reviewer kept alive, no script. It cannot be adopted by implement or rf-qa without breaking their fresh-reviewer rule.

## 9. Measurement plan on scenario S1

**Arm "led"** (two fresh worktrees, for example `exp346-ab-led-r1` and `-r2`), identical to Arm B in everything D11 fixes: scenario S1, base commit 2cb683f5, overlay, verbatim briefs T05 to T09, model claude-opus-5-5, `WORKER-CONTRACT.md` moved aside, watcher on the installed command sha256 (`DEC:59`, `DEC:64`). Changes, all recorded: (1) in the three review briefs `/sc:spec-panel` becomes `/sc:spec-panel-ledger` and `--ledger .dev/orca-command-refactor/review/ledger.jsonl` is appended (no `--re-review`, no `--baseline`); (2) the owner installs the command and the `sc-review-ledger` folder by hand (section 6); (3) ONE added dispatch after review 3: the sweep brief, `/sc:spec-panel-ledger @<spec> --mode critique --focus requirements,architecture --ledger <L> --sweep`. Reviser briefs are unchanged: they read the report, and the report carries the script-written Reviser brief. The added sixth session is a stated deviation; it is the price of the design (section 11).

**Baseline sweep (added so "hiding" can be measured, not argued).** Run the same sweep, as a plain whole-document `/sc:spec-panel` critique with the same focus, on the FINAL spec of each existing replicate: ctl-r1, ctl-r2, trt-r1, trt-r2, flg-r1, flg-r2 (copies made read-only first; the worktrees hold them under `.dev/orca-command-refactor/specs/`). That gives how many critical+major findings a whole-document pass still finds in a 427-loop document, the number the ledger's sweep must be compared with.

**Metrics** (D5 M1 to M5 as before, `DEC:23`, plus these, all read from `L` or the script, not from report prose):
- **P3, "review 3 critical+major" in a ledger loop** = number of rows with grade CRITICAL or MAJOR whose status after the review 3 `close` is `reopened`, `open` or `fixed` (that is: rows review 3 re-raised plus new child rows it added). Grade, not `sev`, so that MAJOR rows 427 relabels as minor are counted exactly as the proxy counted them (`ARMB:37`); `U` (blocking only) is reported next to it. A `reopened` row is the ledger name for what the control reports call "Partly" (`C1R3:17`), so the two are comparable.
- **P3s** = P3 plus the sweep's rows of grade CRITICAL or MAJOR. This is the pre-registered conservative metric, because the control's review 3 was a whole-document pass (`AB:30`). P3 alone is the analogue of Arm B's hunk-scoped review 3.
- **H, hidden-defect share** = sweep CRITICAL/MAJOR rows / (P3 + sweep CRITICAL/MAJOR rows), split by the script into `in_claimed_span`, `in_unclaimed_hunk`, `outside_hunks`.
- **Growth after 2 fix cycles** = size of `DOC` after revise 2 against 57,763 bytes, as in `AB` and `ARMB` (flg-r2: 76,328 / 57,763 = +32.1%, `ARMB:16`).
- **Scope metrics**: `minor_touched` (hunks overlapping the anchor span of a deferred row), unclaimed bytes, `revise-check` exit-7 count, `revert-unclaimed` uses.
- **Cost**: script calls, sessions, wall time per step, report bytes per review (flg-r2 baseline: 50,563, 48,693, 39,100 bytes for reviews 1 to 3, from `ls -la`).

**Bar (set now, same shape as D10 and D11).** The ledger arm counts as better than control only if: (a) P3s mean at most 3 (50% of control mean 6.0, `AB:19`), or a clean pass in fewer rounds; (b) growth at most 44.4%; (c) the effect exceeds the larger within-arm spread; and every ledger replicate is on the better side of both control replicates for (a) and (b) (R3 proxy 8 and 4, so each replicate at most 3; growth below 57.7%). Beating 427 with flags additionally needs P3s mean below 3.5 and growth at most 30.0% (`ARMB:20`).

**Predictions, grounded in traced rows.**

| Trace | What the ledger loop would have done | P3 |
|---|---|---|
| flg-r2, review 3 (`F2R3`) | F22 stays deferred (`answer` refused), so the AC-0.4 WC-1 proof is never written, N5 and N12 never exist; the other five blocking N-rows were resolved at review 3 (`F2R3:31-36`) | 0 to 1 (1 if a different child appears) |
| ctl-r1, review 3 (`C1R3:181-189`) | 8 blocking findings; every one has an anchor inside the changed lines, so verify finds all 8; R3-9 may trace to minor row M2 (`C1R3:196` "M2 resolved for the named instance with a separate defect"), which the ledger would not have edited | 7 to 8 |
| ctl-r1, late share | R3-4, R3-8, R3-9 predate the revision and were missed in round 2 (`C1R3:205`); verify-only would leave them to the sweep | sweep 3 or more |

- **P3 (verify only)**: mean 3.0, plausible range 0 to 7; chance that both replicates are at most 3: about 30%. The shape is bimodal: a clean-ish run when the damage chain starts from a minor row, an unchanged run when it starts from blocking rows.
- **Sweep (CRITICAL/MAJOR)**: mean 3, range 1 to 6 (UNVERIFIED; anchored only on ctl-r1's three pre-existing blockers and on R1 counts of 9 to 17 for a whole-document pass, `AB:13`, `ARMB:13`).
- **P3s**: mean about 5.5, so bar (a) is probably NOT met on the conservative metric.
- **Growth**: mean 23% (range 17 to 30). Derivation: Arm B cycle-1 growth 17.5% and 21.6% times (1 - 0.15), plus the cycle-2 increments 10.3 and 10.5 points times (1 - 0.38), where 0.15 and 0.38 are the shares of changed-line bytes carrying only a minor finding id in flg-r2 (3,920 of 26,768 for revise 1; 7,212 of 19,205 for revise 2; my `diff -w` attribution of whole lines, one replicate, so an upper bound on the saving). Gives 21.3% and 24.9%. Bar (b) passes, but 427 already passes it (`ARMB:24`), so growth cannot show the ledger is better.

**What result would mean the idea failed.** Any of: (1) P3 mean at least 4 (no better than 427 plus flags, which scored 3.5 with spread 5, `ARMB:25`); (2) P3 at most 3 but the ledger sweep finds at least 2 more CRITICAL/MAJOR rows on average than the baseline sweep finds on the flg final specs (the loop hid defects instead of preventing them); (3) `minor_touched` above 0 in either replicate with exit-7 gating on (the mechanical scope rule leaked, usually by claiming a minor edit under a blocking row); (4) a stalled loop caused by the script (a refused call with no recovery path) in either replicate; (5) growth above 30.0%. A result inside the spread of both arms is "not significant", as D6 says.

## 10. Which measured causes the mechanism removes and which it leaves

| Cause | Measured evidence | Verdict | How, and what remains |
|---|---|---|---|
| Fix-induced defects on changed lines | 89% (R2) and 100% (R3) of new findings are `origin=changed` (`AB:30`); flg-r2: 13 blocking fixes gave 6 new blocking (0.46 per fix), 6 gave 1 (0.17) (`F2R2:13`, `F2R3:15`) | **LEFT** | The reviser still writes the defects. The ledger finds them as child rows and names the fix that caused each, which helps the next reviser, nothing more. |
| Reviser applies minor rows and "related defects" | 9 of the 15 rows applied in revise 2 were non-blocking (N7 to N11, C9, C12 to C14; `F2D2:35`); the F22 chain (`F2D1:37`); E5 and AC-1.2 fixed "while applying" (`F2D2:13`) | **REMOVED for minor rows, PARTLY for scope** | `answer` refuses minor rows; hunks no blocking row claims are listed and revertible. A reviser can still widen a blocking fix under the same row id (E5 was the same false claim as N4's, so it was claimable); only `bytes_added` per row is recorded. |
| Reviser adds a mechanism inside a blocking fix | N12 came from the N5 fix adding a new "record the agent command" step (`F2R3:15`, `F2R3:35`) | **LEFT** | Nothing in a script can tell a needed step from an extra one. Per-row byte budgets belong to the minfix theme. |
| Severity drift between rounds | thin: the one traced case is a panel disagreement on a NEW row, resolved upward (`F2R3:144`); 427 grading relabels MAJOR as minor in flg-r1 (`ARMB:37`) | **REMOVED for existing rows, LEFT for new rows** | `sev` and `grade` are frozen and a verifier cannot raise a row. A child row still gets a fresh grade from the verifier; `wrong_outcome` is required for MAJOR-blocking so the grade is auditable, but who judges it is a model. |
| No mechanical stop, verdict by judgement, brief overriding the command | "any finding of any severity is FAIL" in the brief (`F2R3:15`); count kept by prose (`DES:162`) | **REMOVED** for the reviewer session | counter, cap (`open` exit 11), computed verdict, footer written by the script. A coordinator that loops anyway is not stopped (PROSE). |
| Pre-existing defects found late | 3 of the 8 ctl-r1 review-3 blockers predate the revision (`C1R3:205`) | **RELABELLED, not prevented** | they surface in the sweep and are reported, not fixed. |

**Why two fix cycles cannot be promised to converge, with or without the ledger.** If each cycle leaves a fraction r of its blocking fixes as new blocking defects, the expected count at review 3 is about B1 x r x r. With B1 = 13 and the two measured ratios 0.46 then 0.17 it is 1.0 (flg-r2's actual 1); with r = 0.46 twice it is 2.7; with r = 0.17 twice it is 0.4. PASS inside the cap needs B1 x r x r below 1, so the mechanism's honest ceiling is "escalate with 0 to 3 rows", not "always PASS". Only a lower r (a better reviser) or a lower B1 (a better find pass) changes that; the ledger changes neither directly. Its only lever on r is fewer edits (minor rows) and visible `bytes_added`.

**The strongest argument that a verify-only pass hides defects instead of preventing them** (I tried to make it as hard as I can):
1. P3 is lower than a whole-document R3 by construction. Anything outside a hunk cannot become a row in verify, so the number of rows can only fall; if I report P3 and not the sweep, the idea looks better while the document is no better. The ctl-r1 trace shows the size of that effect (3 of 8, `C1R3:205`).
2. Interaction defects are the likely casualties. N15 in flg-r2 (step 1 unchanged, contradicted by 2.3, `F2R3:99-101`) is exactly an `origin=unchanged` finding; the ledger rejects it unless the reviewer finds the right `depends_on` quote. So the reviewer is now paid to find a changed line to hang the defect on.
3. Two tick-box answers per row invite "yes, yes". The real round-3 reviewer did far more than tick: it re-ran greps and read live help (`F2R3:51`, `F2R3:86`). A satisficing verifier passes fixes that deserve N12.
4. The sweep is the only guard, and by design nothing it finds is fixed. A PASS at review 2 with a sweep that returns 4 blocking rows is a hollow PASS that the user sees only at the end.
5. A model that cannot add a row anywhere may add it nowhere: the incentive of `add` refusing is to file fewer rows.

**What the data say about it, and what they do not.** For (1): the three pre-existing ctl-r1 blockers still have an anchor inside a changed line (R3-4 at `SPEC:245`, R3-8 at `SPEC:207,210`, R3-9 at `SPEC:224,238`, all in the changed list at `C1R3:11`), and all eight blockers do; so in the two traces hunk-anchoring lost nothing. That is two documents, one reviewer model. It does not exclude far-from-hunk defects, which only the baseline sweep (section 9) can measure. For (3) I add one mechanical counter: `mark resolved=yes` requires an `evidence` field, a quote that must be byte-present in the current `DOC` (it proves the reviewer opened the text, not that it judged well). For (5) I have no counter other than the sweep's `outside_hunks` count, so that number is the early-warning metric. Items (2) and (4) stay open risks.

## 11. Risks and costs

**Costs per loop** (counts are from the section 2 table; times are estimates, UNVERIFIED):
- Sessions: 6 instead of 5 (reviews 1 to 3, two revisers, one sweep). The experiment adds up to 6 more for the baseline sweeps (section 9).
- Script calls: about 3 to 4 in review 1, 3 to 7 per revise, 4 to 5 per verify, 3 in the sweep: 20 to 31 per loop, each one `uv run --no-project python` start (well under a second each, not measured). Batch inputs keep it from being one call per row.
- Wall time: the sweep is a full review. File times in both worktrees show 9 to 16 minutes between a disposition and the next review report (flg-r2: disposition 13:14, round 2 at 13:26; disposition 13:32, round 3 at 13:41; `ls -la` of `W/exp346-ab-flg-r2/.dev/orca-command-refactor/review/`), so expect about +10 to +15 minutes per loop minus whatever the shorter verify reports save. Verify reports (48.7 KB and 39.1 KB for reviews 2 and 3 in flg-r2, `ls -la`) may shrink because `render` replaces the hand-built Part 1 table; not measured.
- Tokens: findings are written once as JSONL rows and the report narrative refers to ids, instead of the report holding them alone. If the reviewer writes both in full, output tokens rise. The command says "write each finding once, as a row".

**Ways the ledger could make the loop worse**
1. The refusal paths stall a loop: an `add` rejected because a quote is not unique or differs in whitespace; the reviser cannot get `revise-check` to 0 because an edit spans hunks. Mitigations: error text lists candidate lines; `--at`; `revert-unclaimed`. Residual: MEDIUM until the script has run on three real documents.
2. Hidden defects (section 10, items 1, 2, 4, 5). The baseline sweep is how this is measured.
3. A moved section turns every line into a hunk, so verify degrades to a full review. The script prints `HUNKS_LARGE` when changed lines exceed 40% of `DOC` (my threshold, UNVERIFIED as right) and the report footer repeats it.
4. Deferred minor rows stay unfixed; a minor ambiguity can later be an implementer's wrong outcome. S1 cannot show this because it ends at review 3.
5. A wrongly graded first row forces a fix cycle and cannot be demoted except by the user at the end (T10).
6. A harmless reformat of `ledger.jsonl` by a person fails the hash (`LEDGER_TAMPERED`) and stops every command. A `reseal --reason` command is needed (open question 4).
7. Experiment confounds: the extra sweep dispatch, the name change, the hand install, and a sweep reviewer that reads `L` anyway.
8. An unattended coordinator told to "re-review until PASS" meets exit 11 at review 3 and may hang or retry. The command's Cap bullet and the footer both say HALT.

**Rule by rule: MECHANICAL (script-enforced) or PROSE (a model is asked), and the residual risk**

| Rule | Kind | Residual risk |
|---|---|---|
| Row ids, anchor exists, MAJOR-blocking has `wrong_outcome`, MINOR auto-deferred | MECHANICAL | a quote proves presence, not relevance; `wrong_outcome` can be filler |
| Phase order (`init`, `add`, `close`, `open`, `mark`, sweep) | MECHANICAL | none beyond bugs |
| Who may call what (`--as`) | PHASE is mechanical; IDENTITY is PROSE | any session can declare any role |
| Frozen `sev`, `grade`, `anchor`, `wrong_outcome` | MECHANICAL | the first grade is a model's judgement |
| Illegal transitions refused (T1 to T11, forbidden moves) | MECHANICAL | none beyond bugs |
| Minor rows unanswerable | MECHANICAL | the reviser can still edit the text; caught only if `revise-check` runs |
| Reviser runs `revise-check` and reverts or claims hunks | PROSE to run it; detection is MECHANICAL | skipped check; `open` still lists unclaimed hunks and `minor_touched` records it, but nothing blocks |
| A claim must lie in a hunk | MECHANICAL | a small quote inside a large hunk claims the whole hunk (lenient overlap) |
| Both questions answered per `fixed` row; `close` refuses unmarked rows | MECHANICAL | answer quality, yes-yes bias; `evidence` only proves the text was opened |
| New rows only in hunks or with `depends_on` in a hunk | MECHANICAL | interaction defects hidden; honesty of `depends_on` |
| No whole-document panel during verify | PROSE | a reviewer may run it anyway, costing time; rows still obey the anchor rule |
| Review counter, cap, verdict, footer lines | MECHANICAL | a coordinator that ignores exit codes |
| Sweep feeds no reviser; `closed` refuses `mark` and `answer` | MECHANICAL | a person may start a new ledger from the late rows (a decision, not a leak) |
| Sweep reviewer does not read `L` | PROSE | anchoring; shows up as an `in_claimed_span` count of 0 |
| Brief may narrow, not widen | PROSE text, but its main effects (no answer to deferred rows, no verdict from a brief) are MECHANICAL | a brief can still direct edits outside any row |
| Variant equals `spec-panel.md` outside the replaced sections | MECHANICAL (drift test) | none |
| Dual lookup of the script path | PROSE; the test pins the text only | a host with neither copy fails at the first call, loudly (exit not 0) |

## 12. Open questions

1. **Late findings with cycles left.** If the loop is PASS at review 1 or 2 and the sweep finds blocking rows, this design only reports them (as the theme says). Should a second ledger be started from them, by default or only by the user? Recommendation: only by the user.
2. **Unclaimed hunks: record or refuse?** Now `revise-check` exits 7 (the reviser is asked to claim or revert) but `open` only records and lists them, so a reviser that skips the check does not stall the loop. Making `open` refuse is stricter but can deadlock an unattended run. Decide after the first run shows how often exit 7 happens.
3. **Several files and parallel writers.** v1 is one `--doc` and one writer. reflect and rf-qa need per-file snapshots and a file lock (section 7). Build now or at adoption?
4. **`reseal --reason`.** The body hash catches hand edits but also harmless reformatting. Add a logged reseal command, or drop the hash and rely on schema and phase validation?
5. **Per-row byte budget.** `bytes_added` is reported, not limited. A limit is the minfix theme; should this script carry the field so both themes share one checker?
6. **Sweep independence.** The sweep reviewer is told not to read `L`. Is the lost duplicate suppression worth it? The script already classifies overlaps (`in_claimed_span`), so duplicates cost only a few rows.
7. **Who grades child rows.** The freeze covers existing rows only. A frozen rubric or an independent confirmation of each new blocking row belongs to the stoprule theme; the two could share the `wrong_outcome` field.
8. **Hunk computation parity.** `difflib` on whitespace-collapsed lines versus `git diff --no-index -w -U0` (`F2R3:25`): they can differ on moved text. Test on the three S1 history pairs (`HIST/spec-v1-draft.md`, `spec-v2-after-round1.md`, `spec-v3-after-round2.md`) before the first run, and pick the `HUNKS_LARGE` threshold from them.
9. **The coordinator brief still says "apply confirmed findings"** (`F2D1:10`). The experiment keeps it verbatim so that the result shows whether the script beats the brief. If the arm needs a brief edit to run at all, that is a finding.
10. **UNVERIFIED in this spec**: that every worker environment has `uv` (the `managed-workspace.md:54` pattern assumes it); that no S1 brief passes `--unattended` (the round-3 run line shows none, `F2R3:80`, the other briefs were not opened); the size of any token or wall-time saving; whether `reflect`'s two unopened long lines (`SKILL.md:3`, `:35`) describe a loop input; the yes-yes rate of a verify reviewer; whether `plugins/` tests would need a mirror (the plugin command list in `tests/unit/test_cli_install.py:399-404` suggests not).
