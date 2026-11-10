review: 3 of 3

# Spec-panel critique: orca-worker-contract-spec.md (review 3 of 3, re-review, cap reached)

- candidate (SPEC): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (sha256 `e9171857b793b520e3e6291ce69b77aaa2e13a035d1f119ba47eb5a42eff8f83`)
- baseline (V2): `.dev/orca-command-refactor/specs/history/spec-v2.md` (sha256 `24081c933a7fbedd6b461f8f09d06fe7d90105a4b5e12f7221ed9cf63dc4b40e`)
- prior report (R2): `.dev/orca-command-refactor/review/round2.md` (sha256 `42d402d48c015919933628b10ba0cb096be547332490d42264ee9833434b5032`), header `review: 2 of 3`, final line `verdict: FAIL`. Review number N = 2 + 1 = 3. The prior report has the `review: N of 3` header, and N is below the cap, so this run reviews.
- reviewer model: claude-haiku-5-5
- command: `/sc:spec-panel --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2.md`; prompt: RE-REVIEW from `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full (sandbox copy `home/.claude/rules/prompts/document_review_loop_prompts.md`, sha256 `3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8`).
- rf-qa.md: neither `.claude/agents/rf-qa.md` nor `~/.claude/agents/rf-qa.md` exists in the sandbox (`home/.claude/` holds only `rules/`; no `ws/.claude/`), so the re-check rules in this report stand alone (review-loop bullet 5).
- WORKER-CONTRACT.md: not read. The run has no `--unattended` flag, so the Unattended mode section of `command.md` does not apply.
- Baseline note: R2 names `spec-v1.md` as its baseline and records the candidate hash `24081c...`. That hash is the SHA-256 of `spec-v2.md` (the text R2 actually reviewed). This report uses the values in the brief: baseline = `spec-v2.md`, prior = `round2.md`.
- Scope: `diff -w V2 SPEC` changes 2 lines: SPEC:194 and SPEC:195. This report covers those lines, the prior blocking findings of R2 (F-1 to F-6), and M-10 (carried from R2, re-graded here because its text is now in a changed line). It gives no whole-document assurance.
- Citation keys: paths are relative to the workspace root. `INV-A` = `.dev/orca-command-refactor/inventory/commands-a.md`, `INV-B` = `.../commands-b.md`, `CAPS` = `.../orca-capabilities.md`. `SPEC:N` = the candidate, which has the same line numbers as V2 for every line except 194 and 195. `sk/...` and `cmd/...` files are not in the workspace, so any citation to them is UNVERIFIED here.

## Step 1: evidence block

Command: `diff -w .dev/orca-command-refactor/specs/history/spec-v2.md .dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (exit 1; output is 194,195c194,195).

BEFORE (baseline), lines starting `<` (V2:194-195):

```
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; step 3 passes with this P0 variant [F-2]: `worker_done` arrives exactly once, its `--outcome` is WC-5 applied to the command's existing report (`failed` if that report's status is `failed` or `blocked` or no report exists, otherwise `succeeded`), and its `--report-path` names that existing report file; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `/sc:load` (WC-4 exception [F-3]) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate), lines starting `>` (SPEC:194-195):

```
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; step 3 passes with this P0 variant [F-2]: `worker_done` arrives exactly once, its `--outcome` is WC-5 applied to the command's existing report (`failed` if that report's status is `failed` or `blocked` or no report exists, otherwise `succeeded`), and its `--report-path` names that existing report file; step 4 is replaced by this P0 variant [F-5]: `test -s` on the command's existing report file (`.dev/tasks/to-do/<id>/return-contract.yaml` for `/sc:workflow`, INV-B:272; the report the run wrote under `<dir>` for `/sc:adversarial`, whose filename SPEC:83 leaves unfixed, so the phase report names it before step 3; `REPORT.md` for `/sc:troubleshoot`, where a `status` key is UNVERIFIED, `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`). Where that file has a `status` key, its value is one of `succeeded`, `partial`, `failed`, `blocked`. The `command` key is not asserted in P0: INV-B:272 lists none for workflow, and WC-4 adds it only in P1. Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command whose section 3 row names phase P1 (adversarial, analyze, build, business-panel, cleanup-audit, design, document, explain, index, index-repo, test, workflow) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`; that brainstorm and init-lite (no small fix, section 3.1) and `/sc:load` (WC-4 exception [F-3]) have none; and that no section-4 command has one. Each later phase's test asserts the section only for the commands that phase changes [F-6] | passes |
```

Self-check (run before the verdict, whole-line fixed-string match with `grep -nxF`): the 2 AFTER lines were found once each in SPEC (194, 195), and the 2 BEFORE lines were found once each in V2 (194, 195). Cross-check: 0 BEFORE lines appear in SPEC and 0 AFTER lines appear in V2. The roles are correct, so no swap was made.

## Prior blocking findings (R2)

| id | R2 status | this review | basis |
|---|---|---|---|
| F-1 | resolved | resolved | SPEC:73 is unchanged and still says P0 briefs omit `--unattended`. It matches SPEC:158, SPEC:194 (no flag) and the §3.1 brief column (SPEC:79-92). No regression. |
| F-2 | resolved | resolved | SPEC:194 keeps the P0 step-3 variant (`worker_done` outcome from the command's existing report, WC-5 applied). No regression. |
| F-3 | resolved | resolved for the contract, reopened for the section (see F-7) | SPEC:62 (WC-4) and SPEC:266 keep the `/sc:load` contract exception. SPEC:195 keeps the exemption and now also states that `/sc:load` has no `## Unattended mode` section. That statement conflicts with SPEC:76 and SPEC:159 (see F-7). |
| F-4 | resolved | resolved | SPEC:122, SPEC:65 and SPEC:204 are unchanged and still match R2's resolution. No regression. |
| F-5 | open | resolved | Defect: P0 step 4 asserted `d['command']` on the workflow contract, which INV-B:272 does not list (`INV-B:272`: contract 1.1 carries `status`, `plan_path`, `reflect_report_path`), and step 4 had no path for adversarial (SPEC:83, "filename not fixed"). The new SPEC:194 replaces step 4 with `test -s` on the command's existing report, names a per-command path (adversarial: the file the run wrote, named in the phase report before step 3), and drops the `command` assertion in P0. The residual four-value `status` assertion is carried as M-8 (Follow-up candidates). |
| F-6 | open | open (partly fixed) | R2's defect: AC-1.1 required a `## Unattended mode` section for every §3.1-3.2 command, including P2-P4 commands and brainstorm/init-lite, which have no section by design. The new SPEC:195 limits the test to the P1 rows. Checked against the §3 rows: the 12 P1 commands match SPEC:83, 85, 86, 92 (§3.1) and SPEC:99, 101, 102, 106, 107, 108, 111, 123 (§3.2). The P2-P4 commands are excluded. That part is fixed. R2's recommendation also said to state in §3.1 whether brainstorm and init-lite gain a section. SPEC:84 and SPEC:87 are unchanged, and SPEC:159 requires the flag for them, so the contradiction remains. It is reported as F-7. |
| M-10 | Medium (R2) | blocking, merged into F-7 | Re-graded here. R2 graded it Medium because it read as a missing requirement. The candidate now asserts "/sc:load ... have none" in SPEC:195, which contradicts SPEC:76 and SPEC:159 in a test (see F-7). |

Regressed: none. Every resolved finding (F-1 to F-5) still matches its own defect in the candidate.

## New findings (origin = changed unless marked)

### F-7 [BLOCKING] AC-1.1 (SPEC:195) says brainstorm, init-lite and `/sc:load` have no `## Unattended mode` section, but the spec requires one for them

- Text (changed line, SPEC:195): "that brainstorm and init-lite (no small fix, section 3.1) and `/sc:load` (WC-4 exception [F-3]) have none".
- Conflicting stated texts:
  - SPEC:76 (unchanged): "Every changed command also gains the `## Unattended mode` section".
  - SPEC:159 (unchanged), P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". That covers brainstorm (SPEC:84) and init-lite (SPEC:87). P1 also lists `load (usage line only)`, so load is a changed command.
  - SPEC:112 (unchanged): the load row changes its Usage line in P1.
  - SPEC:79 (unchanged): "The only command changes are the small fixes in the last column", and the last column for brainstorm and init-lite is "None". That contradicts SPEC:159 for both commands.
- Grading sentences:
  - brainstorm and init-lite: "An implementer who follows SPEC:159 adds `--unattended` to brainstorm; SPEC:76 then requires the changed command to gain a section, and AC-1.1 (SPEC:195) asserts it has none, so the P1 gate fails. An implementer who follows SPEC:79 and SPEC:84 (no change) breaks SPEC:159." No guess is needed: both readings break a stated text.
  - `/sc:load`: "An implementer who follows SPEC:159 and SPEC:112 changes the load Usage line; SPEC:76 then requires the section, and AC-1.1 (SPEC:195) says load has none, so the P1 gate fails."
- Blocking basis: an acceptance criterion (SPEC:195) cannot pass when the stated texts it depends on (SPEC:76, SPEC:159) are followed, and the two stated texts contradict each other.
- Origin: SPEC:195 changed (the explicit "have none" assertions are new in this revision). SPEC:76, 79, 84, 87, 112 and 159 are unchanged. R2 graded the `/sc:load` part of this as M-10 (Medium); this review re-grades it. The brainstorm and init-lite part is a continuation of R2's F-6 recommendation.
- Recommendation for the coordinator (the reviser brief is omitted at review 3, see Escalation): decide whether brainstorm, init-lite and `/sc:load` gain the section (or whether SPEC:159 stops requiring the flag for brainstorm and init-lite), then state the decision once in §3.1 and make SPEC:76, SPEC:159, SPEC:195 agree with it.

### M-8 (origin = changed dependency, graded Medium) SPEC:194 asserts the four-value status set on existing report files, and adversarial's values are not known

- Text (SPEC:194): "Where that file has a `status` key, its value is one of `succeeded`, `partial`, `failed`, `blocked`."
- Evidence: `INV-A:35` gives the adversarial contract's path and field evidence, but no status vocabulary. The adversarial report file is not fixed (SPEC:83). The adversarial skill is not in the workspace, so its status values are UNVERIFIED.
- Grading sentence: "An implementer who runs the adversarial P0 check gets a value that is outside the four, and the spec states no mapping for it." That needs an assumption about the adversarial file, so it is Medium (a requirement the spec does not state, not a wrong outcome).
- Carried from R2 as M-8 and relevant to F-5.

## Guard Condition Boundary Table (changed guards only)

Triggered by the changed lines: the P0 step-4 `test -s` guard and the `status` assertion (SPEC:194), and the AC-1.1 membership and exemption rules (SPEC:195). Input classes with no meaningful value are left out with the reason given in the row.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| P0 step-4 `test -s` | SPEC:194 | Zero/Empty: existing report missing or 0 bytes | `0` bytes, no file | exit 1 | the gate fails; the pass condition is implied, not restated in the replaced step | OK (the implicit pass condition is noted, not graded) |
| P0 step-4 `status` assertion | SPEC:194 | Sentinel Value Match: `status` outside the four values | `complete` (example; adversarial values UNVERIFIED) | assertion fails | not specified | GAP (M-8, Medium) |
| P0 step-4 `status` assertion | SPEC:194 | Legitimate Edge: file has no `status` key (troubleshoot `REPORT.md`) | no key | conditional pass | "Where that file has a `status` key" | OK (key UNVERIFIED, `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`) |
| P0 step-4 path | SPEC:194 | Typical: workflow package contract | `.dev/tasks/to-do/<id>/return-contract.yaml` | `test -s` | INV-B:272 | OK |
| AC-1.1 P1 membership | SPEC:195 vs §3 rows | Typical: the 12 P1 commands | adversarial, analyze, build, business-panel, cleanup-audit, design, document, explain, index, index-repo, test, workflow | match | SPEC:83, 85, 86, 92, 99, 101, 102, 106, 107, 108, 111, 123 | OK |
| AC-1.1 exemption, `/sc:load` | SPEC:195, SPEC:76 | Legitimate Edge: load changed in P1 (usage line) | usage-line edit | section required by SPEC:76, asserted absent by SPEC:195 | contradictory | GAP (F-7) |
| AC-1.1 exemption, brainstorm/init-lite | SPEC:195, SPEC:159 | Legitimate Edge: no small fix, but flag required by SPEC:159 | flag added | section required by SPEC:76, asserted absent by SPEC:195 | contradictory | GAP (F-7) |

Pipeline Dimensional Analysis: not triggered on the changed lines. They describe no multi-stage data transformation whose count can change.

## Escalation to the user (review: 3 of 3, no further review)

This is review 3 of 3, the cap. The verdict is FAIL with open blocking findings, so the run escalates instead of issuing a Reviser brief (review-loop bullet 4 and bullet 6).

Open blocking findings for the user:
1. F-6 (partly fixed): brainstorm and init-lite need a decision on whether they gain the `## Unattended mode` section. §3.1 (SPEC:84, SPEC:87) and SPEC:159 have to say the same thing. See F-7.
2. F-7 (new, and M-10 re-graded): `/sc:load`, brainstorm and init-lite are asserted to have no section in SPEC:195, which contradicts SPEC:76 and SPEC:159. See F-7.

Resolved in this review: F-1, F-2, F-3 (contract side), F-4 and F-5.

## Follow-up candidates (Medium and minor, not blocking)

The coordinator should ask the user once whether to open issues for these. Under bullet 3 the user is asked once per loop; the list is recorded only.

- M-8 unmapped `status` values; SPEC:194 now asserts the four-value set (origin = changed, see above).
- Carried from R1 and R2, origin = unchanged, not re-graded here (minor notes unless a changed line depends on them):
  - M-1 P1 `--unattended` on gated outward commands (SPEC:159, SPEC:67)
  - M-2 retry output directory (SPEC:64, SPEC:73)
  - M-3 WC-4 presents an unverified fact as settled (SPEC:62, SPEC:274)
  - M-4 P3 run classed as nested-only but cited as direct (SPEC:43, SPEC:23, INV-A:13)
  - M-5 cli-eval safety flags undefined (SPEC:104, SPEC:200)
  - M-6 `partial` and dependent Tasks (SPEC:63, SPEC:263, SPEC:73, CAPS:77, CAPS:84-86)
  - M-7 `\|` in AC-C1 and AC-C5 (SPEC:172, SPEC:176)
  - M-9 gates with no flag name (SPEC:61, SPEC:60, SPEC:103, SPEC:110, SPEC:122)
  - m-1 300-second wait boundary (SPEC:68)
  - m-2 "ready today" heading (SPEC:78-79)
  - m-3 citations outside the workspace remain UNVERIFIED
  - m-4 WC-7 states "cannot send `ask`" as settled, although SPEC:276 lists it as UNVERIFIED (SPEC:65, SPEC:276)
  - m-5 AC-2.6 assumes subagent output reaches the worker transcript (SPEC:204, SPEC:184)

## Coverage

Changed lines SPEC:194 and SPEC:195 (against V2), the R2 blocking findings F-1 to F-6, and M-10. Whole-document assurance is not given. Citations to `sk/`, `cmd/` and `src/` files were not checked and are UNVERIFIED.

verdict: FAIL
