---
name: sc-spec-panel-stoprule-protocol
description: "Delegate-only protocol for /sc:spec-panel-stoprule (activated by that command, no slash command of its own): the review-loop verdict, review cap, Reviser brief and escalation are computed by scripts/stoprule.py from a sealed claim ledger inside the report, and a blind finding-grader agent decides only whether each claim is blocking under the frozen rubric."
allowed-tools: Read, Write, Bash, Agent
---

# sc-spec-panel-stoprule-protocol

Activated only by `/sc:spec-panel-stoprule` in critique mode. The reviewer never writes a verdict: `stoprule.py` computes it from the ledger, and `check` proves the last line came from the ledger.

`<skill base>` is the folder holding this file: `~/.claude/skills/sc-spec-panel-stoprule-protocol/` first, else the project copy `.claude/skills/sc-spec-panel-stoprule-protocol/`. Every script call has the form `uv run --no-project python "<skill base>/scripts/stoprule.py" <sub> ...`. Global options (`--rubric`, `--canaries`, `--cap`, `--root`) go before `<sub>`; every subcommand accepts `--dry-run`, which prints what it would write and writes no file.

## Who runs which step (owner ruling)

Reviewer and reviser sessions run only script calls that write no file: `--dry-run` calls, `grade-prep`, `audit-prep`, `status`, `verdict` and `check`. The reviewer writes only its report: the prose and its own ledger lines (`claim`, `prior`, `checked`). Every call that writes the report (`begin`, `seal`, `apply-grades`, `apply-audit`, `finalize`) is a coordinator step with its own brief template. With no coordinator (a person running the command directly), the same session runs both columns in this order.

| Step | Who | Command |
|---|---|---|
| S0 begin | coordinator, before dispatching the reviewer | `uv run --no-project python "<skill base>/scripts/stoprule.py" begin --report <report> --spec <spec> [--re-review <prior report> --baseline <saved copy>]` |
| S1 review | reviewer | the panel runs as the command says; append one `claim` per finding of any label, one `prior` per prior blocking id `begin` printed, one `checked` per changed hunk reviewed and found clean |
| S2 self-check | reviewer | `uv run --no-project python "<skill base>/scripts/stoprule.py" seal --report <report> --spec <spec> --dry-run`; on exit 3 repair the listed claims once and run it again |
| S2 seal | coordinator | `uv run --no-project python "<skill base>/scripts/stoprule.py" seal --report <report> --spec <spec>`; on exit 3 run it a second time, which is final (still-failing claims become `minor-form`) |
| S3 grade-prep | coordinator | `uv run --no-project python "<skill base>/scripts/stoprule.py" grade-prep --report <report>` |
| S4 grader | coordinator | one Agent call per printed batch, all batches in one message: `subagent_type: finding-grader`, prompt = the batch text from its `=== BATCH Bn ===` line to its `=== END BATCH Bn ===` line, unchanged; save each reply verbatim to a file |
| S5 apply-grades | coordinator | `uv run --no-project python "<skill base>/scripts/stoprule.py" apply-grades --report <report> --batch <Bn> --reply <reply file>`; on exit 3 run S3 again and re-send only that batch once |
| S6 audit-prep | coordinator, only when `verdict` shows no confirmed claim and no open prior | `uv run --no-project python "<skill base>/scripts/stoprule.py" audit-prep --report <report> --spec <spec>`, then one fresh general-purpose Agent call whose prompt is the printed `=== AUDIT ===` block; save the reply |
| S7 apply-audit | coordinator | `uv run --no-project python "<skill base>/scripts/stoprule.py" apply-audit --report <report> --reply <audit reply file>` (no `--reply` when the auditor was unavailable: FAIL `incomplete`) |
| S8 status | reviewer or coordinator | `uv run --no-project python "<skill base>/scripts/stoprule.py" status --report <report>`; the prose copies these statuses and may add one line `brief-verdict: PASS` or `brief-verdict: FAIL`, never a `verdict:` line |
| S9 finalize | coordinator | `uv run --no-project python "<skill base>/scripts/stoprule.py" finalize --report <report> [--grader-model sonnet --reviewer-model <model>]` writes `## Computed result`, then the Reviser brief (reviews 1 and 2, FAIL), the `## Escalation to the user` section (review 3, FAIL) or PASS with known debt, then the sentinel and the last line `verdict: PASS` or `verdict: FAIL` |
| S10 check | reviewer last, coordinator again | `uv run --no-project python "<skill base>/scripts/stoprule.py" check --report <report> --spec <spec>` (exit 0 or 6) |

The coordinator re-runs `check` on the report before dispatching the reviser and stops on exit 6. It then fills the reviser template's finding range with `D1-Dk` from the Reviser brief's `Reviser range:` line, or `NONE` ("No confirmed blocking findings: make no spec edit"). After the reviser it runs `check-disposition --report <report> --disposition <disposition file>` and records any id applied outside D1..Dk (reported, never blocking).

Recorder steps, outside the loop: `verify-transcript --report <report> --transcript <session .jsonl>` (prints `grader-integrity: verified|mismatch|unverified`), `count --report <review-3 report>` (prints `m0_label_cm`, `m0_deferred_cm`, `m1_open_confirmed`) and `audit-sample --report <reports...> --seed <n> --owner-k 5`.

## The ledger

A fenced block in the report, opened by `begin`: ```` ```stoprule-ledger ```` ... ```` ``` ````, one JSON object per line. The reviewer adds only these three kinds, inside the block, before its closing fence:

```
{"k":"claim","id":"R2-1","claimed":"critical|major|minor","quote":"<verbatim spec text, 20 non-space to 300 chars, unique>","span":"<the defective words, part of quote, <=120 chars>","outcome":"<a named reader, implementer or test that follows the quote and the wrong result, >= 8 words>","evidence":[{"path":"<repo path>","line":12,"text":"<verbatim>"} or {"live":"<command>","saw":"<output>"}],"prior":null or "<prior id>","sites":["<other verbatim places of the same defect>"]}
{"k":"prior","id":"R1-3","status":"resolved|open|regressed","resolved_by":"<verbatim text now in the spec>" or null}
{"k":"checked","lines":"170-182"}
```

A GAP or blank Boundary Table row is a candidate `claim`, never an automatic MAJOR. For an omission, quote the requirement or guard whose promised behaviour is incomplete. Every other record kind is written by the script.

## Failure table

| Event | Result | What the session does |
|---|---|---|
| grader reply invalid twice, or Agent tool unavailable | those claims stay `unconfirmed`; verdict FAIL `incomplete` | nothing more; the Reviser brief is NONE, so no reviser edits |
| auditor reply missing or invalid | verdict FAIL `incomplete` | nothing more; never hand-type a PASS |
| exit 3 (repairable once) | `seal` lists the bad claims or uncovered hunks; `apply-grades` rejected a batch | repair once (reviewer: claims; coordinator: re-send the batch); the second run is final |
| exit 4 (HALT at cap) | `begin` found a prior review 3: it prints the prior escalation, or "loop already ended" for a PASS | do not review; HALT and escalate to the user with the open blocking findings |
| exit 5 (stop, bad input) | a missing or invalid sentinel on `--re-review`, a baseline or rubric hash mismatch, a prior verdict that does not match its ledger, a changed spec, a hand-typed `verdict:` line, a usage error | stop and report the message; do not start a review without it |
| exit 6 (ledger tampered) | `check` found an edited ledger line, a changed `grade-raw` text, a record that does not follow from the ledger, or no sentinel | stop; the report is non-compliant and the coordinator does not dispatch the reviser |

## Do not

- Do not write a `verdict:` line by hand; only `finalize` writes it, and a hand-typed one makes `finalize` refuse (exit 5) or `check` fail (exit 6).
- Do not edit any ledger line after `seal`: the seal hash covers every reviewer line and a hash chain covers every script line.
- Do not edit `refs/rubric.md`: `begin` refuses a rubric hash that differs from the loop's review-1 hash, and a new rubric starts a new loop.
- Do not batch, rename or reword a grader batch, and do not show the grader the report, the spec path, a reviewer label or an expert name.
- Do not run a fourth review: at review 3 `begin` exits 4.
