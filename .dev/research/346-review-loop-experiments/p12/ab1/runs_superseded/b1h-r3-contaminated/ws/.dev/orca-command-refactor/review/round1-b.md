review: 1 of 3

# /sc:spec-panel critique: orca-worker-contract-spec.md

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review; no `--re-review` or `--baseline`). Prior report: none.
- Reviewer model: claude-haiku-5-5
- Focus: requirements, architecture. Panel: Wiegers (lead), Adzic, Cockburn; Fowler (lead), Newman, Hohpe, Nygard; Whittaker (active in every panel review).
- Process: FIRST-REVIEW prompt, run by one reviewer in one worker. The three-reviewer MERGE and the fresh-context VERIFY pass were not run (no second reviewer or verifier was available here). Every blocking finding below is therefore unconfirmed by a second reader; the verdict is this reviewer's only.

Citation keys (all files read in full): `SPEC:n` = the candidate, line n. `README:n` = `.dev/orca-command-refactor/README.md`. `INV-A:n` = `inventory/commands-a.md`. `INV-B:n` = `inventory/commands-b.md`. `CAPS:n` = `inventory/orca-capabilities.md`. Any citation to `src/`, `tests/`, `.dev/evals/`, `.dev/codegraph-migration/`, `/opt/Orca` or `~/.claude` is UNVERIFIED: those files are outside the sandbox and were not read.

## Checks run

- The grep in `SPEC:172` was run with `grep -nE` on sample lines (`orca-ide orchestration ask`, `orca orchestration worker-start`, `orca-ide status --json`). As written (`\|` inside the pattern) it matched none of them. With a plain `|` in place of `\|` it matched the first two. In `grep -E`, `\|` is a literal pipe. A temporary probe file was written under the sandbox run directory and then removed.
- Pipeline Dimensional Analysis: not triggered. The spec has no multi-stage data flow whose counts change.
- State Variable Registry: not triggered. The focus is requirements and architecture, not correctness.

## Mandatory output: Guard Condition Boundary Table

The spec contains guard conditions (`SPEC:60`, `SPEC:63`, `SPEC:64`, `SPEC:68`, `SPEC:70`, `SPEC:181`), so the table is produced. Classes left out, with reasons: "Maximum/Overflow" for the outcome guard (the status set is finite, no numeric threshold); "Maximum" for gate booleans (no numeric input); "Sentinel" for WC-12 (no sentinel value).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome | `SPEC:63` | Zero/Empty: no contract file | none | failed | "or no report exists" | OK |
| WC-5 outcome | `SPEC:63` | Zero/Empty: stale contract left by an earlier attempt in a reused directory | old file present | depends on old file | not addressed; WC-6 only covers fresh directories | GAP (F10) |
| WC-5 outcome | `SPEC:63` | One/Minimal: `status: partial` | `partial` | succeeded | `SPEC:63`, `SPEC:263` | OK |
| WC-5 outcome | `SPEC:63` | Typical: `status: succeeded` | `succeeded` | succeeded | `SPEC:63` | OK |
| WC-5 outcome | `SPEC:63` | Invalid status outside the four values in `SPEC:62` | `done`, empty | succeeded ("otherwise") | literal catch-all | GAP (F3) |
| WC-5 outcome | `SPEC:63` | Conflicting: `status: succeeded` with non-empty `blocked_question` | both set | succeeded | precedence not stated | GAP (F15) |
| WC-5 outcome | `SPEC:63` | Legitimate edge: audit verdict FAIL with `status: succeeded` | `succeeded` | succeeded | `SPEC:63` | OK |
| WC-2 gate | `SPEC:60` | Zero/Empty: gate with no flag and no documented default | unset | blocked | `SPEC:60` (c) | OK |
| WC-2 gate | `SPEC:60` | Typical: caller supplies the flag in the brief | set | proceeds | `SPEC:60` (b) | OK |
| WC-3 gate hit | `SPEC:61` | Gate reached with a preamble present | blocked or ask | either ("may") | trigger and answer-flag undefined | GAP (F4) |
| WC-6 retry | `SPEC:64` | Zero/Empty: retry with no on-disk state | none | fresh run | who creates the fresh directory is not stated | GAP (F6) |
| WC-6 retry | `SPEC:64` | One: resume flag with state present | state | resumes | per-row resume column | OK |
| WC-10 wait | `SPEC:68` | Boundary: one tool call of 4 to 5 minutes | 240-300 s | no split required, no target | 4-minute target and 5-minute trigger leave this band open | GAP (F7) |
| WC-10 wait | `SPEC:68`, `SPEC:114` | Maximum: pr-submit poll-plus-sleep iteration | runtime UNVERIFIED (`SPEC:284` item 12) | unknown | deferred to confirmation | GAP (F7) |
| WC-12 check | `SPEC:70` | `check` returns `consumer_fenced` | returned | stop, no `worker_done` | `CAPS:49-52` | OK |
| §7.2 step 2 | `SPEC:181` | Worker correctly asks (WC-3) while `agentWait` is non-null | non-null | check fails | pass condition is "never non-null" | GAP (F8) |
| Decision D2 | `SPEC:232-236` | Coordinator reply quotes the user's words | relayed | rejected under option (a) | D2 pending | OK under (a); pending |

## Findings

Severity follows the grading rule in the review loop. Blocking findings: F1, F2, F3. Medium and minor findings are listed under follow-up candidates and do not trigger revision.

### REQUIREMENTS ANALYSIS

**F1. MAJOR, blocking. Acceptance check AC-C1 cannot fail.** Expert: Wiegers (testability), Whittaker (FR-2.3 sentinel). `SPEC:172` is the only mechanical gate for SA-2 and WC-8: "prints nothing (SA-2, WC-8)". The check cannot fail, for two reasons. (a) The `\|` alternation is a literal pipe in `grep -E` (checked above), so the pattern matches only the literal text `orchestration|worktree|terminal|agent`. (b) Even with `|`, the pattern covers only four subcommands, is case-sensitive, and does not match `orca-ide status`, which the capabilities inventory uses (`CAPS:146`), or `orca-cli`. SA-2 forbids any `orca`/`orca-ide` command (`SPEC:147`).
Grading sentence: "An implementer who runs AC-C1 exactly as written sees empty output on every tree, records pass, and a command that runs `orca-ide orchestration worker-start` also passes, which is wrong because SA-2 and WC-8 forbid it."
Recommendation: match `\borca(-ide|-cli)?\b` case-insensitively, with an explicit allowlist for `ccsession-tag`, and add a self-test that the grep matches a planted sample line.
Priority: High.

**F2. MAJOR, blocking. The load row contradicts WC-4 and AC-1.1.** Expert: Wiegers (traceability). `SPEC:112` gives `/sc:load` report "none", and its phase as "P1 (usage line only)". `SPEC:76` says every changed command gains a `## Unattended mode` section that names its report file. `SPEC:159` requires P1 to accept `--unattended` for every command in 3.1 and 3.2, load included. `SPEC:62` (WC-4) requires the contract on every outcome. `SPEC:265` says a load report file would be "unrequested". `SPEC:195` (AC-1.1) requires every command in 3.1 and 3.2 to have a section "naming `return-contract.yaml`".
Grading sentence: "An implementer who follows the load row writes no `return-contract.yaml` and no Unattended mode section for `/sc:load`, so AC-1.1 fails for load and P1 cannot pass; an implementer who follows AC-1.1 or WC-4 must add a contract the load row and `SPEC:265` say not to add."
Recommendation: choose one. Either give load a minimal contract with `status` and no `report_path` (WC-4 already allows "if any"), or name load as an exception in WC-4 and AC-1.1 with the reason. Priority: High.

**F3. MAJOR, FR-8 GAP, blocking. The outcome rule turns invalid status into success.** Expert: Nygard (guard boundaries), Whittaker (FR-2.1 zero/invalid input). `SPEC:63` maps to `--outcome succeeded` "otherwise", after `failed` and `blocked`. `SPEC:62` allows exactly four status values. `CAPS:73` says "Never encode failure only in prose".
Grading sentence: "An implementer who follows WC-5 as written sends `--outcome succeeded` for a contract whose status is `done` or empty, and that is wrong because the contract does not state success."
Recommendation: map only `succeeded` and `partial` to succeeded; map every other value, including unparseable or missing status, to failed. Add a planted-invalid-status case to P0 or P1 checks. Priority: High.

**F4. Medium. The WC-3 ask path is undefined.** Expert: Cockburn (actor and gate), Fowler (interface). `SPEC:61` says the worker "may instead ask" the coordinator and then "re-invoke or resume the command with the answer as a flag". But `SPEC:60`(c) makes the command stop with a blocked report, and `SPEC:66` (WC-8) forbids the command from calling Orca. No section-3 row defines an answer flag; gates take values supplied in the brief (`SPEC:60` (b)). Nothing says what triggers the ask, who reads `blocked_question`, or whether ask or blocked is used. An implementer must guess, so this is Medium under the grading rule. Recommendation: pick one path (blocked, then the coordinator re-dispatches with a flag, per `SPEC:73`) or define the trigger and the answer flag.

**F5. Medium. Phase 0 contradicts itself on `--unattended`.** Expert: Adzic (examples), Wiegers. `SPEC:73` (§2.3) requires each brief to carry "the exact command line including `--unattended`". `SPEC:158` (P0) makes "no command edits". `SPEC:180` (step 1) says the brief follows §2.3, but `SPEC:194` (AC-0.4) lists the three smoke commands without the flag. An unedited command's handling of an unknown flag is not stated, so the P0 result depends on a guess. Recommendation: state that P0 briefs omit `--unattended`, or list it as a P0 pre-step.

**F6. Medium. Who makes the output directory fresh?** Expert: Fowler (state), Nygard. `SPEC:62` (WC-4) says the coordinator passes `<output-dir>` and the path is known before dispatch. `SPEC:64` (WC-6) says a command "writes each run into a fresh output directory". If the command creates the fresh directory, WC-4 cannot hold. If the coordinator does, `SPEC:73` does not say so for retries. Recommendation: state that the coordinator passes a new `--output` on each retry.

**F7. Medium. The WC-10 wait band is open.** Expert: Nygard (liveness). `SPEC:68` requires a split for a call "longer than 5 minutes" and a target of at most 4 minutes. A call of 4 to 5 minutes is not covered. The heartbeat cadence comes from the preamble, not a guide (`CAPS:130`), and whether Orca uses heartbeat age is UNVERIFIED (`CAPS:130`). The pr-submit iteration runtime is UNVERIFIED (`SPEC:284` item 12). Recommendation: change the trigger to "4 minutes or longer" and state the same bound for pr-submit iterations.

**F8. Medium. The §7.2 pass condition excludes the WC-3 ask path.** Expert: Adzic (given/when/then). `SPEC:181` passes only when `agentWait` is never non-null. `SPEC:61` and `CAPS:52`/`CAPS:129` say a worker parked on its own ask is healthy, and that a non-null `agentWait` means a prompt only a human can answer. A correct worker on the ask path can fail this check, and no AC exercises the ask path, so the defect would surface only later. Recommendation: pass when `agentWait` is null or matches a recorded ask.

**F9. Medium. Unattended mode does not propagate into nested skills.** Expert: Fowler (boundaries), Hohpe (message flow). `SPEC:60` binds WC-2 to "the command". Section 3 handles some nested gates (`SPEC:90` tdd to /task; `SPEC:122` tasklist to reflect), but no rule says `--unattended` flows down. pr-submit dispatches `/sc:troubleshoot` per verified finding (`INV-B:91`), and the pr-submit row (`SPEC:114`) does not address troubleshoot's `--fix` offer. Recommendation: add one propagation rule and list each nested gate it reaches.

**F12. Medium. The §3.1 heading contradicts its own table.** Expert: Wiegers (consistency). `SPEC:79` says the ready-today commands "run as workers now". The same commands need P1/P2 changes in the last column (`SPEC:88` reflect P2, `SPEC:89` release-split P2, `SPEC:90` tdd P2, `SPEC:91` troubleshoot P2), and the contract only appears in P1 (`SPEC:79`). Recommendation: retitle 3.1 "ready for attended smoke runs; contract and gates land in P1-P2".

**F15. Medium. Sentinel collision between status and blocked_question (Whittaker FR-2.3).** `SPEC:63` maps the outcome on status alone, while `SPEC:60` and `SPEC:62` use `blocked_question` as the blocked signal. A contract with `status: succeeded` and a non-empty `blocked_question` is not addressed. Recommendation: define the precedence, and make presence of `blocked_question` force blocked.

### ARCHITECTURE ANALYSIS

**F10. Medium. Stale contracts and no version field.** Expert: Nygard (failure modes), Newman (evolution). `SPEC:63` treats "no report exists" as failed, but a contract left by an earlier attempt in the same directory counts as a report. `SPEC:62` has no staleness rule. The contract also has no version field, so older and newer WORKER-CONTRACT installs cannot be told apart. Recommendation: have the worker delete or rename any existing contract before dispatch, and add `contract_version`.

**F11. Medium. A blocked Task has no defined recovery path.** Expert: Hohpe (message exchange), Nygard. `SPEC:63` maps blocked to failed. `CAPS:142-144` says a failed Task keeps dependents blocked until a `--retry-of` replacement completes it. §2.3 (`SPEC:73`) has no obligation for the coordinator to read `blocked_question`, get an answer and re-dispatch. Recommendation: add the coordinator obligation, or name the human path (D2 option (a)) as the only path.

**F13. Low. Summary overstates scope.** `SPEC:16` says command changes are "limited to" three categories. Section 3 and SA-4 (`SPEC:149`) add defect fixes outside them (roadmap flags, validate-tests default, business-panel frontmatter, explain tools). Recommendation: say "plus named defect fixes (`SPEC:149`)".

**F14. Low. Evidence overreach.** `SPEC:22` says the EVIDENCE.md:45 worker "answered". `CAPS:49` quotes only the readiness result. The EVIDENCE file is outside the sandbox (UNVERIFIED). Recommendation: drop "and answered" unless the evidence file is checked.

## Expert consensus and disagreements

- Consensus: the contract model (Orca on top, commands as workers, WC-2 to WC-12) is coherent, and SA-1 keeps standalone behavior intact. The problems are in the mechanical checks and in gate and outcome edges.
- Disagreement, not resolved here: none between experts. Whittaker's attacks feed F3 and F15.

## Quality metrics (0-10)

- Clarity: 6. The contract is readable, but ask/blocked (F4), the wait band (F7) and the outcome rule (F3) are not precise.
- Completeness: 6. Load and nested propagation (F2, F9) and the stale-contract case (F10) are missing.
- Testability: 4. AC-C1 cannot fail (F1), AC-1.1 cannot pass for load (F2), AC-0.4 and 7.2 disagree (F5).
- Consistency: 5. Section 3.1 framing (F12), the summary (F13) and the P0 brief (F5) disagree with other sections.

## Reviser brief

Blocking finding ids: F1, F2, F3.

Restated rule (review loop step 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id.

Text named by each blocking finding: F1 names `SPEC:172` and the `SA-2`/`WC-8` reference at `SPEC:147` and `SPEC:66`. F2 names `SPEC:112`, `SPEC:195` and `SPEC:265`, and `SPEC:62` for WC-4. F3 names `SPEC:63`.

Clauses overridden by the brief: none (no brief was supplied).

## Follow-up candidates (Medium and minor; not part of the verdict)

The session that ran this review asks the user once whether to open an issue for these. This worker does not ask and creates none.

- F4 ask/blocked path (Medium)
- F5 P0 `--unattended` contradiction (Medium)
- F6 fresh-directory ownership (Medium)
- F7 WC-10 wait band (Medium)
- F8 §7.2 agentWait pass condition (Medium)
- F9 nested propagation (Medium)
- F10 stale contracts and version field (Medium)
- F11 blocked Task recovery (Medium)
- F12 §3.1 framing (Medium)
- F13 summary scope (Low)
- F14 "and answered" overreach (Low)
- F15 status vs blocked_question precedence (Medium)

## Coverage

Read in full: the candidate (285 lines), `README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, `command.md`, and `~/.claude/rules/prompts/document_review_loop_prompts.md`. Checked by grep or probe: `SPEC:172` (see Checks run). Spot-checked against the inventories: `SPEC:` cites to `INV-A`, `INV-B` and `CAPS` lines (for example `INV-A:62`, `INV-A:95`, `INV-B:31`, `INV-B:91`, `CAPS:52`, `CAPS:73`, `CAPS:142-144`); all matched the cited lines. Not covered: every citation to `src/`, `tests/`, `.dev/evals/`, `.dev/codegraph-migration/`, `/opt/Orca` or `~/.claude` (outside the sandbox, so UNVERIFIED here). No git command was run. No second reviewer and no VERIFY pass were run.

verdict: FAIL
