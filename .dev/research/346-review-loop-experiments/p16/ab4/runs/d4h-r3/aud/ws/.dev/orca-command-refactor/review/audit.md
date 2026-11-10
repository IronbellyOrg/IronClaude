review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `150cd2160e83032be24b36d6510052c36e52b128ef009a46dab2f911fab14ca3`
- Baseline: none given (first review of the full document; no `--re-review`, no `--baseline`).
- Reviewer model actually used: claude-sonnet-5-5 (Sonnet 5.5).
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full).
- Sandbox: only `ws/.dev/orca-command-refactor/{README.md,specs,inventory}` was readable. Every citation to a file outside that folder is UNVERIFIED here.
- Citation shorthand: `S:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`.

## What was covered

- Read in full: the candidate, `README.md`, all three inventories, the command definition and the FIRST-REVIEW prompt.
- Checked the candidate's inventory citations against the inventories. Every `INV-A:`/`INV-B:`/`CAPS:` line cited in sections 1-4, 6-9 and the Decisions table points at text that supports the claim. The 43 = 10 + 27 + 6 split matches both inventories (`INV-A:73`, `INV-B:278`) and the row counts in S:81-92 and S:97-125.
- Per-row phase counts: 10 ready commands (6 in P1, 4 in P2), 27 needing change (9 P1, 11 P2, 4 P3, 3 P4), 6 coordinator-only. These reproduce the P1-P4 lists at S:159-162.
- Not checkable here (UNVERIFIED): every `cmd/`, `sk/`, `ag/` line cited directly; `CLAUDE.md`, `HOW-WE-WORK.md`, `install_core.py`, `pyproject.toml`, `Makefile` lines (S:52, S:146, S:150, S:164, S:183, S:192); the `EVIDENCE.md`, codegraph-migration README and `return-contract.yaml` lines (S:22-23, S:43, S:59); the Orca guide text beyond what `orca-capabilities.md` quotes.
- Experts applied (fixed order): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Focus: requirements and architecture. `--focus correctness` was not requested, so no State Variable Registry. The Guard Condition Boundary Table is produced because the spec contains threshold and conditional logic.

## Blocking findings (1)

### F1 (CRITICAL, blocking): the P1 acceptance test and P1 scope contradict the spec's own per-row decisions

Experts: Wiegers (testability), Crispin (acceptance criteria), Fowler (phase boundaries).

An implementer who follows the stated text as written builds a P1 that adds a `## Unattended mode` section naming `return-contract.yaml` to every command in sections 3.1-3.2, and X is wrong because three stated texts cannot all hold:

1. **`/sc:load` has no contract.** AC-1.1 (S:195) requires every command in sections 3.1-3.2 to have a `## Unattended mode` section "naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". `/sc:load` is a section 3.2 row (S:112). The same document says "load has no contract, because it is not dispatched as its own Task" (S:76), the row says "Report: none (see note)" (S:112), and the Decisions table rejects a report file for load as "an unrequested addition" (S:265). AC-1.1 cannot pass without giving load a section that names a file load never writes, or adding the file the spec rejected. S:76 also says "Every changed command also gains the section", and load is changed (usage line, S:112), which makes S:112 and AC-1.1 collide directly.
2. **P1 covers commands whose rows belong to P3/P4.** P1 scope is "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (S:159). The per-row Phase column puts roadmap, save, validate-roadmap and validate-tests in P3, and implement, post-release and pr-submit in P4 (S:109, S:113-114, S:118-119, S:124-125). S:154 and S:225 say P4 waits for D2-D4. AC-1.1 is a P1 gate that must pass before P2 starts (S:154), so it forces edits to the P4 commands before those decisions.
3. **pr-submit.** D3 recommendation (a) is "no pr-submit changes in Phase 4" (S:240), and S:139 says pr-submit stays a worker candidate "only if the user accepts D3". AC-1.1 requires pr-submit to carry a section in P1. Section 4's "no `--unattended` mode" rule (S:128) is the only command group AC-1.1 excludes, and pr-submit is not in it.

Proof the stated text conflicts: AC-1.1 at S:195, S:76, S:112, S:159, S:240.

Wrong outcome: the P1 gate either never goes green, or a contract-naming section is added to load and to commands whose behavior is undecided.

Required repair (narrowest): restate AC-1.1 and the P1 scope sentence as "every command whose Phase column is P1, plus the six ready commands assigned to P1 in S:159, except load", and state what load gets (nothing, or the flag only). Delete rather than add.

## Medium findings (follow-up candidates, warnings only)

- **M1 (MAJOR label, Medium): two workers can collide on the contract for file-valued outputs.** S:76 puts the contract for tdd and init-lite in "a sibling `return-contract.yaml` in that file's directory". WC-11 (S:69) says two workers in one worktree never write the same file. Two tdd workers given `docs/auth/TDD_A.md` and `docs/auth/TDD_B.md` share `docs/auth/return-contract.yaml`. Section 2.3 (S:73) tells the coordinator to state "the output directory" but gives no rule for file-valued flags. Medium because it needs the coordinator to choose a shared directory.
- **M2 (Medium): WC-5 fails open on an unrecognised status.** S:63 maps "`succeeded` otherwise", and S:62 says commands with an existing contract "keep their fields". S:262 fixes the vocabulary to four values, but an existing contract may carry other values (INV-B:272 shows workflow's `status` includes `failed`, with no list of others). An unrecognised or missing `status` becomes `--outcome succeeded`, which would let dependent Tasks start (CAPS:88, CAPS:90). Suggested narrowing: any value outside the four, or no report, maps to `failed`.
- **M3 (Medium): WC-9/D4 depend on authorization flags the spec never names or adds.** S:67 says outward defaults "turn on only through the command's own explicit flag". The auggie-review row (S:100) says posting "returns only with an explicit `--post-pr`", but `INV-A:38` shows only `--no-post-pr` (the default is posting). The "Other required change" cell for auggie-review says "none", and no row adds an authorizing flag for post-release (S:113), task commit/push (S:121) or pr-submit (S:114). D4 option (a) (S:245) therefore has nothing to pass.
- **M4 (Medium): WC-6's "fresh output directory" conflicts with a coordinator-fixed directory.** S:64 has the command write a retry "into a fresh output directory", while WC-4 and S:73 require the coordinator to name the directory before dispatch. A `worker-start --retry-of` retry (CAPS:116) re-uses the same Task brief and so the same directory, and the spec does not say the coordinator must change it. Most 3.2 rows say "fresh dir" for resume.
- **M5 (Medium): AC-C1 can fail on text SA-2 allows.** AC-C1 (S:172) greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)`. SA-2 (S:147) allows an Orca example in the contract file, which lives in core (S:52). P0 also adds an Orca section to `HOW-WE-WORK.md` (S:158, S:150), which is also scanned. Any natural wording such as "orca orchestration ask" fails a check the spec says every phase must pass (S:167).
- **M6 (Medium): AC-2.2 expects a result WC-3 does not force.** S:61 lets a worker with a preamble `ask` the coordinator instead of stopping. AC-2.2 (S:200) expects `worker_done --outcome failed` and `status: blocked` for blocked gates. A worker that uses the permitted `ask` path passes WC-3 and fails AC-2.2. The step-2 `agentWait` check (S:181) also does not say whether a worker parked in `ask` shows a wait (`CAPS:129` describes human prompts only).
- **M7 (Medium): between P1 and P2, `--unattended` is accepted by gated commands but does not remove their gates.** S:159 adds the flag to every command and calls it a no-op "where a command has no gate". For cleanup, improve, tdd, troubleshoot, cli-eval and the other P2 commands the flag exists after P1 while the gates (S:160) still wait. S:154 only says "independently useful" and S:73 tells the coordinator to put `--unattended` in every brief. A coordinator briefing `/sc:cleanup --unattended` after P1 gets a silent stall (CAPS:52, CAPS:129). The spec should say that P1 must not accept the flag on a command whose gate is converted later, or mark such commands "not yet dispatchable" in the brief template.
- **M8 (Medium): no rule for a missing output directory.** WC-4 (S:62) says the contract is written "on success, failure, blocked and partial outcomes, including stops before any other output exists", but the output directory is "the directory the coordinator passed". If it was not passed, there is nowhere to write; only WC-5's "no report exists" branch (S:63) covers the result. The spec-panel command itself refuses before any work without a report directory (`command.md:460`), but section 2 does not generalise this.
- **M9 (Medium): WC-1's bound is not testable.** S:59 requires launch prompts to "fall back on its own well inside the readiness limit" without a number. The evidence it cites (CAPS:49) gives 30 s passing and about 45 s failing at a 45 s limit; the default limit is 60 s (CAPS:44). No AC checks WC-1 beyond `state: ready` (S:180).
- **M10 (Medium): WC-10's cli-eval wait split has no acceptance check.** S:68 and S:104 require waits of at most 4 minutes; AC-4.3 (S:210) tests only pr-submit, and P2 checks (S:199-203) do not test cli-eval timing.

## Minor notes

- N1: S:11 and S:68 cite `sk/sc-pr-submit-protocol/SKILL.md:37-39` for the top-level rule, while `CAPS:40` and `CAPS:161` quote the same text at `:47-49`. One of them is wrong; the file is outside the sandbox, so UNVERIFIED.
- N2: S:16 says command changes are "limited to" the contract, but section 3 and SA-4 (S:149) also list interface reconciliations, a tools-list edit and a changed default target. The scope sentence understates the work.
- N3: SA-3 (S:148) allows the contract file "when the caller passes the new output flag", while WC-4 (S:62) says the contract is written "in unattended mode". The conditions differ.
- N4: AC-1.3 (S:197) and AC-4.3 (S:210) ask for a "scratch worktree"/"scratch fork PR" with no creation method. The repo's worktree rules (Orca-created only) are outside the sandbox, so UNVERIFIED whether this conflicts.
- N5: The tasklist row (S:122) says "none" for nesting although INV-B:209-210 lists nested reflect spawning as UNVERIFIED; the spec's own UNVERIFIED list (S:272-285) omits it.
- N6: S:11 says the 11 re-read locations were "found as cited". Four of the 11 are outside the sandbox and could not be re-checked here.

## === REQUIREMENTS ANALYSIS ===

- Wiegers: requirements are numbered, owned and evidenced (S:57-70), which is above normal for this kind of spec. Weak points: WC-1 has no number (M9); WC-4 has no input-absent case (M8); WC-5 has an unbounded default (M2). F1 is a traceability break between requirement rows (S:76, S:112) and acceptance (S:195).
- Adzic: the examples at S:228 and the per-phase checks are concrete and runnable. AC-2.2 needs one scenario per branch of WC-3 (M6).
- Cockburn: the primary actor is the coordinator, and S:72-73 lists what the coordinator owes each worker. Missing: the person who authorizes outward actions has no named step beyond D4 (M3).
- Crispin: acceptance coverage is broad, but see F1, M5, M6, M10.

## === ARCHITECTURE ANALYSIS ===

- Fowler: the decision "Orca coordinates, commands stay units of work" is well argued (S:13-39, R1-R5 each cited to inventories). The rejected alternative is described fairly. Boundaries are clean: contract file in core, one short section per command. F1 shows the phase boundary leaks.
- Nygard: failure modes are covered (readiness, stall, retry, partial). Gaps: fail-open outcome mapping (M2), the P1-P2 stall window (M7), missing output directory (M8).
- Newman: the contract is a versionless set of fields (`status`, `command`, `report_path`, `artifacts`, `blocked_question`) shared across 30+ commands. No version field and no rule for adding fields later. Advisory only.
- Hohpe: the message pattern (preamble `ask`, `worker_done` once, `check` pull) follows the Orca guide as quoted in CAPS:58-67. File-valued outputs share a mailbox directory (M1).
- Gregory: three-amigos view: the coordinator, the command author and the tester each need different text; AC-1.1 is the one place they disagree (F1).
- Hightower: operational notes on heartbeats and wait splitting are sound (S:68); the pr-submit sleep length is acknowledged UNVERIFIED (S:283).

## Whittaker attacks

Per Whittaker's template; severities follow the Review Loop grading (not the label).

1. I can break this specification by **Sequence Attack**. The invariant at **AC-1.1 / S:159 / S:240** (every listed command carries the section in P1) fails when **pr-submit is left unchanged by D3(a)**. Concrete attack: before: pr-submit file unchanged, D3 answered (a); step: run AC-1.1; after: test red for pr-submit (and for roadmap, save, implement) and for load. Result: F1.
2. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 / S:63** fails when **a contract `status` is neither of the four values**. Before: contract `status: error`; step: worker maps "otherwise" to success; after: `--outcome succeeded`, dependents start. Result: M2. (Orca's own Task status `blocked` at CAPS:89 is a different word space from contract `blocked`; the spec's mapping to `failed` is clear, so no finding.)
3. I can break this specification by **Accumulation Attack**. The invariant at **WC-11 / S:69** fails when **two tdd workers write to the same directory**. Before: two TDD files in `docs/auth/`; step: both write the sibling contract; after: one contract overwrites the other. Result: M1.
4. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / S:62** fails when **no output directory was passed**. Before: brief omits `--output-dir`; after: nowhere to write the contract. Result: M8.
5. I can break this specification by **Divergence Attack**. The invariant at **WC-3 / AC-2.2 (S:61, S:200)** fails when **both a worker `ask` and a blocked stop are allowed**. Before: gate hit; branch A asks, branch B stops; AC passes only on B. Result: M6.

## Guard Condition Boundary Table

Guards found: G1 WC-5 outcome mapping (S:63); G2 WC-10 wait threshold (S:68); G3 WC-4 output-directory resolution (S:62); G4 WC-2 gate resolution (S:60). Classes left out: G1 Maximum/Overflow (no capacity); G2 Sentinel (no sentinel); G3 Maximum/Overflow (no capacity); G4 Maximum/Overflow (no capacity).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 outcome mapping | S:63 | Zero/Empty | no report file | failed branch | `--outcome failed` | OK |
| G1 outcome mapping | S:63 | One/Minimal | `status: succeeded` | succeeded branch | `--outcome succeeded` | OK |
| G1 outcome mapping | S:63 | Typical | `status: partial` | succeeded branch | `--outcome succeeded`, first sentence says partial | OK |
| G1 outcome mapping | S:63 | Sentinel Value Match | `status: blocked` | failed branch | `--outcome failed` | OK |
| G1 outcome mapping | S:63 | Legitimate Edge Case | status outside the four (existing contract) | "otherwise" branch | succeeded | GAP (M2) |
| G2 wait threshold | S:68 | Zero/Empty | no long wait | not triggered | no change | OK |
| G2 wait threshold | S:68 | One/Minimal | wait of 1 minute | not triggered | single call | OK |
| G2 wait threshold | S:68 | Typical | wait of 20 minutes | triggered | split into waits of at most 4 minutes | OK |
| G2 wait threshold | S:68 | Maximum/Overflow | wait of exactly 5 minutes | "longer than 5" false | no split required; heartbeat cadence also 5 minutes | GAP (minor, boundary unspecified) |
| G2 wait threshold | S:68 | Legitimate Edge Case | wait of 4.5 minutes | neither rule applies | not stated | GAP (minor) |
| G3 output directory | S:62 | Zero/Empty | directory not passed | no path | no rule except WC-5 "no report" | GAP (M8) |
| G3 output directory | S:62 | One/Minimal | one directory, one command | path known | contract at `<dir>/return-contract.yaml` | OK |
| G3 output directory | S:62, S:76 | Typical | `--output` is a file | parent directory | sibling contract | OK |
| G3 output directory | S:76, S:69 | Legitimate Edge Case | two file outputs, same directory | same contract path | not stated | GAP (M1) |
| G3 output directory | S:62 | Sentinel Value Match | directory already holds a contract (retry) | path exists | "fresh dir" claim vs coordinator-fixed path | GAP (M4) |
| G4 gate resolution | S:60 | Zero/Empty | command has no gate | not triggered | flag is a no-op | OK |
| G4 gate resolution | S:60 | One/Minimal | one gate, default exists | (a) | documented default | OK |
| G4 gate resolution | S:60 | Typical | one gate, flag supplied | (b) | uses flag | OK |
| G4 gate resolution | S:60 | Sentinel Value Match | gate not yet converted (P1 state) | not resolved | gate waits | GAP (M7) |
| G4 gate resolution | S:60, S:61 | Legitimate Edge Case | blocked gate, preamble present | (c) or `ask` | both allowed | GAP (M6) |

Table completeness: all guards enumerated, all cells populated; FR-10 satisfied. GAP entries propagate as priority targets for `sc:adversarial` AD-1. Of the GAP rows, only F1 meets the blocking test; the rest are Medium or minor under Review Loop bullet 2.

## Quantity Flow Diagram (count conservation of the command split)

```text
[Source: 43 commands (21 INV-A + 22 INV-B)] --> [Verdict split] --> 10 ready + 27 needing change + 6 coordinator-only = 43
   ready (10)   --> P1: 6 (adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow) ; P2: 4 (reflect, release-split, tdd, troubleshoot)
   change (27)  --> P1: 9 ; P2: 11 ; P3: 4 ; P4: 3 = 27
   coordinator-only (6) --> no phase
P1 consumers: AC-1.1 expects the section on 37 commands (S:159, S:195)  <-- MISMATCH: only 15 are P1 by row (6 + 9), and load (1 of the 9) has no contract
```

Counts conserve across the split. The mismatch is the F1 finding.

## follow-up candidates

M1-M10 and N1-N6 above are Medium or minor, never block, and are not part of the Reviser brief. The session running this loop is to ask the user once whether to open an issue for them; this run created none and asked no one.

## Reviser brief

Revise only the text that F1 names. Add no rule, mechanism or section that a blocking finding does not call for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

Blocking finding ids: F1.

verdict: FAIL
