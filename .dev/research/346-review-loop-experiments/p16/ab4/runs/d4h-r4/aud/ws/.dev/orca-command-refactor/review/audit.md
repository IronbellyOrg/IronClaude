review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec; a first review of the whole document (no `--re-review`, no `--baseline`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `5c1ab8696d3015841916a6b721ba37673ca41cc95d7518dd2f44d176aa42898f`
- baseline: none (first review)
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, resolved to `home/.claude/rules/prompts/document_review_loop_prompts.md`)
- shared context read first: `.dev/orca-command-refactor/README.md:1-38`
- spec citations below are `spec:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`
- brief clauses overridden: none
- coverage: all 318 spec lines read; the three inventories read for every line the spec cites for a verdict or for an Orca fact (about 60 inventory lines cross-checked, no wrong line found). Not covered: every `sk/`, `cmd/`, `ag/`, `CLAUDE.md`, `.dev/evals/` and `.dev/codegraph-migration/` citation, because none of those files exist in this sandbox. They are UNVERIFIED here, except where an inventory quotes the same line. I did not re-judge the 10 / 27 / 6 verdicts.
- I ran two checks in the sandbox: the AC-C5 regex against a deleted markdown bullet, and the AC-C1 scan regex against `orca ask` and `orca-ide skills get` (details in M-1 and M-5).

## Summary

The spec's decision (Orca on top, commands stay the units of work) is supported by the evidence it cites, and the counts reconcile: 43 = 21 + 22 (`INV-A:3`, `INV-B:3`); 10 + 27 + 6 = 43; the P1 to P4 split covers all 27 changed commands (9 + 11 + 4 + 3), P2 has 15 commands with one gate-trigger row each (`spec:160`, `spec:227-243`). All CAPS citations I checked match the capabilities inventory. I found no finding that meets the blocking test: no two stated texts that contradict with no further assumption, no stated text that causes data loss or breaks a safety boundary, and no acceptance criterion that cannot pass as written. I found 12 Medium findings, mostly places where the document never states something an implementer needs, or where an acceptance check gives false assurance. Details follow.

Grading check applied to every finding below: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding is blocking only when that sentence holds with no extra assumption. Every finding below needs at least one assumption (the implementer picks the worse of two readings, or the document is silent), so each is Medium or a note. Where the label would have been higher (FR-19 dimensional mismatch, M-2) I graded by consequence, as the command requires.

=== REQUIREMENTS ANALYSIS ===

### M-1 (Medium, Wiegers + Whittaker, sequence/zero attack) AC-C5 and AC-0.3 cannot detect a deleted markdown bullet
- Stated text: `git diff -U0 master...HEAD -- <file> | grep -E '^-[^-]'` "prints nothing: edits are additive" (`spec:188`, same pattern at `spec:205`). It is the only mechanical enforcement of SA-4 and SA-1 (`spec:149`, `spec:146`).
- Evidence: a deleted line `- item` appears in a diff as `-- item`, whose second character is `-`, so `^-[^-]` does not match it. I ran `printf -- '-- item\n' | grep -E '^-[^-]'` and `printf -- '----\n' | grep -E '^-[^-]'` in the sandbox: both printed nothing and returned 1. Deleted bullets and deleted `---` frontmatter delimiters are therefore invisible to the check, and both are common in command files.
- Wrong outcome: an implementer who deletes a bullet from a command file (a standalone behavior change) passes AC-C5, so the "additive" guarantee is unenforced.
- Why not blocking: the harm needs an implementer to actually delete a bullet; the document states no wrong behavior itself.
- Recommendation: use `grep -E '^-' | grep -vE '^--- '` (file headers only), or `git diff --numstat` and require 0 deletions. Priority: Medium. Quality impact: Testability.

### M-2 (Medium, Wiegers, dimensional check; FR-19 label overridden by consequence) Three different sets of commands change in Phase 1
- `spec:79` says Phase 1 adds `--unattended`, the section and the WC-4 contract to all ten commands of 3.1 (M5). `spec:159` says the flag is "accepted by every command in sections 3.1 and 3.2" (37 commands) and lists in the Commands column only 9 section-3.2 commands plus fixes to 4 (13 commands, omitting brainstorm, init-lite, reflect, release-split, tdd, troubleshoot). AC-1.1 requires the section on all of 3.1 plus the P1-phase 3.2 commands except `load` (`spec:207`): 10 + 8 = 18. The N1 note in AC-1.1 contradicts `spec:159` ("every command in 3.2").
- Wrong outcome: an implementer who builds from the section 6 table alone skips six commands and AC-1.1 fails; one who builds from `spec:159` adds the flag to post-release, pr-submit, implement and cleanup in P1, before their gates and outward-action defaults change in P2/P4 (`spec:160`, `spec:162`). A coordinator following `spec:73` that passes `--unattended` to those commands in the interim would assume WC-9 holds when it does not yet.
- Why not blocking: AC-1.1 catches the first reading; the second needs the implementer to choose the broad reading of `spec:159`, and `spec:207` (N1) points the other way.
- Recommendation: make the three statements one list; delete "and 3.2" from `spec:159` and add the six 3.1 commands to the P1 Commands column. Priority: Medium. Impact: Consistency.

### M-3 (Medium, Wiegers + Cockburn) The contract file location (WC-4) is undefined for commands that have no coordinator-passed output directory
- Stated text: the contract is `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", and the coordinator knows the path before dispatch (`spec:62`, `spec:73`). Phase 1 adds the contract to all ten ready commands (`spec:79`), and AC-1.2 runs every P1 command "with `--unattended --output <dir>`" (`spec:208`).
- Cases the rule does not cover:
  - cleanup-audit: output dir is fixed (`spec:85`), no `--output` listed; AC-1.2 passes a flag the row never adds.
  - index-repo: only "state the output location" (`spec:86`).
  - workflow: the contract lives at `.dev/tasks/to-do/<id>/` (`spec:92`, `INV-B:272`), `<id>` does not exist before dispatch, and the new "pre-creation STOP" contract has no package folder to live in.
  - tdd and init-lite: `--output` is a file (`spec:87`, `spec:90`), so "the directory the coordinator passed" does not exist; only init-lite gets a rule ("beside the report").
  - troubleshoot and reflect: default dirs carry a timestamp (`INV-B:242`, `INV-B:112`) and the rows list no output flag.
- Wrong outcome: each implementer picks a location; the coordinator cannot open the report named in `spec:73`, and 7.2 step 3 ("report path is the WC-4 contract path", `spec:194`) cannot be evaluated.
- Why Medium: the document is silent for these cases rather than stating a harmful text.
- Recommendation: state one rule for the location (for example "beside the main report; for a file-valued `--output`, in its parent directory; for fixed dirs, in the fixed dir; for workflow, a coordinator-passed path or the package folder, with the pre-creation case writing to the brief's output dir") and drop `--output <dir>` from AC-1.2 for commands that have none. Priority: High within follow-ups. Impact: Completeness, Testability.

### M-4 (Medium, Wiegers + Crispin) WC-3 lets the worker ask instead of block, but the gate-trigger checks expect only "blocked"
- WC-3: when a gate resolves as blocked and a preamble exists, the session "may instead ask the coordinator once" (`spec:61`). AC-2.2 expects `--outcome failed` and `status: blocked` for every (c) row (`spec:212`, `spec:225`, `spec:229-237`). 2.3 does not say whether the brief permits `ask` (`spec:73`).
- Wrong outcome: a worker that correctly uses WC-3 gets an answer and ends `succeeded`; the live check records a failure. Conversely a coordinator running the check cannot tell which behavior is expected. After the answer, a "fresh dir" command (WC-6) re-runs into a different directory than the one the brief named (`spec:64`, `spec:99-125`), so the contract path the brief promised is stale (sequence attack).
- Recommendation: add to 2.3 an explicit "ask allowed: yes/no" brief field; state which directory a re-invocation after `ask` writes to. Priority: Medium. Impact: Testability, Consistency.

### M-5 (Medium, Crispin) Requirements with no acceptance check, and a scan that can pass while SA-2 is broken
- No check exists for WC-3 (ask path), WC-6 (retry must not corrupt the first attempt), WC-12 (`consumer_fenced`), or for WC-10 on any command except pr-submit (`spec:222`). WC-6 in particular is a stated safety property of retries with no test (`spec:64`, `spec:166-243`).
- AC-C1 scans only four sub-verbs: `\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b` (`spec:176`, `spec:183`). I ran the pattern in the sandbox against `orca-ide skills get x` and `orca ask --question q`: nothing matched. SA-2 says "no command, skill or agent file runs an `orca` or `orca-ide` command" (`spec:147`), so a command file containing `orca ask` or `orca-ide status` passes AC-C1.
- Recommendation: widen the scan to `\borca(-ide)?[[:space:]]+[a-z]` (keep the ccsession-tag exclusion) and add a retry check (run the same Task with `--retry-of` and compare first-attempt files by hash). Priority: Medium. Impact: Testability.

### M-6 (Medium, Adzic) Live check 7.2 has holes that let a stalled worker pass or hang
- Step 2 passes when `observation.agentWait` is "never non-null" (`spec:193`). The capabilities inventory says a null value means Orca looked and found no wait, while an absent field means it never looked, and that absence is not proof (`CAPS:125`, `CAPS:129`). A worker parked on a prompt reads as a pass whenever the field is absent.
- Step 3 loops `check --wait` "until `worker_done` arrives" (`spec:194`) with no stop rule. The spec itself says the real failure mode is a silent stall with no `worker_done` (`spec:44`) and that Orca's total run-time bound is unknown (`spec:315`, `CAPS:188`). A stalled worker hangs the acceptance run.
- Step 5 only searches for `AskUserQuestion` (`spec:196`); WC-2 also forbids ending a turn on a chat question, and AC-0.4 says the "no Agent-tool wrapper" fact is "verified in the step-5 transcript" (`spec:206`) although step 5 has no such pass condition.
- Recommendation: require `agentWait` present and null; add a deadline and a stop action (`worker-show`, then fail the check); add a pass condition to step 5 for an Agent-tool wrapper and for a final chat question. Priority: Medium. Impact: Testability.

### M-7 (Medium, Cockburn + Nygard) Roles and scope not covered: handling of a `blocked` outcome, and propagation to nested skills
- 2.3 says what the brief contains but not what the coordinator does after `worker_done --outcome failed` with `status: blocked` (`spec:73`). The only answer path is the worker's own `ask` (WC-3); otherwise the coordinator needs a new dispatch carrying the answer flag. The retry path `worker-start --retry-of` is cited at `spec:64` but is not tied to this case. Briefs and phases never say how a blocked Task is answered.
- WC-2 binds "the command" but nested skill invocations also hold gates (brainstorm to adversarial, release-split to brainstorm, task TFEP to troubleshoot, workflow Wave 4 to reflect; `INV-B:119`, `INV-B:204`, `INV-B:269`). Only tasklist to reflect gets an explicit pass-through (`spec:122`).
- Recommendation: add one sentence to 2.3 for the blocked path, and one rule in WC-2 that `--unattended` is passed to every Skill-invoked child that has a gate. Priority: Medium. Impact: Completeness.

### M-8 (Medium, Wiegers) Phases 1 to 3 are said to need no user decision, but two P3 rows leave the choice open
- `spec:154` and `spec:258` say Phases 1-3 need no decision. The roadmap, validate-roadmap and validate-tests rows say "reconcile" without naming the winner (`spec:118`, `spec:124`, `spec:125`), while the inventory records that no file says which side wins (`INV-B:309`). AC-3.1 accepts either direction (`spec:216`). business-panel's frontmatter move has an UNVERIFIED effect on loading (`spec:102`, `spec:311`).
- Wrong outcome: two implementers reconcile in opposite directions, each passing AC-3.1; one may remove a flag people use today, against SA-1.
- Recommendation: name the winning side per pair, or move these rows to D-decisions. Priority: Medium.

=== ARCHITECTURE ANALYSIS ===

### M-9 (Medium, Fowler + Newman, Nygard) Worker form is assumed to be a terminal, against the evidence the spec cites
- `spec:16`, `spec:59` and `spec:65` describe a worker as a top-level session "in its own Orca terminal" and rely on a TTY-style reading (UNVERIFIED #9, `spec:313`: reflect's headless signal is `claude --print` with no TTY). The capabilities inventory states "Not every worker has a terminal... A spec must not assume a worker is a PTY" and that how the worker runs follows the user's own setting (`CAPS:139-140`).
- Wrong outcome: if a worker runs as a chat session, the reflect headless-rule assumption, the `ORCA_TERMINAL_HANDLE` reasoning in D1(b) (`spec:262`) and the "terminal" wording of the P0 smoke runs may not hold.
- Recommendation: restate the contract without "terminal", and add one P0 smoke condition that records whether the worker was a terminal or a chat. Priority: Medium.

### M-10 (Medium, Nygard) WC-10 cannot be met by Agent-tool fan-out, and its basis for pr-submit is not checkable here
- WC-10 applies to "a command step that blocks a single tool call for longer than 5 minutes" (`spec:68`) but only cli-eval and pr-submit get a split (`spec:104`, `spec:114`). Fan-out commands whose single Agent call can run long (cleanup-audit waves, tdd, adversarial; `INV-A:42`, `INV-B:221`) have no remedy, and it is UNVERIFIED whether Orca even uses heartbeat age (`CAPS:130`, `CAPS:182`).
- The pr-submit claim that one iteration is "one foreground poll, then a sleep of at least `--poll-interval`" (`spec:68`, `spec:114`) has no support in any inventory (grep for "poll-interval" and "sleep" in the three inventory files finds nothing); the inventories say only "up to `--timeout` 600 s per wait over several rounds" (`INV-B:95`, `INV-B:299`). The default `--poll-interval` is not given, so "under 4 minutes per iteration" cannot be judged. The cited `sk/sc-pr-submit-protocol/SKILL.md:46-64` is outside the spec's own list of re-read locations (`spec:11`). Marked UNVERIFIED.
- Also: pr-submit states "Will Not: run headless / imply a daemon" (`INV-B:90`); D3(b) and the pr-submit row (`spec:114`, `spec:274`) do not address whether an unattended worker conflicts with that line.
- Recommendation: say WC-10 applies to commands that wait in loops only, state that long Agent calls are accepted, and add the poll-interval default to UNVERIFIED #12. Priority: Medium.

### M-11 (Medium, Fowler) Tasklist nesting claim does not match its own source
- `spec:122` says tasklist's reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" and needs no change. The inventory found that Stage 10.5 dispatches N Agent-tool subagents that each run `/sc:reflect`, which spawns its own agents (and at Tier 2, reviewers plus adversarial), so reflect's agents sit two or more layers below the worker, and it is UNVERIFIED whether that nested spawning works (`INV-B:210`, `INV-B:322`; limit text at `INV-A:14`). AC-2.2 marks tasklist "no gate fires" (`spec:238`) so no check exercises the nested path.
- Recommendation: replace "one layer below" with the inventory's UNVERIFIED wording, and make AC-2.3 for tasklist require one reflect result inside the contract artifacts. Priority: Medium.

### M-12 (Medium, Hohpe + Crispin) Test scope for Phase 0 is narrower than the files it changes
- P0 edits `install_core.py` (`KNOWN_CORE_FILES`), `HOW-WE-WORK.md`, its two mirrors and the level table in `core/CLAUDE.md` (`spec:52`, `spec:158`, `spec:150`), but AC-C3 runs only `uv run pytest tests/skills/` (`spec:186`). Installer and routing-guide tests may live elsewhere (UNVERIFIED: no test tree in this sandbox), and the repo's own command is the full suite (`make test`, per the project instructions).
- Recommendation: run the full suite, or add `tests/cli` and the level-table test paths to AC-C3. Priority: Low-Medium.

## Minor notes (never fail the review)
- N-1. The spec cites review labels it does not define: M1, M2, M4, M5, M6, M7 and N1 (`spec:62`, `spec:79`, `spec:147`, `spec:207`, `spec:225`, `spec:298`). They point at a disposition file that is not part of the document, so a reader of the final spec cannot resolve them. Inline a one-line meaning or drop the tags.
- N-2. E3 says "it has worked before" with the PR #329 run as evidence (`spec:23`), while 1.4(1) says that run proves only the nested route (`spec:43`) and UNVERIFIED #1 says no direct run was seen (`spec:305`). The wording of E3 is stronger than section 1.4; soften E3.
- N-3. SA-3 allows the contract when "the caller passes the new output flag" (`spec:148`), WC-4 says only "in unattended mode" (`spec:62`). One rule, please.
- N-4. P0 smoke runs cannot pass `--unattended` (it does not exist yet), but 2.3 says every brief includes it (`spec:73`, `spec:158`). Say that the P0 brief omits it.
- N-5. WC-9 lists "calls a paid external run" (`spec:67`) without saying whether web search (research, recommend `--plugin`, review-translation; `INV-B:104`, `INV-B:134`) counts. State yes or no.
- N-6. `/sc:reflect` runs a default folder move and writes a tracked memory file (`INV-B:114`); the spec offers `--no-promote` only as a brief choice (`spec:88`), not as an unattended default. Consider listing it under WC-9 or WC-11.
- N-7. The directory of 43 commands is taken from the two inventory scope lines (`INV-A:3`, `INV-B:3`), not from a listing of `cmd/` (`spec:76`). Whether `cmd/` holds more files than these 43 is UNVERIFIED here (this session's own skill catalog also lists `sc:graph`, `sc:impact` and `sc:issue`, which neither inventory covers); add the `ls` command and its result as a citation.
- N-8. UNVERIFIED (no file to check): the `CLAUDE.md:N` citations (`spec:34`, `spec:52`, `spec:147`, `spec:150`, `spec:204`, `spec:272`), the `.dev/evals/...` and `.dev/codegraph-migration/...` citations, and every `sk/`, `cmd/`, `ag/` line the inventories do not themselves quote. The spec's own check covers 11 locations and a later validator pass (`spec:11`, `spec:318`); I could not repeat it.

## Guard Condition Boundary Table

Guards identified in the spec: the outcome mapping (WC-5), the heartbeat wait (WC-10), the readiness limit (WC-1), the depth limit (WC-8), the task confidence threshold, and three regex checks (AC-C1, AC-C5, 7.2 step 2). Classes left out per guard are named in the "Omitted" line under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome mapping | spec:63 | Zero/Empty | no report file, or empty file | failed branch | `--outcome failed` ("or no report exists") | OK |
| WC-5 outcome mapping | spec:63 | One/Minimal | `status: partial` | succeeded branch | `--outcome succeeded`, body names `partial` | OK |
| WC-5 outcome mapping | spec:63 | Typical | `status: succeeded` | succeeded branch | `--outcome succeeded` | OK |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match | `status: blocked` after an answered `ask` | failed branch | `failed`; behavior after the answer, and which dir holds the new contract, unspecified (M-4) | GAP (Medium) |
| WC-5 outcome mapping | spec:63 | Legitimate Edge Case | audit verdict FAIL | succeeded branch | `succeeded` (stated) | OK |
| WC-10 wait split | spec:68 | Zero/Empty | wait of 0 s | no split | no rule needed | OK |
| WC-10 wait split | spec:68 | Typical | 240 s | split not needed | under heartbeat cadence | OK |
| WC-10 wait split | spec:68 | Maximum/Overflow | one Agent-tool call of 20 min | cannot be split | no remedy stated (M-10) | GAP (Medium) |
| WC-10 wait split | spec:68 | Legitimate Edge Case | exactly 300 s | ">5 minutes" is false at 300 | heartbeat due at 300 s but the rule splits only above 5 min | GAP (note, boundary off by tolerance) |
| WC-1 readiness limit | spec:59 | Maximum/Overflow | prompt fallback of 45 s or more | fails at 60 s default | stated: fallback "well inside" the limit, evidence 30 s passes, about 45 s fails | OK |
| WC-1 readiness limit | spec:59 | Sentinel Value Match | `--timeout-ms` set to 0 or negative | default 60 s | `CAPS:44` (positive finite only) | OK |
| Depth limit / WC-8 | spec:66 | Typical | depth 1 worker calls `worker-start` | refused | `nested_worker_depth_exceeded` (`spec:33`) | OK |
| Depth limit / WC-8 | spec:66 | Legitimate Edge Case | depth 1 worker calls `task-create` | unknown | UNVERIFIED, forbidden anyway (`spec:309`) | OK |
| task confidence guard | spec:121 | Typical | 0.50 | true | blocked | OK |
| task confidence guard | spec:121 | Legitimate Edge Case | exactly 0.70 | false ("below 0.70") | proceeds; follows the command's own band | OK |
| AC-C5 regex `^-[^-]` | spec:188 | Legitimate Edge Case | deleted bullet `- item` (diff line `-- item`) | false (no match) | check passes although a line was deleted | GAP (Medium, M-1) |
| AC-C1 regex | spec:176 | Legitimate Edge Case | `orca ask ...` or `orca-ide skills get` in a command | false (no match) | scan prints nothing although SA-2 is broken | GAP (Medium, M-5) |
| 7.2 step 2 agentWait | spec:193 | Zero/Empty | field absent (Orca never looked) | "never non-null" is true | counts as pass (`CAPS:129`) | GAP (Medium, M-6) |
| 7.2 step 3 wait loop | spec:194 | Maximum/Overflow | worker never sends `worker_done` | loop continues | no stop rule | GAP (Medium, M-6) |

Omitted classes, with reason: WC-5 Maximum/Overflow (a status value has no capacity); WC-10 Sentinel (no sentinel in a duration); WC-1 Zero/Empty (a 0 s limit is the sentinel case above); depth guard Zero/Empty and Maximum (the setting falls back to 1 for any non-whole value, `CAPS:100`); confidence guard Sentinel and Maximum (range 0 to 1, no sentinel); the three regex checks have no Maximum class.

FR-8 / FR-9 / FR-10: every GAP above is Medium (graded by consequence; none names a data-loss or safety-boundary outcome that follows from the stated text alone), none blocks. No row has a blank Specified Behavior. The table is complete for the guards listed, so synthesis is not blocked.

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

Trigger: the rollout is a multi-stage pipeline in which the count of commands differs between stages (filter at section 4, split by phase, plus the tasklist fan-out of N phases).

```text
[Source: 43 commands in cmd/ (INV-A:3 = 21, INV-B:3 = 22)]
   --> [Stage 1: classify]  --> 10 ready + 27 needs change + 6 coordinator-only = 43   (conserved)
   --> [Stage 2: drop coordinator-only (section 4)] --> 37 dispatchable            (43 -> 37, N != M)
          |
          v
   [Stage 3: phase assignment (section 6)]
          P0: 2 smoke runs (troubleshoot, workflow)                  consumer: AC-0.4 expects 2
          P1: 9 changed (3.2, P1) + 4 fixes (3.1) in table           consumer A, section 6 table: 13
              flag + section + contract on all of 3.1 + P1 of 3.2    consumer B, spec:79/207: 10 + 8 = 18 (load exempt)
              flag on "every command in 3.1 and 3.2"                 consumer C, spec:159: 37   <-- MISMATCH (M-2)
          P2: 11 (3.2) + 4 (3.1) = 15                                consumer: AC-2.2 table 15 rows   (matches)
          P3: 4                                                       consumer: AC-3.1..3.4           (matches)
          P4: 3                                                       consumer: AC-4.1..4.3           (matches; AC-4.3 conditional on D3)
   --> distinct commands touched: 27 + 10 = 37                        (conserved against Stage 2)
```

Mismatch: Stage 3, Phase 1 has three consumers with counts 13, 18 and 37. Concrete scenario: an implementer builds the 13 named in the section 6 table; AC-1.1 then expects 18 commands to carry the section and fails on brainstorm, init-lite, reflect, release-split, tdd and troubleshoot. FR-19 labels a dimensional mismatch CRITICAL; graded by consequence it is Medium (M-2), because AC-1.1 catches the shortfall before anything ships and the broad reading of 37 needs the implementer to ignore `spec:207`.

Other flows checked: tasklist's N phases give N reflect runs (`INV-B:211`), accounted for in `spec:122` but with the wrong nesting depth (M-11). Workers to reports to `worker_done`: one worker, one report, one `worker_done` (WC-5); conserved.

## Whittaker adversarial notes (active in every review)
- Zero/Empty: empty contract file (`test -s` catches it), `None` from `yaml.safe_load` (step 4 raises, fails correctly), empty `blocked_question` (checked only in the AC-2.2 table, not in step 4; note).
- Divergence: `partial` and a FAIL verdict both map to `succeeded` (`spec:63`); a coordinator that reads only the outcome treats a partial result as done. The body sentence mitigates; low risk.
- Sentinel collision: `status: blocked` is a control signal and also appears in user data fields; no collision found in the stated schema.
- Sequence: blocked, then `ask`, then re-run into a fresh dir leaves a stale blocked contract at the path the brief promised (M-4). A second `worker_done` is excluded by WC-5 and WC-12.
- Accumulation: no cap on `check --wait` iterations (M-6); no cap on Agent fan-out inside a worker (accepted by the spec, `spec:45`).

## Follow-up candidates (Medium and minor; none triggers a revision)
- Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12
- Minor notes: N-1, N-2, N-3, N-4, N-5, N-6, N-7, N-8
- Per the command, the session that ran the review asks the user once whether to open an issue for these; I create none and I cannot ask the user in this sandbox. Recorded only.

## Reviser brief
No blocking finding is open, so there is nothing to revise. Revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Blocking ids: none.

verdict: PASS
