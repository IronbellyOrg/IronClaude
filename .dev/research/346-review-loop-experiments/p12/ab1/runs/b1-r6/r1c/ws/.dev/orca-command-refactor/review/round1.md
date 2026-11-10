review: 1 of 3

# /sc:spec-panel critique, first review (one of the three FIRST-REVIEW reviewers)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not given (first review); prior report: not given
- reviewer model: claude-sonnet-5-5
- mode: critique; focus: requirements, architecture; no `--unattended`
- loop note: the FIRST-REVIEW prompt asks for three independent first reviews and a coordinator MERGE (`~/.claude/rules/prompts/document_review_loop_prompts.md:35`). This report is one of the three. Finding ids F1..F3 are local; the coordinator renames them in the merge. Nothing here edits the candidate.

Citation aliases (line numbers are 1-based in the named file):
`SPEC` = the candidate. `INV-A` = `.dev/orca-command-refactor/inventory/commands-a.md`. `INV-B` = `.../commands-b.md`. `CAPS` = `.../orca-capabilities.md`. `CMD` = `/sc:spec-panel` definition `command.md` given to this reviewer.
Checkability: only the three inventory files and the candidate exist in the workspace. Every citation of `src/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `CLAUDE.md`, `pyproject.toml`, `Makefile` and Orca installed files is UNVERIFIED here; where a claim rests only on those, it is marked UNVERIFIED.

## Coverage
- Read in full: candidate (285 lines), README, all three inventories, the review-loop prompts file, `CMD`.
- Counts checked: 43 = 10 + 27 + 6 (SPEC:76 vs INV-A:73, INV-B:278: 5+5 ready, 13+14 needs-change, 3+3 coordinator-only). Section 3.2 rows 27, and their phases (9 P1 + 11 P2 + 4 P3 + 3 P4 = 27) agree with SPEC:159-162. Section 3.1 phases (4 in P1, 4 in P2, 2 none) agree with SPEC:159-160.
- Inventory line cites spot-checked and found as cited: INV-A:14, 62, 90, 95-98, 106, 113, 118, 120; INV-B:65, 105, 272, 285-286, 292, 299, 301, 320, 323; CAPS:44-45, 52, 58-61, 64, 72-80, 92, 97-103, 115-116, 129-130, 145-151, 155-161, 176-188.
- Not covered: the 11 load-bearing `src/` locations SPEC:11 says were re-read (UNVERIFIED here); the per-row `cmd/` and `sk/` lines of section 3 (UNVERIFIED, carried from the inventories); the Orca guide numbering.
- Pipeline Dimensional Analysis: not triggered. The candidate describes lifecycle phases, not a data pipeline whose stage counts diverge. Count conservation of the 43-command partition was checked above and holds.

## Verification block
(No verifier has run; the coordinator inserts one here after the VERIFY prompt.)

=== REQUIREMENTS ANALYSIS ===

### F1. BLOCKING (CRITICAL). `/sc:load` is required to carry a contract section by AC-1.1 and is also given no report
Experts: Wiegers (consistency, testability), Adzic (the acceptance test cannot be exampled).
Stated texts:
1. SPEC:195: "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". SPEC:76: "Every changed command also gains the `## Unattended mode` section". SPEC:159: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
2. SPEC:112: the `load` row is in section 3.2 with Report "none (see note)", Resume "n/a", Other change "use it as a step inside another worker's brief, not as its own Task".
3. SPEC:265 (Decisions): "a report file would be an unrequested addition".
Grading check: An implementer who follows the stated text as written builds a `load` that either (a) carries an `## Unattended mode` section naming `return-contract.yaml` (so AC-1.1 passes), which means `load` writes or promises a contract that SPEC:112 and SPEC:265 say it must not have, or (b) carries no such section as SPEC:112 and SPEC:265 say, and then AC-1.1 and AC-1.2 (SPEC:196: "7.2 live check on each P1 command", whose step 4 SPEC:183 requires a contract file) cannot pass. The acceptance criterion cannot pass with the row as written, and the two stated texts contradict.
Recommendation: remove `load` from the AC-1.1 and AC-1.2 populations (name the exclusion), or give it the contract; do not leave both.

### F2. BLOCKING (CRITICAL). AC-1.1 at Phase 1 requires contract sections whose content waits on decisions D2-D4, which the spec says Phase 1 does not need
Experts: Wiegers (traceability), Cockburn (who decides), Nygard (ordering).
Stated texts:
1. SPEC:154: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4." SPEC:162: Phase 4 = implement, post-release, pr-submit, "needs the user's decision first".
2. SPEC:195 (P1, AC-1.1): every command in sections 3.1-3.2 has the section; SPEC:159: P1 = "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". `implement` (SPEC:109), `post-release` (SPEC:113) and `pr-submit` (SPEC:114) are in section 3.2.
3. SPEC:52: each section "lists only its own gate resolutions and report file". Those resolutions for the three commands are "open decision D2", "(open decision D4)" and "per open decision D3" (SPEC:109, 113, 114).
4. SPEC:241 (D3, recommended (a)): "no pr-submit changes in Phase 4". SPEC:139: `/sc:pr-submit` "stays a worker candidate only if the user accepts open decision D3".
Grading check: An implementer who follows the stated text as written builds, in Phase 1, `## Unattended mode` sections for `implement`, `post-release` and `pr-submit`, to make AC-1.1 pass. Those sections must list gate resolutions that SPEC:109-114 and SPEC:154 make depend on answers not yet given, so the implementer either invents the answers (contradicting SPEC:154 and the D2-D4 text) or writes sections that advertise a worker mode the recommended D3(a) says does not exist. The same applies to the Phase 2 and Phase 3 commands: Phase 1 would accept `--unattended` on `/sc:task` (SPEC:121) while its gates (confidence below 0.70, TFEP) still prompt until Phase 2, which breaks the WC-2 promise (SPEC:60) and the claim that each phase "is independently useful" (SPEC:155). The acceptance criterion and the phase plan contradict.
Recommendation: scope AC-1.1 and the P1 flag rule to the commands whose phase is P1 (and add each later command's check to its own phase).

### F3. BLOCKING (CRITICAL). WC-4's contract path cannot be known before dispatch for workflow, research and file-valued `--output` commands
Experts: Wiegers (testability), Adzic (the 7.2 step has no path), Fowler (interface consistency).
Stated texts:
1. SPEC:62 (WC-4): "One report file, known before dispatch ... the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". It must be written "including stops before any other output exists". SPEC:73: the brief states "the output directory, so the report path is known before dispatch".
2. SPEC:92 (workflow, ready): brief passes `--handoff none` only; Report today `.dev/tasks/to-do/<id>/return-contract.yaml`; P1 fix "Write the contract for pre-creation STOPs too". `<id>` is generated by the command (INV-B:272: "Not written for pre-creation STOPs"); no directory is passed.
3. SPEC:90 (tdd): brief passes `--output <file>`; report is "the TDD at `--output`". SPEC:200 (AC-2.2) runs `/sc:tdd "auth" --unattended --output <file>` and expects "contract `status: blocked`". A file path is not a directory.
4. SPEC:116 (research): report "contract naming the generated `claudedocs/research_*.md` path"; no output flag, no directory.
5. SPEC:183 (7.2 step 4): `test -s <contract>` and the YAML check, on "the WC-4 contract path" named in SPEC:182 (step 3).
Grading check: An implementer who follows the stated text as written builds a coordinator brief and a 7.2 check for `workflow`, `research` and `tdd` in which `<output-dir>` is undefined: for workflow the directory is created by the command after the brief is sent; for research no directory exists; for tdd the passed value is a file. The coordinator then cannot compute the contract path before dispatch, WC-4's "known before dispatch" fails, and a pre-creation workflow STOP has no directory to hold the contract. Step 4 of the acceptance procedure and AC-1.4 (SPEC:198) cannot be evaluated.
Corroboration outside the workspace: `CMD:460` and `CMD:23` show the real spec-panel avoiding exactly this clash by adding a separate directory flag, `--report-dir`, because "`--output` is file-valued". That text also shows SPEC:120 ("add `--output`") and INV-B:43 (no `--output` exists) are stale against the current command definition.
Recommendation: define one coordinator-supplied directory argument for WC-4 (separate from file-valued `--output`) and say where workflow writes a pre-creation STOP contract.

=== ARCHITECTURE ANALYSIS ===

No further blocking finding. Notes below are Medium or minor and never fail the review.

Fowler: the split (one shared core file plus a short per-command section, SPEC:52) is sound and keeps the "no Orca calls in commands" rule checkable (SA-2, SPEC:147). The partition of 43 commands is consistent with both inventories.
Newman: the contract has no schema version, although the existing workflow contract is versioned ("contract 1.1", INV-B:272). WC-4 (SPEC:62) lists fields but no `contract_version`, so a later field addition cannot be detected by a coordinator (Medium, see FC-7).
Hohpe: the pull model (WC-12, SPEC:70; CAPS:66-67) and exactly-once `worker_done` (WC-5, SPEC:63) are correctly bounded by the Orca facts.
Nygard: failure paths are partly covered (WC-3 ask timeout, WC-6 retry, WC-10 liveness). Missing: behaviour when `~/.claude/WORKER-CONTRACT.md` is absent for a command whose section points to it (older install, plugin install; SPEC:279 admits the plugin mirror rule is unread) (Medium, FC-9).
Rejected-alternative argument (SPEC:29-39): R1-R5 hold against CAPS:97-103, 145-150. R1 correctly marks the enforcement call sites UNVERIFIED (CAPS:103).

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Findings use the FR-3 template. All are Medium (a requirement the text never states, or a reading needing an extra guess), so they sit under follow-up candidates.

- W1. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 and Decisions (SPEC:63, 263)** fails when **a command reports `status: partial` while having written none or one of its several artifacts**. Concrete attack: a `cleanup-audit` run with 12 batch reports planned writes 2 and hits a tool failure; it labels itself `partial` (WC-4 gives no definition of `partial`, SPEC:62); the worker sends `--outcome succeeded`; Orca settles the Task as completed (CAPS:77) and unblocks dependents (CAPS:90); the dependent `/sc:adversarial` worker reads 2 of 12 inputs. Before: Task dependents blocked. After: dependents ready.
- W2. I can break this specification by **Sequence Attack**. The invariant at **WC-3 and WC-4 (SPEC:61-62)** ("written on every outcome") fails when **the command's second run, started after a `blocked` contract and an `ask` answer, dies without writing**. Concrete attack: run 1 writes `status: blocked`; worker asks and gets an answer; run 2 is killed by context exhaustion before its write; the stale `blocked` file remains; WC-5 covers only "no report exists" (SPEC:63), so the stale file decides the outcome and the answered question is lost.
- W3. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-2/WC-4 (SPEC:60, 62)** fails when **`--unattended` is passed with no output directory or flag**. Concrete attack: `/sc:analyze src/x.py --unattended`; WC-4 says the contract goes to the passed directory, none was passed, and the command (SPEC:99) has no rule: it may write to the cwd (colliding with another worker, WC-11, SPEC:69) or refuse with no contract (violating "every outcome").
- W4. I can break this specification by **Divergence Attack**. The invariant at **WC-2 (SPEC:60)** (three resolutions only: default, caller flag, blocked) fails at **rows that say "refused under `--unattended`"** (SPEC:102, 103, 108, 110, 114, 123). Concrete attack: `/sc:test --watch --unattended`; "refused" is none of (a), (b), (c); the spec does not say whether a `blocked` contract is written, nor which Orca outcome follows.

=== GUARD CONDITION BOUNDARY TABLE ===
(Triggered: the candidate has guards, thresholds and sentinel comparisons. Nygard built it, Crispin checked completeness, Whittaker attacked entries. Classes left out are listed with a reason after the table.)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome map | SPEC:63 | Zero/Empty | no report file | no report -> failed | `--outcome failed` ("or no report exists") | OK |
| WC-5 outcome map | SPEC:63 | One/Minimal | `status: partial`, zero deliverables | partial -> succeeded | succeeded; no definition of `partial` (W1) | GAP (Medium: names no wrong outcome without an extra assumption about what a command labels partial) |
| WC-5 outcome map | SPEC:63 | Typical | `status: succeeded` | true | succeeded | OK |
| WC-5 outcome map | SPEC:63 | Sentinel Value Match | `status` outside the four-value set (existing vocabularies, SPEC:62 "keep their fields") | undefined | unspecified | GAP (Medium, FC-4) |
| WC-5 outcome map | SPEC:63 | Legitimate Edge Case | audit verdict FAIL with status succeeded | true | succeeded, body states verdict | OK |
| WC-2 unattended gate | SPEC:60 | Typical | gate with documented default | true | default applies | OK |
| WC-2 unattended gate | SPEC:60 | Legitimate Edge Case | "refused under `--unattended`" rows | n/a | unspecified (W4) | GAP (Medium) |
| WC-4 report location | SPEC:62 | Zero/Empty | `--unattended`, no output dir | unspecified | unspecified (W3) | GAP (Medium) |
| WC-4 report location | SPEC:62 | Legitimate Edge Case | generated id, file-valued `--output`, no flag | path unknown | contradiction, see F3 | GAP (BLOCKING, F3) |
| WC-10 wait split | SPEC:68 | Typical | poll iteration under 4 min | true | split into waits of at most 4 min | OK (poll runtime UNVERIFIED, SPEC:283) |
| WC-10 wait split | SPEC:68 | Maximum/Overflow | one Agent-tool call (subagent wave) over 5 min | true | unspecified: Agent-tool waits cannot be split (FC-2) | GAP (Medium) |
| Depth fence | SPEC:33, 66 | Typical | depth 1, worker calls `worker-start` | refused | `nested_worker_depth_exceeded`, WC-8 forbids | OK |
| Depth fence | SPEC:33, 252 | Legitimate Edge Case | depth raised (D5 b) | not refused | out of scope, recommended against | OK |
| ask timeout | SPEC:61 | Typical | `ask` times out | true | resume same message ID, no duplicate | OK |
| task confidence | SPEC:121 | Legitimate Edge Case | confidence below 0.70 | true | blocked | OK (exactly 0.70 is outside "below"; INV-B:199 uses "< 0.70") |
| Heartbeat | SPEC:68 | Zero/Empty | no tool call blocks over 5 min | false | no split needed | OK |

Classes left out, with reason: Maximum/Overflow for WC-5, WC-2, ask and depth (no count or capacity enters those guards); One/Minimal and Sentinel for the depth fence (the setting is a single integer with a stated default; Orca falls back to 1 on a malformed value, CAPS:100); Sentinel Match for WC-10 (no sentinel value).
FR-8 GAP rows: F3 is blocking (it names a wrong outcome); the others are Medium warnings (follow-up candidates). FR-9 blank behaviors: the two "unspecified" rows above, graded Medium. FR-10: every guard is enumerated and every input class has a row or a stated omission.

## follow-up candidates (Medium and minor; never fail the review, never in the Reviser brief)
- FC-1 (Medium; W1) define when a contract may say `partial`, and say a `partial` result does not unblock dependent Tasks, or map it to `failed` when any planned deliverable is missing (SPEC:62-63, 263).
- FC-2 (Medium) WC-10 requires splitting blocking calls into waits of at most 4 minutes (SPEC:68) but a command's own fan-out is an Agent-tool call the session cannot split (SPEC:24 E4); say how the worker heartbeats during a long subagent wave, or that it need not (heartbeat use in liveness is UNVERIFIED, CAPS:130, 182).
- FC-3 (Medium; W3, W4) define behaviour for `--unattended` with no output location, and define what "refused under `--unattended`" writes (SPEC:60, 62, 102, 103, 108, 110, 114, 123).
- FC-4 (Medium) WC-4 says commands with an existing contract "keep their fields" (SPEC:62) while the status set is fixed at four values (SPEC:262); the existing vocabularies of adversarial, brainstorm, reflect and workflow are never mapped (UNVERIFIED here; INV-B:272 shows workflow has `status` and `failed`).
- FC-5 (Medium) AC-C1 greps `src/superclaude/core` and requires no `orca (orchestration|worktree|terminal|agent)` match (SPEC:172), yet Phase 0 adds an Orca section to `HOW-WE-WORK.md` and a contract file in the same directory (SPEC:158), and SA-2 allows an Orca mention in the contract file (SPEC:147). Also the pattern is case-sensitive, so the `ORCA ...` placeholder of section 7.2 is not matched, and the `\|` escapes in the table cell must be unescaped to work in `grep -E`.
- FC-6 (Medium) Section 2.3 and 7.2 step 1 require the brief to contain `--unattended` (SPEC:73, 180), but the Phase 0 smoke commands (SPEC:194) omit it because the flag does not exist until Phase 1; state that AC-0.4 overrides 7.2 step 1.
- FC-7 (Medium; Newman) add a `contract_version` field to WC-4; workflow's contract already has one (INV-B:272).
- FC-8 (Medium) AC-C5 (SPEC:176) forbids removed lines in command files, but documenting `--unattended` or `--output` on an existing one-line Usage block edits that line; say whether flags go on a new line. The check `grep -E '^-[^-]'` also ignores removed lines that start with `--`.
- FC-9 (Medium; Nygard) say what a command does when `~/.claude/WORKER-CONTRACT.md` is missing (SPEC:52, 279).
- FC-10 (Medium) AC-C3 baselines only `tests/skills/` (SPEC:174), yet Phase 0 edits `src/superclaude/cli/install_core.py` (SPEC:52, 191); install and CLI tests live elsewhere (UNVERIFIED).
- FC-11 (Medium) section 3.2 `auggie-review` relies on an explicit `--post-pr` flag returning posting (SPEC:100); INV-A:38 names only `--no-post-pr` (UNVERIFIED that `--post-pr` exists); list it as a new flag if it does not. The `tasklist` row chooses to pass `--unattended` to reflect so a headless auto-accept applies (SPEC:122), while INV-B:46 recommended dropping `--remediate` and SPEC:280 item 9 assumes reflect is not headless; no Decisions row records the choice.
- FC-12 (minor) E3 (SPEC:23) cites `invocation_method: "skill-direct"` as support while section 1.4(1) (SPEC:43) says the same run proves only the nested route; the two readings of that evidence are not reconciled (the cited files are UNVERIFIED).
- FC-13 (minor) SPEC:51 calls unattended mode "the only command-side change ... besides report files and resume", but section 3.2 lists many others (explain Write tool, cli-portify resume flag, wait splitting, frontmatter fix). The Phase 1 title "commands with no gate" (SPEC:159) includes business-panel, explain, test and index, which have gate resolutions (SPEC:102, 108, 111, 123).
- FC-14 (minor) SPEC:11 states a self re-read of 11 `src/` locations and SPEC:285 an external validator pass of about 340 citations; neither can be checked here, and CAPS:161 cites the installed `pr-submit` skill at lines 47-49 while the spec cites the source copy at 37-39 (SPEC:65); the two copies may have drifted (UNVERIFIED).

The session that ran this review would ask the user once whether to open an issue for the follow-up candidates; this worker cannot ask, so it only records the list. No issue was created.

## Reviser brief
Blocking finding ids: F1, F2, F3. Rules (the reviser reads this report, not the command):
- Revise only text a blocking finding names: F1 (SPEC:76, 112, 159, 195, 196, 265), F2 (SPEC:154, 159, 195, 109, 113, 114, 139, 241), F3 (SPEC:62, 73, 90, 92, 116, 182, 183, 198, 200).
- Add no rule, mechanism or section that a blocking finding does not call for; cite the finding id on every added paragraph or table cell.
- Prefer deleting or narrowing text to adding; for example narrow AC-1.1 and the P1 flag rule to the P1 commands, and exclude `load` by name.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (the follow-up candidates) alone; do not award a PASS.
No brief clause was overridden.

verdict: FAIL
