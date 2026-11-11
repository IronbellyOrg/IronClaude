review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (first review, spec-panel critique)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `68ce70455b6b30e6a44dbd6460d0688443a0dcdfe80ef873cfa87d79d9501aee`
- baseline: missing (first review; no `--re-review`, no `--baseline`)
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full
- label: whole-document audit of the final spec, not a scoped re-review
- brief clauses overridden: none
- citation rule: only `.dev/orca-command-refactor/README.md` and `inventory/*.md` could be read. Spec citations to `src/`, `sk/`, `cmd/`, `EVIDENCE.md`, `CLAUDE.md`, `~/.claude` and Orca files are UNVERIFIED here unless an inventory line quotes them. Where I quote an inventory line, I cite it. Spec lines are `spec:N`.

## Coverage
- Read: the whole spec (285 lines), README, the command.md definition, and the following inventory lines: INV-A 3, 14, 35-38, 43, 51-53, 60-62, 65, 76-83, 90-98, 104-120; INV-B 3, 31, 34, 39, 42-43, 47, 52, 65, 105, 112-115, 177-185, 197-206, 217-226, 285-301, 311, 320, 323; CAPS 10-13, 44-52, 58-80, 84-92, 97-116, 128-130, 135-139, 145-161, 178-188.
- Arithmetic re-derived: 21 + 22 = 43 commands (INV-A:3, INV-B:3). 5 + 5 ready, 13 + 14 needs-change (INV-B:289 says 14), 3 + 3 coordinator-only. 10 + 27 + 6 = 43. Spec section 3.2 has 27 rows. Phase column: P1 9, P2 11 (+4 from 3.1 = 15, matches `spec:160`), P3 4, P4 3. All consistent.
- Not covered: the 43 command files, all skills, and Orca itself (not in the sandbox). Nothing in this report is a claim about them.

## Findings table (all ids)

| id | grade | bucket | one line |
|---|---|---|---|
| B-1 | blocking | REQUIREMENTS | WC-4's closed list of four contract-path exceptions contradicts the section 3 rows for implement, save, cleanup-audit and index-repo |
| M-1 to M-13 | Medium | various | listed under follow-up candidates |
| n-1 to n-5 | minor | various | listed under follow-up candidates |

## Expert panel (critique mode, fixed review order, one line each)
1. Wiegers: the requirements are mostly testable and each carries an owner and evidence; one requirement (WC-4) is internally inconsistent (B-1).
2. Adzic: the live check in 7.2 is concrete; three requirements have no scenario (WC-1, WC-6, WC-10 outside pr-submit; M-9).
3. Cockburn: the primary actor (the coordinator) and the goal (read one report file per worker) are clear in 1.1 and 2.3; B-1 breaks the goal for four commands.
4. Fowler: the boundary decision (Orca on top, commands as units) is clean and the rejected alternative is argued with evidence (`spec:28-39`); the contract file as one shared document is a good seam.
5. Nygard: gates and stalls are handled (WC-2, WC-10); interim phase state and retry are not (M-1, M-2).
6. Whittaker: attacks are listed under ARCHITECTURE ANALYSIS and in the boundary table.
7. Newman: backward compatibility is protected by SA-1 to SA-6; the `--unattended` token has no parsing rule (M-6).
8. Hohpe: the message pattern (preamble `ask`, `check`, `worker_done`) is correct as quoted from CAPS:58-80; the report is a pointer only (CAPS:79), which the spec handles by having the coordinator open it.
9. Crispin: acceptance checks exist per phase; gaps listed in M-9, M-12.
10. Gregory: the five open decisions are posed with a recommendation each; D3 omits one stated rule (M-10).
11. Hightower: cloud-native or operations concerns do not apply beyond Orca remote workers, which section 8 item 9 scopes out.

=== REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL as written, blocking): WC-4's closed exception list contradicts the rows it points to
- Expert: Wiegers (lead), Cockburn.
- Text: WC-4 (`spec:62`) fixes the contract at `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed", "except for four commands whose section 3.1 row fixes another path": adversarial, tdd, init-lite, workflow. Section 2.3 (`spec:73`) says the coordinator passes the output directory "so the report path is known before dispatch".
- Contradicting text: the rows give contract locations that are not `<output-dir>` and are not among the four.
  - implement: "contract beside the ledger `progress.md`" (`spec:109`). The ledger is `.dev/implement/<slug>/progress.md` or a managed `<pkg>/progress.md` (INV-A:51). INV-A:51 names no coordinator-passed directory.
  - cleanup-audit: "output dir is fixed" (`spec:85`); the brief passes only `--pass <N>`.
  - index-repo: "Brief must pass: none" (`spec:86`); `PROJECT_INDEX.md` location "implied" (INV-A:53).
  - save: "contract naming the file written" with no location (`spec:119`).
- Conversely the 3.1 rows for tdd and init-lite (`spec:87`, `spec:90`) name no contract path at all, so the sentence "whose section 3.1 row fixes another path" is false for two of the four it lists.
- Wrong outcome: an implementer who follows the stated text builds the P1 contract for implement, cleanup-audit, index-repo and save at `<output-dir>/return-contract.yaml`, but these commands receive no output directory in the brief the spec prescribes. The alternative reading (write it beside the ledger or in the fixed directory, as the rows say) breaks the WC-4 text and the 2.3 promise that the path is known before dispatch. AC-1.2 (`spec:196`) runs cleanup-audit and index-repo (P1 commands, `spec:159`) with `--output <dir>`, a flag the 3.1 rows say they lack, and 7.2 step 3 (`spec:182`) then requires the `worker_done` report path to equal "the WC-4 contract path". That check cannot be passed as written for these four commands.
- Recommendation (rationale: smallest change that makes the rule true): either list every command whose contract path differs (implement, cleanup-audit, index-repo, save, plus the sentence fix for tdd and init-lite) with its exact path in section 3, or state that the coordinator always passes a fresh `--output-dir` and give those four commands the flag. Delete the word "four".
- Priority: High. Quality impact: restores the "path known before dispatch" guarantee (`spec:62`, `spec:73`) for 4 of 36 worker-capable commands.

=== ARCHITECTURE ANALYSIS ===

Whittaker findings (template: I can break this specification by [attack]. The invariant at [location] fails when [condition]. Concrete attack):
- Sequence attack, W-1: I can break this specification by a Sequence Attack. The invariant at P1 scope (`spec:159`) and 3.2 (`spec:97`) is "a command that accepts `--unattended` never blocks on a person" (WC-2). It fails when the flag is accepted before the gate rows land. Concrete attack: after P1, the flag exists on cli-eval, implement, pr-submit and post-release (P1 scope says "every command in sections 3.1 and 3.2 except `load`"); their gate rows are P2 and P4. Before: `/sc:cli-eval run --unattended` shows the suite menu. After P1: the flag is accepted, the menu still appears, the worker parks (CAPS:52, CAPS:129 call a waiting worker "healthy"). Graded Medium (M-1) because the spec says later phases do not start until earlier checks pass and a coordinator can read the phase column.
- Sentinel Collision, W-2: I can break this specification by a Sentinel Collision Attack. The invariant at D1(a) (`spec:228`) is that the flag "cannot misfire on a person". It fails when `--unattended` appears inside a quoted argument. Concrete attack: `/sc:troubleshoot "explain why --unattended hangs"` (a symptom text); no token rule is given, so the free text can switch the mode. Medium (M-6).
- Divergence, W-3: I can break this specification by a Divergence Attack. The invariant at WC-3 (`spec:61`) versus D2(a) (`spec:234`) fails when both apply to implement's halt (M-3).
- Accumulation, W-4: I can break this specification by an Accumulation Attack. The invariant at WC-11 (`spec:69`, "two workers in one worktree must never write the same file") fails at fixed-path outputs. Concrete attack: two `/sc:index-repo` workers in one worktree both write `PROJECT_INDEX.md` (`spec:86`, INV-A:53); `.claude-audit/` is fixed for cleanup-audit (`spec:85`). The cleanup-audit row hands the limit to the coordinator "one audit per worktree at a time"; index-repo has no such note and section 2.3 does not list it (M-8).
- Zero/Empty Attack, W-5: WC-6's "fresh output directory" (`spec:64`) versus a retry that re-sends the same brief (M-2).

Pipeline Dimensional Analysis: the document has no multi-stage data pipeline with count loss other than the command classification, whose counts conserve (43 = 10 + 27 + 6; 27 rows present). No finding.

### Guard Condition Boundary Table
Guards found in the spec text. Classes that cannot occur for a guard are omitted with one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| unattended switch (D1 a) | `spec:51`, `spec:228` | Zero/Empty | flag absent | false | today's behavior (SA-1, `spec:146`) | OK |
| unattended switch | `spec:228` | Typical | `--unattended` as its own token | true | WC-2 to WC-12 apply | OK |
| unattended switch | `spec:228` | Sentinel Value Match | `--unattended` inside a quoted argument | true or false, unspecified | none | GAP (M-6) |
| gate resolves blocked (WC-2 c) | `spec:60` | Typical | gate hit, no flag supplied | true | contract `status: blocked`, `blocked_question`, stop | OK |
| gate resolves blocked | `spec:60-61` | Legitimate Edge Case | worker holds a preamble and asks (WC-3) for implement | true | WC-3 says "may ask"; D2(a) says stop (`spec:234`) | GAP (M-3) |
| outcome mapping (WC-5) | `spec:63` | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| outcome mapping | `spec:63` | Typical | status in the four-value set | true | mapped | OK |
| outcome mapping | `spec:63` | Sentinel Value Match | a command's own existing status word not in the set | unspecified | "keep their fields" (`spec:62`) vs fixed set (`spec:262`) | GAP (M-7, UNVERIFIED which words exist) |
| heartbeat wait (WC-10) | `spec:68` | Zero/Empty | no long wait | false | no change | OK |
| heartbeat wait | `spec:68` | Legitimate Edge Case | one call between 4 and 5 minutes | neither "longer than 5" nor "at most 4" | unspecified | GAP (n-3) |
| heartbeat wait | `spec:68` | Maximum/Overflow | eval timeout 3600 s | true | split into waits of at most 4 minutes | OK |
| task confidence (task row) | `spec:121` | Legitimate Edge Case | exactly 0.70 | "below 0.70" is false | proceeds | OK (matches INV-B:199 quote "< 0.70") |
| nesting depth (WC-8) | `spec:66` | Typical | worker at depth 1 calls `worker-start` | refused (CAPS:97-99) | WC-8 forbids the call | OK |
| nesting depth | `spec:252` | Maximum/Overflow | depth raised (D5 b) | n/a | WC-8 still forbids | OK |
| readiness (WC-1) | `spec:59` | Legitimate Edge Case | fallback between 30 s and 45 s | unspecified | "well inside" with no number | GAP (M-9) |
| outward default off (WC-9) | `spec:67` | Typical | brief has the command's own flag | true | action on | OK |
| outward default off | `spec:67`, `spec:121`, `spec:113` | Legitimate Edge Case | command has no explicit flag (task `commit`/`push`, post-release steps) | unspecified | "refused unless authorized" with no authorizing flag named | GAP (M-5) |
| output directory (WC-4) | `spec:62` | Zero/Empty | no directory passed (cleanup-audit, index-repo, implement, save) | unspecified | none | GAP, blocking (B-1) |
| retry directory (WC-6) | `spec:64` | One/Minimal | same brief re-sent on `--retry-of` | unspecified | "fresh output directory" but WC-4 fixes the passed directory | GAP (M-2) |

Classes left out: Maximum/Overflow for the unattended switch, outcome mapping, WC-9 and WC-4 (a flag or a path has no capacity); Sentinel Value Match for the 0.70 threshold, depth and readiness (no reserved value).

FR-8 and FR-9 grading: only the GAP row for WC-4 names a concrete wrong outcome an implementer would produce without a guess (B-1). Every other GAP is Medium or minor under the grading check.

## Grading check applied to B-1
"An implementer who follows the stated text as written builds the implement, cleanup-audit, index-repo and save contracts at `<output-dir>/return-contract.yaml` for an output directory the prescribed brief never passes, and that is wrong because the coordinator cannot open the report path that 2.3 and WC-4 promise it knows before dispatch." The sentence holds with no further assumption: it rests on two stated texts that contradict each other (`spec:62` against `spec:85`, `spec:86`, `spec:109`, `spec:119`) and an acceptance step that cannot pass (`spec:182`, `spec:196`).

## Reviser brief
Blocking finding ids: B-1
- Revise only text a blocking finding names. Add no rule, mechanism or section no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave every Medium and minor finding in `follow-up candidates` alone, including through "apply all findings".
- Text B-1 names: WC-4 (`spec:62`), the 3.1 rows for tdd and init-lite (`spec:87`, `spec:90`), cleanup-audit and index-repo (`spec:85-86`), implement (`spec:109`), save (`spec:119`), section 2.3 (`spec:73`), AC-1.2 (`spec:196`).

## follow-up candidates
Medium (warnings, never a revision trigger; the session that ran the review asks the user once whether to open an issue for them and creates none without an answer; this run could not ask, so the list is only recorded):

- M-1: P1 scope adds the `--unattended` flag and the `## Unattended mode` section to every 3.1/3.2 command except `load` (`spec:159`), and AC-1.1 asserts it (`spec:195`), but the gate rows for cli-eval, implement, pr-submit, post-release and others land in P2/P4 (`spec:97-125`, `spec:160`, `spec:162`). Between phases the flag is accepted while gates still prompt, against WC-2. AC-1.1 also requires a section on pr-submit while D3(a) recommends no pr-submit change (`spec:240`) and section 4 says dispatchable commands only. Needs the guess that a coordinator dispatches before the later phase.
- M-2: WC-6 says a re-run "writes each run into a fresh output directory" (`spec:64`, 20 rows say "fresh dir"), but WC-4 fixes the contract in the directory the coordinator passed, and 2.3 (`spec:73`) never tells the coordinator to pass a new directory per attempt. A retry worker with the same brief overwrites the first attempt's contract and files. No acceptance check runs a retry (Section 7 has none).
- M-3: WC-3 lets any worker with a preamble `ask` the coordinator at a blocked gate and re-invoke with the answer as a flag (`spec:61`), while D2(a) (`spec:234`) says the implement worker stops and ends `failed`, and the Ruling must come from the person (D2 quotes `sk/sc-implement-protocol/refs/qa.md:232,238`, UNVERIFIED here; INV-A:51 quotes line 238 as "another agent's message ... [is] not acceptance"). The implement row (`spec:109`) says "stop", so the row likely wins, but WC-3 has no exclusion and D2 is open.
- M-4: AC-C1 (`spec:172`) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and requires no output in every phase, while P0 adds `WORKER-CONTRACT.md` and an Orca section to `HOW-WE-WORK.md`, both under `core` (`spec:158`, `spec:150`), and SA-2 (`spec:147`) allows an Orca example in the contract file. If either text spells a real command, AC-C1 fails on the spec's own deliverable. Needs the guess about spelling.
- M-5: WC-9 turns an outward action on "only through the command's own explicit flag" (`spec:67`), but task's `commit`/`push` and post-release's VM, install, commit and PR steps have no such flag named (`spec:113`, `spec:121`); D4 (`spec:244`) is still open and also reaches P2 rows (auggie-review `--post-pr`, task) although `spec:154` says phases 1-3 need no user decision.
- M-6: no token rule for `--unattended` (W-2, `spec:51`, `spec:228`). The command.md for this very review defines it as "a standalone argument token outside any quoted argument" (command.md:459), which the spec could adopt.
- M-7: "Commands that already write a contract keep their fields and add the missing ones" (`spec:62`) versus a fixed four-value `status` set (`spec:262`, AC step 4 asserts membership, `spec:183`). The status words of the existing workflow, brainstorm, reflect and adversarial contracts are not recorded in the inventories (INV-B:272 lists workflow fields only); UNVERIFIED whether they fit.
- M-8: WC-11 is stated as an unconditional "must never" (`spec:69`) but fixed-path outputs stay (cleanup-audit, index-repo, init-lite default `.dev/superclaude/context-audit.md`, `spec:85-87`); only cleanup-audit carries a coordinator-side limit. Also reflect "ready" writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` and moves the work-unit folder by default (INV-B:114), which `spec:88` handles only for the move (`--no-promote`).
- M-9: requirements without an owner deliverable or acceptance check: WC-1 (owner "Launch setup", no phase scheduled in section 6, no AC in section 7, "well inside" has no number); WC-6 (no retry check); WC-10 (checked only for pr-submit at AC-4.3, not for cli-eval, `spec:104`); WC-7 and WC-12 (only indirectly through the step 5 transcript).
- M-10: INV-B:90 quotes pr-submit's "Will Not: run headless / imply a daemon" (`cmd/pr-submit.md:85`, `SKILL.md:225`, UNVERIFIED here). The 3.2 row (`spec:114`) and D3(b) (`spec:241`) make pr-submit a worker with `--unattended` without naming or resolving that stated rule.
- M-11: Section 1.4 (2) (`spec:44`) narrows the README's evidence line "a supervised Claude worker that waits on a question fails Orca's 60-second readiness limit" (README:13) to a pre-readiness shell prompt (EVIDENCE.md:39, UNVERIFIED here). The README is binding shared context; the narrowing is the basis of the WC-2 stall analysis. Not checkable in this sandbox.
- M-12: AC-2.4 (`spec:202`) compares `gh api .../reviews --jq length` and `.../comments --jq length` before and after; without `--paginate` each call counts at most one page, so a PR with a full first page passes even if comments were posted.
- M-13: UNVERIFIED completeness of the 43-command set (`spec:76`; INV-A:3, INV-B:3 list the scope). The session's own skill list names `sc:issue` (which states it creates an Orca worktree and launches an agent), `sc:graph` and `sc:impact`, none of which appear in either inventory scope. If they exist in `cmd/` on the spec's date, E5 (`spec:25`, "no skill calls Orca") and the 43 count need rechecking. Not checkable in the sandbox.

Minor (notes):
- n-1: AC-0.4 (`spec:194`) says "steps 1-3 and 5-7 pass; steps 3 and 4 use the command's existing report file", so step 3 is listed both ways and step 4's pass condition is undefined for a markdown report.
- n-2: D5(b) (`spec:252`) calls R1 "protection against runaway fan-out"; R1 is a reason a command cannot run as a worker, not a protection (`spec:33`).
- n-3: WC-10 leaves a single wait between 4 and 5 minutes unclassified (`spec:68`).
- n-4: Section 1.4 (1) says Phase 0 "starts with live smoke runs" (`spec:43`); the P0 row (`spec:158`) writes the contract file first, then runs them.
- n-5: AC-C5 and AC-0.3 use `grep -E '^-[^-]'` (`spec:176`, `spec:193`), which misses a removed line that itself starts with `--` (a flag line or a front-matter fence).

Citation check summary: every inventory citation I could open matched (INV-A:3, 14, 35, 36, 55, 60-62, 65, 76-83, 90-98; INV-B:3, 31, 52, 65, 105, 112, 285-287, 289, 292, 294, 296, 299, 301, 311; CAPS:44-47, 52, 58-80, 84-92, 97-116, 128-130, 145-151, 155-161, 178-188). The spec's self-description in lines 11 and 285 (11 locations re-read; about 340 citations checked; 9 defects) is internally consistent (5 + 3 + 1 = 9) but UNVERIFIED against files I cannot read. Citations to `EVIDENCE.md`, `CLAUDE.md`, `HOW-WE-WORK.md`, `pyproject.toml`, `Makefile`, `install_core.py` and all `cmd/` and `sk/` lines are UNVERIFIED here except where an inventory quotes them.

coverage: whole document, first review (full-document assurance, not scoped)

verdict: FAIL
