# Design: `/sc:spec-panel-stoprule`, a computed stop rule for the spec-panel review loop (issue #346)

Status: experimental variant, built 2026-11-08. The existing `/sc:spec-panel` is not changed. Source: the stoprule SPEC (`.dev/brainstorms/346-stoprule/SPEC.md`), trimmed here to the final decision.

## 1. Problem

In the S1 scenario no arm of the spec-panel review loop reached PASS in three reviews, and review-3 critical+major counts stayed high (control 8 and 4). The verdict was the reviewer's own line, the 3-review cap was prose, the Boundary Table rules FR-8/FR-9 forced every GAP row to MAJOR, and revisers applied minor findings because nothing separated them from blocking ones. Nothing computed "blocking" or ended the loop.

## 2. Mechanism

The reviewer writes every finding as a machine-readable claim (verbatim quote plus a concrete wrong outcome) into a fenced ledger block inside its report. A standard-library script, `stoprule.py`, checks the quotes, applies a changed-line ratchet, sends each surviving claim to a blind `finding-grader` agent that sees only the quote, the outcome and a frozen rubric, and then computes `verdict: PASS|FAIL` itself and writes either a Reviser brief listing only confirmed blocking findings or, at review 3, a fixed-format escalation.

| Part | Installed at | Decides |
|---|---|---|
| Command `spec-panel-stoprule.md` | `~/.claude/commands/sc/` | the Arm B `spec-panel.md` with the Review Loop bullets 2-6 rewritten, bullet 8 added, FR-8/FR-9 no longer forcing MAJOR; activates the skill |
| Skill `sc-spec-panel-stoprule-protocol` | `~/.claude/skills/` | `SKILL.md` (steps S0-S10 and who runs each), `refs/rubric.md` (frozen rubric, sha256 prefix `dbc4926c7421`), `refs/canaries.json`, `scripts/stoprule.py` |
| Script `stoprule.py` | inside the skill | review count and cap, quote and citation read-back, ratchet, grade validation and merge, verdict, Reviser brief, escalation, tamper check, recorder counts |
| Agent `finding-grader` | `~/.claude/agents/` | the one judgement a script cannot make: does the stated outcome follow from the quoted text under the rubric (`model: sonnet`, `tools: Read`, writes nothing) |

### 2.1 Claim ledger

JSON lines in a ```` ```stoprule-ledger ```` block. The reviewer writes `claim` (id, reviewer label `claimed`, `quote`, `span`, `outcome`, `evidence`, `prior`, `sites`), `prior` (status of each prior blocking id) and `checked` (a changed hunk reviewed and found clean). Every other record is script-written: `begin`, `form`, `mark`, `uncovered`, `seal`, `grade-raw`, `grade-reject`, `grade`, `audit-raw`, `audit`, `final`, `verdict`, and a `chain` link after every script write. Final claim statuses: `confirmed`, `minor`, `late-found`, `minor-form`, `unconfirmed`, `confirmed-audit`. The reviewer's `claimed` label is never read by the verdict; it exists for the owner measure.

### 2.2 Steps

1. `begin`: review number N from the prior report's sentinel (1 without `--re-review`); a `--re-review` report with no valid sentinel exits 5; a prior review 3 exits 4 (prints the escalation, or "loop already ended" for a PASS); exits 5 when the prior report's recomputed verdict differs from its last line, the baseline hash differs from the prior `spec=`, or the rubric hash differs from the loop's review-1 hash. Opens the ledger with a random nonce and prints the rubric and the changed hunks.
2. Review: one `claim` per finding of any label, a `prior` line per prior blocking id, a `checked` line per clean changed hunk. A GAP or blank Boundary Table row is a candidate claim.
3. `seal`: quote is a unique normalised substring of the spec (20 non-space to 300 characters), outcome at least 8 words, `{path,line,text}` evidence read back under `--root` (`..` refused), `live` evidence unverified, every changed hunk covered. The first failure exits 3 once and records each claim's id, label and prior link; the second seal is final (still-failing claims become `minor-form`). Ratchet in reviews 2 and 3: a claim is `late-found` unless a quote line is a changed line or its `prior` is a valid link.
4. `grade-prep`: batches of at most 6 claims plus one blocking and one minor canary, seeded with sha256(nonce, review, seal) and renamed C1..Cn; frozen priors are never batched; no report, spec path, label or expert name.
5. Grader: one `finding-grader` Agent call per batch.
6. `apply-grades`: stores the reply verbatim with its sha256, validates it (one line per Cn, `blocking` boolean, `q2`, `why` at most 25 words, canaries right); one rerun, then the claims stay `unconfirmed`. A late-found claim keeps `late-found`.
7. PASS-time audit (`audit-prep`, one fresh general-purpose Agent call, `apply-audit`): only when nothing is confirmed and no prior is open; any `real:true` reinstates the claim (or an unclaimed hunk) as `confirmed-audit`.
8. `status`, then the prose.
9. `finalize`: refuses a hand-typed `verdict:` line; writes `## Computed result`, then the Reviser brief (reviews 1-2, FAIL; D1..Dk, priors after new claims; NONE for an `incomplete`-only FAIL), the `## Escalation to the user` (review 3, FAIL) or PASS with known debt, then the sentinel and `verdict: PASS|FAIL`. Verdict: FAIL `confirmed` on any confirmed claim (claims linked to one prior count once), `unresolved-prior` on any open frozen prior, `incomplete` on any unconfirmed claim, uncovered hunk or missing PASS-time audit; else PASS.
10. `check`: verifies the seal, the chain links, every `grade-raw` and `audit-raw` hash, re-derives grades, uncovered hunks, audit records, ratchet marks, final records and the verdict, and compares the computed block, sentinel and last line; exit 0 or 6.
11. Fix cycle: the coordinator re-runs `check` before the reviser, fills the reviser range with D1-Dk or NONE, and runs `check-disposition` after it.
12. Recorder: `verify-transcript` (each grader reply must sit whole in one Agent tool result of the session transcript), `count`, `audit-sample`.

Exit codes: 0 ok, 3 repairable once, 4 HALT at cap, 5 stop on bad input (usage errors included), 6 ledger tampered.

### 2.3 What is mechanical and what is prose

Mechanical (script): count and cap, frozen rubric, quote and citation read-back, ratchet, grade validation, verdict, Reviser brief, escalation, tamper evidence. Prose: running the steps at all, the grader being fresh, the reviser reading only the brief. The seal and chain are tamper evidence, not security: a session that recomputes the hashes is caught only by the recorder's transcript check, and a session that never calls the script has no sentinel, which `check` reports as non-compliant.

## 3. Files

| File | Installed to |
|---|---|
| `src/superclaude/commands/spec-panel-stoprule.md` | `~/.claude/commands/sc/spec-panel-stoprule.md` |
| `src/superclaude/skills/sc-spec-panel-stoprule-protocol/` (`SKILL.md`, `refs/rubric.md`, `refs/canaries.json`, `scripts/stoprule.py`) | `~/.claude/skills/sc-spec-panel-stoprule-protocol/` |
| `src/superclaude/agents/finding-grader.md` | `~/.claude/agents/finding-grader.md` |
| `tests/skills/test_stoprule_script.py`, `tests/skills/test_spec_panel_stoprule.py`, `tests/skills/fixtures/stoprule/` | not installed |

The skill name ends in `-protocol` so `install_skills` installs it standalone. No routing-guide row, `/sc:help` entry or plugin mirror while the variant is experimental. `tests/recommend/test_routing_refresh.py` lists `spec-panel-stoprule` in `_POST_REFRESH_ADDITIONS`.

## 4. Names and install

Command `spec-panel-stoprule` (`/sc:spec-panel-stoprule`), skill `sc-spec-panel-stoprule-protocol`, agent `finding-grader`. Briefs switch to the variant with `perl -pe 's#(/?sc:spec-panel)(?![-\w])#$1-stoprule#g' brief.md > brief.stoprule.md`. The experiment install copies the agent, the skill and the command (in that order) with `test ! -e` guards and checks that the installed `spec-panel.md` is unchanged; `uv run superclaude install` without `--force` is the repo route, and `--force` is never used on the experiment machine. The step-by-step install note is `.dev/brainstorms/346-stoprule/INSTALL.md`.

## 5. Owner decisions (2026-11-08)

- **Base file.** The variant is the 472-line Arm B `spec-panel.md` (sha256 prefix `c8d80346a96c`) plus this design's edits. That file is the current `src/superclaude/commands/spec-panel.md` without its `## Unattended mode` section and without two more lines (the second Usage line advertising `--unattended` and the sentence explaining `--target-release`). So the variant has no `## Unattended mode` section and does not accept `--unattended`, and there is no separate measurement copy: the repo copy is the installed copy. A byte-identical copy of the base, `tests/skills/fixtures/stoprule/spec-panel-armb-base.md`, pins it, and the static test fails on any drift from it outside the replaced blocks.
- **Deferred, demoted and withdrawn findings stay counted.** A critical or major (reviewer label) new finding that ends `late-found`, `minor`, `minor-form` or `unconfirmed`, or that was dropped from the ledger between the first and second `seal`, stays in the review-3 critical+major count. `stoprule.py count` reports it as `m0_label_cm` (all such new findings, carried priors excluded), `m0_deferred_cm` (the part not confirmed) and `m1_open_confirmed` (the sentinel `confirmed=` plus open frozen priors, one defect counted once). `finalize` prints the same `m0_label_cm` value on its `label-count critical+major` line. This is reporting only and never changes the verdict.
- **Review-3 brief unchanged.** The S1 review-3 brief text stays verbatim, including "any finding of any severity is FAIL"; the command-name substitution and the Arm B `--re-review`/`--baseline` clause are the variant mechanism, not an edit. The reviewer may record that rule on a `brief-verdict:` line; the sentinel carries `brief=`.
- **No ablation arm.** `spec-panel-stoprule-noscript` is not built.
- **Read-only script calls in review sessions.** Reviewer and reviser sessions run only calls that write no file (`--dry-run` calls, `grade-prep`, `audit-prep`, `status`, `verdict`, `check`). `begin`, `seal`, `apply-grades`, `apply-audit` and `finalize` are coordinator steps. Every subcommand accepts `--dry-run`, which writes nothing, and the tests prove it by comparing every fixture file before and after.

## 6. Measured on the control-r1 replay

Replaying control r1's review 3 (8 blocking findings) against its spec v2 and v3 gives 8 anchored and 0 late-found, not the 5 and 3 the SPEC predicted: fix 2 rewrote every cited line. The fixture is `tests/skills/fixtures/stoprule/ctl-r1/`.

## 7. Open items

Whether the recorder can read a worker transcript in a stable format (else `grader-integrity: unverified`); whether the Agent tool honours `model:` inside an Orca worker (UNVERIFIED); the attribution question the ablation arm would answer. The grader, the canaries and the PASS-time audit are untested against a live model; only the script is tested.
