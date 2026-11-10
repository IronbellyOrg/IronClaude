review: 1 of 3

# /sc:spec-panel critique, round 1

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (computed with `sha256sum` in this run).
- Mode and focus: `--mode critique --focus requirements,architecture`. Not `--re-review`, so this is a first review of the full document. No baseline given, none needed.
- Reviewer model actually used: claude-sonnet-5-5.
- Lint evidence: `.dev/orca-command-refactor/review/lint-1.md:1-5` (review-lint/1, sha256 of the linted file `d3cdbe57...5200d`, which equals the candidate hash; checks REF; 0 findings). No lint ids to confirm or dismiss. A lint id never fails a review by itself.
- Citation notation: `spec:N` is line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` are lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `command.md:N` is the /sc:spec-panel definition used in this run.
- Binding context read: `.dev/orca-command-refactor/README.md:1-38`.

## What was covered, and what could not be checked

Covered: sections 1 to 9 and the Decisions and UNVERIFIED lists of the candidate. Every `CAPS:` and `INV-A/B:` citation the candidate relies on was compared with the inventory line (about 60 distinct citations, including the 43-command split of 10 ready, 27 needing change and 6 coordinator-only against `INV-A:73`, `INV-B:278`, and the row counts at `spec:81-125` and `spec:130-137`). Those citations match.

UNVERIFIED, not checkable inside this workspace (only the README, the three inventories, the candidate and the lint file exist here):
- every `src/superclaude/...` line the candidate cites directly (`spec:11`, `spec:25`, `spec:52`, `spec:83-125`);
- every `CLAUDE.md:N` line (`spec:34`, `spec:52`, `spec:150`);
- `.dev/codegraph-migration/...` and `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md` lines (`spec:22-23`, `spec:43-44`). `EVIDENCE.md:39,45,56` is checked only through the quotations at `CAPS:49`;
- the "11 locations re-read" and "about 340 citations re-checked" statements (`spec:11`, `spec:285`);
- the `src/superclaude/core/HOW-WE-WORK.md` lines cited at `spec:146`.
`~/.claude/WORKER-CONTRACT.md` does not exist under the sandbox home, so the shared contract the candidate proposes could not be compared with anything.

Pipeline Dimensional Analysis (FR-17) did not trigger: the candidate has phases and a command split, not a data pipeline with changing counts. `--focus correctness` is not active, so no State Variable Registry is required. The Guard Condition Boundary Table is triggered (thresholds at `spec:33`, `spec:68`, `spec:121`) and is produced before synthesis.

## Guard Condition Boundary Table (produced before synthesis, FR-10)

Classes that cannot occur for a guard are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 outcome mapping `failed if report failed/blocked or absent, else succeeded` | spec:63 | Zero/Empty | contract file absent | failed | `--outcome failed` ("no report exists") | OK |
| G1 | spec:63 | Zero/Empty | contract file present but empty or unparsable | unspecified | falls under "otherwise", so `succeeded`; never stated either way | GAP (M-3, Medium) |
| G1 | spec:63 | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| G1 | spec:63 | Sentinel Value Match | `status: blocked` | failed | `--outcome failed`; circuit breaker does not count it (`CAPS:80`, `spec:263`) | OK |
| G1 | spec:63 | Legitimate Edge Case | `status: partial`, or audit verdict FAIL | succeeded | `--outcome succeeded`, body states status | OK |
| G1 | spec:62-63 | Legitimate Edge Case | existing command contract with its own `status` word not in the four-value set | unspecified | "keep their fields" (spec:62) and "one of four values" (spec:62) both apply | GAP (M-3, Medium) |
| G2 wait split `single tool call > 5 min must be split into waits <= 4 min` | spec:68 | Typical | 2-minute poll | not split | no action | OK |
| G2 | spec:68 | Legitimate Edge Case | one call of 4.5 minutes | false (not over 5) | allowed by the first clause, yet over the 4-minute cap the pr-submit row applies (spec:114) | GAP (M-11, minor) |
| G2 | spec:68, spec:104 | Maximum/Overflow | eval timeout 3600 s | true | split into waits of at most 4 minutes | OK |
| G2 | spec:68 | Zero/Empty | a 0-second wait | not applicable | left out: a zero wait blocks nothing | OK |
| G3 `--unattended` as a standalone token | spec:16, spec:51 | Zero/Empty | flag absent | false | today's behaviour unchanged (SA-1, spec:146) | OK |
| G3 | spec:51 | Sentinel Value Match | the literal text `--unattended` inside a quoted prompt or inside specification text under review | unspecified | no tokenizing rule in the candidate | GAP (M-5, Medium) |
| G3 | spec:51, spec:100, spec:103 | Legitimate Edge Case | `--unattended` together with `--interactive` | unspecified | cleanup and improve say `--interactive` is refused (spec:103,110); adversarial, brainstorm, release-split, roadmap rows do not | GAP (M-5, Medium) |
| G3 | spec:128 | Legitimate Edge Case | `--unattended` passed to a section-4 command | unspecified | "get no --unattended mode" with no stated reaction | GAP (minor) |
| G4 task confidence `< 0.70 resolves as blocked` | spec:121 | Zero/Empty | confidence 0 | true | blocked | OK |
| G4 | spec:121 | Typical | confidence 0.85 | unspecified | the row names only the sub-0.70 case; INV-B:45 also names only sub-0.70, but the project's own confidence rule has a 0.70-0.89 "present alternatives" band (`command.md` of the agent is not in this workspace, so UNVERIFIED for task) | GAP (M-14, Medium) |
| G4 | spec:121 | Legitimate Edge Case | confidence exactly 0.70 | false | proceeds (implied) | OK |
| G5 nesting depth `max 1` | spec:33 | Typical | worker calls `worker-start` | true | refused `nested_worker_depth_exceeded`; WC-8 forbids the call (spec:66) | OK |
| G5 | spec:33 | Maximum/Overflow | depth raised above 1 by the user | false | D5 keeps depth 1 (spec:249-253) | OK |

## Blocking findings

### B-1 (CRITICAL as graded: stated acceptance checks cannot pass for `/sc:load`)

- Expert: Wiegers (traceability, testability), Whittaker (divergence attack).
- Sentence: An implementer who follows the stated text as written builds a P1 test and live check that require `/sc:load` to carry an `## Unattended mode` section naming `return-contract.yaml` and to pass live-check step 4 on a written contract file, and that cannot pass, because the spec's own `/sc:load` row says it writes no report and is not a worker Task.
- Stated texts that collide:
  - AC-1.1 (spec:195) asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". `/sc:load` is in section 3.2 (spec:112).
  - P1 scope (spec:159) lists load among the P1 commands and requires the flag on "every command in sections 3.1 and 3.2".
  - AC-1.2 (spec:196) runs the 7.2 live check "on each P1 command with `--unattended --output <dir>`". Step 4 of 7.2 (spec:183) requires `test -s <contract>` and a parsed `status`.
  - The `/sc:load` row (spec:112) says report "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task". The Decisions table repeats this (spec:265, citing INV-B:65, which says it "writes no file" and has no `--output`).
- Why the check cannot pass: a command that writes no contract fails 7.2 step 4 by construction, and `/sc:load` has no output flag to pass (INV-B:63). Section 6 says a phase "passes only when every check in its block ... passes" (spec:167), so P1 cannot finish. The AC-1.1 assertion has the same gap, because WC-4 says the contract is written on every outcome (spec:62), which the load row denies.
- Recommendation: exclude `/sc:load` from AC-1.1, AC-1.2 and the P1 flag requirement (it keeps only its usage-line fix), or give it a real contract and an output flag. The first is the smaller change.
- Priority: High.

## Follow-up candidates (Medium and minor; none fails the review)

### Requirements analysis

- M-1 (MAJOR label, graded Medium; Wiegers, Adzic). WC-4 puts the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62). Several rows use `--output` for a file: tdd "`--output <file>`" (spec:90), init-lite (spec:87), and AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` expecting a blocked contract (spec:200). No directory exists for those runs. The implementer must guess (dirname of the file, a new flag, a fixed path). The spec-panel definition in this sandbox already chose a separate `--report-dir` because "`--output` is file-valued" (`command.md:460`), which shows the gap is real. Add one rule for file-valued `--output` commands, for example a required `--report-dir`.
- M-2 (Medium; Wiegers). WC-6 says a command without a resume flag "writes each run into a fresh output directory" (spec:64), and 29 rows are marked "fresh dir". WC-4 and section 2.3 say the coordinator passes one output directory known before dispatch (spec:62, spec:73), and a `--retry-of` retry reuses the same Task brief (`CAPS:116`). Nothing says who creates the fresh directory or what name the retry gets, so a retry can overwrite the first attempt's contract, the exact corruption WC-6 forbids. State that the coordinator passes a new directory per attempt, or that the command creates a timestamped child and reports its path.
- M-3 (Medium; Whittaker, zero/empty and sentinel attacks). WC-5 maps "no report exists" to failed and everything else to succeeded (spec:63). An empty, truncated or unparsable contract, or a `status` outside the four values, falls under "otherwise" and reports `succeeded`. WC-4 also says commands that already write a contract "keep their fields" (spec:62), but the existing status vocabularies were never listed: INV-B:272 notes only that workflow's contract includes `failed`. Add: a missing, unparsable or out-of-set `status` maps to failed, and list the existing status words of workflow, reflect, brainstorm and adversarial contracts.
- M-5 (Medium; Whittaker, sentinel collision). `--unattended` is a flag token (spec:16, spec:51), but no rule says it counts only as a standalone argument. A prompt that quotes the word (`/sc:troubleshoot "why does --unattended fail"`) or specification text under review that contains it could switch the mode. Precedence with `--interactive` is stated for cleanup and improve (spec:103,110) but not for adversarial, brainstorm, release-split or roadmap. Add one line to the contract file: the token counts only outside quoted arguments, and `--unattended` with `--interactive` is refused.
- M-6 (Medium; Newman, Hohpe). WC-2 binds "the command" (spec:60), but the gates live in the skills and in nested invocations: tdd runs the `task` skill, which asks on ambiguity (spec:90), tasklist runs reflect (spec:122), brainstorm and roadmap run adversarial (INV-A:39, INV-B:40). Only tdd and tasklist state that `--unattended` reaches the nested invocation. Add a general rule: every nested skill or command call made under `--unattended` receives it.
- M-7 (Medium; Adzic). The auggie-review row and D4 say posting comes back "only with an explicit `--post-pr` in the brief" (spec:100, spec:245). The inventory names only the off switch `--no-post-pr` (INV-A:38, INV-A:78). Whether a `--post-pr` flag exists is UNVERIFIED (the command file is not in the workspace). WC-9 says outward actions turn on "only through the command's own explicit flag" (spec:67); if no such flag exists the rule has nothing to point to. Name the real mechanism or state that a new flag is added.
- M-8 (Medium; Wiegers). Section 6 says "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4" (spec:154), and section 9 says "Phases 0-3 can proceed on the recommendations" (spec:225). Those differ: D4 governs auggie-review `--post-pr` and task `commit`/`push` (spec:244), both P2 rows (spec:100, spec:121, spec:160), and D1 governs every phase. Say that P0-P3 proceed on the recommendations and are re-opened if a recommendation is rejected.
- M-12 (Medium; Cockburn). The workflow row asks to "write the contract for pre-creation STOPs too" (spec:92, AC-1.4 at spec:198), yet the workflow contract lives in `.dev/tasks/to-do/<id>/` and "Not written for pre-creation STOPs" because no package id exists yet (INV-B:272). Nothing says where such a contract goes, and WC-4's `<output-dir>` does not cover workflow. The implementer must invent the location. Also the workflow path cannot be "known before dispatch" (spec:62) because `<id>` is generated at run time. State the location (for example the coordinator-passed directory) for this case.
- M-13 (Medium; Crispin). WC-3 lets a worker "ask the coordinator once" when a gate would resolve as blocked (spec:61), while AC-2.2 expects `worker_done --outcome failed` with a blocked contract (spec:200) and 7.2 step 2 expects `agentWait` never to appear (spec:181). Whether the worker may use `ask` is a choice the brief makes (section 2.3, spec:73, does not list it), so the same input can pass or fail the check depending on the worker. Add to the brief template: "do not use `ask`" for the gate-trigger test, or define what a pass looks like when `ask` is used.
- M-14 (Medium; Wiegers). Task's confidence gate is resolved only below 0.70 (spec:121, INV-B:45). The 0.70-0.89 band is not addressed. UNVERIFIED whether `/sc:task` prompts in that band (the command file is not in the workspace). Confirm the band and state its unattended behavior.

### Architecture analysis

- M-4 (Medium; Fowler, Nygard). Tasklist: the candidate has Stage 10.5 pass `--unattended` to each reflect "so the headless rule applies" (spec:122) and has reflect follow "the existing headless auto-accept rule" under `--unattended` (spec:88). The inventory recommended the opposite: call reflect without `--remediate` (INV-B:215) and run the reflect fan-out at the worker's top level, not inside subagents (INV-B:210, INV-B:295). The candidate reverses this without a row in its Decisions table, even though the Decisions table says it kept the inventory verdicts (spec:268). The headless rule auto-accepts remediation for auto-fixable registers (INV-B:109), so an unattended tasklist run could start N remediation hand-offs that write extra files, beyond "no outward capability" claimed for P2 (spec:160). The text of the headless rule is UNVERIFIED here (`remediation-handoff.md:239-247` not in the workspace). Record the decision, and either drop `--remediate` under `--unattended` or state the files it may write and where.
- M-15 (Medium; Hohpe, Newman). The worker-session rules (WC-3, WC-5, WC-7, WC-12, spec:61, 63, 65, 70) mention `worker_done`, `ask` and `check`. Section 2.1 says the unattended mode "names no Orca command" (spec:51) and SA-2 allows an Orca mention in the contract file only as an example (spec:147), while the contract file is where those rules are to be written (spec:52, spec:158). The coordinator brief of section 2.3 (spec:73) lists the command line, output directory, authorizations and placement, but not the outcome mapping or the top-level-only rule. It is not stated how a worker session that is told only to run `/sc:x --unattended` learns WC-5 and WC-7. Say which document the worker session reads and when (the brief, or the command telling it to read `~/.claude/WORKER-CONTRACT.md` first).
- M-16 (minor). AC-C1 (spec:172) greps only `orca(-ide) (orchestration|worktree|terminal|agent)`, so `orca-ide status`, `orca open` or `orca-ide skills` in a primitive would pass although SA-2 forbids any Orca command (spec:147). In the table the alternation is written `\|`; as an ERE that is a literal pipe, so the pattern must be unescaped when copied.
- M-9 (Medium; Crispin). AC-C5 and AC-0.3 detect deletions with `grep -E '^-[^-]'` (spec:176, spec:193). In `git diff -U0` a deleted markdown bullet `- text` appears as `-- text`, which this pattern skips, so removing bullets from a command passes the "additive only" check (SA-4, spec:149) that exists to catch it. Use `grep -E '^-' | grep -v '^---'`.
- M-10 (Medium). AC-0.4 step 4 for `/sc:adversarial` uses "the command's existing report file" (spec:194), but the adversarial row says its contract filename is "not fixed" (spec:83, INV-A:60). The check has no path to open until P1 fixes it. Name the file the check reads (the contract under `--output`, found by search).
- M-11 (minor). WC-10 triggers a split at "longer than 5 minutes" but splits into waits of "at most 4 minutes" (spec:68), and the pr-submit row checks "under 4 minutes" (spec:114). A single 4.5-minute call needs no split under the first clause and exceeds the second. Use one number. The effect of a late heartbeat on Orca's verdict is UNVERIFIED (`CAPS:182`).

### Notes

- N-1. E4 says Agent-tool subagents "are not counted by Orca's nesting limit" as a fact (spec:24); the cited line says the same but marks "Orca never limits them" UNVERIFIED (`CAPS:155`), and section 1.4(3) already says so (spec:45). No change needed beyond consistent wording.
- N-2. AC-1.3 suggests a "scratch worktree" for a plain-session run (spec:197). The repo rules on worktree creation are not in this workspace, so whether a scratch worktree is allowed is UNVERIFIED.
- N-3. The cited counts in section 3 (10, 27, 6) and the phase lists at spec:159-162 are consistent: 9 P1 commands plus 11 P2 commands plus 4 P3 plus 3 P4 give 27 changed commands, and the 4 ready commands with gate fixes (reflect, release-split, tdd, troubleshoot) sit in P2.

Follow-up issue question: the review loop asks the session that ran the review whether to open an issue for the Medium and minor list. This sandbox run has no user to ask and creates none. The list is recorded here only.

## Expert synthesis

- Wiegers: requirements are mostly specific and cited; the one blocking defect is a verification gap (B-1). Several requirements leave a value to the implementer (M-1, M-2, M-3, M-8, M-14).
- Adzic: the live check (7.2) is concrete; examples for the file-valued `--output` case are missing (M-1, M-7).
- Cockburn: the coordinator and worker goals are clear; the workflow pre-creation stop has no destination (M-12).
- Fowler: the decision "Orca on top, commands stay units" is well supported by CAPS:97-103, CAPS:145-149 and INV-A:90; the tasklist reversal is the one architectural deviation not recorded (M-4).
- Newman: nested invocations need a propagation rule (M-6). Hohpe: delivery of worker-session rules is unclear (M-15).
- Nygard: failure modes are handled well (blocked, partial, fenced), with the empty-contract case missing (M-3).
- Whittaker: attacks found, all graded above: Zero/Empty (M-3), Sentinel Collision (M-5), Sequence (M-2, retry order), Divergence (M-11, M-14).
- Crispin: M-9, M-10, M-13 are check-quality items.

## Reviser brief

Blocking finding ids: B-1.

Contract for the reviser (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. For B-1 the narrowest repair is to remove `/sc:load` from AC-1.1, AC-1.2 and the P1 flag requirement at spec:159, spec:195 and spec:196. No brief clause was overridden.

verdict: FAIL
