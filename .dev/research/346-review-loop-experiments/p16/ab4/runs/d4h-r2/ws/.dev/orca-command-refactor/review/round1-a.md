review: 1 of 3

# Spec-panel critique (`--mode critique --focus requirements,architecture`): orca-worker-contract-spec.md

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: missing (first review, no `--baseline` given)
- lint: `.dev/orca-command-refactor/review/lint-1.md`; its line 1 records sha256 `d3cdbe...5200d`, which matches the candidate above. It reports `Checks: REF. Findings: 0.` so there is no lint id to confirm or dismiss.
- reviewer model: claude-haiku-5-5 (one reviewer; this report is one of the two first reviews. The coordinator applies the MERGE rule across both.)
- focus: requirements, architecture. Correctness focus is not active, so the State Variable Registry is not triggered. The Guard Condition Boundary Table and the Pipeline Dimensional Analysis were produced (see below).
- verdict basis: six blocking findings (F1-F6). Medium and minor items are under `follow-up candidates`.

Abbreviations used below: `spec:N` = line N of the candidate. `INV-A:N` = `.dev/orca-command-refactor/inventory/commands-a.md` line N. `INV-B:N` = `.dev/orca-command-refactor/inventory/commands-b.md` line N. `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md` line N. `README:N` = `.dev/orca-command-refactor/README.md` line N.

## Coverage and citation check

Read in full: `command.md` (spec-panel definition), the FIRST-REVIEW section of `~/.claude/rules/prompts/document_review_loop_prompts.md`, the candidate, the lint file, `README.md`, and the three inventories. Only files inside the workspace could be checked.

- Checked against the inventories and README (line numbers matched): `INV-A:53, 62, 66, 76-83, 90, 94-98`; `INV-B:46, 65, 91, 105, 210, 272, 285-286, 292, 301, 314`; `CAPS:44-45, 49, 52, 58-61, 64, 66-67, 72-74, 76, 79, 86, 92, 97-103, 107-113, 111, 115, 129, 130, 147-151, 161`; `README:11-17, 30, 31`. Spec citations to these lines are accurate except where noted in N1, N2 and N3.
- Not checkable here, marked UNVERIFIED: every `src/superclaude/...` citation, `CLAUDE.md`, `.dev/evals/.../EVIDENCE.md` (quoted only through `CAPS:49`), `.dev/codegraph-migration/...`, `pyproject.toml`, the `sk/` and `cmd/` files and the Orca binary.
- Not checkable by file: the session's own skill roster lists `sc:graph`, `sc:impact` and `sc:issue`, and describes `sc-issue-protocol` as creating an Orca worktree. Those skill files are outside this sandbox (UNVERIFIED), and they bear on M11 and M12.

## Verdict summary

verdict: FAIL (six blocking findings: F1, F2, F3, F4, F5, F6). The count of Medium and minor findings does not change the verdict.

---

=== REQUIREMENTS ANALYSIS ===
(Wiegers lead; Adzic and Cockburn contribute)

### F1. Phase 0 acceptance check cannot pass as written. BLOCKING. CRITICAL.
- Expert: Wiegers (lead), Adzic.
- Issue: AC-0.4 says "steps 1-3 and 5-7 pass" in P0 (`spec:194`). Step 3 passes only if the worker_done "report path is the WC-4 contract path" (`spec:182`). The WC-4 contract does not exist for these commands until P1 (`spec:159`), and `spec:194` says so itself ("the contract arrives in P1").
- Grading check: An implementer who runs AC-0.4 as written in P0 finds that step 3 cannot pass, because the WC-4 contract path is not produced until P1 (`spec:159`), and that is wrong because `spec:194` says steps 1-3 pass.
- Recommendation: In P0, make step 3 check that the worker_done report path equals the command's existing report file (for example `REPORT.md` for troubleshoot, `INV-B:242`; the existing contract for workflow, `INV-B:272`). State that step 4 is not evaluated until P1.
- Priority: High. Quality impact: P0 is the gate that tests the whole decision (`spec:158`) and cannot close as written.

### F2. Two commands needing a change are assigned to no phase, so AC-1.1 cannot pass. BLOCKING. CRITICAL.
- Expert: Wiegers (lead), Fowler (count check).
- Issue: `brainstorm` (`spec:84`) and `init-lite` (`spec:87`) are in section 3.1 and need the `## Unattended mode` section. The phase rows (`spec:159-162`) list P1 13 commands, P2 15, P3 4, P4 3, for 35 in total. The 3.1 and 3.2 rows add up to 37 (10 + 27). Neither brainstorm nor init-lite appears in any phase row. P1 says the flag is accepted "by every command in sections 3.1 and 3.2" (`spec:159`), and AC-1.1 asserts the section for every such command (`spec:195`).
- Grading check: An implementer who follows the phase table builds 35 of the 37 changes and leaves brainstorm and init-lite without `--unattended`, and that is wrong because `spec:195` requires the section for every command in 3.1-3.2.
- Recommendation: Add brainstorm and init-lite to P1. init-lite also needs the F4 fix.
- Priority: High. Quality impact: AC-1.1 fails in P1 and in every later phase; see also the Pipeline Dimensional Analysis below.

### F3. /sc:load contradicts itself on whether it names the contract. BLOCKING. MAJOR.
- Expert: Wiegers (lead), Cockburn.
- Issue: The `load` row gives "Report (WC-4): none (see note)" (`spec:112`). The Decisions table says `/sc:load` gets no report file: "a report file would be an unrequested addition" (`spec:265`). AC-1.1 requires every command in 3.1-3.2 to have a section "naming `return-contract.yaml`" (`spec:195`), and `load` is in P1 (`spec:159`).
- Grading check: An implementer who follows the load row adds no contract and fails AC-1.1; an implementer who satisfies AC-1.1 writes a report file that the Decision rejects.
- Recommendation: Choose one. Either `load` writes a contract in unattended mode and the Decision at `spec:265` changes, or AC-1.1 names `load` as an explicit exception with its reason.
- Priority: High.

### F4. The init-lite row breaks WC-6. BLOCKING. MAJOR.
- Expert: Nygard (lead), Wiegers.
- Issue: WC-6 allows exactly two behaviours: resume "when given its resume flag", or "writes each run into a fresh output directory", and a retry "must not corrupt the first attempt's output" (`spec:64`). The `init-lite` row says "Re-run overwrites its marked report" (`spec:87`; source `INV-A:55`, which says the marked report is overwritten on re-run). Overwriting is neither allowed behaviour.
- Grading check: An implementer who follows the init-lite row builds a re-run that replaces the first attempt's report, and that is wrong because WC-6 (`spec:64`) forbids corrupting the first attempt's output and allows only resume or a fresh directory.
- Recommendation: Put a per-attempt unique `--output` path in the brief template (`spec:73`). `init-lite` already takes `--output <file>` (`spec:87`), so the brief can make each run fresh without any command change. Write that rule into WC-6 so the row is not the only source.
- Priority: High.

### F5. Ready-today commands can write one file from two workers. BLOCKING. CRITICAL.
- Expert: Hohpe (lead), Nygard.
- Issue: WC-11 says "Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes" (`spec:69`). Section 2.3 sends workers to the current worktree by default (`spec:73`, citing `CAPS:115`: "workers share the current worktree by default"). `index-repo` is listed as ready today with brief flags "none" and writes a fixed `PROJECT_INDEX.md` whose location is only "implied" (`spec:86`, `INV-A:53`). It gets an output flag only in P1. `cleanup-audit` writes a fixed `.claude-audit/` path and the row relies on "one audit per worktree at a time (WC-11)" (`spec:85`). Section 2.3 does not state that serialization rule (`spec:73`). Ready waves run tasks in parallel (`CAPS:86`).
- Grading check: An implementer who dispatches two `index-repo` tasks in one ready wave (`CAPS:86`, placement `spec:73`) gets two writers to `PROJECT_INDEX.md`, and WC-11 (`spec:69`) says that must never happen.
- Recommendation: Mark `index-repo` and `cleanup-audit` as not ready until they take a per-worker output path (P1), or add the serialization rule to section 2.3 and to their verdict rows. Remove "ready today" for them in the meantime.
- Priority: High.

---

=== ARCHITECTURE ANALYSIS ===
(Fowler lead; Newman, Hohpe and Nygard contribute)

### F6. WC-3 lets a coordinator's answer become the implement Ruling. BLOCKING. CRITICAL (safety boundary).
- Expert: Fowler (lead), Nygard, Whittaker (sequence attack, see the adversarial section).
- Issue: WC-3 says that when a gate "would resolve as blocked", the session "may instead ask the coordinator once ... wait, then re-invoke or resume the command with the answer as a flag" (`spec:61`). The `implement` halt at `E-HALT-QA` or `E-NO-RULING` is a blocked gate (`spec:109`). D2 option (a) keeps the rule that the person rules, and says the worker ends `failed` (`spec:234-236`). Option (b), a relayed Ruling, is described as one that "weakens a deliberate safety rule" (`spec:235`). The rule that "another agent's message ... [is] not acceptance" is quoted at `INV-A:66`, and `INV-A:66` says an Orca coordinator is "another agent".
- Grading check: An implementer who follows WC-3 as written lets the coordinator's answer to the worker's `ask` be passed back to `/sc:implement` as its Ruling, and that is wrong because `INV-A:66` quotes the rule that another agent's message is not acceptance. WC-3 thereby adopts D2(b) before the user decides it.
- Recommendation: In WC-3 (`spec:61`) and in the implement row (`spec:109`), exclude gates that are safety rules, and in particular the implement Ruling, until D2 is answered. State that a re-invocation's answer can never serve as a Ruling.
- Priority: High.

### Medium and minor architecture points are listed under `follow-up candidates` below. The ones most likely to affect implementation are M1 (permissions), M2 (Agent-tool heartbeat) and M5 (stale contract).

---

=== ADVERSARIAL ANALYSIS ===
(Whittaker; all five attack methodologies were applied to the WC-4/WC-5 and D2 invariants)

I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (`spec:63`, "no report exists -> failed")** fails when **an earlier run's `return-contract.yaml` remains in the output directory and the current run dies before writing its own**. Concrete attack: **run 1 writes `status: succeeded` to `<output>/return-contract.yaml`; a retry (`worker-start --retry-of`, `CAPS:116`) of the same command in the same directory dies at its second step; the file still reads `succeeded`; WC-5 sends `--outcome succeeded` and the coordinator releases a worker that produced nothing.** Severity: MAJOR (ambiguous under attack). It becomes reachable only through the fixed-path commands in F4 and F5. Graded Medium (see M5).

I can break this specification by **Sequence Attack**. The invariant at **D2 (`spec:234-236`) and the implement row (`spec:109`)** fails when **a blocked gate is answered through the WC-3 `ask` path (`spec:61`)**. Concrete attack: **`/sc:implement` halts with `E-NO-RULING`; the worker asks the coordinator; the coordinator answers with words it attributes to the person; the worker re-invokes `/sc:implement` with that answer as the Ruling.** Severity: CRITICAL. This is F6.

I can break this specification by **Divergence Attack**. The invariant at **WC-5 and the Decisions row "partial maps to succeeded" (`spec:63`, `spec:263`)** fails when **a run's contract says `partial` and its deliverable is missing**. Concrete attack: **contract `status: partial`, `report_path` points to nothing; WC-5 sends `--outcome succeeded` and Orca records a success.** Severity: MINOR. The coordinator reads the report before it releases or reuses the worker (`spec:73`, `CAPS:107-113`), so the attack is largely contained.

---

=== GUARD CONDITION BOUNDARY TABLE ===
(Triggered: the spec contains outcome mapping, gate resolution, wait-size and path-uniqueness guards. Produced because the Mandatory Outputs require it. Nygard, Crispin and Whittaker participated in the table entries.)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome | `spec:63` | Zero/Empty: no report file | none | failed | `--outcome failed` | OK |
| WC-5 outcome | `spec:63`, `spec:263` | One/Minimal: `status: partial` | `partial` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome | `spec:63` | Typical: `status: succeeded` | `succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome | `spec:62`, `spec:63` | Sentinel Value Match: stale contract left by an earlier run, current run dies before writing | `succeeded` on disk | succeeded | "no report exists" branch never fires | GAP (Medium, M5) |
| WC-5 outcome | `spec:63` | Legitimate Edge: audit whose verdict is FAIL | `status: succeeded`, body verdict FAIL | succeeded | as stated (intended; the coordinator reads the body) | OK |
| WC-6 retry | `spec:64` | Zero/Empty: retry with no on-disk state | no output directory | fresh run | fresh directory | OK |
| WC-6 retry | `spec:64`, `spec:87` | Typical: retry of `init-lite` | existing report | overwrite | neither WC-6 option | GAP (F4) |
| WC-6 retry | `spec:64`, `spec:109` | Legitimate Edge: `implement` with a ledger present, no flag | ledger `progress.md` | implicit resume | not covered by WC-6's flag wording | GAP (Medium, M8) |
| WC-10 wait | `spec:68` | Maximum: one Agent-tool call lasting 6 minutes | 360 s | no heartbeat during the call | rule covers poll waits and evals only | GAP (Medium, M2) |
| WC-10 wait | `spec:68`, `spec:266` | Typical: poll wait of at most 4 minutes | at most 240 s | split | per-iteration runtime UNVERIFIED (`spec:283`) | OK, conditional on UNVERIFIED #12 |
| WC-11 path | `spec:69` | Typical: per-worker path with a slug | unique | no collision | as stated | OK |
| WC-11 path | `spec:69`, `spec:86` | One: fixed default path, two workers | `PROJECT_INDEX.md` | same file written twice | "never" | GAP (F5) |
| WC-2 gate | `spec:60`, `spec:104` | Zero/Empty: `cli-eval run` with no `--suite` | flag absent | blocked (c) | blocked | OK |
| WC-2 gate | `spec:60`, `spec:104` | Sentinel Value Match: safety flags absent | flags absent | blocked (c) | blocked | OK |
| WC-9 outward | `spec:67`, `spec:113` | Zero/Empty: `post-release` with no authorization flags | flags absent | outward steps off | as stated | OK |
| D2 Ruling | `spec:109`, `spec:234` | Legitimate Edge: coordinator relays the person's words through `ask` | relayed text | accepted via WC-3 | WC-3 permits it; D2(a) forbids it | GAP (F6) |
| Check 7.2 step 3 | `spec:182` | Zero/Empty: P0 run with no WC-4 contract | none | cannot pass | `spec:194` says steps 1-3 pass | GAP (F1) |
| Check 7.2 step 4 | `spec:183` | Typical: contract with only `status` and `command` | two keys | pass | `spec:62` requires more fields | OK, but weak (M10) |

Classes left out, with reasons: Maximum/Overflow for WC-5 (no numeric value); One/Minimal for WC-9 (boolean); Sentinel for WC-6 (no sentinel value in WC-6). Limitation: section 3.2 gate rows are covered by the WC-2 row and not expanded cell by cell. This table is therefore complete for the guards enumerated in sections 2.2 and 7 and in D2, and not for each per-command row.

---

=== PIPELINE DIMENSIONAL ANALYSIS ===
(Triggered: two multi-stage flows where counts may diverge. Fowler leads the count annotation, Whittaker the consistency check.)

Pipeline 1, command partition to phase assignment:

```text
[43 commands in cmd/ (spec:76)] --> [10 ready (spec:78) + 27 change (spec:94) + 6 coordinator (spec:127)] = 43 OK
                                              |
                                              v
                              [phase rows spec:159-162: P1 13 + P2 15 + P3 4 + P4 3 = 35 assigned]
                              [expected: 10 ready + 27 change = 37]        <-- MISMATCH: brainstorm (spec:84), init-lite (spec:87) get no phase
```

Severity: CRITICAL under FR-19, the same finding as F2.

Pipeline 2, worker reports to coordinator:

```text
[N workers in one worktree (spec:73)] --> [N contract writes (spec:62)] --> [1 file for index-repo (spec:86), cleanup-audit (spec:85)]
                                                                           <-- MISMATCH: coordinator expects N contracts
```

Severity: CRITICAL under FR-19. The same finding as F5.

Pipeline 3, worker_done to contract: N dispatches give N worker_done (`CAPS:76`, once per worker). A crash between the contract and worker_done leaves a contract with no worker_done. This is undefined; see M4.

Downstream integration wiring (`spec-panel` SP-1 to SP-4) is not triggered, because the candidate is not an input to adversarial or roadmap commands.

---

=== EXPERT FINDINGS: ARCHITECTURE, FOLLOW-UP (MEDIUM AND MINOR) ===

These do not block. They are listed for the coordinator and the session that ran the review.

- M1 (Nygard, Medium). WC-2 is titled "No person-blocking step in unattended mode" (`spec:60`), but it lists only AskUserQuestion, chat yes/no and STOP AND WAIT. Tool permission prompts for Bash, Write and Edit are not covered by any requirement, and AC step 5 checks only AskUserQuestion (`spec:184`). A worker that stops at a permission prompt is invisible (`CAPS:52`, `CAPS:129`). E2 also says a worker "has the same tools as a command a person runs" (`spec:22`), which does not account for permission mode. Whether worker sessions run with prompts is UNVERIFIED. Recommendation: add a requirement for permission mode or an allowlist, and an AC.
- M2 (Nygard, Medium). WC-10 requires a heartbeat every 5 minutes (`spec:68`). WC-7 keeps Agent-tool fan-out unchanged (`spec:65`). A single Agent-tool call blocks the top-level session until its subagents finish, so a tdd, cleanup-audit or adversarial fan-out can exceed 5 minutes with no heartbeat. WC-10 names only poll waits and evals. Whether Orca uses heartbeat age is UNVERIFIED (`CAPS:130`). Recommendation: state the rule for Agent calls.
- M3 (Fowler, Medium). WC-2(c) says the command "writes its report with status: blocked and stops" (`spec:60`). WC-3 says the session "may instead ask ... wait, then re-invoke" (`spec:61`). A command cannot pause for Orca (SA-2, `spec:147`). The only implementable sequence is: the command stops, then the session asks, then it re-invokes. The word "instead" and the word "wait" suggest otherwise. Recommendation: write the sequence out.
- M4 (Hohpe, Nygard, Medium). A worker can write a contract and then never send worker_done. The spec has no rule for "contract present, no worker_done". The check waits 900000 ms and then does not say what to do (`spec:182`). `CAPS:111` forbids release on timeout, and the Orca bound on a Dispatch is UNVERIFIED (`spec:282`). Recommendation: define the coordinator's action.
- M5 (Whittaker, Medium). The stale-contract attack in the adversarial section. Reachable only through the fixed-path commands in F5 and the re-run of F4. Fixing F4 and F5 removes most of it. Recommendation: state that a worker deletes or renames any existing contract before it starts.
- M6 (Newman, Medium). WC-4 lists required fields "at least" (`spec:62`) and has no schema version. "Commands that already write a contract keep their fields" means the shape differs per command. Check 7.2 step 4 asserts only `status` and `command` (`spec:183`). Recommendation: a single versioned schema with a required-field list.
- M7 (Fowler, Medium). SA-3 says "A standalone default run writes the same files it writes today" (`spec:148`). P1 changes the standalone adversarial contract filename and makes workflow write a contract on pre-creation STOPs (`spec:159`; `INV-B:272`, "Not written for pre-creation STOPs"). SA-4 allows the change "or correct a documented defect" (`spec:149`), which resolves it only by inference. Recommendation: state the exception in SA-3.
- M8 (Fowler, Medium). WC-6 covers resume only "when given its resume flag" (`spec:64`). `implement` resumes implicitly from a ledger (`spec:109`), `cleanup-audit` resumes from `progress.json` with no flag named (`spec:85`), and `index-repo` uses `mode=update` (`spec:86`). Recommendation: name the resume trigger for each.
- M9 (Fowler, Medium). SA-4 (`spec:149`) lists the existing-line changes that are allowed. Section 3 also requires existing-line changes not on that list: the tasklist Stage 10.5 invocation (`spec:122`), the task TFEP commit removal (`spec:121`), the cli-eval wait split (`spec:104`), the spec-panel `target_release` input (`spec:120`), and the cleanup-audit output naming (`spec:85`). AC-C5 (`spec:176`) will flag some of them. Recommendation: extend the SA-4 list or change AC-C5.
- M10 (Newman, Medium). Check 7.2 step 4 is the only contract validator (`spec:183`). See M6.
- M11 (Whittaker, Medium; UNVERIFIED). The spec says the command set is 43 (`spec:76`), using the scope lists in `INV-A:3` and `INV-B:3` (21 + 22). Neither list includes `sc:graph`, `sc:impact` or `sc:issue`, which appear in this session's skill roster. Whether they live under `src/superclaude/commands/` is UNVERIFIED here. If they do, the 10/27/6 split is incomplete.
- M12 (Whittaker, Medium; UNVERIFIED). E5 (`spec:25`) and SA-2 (`spec:147`) rest on a grep dated 2026-11-02. The session's skill roster describes `sc-issue-protocol` as creating "an Orca worktree and launches an agent in it at the --pipeline level". If that skill file is in `src/superclaude/skills/`, E5's "nothing has to be removed" is false, and AC-C1 (`spec:172`) fails on the P0 baseline. The skill file is outside this sandbox. Recommendation: re-run the E5 grep now and add `sc-issue` to the inventory before P0.
- M13 (Fowler, Medium). The tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit", citing `INV-A:14` (`spec:122`). `INV-A:14` is a general statement about nesting. `INV-B:210` says nested spawning is UNVERIFIED for tasklist, and `INV-B:314` lists it as open item 1. Recommendation: state it as UNVERIFIED.
- M14 (Wiegers, Crispin, Medium). Traceability. WC-1 (`spec:59`), WC-3 (`spec:61`), WC-6 (`spec:64`), WC-7 (`spec:65`) and WC-12 (`spec:70`) have no acceptance check. WC-10 is checked only for pr-submit (`spec:210`). Recommendation: one check per WC requirement.
- M15 (Hohpe, Minor-to-Medium). WC-1 gives its owner as "Launch setup, not commands" (`spec:59`), but no phase and no check covers launch setup. Recommendation: name the owner and a phase.
- M16 (Fowler, Medium). Commands point to `~/.claude/WORKER-CONTRACT.md` (`spec:52`). The spec does not say what happens if the file is missing (a stale install or a plugin copy). Recommendation: state the behaviour, for example stop and write `status: blocked`.
- M17 (Nygard, Medium; UNVERIFIED). AC step 2 fails on any non-null `agentWait` (`spec:181`). WC-3's ask path parks the worker for the coordinator, and whether that appears as `agentWait` is not stated; `CAPS:129` describes `agentWait` as a prompt "only a human can answer". A permitted path could fail AC-2.x. Recommendation: say whether an `ask` shows as `agentWait`.
- M18 (Wiegers, Minor). WC-4 names the output flag as `--output / --output-dir` (`spec:62`), while section 3 uses `--output` throughout (for example `spec:83`, `spec:87`). Recommendation: pick one flag name.
- N1 (Minor). WC-4 states as fact that "Orca does not check the file" (`spec:62`). The spec itself lists this as UNVERIFIED (`spec:274`; `CAPS:79`). The design opens the file in any case, so it is not load-bearing.
- N2 (Minor). E2 says the worker reached `input_accepted` "and answered" (`spec:22`). The quote at `CAPS:49` reads "returned after 34s, state: ready, stage: input_accepted" and does not mention an answer.
- N3 (Minor). `spec:114` reads the pr-submit 600 s as a cumulative budget over poll-then-sleep iterations. `INV-B:91` says "600 s per wait". The spec flags the difference as UNVERIFIED (`spec:283`), but states it as the reading in the row.
- N4 (Minor). D3 option (a) recommends "no pr-submit changes in Phase 4" (`spec:240`), but P4 lists pr-submit without that condition (`spec:162`).
- N5 (Minor). Section 4 says `load` and `recommend` are "better used on the coordinator side" (`spec:139`), yet section 3.2 gives both worker changes (`spec:112`, `spec:115`).

---

## Follow-up candidates

Medium and minor findings: M1-M18 and N1-N5. Under the review loop, the session that ran this review asks the user once whether to open an issue for them. No issue is created without that answer, and an `--unattended` run only records the list.

## Reviser brief

Blocking finding ids: F1, F2, F3, F4, F5, F6.

Restated rule (`document_review_loop_prompts` and the command's bullet 6): revise only text that a blocking finding names. Add no rule, mechanism or section that a blocking finding does not call for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, with the bytes added and deleted per finding id. Medium and minor findings are not revised, and no brief clause may make them blocking.

verdict: FAIL
