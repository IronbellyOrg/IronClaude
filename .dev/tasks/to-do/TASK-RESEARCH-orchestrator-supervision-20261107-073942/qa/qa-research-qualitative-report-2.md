# QA Report — Research Qualitative Review (Partition 2 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339), research depth
**Date:** 2026-11-07
**Phase:** research-qualitative (adapted from report-qualitative; partition instance)
**Fix cycle:** N/A
**Fix authorization:** false (no research file edited)
**Assigned files:** `research/scope-03-cli-patterns.md` (200 lines), `research/scope-04-409-layout.md` (331 lines), `research/06-orca-open-questions.md` (182 lines)
**Input only:** `research/research-notes.md`

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

Research-file checksums taken before review (md5): scope-03 `11ae4805...`, scope-04 `92480198...`, 06 `6997f04c...`. Re-checked at the end (see Self-Audit).

---

## Overall Verdict: FAIL

Six blocking findings (all IMPORTANT, none CRITICAL) and three minor notes. The research shows how to register and test a new command, but it leaves out the lint gates. It overstates what the read-only test pattern proves. It does not map the sweep classes onto the #409 layout. It leaves the destructiveness of Orca reads open, even though the handler that settles that question was installed and readable.

## Items Reviewed

The 12 report-qualitative checks are adapted to research depth (no check is N/A). D1-D4 are the four depth questions from the spawn prompt.

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| D1 | Registration and read-only testing of a new CLI command and slash command | FAIL | These match the code: main.py:519-561 (deferred `add_command`), test_contract_status_cli.py:44-66, test_routing_refresh.py:33/:38-40, test_how_we_work_routing_table.py:27-40/:291-311 and HOW-WE-WORK.md:314/:318/:337. Two gaps: the lint-architecture gates (Makefile:362-475) are absent (F5), and the read-only proof is overclaimed (F6). |
| D2 | Mapping of the dated static report onto the #409 Shift Brief, Attention Ledger and omission rules | FAIL | Every scope-04 citation re-checked with `git show 495eb96d` matches: agent_focus.py:9-24/41-53/156-169, canvas.py:73-81/117-122, DESIGN-CONTRACT.md:1-17, fixtures.py:11-21/50-57. However, the skeleton (scope-04:264-309) does not place the sweep classes (F7), and the omission-rule analysis cites the wrong rule (F9). |
| D3 | Whether reading Orca questions is destructive | FAIL | 06:55 contradicts its own quote (F1). 06:60/:63/:71/:74 and Gaps 1-4 (:155-158) are left open, but message-check-handler.js:17, :30, :33-34, :58-71 and :74-95 settle most of them (F2). |
| D4 | Names what remains unknown | PASS (with notes) | Open questions are explicit in every file: scope-03 lists 6, scope-04 lists 8 and 06 lists 16 gaps. Some of them could have been settled (F2), but nothing uncertain is presented as settled except 06:55 (F1). |
| 1 | Problem statement matches findings | PASS | All three files stay on the Phase 1 sweep: command registration, layout and Orca reads. Nothing drifts into Phase 2 orchestration. |
| 2 | Current state is current | PASS | The main.py, test file, HOW-WE-WORK and reflect/config.py line citations re-read and match. The scope-04 citations match commit 495eb96d. |
| 3 | Options are distinct | PASS | The five read modes in the 06 Q2 table are behaviourally distinct. scope-03 separates the CLI side (click group in main.py) from the slash-command side (command file, skill, routing lists). |
| 4 | Recommendation follows from analysis | FAIL | 06:71 approves `check --peek` / `check --all` without a runtime-version condition. Yet 06:60 and Gap 1 leave the runtime behaviour open, and handler :17 warns that "Older runtimes ignore peek" (F2). |
| 5 | Implementation plan is actionable | FAIL | A builder following scope-03:131-157 would miss the size, frontmatter, `-protocol` naming and Check 11 gates (F5). A builder following the scope-04 skeleton would have no place to put the classes (F7). |
| 6 | Gaps are honest | FAIL | The 06:55 label `[CODE-VERIFIED]` contradicts the evidence quoted next to it (F1). |
| 7 | External research is relevant | PASS | The Orca `--help` text and the installed docs cited in 06 bear directly on the read-mode decision. No padding was found. |
| 8 | Scale claims are substantiated | PASS (with note) | No scale claims are made. The only bound is the newest-100 cap. 06 records it, but the research never ties it to the runtime-version fallback (part of F2). |
| 9 | Risk assessment is complete | FAIL | Missing risks: the CLI falls back to `unread:false` on older hosts (handler :33-34); the legacy `compatibilityAck` second `orchestration.check` call runs after printing (handler :58-71); a mis-chosen mode consumes messages (F2). |
| 10 | Evidence trail is complete | PASS (with notes) | The cited file:line evidence traces to real code, apart from the mislabels in F3 and F9. |
| 11 | No circular reasoning | PASS | Each file cites code, `--help` text or git objects as proof, never another synthesis file. |
| 12 | Conclusion is proportionate | FAIL | scope-03:99 says "Directly reusable to prove `/sc:sweep` writes nothing but its report. [CODE-VERIFIED]", but that pattern cannot observe Orca state changes (F6). 06:55 is marked CODE-VERIFIED (F1). |
| X | Cross-file vocabulary (within the partition) | FAIL | 06:134 uses "could not determine" and "stopped". research-notes.md:182-191 uses "stuck" and "timed out". scope-04 uses neither set (F8). |

## Summary

- Checks passed: 8 / 17 (D4, 1, 2, 3, 7, 8, 10, 11)
- Checks failed: 9 (D1, D2, D3, 4, 5, 6, 9, 12, X)
- Critical issues: 0
- Important issues: 6 (F1, F2, F5, F6, F7, F8)
- Minor issues: 3 (F3, F4, F9)
- Issues fixed in-place: 0 (fix authorization false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | IMPORTANT (contradiction) | `06-orca-open-questions.md:55`; repeated at :79 and :148 | The row says "Draining needs `--ack`: [CODE-VERIFIED]". The quote in the same row says the batch replays "until acknowledged **or all its messages are marked read**", and the same row adds that the default probably marks rows read. So plain `check` may drain without `--ack`. The CODE-VERIFIED label contradicts the evidence it cites. | Restate it: "drained by `--ack` or by every row being marked read; whether plain `check` marks rows read is [UNVERIFIED]". Mark plain `check` as potentially draining, then update the takeaway (:79) and the summary (:148) to match. |
| F2 | IMPORTANT (omission) | `06-orca-open-questions.md:60` (`--unread` Unknown), :63 (`inbox` Unknown), :71 (allowed modes), :74, :149, Gaps 1-4 (:155-158) | Gap 1 names the handler folder as the way to settle the question, but the research never read `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/message-check-handler.js`. What it shows: (a) line 17 says "Older runtimes ignore peek, making --unread --peek destructive", so `--unread` is consuming; (b) line 30 sends every `check`, including `--peek` and `--all`, through `callOrchestrationMutation`; (c) lines 33-34 send `unread:false` with peek, so an older host falls back to all mode; (d) lines 74-95 filter read rows and warn that the runtime "returned only its newest 100 messages for --peek"; (e) lines 58-71 make a second `orchestration.check` call with `compatibilityAck` after printing, which can mark messages read on legacy hosts. `message-inbox-handlers.js` shows that `inbox` uses a plain `client.call('orchestration.inbox', …)` and prints a read-only tag. The allow-list at :71 has no runtime-version guard, and the `inbox` ban at :74 rests on an unknown the code answers. | Read the CLI handlers (and the runtime-side `orchestration.check` handler, if reachable). Rewrite the Q2 rows for `--unread`, `inbox` and `--peek`. Forbid `--unread` explicitly. Require a runtime-version check, or a probe for a `legacyCompatibility` result, before `--peek` is trusted, and say what the sweep does when one appears. Close or narrow Gaps 1-4, and add a gap for the `compatibilityAck` path. |
| F3 | MINOR | `06-orca-open-questions.md:62` and :169 | `--format` is labelled CODE-CONTRADICTED. Help line 28 is a generic option label that the help text shares with screenshot commands. Help line 36 agrees with handler :38/:55 (local text rendering only). This is a mislabel, not a contradiction in the code. | Relabel it "ambiguous help label; handler confirms local-text-only rendering". |
| F4 | MINOR (input-only file; note only) | `research-notes.md:9` | Says scope-03 has 197 lines; the file has 200. | Correct the count when research-notes is next edited. |
| F5 | IMPORTANT (omission) | `scope-03-cli-patterns.md:131-150` ("Lists that would fail") and :157 | `make lint` is described only as "`lint-architecture` then ruff". The research never lists what lint-architecture enforces (Makefile:362-475): Checks 1/2, links from command to skill and back; Checks 3/4, a command file over 200 lines warns and over 500 lines fails; Check 6, a paired command needs `## Activation`; Check 8, skill frontmatter needs `name:`, `description:` and `allowed-tools:`; Check 9, the skill name must end in `-protocol`; Check 11, `superclaude.tools.arch_lint --check-contracts` scans `src/superclaude/cli/` for duplicated contract constants (contracts/__init__.py `RETURN_CONTRACTS` :204 and others). A sweep module that re-declares return-contract field names would fail Check 11. A grep of `research/` finds no mention of arch_lint, Check 11 or the size limits. | Add the lint-architecture gates to the "Lists that would fail" registry. Say that `make lint` must pass. Tell the builder to import contract constants from `superclaude.contracts`, not re-declare them. |
| F6 | IMPORTANT (overclaim / weakened criterion) | `scope-03-cli-patterns.md:99` | "Directly reusable to prove `/sc:sweep` writes nothing but its report. [CODE-VERIFIED]" `side_effect=AssertionError` patches and `isolated_filesystem()` catch Python entry points and cwd file writes only. They cannot see an Orca subprocess that consumes messages or changes Run state, which is the main read-only risk for this command (see F2). | Narrow the claim to "proves no repo file writes outside the report". Add a requirement for a single subprocess seam for Orca calls, in the style of `reflect/config.py:64-78` `_git`, plus a test asserting that every argv is on an allow-list. The test must reject plain `check`, `--ack`, `--wait`, `--unread`, `reply` and any other mutating verb. |
| F7 | IMPORTANT (omission) | `scope-04-409-layout.md:264-309` (skeleton), :311-320 | The report skeleton has no section or column for the sweep classes (needs a person, stuck or stopped, timed out or undetermined, finished, idle). Its "Needs a human" table assumes request records with a requester and a question. 06 shows these cannot be listed without risking consumption. The fallback sources (`agentWait`, `blocked_question`, a Ruling halt, a frozen plan, a ready Task this coordinator did not create) do not carry those fields. So the core question "how does the report map onto the Attention Ledger" is answered only for data the sweep may not have. | Add a class column or one section per class. For each fallback source, show how it fills the question and requester cells or prints "unknown". State which classes reach the Attention Ledger and which go only into the Shift Brief. |
| F8 | IMPORTANT (contradiction across files in the partition) | `06-orca-open-questions.md:134` vs `research-notes.md:182-191`; `scope-04` | 06 maps states to "waiting on a person", "could not determine" and "stopped". The notes and the issue use "needs a person", "stuck" and "timed out" (plus finished and idle). scope-04 names neither set. So a builder gets two incompatible state vocabularies and a layout that uses neither. [PARTITION NOTE: other partition files may add more terms.] | Pick one class vocabulary, cite its source (issue #339 or the notes), and use it in 06:134 and in the scope-04 skeleton. |
| F9 | MINOR | `scope-04-409-layout.md:247` (and :129) | It says the wide Ledger and Brief "break DESIGN-CONTRACT.md:11" (the omission rule). That rule applies only when a list *is* limited, and the code never limits it, so the real breach is DESIGN-CONTRACT.md:8 ("All positions must be in bounds"). Also, the `listbox()` count includes rule lines ("5/5" = 3 questions + 2 rules), so a `<shown>/<total>` copied from it counts text lines, not records. The finding still reaches the right conclusion: the static report must count and state its omissions. | Cite :8 as the breach, keep :11 as the rule the report must follow, and require `<shown>/<total>` to count records. |

## Actions Taken

- None. Fix authorization is false, so no research file, task file or other file was edited; only this report was written.
- No Orca, ccsession, sweep or close command was run. The Orca behaviour was established by reading the installed handler source only.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` was supplied in the spawn prompt, so this was a standalone review. Nothing was relied on as an rf-qa PASS.
- For behaviour the research reports from `orca --help` text (`[H:check]`, `[H:inbox]`) and the Orca guides (`[G:messaging]`, `[G:recovery]`), the quoted text was taken as given and was not re-run, because running Orca commands is out of bounds for this step. The handler source was read instead (see b).

**(b) Independent semantic checks (≥1 required, INV-019):**
- Orca read destructiveness: read `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/message-check-handler.js` lines 1-95 (lines 17, 30, 33-34, 58-71, 74-95), plus `message-inbox-handlers.js` and `mutation-request.js`. This is the basis for F2 and F3.
- 06:55 self-contradiction: re-printed the full row text of 06:55. This is the basis for F1.
- lint-architecture gates: read Makefile:362-475, contracts/__init__.py (:64, :104, :129, :204) and grepped `research/` for `arch_lint` / Check 11 / size limits (no hits). This is the basis for F5.
- Registration and tests: read main.py:519-565, test_contract_status_cli.py:18-22/:44-66, test_routing_refresh.py:33-40, test_how_we_work_routing_table.py:27-40/:291-311, HOW-WE-WORK.md:314-337 and reflect/config.py:64-78. All matched scope-03 (D1 PASS parts). The scope-03:99 claim was judged against what those patches can observe (F6).
- #409 layout: ran `git show 495eb96d:` on agent_focus.py, canvas.py, DESIGN-CONTRACT.md and fixtures.py and compared every scope-04 citation (all matched). The skeleton at :264-309 was compared against the class list in research-notes.md:182-191 (F7, F8, F9).
- Research files untouched: md5 before and after are identical. scope-03 `11ae48052f171505d23a4aa36c80a8f9`, scope-04 `924801984e4c13865000ef6ba0d7f456`, 06 `6997f04c6493272b29fa954b89b19ea0`, research-notes `67010c9b8fc4b4b52c66e7c5a6cf0238`.

**Self-audit answers:** About 45 factual claims were checked independently against source (file:line citations in all three files plus the handler behaviour). The files read are listed in (b). There were 9 findings, not zero. No web research was done, so Tavily was not needed.

**Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (this is confidence in the review's coverage, not a PASS; the verdict is FAIL on blocking findings)

**Tool engagement:** Read: 25 | Grep: 6 | Glob: 2 | Bash: 9

Not checked: the runtime-side `orchestration.check` handler, which would show whether plain `check` marks rows read. It was not located in the installed CLI bundle. F2 asks the research to locate it.

## Recommendations

- Fix F1, F2, F5, F6, F7 and F8 in the research files (a fix pass with authorization), then re-run this partition's qualitative review.
- Priority: F2 and F6 together, because they decide whether `/sc:sweep` can be read-only at all. The answer needs to be a code-backed allow-list of Orca argv plus a test that enforces it.
- Merge with partition 1 before deciding F8's vocabulary, since other files may use further terms.
- F3, F4 and F9 are notes; fix them opportunistically.

## QA Complete

## Verdict: FAIL

