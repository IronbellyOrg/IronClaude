# Round 2 findings: #802 (C21) Text hygiene: no em or en dashes and no secrets in what the coordinator writes

Checked 2026-11-24 against master f2894fc44 (worktree Realign). Parent: #716 (coordinator). Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/7/802/findings.md`. Static run: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/7/analyze` (`.dev/issuecleanup/b/7/analyze/analyze-report.md`, findings 1, 2, 4). Plan paths below are under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`).

## Alignment with architectural decisions

- **R38** (owner 2026-11-21, `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`): the merged watcher is the design; no element of Clay's orchestrator design is adopted; names stay `/sc:coordinator`. The list of rejected elements (wake file, cap, registry, tier keys, living work report, merge gate, flags) does not name a dash or secret check. **Aligned** on direction; **partly aligned** on target: R38 supersedes the "Clay strengths adopted" rows of SPEC, and the living report that `report-entry` writes into is among the rejected elements (and parked by the owner, #716 comment 2026-11-22), so the `report-entry` half of the done-when has no writer to test.
- **OD-4 / OA-30, debate QG2** (DEC:807-809, DEC:1252, `debates/QG2/VERDICT.md:59`): `report-entry` and `escalate` write even when a check fails, the matched span is replaced by a visible marker, "the original match is kept in the action log". Origin OURS (DEC:121), status after PR 700 "UNCHANGED" but moot until the report skill is restored (DEC OD-4 entry). For names this is fine; for a secret it would store the secret. **Partly aligned, in conflict on one point**: C21's own watch-out asks fail-closed with no logging of the match, the opposite of OD-4's log rule. A separate recorded rule is needed.
- **OD-3 / OA-29, scope B** (DEC:120, DEC:1251; SPEC FR-37 `SPEC.md:239`): the naming scan runs only in `report-entry` and `escalate`, after live check U54 (`SPEC.md:710`). C21 adds "handoff prompts, PR and issue text". **Partly aligned**: the two verbs match; the wider reach is beyond scope B, and `debates/QG2/VERDICT.md:63` says the owner has not ruled on the naming rule at all.
- **SPEC FR-26 / S15c** (`SPEC.md:228`, `:499`): verb group `superclaude coordinator` with `report-entry` and `escalate`, NOT BUILT (`SPEC.md:62`). **Aligned** as the future home. Master calls `superclaude orchestrator report-entry` (`src/superclaude/skills/sc-closeout-protocol/scripts/settle.sh:1037`, `:1042`): a spelling mismatch that must be fixed before any test.
- **SPEC.md:545** (rotate the leaked Orca auth token, "not rotated") and DEC:1176 (g): the incident behind the secret half. **Aligned** (motive).
- **Owner writing rule** (`spec/SPEC-BRIEF.md:32` "No em dashes or en dash ranges"; pragmatic output style): the dash half matches it. **Aligned**.
- **WORKER-CONTRACT.md**: WC-9 (`~/.claude/WORKER-CONTRACT.md:41`) bars outward action; WC-4 keeps secrets out of `artifacts` only by the git-ignore rule (`:34`). No rule on text scanning. **None conflicts; none governs.**
- **Architecture finding** (analyze finding 1): no scan exists in `src/superclaude/cli/issue_pipeline/`; the only runtime dash refusal is shell in `settle.sh:161-188` (refuses the whole text; does not mask). **Aligned** if C21 reuses it.

## Complementary issues

- #790 C9: its handoff template tells the worker never to print or commit secrets (S04-F26). C21 is the mechanical backstop for text the coordinator writes. Interface: both cite the same rule; one fixture can serve both.
- #808 C27: sends a notice after an escalation entry; its watch-out says the secret rule of S10-F18 applies. It depends on C21's secret rule and on the `escalate` verb.
- #795 C14 and the report-entry line of C8 (#789): the `report-entry` writer; parked by the owner (#720, #719). C21's test for `report-entry` waits on them.
- #801 C20: refuses commands that change credentials (S09-F34). Different layer (what the coordinator may run, not what it writes).
- #716 phase 3 lists C21 with C16 to C18 and C20 to C24; no open item builds the `escalate` verb itself (grep of #801, #808, #790, #795, #794, #787, #783, #788: only #801 and #808 mention it, neither builds it): UNVERIFIED beyond that grep.
- #758 (blind-user question rule) and #672 (report-writing prohibition): same plain-writing family; no interface.

## Closest overlap

**#790 C9, Handoff prompt template (no secrets line).** Shared: the no-secret goal and the handoff text as a surface. It covers about 10 percent of C21's done-when (an instruction to the worker, not a test that a secret-shaped string is masked in `report-entry` and `escalate`). Next two: **#808 C27** (about 5 percent: names the secret rule as a watch-out, builds nothing for it) and **#801 C20** (about 5 percent: credential commands refused, not text scanned). The brief's candidate #795 C14 shares the `report-entry` target but not the scan.

## Standalone or merge

**Stand alone.** Tested against #790: owner same (coordinator workstream), but the acceptance test differs (template render test versus a scan test on two verbs); files differ (template files versus a shared text-check module near `settle.sh` and `credential_scanner.py`); build phase differs only slightly (both phase 2 and 3); risk if merged: the secret scan's no-logging rule, a safety control, would be buried inside a template item and its false-positive plan lost. Merging into #808 would be wrong too: #808 consumes the check, and a notice sender is a larger, owner-gated build. Merging would be right only if the owner drops `report-entry` and `escalate` from the coordinator, because then C21 has no target; that is not decided (R38 does not say so).

## Closed issues and merged PRs checked

- #683 (merged, `/sc:closeout`, issue #668 closed): already ships the dash check and a names deny list in `settle.sh` with tests (`tests/skills/test_closeout_protocol.py`). Delivers the dash half for closeout text only; C21 should port it, not rewrite it. Issue #668 listed "no em or en dashes and no secret is printed or written" as its own hygiene criterion.
- #700 (merged revert of PRs 681, 682, 684): removed the report skill and the orchestrator design; `report-entry` lost its home. Supersedes the report-entry half of the target.
- #729 (merged, R38 record) and #707 (merged watcher): no scan in the watcher; R38 does not reject hygiene.
- #608 (merged, plain English style): the owner's writing rule that the dash half enforces; it is a style rule for the agent, not a runtime check.
- #655 (closed, source design; lines 129 and 141 name a secret row and a refuse list): the origin of S10-F18; closed as not planned, features carried in #716.
- #675 and #665 (closed review follow-ups of the #655 plan): no change to C21.

## Updated recommendation

**Keep open with changes**, priority **P3**, complexity **medium**, size **M**. Changes: (1) done-when: a shared text-check function (port of `text_refused` for dashes, reuse of `credential_scanner.py` patterns and `[REDACTED]` marker) that masks with a visible marker, never rejects, never writes or logs the original match; the test targets the function first, `escalate` second, `report-entry` only after the report is restored; (2) first build limited to scope B (two verbs); wider text is a later owner decision; (3) fix `orchestrator` versus `coordinator` verb spelling first; (4) record the secret rule as an owner choice separate from OD-4. Unchanged from round 1 on priority, complexity and size; changed from round 1: closest overlap named (#790), R38 and OD-4 status added, and the dependency "no open item builds `escalate`" recorded.

## Scan record

Read in full: open-issues.tsv (134 lines), closed-issues.tsv (157), merged-prs.tsv (508). Search terms for picking candidates: secret, token, credential, dash, hygiene, escalat, report, entry, handoff, template, plain English, style, closeout, guard, scan, names. Opened in full (body read with `gh issue view` / `gh pr view`): open #716, #717, #790, #795, #794, #801, #808, #719, #720, #758, #672, #722, #787, #783, #788, #807(requested, headline only), #698 (headline only); closed or merged #683, #608, #700, #729, #707, #668, #655, #444, #675, #665. Plan files read: SPEC.md lines 62, 97, 228, 239, 260, 499, 545, 710; DECISIONS.md 120-121, 807-830, 1176, 1251-1252; QG2 VERDICT lines 59, 63; requirements.md:64; design-comparison-655.md:3. Master read: settle.sh:155-190, 1035-1043; credential_scanner.py markers. UNVERIFIED: ruling 17 (cited by #808) is not in the plan files; that no other issue builds `escalate`.
