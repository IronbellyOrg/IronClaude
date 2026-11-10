review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `363aad34a552033a79d2d651495b742507e757c6d9545270ee860f0bf999e142`
- baseline: not given (this is a first review of the whole document; `--re-review` and `--baseline` absent)
- command: `/sc:spec-panel --mode critique --focus requirements,architecture`; label: whole-document audit of the final spec
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full)
- evidence available: the README (`.dev/orca-command-refactor/README.md`) and the three files under `.dev/orca-command-refactor/inventory/`. The workspace contains no `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml` or `.dev/codegraph-migration/`, so every spec citation into those is UNVERIFIED here. Citations of the form `INV-A:N`, `INV-B:N`, `CAPS:N` were checked against the inventories and all that were sampled match (see Coverage).

Spec line numbers below are `spec:N`.

## Result in one paragraph

The spec's central decision (Orca coordinates, commands stay the units of work, a shared opt-in `--unattended` mode, a fixed report file, resume or safe re-run) is internally consistent with the inventories and the Orca facts. Counts are conserved end to end (43 commands = 10 ready + 27 needing change + 6 coordinator-only; the 27 map exactly onto the P1-P4 lists). No finding meets the blocking test in the FIRST-REVIEW grading check: none is two stated texts that contradict with no further assumption, a data-loss or safety-boundary text, or a text an acceptance criterion cannot pass. Eleven Medium findings and some notes are listed under follow-up candidates. Several of them are the first things an implementer will trip on (M1, M2, M3), so they are worth a pass before Phase 1 starts.

## Panel (critique mode, order per the command: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower)

Only experts with something to say on the two requested focus areas are listed. Newman, Hohpe, Gregory and Hightower had no finding beyond those attributed below.

=== REQUIREMENTS ANALYSIS ===

Findings are in the follow-up table (section "Findings"). Expert attribution:

- Wiegers (lead): M3 (WC-4 contract path undefined for file-valued `--output`), M5 (universal WC-4 versus the `init-lite`/`brainstorm` exemption), M6 (WC-5 has no row for a malformed or out-of-set `status`), N2 (undefined finding ids).
- Adzic: M9 (WC-10 threshold of 5 minutes versus AC-4.3's 240 s). Concrete Given/When/Then for M3: Given `/sc:tdd "auth component" --unattended --output docs/auth/TDD_AUTH.md`, When the command writes its contract at `<output-dir>/return-contract.yaml` with `<output-dir>` read as "the value of `--output`", Then the path is `docs/auth/TDD_AUTH.md/return-contract.yaml`, which cannot be created, so no contract exists on any outcome.
- Cockburn: the primary actor (an Orca coordinator session) and its goal (dispatch a command, read one file, decide) are clear in sections 1.1 and 2.3. The supporting actor "worker session" versus "command" split in the Owner column of WC-1..WC-12 is mostly clean; the exception is WC-6 (M2).

=== ARCHITECTURE ANALYSIS ===

- Fowler (lead): the boundary choice is sound and well supported: commands contain no Orca calls (R1-R5, `spec:29-39`), shared rules live in one core file (`spec:52`), per-command rows hold only deltas. Weak seams: the "Phase 1 adds the flag to every command" scope versus gate resolutions arriving in P2/P4 (M1), and the tasklist reflect-nesting claim (M7).
- Nygard: failure modes are mostly covered (silent stall, `consumer_fenced`, `ask` timeout, circuit breaker, runtime unavailable). Gaps: retry into the same output directory (M2), no row for a contract that cannot be written at all (M3, M10).
- Whittaker: attack results are in the next section and in M2, M6, M8, M9, M10.
- Newman: versioning of the new contract file is not stated (N3).

## Guard Condition Boundary Table (Nygard builds, Crispin checks completeness, Whittaker attacks)

Guards found: readiness limit, heartbeat/wait split, nesting depth, status vocabulary, `partial`/`blocked` outcome mapping, confidence threshold, `--monitor` ordinal, blocked-question, report existence. Classes that cannot occur are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit (60 s) | WC-1 `spec:59` | Typical | prompt falls back in 30 s | pass | worker-start passes (`EVIDENCE.md:45` via `CAPS:49`) | OK |
| readiness limit (60 s) | WC-1 `spec:59` | Maximum/Overflow | fallback above about 45 s | fail | stated: fails again (`spec:59`) | OK |
| readiness limit (60 s) | WC-1 `spec:59` | Zero/Empty | no fallback timeout | fail | covered by "must fall back on its own" | OK |
| wait split (>5 min split, <=4 min) | WC-10 `spec:68` | Typical | 3 min call | no split needed | allowed | OK |
| wait split (>5 min split, <=4 min) | WC-10 `spec:68` | Legitimate Edge Case | single call of 4.5 min | not >5 min, so no split | allowed by WC-10, but AC-4.3 `spec:210` fails any call over 240 s | GAP (M9) |
| wait split | WC-10 `spec:68` | Maximum | 3600 s eval (cli-eval) | split required | split into <=4 min waits (cli-eval row `spec:104`) | OK |
| nested depth (1) | `spec:33`, WC-8 `spec:66` | Typical | depth 1 | worker may not start workers | refused `nested_worker_depth_exceeded` (`CAPS:99`) | OK |
| nested depth (1) | D5 `spec:249-253` | Maximum/Overflow | depth raised to 2+ | allowed | D5(b) is rejected as a recommendation; WC-8 still forbids the command doing it | OK |
| nested depth (1) | `spec:33` | Zero/Empty | setting 0 or malformed | falls back to 1 | `CAPS:100`; spec does not need more | OK |
| status vocabulary | WC-4 `spec:62` | Typical | one of `succeeded/partial/failed/blocked` | valid | WC-5 maps it | OK |
| status vocabulary | WC-4/WC-5 `spec:62-63` | Zero/Empty | file present, `status` missing, empty, or outside the four values | undefined | only "no report exists" is mapped; malformed is not | GAP (M6) |
| outcome mapping | WC-5 `spec:63` | Legitimate Edge Case | `partial` | maps to `succeeded` | body's first sentence states `partial` | OK (see N4) |
| blocked_question | WC-4 `spec:62`, AC-2.2 `spec:200` | Zero/Empty | `status: blocked`, empty question | undefined in WC-4; AC-2.2 demands non-empty | WC-4 does not require non-empty | GAP (N5, minor) |
| contract location | WC-4 `spec:62` | Legitimate Edge Case | `--output` is a file (tdd, init-lite, spec-panel today) | undefined | `<output-dir>` read literally is a file | GAP (M3) |
| contract location | WC-4 `spec:62`, 3.1 workflow `spec:92` | Zero/Empty | stop before the package id exists | no `<id>` directory | row requires a contract for pre-creation STOPs but names no path | GAP (M4) |
| contract existence | WC-4 `spec:62`, 3.1 `spec:84,87`, F-02 `spec:76` | Sentinel (exemption) | `init-lite`, `brainstorm` get no `## Unattended mode` | undefined | WC-5 "no report exists" maps to `failed` | GAP (M5) |
| retry output dir | WC-6 `spec:64` vs WC-4 `spec:62` | Legitimate Edge Case | `worker-start --retry-of` reuses the Task brief | same dir | "fresh dir" owned by the command, path fixed by the brief | GAP (M2) |
| confidence threshold (0.70) | task row `spec:121` | Typical / below | <0.70 | blocked | stated | OK |
| confidence threshold (0.70) | task row `spec:121` | exactly 0.70 | 0.70 | not stated here; inventory says "<70%" (INV-B:199) | inferable (below means <) | OK |
| `--monitor` ordinal | pr-submit row `spec:114` | Typical | 1 | refused under `--unattended` | stated | OK |
| `--monitor` ordinal | pr-submit row `spec:114` | Zero/Empty | 0 and 2 | no statement | default is 3 (INV-B:89); 0 and 2 gates not read | GAP (N6, minor, UNVERIFIED) |
| `--unattended` token | WC-2 `spec:60`, D1 `spec:228` | Sentinel Value Match | the string `--unattended` inside a quoted prompt or topic | undefined | the spec does not say the flag must be a standalone token | GAP (N7, minor) |
| circuit breaker (3 failures) | WC-5 `spec:63`, decision `spec:263` | Maximum | third consecutive `blocked` mapped to `failed` | a worker's own failed report does not count (`CAPS:80`) | covered | OK |

Left out, with reason: confidence-threshold negative values (cannot occur, a score in 0-1); `--monitor` sentinel (no sentinel value in the ordinal).

FR-10: the table is complete (every guard has rows or a reason), so synthesis is not blocked. FR-8/FR-9 grading: every GAP above is Medium or minor, because none names a concrete wrong outcome that follows from the stated text without a guess; each needs the implementer to pick one of two readings or concerns a requirement the spec never states.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, Fowler leads, Whittaker attacks)

The spec has one counted pipeline: inventory verdicts -> section 3/4 -> phases. No mismatch found.

```text
[Commands in cmd/: 43 (INV-A:3 = 21, INV-B:3 = 22)]
   --> [Verdict split: ready 10 + needs-change 27 + coordinator-only 6 = 43]   (spec:76; INV-A:73 = 5/13/3, INV-B:278 = 5/14/3)
         |-- ready 10 (spec 3.1 rows) --> P1 fixes: adversarial, cleanup-audit, index-repo, workflow (4)
         |                                P2 gate edits: reflect, release-split, tdd, troubleshoot (4)
         |                                no edit: brainstorm, init-lite (2)             = 10
         |-- needs-change 27 (spec 3.2 rows) --> P1 9 + P2 11 + P3 4 + P4 3             = 27
         '-- coordinator-only 6 (spec 4)       --> no phase                              = 6
   P1 9: analyze build business-panel design document explain index test load
   P2 11: auggie-review cleanup improve cli-eval cli-portify recommend research review-translation spec-panel task tasklist
   P3 4: roadmap validate-roadmap validate-tests save
   P4 3: implement post-release pr-submit
[AC-1.1 consumers: 3.1 + 3.2 = 37 commands minus load, brainstorm, init-lite = 34 need a "## Unattended mode" section]
```

Check on the section 6 P2 list: it names 15 commands (11 needs-change plus the 4 ready commands that get gate edits), which matches the rows. Consumer count for AC-1.1 is 34, stated implicitly; no consumer assumes 37.

## Findings

All findings are Medium or minor. None is blocking.

### Medium (warnings; listed under follow-up candidates)

| id | Expert | Finding | Why it is Medium, not blocking | Evidence |
|---|---|---|---|---|
| M1 | Fowler, Nygard | Phase 1 puts `--unattended` into every command of 3.1 and 3.2 "a no-op where a command has no gate" (`spec:159`), and AC-1.1 (`spec:195`) requires the `## Unattended mode` section on 34 commands in P1. The gate resolutions of 15 gated commands arrive only in P2 and of 3 in P4 (`spec:160,162`). Between P1 and P2/P4, `/sc:task`, `/sc:cleanup`, `/sc:improve`, `/sc:cli-eval`, `/sc:roadmap`, `/sc:pr-submit` and others would accept `--unattended` and still prompt. Section 2.3 tells the coordinator to put `--unattended` in every brief (`spec:73`), and WC-2 says no person-blocking step under `--unattended` (`spec:60`). | The phase order is stated ("Later phases do not start until the earlier phase's checks pass", `spec:154`) and P2 checks gate behaviour; a wrong outcome needs a coordinator to dispatch a gated command in the gap. Also the spec never says a P1 flag on a gated command must refuse or warn. | `spec:60,73,154,159,160,162,195` |
| M2 | Nygard, Whittaker (Sequence) | WC-6 gives non-resumable commands "a fresh output directory so a re-run starts clean" and names the command as owner (`spec:64`). WC-4 makes the report path the directory the coordinator passed, known before dispatch (`spec:62,73`). A `worker-start --retry-of` reuses the Task (`CAPS:116`), so the same brief and the same directory. A command that picks its own fresh subdirectory breaks WC-4; a command that writes into the passed directory overwrites the first attempt, which is what WC-6 forbids. The rule works only if the coordinator passes a new directory per attempt, and 2.3 does not say so. Fixed-path commands (cleanup-audit `.claude-audit/`, adversarial `<output>/adversarial/`, workflow `.dev/tasks/to-do/<id>/`, validate-roadmap) have no stated fresh-dir mechanism either. | Two readings (coordinator-owned or command-owned) are allowed by the text; the worse one needs a guess. | `spec:62,64,73,85,92`; `CAPS:116` |
| M3 | Wiegers, Adzic | WC-4 defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)" (`spec:62`). Three commands have a file-valued `--output` today: `/sc:tdd` (`--output <file>`, `spec:90`; INV-B:222), `/sc:init-lite` (`--output <file>`, `spec:87`), and `/sc:spec-panel`, where the new `--output` is only "add `--output`" (`spec:120`). For tdd, AC-2.2's own example is `/sc:tdd "auth" --unattended --output <file>` (`spec:200`), and 7.2 step 3 requires the report path to equal "the contract path WC-4 gives" (`spec:182`). The spec states no contract path for a file-valued `--output`. The live `/sc:spec-panel` definition used for this audit already splits the two: `--report-dir` for the contract directory and `--output` as a file (`command.md:460-461`, outside the spec's evidence set), which shows the gap is real. | The document never states the rule for this case; a sensible implementer picks the parent directory or a separate dir flag. Medium per the grading check (requirement the document never states). | `spec:62,87,90,120,182,200`; INV-B:222 |
| M4 | Wiegers, Whittaker (Divergence) | 3.1 workflow: "Write the contract for pre-creation STOPs too (WC-4 'every outcome')" (`spec:92`), while the contract path is `.dev/tasks/to-do/<id>/return-contract.yaml` with `<id>` generated by the command (`spec:62`). A pre-creation stop has no package directory and no id (INV-B:272 records the contract is "Not written for pre-creation STOPs", `:39` of its ref). The spec names no fallback path, and F-03 says the worker "passes the path it finds" (`spec:62`), so a worker after a pre-creation stop finds nothing and WC-5 maps "no report exists" to `failed` with no blocked question. AC-1.4 only greps that the ref "states" the contract is written (`spec:198`). | The requirement is stated but its location is not; the fix is a one-line path. No unconditional wrong outcome without choosing a location. | `spec:62,92,198`; INV-B:272 |
| M5 | Wiegers | WC-4 says the command "writes `<output-dir>/return-contract.yaml`" in unattended mode and that commands with a contract "keep their fields and add the missing ones" (`spec:62`). Yet 3.1 lists `brainstorm` and `init-lite` as "None" for small fixes (`spec:84,87`) and section 3 intro and AC-1.1 exempt them from the `## Unattended mode` section (`spec:76,195`). `init-lite` today has no contract (INV-A:55), so its worker has no contract path to pass; WC-5 then maps it to `--outcome failed` ("no report exists", `spec:63`) although the audit succeeded. `brainstorm`'s existing contract may lack the required `command` field that 7.2 step 4 asserts (`spec:183`); its fields were not read (INV-A:39 only names the file). Neither command is in any live check list (`spec:194-196,200-201`). | The exemption is stated, but the failure needs the implementer to apply WC-5 to the exempt commands literally; the intent is probably that the existing file serves. Medium. | `spec:62,63,76,84,87,183,195`; INV-A:39,55 |
| M6 | Whittaker (Sentinel/Zero), Crispin | WC-5 maps `failed`/`blocked`/"no report" to `failed` and everything else, "including `partial`", to `succeeded` (`spec:63`). A report that exists but has a missing, empty or unknown `status`, or is not valid YAML, falls in "otherwise" and is reported `succeeded`. 7.2 step 4 asserts membership in the four values (`spec:183`) only in test, not as a worker rule. | A worker can only reach this through a command bug, and the fix is one clause. | `spec:63,183` |
| M7 | Fowler | tasklist row: "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`" (`spec:122`). INV-A:14 states only the platform rule (up to three layers below main, Agent tool withheld at the limit). The chain is worker (main) -> tasklist Stage 10.5 subagent -> reflect Tier 1 agents (`root-cause-analyst`, `confidence-calibrator`) or Tier 2 reviewers -> `sc:adversarial-protocol` generators and advocates (INV-B:111, INV-B:210). That is at least two layers below the worker and up to three, not one. INV-B:210,314 and INV-B:322 mark nested spawning as UNVERIFIED, which the spec row does not carry. The same row has `--unattended` make Stage 10.5 pass `--unattended` to reflect "so the headless rule applies" (`spec:122`), but the headless rule keys on `claude --print` without a TTY (spec UNVERIFIED 9, `spec:280`; INV-B:310) and only fires with `--remediate`, which Stage 10.5 always passes (INV-B:209). The effect is that reflect would auto-accept remediation for auto-fixable registers in each subagent. The spec's `/sc:reflect` P2 row proposes this reuse (`spec:88`) but the tasklist consequence (unrequested remediation handoffs per phase) is not discussed, and WC-9 does not cover it. | The depth claim is an unsupported statement, not a requirement that produces a wrong outcome by itself; the auto-accept consequence needs the headless rule's registers to be read. | `spec:88,122,280`; INV-A:14; INV-B:111,209,210,310,314,322 |
| M8 | Nygard | WC-3 lets any worker session, when a gate "would resolve as blocked", `ask` the coordinator once and re-invoke "with the answer as a flag" (`spec:61`). For `/sc:implement` the Ruling must come from the person, not another agent (`spec:233`, INV-A:66), and D2(a) says keep the rule (`spec:234`). WC-3 has no carve-out. The command still rejects a coordinator-relayed Ruling by its own rule, so the safety holds in the command; but a worker following WC-3 will `ask`, receive an agent answer and re-invoke, wasting a cycle, or if the command is later weakened the rule silently moves. | Safety boundary is preserved by the command text; the issue is a missing cross-reference. | `spec:61,233,234`; INV-A:66 |
| M9 | Adzic, Crispin | WC-10 requires splitting a "single tool call for longer than 5 minutes" into waits "of at most 4 minutes" (`spec:68`); the decision row justifies 4 minutes as the margin under the 5-minute heartbeat (`spec:266`). AC-4.3 then fails any single call over 240 s (`spec:210`). A call of 4 to 5 minutes passes WC-10 and fails AC-4.3. Applies only if D3(b) is chosen. | Narrow (one acceptance check, one optional decision). Align the sentence to "longer than 4 minutes". | `spec:68,210,266` |
| M10 | Nygard, Whittaker (Accumulation) | WC-4 requires a contract "on every outcome, including stops before any other output exists" (`spec:62`), and the unattended refusal case in the live command is "printed in chat only" when no report dir is known (`command.md:460`, outside the spec's evidence). The spec has no rule for the case where the output directory cannot be created or written, or is missing from the brief. 2.3 makes the coordinator responsible for passing it (`spec:73`) but WC-2 offers only default, flag or blocked, and "blocked" needs a writable place for the contract. | Not stated by the document; likely resolved in the shared contract file at implementation. | `spec:62,73,60` |
| M11 | Wiegers, Fowler | SA-2 permits Orca to be mentioned in the contract file as "an example of a caller's question channel" (`spec:147`), and P0 adds an Orca section to `HOW-WE-WORK.md` (`spec:158`) and a brief template. AC-C1's grep covers `src/superclaude/core` and matches `orca orchestration`, `orca worktree`, `orca-ide terminal` etc., with the pass condition "prints nothing" and only `ccsession-tag` excluded (`spec:172`), and it applies to every phase including P0 (`spec:169`). A contract or routing-guide paragraph that writes the actual command (`orca orchestration ask`, `orca-ide orchestration worker-start`) satisfies SA-2 and fails AC-C1. Writing "Orca's ask command" satisfies both. | Two readings; the compliant one exists, so the implementer's choice, not the text, causes the failure. | `spec:147,158,169,172` |

### Minor notes

| id | Note | Evidence |
|---|---|---|
| N1 | AC-C5 (`spec:176`) says edits without a named defect fix must be pure additions (`^-[^-]` prints nothing). A new flag shown on an existing Usage line, or an `argument-hint`/tools frontmatter line, is a changed line. SA-4 calls new flags additive (`spec:149`). Add "as new lines" or exempt the Usage line. | `spec:149,176` |
| N2 | Finding ids F-01, F-02, F-03 are cited as authorities in the spec (`spec:52,62,76,194,195,196,198`) but defined nowhere in the candidate or the README. They presumably come from `review/disposition.md`, which this audit was not given. A reader of the spec alone cannot resolve them. | `spec:52,62,76,194-198`; README table `.dev/orca-command-refactor/README.md:19-27` |
| N3 | The shared contract file and `return-contract.yaml` have no version field or compatibility note, although other contracts the spec reuses carry a version (workflow "contract 1.1", INV-B:272). A later field addition has no negotiation rule. | `spec:62`; INV-B:272 |
| N4 | `partial` maps to `succeeded` (`spec:63,263`). A coordinator that branches only on Orca's `--outcome` will treat `partial` as complete; the spec relies on the first body sentence and says the coordinator "opens the report file" (`spec:62,73`). Consider stating the coordinator must read `status` before releasing the worker. | `spec:62,63,73,263` |
| N5 | WC-4 does not say `blocked_question` is non-empty when blocked, but AC-2.2 asserts it (`spec:200`). | `spec:62,200` |
| N6 | The pr-submit row refuses `--monitor 1` only (`spec:114`); other ordinals' gates are not stated. UNVERIFIED (not in the inventories beyond INV-B:89). | `spec:114`; INV-B:89 |
| N7 | The spec does not say `--unattended` is recognised only as a standalone argument token. A topic string such as `/sc:tdd "how --unattended works"` is a possible false trigger. (The live spec-panel definition handles this, `command.md:459`, outside the evidence set.) | `spec:60,228` |
| N8 | Section 1.1 says what changes in commands "is limited to the worker contract in section 2" (`spec:16`), but section 3 also requires interface-drift fixes, a tools change, a frontmatter move, a usage-line fix and a new `--resume` flag (`spec:102,105,108,112,118,124,125`). SA-4 lists them (`spec:149`). Edit 1.1 to point at SA-4. | `spec:16,149` |
| N9 | 7.2 steps 2 and 3 are written as sequential, with "worker-show at least once per 5 minutes" (`spec:181`) while `check --wait` can block 15 minutes (`spec:182`). A single coordinator cannot do both unless it polls in the wait loop. | `spec:181,182` |
| N10 | The scope statement "The 43 commands in `cmd/`" (`spec:76`) rests on the two inventory scopes (INV-A:3, INV-B:3). The skill list shown to this session also lists `sc:graph`, `sc:impact` and `sc:issue`, none of which appears in either inventory or in the spec. UNVERIFIED here (no `src/` in the workspace). `sc:issue` creates Orca worktrees and launches agents, so it is relevant to the "Orca on top" decision. If these exist as commands in `cmd/`, the 43 count and the 10/27/6 split are short by three. | `spec:76`; INV-A:3; INV-B:3 |

## Follow-up candidates (Medium and minor, for the user's decision; none is blocking)

M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, and notes N1-N10. The session that ran this review would ask the user once whether to open an issue for these; no issue was created and no answer was available in this sandbox.

## Coverage

- Read in full: command.md, README, the review-loop prompts file, the spec (all 285 lines), `orca-capabilities.md` (188 lines), `commands-a.md` (120 lines), `commands-b.md` (323 lines).
- Cross-checked against the inventories (all matched, 0 mismatches): every `INV-A:N` and `INV-B:N` row citation in the section 3 and section 4 tables (43 command rows), the counts (`spec:76` against INV-A:73 and INV-B:278), the `CAPS:N` citations in E1-E6, R1-R5, WC-1..WC-12, 1.4, D1, D5 and the UNVERIFIED list, and the phase membership of all 27 needs-change commands.
- UNVERIFIED (outside the workspace, not checked): every `cmd/…`, `sk/…`, `src/…`, `CLAUDE.md:…`, `Makefile`, `pyproject.toml:38`, `.dev/codegraph-migration/…` and `EVIDENCE.md` citation in the spec; the claim that 11 locations were re-read (`spec:11`); the E5 grep results; the "about 340 citations checked" claim (`spec:285`). Where an inventory repeats the same fact with the same citation, the inventory line was used as the only available evidence.
- Not covered: behaviour of any command (no command was run); Orca output (no Orca in the sandbox); `review/disposition.md` (not provided, which is why F-01..F-03 stay unresolved, N2).
- Brief clauses overridden: none. The brief asked for no number of findings and no grading beyond the command's rules; none was applied.

## Reviser brief

No blocking finding is open; there are no ids to list and no revision is called for by this review. Medium findings and notes never trigger a revision, never fail a review and are not part of a Reviser brief.

verdict: PASS
