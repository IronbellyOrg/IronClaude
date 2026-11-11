review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Kind: labelled whole-document audit, first review of the final spec. No `--re-review` or `--baseline` was given, so no `baseline: missing` note applies.
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, SHA-256 `84aa3fdce83498845e1a3cf58e05e4b1f83a15e38b34520e6f0393658bd74d26`. Baseline: none.
- Reviewer model used: `claude-sonnet-5-5`.
- Prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before reviewing; the grading check below was applied to every finding marked blocking).
- Brief clauses overridden: none. The brief narrowed nothing and widened nothing.
- Panel (command order, active for the requirements and architecture focus plus the always-on adversarial seat): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe. The focus area `correctness` was not requested, so the State Variable Registry is not produced.
- Candidate lines are written `spec:N`. Inventory lines are `INV-A:N`, `INV-B:N`, `CAPS:N`, `README:N` (all under `.dev/orca-command-refactor/`).

## Coverage
Read in full: the candidate (285 lines), `README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`.

Checked against those inventories: the 43-command split (10 ready + 27 needs-change + 6 coordinator-only; rows counted in `spec:81-92`, `spec:97-125`, `spec:131-137`; inventory totals `INV-A:73`, `INV-B:278` add up to the same 10/27/6), every `INV-A:N`, `INV-B:N`, `CAPS:N` and `README:N` pointer I could resolve (about 90; none pointed at the wrong line), and each row's verdict against its inventory verdict.

Not checkable in this sandbox, so UNVERIFIED: every direct citation of `src/superclaude/...` (`cmd/`, `sk/`), `CLAUDE.md`, `Makefile`, `pyproject.toml`, `src/superclaude/cli/install_core.py`, `HOW-WE-WORK.md`, `.dev/codegraph-migration/...`, `EVIDENCE.md` (only seen as quoted in `CAPS:44-52`) and `orca-data.json`. That includes `spec:11` (11 locations re-read) and `spec:285` (about 340 citations validated), which are self-attestations I could not repeat. Every finding below rests on the candidate text and on inventory lines I read.

## Verdict summary
3 blocking findings (B1 to B3), 14 Medium findings and 3 minor notes. Verdict: FAIL.

## Prior blocking findings
None (first review, no prior-findings table).

=== REQUIREMENTS ANALYSIS ===

### B1 - WC-3 lets a coordinator's reply stand in for confirmation that three source rules reserve for the person
- Severity: CRITICAL. Experts: Wiegers (lead), Nygard, Whittaker (Sequence attack). Priority: High. Quality impact: Consistency -2, safety.
- Location: `spec:61` (WC-3) against `spec:109` (implement row), `spec:208` (AC-4.1), `spec:218` (non-goal 6), `spec:232-236` (D2), `spec:121` (task row).
- Grading check: an implementer who follows WC-3 as written builds a worker that, when a gate "would resolve as blocked", asks the coordinator once and then "re-invoke[s] or resume[s] the command with the answer as a flag". That is wrong because `/sc:implement` accepts a Ruling only from "clear user confirmation in the current conversation" and says "another agent's message" is not acceptance (`INV-A:51`, `INV-A:66`), and the spec itself says "An Orca coordinator is another agent" (`spec:233`), keeps that rule as the recommendation (D2(a), `spec:234`, `spec:236`), states changing it is a non-goal unless the user picks D2(b) (`spec:218`), and tests that no Ruling is recorded (AC-4.1, `spec:208`). WC-3 has no carve-out, so the contract file written in P0 (`spec:158`) already permits the relay that D2 reserves for the user.
- The same text lets a coordinator override `/sc:task`'s "Will Not: Proceed with <70% confidence without user confirmation" (`INV-B:199`, `INV-B:205`) by answering the blocked question and passing a compliance flag; the task row only says "resolves as blocked" (`spec:121`).
- Whittaker: I can break this specification by **Sequence attack**. The invariant at **WC-3 / D2** fails when **`/sc:implement` halts with `E-HALT-QA` in a worker holding a preamble**. Concrete attack: before: ledger records halt, contract `status: blocked`, no Ruling. Step 1: worker asks the coordinator (WC-3 permits). Step 2: coordinator replies "approved". Step 3: worker re-invokes with the answer. After: Ruling recorded from an agent message; D2(a) and AC-4.1 are false although no user decision was taken.
- Recommendation: narrow WC-3 to gates whose source rule does not require the person's own words, and name the exceptions (implement Ruling, task below 0.70, any outward action, per D2 and D4); otherwise require the relayed answer to quote the person verbatim and be recorded as such. Deleting the sentence "re-invoke or resume the command with the answer as a flag" for those gates is enough.

### B2 - cli-portify cannot pass its own happy-path acceptance check, because no approval input exists in the spec
- Severity: CRITICAL. Experts: Wiegers (lead), Adzic, Crispin-style testability (Wiegers shift). Priority: High. Quality impact: Testability -2.
- Location: `spec:105` (cli-portify row), `spec:200` (AC-2.2), `spec:201` (AC-2.3), `spec:160` (P2 list includes cli-portify).
- Grading check: an implementer who follows the cli-portify row as written builds an unattended mode in which "each of the three approval gates resolves as blocked", with the only other changes being a `--resume <contract>` flag and a contract file; no flag or input that pre-approves a gate is defined anywhere in the row or in section 2. That is wrong because AC-2.3 demands a "Happy-path run per P2 command with every required flag in the brief" that passes "with `--outcome succeeded`" (`spec:201`), and AC-2.2 itself names "a run with no approval input" as the blocked trigger (`spec:200`), which presupposes an approval input the row never defines. The three gates are "always on" (`INV-A:45`), so with the row as written every unattended cli-portify run ends `blocked` at the first gate and AC-2.3 cannot pass.
- Recommendation: either define the approval input per gate (flag names, as `--target-release` is for spec-panel) or remove cli-portify from AC-2.3 and state in the row that it is blocked-only until the user decides.

### B3 - Phase 1 ships `--unattended` and the "Unattended mode" section on commands whose gate resolutions, GitHub-post-off default and decisions arrive only in P2 and P4
- Severity: CRITICAL. Experts: Fowler (lead), Newman (versioning/sequence), Nygard. Priority: High. Quality impact: Consistency -2, safety.
- Location: `spec:159` (P1 scope), `spec:195` (AC-1.1), `spec:76` (section 3 intro), `spec:73` (section 2.3), `spec:67` (WC-9), `spec:100` (auggie-review row), `spec:160` and `spec:162` (P2, P4), `spec:241` and `spec:240` (D3), `spec:154` and `spec:225`.
- Grading check: an implementer who follows P1 and AC-1.1 as written builds `--unattended` plus an `## Unattended mode` section naming only `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` on every command of sections 3.1 and 3.2, including auggie-review, cli-portify, implement, post-release and pr-submit, "a no-op where a command has no gate" (`spec:159`). That is wrong because section 2.3 tells the coordinator to put `--unattended` in the brief "from P1 on" (`spec:73`) and WC-9 says that under `--unattended` the GitHub-posting default is off (`spec:67`); until P2 lands, `/sc:auggie-review <PR> --unattended` still posts a PR review with no prompt (`INV-A:38`). For pr-submit the P1 section also contradicts D3(a), "no pr-submit changes in Phase 4" (`spec:240`), because the command would carry an unattended contract before the user decides whether it is a worker at all.
- Divergence attack (Whittaker): the boundary between P1 and P2 is a state where the flag exists and its documented meaning (WC-2, WC-9) is false for 15 commands.
- Recommendation: add the flag and the section to a command in the same phase that implements its gate resolution (or have AC-1.1 cover only the P1 commands and the 3.1 ready commands); state that `--unattended` on a not-yet-converted command is refused, not ignored.

=== ARCHITECTURE ANALYSIS ===

No architecture finding reaches blocking. The central decision (Orca on top, commands stay units of work, `spec:13-45`) is supported: the rejected alternative rests on checkable facts (`CAPS:97-103`, `CAPS:147-150`, `CAPS:145`, `INV-A:90`, `INV-B:285-286`), and the spec states the weak points plainly (`spec:41-45`). Fowler/Newman/Hohpe/Nygard notes on interfaces and sequencing are in the Medium list below (M4, M5, M7, M13, M15).

## follow-up candidates (Medium and minor; none triggers a revision, none is in the Reviser brief)

Medium (warnings):

- **M1 - Heartbeat threshold stated three ways.** WC-10 splits waits "longer than 5 minutes" into waits "of at most 4 minutes" (`spec:68`); the pr-submit row and the Decisions row use 4 minutes (`spec:114`, `spec:266`); AC-4.3 fails any call over 240 s (`spec:210`). A 4.5-minute step passes WC-10 and fails AC-4.3, and a 4.9-minute call started 1 minute after the last heartbeat leaves a 5.9-minute gap. Wiegers/Nygard. Fix: one threshold (4 min) in WC-10.
- **M2 - "Fresh output directory" has no mechanism on retry.** WC-6 says commands without resume "write each run into a fresh output directory" (`spec:64`), and 16 rows use "fresh dir" (`spec:99-125`), but section 2.3 has the coordinator pass the directory in the Task brief (`spec:73`); a `--retry-of` worker re-reads the same brief and writes into the first attempt's directory. Needs the reading "coordinator passes a new directory on retry" or a command-side subdirectory rule. Fowler/Nygard.
- **M3 - Status vocabulary of existing contracts unchecked.** WC-5 maps any status outside `succeeded/partial/failed/blocked` to `--outcome failed` (`spec:63`), while WC-4 says contracts that already exist "keep their fields" (`spec:62`); the vocabularies of the workflow, brainstorm, reflect and adversarial contracts are not listed (`INV-B:272` names `status` only), so a good run could map to `failed`. UNVERIFIED until the four ref files are read. Wiegers.
- **M4 - P0 order contradicts section 1.4.** Section 1.4 says "Phase 0 therefore starts with live smoke runs" (`spec:43`); section 6 builds the contract file, the routing-guide section and the test file first and runs the smoke runs "Then" (`spec:158`), while claiming they "test the decision before anything is built on it" (`spec:158`). AC-0.4 says a failure "reopens section 1" (`spec:194`) after the guide edits exist. Fowler.
- **M5 - AC-C1 can fail on text SA-2 allows.** SA-2 permits an Orca mention "as an example of a caller's question channel inside the contract file" (`spec:147`), and P0 adds an Orca section to `HOW-WE-WORK.md` (`spec:158`, `spec:150`); AC-C1 greps `src/superclaude/core` for `orca (orchestration|worktree|terminal|agent)` and requires no output in every phase (`spec:172`). A natural example such as `orca orchestration ask` fails the check. Fix: exclude those two files in AC-C1 or require uppercase `ORCA` placeholders. Nygard/Adzic.
- **M6 - WC-11 against fixed output paths.** WC-11 says two workers in one worktree must never write the same file (`spec:69`); cleanup-audit keeps a fixed `.claude-audit/` directory and the row accepts "one audit per worktree at a time" (`spec:85`), index-repo writes one `PROJECT_INDEX.md` whose location is "implied" (`spec:86`, `INV-A:53`, `INV-A:117`). Row text should say these are serialized by the coordinator or give them a per-run path. Newman.
- **M7 - AC-2.2 ignores the WC-3 ask path.** AC-2.2 expects `worker_done --outcome failed` with `blocked` and no `agentWait` (`spec:200`), but WC-3 lets the worker `ask` instead (`spec:61`); 7.2 step 3 then waits for `question` with a 900 s timeout and no coordinator reply is specified (`spec:182`). The result depends on which path the worker picks. Crispin/Hohpe.
- **M8 - Other inputs named but not defined.** review-translation needs "a pre-confirmed context input" (`spec:117`) and post-release "an explicit pre-tag choice" (`spec:113`); neither gets a flag name. Same family as B2, but each has a documented fallback (`blocked`), so no acceptance check is unreachable. Cockburn/Wiegers.
- **M9 - `--unattended` with `--interactive` is undefined where the row only says "never --interactive".** adversarial, brainstorm and release-split rows tell the coordinator not to pass it (`spec:83`, `spec:84`, `spec:89`), but only cleanup, improve, roadmap, business-panel, explain and test state a refusal; a brief that passes both has no specified result. Whittaker (Divergence).
- **M10 - `--unattended` without an output directory.** WC-4 writes the contract in "the directory the coordinator passed" (`spec:62`) and promises a write "on every outcome, including stops before any other output exists"; with no directory passed (or an unwritable one) there is nowhere to write, and the spec does not say the command must stop and print. WC-5 degrades this to `failed` (`spec:63`), so impact is a silent failure, not a wrong outcome. Whittaker (Zero/Empty).
- **M11 - AC-0.4 step 4 for adversarial has no named file.** It tests "the command's existing report file" (`spec:194`), but the adversarial row says the contract filename is not fixed until P1 (`spec:83`, `INV-A:35`, `INV-A:60`); the merged-output filename is not given. Adzic.
- **M12 - WC-1 "well inside the limit" is not measurable.** The evidence gives 30 s passing and about 45 s failing (`CAPS:49`, `spec:59`); the requirement states no number. Owner is launch setup, outside the 43 commands. Wiegers.
- **M13 - tasklist row departs from its inventory.** INV-B recommends dropping `--remediate` in Stage 10.5 (`INV-B:215`, `INV-B:295`); the row instead passes `--unattended` to each reflect so the headless auto-accept rule applies (`spec:122`), while UNVERIFIED item 9 admits an Orca worker is probably not headless (`spec:280`, `INV-B:315`) and the reflect row separately advises "no `--remediate`" (`spec:88`). The consequence (remediation auto-accepted in N subagents, extra packages outside the contract's `artifacts`) is not stated. Fowler/Newman.
- **M14 - pr-submit wait semantics re-read against the inventory.** The spec says the 600 s default is a cumulative per-wait budget over short iterations (`spec:68`, `spec:114`); the inventory says "600 s per wait" (`INV-B:95`, `INV-B:299`). The spec's source lines are not checkable here (UNVERIFIED). If the inventory is right, WC-10 splitting is required and the row's "already can heartbeat" claim is wrong. Nygard.

Minor notes:

- **n1.** Evidence E3 cites `invocation_method: "skill-direct"` as support (`spec:23`) while section 1.4 says that run went through an Agent-tool subagent and "proves the nested route" (`spec:43`); the two are reconcilable but read as opposed.
- **n2.** `README:31` is a rule for this planning run; it is cited as standing policy for `/sc:git` and for WC-9 (`spec:67`, `spec:133`).
- **n3.** `spec:154` says "Phases 1-3 need no user decision" while `spec:225` says "Phases 0-3 can proceed on the recommendations"; D4 touches auggie-review and task, which are P2 (`spec:244`).

## Guard Condition Boundary Table
Trigger present (thresholds, boolean guards, a mode switch, status sentinels). Nygard built it, Crispin checked completeness, Whittaker attacked entries. Classes left out are listed with a reason after the table. A GAP is graded by consequence: none of the GAP rows below names a concrete wrong outcome without a further guess, so each is Medium (see M-ids) except where tied to B1 to B3.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` token | `spec:16`, `spec:51`, WC-2 | Zero/Empty | flag absent | false | SA-1: every prompt and default unchanged (`spec:146`) | OK |
| `--unattended` token | WC-2, `spec:76` | One/Minimal | flag on a command with no gate | true | no-op plus contract (`spec:159`) | OK |
| `--unattended` token | WC-2, P1 vs P2 | Typical | flag on a gated command before its phase | true | contradicts WC-9 (B3) | GAP |
| `--unattended` + `--interactive` | `spec:83-89` | Legitimate Edge Case | both flags | both true | refusal stated for 6 commands only (M9) | GAP |
| contract `status` | WC-5 `spec:63` | Zero/Empty | empty or unparseable file | outcome `failed` | `failed` | OK |
| contract `status` | WC-5 | One/Minimal | `partial` | outcome `succeeded` | `succeeded`, body says partial | OK |
| contract `status` | WC-5 | Sentinel Value Match | `blocked` | outcome `failed` | `failed`; WC-3 ask path conflicts (B1, M7) | GAP |
| contract `status` | WC-5 | Legitimate Edge Case | existing contract using another word | outside the four | `failed` (M3) | GAP |
| wait length | WC-10 `spec:68` | Typical | 2 minutes | no split | no split | OK |
| wait length | WC-10 | Maximum/Overflow | 4.5 minutes | not over 5, no split | allowed; AC-4.3 fails it (M1) | GAP |
| wait length | WC-10 | Legitimate Edge Case | exactly 5 minutes | not "longer than" | no split; heartbeat gap up to 5.9 min (M1) | GAP |
| readiness limit | WC-1 `spec:59` | Maximum/Overflow | fallback over about 45 s | fails | evidence only, no number in rule (M12) | GAP |
| task confidence | `spec:121` | Sentinel Value Match | exactly 0.70 | not below 0.70, proceed | "below 0.70" is blocked; 0.70 proceeds | OK |
| task confidence | `spec:121` | Typical | 0.50 | blocked | blocked, but coordinator answer overrides (B1) | GAP |
| nesting depth | R1 `spec:33` | Typical | depth 1 | worker cannot start workers | refused, `CAPS:99` | OK |
| output dir | WC-4 `spec:62` | Zero/Empty | none passed under `--unattended` | no path | not specified (M10) | GAP |
| fresh dir on retry | WC-6 `spec:64` | One/Minimal | second attempt, same brief | same directory | not specified (M2) | GAP |
| `check` result | WC-12 `spec:70` | Legitimate Edge Case | `consumer_fenced` | stop | no `worker_done` | OK |

Classes left out: Maximum for `--unattended`, nesting depth and `check` (a boolean or fixed value cannot overflow); Sentinel for `--unattended` and readiness (no reserved value); Zero for nesting depth (root coordinator is depth 0 and starts no worker, `CAPS:97`).

## Pipeline Dimensional Analysis
Trigger evaluated: the spec describes no data pipeline whose stage output counts differ, but it has count-bearing sets; their conservation was checked (Fowler, Whittaker).

```text
[43 commands: INV-A 21 + INV-B 22] --> [classify] --> [10 ready (3.1)] + [27 needs change (3.2)] + [6 coordinator-only (4)] = 43   N = M, conserved
[P2 list: 15 commands] --> [AC-2.2: 9 blocked-path] + [AC-2.3 default-path 6: auggie-review, cleanup, improve, research, reflect, tasklist] = 15   conserved
[P1 flag scope: 3.1 + 3.2 = 37 commands] --> [AC-1.1: 36 (load exempt)]   divergence of 1, stated (M10 note in spec:195)
[AC-2.3 happy path: 15 P2 commands] --> [cli-portify has no succeeding input]   14 reachable (B2)
```

No count mismatch beyond B2 was found.

## Adversarial summary (Whittaker)
- Zero/Empty: M10 (no output directory), M3 (empty status vocabulary check).
- Divergence: B3 (P1 vs P2 states), M9 (`--unattended` with `--interactive`).
- Sentinel collision: `blocked` is both a contract status and a Task-level concept; B1 (blocked then answered by an agent).
- Sequence: B1 (ask then re-invoke), B3 (flag before gate), M4 (build before smoke test).
- Accumulation: M1 (heartbeat gap accumulation across split waits).

## Expert consensus and disagreement
Consensus: the decision and the rejected alternative are sound and well evidenced; the inventory pointers are accurate where checkable. Remaining disagreement: Wiegers and Nygard want WC-3 narrowed now; Fowler would keep WC-3 general and fix D2 instead. Resolved in B1 in favor of narrowing WC-3, since D2 and AC-4.1 already treat the rule as fixed.

## Quality scores (0-10)
Clarity 8, Completeness 7, Testability 6 (B2, M1, M7, M11), Consistency 6 (B1, B3, M1, M4, M5).

## Reviser brief
Blocking finding ids: B1, B2, B3. Restated contract (the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M1 to M14, n1 to n3) alone; do not award a PASS.

follow-up candidates: M1 to M14, n1 to n3 above. The session that ran this review has no user to ask whether to open an issue for them; none was created.

verdict: FAIL
