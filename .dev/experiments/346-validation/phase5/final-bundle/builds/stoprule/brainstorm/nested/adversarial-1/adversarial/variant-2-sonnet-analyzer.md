# Variant 2 (analyzer): `spec-panel-stoprule` - computed verdict, graded blockers, sealed ledger

Theme: stoprule | Issue: #346 | Base: PR 427 `## Review Loop` | Author stance: analyzer (root cause, counted evidence) | Status: draft for adversarial debate
Evidence read for this variant: seed-brief.md, enrichment/codebase-context.md, AB-REPORT.md, ARMB-REPORT.md, ctl-r1 and flg-r2 `spec-panel-round3.md`, flg-r2 `disposition-round2.md`, ctl-r1 spec history v2/v3, `spec-panel.md`, `docs/designs/spec-panel-review-loop.md`, `sc-implement-protocol/refs/qa.md`, `confidence-calibrator.md`, `evidence-validator.md`.

## 1. Problem and evidence

1. No S1 run reached PASS inside 3 reviews. R3 critical+major proxy: control 8/4 (mean 6.0), 427 6/5, 427+flags 6/1; growth after two cycles 63.5% / 29.7% / 30.0% (AB-REPORT, ARMB-REPORT). 427 fixed growth, not convergence.
2. Root cause, counted on ctl-r1 R3 (`spec-panel-round3.md:179-189`, 8 blocking) against the real fix-cycle diff (`specs/history` v2 vs v3): all 8 map to a round-2 row the fix touched (Part 1, lines 21-31); 5 sit on text the fix wrote (defect span absent from the baseline: R3-1, 2, 3, 5, 6) and 3 on text already in the baseline (R3-4, 8, 9; R3-8 says so itself, line 188). flg-r2's only R3 blocker (N12) sits on text N5's fix wrote. The loop mostly re-meets its own partial fixes, so a late-finding ratchet alone cannot reach the bar.
3. Severity drift is built in: FR-8/FR-9 force every GAP or blank row to MAJOR (`spec-panel.md` FR-8/FR-9), ctl-r1 R3 recorded both expert disagreements as MAJOR (lines 169-170), and the verdict is the reviewer's own last line. Revisers applied 15 of 15 findings, 9 of them minor, because their brief said "apply confirmed findings" (flg-r2 `disposition-round2.md:12,35`).
4. Nothing computes "blocking" or ends the loop: the 427 section is seven prose bullets and its own design doc says the tests prove the text exists, not obedience (`spec-panel-review-loop.md:143`); count and cap live in the coordinator's memory.
5. This variant moves verdict, cap check, anchor check and citation check into a script over a sealed ledger, adds one independent semantic judgement (a grader) and a sampled audit of what the grader removes.

## 2. Mechanism

### 2.0 Decisions this variant commits to

- Where computation lives: BOTH, split by kind. A script (`stoprule.py`, stdlib only) does everything deterministic: cap and count, quote and citation read-back, ratchet anchoring, hunk coverage, grade merge, verdict, escalation text. A second agent call (`finding-grader`) supplies the single semantic judgement the script cannot make: does the stated outcome follow from the quoted text under the rubric. The script validates and merges the grader's reply; the grader never writes a file.
- Independence of the grader: fresh context (subagent), a different model class from the reviewer (`sonnet` for an opus reviewer, `opus` for a sonnet reviewer), input built by the script from claim fields only (opaque ids, no report, no spec path, no reviewer severity word, no expert names), plus two planted canary claims per batch with known answers.
- Audit: a stronger-class auditor with local spec context re-judges demotions and one unclaimed hunk per round; at a PASS candidate it re-judges every demotion and a contested one blocks the PASS. The false-demotion rate is a reported number.
- Output location: the report file is the only repository file written. The ledger lives in a private scratch dir outside the repo and is embedded into the report at the end, so the verdict is reproducible from the report alone and the S1 briefs' "write only this file" holds (UNVERIFIED that a worker may write under `/tmp`; ctl-r1 R3 ran `uv run` and a private `/tmp/ironclaude-batch.*` dir, lines 13, 209).

### 2.1 Parts

| Part | Installed at | Role |
|---|---|---|
| Command `spec-panel-stoprule` | `~/.claude/commands/sc/` | copy of `spec-panel.md`; Review Loop bullets 2-6 rewritten, bullet 8 added; calls the skill |
| Skill `sc-spec-panel-stoprule-protocol` | `~/.claude/skills/` | `SKILL.md` procedure; `refs/rubric.md` (frozen); `refs/canaries.json`; `scripts/stoprule.py` |
| Agent `finding-grader` | `~/.claude/agents/` | `tools: Read`, `model: sonnet`; two input kinds, `grade` and `audit`; replies JSON lines only |
| Scratch dir | `/tmp/stoprule-XXXXXXXX/` (umask 077) | `ledger.jsonl`, `diff.json`, `grader-in-K.txt`, `grader-out-K.txt`; removed by `finalize` |
| Report | path the brief names | prose, then sealed ledger, computed block, Reviser brief or Escalation, sentinel, `verdict:` |

### 2.2 Ledger schema (JSON Lines; reviewer writes `claim`, `prior`, `checked`; the script appends the rest)

```
{"k":"claim","id":"R3-1","quote":"<verbatim, <=300 chars>","span":"<verbatim part of quote, <=120 chars: the defective words>",
 "outcome":"<named reader or test that follows the quote and the wrong result it produces, or the two quotes that contradict>",
 "evidence":[{"path":"src/...","line":376,"text":"<verbatim>"} | {"live":"<command>","saw":"<output>"}],
 "prior":null|"N1","sites":["<verbatim other places of the same defect>"]}
{"k":"prior","id":"N1","status":"resolved|open|regressed","resolved_by":"<verbatim text now in the spec>"|null}
{"k":"checked","lines":"170-182"}                  # one per changed hunk that has no claim
script-appended: seal{sha256 of the reviewer lines} | form{id,quote_lines,span_novel,evidence_ok,issues} | grade{id,blocking,q2,why}
                 | audit{id,real,why} | final{id,status} | verdict{value,counts}
```
`status` of a claim ends as one of: `confirmed`, `minor-form` (no verbatim quote or no outcome after one repair), `late-found` (ratchet), `minor` (grader), `unconfirmed` (grader failed twice). A reviewer-written severity word appears nowhere in the schema; there is nothing to read.

### 2.3 The loop, in order (one review = steps S0-S10; the coordinator's fix cycle sits between reviews)

All script calls are `uv run --no-project python "<skill base>/scripts/stoprule.py" <sub> ...`; `<skill base>` is the directory the Skill call reports, else `~/.claude/skills/sc-spec-panel-stoprule-protocol`, else the project `.claude/skills/...` copy. Exit codes: 0 ok, 3 repairable once, 4 HALT at cap, 5 stop (bullet 1 conditions), 6 ledger tampered.

- S0 `begin --spec S --report R [--prior P --baseline B]`. Applies 427 bullet 1 (unreadable or empty file, no `review: N of 3` header in P: exit 5, say which). Reads the prior sentinel (below) for N, verdict and rubric hash; N = prior N + 1, or 1. If prior is `review=3` with `verdict: FAIL`: exit 4 and print the prior Escalation section, no review (this replaces "the coordinator remembers"). If the prior rubric hash differs from the installed `refs/rubric.md`: exit 5 (rubric is frozen for the loop). Computes the token diff B to S, writes `diff.json` (changed hunks, novel spans), prints the hunk list the reviewer must cover and prints the rubric with its sha256. First review: no baseline, no ratchet, no hunk list (`ratchet: off` is recorded, never silent).
- S1 Review as 427 (panel, prior-findings table, FR-8 to FR-10 on changed lines only). Before any prose the reviewer appends ledger lines: one `claim` per candidate blocker, one `prior` per prior confirmed id, one `checked` per changed hunk without a claim. A GAP or blank-behaviour row becomes a candidate claim; it is not automatically MAJOR.
- S2 `seal`. The script checks each claim: `quote` is a whitespace-normalised substring of S (lines recorded); `span` is a substring of `quote`; `outcome` has at least 8 words; each `{path,line,text}` evidence entry is read back (file exists under the repo root, `text` within 3 lines of `line`), `live` entries are marked `unverified`; `prior` names an id in P's confirmed set; `resolved_by` for a `resolved` prior is a substring of S inside changed tokens, else the status is forced to `open`; every changed hunk has a `checked` or a claim. Anchor (the ratchet, review 2 and 3): `span_novel` = `span` does not occur verbatim in B. A claim with `span_novel=false` and no `prior` is `late-found`. Defects that can be repaired (quote not verbatim, outcome empty, missing `checked`) exit 3 once and list the claim ids; the reviewer may edit those fields of those lines only; the second `seal` is final (`repair_used` recorded). Then it appends `seal` with the sha256 of all reviewer lines.
- S3 `grade-prep`. Claims still eligible go into batches of at most 6 plus 2 canaries drawn from `refs/canaries.json` (one known-blocking, one known-minor), shuffled with a seed derived from the sealed hash, renamed `C1..Cn`. Each claim block holds only: `quote`, `span`, `outcome`, evidence entries marked `verified` or `unverified`, and, for claims without a `prior`, the baseline hunk text (old side) for question Q2. Batch file = rubric text + blocks.
- S4 Grader: one Agent call per batch, all batches in one message: `subagent_type: finding-grader`, `model: sonnet` (opus if the reviewer is a sonnet-class model; the command says "a class different from your own"), prompt = "Read `<batch file>` and return the JSON lines it asks for, nothing else". The parent saves each reply byte for byte to `grader-out-K.txt`.
- S5 `apply-grades`. Validates one line per `Cn`, no extras, `blocking` boolean, `q2` in `same|different|na`, `why` at most 25 words. A wrong canary rejects that batch (rerun once). A second failure leaves its claims `unconfirmed`, which can never PASS. Final status per claim: grader `blocking:false` gives `minor`; `blocking:true` with `q2=same` and no `prior` gives `late-found`; otherwise `confirmed`.
- S6 `audit-prep` / S7 Auditor / `apply-audit`. Pool = every demoted claim (`minor`, `late-found`, `minor-form`) plus one unclaimed hunk (seeded) re-reviewed as a mini-review. FAIL candidate: sample up to 3 demotions plus the hunk. PASS candidate (zero confirmed): ALL demotions plus 2 hunks. The auditor sees the claim, the rubric and 15 lines of S around the quote, not the grader's reason. `finding-grader` in `audit` mode, `model: opus`. `real:true` on a demotion sets `contested`; at a PASS candidate it promotes the claim to `confirmed (audit)`. A hunk finding that passes the form check is added as a claim `A-n`. Counts `sampled` and `contested` go into the sentinel.
- S8 `status` prints each id with its final status and reason. The reviewer now writes the prose report and copies those statuses; the prose carries no verdict line and treats the ledger as the only severity source. Non-blocking observations stay in the prose as notes without severity words.
- S9 `finalize --report R`. Refuses if R already holds a line starting `verdict:` (hand-typed) or a prose mismatch it cannot repair. Appends: the sealed ledger in a fenced block; `## Computed result` (counts, a table of confirmed findings with quote, outcome, sites; the list of late-found, minor and demoted ids with one line each; `label_mismatch` ids whose prose says MAJOR, CRITICAL or blocking near the id while the final status differs); then the Reviser brief (review 1 and 2, FAIL) or the Escalation (review 3, FAIL) or "PASS with known debt" (the late-found and contested ids, still listed); then the sentinel `<!-- stoprule v1 review=N/3 rubric=<12hex> confirmed=a late=b minor=c contested=d sampled=e unconfirmed=f ratchet=on|off growth=+x% ledger=<12hex> -->`; then the last line `verdict: PASS|FAIL`. Removes the scratch dir.
- S10 `check --report R` (reviewer runs it; the coordinator runs it before the fix cycle). Re-extracts the ledger, verifies the seal, recomputes every status except the grader and auditor replies (those are in the ledger as data), recomputes the verdict, compares sentinel, computed block and the last line. Exit 0 or 6. A report without a sentinel is a non-compliant run and is counted as such.

### 2.4 The verdict function (pure over the ledger; `stoprule.py verdict --report R` prints it)

```python
confirmed  = [c.id for c in claims if c.final in ("confirmed", "confirmed-audit")]
unresolved = [p.id for p in priors if p.status != "resolved" and p.id not in asserted]  # an open prior needs a claim line; without one it counts
pending    = [c.id for c in claims if c.final == "unconfirmed"] + uncovered_hunks
verdict    = "PASS" if not (confirmed or unresolved or pending) else "FAIL"
```
Any confirmed blocking finding is FAIL, none is PASS; a missing grade, an uncovered hunk or an unresolved prior is also FAIL, so silence never passes. `stalled` (confirmed count not lower than the previous review while at least one remains) is reported in the computed block and is not a halt; the canonical cap is the only halt.

### 2.5 Cap-hit outcome (review 3 with `verdict: FAIL`, or `begin` exit 4)

`finalize` writes `## Escalation to the user` instead of a Reviser brief: (a) first line `ESCALATION: spec-panel-stoprule review 3 of 3, verdict FAIL`; (b) table of open confirmed findings: id, first review it appeared in, status trail (`r1 open, r2 open, r3 open`), quote, outcome, evidence; (c) contested demotions the auditor judged real; (d) late-found items, printed once, labelled "real or not, not looped on"; (e) counts and spec growth per round; (f) "Not looped on: minor notes (count and where), late-found items, any fourth review, any fix cycle beyond two"; (g) the two decisions only the user can take: accept the spec with (b) recorded as known issues, or authorize one extra cycle limited to the ids in (b) (the user lifts the cap, the loop never does). The canonical sentence `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` stays in bullet 4 and in the Escalation footer.

### 2.6 What is mechanical and what is prose

| Rule | Enforced by | If the model ignores it |
|---|---|---|
| Review count, HALT at cap, rubric frozen across the loop | `begin` exit 4 / 5 | a run that never calls `begin` has no sentinel; `check` fails it; not preventable |
| Quote verbatim, outcome present, citation read-back, hunk coverage, prior ids | `seal` | claim demoted `minor-form` (after one repair) |
| Ratchet: span absent from baseline, or open prior | `seal`, then Q2 in the grader batch | claim `late-found` |
| Blocking confirmed by an independent judge | Agent call (prose instruction) + script validation of the reply | skipping the Agent call leaves claims `unconfirmed`, so FAIL, never PASS |
| Verdict line | `finalize` + `check` | a hand-typed line is refused or fails `check` |
| Reviser touches only the brief's ids | prose (Reviser contract) | residual risk, see section 6 |
| Grader really is a different class and really fresh | prose (Agent call parameters) | residual; canaries and the audit measure the effect, not the cause |

### 2.7 Measured causes: removed and left

| Cause (AB/ARMB data) | Effect of this mechanism |
|---|---|
| Fix-induced findings on changed lines (89% R2, 100% R3) | LEFT, by design: the ratchet anchors them. Only trimmed at the edges (form check, grader) and by a smaller edit surface. The 5 of 8 ctl-r1 findings on fix-written text pass every filter. |
| Severity drifts upward round to round | REMOVED as a label: severity is computed from a hash-frozen rubric, FR-8/FR-9 floor overridden, no consensus clause. Residual: outcome wording can still be inflated; the grader and the audit are the check. |
| Revisers add mechanisms and apply minor findings | PARTLY: the Reviser brief is generated from confirmed ids only, with quotes and `sites`; notes are labelled "not instructions". The prose report still sits beside it. |
| No mechanical stop | REMOVED for count, cap, verdict and escalation format; PRESERVED as a risk that a session skips the script (detected by `check`, not prevented). |

## 3. Exact changes

### 3.1 Command: `src/superclaude/commands/spec-panel-stoprule.md` (new file, additive)

Produced by copying `spec-panel.md` and applying exactly these edits (the measurement copy is made the same way from the 472-line 427 file that Arm B used, so the base text is identical; master's file adds `## Unattended mode`, 14 lines, orthogonal):
- Frontmatter `name: spec-panel-stoprule`; `description` ends with "(experimental variant: computed review-loop verdict)". Heading and every `/sc:spec-panel` in Usage and Examples become `/sc:spec-panel-stoprule`. `mcp-servers`, personas, FR-1 to FR-10, Output Formats, Boundaries: unchanged. FR-8/FR-9 stay in the file; Review Loop bullet 2 is what overrides their "MAJOR minimum" for blocking purposes inside the loop.
- `## Review Loop`: bullets 1 and 7 keep the 427 text (7 adds "and may not change the rubric or its hash"); bullets 2-6 are replaced; bullet 8 is new. New text (each one line in the file):

```
2. **Grading**: severity is computed by the skill's script from its frozen rubric and is never read from a reviewer's word; a finding is blocking only if it quotes the offending text verbatim, states a concrete wrong outcome or failing example, and a second grader who sees only the quote, the outcome and the rubric confirms it; an FR-8/FR-9 row is a candidate that must pass the same test, not an automatic MAJOR; agreement or disagreement of experts, importance of the section and lateness never make a finding blocking; everything else is minor, goes to the notes and never triggers a revision.
3. **Verdict**: a critique-mode report's last line is `verdict: PASS` or `verdict: FAIL`, written only by the script's `finalize` from the sealed finding ledger (PASS = no confirmed blocking finding, no open or regressed prior blocking finding, every changed hunk covered, every claim graded); a hand-typed verdict line fails `check`.
4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; <427 clauses on N, header, --iterations, Improve and the coordinator's saved copy, verbatim>; `begin` derives N from the prior report's sentinel and exits 4 on a prior `review: 3` with `verdict: FAIL` (HALT, no review); a review 3 that ends FAIL carries the `## Escalation to the user` section written by `finalize` and no Reviser brief.
5. **Re-review output**: first the prior blocking findings `resolved|open|regressed`, then claims on lines changed against the baseline; `origin=changed|unchanged` is computed by the script; a blocking claim in review 2 or 3 must have a `span` that does not occur in the baseline copy or cite an open prior id, else it is `late-found`: listed in the report, never looped; <427 sentences on empty diff, FR-8 to FR-10 on changed lines only and the rf-qa Fix Cycle steps 1-5 lookup, verbatim>.
6. **Reviser contract**: the Reviser brief is generated by `finalize` from confirmed findings only (id, quote, outcome, sites), placed just above the sentinel and the `verdict:` line, and omitted at review 3; revise only the quoted text and the listed `sites`; apply no id that is not in the brief, notes are not instructions; add no rule, mechanism or section no listed finding calls for; each added paragraph or table cites its finding id; the reviser reports the byte size before and after.
8. **Procedure** (critique mode only): before the first panel step invoke Skill `sc-spec-panel-stoprule-protocol` and follow its steps S0 to S10 in order; never write a `verdict:` line yourself; run `check` last.
```
Fallback if the skill folder is missing: say so and run the 427 loop unchanged with `stoprule: missing` in the header (never a silent downgrade).

### 3.2 Skill: `src/superclaude/skills/sc-spec-panel-stoprule-protocol/`

- `SKILL.md` (about 90 lines, `allowed-tools: Read, Write, Bash, Agent`, delegate-only, no slash command, same pattern as `sc-bare-review`): steps S0-S10 of section 2.3 with the literal commands; the Agent-call parameters; the failure table (grader reply invalid twice -> claims stay `unconfirmed` and the report says so; Agent tool unavailable -> same, verdict FAIL with `grader: unavailable`; script exit codes); a "do not" list (no verdict line, no severity words before `status`, no ledger edits after `seal`, no editing `refs/rubric.md`).
- `refs/rubric.md` (frozen text; its sha256 prefix is pinned in a test and recorded in every report):

```
RUBRIC v1 (frozen; a change is a new version and starts a new loop)
BLOCKING needs B1, B2 and B3.
B1 Quote: the finding quotes the offending text verbatim (a substring of the spec under review) and marks the defective words (span).
B2 Outcome: it states a concrete wrong outcome: a named reader, implementer or test that follows the quoted text exactly and produces a
   specific wrong result; or two quoted texts that cannot both hold; or a check that cannot pass or always passes, with the input that shows it.
B3 Kind, one of: (a) contradiction between two quoted texts; (b) a claim about a source that the source's quoted text contradicts; (c) an
   acceptance check that cannot pass or passes vacuously; (d) one text with two readings that lead to different observable results, both named;
   (e) a step that loses data or takes an unsafe action.
CRITICAL is BLOCKING under (e) or in a requirement the spec calls core; the verdict does not tell them apart.
MINOR is everything else: wording, missing example, moved line number or citation drift, style, a gap whose intended behaviour is inferable
   from nearby text, a suggestion to add a rule, mechanism or section.
Never a reason to be blocking: experts agree; experts disagree; the section is important; the finding was found late; a Boundary Table row says
   GAP or blank (such a row is a candidate and must meet B1-B3).
Q2 (re-reviews): given the baseline text shown, could a reader of the baseline already produce the same wrong outcome? same | different | na.
```
- `refs/canaries.json`: 4 synthetic blocking and 4 synthetic minor claims (each `{quote, span, outcome, evidence, answer}`), none about the spec under review. Rotated by seed so no batch repeats a pair within a loop.
- `scripts/stoprule.py` (stdlib only: `argparse, difflib, hashlib, json, pathlib, random, re, sys`; about 380 lines; no network, no subprocess; reads only the paths in its arguments and evidence paths resolved under `--root`, rejecting `..` escapes; writes only the scratch dir and, in `finalize`, the report). Functions: `norm(text)` whitespace normaliser used by every substring test; `novel(span, baseline)`; `hunks(base, spec)` (token diff, ranges in spec lines); `load_ledger(path)`; `cmd_begin, cmd_seal, cmd_grade_prep, cmd_apply_grades, cmd_audit_prep, cmd_apply_audit, cmd_status, cmd_finalize, cmd_check, cmd_verdict`; `compute_verdict(ledger)` (section 2.4); `render_escalation(ledger)`; `render_reviser_brief(ledger)`. The seed for shuffles is `sha256(sealed ledger)[:8]`, so a replay gives the same batches.

### 3.3 Agent: `src/superclaude/agents/finding-grader.md`

Frontmatter `name: finding-grader`, `category: quality`, `tools: Read`, `model: sonnet`, `maxTurns: 10`, `permissionMode: plan` (same pattern as `confidence-calibrator`: the parent writes the reply to disk, the agent writes nothing). Body: role (you did not review the spec and cannot see it; you see claim blocks only); "Read exactly the one file named in your prompt, no other file, no search"; apply B1-B3 mechanically, one claim at a time; facts marked `verified` are true, facts marked `unverified` are the reviewer's assertion: grade as if true and say `unverified fact` in `why`; never use outside knowledge to add or remove a fact; modes `grade` (reply `{"cid":"C3","blocking":true,"q2":"different","why":"..."}` per claim) and `audit` (claim plus 15 spec lines: reply `{"cid":"C3","real":true,"why":"..."}`; a hunk probe replies a list of claim objects or `[]`); reply only JSON lines, at most 25 words in `why`.

### 3.4 Tests

- `tests/skills/test_spec_panel_stoprule.py` (static; proves text exists): variant file present with `name: spec-panel-stoprule`; `## Review Loop` has eight bullets in order; `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` (imported from `tests.skills.test_review_severity_rule`) present; section names `stoprule.py`, `sc-spec-panel-stoprule-protocol`, `verdict: PASS`, `verdict: FAIL`; no `src/superclaude` in the command, SKILL.md, rubric or agent; `uv run --no-project python` form in SKILL.md; agent `tools:` equals `Read`; sha256 prefix of `refs/rubric.md` equals the pinned literal.
- `tests/skills/test_stoprule_script.py` (behaviour; the only tests that prove an enforcement): tmp_path fixtures for spec, baseline, ledgers. Cases: non-verbatim quote -> exit 3, then `minor-form` after the one repair; span present in baseline -> `late-found`; `prior` open exempts; uncovered hunk -> FAIL; unknown or missing `Cn` in a grader reply -> rejected; wrong canary -> batch rejected; two bad replies -> `unconfirmed` -> FAIL; verdict table (confirmed -> FAIL, none and all covered -> PASS); `begin` exit 4 on a prior `review: 3` FAIL; rubric hash mismatch exit 5; ledger line edited after `seal` -> `check` exit 6; `finalize` refuses a hand-typed `verdict:`; Escalation holds the canonical cap sentence; replay fixture built from ctl-r1 v2/v3 and the eight curated claims asserts the 5 novel / 3 non-novel split of section 5.
- Run, do not edit: `tests/skills/test_review_severity_rule.py` (its matchers scan spec-panel text; whether they glob the new file is UNVERIFIED), `tests/unit/test_cli_install.py` (lists command files at lines 118 and 404), `tests/recommend/test_routing_refresh.py` (line 137 asserts 47 commands; UNVERIFIED whether a new command changes it), `tests/skills/test_primitive_dual_surface_lookup.py`.

### 3.5 Docs and registration

New `docs/designs/spec-panel-stoprule.md` (this spec trimmed to the final decision). One sentence in `docs/designs/spec-panel-review-loop.md` section 11 pointing to it. No `HOW-WE-WORK.md` row, no `/sc:help` entry and no plugin mirror while the variant is experimental (so `plugins/superclaude/commands/spec-panel.md` and `tests/core/test_how_we_work_routing_table.py:1147` are untouched). After editing: `make sync-dev`, `make verify-sync`; stage `src/`, `tests/`, `docs/`, `.dev/tasks`; never `.claude/`.

### 3.6 Not changed

`src/superclaude/commands/spec-panel.md`, `~/.claude/commands/sc/spec-panel.md` (never edited; verified by sha256 before and after install), rf-qa agents, `confidence-calibrator`, `evidence-validator`, `sc-implement-protocol`, `WORKER-CONTRACT.md`.

## 4. Variant command name and install note

Names: command `spec-panel-stoprule` (invoked `/sc:spec-panel-stoprule`, or `Skill sc:spec-panel-stoprule` from a worker's top level as WC-7 requires); skill `sc-spec-panel-stoprule-protocol`; agent `finding-grader`. A worker loads commands from `~/.claude/commands/sc/` first, so the new name never competes with `spec-panel.md`.

Install, repo route: `uv run superclaude install` without `--force`. `install_commands.py:56-80` skips existing command files and copies new ones, so `spec-panel.md` is not touched; that skipping applies to commands as read; the same behaviour for skills and agents is UNVERIFIED, so the experiment uses the manual route. Never pass `--force`: it would overwrite `spec-panel.md` and every other command.

Install, experiment route (three copies, no overwrite of any existing file):
```
sha256sum ~/.claude/commands/sc/spec-panel.md > /tmp/spec-panel.before
cp <variant dir>/spec-panel-stoprule.md ~/.claude/commands/sc/spec-panel-stoprule.md
cp -r <variant dir>/sc-spec-panel-stoprule-protocol ~/.claude/skills/
cp <variant dir>/finding-grader.md ~/.claude/agents/finding-grader.md
sha256sum -c /tmp/spec-panel.before          # must print OK: the original command is unchanged
```
The measurement copy of the command is the Arm B base file (472 lines, sha256[:12] `c8d80346a96c`) plus the section 3.1 edits, so the only difference between arms is the stoprule change. Record the sha256 of all three installed items in the run log, as the install watcher did for Arm B.

One-line substitution for an experiment brief (idempotent; covers `/sc:spec-panel ...` and `Skill sc:spec-panel`, skips a name already suffixed):
```
perl -pe 's#(/?sc:spec-panel)(?![-\w])#$1-stoprule#g' brief.md > brief.stoprule.md
```
Check: `grep -c 'spec-panel-stoprule' brief.stoprule.md` equals `grep -c 'sc:spec-panel' brief.md`. The review 2 and review 3 briefs must be the Arm B briefs (they pass `--re-review <prior> --baseline <saved copy>`); with the treatment-A briefs (no flags) the ratchet and hunk coverage are off (`ratchet=off` in the sentinel) and only the quote, grader, verdict and cap parts are measured. Removal: delete the three installed paths.

## 5. Measurement plan on scenario S1

### 5.1 How the prediction was counted (offline replay of the filters on the two real R3 reports I may read)

Mechanical tests were run on the real files: the reviewer's quoted defect text (`span`) searched in `specs/history/spec-v3-after-round2.md` (the text R3 reviewed; byte-identical to the final spec) and in `spec-v2-after-round1.md` (the baseline), whitespace-normalised. Grader columns are my judgement, not a measurement.

| ctl-r1 R3 id (`spec-panel-round3.md:181-189`) | Quote + outcome as written | `span` (from the report) | In baseline v2? | Ratchet | P(grader confirms) | Expected |
|---|---|---|---|---|---|---|
| R3-1 adapter not total | yes (`SPEC:64`) | "is total: every own value a command documents today has a row" | no (11 of 12 tokens changed) | anchored; prior N1 | 0.9 | 0.9 |
| R3-2 verdict rules misattributed | yes (`SPEC:88`) | "the rule tasklist's reflect gate already applies" | no | anchored; prior N2 | 0.6 (Fowler would grade it minor, line 169) | 0.6 |
| R3-3 `find -newer` lists caches | paraphrase, one repair | "every file created or modified since step 0, tracked, untracked or gitignored" | no | anchored; prior N3 | 0.8 | 0.8 |
| R3-4 AC-2.2 unpassable for 6 commands | yes (`SPEC:245`) | "Gate-trigger run per P2 command" | YES | `late-found` (N5 is resolved, no exemption) | - | 0 |
| R3-5 P0 worker block | yes (`SPEC:75`) | "the only carrier" | no | anchored; prior N6 | 0.9 | 0.9 |
| R3-6 P0 install gate | yes (`SPEC:179`) | "only confirms the installed copies match" | no | anchored; prior N7 | 0.9 | 0.9 |
| R3-8 `master...HEAD` vacuous | paraphrase, one repair | `master...HEAD` | YES (v2 lines 177, 204; the report says so at 188) | `late-found`; if the reviewer picks the longer span with the new flag, the span is novel and Q2 (baseline gives the same outcome) demotes it, p about 0.7 | - | 0.2 |
| R3-9 adversarial file undefined | yes (`SPEC:238`) | "the command's existing report file" | YES (two lines) | `late-found` (M2 resolved) | - | 0 |
| **Total** | 6 of 8 pass as written, 8 of 8 after repair | | 3 of 8 in baseline | 5 anchored | | **4.3 of 8** |

flg-r2 R3 (`spec-panel-round3.md:84-89`): one blocking finding, N12; quote "the session-name question appears in that worker's `worker-read` output" is on `SPEC:220`, a line in the changed-line list (line 25); span absent from the baseline; outcome concrete (every correct launcher run recorded "WC-1 not exercised"). Expected 0.85 of 1.

Reading of the count: the filters remove about 43% of the blockers the two reports carried (9 raw, 5.2 expected). They remove late-found items completely (3 of 8 in ctl-r1) and almost none of the fix-written ones, which is what section 1 predicted. On a control-style report (8 raw) the result stays above the bar (4.3 > 3); the bar needs the 427-style report plus the filters, as below. Gate before any live run: replay all six existing R3 reports through the script and the grader; my reading finds all 9 counted claims rubric-blocking, so a grader that demotes more than 3 of those 9 is miscalibrated and is fixed first.

### 5.2 Live design

Scenario S1 (Orca worker-contract spec, 57,763 bytes, base commit 2cb683f5), the Arm B briefs with the section 4 substitution, same reviewer and reviser model as AB/ARMB (claude-opus-5-5), same loop (3 reviews, 2 fix cycles), n = 2, the variant installed per section 4. One fresh Arm B replicate pair in the same time window is optional (control and Arm B were not run concurrently before). Metrics, all read from files:
- M1 R3 open confirmed critical+major = sentinel `confirmed` plus unresolved priors in the R3 report (script-computed). M1b the recorders' old proxy on the report body. M1c probe proxy: one unmodified 427 `/sc:spec-panel` review (fresh session, same brief form) of the spec after fix cycle 2, counted with the old method. M1c is the guard against a mechanism that only filters.
- M2 growth in bytes after fix cycles 1 and 2 (same `wc -c` method as AB-REPORT). M3 compliance: every review has a sentinel, a sealed ledger and `check` exit 0. M4 audit: `sampled`, `contested`, false-demotion rate = contested/sampled. M5 reviser leak: ids applied in `disposition-round2.md` that are not in the Reviser brief. M6 cost: Agent calls, Bash calls, wall time per review from transcripts. M7 PASS reached and at which review.

### 5.3 Predicted numbers (judgement from 5.1; the interval is what I would be surprised outside of)

| Metric | Control mean | 427 / Arm B | Predicted, this variant | Bar | Chance bar met |
|---|---|---|---|---|---|
| M1 R3 confirmed open | 6.0 | 5.5 / 3.5 (blocking 4 and 1) | r1 3, r2 1; mean 2.0 (each replicate 1-5) | <= 3 in both | about 0.5 |
| M1b old proxy on the report body | 6.0 | 5.5 / 3.5 | 3.0 (report labels follow computed statuses by construction, so it is no longer independent) | - | - |
| M1c probe proxy on the final spec | 6.0 | - | 4.5 (2-7); not distinguishable from 427 | no worse than 6.0 | about 0.8 |
| M2 growth after two cycles | 63.5% | 29.7% / 30.0% | 20% (r1 22%, r2 18%; 12-30%) | <= 44.4% | about 0.9 |
| M7 clean PASS by review 3 | none | none | about 0.2 per replicate | - | - |

Arithmetic: M1 = Arm B's blocking counts (4, 1) times a survival rate between 0.55 (ctl-r1 style, 5.1) and 0.85 (flg-r2 style): 4 x 0.7 = 2.8, 1 x 0.85 = 0.9. Chance for r1 to stay at or under 3 with 4 candidates at 0.7: 1 - 0.7^4 = 0.76; the figure 0.5 for "both" discounts for the 427 population also containing 6-proxy reviews. M2: flg-r2 fix cycle 2 applied 15 findings (6 blocking, 9 minor; `disposition-round2.md:35`) and added about 10.5 points; cycle 1 added 21.6 points for 22 findings (proxy 17). Weighting a blocking edit as 2 units and a minor edit as 1: cycle 2 = 21 units, 0.5 points per unit; the variant applies about 4 confirmed items (8 units) = 4 points. Cycle 1 = 39 units, 0.55 per unit; the variant applies about 12 confirmed items (24 units) = 13 points. Sum 17, rounded up to 20% for the 427 base. Growth proportional to weighted applied volume is an assumption (UNVERIFIED); the bar has a wide margin, so the gain is only mildly sensitive to it.

### 5.4 What would falsify the idea (fixed before the run)

- F1 M1 is 4 or more in either replicate and M1c averages 5.5 or more: no convergence gain over 427; stop.
- F2 `contested / sampled` is 25% or more over at least 8 sampled demotions: the grader removes real defects; reject the grader (the script and cap parts may stay).
- F3 a review ends PASS and the probe review finds 3 or more claims that meet B1-B3 on the final spec: the computed PASS is hollow.
- F4 fewer than all reviews carry a sentinel with `check` exit 0: the mechanism is prose in practice; the headline claim is void.
- F5 growth above 30% in either replicate: no growth gain over 427.
- F6 two or more applied ids per cycle outside the Reviser brief: separating the notes did not stop minor edits.
- F7 more than 25 minutes added per review: not usable as a default.

## 6. Risks, costs, and ways it could make the loop worse

### 6.1 Cost per review and per loop (estimates; wall time and tokens are UNVERIFIED until the live run, M6 measures them)

| Item | Per review | Per loop (3 reviews) |
|---|---|---|
| Script calls (`begin`, `seal` 1-2, `grade-prep`, `apply-grades` 1-2, `audit-prep`, `apply-audit`, `status`, `finalize`, `check`) | 9-11 Bash calls, about 1-2 s each | 27-33 |
| Agent calls (1-2 grader batches of at most 6 claims + 2 canaries, 1 audit, 0-1 rerun) | 2-4 | 6-12 (median 8) |
| Write/Edit calls (ledger, repair edit, saved grader replies) | 3-5 | 9-15 |
| Extra Orca sessions | 0 (grader and auditor are subagents of the reviewer session) | 0 in the loop; +1 probe session per replicate in the experiment only |
| Wall time added | 6-10 min: ledger authoring 2-4, grader 1, audit 1-3, scripts under 1 | 18-30 min |
| Tokens added | about 30-40k (ledger 8k out, grader 2 x 5k, audit 10k, script output 5k) | 90-120k |

Break-even view: the loop already costs 3 review sessions and 2 reviser sessions; this adds about 15-20 tool calls and 2-4 subagent calls to each review and no session.

### 6.2 Ways it could make the loop worse (each with its check)

1. Effort moves from finding to form. A reviewer that spends its budget on the ledger finds fewer true defects, and the computed PASS follows. Checks: hunk coverage (every changed hunk needs a claim or a `checked` line), the hunk probe in the audit, and M1c, the unmodified probe review of the final spec.
2. The quote rule structurally demotes defects of omission. A missing rule has no offending text to quote; only a claim sentence the omission falsifies (as R3-1's "is total") can be quoted. Pure omissions become minor. Residual risk, not fixed here; the escalation lists minor counts so the user can see them.
3. Late-found demotion hides real defects the first reviews missed (3 of 8 in ctl-r1, all real). Bounds: they are listed in every report that has them, including a PASS ("PASS with known debt"), and the user sees them at the cap; the audit samples them. The cost is that the loop never fixes them; that is the stated trade.
4. The grader is wrong in a patterned way. A sonnet grader may demote cross-reference defects it cannot verify (R3-2 is the example). Canaries test only easy cases. The audit measures the effect (F2) but does not prevent it for the demotions it does not sample on a FAIL path (all but 3 per review).
5. Independence is partial. Same vendor, similar training, and the model-class choice is an instruction the model follows, not something the script can check (UNVERIFIED that the Agent tool honours `model` inside a dispatched worker). The input builder is mechanical; "fresh context" holds because a subagent does not inherit the report, and a grader that opens other files is a prose violation.
6. The ledger seal is tamper-evidence, not security. One session writes the ledger, runs `finalize` and could skip the script. Defence: a missing sentinel is visible to the coordinator's `check` and to M3; there is no mechanical way to force a session to call the script, and I do not claim one.
7. Prose obedience is the largest residual: the reviewer must run the steps, the reviser must read only the brief, the grader must stay within its file. ARMB-REPORT point 2 shows reviewers obey format rules of this kind when asked (both Arm B R2 and R3 reports honour the status table, `origin=` tags and `review: N of 3`), which is supporting evidence for format, not for restraint. Tests of prose prove the text exists; only `test_stoprule_script.py` proves behaviour, and only of the script.
8. The gaming risk of the headline number: M1 is an output of the mechanism. That is why M1c exists and why F1 and F3 are stated against it.
9. Interaction with the S1 briefs. They allow the reviewer to write only the report; the scratch dir is outside the repo, but a worker sandbox that blocks `/tmp` would break S0 (fail closed: exit 5 and the review stops). The Orca step-6 changed-files check sees only the report.
10. Maintenance: 6 installed files (command, SKILL.md, rubric, canaries, script, agent), 2 test files, a 380-line script, one new agent. It is additive, so removing the variant is deleting three installed paths.

## 7. Open questions

1. Is the "span absent from the baseline" ratchet too hard? It demotes R3-4 and R3-9, which are real defects found late. The softer rule (demote only when Q2 says the baseline gives the same outcome) would keep them if the grader says `different`, at the price of a second semantic gate on the ratchet. I chose the mechanical rule because the data show that 427's reviewer-tagged anchor (`origin=changed|unchanged`) passed 89% (R2) and 100% (R3) of new findings; a judged anchor is the thing already measured to be weak.
2. Should an audit disagreement ever promote a demotion outside a PASS candidate? As written it only counts (a measurement) on a FAIL path. Promoting there makes the verdict depend on which demotions the seed sampled; not promoting leaves some real defects unreported until the cap. The owner may prefer the opposite.
3. One grader call per batch of claims or one per claim? Batches are cheaper and share anchoring across claims; the shuffle and canaries only partly reduce it. Per-claim calls would cost about 6-10 calls per review. Not measured.
4. Does the Agent tool honour `model:` inside a dispatched Orca worker, and may a worker write under `/tmp`? Both UNVERIFIED; if not, the class-difference rule falls back to prose and the scratch dir moves under the report's directory (which contradicts the briefs' write-only-the-report rule).
5. The override of FR-8/FR-9 happens only in the variant's Review Loop. Whether the owner accepts "a GAP row is a candidate, not an automatic MAJOR" for the shared command later is a product decision; this variant does not touch `spec-panel.md`.
6. The `sites` field widens a fix from "the quoted text" to "every listed site of the defect". It targets the partial-fix residue (5 of 8 in ctl-r1) but it may raise growth. M2 and F5 will show it; if growth rises, drop `sites` first.
7. Should a stall (confirmed count not lower than last review) halt early? 427's design left a monotonic halt out as overlapping the cap (`spec-panel-review-loop.md:154`). Here it is only reported. An early halt would save a fix cycle but would change the canonical cap meaning.
8. Base file: master's `spec-panel.md` has 14 more lines (`## Unattended mode`) than the 472-line file the arms used. The measurement copy uses the arm's file; the repo copy uses master. Is one more copy of the Unattended section acceptable, or should the variant inherit it by reference?
9. Does `--mode discussion` or `socratic` need the ledger? As written, no: critique mode only, as 427 bullet 1.

## 8. Reuse by other review commands

What transfers is the script and the three schemas (claim, grade, verdict), not the rubric text: each reviewer family needs its own rubric file with its own hash. The script takes `--rubric` and `--cap` so the same code serves other loops.

| Consumer | What it reuses | What it must change or keep | Residual |
|---|---|---|---|
| `/sc:reflect` (reflect-reviewer, Tier 2 merge, evidence-validator gate) | `verdict`/`check` over a claim ledger; the `finding-grader` agent as one more blind calibrator; the citation read-back (`seal`) in place of part of what `evidence-validator` does by prose | Keep its 4-category deviation taxonomy (Authorized expansion / Necessary deviation / Drift / Regression): it is a classification, not a severity, so the B1-B3 rubric does not apply; keep heterogeneous reviewers | reflect already has a heterogeneous ensemble and a validator; the added value is the computed verdict and the frozen hash, not a new judge |
| rf-qa agents (Fix Cycle) | `begin` cap and count enforcement (`--cap`), the sealed ledger, the Reviser brief generator | rf-qa fixes in place and has its own cap; the reviser is the same agent, so "reviser sees only the brief" is weaker there | prose obedience again; rf-qa tools include Write, so a separate grader session is advisable |
| `/sc:implement` final review | The ratchet idea and `escalation` format only | Do not add a second model pass: `qa.md:79` rules it out and derives severity from four yes/no answers with parent Read-back, which is already mechanical for code; its `late` blockers still block (`qa.md:167`), so keep that rule | The opposite design choice, deliberately: implement has tests and ACs to anchor on, a planning spec does not |
| `/sc:implement`, borrowed back | Its four-answer derivation could replace Q1 for the defect kinds (a) and (b) here, where the proof is two quotes or a quote plus a source line | A variant that confirms (a) and (b) by read-back only and calls the grader for (c)-(e) would cut grader calls | Presence of two quotes does not prove they contradict; a judge is still needed |
