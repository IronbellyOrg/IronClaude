review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (whole-document audit, first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `39bbe6871713a48397dee32c0a486174eebbc1b08a14833316eed1593df495bb`
- Baseline: none given, neither `--re-review` nor `--baseline`; this is a first review of the full document (a labelled whole-document audit).
- Reviewer model actually used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`.
- Evidence checked: `README.md` and the three files under `inventory/` (`commands-a.md` 120 lines, `commands-b.md` 323 lines, `orca-capabilities.md` 188 lines). Citations I could not check against a file in this workspace are marked UNVERIFIED.
- Citation keys follow the spec's own: SPEC:N = the candidate, INV-A:N / INV-B:N / CAPS:N = the three inventories.

## Coverage

Read in full: the candidate (SPEC:1-285), `README.md`, the review-loop prompts file, and `command.md`. Checked against the inventories: CAPS:44-52, 58-80, 86-130, 145-162, 177-188; INV-A:35-55, 62, 65, 90-96, 106-120; INV-B:28-53, 87-115, 207-216, 285-323. Also ran a mechanical test of the AC-C5 / AC-0.3 grep expression (see B-2).

Not checked, UNVERIFIED because the file is outside the workspace:
- Every `src/superclaude/...` line citation (all `sk/` and `cmd/` cites; SPEC:11 says 11 of them were re-read, I could not repeat that).
- `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/...`, `CLAUDE.md` line cites, `pyproject.toml:38`, `src/superclaude/cli/install_core.py:13-24`, and the Orca guide line numbers (only checkable through CAPS quotes).

Panel (fixed order): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Focus experts leading: Wiegers, Fowler, Nygard.

Pipeline Dimensional Analysis: not triggered. The spec describes no multi-stage data flow whose item counts diverge; its phases are a rollout order, not a data pipeline. `--focus correctness` is not active, so no State Variable Registry is produced.

## Guard Condition Boundary Table

Guards found: G1 `--unattended` switch (SPEC:16, 51, 60); G2 outcome mapping (WC-5, SPEC:63); G3 wait-size rule (WC-10, SPEC:68); G4 file-valued output rule (WC-4, SPEC:62); G5 task confidence threshold (SPEC:121). Classes left out are given with a one-line reason. Responsibility: Nygard built, Crispin checked completeness, Whittaker attacked.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` | SPEC:60, 62 | Zero/Empty | flag present, no `--output`/`--output-dir` | true | not specified; WC-4 only says "the directory the coordinator passed" and 2.3 says the brief carries one | GAP (M-2) |
| G1 `--unattended` | SPEC:128 | Sentinel Value Match | flag passed to a section-4 command | true | "get no `--unattended` mode" says nothing about what such a command does with the token | GAP (minor, n-1) |
| G1 `--unattended` | SPEC:146 | Legitimate Edge Case | flag absent (person at keyboard) | false | SA-1: behaviour unchanged | OK |
| G1 `--unattended` | SPEC:60 | Typical | flag + required flags in brief | true | gates resolve per section 3 | OK |
| G2 outcome | SPEC:63 | Zero/Empty | contract file zero bytes / no `status` key | parse fails | `--outcome failed` (F-05) | OK |
| G2 outcome | SPEC:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G2 outcome | SPEC:63, 263 | Sentinel Value Match | `status: partial` | true | maps to `succeeded`, body states `partial` | OK |
| G2 outcome | SPEC:63 | Legitimate Edge Case | `status: blocked` with empty `blocked_question` | status valid | outcome `failed`; the non-empty question is required only by the test at SPEC:200, not by WC-4 | GAP (minor, n-2) |
| G3 wait size | SPEC:68 | One/Minimal | single blocking call of exactly 4 to 5 min | ambiguous | rule splits calls "longer than 5 minutes" into waits "of at most 4 minutes"; a 4.5 min call is neither | GAP (minor, n-3) |
| G3 wait size | SPEC:114, 283 | Maximum/Overflow | pr-submit poll script runtime | unknown | explicitly UNVERIFIED (item 12); the check is deferred to AC-4.3 | GAP (known, recorded) |
| G3 wait size | SPEC:104 | Maximum/Overflow | cli-eval 3600 s eval | true | split into waits of at most 4 min | OK (no acceptance check, see M-7) |
| G4 file output | SPEC:62 | Legitimate Edge Case | two outputs with the same stem and different extensions in one directory (`a.md`, `a.txt`) | stem equal | not specified; N-1 only separates different stems | GAP (minor, n-4) |
| G4 file output | SPEC:62 | Zero/Empty | `--output` with no extension | true | stem is the whole name; inferable | OK |
| G5 confidence | SPEC:121 | Typical | confidence below 0.70 | true | blocked | OK |
| G5 confidence | SPEC:121 | Legitimate Edge Case | confidence 0.70 to 0.89 | false | not specified under `--unattended`; INV-A:36 shows another command prompts in that band; whether `task` does is UNVERIFIED | GAP (minor, n-5) |

Left out with reasons: One/Minimal and Maximum for G1, G2 and G5 (booleans and enums have no magnitude); Zero/Empty for G3 (a zero-length wait cannot trigger the rule); Sentinel for G3 and G4 (no reserved value).

GAP grading under FR-8/FR-9: the first GAP names a missing requirement, not a stated text that does harm, so it is Medium (M-2); the other GAPs are minor.

## === REQUIREMENTS ANALYSIS ===

### B-1. WC-3 lets a worker obtain a Ruling from the coordinator, contradicting D2(a) and Non-goal 6
- Severity: CRITICAL (blocking). Experts: Wiegers (requirements consistency), Nygard (safety boundary), Whittaker (Sequence Attack on the halt path). Priority: High. Quality-impact: Consistency and Safety, large.
- Grading sentence: An implementer who follows WC-3 as written writes into `WORKER-CONTRACT.md` that a worker whose gate "would resolve as blocked" may "ask the coordinator once ... then re-invoke or resume the command with the answer as a flag" (SPEC:61); `/sc:implement`'s halt is exactly such a gate (SPEC:109); so the implementer builds a path where the coordinator, which is another agent, supplies the Ruling, and that is wrong because the same document says the Ruling rule is kept unchanged (Non-goal 6, SPEC:218) and recommends option (a) "Keep the rule", citing the rule's text that "another agent's message" does not count (SPEC:233-236).
- Evidence: WC-3 is generic and names no exception (SPEC:61). The implement row says only "stop with the halt recorded ... blocked" (SPEC:109) and refers to D2 for the rule. D2(b) is the option that "allows a relayed Ruling" (SPEC:235) and is described as weakening "a deliberate safety rule"; D2 is open and Phase 4 waits for it (SPEC:154), yet WC-3 belongs to Phase 0 (SPEC:158) and applies to every command from the start. So the weakening is decided by default before the user answers D2. The same text also lets a coordinator answer cli-portify's three approval gates (SPEC:105) and `task`'s TFEP "present to user" stop (SPEC:121), which the table resolves as "blocked" and never says may be answered by an agent.
- Concrete attack (Whittaker, Sequence): worker runs `/sc:implement --unattended`; QA halts with `E-NO-RULING`; the worker follows WC-3, asks, the coordinator replies "approved", the worker re-invokes with the answer as a flag; the implementer's own work was approved by an agent. State before: ledger shows halt, no Ruling. State after: ledger shows a Ruling that no person gave.
- Recommendation (narrow, no new mechanism): in WC-3 exclude gates whose acceptance must come from a person (the implement Ruling, any row whose gate is an approval), or state that D2(a)/Non-goal 6 override WC-3 until the user chooses (b).

### B-3. WC-4 fixes the contract at `<output-dir>/return-contract.yaml`, but section 3.1 and AC-1.4 fix adversarial's at `<output>/adversarial/return-contract.yaml`
- Severity: MAJOR (blocking). Experts: Wiegers (consistency), Adzic (example), Hohpe (path contract between coordinator and worker). Priority: High. Quality-impact: Consistency, Testability.
- Grading sentence: An implementer who follows the stated text builds, for adversarial, a contract at `<output>/adversarial/return-contract.yaml` (SPEC:83, 198) while WC-4 and Step 3 of the live check require the worker to send, and the coordinator to read, `<output-dir>/return-contract.yaml` as "the WC-4 contract path" (SPEC:62, 182); the two paths differ, so the report path the coordinator predicts before dispatch does not exist and AC-1.2 step 4 (`test -s <contract>`, SPEC:183) fails for a command the spec itself calls ready.
- Evidence: INV-A:35 confirms the artifacts live under `<output>/adversarial/` and that real runs wrote there, sometimes in a doubled `adversarial/adversarial/` folder. WC-4's own reason for being is that the path is "known before dispatch" (SPEC:62). The same split affects workflow (`.dev/tasks/to-do/<id>/`, SPEC:92), cleanup-audit (`.claude-audit/`, SPEC:85) and reflect (`.dev/reflect/<mode>-<slug>-<ts>/`, INV-B:109); only some of these are reconciled by F-02/F-03 text.
- Recommendation (narrow): state in WC-4 that for adversarial `<output-dir>` is `<output>/adversarial/` and tell the brief to pass that, or move the contract to `<output>/return-contract.yaml`; say which in one sentence.

### M-2. `--unattended` without an output directory is undefined
- Severity: MAJOR label, graded Medium. Experts: Wiegers, Whittaker (Zero/Empty Attack). Priority: Medium.
- This is a requirement the document never states (a missing restriction), not a stated text that does harm (first-review prompt, `document_review_loop_prompts.md:31`). WC-4 and 2.3 assume the brief carries the directory (SPEC:62, 73), and AC-C3/AC-1.x tests only supply it. See guard table G1.
- Follow-up: say whether the command refuses, writes to a documented default, or resolves as blocked when the directory is missing.

### M-7. Several requirements have no acceptance check
- Graded Medium. Experts: Crispin, Wiegers. Priority: Medium.
- WC-1 (SPEC:59), WC-6 resume or fresh run (SPEC:64), WC-10 wait splitting for cli-eval (SPEC:68, 104; only pr-submit is tested, AC-4.3 at SPEC:210) and WC-12 (SPEC:70) appear in no AC row of section 7 (SPEC:167-210). SA-1 has one manual check (AC-2.5, SPEC:203) that covers two commands out of thirty-six.

### M-8. Phase boundaries leave a window where a command accepts `--unattended` and still prompts
- Graded Medium. Experts: Cockburn, Fowler. Priority: Medium.
- P1 says every command in 3.1 and 3.2 accepts `--unattended`, "a no-op where a command has no gate" (SPEC:159), and AC-1.1 requires a `## Unattended mode` section on all of them (SPEC:195). Gate resolution for 15 of them arrives in P2 (SPEC:160), for roadmap, validate-roadmap, validate-tests and save in P3, and for implement, post-release and pr-submit in P4. Between P1 and the later phase, a brief that follows 2.3 and passes `--unattended` (SPEC:73) to tdd, task or implement gets a command that claims unattended mode and can still stop on a person. Nothing says the P1 section must declare the gates as not yet converted. Reading it so needs a guess, so Medium.
- Also: P1's command list (SPEC:159) names no phase for the WC-4 contract of tdd, troubleshoot and release-split (SPEC:90-91), though AC-2.2 expects a contract from tdd (SPEC:200).

### M-1. WC-6 "fresh output directory" depends on a rule the document does not state
- Graded Medium. Experts: Nygard, Wiegers. Priority: Medium.
- WC-6 says a command with no resume flag "writes each run into a fresh output directory" (SPEC:64), and 25 rows say "fresh dir"; 2.3 tells the coordinator to pass one output directory so the report path is known before dispatch (SPEC:73). If a retry (`--retry-of`, CAPS:116) reuses that same directory, the second attempt overwrites the first attempt's `return-contract.yaml`, the corruption WC-6 forbids. Neither section says the coordinator passes a new directory per attempt, or that the command makes a sub-directory.

### M-11. WC-4 "known before dispatch" is not met for workflow and tdd
- Graded Medium. Experts: Hohpe, Adzic.
- Workflow's `<id>` is created at run time, and the fix is "the flag the P1 plan names" (SPEC:62, 92), a flag that does not exist in the spec and is deferred. AC-0.4 runs workflow in P0 with no such flag (SPEC:194).

## === ARCHITECTURE ANALYSIS ===

### B-2. AC-C5 and AC-0.3 cannot detect the deletions they are written to catch
- Severity: MAJOR (blocking). Experts: Fowler (interface/gate design), Crispin (check validity), Whittaker (Divergence Attack on the check). Priority: High. Quality-impact: Testability, Safety of SA-1/SA-4.
- Grading sentence: An implementer who runs AC-C5 (SPEC:176) and AC-0.3 (SPEC:193) as written gets "prints nothing" for a phase that deleted an existing Markdown bullet or a `---` line from a command file or from `HOW-WE-WORK.md`, and that is wrong because those checks are the only mechanical evidence for SA-4 ("additive edits", SPEC:149), SA-5 ("no existing routing row changed", SPEC:150), and through them SA-1, which SPEC:142 calls a hard requirement on every phase.
- Evidence (tested, not assumed): in `git diff -U0` a removed line carries a leading `-`. A removed bullet `- old bullet` appears as `-- old bullet`, and a removed `---` appears as `----`. The expression `grep -E '^-[^-]'` rejects any line whose second character is `-`. I fed it `-- old bullet`, `-| old row |` and `----`: only the table row was printed. Command files are written mostly as bullets (see `command.md` structure), so the common deletion is the one the check misses.
- Recommendation (narrow): replace the expression with one that excludes only the file header, for example `grep -E '^-' | grep -vE '^---[[:space:]]+[ab]/'`, or count removed lines with `git diff --numstat` and require the deleted count to be 0.

### M-5. AC-C1 conflicts with the Orca text SA-2 and SA-5 allow or require in `core/`
- Graded Medium. Experts: Fowler, Newman.
- AC-C1 greps `src/superclaude/core` for `orca(-ide)? orchestration|worktree|terminal|agent` and demands nothing (SPEC:172). SA-2 allows the contract file to mention Orca as "an example of a caller's question channel" (SPEC:147), and P0 adds "an Orca section" to `HOW-WE-WORK.md` plus the contract file, both under `core/` (SPEC:158, 150). Whether both texts can be written without the matched phrase takes a guess about wording, so Medium. State which files AC-C1 excludes.

### M-3. AC-2.2 requires `failed` and `blocked`, while WC-3 permits asking instead
- Graded Medium. Experts: Crispin, Gregory.
- AC-2.2 passes only on `worker_done --outcome failed` with a blocked contract (SPEC:200), but WC-3 lets a compliant worker ask the coordinator and wait (SPEC:61). The test brief does not say to forbid `ask`. A compliant worker could fail the test.

### M-4. WC-5 and 7.2 step 4: who runs the parse check, when, and where
- Graded Medium. Experts: Nygard, Hightower.
- WC-5 has the worker run the check "before it sends `worker_done`" (SPEC:63); 7.2 lists the same check as a coordinator step that follows `worker_done` (SPEC:182-183). The check is `uv run python -c "import yaml ..."`. Workers run commands in other projects (SPEC:34), where `uv run` uses that project's environment; PyYAML being a dependency of IronClaude (`pyproject.toml:38`, UNVERIFIED) does not make it importable there. A good contract could then be marked `failed`.

### M-6. tasklist and reflect rows change the inventory's advice without a recorded decision, and state UNVERIFIED nesting as fact
- Graded Medium. Experts: Fowler, Newman, Nygard.
- INV-B:213 says Stage 10.5 "should call reflect without `--remediate`"; the spec instead passes `--unattended` so reflect's headless rule auto-accepts (SPEC:122, 88). The headless rule "auto-accepts for auto-fixable registers" (INV-B:107), which starts remediation work. WC-9 turns off outward actions only (SPEC:67), and the Decisions table has no entry for this (SPEC:259-269). SPEC:122 also says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit"; INV-B:109 shows reflect itself spawns agents and runs adversarial, and INV-B:214 records subagent-to-agent nesting as UNVERIFIED. INV-A:14 records the limit as three layers and loss of the Agent tool at the limit. The claim is unproven. UNVERIFIED item 9 (SPEC:280) concedes reflect may not treat a worker as headless, which is the premise of the row.

### M-9. pr-submit's own "Will Not: run headless" is not reconciled
- Graded Medium. Experts: Newman, Hightower.
- INV-B:92 cites `cmd/pr-submit.md:85` and `SKILL.md:225`: "Will Not: run headless / imply a daemon". The pr-submit row (SPEC:114) and D3(b) (SPEC:241) add `--unattended` without saying this line changes. D3(a) is recommended, so no harm now; the P4 plan will have to resolve it.

### M-10. reflect's tracked-file write is omitted
- Graded Medium. Experts: Hohpe, Nygard.
- INV-B:109 (f): UC-2 writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md`. The reflect row (SPEC:88) names `--no-promote` but not this write, which touches WC-9 (outward) and WC-11 (shared files).

### M-12. Which copy of a skill the worker reads is not stated
- Graded Medium (citation hygiene). Experts: Wiegers, Hightower.
- The pr-submit top-level rule is at `SKILL.md:37-39` in the source tree (INV-B:90, SPEC:65) and at `:47-49` in the installed copy (CAPS:161). Workers run the installed copy. The spec's line cites to `sk/` and `cmd/` (UNVERIFIED here) therefore may not match the text a worker sees. D3 and WC-10 cite `:41-64` and `:46-64` as the poll loop, which overlaps the installed rule lines.

## Adversarial analysis (Whittaker), summary

Attacks applied: Zero/Empty (G1, M-2), Divergence (B-3, M-3), Sentinel Collision (`partial`, `blocked`, G2), Sequence (B-1, M-4, P1 before P2 in M-8), Accumulation (retry overwrite in M-1; no counter or capacity limit is specified elsewhere). Only B-1, B-2 and B-3 meet the blocking bar.

## Minor notes (never fail the review)
- n-1 to n-5: the minor GAP rows in the guard table.
- n-6. The `Decisions` table cites "ladder rung 2" (SPEC:261) with no definition in the document.
- n-7. SPEC:285 item 14 is a record of a check, not an unverified item; it sits in the UNVERIFIED list.
- n-8. SA-2 (SPEC:147) says "in a changed command" and "inside the contract file" in one sentence; split it.
- n-9. The count "43 commands ... 10 / 27 / 6" is consistent with the tables (10 rows at SPEC:83-92, 27 rows at SPEC:99-125, 6 rows at SPEC:132-137) and with INV-A:3 and INV-B:3.
- n-10. Spot checks of CAPS cites in E1, E2, E4, R1 to R5 and WC-3/WC-5/WC-12 matched their CAPS lines (CAPS:52, 58-64, 66-67, 73-77, 80, 97-103, 129-130, 155, 159-161).

## Follow-up candidates (Medium and minor, listed only)

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12. Minor: n-1 to n-8.

Per Review Loop bullet 3 the session that ran the review asks the user once whether to open an issue for these; this sandbox has no user to ask, so none was asked and none was created. This list is only recorded.

## Brief clauses overridden

None. The brief did not widen the scope or regrade a minor finding.

## Reviser brief

Blocking finding ids: B-1, B-2, B-3.

Rules for the reviser (restating Review Loop bullet 6, since the reviser reads this report and not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the file's byte size before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.

verdict: FAIL
