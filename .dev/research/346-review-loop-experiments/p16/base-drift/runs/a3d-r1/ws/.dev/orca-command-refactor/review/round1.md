review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: not given. Re-review: not requested. This is a first review of the full document.
- Reviewer model actually used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full). The brief does not widen scope and regrades nothing; no brief clause was overridden.
- Citation convention: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` in the workspace (the only evidence I could check). Any citation to `src/`, `CLAUDE.md`, `~/.claude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...` or Orca guides is UNVERIFIED unless the inventories quote it.
- Focus: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard); Whittaker is active on every review. `--focus correctness` is not active, so no State Variable Registry is produced.

## Coverage

Covered: all of the candidate (`spec:1-285`): decision and rejected alternative (sec. 1), WC-1..WC-12 (sec. 2), the 10/27/6 command split and per-command rows (sec. 3), coordinator-only list (sec. 4), SA-1..SA-6 (sec. 5), phases (sec. 6), acceptance checks (sec. 7), non-goals, decisions D1-D5. Cross-checked against `README.md` (all 38 lines), `commands-a.md` (rows, summary, decisions), `commands-b.md` (rows, notes 265-275, summary), `orca-capabilities.md` (sections 1, 2, 3, 5, 6, 9, 10). Command definition `command.md` (the spec-panel file in the sandbox) was read as a side reference only.

Not covered / UNVERIFIED: every `src/superclaude/...` and `CLAUDE.md` line the spec cites (the workspace has no `src/`). The count and the verdict split were re-derived from the inventories, not from the command files.

## Pipeline Dimensional Analysis (FR-17..FR-21)

Trigger: yes. The spec turns an inventory into a classification and then into phases, and the counts change at each stage. Counts were traced and conserve.

```text
[INV-A: 21 cmds (INV-A:1)] --+
                             +--> [43 cmds, spec:76] --> [Sec 3.1 ready: 10] ----> P0 smoke (3), P1 fixes (adversarial, cleanup-audit, index-repo, workflow), P2 fixes (reflect, release-split, tdd, troubleshoot)
[INV-B: 22 cmds (INV-B:1)] --+                         --> [Sec 3.2 change: 27] --> P1: 9, P2: 11, P3: 4, P4: 3  (9+11+4+3 = 27)
                                                       --> [Sec 4 coordinator-only: 6]
INV-A 5/13/3 + INV-B 5/14/3 = 10/27/6 = 43   (INV-A:73, INV-B:278)
```

No count mismatch (no CRITICAL under FR-19). One consumer assumes a count the producer does not give: AC-1.1 asserts a section in "every command in sections 3.1-3.2" (all 37), but the P1 row (spec:159) and rows `load`, `implement`, `pr-submit` do not give all 37 a contract (finding B-2).

## Guard Condition Boundary Table

Guards identified: G1 `--unattended` switch (spec:51); G2 readiness limit 60 s (spec:59); G3 heartbeat cadence 5 min / wait split 4 min (spec:68); G4 `outcome` mapping (spec:63); G5 nesting depth 1 (spec:33); G6 `confidence < 0.70` (spec:121); G7 contract location `<output-dir>/return-contract.yaml` (spec:62). Classes left out: Maximum/Overflow for G1, G4, G6, G7 (boolean or enumerated, no capacity); Sentinel for G2, G3, G5, G6 (no sentinel value in the text).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| G1 `--unattended` | spec:16,51 | Zero/Empty | flag absent | false | today's behaviour unchanged (SA-1, spec:146) | OK |
| G1 | spec:51 | Typical | `--unattended` present | true | WC-2 gate resolution | OK |
| G1 | spec:112 | Legitimate Edge Case | `load` with `--unattended` | true | no report, no gate, contradicts AC-1.1 (spec:195) | GAP (B-2) |
| G2 readiness | spec:59 | Zero/Empty | no prompt at launch | pass | `state: ready` | OK |
| G2 | spec:59 | Maximum/Overflow | prompt falls back at 30 s / 45 s | pass at 30 s, fail above about 45 s | WC-1 says "well inside" the limit, no number | OK (evidence `EVIDENCE.md:45,56` via spec:59, UNVERIFIED) |
| G3 heartbeat | spec:68 | Typical | wait 4 min | heartbeat possible | allowed | OK |
| G3 | spec:68 | Legitimate Edge Case | wait exactly 4 to 5 min | unspecified wording ("longer than 5 minutes" vs "at most 4 minutes") | split needed for >4 min, only >5 min named as the trigger | GAP (M-5) |
| G4 outcome | spec:63 | Zero/Empty | no report file exists | failed | `--outcome failed` | OK |
| G4 | spec:63 | One/Minimal | `partial` | succeeded | `partial` has no definition of what is partial | GAP (M-4) |
| G4 | spec:63 | Legitimate Edge Case | `blocked` after a successful `ask` and re-run | unspecified | WC-3 re-run overwrites the contract, WC-5 maps the first one | GAP (M-3) |
| G5 depth | spec:33,66 | Typical | worker calls `worker-start` | refused | WC-8 forbids it | OK |
| G6 confidence | spec:121 | Zero/Empty | confidence `0` | true | blocked | OK |
| G6 | spec:121 | Legitimate Edge Case | confidence exactly `0.70` | false | "below 0.70" is blocked; 0.70 proceeds (INV-B:45 quotes "< 0.70") | OK |
| G7 location | spec:62 | Typical | `--output <dir>` | contract at `<dir>/return-contract.yaml` | stated | OK |
| G7 | spec:62,81-92,105,114 | Legitimate Edge Case | `--output <file>` (tdd, init-lite, spec-panel) | `<file>/return-contract.yaml` | impossible for a file | GAP (B-1) |
| G7 | spec:83 | Legitimate Edge Case | adversarial | `<output>/adversarial/return-contract.yaml` | differs from WC-4 | GAP (B-1) |
| G7 | spec:92 | Legitimate Edge Case | workflow, no `--output` | `.dev/tasks/to-do/<id>/return-contract.yaml`, `<id>` unknown before dispatch | contradicts "known before dispatch" | GAP (B-1) |

FR-10 gate: the table is complete for the guards enumerated; each omitted class has its reason above. GAP rows are graded in the findings below (FR-8): B-1 and B-2 are blocking, M-3 to M-5 are Medium.

## === REQUIREMENTS ANALYSIS ===

### B-1 (MAJOR, blocking; Wiegers, Whittaker divergence attack). WC-4 fixes one report location, and the spec's own rows put the contract somewhere else.

Sentence: an implementer who follows the stated text as written builds a contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (`spec:62`), and also builds the rows that say otherwise, and the two cannot both hold.

- WC-4 (`spec:62`): the report path is "known before dispatch", written at `<output-dir>/return-contract.yaml`, and `--output` is named as a directory source.
- Section 3.1 passes `--output <file>` for `tdd` (`spec:90`) and `init-lite` (`spec:87`), and section 3.2 adds `--output` for `spec-panel` (`spec:120`). A file has no child path, so `<file>/return-contract.yaml` cannot exist. The spec never says which directory holds the contract for a file-valued `--output`. Two tdd workers given `a.md` and `b.md` in one folder would write the same `return-contract.yaml` if the parent is chosen, which also breaks WC-11 (`spec:69`).
- The P1 fix for adversarial is a different path, `<output>/adversarial/return-contract.yaml` (`spec:83`), not `<output>/return-contract.yaml`. AC-1.2 and 7.2 step 4 (`spec:182,195-196`) open "the WC-4 contract path". An implementer who applies the adversarial row produces a file the check does not look at.
- For workflow the contract lives in `.dev/tasks/to-do/<id>/` (`spec:92`), the brief passes no output directory (`spec:92`), and the id is created by the command (`INV-B:272-273`). The coordinator cannot know the path "before dispatch", and the P1 fix "write the contract for pre-creation STOPs too" (`spec:92`) has no `<id>` to put it under, since a pre-creation STOP happens before an id exists (`INV-B:272`).
- Corroboration outside the brief's evidence: the command definition under review already resolves the same conflict with a directory-valued `--report-dir` because "`--output` is file-valued" (`command.md:460-461`). That contradicts the candidate's `--output` as a directory source.

Recommendation (narrow, no new mechanism): state one rule for where the contract goes when `--output` is a file, and either bring the adversarial and workflow rows into line with WC-4 or name them as WC-4 exceptions with the exact path the coordinator is told.
Priority: High. Impact: coordinators open a path that does not exist, and the AC-1.2 and AC-2.x live checks fail for three named commands.

### B-2 (MAJOR, blocking; Wiegers traceability, Adzic). AC-1.1 and the P1 row require what the section 3 rows and decision D3 say is not done.

Sentence: an implementer who follows the stated text as written adds a `## Unattended mode` section naming `return-contract.yaml` to every command in sections 3.1 and 3.2 in Phase 1 (`spec:159,195`), and that is wrong because the same sections say otherwise for at least `load` and `pr-submit`, and say Phase 1 does not yet contain the gate behaviour for the rest.

- AC-1.1 (`spec:195`): the test asserts every command in sections 3.1-3.2 has the section "naming `return-contract.yaml`". The `load` row says "Report: none", "n/a", "use it as a step inside another worker's brief, not as its own Task" (`spec:112`), and WC-4 requires a contract on every outcome. A `load` section that names `return-contract.yaml` writes no contract, or the row must be changed. The test cannot pass without breaking one of them.
- The P1 row requires "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (`spec:159`). The same sections assign auggie-review, cleanup, cli-eval, cli-portify and others to P2 (`spec:100,103-105`) and implement, post-release and pr-submit to P4, which "waits for answers to D2-D4" (`spec:154,162`). Between P1 and P2/P4 the flag is accepted but the gate and the outward-default switch-off (`spec:100`, WC-9) are not yet implemented. A coordinator told "P1 passed" can dispatch `/sc:auggie-review <PR> --unattended`, which still posts to the PR by default (`cmd/auggie-review.md:51-54` via `INV-A:38,62`), and `/sc:pr-submit --unattended`, which still prompts at `--monitor 1`. The spec does not say a command must refuse `--unattended` until its own phase lands.
- D3 recommends (a) "Coordinator or person only ... no pr-submit changes in Phase 4" (`spec:240`), and section 4 says pr-submit "stays a worker candidate only if the user accepts D3" (`spec:139`). Yet pr-submit is one of the 27 counted commands (`spec:76`) and is covered by AC-1.1. With D3(a) chosen, AC-1.1 asserts a section in a command the plan leaves unchanged.

Recommendation: restrict the AC-1.1 assertion and the P1 flag requirement to the commands whose phase delivers them (or state that a command refuses `--unattended` until its phase lands), and mark `load` and `pr-submit` as exceptions.
Priority: High. Impact: AC-1.1 cannot pass as written; the interim state accepts `--unattended` where gates and outward defaults are still on.

## === ARCHITECTURE ANALYSIS ===

Architecture decision (Orca coordinates, commands stay units of work): consistent with CAPS:97-103 (depth 1), CAPS:147-149 (standalone needs no Orca), CAPS:150 (`worker_done` from the dispatched pane) and the single-owner-orchestrator reading (`INV-A:90`, `INV-B:285-286`). No blocking architectural defect found in section 1. Evidence gap 1.4 (1) is stated plainly and Phase 0 tests it.

### M-1 (Medium; Fowler, Nygard). The AC-C1 grep contradicts the P0 work it gates.
AC-C1 (`spec:172`) requires that `grep` for `orca orchestration|worktree|terminal|agent` in `src/superclaude/{commands,skills,agents,core}` prints nothing. P0 adds `src/superclaude/core/WORKER-CONTRACT.md` (`spec:52,158`) and an Orca section in `src/superclaude/core/HOW-WE-WORK.md` (`spec:150,158`), and SA-2 permits an Orca mention as "an example of a caller's question channel inside the contract file" (`spec:147`). If those files name the commands, the common check fails at P0. Whether they will is a guess about wording the spec does not fix, so this is Medium. A narrower allowance (exclude the two core files, or ban only `commands/skills/agents`) removes the question. The baseline `grep -ci orca HOW-WE-WORK.md` is `0` per `spec:25` (UNVERIFIED).

### M-2 (Medium; Nygard, Whittaker sequence attack). WC-3 permits `ask`, AC-2.2 requires `failed`.
WC-3 says the worker "may instead ask the coordinator once" (`spec:61`). AC-2.2 requires the gate-trigger run to end with `worker_done --outcome failed` and contract `status: blocked` (`spec:200`), and 7.2 step 3 waits for exactly one `worker_done` (`spec:182`). A worker that chooses `ask` produces a `question` message first and no `worker_done` until answered. Section 2.3 (`spec:73`) does not tell the coordinator to forbid `ask` for the test. Graded Medium: it needs a guess that the worker chooses to ask.

### M-3 (Medium; Nygard, Whittaker). Re-run after a blocked contract and WC-6 fresh directories disagree with a path fixed before dispatch.
WC-6 says a command without a resume flag "writes each run into a fresh output directory" (`spec:64`); that describes about 20 rows with "fresh dir" in section 3. WC-4 says the report path is known before dispatch (`spec:62`). If the command creates the fresh directory, the path is no longer the one in the brief; if the coordinator creates it, section 2.3 does not say so (`spec:73`). WC-3 also re-invokes the command after a blocked answer (`spec:61`), which overwrites the `blocked` contract the first attempt wrote. Which attempt `worker_done` reports is not stated.

### M-4 (Medium; Wiegers). `partial` has no definition.
`partial` maps to `succeeded` (`spec:63,263`), and the spec says the first sentence of the body still says `partial`. No row says which commands can produce `partial` or what a coordinator does with it. A half-written deliverable then arrives as `succeeded` in Orca's record (`CAPS:73` accepts only two outcomes).

### M-5 (Medium; Adzic). WC-10 states the wait limit two ways.
"longer than 5 minutes" is the trigger and "at most 4 minutes" is the size (`spec:68`). A 4.5-minute wait is neither required nor forbidden. The heartbeat cadence itself is from the preamble, UNVERIFIED (`CAPS:130`).

## === OTHER MEDIUM AND MINOR FINDINGS ===

### M-6 (Medium; Crispin, Whittaker sequence). AC-C5 and AC-0.3 miss deleted bullet lines.
`git diff -U0 ... | grep -E '^-[^-]'` (`spec:176,193`) is meant to print every deleted line. A deleted markdown bullet `- text` appears in the diff as `-- text`, whose second character is `-`, so the pattern skips it. Checked in the sandbox: `printf -- '-- old bullet\n-| row\n-plain\n' | grep -E '^-[^-]'` printed only the last two lines. Command files are mostly bullets, so SA-4 "additive" (`spec:149`) can be broken without the check noticing. Medium: the stated text builds a gate with a hole, but no wrong deliverable follows from it by itself.

### M-7 (Medium; Fowler). SA-3 is wider than WC-4.
SA-3 allows the contract "in unattended mode or when the caller passes the new output flag" (`spec:148`); WC-4 writes it "in unattended mode" (`spec:62`); AC-1.3 tests the case with neither (`spec:197`). The case "new output flag, no `--unattended`" has no stated result.

### M-8 (Medium; Nygard). Tasklist and reflect rely on a headless rule the spec has not read.
The tasklist row passes `--unattended` to each reflect "so the headless rule applies" (`spec:122`) and the reflect row says `--remediate` should "follow the existing headless auto-accept rule" (`spec:88`). The spec does not say what auto-accept does (it can start a remediation handoff in each of N reflect subagents). INV-B proposed dropping `--remediate` at Stage 10.5 instead (`INV-B:46,295`). The rule text (`sk/sc-reflect-protocol/refs/remediation-handoff.md:239-247`) is not in the workspace: UNVERIFIED. The spec's own UNVERIFIED item 9 (`spec:280`) says the headless signal is `claude --print`. Result of the choice is not stated, so it stays Medium.

### M-9 (Medium; Crispin). Live check step 2 may not see the stall WC-2 is about.
Step 2 passes when `observation.agentWait` is never non-null (`spec:181`). Section 1.4 (2) says a plain chat question is a silent stall (`spec:44`), and `CAPS:125` says a null `agentWait` is "absence". The check can pass on a worker stalled on a chat question; only step 5's transcript search (`spec:184`) would catch an `AskUserQuestion`, not a chat question.

### M-10 (Medium; Hightower). Phase 0 smoke runs close evidence gap 1.4 (1) for only 3 of the 10 ready commands, and the rest of P1 to P4 are described as ready from reading alone (`INV-B:323`). Spec states the gap (`spec:43`); noted here because the 10/27/6 counts stay unverified in practice.

### Minor notes (never blocking)
- n-1: Section 4 cites `.dev/orca-command-refactor/README.md:31` for `/sc:git` authorization (`spec:133`); that README line is a rule for this run (no commits or pushes), not a policy for the repo. The same cite sits in `INV-A:49`.
- n-2: AC-C1 and AC-0.3 are written inside Markdown table cells with `\|`; copied raw, they are not valid shell. Put them in a fenced block.
- n-3: Section 3 header says "43 commands ... 10 ready today" but `reflect`, `release-split`, `tdd`, `troubleshoot` carry a P2 change (`spec:88-91`); "ready" means ready with the stated flags only. The wording at `spec:79` says this; the heading does not.
- n-4: The `/sc:spec-panel` row cites `cmd/spec-panel.md:34-35,222,451,455` (`spec:120`). In the command definition read in the sandbox, lines 34-35 are the Synthesize and Improve steps and 455 is the start of an `## Unattended mode` section (`command.md:34-35,455-465`). That definition is a different revision than the one the spec saw, so the row may be stale; UNVERIFIED.
- n-5: Spec section 1.2 E5 and R2 cite `CLAUDE.md:74` and a `grep` run; neither can be checked here: UNVERIFIED.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- Divergence attack on WC-4: file-valued `--output` against directory-valued `<output-dir>`. State trace: before, brief says `--output .dev/out/a.md`; after, contract path is `.dev/out/a.md/return-contract.yaml` (impossible) or `.dev/out/return-contract.yaml` (shared with `b.md`). Reported as B-1.
- Sequence attack on P1/P4: after P1 passes, `/sc:auggie-review <PR> --unattended` is accepted and still posts. State trace: P1 done, P2 not started, flag accepted, default `--post-pr` unchanged (`INV-A:38`). Reported as B-2.
- Sentinel collision: `blocked` and `failed` both map to `--outcome failed` (`spec:63`); the coordinator separates them only by opening the contract. Stated in WC-4 and 2.3; no finding.
- Accumulation attack: three consecutive failed starts circuit-break a Task (`CAPS:80,116`); blocked workers end `failed` through `worker_done`, which the guide says does not count (`CAPS:80`). No finding.
- Zero/empty attack: no report exists maps to `failed` (`spec:63`); `artifacts: []` allowed; fine.

## Consensus and disagreements

- Consensus: the decision, the rejected alternative and the 10/27/6 split are consistent with the inventories (counts traced above) and with the Orca facts the inventories quote (`CAPS:97-103,145-161`).
- Disagreement (Wiegers vs Fowler): Wiegers wants the report-path rule to be exact for every command (B-1); Fowler would accept a short list of named exceptions. Both fix the defect.

## Follow-up candidates (Medium and minor, not blocking, not in the Reviser brief)

M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, n-1, n-2, n-3, n-4, n-5. The review session is to ask the user once whether to open an issue for these; this run created none and asked nothing (non-interactive worker). Unattended behaviour: list recorded only.

## Reviser brief

Blocking finding ids: B-1, B-2. Repair only the text these ids name in the candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table row cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the file's byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone; do not apply "all findings"; do not award yourself a PASS.
- B-1: make the contract location unambiguous for file-valued `--output`, and align or name as exceptions the adversarial row (`spec:83`) and the workflow row (`spec:92`).
- B-2: make the AC-1.1 assertion and the P1 flag requirement (`spec:159,195`) match the rows for `load`, `pr-submit` (D3) and the commands assigned to P2 and P4.

verdict: FAIL
