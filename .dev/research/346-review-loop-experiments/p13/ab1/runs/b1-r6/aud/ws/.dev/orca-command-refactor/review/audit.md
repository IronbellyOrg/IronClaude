review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec, a first review of the full document
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (290 lines)
- candidate sha256: `e550dcb7fc3a3d867b7e5294799b7396379b1aa09607edb9890463612dc110e6`
- baseline: none given (first review, not a re-review)
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- coverage: the whole candidate was read (lines 1-290). Only `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` and `README.md` could be checked. About 35 `INV-A`, `INV-B`, `CAPS` and `README` citations were spot-checked and all matched (for example `CAPS:187-188`, `INV-A:14,95`, `INV-B:323`, `README.md:6,30`). The 10 / 27 / 6 split reconciles with the two inventories (5+14 B, 13 A needs-change, 3+3 coordinator-only; 43 commands). Every `src/superclaude/...`, `CLAUDE.md:N`, `Makefile`, `pyproject.toml`, `orca-data.json` and Orca-source citation is UNVERIFIED here, because those files are outside the sandbox. The "re-read 11 locations" (spec line 11) and the "340 citations re-read by evidence-validator" (spec UNVERIFIED item 14) claims are UNVERIFIED.
- panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, always active).
- FOCUS correctness is not active, so no State Variable Registry or Pipeline Flow Diagram is required. Pipeline Dimensional Analysis does not trigger: the stages (task-create, worker, report, dependents) never change counts, and the 43-command total is conserved across 21+22 and 10+27+6.

## Reviewer note on grading

Each blocking finding below carries the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." Findings that need a guess about which reading the implementer picks, or that report a requirement the document never states, are Medium and sit under `follow-up candidates`.

## === REQUIREMENTS ANALYSIS ===

### F1 - CRITICAL-equivalent BLOCKING (MAJOR label): P1 acceptance check and P1 scope contradict the phase table and the user-decision gate
- Experts: Wiegers (traceability), Cockburn (who owns what), Whittaker (Sequence Attack).
- Priority: High.
- Stated texts that contradict (spec lines):
  - Line 159 (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except load".
  - Line 200 (AC-1.1, pass condition of P1): the test asserts "every command in sections 3.1-3.2 except load has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - Lines 109, 113, 114 (section 3.2 rows) and line 162 (P4): implement, post-release and pr-submit belong to P4. Line 154 says "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4". Line 245 (D3 option a, the recommendation): "no pr-submit changes in Phase 4". Lines 124-125 and 118-119 place validate-roadmap, validate-tests, roadmap and save in P3. Line 162 says the coordinator "cannot predict their report path until they are fixed".
- Sentence: An implementer who follows the stated text as written adds a `## Unattended mode` section naming `return-contract.yaml` to pr-submit, implement, post-release, validate-roadmap, validate-tests and roadmap in Phase 1 so that AC-1.1 passes, and X is wrong because those sections need the gate resolutions that D2, D3 and D4 have not yet decided (and under the recommended D3(a) pr-submit is never changed), and for the P3 commands the report path the section would name is not defined until P3 reconciles command and skill (lines 118, 124).
- Whittaker, Sequence Attack: I can break this specification by **Sequence Attack**. The invariant at **section 6 / section 7.3 AC-1.1** (a phase leaves "later phases do not start until the earlier phase's checks pass", line 154) fails when **P1's check demands artifacts that the phase table assigns to P2-P4**. Concrete attack: before = 3 commands (implement, post-release, pr-submit) with no section and an undecided D2-D4; step 1 an implementer runs AC-1.1; step 2 the test fails for those 3 (and for roadmap, save, validate-roadmap, validate-tests); step 3 the implementer either invents gate text for them (pre-empting D2-D4) or weakens the test; after = P1 cannot pass without a user decision, which line 154 says it does not need.
- Recommendation (delete or narrow, do not add): restrict AC-1.1 and the P1 flag/section scope to the commands the section 3 table gives P1 (analyze, build, business-panel, design, document, explain, index, test, plus the section 3.1 commands whose P1 fix is listed), or state per phase which commands the test covers.

### F2 - BLOCKING (MAJOR label): `--unattended` is passed from P1 on but is a no-op for default-on outward actions until P2 or P4
- Experts: Nygard (safety boundary), Wiegers, Whittaker (Divergence Attack).
- Priority: High.
- Stated texts (spec lines): line 73 (section 2.3): the coordinator's brief states "the exact command line including every flag section 3 lists as required, plus `--unattended` from P1 on". Line 159: the P1 flag is "a no-op where a command has no gate". Line 67 (WC-9): "Under `--unattended`, any default that pushes, opens a PR, posts to GitHub ... is off." Line 100: the auggie-review off switch (`--unattended` implies `--no-post-pr`) is P2. Line 121: task's `commit`/`push` refusal is P2. Line 113-114: post-release and pr-submit outward actions are P4. Line 160 confirms "P2 only turns it off under `--unattended`".
- Sentence: An implementer who follows the stated text as written ships P1 (flag accepted by every command, the flag a no-op where the gate conversion is not yet done), and a coordinator following section 2.3 passes `--unattended` to `/sc:auggie-review` after P1, so the worker posts the review to the PR by default (`INV-A:98`, `cmd/auggie-review.md:51-54` via line 67), and X is wrong because WC-9 says `--unattended` turns that default off, a data-write to a shared GitHub PR the person never authorized.
- Whittaker, Divergence Attack: I can break this specification by **Divergence Attack**. The invariant at **WC-9 (line 67)** fails when **the run is between P1 and P2**. Concrete attack: state before = auggie-review accepts `--unattended`, still has `--post-pr` default on; the brief says `/sc:auggie-review 123 --unattended --output d/`; state after = review comment posted on PR 123, contract says succeeded, WC-9 is violated with no failing check (AC-2.4 only runs in P2).
- Recommendation (narrow): in P1 make the flag accepted only by commands that have no outward default or gate, and say in section 2.3 that `--unattended` is passed only to commands whose section 3 phase has shipped; or move the WC-9 off-switch of auggie-review and task into P1.

### F3 - BLOCKING (MAJOR label): the live-check script asserts `status` in the four-value set, but WC-4 gives some commands a separate `worker_status`
- Experts: Adzic (examples), Wiegers (testability), Whittaker (Sentinel Collision Attack).
- Priority: High.
- Stated texts (spec lines): line 62 (WC-4): a command whose existing `status` uses other values, "such as workflow's", writes the four-value field as `worker_status`, "which WC-5 and 7.2 read in place of `status` for it". Line 188 (7.2 step 4): the check is `assert d['status'] in {'succeeded','partial','failed','blocked'}`. Line 187 (step 3): outcome "matches the contract's `status` under WC-5". Line 199 (AC-0.4): workflow is a P0 smoke command run against "the command's existing report file", and `INV-B:272` (via line 92) records that workflow's existing contract already has a `status` key.
- Sentence: An implementer who follows the stated text as written runs step 4 on workflow's contract (in P0 against its existing file, in P1 against the added `worker_status`), and X is wrong because the script reads `d['status']`, which holds workflow's own vocabulary (the spec itself says it is not the four values), so the assertion fails even though the run is correct, and no stated text lets the check pass.
- Whittaker, Sentinel Collision Attack: I can break this specification by **Sentinel Collision Attack**. The invariant at **line 188** fails when **the contract's `status` key is a legitimate value from the command's own vocabulary**. Concrete attack: state before = workflow contract `status: <its own value>`, `worker_status: succeeded`; step = the 7.2 step 4 command runs; state after = `AssertionError`, P0 and P1 fail for workflow although WC-4 and WC-5 were followed.
- Recommendation (narrow): in 7.2 steps 3-4 read `d.get('worker_status', d['status'])`, naming the commands that use `worker_status`.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The core decision (Orca on top, commands as units, no Orca calls inside commands) is supported by the cited capability lines: depth 1 (`CAPS:97-99`), `worker_done` bound to the dispatched pane (`CAPS:76`, `CAPS:150`), no live preamble means no lifecycle messages (`CAPS:148`), report path is metadata only (`CAPS:79`). The Medium items below are architecture and requirement gaps.

## Guard Condition Boundary Table (Nygard builds, Crispin completes, Whittaker attacks)

Triggered: the spec has guards (flag detection, thresholds, status mapping). Classes left out: One/Minimal and Maximum where they cannot occur for the guard (stated per row group). Status GAP rows are graded by FR-8/FR-9: none names a concrete wrong outcome beyond F1-F3, so they are Medium (F4-F8).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` detected | WC-2, line 60 | Zero/Empty | flag absent | false | SA-1: today's behaviour (line 146) | OK |
| `--unattended` detected | WC-2, line 60 | Typical | standalone token | true | gates resolve (a)/(b)/(c) | OK |
| `--unattended` detected | WC-2, line 60 | Sentinel Value Match | `--unattended` inside quoted content | false | "counts only on the command line, not inside quoted content" | OK |
| `--unattended` detected | WC-2, line 60 | Legitimate Edge Case | `--unattended` plus `--interactive` | true | command stops `blocked` | OK |
| (One/Minimal and Maximum | left out | | | | a boolean flag has no minimal or maximum value) | |
| output location present | WC-4, line 62 | Zero/Empty | no output location, command takes output flag | false | writes nothing, chat reply, maps to `failed` | OK |
| output location present | WC-4, line 62 | Zero/Empty | `--output ""` (flag present, value empty) | unspecified | unspecified | GAP (F7) |
| output location present | WC-4, line 62 | Typical | fresh directory | true | contract written | OK |
| output location present | WC-4 / WC-6, lines 62, 64, 73 | Legitimate Edge Case | directory already holds a prior run's files, no resume flag | unspecified | the brief supplies a fresh dir, but no command-side rule if it does not | GAP (F7) |
| contract status mapping | WC-5, line 63 | Zero/Empty | no report | n/a | `failed` | OK |
| contract status mapping | WC-5, line 63 | Typical | `partial` | n/a | `succeeded`, body says partial | OK |
| contract status mapping | WC-5, line 63 | Sentinel Value Match | command's own `status` value (workflow) | n/a | `worker_status` in WC-4, but 7.2 step 4 reads `status` | GAP, blocking (F3) |
| contract status mapping | WC-5, line 63 | Legitimate Edge Case | unparseable or unknown `status` | n/a | `failed` | OK |
| wait size | WC-10, line 68 | Typical | 4 minutes | within 5 min heartbeat | allowed | OK |
| wait size | WC-10, line 68 | Maximum/Overflow | single call over 5 minutes | exceeds | must be split to at most 4 minutes; Agent-tool fan-out exempt | OK |
| (Zero/Empty, One/Minimal | left out | | | | a wait cannot be zero in a poll loop) | |
| task confidence | row `task`, line 121 | Typical | below 0.70 | true | blocked | OK |
| task confidence | row `task`, line 121 | Legitimate Edge Case | 0.70 to 0.89 band and exactly 0.70 | unspecified | unspecified (UNVERIFIED which prompt `cmd/task.md:93` fires there) | GAP (F8) |
| launch fallback | WC-1, line 59 | Typical | fallback at 30 s | within 60 s | passes (`EVIDENCE.md:45`, UNVERIFIED here) | OK |
| launch fallback | WC-1, line 59 | Legitimate Edge Case | fallback between 45 s and 60 s | false | stated to fail again (`EVIDENCE.md:56`) so the 30 s bound is chosen | OK |
| launch fallback | WC-1, line 59 | Sentinel Value Match | no fallback exists | n/a | no phase item or acceptance check owns this | GAP (F6) |
| nesting depth | WC-8, line 66 | Maximum/Overflow | depth 2 | refused | `nested_worker_depth_exceeded` (`CAPS:99`) | OK |

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium (warnings):
- F4 (MAJOR label, Medium): AC-C5 (line 176) requires `git diff -U0 ... | grep -E '^-[^-]'` to print nothing for every edited command file without a named defect fix, but P1 adds `--unattended` and `--output` flags, which SA-4 (line 149) calls additive. If the implementer extends the existing Usage line in place (the usual way, as `command.md` in this repo shows with its single Usage line carrying all flags), the old line appears as a `-` line and the check fails. Needs a guess that the line is edited in place rather than a new line added. Suggest: say Usage-line extension is allowed in AC-C5. Experts: Adzic, Crispin.
- F5 (Medium): `/sc:tasklist` row (line 122) makes Stage 10.5 pass `--unattended` to each reflect so the headless auto-accept applies, and reflect's own row (line 88) makes `--remediate` auto-accept under `--unattended`. The inventory (`INV-B:293-297` region, "Remove a nested fan-out or remediation offer") named removal of the offer, not auto-acceptance. Auto-accept starts a remediation handoff (reflect to workflow, which itself runs reflect) inside N subagents of the worker, and the row's claim "one layer below the worker, inside Claude Code's nesting limit" (`INV-A:14`: three layers) is not shown for the remediation chain. Needs a guess about the depth the chain reaches. Suggest: have tasklist pass `--no-reflect` or `--no-remediate` under `--unattended`, or state the depth. Experts: Fowler, Nygard.
- F6 (Medium, requirement never stated): WC-1 (launch fallback, owner "Launch setup, not commands"), the tool-permission pre-approval of WC-2 (line 60) and WC-12's `consumer_fenced` stop have no phase scope item (section 6, lines 158-162) and no acceptance check (sections 7.1-7.3). AC-2.2 runs only the no-answer path, so the `ask` path of WC-3 (answer relayed, re-invoke with the named flag) is also untested. A requirement without an owner or check is never confirmed. Experts: Wiegers (traceability), Crispin.
- F7 (Medium, FR-8/9 GAP): behaviour for `--output ""`, and for an output directory that already holds a prior run's files when the brief reuses it, is unstated; the protection rests only on the coordinator's brief (lines 73, 64). Suggest: one line that a non-empty, non-resume output directory resolves as blocked. Experts: Nygard, Whittaker (Zero/Empty Attack).
- F8 (Medium, FR-8/9 GAP): task's confidence band 0.70-0.89 and the exact value 0.70 have no stated gate resolution (line 121); UNVERIFIED which prompt the command fires there. Experts: Wiegers, Whittaker.
- F9 (Medium, requirement never stated): the spec says the brief carries "the exact command line" (line 73) and that the worker runs the command "directly" (WC-7, line 65), but never says how a worker session receives it as a command: the Orca preamble and Task block precede the brief text, so the message may not begin with `/sc:`, and the repo rule that a message starting `/sc:` must invoke the skill first (CLAUDE.md, project instructions) may not fire. `E3` (line 23) shows the earlier run used `invocation_method: "skill-direct"`. AC-0.4 will reveal this, but the invocation form (slash line first versus Skill tool call) is not specified. Experts: Cockburn, Fowler.

Minor notes:
- N1: `.dev/orca-command-refactor/README.md:31` ("No git commits, pushes, PRs or GitHub comments") is a rule for this run's workers. The spec cites it as evidence for the product rule WC-9 (line 67) and for `/sc:git` being coordinator-only (line 133); the support is real elsewhere (`cmd/git.md:14-17`, UNVERIFIED) but this line does not establish it.
- N2: section 3.1 intro (line 79) says the only command changes are small fixes, while four of its rows are P2 gate conversions (lines 88-91). The table is clear; the sentence is loose.
- N3: `CAPS:161` quotes the pr-submit top-level rule at installed `~/.claude/skills/...SKILL.md:47-49`, while the spec cites the source copy at `sk/sc-pr-submit-protocol/SKILL.md:37-39` (lines 11, 65). Different copies, so line numbers differ; UNVERIFIED which one is current.
- N4: `CAPS:178` (cited at spec UNVERIFIED item 3) was not checked by this audit; `CAPS:79` states the same point.

Open question for the person (the review loop asks once per loop whether to open an issue for the follow-up candidates): not asked, because this audit ran in a sandbox with no user session. The list is recorded only; no issue is created.

## Reviser brief

Blocking finding ids: F1, F2, F3.

Rules for the reviser (restated from the command's Review Loop bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names (F1: AC-1.1 and the P1 scope at lines 159 and 200; F2: section 2.3 line 73 and P1 flag scope at line 159, or the WC-9 off-switch phase; F3: 7.2 steps 3-4 at lines 187-188).
- Add no rule, mechanism or section that a blocking finding does not call for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the spec before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (F4-F9, N1-N4) alone.
- Do not award yourself a PASS; return the candidate once.
- Brief clauses overridden by this report: none.

verdict: FAIL
