review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md

| Header field | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (acted as the command definition in `command.md`; no slash command run) |
| run type | first review of the whole document (labelled whole-document audit of the final spec). No `--re-review` and no `--baseline` were given, so no baseline exists and `baseline: none (first review)`. |
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 57,873 bytes |
| candidate sha256 | `92073bce9aa934458a66ff79344ce2e439141e3c08d2246944949c626f472a09` (taken with `sha256sum`) |
| reviewer model actually used | `claude-sonnet-5-5` (Sonnet 5.5) |
| prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full first) |
| panel | Wiegers (lead), Adzic, Cockburn, Fowler (lead), Nygard, Whittaker, Newman, Hohpe. Crispin took part only in the Guard Condition Boundary Table completeness check. Gregory and Hightower were not convened (outside `--focus`). |
| iterations | one review (the run is one review whatever `--iterations` says) |

## Citation conventions and evidence limits
- `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`.
- Only the candidate, the README and the three inventory files exist in this sandbox. Every citation of `src/`, `EVIDENCE.md`, `CLAUDE.md`, `HOW-WE-WORK.md`, `pyproject.toml`, Orca's compiled JS or the Orca guides is UNVERIFIED here. I can check only that the candidate's `INV-*`/`CAPS:*` line numbers point at the lines it says they do.
- Verified in the sandbox: the candidate's `INV-A`, `INV-B`, `CAPS` and `README` line references (about 120 spot-checked, no wrong line found); the 43 = 21 + 22 command split; the 10 / 27 / 6 split (counted 10 rows in 3.1, 27 rows in 3.2, 6 in section 4); the phase assignment counts (Guard table and Quantity Flow Diagram below); the behaviour of the AC-C5 grep pattern (run on stdin only, no file touched).

## Findings index (every id cited anywhere in this report)
| id | Grade | Label | Expert | One line |
|---|---|---|---|---|
| B-01 | blocking | MAJOR | Whittaker / Crispin | AC-C5 (and SA-4's only mechanical guard) cannot see a deleted bullet line |
| M-01 | Medium | MAJOR | Wiegers | WC-4 contract location does not hold for adversarial, workflow, file-valued `--output`, default timestamp dirs |
| M-02 | Medium | MAJOR | Wiegers / Newman | Contract schema is prose only: no path base, no version field, "keep their fields" vs a fixed status set |
| M-03 | Medium | MAJOR | Whittaker / Nygard | WC-5 maps any report that is not failed or blocked to `succeeded`, including empty or unrecognised ones |
| M-04 | Medium | MAJOR | Wiegers | Phase coverage: brainstorm and init-lite are in no phase's command list; scope sentence, 3.1 header, AC-1.1 and load disagree |
| M-05 | Medium | MAJOR | Nygard / Newman | `--unattended` is accepted in P1 by commands whose gates convert in P2-P4; P0 brief template names a flag that does not yet exist; no capability signal |
| M-06 | Medium | MAJOR | Wiegers / Crispin | Requirements WC-1, 3, 6, 10, 11, 12 have no acceptance check (or only one command's); AC-C3 scope too narrow; AC-2.4 is racy |
| M-07 | Medium | MAJOR | Nygard | Retry/resume: WC-6 vs WC-4 vs 2.3 vs AC-3.2 give no consistent retry brief |
| M-08 | Medium | MAJOR | Fowler / Hohpe | No general rule for nested invocations; roadmap's per-wave `sc:save` clobbers single-owner keys (WC-11) |
| M-09 | Medium | MAJOR | Nygard / Cockburn | WC-3 `ask` path is not carved out for user-only gates; "once" is ambiguous for multi-gate commands |
| M-10 | Medium | MAJOR | Fowler | WC-11 is owned by "Command" but is unsatisfiable for product-editing commands in a shared worktree; fixed-path commands contradict it |
| M-11 | Medium | MAJOR | Whittaker | `--unattended` recognition rule missing; D1(a) "cannot misfire on a person" is false for free-text arguments |
| M-12 | Medium | MAJOR | Whittaker | `--unattended` with no (or an unwritable) output directory: no behaviour, so no contract |
| M-13 | Medium | MAJOR | Nygard | WC-10 cannot be met for Agent-tool fan-out calls; no coordinator stall or dead-worker policy |
| M-14 | Medium | MAJOR | Cockburn / Nygard | WC-9 terms undefined ("paid external run"); authorizing flags for post-release and `--post-pr` not defined; P2 depends on D4 although "no decision" is claimed |
| M-15 | Medium | MAJOR | Fowler / Crispin | AC-C1 vs SA-2 vs the P0 content of the core files; plugin mirror has no check |
| M-16 | Medium | MAJOR | Wiegers | roadmap and validate-roadmap "reconcile" with no winner named, so the report path stays unknowable |
| M-17 | Medium | MAJOR | Adzic | No worked example of a brief, a contract file and a `worker_done` line |
| N-01 | minor | MINOR | Wiegers | `\|` escapes inside code spans in the AC tables break copy-paste |
| N-02 | minor | MINOR | Fowler | 1.1 and 2.1 say the command changes are "limited to" the contract, while section 3 lists defect fixes |
| N-03 | minor | MINOR | Wiegers | Same pr-submit quote cited at two line ranges (`SKILL.md:37-39` and `:47-49`); `:41-64` vs `:46-64` |
| N-04 | minor | MINOR | Wiegers | Dangling ids and terms: `F-01` (SPEC:195), "ladder rung 2" (SPEC:261) |
| N-05 | minor | MINOR | Fowler | D5(b) says raising depth breaks "R1's protection against runaway fan-out", but R1 is a refusal rule |
| N-06 | minor | MINOR | Cockburn | pr-submit is counted among the 27 workers although D3(a), the recommendation, makes it coordinator-side |
| W-1 to W-6 | labels only | n/a | Whittaker | Attack labels in the Adversarial Analysis; each maps to the B-/M- ids shown in that table and carries no grade of its own |

Blocking findings open: B-01 only. All M-* findings are Medium (warnings, `follow-up candidates`) and do not fail the review. Whittaker's FR-2.x attack findings reuse these ids and are listed in the Adversarial Analysis.

## Quality assessment (0-10)
Clarity 7, Completeness 6, Testability 5, Consistency 6. The decision (section 1), the owner column on each requirement, the per-command evidence and the explicit UNVERIFIED list are strong. Weak points are the verification layer (section 7), the report-location rule, and phase bookkeeping.

## === REQUIREMENTS ANALYSIS ===

### Wiegers (requirements quality), lead
"Lacks measurable acceptance criteria. How would you validate compliance in production?" Twelve requirements (WC-1 to WC-12, SPEC:59-70) carry owner and evidence, which is good. But the acceptance layer does not cover them (M-06), and the schema they depend on is prose (M-02).

**B-01. AC-C5 and AC-0.3 cannot detect a deleted bullet line.**
- Where: `AC-C5` (SPEC:176), used by SA-4 (SPEC:149) as the only mechanical test that "edits are additive"; `AC-0.3` (SPEC:193) uses the same pattern.
- Severity: MAJOR. Grade: **blocking**. Expert: Whittaker (Sentinel Collision) confirmed by Crispin.
- Grading sentence: An implementer who follows AC-C5 as written builds a check that prints nothing, and so passes, when an existing bullet line is deleted or rewritten, and that is wrong because SPEC:176 states that "prints nothing" means "edits are additive" and SPEC:149 and SPEC:146 depend on it to keep existing gates and boundaries unchanged.
- Evidence: the pattern is `grep -E '^-[^-]'` on a `git diff -U0` (SPEC:176). A deleted markdown bullet `- Will Not: ...` appears in the diff as `-- Will Not: ...`; its second character is `-`, so `[^-]` rejects it. I ran the pattern on stdin with four diff lines: `-- Will Not: modify specs without consent` (not printed), `-foo plain line deleted` (printed), `----` (a deleted `---` rule, not printed), `-| table row deleted |` (printed). Command files are mostly bullet lists (for example the "Will Not" and "Approval Required" bullets cited at INV-A:43 and INV-A:52 and the Boundaries lists the spec relies on at SPEC:100, SPEC:110). The pattern was written to skip the `--- a/file` header, which is why it also skips every `- ` bullet.
- Concrete state trace: before, `cmd/cleanup.md` contains `- Approval Required (prompts user first)` bullets; after a P2 edit that deletes one, `git diff -U0 master...HEAD -- src/superclaude/commands/cleanup.md | grep -E '^-[^-]'` prints nothing; AC-C5 passes; the approval gate is gone from standalone use, which SA-1 forbids (SPEC:146).
- Recommendation: replace the pattern with one that excludes only the file header, for example `grep -E '^-' | grep -vE '^--- (a/|/dev/null)'` (or `git diff --numstat` and require the deleted-lines column to be 0 for files without a named defect fix). Rationale: a deleted-line count is independent of the line's first character.
- Priority: High. Quality-impact estimate: Testability +2.

**M-01. The WC-4 report location holds for only some commands.** (Medium; MAJOR label)
- WC-4 says the contract is `<output-dir>/return-contract.yaml`, "the directory the coordinator passed" (SPEC:62), and Section 3 repeats it: "Contract means the WC-4 file" (SPEC:76). The rows then disagree:
  - adversarial: fixed to `<output>/adversarial/return-contract.yaml` (SPEC:83), one directory deeper.
  - workflow: `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92); `<id>` is made at run time and the brief passes no output directory (SPEC:92).
  - tdd, init-lite, spec-panel: the only output flag is file-valued (`--output <file>`, SPEC:87, SPEC:90, SPEC:120), so there is no "directory the coordinator passed".
  - troubleshoot and reflect: the 3.1 brief passes no output flag (SPEC:88, SPEC:91) and the defaults are timestamped (INV-B:112, INV-B:242), so the path is not known before dispatch, which 2.3 requires (SPEC:73).
- AC-0.4's commands (SPEC:194) pass no output directory for troubleshoot or workflow; 7.2 step 3 requires "its report path is the WC-4 contract path" (SPEC:182).
- A sentence that does not reach blocking: an implementer can read the per-command row as an override of WC-4, or the reverse; the text allows both. Hence Medium.
- Recommendation: state one rule (the contract lives in `--report-dir <dir>` if given, else beside the main report, and `worker_done --report-path` carries the actual path), and make the AC read the path from the worker's message. Priority: High. Quality-impact: Consistency +1.5.

**M-02. The contract has no schema.** (Medium)
- WC-4 lists five fields in prose (SPEC:62). Not stated: whether `report_path` and `artifacts` are absolute or relative and to what; the `status` type for existing contracts that "keep their fields" (SPEC:62) when their own status words differ from the fixed set (SPEC:262); no `contract_version` field although workflow already versions its contract (INV-B:272, "contract 1.1"). 7.2 step 4 checks only `status` and `command` (SPEC:183).
- Recommendation: add a 12-line example YAML and a version field; say which existing status words map to which of the four. Newman: without a version, a coordinator cannot tell a stale installed command from a converted one (see M-05). Priority: Medium.

**M-03. WC-5's mapping is fail-open.** (Medium; also an FR-8 GAP, see the Guard table)
- WC-5: `failed` when the report says failed or blocked "or no report exists", `succeeded` "otherwise" (SPEC:63). A report that exists but is empty, unparseable, or has a status outside the four values (including an existing contract's own words) falls into "otherwise", so `worker_done --outcome succeeded`, which settles the Task as completed (CAPS:77) and leaves its dependents startable, whereas a failed Task keeps them blocked (CAPS:90).
- Not graded blocking: WC-4 says `status` is one of four values, so the text can be read as making the other cases a WC-4 violation rather than a WC-5 state. That is a reading, not a stated text.
- Recommendation: "succeeded only when the report parses and `status` is `succeeded` or `partial`; anything else is `failed`". Deleting "otherwise" is the smaller change. Priority: Medium. Quality-impact: Correctness +1.

**M-04. Phase coverage does not conserve the command count.** (Medium; see the Quantity Flow Diagram)
- The P1 scope says the flag is accepted by "every command in sections 3.1 and 3.2" (SPEC:159), which is 37 commands. The commands cells name 35: brainstorm (SPEC:84) and init-lite (SPEC:87) appear in no phase (SPEC:158-162). init-lite writes no return contract today (INV-A:55), so WC-4 is unmet for it if the cells govern.
- 3.1 says "The only command changes are the small fixes in the last column" (SPEC:79) and, in the same paragraph, that "Phase 1 adds the contract" (SPEC:79).
- AC-1.1 tests 12 commands (the P1 cell without load); the P1 scope sentence says load also accepts the flag (SPEC:159) while the same cell says "usage line only" and AC-1.1 exempts it (SPEC:195, SPEC:112).
- A reviewer applying FR-19 would label a dimensional mismatch CRITICAL; graded by consequence it is Medium, because the scope sentence is clear and an implementer can follow it.
- Recommendation: replace the commands cells with a single list generated from the 3.1/3.2 tables (37 names), or add "no change: brainstorm, init-lite" explicitly. Priority: High. Quality-impact: Completeness +1.

**M-16. "Reconcile" names no winner.** (Medium)
- roadmap (SPEC:118) and validate-roadmap (SPEC:124) say reconcile the command with the skill, and AC-3.1 asserts only that both name "the same report filename" (SPEC:204). Which filename wins (`validate/validation-report.md` or `02-consolidated-report.md`, INV-B:252) decides the standalone path, which SA-1 protects. Recommendation: name the surviving path in the row. Priority: Medium.

### Adzic (specification by example)
"Can you provide concrete examples demonstrating this in real-world scenarios?" **M-17.** The spec gives one command line (D1, SPEC:228) but no complete worked case. A coordinator brief (2.3, SPEC:73), a blocked contract file with `blocked_question`, and the matching `worker_done` line (WC-5) are all described and none is shown. A scenario for the central claim would pin the rest: Given `/sc:tdd "auth" --unattended --output docs/auth/TDD_AUTH.md` with a bare topic, When the worker runs it, Then `<where>/return-contract.yaml` holds `status: blocked` and a non-empty `blocked_question`, and the worker sends `--outcome failed`. Writing it exposes M-01 (where is `<where>` when `--output` is a file?) at once. Priority: Medium. Quality-impact: Clarity +1.

### Cockburn (use cases and stakeholders)
Primary actor: the Orca coordinator; supporting actors: the worker session, the command, the person. The owner column in 2.2 (SPEC:57-70) is a real strength. Gaps: **M-09** (the person is a stakeholder for user-only gates but WC-3 lets the coordinator answer); **M-14** (what the brief may authorize depends on D4, but phases 1-3 are said to need no decision); **N-06** (pr-submit is counted as a worker, SPEC:76, but D3(a) recommends it stays with the coordinator, SPEC:240, so the effective split is 10 / 26 / 7 under the recommendations).

## === ARCHITECTURE ANALYSIS ===

### Fowler (architecture and interface), lead
"This interface violates single responsibility, consider separating concerns." The decision (coordinator on top, commands as units of work, SPEC:16, SPEC:29-39) is well argued and the evidence is traceable to the inventories. Boundary observations:
- **M-08. No rule for nested invocation.** Many commands run other commands: tasklist runs N reflect subagents (SPEC:122), roadmap calls `sc:save` at every wave (INV-B:154), task calls troubleshoot on TFEP (INV-B:201), brainstorm and release-split call adversarial (INV-A:39, INV-B:37), tdd runs `/task` (SPEC:90). Only tasklist-to-reflect says to pass `--unattended` down (SPEC:122). For roadmap the P3 row never says its wave saves become per-session (SPEC:118-119), so two roadmap workers write `pm_context`, `last_session`, `next_actions` whole (INV-B:165), the clobbering WC-11 forbids (SPEC:69). Also, if N nested reflect subagents each write `<output>/return-contract.yaml`, they collide on the filename (WC-4) when they share an output directory. Recommendation: add one requirement: "a command run under `--unattended` passes it to every command it invokes and gives each its own output directory". Priority: High. Quality-impact: Consistency +1.
- **M-10. WC-11's owner cannot satisfy it.** "Two workers in one worktree must never write the same file", owner "Command" (SPEC:69). A command cannot stop two workers from editing the same product file: implement, cleanup, improve, document, test `--fix` and explain edit the tree (SPEC:103, SPEC:107, SPEC:109-110). The default placement is a shared worktree (CAPS:115). 3.1 accepts "one audit per worktree at a time" for cleanup-audit (SPEC:85), which contradicts the unqualified rule, and index-repo writes a fixed `PROJECT_INDEX.md` (INV-A:53). Recommendation: make this a coordinator duty in 2.3 (one worker per worktree for any command that edits product files or writes a fixed path), and narrow WC-11 to report and default paths. Priority: High.

### Nygard (reliability and failure modes)
"What happens when this fails? Where are the monitoring and recovery mechanisms?"
- **M-13.** WC-10 splits waits at 4 minutes (SPEC:68) but an Agent-tool call that fans out to many agents (tdd, cleanup-audit waves, adversarial, SPEC:83, SPEC:85, SPEC:90) blocks the worker's turn for the whole call and cannot be split. The text does not say these are exempt. Whether a missed heartbeat matters is itself UNVERIFIED (CAPS:130, SPEC:277). There is also no coordinator-side stall policy: what the coordinator does when no contract appears and `worker_done` never arrives (SPEC:44 admits "a silent stall with no `worker_done`"; 7.2 describes polling only as a test). A worker that dies before it writes the contract leaves no WC-4 file, and WC-5's "no report exists" rule needs a living worker. Recommendation: one paragraph in 2.3: poll cadence, how many empty polls before the coordinator reads `worker-show`/`worker-list` (CAPS:127), and that a missing contract plus an `exited` verdict means retry per WC-6. Priority: Medium.
- **M-05. Phase window.** P1 makes every command accept `--unattended` (SPEC:159) but gates convert in P2 to P4 (SPEC:160-162). Between P1 and P2, `/sc:cli-eval run --unattended` accepts the flag and still asks the suite question, which WC-2 forbids (SPEC:60). 2.3 tells the coordinator to put `--unattended` on every line (SPEC:73) but P0's brief template ships before any command knows the flag, and the 3.1 and AC-0.4 command lines omit it (SPEC:81-92, SPEC:194). There is no capability signal (Newman): a coordinator cannot tell a converted command from an old install. Recommendation: P1 accepts the flag only in commands with no gate, or the brief template carries a per-phase support table and the contract file has a version (M-02). Priority: High.
- **M-09. WC-3 is general.** It lets any blocked gate go to the coordinator, who answers and the session "re-invokes with the answer as a flag" (SPEC:61). Rules that accept only the person's confirmation are not carved out: implement's Ruling ("another agent's message ... not acceptance", INV-A:51, SPEC:233), task's "Will Not: proceed with less than 70 percent confidence without user confirmation" (INV-B:199, SPEC:121), spec-panel's "without explicit user consent" (INV-B:179). D2 protects only implement. The command's own rule would reject the relayed answer, so the likely outcome is a wasted loop, not a bypass. "Ask the coordinator once" is also unclear for cli-portify's three gates (SPEC:105): once per command or per gate. Recommendation: list the user-only gates and exclude them from WC-3, and say "once per gate, at most twice per run". Priority: Medium.
- **M-07. Retry.** WC-6: a retry must not corrupt the first attempt (SPEC:64). A retry of the same Task re-runs the same Task brief (CAPS:116); 2.3 does not say the coordinator changes the command line or output directory on retry. For commands whose resume is "fresh dir" (most of 3.2), a fresh directory under the passed one moves the contract away from `<output-dir>/return-contract.yaml` (WC-4); reusing the directory overwrites (against WC-6). AC-3.2 expects roadmap without a resume flag to "start fresh" in a directory that already has `.session-memory.md` (SPEC:205), i.e. overwrite. A coordinator-supplied fresh `--output` per attempt reconciles all of it, but no text says so (and the text gives the command, not the coordinator, that duty). Recommendation: add to 2.3 "a retry brief uses a new output directory unless it passes the command's resume flag". Priority: High.

### Newman (API evolution)
Covered in M-02 (no contract version) and M-05 (no capability signal across a five-phase rollout). Add **M-15 (part)**: `plugins/superclaude/commands/` mirrors the commands and its update rule is UNVERIFIED (SPEC:279); no acceptance check covers it, so a phase can pass with the plugin copy stale.

### Hohpe (integration)
Message pattern: pull-only follow-ups, one `worker_done`, `ask` resumed by message id (SPEC:61, SPEC:63, SPEC:70) are all consistent with CAPS:60, CAPS:66. The file contract between worker and coordinator is the weak edge (M-01, M-02, M-03). The path travels twice (inside the file and in `--report-path`, SPEC:62), and nothing says which wins on disagreement. Recommendation: the `--report-path` value is authoritative and the file must name itself. Priority: Low.

## === ADVERSARIAL ANALYSIS (Whittaker, FR-3 format) ===
Severity uses the panel scale; the Grade column applies the review-loop rule (blocking only for a concrete wrong outcome or a safety-boundary risk).

| # | Attack (method) | Invariant location | Label | Grade | Finding id |
|---|---|---|---|---|---|
| W-1 | Sentinel Collision | SPEC:176 | MAJOR | blocking | B-01 |
| W-2 | Sentinel Collision | SPEC:228 | MAJOR | Medium | M-11 |
| W-3 | Zero/Empty | SPEC:62, SPEC:63 | MAJOR | Medium | M-12, M-03 |
| W-4 | Sequence | SPEC:159-162 | MAJOR | Medium | M-05 |
| W-5 | Accumulation | SPEC:61, SPEC:68, SPEC:69 | MAJOR | Medium | M-09, M-13, M-10 |
| W-6 | Divergence | SPEC:62 vs SPEC:76, SPEC:83 | MAJOR | Medium | M-01 |

- **W-1.** I can break this specification by **Sentinel Collision**. The invariant at **AC-C5, SPEC:176** fails when **a deleted line starts with a dash, as every markdown bullet does**. Concrete attack: before: `cmd/test.md` has `- Will Not: ...`; step 1: the phase deletes it; step 2: diff line is `-- Will Not: ...`; step 3: `grep -E '^-[^-]'` rejects it because of the second dash; after: the check prints nothing and passes. Verified on stdin (see B-01).
- **W-2 (M-11).** I can break this specification by **Sentinel Collision**. The invariant at **D1(a), SPEC:228 ("cannot misfire on a person")** fails when **the literal `--unattended` appears inside a person's free-text argument**. Concrete attack: before: a person runs `/sc:troubleshoot "why does --unattended skip the prompt"` in a plain session, SA-1 expects today's behaviour (SPEC:146); step 1: the command matches the token anywhere in the argument string; step 2: unattended mode switches on; after: gates resolve as blocked or defaults, the person gets a contract file they did not ask for (SA-3, SPEC:148) and no prompt. The spec never states that the token counts only as a standalone, unquoted argument. (Cross-reference only, not evidence: the definition of this very command states that rule at `command.md:459`.)
- **W-3 (M-12, M-03).** I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4, SPEC:62 ("written on every outcome")** fails when **`--unattended` is given with no output directory, an empty one, or an unwritable one**. Concrete attack: before: brief `/sc:analyze src/x.py --unattended` (analyze has no output flag today, SPEC:99); step 1: the command must write `<output-dir>/return-contract.yaml`; step 2: no `<output-dir>` exists; after: no file is written, WC-5 sends `failed` (no report), and the coordinator cannot tell a refusal from a crash. Second attack: a 0-byte `return-contract.yaml` exists, so WC-5's "otherwise" gives `--outcome succeeded` (M-03).
- **W-4 (M-05).** I can break this specification by **Sequence Attack**. The invariant at **WC-2, SPEC:60, with the phase order, SPEC:159-162** fails when **P1 is shipped and P2 is not**. Concrete attack: before: coordinator dispatches `/sc:cli-eval run --unattended` (flag accepted since P1); step 1: the W0 suite menu still asks (INV-A:44); step 2: the worker sits at a question with no `worker_done`; after: a silent stall, the failure mode of SPEC:44.
- **W-5 (M-09, M-13, M-10).** I can break this specification by **Accumulation Attack**. The invariants at **WC-3 "once" (SPEC:61), WC-10 (SPEC:68), WC-11 (SPEC:69)** fail at **N gates, N minutes, N workers**. Concrete attack: cli-portify has three approval gates (SPEC:105): ask 1 answered, re-invoke, gate 2 blocks, "once" is spent, the run ends `failed` after the person-visible work is half done. Or: four workers in one worktree each run improve and edit `src/x.py`: no command text can prevent the overlap.
- **W-6 (M-01).** I can break this specification by **Divergence Attack**. The invariant at **SPEC:62/SPEC:76 (generic location) vs SPEC:83 (adversarial row)** fails when **both rules apply to the same command**. Concrete attack: `/sc:adversarial --output D --unattended`: WC-4 says `D/return-contract.yaml`; the row says `D/adversarial/return-contract.yaml`; AC step 3 requires the report path to be "the WC-4 contract path" (SPEC:182): one of the two texts must lose.

## Mandatory Output Artifacts

### Guard Condition Boundary Table
Triggered: the spec contains conditional logic and thresholds (flag switches, 60 s, 4 and 5 minutes, 0.70, depth 1, status values, diff-line patterns). Construction: Nygard (lead), Crispin (completeness), Whittaker (attacks). Every row has a Specified Behavior; "spec silent" in that column is itself the GAP (FR-9). Only the B-01 row is blocking under FR-8; every other GAP is Medium and its finding id is listed under follow-up candidates.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `unattended_switch` | SPEC:51,60,146 | Zero/Empty | flag absent | false | Today's behaviour exactly (SA-1) | OK |
| `unattended_switch` | SPEC:228 | One/Minimal | `--unattended` alone | true | Mode on (D1(a) example) | OK |
| `unattended_switch` | SPEC:73 | Typical | brief line with flag + output | true | Per section 3 row | OK |
| `unattended_switch` | SPEC:228 | Sentinel Value Match | literal token inside quoted free text | ambiguous | Spec silent; D1(a) claims "cannot misfire" (M-11) | GAP |
| `unattended_switch` | SPEC:128,159 | Legitimate Edge | flag sent to a section-4 command, or to a command not yet converted (P0-P1) | ambiguous | Spec silent (M-05) | GAP |
| `output_dir_present` | SPEC:62 | Zero/Empty | no output flag / `""` | false | Spec silent (M-12) | GAP |
| `output_dir_present` | SPEC:62 | Zero/Empty | unwritable or missing directory | false | Spec silent (M-12) | GAP |
| `output_dir_present` | SPEC:62,84,88 | Typical | dir passed to brainstorm, reflect, pr-submit | true | Contract at `<dir>/return-contract.yaml` | OK |
| `output_dir_present` | SPEC:83,92 | Legitimate Edge | adversarial subdirectory; workflow run-time id dir | conflict | Row differs from SPEC:76 (M-01) | GAP |
| `output_dir_present` | SPEC:87,90,120 | Legitimate Edge | file-valued `--output` (tdd, init-lite, spec-panel) | undefined | Spec silent (M-01) | GAP |
| `output_dir_present` | SPEC:122 | Sentinel Value Match | N nested reflects writing the same filename in one dir | collision | Spec silent (M-08) | GAP |
| `outcome_mapping` | SPEC:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| `outcome_mapping` | SPEC:63 | Zero/Empty | report exists, 0 bytes or unparseable | "otherwise" | `--outcome succeeded` (M-03) | GAP |
| `outcome_mapping` | SPEC:63 | One/Minimal | `status: succeeded` | true | `--outcome succeeded` | OK |
| `outcome_mapping` | SPEC:63,263 | Typical | `failed`/`blocked` -> failed; `partial`, FAIL-grade audit -> succeeded | true | Stated, with rationale (SPEC:263) | OK |
| `outcome_mapping` | SPEC:62,63 | Sentinel Value Match | `status` outside the four values | "otherwise" | `--outcome succeeded` (M-03, M-02) | GAP |
| `wait_size` | SPEC:68 | Typical | poll plus sleep iteration at or under 240 s | no split | Allowed; AC-4.3 checks pr-submit | OK |
| `wait_size` | SPEC:68,266 | Legitimate Edge | one call between 240 s and 300 s | no split needed | Margin stated (SPEC:266) | OK |
| `wait_size` | SPEC:68,104 | Legitimate Edge | cli-eval eval up to 3600 s | split to waits of 4 min | Stated for cli-eval | OK |
| `wait_size` | SPEC:68 | Maximum/Overflow | one Agent-tool fan-out call over 300 s | cannot split | Spec silent (M-13) | GAP |
| `ask_once` | SPEC:61 | Zero/Empty | no preamble (person's session) | false | Blocked-and-stop, no `ask` | OK |
| `ask_once` | SPEC:61 | Typical | first gate, preamble present | true | May ask once; timeout resumes same message id | OK |
| `ask_once` | SPEC:61,105 | Maximum/Overflow | second gate in one command (cli-portify has 3) | ambiguous | "once" undefined (M-09) | GAP |
| `ask_once` | SPEC:61,109,121 | Legitimate Edge | gate that accepts only the person's confirmation | true | Not carved out (M-09) | GAP |
| `retry_resume` | SPEC:64 | Zero/Empty | first attempt, no prior output | false | Fresh start | OK |
| `retry_resume` | SPEC:64 | One/Minimal | resume flag passed | true | Resumes from disk | OK |
| `retry_resume` | SPEC:64,62 | Typical | `--retry-of`, same brief, same output dir, flag not passed | true | WC-6 vs WC-4 disagree (M-07) | GAP |
| `retry_resume` | SPEC:205 | Legitimate Edge | roadmap with `.session-memory.md`, no flag | true | AC-3.2 "starts fresh" in same dir (M-07) | GAP |
| `retry_resume` | SPEC:85,86,69 | Sentinel Value Match | fixed paths (`.claude-audit/`, `PROJECT_INDEX.md`) | collision | Row accepts it; WC-11 forbids it (M-10) | GAP |
| `outward_default_off` | SPEC:67 | Zero/Empty | no authorizing flag | off | Off | OK |
| `outward_default_off` | SPEC:67,100 | Typical | auggie-review: `--no-post-pr --no-remediation-offer` implied | true | Stated | OK |
| `outward_default_off` | SPEC:67 | Sentinel Value Match | "paid external run", "installs, provisions": web search, real-model eval runs | undefined | Terms undefined (M-14) | GAP |
| `outward_default_off` | SPEC:67,113 | Legitimate Edge | authorizing flag for post-release steps or `--post-pr` | undefined | Flag not defined (M-14) | GAP |
| `readiness_budget` | SPEC:59 | Typical | start in 34 s | pass | Passes (EVIDENCE via CAPS:49) | OK |
| `readiness_budget` | SPEC:59 | Legitimate Edge | fallback "well inside" 60 s | undefined | No number; evidence shows 30 s passes and about 45 s fails under a 45 s limit (CAPS:49) | GAP |
| `depth_fence` | SPEC:66 | Typical | command with Agent-tool fan-out | not counted | Allowed (E4, SPEC:24) | OK |
| `depth_fence` | SPEC:66 | Legitimate Edge | command calls `worker-start` | depth 1 | Forbidden by WC-8, refused by Orca (CAPS:99) | OK |
| `additive_diff_check` | SPEC:176 | Zero/Empty | empty diff | prints nothing | Pass | OK |
| `additive_diff_check` | SPEC:176 | Typical | deleted prose line | printed | Fail (correct) | OK |
| `additive_diff_check` | SPEC:176,193 | Sentinel Value Match | deleted bullet `- x` (diff shows `-- x`), deleted `---` | not printed | Passes although a line was deleted (B-01) | GAP |
| `additive_diff_check` | SPEC:193 | Legitimate Edge | deleted table row `-\| ... \|` | printed | Fail (correct) | OK |
| `confidence_gate` (task) | SPEC:121 | Zero/Empty | confidence 0 | below 0.70 | Blocked | OK |
| `confidence_gate` (task) | SPEC:121 | Legitimate Edge | exactly 0.70 | not below | Proceeds ("below 0.70" is the stated rule) | OK |
| `confidence_gate` (task) | SPEC:121 | Typical | 0.85 | not below | Proceeds | OK |
| `cli_eval_run_inputs` | SPEC:104 | Zero/Empty | no `--suite` | missing | Blocked (AC-2.2 tests it) | OK |
| `cli_eval_run_inputs` | SPEC:104 | Legitimate Edge | suite given, one "safety flag" missing | partial | Flags not enumerated (M-06) | GAP |
| `tdd_topic_only` | SPEC:90 | One/Minimal | one-word topic | true | Blocked | OK |
| `tdd_topic_only` | SPEC:90 | Legitimate Edge | short but component-named prompt | judgement | No test for "precise" (M-06) | GAP |
| `troubleshoot_deep_input` | SPEC:91 | Legitimate Edge | `--depth deep` with 9 vs 10 words | threshold | Short-input STOP resolves as blocked; the threshold is the skill's, quoted at INV-B:239 | OK |

Omitted classes, one line each: `unattended_switch` Maximum/Overflow (a boolean has no capacity); `wait_size` Zero/Empty and Sentinel (a zero wait is a poll; no sentinel value); `depth_fence` Zero/Empty, One, Max, Sentinel (a fixed integer of 1 set by Orca, not by the spec); `readiness_budget` Zero, Max, Sentinel (an Orca constant, only its use is specified); `confidence_gate` Maximum/Sentinel (the value is bounded to 0-1 by the task skill); `cli_eval_run_inputs` and `tdd_topic_only` Max and Sentinel (a text or flag presence test); `troubleshoot_deep_input` other classes (the one threshold is the only decision); `ask_once` Sentinel (no reserved value).

### Quantity Flow Diagram (Pipeline Dimensional Analysis)
Triggered: a multi-stage flow where counts change (inventory -> verdict split -> phase assignment -> acceptance tests). Fowler annotated counts; Whittaker attacked the divergence points.

```text
[Source: 43 command files = INV-A 21 + INV-B 22 (SPEC:76)]
   --> [Verdict split: 10 ready + 27 needs-change + 6 coordinator-only = 43]  OK (counted in 3.1, 3.2, section 4)
          |
          +--> [6 coordinator-only]      --> no phase, no --unattended (SPEC:128)             OK
          |
          +--> [37 worker-capable]
                 |
                 +--> [10 ready]  --> P1 Commands cell names 4 (adversarial, cleanup-audit, index-repo, workflow)
                 |                --> P2 Commands cell names 4 (reflect, release-split, tdd, troubleshoot)
                 |                --> named nowhere: 2 (brainstorm, init-lite)             <-- MISMATCH (M-04)
                 |
                 +--> [27 needs-change] --> P1 9 (incl. load) + P2 11 + P3 4 + P4 3 = 27   OK

[Consumers of the 37]
   P1 scope sentence "flag accepted by every command in 3.1 and 3.2"   expects 37
   P1 + P2 + P3 + P4 Commands cells                                     sum to 35            <-- MISMATCH (37 vs 35)
   AC-1.1 test (P1 cell without load)                                   asserts 12 sections  <-- 12 of the 37
   2.1 "each changed command gains ## Unattended mode"                  expects 35 to 37, depends on the reading
   load: scope sentence says flag accepted; cell says "usage line only"; AC-1.1 exempts it   <-- MISMATCH (+1)

[Coordinator: N Tasks] --> [N workers] --> [N worker_done, exactly one each (WC-5)] --> [N contracts]
   a retry adds attempt 2 for the same Task: contracts per Task becomes 2 at ONE path   <-- MISMATCH (M-07)
```
FR-19 labels any dimensional mismatch CRITICAL. Graded by consequence (Review Loop bullet 2): the 37-vs-35 mismatch has an unambiguous scope sentence and is Medium (M-04); the retry mismatch needs a reading choice and is Medium (M-07). No mismatch here names a concrete wrong outcome without a further assumption.

### State Variable Registry
Not produced: `--focus correctness` was not requested. Advisory (no forced activation): the spec has 3+ numeric thresholds and several stateful files (run log, ledger, memory keys), so `--focus correctness` would add value on a later review.

### Downstream propagation (advisory)
GAP rows feed `sc:adversarial` AD-1 as priority invariants: `additive_diff_check`, `output_dir_present`, `outcome_mapping`, `retry_resume`, `ask_once`.

## Coverage
Covered: all nine sections and the Decisions and UNVERIFIED sections of the candidate (SPEC:1-285); every row of 3.1, 3.2 and section 4 against the three inventories for count, phase and cited line; all of section 7 for whether each check can fail; the Orca-fact lines the spec leans on, through `CAPS:*`.
Not covered, UNVERIFIED because the file is absent from the sandbox: `src/` command and skill files, `EVIDENCE.md`, `CLAUDE.md`, `HOW-WE-WORK.md`, `install_core.py`, `pyproject.toml`, Orca's JS and guides (including `SPEC:11`'s eleven re-read locations and `SPEC:285`'s citation-check claim). The inventories' own claims about those files were treated as the spec's evidence, not re-derived.
Not done: no command was run against the spec's proposals; the only command run was the AC-C5 pattern on stdin.

## Brief clauses overridden or constrained
- The brief asks for a reply of only `DONE <path>`. The command says the reviewing session asks the user once per loop whether to open an issue for the follow-up candidates. The fixed reply format prevents that question in this sandbox, so no question was asked and no issue was created. The coordinator is the one to put the question to the user. This does not widen or narrow the review scope.
- No brief clause graded a minor finding as blocking or widened the scope; none needed to be overridden.

## Follow-up candidates (Medium and minor; none triggers a revision, none appears in the Reviser brief)
Medium: M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08, M-09, M-10, M-11, M-12, M-13, M-14, M-15, M-16, M-17.
Minor notes:
- N-01: AC tables write `\|` inside code spans (SPEC:172, SPEC:175, SPEC:176); copying the raw text into a shell breaks the pipe. Put the commands in fenced blocks.
- N-02: SPEC:16 and SPEC:51 say command changes are "limited to" the contract, while WC-8 to WC-11 and the "Other required change" column (SPEC:97-125) add further change types; SA-4 covers it, the wording should match.
- N-03: the pr-submit top-level quote is cited at `SKILL.md:37-39` (SPEC:65) and at `:47-49` (CAPS:161), and the poll budget at `:41-64` (SPEC:239, INV-B:299) and `:46-64` (SPEC:68, SPEC:114). Different copies of the file are the likely cause. UNVERIFIED.
- N-04: `F-01` (SPEC:195) names a finding from a review not included in the spec, and "ladder rung 2" (SPEC:261) is never defined.
- N-05: D5(b) (SPEC:252) says raising depth would "break R1's protection against runaway fan-out", but R1 (SPEC:33) is a reason the alternative is refused, not a protection.
- N-06: pr-submit stays in the count of 27 (SPEC:76) while D3(a) recommends keeping it with the coordinator (SPEC:240).
- Also M-06 detail: no acceptance check exists for WC-1 (launch setup), WC-3 (ask path), WC-6 (retry), WC-12; WC-10 is checked only for pr-submit (AC-4.3) and WC-11 only for save (AC-3.4); AC-C3 runs only `tests/skills/` (SPEC:174) although P0 edits `install_core.py` (SPEC:52, SPEC:158); AC-2.4 counts all reviews and comments on a fork PR (SPEC:202), which the Augment and Codex reviewers can change during the run. Use a count filtered to the worker's own login.
- Also M-14 detail: P2 contains auggie-review's explicit posting flag and task's `commit`/`push` authorization (SPEC:100, SPEC:121), which D4 governs (SPEC:244), while SPEC:154 says phases 1-3 need no user decision.
- Also M-15 detail: SA-2 permits one Orca mention in the contract file (SPEC:147) and P0 adds an Orca section to `HOW-WE-WORK.md` (SPEC:158), whose baseline is 0 mentions (SPEC:25), while AC-C1 requires its grep over `src/superclaude/core` to print nothing (SPEC:172). The two agree only if no added text spells `orca orchestration ...` in lower case. The plugin mirror (SPEC:279) has no check.

## Reviser brief
Blocking finding ids: B-01.

Rules for the reviser (Review Loop bullet 6, restated; the reviser reads this report, not the command): revise only text that a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

B-01 text to repair: `AC-C5` (SPEC:176) and, because it uses the same pattern, `AC-0.3` (SPEC:193). Replace the `grep -E '^-[^-]'` filter with one that excludes only the diff file header, so a deleted line that starts with a dash is reported.

verdict: FAIL
