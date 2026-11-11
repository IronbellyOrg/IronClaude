review: 1 of 3

# Spec-panel review, round 1: Orca worker-contract spec

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (acted out from `command.md`; no slash command was run)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given (first review of the full document); prior report: none
- reviewer model actually used: `claude-sonnet-5-5` (Sonnet 5.5), one reviewer. `superclaude review panel resolve` and `superclaude review merge` were not run: the `superclaude` command is not installed in this sandbox (`which superclaude` printed nothing), so per the loop prompt file one reviewer ran and there is no merge ledger.
- prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). Brief clauses overridden: none.
- panel engaged (Review Sequence order): Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker (always active), Newman, Hohpe. Not in the requested focus areas and not engaged: Crispin, Gregory, Hightower.
- citation keys: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (the only evidence files in the workspace). `README:N` = `.dev/orca-command-refactor/README.md`. `PROMPTS:N` = the loop prompts file, `CMD:N` = `command.md`.
- ordering note: `CMD:263` puts the `Reviser brief` just above the final `verdict:` line; `PROMPTS:58` makes `## Findings block` the last section. This report ends with the findings block, then the Reviser brief, then the verdict line, so both stay satisfied in the closing lines.

## Coverage

Read in full: `command.md`, the loop prompts file, `README.md`, the whole candidate (285 lines), and all three inventories. I checked about 70 `INV-A`, `INV-B`, `CAPS` and `README` citations in the candidate against those files. They are present and say what the candidate says, with two exceptions noted in F11 and F17. I did not run any command. A first review has no baseline, so there is no diff and no prior-findings table.

Cannot be checked inside the sandbox, so UNVERIFIED: every `src/superclaude/...` line citation not routed through an inventory; `CLAUDE.md:N` and `HOW-WE-WORK.md:N` citations (`spec:34`, `spec:146`, `spec:150`, `spec:164`, `spec:175`, `spec:192`); `.dev/codegraph-migration/...` and `.dev/evals/...` files (reachable only through the CAPS quotes); `spec:25` (E5, the `grep` results); `spec:11` (the claim that 11 locations were re-read); `spec:285` (the 340-citation validator pass); `pyproject.toml:38` (`spec:183`).

## Grading checks for blocking findings

Each sentence is "An implementer who follows the stated text as written builds X, and X is wrong because Y."

- F1: An implementer who follows the `load` row (`spec:112`) and the `/sc:load` decision (`spec:265`) builds `/sc:load` with no contract and no `return-contract.yaml` section, and that is wrong because AC-1.1 (`spec:195`) fails its test for every command in sections 3.1-3.2, so the P1 gate cannot pass. An implementer who instead adds the section and a contract contradicts `spec:265`.
- F2: An implementer who follows WC-4 (`spec:62`) for `/sc:tdd --output <file>` (`spec:90`, `spec:200`) writes the contract to `<file>/return-contract.yaml`, which is impossible because `<file>` is a regular file. For `/sc:adversarial` (`spec:83`) WC-4 puts the contract at `<dir>/return-contract.yaml` while the same spec fixes it at `<dir>/adversarial/return-contract.yaml`.
- F3: An implementer who follows AC-0.4 (`spec:194`) with `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` run as P0 smoke workers cannot make step 3 of 7.2 (`spec:182`) pass, because step 3 requires a WC-4 contract path and contract `status` that the spec itself says do not exist until P1. P0 is the gate for every later phase (`spec:154`).

=== REQUIREMENTS ANALYSIS ===

### F1 (blocking, CRITICAL) `/sc:load`: acceptance check demands a section the spec says must not exist
- Expert: Wiegers (traceability of requirement to check), Adzic.
- Texts in conflict: AC-1.1 asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`" (`spec:195`). `load` is one of those 27 rows. Its report column says "none (see note)" and its change column says "use it as a step inside another worker's brief, not as its own Task" (`spec:112`). The Decisions table says "a report file would be an unrequested addition" (`spec:265`). P1 lists `load (usage line only)` (`spec:159`), and AC-1.2 runs a live check "on each P1 command with `--unattended --output <dir>`" (`spec:196`), but `load` has no output flag or contract for step 4 of 7.2 to open (`spec:183`).
- Concrete trace: P1 done as written, `load` gets only a Usage-line fix. `uv run pytest tests/skills/test_worker_contract.py` then fails on the `load` assertion, and P1 cannot close. P2 onward is blocked by `spec:154`.
- Recommendation: delete `load` from the AC-1.1 and AC-1.2 scope, or move it out of 3.2 into a "not a worker task" list. This is a deletion and needs no new rule. Priority High. Quality impact: Testability +1.

### F7 (Medium) Status vocabulary has no definitions and may clash with existing contracts
- Expert: Wiegers. WC-4 fixes `status` to `succeeded|partial|failed|blocked` (`spec:62`), but nothing says when a run is `partial` rather than `failed`. WC-4 also says commands that already write a contract "keep their fields and add the missing ones" (`spec:62`). The inventories do not list the status values workflow, reflect or brainstorm already use (`INV-B:272`, `INV-B:112`, `INV-A:97`), so a clash is UNVERIFIED. Two readings of `partial` give two different WC-5 outcomes only for a coordinator that reads `partial` as a loss, which the Decisions table settles (`spec:263`). Recommendation: one sentence per status. Follow-up candidate.

### F8 (Medium) `--unattended` edge cases are unspecified
- Expert: Wiegers, Cockburn. (a) `--unattended` without an output directory: WC-4 says the contract is written "on every outcome ... including stops before any other output exists" (`spec:62`) but the location needs `<output-dir>`; there is none. (b) The flag on a section-4 command: those "get no `--unattended` mode" (`spec:128`), but the result of passing it is not stated. (c) Commands "refused" under `--unattended` (business-panel socratic, explain interactive, pr-submit `--monitor 1`, test `--watch`, cleanup `--interactive`: `spec:102,103,108,114,123`) have no stated status or contract content. (d) The flag appearing inside quoted content such as a bare tdd topic: D1 says it "cannot misfire on a person" (`spec:228`), which does not cover quoted text. `CMD:459` shows how a command can define this. Follow-up candidate.

### F12 (Medium) P1 names 13 commands but its scope and check cover 37
- Expert: Wiegers. The P1 Commands cell names 13 (nine 3.2 rows plus four fixes to 3.1 rows), while the P1 Scope cell says the flag is "accepted by every command in sections 3.1 and 3.2" (`spec:159`) and AC-1.1 checks 37. `brainstorm` and `init-lite` have "Small fix: None" (`spec:84,87`) and appear in no phase cell, yet AC-1.1 wants their section in P1. See the Quantity Flow Diagram. Graded Medium: the scope sentence names the larger set, so an implementer has one reading. Follow-up candidate.

### F13 (minor) Contract-writing condition differs between WC-4 and SA-3
WC-4 writes the contract "in unattended mode" (`spec:62`); SA-3 adds "or when the caller passes the new output flag" (`spec:148`); AC-1.3 tests only the case with neither (`spec:197`).

### F14 (minor) "paid external run" is undefined
WC-9 turns off "a paid external run" under `--unattended` (`spec:67`). It is unclear whether default web search in research, recommend and review-translation, or cli-eval's `uv run superclaude eval run` (`INV-A:44`), counts.

### F18 (minor) WC-1 has no unit, no phase and no check of its own
"Fall back on its own well inside the readiness limit (default 60 s)" (`spec:59`), while the evidence it cites says a 30 s fallback passes and about 45 s fails (`CAPS:49`). The owner is "Launch setup, not commands" and no phase in `spec:156-162` delivers it.

### F19 (minor) The contract file has no version field
WC-4 lists required keys (`spec:62`) but no `contract_version`; `INV-B:272` shows the workflow contract already carries a contract number. Not needed for this phase.

=== ARCHITECTURE ANALYSIS ===

### F2 (blocking, CRITICAL) WC-4 defines the contract location as a directory the coordinator passes, but the spec's own rows and checks pass files or fix other paths
- Expert: Fowler (lead), Newman (interface consistency), Hohpe.
- Texts in conflict: WC-4 says the contract is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (`spec:62`), and 2.3 says the path must be "known before dispatch (WC-4)" (`spec:73`). But: `tdd` and `init-lite` take `--output <file>` (`spec:87,90`; `INV-B:222`; `INV-A:55`) and AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` (`spec:200`) while AC-1.2 uses `--output <dir>` (`spec:196`); `adversarial`'s fix puts the contract at `<output>/adversarial/return-contract.yaml` (`spec:83`); `workflow`'s contract is at `.dev/tasks/to-do/<id>/` with no output flag and an id made at run time (`spec:92`; `INV-B:272`), and its "pre-creation STOPs" have no package directory yet; `implement` writes beside its ledger (`spec:109`) and `cleanup-audit` has a fixed output directory (`spec:85`).
- Concrete trace: brief `/sc:tdd "<component>" --unattended --output docs/x/TDD_X.md`. WC-4 asks for `docs/x/TDD_X.md/return-contract.yaml`, which cannot be created. The worker has no defined `--report-path`, and 7.2 step 3 ("its report path is the WC-4 contract path", `spec:182`) has no value to compare.
- Recommendation: state one rule, either "the contract sits in the directory that holds the report (the parent of a file-valued `--output`)" or "each row names its own contract path", and make 2.3, the rows named above and the checks agree with it. Priority High. Quality impact: Consistency +2, Testability +1.

### F9 (Medium) SA-2 permits a mention of Orca that AC-C1 would flag
- Expert: Fowler. SA-2 allows "a caller's question channel inside the contract file" (`spec:147`). AC-C1 greps `src/superclaude/core` and requires an empty result for `orca (orchestration|worktree|terminal|agent)` (`spec:172`). P0 adds the contract file and "an Orca section to `HOW-WE-WORK.md`" (`spec:158`), both under `core/`. The baseline is zero Orca mentions in `HOW-WE-WORK.md` (`spec:25`, UNVERIFIED). Whether the new text may contain a command-shaped string like `orca orchestration ask` is not stated. The check passes or fails on how the implementer words the example. Also, the `\|` inside the table cell is the GFM escape for `|`; copied raw into a shell, `grep -E` reads `\|` as a literal pipe and the pattern matches nothing. Follow-up candidate.

### F10 (Medium) "Fresh dir" for re-runs and "path known before dispatch" can disagree
- Expert: Nygard, Fowler. WC-6 has the command write "each run into a fresh output directory" (`spec:64`); about 20 rows use "fresh dir" as the resume answer (`spec:99-125`). WC-4 and 2.3 need the contract path fixed before dispatch (`spec:62,73`). If the command creates the fresh directory, the pre-computed path is stale. If the coordinator passes a new directory on retry, the command is not what makes the directory fresh, and re-using the same `<dir>` overwrites the first attempt, which WC-6 sets out to prevent. After a `blocked` result the answer comes as a flag on a re-run (`spec:60,61`), so a "fresh dir" command restarts all its work. Own `failed` reports also do not count toward the circuit breaker (`CAPS:80`), so a block-and-retry loop has no stated cap, and the same holds for repeated `ask` resumes (`spec:61`). Follow-up candidate.

### F11 (Medium) The pr-submit wait reading differs from the inventory it relies on, and D3(b) names a change the row says is not needed
- Expert: Nygard. The inventories read pr-submit as one wait of up to 600 s per round that needs heartbeats (`INV-B:95`, `INV-B:299`). The spec reads the same budget as cumulative poll-then-sleep iterations that already allow a heartbeat (`spec:68`, `spec:114`), citing `SKILL.md:46-64`, which is UNVERIFIED here. The 3.2 row then asks to "confirm" the 4-minute bound (`spec:114`), while D3(b) says to "Apply the section 3 row (wait splitting, summary file, HALTs as blocked)" (`spec:241`). Phase 4 waits for D3 anyway (`spec:154`), so the cost is limited. Follow-up candidate.

### F4 (Medium) WC-3 lets an `ask` answer become a flag for gates that D2 and D4 say a person must decide
- Expert: Nygard, Hohpe. WC-3: the worker "may instead ask the coordinator once ... wait, then re-invoke or resume the command with the answer as a flag" (`spec:61`). D2(a), the recommended option, is: "The worker stops, writes the halt to its ledger and contract, and ends `failed`" (`spec:234`), because a coordinator is "another agent" (`spec:233`); D4(a) allows outward actions only when the user's own instruction names them (`spec:245`). WC-3 has no carve-out for implement Rulings or outward-action flags. It says "may", and implement has no flag that carries a Ruling (`INV-A:51`), so a wrong build needs a second guess. Follow-up candidate.

### F5 (Medium) P1 ships `--unattended` as a no-op on commands whose gates and outward defaults are fixed only in P2 or P4
- Expert: Nygard. P1 scope: the flag is "accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (`spec:159`); AC-1.1 requires each command's section in P1 (`spec:195`). WC-9 says that under `--unattended` "any default that pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run is off" (`spec:67`). Between P1 and P2, `auggie-review --unattended` would still post to the PR (`spec:100`; `INV-A:38`) and `task --unattended` would still run `commit`/`push` (`spec:121`). The spec says phases are "independently useful" (`spec:154`) but not that a coordinator must not dispatch a command before its phase. A wrong outcome needs someone to dispatch early, so Medium. Follow-up candidate.

### F6 (Medium) WC-10's threshold and AC-4.3's threshold differ
- Expert: Adzic. WC-10 splits a call that "blocks a single tool call for longer than 5 minutes" into waits "of at most 4 minutes" (`spec:68`); AC-4.3 passes only if "no single tool call exceeds 240 s" (`spec:210`). A 4 to 5 minute call is allowed by the rule and fails the check. A call of exactly 5 minutes also lands on the heartbeat cadence. The check is stricter, so it can be met. Follow-up candidate.

### F15 (minor) The tasklist nesting claim has no depth count
"One layer below the worker, inside Claude Code's nesting limit" (`spec:122`) rests on `INV-A:14`, which describes a limit of three layers below the main conversation but was read for only part of the docs page (`INV-A:112`). The row does not count layers for reflect Tier 2 plus adversarial.

### F16 (minor) Unverifiable validation claims in the header and footer
"This worker re-read 11 of the load-bearing locations on 2026-11-02" (`spec:11`) and the 340-citation check (`spec:285`) cannot be reproduced here. They add no requirement.

### F17 (minor) E3 and 1.4(1) use the same evidence in opposite directions
E3 cites `invocation_method: "skill-direct"` as support (`spec:23`); 1.4(1) says the PR #329 run "proves the nested route, not the direct route this spec requires" (`spec:43`). Section 1.4 states the gap openly; E3 should say the same.

=== ADVERSARIAL ANALYSIS (Whittaker, always active, after Fowler and Nygard) ===

1. I can break this specification by **Zero/Empty Attack**. The invariant at **AC-1.1 / `load` row (`spec:195`, `spec:112`)** fails when **a command in 3.2 has no report at all**. Concrete attack: state before: 27 rows in 3.2, `load` has report "none". Step: implement P1 per rows. After: 26 sections exist, test asserts 27, red. See F1.
2. I can break this specification by **Divergence Attack**. The invariant at **WC-4 (`spec:62`)** fails when **`--output` is a file, not a directory**. Concrete attack: before: coordinator passes `--output docs/x/TDD_X.md`. Branch A (WC-4): contract at `docs/x/TDD_X.md/return-contract.yaml`, write error. Branch B (row 3.1 `tdd`): report is the TDD file, no contract. Both can apply to one run. After: no contract, `worker_done --outcome` cannot be derived under WC-5. See F2.
3. I can break this specification by **Sequence Attack**. The invariant at **P0 gate (`spec:154`) and AC-0.4 (`spec:194`)** fails when **7.2 step 3 runs before the P1 contract exists**. Concrete attack: before: P0 done, contracts arrive in P1 (`spec:194`). Step: run 7.2 on `/sc:troubleshoot`. Step 3 needs "the contract's `status`" and "the WC-4 contract path"; troubleshoot writes `REPORT.md` and a `return-contract.yaml` only with `--caller task-unified` (`INV-B:242`). After: step 3 cannot pass, P0 never closes, P1 never starts. See F3.
4. I can break this specification by **Sentinel Collision Attack**. The invariant at **D1 (a) (`spec:228`)** fails when **a quoted topic contains the token `--unattended`**. Concrete attack: `/sc:tdd "how does --unattended work" --output f.md` read by a command that tokenises naively turns the mode on for a person. The spec does not say that only a standalone token counts. See F8. A second sentinel: a prior contract whose `status` value is outside the four (`spec:62`), see F7.
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-3 / WC-5 (`spec:61,63`)** fails when **a gate keeps resolving as blocked**. Concrete attack: coordinator answers, re-dispatches, worker returns `failed` again, N times. Own `failed` reports do not count toward the 3-failure breaker (`CAPS:80`), and the spec sets no cap on retries or on `ask` resumes. See F10.

## Guard Condition Boundary Table

Guards found: conditional logic and numeric thresholds in WC-1, WC-2, WC-3, WC-5, WC-8, WC-10 and the task confidence rule. Experts: Nygard (construction), Crispin (completeness check, applied by the panel chair as a check only), Whittaker (attack). The table is complete: every class is a row or is left out with a reason in the line below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome map | spec:63 | Zero/Empty | report file present but empty or not valid YAML | unknown | not stated (7.2 step 4 `test -s` runs in the coordinator, spec:183) | GAP (Medium, F7) |
| WC-5 outcome map | spec:63 | One/Minimal | contract with `status` only, no `command` | `failed`/`blocked`? no | WC-4 says "at least" `command` (spec:62); no outcome for a short contract | GAP (Medium, F7) |
| WC-5 outcome map | spec:63 | Typical | `status: succeeded` | not failed | `--outcome succeeded` | OK |
| WC-5 outcome map | spec:63 | Sentinel Value Match | `status` outside the four values (existing contracts keep their fields, spec:62) | not failed | not stated | GAP (Medium, F7) |
| WC-5 outcome map | spec:63 | Legitimate Edge Case | `partial`; audit with verdict FAIL | not failed | `--outcome succeeded`, first sentence states status (spec:63, 263) | OK |
| WC-10 wait split | spec:68 | Typical | single call 3 min | false | no split needed | OK |
| WC-10 wait split | spec:68 | Legitimate Edge Case | single call 4 to 5 min | false | no split (rule), but AC-4.3 fails above 240 s (spec:210) | GAP (Medium, F6) |
| WC-10 wait split | spec:68 | Maximum/Overflow | 600 s pr-submit budget; 3600 s cli-eval (spec:68) | true | split to at most 4 min; pr-submit reading UNVERIFIED (spec:114) | OK for cli-eval; pr-submit see F11 |
| WC-2 unattended gate | spec:60 | Zero/Empty | `--unattended` with no output directory | true | contract location not stated | GAP (Medium, F8) |
| WC-2 unattended gate | spec:60 | Typical | `--unattended --output <dir>` | true | gate resolves (a), (b) or (c) | OK |
| WC-2 unattended gate | spec:60, 128 | Legitimate Edge Case | flag passed to a section-4 command | true | not stated | GAP (Medium, F8) |
| WC-2 unattended gate | spec:228 | Sentinel Value Match | token `--unattended` inside quoted content | ambiguous | not stated | GAP (minor, F8) |
| WC-2 / WC-9 in P1 | spec:159, 67 | Legitimate Edge Case | P1 shipped, P2 not yet, `auggie-review --unattended` | true | flag is a no-op; posting default stays on | GAP (Medium, F5) |
| WC-3 ask timeout | spec:61 | Maximum/Overflow | coordinator never answers; repeated resumes | true | resume same message ID, no cap stated | GAP (Medium, F10) |
| WC-3 ask timeout | spec:61 | Typical | one timeout, then answer | true | resume the same ID, no duplicate | OK |
| WC-8 nesting depth | spec:33, 66 | Typical | worker calls `worker-start` at depth 1 | true | refused, WC-8 forbids the call | OK |
| WC-8 nesting depth | spec:252 | Legitimate Edge Case | user raises depth (D5 b) | false | WC-8 still forbids | OK |
| WC-1 readiness | spec:59 | Legitimate Edge Case | startup prompt fallback of 45 s | false | "well inside" 60 s, no number; evidence says about 45 s fails (CAPS:49) | GAP (minor, F18) |
| task confidence | spec:121 | Legitimate Edge Case | confidence exactly 0.70 | false | "below 0.70" blocks; 0.70 proceeds (INV-B:199) | OK |

Classes left out, with reasons: WC-5 Maximum/Overflow (no count or capacity is involved); WC-10 Zero/Empty and One/Minimal (a wait of 0 s has nothing to split); WC-2 Maximum/Overflow (a flag has no capacity); WC-3 Zero/Empty and Sentinel (a question text cannot collide with a control value; an empty question is rejected by the Orca CLI usage line, CAPS:58, UNVERIFIED); WC-8 Zero/Empty (depth below 1 is not accepted, CAPS:100) and Sentinel (no sentinel); WC-1 Zero/Empty (no prompt at all passes); task confidence Zero/Empty and Maximum (not a spec-defined input).

Every GAP above is graded under FR-8/FR-9: none names a concrete wrong outcome without a further guess, so they are Medium and listed under follow-up candidates. The table is complete, so the synthesis gate (FR-10) is met.

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

Trigger: the spec describes a multi-stage flow, command inventory to verdict split to phase, where counts change between stages.

```text
[Commands in cmd/: 43 = 21 (INV-A:3) + 22 (INV-B:3)]
   --> [Split: 10 ready + 27 needs change + 6 coordinator-only = 43]   (conserved, spec:76)
   --> [Worker-capable: 37]        (6 removed at spec:128)
         |-> [3.1 ready: 10]  phases: P1 fixes 4 (adversarial, cleanup-audit, index-repo, workflow)
         |                            P2 gates 4 (reflect, release-split, tdd, troubleshoot)
         |                            no phase 2 (brainstorm, init-lite)          4+4+2 = 10 conserved
         |-> [3.2 needs change: 27] phases: P1 9, P2 11, P3 4, P4 3             9+11+4+3 = 27 conserved
   --> [P1 "Commands" cell: 13 named]            <-- MISMATCH vs
   --> [P1 "Scope" cell + AC-1.1: 37 commands]   (spec:159, spec:195)
   --> [P1 live check AC-1.2: "each P1 command" = 13]
   --> [AC-1.1 assertion count: 37 sections, 26 realisable if load has none] <-- MISMATCH (F1)
   --> [P2 command list: 15 = 11 from 3.2 + 4 from 3.1]                       (conserved, spec:160)
```

Divergence points: 13 vs 37 at P1 (F12, Medium: the scope sentence gives one reading) and 37 vs 26 at AC-1.1 (F1, blocking: the check cannot pass). The panel applies the consequence rule of `CMD:259` rather than the FR-19 label: only the second mismatch names a wrong outcome.

## Quality assessment (0-10)

Clarity 7. Completeness 7. Testability 5 (about 40 acceptance checks are concrete, but AC-1.1 and AC-0.4 cannot pass as written). Consistency 6 (counts and phase lists reconcile; the contract path and load rows do not).

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.3
  clarity: 7
  completeness: 7
  testability: 5
  consistency: 6
critical_issues:
  - {category: contradiction, severity: CRITICAL, expert: wiegers, issue: "F1 load vs AC-1.1", recommendation: "drop load from AC-1.1/AC-1.2 scope"}
  - {category: contradiction, severity: CRITICAL, expert: fowler, issue: "F2 WC-4 output-dir vs file-valued --output and per-row paths", recommendation: "one contract-location rule"}
  - {category: unpassable-check, severity: CRITICAL, expert: adzic, issue: "F3 AC-0.4 step 3 needs the P1 contract", recommendation: "limit P0 step 3 to the existing report file"}
expert_consensus:
  - "The decision (Orca on top, commands as units of work) is supported by the inventories and CAPS; no finding disputes it."
  - "Counts (43 = 10 + 27 + 6) and the phase lists reconcile line by line."
  - "The three blocking findings are all in the contract-path and acceptance-check wiring, not in the design."
improvement_roadmap:
  immediate: [F1, F2, F3]
  short_term: [F4, F5, F6, F7, F8, F9, F10, F11, F12]
  long_term: [F13, F14, F15, F16, F17, F18, F19]
adversarial_analysis: "see section above (5 attacks)"
```

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium: F4, F5, F6, F7, F8, F9, F10, F11, F12. Minor: F13, F14, F15, F16, F17, F18, F19. The command (`CMD:260`) has the session that ran the review ask the user once per loop whether to open an issue for them. This worker has no user channel and `--unattended` was not passed; no question was asked and no issue was created. The list is recorded here only.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "anchor2": "a report file would be an unrequested addition", "refs": ["AC-1.1", "AC-1.2", "3.2", "Decisions"], "claim": "AC-1.1 requires /sc:load to carry a return-contract.yaml section while its row and the Decisions table say it gets no report file, so the P1 check cannot pass."}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", "anchor2": "--unattended --output <file>` with a bare topic", "refs": ["WC-4", "2.3", "3.1", "AC-2.2"], "claim": "WC-4 puts the contract inside a directory the coordinator passes, but tdd and init-lite take a file-valued --output and adversarial and workflow fix other paths, so the contract location is contradictory."}
{"id": "F3", "severity": "CRITICAL", "blocking": true, "category": "unpassable-check", "anchor": "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1", "anchor2": "its report path is the WC-4 contract path", "refs": ["AC-0.4", "7.2", "6"], "claim": "AC-0.4 excuses only step 4 of the live check although step 3 also needs a WC-4 contract that does not exist until P1, so the P0 gate that blocks every later phase cannot pass."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "safety", "anchor": "then re-invoke or resume the command with the answer as a flag", "anchor2": "The worker stops, writes the halt to its ledger and contract, and ends `failed`.", "refs": ["WC-3", "D2", "D4"], "claim": "WC-3 lets a coordinator answer become a flag for gates that D2 and D4 reserve for the person."}
{"id": "F5", "severity": "MAJOR", "blocking": false, "category": "safety", "anchor": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)", "anchor2": "any default that pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run is off", "refs": ["P1", "WC-9"], "claim": "After P1 alone, --unattended is accepted but inert on commands whose outward defaults are only turned off in P2 or P4."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "blocks a single tool call for longer than 5 minutes", "anchor2": "no single tool call exceeds 240 s", "refs": ["WC-10", "AC-4.3"], "claim": "A 4 to 5 minute call is allowed by WC-10 and fails AC-4.3."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)", "anchor2": "Commands that already write a contract keep their fields and add the missing ones.", "refs": ["WC-4", "WC-5"], "claim": "The four statuses are not defined and may clash with the values existing contracts already use."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "including stops before any other output exists", "anchor2": "These six are never dispatched as workers and get no `--unattended` mode.", "refs": ["WC-4", "4", "D1"], "claim": "No behavior is given for --unattended without an output directory, on a coordinator-only command, as a refusal, or inside quoted content."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file.", "anchor2": "add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies", "refs": ["SA-2", "AC-C1", "P0"], "claim": "Whether the new core files may contain a command-shaped Orca example decides if AC-C1 passes, and the spec does not say."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "anchor2": "so the report path is known before dispatch (WC-4)", "refs": ["WC-6", "WC-4", "WC-3"], "claim": "Fresh-directory re-runs can make the pre-announced report path stale or overwrite the first attempt, and retries and ask resumes have no cap."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "so the session can already heartbeat between iterations", "anchor2": "Apply the section 3 row (wait splitting, summary file, HALTs as blocked)", "refs": ["3.2", "D3", "WC-10"], "claim": "The pr-submit wait reading differs from the inventories and D3(b) names a wait change the row says may be unneeded."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow", "anchor2": "every command in sections 3.1-3.2 has a `## Unattended mode` section", "refs": ["P1", "AC-1.1", "AC-1.2"], "claim": "P1 names 13 commands but its scope and AC-1.1 cover 37, so brainstorm and init-lite are in no phase cell."}
{"id": "F13", "severity": "MINOR", "blocking": false, "category": "contradiction", "anchor": "The new contract file and report files are written only in unattended mode or when the caller passes the new output flag.", "anchor2": "In unattended mode the command writes", "refs": ["SA-3", "WC-4"], "claim": "WC-4 and SA-3 give different conditions for writing the contract."}
{"id": "F14", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "calls a paid external run is off", "refs": ["WC-9"], "claim": "The term paid external run is not defined."}
{"id": "F15", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit", "refs": ["3.2"], "claim": "The nesting claim for tasklist has no layer count."}
{"id": "F16", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "This worker re-read 11 of the load-bearing locations on 2026-11-02", "refs": ["Citation conventions"], "claim": "The re-read and validator claims cannot be reproduced from the workspace."}
{"id": "F17", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "invocation_method: \"skill-direct\"", "anchor2": "so it proves the nested route, not the direct route this spec requires", "refs": ["E3", "1.4"], "claim": "E3 and 1.4(1) use the same evidence for opposite points."}
{"id": "F18", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "Any such prompt must fall back on its own well inside the readiness limit (default 60 s).", "refs": ["WC-1"], "claim": "WC-1 gives no number, no delivering phase and no check."}
{"id": "F19", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "It follows the return-contract pattern several commands already use and carries at least", "refs": ["WC-4"], "claim": "The contract has no version field."}
```

## Reviser brief

Blocking finding ids: F1, F2, F3.

Repair only the blocking findings F1, F2, F3 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Revise only text a blocking finding names. Prefer deleting or narrowing text to adding. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every added paragraph or table. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once, end with the `## Fix map` block, and do not award yourself a PASS.

verdict: FAIL
