review: 3 of 3

# Spec-panel critique: Orca worker-contract spec, round 3 (re-review)

- candidate (CANDIDATE, `SPEC:n`): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (291 lines; sha256 `5dc5c21ad2cf82fb9524020aa4cd5b0bc6a285be451e62fe6377194b27c70222`)
- baseline (BASELINE, `BASE:n`): `.dev/orca-command-refactor/specs/history/spec-v2.md` (291 lines; sha256 `013a84aaca6a86058868c7f7b79fe52a951e5bbb08547665cff18e7d59d845ed`, the same hash round 2 recorded for its candidate)
- prior report (PRIOR, `R2:n`): `.dev/orca-command-refactor/review/round2.md` (194 lines; sha256 `3ba76d94185b6ed74b7207c89de9a3d71d721a4fab1a5400bd737c04eac31dd2`; `review: 2 of 3`, `verdict: FAIL`)
- mode: critique; focus: requirements, architecture; format: standard; re-review of round 2
- reviewer model used: claude-haiku-5-5
- review prompt: RE-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox copy `home/.claude/rules/prompts/document_review_loop_prompts.md`, read in full, sha256 `3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8`)
- review number: prior report is `review: 2 of 3`, so this is `review: 3 of 3`. This is the last permitted review. Any open blocking finding escalates to the user and starts no fourth review.
- rf-qa process (command step 5): neither `.claude/agents/rf-qa.md` nor `~/.claude/agents/rf-qa.md` is in the sandbox, so the rules in the command's Review Loop section stand alone.
- shared rules: `~/.claude/WORKER-CONTRACT.md` is not in the sandbox. It governs `--unattended` runs only, and this run is not one.
- citation rule: a citation is "checked" when its target is a file inside the workspace (`.dev/orca-command-refactor/`) and I read the cited line. Citations to `src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `pyproject.toml`, `CLAUDE.md`, `~/.claude/` and Orca's installed files are outside the workspace and are UNVERIFIED in this run.
- git: the workspace is not a git repository (`fatal: not a git repository`), so the `git status --short` rule has no tracked files to check. No file other than this report was written.
- no revised specification was written: this is a re-review, so `--iterations` is ignored and the Improve step is skipped.

## Coverage

Read in full: CANDIDATE, BASELINE, PRIOR, the review-loop prompt file, the README (binding shared context), and `command.md`. Inventory lines checked: `inventory/commands-a.md:35,60,85` and `inventory/commands-b.md:36,242,268,272,275`. Checks run in the sandbox:

- Step 1 evidence block (below) from `diff -w BASELINE CANDIDATE`. The diff has three hunks: `85`, `189` and `200`.
- Self-check: `grep -cF` on each AFTER line (`>`) in CANDIDATE and each BEFORE line (`<`) in BASELINE returned `1` for all six quotes, so the roles are not swapped.
- Hash check: the BASELINE hash equals the hash round 2 recorded for its CANDIDATE, so the baseline is the text round 2 reviewed.
- Not re-read: the inventory files other than the lines listed above, and the spec's unchanged sections, except where a changed line depends on them.
- Guard Condition Boundary Table: the spec contains no guard table, and no changed line adds one, so FR-8 to FR-10 do not apply to this round.

## Step 1: evidence block (diff -w BASELINE CANDIDATE, verbatim)

`<` lines are BEFORE (baseline). `>` lines are AFTER (candidate). Hunk headers are kept.

```text
85c85
< | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report and write `return-contract.yaml` beside it. The output dir is fixed today, so under `--unattended` the output path carries a per-run slug the coordinator passes; two runs in one worktree then never share `progress.json` (WC-11) (P1; F-03, F-04) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
---
> | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | A single-pass run (`--pass <N>`) writes `return-contract.yaml` beside its `pass<N>-summary.md`; `--pass all` writes it beside the final report (F-03). The output dir is fixed today, so under `--unattended` the output path carries a per-run slug the coordinator passes; two runs in one worktree then never share `progress.json` (WC-11) (P1; F-03, F-04) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
189c189
< 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
---
> 4. For a YAML contract only (`REPORT.md` is checked by AC-0.4 instead; F-01): `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
200c200
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; steps 3 and 4 check the command's existing report file (`REPORT.md` for troubleshoot, `.dev/tasks/to-do/<id>/return-contract.yaml` for workflow, the adversarial return contract as written today), because the WC-4 path check starts in P1 (F-01). Record the results in the phase report; a failure here reopens section 1 |
---
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; step 3 checks the command's existing report file, because the WC-4 path check starts in P1 (F-01). Step 4 runs only on YAML files: `.dev/tasks/to-do/<id>/return-contract.yaml` for workflow and the adversarial return contract as written today. For troubleshoot, step 4 is replaced by the check that `REPORT.md` exists and is non-empty (F-01; it is markdown, `SPEC:91`). Record the results in the phase report; a failure here reopens section 1 |
```

Changed-line map of CANDIDATE: `SPEC:85` (cleanup-audit row), `SPEC:189` (7.2 step 4), `SPEC:200` (AC-0.4).

## Prior blocking findings

| Prior id | Prior status | Now | Basis (AFTER text only) |
|---|---|---|---|
| F-01 | open (blocking) | **resolved** | `SPEC:189` now limits step 4 to YAML contracts ("For a YAML contract only"). `SPEC:200` replaces step 4 for troubleshoot with a check that `REPORT.md` exists and is non-empty, and `SPEC:91` says REPORT.md is markdown. No AFTER line asks a YAML assertion of a markdown file. The residual step-3 wording is carried as a Medium follow-up (see follow-ups), not a blocker. |
| F-02 | open (blocking) | **resolved** (unchanged) | `SPEC:172` and the block at `SPEC:178-183` are unchanged from `BASE:172` and `BASE:178-183`. The grep is plain alternation. |
| F-03 | open (blocking) | **resolved** | `SPEC:85` now says a single-pass run (`--pass <N>`) writes `return-contract.yaml` beside `pass<N>-summary.md`, and `--pass all` writes it beside the final report. The defect R2 named (a single-pass run with no contract location) is gone. The unnamed slug flag that remains is N-5 (Medium). |
| F-04 | open (blocking) | **resolved** (unchanged in substance) | `SPEC:85` still gives cleanup-audit a per-run slug under `--unattended`, and the statement "two runs in one worktree then never share `progress.json` (WC-11)" stands. The slug flag is N-5 (Medium). |

No prior blocking finding is `regressed`, and no prior finding is `open`.

## New and narrowed findings on changed lines

### N-5 (MEDIUM, follow-up; carried from R2, origin=changed): the cleanup-audit location has no flag and no WC-4 directory

- Location: `SPEC:85` (cleanup-audit row, "under `--unattended` the output path carries a per-run slug the coordinator passes") against `SPEC:62` (WC-4: `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)") and `SPEC:85` "Brief must pass" column (`--pass <N>` only).
- The row gives a single-pass location (`.claude-audit/pass<N>-summary.md`, beside which the contract goes) for standalone runs. Under `--unattended` the location depends on a slug whose flag the row and section 2.3 (`SPEC:73`) never name, and cleanup-audit has no `--output` flag, so WC-4's "directory the coordinator passed" has no value here.
- Sentence: "An implementer who dispatches cleanup-audit with `--pass <N> --unattended` cannot tell the coordinator where `return-contract.yaml` will be, because the slug flag is not stated." This needs a requirement the document never states (a flag name), so it is Medium under the Review Loop rule, not blocking.
- Origin: changed (`SPEC:85`).
- Expert: Fowler (interface contract coverage), Wiegers (each requirement needs an owner).

### N-6 (MEDIUM, follow-up; origin=changed): AC-0.4 step 4 applies the P1 `command` field to existing P0 contracts

- Location: `SPEC:189` (step 4 asserts `d['command']` and a four-value `status` set) and `SPEC:200` (step 4 is applied in P0 to `.dev/tasks/to-do/<id>/return-contract.yaml` for workflow and to the adversarial contract "as written today").
- The spec's own WC-4 (`SPEC:62`) says a command that already writes a contract "keep[s] its fields and add[s] the missing ones", and the workflow row (`SPEC:92`) and P1 (`SPEC:159`) add to workflow in P1. The inventory lists the workflow contract's fields as `status`, `plan_path` and `reflect_report_path` (`inventory/commands-b.md:272`), with no `command` field. Nothing in the workspace shows a `command` key or the status vocabulary of the existing workflow contract. The reference that would show it, `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41`, is outside the workspace and is UNVERIFIED.
- The grade is Medium, not blocking, because the sentence "the P0 workflow contract has no `command` key, so step 4 fails on a correct run" needs the inventory's field list to be complete, which the workspace cannot confirm. A P0 live run would settle it. If the key is absent, the step fails for a reason WC-4 assigns to P1, which would be a blocking defect in a later review.
- Origin: changed (`SPEC:200`, `SPEC:189`).
- Expert: Adzic (acceptance criteria that cannot pass), Nygard (gate reliability).

### N-7 (MEDIUM, follow-up; origin=changed): the adversarial contract path that step 4 tests is not fixed

- Location: `SPEC:200` ("the adversarial return contract as written today") against `SPEC:83` (adversarial row, "Fix the contract filename ... (P1)").
- The inventory records two locations for real runs: `<output>/adversarial/return-contract.yaml`, sometimes `.../adversarial/adversarial/return-contract.yaml` (`inventory/commands-a.md:35` and `inventory/commands-a.md:60`). Step 4 needs a concrete `test -s <contract>` path, and P0 has no fixed filename. The implementer must guess which of the two the run writes, which is Medium under the Review Loop rule.
- Origin: changed (`SPEC:200`); the filename fix it depends on is in P1 (`SPEC:83`).

### Sentence-level note on F-01 (MEDIUM, follow-up; origin=unchanged text, depends on changed `SPEC:200`): step 3 still names the contract for its outcome in P0

- Location: `SPEC:188` ("its `--outcome` matches the contract's `status` under WC-5") against `SPEC:200` ("step 3 checks the command's existing report file"). For troubleshoot in P0 there is no contract (`inventory/commands-b.md:242`: `return-contract.yaml` only with `--caller task-unified`), so the clause does not say what the outcome is compared with.
- The reading "compare with the report's status line" is likely, but the text does not state it. Medium, as R2 graded it.

## Unchanged findings (origin=unchanged; minor notes unless they quote a changed line)

No changed line in this round touches the R1 findings F-05 to F-20, except where listed under follow-up candidates. None of them is re-graded to blocking.

## follow-up candidates (Medium and minor; not blocking)

- N-5 cleanup-audit slug flag and WC-4 directory (`SPEC:85`, `SPEC:62`, `SPEC:73`; origin=changed)
- N-6 AC-0.4 step 4 `command` field and status set on the P0 workflow contract (`SPEC:189`, `SPEC:200`, `SPEC:62`; origin=changed; UNVERIFIED against `sk/sc-workflow-protocol/refs/return-contract.md`)
- N-7 adversarial contract path not fixed before P1 (`SPEC:200`, `SPEC:83`; origin=changed)
- step 3 outcome clause for P0 troubleshoot (`SPEC:188`, `SPEC:200`; origin=unchanged, depends on changed `SPEC:200`)
- R2 Medium items carried without change: N-1 (`SPEC:62`, `SPEC:87`, `SPEC:90`), N-2 (`SPEC:62`, `SPEC:112`), N-3 (`SPEC:91`), F-05 to F-20 as listed in `review/round2.md:166-185`. Their status is unchanged from R2.

The session that ran this review asks the user once per loop whether to open an issue for the follow-up candidates above. This worker has no user and creates no issue.

## Reviser brief

Not applicable. No blocking finding is open, so no brief is written. (At `review: 3` a brief is omitted in any case, because the run escalates instead.)

Coverage line: `scoped PASS: changed lines + prior blockers`

verdict: PASS
