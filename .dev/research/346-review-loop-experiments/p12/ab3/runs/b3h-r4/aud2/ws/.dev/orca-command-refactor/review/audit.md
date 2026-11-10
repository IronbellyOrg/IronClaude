review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document first review)

## Header
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec; a first review, not a re-review. No `--re-review` and no `--baseline` were given, so `baseline: not applicable`.
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 60136 bytes), sha256 `2fadf1465791032cab449691f98fc1d6c0b5bd279da252336d54f84f58e6198f`
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full).
- panel (fixed order, focus requirements + architecture): Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker (adversarial, always active), Newman, Hohpe, Crispin, Gregory, Hightower. Experts with nothing to add are not quoted.
- mode notes: `--unattended` not passed, so the follow-up-issue question is not asked here (no interactive channel in this run); the coordinator should put the follow-up list to the user once. Improve step skipped (critique mode, first review, no revised spec written). `--focus correctness` not active, so no State Variable Registry. Pipeline Dimensional Analysis is not triggered (no multi-stage data flow whose item count changes; the 10 / 27 / 6 split is a partition, checked by sum below).

## Coverage (what was and was not checked)
Covered: all 285 lines of the candidate; `.dev/orca-command-refactor/README.md` (all 39 lines); the three inventories as the only checkable evidence.
- Checked against inventory text: about 70 `INV-A:N`, `INV-B:N` and `CAPS:N` citations from sections 1, 2, 3, 4 and 9 and the Decisions table, each opened and compared with the claim. All matched except where a finding below says otherwise. README citations `README.md:6,11-17,12,30,31` match.
- Arithmetic: section 3.1 has 10 rows, 3.2 has 27, section 4 has 6; 10 + 27 + 6 = 43 = 21 (`INV-A:3`) + 22 (`INV-B:3`). Phase assignments in section 3 rows agree with the section 6 command lists (P1 9 + 2 + fixes, P2 15, P3 4, P4 3).
- UNVERIFIED (cannot be opened inside the workspace, so every claim that rests only on them is unchecked): all `sk/`, `cmd/`, `ag/` path:line citations as primary sources (only their inventory quotation was read); `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:35-56`; `.dev/codegraph-migration/orchestration/README.md:31,33,42`; `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10`; `CLAUDE.md:16,50,72-83,157,334,408` (line numbers, not text); `src/superclaude/cli/install_core.py:4,13-24,33`; `pyproject.toml:38`; `Makefile:68-74`; `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254`; `src/superclaude/core/CLAUDE.md:65`; the Orca guides and compiled files quoted in the capabilities inventory (checked only as quoted there).
- Not covered: whether Orca behaves as the capabilities inventory quotes it; the correctness of any verdict that the inventories derived from files I could not open.

## === REQUIREMENTS ANALYSIS ===

### B1 [MAJOR, blocking] WC-4 puts the report in a directory, but tdd's output flag is a file (Wiegers, Adzic, Fowler)
Location: spec:62 (WC-4), spec:90 (tdd row), spec:87 (init-lite row and N-2), spec:200 (AC-2.2), spec:182-183 (7.2 steps 3-4).
Grading check: an implementer who follows the stated text as written builds a tdd worker that writes its contract to `<output-dir>/return-contract.yaml`, where WC-4 defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62) and the tdd row and AC-2.2 pass `--output <file>` (spec:90, spec:200). The only reading of that text is a directory at the TDD file's own path (for example `docs/auth/TDD_AUTH.md/return-contract.yaml`). That is wrong because the blocked or failed run leaves a directory where the TDD deliverable must be written, so a retry or a happy-path run on the same `--output` cannot create the file, and AC-2.2's own command (`/sc:tdd "auth" --unattended --output <file>`, spec:200) has no contract path for step 4 of the live check (spec:183, `test -s <contract>`) to open.
Why it holds with no guess: the inventory states the tdd `--output` is a file ("TDD file at `--output`", `INV-B:47`; "the final TDD at `--output` or `docs/[domain]/TDD_[COMPONENT-NAME].md`", `INV-B:222`), and the spec itself treats this case as a defect for init-lite: it adds `--output-dir` because `--output` is file-valued (spec:87, N-2). Nothing in the tdd row (spec:90) does the same.
Same gap, other rows (listed here so the reviser can narrow in one edit; each is graded under B1 only where the contract path is undefined, the rest are in M2): spec-panel "add `--output`" without saying file or directory (spec:120; `INV-B:177-185` (d) says no flag exists today), research "contract naming the generated `claudedocs/research_*.md` path" with no flag for the contract itself (spec:116; `INV-B:131`), index-repo and cleanup-audit, which fix their own output path (`INV-A:53`, `INV-A:42`) yet AC-1.2 (spec:196) passes `--unattended --output <dir>` to every P1 command.
Recommendation: for each command whose existing output flag is file-valued, fixed-path or absent, state in its section-3 row the single flag or fixed path that locates the contract, the way N-2 does for init-lite. Narrow: no new mechanism, one cell per row.
Priority: High. Quality impact: Testability 4 -> 8 for AC-2.2 and AC-1.2.

### M1 [MAJOR, Medium] "Fresh dir" retries share one directory with the first attempt (Wiegers, Nygard)
spec:64 (WC-6) says a command without a resume flag "writes each run into a fresh output directory so a re-run starts clean"; spec:62 and spec:73 (2.3) say the coordinator passes the output directory before dispatch and the contract goes in it. About 20 section-3 rows say only "fresh dir". A retry (`worker-start --task ... --retry-of`, `CAPS:116`) re-uses the Task, whose spec carries the same directory, unless the coordinator rewrites the brief, which section 2.3 does not require. The text allows two readings (the command makes a subdirectory, or the coordinator passes a new directory per attempt) and the first would move the contract off the path WC-4 says is known before dispatch. Medium, because the worse reading needs a guess. Recommendation: one sentence in 2.3 saying who makes the directory fresh on `--retry-of`.

### M2 [MAJOR, Medium] Contract location unnamed for implement, task, tasklist, review-translation, recommend, save (Wiegers)
spec:109 (implement: "beside the ledger", slug chosen by the command, `INV-A:51`), spec:121 (task: "contract on every tier"), spec:115 (recommend), spec:117 (review-translation), spec:122 (tasklist, `TASKLIST_ROOT` default `.dev/releases/current/<segment>/`, `INV-B:211`). For workflow and troubleshoot the spec reasons that a command-chosen directory is "not known before dispatch" and adds a flag (R-3, spec:62); the same reasoning is not applied to these rows. The worker can still report the path in `worker_done --report-path`, so no wrong outcome follows from the text as written; the requirement is simply unstated. Medium.

### M3 [MAJOR, Medium] Existing contracts keep their fields, but WC-5 rejects any status outside four values (Wiegers, Crispin)
spec:62 ("Commands that already write a contract keep their fields and add the missing ones") against spec:63 (a `status` outside the four values is `failed`) and spec:262 (fixed four-value set chosen). The inventories name the field (`status`, contract 1.1, `INV-B:272`) but not its values, and the Decisions row does not show that workflow, brainstorm, reflect or adversarial already use these four. If one uses another word (for example a plain "completed"), every successful run of that command is reported `failed`. UNVERIFIED: the existing value sets (`sk/sc-workflow-protocol/refs/return-contract.md:3-19` not readable here). Medium. Recommendation: one line per existing-contract command stating its mapping to the four values.

### M4 [MAJOR, Medium] auggie-review posting: the "explicit `--post-pr`" flag does not exist (Adzic, Cockburn)
spec:100 and spec:67 (WC-9) say posting "returns only with an explicit `--post-pr` in the brief" and that an outward default turns on "only through the command's own explicit flag". The inventory shows posting is on by default and the flag is the negative `--no-post-pr` (`INV-A:38`, `INV-A:78`). The row's "Other required change" is "none", so the new positive flag, and what `--unattended --post-pr` does with `--no-post-pr`, are unstated. AC-2.4 (spec:202) tests only the off case. Medium (a missing restriction, not a stated text that does harm).

### M5 [MAJOR, Medium] "No acceptance check" for several requirements (Crispin, Gregory)
WC-1 (launch setup, no phase and no check: spec:59, spec:156-162, spec:166-210), WC-6 resume or fresh re-run (no AC exercises a retry), WC-12 (`check` before `worker_done`, no AC), WC-10 for cli-eval (only pr-submit has AC-4.3, spec:210), WC-11 only for save (AC-3.4, spec:207). Under section 6 these requirements are owned by "launch setup" or by commands but never reach a phase gate. Medium. Recommendation: for each, either name the phase and check or say it is carried by the coordinator's brief and not checked.

### M6 [MINOR-to-MAJOR, Medium] `--unattended` is detected from free text (Whittaker, sentinel collision)
I can break this specification by Sentinel Collision. The invariant at spec:51 and spec:228 (D1(a): "explicit `--unattended` flag in the brief"; "cannot misfire on a person") fails when the sentinel appears inside user data: `/sc:tdd "document how --unattended works" --output f.md`, `/sc:research "the --unattended flag"`. Before: interactive run, gates on. After (if the command matches the token anywhere in its arguments): gates resolve as blocked or defaults, no person is asked, and the report is written as if a worker. The spec never says the token must be a standalone argument outside quoted content. Medium (an unstated edge case). Recommendation: one clause in WC-2 or 2.1.

### M7 [MINOR, Medium] `--unattended` is "accepted" in P1 for commands whose gates land in P2-P4 (Cockburn, Hightower)
spec:159 (P1: flag accepted by every 3.1 and 3.2 command except load) with spec:154 and spec:225 ("Phases 1-3 need no user decision; Phase 4 waits for D2-D4") and AC-1.1 (spec:195: every such command has the section "naming its report file"). For implement, post-release and pr-submit the report and gate rows are P4 and, for pr-submit under the recommended D3(a), never happen (spec:240, spec:139). A coordinator that follows 2.3 and passes `--unattended` to a P2-P4 command between phases gets a flag that promises no person but still prompts. The spec's own rule "later phases do not start until..." (spec:154) does not stop a coordinator dispatching early. Medium: needs a guess that a coordinator dispatches before the phase ends. Recommendation: say in 2.3 that a command is dispatched with `--unattended` only after its own phase passes.

## === ARCHITECTURE ANALYSIS ===

### M8 [MAJOR, Medium] Section 1.4(2) states an inference as fact and departs from the capabilities inventory (Fowler, Nygard)
spec:44 says a command's own `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`". The capabilities inventory records the opposite consequence: "An IronClaude command launched as a worker must not show any interactive question (for example `AskUserQuestion`, a session-name prompt) before its agent input is ready" (`CAPS:53`), and for Claude the task is passed on the command line (`CAPS:47`), so a command that opens with a gate runs from process start. README:13 states the same worry ("a supervised Claude worker that waits on a question fails Orca's 60-second readiness limit"). The spec narrows the evidence to a shell-wrapper prompt via `EVIDENCE.md:39` (UNVERIFIED here). The design still holds because `--unattended` removes the prompts, but the failure mode in 1.4(2), the "silent stall" reasoning in WC-2 (spec:60) and the AC-2.2 expectation that step 1 still reports `state: ready` (spec:180) all rest on it, and it is absent from the UNVERIFIED list (spec:271-285). Medium. Recommendation: add it to the UNVERIFIED list or cite the line that shows the order.

### M9 [MAJOR, Medium] tasklist row departs from the inventory without reasoning and asserts nesting safety (Fowler, Newman, Nygard)
spec:122: under `--unattended`, Stage 10.5 passes `--unattended` to each reflect; the nested fan-out is "one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". The inventory recommends calling reflect without `--remediate` and running the per-phase reflect "at the worker's top level, not inside subagents" (`INV-B:213` (g); `INV-B:296` row "Remove a nested fan-out or remediation offer that runs inside subagents"), and says nested spawning is UNVERIFIED (`INV-B:211` (b)). `INV-A:14` gives a three-layer allowance, and reflect Tier 2 adds reviewers and an adversarial merge below the tasklist subagent (`INV-B:107` (c)), so the claim "one layer" is not shown. Also the reflect row (spec:88) tells the brief to omit `--remediate`, while the tasklist path makes reflect run `--remediate` under the headless auto-accept (`INV-B:107` (a)). The Decisions row (spec:268) says inventory verdicts are kept and "nothing read in this task contradicted a verdict"; this is a changed remedy, not a verdict, and is unrecorded. Medium: the worse reading needs a guess about the layer count. Recommendation: record the departure in Decisions or follow `INV-B:213`.

### M10 [MINOR, Medium] AC-C1 and AC-C5 can fail on the spec's own deliverables (Crispin, Newman)
- AC-C1 (spec:172) must print nothing over `src/superclaude/core`, but P0 adds an Orca section to HOW-WE-WORK and a new WORKER-CONTRACT.md in that directory (spec:158, spec:150), and SA-2 (spec:147) permits an Orca mention "inside the contract file" while AC-C1's only exclusion is `skills/ccsession-tag/`. Whether the new text contains `orca orchestration` or `orca worktree` is not specified. Also the pipe characters inside the regex are written `\|` for the table, so copied as printed the group matches a literal pipe.
- AC-C5 (spec:176) requires that edited command files show no deleted line, while P1 adds `--unattended` to each command (spec:159) and a Usage line in a command file lists its flags on one line, so documenting a flag there deletes the old line. SA-4 (spec:149) exempts only named defect fixes. Whether the flag goes in the Usage line is not stated.
Both are Medium: each needs a guess about content the spec leaves open.

### M11 [MINOR, Medium] WC-11 is stated absolutely but only some fixed paths are handled (Nygard, Whittaker)
spec:69: "Two workers in one worktree must never write the same file." Fixed-path writers: index-repo `PROJECT_INDEX.md` (`INV-A:53`), init-lite default `.dev/superclaude/context-audit.md` (`INV-A:55`), cleanup-audit `.claude-audit/` (handled, spec:85). Attack by Accumulation / Divergence: two index-repo workers in one worktree (the default placement, `CAPS:115`) both rewrite the same file; the spec says "must never" and assigns no owner (command, coordinator brief). Medium. Recommendation: add the rule to the 2.3 coordinator list.

### M12 [MINOR, Medium] WC-10 trigger and AC-4.3 limit differ (Crispin)
spec:68 requires splitting only for a blocking call "longer than 5 minutes", into waits of at most 4; AC-4.3 (spec:210) requires "no single tool call exceeds 240 s". A 4.5-minute wait follows WC-10 and fails AC-4.3. The pr-submit row (spec:114) uses 4 minutes, so the 3.2 text is aligned with the AC; only the WC-10 trigger disagrees. Medium.

### M13 [MINOR, Medium] The quoted-words safeguard cannot be checked by the worker (Whittaker)
spec:61 (WC-3) and spec:245 (D4(a)): an `ask` answer supplies a flag value "only when it quotes the user's own words". The worker receives text from the coordinator and cannot tell a real quote from a fabricated one; the safeguard rests on the coordinator's honesty, which D2(b) names for the Ruling case (spec:235) but WC-3 and D4(a) do not. Medium. Recommendation: say so in one line.

### M14 [MINOR, Medium] Citation discrepancy for the pr-submit top-level rule (Gregory)
spec:65 and spec:11 cite `sk/sc-pr-submit-protocol/SKILL.md:37-39` for the top-level rule and say the worker re-read it as cited; spec:68 and spec:283 cite `:46-64` and `:46-48` for the poll loop and scripts; the capabilities inventory quotes the top-level rule at `:47-49` and `:82-84` (`CAPS:161`), from the installed copy under `~/.claude/skills/`. The repo copy and installed copy may differ, or one citation is wrong. UNVERIFIED either way.

### M15 [MINOR, Medium] E3 cites a field that reads as direct-route proof while 1.4(1) says the run proved only the nested route (Cockburn)
spec:23 cites `invocation_method: "skill-direct"` (also `INV-A:35`) as part of the evidence that the decision "has worked before", and spec:43 says the brief used an Agent-tool subagent, so the run "proves the nested route". The two are not reconciled (spec:23 vs spec:43). The gap is stated honestly in 1.4 and Phase 0 tests it, so no wrong outcome follows. UNVERIFIED: the yaml file.

## Minor notes (never fail the review)
- N1 Review-ids `R-1` to `R-5`, `N-1`, `N-2`, `SP`-style tags appear in the text (spec:61, spec:62, spec:63, spec:87, spec:182-183, spec:194-195, spec:234) with no definition in the document; a reader of the final spec cannot resolve them.
- N2 README:31 is cited as the policy source for WC-9 (spec:67); it is a rule for this planning run's workers, not a product requirement.
- N3 7.2 step 5 (spec:184) searches the transcript for the string `AskUserQuestion`; the command files and tool lists contain that word, so a plain search can fail a clean run. The pass condition says "no call", so the intent is clear.
- N4 AC-1.3 and AC-4.3 say "scratch worktree" and "scratch fork PR" (spec:197, spec:210) without saying how the worktree is created; the repo rule requires Orca creation with an agent (`CLAUDE.md`, UNVERIFIED line).
- N5 `E5` (spec:25) rests on a grep run on 2026-11-02 that cannot be repeated here (UNVERIFIED).

## Guard Condition Boundary Table
Guards found: G1 readiness limit (WC-1), G2 status mapping (WC-5), G3 `--unattended` switch (WC-2), G4 confidence gate (task row), G5 nesting depth (WC-8), G6 wait/heartbeat size (WC-10), G7 retry (WC-6), G8 parallel writes (WC-11). Classes left out are named in the line under the table. FR-8 / FR-9 grading follows the Review Loop: a GAP is blocking only with a concrete wrong outcome; otherwise Medium and listed above.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 readiness limit | spec:59 | Zero/Empty | `--timeout-ms` absent or 0 | default 60 s used | Orca default only (`CAPS:44`); spec silent | OK |
| G1 | spec:59 | Typical | fallback of 30 s | passes | "well inside the limit", 30 s example (EVIDENCE.md:45, UNVERIFIED) | OK |
| G1 | spec:59 | Maximum/Overflow | prompt fallback above about 45 s | fails | "above about 45 s it fails again" (UNVERIFIED); no number in the requirement | GAP (M5) |
| G2 status mapping | spec:63 | Zero/Empty | missing, empty or unparsable contract | `--outcome failed` | specified | OK |
| G2 | spec:63 | One/Minimal | `status: partial` | `succeeded` | specified | OK |
| G2 | spec:63 | Sentinel Value Match | `status` outside the four values | `failed` | specified; collides with existing contracts' own values | GAP (M3) |
| G2 | spec:63 | Legitimate Edge Case | audit with verdict FAIL | `succeeded` | specified | OK |
| G3 `--unattended` | spec:51, 228 | Zero/Empty | flag absent | today's behavior | SA-1 (spec:146) | OK |
| G3 | spec:51 | Sentinel Value Match | token inside quoted topic text | unspecified | not specified | GAP (M6) |
| G3 | spec:159 | Legitimate Edge Case | flag passed to a P2-P4 command before its phase | unspecified | not specified | GAP (M7) |
| G4 confidence gate (task) | spec:121 | Typical | 0.50 | blocked | specified | OK |
| G4 | spec:121 | Legitimate Edge Case | exactly 0.70 | no gate ("below 0.70") | follows the "below" wording; command text `< 0.70` (`INV-B:197`) | OK |
| G5 nesting depth | spec:66 | Typical | depth 0 coordinator | may start workers | `CAPS:97-101` | OK |
| G5 | spec:66 | Legitimate Edge Case | depth-1 worker calls `task-create` | unknown | forbidden by WC-8 regardless; Orca behavior UNVERIFIED | OK |
| G6 wait size | spec:68 | Typical | blocking call 3 min | no split | implied | OK |
| G6 | spec:68, 210 | Legitimate Edge Case | blocking call 4.5 min | WC-10 no split; AC-4.3 fails | conflict | GAP (M12) |
| G7 retry | spec:64 | One/Minimal | second attempt | fresh dir or resume flag | who makes the dir fresh unspecified | GAP (M1) |
| G8 parallel writes | spec:69 | Typical | two workers, distinct output dirs | no collision | specified | OK |
| G8 | spec:69, 85-86 | Legitimate Edge Case | two workers, fixed-path command | collision | owner unspecified | GAP (M11) |

Left out with reason: G1, G3, G5 have no Maximum row beyond what is shown (G3 and G5 are not numeric); G4 has no Zero/Empty row (confidence is always computed, never empty); G7 and G8 have no Sentinel row (no reserved value); G2 has no Maximum row (the value set is closed).

## Whittaker attack log (not blocking unless named above)
- Zero/Empty: empty contract and absent flag are specified (G2, G3 rows).
- Divergence: WC-4 directory against file-valued `--output` diverges at tdd (B1).
- Sentinel Collision: `--unattended` in user data (M6); `status` words (M3).
- Sequence: retry before the first attempt's report is read (M1); a P2 command dispatched before its phase (M7).
- Accumulation: two index-repo workers on one fixed file (M11); three failed starts trip Orca's breaker but a worker's own `failed` does not (`CAPS:80`), so a command that keeps failing is retried without limit by a coordinator that does not count (not a spec defect; noted).

## Follow-up candidates (Medium and minor; none triggers a revision)
M1 retry directory; M2 contract location for six commands; M3 existing status vocabularies; M4 auggie-review positive flag; M5 requirements without checks; M6 token in free text; M7 early `--unattended`; M8 readiness-order claim; M9 tasklist departure from inventory; M10 AC-C1 and AC-C5 against own deliverables; M11 WC-11 fixed paths; M12 WC-10 against AC-4.3; M13 unverifiable quote; M14 pr-submit line discrepancy; M15 E3 field; notes N1 to N5. The session that ran this review asks the user once whether to open an issue for these; no issue is created without the answer.

## Brief clauses overridden
None. The brief asked for a labelled whole-document first review and gave no clause that widens the scope or regrades a minor finding.

## Reviser brief
Repair only the blocking findings B1 in the candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS. (Revise only text a blocking finding names; each added paragraph or table cites its finding id; this is the report's Reviser contract, the reviser reads this report and not the command.)

verdict: FAIL
