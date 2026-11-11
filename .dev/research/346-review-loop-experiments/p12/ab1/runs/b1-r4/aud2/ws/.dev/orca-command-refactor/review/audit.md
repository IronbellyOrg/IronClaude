review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `ecccef2cd605be2429bee0a2ca58d7ed10decc68e84a2d03445f68dc64843d1c`
- baseline: none (first review of the full document; no `--re-review` or `--baseline` given)
- reviewer model used: claude-sonnet-5-5
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` per the FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, lines 1-55)
- other inputs read: `.dev/orca-command-refactor/README.md` (sha256 `086e5b82...2069e`), `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`
- panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, always active). Crispin completes the boundary table.
- notation: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of the three inventory files (the spec's own convention, SPEC:8-10); `README:N` = line N of the README.

## Coverage statement

Covered: all 9 sections of the candidate plus its Decisions and UNVERIFIED lists. I checked every `INV-A`, `INV-B` and `CAPS` line citation I could find in the spec against the inventory files. They all land on the claimed content: the 43/10/27/6 split, the per-command rows in sections 3 and 4, and the Orca facts used in WC-1 to WC-12 and R1 to R5.

I cannot check these, so they are UNVERIFIED here:

- Every `cmd/...`, `sk/...`, `ag/...` source line.
- `src/superclaude/cli/install_core.py`, `src/superclaude/core/HOW-WE-WORK.md`, `Makefile`, `pyproject.toml` and `CLAUDE.md` line cites.
- `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md` and the `.dev/codegraph-migration/...` files.
- The `grep -rlni orca` run behind E5 (SPEC:25).
- The claimed `evidence-validator` pass (SPEC:285).

Where the inventories re-quote such a line, I treated it as the inventory's claim, not as verified.

Not done: no command was run and no Orca call was made (no Orca in this sandbox). No test of the candidate's shell checks was run.

## Prior-findings table

Not applicable (review 1).

## === REQUIREMENTS ANALYSIS ===

### F-1  Blocking, MAJOR (Wiegers, Whittaker): the contract location rule for a file-valued `--output` collides with the parallel-write rule

- Stated texts: WC-4 says that when `--output` is a file, `<output-dir>` "is that file's parent directory", and the contract is written at `<output-dir>/return-contract.yaml` (SPEC:62). WC-11 says "Two workers in one worktree must never write the same file" (SPEC:69).
- The spec's own briefs use file-valued `--output` for `tdd` (SPEC:90), `init-lite` (SPEC:87) and `spec-panel` (SPEC:120). The `tdd` default target is `docs/[domain]/TDD_[COMPONENT-NAME].md` (INV-B:222, `cmd/tdd.md:49` via INV-B), so sibling TDDs share a parent by default.
- Wrong outcome: an implementer who follows WC-4 as written puts the contract at the parent of the `--output` file. Two parallel `tdd` workers with `docs/auth/TDD_A.md` and `docs/auth/TDD_B.md` both write `docs/auth/return-contract.yaml`.
- The second write replaces the first, and both workers pass the same `--report-path`. If worker A ended `blocked` and B `succeeded`, the coordinator opens one file and reads B's status for A (WC-4 and 2.3 make the coordinator open that file, SPEC:62, SPEC:73).
- This is two stated texts contradicting each other, with no extra assumption beyond the spec's own model of parallel workers in one worktree (CAPS:115, SPEC:69).
- Recommendation: derive the contract name from the output file for file-valued outputs (for example `<output-file-stem>.return-contract.yaml`), or require the coordinator to give each worker its own directory and state that rule in WC-4 and 2.3.
- Priority: High. Quality impact: coordinator reads the wrong worker's status.

### F-2  Medium (Wiegers): a retry can reuse a directory that holds the previous attempt's contract, and the contract has no field that tells attempts apart

- WC-6 requires a retry not to corrupt the first attempt (SPEC:64). Most commands meet that with "fresh dir" (SPEC:99-125), but the spec never says who makes the directory fresh.
- WC-4 makes the report path known before dispatch from the directory the coordinator passes (SPEC:62), and 2.3 repeats it (SPEC:73). A `--retry-of` brief therefore carries the same `--output`.
- The required contract fields are `status`, `command`, `report_path`, `artifacts`, `blocked_question` (SPEC:62). There is no run, attempt or dispatch id and no timestamp.
- If attempt 2 dies before writing, the coordinator and the WC-5 mapping read attempt 1's contract. This is wrong when attempt 1's contract says `succeeded` or `partial`.
- AC-3.2 goes the other way: it tests that a roadmap run with an existing `.session-memory.md` and no resume flag "starts fresh" in the same `<dir>` (SPEC:205).
- This is a requirement the document never states, not a stated text that does harm, so it is graded Medium.

### F-3  Medium (Wiegers, Cockburn): behavior when `--unattended` is passed without an output location is undefined

- WC-4 defines `<output-dir>` as the directory "the coordinator passed" and demands a contract "including stops before any other output exists" (SPEC:62). 2.3 only says the brief states it (SPEC:73).
- Nothing says what a command does when `--unattended` arrives with no output flag. This applies to every command that gains the flag in P1/P2 (SPEC:99-125). A blocked stop then has no place to write its contract.
- Missing requirement. Graded Medium.

### F-4  Medium (Wiegers, Adzic): contract location for `workflow` pre-creation stops and for commands whose path is created at run time contradicts "known before dispatch"

- WC-4's title requires the report file to be "known before dispatch" (SPEC:62).
- The workflow row puts the contract at `.dev/tasks/to-do/<id>/return-contract.yaml` and adds "write the contract for pre-creation STOPs too" (SPEC:92, INV-B:272). The package `<id>` does not exist before creation, and the brief in 3.1 passes only `--handoff none`.
- A pre-creation stop has no directory to write to, and the spec gives none. AC-1.4 only greps that the ref "states" the contract is written (SPEC:198), so it passes without a location.
- The research row has the same shape: "contract naming the generated `claudedocs/research_*.md` path" with no stated contract location (SPEC:116).
- No harm results from a worker reporting the path after the fact, so this is Medium. A pre-creation location is a missing requirement.

### F-5  Medium (Wiegers): SA-3 and WC-4 disagree on when a contract is written

- WC-4 writes the contract "In unattended mode" (SPEC:62).
- SA-3 says the contract and report files are written "only in unattended mode or when the caller passes the new output flag" (SPEC:148).
- For commands that gain `--output` in P1 (analyze, build, design, and others, SPEC:99-111), a plain `--output x` run without `--unattended` is a contract writer under SA-3 and not under WC-4. AC-1.3 tests only the no-flag case (SPEC:197).
- Two readings are allowed, so Medium.

### F-6  Medium (Adzic, Crispin): WC-10's trigger is looser than the checks that test it

- WC-10 requires splitting only for a call that blocks "longer than 5 minutes", into waits of "at most 4 minutes" (SPEC:68).
- The pr-submit row asks that each iteration "stays under 4 minutes" (SPEC:114), and AC-4.3 fails any "single tool call" over 240 s (SPEC:210).
- A 270 s wait follows WC-10 and fails AC-4.3. A reader of WC-10 alone leaves it unsplit.
- This needs the implementer to pick one of two allowed readings, so Medium.

### F-7  Medium (Wiegers, Whittaker): WC-9 says outward actions turn on "only through the command's own explicit flag", but the spec names no such flag for post-release or task

- WC-9 (SPEC:67) and D4(a) (SPEC:245) assume a per-command explicit flag.
- For post-release, the inventory shows a conversational rule ("unless the user pre-authorized them this session", INV-B:79, INV-B:84), not a flag. The post-release row lists "none" as other required change (SPEC:113).
- For `/sc:task`, `commit` and `push` are EXEMPT keywords in the argument (INV-B:204), not flags. The task row says "refused unless authorized" without naming how authorization is given (SPEC:121).
- AC-4.2 runs "with no authorization flags" (SPEC:209), which assumes flags exist; no positive-path check is possible.
- Missing requirement, graded Medium.

### F-8  Medium (Whittaker, Sentinel Collision): `--unattended` is a control token with no rule against collision with user content

- D1(a) selects an explicit `--unattended` flag and calls it one that "cannot misfire on a person" (SPEC:228).
- The spec does not say the token counts only as a standalone argument outside quoted or inline content. Several unattended commands take free text: `/sc:tdd "<topic>"`, `/sc:spec-panel "<inline content>"`, `/sc:troubleshoot "<symptom>"`.
- A quoted topic or pasted spec that contains `--unattended` can flip the mode, and flipping it also turns off outward defaults (WC-9).
- The command definition in this sandbox (`command.md:459`) already states such a standalone-token rule for spec-panel, so the spec's omission is a visible gap relative to a sibling design.
- Missing requirement, Medium.

### F-9  Medium (Wiegers): WC-11 versus ready commands with fixed output paths

- WC-11 requires default output paths to carry a timestamp or the coordinator's slug (SPEC:69).
- `index-repo` writes fixed `PROJECT_INDEX.md`, listed "ready" with the fix "State the output location" (SPEC:86, INV-A:53). The `cleanup-audit` row notes the one-per-worktree limit (SPEC:85), but the `index-repo` row does not.
- `reflect` writes a tracked shared file `docs/memory/reflect/deviation-patterns-<slug>.md` (INV-B:114), not mentioned in its 3.1 row (SPEC:88).
- Two parallel workers of these commands in one worktree collide. This is an unstated restriction, so Medium.

### F-10  Medium (Cockburn): worker-session duties are delivered through the command's `## Unattended mode` section, which ready commands do not have

- WC-3, WC-5, WC-7 and WC-12 are owned by the worker session (SPEC:61, 63, 65, 70).
- The only stated delivery of these rules to a worker is the shared contract file read by commands that have the new section (SPEC:52), and the brief contents in 2.3 (SPEC:73).
- 2.3 lists the command line, the output directory, authorized outward actions and worktree placement. It does not list WC-5's outcome mapping (for example "FAIL verdict still means `succeeded`") or "read `~/.claude/WORKER-CONTRACT.md`".
- The 10 ready commands run as workers in P0 with no section until P1 or P2 (SPEC:158-160).
- The brief template in P0 may cover this (SPEC:158), but the spec does not say so. Medium.

### F-11  Medium (Wiegers): tasklist `needs_human_decision` HALT has no resolution

- Stage 10.5 says `needs_human_decision` items HALT (INV-B:209).
- The tasklist row defines only `--unattended` passthrough to reflect (SPEC:122). WC-2 requires every gate to resolve (SPEC:60). Missing requirement, Medium.

### F-12  Medium (Wiegers): completeness of the "43 commands" claim

- SPEC:76 says the 43 commands in `cmd/` are all of them (INV-A:3 plus INV-B:3).
- UNVERIFIED in this sandbox. The command list visible to this reviewer's session also includes `/sc:graph`, `/sc:impact` and `/sc:issue`, which are in neither inventory. The `sc:issue` description there says it creates an Orca worktree and launches an agent, which would contradict E5 ("no command, skill, agent or core file calls Orca today", SPEC:25) and SA-2 (SPEC:147).
- I could not check `cmd/` from the sandbox. The coordinator should check before treating the split as complete.

### Notes (minor, never fail the review)

- N-1: the tags `M1`..`M5` appear at SPEC:76, 159, 194, 195 without any definition in the document (they look like review-loop markers). A reader cannot resolve them.
- N-2: WC-4 states "Orca does not check the file" as a requirement premise (SPEC:62) while its own evidence cell and UNVERIFIED item 3 say that is unverified (SPEC:62, SPEC:274, CAPS:79).
- N-3: the Decisions row cites adversarial among commands that "already write `return-contract.yaml`" (SPEC:261), while the spec elsewhere records that adversarial's filename is not fixed (SPEC:83, INV-A:35, INV-A:60).
- N-4: the WC-4 fixed four-value status set may conflict with "keep their fields" for existing contracts (SPEC:62, SPEC:262). The existing status vocabularies were not given in the inventories, so this is UNVERIFIED.
- N-5: AC-1.3 suggests a "scratch worktree" (SPEC:197). The project rule is that worktrees are created only through Orca with an agent (CLAUDE.md worktree section; no workspace file, UNVERIFIED).
- N-6: the cli-eval wait split (SPEC:104) and the reflect/tasklist reuse of the headless rule (SPEC:88, 122) edit or reuse existing lines, which SA-4's named-fix list does not include (SPEC:149).
- N-7: reflect `--remediate` auto-accepts under `--unattended` (SPEC:88) while troubleshoot `--fix` resolves as blocked (SPEC:91). Both are the same kind of offer (INV-B:109, INV-B:239).

## === ARCHITECTURE ANALYSIS ===

### Fowler (boundaries, interfaces)

The boundary is sound and well argued. Orca stays on top, commands stay units of work, and the shared rules live in one installed document (SPEC:13-39, 52). R1 to R5 are backed by CAPS lines I checked (CAPS:97-103, 145-150). One interface smell: `--unattended` bundles three separate concerns, namely no prompts, outward actions off, and a report file (SPEC:51, 60, 62, 67). This is acceptable but is the root of F-5 and F-7.

### Newman (evolution, compatibility)

SA-1 to SA-6 are a solid backward-compatibility set (SPEC:141-151). Gap: plugin mirror handling is listed as UNVERIFIED item 8 (SPEC:279), and AC-C2 `make verify-sync` covers only `.claude/` (SPEC:173). Edits to a `plugins/superclaude/commands/` mirror are not checked by any phase. This is a missing check, Medium (F-13 below).

### Hohpe (message exchange)

The ask/reply/check/worker_done choreography matches CAPS:58-80. Ordering is stated: check before worker_done, `consumer_fenced` stop, exactly one `worker_done` (SPEC:63, 70). The contract file is the second channel and carries no attempt identity (F-2).

### Nygard (failure modes)

- Worker dies before writing: WC-5 maps "no report exists" to failed (SPEC:63), but a stale file from an earlier attempt can exist (F-2).
- Contract read while being written: no atomic-write or write-last rule is stated. Minor; the coordinator reads after `worker_done`.
- Retry and circuit breaker: a worker's own `failed` report does not trip the breaker (CAPS:80, SPEC:263). A command that ends `blocked` on every attempt therefore never trips it, which can loop a coordinator retry. Minor note.

### F-13  Medium: plugin mirror not covered by any acceptance check

See Newman above. Requirement never stated for the mirror, and the spec's own UNVERIFIED item 8 flags it.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Findings use the FR-3 template.

1. I can break this specification by **Accumulation Attack** (two writers, one file). The invariant at **WC-4 and WC-11 (SPEC:62, 69)** fails when **two parallel workers pass `--output` files in one directory**. Concrete attack: state before: `docs/auth/` has no contract. W1 (`TDD_A.md`) ends `blocked` and writes `status: blocked`; W2 (`TDD_B.md`) ends `succeeded` and overwrites it. After: one file says `succeeded`; W1's `--report-path` points at it. Result: W1's block is invisible. Severity: blocking (F-1).
2. I can break this specification by **Sequence Attack**. The invariant at **WC-6 and WC-4 (SPEC:62, 64)** fails when **a retry runs in the directory of a finished attempt and crashes early**. Concrete attack: attempt 1 writes `status: partial` at D. Attempt 2, same brief and same D, dies at start. Coordinator reads `partial`, which WC-5 maps to `succeeded`. Severity: Medium (F-2).
3. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)** fails when **`--unattended` is passed with no output flag**. Concrete attack: `/sc:analyze src --unattended`; no `<output-dir>` exists, so the blocked/failed contract has no home. Severity: Medium (F-3).
4. I can break this specification by **Sentinel Collision Attack**. The invariant at **D1(a) (SPEC:228)** fails when **user content contains the control token**. Concrete attack: `/sc:tdd "document how --unattended works" --output x.md` can be read as unattended mode and turn off outward defaults. Severity: Medium (F-8).
5. I can break this specification by **Divergence Attack**. The invariant at **WC-10 (SPEC:68) versus AC-4.3 (SPEC:210)** fails when **a wait is between 240 s and 300 s**. Concrete attack: a 270 s pr-submit poll satisfies WC-10 and fails AC-4.3. Severity: Medium (F-6).
6. I can break this specification by **Sequence Attack**. The invariant at **AC-C1 (SPEC:172) versus SA-2 (SPEC:147) and the P0 core edits (SPEC:158)** fails when **the contract file or the new HOW-WE-WORK Orca section contains the phrase `orca orchestration ...`**. Concrete attack: the grep greps `src/superclaude/core`, so the P0 deliverables are themselves matches, even though SA-2 allows an Orca example inside the contract file. This needs the assumption that those documents spell out the command, so it is Medium (F-14 below).

### F-14  Medium: AC-C1 scans `src/superclaude/core` while SA-2 allows an Orca mention in the contract file

AC-C1's pattern is `orca(-ide)? (orchestration|worktree|terminal|agent)` across commands, skills, agents and core, excluding only `ccsession-tag` (SPEC:172). If the P0 contract or routing section names an Orca command, AC-C1 fails in every phase. The spec does not say how it should be spelled. Medium.

## Guard Condition Boundary Table

Guards found in the candidate: the 60 s readiness limit (WC-1), the heartbeat and wait thresholds (WC-10), the `--output` file-versus-directory rule (WC-4), the `--unattended` token (D1), the confidence threshold 0.70 (task row), nesting depth 1 (R1), and the circuit breaker of 3 failures (CAPS:80, used at SPEC:263). Classes that cannot occur for a guard are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit | SPEC:59 | Typical | fallback 30 s | passes | EVIDENCE passes at 30 s fallback | OK |
| readiness limit | SPEC:59 | Maximum/Overflow | fallback above about 45 s | fails | "well inside" the limit, no number given in WC-1 | GAP (Medium: no value stated; evidence supports about 45 s only via SPEC:59 cite, unverifiable here) |
| `--output` file-or-dir | SPEC:62 | Typical (directory) | `--output dir/` | contract in dir | specified | OK |
| `--output` file-or-dir | SPEC:62 | Legitimate Edge Case | `--output docs/a/X.md`, sibling output | contract in `docs/a/` | collides with WC-11 | GAP (F-1, blocking) |
| `--output` file-or-dir | SPEC:62 | Zero/Empty | no output flag under `--unattended` | none | unspecified | GAP (F-3, Medium) |
| `--unattended` token | SPEC:51, 228 | Sentinel Value Match | token inside quoted topic | true or false | unspecified | GAP (F-8, Medium) |
| `--unattended` token | SPEC:51 | Zero/Empty | flag absent | false | SA-1 keeps today's behavior | OK |
| wait split | SPEC:68 | One/Minimal | wait of 1 s | no split | implied | OK |
| wait split | SPEC:68 | Legitimate Edge Case | wait of 270 s | no split (under 5 min) | AC-4.3 says over 240 s fails | GAP (F-6, Medium) |
| wait split | SPEC:68 | Maximum/Overflow | wait over 5 min | split into at most 4 min | specified | OK |
| confidence threshold | SPEC:121 | Typical | 0.50 | blocked | specified | OK |
| confidence threshold | SPEC:121 | Sentinel Value Match | exactly 0.70 | "below 0.70" is false, proceeds | follows INV-B:199 wording | OK |
| depth fence | SPEC:33, 66 | Typical | depth 1 worker calls `worker-start` | refused | specified (WC-8) | OK |
| depth fence | SPEC:66 | Legitimate Edge Case | depth-1 worker calls `task-create` | unknown | UNVERIFIED, forbidden anyway | OK |
| circuit breaker | SPEC:263 | Maximum/Overflow | 4th consecutive `blocked` ending | not tripped (own report) | retry loop not bounded by the spec | GAP (note, Medium; coordinator-side, no wrong command outcome) |

Class left out: "One/Minimal" for the readiness, `--output` and depth guards, since a single unit does not change the branch. Hard-gate FR-10: table complete.

## Quantity Flow Diagram (Fowler, Whittaker)

```text
[Source: 43 command files (INV-A 21 + INV-B 22)]
   --> [Classify: INV verdicts] --> [10 ready | 27 needs-change | 6 coordinator-only]
         ready 10   --> P1: 6 (adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow)
                        P2: 4 (reflect, release-split, tdd, troubleshoot)
         needs 27   --> P1: 9 | P2: 11 | P3: 4 | P4: 3
         coordinator-only 6 --> no phase (section 4)
   P1 15 + P2 15 + P3 4 + P4 3 = 37 phased, + 6 excluded = 43   (conserved, no mismatch)
```

Count conservation holds (SPEC:76, 79-125, 130-137, 156-162). The only unchecked item is the source count itself (F-12).

## Verified citation spot-check results

- Matches: SPEC:26 (INV-A:76-83, 94-98; INV-B:289-299), SPEC:33-37 (CAPS lines), SPEC:43-45 (INV-B:323, CAPS:52,129,155,156,159-160,186,187), WC-1 to WC-12 CAPS cites, all 3.1 and 3.2 `INV-*` row cites, section 4 `INV-*` cites.
- Mismatch or overstatement: none found among checkable cites except N-3.
- UNVERIFIED: all source-tree, `EVIDENCE.md`, `CLAUDE.md`, `Makefile` and `pyproject.toml` cites, and SPEC:285.

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium: F-2, F-3, F-4, F-5, F-6, F-7, F-8, F-9, F-10, F-11, F-12, F-13, F-14.
Minor notes: N-1 to N-7.
The session that ran this review would ask the user once whether to open an issue for this list. No user is attached to this run, so the list is recorded only and no issue was created.

## Brief clauses overridden

None. The brief's values were used as given.

## Reviser brief

Blocking finding ids: F-1

Rules for the reviser (restated from the review loop, since the reviser reads this report and not the command):

- Revise only text that a blocking finding names.
- Add no rule, mechanism or section that a blocking finding does not call for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing text over adding.
- Report the byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone.
- Return the candidate once and do not award yourself a PASS.

For F-1 the text to repair is WC-4 (SPEC:62) and, if needed, the matching sentence in 2.3 (SPEC:73): the contract location for a file-valued `--output` must not collide across workers (WC-11, SPEC:69).

verdict: FAIL
