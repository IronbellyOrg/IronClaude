review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (critique mode, focus requirements,architecture)

- Run label: whole-document audit of the final spec, a first review of the full document (not a re-review; no `--re-review` and no `--baseline` was given, so the Step 1 evidence block does not apply).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 59060 bytes)
- Candidate sha256: `87c84d9ca9169f943376688b64d421baec2513be9fe5034504496a4473d86140`
- Baseline sha256: none given
- Reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- Input read first: `.dev/orca-command-refactor/README.md` (binding context), `command.md` (/sc:spec-panel), `~/.claude/rules/prompts/document_review_loop_prompts.md` (FIRST-REVIEW prompt, followed).
- Citation convention in this report: `S:N` = line N of the candidate spec. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Any `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/` or Orca-source path:line is UNVERIFIED here because those files are not in the workspace; I checked only the inventory lines.

## Coverage statement

Covered: all 285 lines of the spec. Every `INV-A:`, `INV-B:` and `CAPS:` citation in sections 1, 2, 4, 8 and the Decisions table was spot-checked against the inventory files (about 60 distinct lines read). All were found and support the claim, except where a finding below says otherwise. Also checked: the 43 = 10 + 27 + 6 count (INV-A:3 lists 21 commands, INV-B:3 lists 22; the spec's 10 ready rows, 27 needs-change rows and 6 coordinator-only rows all match, and the split per inventory is 5+13+3 and 5+14+3). Count conservation holds.
Not covered (UNVERIFIED): the 11 "re-read" source locations (S:11), the ~340-citation validator claim (S:285), every `sk/` and `cmd/` line, `CLAUDE.md:*`, `EVIDENCE.md:*`, the PR #329 README lines and Orca source lines. Their claims are carried as the inventories' claims only. Grading uses only text and inventory lines inside the workspace.
Not run: no command could be run against live Orca (none exists in the sandbox). The Pipeline Dimensional Analysis heuristic is not triggered (the spec has no multi-stage data pipeline whose output count diverges from input; the only count flow is the 43 -> 10/27/6 split, which conserves).

Fixed focus: `requirements`, `architecture`. Experts used in review order: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture). Crispin, Gregory and Hightower are not in the selected focus panels and were not used. `--focus correctness` was not requested, so no State Variable Registry is produced.

## Guard Condition Boundary Table

Guards in the spec (thresholds, status switches, path rules, mode switches). One row per input class that applies; classes that cannot occur are left out with a one-line reason below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome map (P1+) | S:63 | Zero/Empty | contract file 0 bytes | file invalid | `--outcome failed` (B-5 default) | OK |
| WC-5 outcome map | S:63 | Sentinel Value Match | `status: blocked` with empty `blocked_question` | `failed` | `failed` is sent, but WC-2 (c) S:60 requires "the exact question"; no rule for an empty question | GAP |
| WC-5 outcome map | S:63 | Legitimate Edge Case | command's existing contract uses its own `status` words (workflow, brainstorm, reflect, adversarial contracts, S:62, S:261) | not one of the four values | maps to `failed` by the B-5 default, though the run succeeded; the spec never says the existing vocabularies were checked | GAP |
| WC-4 path rule | S:62 | Zero/Empty | no `--output`/`--output-dir` argument exists or is passed | neither directory nor file branch | unspecified; rows research, save, cleanup-audit, index-repo, review-translation, post-release have no output argument (S:85,86,116,117,119) | GAP |
| WC-4 path rule | S:62 | Typical | `--output <dir>` | directory branch | `<dir>/return-contract.yaml` | OK |
| WC-4 path rule | S:62, S:69 | Maximum/Overflow | two workers, `--output <file>` in the same directory | file branch, same name | both write `<dir>/<command>-return-contract.yaml`; WC-11 forbids two workers writing one file, WC-4 produces it | GAP |
| WC-10 wait split | S:68 | Legitimate Edge Case | one blocking call of 4.5 minutes | "longer than 5 minutes" is false | not split, but the AC S:210 demands no call over 240 s | GAP |
| WC-10 wait split (pr-submit) | S:68, S:114 | Maximum/Overflow | `--poll-interval` larger than 240 s (the sleep is "at least" poll-interval) | iteration over 4 minutes | no bound on the flag value; only "confirm" S:114 | GAP |
| WC-2 gate (c) / WC-3 `ask` | S:60-61 | One/Minimal | one gate blocks, answer arrives | re-invoke with answer as a flag | OK for a command with one gate | OK |
| WC-3 `ask` once | S:61 | Maximum/Overflow | command with several gates (cli-portify three, S:105; task two, S:121; review-translation two, S:117) | second gate blocks after re-invoke | "ask the coordinator once" is not defined as once per run or once per gate | GAP |
| WC-6 safe re-run | S:64 | Legitimate Edge Case | `--retry-of` after attempt 1 already edited source files (cleanup, improve, task, document inline) | "fresh output directory" | covers output only; edits in the worktree from attempt 1 are not addressed | GAP |
| `--unattended` switch | S:51, D1 S:228 | Sentinel Value Match | the literal text `--unattended` inside a quoted prompt or topic argument (`/sc:research "..."`, `/sc:tdd "..."`) | switch on or off? | token parsing rule not stated; D1 (a) claims it "cannot misfire on a person" | GAP |
| WC-9 outward default | S:67 | Typical | `--unattended` without an authorizing flag | outward action off | OK as a rule; see F-1 for phase timing | OK |
| WC-12 `check` | S:70 | Typical | `consumer_fenced` returned | stop, no `worker_done` | OK | OK |
| AC-C5 / AC-0.3 additive check | S:176, S:193 | Sentinel Value Match | removed line that starts with `- ` (a markdown bullet) or `---` (frontmatter fence) | diff line starts `--` or `---` | regex `^-[^-]` does not match it, so the check "prints nothing" | GAP |
| AC-2.4 post-count | S:202 | Maximum/Overflow | PR with 30 or more reviews or comments | `gh api ... --jq length` | no `--paginate`; first page caps at 30 | GAP |

Classes left out: Zero/Empty for WC-10 (a zero-length wait never blocks), Maximum/Overflow for WC-12 and WC-9 (boolean guards), One/Minimal for the path rule (no size dimension).

---

=== REQUIREMENTS ANALYSIS ===

### F-1 (blocking) `--unattended` ships before the gate and outward-action rules that make it safe

- Severity: MAJOR, graded blocking by the Grading check. Experts: Wiegers (consistency), Whittaker (Sequence Attack), Cockburn (who is the actor after P1).
- Location: S:67 (WC-9), S:60 (WC-2), S:154 and S:159-162 (phases), S:195 (AC-1.1), S:240 (D3 a).
- Grading sentence: An implementer who follows the stated text as written builds `--unattended` accepted by every command in sections 3.1 and 3.2 in Phase 1 (S:159), with auggie-review, cleanup, improve, task, pr-submit and post-release gate and outward-action resolutions deferred to P2 (S:160) and P4 (S:162); that build is wrong because WC-9 says that under `--unattended` a default that posts, pushes or opens a PR "is off" (S:67) and WC-2 says no person-blocking step remains (S:60), yet after P1 `/sc:auggie-review <PR> --unattended` still posts to the PR by default (INV-A:78, quoting `cmd/auggie-review.md:51-54`, UNVERIFIED line) and ends its turn on the chat offer (INV-A:62). Each phase must be "independently useful" and leave a usable state (S:154), and P1's own checks (AC-1.2, S:196) run live checks only on P1 commands, so the gap is not caught. This is a safety-boundary risk (a GitHub post).
- Concrete attack (Whittaker, Sequence Attack): I can break this specification by running its steps out of order within its own plan. The invariant at S:67 (WC-9) fails when the flag exists but the gate rows are not yet built. State trace: before P1, `--unattended` is unknown; after P1 (all P1 checks green), the flag is accepted on auggie-review, whose posting default is unchanged; a coordinator, trusting WC-9, dispatches it with `--unattended`; the worker posts a review to the PR and stalls on the remediation offer.
- Second text that contradicts: AC-1.1 (S:195) requires a `## Unattended mode` section on every command in 3.1-3.2, which includes pr-submit, while D3 recommends (a) "no pr-submit changes in Phase 4" (S:240) and S:139 says pr-submit stays a worker candidate only if D3 is accepted.
- Recommendation: limit P1's flag and section to the commands whose gate and outward rows land in P1, or state that the P1 flag on a gated command refuses to run (`status: blocked`, stated reason: gate not yet converted) until its phase lands. Prefer narrowing: delete "every command in sections 3.1 and 3.2" from S:159 and AC-1.1 and name the P1 list.
- Priority: High. Quality impact: Consistency 8 -> 5 for the rollout plan if left.

### F-2 (blocking) AC-1.1 cannot pass for `/sc:load`

- Severity: MAJOR, graded blocking. Experts: Wiegers (traceability), Adzic (testable example).
- Location: S:195 (AC-1.1) against S:112 (load row), S:265 (Decisions: load handling), S:52 and S:76 (every changed command gains the section), S:62 (WC-4).
- Grading sentence: An implementer who follows the stated text as written adds a `## Unattended mode` section to `/sc:load` (it is "changed": its usage line, S:112) and AC-1.1 requires every command in 3.1-3.2 to have such a section "naming `return-contract.yaml`"; that is wrong because the load row says Report "none" and "use it as a step inside another worker's brief, not as its own Task" (S:112) and the Decisions table says a report file "would be an unrequested addition" (S:265), so the test either fails for load or forces the contract the spec rejects. Two stated texts contradict (AC-1.1 against S:112 and S:265).
- Recommendation: exempt `load` from AC-1.1 and from WC-4 in one line (the narrower edit); do not add a contract to load.
- Priority: High. Quality impact: Testability 7 -> 5.

### F-3 (Medium, not blocking) WC-4 gives no contract path for commands without an output argument

- Severity label MAJOR, graded Medium (requirement the document never states; no stated text does harm).
- Location: S:62 (WC-4 path rule), S:73 (2.3), rows S:85 (cleanup-audit, fixed `.claude-audit` dir), S:86 (index-repo), S:113 (post-release), S:116 (research: "contract naming the generated `claudedocs/research_*.md` path"), S:117 (review-translation), S:119 (save), S:112 (load).
- WC-4 says the path is "fixed by the output argument the coordinator passed" and must be known before dispatch (S:62, S:73). The rows above add no output argument, so the directory and file branches do not apply. "Fresh dir" in the Resume column (S:99-125) does not say whether the coordinator supplies the directory or the command generates a timestamped one; if the command generates it, the path is not known before dispatch.
- Recommendation: add one sentence to WC-4: when a command has no output argument, name the fixed contract location per row, or the row adds an output argument.
- Priority: Medium.

### F-4 (Medium) Existing contract `status` vocabularies are not checked against the four-value set

- Location: S:62 ("Commands that already write a contract keep their fields"), S:63 (status outside the four values maps to `failed`, B-5), S:261 (reuse of `return-contract.yaml` by workflow, brainstorm, reflect, adversarial).
- INV-B:272 lists the workflow contract fields (`status`, `plan_path`, `reflect_report_path`) but not the allowed status words; nothing in the inventories lists the status words of the other three. If any uses other words, a succeeded run maps to `failed`. A guess that the words match is needed to call this safe, so Medium.
- Recommendation: add a one-line check item to Phase 0 (read the four contracts' status words) or state a mapping table.
- Priority: Medium.

### F-5 (Medium) `--unattended` token parsing is not specified

- Location: S:51, S:228 (D1 a, "cannot misfire on a person"), S:146 (SA-1).
- Several commands take a free-text prompt (research, tdd, troubleshoot, workflow, recommend). The spec does not say that the switch applies only to a standalone argument token outside quoted text. A person whose topic text contains `--unattended` (for example a design discussion of this very feature) could flip the mode, which D1 claims is impossible.
- Recommendation: state the token rule in the contract file requirements (WC section) in one sentence.
- Priority: Medium.

### F-6 (Medium) Undefined references B-1, B-3, B-5, N-1

- Location: S:62, 63, 73, 76, 79, 83, 87, 90, 92, 182, 198, 200.
- The spec cites B-1, B-3, B-5 and N-1 as if defined; the document defines none of them (no table or paragraph introduces these ids; the README does not either, README.md:19-27). Their content is partly recoverable from nearby words (B-5 "the default is `failed`", S:63; B-3 as the output-kind path rule), but B-1 and N-1 are only guessable. They probably point at the disposition file the README lists as a Task 6 output (README.md:25), which a reader of the spec alone does not have.
- Recommendation: add a short key, or replace each id with the rule's words.
- Priority: Medium.

### F-7 (Medium) WC-6 re-run safety covers output directories only

- Location: S:64 (WC-6), rows S:103 (cleanup), S:107 (document), S:110 (improve), S:121 (task), all "fresh dir".
- A retry worker (`--retry-of`) of a command that edits source files in the shared worktree (CAPS:115 says workers share the current worktree by default) starts clean for output but not for the edits attempt 1 already made. "Must not corrupt the first attempt's output" is met; the repeated edit case is not addressed.
- Recommendation: add to WC-6 that a retry brief names which edits already exist, or that these commands list applied items in the contract (cleanup row already does this, S:103) and re-run reads that list.
- Priority: Medium.

### F-8 (Medium) Fixed contract file name collides in a shared directory

- Location: S:62 (`<file's directory>/<command>-return-contract.yaml`), S:69 (WC-11), rows S:87, S:90.
- Two parallel `/sc:tdd` workers writing TDDs into one directory both write `tdd-return-contract.yaml`; WC-11 says two workers must never write the same file. The collision needs the coordinator to place both outputs in one directory (a guess), so Medium.
- Recommendation: the file rule carries the output file's stem: `<file stem>-return-contract.yaml`.
- Priority: Medium.

### F-9 (Medium) WC-3 "ask once" is undefined for multi-gate commands

- Location: S:61 against rows S:105 (three gates), S:117 (two), S:121 (two).
- Not stated whether "once" is per gate, per run or per Task; a re-invoked fresh-dir command that blocks at a second gate is not covered. Needs a guess about which reading an implementer picks.
- Priority: Low to Medium.

---

=== ARCHITECTURE ANALYSIS ===

### F-10 (Medium) tasklist row contradicts its inventory verdict and rests on UNVERIFIED claims

- Experts: Fowler (boundaries), Nygard (failure mode), Whittaker (Divergence Attack).
- Location: S:122 against INV-B:211, INV-B:214, INV-B:215, INV-B:295; S:268; S:280 (UNVERIFIED 9).
- The inventory's verdict for tasklist is that the per-phase reflect fan-out "must run at the worker's top level, not inside subagents" or Stage 10.5 must call reflect without `--remediate` (INV-B:215), and that nested spawning is UNVERIFIED (INV-B:214). The spec row instead keeps the nesting ("none") and asserts it runs "inside Claude Code's nesting limit" (S:122, citing INV-A:14, a general doc statement). The Decisions table says nothing read contradicted an inventory verdict (S:268), which is not true here. The row also does not resolve the `needs_human_decision` HALT (INV-B:211, UNVERIFIED line `SKILL.md:1631`), a person gate under WC-2. The fix relies on reflect's headless rule, which UNVERIFIED 9 says does not apply to an Orca worker (S:280); it holds only if the P2 reflect change (S:88) lands in the same phase, which it does (both P2), but the HALT stays open.
- Concrete attack: I can break this specification by a Divergence Attack on the tasklist row. The invariant at S:122 ("passes `--unattended` to each reflect so the headless rule applies") fails when a reflect subagent meets a `needs_human_decision` item: the subagent has no path to the coordinator (WC-7 forbids it from sending lifecycle messages, S:65), so tasklist stalls with no `worker_done`.
- Recommendation: either follow INV-B:215 (call reflect without `--remediate` under `--unattended`) or add the HALT to the row and the UNVERIFIED list.
- Priority: Medium.

### F-11 (Medium) AC-C1 conflicts with the spec's own Orca-mentioning artifacts

- Location: S:172 (AC-C1 greps `src/superclaude/core` and prints nothing), S:147 (SA-2 allows an Orca mention in the contract file), S:158 (P0 adds an Orca section to `HOW-WE-WORK.md` in `core/`), S:25 (E5 baseline `grep -ci orca HOW-WE-WORK.md` = 0, UNVERIFIED).
- AC-C1's pattern matches `orca orchestration ...` and `orca-ide orchestration ...`; its only exclusion is `skills/ccsession-tag/`. A coordinator-facing Orca section in `HOW-WE-WORK.md` or the brief template in `WORKER-CONTRACT.md` will normally contain those words (the spec's own 7.2 uses `ORCA orchestration ...`). Whether it fails depends on how those files are worded, so Medium.
- Recommendation: exclude `core/WORKER-CONTRACT.md` and the Orca section of `core/HOW-WE-WORK.md` in AC-C1, or state the files must not use the matching form.
- Priority: Medium.

### F-12 (Medium) The "additive edits" checks miss deleted bullets and frontmatter fences

- Location: S:176 (AC-C5), S:193 (AC-0.3), SA-4 S:149.
- `git diff -U0 ... | grep -E '^-[^-]'` does not match a removed line that itself begins with `-` (a markdown bullet appears in the diff as `-- item`; a removed `---` fence as `----`). Commands are bullet-heavy. Deleting a gate bullet leaves the check printing nothing, so "edits are additive" is not enforced as stated.
- Recommendation: use `grep -E '^-' | grep -vE '^---[^-]'` for the `---` header lines only (header lines are `--- a/...`), or compare with `git diff --numstat` deletions.
- Priority: Medium.

### F-13 (Medium) AC-2.4 count check caps at one page

- Location: S:202.
- `gh api .../reviews --jq length` and `.../comments --jq length` return the first page (30 items) unless `--paginate` is used. On a PR already holding 30 or more items, both counts read 30 before and after even when the command posted. The pass condition then holds although WC-9 was violated. Needs a PR with that many items, so Medium.
- Recommendation: add `--paginate` and sum the pages.
- Priority: Medium.

### F-14 (Medium) WC-10 leaves a 4 to 5 minute gap and an unbounded pr-submit poll interval

- Location: S:68, S:114, S:210, S:283 (UNVERIFIED 12).
- WC-10 triggers on a step "longer than 5 minutes" but asks for waits "at most 4 minutes"; a single 4.5-minute call is neither required to split nor allowed by AC-4.3 ("no single tool call exceeds 240 s"). pr-submit's sleep is "at least `--poll-interval`" (S:68), and the value is not bounded. Both only matter for the D3 (b) path and the UNVERIFIED poll runtime is already flagged.
- Recommendation: state one threshold (240 s) for both clauses; cap or refuse `--poll-interval` over 240 under `--unattended`.
- Priority: Low to Medium.

### Notes (minor, never fail the review)

- N-a. S:83 and S:158 list adversarial as "ready today" and S:44 (1.4 item 1) says no direct-route run exists; INV-A:35 and INV-A:35 "proven" wording is stronger than S:43. The spec states the gap openly; consider calling the 10 "ready on reading" in S:76-79.
- N-b. S:11 says the `sk/sc-pr-submit-protocol/SKILL.md:37-39` quote was re-read; CAPS:161 gives the same quote at `:47-49` of the installed copy. The line difference between the src and installed copies is not explained. UNVERIFIED.
- N-c. S:22 cites `CAPS:161` for `[H:worker-start]` line 38 and `--agent claude`; that parenthetical is at CAPS:136. CAPS:161 does support the top-level-worker claim.
- N-d. WC-3 lets the worker relay a coordinator answer as a flag; for implement, D2 (a) says another agent's words are not a Ruling (S:233). The implement row (S:109) already stops with `blocked`; add "WC-3 not used for Ruling" for clarity.
- N-e. S:63 "partial" maps to `succeeded`; Decisions S:263 argues it. No flaw, but the coordinator must read `status` in the body's first sentence, which relies on the worker following prose.
- N-f. S:112 counts `load` as "needing a change" while the same row says to use it as a brief step; the 27 is a count of rows, not of dispatchable commands.
- N-g. CAPS:115 (`[G:placement]` lines 8-11) allows a separate worktree "when a concrete checkout or filesystem conflict makes sharing unsafe"; WC-11 and the cleanup-audit row (S:85) could name that option instead of accepting one audit per worktree.

## Follow-up candidates (Medium and minor; not blocking)

Medium: F-3, F-4, F-5, F-6, F-7, F-8, F-9, F-10, F-11, F-12, F-13, F-14. Minor: N-a to N-g.
Issue question: the loop rule has the session that ran the review ask the user once whether to open an issue for these. This run is a worker whose only permitted output is this file and which may not message anyone, so the question is not asked and no issue is created. The coordinator should ask.

## Checks that passed

- Count conservation 21 + 22 = 43 = 10 + 27 + 6 against INV-A:3, INV-B:3, INV-A:90-92, INV-B:285-287 (the six coordinator-only rows match the inventories).
- Evidence rows E1, E4, R1-R5, WC-1, WC-3, WC-5 (`partial` rationale), WC-7, WC-10 cadence and the 7.2 release check match the CAPS lines they cite (CAPS:44-46, 52, 58-61, 64, 66-67, 72-80, 92, 97-103, 107-113, 115-116, 129-130, 145-150, 155-161).
- Rejected-alternative reasoning (S:28-39) is internally consistent with D5 and Non-goal 1.
- Standalone-use section (SA-1 to SA-6) does not contradict any per-command row apart from the phase timing in F-1.

## Reviser brief

Blocking finding ids: F-1, F-2.
Rules for the reviser (restating the review loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings (F-3 to F-14, notes N-a to N-g) alone. Return the candidate once; do not award yourself a PASS.
- F-1: S:159 (and S:195) fix by narrowing the P1 flag scope or by making a not-yet-converted gated command refuse with `blocked`; no new mechanism beyond that.
- F-2: S:195 exempt `/sc:load` (one line), or equivalent.

verdict: FAIL
