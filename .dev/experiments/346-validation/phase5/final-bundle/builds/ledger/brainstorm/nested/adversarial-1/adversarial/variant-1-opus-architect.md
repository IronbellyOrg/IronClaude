# Variant 1 (architect): finding ledger with separate FIND and VERIFY phases for `/sc:spec-panel-ledger`

Status: design only, nothing implemented. Author: variant 1 of 3 (architect lens: maintainability and extension seams). Date 2026-11-08.

## 1. Problem and evidence

- S1, n=2 per arm: no run of control, 427 or 427+flags reached PASS; R3 critical+major proxy means 6.0 / 5.5 / 3.5 against a bar of 3 (`exp346-p1-logs/.../phase4/AB-REPORT.md:13,19`, `ARMB-REPORT.md:13,20,23`).
- 89% (R2) and 100% (R3) of new treatment findings sat on lines the previous fix changed (`AB-REPORT.md:30`); flg-r2 R3 resolved 6 of 6 prior blockers, then found N12, created by the N5 fix (`exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round3.md:15,35`).
- Revisers widen scope: disposition-round2 applied 15 of 15 rows, 9 of them minor, plus "related defects found while applying" (`disposition-round2.md:13,35`).
- The verdict, the count and the baseline are prose: "every rule here is prose read by a model" (`docs/designs/spec-panel-review-loop.md:143`), "nothing enforces the count" (`:162`).

## 2. Mechanism

Three components, each with one job, so later adopters reuse the first two unchanged:

| Component | Job | Ships as |
|---|---|---|
| Ledger kernel | The ONLY writer of ledger state: snapshots, diffs, anchors, transitions, verdict | `scripts/review_ledger.py` inside skill `sc-review-ledger` |
| Ledger contract | Roles, file layout, input schemas, CLI, how to add a profile | `sc-review-ledger/SKILL.md` (delegate-only, like `sc-bare-review`, `src/superclaude/skills/sc-bare-review/SKILL.md:20-24`) |
| Adapter | Tool-specific review behaviour plus a severity profile name | `/sc:spec-panel-ledger` (profile `spec-panel`); later reflect, rf-qa, implement |

Models never edit `ledger.json`. They write small JSON input files with the Write tool; the script validates and ingests them atomically (all rows or none). Every script call below is `uv run --no-project python "<skill base>/scripts/review_ledger.py" <subcommand> ...`, the form skills already use (`src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:54`). `<skill base>` is given by the Skill tool when the command invokes `sc-review-ledger`. Below, `L` is the ledger directory and `D` the document.

**Review 1 (FIND, full document).** Who: the `/sc:spec-panel-ledger --mode critique` session.
1. Invoke Skill `sc-review-ledger`. Run `init --doc D [--ledger L] --profile spec-panel`. The script creates `L`, copies `D` to `L/snapshots/r1.md` with its sha256, sets `round=1 phase=find`. It refuses with exit 3 `E-EXISTS` if `L/ledger.json` exists, so a lost flag can never restart a first review.
2. The panel runs the normal critique over the whole document and writes the report `R1` (header `review: 1 of 3`).
3. The reviewer writes `L/inputs/r1-find.json` (one object per finding: label, severity, rule tag, anchor quote, wrong outcome, summary) and runs `find --ledger L --input L/inputs/r1-find.json`. The script checks each anchor against `snapshots/r1.md`, computes `blocking` from the profile, sets `open` (blocking) or `deferred` (non-blocking), and prints the decision preview.
4. Run `close --ledger L --report R1`: the script checks the `review: 1 of 3` header, appends the ledger summary, the script-written Reviser brief (CONTINUE only) and the last line `verdict: PASS|FAIL`. If the decision is PASS (no blocking row), the find pass itself counts as the final sweep.

**Revise 1.** Who: a separate reviser session (its brief is unchanged; it reads the report, as 427 already relies on, `src/superclaude/commands/spec-panel.md:263`).
1. Reads the Reviser brief the script wrote: the open blocking row ids, each with anchor, wrong outcome, and the exact `answer` command.
2. Edits `D`, only at text a listed row names.
3. Writes `L/inputs/c1-answers.json` (per row: `fixed` with a `new_anchor` quote of the changed sentence, or `deleted: true`, or `not-fixed` with a reason) and runs `answer --ledger L --input L/inputs/c1-answers.json`. The script diffs `snapshots/r1.md` against `D`, attributes each changed hunk to the row whose new anchor lies in it, lists `unattributed` hunks, records bytes before and after, and moves answered rows to `fixed`. Re-running `answer` before the next `begin` replaces the cycle's answers (idempotent).

**Review 2 (VERIFY).** Who: a fresh `/sc:spec-panel-ledger` session.
1. Run `begin --ledger L --doc D`. The script checks the integrity hash, that the prior report's last line equals the recorded verdict (`E-REPORT-EDITED`), that the round stays within 3 (`E-CAP`), copies `D` to `snapshots/r2.md`, diffs it against `r1.md`, and writes `L/plan-r2.md`: for each blocking row in `open|fixed|reopened` the frozen severity, wrong outcome, old anchor and attributed hunks (old and new text); each `verified` row whose stored span a hunk touched; and the unattributed hunks. If the reviser never ran `answer`, every hunk is unattributed and the plan says `W-NO-ANSWERS`.
2. The verifier reads the plan and, as needed, the document around each hunk. For every plan row it answers two questions: is the named wrong outcome gone (`resolved|open|regressed`), and did the change break the sentence it touched. Then it runs one bounded new-defect check over the changed hunks only.
3. Writes `L/inputs/r2-verify.json` and runs `verify --ledger L --input ...`. The script refuses a missing plan row (`E-INCOMPLETE`), a new row whose anchor is outside a round-2 hunk (`E-OUT-OF-SCOPE`), a severity field on an existing id (`E-FROZEN`), and an evidence quote absent from `r2.md` (`E-ANCHOR`). New rows get `origin=fix-induced` and `caused_by=<row id>|unattributed`, computed from hunk attribution.
4. Writes report `R2` (header `review: 2 of 3`, the per-row table, the new rows) and runs `close`. On CONTINUE the script writes the Reviser brief; on PASS or ESCALATE it first requires the final sweep.

**Revise 2.** Same as revise 1 with `c2-answers.json`; diff base `snapshots/r2.md`.

**Review 3 (VERIFY, then FINAL SWEEP).** Who: a fresh `/sc:spec-panel-ledger` session.
1. `begin` (snapshot `r3.md`, plan `plan-r3.md`), verify as in review 2, `verify`.
2. The decision at review 3 is always final (PASS or ESCALATE). The same session then runs the final sweep: one whole-document critique of `r3.md`, written to `L/inputs/sweep.json` and ingested by `sweep --ledger L --input ...`. Every sweep row is `deferred` with `round_found=sweep`; the script matches each against existing anchors (`dup_of=<id>`). Sweep rows never change the verdict.
3. `close --report R3` refuses without a sweep (`E-SWEEP-MISSING`); it appends the ledger summary, the line `sweep: <b> blocking, <m> minor reported, not looped` and the computed verdict. At ESCALATE the report lists the open blocking rows for the user and carries no Reviser brief.

If the decision becomes final earlier (PASS at review 2, or the no-progress ESCALATE of section 4), the sweep runs in that session instead. Exactly one sweep happens per loop: `close` requires it on a final decision, and `sweep` refuses a second call (`E-SWEEP-DONE`) or a non-final decision (`E-NOT-FINAL`).

## 3. Ledger file

**Location.** Default `L = <dir of D>/<stem of D>.review-ledger/`, overridable with `--ledger <dir>`. For S1: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger/`. Why this path:
- It is derivable from the document path alone, so every session (reviewer, reviser, a resumed coordinator) finds the same ledger without being told; 427 depends on the coordinator keeping the prior-findings file and the saved copy, and drops to a first review without them (`docs/designs/spec-panel-review-loop.md:162`). Here `init` refuses when a ledger exists.
- It sits next to the document, so it has the same tracking state: a `.dev/` document's ledger is under `.dev/` and is staged with it; it never lands in `~/.claude/` or `/tmp`, which do not survive across sessions or machines.
- It holds its own baselines (`snapshots/`), so no git ref is needed; 427 already rejected refs because "a ref fails on untracked or `.dev/` files" (`docs/designs/spec-panel-review-loop.md:50`).

**Layout.**

```text
<stem>.review-ledger/
  ledger.json            state; written only by review_ledger.py
  snapshots/r1.md r2.md r3.md   the text each review saw (sha256 in ledger.json)
  inputs/r1-find.json c1-answers.json r2-verify.json c2-answers.json r3-verify.json sweep.json
  plan-r2.md plan-r3.md  verify plans, written by begin, read by the verifier
```

**Format.** One JSON object, pretty-printed, schema version 1. JSON, not a markdown table, because anchor quotes hold pipes, backticks and quotes that break a table parser, and because only the script writes it. Keys reuse implement's finding-line vocabulary (`at`, `anchor`, `origin`, `resolved|open|regressed`, `src/superclaude/skills/sc-implement-protocol/refs/qa.md:137,143`) so adopters read one vocabulary. Example (3 rows, after review 2 of S1-like content; quotes shortened):

```json
{
  "schema": 1, "profile": "spec-panel", "doc": ".dev/orca-command-refactor/specs/orca-worker-contract-spec.md",
  "cap_reviews": 3, "round": 2, "phase": "closed",
  "snapshots": {"r1": {"sha256": "9f1c...", "bytes": 57763}, "r2": {"sha256": "4be0...", "bytes": 61210}},
  "decisions": [{"round": 1, "open_blocking": 6, "decision": "CONTINUE"},
                {"round": 2, "open_blocking": 1, "decision": "CONTINUE"}],
  "unattributed_hunks": {"c1": [{"new_lines": "112-112", "bytes_added": 96}]},
  "sweep": null,
  "rows": [
    {"id": "F01", "label": "N5", "round_found": 1, "origin": "new", "caused_by": null,
     "severity": "MAJOR", "rule": null, "blocking": true,
     "wrong_outcome": "AC-0.4 step 1 passes WC-1 with any launcher",
     "anchor": "step 1 proves WC-1 for the worker", "at": "r1:220",
     "status": "verified",
     "answers": [{"cycle": 1, "action": "fixed", "new_anchor": "counts step 1 as proof of WC-1 only when", "span": "r2:220-220", "hunks": ["r2:220-220"]}],
     "history": [{"round": 1, "actor": "reviewer", "to": "open"},
                 {"cycle": 1, "actor": "reviser", "from": "open", "to": "fixed"},
                 {"round": 2, "actor": "verifier", "from": "fixed", "to": "verified", "evidence": "otherwise \"WC-1 not exercised\"", "broke_sentence": false}]},
    {"id": "F07", "label": "N12", "round_found": 2, "origin": "fix-induced", "caused_by": "F01",
     "severity": "MAJOR", "rule": null, "blocking": true,
     "wrong_outcome": "correct launcher runs are recorded WC-1 not exercised",
     "anchor": "appears in that worker's `worker-read` output", "at": "r2:220",
     "status": "open", "answers": [],
     "history": [{"round": 2, "actor": "verifier", "to": "open", "hunk": "r2:220-220"}]},
    {"id": "F03", "label": "N9", "round_found": 1, "origin": "new", "caused_by": null,
     "severity": "MINOR", "rule": null, "blocking": false,
     "wrong_outcome": null,
     "anchor": "uses the same output location", "at": "r1:62",
     "status": "deferred", "answers": [],
     "history": [{"round": 1, "actor": "script", "to": "deferred", "reason": "non-blocking under profile spec-panel"}]}
  ],
  "body_sha256": "c41e..."
}
```

**Computed fields.** `blocking` comes from the profile, never from the model. Profile `spec-panel` copies 427's grading (`src/superclaude/commands/spec-panel.md:259`): `blocking = severity == CRITICAL or rule in {FR-8, FR-9} or (severity == MAJOR and wrong_outcome is non-empty)`. `at`, `span`, `hunks`, `origin` and `caused_by` are computed from anchors and diffs, mirroring implement, where the parent, not the reviewer, writes `origin=` (`qa.md:141,150`).

**Frozen at creation (review 1 for found rows, the creating round for fix-induced rows):** `id`, `label`, `round_found`, `origin`, `caused_by`, `severity`, `rule`, `wrong_outcome`, `blocking`, `anchor`, `at`. Any later input that carries one of these keys for an existing id is refused (`E-FROZEN`, exit 2). There is no regrade subcommand; a wrong grade goes to the user at escalation. This is what stops upward drift: the R2 and R3 verifier never sees a severity field it may set for an existing row.

**Anchor rules (script-checked).** The quote is whitespace-normalized (`" ".join(text.split())`, the same flatten the 427 tests use, `docs/designs/spec-panel-review-loop.md:126`), must be at least 12 characters, and must occur exactly once in the snapshot (`E-ANCHOR` if absent, `E-ANCHOR-AMBIGUOUS` if repeated). The script maps the match back to a line span.

**Changed lines.** `difflib.SequenceMatcher` over whitespace-normalized lines of the two snapshots, giving hunks as new-file line ranges. This matches 427's "ignoring whitespace-only changes" (`spec-panel.md:262`) and what the flg-r2 R3 reviewer did by hand with `git diff --no-index -w -U0` (`spec-panel-round3.md:25`), with no git dependency. A hunk is attributed to a row when the row's answer span overlaps it; a hunk no answer covers is `unattributed`.

**Status transitions.** The script is the only writer; the actor column says whose input file may request the move, which the script infers from the subcommand.

| From | To | Requested by (subcommand) | Script check; refusal |
|---|---|---|---|
| (none) | `open` | reviewer (`find`, round 1) or verifier (`verify` new row, rounds 2-3) | anchor present and unique; profile says blocking; a verify-time row must anchor inside a hunk of this round, else `E-OUT-OF-SCOPE` |
| (none) | `deferred` | script (`find`, `verify`, `sweep`) | profile says non-blocking, or the row came from `sweep` |
| `open`, `reopened` | `fixed` | reviser (`answer` action `fixed`) | row is blocking and in this cycle's brief; `new_anchor` present in the current `D`, or `deleted: true` and the old anchor absent from `D`; else `E-ANCHOR` |
| `open`, `reopened` | unchanged | reviser (`answer` action `not-fixed`) | non-empty reason |
| `open`, `fixed`, `reopened` | `verified` | verifier (`verify` result `resolved`) | evidence quote present in the new snapshot; `broke_sentence` given |
| `fixed`, `reopened` | `reopened` | verifier (`verify` result `open`) | reason plus a quote present in the new snapshot |
| `verified` | `reopened` | verifier (`verify` result `regressed`) | the row's stored span overlaps a hunk of this round, else `E-NOT-CHANGED` (accepted text cannot be re-attacked) |
| `deferred` | any | nobody | `E-ILLEGAL` (also refuses `answer` on a deferred row, which blocks reviser scope creep on minors) |
| any | any, with a frozen key | nobody | `E-FROZEN` |
| any | any, after `close` of round 3 or a final decision | nobody | `E-DONE` |

Phase order is also enforced: `answer` only while `phase=closed` with decision CONTINUE; `verify` only after `begin` of that round; `begin` refuses a second call for the same round. Refusals are atomic: exit 2, one line `refused <code>: <row id>: <detail>`, ledger untouched.

**Integrity.** `body_sha256` is the sha256 of the canonical JSON without that key. Any call that finds a mismatch stops with exit 3 `E-TAMPERED`. This detects hand edits by a model; it is not a security boundary.

## 4. Termination rule

Computed by the script after `find` (k = 1) or `verify` (k = 2, 3), and stored in `decisions`:

```text
B(k) = count of rows with blocking = true and status in {open, fixed, reopened}
       (includes fix-induced rows created at review k; excludes deferred and sweep rows)

decision(k) = PASS       if B(k) = 0
              ESCALATE   if B(k) > 0 and k = 3
              ESCALATE   if B(k) > 0 and k = 2 and B(2) >= B(1)      (no progress)
              CONTINUE   otherwise                                    (B(k) > 0, k < 3, and k = 1 or B(k) < B(k-1))

verdict line = "verdict: PASS" if decision = PASS, else "verdict: FAIL"
```

- The verdict is the script's output, appended by `close`; the reviewer never writes it. The next `begin` refuses if the prior report's last line differs (`E-REPORT-EDITED`). Implement already says "the orchestrator computes it" (`qa.md:334`); here a script does.
- The no-progress branch is rf-qa's `|F_{n+1}| < |F_n|` rule (`src/superclaude/agents/rf-qa.md:401`) made mechanical, on blocking rows only. It differs from the 427 design, which chose no second stop (`docs/designs/spec-panel-review-loop.md:154`); with only one cycle left, a cycle that did not shrink the blocking count is unlikely to clear it. It is listed as an open question (section 12) because it changes what "R3" means in the measurement (section 9).
- **Cap text.** The command's cap bullet carries `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` verbatim and the at-cap clause `HALT and escalate to the user with the open blocking findings` (`tests/skills/test_review_severity_rule.py:215-219`). The script constant `CAP_REVIEWS = 3` implements it: `begin` refuses a fourth review (`E-CAP`), and `answer` refuses a third cycle. A test pins that the constant and the text agree.
- **The final sweep is inside review 3's session and outside the count of fix cycles.** It is not a fourth review: it adds no session, cannot open a cycle, and cannot change the verdict. The loop still has exactly 3 reviews and at most 2 fix cycles. A sweep that finds a blocking defect reports it to the user under `sweep:` next to the verdict.

## 5. Difference from PR 427 `--re-review --baseline`

427's re-review is still a review of the changed document: the reviewer reads the whole revised spec and the prior report, re-derives a resolution table in prose, then searches for findings on changed lines and may record `origin=unchanged` findings anywhere as minor notes (`spec-panel.md:262`); it re-grades every finding it writes, writes its own verdict, and relies on a coordinator-kept baseline and count (`spec-panel.md:261`). The ledger removes, concretely:

| 427 re-review (reviews 2 and 3) | Ledger verify (reviews 2 and 3) |
|---|---|
| Reviewer re-reads the prior report and rebuilds the status table | Script hands the verifier a plan: per row, frozen severity, wrong outcome, old and new text of the attributed hunks |
| Severity of carried findings re-stated each round (drift possible) | Severity frozen; any severity key on an existing id refused |
| New findings anywhere, tagged `origin=unchanged` as notes | New rows only inside this round's hunks; anything else refused (`E-OUT-OF-SCOPE`); a whole-document look happens once, in the final sweep |
| `origin=` tag written by the reviewer | `origin` and `caused_by` computed from hunk attribution |
| `verdict:` line written by the reviewer | Verdict computed and appended by the script; edits detected |
| Coordinator keeps baseline copy and review count | Script snapshots each review and keeps the round; a missing flag cannot restart a first review |
| Reviser told in prose which findings to fix | Script refuses answers on deferred (minor) rows; unattributed hunks listed in the next plan and the report |
| Reviser reports byte size before and after | Script records bytes per snapshot and per hunk |

What it keeps from 427: the grading rule (now the `spec-panel` profile), the `review: N of 3` header, the cap text, the Reviser brief delivered in the report, critique-mode only, no Improve step, and the Precedence bullet.

## 6. Exact changes, file by file

| Group | File | Change |
|---|---|---|
| Command | `src/superclaude/commands/spec-panel-ledger.md` (new; installed to `~/.claude/commands/sc/spec-panel-ledger.md` because the installer copies every `*.md` except `README.md`, `src/superclaude/cli/install_commands.py:11,40`) | Copy of `spec-panel.md` with three blocks replaced (below) |
| Skill | `src/superclaude/skills/sc-review-ledger/SKILL.md` (new) | Contract: roles, layout, schemas, CLI, profiles, adoption seam |
| Script | `src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py` (new; reaches `~/.claude/skills/sc-review-ledger/scripts/` because install copies the whole skill folder, `src/superclaude/cli/install_skill.py:52`) | Ledger kernel, standard library only (`json`, `difflib`, `hashlib`, `argparse`, `pathlib`) |
| Test | `tests/skills/test_review_ledger_script.py` (new) | Behaviour tests of the kernel |
| Test | `tests/skills/test_spec_panel_ledger_command.py` (new) | Text and parity tests of the command |
| Test | `tests/unit/test_cli_install.py` | Add `spec-panel-ledger.md` to the `commands` baseline (`:111-121`) and the two skill files to the `skills` baseline (`:187`); the check is presence-only (`:501-505`), so nothing else breaks |
| Design | `docs/designs/spec-panel-ledger.md` (new) | This design, plus "how to add a profile" |
| Not changed | `src/superclaude/commands/spec-panel.md`, its plugin copy, `HOW-WE-WORK.md` | Additive until S1 proves it; the plugin parity test mirrors only four commands (`tests/commands/test_routing_plugin_parity.py:41-47`), so no plugin copy is required |

**Command file outline (`spec-panel-ledger.md`).** Byte-identical to `spec-panel.md` except:
1. Frontmatter `name: spec-panel-ledger` and a description ending "with a script-kept finding ledger (find once, then verify)".
2. Usage line 1 (`spec-panel.md:22`): `[--re-review <prior-findings-file> --baseline <saved-copy>]` replaced by `[--ledger <dir>]`.
3. `## Review Loop` (`spec-panel.md:256-264`) replaced by `## Ledger Loop`, one line per bullet (as 427 does, so line-based matchers see each bullet whole, `docs/designs/spec-panel-review-loop.md:54`):
   1. **Setup**: applies to `--mode critique` only; before any other step invoke `Skill sc-review-ledger` and run every ledger step as `uv run --no-project python "<skill base>/scripts/review_ledger.py"`; ledger dir is `--ledger` or `<doc dir>/<doc stem>.review-ledger/`; if `ledger.json` exists run `begin`, else `init`; a refused call is reported and stops the run, and never falls back to a first review.
   2. **Grading**: 427 bullet 2 verbatim, plus: severity, rule and wrong outcome are written once, when a row is created, and never restated.
   3. **Find (review 1)**: full-document critique; every finding goes into `inputs/r1-find.json` with an exact anchor quote; run `find`.
   4. **Verify (reviews 2 and 3)**: read `plan-r<k>.md`; for each plan row answer `resolved|open|regressed` with an evidence quote and whether the change broke the sentence it touched; do not grade unchanged text.
   5. **Changed-line check**: one pass over this round's hunks only; each new defect is a row anchored inside a hunk; run `verify` once with all answers.
   6. **Final sweep**: when the decision printed by `verify` is PASS or ESCALATE, run one whole-document critique, write `inputs/sweep.json`, run `sweep`; its findings are reported, not looped.
   7. **Verdict**: run `close --report <report>`; the script appends the summary, any Reviser brief and the last line `verdict: PASS|FAIL`; do not write or edit those lines.
   8. **Cap**: the canonical cap text and at-cap clause verbatim; header `review: N of 3` with N from `init`/`begin` output; every run is one review whatever `--iterations` says; skip the Improve step and write no revised specification.
   9. **Reviser contract**: the script-written Reviser brief lists only open blocking row ids with the exact `answer` command; revise only text a listed row names; add no rule, mechanism or section no listed row calls for; answer every listed row, then run `answer`.
   10. **Precedence**: 427 bullet 7, with "the changed lines and the prior blocking findings" read as "this round's hunks and the ledger's blocking rows".

**Script CLI (`review_ledger.py`).** Common flag `--ledger <dir>` (or `--doc` to derive it). Output: line 1 `ok <subcommand>` or `refused <code>: <detail>`, then `key: value` lines. Exit codes: 0 ok; 1 usage error; 2 input refused (row level: `E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`, `E-FROZEN`, `E-ILLEGAL`, `E-INCOMPLETE`, `E-OUT-OF-SCOPE`, `E-NOT-CHANGED`, `E-SCHEMA`); 3 state refused (`E-EXISTS`, `E-MISSING`, `E-TAMPERED`, `E-PHASE`, `E-CAP`, `E-DONE`, `E-REPORT-EDITED`, `E-HEADER`, `E-SWEEP-MISSING`, `E-SWEEP-DONE`, `E-NOT-FINAL`).

| Subcommand | Inputs | Writes | Prints | Main checks |
|---|---|---|---|---|
| `init --doc D --profile P` | document | `ledger.json`, `snapshots/r1.md` | `review: 1 of 3`, ledger path | profile known; no existing ledger |
| `find --input F` | `r1-find.json` | rows | counts, decision preview | round 1, phase find; schema; anchors; blocking from profile |
| `answer --input F` | `c<n>-answers.json`, current `D` | answers, hunks, bytes | per-row result, unattributed hunks, bytes before and after | phase closed with CONTINUE; listed rows only; anchor or deletion proven; cycle within cap |
| `begin --doc D` | current `D`, prior report | `snapshots/r<k>.md`, `plan-r<k>.md` | `review: k of 3`, plan path | integrity; prior verdict line; round within cap; one begin per round |
| `verify --input F` | `r<k>-verify.json` | transitions, new rows | counts, decision preview | every plan row answered once; quotes present; new rows inside hunks; no frozen keys; `regressed` only on touched spans |
| `sweep --input F` | `sweep.json` | sweep rows (`deferred`) | blocking and minor counts, duplicates | decision final; once per loop; anchors present in the last snapshot |
| `close --report R` | report | `decisions`, report tail | decision, verdict line | header `review: k of 3` present; sweep present when final and k > 1 |
| `status [--json]` | ledger | nothing | the metrics of section 9 | integrity |

Input schemas are versioned (`"schema": 1`) and documented in `SKILL.md`. Extension seam: a `PROFILES` table in the script maps a profile name to its severity vocabulary, its blocking predicate and its cap; this change ships only `spec-panel`. Adding an adopter is one table entry plus one parametrized test row, never a change to the transitions or the decision formula.

**Tests.**
- `test_review_ledger_script.py` (loads the script by path, runs it in `tmp_path`): `init` refuses an existing ledger; `find` is atomic on one bad anchor; blocking per profile for CRITICAL, FR-8, MAJOR with and without wrong outcome, MINOR; `E-FROZEN` on a severity key; `answer` refuses a deferred row; an edit outside every answer span is listed unattributed; `verify` refuses a missing plan row and a new row outside the hunks; `regressed` refused on an untouched span; the decision formula over a table of (k, B(k-1), B(k)) covering all four branches; `begin` refuses round 4; `close` refuses a final decision without a sweep; `sweep` refused on CONTINUE and on a second call; a hand edit of `ledger.json` gives `E-TAMPERED`; an edited verdict line gives `E-REPORT-EDITED`; `CAP_REVIEWS == 3`.
- `test_spec_panel_ledger_command.py`: the file equals `spec-panel.md` outside the three replaced blocks (drift guard: any edit to `spec-panel.md` fails this test until mirrored); ten one-line bullets in order; `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]`, imported from `tests.skills.test_review_severity_rule`, are present; `Skill sc-review-ledger` and `<skill base>/scripts/review_ledger.py` present; no `src/superclaude` inside the section.
- Keep green, unedited: `tests/skills/test_review_severity_rule.py` (it scans all of `src/`, so the new text must avoid its banned phrases and old-cap patterns, `:112-125,288-292`), `tests/skills/test_spec_panel_review_loop.py`, `tests/skills/test_primitive_dual_surface_lookup.py`.

## 7. Adoption by `/sc:reflect`, rf-qa and the `/sc:implement` final review

Every adopter reuses the kernel and the contract unchanged and adds only a profile row and a short adapter section. No adopter is changed by this design; each is a later, separate change gated on the S1 result.

| Adopter | What it would need | What stays different |
|---|---|---|
| `/sc:reflect` | A `--ledger <dir>` flag; rows created only from items that survive the evidence-validator gate (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:42`); a `reflect` profile mapping its deviation taxonomy (Authorized expansion, Necessary deviation, Drift, Regression) to blocking. Which classes block is UNVERIFIED: I did not read the reflect grading text. | Reflect has no loop counter of its own; its caller drives the loop (`enrichment/codebase-context.md` section 4). The Tier 2 ensemble and adversarial merge stay; they feed `find` once. Verify rounds can run as Tier 1 only, a cost saving. |
| rf-qa agents | A `rf-qa` profile (CRITICAL and IMPORTANT block, MINOR does not, `src/superclaude/agents/rf-qa.md:387,391`); the Fix Cycle steps 1-5 (`:386-396`) become `begin`, `verify`, `close`; the prose monotonicity halt (`:401`) becomes the computed no-progress branch, and `[HALT-MONOTONICITY] |F|=<n>` is printed from `B(k)`. | rf-qa may fix in place when authorized, so one agent is both reviser and verifier; the script records the actor by subcommand but cannot prove two sessions. The S1-S3 copies in `rf-qa.md` are pinned verbatim (`tests/skills/test_review_severity_rule.py:181-182`), so the adapter goes in a new section, never between them. Regression detection (`rf-qa.md:407-412`) maps to the `verified -> reopened` transition. |
| `/sc:implement` final review | Nothing for FINAL. Per-task re-reviews (A2 to A5) could store their finding lines as ledger rows, since the keys already match (`qa.md:137,143`). | FINAL is one fresh full audit per archive attempt against the real files (`managed-workspace.md:55`): it already plays the role of the single final sweep and must stay a full audit. Implement keeps its own retry ladder and cap, which the pin tests exempt (`test_review_severity_rule.py:320-325`), and its inherited-text cap (`qa.md:166`). |

## 8. Stateful single reviewer session vs file ledger

| Criterion | One stateful reviewer session across rounds | File ledger (this design) |
|---|---|---|
| Survives crash, compaction, a new worker | No: the state lives in one context; Orca workers in S1 are fresh per step | Yes: on disk next to the document |
| Mechanical checks (frozen severity, scope, verdict) | None; all prose | Script-enforced |
| Independence of the verify pass | Low: the same context that missed a defect re-checks its own findings | Any fresh session or model can verify |
| Fits S1 without changing briefs | No: S1 dispatches a new worker per review (`DECISIONS.md:59`) | Yes: one-line name change plus the ledger path |
| Reuse by reflect, rf-qa, implement | Each needs session plumbing | Same kernel, new profile row |
| Cost | Fewer tool calls; context grows each round | About 4 extra script calls per review (section 11) |
| Severity drift | Still possible (the model restates grades) | Refused (`E-FROZEN`) |

Recommendation: the file ledger. A stateful session buys only lower call count, and loses durability, independence and every mechanical check. A team that wants continuity can still resume a reviewer session and point it at the same ledger; the ledger does not forbid that.

## 9. Measurement plan on S1

**Setup.** Same as Arm B (`DECISIONS.md:59-62`): scenario S1, base commit 2cb683f5, verbatim briefs, model claude-opus-5-5, two fresh worktrees, `WORKER-CONTRACT.md` moved aside. The variant installs as an additive name in `~/.claude/commands/sc/` plus the skill in `~/.claude/skills/sc-review-ledger/`, so `spec-panel.md` is untouched (machine fact D9, `DECISIONS.md:46`; `AB-REPORT.md:47`). Brief change, recorded per brief: `/sc:spec-panel` becomes `/sc:spec-panel-ledger --ledger .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger`, in the three review briefs only. No `--re-review` or `--baseline`. Revise briefs are unchanged (the reviser reads the report's script-written Reviser brief). Comparators: control ctl-r1/ctl-r2 and Arm B flg-r1/flg-r2, reused.

**Validity checks (new, mechanical).** V1-ledger: `ledger.json` shows rounds 1 to 3 (or an earlier final decision), three snapshots, a sweep record, and no `E-TAMPERED` in the session logs; a replicate whose reviewers never ran the script counts as "ledger not honoured" and is not treatment. Count script refusals per session as a covariate.

**Metrics (D5 M1-M5, `DECISIONS.md:23`), read from `status --json`.**
- M1 rounds to the final decision; M2 blocking rows `B(k)` per round; M3 share of new rows with `origin=fix-induced` (computed, no longer a reviewer tag); M4 bytes of each snapshot and growth after two cycles; M5 tool calls per session. Plus: unattributed hunk bytes per cycle, sweep blocking count.
- **"Review 3 critical+major" in a ledger loop** = (a) ledger rows with severity CRITICAL or MAJOR and status `open|fixed|reopened` after review 3's verify (carried and fix-induced), plus (b) sweep rows with severity CRITICAL or MAJOR that are not `dup_of` a row already counted in (a). Sweep rows that duplicate a `deferred` or `verified` row count, with the frozen severity of the matched row. Reason: the control's R3 number is what a whole-document look at review 3 reports; counting the ledger alone would let the ledger win by not looking. If the loop ends early (PASS or no-progress ESCALATE at review 2), the same count is taken at that review. The ledger-only part (a) is reported as a secondary number.

**Predictions (n=2, a screen only).**

| Metric | Control mean | Arm B mean | Ledger predicted | Bar |
|---|---|---|---|---|
| R3 critical+major (a)+(b) | 6.0 | 3.5 | 2.5 (range 1 to 4): (a) 0 to 1, (b) 1 to 3 | <= 3 |
| R3 ledger-only (a) | n/a | n/a | 0.5 | none |
| Growth after 2 cycles | 63.5% | 30.0% | 18% (range 12% to 26%) | <= 44.4% |
| Clean PASS within 3 reviews | 0 of 2 | 0 of 2 | 1 of 2 | none |

Basis: R1 blocking in Arm B was about 5 to 6 under 427 grading (the R2 proxy fell from 16-17 to 5-6, `ARMB-REPORT.md:13`); flg-r2 R3 had 1 blocking left, created by a fix (`ARMB-REPORT.md:14,31`). Growth drops below Arm B's 27.8% and 32.1% because the reviser can no longer apply the 9-of-15 minor rows it applied in flg-r2 (`disposition-round2.md:35`) and every unattributed hunk is surfaced.

**What would mean the idea failed.**
- R3 (a)+(b) mean above 3, or any ledger replicate not below every control replicate (the D11 rule, `DECISIONS.md:64`); in particular a mean of 3.5 or more means the ledger adds nothing over Arm B.
- (b) alone at 4 or more: a verify-only middle hides defects that the end-of-loop sweep then finds, so the loop only moved them.
- M3 fix-induced share still at or above 80% with `B(2) >= B(1)/2`: fixes keep creating blockers and the ledger did not change that.
- V1-ledger failing in either replicate: the mechanism is not followed in practice.

## 10. Measured causes removed and left

| Measured cause | Effect of the ledger | How |
|---|---|---|
| Fresh whole-document re-review after each fix finds new defects (89%/100% on changed lines, `AB-REPORT.md:30`) | Removed for reviews 2 and 3; moved to one final sweep that cannot loop | `E-OUT-OF-SCOPE` on new rows outside hunks |
| Fix-induced defects on changed lines (N12) | Reduced, not removed. Fewer and smaller edits mean fewer chances; each is attributed (`caused_by`) and still blocks at review 2; at review 3 it escalates | Answer spans, hunk attribution, refusal of answers on deferred rows |
| Severity drift between rounds | Removed for existing rows; new rows are graded once by the profile | `E-FROZEN`, profile-computed `blocking` |
| Reviser applies minor findings and fixes "related defects" (`disposition-round2.md:13`) | Minor rows: removed (refused). Unlisted related edits: detected and reported, not prevented | `E-ILLEGAL` on deferred rows; unattributed hunks in the plan and report |
| Reviser adds mechanisms | Left as prose (bullet 9); visible as bytes per hunk and unattributed hunks | Measured only |
| No mechanical stop; verdict and count in prose (`spec-panel-review-loop.md:143,162`) | Removed | Computed decision, `E-CAP`, `E-REPORT-EDITED`, script-kept snapshots |
| Brief says "any finding of any severity is FAIL" (`spec-panel-round3.md:15`) | Removed for the verdict line, which the script writes; the report prose may still echo the brief | `close` appends the verdict |

## 11. Risks and costs

**Costs per loop (estimates, UNVERIFIED until measured as M5).**
- Tool calls: review 1 about +4 (Skill, `init`, Write input, `find`, `close`); reviews 2 and 3 about +5 each (`begin`, Read plan, Write input, `verify`, `close`), plus +2 for the sweep (Write, `sweep`); each revise +2 (Write answers, `answer`). Total about +20 per loop, plus any retries after refusals.
- Sessions: none added; the sweep runs inside the last review session.
- Wall time: each script call is under a second on a 60 to 90 KB document (difflib on a few hundred lines). The sweep adds one whole-document critique to the last session, roughly the length of a review 1 pass (UNVERIFIED; no per-step timing in the reports I read). Verify passes should be shorter than 427 re-reviews, which re-read everything.
- Maintenance: one copied command kept in step by a parity test, one script with its own tests.

**Ways it could make the loop worse.**
1. Verify-only middle hides real defects that review 1 missed in unchanged text; the sweep finds them only at the end, with no cycle left. Mitigation: the sweep's blocking count is printed next to the verdict, and the measurement counts it (section 9). Residual: a PASS can stand next to `sweep: 2 blocking`; the user decides.
2. Review 1 under-finds or mis-grades; frozen severity then locks the error (a real blocker graded MINOR is deferred forever). Mitigation: the sweep reports its own grade for a duplicate next to the frozen one. Residual: no in-loop correction.
3. Anchor brittleness: a reviser rewrite leaves no quotable new anchor, or a short phrase is ambiguous; refusals cost calls and may stall an unattended reviser. Mitigation: `deleted: true`, the uniqueness error names a longer quote to use, re-runnable `answer`.
4. A model hand-edits `ledger.json` or skips the script. Detected (`E-TAMPERED`, `E-REPORT-EDITED`, `W-NO-ANSWERS`, V1-ledger), never silently accepted; but a detected break stops the loop and escalates early.
5. The no-progress branch escalates at review 2 a loop that review 3 might have cleared.
6. Moved paragraphs diff as delete plus insert, widening the hunk scope and the new-row surface.
7. Two kinds of state (report prose and ledger) can disagree in prose; the ledger wins for the verdict, but a reader may trust the prose table.

**Rule classification.**

| Rule | Kind | Residual risk of prose rules |
|---|---|---|
| One ledger per document; no restart of a first review | MECHANICAL (`E-EXISTS`) | |
| Snapshots and round count kept by the script | MECHANICAL | |
| Anchors present and unique | MECHANICAL | |
| `blocking` computed from severity, rule and wrong outcome | MECHANICAL | |
| The severity a reviewer chooses at creation is honest | PROSE | the grade itself is still model judgement; the rule only stops it changing |
| Severity frozen | MECHANICAL (`E-FROZEN`) | |
| Reviser answers only listed blocking rows | MECHANICAL (`E-ILLEGAL`) | |
| Reviser edits only text a listed row names; adds no mechanism | PROSE, detected | unattributed hunks are reported, not refused; text added inside an attributed hunk is invisible to the check |
| Reviser runs `answer` at all | PROSE, detected (`W-NO-ANSWERS`) | rows then verify with no attribution and `caused_by=unattributed` |
| Every plan row verified | MECHANICAL (`E-INCOMPLETE`) | |
| The verifier's resolved/open judgement is correct | PROSE | a lazy verifier can mark `resolved` with any present quote |
| New rows only on changed hunks | MECHANICAL (`E-OUT-OF-SCOPE`) | |
| The verifier actually looks for new defects on the hunks | PROSE | an empty new-row list is always accepted |
| `regressed` only on touched spans | MECHANICAL (`E-NOT-CHANGED`) | |
| Verdict computed and appended | MECHANICAL | |
| Report verdict not edited | MECHANICAL at the next `begin`; at review 3 only by a final `status` check | the last report could be edited after `close` without detection unless a coordinator runs `status` |
| Cap of 3 reviews, 2 cycles | MECHANICAL (`E-CAP`) | |
| Exactly one final sweep | MECHANICAL (`E-SWEEP-MISSING`, `E-SWEEP-DONE`) | |
| The sweep is a real whole-document look | PROSE | a thin sweep makes (b) look small; compare its finding count with review 1 |
| Reviewer, reviser and verifier are different sessions | PROSE | the script knows the subcommand, not the session |
| Invoke the skill and use the script at all | PROSE, detected at the next step | |

## 12. Open questions

1. Keep the no-progress ESCALATE at review 2, or follow the 427 design's single stop (`docs/designs/spec-panel-review-loop.md:154`)? It makes the loop shorter but changes what "R3" counts.
2. Should a fix-induced blocking row found at review 3 escalate (this design) or be reported like a sweep row? Escalating is honest; reporting would make PASS reachable more often.
3. Should the sweep run in a separate fresh session (better independence, one more session, changes the S1 briefs) instead of inside review 3?
4. Should unattributed hunks above a byte threshold refuse `answer` instead of being reported? A limit conflicts with FR-8/FR-9 gap filling (`spec-panel-review-loop.md:73`).
5. Who may regrade a frozen row: nobody (this design), or a user-only command recorded in the ledger?
6. Copy-plus-parity-test for the command, or a short command that points at `spec-panel.md` for the panel and overrides only the loop? The pointer avoids 480 duplicated lines but reads whatever `spec-panel.md` is installed, which the S1 experiments swap.
7. Is 12 normalized characters the right minimum anchor length on real reports?
8. Reflect's blocking classes for its profile (UNVERIFIED, section 7).
