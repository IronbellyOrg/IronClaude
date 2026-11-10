review: 1 of 3

# Gate review: orca-worker-contract-spec.md

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (sha256 `06cb4bcd39e29ea26abacd7521abf23c5e125f1cefda82fb1736f725a01d24b0`, 290 lines)
- baseline: none (no `--baseline`, no `--re-review`; first review of a complete document under the GATE prompt)
- prior report: none
- reviewer model: claude-haiku-5-5
- command: `/sc:spec-panel --mode critique --focus requirements,architecture`, reviewed under the GATE prompt of `document_review_loop_prompts.md`, using the grading check of the FIRST-REVIEW prompt
- sandbox note: only files inside the workspace were read. Any citation into a file outside the workspace (src/, tests/, `~/.claude/`, EVIDENCE.md, codegraph paths, CLAUDE.md, the Orca application) is marked UNVERIFIED.

## Coverage

What was covered:

- All 290 lines of the candidate, read in full (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:1-290`).
- The shared context `.dev/orca-command-refactor/README.md:1-39`, and the three inventories `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, read in full.
- Cross-section consistency: section 3 tables against the section 6 phase table; section 7 acceptance checks against sections 2, 3 and 5; section 5 against sections 2 and 3; the section 9 decisions against section 6.
- Line-level spot checks of the `INV-A:N`, `INV-B:N` and `CAPS:N` citations the spec uses (listed under "Citations checked" below). Not every citation was checked; checked citations are not claimed as a full audit.
- Focus areas: requirements (WC, SA and AC rules, testability) and architecture (layering of command, worker session and coordinator; phase ordering; installed-path design).

Not covered: any citation into a file outside the workspace (UNVERIFIED list at the end), and any live Orca behaviour.

## Grading used

For each finding, the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." is written first. A finding is blocking only when that sentence holds with no further assumption: two stated texts contradict each other, an acceptance criterion cannot pass as written, or a security, data-loss or safety boundary is at risk. Otherwise it is Medium (listed under follow-up candidates) or a minor note.

## Findings

### Blocking

**RA-01 (blocking; requirements; testability): AC-0.4 cannot pass in P0.**
- Location: `spec:199` (AC-0.4), `spec:187` (section 7.2 step 3), `spec:158` (P0 makes no command edits).
- Sentence: An implementer who runs AC-0.4 as written performs the P0 smoke runs and checks steps 1-3; step 3 requires that "its report path is the WC-4 contract path" and that its outcome "matches the contract's status" (`spec:187`). P0 creates no WC-4 contract, and AC-0.4 itself says "the contract arrives in P1" (`spec:199`; P1 at `spec:159`). Step 3 therefore fails on every P0 run, and the P0 gate cannot be passed.
- Direction for the reviser: let step 3 use the command's existing report path in P0, or write the P0 outcome check against the command's own status.

**RA-02 (blocking; requirements; testability): AC-1.2 applies the live worker check to `load`, which has no Task and no contract.**
- Location: `spec:201` (AC-1.2), `spec:112` (load row: "not as its own Task"; "none" contract), `spec:62` (WC-4: `load` writes no contract), `spec:200` (AC-1.1 excludes `load` from the contract name).
- Sentence: An implementer who runs AC-1.2 as written sends `load` through the section 7.2 live check. That check needs `task-create` and `worker-start` (`spec:185`), `test -s` on a contract (`spec:188`) and a `worker_done` report path equal to the WC-4 contract (`spec:187`). `load` is never its own Task and never writes a contract, so the P1 gate cannot pass for `load`.
- Direction for the reviser: exclude `load` from AC-1.2, or give it a separate check that does not need a Task or a contract.

**RA-03 (blocking; architecture and phasing): brainstorm is in section 3.1 but in no phase.**
- Location: `spec:84` (brainstorm row in 3.1; small fix "None"), `spec:76` ("Every changed command also gains the `## Unattended mode` section"), `spec:79` ("ready today"), `spec:159` (P1: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"), `spec:200` (AC-1.1 requires every 3.1-3.2 command to have the section). The phase rows at `spec:158-162` do not name brainstorm.
- Sentence: An implementer who executes P1 as written adds the flag and the section to the commands the phase table lists, leaves brainstorm untouched (its row says "None"), and then AC-1.1 fails because brainstorm has no `## Unattended mode` section. AC-1.2 and the `--unattended` requirement of P1 also cannot be met for brainstorm, since it does not accept the flag.
- Context: `inventory/commands-a.md:39` rates brainstorm ready with default flags. That verdict is consistent with brainstorm needing a flag and a section, so the gap is internal to the spec.
- Direction for the reviser: add brainstorm to a phase with the additive flag and section, or narrow AC-1.1 and P1 to exclude it with a reason.

**RA-04 (blocking; requirements): section 5 says standalone behaviour does not change, and SA-3 names a standalone change.**
- Location: `spec:142` ("must see exactly today's behaviour. This is a hard requirement on every phase."), `spec:148` (SA-3: "A standalone default run writes the same files it writes today, with one exception: the adversarial contract path that section 3.1 pins (F-04)"), `spec:83` (adversarial row), `spec:203` (AC-1.4).
- Sentence: An implementer who reads the `spec:142` requirement as written keeps the adversarial standalone output path unchanged, including the nested `adversarial/adversarial/` variant the spec calls a defect; AC-1.4 then fails, since it requires adversarial to name one fixed path. An implementer who follows SA-3 changes a standalone output path that `spec:142` says must not change.
- Evidence: `inventory/commands-a.md:35` and `:60-61` record two different contract paths written by real runs, one of them nested.
- Direction for the reviser: state in `spec:142` that SA-3 names the one allowed standalone change, or move the adversarial path fix into SA-4's named defect fixes with its own check.

### Medium (follow-up candidates)

**RA-05 (medium; architecture): the handoff from a blocked gate to an `ask` is not defined.**
- Location: `spec:60` (WC-2(c): write the contract as blocked and stop), `spec:61` (WC-3: the worker "may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag"), `spec:50-51` (worker run and unattended mode).
- The command cannot know it runs in a worker, since lifecycle messages belong to the preamble session only (`spec:50`). So the command always stops as blocked. The spec never says that the worker reads `blocked_question` from the contract, when it asks, or how the second invocation sits with the fresh-directory rule of WC-6 (`spec:64`). The same gate has two outcomes (stop, or ask) and no rule chooses between them.

**RA-06 (medium; requirements): WC-11 is violated by fixed defaults that section 3 keeps.**
- Location: `spec:69` (WC-11: default paths carry a timestamp or slug; "The coordinator never gives two workers the same output path"), `spec:85` (cleanup-audit: "output dir is fixed, so one audit per worktree at a time (WC-11)"), `spec:104` (cli-eval row: no output path handled).
- Evidence: `inventory/commands-a.md:42` (cleanup-audit writes to `.claude-audit/` with fixed pass summaries); `inventory/commands-a.md:44` (cli-eval create writes `.dev/eval-workspaces/cli-eval/design/`, run writes `.dev/eval-workspaces/cli-eval/runs/`).
- An implementer who starts two cleanup-audit or two cli-eval workers in one worktree gives them the same output path, which WC-11 forbids. The only mitigation is the unenforced "one at a time" note at `spec:85`. The uniqueness rule that `spec:69` attributes to "section 2.3" is not in section 2.3 (`spec:73`).

**RA-07 (medium; requirements): WC-4 has no default directory for cleanup-audit, and AC-1.1 requires a contract name for it.**
- Location: `spec:62` (default `<output-dir>/return-contract.yaml`), `spec:85` (no `--output` flag; fixed `.claude-audit/`), `spec:200` (AC-1.1: every 3.1-3.2 command except `load` names `return-contract.yaml`).
- Cleanup-audit has no `<output-dir>` in the spec's terms, and its row names no contract path. The contract location cannot be stated for this command, so AC-1.1 cannot be satisfied as the rule is written.

**RA-08 (medium; requirements): outward and safety flags are undefined or absent from the inventories.**
- WC-9 (`spec:67`) turns outward defaults on "only through the command's own explicit flag written in the brief". Task's `commit`/`push` gate (`spec:121`) and post-release's authorization (`spec:113`) name no flag, so the rule has nothing to test.
- auggie-review: `spec:100` says posting "returns only with an explicit `--post-pr` in the brief" and gives "Other required change: none". No inventory line names `--post-pr`; `inventory/commands-a.md:38` gives only `--no-post-pr` as the off switch. Either the flag exists (UNVERIFIED here) or the row omits a required change.
- cli-eval: `spec:104` requires "the safety flags in the brief" without naming them. `inventory/commands-a.md:44` also says "safety flags" without naming them.
- Each is Medium: the gate cannot be built from the text, but no wrong outcome is stated.

**RA-09 (medium; requirements): "ready today" conflicts with section 2.3.**
- `spec:73` says each brief states the exact command line "including `--unattended`". `spec:79` says section 3.1 commands run "now if the brief uses the stated flags", and the 3.1 flag column (`spec:81-92`) never lists `--unattended`. P0 (`spec:158`) runs three commands without it.
- An implementer who follows `spec:73` passes `--unattended` to `/sc:troubleshoot` or `/sc:workflow` before P1 adds the flag, and the run fails on an unknown flag. An implementer who follows `spec:79` omits it, which contradicts `spec:73`. The spec must say whether P0 runs are non-unattended.

**RA-10 (medium; architecture; evidence): the tasklist nested fan-out is stated as settled, but the inventory marks it UNVERIFIED.**
- `spec:122` says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`".
- `inventory/commands-a.md:14` is a depth statement drawn from a docs fetch, not from a file in the workspace. `inventory/commands-b.md:210` marks "whether nested spawning works" UNVERIFIED for the same fan-out, and `inventory/commands-b.md:314` lists it as UNVERIFIED item 1.
- The spec's UNVERIFIED list (`spec:277-290`) omits this item, so an UNVERIFIED item reads as verified.

**RA-11 (medium; evidence): two evidence rows state more than the cited sources support.**
- E4 (`spec:24`) says Agent-tool subagents "are not counted by Orca's nesting limit", citing `CAPS:155`. `inventory/orca-capabilities.md:155` says "UNVERIFIED that Orca never limits them". The depth code cited covers Orca dispatch only.
- E2 (`spec:22`) says a command run by a worker "has the same tools as a command a person runs". `inventory/orca-capabilities.md:161` establishes only a top-level Claude session with `--agent claude`. "Same tools" appears in no cited line.
- Section 1.1's decision that commands keep their own fan-out rests partly on E4. Section 1.4 gap 3 (`spec:45`) states the gap, but the table still reads as proven.

**RA-12 (medium; architecture): under `--unattended`, reflect changes the trigger of the headless rule and auto-accepts remediation with no authorization rule.**
- `spec:88` says that under `--unattended`, `--remediate` should "follow the existing headless auto-accept rule". `spec:151` (SA-6) says `--unattended` "reuses it and does not replace it".
- The existing rule keys on `claude --print` with no TTY (`inventory/commands-b.md:109`, citing `sk/sc-reflect-protocol/refs/remediation-handoff.md:239-242`, UNVERIFIED here). Making `--unattended` the trigger is a new trigger, not a reuse.
- The rule auto-accepts remediation "for auto-fixable registers and skips the gates" (`inventory/commands-b.md:109`). WC-9 (`spec:67`) covers outward actions only, so the spec does not say whether unattended auto-fix may edit code. `spec:285` (UNVERIFIED 9) already asks whether a worker counts as headless.

**RA-13 (medium; architecture): the installed contract is a hard dependency with no defined failure mode.**
- `spec:51-52` make `~/.claude/WORKER-CONTRACT.md` the one place for the shared rules (WC-2 to WC-12), and each changed command points to it. Commands run in other projects (`spec:34` cites `CLAUDE.md:74`, UNVERIFIED here).
- The spec does not say what a command or worker does when the file is missing or comes from an older install. The unattended path then has undefined behaviour exactly where it is needed.

**RA-14 (medium; requirements): index's knowledge-base mode. UNVERIFIED 6 says section 3 refuses or pins it, but the row does not.**
- `spec:282` (UNVERIFIED 6) says "section 3 refuses or pins them under `--unattended` regardless", naming index's knowledge-base mode.
- The index row (`spec:111`) only says to "state that knowledge-base mode does not wait (whether it does is UNVERIFIED)". Business-panel (`spec:102`) and explain (`spec:108`) are refused; index is not. An unattended index run can block on a wait nobody has verified.
- Evidence: `inventory/commands-a.md:54` and `:113` record the same uncertainty.

**RA-15 (medium; requirements): implement's implicit resume falls outside WC-6's two branches.**
- WC-6 (`spec:64`) says a command resumes "when given its resume flag, or, if it has none, writes each run into a fresh output directory". Implement has no flag. `spec:109` says its resume is "`--resume` (implicit when a ledger matches)"; `inventory/commands-a.md:51` confirms the implicit resume.
- A retry worker for implement therefore either reuses the halted ledger (`spec:109`) or starts fresh (`spec:64`). The spec does not choose. The consequence is confined to retry behaviour, so the finding is Medium.

**RA-16 (medium; requirements): several stated rules have no acceptance check.**
- WC-3 ask flow (`spec:61`): no check.
- WC-6 retry safety (`spec:64`): no check; no P-row runs `--retry-of`.
- WC-10 wait splitting for cli-eval (`spec:68`, `spec:104`): no check. AC-4.3 (`spec:215`) covers pr-submit only, and only if D3 is accepted (`spec:243-247`).
- WC-11 for index-repo and cleanup-audit (`spec:69`): the only parallel test is AC-3.4 for save (`spec:212`).
- WC-12 pull-based follow-ups (`spec:70`): no check.
- An implementer cannot tell from section 7 whether these rules hold.

**RA-17 (medium; requirements; safety boundary): the AC-C1 scan is case-sensitive and misses forms the spec itself uses.**
- `spec:180` runs `grep -rnE` without `-i` on the pattern `\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b`.
- The spec defines `ORCA` as the executable (`spec:167`) and writes its live checks as `ORCA orchestration ...` (`spec:185-187`). The guides use the same form (`inventory/orca-capabilities.md:63`, `:116`, `:137`). A command that calls `ORCA orchestration ask` passes AC-C1, which is the SA-2 and WC-8 boundary.
- The `orca-cli` executable (`inventory/orca-capabilities.md:19`, `:115`) is also missed by the pattern.
- The positive control (`spec:172`) uses only the lowercase fixture `orca orchestration task-create`.

**RA-18 (medium; traceability): finding ids F-01 to F-07 are cited but defined nowhere in the spec or the inventories.**
- Cited at `spec:61` (F-03), `spec:62` (F-01, F-02), `spec:69` (F-07), `spec:86-87` (F-05, F-07), `spec:92` (F-01), `spec:112` (F-02), `spec:148` (F-04), `spec:159` (F-05), `spec:172` and `spec:179` (F-06), `spec:200` (F-02).
- Their source is not in the workspace (UNVERIFIED). A reader cannot check the rules they gate.

### Minor notes

- N-01 (`spec:147`, SA-2): "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file" is ambiguous. A changed command cannot mention Orca "inside the contract file".
- N-02 (`spec:139` and `spec:273`): the spec calls `load` and `recommend` "coordinator-side helpers without changing their verdict", but `spec:112` and `spec:115` still give them worker changes. No wrong outcome, but the intent is unclear.
- N-03 (`spec:249-252`, D4 option (a)): the rule depends on the coordinator quoting the user's instruction faithfully, and no worker-side check exists. A safety reliance on coordinator fidelity; note only.
- N-04 (`spec:150`, SA-5; `spec:158`): P0 adds an Orca section to the routing guide that every standalone user installs. Not a command behaviour change, but visible in every install.

## Citations checked

Checked against the inventories in the workspace (line present and matching the claim):

- `inventory/commands-a.md`: 14, 35, 38, 39, 42, 44, 51, 54, 60-61, 97, 107, 113.
- `inventory/commands-b.md`: 109, 210, 314, 323.
- `inventory/orca-capabilities.md`: 19, 46, 52, 63, 73, 92, 115, 116, 137, 155, 161.
- Spec internal references checked: `spec:22`, `:24`, `:45`, `:50-52`, `:59-70`, `:73`, `:76`, `:79`, `:81-92`, `:100`, `:104`, `:109`, `:111-113`, `:121-122`, `:125`, `:142`, `:148-151`, `:158-162`, `:167`, `:172`, `:179-180`, `:185-188`, `:199-203`, `:212`, `:215`, `:243-252`, `:268`, `:273`, `:277-290`.
- `README.md:6`, `:11-17`, `:30-31`, `:35` are as the spec cites them.

Not checked (UNVERIFIED in this sandbox): every citation into `src/`, `tests/`, `plugins/`, `~/.claude/`, `CLAUDE.md`, `.dev/evals/`, `.dev/codegraph-migration/`, `.dev/research/`, `/opt/Orca/`, and every `[G]`, `[H:...]` and `CAPS` quote that depends on the Orca CLI output (the output itself is in `inventory/orca-capabilities.md`, which is checked only as a file).

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| Apply the FIRST-REVIEW grading check, since the GATE prompt routes to it | Grade by label; grade by the check | The GATE prompt says to use the check. Contradictions and unpassable acceptance checks are blocking under it. |
| RA-04 blocking | Blocking; Medium | The spec's own section 5 and SA-3 contradict each other, which the check counts as blocking. |
| RA-15 Medium | Blocking; Medium | The consequence is limited to retry behaviour, so no stated wrong outcome is blocking. |
| Sample the cross-file citations, not all | Check all; sample | Time budget. Only checked lines are claimed as verified. |
| Include minor notes | Omit; include | The notes help the next revision and do not affect the verdict. |

## Follow-up candidates

Medium and minor findings, for the session to ask the user about once (no issue is created without the user's answer, per bullet 3 of the Review Loop): RA-05 through RA-18, and N-01 through N-04.

## UNVERIFIED citations

1. Every citation into files outside the workspace (listed under "Citations checked").
2. The claim in `spec:122` that the reflect fan-out is inside the nesting limit (RA-10).
3. The existence of `--post-pr` (RA-08).
4. The headless trigger in `sk/sc-reflect-protocol/refs/remediation-handoff.md:239-242` (RA-12).
5. The identity of the finding ids F-01 to F-07 (RA-18).

## Reviser brief

Blocking ids: RA-01, RA-02, RA-03, RA-04.

Restating the Review Loop bullet 6 for the reviser: revise only text a blocking finding names; add no rule, mechanism or section that a blocking finding does not call for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief and must not be edited under it.

verdict: FAIL
