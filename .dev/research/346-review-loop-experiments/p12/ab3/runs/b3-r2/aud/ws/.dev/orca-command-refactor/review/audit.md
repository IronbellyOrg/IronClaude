review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (`/sc:spec-panel --mode critique --focus requirements,architecture`)

Spec-panel report. Labelled whole-document audit, first review of the full document.

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `3df6411553609a3781774f54ed644139d6073eeb6265fab7bf239562e2658b99`
- baseline: not given (no `--re-review`, no `--baseline`); baseline sha256: n/a. This is a first review of the whole document, not a scoped re-review.
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full).
- evidence available inside the workspace: `.dev/orca-command-refactor/README.md`, `inventory/commands-a.md` (120 lines), `inventory/commands-b.md` (323 lines), `inventory/orca-capabilities.md` (188 lines). Nothing else is readable. Every citation into `src/superclaude/...`, `CLAUDE.md`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `pyproject.toml`, `Makefile` and Orca guide text can only be checked through the inventory line that quotes it; where it cannot, it is marked UNVERIFIED below.
- Improve step: not run. The command was run for a critique; the brief says edit nothing else. No revised specification is written. Candidate not edited.

## Coverage (what was and was not checked)

Covered: the whole spec (sections 1-9, Decisions, UNVERIFIED list) read end to end; internal consistency of counts, phases, WC/SA/AC ids; every `INV-A:`, `INV-B:`, `CAPS:` citation spot-checked against the inventories (about 60 lines opened); the panel sequence Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower applied through the requirements and architecture focus.

Checked and found as cited: 43 = 21 + 22 commands (`commands-a.md:3`, `commands-b.md:3` list 21 and 22 names); 10 ready, 27 needs-change, 6 coordinator-only (spec rows `orca-worker-contract-spec.md:81-92`, `97-125`, `131-137` sum to 10, 27, 6); phase lists at spec `:159-162` cover exactly the 37 worker-capable commands once each; `INV-A:90-92,94-98,106`, `INV-B:272,285-286,301,311,320,323`, `CAPS:44-47,52,72-79,97-103,129-130,145-151,155-161` match what the spec says they say.

Not covered: any claim whose only source is a file outside the workspace (see UNVERIFIED citations at the end). Not run: anything (planning only).

Pipeline Dimensional Analysis: not triggered. The spec describes no multi-stage data pipeline whose output count diverges from its input count; the Task fan-out is a coordinator concern, not a count-changing data flow. No Quantity Flow Diagram is produced. State Variable Registry: not required (`--focus correctness` not active).

## Findings summary

| id | grade | bucket | one line |
|---|---|---|---|
| F1 | blocking (MAJOR) | requirements | `index` row says to state that knowledge-base mode does not wait, but UNVERIFIED item 6 says section 3 refuses or pins that mode |
| M1 | Medium | requirements | WC-4 contract path undefined for commands whose row adds no output flag or path |
| M2 | Medium | requirements | blocked report cannot be written when the missing item is the output directory itself |
| M3 | Medium | requirements | WC-4 four-value `status` set vs "keep their fields" for existing contracts |
| M4 | Medium | architecture | tasklist row asserts reflect fan-out is inside the nesting limit and relies on headless auto-accept without evidence |
| M5 | Medium | requirements | "own explicit flag" authorizing outward actions is not defined for task and post-release |
| M6 | Medium | requirements | AC-C1 grep contradicts the SA-2 allowance and is weaker than SA-2 |
| M7 | Medium | requirements | AC-0.4 steps 3 and 4 cannot be applied literally to troubleshoot, which has no contract |
| M8 | Medium | requirements | WC-10 (5 minutes) vs AC-4.3 (240 s) thresholds differ; gap between 4 and 5 minutes |
| M9 | Medium | architecture | `partial` maps to `succeeded`, so Orca DAG dependents start on an incomplete deliverable |
| N1-N5 | minor | mixed | notes, below |

## === REQUIREMENTS ANALYSIS ===

Lead experts: Wiegers, Adzic, Cockburn (then Crispin, Gregory on the acceptance checks).

### F1. `index` unattended handling contradicts UNVERIFIED item 6 (blocking)

- Severity: MAJOR, graded blocking. Expert: Wiegers (consistency), Whittaker (Sequence/Divergence attack). Priority: High.
- Stated text A: section 3.2 `index` row, gate resolution column: "state that knowledge-base mode does not wait (whether it does is UNVERIFIED)" (`orca-worker-contract-spec.md:111`). The row's own parenthesis admits the fact is unknown; the inventory says the same: "no gate described, so whether it waits is UNVERIFIED" (`inventory/commands-a.md:54`, `:113`).
- Stated text B: UNVERIFIED item 6: "Whether `/sc:business-panel --mode socratic`, `/sc:explain --format interactive` and `/sc:index`'s knowledge-base mode wait for a person; section 3 refuses or pins them under `--unattended` regardless" (`orca-worker-contract-spec.md:277`).
- Grading sentence: an implementer who follows row `:111` as written adds one sentence to `/sc:index` saying knowledge-base mode does not wait, and builds an unattended mode that does not refuse or pin that mode; that is wrong because item 6 (`:277`) promises it is refused or pinned "regardless", WC-2 forbids any person-blocking step in unattended mode (`:60`), and a worker parked on a prompt is "healthy" and invisible to the coordinator (`CAPS:52`, `CAPS:129`, spec `:44`), so if the mode does wait the worker silently stalls with no `worker_done`. The other two modes in item 6 are handled as item 6 says (business-panel `--mode socratic` refused, `:102`; explain `--format interactive` refused, `:108`); `index` alone is not, so the two texts contradict.
- Recommendation: make the `index` row match its siblings (refuse or pin the knowledge-base mode under `--unattended`), or, if the mode is meant to stay allowed, change item 6 to say so and state how the fact will be verified before P1. Delete rather than add: the row text "state that ... does not wait" can be replaced by the same refuse/pin wording the two sibling rows use.
- Quality-impact estimate: low effort, removes the only unguarded silent-stall path among the P1 "no gate" commands.

### M1. WC-4 contract path undefined for several commands (Medium)

- Expert: Wiegers (testability), Crispin. Priority: Medium.
- WC-4 says the contract goes to `<output-dir>/return-contract.yaml` "where `<output-dir>` is the directory the coordinator passed", "known before dispatch" (`orca-worker-contract-spec.md:62`). These rows add a contract but name neither an output flag nor a contract path: research (`:116`, "contract naming the generated `claudedocs/research_*.md` path"), recommend (`:115`), save (`:119`), task (`:121`), review-translation (`:117`, "contract pointing at the `reports/localization/` files"). Check 7.2 step 3 needs "the contract path WC-4 or the command's section 3 row gives" (`:182`), which does not exist for these five.
- Why Medium: the document never states the missing requirement (an output flag or fixed path for these commands); an implementer must guess one. Not a stated text that does harm.
- Recommendation: add one fixed contract path per row, or one default rule in WC-4 (for example, a stated default directory when no output flag exists).

### M2. Blocked report with no output directory (Medium)

- Expert: Whittaker, Zero/Empty Attack. Priority: Medium.
- Concrete attack: the brief omits `--output`. For post-release the row says "require an explicit `--output` ... else blocked" (`orca-worker-contract-spec.md:113`), and the blocked outcome must be written to a contract (WC-2 (c), `:60`; WC-4 "written on every outcome", `:62`). The contract path is `<output-dir>/...` and the directory is the thing that is missing. State trace before: no output dir; after: spec says a contract exists, but gives no location. WC-5 then falls to "or no report exists" so the outcome is `failed` without the question (`:63`).
- Why Medium: a requirement the document never states (a fallback location, or "print the refusal and exit failed"), not text that does harm.
- Recommendation: one sentence in WC-4 stating the fallback.

### M3. Status vocabulary vs existing contracts (Medium)

- Expert: Wiegers. Priority: Medium.
- WC-4 fixes four `status` values and says commands that already write a contract "keep their fields and add the missing ones" (`orca-worker-contract-spec.md:62`). The check asserts `d['status'] in {'succeeded','partial','failed','blocked'}` (`:183`). The inventory records that workflow's contract has a `status` field (`inventory/commands-b.md:272`) but not its values; adversarial, brainstorm and reflect contracts are cited without values (`commands-a.md:97`, `commands-b.md:112`). If an existing contract uses other values, "keep their fields" and the step-4 assertion disagree.
- Why Medium: depends on values nobody read.
- Recommendation: state which wins, or list the existing values.

### M5. Outward-action flag not defined (Medium)

- Expert: Wiegers, Nygard. Priority: Medium.
- WC-9 turns an outward default on "only through the command's own explicit flag written in the brief" (`orca-worker-contract-spec.md:67`). For auggie-review the flag exists (`--post-pr`, `:100`). For task `commit`/`push` ("refused unless authorized", `:121`) and post-release ("VM, real-target install, commit and PR off unless the brief authorizes them", `:113`) no flag is named, and D4 (`:244-247`) leaves the decision to the user. P2 contains task (`:160`), so P2 depends on a flag that is only defined for P4.
- Safety direction is fine (off by default); the gap is that no authorization path exists to build. Medium.

### M6. AC-C1 versus SA-2 (Medium)

- Expert: Crispin, Whittaker. Priority: Medium.
- SA-2 allows one Orca mention in a changed file: "as an example of a caller's question channel inside the contract file" (`orca-worker-contract-spec.md:147`). AC-C1 greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` and expects nothing (`:172`); the contract file lives in `src/superclaude/core` (`:52`) and P0 also adds an Orca section to `HOW-WE-WORK.md` in the same folder (`:158`, SA-5 `:150`). An example written as a command (`orca orchestration ask`) fails AC-C1; an example written as prose passes. The text does not say which form.
- Also: AC-C1 matches four verbs only, while SA-2 says no file "runs an `orca` or `orca-ide` command"; `orca-ide skills`, `orca-ide status` and others would pass.
- Also: in the raw markdown the pattern is written `(orchestration\|worktree\|...)` and the pipeline as `\| grep -v` (`:172`); copied verbatim, `\|` is a literal pipe in `grep -E` and the check never matches. The same applies to AC-C4, AC-C5, AC-0.3 (`:175,176,193`). Medium: needs a guess on how the implementer reads the table.
- Recommendation: state the allowed form of the example and exclude the contract file or write the pattern in a code block.

### M7. AC-0.4 steps 3 and 4 for troubleshoot (Medium)

- Expert: Crispin, Gregory. Priority: Medium.
- AC-0.4 requires "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (`orca-worker-contract-spec.md:194`). Step 3 needs the `--outcome` to match "the contract's status" (`:182`), and troubleshoot writes `REPORT.md`, not a contract (`:91`). Step 4's assertion needs `d['status']` and `d['command']` (`:183`), which a markdown report cannot satisfy. A failure here "reopens section 1" (`:194`), so a false failure is costly.
- Why Medium: a reader can reasonably apply "uses the existing report" to step 3 as well; it takes a guess, so not blocking.
- Recommendation: replace "step 4 uses the existing report file" by an explicit weaker check for the three P0 commands.

### M8. Wait thresholds (Medium)

- Expert: Nygard, Whittaker (Divergence Attack at the boundary). Priority: Medium.
- WC-10 requires splitting only a step that blocks "longer than 5 minutes", into waits of "at most 4 minutes" (`orca-worker-contract-spec.md:68`). A single call of 4.5 minutes needs no split under WC-10 but would be accepted by neither the Decisions row (4 minutes for margin, `:266`) nor AC-4.3, which fails any call over 240 s (`:210`). The pr-submit row asks for iterations "under 4 minutes" (`:114`). Pick one threshold. Medium: the stricter reading is inferable.

### Notes (minor)

- N1. E2 cites `CAPS:161` for "`[H:worker-start]` line 38, `--agent claude`" (`orca-worker-contract-spec.md:22`). `inventory/orca-capabilities.md:161` is the pr-submit top-level rule, not that quote; no line in the capabilities file carries `[H:worker-start]` line 38. Mis-cited, claim itself is supported by `commands-a.md:12`.
- N2. E3 states "It has worked before" and cites `invocation_method: "skill-direct"` (`orca-worker-contract-spec.md:23`), while section 1.4 (1) says the PR #329 brief used an Agent-tool subagent and proves only the nested route (`:43`; `CAPS:156,187`). Reconciled in 1.4, but E3's wording is stronger than the evidence it relies on.
- N3. Section 6 says "Phases 1-3 need no user decision" (`orca-worker-contract-spec.md:154`) while section 9 says "Phases 0-3 can proceed on the recommendations" (`:225`) and D1 and D4 affect P1 and P2. Wording only.
- N4. The `--unattended` token is free text in prompt-style commands (tdd, research, troubleshoot, workflow, task). The spec does not say a quoted occurrence inside the topic text must not switch the mode (D1, `:228`, says it "cannot misfire on a person" only). Sentinel Collision note.
- N5. AC-1.3 says "in a scratch worktree" (`orca-worker-contract-spec.md:197`) without saying how it is created; the repo rule allows worktrees only through Orca with an agent (`CLAUDE.md` rule, quoted in the run context; not in the workspace, UNVERIFIED here).

## === ARCHITECTURE ANALYSIS ===

Lead experts: Fowler, Newman, Hohpe, Nygard.

Assessment of the main decision (section 1): sound. Orca coordinates, commands stay units of work; the rejected alternative has five independent reasons R1-R5 (`orca-worker-contract-spec.md:29-37`), each backed by a capabilities line that was found as cited (`CAPS:97-103,145-150`). The three evidence gaps are stated plainly (`:41-45`), and Phase 0 tests the decision first (`:158`). The interface boundary is small (flag, report file, resume) and written once in a shared core file (`:52`), which is the right segregation. Section 4 correctly keeps orchestrators (agent, pm, spawn) out of the worker set (`INV-A:90`, `INV-B:285-286`).

### M4. tasklist nesting and headless auto-accept (Medium)

- Expert: Fowler (data flow / layers), Nygard (failure mode). Priority: Medium.
- Spec row: Stage 10.5 passes `--unattended` to each reflect "so the headless rule applies"; "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`" (`orca-worker-contract-spec.md:122`). The inventory's own verdict was different: call reflect without `--remediate`, and run the per-phase reflect fan-out at the worker's top level (`inventory/commands-b.md:215`), with nested spawning recorded as UNVERIFIED (`commands-b.md` UNVERIFIED items 1 and 8). `INV-A:14` gives a limit of three layers and warns that at the limit the Agent tool is silently withheld. Reflect itself spawns agents (`commands-b.md:111`) and its auto-accepted remediation hands off to workflow or task-builder (`commands-b.md:109`); that is more than one layer below the worker.
- Consequence: the "one layer" claim understates the depth, and the auto-accept turns on remediation work inside subagents that the inventory wanted off. The spec's own UNVERIFIED item 9 admits reflect's headless behaviour in an Orca worker is assumed not to apply (`:280`), yet the row relies on it. The row also does not resolve the `needs_human_decision` HALT recorded at `commands-b.md:209`.
- Why Medium: the wrong outcome requires a guess about how Claude Code counts layers; not provable from the text.
- Recommendation: either keep the inventory's choice (no `--remediate` under `--unattended`, which is smaller) or add the verification to P0.

### M9. `partial` maps to `succeeded` (Medium)

- Expert: Hohpe (message semantics), Nygard. Priority: Medium.
- WC-5 and the Decisions row map `partial` to `--outcome succeeded` (`orca-worker-contract-spec.md:63,263`). Orca settles the Task as succeeded and starts no retry, and dependents of a completed Task become startable (`CAPS:34`; a failed Task keeps dependents blocked, `CAPS:90`). A coordinator following the DAG would start downstream Tasks on an incomplete deliverable unless it reads the body. The spec says the body and contract "still say `partial`", so nothing is hidden, but section 2.3 does not tell the coordinator to check status before starting dependents.
- Recommendation: add that instruction to 2.3 (one sentence), or map `partial` to `failed`.

### Other architecture observations (no finding)

- Hohpe: the report-file-plus-`worker_done --report-path` design is a claim-check pattern; Orca does not read the file (`CAPS:79`, spec UNVERIFIED 3), which the spec states and handles by making the coordinator open it (`orca-worker-contract-spec.md:62`). Good.
- Newman: backward compatibility is handled by SA-1 to SA-6 and AC-1.3, AC-2.5. Good.
- Hightower: operational limits (heartbeat 5 min, readiness 60 s, depth 1) are all stated with sources.

## Guard Condition Boundary Table

Guards identified in the spec: readiness limit (WC-1), heartbeat/wait split (WC-10), nesting depth (R1), outcome mapping (WC-5), unattended without output directory (WC-4), `--monitor 1` (pr-submit row), `target_release` (spec-panel row). Classes left out per guard are given in one line each.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| readiness limit 60 s | WC-1 `:59` | Typical | prompt falls back at 30 s | pass | worker-start succeeds (`EVIDENCE.md:45`, via `CAPS:49`) | OK |
| readiness limit 60 s | WC-1 `:59` | Maximum/Overflow | fallback above about 45 s | fail | worker-start fails again (`:59`, evidence UNVERIFIED here) | OK |
| readiness limit 60 s | WC-1 `:59` | Legitimate Edge Case | `--timeout-ms` raised | pass | `CAPS:45` allows it; WC-1 asks only for "well inside" the limit | OK |
| wait split | WC-10 `:68` | Zero/Empty | wait of 0 s | n/a | none needed | OK |
| wait split | WC-10 `:68` | Typical | one call of 3 min | no split | no split required | OK |
| wait split | WC-10 `:68` | Maximum/Overflow | one call of 4.5 min | no split under WC-10; fail under AC-4.3 (`:210`) | WC-10 silent; AC-4.3 stricter | GAP (M8) |
| nesting depth 1 | R1 `:33`, WC-8 `:66` | Legitimate Edge Case | worker calls `task-create` | unknown | forbidden by WC-8 whatever Orca does | OK |
| unattended, output dir | WC-4 `:62` | Zero/Empty | `--output` omitted, post-release | gate says blocked | no location for the blocked contract | GAP (M2) |
| unattended, output dir | WC-4 `:62` | Typical | `--output <dir>` | pass | contract `<dir>/return-contract.yaml` | OK |
| contract path | WC-4 `:62` | Legitimate Edge Case | research, recommend, save, task, review-translation | no output flag | path not stated | GAP (M1) |
| outcome mapping | WC-5 `:63` | Sentinel Value Match | `status: partial` | maps to `succeeded` | stated; dependents effect not stated | GAP (M9) |
| outcome mapping | WC-5 `:63` | One/Minimal | audit with verdict FAIL | maps to `succeeded` | stated explicitly | OK |
| `--monitor 1` | pr-submit row `:114` | Legitimate Edge Case | `--unattended --monitor 1` | refused | stated | OK |
| `target_release` | spec-panel row `:120` | Zero/Empty | TDD input, flag absent | blocked | stated | OK |
| index knowledge-base mode | index row `:111` | Legitimate Edge Case | mode that may wait | unknown | row asserts "does not wait" without refuse/pin | GAP (F1) |

FR-8/FR-9: GAP rows graded by consequence. The `index` row (F1) names a concrete wrong outcome (silent stall) and contradicts a stated text, so it is blocking; the other four GAP rows are Medium (M1, M2, M8, M9). FR-9 blank behaviors: the blocked-contract location (M2) and the contract path for five commands (M1) are the two unspecified entries. FR-10: the table is complete for the guards identified above; classes left out are Zero/Empty for the wait split (a 0-second wait cannot occur) and Maximum for `--monitor 1` (a flag, not a quantity).

## Adversarial analysis (Whittaker)

- I can break this specification by **Sequence Attack**. The invariant at **WC-2 / `index` row (`:60`, `:111`)** fails when **knowledge-base mode waits for a person**. Concrete attack: coordinator dispatches `/sc:index --unattended <kb-mode input>`; before: worker `state: ready`; after: worker parked on a prompt, `agentWait` set only if the coordinator polls `worker-show`, no `worker_done`, no contract (F1).
- I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (`:62`)** fails when **the brief names no output directory**. Concrete attack: post-release dispatched without `--output`; gate resolves blocked; contract location undefined; outcome falls to `failed` with no question (M2).
- I can break this specification by **Accumulation Attack**. The invariant at **WC-6 / cleanup-audit row (`:85`)** fails when **two audits run in one worktree**. Concrete attack: the output directory `.claude-audit/` is fixed, the row says one audit per worktree at a time but nothing enforces it; the second worker overwrites `progress.json` and the contract. The spec states the limit, so this is a note, not a finding.
- Divergence Attack and Sentinel Collision: see M8 and N4.

## Follow-up candidates (Medium and minor, none blocking, none trigger a revision)

M1, M2, M3, M4, M5, M6, M7, M8, M9, N1, N2, N3, N4, N5 as above. Whether to open an issue for them is a question for the user, to be asked once by the session that coordinates this loop; this run cannot ask (final reply is restricted) and created none.

## UNVERIFIED citations (cannot be checked from the workspace)

- Spec `:11` (11 locations "re-read" by the spec's author), `:285` (340-citation check): self-reports, not checkable.
- All `src/superclaude/...`, `cmd/`, `sk/` lines used as primary evidence in sections 2-3, 7 (for example `sk/sc-implement-protocol/refs/qa.md:231-238`, `cmd/auggie-review.md:51-54`, `cmd/save.md:42-45`): checked only through the inventory rows that quote them.
- `CLAUDE.md:16,50,72-83,157,334,408`, `src/superclaude/cli/install_core.py:4,13-24,33`, `pyproject.toml:38`, `Makefile:68-74`, `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254`, `src/superclaude/core/CLAUDE.md:65`: not in the workspace.
- `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39,45,56` and `.dev/codegraph-migration/...:31,33,42` and `.../return-contract.yaml:10`: not in the workspace; the inventories quote lines 39 and 45 (`commands-a.md:12`, `orca-capabilities.md:49`).
- Spec `:25` grep results (E5): not re-runnable here.

## Reviser brief

Blocking finding ids: F1.

Rules for the reviser (restating the Reviser contract; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.

Finding F1: in `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` the `index` row (`:111`) and UNVERIFIED item 6 (`:277`) contradict each other about whether knowledge-base mode is refused or pinned under `--unattended`. Make the two texts agree, preferably by giving `index` the same refuse-or-pin resolution as the business-panel and explain rows.

Brief clauses overridden: none (the brief gave no clause that widened scope).

verdict: FAIL
