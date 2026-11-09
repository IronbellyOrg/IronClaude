# Variant 1 (architect): `/sc:spec-panel-stoprule`, a computed stop rule for the spec-panel review loop

Author lens: ARCHITECT (structure, dependencies, long-term impact). Instruction applied: maintainability and extension scaffolding.
Date: 2026-11-08. Builds on the PR 427 `## Review Loop` text as it stands in `src/superclaude/commands/spec-panel.md:256-264` (read 2026-11-08).

## 1 Problem and evidence

- On S1 (n=2 per arm) no run reached PASS in 3 reviews: R3 critical+major proxy control 8/4 (mean 6.0), 427 6/5, 427+flags 6/1 (mean 3.5); growth after 2 cycles 63.5% / 29.7% / 30.0% (`AB-REPORT.md`, `ARMB-REPORT.md`).
- 89% (R2) and 100% (R3) of new findings in 427 runs sit on lines the previous fix changed (`origin=changed`).
- Severity drifts up: control R3 graded every Boundary-Table GAP MAJOR under FR-8 (`spec-panel.md:328`) and resolved two minor-vs-MAJOR disagreements to MAJOR; R3-8 was "present in the round-2 input, not flagged then" and still blocked.
- Arm B revisers applied 15 of 15 findings, 9 of them minor, because the brief said "apply confirmed findings" and nothing defined "confirmed".
- The verdict line and the cap are prose the reviewer writes and obeys (`spec-panel.md:260-261`; the design itself says "The tests prove the text is present").

## 2 Mechanism

### 2.1 Architecture in one picture

The design splits the loop into three roles with one owner each, so no role can both raise and decide a blocker:

| Role | Who | Writes | Never writes |
|---|---|---|---|
| Reviewer | the `/sc:spec-panel-stoprule` session (the panel) | report prose, `findings-r<N>.json` | severity outcome, origin, verdict, Reviser brief |
| Form + ratchet + verdict | `stoprule.py` (stdlib-only Python, no model) | `ledger-r<N>.json`, `cards-r<N>.md`, `verdict-r<N>.json`, the report's last 2 blocks, `escalation.md` | finding text |
| Second grader | `stoprule-grader` agent (fresh Task, `model: sonnet`, tools `Read` only) | one grade line per card | anything else |

All three live behind one companion skill, `sc-spec-panel-stoprule-protocol`, which the command activates. The command stays a near-copy of spec-panel; every new rule lives in the skill (rubric file, grader brief, script), so a later `/sc:reflect` or rf-qa variant reuses the skill without copying the panel (section 8).

Every step happens inside the one command invocation. The coordinator's brief is unchanged apart from the command name, so the experiment stays comparable (section 4).

### 2.2 Loop directory

The loop directory is `--report-dir <dir>` (an existing spec-panel flag, `spec-panel.md:23,456`). Without it, it is the directory of the `--re-review` file; for a first review without either, the skill uses `./.dev/spec-panel-stoprule/<spec file stem>/` and prints that path, because the ratchet and the verdict check need saved files. All files below are in that directory; `<N>` is the review number.

### 2.3 Steps of review N, in order

**S0 Load.** The command activates the skill (`> Skill sc:spec-panel-stoprule-protocol`). The skill runs `stoprule.py init --loop-dir <dir> --rubric "<skill base>/refs/rubric.md"`, which writes `rubric.sha256` on review 1 and, on later reviews, exits 4 (`rubric-changed`) if the rubric file's hash differs from the stored one. The rubric is therefore frozen per loop by a hash, not by a request.

**S1 Prior check (reviews 2 and 3).** `stoprule.py verify-prior --loop-dir <dir> --prior <prior report>` recomputes review N-1's verdict from `ledger-r<N-1>.json` and compares it with the prior report's last line. Outcomes, by exit code:

- 0: match; N = prior N + 1.
- 3 `cap-reached`: prior review is 3 (or higher) with FAIL. Do not review. Run `stoprule.py escalate` if `escalation.md` is missing, print it, stop. This is 427 bullet 4's HALT, now decided by the script.
- 5 `prior-verdict-mismatch`: the prior report's verdict line was not the script's line (hand-edited or hand-written). Stop and say so; never fall back to a first review (427 bullet 1 rule).

**S2 Review.** The panel reviews as in 427 (`--mode critique`; re-reviews look at changed lines plus prior blocking findings). Two changes to what the reviewer emits:

1. The report carries a `## Rubric (frozen)` block that is the rubric file pasted byte for byte (checked in S3).
2. Every finding, of every severity, is also written to `findings-r<N>.json` (schema 2.4). The reviewer writes no `verdict:` line and no Reviser brief.

**S3 Form and ratchet (script).** `stoprule.py check --loop-dir <dir> --review N --spec <current spec> [--baseline <saved copy>]` writes `ledger-r<N>.json`. For each finding:

- `form`: `ok` only if `quote` is at least 20 non-space characters and occurs in the current spec after whitespace normalisation, and `outcome` is at least 40 characters. Else `no-quote`, `quote-too-short`, `quote-not-found` or `no-outcome`. This is the evidence rule's mechanical half: presence and verbatim match. Whether the outcome is concrete is the grader's half (S5).
- `anchor_lines`: every line span in the current spec where the quote occurs.
- `origin` (reviews 2 and 3): `changed` if any anchor line is in the changed-line set, else `unchanged`. The changed-line set comes from `difflib` between the saved baseline copy and the current spec, ignoring whitespace-only changes, plus the line before and after each pure deletion so a finding about removed text can quote a neighbour.
- `ratchet` (reviews 2 and 3): `pass` if `origin=changed`, or if `prior` names an id whose ledger `final` was `blocking` in review N-1 (citing a minor or demoted id does not count). Else `late-found`.
- `candidate`: true only if `claimed` is `critical` or `major`, `form=ok`, and ratchet is `pass` (or review 1). A finding the reviewer called minor is never raised.
- Prior status guard: a prior blocking finding the reviewer marked `resolved` whose quote is still byte-present and whose markdown section (heading to heading) has no changed line is forced to `open`. A fix that touched nothing near the defect cannot have resolved it.
- Rubric check: the report's `## Rubric (frozen)` block must hash to `rubric.sha256`; otherwise exit 6 (`rubric-not-copied`), the skill asks the reviewer once to paste it, then stops.

**S4 Cards (script).** `stoprule.py cards --loop-dir <dir> --review N` writes `cards-r<N>.md`: the rubric, then one card per new candidate holding only `quote`, `outcome`, `example`. No finding id, expert name, claimed severity, section title, report path or panel discussion. Card ids are `C1..Cn` in an order shuffled by a seed taken from the findings file's hash. Prior findings already `blocking` and still `open` or `regressed` are not re-graded: their status is frozen, so a grade cannot oscillate between rounds. With zero candidates S4 and S5 are skipped.

**S5 Second grader (one agent call per review).** The skill spawns `stoprule-grader` once with the cards path as its only input. It answers one line per card, `G <card> blocking|minor: <one-sentence reason>`, applying rubric R1-R2 only: "would an implementer who follows the quoted text as written produce the stated outcome, and is that outcome wrong?". The skill writes the reply verbatim to `grades-r<N>.txt`; `stoprule.py grades` merges it into the ledger. A card without a parsable line gets one re-spawn; still missing, it is `grade=missing` and stays blocking (a false FAIL is cheaper than a false PASS, the stance of `evidence-validator.md:35`).

**S6 Verdict (script).** `stoprule.py verdict --loop-dir <dir> --review N` computes `final` per finding and writes `verdict-r<N>.json`:

- `blocking`: candidate graded `blocking` or `missing`; or a prior blocking finding with status `open` or `regressed`.
- `demoted`: candidate graded `minor` by the grader.
- `late-found`: ratchet `late-found` on a CRITICAL/MAJOR claim with `form=ok`.
- `minor`: everything else, with the form code kept.

`verdict = FAIL` if any `final=blocking`, else `PASS`. The script prints two blocks that the skill appends to the report unchanged: the `Reviser brief` (only when FAIL and N < 3) and the last line, `verdict: PASS|FAIL (computed by stoprule.py, ledger sha256 <12 hex>)`. The line still starts with `verdict: PASS` or `verdict: FAIL`, so 427's text tests and any coordinator grep keep working.

**S7 Terminal outcomes.**

- PASS at any N: terminal audit (2.6). If the audit reinstates a finding, the script recomputes FAIL; otherwise done.
- FAIL, N < 3: the script-written Reviser brief lists only `final=blocking` ids, each with its quote and outcome, plus the rubric and 427 bullet 6 restated. Minor, demoted and late-found findings are not in it, so a brief that says "apply confirmed findings" now has one meaning: the ids in the brief.
- FAIL, N = 3: cap hit. `stoprule.py escalate` writes `escalation.md` (2.5); the report ends with the cap text and `verdict: FAIL`.

### 2.4 Finding-file schema (`findings-r<N>.json`, written by the reviewer)

```json
{
  "schema": "spec-panel-stoprule/1",
  "review": 2,
  "spec_sha256": "<hex of the spec text reviewed>",
  "findings": [
    {
      "id": "R2-4",
      "claimed": "critical|major|minor",
      "expert": "Whittaker",
      "section": "4.2 Worker heartbeat",
      "quote": "<verbatim text from the current spec, >= 20 non-space chars>",
      "outcome": "<what an implementer following the quote builds or does, and why it is wrong>",
      "example": "<optional failing input or sequence and its wrong result>",
      "prior": "R1-3 or null",
      "text": "<the finding as written in the report>"
    }
  ],
  "prior_status": [ { "id": "R1-3", "status": "resolved|open|regressed" } ]
}
```

The script writes `ledger-r<N>.json` with the same ids plus `form`, `anchor_lines`, `origin`, `ratchet`, `candidate`, `card`, `grade`, `grade_reason`, `final`. The reviewer never writes ledger keys: the same split as `qa.md:141` ("The parent writes `sev=`, `trigger=`, `first=` and `origin=`"). `spec_sha256` must equal the hash of the `--spec` file the script reads (exit 7 `spec-mismatch` otherwise), so a reviewer cannot grade one text and quote another.

### 2.5 Cap-hit escalation format (`escalation.md`)

Fixed sections, all generated by the script from the ledgers:

1. Header: spec path, `review: 3 of 3`, the canonical cap text `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`, spec bytes at review 1 and now (growth %).
2. Open blocking findings (the decision list): id, first-seen review, quote, outcome, grader reason, origin. One row each.
3. For awareness, not looped on: grader-demoted findings (with the grader's reason), late-found findings, and CRITICAL/MAJOR claims that failed the form check, one line each.
4. A fixed sentence: "Not looped on: minor, late-found, demoted and form-failed findings. This command will not run review 4." (S1 exit 3 enforces the second half.)
5. A decision prompt per open finding: accept the risk, fix by hand, or start a new loop (a first review, new count, deliberately visible as a reset).

Under `--unattended` the file is added to the return contract's `artifacts` list (UNVERIFIED: whether the git-ignored-path rule of WC-4, `spec-panel.md:457`, drops it when the loop directory is ignored).

### 2.6 Keeping the grader honest: independence and the sampled audit

Independence is by construction, not by instruction:

- Fresh context: a Task subagent spawned with only the cards path; the cards file is script-written and holds no pointer to the report.
- Label stripped: the grader never sees `claimed`, the expert or the panel discussion, which is where the upward anchor lives (the same argument as `confidence-calibrator.md:21`).
- Different model class where available: the agent pins `model: sonnet` while S1 runs the reviewer on `claude-opus-5-5`. The ledger records `grader_model` from the agent frontmatter; if the session itself runs sonnet the ledger flags `same-class`.
- Residual: the agent has `Read` and could open the report if it guessed the path. Nothing mechanical blocks that (section 6).

Audit, two layers:

- In-loop terminal audit, only on a computed PASS: `stoprule.py audit-sample` picks up to 3 `demoted` findings from the whole loop, seeded by the final ledger hash. One auditor call (fresh general-purpose Task, session model, given the full spec, the finding text and the rubric) answers `blocking|minor` per finding. Any `blocking` answer sets that finding's `final=reinstated` (counts as blocking) and the script recomputes FAIL. This bounds a silent wipe-out exactly where it matters: a PASS that rests on demotions. At the cap, the user is the audit: every demotion is listed in `escalation.md`.
- Offline measurement (experiment, then periodic): every demotion in a run is graded post hoc by an auditor with full context and spot-checked by the owner (section 5). `stoprule.py audit-report` computes the demotion error rate = auditor-confirmed real defects / all demotions.

## 3 Exact changes

All new files; no existing file is edited. Source of truth is `src/superclaude/`, then `make sync-dev` (never stage `.claude/`).

| # | File | Kind |
|---|---|---|
| 1 | `src/superclaude/commands/spec-panel-stoprule.md` | new command: copy of `spec-panel.md` (486 lines on master today) plus 5 replaced blocks |
| 2 | `src/superclaude/skills/sc-spec-panel-stoprule-protocol/SKILL.md` | new companion skill: steps S0-S7 |
| 3 | `.../sc-spec-panel-stoprule-protocol/refs/rubric.md` | frozen rubric (text below) |
| 4 | `.../sc-spec-panel-stoprule-protocol/refs/grader-brief.md` | the grader's spawn prompt template |
| 5 | `.../sc-spec-panel-stoprule-protocol/scripts/stoprule.py` | the script (stdlib only) |
| 6 | `src/superclaude/agents/stoprule-grader.md` | new agent |
| 7 | `tests/skills/test_spec_panel_stoprule.py`, `tests/skills/test_stoprule_script.py` | new tests |
| 8 | `docs/designs/spec-panel-stoprule.md` | design note, including the measurement result when it exists |

Not changed: `spec-panel.md` (src, plugin mirror, installed copy), `HOW-WE-WORK.md` (routing stays on `/sc:spec-panel` until the variant is measured), `plugins/superclaude/` (only README-listed commands are mirrored, `tests/commands/test_routing_plugin_parity.py:42-45`).

### 3.1 Command file `spec-panel-stoprule.md`

A byte copy of `spec-panel.md` with exactly these replacements (a test pins the diff, 3.6):

1. Frontmatter `name: spec-panel-stoprule`; the description gets the suffix "with a frozen rubric, a second grader and a script-computed verdict".
2. Title `# /sc:spec-panel-stoprule - ...`; both Usage lines say `/sc:spec-panel-stoprule`.
3. Directly under the title, one line: `> Skill sc:spec-panel-stoprule-protocol`. This is the activation form `install_skills.py:30-32` recognises, so the project rule "a command that names a skill must load it first" applies, and the skill installs standalone (its name ends `-protocol`, `install_skills.py:13-21`).
4. FR-8 and FR-9 (`spec-panel.md:328-329`): "automatically generates a finding with **MAJOR** severity minimum" becomes "generates a finding; it is blocking only under rubric R1 of the Review Loop, otherwise minor". FR-10 (table completeness gates synthesis) is unchanged. This removes the mechanical upward floor that 427 bullet 2 kept.
5. `## Review Loop`: bullets 1, 4 and 7 kept byte for byte (bullet 4 holds the canonical cap text and the HALT clause the pin tests need, `test_review_severity_rule.py:215-219`). Bullets 2, 3, 5 and 6 replaced by:

```markdown
2. **Grading**: severity follows the frozen rubric in the companion skill (`refs/rubric.md`), pasted unchanged into every report as `## Rubric (frozen)`; a finding is blocking only if it quotes the spec verbatim and states a concrete wrong outcome or failing example and the second grader confirms it; CRITICAL and MAJOR labels are kept for reporting only; minor findings are notes and never trigger a revision.
3. **Verdict**: the reviewer writes every finding to `findings-r<N>.json` and writes no verdict; `stoprule.py verdict` computes the last line `verdict: PASS` or `verdict: FAIL` from the ledger, and a re-review stops if the prior report's last line is not the script's line.
5. **Re-review output**: as before, the prior blocking table `resolved|open|regressed`, then findings with `origin=changed|unchanged` computed by the script against the baseline; a blocking claim on unchanged text that cites no prior blocking finding id is `late-found`: reported, never blocking, never in the Reviser brief.
6. **Reviser contract**: the script writes the `Reviser brief` above the last line; it lists only confirmed blocking ids with their quotes and the rubric; revise only text a listed id names; add no rule, mechanism or section no listed id calls for; each added paragraph or table cites its id; report the byte size before and after; at `review: 3` there is no brief and the script writes `escalation.md`.
```

Each bullet stays one line (the repo's line-based matchers, design doc section 5).

### 3.2 Frozen rubric `refs/rubric.md` (literal text)

```markdown
STOPRULE RUBRIC v1 (frozen; hash-checked per loop)
R1 BLOCKING requires both: (a) a verbatim quote of the offending spec text, at least 20 characters, present in the spec under review; (b) a concrete wrong outcome: what an implementer who follows the quoted text as written would build or do, and why that is wrong; or a failing example: a specific input or sequence and the wrong result it gets.
R2 Everything else is MINOR: ambiguity without a wrong outcome, missing rationale, style, "could be clearer", "consider", and wishes for more completeness.
R3 CRITICAL and MAJOR labels never make a finding blocking by themselves. A GAP or blank row in the Guard Condition Boundary Table is blocking only under R1.
R4 When experts disagree on severity, the finding is MINOR unless R1 holds.
R5 In review 2 or 3 a blocking finding must quote a line changed by the last fix, or cite the id of a prior blocking finding; otherwise it is LATE-FOUND: reported, not blocking.
R6 MINOR and LATE-FOUND findings never enter the Reviser brief and are never applied.
```

R1(a) and R5 are checked by the script; R1(b), R2 and R4 by the grader; R3 and R6 by the script's derivation. The reviewer reads all six, so it can predict how its findings will be graded (a design choice: the rubric is the contract, not a trap).

### 3.3 Companion skill `SKILL.md` (outline, about 120 lines)

- Frontmatter: `name: sc:spec-panel-stoprule-protocol`, `allowed-tools: Read, Write, Bash, Task, Grep, Glob`.
- Inputs: the spec, `--re-review`, `--baseline`, `--report-dir` as parsed by the command.
- Steps S0-S7 of section 2.3, each one numbered step naming the exact `uv run --no-project python "<skill base>/scripts/stoprule.py" <subcommand> ...` line and what each exit code means. Exit codes: 0 ok, 2 usage, 3 cap-reached, 4 rubric-changed, 5 prior-verdict-mismatch, 6 rubric-not-copied, 7 spec-mismatch, 8 schema-invalid, 9 loop-exists (`init` for a review 1 in a directory that already holds ledgers).
- Grader spawn: `subagent_type: stoprule-grader`, prompt = `refs/grader-brief.md` with only `{cards_path}` filled. The skill passes no other path.
- Rule: the session appends the script's stdout to the report unchanged and never writes a `verdict:` line itself (prose; S1 of the next review is the mechanical check).
- Installed-path rule: the skill names other primitives only by installed paths (project `.claude/agents/` first, then `~/.claude/agents/stoprule-grader.md`), never `src/superclaude/`.

### 3.4 Script `scripts/stoprule.py` (outline)

Stdlib only (`argparse`, `json`, `hashlib`, `difflib`, `random`, `re`, `pathlib`), so `uv run --no-project python` needs no environment. Pure functions, one thin `main()`:

```python
def norm(text) -> str                               # collapse whitespace for quote matching
def find_anchors(spec_lines, quote) -> list[tuple[int, int]]
def changed_lines(baseline_lines, current_lines) -> set[int]   # difflib opcodes; ignore whitespace-only; +-1 around deletions
def form_check(finding, spec_text) -> str           # ok | no-quote | quote-too-short | quote-not-found | no-outcome
def ratchet(finding, anchors, changed, prior_ledger) -> str    # pass | late-found | n/a
def guard_prior_status(prior, spec_lines, changed) -> str      # forces open when quote present and section untouched
def derive_final(entry) -> str                      # blocking | demoted | late-found | minor | reinstated
def compute_verdict(ledger) -> str                  # FAIL if any blocking or reinstated, else PASS
def render_reviser_brief(ledger, rubric) -> str
def render_escalation(ledgers, sizes) -> str
def sample_demoted(ledgers, seed, k=3) -> list[str]
# subcommands: init, verify-prior, check, cards, grades, verdict, escalate, audit-sample, audit-report
```

Every subcommand writes only inside `--loop-dir` (it reads `--spec`, `--baseline`, `--prior`). Shortcut, stated in the code: the quote match is a whitespace-normalised substring search, not fuzzy; a reviewer who reflows a quote fails the form check and the finding is minor. Upgrade only if the audit shows real defects lost to `quote-not-found`.

### 3.5 Agent `stoprule-grader.md`

Frontmatter: `name: stoprule-grader`, `model: sonnet`, `tools: Read`, `permissionMode: plan`, `maxTurns: 10`. Body (about 40 lines): you see a rubric and cards, nothing else; for each card answer `G <card> blocking|minor: <reason>`; blocking only if R1(b) holds for the quote as written; "the spec could be read this way" without a wrong outcome is minor; open no file except the cards path; do not soften or harden to match an imagined reviewer. Read-only, like `evidence-validator`.

### 3.6 Tests

`tests/skills/test_stoprule_script.py` (behaviour, the part that matters):

- quote found / reflowed / too short / absent gives the four form codes;
- `changed_lines` on a fixture pair: an edited line, an inserted paragraph, a pure deletion (neighbours counted), a whitespace-only change (ignored);
- ratchet: a changed-line quote passes; an unchanged quote is late-found; `prior` citing a blocking id passes, citing a demoted id does not;
- the prior-status guard forces `open`;
- verdict: zero blocking gives PASS; one `grade=missing` gives FAIL; a `reinstated` gives FAIL;
- `verify-prior` exits 5 on a hand-written verdict line and 3 at review 3 FAIL;
- `init` exits 4 when the rubric file changes mid-loop;
- the cards file holds no finding id, no `claimed` value and no report path;
- the escalation output holds the canonical cap text (imported `CANONICAL_CAP_TEXT`, `tests/skills/test_review_severity_rule.py:215`).

`tests/skills/test_spec_panel_stoprule.py` (text and wiring): the variant equals `spec-panel.md` outside the 5 replaced blocks (a computed diff, so a later spec-panel change shows up as a failing test instead of silent drift); the activation line is present; bullets 1, 4, 7 are byte-identical to `spec-panel.md`; no `src/superclaude` string in the command, skill or agent; no phrase matched by `CAP_REGRESSION` (`test_review_severity_rule.py:288`); `install_skills._has_corresponding_command("sc-spec-panel-stoprule-protocol")` is False (the skill installs).

Text tests prove the text exists, not obedience. The script tests are the mechanical part.

### 3.7 Docs

`docs/designs/spec-panel-stoprule.md`: sections 2, 5 and 6 of this spec, the S1 result table when measured, and the promotion rule: the variant replaces the 427 loop in `spec-panel.md` only if section 5's bar is met and the audit error rate is within bound.

## 4 Variant command name and install note

- Command: `/sc:spec-panel-stoprule`, installed at `~/.claude/commands/sc/spec-panel-stoprule.md`, next to `spec-panel.md`, which is never edited.
- Companion skill: `~/.claude/skills/sc-spec-panel-stoprule-protocol/` (with `refs/` and `scripts/stoprule.py`). Script call: `uv run --no-project python "<skill base>/scripts/stoprule.py" <subcommand>`, the form used by `sc-implement-protocol/refs/managed-workspace.md:54`.
- Agent: `~/.claude/agents/stoprule-grader.md`.
- Install path: `superclaude install` copies new command files and skips existing ones without `--force` (`install_commands.py:60-80`), and installs skills the same way (`install_skills.py:100-104`), so a plain install adds the three new primitives and leaves `spec-panel.md` alone. Never run it with `--force` on the experiment host. Before the experiment, check the three target paths do not exist, then record their sha256 in the install watcher as the A/B did.
- Host requirement: `uv` on the worker's PATH (the script has no dependencies).
- Experiment brief substitution, one line: `/sc:spec-panel` -> `/sc:spec-panel-stoprule`, applied to the Arm B review briefs (rounds 1, 2, 3), which already pass `--re-review <prior-findings-file> --baseline <saved copy>`. The ratchet needs the baseline, so the comparator brief set is Arm B's, not treatment A's (which had no flags). No other brief change; reviser briefs are untouched (their "apply confirmed findings" now resolves to the script-written list).
- Covariate to log: the variant is copied from today's master `spec-panel.md` (486 lines, with the unattended worker-contract section), while the A/B ran the 472-line 427 file. The worker-contract section is inert without `--unattended`, which the S1 briefs did not pass (UNVERIFIED: confirm against the saved briefs).

## 5 Measurement plan on S1

**Setup.** Scenario S1 (Orca worker-contract spec, 57,763 bytes, base 2cb683f5), same model (`claude-opus-5-5` reviewer), same Arm B briefs with the one-line name substitution, same loop (3 reviews, 2 fix cycles), 2 replicates (`stp-r1`, `stp-r2`), run one after the other with the install watcher on, `WORKER-CONTRACT.md` moved aside as before. Comparators: control (`ctl-r1`, `ctl-r2`) for the pre-registered bar, Arm B (`flg-r1`, `flg-r2`) as the nearest arm. The bar is fixed before the first run, as D10/D11 were.

**Metrics** (recorders' `metrics.json`, as in the A/B, plus new rows):

| Metric | Source | Already in A/B? |
|---|---|---|
| Findings per review | report | yes |
| Critical+major proxy per review (reviewer labels) | `findings-r<N>.json` `claimed` | yes |
| Confirmed blocking per review | `verdict-r<N>.json` | new (the primary R3 metric) |
| Growth after fix cycles 1 and 2 | spec bytes | yes |
| Clean PASS and its review number | last line | yes |
| Candidates, demoted, late-found, form-failed per review | ledgers | new |
| Reviser: findings applied vs ids in brief; uncited added hunks | disposition file, `difflib` | new |
| Extra agent calls, script calls, wall time per review | session logs | new |
| Demotion error rate | offline audit | new |
| Verdict reproducible | `stoprule.py verdict` re-run on saved ledger gives the same line | new |

**Predicted numbers** (committed now, before any run):

| | Control mean | Arm B mean | Stoprule prediction | Bar |
|---|---|---|---|---|
| R3 open critical+major, after confirmation | 6.0 (proxy) | 3.5 proxy, 2.5 blocking by 427 grading | r1 = 3, r2 = 1, mean 2.0; one replicate may PASS at R3 | <= 3 in both replicates, or a clean PASS earlier |
| R3 reviewer-label proxy (unconfirmed) | 6.0 | 3.5 | mean 4 (labels still drift; only R3/R4 of the rubric touch them) | reported, not a bar |
| Growth after 2 fix cycles | 63.5% | 30.0% | mean 22% (range 16-28%) | <= 44.4% |
| R1 confirmed blocking | n/a | n/a | 5-8 (of 9-17 proxy) | >= 3 (evasion check) |
| Demotion error rate | n/a | n/a | about 10-15% | <= 20% |

Why these numbers: the R3 drop comes from three removals visible in the record (FR-8 GAP-floor MAJORs, disagreements resolved upward, late-found R3-8-type findings) plus fewer changed lines because the reviser gets 5-8 ids instead of 15. It does not come from the ratchet on 427-style runs, because 89-100% of their new findings were already `origin=changed`; the ratchet mostly blocks re-attacks on untouched text. Growth falls because the 9 of 15 minor findings Arm B applied in round 2 are no longer in the brief. Confidence that both replicates are <= 3: about 60%; n = 2 cannot show more than a large effect.

**What falsifies the idea** (any one):

1. R3 confirmed blocking > 3 in either replicate with no earlier PASS.
2. Growth after 2 cycles > 44.4% in either replicate.
3. Demotion error rate > 20% over all demotions in both replicates: then any R3 gain is counted as wiped-out defects, and the result is void, not a pass.
4. Problem moved, not solved: R3 confirmed <= 3 while the R3 reviewer-label proxy stays >= 6 AND the auditor rates at least half of R3 demoted plus late-found findings as real blocking defects.
5. Evasion: at R1, fewer than 3 confirmed blocking findings, or more than half of CRITICAL/MAJOR claims fail the form check (the reviewer stopped quoting).
6. Not reproducible: re-running `stoprule.py verdict` on any saved ledger gives a different line.

**Audit protocol (offline).** After both replicates, every `demoted` and every `late-found` finding goes to one fresh auditor session (Opus, full spec at that review, the finding text, the rubric) that answers `blocking|minor` with a reason; the owner spot-checks 5 of them, picked by `stoprule.py audit-sample` with k=5. Error rate = auditor `blocking` / demotions. Late-found findings are reported separately (they are demoted by design; their audit measures what the ratchet hides, not grader accuracy).

## 6 Risks, costs and ways it could make the loop worse

### 6.1 Which measured causes the mechanism removes

| Measured cause | Effect of this variant | Enforcement |
|---|---|---|
| Fix-induced findings on changed lines | **Left.** They stay blocking by design: a defect a fix wrote is real (flg-r2 N12). Reduced only indirectly: fewer ids in the brief means fewer changed lines to attack. | none new |
| Severity drift upward | **Removed in the main.** Labels never decide (R3); FR-8/FR-9 floor gone; disagreements go minor (R4); the grader sees no label; a confirmed prior status is frozen; untouched text cannot be re-raised (R5); the rubric hash is fixed per loop. Residual: the grader is a model. | script + second model |
| Revisers adding mechanisms and applying minor findings | **Minor-applying removed; mechanism-adding reduced, not removed.** The script-written brief carries only confirmed ids, so minors cannot be applied by following the brief. Added text outside a cited id is only counted (uncited hunks), not blocked. | script for the first; prose for the second |
| No mechanical stop | **Removed within one loop directory.** The verdict is computed; a hand-written verdict is caught next round (exit 5); review 4 is refused (exit 3); the escalation file is generated. Residual: starting a new loop directory resets the count. | script |

### 6.2 Costs per loop (3 reviews)

| Item | Per review | Per loop |
|---|---|---|
| Extra agent calls | 1 grader call when there is at least one candidate (plus 1 re-spawn only on an unparsable reply) | 2-3, plus 1 terminal auditor call only on a PASS |
| Script calls (Bash) | 5-6 (`init`, `verify-prior`, `check`, `cards`, `grades`, `verdict`) | about 17, plus `escalate` at the cap |
| Extra sessions | 0 (the grader and auditor are Task subagents of the reviewer session) | 0 |
| Wall time | grader 1-3 min, scripts under 5 s (UNVERIFIED estimate; no grader has run yet) | +4-10 min |
| Reviewer output | one JSON entry per finding, about +10-15% output tokens (UNVERIFIED estimate) | same |

Against this, a loop that ends on a defined outcome saves the unbounded human triage the A/B runs ended in.

### 6.3 Risks and ways it could make things worse

1. **Grader wipes out real defects.** A lenient grader produces a PASS that hides blockers. Bounded by the PASS-time audit sample (2.6), the listing of every demotion at the cap, and the offline error-rate bar (<= 20%). Residual: with k=3, a 1-in-5 error rate is missed about half the time in a single loop.
2. **Grader not truly independent.** It has `Read` and could open the report; when the session itself runs sonnet the classes match. Both are recorded (`same-class` flag); neither is blocked. A tool-less agent would close the first gap if the platform allows `tools:` to be empty (UNVERIFIED).
3. **Ratchet laundering.** A reviewer can quote an unrelated changed line to pass R5. Partial guard: the grader judges whether following *the quoted text* produces the outcome, so an unrelated quote should fail R1(b). Not mechanical.
4. **Late-found demotion hides first-review misses.** A real defect missed in review 1 cannot block reviews 2-3 unless a fix touched it. This departs on purpose from `qa.md:167` (where `late` blockers always block): the spec loop's problem is non-convergence, and a late finding is still listed for the user in the PASS record and in `escalation.md`. Measured by the late-found audit row.
5. **Evasion moves the problem.** A reviewer that dislikes demotions may stop quoting, or a computed PASS may simply mean nobody wrote blocking findings. Measured by falsifiers 4 and 5; not prevented.
6. **More FAILs from fail-safe paths.** `grade=missing` stays blocking; schema or rubric errors stop the run. A flaky grader therefore makes the loop stop more, not pass more (the intended direction).
7. **Prose residuals.** The skill must append the script's output instead of writing a verdict, and must give the grader nothing but the cards path. The next review's `verify-prior` catches the first; at a final PASS there is no next review, so the recorder (or user) must run `stoprule.py verify-prior` on the final report. The second has no check.
8. **Reset bypass.** `init` refuses a review 1 in a loop directory that already holds ledgers (exit 9, `loop-exists`), but a coordinator can pick a new directory. The cap is mechanical per directory, not per spec.
9. **Maintenance cost.** A 486-line copy of spec-panel drifts when spec-panel changes; the diff test (3.6) turns drift into a red test, and the owner must re-copy. The repo gets a second computed-severity model next to `qa.md`'s; section 8 keeps them separate on purpose rather than merging them early.
10. **FR-8/FR-9 relaxation.** A real guard gap with a blank behaviour cell now blocks only with a quote and a wrong outcome. Guard gaps that matter usually have one (the input that reaches the blank row); demoted GAP rows are in the audit.
11. **Metric change.** Success is now counted on confirmed blocking, which the variant itself defines. The raw label proxy is reported beside it and falsifier 4 tests whether the gain is only definitional.

## 7 Open questions

1. Can an agent definition carry an empty `tools:` list so the grader cannot read anything but its prompt (inline the cards instead of a path)? UNVERIFIED; it would close risk 2's first half.
2. Is `model: sonnet` independent enough from an Opus reviewer, or does the grader need a different family (for example through the external-model proxy `sc-bare-review` uses)? The offline audit measures error rate, not independence; a same-family bias toward the same wording would not show up in it.
3. Should the reviser read only the script-written brief file rather than the whole report (which still shows minor findings)? This variant keeps 427's "the reviser reads the report" and relies on the brief's id list; a separate `reviser-brief.md` handed to the reviser would need a brief change, which breaks the one-line substitution.
4. Is k=3 right for the PASS-time audit, and should the audit also sample late-found findings at PASS? Each extra sample is part of one auditor call, so the cost is tokens, not calls.
5. Should a late-found finding that the auditor rates blocking reopen the loop (count unchanged) or only be listed? This variant only lists it.
6. The 20-character quote minimum and 40-character outcome minimum are guesses; the audit's `quote-not-found` and `no-outcome` rows should tune them.
7. Does the reviewer reliably produce valid JSON over a 22-finding review? Exit 8 stops the run; a one-retry rule (re-ask for the file) may be needed after the first S1 run.
8. Under `--unattended`, is a cap-hit run `succeeded` (report written) or `blocked` (needs a user decision)? The current contract says succeeded when the report is written (`spec-panel.md:457`); escalation arguably fits `blocked_question` better.

## 8 Reuse by other review commands

The reusable unit is the skill's middle: finding file in, script-computed ledger and verdict out, one blinded grader call between. The spec-panel parts (panel, FR-8/FR-9 text, Boundary Table) stay in the command. To make that split real rather than promised:

- `stoprule.py` takes the rubric path and a `--severity-map` (JSON mapping a command's labels to `raise|never`, default `{"critical": "raise", "major": "raise", "minor": "never"}`) instead of hard-coding spec-panel labels. That is the only extension point added now; no plug-in system.
- `--spec` accepts any single text file (spec, plan, report). The ratchet needs a baseline copy of that file; reviews of code diffs (several files) are out of scope for v1.

| Consumer | Fit | What it would take |
|---|---|---|
| `/sc:reflect` (UC-1 plan/spec reviews; Tier 2 already merges heterogeneous reviewers) | Good for UC-1 on a single document: map `Drift`/`Regression` to `raise`, `Authorized expansion`/`Necessary deviation` to `never`. Its evidence-validator gate already re-reads citations; the grader adds the outcome check. | A reflect variant that writes the finding file and calls the same script; not part of this change. |
| rf-qa agents (CRITICAL/IMPORTANT/MINOR, Fix Cycle at `rf-qa.md:379-`) | Partial: rf-qa fixes in place, so there is no separate reviser, but its Fix Cycle re-checks are exactly the review N+1 step. Map CRITICAL and IMPORTANT to `raise`. | The rf-qa caller (a skill, not the agent) runs the script; the agent only writes the finding file. |
| `/sc:implement` final review | **Do not reuse the stop rule.** `qa.md` already derives severity from checklist answers with a parent Read-back and computes the verdict (`qa.md:37-97`), and deliberately keeps `late` blockers blocking (`qa.md:167`) because code defects found late are still defects in shipped code. Possible later reuse: the blinded grader as an optional check of `harmful-effect`/`false-claim` answers, only if implement's own measurements show reviewer inflation. | nothing now |
| Plain agents (no command) | Out of reach: nothing invokes the script. | the brief would have to run the skill |

Promotion path: if S1 meets the bar with an audit error rate <= 20%, move the four Review Loop bullets and the FR-8/FR-9 change into `spec-panel.md` itself, keep the skill as the shared engine, and retire the variant command. If it fails, delete the three primitives; nothing else depends on them.
