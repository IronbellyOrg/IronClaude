review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

## Header
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `284cc6b74e9164675f12bdb0a33d7d0c5edf49544b271cb956ec89ae5853237e` (288 lines)
- baseline: none given, and no `--re-review`. This is a first review of the full document, so the "baseline: missing" note does not apply.
- reviewer model actually used: `claude-sonnet-5-5`
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, resolved under the sandbox home), plus the command's Review Loop (bullets 1-7) and Mandatory Output Artifacts.
- brief clauses overridden: none. The brief neither widens scope nor regrades a minor finding.
- `--iterations`: not given; one review. No Improve step and no revised specification are written (`--re-review` not used, but the brief says "do not edit anything else").

## Citation conventions
- `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`.
- Only those four files plus the candidate exist in the sandbox. Every citation to `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/`, `orca-data.json`, Orca guides or Orca source is UNVERIFIED except where an inventory line quotes it; I cite the inventory line in that case.

## What was checked and found sound (no finding)
- Counts reconcile. Section 3.1 lists 7 commands (`spec:83-89`), section 3.2 lists 30 (`spec:96-125`, counted row by row), section 4 lists 6 (`spec:132-137`): 43. The inventories give 21 + 22 (`INV-A:3`, `INV-B:3`) and 5 + 5 ready, 13 + 14 needs-change, 3 + 3 coordinator-only (`INV-A:73`, `INV-B:278`). Moving workflow, index-repo and cleanup-audit to needs-change gives 7 / 30 / 6 (`spec:76`, `spec:271`).
- Phase lists reconcile with the section-3.2 phase column: P1 12 + P2 11 + P3 4 + P4 3 = 30, and the 4 P2 commands from section 3.1 (reflect, release-split, tdd, troubleshoot) make P2's 15 (`spec:159-162`).
- Every `INV-A:N` / `INV-B:N` evidence pointer in the section 3 and section 4 rows lands on that command's row or note (spot-checked all 43).
- Every `CAPS:N` pointer in sections 1 and 2 lands on the stated fact (R1-R5 at `CAPS:97-103,145-150`; WC-1 to WC-12 at the lines cited).
- The `gh` forms in AC-2.4 and AC-4.2 name `IronbellyOrg/IronClaude` explicitly (`spec:205`, `spec:212`).

## Panel (review sequence, `--focus requirements,architecture`)
Focus panels: requirements = Wiegers, Adzic, Cockburn; architecture = Fowler, Newman, Hohpe, Nygard. Whittaker is active in every review. Because `--focus correctness` is not active, no State Variable Registry is produced. Advisory auto-suggestion: the spec introduces 3+ mutable pieces of state (Task/Dispatch status, the per-run output directory, `return-contract.yaml` status) and numeric thresholds (confidence 0.70, 4 and 5 minute waits, 600 s), so `--focus correctness` is recommended for the next review of this spec. Advisory only.

### Grading check (FIRST-REVIEW prompt) for each blocking finding
- AUD-01: An implementer who follows the stated text as written builds a worker that, after the command writes `status: blocked` into `--output`, asks the coordinator (WC-3), then re-invokes the same command with the answer flag; the command refuses because `--output` is non-empty (`spec:73`), writes no contract, and the worker ends `failed`. That is wrong because the relay path WC-3 describes can never complete for any command without a resume flag.
- AUD-02: An implementer who follows the load row builds no `## Unattended mode` section for `/sc:load` (`spec:111`, `spec:268`), and one who follows the ready-today text builds none for brainstorm or init-lite (`spec:79`, `spec:84-85`). That is wrong because AC-1.1 requires that section for every command in sections 3.1-3.2 (`spec:195`), so the P1 gate fails.
- AUD-03: An implementer who runs AC-0.4 as written on `/sc:troubleshoot` (`spec:194`) cannot satisfy step 3's "its report path is the WC-4 contract path" (`spec:182`), because no contract exists before P1 (`spec:194`, `spec:83`, `spec:89`). That is wrong because P0 must pass before any later phase starts (`spec:154`), so the phase gate cannot open.

## === REQUIREMENTS ANALYSIS ===

**Karl Wiegers (requirements quality)**
- AUD-02 [MAJOR, blocking, priority High]. Contradiction between the "only small fixes / load usage line only" texts and AC-1.1 / AC-1.2 / the P1 scope.
  - `spec:79`: for the 7 ready commands "The only command changes are the small fixes in the last column". The last column says "None" for brainstorm (`spec:84`) and init-lite (`spec:85`).
  - `spec:76`: "Every changed command also gains the `## Unattended mode` section".
  - `spec:159`: P1 makes "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" and writes the WC-4 contract.
  - `spec:195` (AC-1.1): the test asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - `spec:111` and `spec:268`: `/sc:load` gets "none" for the report, is "not its own Task", and "Only its usage-line defect is fixed"; the Decisions row calls a report file "an unrequested addition". `spec:196` (AC-1.2) additionally runs a live worker check on "each P1 command with `--unattended --output <dir>"`, and load is a P1 command with no `--output`.
  - Concrete outcome: AC-1.1 cannot pass for load, and cannot pass for brainstorm or init-lite if their rows are followed literally. Either the Decisions row or AC-1.1/AC-1.2 must give way; the spec does not say which.
- Recommendation: state one rule. Either exclude load from AC-1.1/AC-1.2 and from the P1 `--unattended` clause, or give it the section; and change `spec:79` to say that the ready commands also gain the `## Unattended mode` section and the contract in P1.

**Gojko Adzic (specification by example, testability)**
- AUD-03 [MAJOR, blocking, priority High]. AC-0.4 (`spec:194`) says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file". Step 3 (`spec:182`) requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
  - Before P1 there is no WC-4 contract for troubleshoot (report today is `REPORT.md`, `spec:89`; `return-contract.yaml` only with `--caller task-unified`, `INV-B:242`) and the adversarial contract path is "not fixed" (`spec:83`, `INV-A:35`). Only brainstorm writes a named contract (`spec:84`, `INV-A:97`).
  - Concrete scenario: P0 run on `/sc:troubleshoot`, worker sends `worker_done --outcome succeeded --report-path .../REPORT.md`. Step 3's second and third conditions are both false by construction. The P0 verdict is a fail, and `spec:194` says a failure here "reopens section 1" (the core decision) although nothing is wrong with the decision.
- Recommendation: restate AC-0.4 so step 3 reads "its `--report-path` is the command's existing report file" for P0 and the contract wording applies from P1.

**Alistair Cockburn (use cases, stakeholders)**
- No blocking finding. The primary actor (the coordinator) and its obligations are clear (`spec:73`, `spec:230-256`). Gap noted as follow-up M-08: nothing says how a worker session invokes the `/sc:` command (the worker prompt starts with an Orca preamble, not `/sc:...`; `CAPS:47` shows the task is passed as argv).

## === ARCHITECTURE ANALYSIS ===

**Martin Fowler (architecture and interface design)**
- The decision (Orca on top, commands as units of work, no Orca calls in commands) is consistent with its evidence: `spec:21-26`, rejection reasons `spec:31-37`, depth 1 at `CAPS:97-101`. No finding against the decision itself.
- Interface gap, follow-up M-02: the contract location `<output-dir>/return-contract.yaml` (`spec:62`) presumes an output-directory flag; many rows have none or a file-valued one (see M-02).
- Quantity annotation is in the Pipeline Dimensional Analysis below.

**Michael Nygard (reliability, failure modes)**
- AUD-01 [CRITICAL for this pipeline stage under FR-19, blocking, priority High]. The answer-relay path contradicts the safe-re-run rule.
  - `spec:61` (WC-3): when a gate would resolve as blocked, the worker session "may instead ask the coordinator once ... wait, then re-invoke or resume the command with the answer as a flag."
  - `spec:62` (WC-4): the contract is written "on success, failure, blocked and partial outcomes", into `<output-dir>`.
  - `spec:73` (section 2.3): "a command with no resume flag refuses a non-empty `--output` directory: it stops before writing into it, writes no contract there".
  - `spec:64` (WC-6) and the section 3.2 resume column: most commands in the table have "fresh dir" and no resume flag (for example analyze, spec-panel, task, recommend, review-translation, cli-eval: `spec:96,119,120,114,116,101`).
  - Concrete attack/trace: (1) worker runs `/sc:spec-panel <tdd> --unattended --output O/`; (2) the target_release gate resolves blocked (`spec:119`), O/ now holds `return-contract.yaml (status: blocked)`; (3) worker `ask`s, receives the release name; (4) worker re-invokes `/sc:spec-panel <tdd> --unattended --output O/ --target-release R`; (5) O/ is non-empty and the command has no resume flag, so it refuses, writes no contract, and the worker reports `failed`. The relay in WC-3 therefore only works for commands that have a resume flag, or if the worker invents a fresh directory, which breaks the "report path known before dispatch" promise (`spec:62`, `spec:73`) and the AC-1.5 check (`spec:199`).
  - The spec states neither exception nor a fresh-directory rule for the WC-3 re-invocation.
- Recommendation: narrow WC-3 so that the re-invocation of a command with no resume flag uses a new `--output` named by the worker and reports it as the `worker_done --report-path`; or delete the "re-invoke" option and leave only "resume". Preferring deletion: keep only the resume branch, and say that a no-resume command's blocked outcome ends the Task for the coordinator to re-brief via `--retry-of` (`spec:73`).

**Sam Newman (service boundaries, API evolution)**
- The new flag surface (`--unattended`, `--output`, `--slug`) is added per command with SA-4 as the backward-compatibility rule (`spec:149`). Follow-up M-05 covers the check that is meant to prove additivity (AC-C5) and does not.
- Follow-up M-04: existing contracts keep their own fields (`spec:62`), yet the `status` value set is fixed by the spec (`spec:62`, `spec:265`) and asserted in `spec:183`; the existing contracts' value sets are not recorded in the inventories (`INV-B:272` gives only the workflow field names).

**Gregor Hohpe (integration patterns, data flow)**
- Message flow matches Orca's documented contract (`worker_done` once from the dispatched pane, outcome flag, `--report-path` as metadata only: `CAPS:72-79`). WC-5 is a clean mapping (`spec:63`).
- Follow-up M-06 (wait splitting) and M-10 (SA-3 vs WC-4) concern the exchange pattern.

**James Whittaker (adversarial attacks)** (template: "I can break this specification by **[attack]**. The invariant at **[location]** fails when **[condition]**. Concrete attack: **[trace]**.")
- Sequence Attack: see AUD-01 (WC-3 relay after a blocked run, then re-invoke). Blocking.
- Zero/Empty Attack: I can break this specification by **passing an `--output` directory that does not exist**. The invariant at **`spec:62` ("written on every outcome") and `spec:73` (refusal on a non-empty directory)** fails when **the directory is missing or unwritable**. Concrete attack: `--output /nonexistent/x/`; the spec defines neither creation nor refusal; WC-5 then maps "no report exists" to `failed` (`spec:63`), so the outcome is acceptable but the cause is invisible. MINOR, listed under follow-up (see Guard table rows G1.1, G1.4).
- Sentinel Collision Attack: I can break this specification by **putting the literal `--unattended` in free text**. The invariant at **D1(a), `spec:231` ("cannot misfire on a person")** fails when **a command that takes a free-text prompt (tdd, troubleshoot, research, brainstorm: `spec:88-89,115,84`) receives a symptom or topic that contains the string**. Concrete attack: `/sc:troubleshoot "docs say pass --unattended to run" ` in a person's own session; the spec gives no rule that the switch applies only as a standalone argument token. Follow-up M-03.
- Divergence Attack: I can break this specification by **choosing a wait between 240 s and 300 s**. The invariant at **WC-10 `spec:68` vs AC-4.3 `spec:213`** fails when **a single tool call blocks 270 s**: WC-10 requires splitting only for waits "longer than 5 minutes" and splits into "at most 4 minutes", while AC-4.3 fails any call over 240 s. Follow-up M-06.
- Accumulation Attack: I can break this specification by **retrying blocked workers without bound**. The invariant at **`spec:63` and `CAPS:80`** fails when **each blocked outcome is reported `failed` (a worker's own `failed` report does not count toward Orca's three-failure circuit breaker)**. Concrete attack: coordinator re-briefs the same blocked Task with `attempt-2/`, `attempt-3/`, ... each ends `blocked`; no limit stops it and each attempt leaves a new directory (`spec:73`). MINOR; the spec leaves the retry cap to the coordinator.

**Lisa Crispin and Janet Gregory (testing, acceptance)**
- AUD-03 and the AC-1.1 part of AUD-02 above are the blocking testability defects.
- Follow-up M-05 (AC-C5 oracle) and M-11 (step 2 can pass vacuously) are test-oracle weaknesses. M-12 (AC-C3 scope).

**Kelsey Hightower (cloud-native, operations)**
- Operational concerns are covered by WC-1, WC-10, WC-12 and `spec:167-186`. See M-06 for the missing mechanism for Monitor-based waits.

## Pipeline Dimensional Analysis (FR-17 to FR-21)
Trigger: the spec describes a multi-stage flow (Task, worker, command run, contract file, `worker_done`) where counts may diverge (a blocked run followed by a re-invocation; a refusal that writes no contract; a worker that never sends `worker_done`).

Quantity Flow Diagram:

```text
[Task: 1] --> [worker-start: 1 worker, 1 Dispatch] --> [command run: 1 (WC-12: 0 if fenced)]
                                                          |
                                                          v
                                  [contract file per --output dir: 1, or 0 on F-05 refusal (spec:73)]
                                                          |
                                                          v
                                  [worker_done: exactly 1 (spec:63)]  <-- 0 on silent stall / crash
   WC-3 relay: [command run #2 in same --output dir] --> [contract: 0 (refused, spec:73)]   <-- MISMATCH (AUD-01)
   Consumer: coordinator step 4 `test -s <contract>` (spec:183) expects 1 contract per worker_done
```

Divergence points: (1) 1 worker, 2 runs (WC-3) against 1 allowed run per no-resume directory: AUD-01. (2) F-05 refusal yields 0 contracts against "written on every outcome": explicitly excepted at `spec:62` and `spec:73`, so handled. (3) 0 `worker_done` on a crash: the spec has no requirement beyond the liveness checks at `spec:181`; M-11 covers weakness of that check. The count of commands 43 = 7 + 30 + 6 is conserved (verified above).

## Guard Condition Boundary Table (hard gate; completed before synthesis)
Guards identified: G1 non-empty `--output` refusal (`spec:73`); G2 outcome mapping on contract `status` (`spec:63`); G3 wait threshold (`spec:68`, `spec:213`); G4 confidence below 0.70 (`spec:120`); G5 `--unattended` switch detection (`spec:51`, `spec:231`); G6 contract-write condition (`spec:62` vs `spec:148`). Classes left out: Maximum/Overflow for G1, G2, G4, G5, G6 (no capacity bound is stated; Orca's own limit on directory contents is not part of this spec); Sentinel for G3 and G4 (no sentinel value exists for a duration or a confidence score in the spec).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 non-empty output dir refusal | `spec:73` | Zero/Empty | empty existing dir | false (no refusal) | command runs and writes into it | OK |
| G1 | `spec:73` | Zero/Empty | `--output` path does not exist | unspecified | not stated whether it is created or refused (follow-up M-02) | GAP |
| G1 | `spec:73` | One/Minimal | dir holding only the contract of a blocked run | true | refuse, no contract, failure stated in body; WC-3 re-invocation hits this (AUD-01) | GAP |
| G1 | `spec:73` | Typical | dir with a finished earlier run, no resume flag | true | refuse | OK |
| G1 | `spec:73`, `spec:62` | Sentinel Value Match | `--output` is a file path (tdd, init-lite today take a file: `spec:85,88`) | unspecified | "directory" is the only form stated; behavior for a file-valued flag not stated (M-02) | GAP |
| G1 | `spec:73` | Legitimate Edge Case | non-empty dir plus the command's resume flag | false | command resumes (WC-6) | OK |
| G2 outcome mapping | `spec:63` | Zero/Empty | no report file | n/a | `--outcome failed` | OK |
| G2 | `spec:63`, `spec:183` | One/Minimal | report exists but `status` key missing or outside the four values | unspecified | WC-5 silent; only the live check asserts the set (`spec:183`) | GAP |
| G2 | `spec:63` | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G2 | `spec:62`, `spec:63` | Sentinel Value Match | existing contract whose own `status` word differs (brainstorm, reflect, adversarial; values not recorded) | unspecified | "keep their fields" vs fixed vocabulary (M-04) | GAP |
| G2 | `spec:63` | Legitimate Edge Case | `partial`, or audit verdict FAIL | true | `--outcome succeeded`, body states status and verdict | OK |
| G3 wait split (WC-10) | `spec:68`, `spec:213` | One/Minimal | single wait of 270 s | WC-10 false, AC-4.3 true | WC-10 allows it, AC-4.3 fails it (M-06) | GAP |
| G3 | `spec:68` | Typical | poll plus sleep iterations under 240 s | false | no split needed | OK |
| G3 | `spec:68` | Legitimate Edge Case | Monitor-based wait on a background job (cli-eval, up to 3600 s per eval: `INV-A:65`) | unspecified | "split the eval wait" (`spec:101`) without a mechanism for an event-driven wait | GAP |
| G4 confidence below 0.70 (task) | `spec:120` | Zero/Empty | confidence 0 | true | blocked | OK |
| G4 | `spec:120` | Typical | 0.85 | false | proceeds (spec silent on the 0.70-0.89 band; `INV-B:199` gives only the below-0.70 prompt) | OK |
| G4 | `spec:120` | Legitimate Edge Case | exactly 0.70 | false | "below 0.70" means not blocked | OK |
| G5 `--unattended` detection | `spec:51`, `spec:231` | Zero/Empty | flag absent | false | standalone behavior (SA-1) | OK |
| G5 | `spec:231` | Sentinel Value Match | the string `--unattended` inside quoted or free-text prompt content | unspecified | no standalone-token rule stated (M-03) | GAP |
| G5 | `spec:51` | Legitimate Edge Case | flag present on a command in section 4 | unspecified | section 4 says "get no `--unattended` mode" (`spec:128`) but not what they do with the flag | GAP |
| G6 contract-write condition | `spec:62`, `spec:148`, `spec:197` | Zero/Empty | `--unattended` without any output flag | unspecified | WC-4 needs `<output-dir>`; no default stated (M-02) | GAP |
| G6 | `spec:148` | Legitimate Edge Case | new output flag without `--unattended` | unspecified | SA-3 allows the contract; WC-4 says only in unattended mode (M-10) | GAP |

Grading of the GAP rows (FR-8/FR-9): the row for G1 One/Minimal is the blocking AUD-01 (names a concrete wrong outcome). Every other GAP row is Medium: each names a missing restriction or unspecified edge, not a stated text that does harm, and is listed under follow-up candidates.

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

Medium (warnings):
- M-01. `spec:44` states that a command's own question "comes after readiness, so it does not fail `worker-start`". The capabilities inventory records that for Claude the task is passed on the command line (`CAPS:47`) and that readiness waits for a fresh input box (`CAPS:47`, `CAPS:52`). If the slash command runs from argv, a first-turn question could precede readiness. Whether it does is not shown (UNVERIFIED). WC-2 still forbids the prompt, so no wrong text results; the "silent stall" description in section 1.4 (2) may be wrong in one case.
- M-02. `<output-dir>` is undefined where there is no directory flag: file-valued `--output` for tdd and init-lite (`spec:85,88`; section 3.1), `--output` to be added for research, spec-panel and analyze but not for implement ("beside the ledger", `spec:106`), cli-portify ("file location unnamed", `spec:102`), cli-eval (`spec:101`), cleanup-audit (`spec:107`, only `--slug`), index-repo (`spec:110`), cleanup, improve, test, tasklist (`TASKLIST_ROOT`: `INV-B:212`). The principle that the path be known before dispatch (`spec:62`, F-04 at `spec:83,115,125`) is therefore only stated for some rows. Also SA-1 forbids changing today's file-valued `--output`. State the directory flag per row.
- M-03. No rule that `--unattended` counts only as a standalone argument token (Sentinel Collision above; `spec:51`, `spec:231`).
- M-04. `status` vocabularies of the contracts that already exist (brainstorm `INV-A:39`, reflect `INV-B:36`, adversarial `INV-A:35`, workflow `INV-B:272`) are not recorded; `spec:62` says to keep their fields, `spec:183` asserts a fixed set. Verify or map each (UNVERIFIED: the skills are outside the sandbox).
- M-05. AC-C5 (`spec:176`) does not prove additivity. Verified in the sandbox with `diff -U0 | grep -E '^-[^-]'`: a deleted list item such as `- Will Not: push` appears as `-- Will Not: push` and a deleted YAML fence as `----`; neither matches `^-[^-]`, so the check prints nothing. In the other direction, adding a new flag to a one-line Usage line changes an existing line and prints a `-` line, so AC-C5 fails for the very additions SA-4 permits (`spec:149`). Use `grep -E '^-' | grep -vE '^---'` on the diff body, and say where a new flag is documented.
- M-06. WC-10 triggers at "longer than 5 minutes" but splits to "at most 4 minutes" (`spec:68`), AC-4.3 fails any call over 240 s (`spec:213`): the 240-300 s band is permitted by one and failed by the other. No mechanism is given for an event-driven wait such as cli-eval's background job plus Monitor (`spec:101`, `INV-A:65`); an idle session cannot send a heartbeat between events.
- M-07. WC-9 (`spec:67`) turns off "a paid external run" and lists installs, pushes, PRs, posts. Web search through Tavily (research `INV-B:134`, review-translation `INV-B:144`, recommend `INV-B:104`) is not classified; the rows for these commands leave it on. Say whether network search counts.
- M-08. The spec never says how a worker session runs a `/sc:` command (Skill tool versus typed slash command). The prompt arrives as an Orca preamble (`CAPS:47`, `CAPS:148`), not a message starting with `/sc:`; WC-7 only says "directly" (`spec:65`) and AC-0.4 checks "no Agent-tool wrapper" in the transcript (`spec:194`). State the invocation method in the brief template.
- M-09. Tasklist row (`spec:121`) passes `--unattended` to each nested reflect, but a reflect `needs_human_decision` item still HALTs (`INV-B:209`); the row does not say how that HALT resolves (WC-2 requires one of three resolutions). Also reflect's `--remediate` is resolved by auto-accept (`spec:86`) while the same offer in troubleshoot resolves as blocked (`spec:89`); P2's statement that these changes "add no outward capability" (`spec:160`) is true only if the auto-accepted handoff (sc:workflow, task-builder) writes inside the output directory, which the spec does not check.
- M-10. SA-3 (`spec:148`) lets "the new output flag" alone cause a contract file; WC-4 (`spec:62`) ties it to unattended mode; AC-1.3 (`spec:197`) tests only the case with neither. State one rule.
- M-11. Live check step 2 (`spec:181`): "`observation.agentWait` is never non-null" also passes when the field is absent (`CAPS:129`: "An absent field means it never looked"; `CAPS:125`: a null `agentWait` is "that same absence"). Require the field present and null at each poll, and treat the transcript search in step 5 as the real proof.
- M-12. AC-C3 (`spec:174`) baselines only `tests/skills/`, while P0 edits `src/superclaude/cli/install_core.py` and the core CLAUDE.md level table (`spec:158`, `spec:192`), whose tests may live elsewhere (UNVERIFIED).

Minor (notes):
- n1. E3 (`spec:23`) cites `invocation_method: "skill-direct"` as support, while section 1.4 (1) (`spec:43`) says the PR #329 run proved only the nested route. Rephrase E3.
- n2. E2 (`spec:22`) says the worker "answered"; the inventory quote (`CAPS:49`) shows `state: ready, stage: input_accepted` only.
- n3. tdd row (`spec:88`): "a precise component prompt ... that names one task file" is unclear for a first run, which creates the task file (`INV-B:221-222`).
- n4. Under D3(a) (`spec:243`) pr-submit stays in section 3.2 and in the "30 needing change" and in AC-1.1, although "no pr-submit changes in Phase 4"; the count and test should say it is deferred.
- n5. AC-3.1 (`spec:207`) phrases one assertion as a disjunction ("or the command stops listing it") that a test cannot encode.
- n6. `/sc:save --unattended` writes only per-session keys (`spec:118`); nothing says that `/sc:load` reads them (`INV-B:63` names `<key>.md`), so saved state may not be resumed by load. AC-3.4 (`spec:210`) tests only that files exist.
- n7. The pr-submit top-level rule is cited at `sk/sc-pr-submit-protocol/SKILL.md:37-39` (`spec:65`, `INV-B:90`) and at `:47-49` (`CAPS:40`, `CAPS:161`, which cites the installed copy under `~/.claude`). Different copies or a drifted line; both UNVERIFIED here.
- n8. Section 1.1 says command changes are "limited to" the section-2 contract (`spec:16`), while section 3 and P3 also fix interface drift (`spec:117,123,124`, `spec:161`); the later text states why. Harmonize the sentence.
- n9. Retry of blocked workers has no cap (Accumulation Attack above).

The session that ran this review would ask the user once whether to open an issue for these follow-up candidates. This was an unattended-style delegated run with a fixed final reply, so the question was not asked and no issue was created.

## Coverage
Whole document, first review (`review: 1 of 3`): lines 1-288 read in full. Cross-checked against the three inventories in full; all other cited sources are UNVERIFIED in this sandbox. Not covered: the correctness of the cited source lines in `src/`, `CLAUDE.md`, `EVIDENCE.md` and the Orca installation, and the 340-citation validator claim at `spec:288`. No edit was made to the candidate. No fourth review is started.

## Reviser brief
Blocking finding ids: AUD-01, AUD-02, AUD-03. Rules for the reviser (restated from the command, since the reviser reads this report and not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave minor and Medium findings (M-01 to M-12, n1 to n9) alone.
- Return the candidate once and do not award yourself a PASS.

Pointers (text each finding names): AUD-01 = `spec:61` (WC-3 "re-invoke or resume") against `spec:73`; AUD-02 = `spec:79`, `spec:111`, `spec:159`, `spec:195-196`, `spec:268`; AUD-03 = `spec:182` and `spec:194`.

verdict: FAIL
