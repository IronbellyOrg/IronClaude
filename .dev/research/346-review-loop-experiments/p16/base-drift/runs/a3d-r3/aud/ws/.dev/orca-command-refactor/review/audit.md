review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec; first review of the whole document (FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `ee66feb509d270d43ad6b910ad610ca80e6ec53ce17ddf42d33226ff403c6470`
- baseline: n/a (first review; no `--re-review`, no `--baseline`)
- reviewer model used: claude-sonnet-5-5
- brief clauses overridden: none
- citation convention: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `CMD:N` = line N of `command.md` (the /sc:spec-panel definition). Any citation I could not check inside the workspace is marked UNVERIFIED.

## What I covered
- Read in full: README (`.dev/orca-command-refactor/README.md`), the candidate (285 lines), the three inventories, the review-loop prompts file and command.md.
- Checked: the 10/27/6 split against both inventories (it holds: 5+5 ready, 13+14 needs-change, 3+3 coordinator-only, `INV-A:73`, `INV-B:278`; the 3.1, 3.2 and section 4 lists name 10, 27 and 6 distinct commands). The section 3.2 phase column against the section 6 command lists (it matches: 9 + 11 + 4 + 3 = 27 in P1..P4, with 4 more 3.1 commands in P2). The `INV-*` and `CAPS:*` line pointers I could resolve (all resolve to the cited content). Requirements WC-1..WC-12 against SA-1..SA-6, the phases and the acceptance checks AC-*.
- Not checkable in this sandbox (UNVERIFIED): every citation into `CLAUDE.md`, `src/superclaude/...` (`cmd/`, `sk/`), `Makefile`, `pyproject.toml:38`, `install_core.py`, `HOW-WE-WORK.md`, `.dev/evals/.../EVIDENCE.md`, `.dev/codegraph-migration/...`. Where the inventories quote the same line, I treated the citation as supported only through that quote.
- Not run: no command or Orca call (none exists in the sandbox).

## Panel
Focus requirements: Wiegers (lead), Adzic, Cockburn. Focus architecture: Fowler (lead), Newman, Hohpe, Nygard. Whittaker (adversarial, every panel). Review order per command.md:103-113 restricted to these experts. Correctness focus is not active, so no State Variable Registry is produced. Advisory (CMD:192): the spec has numeric guard thresholds (0.70 confidence, 5/4 minute wait, depth 1, 60 s readiness) and 3+ mutable files, so `--focus correctness` is recommended for a later review.

=== REQUIREMENTS ANALYSIS ===

### F-01 | MAJOR | BLOCKING | priority High | Wiegers, Adzic
**Issue.** The P1 acceptance test AC-1.1 cannot pass against the P1 scope the spec itself states.
- AC-1.1 (SPEC:195) asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and (SPEC:171, SPEC:167) a phase passes only when every check in its block passes.
- `/sc:load` is a 3.2 command (SPEC:112) whose report is "none (see note)", whose resume is "n/a", and which "use it as a step inside another worker's brief, not as its own Task"; the P1 row lists it as "load (usage line only)" (SPEC:159) and the Decisions table says a report file "would be an unrequested addition" (SPEC:265). A section that names `return-contract.yaml` for load contradicts all three.
- AC-1.1 also covers the P4 commands `/sc:implement`, `/sc:post-release` and `/sc:pr-submit` (SPEC:109, 113, 114). Phase 4 "waits for answers to D2-D4" (SPEC:154), and D3's recommended option (a) says "no pr-submit changes in Phase 4" (SPEC:240). P1's scope sentence "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (SPEC:159) reads the other way, while its Commands column lists only 9 commands plus 4 fixes.

**Grading sentence.** An implementer who follows the stated text as written (P1 Commands column and the load row) builds P1 with `/sc:load` untouched except for its usage line and with no `## Unattended mode` section on the P2-P4 commands, and that is wrong because AC-1.1, a P1 pass condition, then fails; the implementer who instead satisfies AC-1.1 must edit load, implement, post-release and pr-submit in P1, which SPEC:109-114, SPEC:154 and SPEC:240 forbid. Two stated texts contradict each other with no assumption needed.

**Recommendation.** Narrow AC-1.1's quantifier to the commands the section 6 P1 row names (plus the 3.1 commands whose section 3.1 row says P1), and let AC-2.1, AC-3.x and AC-4.x carry the same assertion for their own commands; say explicitly that `/sc:load` gets no `## Unattended mode` section. Rationale: deleting a clause is smaller than adding rules. Quality impact: removes an unpassable gate (testability +).

=== ARCHITECTURE ANALYSIS ===

(No blocking architecture finding. The central decision, section 1, is supported: R1-R5 (SPEC:31-37) resolve to `CAPS:97-103`, `CAPS:145-150`; E4/E5 hold against `CAPS:155`. The spec states its evidence gaps itself (SPEC:41-45).)

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

### Medium
- **M-01 | MAJOR label, graded Medium | Nygard, Whittaker (Sequence attack).** WC-6 (SPEC:64) makes a command without a resume flag "write each run into a fresh output directory" (Owner: Command), while WC-4 (SPEC:62) fixes the contract at `<output-dir>/return-contract.yaml`, the directory the coordinator passed, and 2.3 (SPEC:73) requires that path before dispatch. The spec never says who makes the directory fresh. Attack: retry worker B is started with the same `--output` as failed attempt A; B is killed before it writes its contract; A's stale `status: succeeded` file satisfies `test -s` and the status assert in AC step 4 (SPEC:183). Graded Medium because it needs the reading "coordinator reuses the dir". Fix direction: one sentence that the brief gives a unique output path per Dispatch and the command removes or refuses a stale contract.
- **M-02 | Cockburn, Wiegers.** 2.3 says the brief carries the output directory so the report path is "known before dispatch" (SPEC:73), but the 3.1 "Brief must pass" column gives no `--output` for troubleshoot, reflect or workflow (SPEC:88, 91, 92), and workflow has no output flag (its contract lives at `.dev/tasks/to-do/<id>/`, `INV-B:272`; troubleshoot's default dir carries a timestamp, `INV-B:242`). The P1 fix "write the contract for pre-creation STOPs too" (SPEC:92) names no location, because no `<id>` directory exists before creation; AC-1.4 (SPEC:198) only checks that text says so. A requirement the document does not state, so Medium.
- **M-03 | Fowler.** AC-C1 (SPEC:172) must print nothing for `orca(-ide) (orchestration|worktree|terminal|agent)` in `src/superclaude/core` in every phase, but P0 adds an Orca section to `HOW-WE-WORK.md` and a contract file with a coordinator brief template in that directory (SPEC:158), and SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (SPEC:147). Whether those texts may contain `orca orchestration ask` is undecided. In the raw file the pattern also carries `\|`, which is a literal pipe under `grep -E` outside a markdown table.
- **M-04 | Wiegers.** WC-4 (SPEC:62) says commands that already write a contract "keep their fields and add the missing ones", yet `status` must be one of four values, and AC step 4 (SPEC:183) asserts it for P1 live checks. The existing contracts' status vocabularies (workflow, brainstorm, reflect, adversarial; `INV-B:272`, `INV-A:97`) were never read; if one differs, a command cannot both keep its field and pass AC-1.2.
- **M-05 | Cockburn.** D4 (SPEC:244) says it affects auggie-review `--post-pr` and task `commit`/`push`, yet those rows are P2 (SPEC:100, 121) and "Phases 1-3 need no user decision" (SPEC:154). Under D4 option (b) "Never", the P2 rows (an explicit `--post-pr` in the brief) would need rework.
- **M-06 | Newman, Hohpe.** The sibling definition under review contradicts WC-4 and F-1 in three places: its Unattended section takes `--report-dir` (not `--output`/`--output-dir`), writes `<report-dir>/return-contract.yaml` even when `--output` is a file, and on a missing report dir prints a chat-only refusal and writes no contract (CMD:459-463). The spec's spec-panel row (SPEC:120) and F-1 (SPEC:62) assume the opposite. Either the spec or the command is stale; the spec is silent on which wins.
- **M-07 | Nygard.** WC-1 (SPEC:59) is owned by "Launch setup, not commands" but no phase, command or acceptance check assigns work for it; section 6 (SPEC:156-162) and section 8 (SPEC:212-222) never mention the ccsession-tag launcher that E5 names (SPEC:25). Only the generic step-1 readiness pass (SPEC:180) touches it.
- **M-08 | Adzic.** 2.3 requires the brief's command line to include `--unattended` (SPEC:73), but the flag exists only after P1 (SPEC:159), and the 3.1 and AC-0.4 command lines omit it (SPEC:81-92, 194). AC-2.2 expects `--outcome failed` and `status: blocked` for a gate hit (SPEC:200) although WC-3 lets the worker `ask` instead (SPEC:61); the brief must say not to.
- **M-09 | Fowler.** P0's rationale says the smoke runs "test the decision before anything is built on it" (SPEC:158), but the same row builds the contract file, the install-list change, the routing-guide section and the test file first; the failure branch "reopens section 1" (SPEC:194) after those edits.

### Minor
- m-01. Section 4 supports "need the user's authorization in this repo" for `/sc:git` with `README.md:31` (SPEC:133), which is a rule for this run's workers (`.dev/orca-command-refactor/README.md:31`), not a repo-wide rule.
- m-02. WC-9 (SPEC:67) names the command's "own explicit flag", but task `commit`/`push` are keywords, not flags (SPEC:121); reflect's default UC-2 folder move and tracked `docs/memory/reflect/...` write (`INV-B:114`) fall outside WC-9's list.
- m-03. The pr-submit top-level rule is cited as `sk/sc-pr-submit-protocol/SKILL.md:37-39` (SPEC:65, `INV-B:90`), but `CAPS:161` cites `:47-49` of the installed copy; likely different copies, UNVERIFIED which lines the repo file has.
- m-04. `--unattended` detection when the string appears inside quoted content is not stated in the spec (CMD:459 does state it); a prompt such as `"login fails --unattended"` is a sentinel collision (Whittaker FR-2.3).
- m-05. The "11 re-read locations" and "about 340 citations re-read" (SPEC:11, SPEC:285) cannot be checked here (UNVERIFIED).

## Guard Condition Boundary Table
Guards found: G1 confidence threshold 0.70 (task, SPEC:121); G2 wait/heartbeat 4 and 5 minutes (WC-10, SPEC:68); G3 nested depth 1 (SPEC:33); G4 readiness 60 s (WC-1, SPEC:59); G5 `--outcome` mapping (WC-5, SPEC:63); G6 `--output` file versus directory (WC-4, SPEC:62). Omitted classes carry a one-line reason. Table completed before synthesis (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 confidence < 0.70 | SPEC:121 | Zero/Empty | confidence unavailable (`null`) | not stated | not specified | OK (non-blocking): class not reachable, the command computes it (`INV-B:199`) |
| G1 | SPEC:121 | Typical | 0.50 | true | blocked, contract written | OK |
| G1 | SPEC:121 | Legitimate Edge Case | exactly 0.70 | false | proceed (stated `below 0.70`) | OK |
| G2 4 min wait | SPEC:68 | Zero/Empty | wait of 0 s | n/a | no rule | OK: a zero wait cannot overrun 5 minutes |
| G2 | SPEC:68 | Maximum/Overflow | single call 5 min + 1 s | true | must be split (WC-10) | OK |
| G2 | SPEC:68, 114 | Legitimate Edge Case | pr-submit poll script runtime unknown | unknown | UNVERIFIED, deferred to P4 check AC-4.3 (SPEC:210) | OK (stated as UNVERIFIED) |
| G3 depth 1 | SPEC:33 | Sentinel Value Match | depth setting 0 or malformed | n/a | out of scope; Orca falls back to default (`CAPS:100`) | OK |
| G4 60 s readiness | SPEC:59 | Maximum/Overflow | launch prompt fallback 46-60 s | true | "well inside" the limit, no number | GAP (Medium M-07 area): evidence says about 45 s fails (`CAPS:49`), the text gives no bound |
| G5 outcome mapping | SPEC:63 | Zero/Empty | no report file | true | `failed` | OK |
| G5 | SPEC:63 | Sentinel Value Match | `partial` | false for failed | `succeeded`, status in first sentence | OK |
| G5 | SPEC:63 | Legitimate Edge Case | stale report from a prior attempt | not stated | not specified | GAP (Medium M-01) |
| G6 file vs directory | SPEC:62 | Typical | `--output docs/auth/TDD_AUTH.md` | true | sibling `TDD_AUTH.return-contract.yaml` | OK |
| G6 | SPEC:62, 92 | Zero/Empty | no `--output` flag exists (workflow) / pre-creation STOP | not stated | location not specified | GAP (Medium M-02) |
| G6 | SPEC:62, CMD:459-463 | Legitimate Edge Case | `--report-dir` missing under `--unattended` | refused | spec requires a contract on every outcome; command prints chat only | GAP (Medium M-06) |

Classes left out: One/Minimal for G1-G6 (no distinct behavior from Typical); Maximum for G1, G5, G6 (bounded domains).
FR-8/FR-9 grading: the GAP rows name no concrete wrong outcome that follows from the stated text without a guess, so all are Medium.

## Whittaker attacks (adversarial)
- Sequence (FR-2.4): retry with a reused output directory leaves a stale contract that passes `test -s` (M-01). Before: A wrote `succeeded`; after B killed: file unchanged and read as B's result.
- Zero/Empty (FR-2.1): `/sc:workflow` stopped before package creation has no directory for its contract (M-02).
- Sentinel collision (FR-2.3): `--unattended` inside quoted prompt text (m-04).
- Divergence (FR-2.2): `partial` maps to `succeeded` while `blocked` maps to `failed` (SPEC:63); a partial run that stopped on a gate has no stated class. Not graded blocking: WC-2 (c) says gates resolve as `blocked`.
- Accumulation (FR-2.5): not applicable, no counters or buffers are specified.

## Pipeline Dimensional Analysis
Not triggered: the spec describes no multi-stage data pipeline where a stage's output count differs from its input. The only counts are classification totals, and they are conserved: 21 + 22 = 43 = 10 + 27 + 6 (`INV-A:73`, `INV-B:278`, SPEC:76); phase counts 9 + 11 + 4 + 3 = 27 (SPEC:159-162).

## Consensus and disagreements
- Consensus: the decision (Orca coordinates, commands stay workers), the six coordinator-only commands, and the phase order are sound and evidenced.
- Disagreement: Wiegers and Adzic treat the AC-1.1 contradiction as blocking; Fowler and Nygard would raise M-01 to blocking if the coordinator is ever allowed to reuse an output path. Under the grading rule M-01 stays Medium.

## Follow-up candidates (recorded, not asked)
M-01 to M-09 and m-01 to m-05 above. This run is a coordinator-launched audit with no user in the loop, so the once-per-loop question about opening an issue was not asked and no issue was created.

## Reviser brief
Blocking finding ids: F-01 only. Rules (command.md Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on every added paragraph or table; prefer deleting or narrowing to adding; report the candidate's byte size before and after and the bytes added and deleted per finding id. Leave Medium and minor findings alone.
- F-01: repair AC-1.1 (SPEC:195) and, only if needed, the P1 scope sentence (SPEC:159) so that the assertion covers exactly the commands whose P1 row says they receive the section, and states that `/sc:load` receives none.

verdict: FAIL
