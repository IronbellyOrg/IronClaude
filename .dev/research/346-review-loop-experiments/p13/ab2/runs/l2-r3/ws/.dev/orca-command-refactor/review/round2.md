review: 2 of 3

# Spec-panel re-review: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `032a73216d9fa2a2e58b2be6fa0c2ed6374df75cb60076a9b7d7f4bd03d07a67` (`sha256sum`; equals the hash on `lint-2.md:1`)
- baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- prior report: `.dev/orca-command-refactor/review/round1.md`, sha256 `b6839f5d601529e0126b171a4303b348027904f9e188d18a0141b8f35bbf11ba`; its header is `review: 1 of 3` (round1.md:1), so N = 2. Its final line is `verdict: FAIL` at 1 of 3, so the cap check does not stop this run.
- lint: `.dev/orca-command-refactor/review/lint-2.md`, sha256 `ba62293f29c9033e132c6495b93b06957190e2b28cf33e2f635a7bfdeccdd114`
- reviewer model used: claude-sonnet-5-5
- prompt followed: RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full), plus Review Loop bullets 1-7 of `command.md:258-264`. The rf-qa Fix Cycle file is not in the sandbox, so its steps 1-5 are UNVERIFIED; the rules of the Review Loop section were applied standalone.
- citation key: `SPEC:N` = line N of the candidate; `BASE:N` = line N of the baseline (same numbering, no lines were added or removed); `INV-A:N`, `INV-B:N` = `inventory/commands-a.md`, `commands-b.md`; `R1:N` = `round1.md`. Any `cmd/`, `sk/`, `CLAUDE.md`, `src/` citation reached only through the spec or an inventory is UNVERIFIED.

## Lint evidence (lint-2.md)

Lint-2 has two findings (`lint-2.md:3`), both on lines the diff touches.

- LINT-REF-1 (line 62, "F-1 is referenced but never defined", `lint-2.md:7-11`): dismissed as a defect. The reference is the citation the reviser contract requires on every addition ("each added paragraph or table cites its finding id", `command.md:263`; Revise prompt "cite the finding id on every addition"). F-1 is defined in `R1:34-45`, not in the spec. Quote showing it is intended: `contract sits beside that file or in that fixed directory ... (F-1)` (SPEC:62). Minor note n-A below: the spec keeps dangling ids after the loop ends.
- LINT-REF-2 (line 159, "F-2 is referenced but never defined", `lint-2.md:13-17`): dismissed the same way; quote: `accepted by every command in sections 3.1 and 3.2 except /sc:load (F-2)` (SPEC:159). F-2 is defined at `R1:47-55`.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

`diff -w` reports 9 changed hunks at lines 62, 76, 85-87 (three lines), 90, 120, 159 and 195; nothing else. The AFTER quotes were found in the candidate with `grep -cF` (9 of 9 found) and the BEFORE quotes in the baseline (9 of 9 found), so roles are not swapped. Long lines are quoted in full-length excerpts that are verbatim substrings; unchanged tail cells are cut with `...` and the cut parts are identical on both sides.

BEFORE (baseline)
- BASE:62 `... the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use ...`
- BASE:76 `... "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). ...`
- BASE:85 `... Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) ...`
- BASE:86 `... | State the output location (P1) | ...`
- BASE:87 `... | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | ...`
- BASE:90 `... | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | ...`
- BASE:120 `| spec-panel | ... | add `--output`; contract | fresh dir | none | ...`
- BASE:159 `... the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); ...`
- BASE:195 `... asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` ...`

AFTER (candidate)
- SPEC:62 `... (`--output` / `--output-dir`). Where `--output` is a file, or the command's output location is fixed, the contract sits beside that file or in that fixed directory as named in the section 3 row (for a file: `<file stem>.return-contract.yaml` in the file's directory) (F-1). It follows the return-contract pattern ...`
- SPEC:76 `... "Contract" means the WC-4 file (path per the row where `--output` is a file or the location is fixed, F-1). Every changed command also gains the `## Unattended mode` section (section 2.1). ...`
- SPEC:85 `... (WC-11); contract at `.claude-audit/return-contract.yaml` (F-1) (P1) ...`
- SPEC:86 `... | State the output location; contract beside it as `PROJECT_INDEX.return-contract.yaml` (F-1) (P1) | ...`
- SPEC:87 `... | Contract beside the `--output` file as `<stem>.return-contract.yaml` (F-1) (P1) | ...`
- SPEC:90 `... | Contract beside the `--output` file as `<stem>.return-contract.yaml` (F-1). Under `--unattended`, the topic-only clarification ... (P2) | ...`
- SPEC:120 `| spec-panel | ... | add `--output <file>`; contract beside it as `<stem>.return-contract.yaml` (F-1) | fresh dir | none | ...`
- SPEC:159 `... the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `/sc:load` (F-2) (a no-op where a command has no gate); ...`
- SPEC:195 `... asserts that every command in sections 3.1-3.2 except `/sc:load` (F-2) has a `## Unattended mode` section naming `return-contract.yaml` ...`

## Prior blocking findings

| id | prior state | now | basis |
|---|---|---|---|
| F-1 | open (FAIL, R1:34-45) | resolved | The contradiction was SPEC:62 (`<output-dir>/return-contract.yaml`, `<output-dir>` = the `--output` value) against file-valued `--output` in tdd (SPEC:90; INV-B:222), init-lite (SPEC:87; INV-A:55), spec-panel (SPEC:120; INV-B:182) and the fixed locations of cleanup-audit (SPEC:85; INV-A:42) and index-repo (SPEC:86; INV-A:53). The AFTER text states one rule (SPEC:62) and gives each of the five rows an explicit path. The worked attack now yields: `/sc:tdd "auth" --unattended --output docs/x/TDD_FOO.md` writes `docs/x/TDD_FOO.return-contract.yaml`, a creatable path in an existing directory, so AC-2.2 (SPEC:200, `blocked` with a non-empty `blocked_question`) and the `test -s <contract>` step (SPEC:183) have a file to check. SPEC:76 no longer restates the old unconditional path. AFTER text is consistent with the requirements that depend on it: AC-1.1 and AC-1.4 grep for `return-contract.yaml` (SPEC:195, SPEC:198), a substring of `<stem>.return-contract.yaml`. |
| F-2 | open (FAIL, R1:47-55) | resolved | AC-1.1 (SPEC:195) and the P1 flag clause (SPEC:159) now exclude `/sc:load`, which matches SPEC:112 (no report file), SPEC:149 and the Decisions row (SPEC:265, `a report file would be an unrequested addition`). The test no longer demands an `## Unattended mode` section naming `return-contract.yaml` from load. |

Regressed: none. Deferred or withdrawn: none (`revise1.md` records both as applied).

## Findings on changed lines

Guard Condition Boundary Table, scoped to guards on changed lines (re-review rule, `command.md:262`). Guard: the WC-4 path rule at SPEC:62.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-4 path rule | SPEC:62 | Typical | `--output <dir>` (analyze, SPEC:99) | dir | `<dir>/return-contract.yaml` | OK |
| WC-4 path rule | SPEC:62, SPEC:90 | Legitimate Edge Case | `--output docs/x/TDD_FOO.md` | file | `docs/x/TDD_FOO.return-contract.yaml` | OK |
| WC-4 path rule | SPEC:62, SPEC:85 | Legitimate Edge Case | fixed directory (cleanup-audit) | fixed | `.claude-audit/return-contract.yaml` | OK |
| WC-4 path rule | SPEC:62, SPEC:87 | Zero/Empty | init-lite with no `--output` (its default is `.dev/superclaude/context-audit.md`, SPEC:87 col 3) | fixed default | row names only the "beside the `--output` file" case | GAP (Medium, M-A) |
| WC-4 path rule | SPEC:62 | Sentinel Value Match | `--output` file whose name already ends `.return-contract.yaml`, or two files with the same stem and different extensions in one directory (for example `X.md` and `X.json`) | unknown | not specified | GAP (Medium, M-B) |
| P1 flag clause | SPEC:159, SPEC:195 | Legitimate Edge Case | `/sc:load` | excluded | AC-1.1 excludes it; SPEC:76 still says every changed command gains the section | GAP (Medium, M-C) |

Omitted classes: WC-4 "One/Minimal" and "Maximum/Overflow" do not apply (the rule is a path template, not a bounded value); the P1 clause has no numeric guard. FR-8 and FR-9: no GAP row names a concrete wrong outcome that follows from the stated text with no further assumption, so none is blocking (grading below).

Whittaker, scoped to changed lines:
- Sentinel Collision Attack on SPEC:62: `<file stem>.return-contract.yaml` collides when two deliverables in one directory share a stem. Trace: coordinator dispatches two spec-panel Tasks with `--output docs/a/X.md` and `--output docs/a/X.json`; both write `docs/a/X.return-contract.yaml`, the second overwrites the first. The spec's own brief template already requires one path per Task known before dispatch (SPEC:73) and WC-6 forbids shared state (SPEC:64), so a coordinator that follows them picks distinct files. Needs the guess that a coordinator reuses a stem. Medium (M-B), origin=changed.
- Divergence Attack on SPEC:87: init-lite has an `--output` file case and a default case; the new cell covers one branch. Trace: `/sc:init-lite --unattended` with no `--output`; WC-4 says "known before dispatch" but the row gives no path, so the coordinator cannot name the `--report-path` before the run. The deliverable path default is known (SPEC:87 col 3) and `--dry-run` writes nothing (INV-A:55), so an implementer can derive a sibling name by the same rule. Needs a guess. Medium (M-A), origin=changed.

All new findings below have `origin=changed` unless marked.

## Synthesis

The two blocking findings of review 1 are fixed by narrowing edits on exactly the lines the findings named, with no new mechanism: one sentence in WC-4, five row cells, a reworded definition at SPEC:76, and one clause each in SPEC:159 and SPEC:195. The AFTER text is consistent with the lines that depend on it (AC-1.1, AC-1.4, AC-2.2, live-check step 4). Remaining gaps are requirements the spec does not state (an init-lite default, same-stem collisions, an inherited "every changed command" sentence), each needing a guess about which reading an implementer picks, so they are Medium. Expert consensus: close the loop; fix the Medium items in a later pass if wanted.

## follow-up candidates

Medium (warnings; none triggers a revision, none is in the Reviser brief):
- M-A (origin=changed, SPEC:87, SPEC:62): init-lite's row places the contract beside the `--output` file only; with no `--output` the report is the default `.dev/superclaude/context-audit.md` (SPEC:87 col 3; INV-A:55) and the contract path is unstated. tdd is not affected because its row requires `--output` (SPEC:90).
- M-B (origin=changed, SPEC:62): `<file stem>.return-contract.yaml` can collide for two deliverables with the same stem in one directory.
- M-C (origin=changed, SPEC:76 depends on SPEC:195 and SPEC:159): SPEC:76 says "Every changed command also gains the `## Unattended mode` section"; `/sc:load` is a changed command (SPEC:112) but is now excluded from the test (SPEC:195) and the flag clause (SPEC:159), and SPEC:149 and SPEC:265 keep its change to the usage line. The stated texts allow reading load as exempt. Quote of the inherited sentence: `Every changed command also gains the `## Unattended mode` section (section 2.1).`
- Carried from review 1, all `origin=unchanged` and not on changed lines, so notes unless they quote a changed line: M-1 to M-10 of `R1:104-115` are not re-graded and none depends on a changed line, except M-5 (existing status words) and M-6 (workflow pre-creation location), which touch WC-4's old and new text equally and stay Medium. M-2 (fresh output directory, SPEC:64 against SPEC:62) now also covers the file-valued case: a retry with the same `--output <file>` rewrites the same `<stem>.return-contract.yaml`. Still Medium.

Minor (notes):
- n-A: the final spec carries dangling finding ids "(F-1)" and "(F-2)" (SPEC:62, 76, 85-87, 90, 120, 159, 195) that are defined only in `round1.md`; strip or footnote them once the loop ends. (Lint-2 ids dismissed above.)
- n-B: the Decisions row on report shape says one name `return-contract.yaml` lets the coordinator check every worker the same way (SPEC:261); five commands now use `<stem>.return-contract.yaml` or a fixed path, so the coordinator reads the path from `--report-path`, not the name. Origin=unchanged.
- n-C: SPEC:197 (AC-1.3) asserts "no `return-contract.yaml` appears" by name; a `<stem>.return-contract.yaml` would also match a `*return-contract.yaml` glob but not an exact-name check. Origin=unchanged.
- n-D: the user question on follow-ups was not asked; this worker run is non-interactive, so no issue was opened.

## Coverage

scoped PASS: changed lines + prior blockers

What was covered: the full diff (9 hunks), both prior blocking findings, the 3 inventories' lines cited by the changed rows (INV-A:42, 53, 55; INV-B:177-185, 217-225), SPEC:62-76, 85-90, 112, 120, 149, 159, 183, 195-200, 261, 265. Not covered: whole-document assurance (a separate, labelled first review would be needed; its blockers go to the user, never to a fourth review), and every UNVERIFIED `cmd/`, `sk/`, `src/` and `CLAUDE.md` citation. Experts run: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe. Pipeline Dimensional Analysis and the State Variable Registry were not triggered. Brief clauses overridden: none. The candidate was not edited and no revised specification was written.

verdict: PASS
