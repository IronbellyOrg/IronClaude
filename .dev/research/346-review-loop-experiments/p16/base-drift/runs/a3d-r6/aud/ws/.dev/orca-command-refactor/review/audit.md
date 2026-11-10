review: 1 of 3

# Audit: orca-worker-contract-spec.md (/sc:spec-panel --mode critique --focus requirements,architecture)

| Item | Value |
|---|---|
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| Candidate sha256 | `21fdbd31168a1ef40b1a05d12ef2b15a3e9d6f6fb4d8afb6da439fffe555cae8` (58141 bytes) |
| Baseline | none given (not a re-review) |
| Prior report | none given |
| Reviewer model actually used | claude-sonnet-5-5 |
| Date | 2026-11-10 |
| Label | whole-document audit of the final spec, first review (FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`) |
| Brief clauses overridden | none |

Citation keys: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `LOOP:N` = `~/.claude/rules/prompts/document_review_loop_prompts.md`. `CMD:N` = the `/sc:spec-panel` definition `command.md` supplied in the sandbox. Source files cited by the inventories (`src/superclaude/...`, `EVIDENCE.md`, Orca internals, `CLAUDE.md`) are not in the sandbox: a claim that depends only on them is marked UNVERIFIED.

## Coverage
- Read in full: the candidate (285 lines), `README`, all three inventories, `command.md`, the loop prompts file.
- Checked: every count in section 3 against the inventory tables (43 = 10 + 27 + 6; 21 + 22; the 27 section 3.2 rows; the 15 P2 rows against the section 6 P2 list); every `CAPS:` and `INV-A/INV-B:` line citation I used to test a load-bearing claim (spot checks listed per finding); the internal consistency of WC-1..12, SA-1..6, AC-C1..5, AC-0..4 and D1..D5.
- Not checkable here (UNVERIFIED): every `src/superclaude/...:N`, `EVIDENCE.md:N`, `CLAUDE.md:N`, `Makefile:N`, `pyproject.toml:38` citation and the two grep results in E5 (`SPEC:25`). Two inventories disagree on the pr-submit top-level rule lines (see m1).
- Quantity check (Pipeline Dimensional Analysis, advisory): 43 commands = 10 ready + 27 changed + 6 coordinator-only (`SPEC:76`); 37 worker-capable commands = P1 13 (8 in 3.2 + `load` + 4 fixes to ready commands) + P2 15 + P3 4 + P4 3 + 2 with no change (brainstorm, init-lite). Counts are conserved; no mismatch. No filter/aggregate stage with unaccounted divergence, so the heuristic does not escalate.
- Not active under this focus: Crispin, Gregory, Hightower as leads (Crispin's testability points appear where they changed a grade).

## Verdict summary
1 blocking finding (B1), 17 Medium warnings, 5 minor notes. Everything else I traced holds (decision, rejected alternative, command partition, phase membership).

=== REQUIREMENTS ANALYSIS ===

### Blocking

**B1. MAJOR, graded BLOCKING. The P0 acceptance check cannot pass for the commands it names.**
- Experts: Wiegers (testability), Adzic (example), Crispin.
- Stated texts: `SPEC:182` (7.2 step 3) passes only when "its report path is the WC-4 contract path" and its `--outcome` "matches the contract's `status`". `SPEC:62` fixes the WC-4 contract path as `<output-dir>/return-contract.yaml`. `SPEC:194` (AC-0.4) runs 7.2 on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` and requires "steps 1-3 and 5-7 pass"; it relaxes only step 4 ("uses the command's existing report file, since the contract arrives in P1"). `SPEC:91` says troubleshoot reports `REPORT.md` today; `SPEC:92` puts the workflow contract at `.dev/tasks/to-do/<id>/return-contract.yaml`; `SPEC:83` puts the adversarial contract at `<output>/adversarial/`. `SPEC:154` says later phases do not start until the earlier phase's checks pass.
- Grading sentence: An implementer who follows the stated text as written runs step 3 on `/sc:troubleshoot` in P0, finds a `worker_done --report-path` of `REPORT.md` and no WC-4 contract to compare the outcome with, and step 3 fails; so AC-0.4 can never pass, and X (P0 -> P1 gating, `SPEC:154`) is wrong because the rollout stops on a check the same spec says cannot yet be satisfied. The same step fails for workflow and adversarial, whose contract paths differ from the WC-4 formula.
- Recommendation: in AC-0.4, state that step 3 also uses the command's existing report file and existing status field (as step 4 does), and that the WC-4 path and outcome-to-contract match apply from P1. Narrow, no new mechanism.
- Priority: High. Quality impact: Testability 5 -> 8.

=== ARCHITECTURE ANALYSIS ===

Grade key for the rest: each item below is Medium (warning, `follow-up candidates`); each needs the implementer to guess between readings, or is a requirement the document never states (`LOOP:31`).

**M1. The WC-4 contract location is undefined when the output flag is file-valued, and not computable before dispatch for commands whose contract path is generated.** Fowler (interface), Wiegers.
- `SPEC:62`: contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", "known before dispatch" (also `SPEC:73`). But tdd and init-lite take `--output <file>` (`SPEC:87`, `SPEC:90`), spec-panel gets an `--output` (`SPEC:120`), workflow's contract path embeds a generated `<id>` (`SPEC:92`, `INV-B:272`), adversarial's sits in a subfolder (`SPEC:83`), reflect's defaults to a timestamped folder (`INV-B:112`).
- Concrete: `AC-2.2` (`SPEC:200`) uses `/sc:tdd "auth" --unattended --output <file>` as its own example and then needs `<contract>` for 7.2 step 4 (`SPEC:183`); no path follows from the text. A literal reading creates a directory named like the TDD file, which collides with the TDD write.
- Recommendation: one sentence: for a file-valued output flag the contract is written beside the file (`<file-dir>/return-contract.yaml` or a named sibling), and the worker's `--report-path` carries the actual path. Priority: High. Impact: Completeness +1, Testability +1.
- Evidence the gap is real: the later definition in `CMD:23` and `CMD:460-461` introduces a separate directory flag `--report-dir` because `--output` is file-valued.

**M2. `--unattended` and the contract duties never reach five "ready" commands, although the brief is told to pass `--unattended` everywhere.** Cockburn (primary actor: the worker session), Hohpe.
- `SPEC:73` (2.3): the brief states "the exact command line including `--unattended`". `SPEC:228` (D1a): the coordinator writes it "into every worker's command line". But `SPEC:83-87` (adversarial, brainstorm, cleanup-audit, index-repo, init-lite) give no `--unattended` flag, and P1 adds the flag to the eight listed commands only (`SPEC:159`, `SPEC:195`). `SPEC:52` makes the per-command `## Unattended mode` section the place that points to `~/.claude/WORKER-CONTRACT.md`, which is where WC-3, WC-5, WC-7 and WC-12 (worker-session duties, `SPEC:61,63,65,70`) are written.
- Effect: for those commands the brief template from P0 passes an unrecognised token (outcome depends on each command's argument parser; unknown), and the worker session has no pointer to the outcome-mapping and top-level duties. Same gap for the 15 P2 commands during P0/P1 (`SPEC:158`).
- Recommendation: state per phase that the brief adds `--unattended` only for commands whose phase has landed, and put WC-3/5/7/12 into the coordinator brief template (P0) so they do not depend on the command text. Priority: High.

**M3. WC-10 has a threshold hole and a coverage hole.** Nygard, Whittaker (FR-2.2, FR-2.5).
- Boundary: WC-10 (`SPEC:68`) splits only a step that blocks "longer than 5 minutes" into waits of at most 4 minutes, yet AC-4.3 (`SPEC:210`) fails any single call above 240 s and requires heartbeats at most 5 minutes apart. A 4.5-minute call passes WC-10 and fails AC-4.3; a 5-minute call plus the heartbeat cadence gives a gap above 5 minutes.
- Coverage: the rule is generic ("a command step that blocks a single tool call"), but only cli-eval and pr-submit carry a fix (`SPEC:104`, `SPEC:114`). Agent-tool fan-out calls that block the top-level session (adversarial rounds, tdd, cleanup-audit waves of 7-8 agents, post-release scanners; `INV-A:35,42`, `INV-B:33,47`) are the same kind of call and are not addressed. Whether heartbeat age even feeds liveness is UNVERIFIED (`CAPS:130`, `CAPS:182`).
- Recommendation: use one number (4 minutes) in WC-10 and AC-4.3, and say whether Agent-tool fan-out is exempt (and why). Priority: Medium.

**M4. `--unattended` is not required to propagate into nested commands and skills, except tasklist to reflect.** Newman (service boundaries), Whittaker (FR-2.4).
- Only `SPEC:122` passes the flag down. Other commands call nested prompts-bearing commands: brainstorm to adversarial (`INV-A:39`), release-split to brainstorm and adversarial (`INV-B:37,119`), cli-eval to spec-panel and adversarial (`INV-A:44`), task TFEP to troubleshoot (`INV-B:45`; troubleshoot has a `--fix` offer and a short-input STOP, `SPEC:91`), workflow to reflect (`INV-B:52`), tdd to the `task` skill (`SPEC:90`).
- Effect: a nested prompt can still stall a worker, which WC-2 (`SPEC:60`) forbids only for "the command" itself. Recommendation: one sentence in WC-2: a command in unattended mode passes the mode (or the equivalent flags) to every command or skill it invokes, or names why it need not. Priority: Medium.

**M5. The tasklist fix reverses the inventory's recommendation without a recorded decision and does not say what auto-accept does.** Fowler, Nygard.
- `SPEC:122`: under `--unattended`, Stage 10.5 passes `--unattended` to each reflect "so the headless rule applies". `INV-B:46` recommended dropping `--remediate` in Stage 10.5; `INV-B` Decisions say an Orca worker is not headless. Under the headless rule reflect "auto-accepts for auto-fixable registers" (`INV-B:109`), i.e. it runs the remediation hand-off (workflow or task-builder), which writes files. The spec states neither that effect nor that it is wanted in a generation worker; the Decisions table (`SPEC:259-269`) has no entry for the divergence; UNVERIFIED #9 (`SPEC:280`) concedes the headless assumption.
- Recommendation: either pass `--no-remediate` semantics (drop it, as the inventory advised) or add the one-line decision and the expected files to the contract's `artifacts`. Priority: Medium.

**M6. WC-4 "keep their fields" and the fixed `status` set can collide.** Wiegers, Adzic.
- `SPEC:62`: commands with a contract "keep their fields and add the missing ones"; the same row and `SPEC:262` fix `status` to `succeeded|partial|failed|blocked`. Only workflow's `status` field is known to exist (`INV-B:272`); the status values of workflow, reflect, adversarial, brainstorm and troubleshoot contracts were not recorded. AC step 4 (`SPEC:183`) asserts membership in the fixed set for all of them.
- Recommendation: add the existing vocabularies to the spec (or say a mapped alias field is added) before P1. Priority: Medium. The spec's own checks cannot tell which side wins.

**M7. WC-6 "fresh output directory" conflicts with WC-4 "directory known before dispatch", and a stale contract is not excluded.** Whittaker (FR-2.4 sequence attack), Nygard.
- Concrete attack: a `--retry-of` worker (`CAPS:116`) receives the same brief and the same `<output-dir>`; attempt 1 left `return-contract.yaml` with `status: failed` (or `blocked`). Attempt 2 dies before writing. The coordinator reads the stale file as attempt 2's result; 7.2 step 4 (`SPEC:183`) only checks existence and validity. About 20 commands are "fresh dir" (`SPEC:99-125`), and nothing says who creates the fresh directory or that the contract is removed at start.
- Recommendation: the coordinator passes a new directory per attempt (add to 2.3), and a command in unattended mode overwrites or deletes any existing contract before doing work. Priority: Medium.

**M8. Several requirements have no phase deliverable or check; one pass condition is vacuous.** Crispin, Wiegers.
- WC-1 (owner "launch setup, not commands", `SPEC:59`) appears in no phase (`SPEC:156-162`) and no check; WC-3 and WC-12 (`SPEC:61,70`) have no check either. 7.2 step 2 (`SPEC:181`) passes when `observation.agentWait` is "never non-null", but an absent field means Orca never looked (`CAPS:129`), so an absent field passes vacuously.
- Recommendation: add a P0 deliverable and check for WC-1 (or move it out of the contract), and require `agentWait: null` present, not absent. Priority: Medium.

**M9. Common check AC-C1 may fail on the spec's own deliverables and has no baseline.** Crispin, Fowler.
- `SPEC:172` requires no output for a grep over `src/superclaude/core` and the other trees. `SPEC:147` (SA-2) allows an Orca example in the contract file, and P0 adds an Orca section to `HOW-WE-WORK.md` (`SPEC:158`, `SPEC:150`). Any text that names `orca orchestration ...` makes AC-C1 fail in P0. AC-C3 (`SPEC:174`) captures a baseline for tests; AC-C1 does not, and E5 (`SPEC:25`) is a one-time grep result I cannot check (UNVERIFIED). The session's current skill list describes `sc-issue-protocol` as creating an Orca worktree (UNVERIFIED against the spec's tree, dated 2026-11-02): if that skill is present, E5 and AC-C1 are already false.
- Recommendation: make AC-C1 baseline-relative and exempt the contract file and the routing-guide section, or restrict the pattern. Priority: Medium.

**M10. AC-C3 covers one test directory, and AC-1.1's negative assertion breaks in P2.** Crispin.
- `SPEC:174` runs only `tests/skills/`; P1-P3 edit about 35 command files, and the plugin mirror question is unresolved (`SPEC:279`, UNVERIFIED #8). `SPEC:195` asserts that no P2-P4 command has an `## Unattended mode` section; P2 adds exactly those sections, so P2 must edit a P1 test while AC-C3 says no baseline-passing test may fail. Recommendation: assert presence for landed phases only, and run `make test` as the baseline in AC-C3. Priority: Medium.

**M11. WC-3 has no carve-out for the implement Ruling.** Nygard (safety boundary), Fowler.
- `SPEC:61` lets the worker "ask the coordinator once" for any gate that would resolve as blocked, then re-invoke "with the answer as a flag". D2(a) (`SPEC:234`) keeps the rule that another agent's message is not a Ruling (`INV-A:51,66`). WC-3 does not exclude implement, so a worker may ask, and the coordinator (an agent) may answer. The command's own rule (`SPEC:109`, "Ruling rule itself is unchanged") should still refuse it, so the harm is guarded; the contradiction in wording remains. Recommendation: one clause in WC-3 or the implement row: a Ruling is never accepted from `ask`. Priority: Medium.

**M12. The statement that a command's own question "does not fail worker-start" is an inference listed as fact.** Nygard.
- `SPEC:44` (1.4 point 2): a command question comes after readiness. But Claude gets its task by argv (`CAPS:47`), so the command starts running at launch; a command that asks in its first seconds (cli-eval with no `$1`, tdd with a bare topic; `INV-A:44`, `INV-B:47`) may still be at the question when the 60-second limit runs out (`CAPS:44`, `CAPS:49`). This is not in the UNVERIFIED list (`SPEC:271-285`). WC-1 covers the launch path only. The effect is a failed `worker-start` plus a reclaimable terminal (`CAPS:112`), not a silent stall.
- Recommendation: add it to UNVERIFIED and to AC-0.4 as an explicit trial (a gate-hit run). Priority: Medium.

**M13. The shared-worktree default sits against the repo's parallel-session rule, and WC-11 has no enforcement.** Newman, Nygard.
- `SPEC:69` and `SPEC:180` (`--worktree current`) and AC-3.4 (`SPEC:207`) put several workers in one worktree (`CAPS:115`). The repo's own `CLAUDE.md` "Parallel Development with Git Worktrees" section tells parallel sessions to use their own worktrees (UNVERIFIED line; text is in the session instructions, not in the sandbox). WC-11 asks commands not to write the same file, but fixed outputs exist (cleanup-audit `.claude-audit/`, `SPEC:85`), and cleanup, improve and test `--fix` edit code in the shared tree (`SPEC:103,110,123`). The spec leaves it to the brief (`SPEC:73`).
- Recommendation: state when the coordinator must pass a separate worktree (any two Tasks that can edit source, or a fixed output dir) and add it to 2.3. Priority: Medium.

**M14. Retry has no cap for report-level failures.** Whittaker (FR-2.5 accumulation), Nygard.
- `SPEC:63` maps `blocked` and `failed` reports to `--outcome failed`; Orca's circuit breaker ignores a worker's own failed report (`CAPS:80`, `SPEC:263`). A coordinator that answers a blocked worker by retrying (WC-3, WC-6) can loop forever; nothing in the spec caps it. Recommendation: one line in 2.3: at most N retries per Task, then escalate to the person. Priority: Low.

**M15. Empty and quoted `--unattended` cases are unspecified.** Whittaker (FR-2.1, FR-2.3).
- No output directory: WC-4 says the contract is written "on every outcome, including stops before any other output exists" (`SPEC:62`), which cannot be met without a directory; 2.3 makes the coordinator supply one, but the command behaviour when it is missing is not given. The later command definition refuses before work and prints in chat only (`CMD:460`). A quoted topic that contains the word `--unattended` (a TDD about this feature) is not distinguished from the switch (`CMD:459` handles it; the spec does not). Recommendation: two sentences in WC-2 or WC-4. Priority: Low.

**M16. WC-5 does not say what happens to an unreadable or empty report, or to a status outside the set.** Whittaker (FR-2.3 sentinel collision).
- `SPEC:63`: failed when no report exists; succeeded "otherwise". A zero-byte or malformed file, or `status: complete` from an old-style contract (M6), falls into "otherwise" and sends `succeeded`. Recommendation: "no readable report with a status in the set" means `failed`. Priority: Medium.

**M17. Scope drift against the spec's own rule.** Cockburn, Wiegers.
- Non-goal 8 (`SPEC:220`) keeps only defects that stop a command working as a worker; yet the business-panel frontmatter move (effect on loading UNVERIFIED, `SPEC:102`, `SPEC:278`) and the `load` usage line (`SPEC:112`, `SPEC:149`) are in P1, and P1 is titled "commands with no gate" (`SPEC:159`) while business-panel, explain, index and test carry refusals or pins (`SPEC:102,108,111,123`). Recommendation: drop the two cosmetic fixes or amend non-goal 8; fix the P1 title. Priority: Low.

=== FOLLOW-UP SUMMARY (minor notes) ===

- **m1.** Citation sources disagree on the pr-submit top-level rule: `sk/sc-pr-submit-protocol/SKILL.md:37-39` and `:66-68` (`SPEC:65`, `INV-A:10,14`, `INV-B:90`) against `:47-49` and `:82-84` (`CAPS:161`, which names the installed `~/.claude` copy). The spec says it re-read `:37-39` (`SPEC:11`). Also `SPEC:68` cites `:46-64` and `SPEC:114`/`SPEC:239` cite `:41-64`. UNVERIFIED here; confirm the installed and source copies match.
- **m2.** UNVERIFIED item 14 (`SPEC:285`) is a process note, not an unverified fact. The "43 commands" total (`SPEC:76`) cannot be checked in this sandbox (no directory listing); the session's skill list also names `sc:graph`, `sc:impact` and `sc:issue`, which no inventory covers (UNVERIFIED against the spec's tree).
- **m3.** `SPEC:76` says every changed command gains the section; `load` (`SPEC:112`, AC-1.1 `SPEC:195`) and the four P1 fixes to ready commands (`SPEC:83-92`) do not.
- **m4.** AC-2.4 (`SPEC:202`) counts with `--jq length` on `gh api` list endpoints, which return the first page only; a PR with 30 or more reviews or comments would show an unchanged count after a post.
- **m5.** 7.2 step 5 (`SPEC:184`) searches the transcript for the string `AskUserQuestion`; the command text itself can contain that word (WC-2 names it, `SPEC:60`), so the check needs "tool call", not "string".

## Guard Condition Boundary Table

Trigger: the spec contains thresholds, boolean guards and sentinel comparisons (readiness limit, heartbeat and wait sizes, confidence < 0.70, depth 1, status mapping, `--monitor 1`, topic-only and short-input stops, `--unattended` itself). Constructed by Nygard, completeness-checked by Crispin, attacked by Whittaker. FR-8/FR-9 grading follows `CMD:332-333`: a GAP is blocking only with a concrete wrong outcome; none below reaches it, so each GAP is a Medium warning (see the finding id).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit | SPEC:59 (WC-1) | Zero/Empty | `--timeout-ms` absent or non-positive | default 60 s | default applies (`CAPS:44`) | OK |
| readiness limit | SPEC:59 (WC-1) | Typical | prompt with 30 s fallback | pass | worker-start returns ~34 s (`SPEC:59`) | OK |
| readiness limit | SPEC:59 (WC-1) | Maximum/Overflow | fallback above ~45 s | fail | "fails again" (`SPEC:59`) | OK |
| readiness limit | SPEC:59 (WC-1) | Legitimate Edge Case | "well inside the limit", no number | undefined | no threshold given | GAP (M8, M12) |
| wait split | SPEC:68 (WC-10) | One/Minimal | one wait of 4 min | no split | allowed | OK |
| wait split | SPEC:68 (WC-10) | Legitimate Edge Case | one call of 4.5 min | no split (<= 5) | AC-4.3 fails calls above 240 s (`SPEC:210`) | GAP (M3) |
| wait split | SPEC:68 (WC-10) | Maximum/Overflow | one call of 5 min exactly | no split ("longer than") | heartbeat gap above 5 min | GAP (M3) |
| wait split | SPEC:68 (WC-10) | Typical | pr-submit poll iteration | "confirm under 4 min" | poll runtime UNVERIFIED (`SPEC:283`) | GAP (M3) |
| confidence gate | SPEC:121 (task row) | Zero/Empty | confidence 0 | below 0.70 | blocked | OK |
| confidence gate | SPEC:121 | Legitimate Edge Case | confidence exactly 0.70 | not below | proceeds (inventory text "< 0.70", `INV-B:45`) | OK |
| confidence gate | SPEC:121 | Typical | 0.85 | not below | proceeds | OK |
| status to outcome | SPEC:63 (WC-5) | Zero/Empty | no report, or 0-byte file | no readable status | "no report exists" gives failed; 0-byte file unstated | GAP (M16) |
| status to outcome | SPEC:63 (WC-5) | Typical | `succeeded` / `partial` | succeeded | `--outcome succeeded` | OK |
| status to outcome | SPEC:63 (WC-5) | Legitimate Edge Case | `blocked` / audit verdict FAIL | failed / succeeded | stated both ways | OK |
| status to outcome | SPEC:63 (WC-5) | Sentinel Value Match | status outside the set (e.g. `complete`) | "otherwise" | maps to succeeded | GAP (M6, M16) |
| `--unattended` switch | SPEC:51, SPEC:228 | Zero/Empty | flag absent | standalone | behaviour unchanged (SA-1, `SPEC:146`) | OK |
| `--unattended` switch | SPEC:51 | Sentinel Value Match | the word inside a quoted topic | unspecified | not distinguished from the switch | GAP (M15) |
| `--unattended` switch | SPEC:73, SPEC:83-87 | Legitimate Edge Case | passed to a command that has no such flag | unspecified | not stated | GAP (M2) |
| output directory | SPEC:62 (WC-4) | Zero/Empty | no directory passed | contract has no place | not stated | GAP (M15) |
| output directory | SPEC:62 | Legitimate Edge Case | file-valued `--output` | `<file>/return-contract.yaml` read literally | not stated | GAP (M1) |
| retry cap | SPEC:63, SPEC:64 | Maximum/Overflow | repeated `blocked` or `failed` reports | breaker ignores them (`CAPS:80`) | no cap | GAP (M14) |
| `--monitor` level | SPEC:114 (pr-submit) | Legitimate Edge Case | `--monitor 1` | refused | blocked | OK |
| `--monitor` level | SPEC:114 | Typical | `--monitor 3` (default) | no y/n gate (`INV-B:89`) | proceeds | OK |
| topic-only stop | SPEC:90 (tdd row) | Legitimate Edge Case | prompt between "topic" and "component" | skill judgment | no measurable rule | GAP (Medium, M12 area) |
| short-input stop | SPEC:91 (troubleshoot row) | Zero/Empty | empty `--depth deep` prompt | under 10 words | blocked (`INV-B:49`) | OK |
| nesting depth | SPEC:33, SPEC:214 | Legitimate Edge Case | depth raised to 2 (D5b) | fence relaxed | WC-8 still forbids; D5 recommends keeping 1 | OK |

Left out, with reason: nesting depth Zero/Empty, because a malformed value falls back to the default (`CAPS:100`) and the spec does not rely on it; confidence gate Maximum, because 1.0 is not below 0.70; `--monitor` level Zero/Empty, because the row refuses only level 1 and levels 0 and 2 carry no y/n gate (`INV-B:89`); every guard's Sentinel class not listed above, because no sentinel value exists for it. FR-10 is met: no cell is blank and every guard is listed.

## Adversarial analysis (Whittaker)

- I can break this specification by **Sequence Attack (FR-2.4)**. The invariant at **WC-4/WC-6 (`SPEC:62`, `SPEC:64`)**, "the report is written on every outcome and a retry does not corrupt the first attempt", fails when **a retry reuses the first attempt's output directory and the second attempt dies before writing**. Concrete attack: attempt 1 ends `blocked` and leaves `D/return-contract.yaml` (status blocked); the coordinator answers and starts `--retry-of` with the same brief (dir `D`); the session crashes at second 20; before: contract blocked from attempt 1; after: same file, so the coordinator reads attempt 1's question as attempt 2's state. (M7)
- I can break this specification by **Sentinel Collision Attack (FR-2.3)**. The invariant at **WC-5 (`SPEC:63`)** fails when **a legacy contract carries `status: complete`**. Concrete attack: workflow or reflect writes its own vocabulary and keeps its fields (`SPEC:62`); the worker maps "otherwise" to `--outcome succeeded`; 7.2 step 4 asserts membership and fails only afterwards, in the coordinator. (M6, M16)
- I can break this specification by **Zero/Empty Attack (FR-2.1)**. The invariant at **WC-4 (`SPEC:62`)** fails when **no output directory is given or the output flag is a file**. Concrete attack: `/sc:tdd "auth" --unattended --output docs/TDD_AUTH.md`; the command writes `docs/TDD_AUTH.md/return-contract.yaml` before the TDD file; the later TDD write fails. (M1, M15)
- I can break this specification by **Divergence Attack (FR-2.2)**. The invariant at **WC-10/AC-4.3 (`SPEC:68`, `SPEC:210`)** fails when **one call lasts between 240 s and 300 s**. Concrete attack: a 4.5-minute fan-out call: WC-10 says no split; AC-4.3 says the phase fails. (M3)
- I can break this specification by **Accumulation Attack (FR-2.5)**. The invariant at **WC-5 and `CAPS:80` (`SPEC:63`, `SPEC:263`)**, "a failed report does not trip the breaker", fails when **a coordinator answers `blocked` by retrying without limit**. Concrete attack: 10 retries of a task that always hits the same gate; Orca's breaker count stays 0; the loop ends only on the coordinator's own policy. (M14)
- I can break this specification by **Sequence Attack (FR-2.4)** on rollout order. The invariant at **AC-1.1 and AC-C3 (`SPEC:195`, `SPEC:174`)** fails when **P2 adds the sections that P1's test asserts are absent**. Concrete attack: P1 merges the negative assertion; P2 adds `## Unattended mode` to tdd; the P1 test fails; AC-C3 forbids a baseline-passing test failing. (M10)

## Cross-expert notes
- Agreement: the central decision (Orca coordinates, commands stay units of work) is well supported: R1-R5 (`SPEC:31-37`) check against `CAPS:97-103,145-150`, and 1.4 states its own evidence gaps plainly (`SPEC:41-45`). Wiegers, Fowler and Cockburn concur.
- Disagreement: Crispin would grade M8 and M10 up if P0 is run as a gate; Nygard would grade M12 up if the first live trial hits an early prompt. Both stay Medium here because the text allows a reasonable reading and the harm is a visible failed check, not data loss.

## Decisions
| Decision | Options | Rationale |
|---|---|---|
| Grade B1 blocking | Blocking; Medium | `SPEC:194` relaxes step 4 but not step 3, so the stated text cannot pass for troubleshoot (`SPEC:91`); it needs no guess (`LOOP:31`). |
| Grade M1, M2, M4, M5 Medium | Blocking; Medium | Each needs the implementer to choose between readings or concerns a requirement the spec never states; none names a wrong outcome without an extra assumption. |
| Do not grade the shared-worktree finding blocking | Blocking; Medium | The conflicting text is in `CLAUDE.md`, which is not in the sandbox (UNVERIFIED), and the spec says worktree placement is the brief's choice (`SPEC:73`). |
| Treat `command.md` flags as non-evidence for the candidate | Use as evidence; note only | The README names the inventories as the only checkable evidence; I cite `CMD:` only to show a gap is real (M1, M15). |

## Follow-up candidates
Medium: M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15, M16, M17. Minor: m1, m2, m3, m4, m5. Medium and minor findings never trigger a revision and are not in the Reviser brief. The review session asked the user nothing about opening an issue for them: this run is a worker with no user channel, so it only records the list and creates no issue (`CMD:260`).

## Reviser brief
Blocking finding ids: **B1**.
Rules for the reviser (restating the Reviser contract, `CMD:263`): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the candidate's byte size before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.
Scope for B1: `SPEC:182` (7.2 step 3) and `SPEC:194` (AC-0.4) only.

verdict: FAIL
