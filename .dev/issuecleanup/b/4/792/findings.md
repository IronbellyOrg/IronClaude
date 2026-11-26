# Round 2 findings for #792 (C11): Define and validate a valid worker_done message

Checked against master `f2894fc44` (2026-11-24). Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/4/792/findings.md`. Command run: `/sc:analyze src/superclaude/cli/sweep --focus architecture --depth quick` (report `.dev/issuecleanup/b/4/analyze/analyze-report.md`). `WORKER-CONTRACT.md:N` is `src/superclaude/core/WORKER-CONTRACT.md`. `SPEC` = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md`. `R38` = row 64 of `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`.

## Alignment with architectural decisions

- **FR-83 (`SPEC:243`): aligned.** The coordinator runs `issue-pipeline complete` "after it reads a succeeded `worker_done` or a launched agent's `result.md`", posting "outcome word, validated paths, PR number only". A validator on the read side is what FR-83 presumes. `SPEC:61` still says `complete.py` is NOT BUILT; that is stale: `src/superclaude/cli/issue_pipeline/complete.py` is on master (added by PR #707, `git log --follow`).
- **SPEC:677 (UNVERIFIED "PR 693's result file path and shape"): partly settled.** The closed three-line result format (`outcome`, `artifacts`, `pull_request`) is validated at `complete.py:144-168` (`_read_summary`), outcome word at `complete.py:184-185`, and agreement of the file's outcome with the call at `complete.py:364-366`. PR #693 itself only saves `launch-result.json`, which is a launch record, not a completion shape.
- **WC-4 (`WORKER-CONTRACT.md:32-39`) and WC-5 (`:60`): aligned and decisive.** The contract file `return-contract.yaml` holds the fields (`worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`, `blocked_question`, `reason`); `worker_done` carries only the outcome and a body. The dispatch preamble in this brief gives `worker_done` the flags `--outcome`, `--body`, `--task-id`, `--dispatch-id`, optional `--files-modified` and `--report-path`; the contract says the preamble is the authority for syntax (`:7`). So "paths, PR number or branch, regression-gate result" are not fields of the Orca message. They can only live in the contract file or in the body text (WC-5 fixes only the body's first sentence, `:60`). UNVERIFIED: that every Orca version has these same flags.
- **WC-4 (`:35`) on a command that has its own status field, and WC-5's "never reads the command's own status":** a new required-field check must read `worker_status` only.
- **Duplicates and mismatches (`:107`, `:109`): aligned.** A mismatched id is quarantined; a second `worker_done` for the same dispatch is "logged and ignored". The coordinator never sends or synthesizes `worker_done` (`:109`), so a validator may only read.
- **SEC-16 and FR-83 "validated paths, PR number only" (`SPEC:305`, `SPEC:243`): aligned.** The existing path and PR-number checks at `complete.py:144-168` are the plan's direction; one shared reader is better than a third parser.
- **R38 (`requirements.md:64`): aligned.** The item is not an element of Clay's design; it checks the merged contract. R38(D) (the coordinator never merges or closes on its own) holds: the validator reads.
- **Closing review of #716 (2026-11-24, step 5): aligned.** "PR #693 adds `launch-result.json`, not a universal `worker_done` validator" is exactly this item's gap.
- **D12 (`debates/D15/VERDICT.md:96`):** "one message handled once per id" is Adopt with change; matches the duplicate rule.

## Complementary issues

- **#790 (C9, handoff template with regression gate):** C9 tells the worker to run the regression gate and report its result (S02-F27); C11 checks that result. Interface: one field name, defined once, in the contract file. C11 depends on C9 for this field or drops it.
- **#800 (C19, settle each worker):** relies on a valid `worker_done`; blocked by C11.
- **#770 (the watcher hands claims to the coordinator and results come back):** its option (a) and (c) would notice `result.md`; C11 gives the shape it would check. `grep result.md src/superclaude/cli/sweep` finds nothing (checked), so the sweep does not read it today.
- **#784 (C3, the coordinator's own return contract):** a second contract shape; define fields in one style.
- **#766 and #590 (sweep misreads or never reads contracts):** same reader (`read_contract`, `probes.py:781`); #766 fixes a path regex, C11 would add a field check on the same function. Order: fix #766 first, since a wrong path means no contract is read to validate.
- **#774 (docs refresh):** edits the same contract text (WC-4 fields would change).
- **#782 (C1):** C11 says "before wave 5 ends"; the plan has no waves on master until C1 builds the skill.

## Closest overlap

**#790 (C9) "Handoff prompt template: ... regression gate".** Shared: the regression-gate result that the worker must report and the coordinator must check. Estimated share of C11's done-when covered: about 20 percent (one of the four fields named in "what to build"; none of its three test cases). Next two: **#770**, about 15 percent (it needs the result file's shape, which C11 defines, and its done-when has a "notice `result.md`" check), and **#784 (C3)**, about 10 percent (another return-contract shape to be defined in the same style). #800 depends on C11 and covers about 5 percent.

## Standalone or merge

**Verdict: stand alone.** Tested against #790:

- Owner: same (coordinator skill author).
- Acceptance test: different. C9 renders a prompt and checks section order and `Fixes`/`Refs`; C11 is a table-driven test of a contract with accept and reject cases.
- Files: C9 a template file and golden prompts in the skill; C11 `src/superclaude/cli/sweep/probes.py` (the reader) or a small module beside `complete.py`, plus fixtures in `tests/sweep/`.
- Build phase: C11 is code that can ship before the skill exists; C9 needs the skill (C1).
- Risk if merged: a code change to a reader used by the sweep would wait for a skill template, and the template could not ship until the validator is reviewed.

Merging into #790 would be right only if the owner decides the regression gate is the only field to add; then C11 shrinks to one rule and the rest could be dropped. Not the case today (outcome word, paths and PR number need a check too).

## Closed issues and merged PRs checked

- **PR #707 (merged):** delivers `complete.py` with the closed result-file validator (the launched-agent half of C11). Supersedes the "UNVERIFIED shape of result.md" watch-out for that file; does not cover `worker_done` or `return-contract.yaml`.
- **PR #693 (merged 2026-11-20):** `launch-result.json`; a launch record only. Does not deliver C11.
- **PR #591 (merged 2026-11-17):** coordinator handoff, WC-17 and the completion duty text (`WORKER-CONTRACT.md:302`) that reads the contract. Names the need; no field check.
- **PR #411 and #422 (merged):** converted commands to write `return-contract.yaml` (WC-4). Define the fields C11 would check.
- **PR #539 (merged):** the sweep with the one contract reader. Hosts the reader a validator extends.
- **PR #729 and #700/#701 (merged):** R38 record; rollback of the 655 build; contract corrections. No change to this item; confirm that nothing from the 655 build remains to validate.
- **#655 (closed, not planned):** source of "regression-gate result in `worker_done`" (S02-F27); no merged work.

## Updated recommendation

- **Action: keep open with changes.** (1) Validate `return-contract.yaml` by adding a required-field check on `read_contract` (`probes.py:781`), reusing the existing outcome-word list (`classify.py:98`, `complete.py:184`) rather than a third parser. (2) Say in the issue that `worker_done` has no paths, PR or gate fields; they belong in the contract file, so a new field (for example the gate result) means a contract version bump under WC-4. (3) Define the regression-gate field in #790 first, or drop it. (4) Change "sent twice" to "second message ignored", since Orca and the contract settle it. (5) Remove "before wave 5 ends".
- **Priority: P2. Complexity: simple, size S.**
- **Versus round 1: action, priority, complexity and size unchanged.** Changed or added: the fact that `worker_done` itself has only outcome, body and ids (so the field list belongs to the contract file); `complete.py` comes from PR #707; #766 ordering; closest overlap named (#790 at about 20 percent); R38 checked (no conflict).

## Scan record

- Lists read in full (columns number and title): open-issues.tsv 134 of 134; closed-issues.tsv 157 of 157; merged-prs.tsv 508 of 508.
- Search terms: worker_done, contract, return-contract, validate, result, launch-result, outcome, completion, regression gate, shape, complete, handoff.
- Opened with `gh` (partly read by sections): open #716 (all comments), #784, #787, #789, #790, #800, #770, #771, #766, #590, #774, #782, #806; closed #431, #655 (keyword lines); PRs #591, #693, #539, #729, #434. Not opened: #411, #422, #700, #701, #707 (list titles and `git log` only).
- Code read: `complete.py:144-146, 184-185, 364-366`; `probes.py:722, 737, 781`; `classify.py:98, 283`; `WORKER-CONTRACT.md` lines named above; codegraph callers of `read_contract` (7, all tests). UNVERIFIED: whether Orca rejects a missing `--outcome` itself; the exact `worker_done` flag set across Orca versions.
