review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (critique, requirements + architecture)

## Header
- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (run by a worker acting as the command; no slash command available).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d33b89a08efc2ef08e5a0449828d8b35251424cc7d54958dac98f929b1383529`.
- Baseline: not given (first review of the whole document; no `--re-review`, so no `baseline: missing` note needed).
- Reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`).
- Review type: labelled whole-document audit of the final spec. Prompt followed: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- Panel (fixed order, critique mode): Wiegers, Adzic, Cockburn (requirements lead set), Fowler, Nygard, Whittaker (always active), Newman, Hohpe (architecture set). Crispin, Gregory and Hightower not used (`testing`/`compliance` not requested).
- Citation shorthand: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. Anything I could not open inside the workspace (`src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/`, Orca output) is marked UNVERIFIED.

## Coverage (what I did)
- Read the whole candidate (291 lines), `README.md`, all three inventories (the only checkable evidence), and `command.md` in full.
- Checked every `INV-A:`, `INV-B:` and `CAPS:` citation in sections 1, 2, 3, 4 and 9 against the inventory text. All resolve to the stated rows or notes. One is imprecise (M-07). The per-command verdict counts reproduce: INV-A 5/13/3 plus INV-B 5/14/3 gives 10 ready / 27 needing change / 6 coordinator-only (S:76), and the section 3.1 and 3.2 row counts are 10 and 27.
- Re-derived the phase counts: P1 = 15 (9 rows in 3.2 plus 6 in 3.1), P2 = 15, P3 = 4, P4 = 3, coordinator-only 6, total 43 (S:156-162).
- Ran the AC-C5 grep pattern on a throw-away pair of files inside the sandbox to test it (F-03).
- Not covered: source files under `src/superclaude/`, `EVIDENCE.md`, the codegraph run, Orca itself. Every spec claim that rests on them is UNVERIFIED here; the spec says the same for most of them (S:11, S:276-290).

## Blocking findings

| ID | Sev | Expert | Location | Status |
|---|---|---|---|---|
| B-01 | CRITICAL | Whittaker (sequence attack), Nygard | S:159 vs S:160, S:67, S:114, S:121 | open |
| B-02 | MAJOR (blocking) | Wiegers, Adzic | S:200 vs S:154, S:162, S:139, S:243-247 | open |
| B-03 | MAJOR (blocking) | Adzic, Whittaker (zero/empty attack) | S:176, S:198 vs S:149 | open |

### B-01. Phase 1 makes `--unattended` accepted by all 37 commands before the gates and outward defaults it promises are honoured
- Stated text: P1 adds "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (S:159). WC-2 and WC-9 say that under `--unattended` no gate waits and every pushing, posting or committing default is off (S:60, S:67). The section 3 rows put the actual resolutions in later phases: auggie-review posting, `/sc:task` `commit`/`push` and the committed TFEP report in P2 ("P2 only turns it off under `--unattended`", S:160, S:100, S:121), pr-submit HALTs and post-release in P4 (S:114, S:113, S:162).
- Grading sentence: An implementer who follows S:159 then S:160/S:162 as written ships, after P1, commands that accept `--unattended` and still post to GitHub (auggie-review, S:100; INV-A:38 shows the default posts with no prompt), commit and push (task EXEMPT keywords, S:121; INV-B:45) or ask a person (cleanup, improve, cli-portify, S:103/105/110). The coordinator brief (S:73) always puts `--unattended` on the command line, so the coordinator reads the flag as "safe, no person, no outward action". That behaviour is wrong because WC-9 is false in that state, and the effect is an outward action (a posted review, a push) on a command the brief believed was quiet.
- The spec never says a coordinator must not dispatch a command before its phase lands, and the P0 brief template lists only the section 3.1 flags (S:158), so nothing blocks the dispatch.
- Attack trace (Whittaker, sequence): State after P1 passes: auggie-review accepts `--unattended`, section says nothing yet. Step 1: coordinator dispatches `/sc:auggie-review 42 --unattended`. Step 2: command runs its default (post to PR, then wait on the remediation offer, INV-A:38, INV-A:62). Before: no review on PR 42. After: review and inline comments posted, worker stalled with no `worker_done`.
- Recommendation: until a command's resolutions land, it must refuse `--unattended` (fail closed with `status: blocked`), or P1 must limit the flag to the 15 commands whose full resolution lands in P1. Narrow, do not add a mechanism.

### B-02. The P1 acceptance check requires a `## Unattended mode` section on every command in 3.1 and 3.2, including the P2-P4 commands and a pr-submit section that D3(a) says must not exist
- Stated text: AC-1.1 (a P1 check) asserts that "every command in sections 3.1-3.2" has the section naming `~/.claude/WORKER-CONTRACT.md`, and each except `load` also names `return-contract.yaml` (S:200). Section 7.1 says a phase passes only when every check in its block passes (S:167). Section 6 says later phases do not start until the earlier checks pass (S:154), that Phases 1-3 need no user decision and that Phase 4 waits for D2-D4 (S:154, S:162). Section 3.2 gives implement, post-release and pr-submit as P4 (S:109, S:113, S:114). D3(a), the recommendation, is "no pr-submit changes in Phase 4" (S:245), and section 4 says pr-submit stays a worker candidate only if D3 is accepted (S:139).
- Grading sentence: An implementer who follows AC-1.1 as written builds, in P1, `## Unattended mode` sections for all 37 commands, including implement (its section must hold the halt resolution that D2 decides, S:109, S:237-241), post-release (D4) and pr-submit (D3). That is wrong because those sections encode decisions the same spec says wait for the user, and under D3(a) the pr-submit edit must not happen at all. The only way to make P1 pass without that is to change the check, so P1 cannot be closed by the text as written.
- Dimensional trace (Quantity Flow Diagram below): the AC consumer expects 37, the P1 stage produces 15 command edits.
- Recommendation: scope AC-1.1 to the commands the section 3 phase column assigns to P1, and let each later phase add its own assertion, as AC-2.1 and AC-3.1 already do for P2 and P3 (S:204, S:209).

### B-03. The additive-edit gate AC-C5 (and AC-0.3) cannot see a deleted markdown bullet
- Stated text: AC-C5 `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md | grep -E '^-[^-]'` must print nothing, "edits are additive" (S:176); AC-0.3 uses the same pattern for `HOW-WE-WORK.md` (S:198). SA-1 and SA-4 rest on it ("keeps the diff reviewable and SA-1 checkable", S:149).
- Verified in the sandbox with a throw-away pair of files: deleting the bullet `- Modify source` produces the diff line `-- Modify source`, and `^-[^-]` does not match it; only the deleted table row `-| row | x |` was reported. The pattern excludes every removed line whose content starts with `-`, that is every removed markdown list item, which is the dominant form in command files ("Will Not" lists, INV-A:41, INV-A:100).
- Grading sentence: An implementer who follows AC-C5 builds a gate that passes when an existing `Will Not` or other bullet is deleted. That is wrong because SA-4 requires existing lines to change only where section 3 names a defect fix, and AC-C5 is the only mechanical check of it (S:149, S:176).
- Recommendation: `grep -E '^-' | grep -vE '^--- '` (header lines are `--- a/...`), or compare with `git diff --numstat` deletions. Change only the pattern.

## Follow-up candidates (Medium and minor; never trigger a revision)

### Medium (warnings)
| ID | Expert | Location | Finding | Why Medium |
|---|---|---|---|---|
| M-01 | Wiegers | S:59 | WC-1 (no prompt before readiness) is owned by "launch setup, not commands" but no phase, file or acceptance check delivers it. The evidence for the 30 s fallback and the 45 s failure point sits in `EVIDENCE.md:45,56` (UNVERIFIED here). Step 1 of 7.2 only observes the result (S:185). | Requirement never delivered; needs a guess about which launcher a worker uses. |
| M-02 | Whittaker (zero/empty), Adzic | S:62, S:87, S:90, S:120 | The contract path is `<output-dir>/return-contract.yaml`, "the directory the coordinator passed" (S:62). For file-valued flags only init-lite defines it (dir of the `--output` file, S:87); tdd (`--output <file>`, S:90) and spec-panel (new `--output`, S:120) do not, and two file outputs in one directory would share one contract (WC-11, S:69). Also undefined: `--unattended` with no output flag at all (the real command in this run refuses before any work and prints in chat, `command.md:460`; the spec has no such rule). | Missing requirement, not a stated text that does harm. |
| M-03 | Fowler | S:62, S:64, S:87 | WC-4 fixes the report path "before dispatch"; WC-6 has 20-odd commands "write each run into a fresh output directory" (Owner: Command). Only init-lite says the retry brief passes the new directory (S:87). If the command makes its own subdirectory, the pre-dispatch path is wrong; if the coordinator does, 2.3 (S:73) does not say so. | Two readings allowed. |
| M-04 | Newman, Hohpe | S:90, S:121, S:52 | `--unattended` propagation to nested skills is not a rule. tdd's row relies on the `/task` skill's "ask the user" lines resolving as blocked (S:90, INV-B:47) and workflow, task (TFEP to troubleshoot), brainstorm and troubleshoot call other skills. `sk/task` and `sk/tdd` are not commands, so they have no section 3 row and AC-1.1 does not count them. Only tasklist passes the flag on explicitly (S:122). | Missing requirement. |
| M-05 | Whittaker (sentinel collision) | S:62, S:267 | WC-4 forces a four-value `status` onto contracts that "keep their fields" (adversarial, brainstorm, reflect, workflow). The existing status vocabularies are not in any inventory, so a collision with existing consumers (SA-1 "unchanged") is unchecked. UNVERIFIED. | Guess needed. |
| M-06 | Fowler, Nygard | S:122, S:88 | tasklist departs from the inventory's recommendation to drop `--remediate` (INV-B:46, INV-B:295) and instead auto-accepts remediation through reflect's headless rule. The row states "inside Claude Code's nesting limit, INV-A:14" for the N reflect subagents, but each reflect itself spawns agents (INV-B:46, INV-B:271) and INV-B:314 and INV-A:112 mark nested spawning UNVERIFIED. The departure is not in Decisions. | Premise unverified; harm not shown. |
| M-07 | Wiegers | S:61, S:237-241 | WC-3 says a Ruling gate "never takes a coordinator answer", while D2(b) allows exactly that if chosen and non-goal 6 conditions on D2 (S:223). WC-3 cites `INV-A:51-52` for the Ruling rule; INV-A:52 is the improve row, the rule is at INV-A:51 and INV-A:66. | Conditional on a pending user decision. |
| M-08 | Whittaker (accumulation) | S:63, S:268 | `blocked` maps to `--outcome failed` (WC-5), and a worker's own failed report does not trip Orca's circuit breaker (CAPS:80, quoted in S:268). Nothing caps coordinator re-dispatch of a worker that blocks every time on the same gate. | Missing restriction. |
| M-09 | Newman | S:69, S:73 | WC-11 covers output paths only. Commands that edit product files (cleanup, improve, document inline, test `--fix`, implement) share the worktree by default (CAPS:115), and 2.3 lists "worktree placement" without a rule for parallel editors. | Requirement never stated. |
| M-10 | Cockburn | S:25, S:76, S:172 | UNVERIFIED scope check: the skill list visible in this session names `sc:issue` (creates an Orca worktree), `sc:graph` and `sc:impact`, which are not among the 43 inventoried commands (INV-A:3, INV-B:3). If they exist in `src/superclaude/commands/`, E5 ("no command calls Orca") and the AC-C1 baseline ("prints nothing") are false. I cannot open `src/` to settle it. | Premise outside the workspace. |
| M-11 | Adzic | S:100-125 | Several rows say a flag is "refused" under `--unattended` (`--mode socratic`, `--interactive`, `--format interactive`, `--monitor 1`, `--watch`). WC-2 allows three resolutions (default, supplied flag, blocked); "refused" is none of them, and no contract status or exit is named. | Two readings. |
| M-12 | Crispin-style check (no testing focus) | S:199 | AC-0.4 step 3 applies to "the command's existing report file", but adversarial's file is "not fixed" (S:83, INV-A:60) and workflow's path contains a generated id (S:92). The step does not say the worker reports the located file and the coordinator opens it. A failure "reopens section 1". | Under-specified check. |

### Minor (notes)
- m-01 WC-10 says split a step "longer than 5 minutes" into waits "at most 4 minutes" (S:68); a 4-5 minute wait is unconstrained, and AC-4.3 checks "no single tool call exceeds 240 s" (S:215). Align the thresholds.
- m-02 The section 3.1 intro says the ten run "now" (S:79), yet the index-repo and workflow rows need new flags (`--output-dir`, `--output`; S:86, S:92) and init-lite needs `--unattended` (S:87). The rows flag this themselves, so only the intro wording is off.
- m-03 AC-C5 and the "additive" rule do not say where `--unattended` and `--output` are declared. A rewritten Usage line shows as a removed line; the real command in this run adds a second Usage line instead (`command.md:23`). State "add a new Usage line".
- m-04 `command.md:460` (the spec-panel command this run follows) uses `--report-dir <dir>` and `<report-dir>/return-contract.yaml`; the spec's WC-4 names `--output`/`--output-dir` and S:120 says "add `--output`". Outside the checkable evidence; reconcile when P2 reaches spec-panel.
- m-05 WORKER-CONTRACT.md mixes command rules with worker-session rules that name `worker_done`, `ask`, `check` and `heartbeat` (WC-3, 5, 7, 12; S:61, 63, 65, 70), while S:51 says the mode "names no Orca command" and SA-2 limits Orca mentions (S:147). Consider moving the session rules to the coordinator brief template.
- m-06 E3 cites `invocation_method: "skill-direct"` as evidence the direct route works (S:23), while S:43 says the PR #329 run proved only the nested route. The caveat is in 1.4; E3 could carry it.
- m-07 D5(b) says raising depth would "break R1's protection against runaway fan-out" (S:257); R1 is a reason against the alternative, not a protection (S:33). Wording only.
- m-08 S:11 says 11 locations were re-read and S:290 says an independent check re-read about 340 citations. I could not reproduce either outside the inventories (UNVERIFIED); the inventory-level citations I checked were all correct except M-07's.

## Mandatory output artifacts

### Guard Condition Boundary Table
Trigger: thresholds, boolean guards and sentinel comparisons are present. One row per input class that applies; left-out classes are named in the note under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` switch | S:51, S:60 | Zero/Empty | flag absent | false | SA-1: today's behaviour (S:146) | OK |
| `--unattended` switch | S:60, S:159 | Typical | flag present, command's phase landed | true | per section 3 row | OK |
| `--unattended` switch | S:159-162 | Legitimate Edge Case | flag present, command's phase not landed | true (accepted) | flag accepted, resolutions missing (B-01) | GAP |
| `--unattended` + output flag | S:62, S:87 | Zero/Empty | no `--output`/`--output-dir` | n/a | unspecified (M-02) | GAP |
| contract path | S:62 | Legitimate Edge Case | `--output` is a file, two workers in one dir | collision | defined only for init-lite (S:87) | GAP |
| `status` value | S:62, S:63 | Typical | `succeeded`/`failed`/`blocked`/`partial` | mapped | WC-5 table | OK |
| `status` value | S:62 | Sentinel Value Match | existing contract with another vocabulary | unknown | unspecified (M-05) | GAP |
| report missing | S:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| WC-10 wait split | S:68 | Typical | 6 min wait | true | split to at most 4 min | OK |
| WC-10 wait split | S:68, S:215 | Legitimate Edge Case | 4-5 min wait | false | unconstrained; AC says 240 s (m-01) | GAP |
| WC-10 wait split | S:68 | Maximum/Overflow | 3600 s eval (cli-eval) | true | split (S:104) | OK |
| readiness timeout | S:59 | Typical | 60 s default | n/a | observed only (M-01) | GAP |
| nested depth fence | S:33, S:219 | One/Minimal | depth 1 | true | worker-start refused (R1), CAPS:99 | OK |
| nested depth fence | S:254-258 | Legitimate Edge Case | user raises depth | false | D5, keep 1 | OK |
| circuit breaker (3 failures) | S:268, CAPS:80 | Accumulation | N `blocked` reports | no trip | no cap on re-dispatch (M-08) | GAP |
| confidence guard | S:121 | Typical / below | < 0.70 | true | blocked | OK |
| `--interactive`/`--watch` refusals | S:100-125 | Legitimate Edge Case | flag + `--unattended` | refused | no status named (M-11) | GAP |

Classes left out: Maximum/Overflow for the confidence guard (a score above 1.0 cannot occur); One/Minimal for the status mapping (a single value is a Typical row); Sentinel Value Match for the depth fence (CAPS:100 shows malformed values fall back to 1, so no collision).

Grading of the GAP rows (FR-8/FR-9): row 3 is B-01 (blocking); every other GAP is Medium or minor and is listed above; none names a concrete wrong outcome without a further guess.

### Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17: inventory to phases to checks)
```text
[Source: 43 commands (21 + 22)] --> [Triage: INV verdicts] --> [Section 3.1: 10 ready]
                                                            --> [Section 3.2: 27 need change]
                                                            --> [Section 4: 6 coordinator-only]   (10+27+6 = 43, conserved)
[37 worker-capable (3.1 + 3.2)] --> [Phase split] --> [P1: 15] [P2: 15] [P3: 4] [P4: 3]            (sum 37, conserved)
[P1 stage: 15 command edits] --> [AC-1.1: expects 37 sections]  <-- MISMATCH (B-02)
[P1 stage: flag on 37 commands] --> [gates honoured: 15 by end of P1, 22 later]  <-- MISMATCH (B-01)
[AC-1.2 live check: 15 P1 commands minus load = 14]
```
Both mismatches are blocking findings.

## Whittaker attack summary (FR-3 template)
- I can break this specification by **sequence attack**. The invariant at **S:60/S:67 (no gate, no outward action under `--unattended`)** fails when **the command is dispatched after P1 and before its gate phase**. Concrete attack: B-01 trace above (PR 42 gets a posted review; worker stalls on the offer). CRITICAL.
- I can break this specification by **divergence attack** at **S:200 (AC-1.1)**: the condition "every command in 3.1-3.2" diverges from "commands whose phase is P1" (B-02). MAJOR.
- I can break this specification by **zero/empty attack** on **the diff gate S:176**: input "deleted bullet" yields no output, so the gate reads as "additive" (B-03). MAJOR.
- Also found: zero/empty on the output flag (M-02), sentinel collision on `status` (M-05), accumulation on blocked re-dispatch (M-08).

## Expert notes (consensus and disagreement)
- Consensus: the central decision (Orca coordinates, commands stay units of work), the rejection reasons R1-R5 and the per-command table are well supported by the inventories; citations in sections 1-4 are accurate and the spec states its own evidence gaps (S:41-45, S:276-290).
- Wiegers/Adzic: the weak spot is acceptance wording (AC-1.1, AC-C5), not the requirements themselves.
- Fowler/Newman/Hohpe: the shared contract file is the right shape; propagation to nested skills, owner of the "fresh dir", and the mixed audiences in one file are unspecified (M-03, M-04, m-05).
- Nygard: the phase order is sound for gates and drift, but the flag-before-gate window (B-01) and the unbounded blocked retry (M-08) are the failure modes.
- Disagreement: none recorded.

## Review-loop notes
- Issue offer: per the command, the session that ran the review asks the user once whether to open an issue for the follow-up candidates. This worker has no user channel, asked nothing and created no issue.
- No brief clause was overridden. No file other than this report was written.

## Reviser brief
Blocking finding ids: B-01, B-02, B-03.
Reviser contract (restated from the command's Review Loop, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. Do not award yourself a PASS.

verdict: FAIL
