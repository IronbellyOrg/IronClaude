review: 1 of 3

# Spec-panel critique, round 1: Orca worker-contract spec

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full before this review).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57763 bytes)
- baseline: not applicable (first review; no `--re-review`, no `--baseline` given)
- reviewer model actually used: `claude-sonnet-5-5`
- Mode and scope: critique, first review of the full document. Improve step (step 6) not run: the brief says edit nothing else, and the command's Will Not forbids modifying a specification without consent (`command.md:481`). `--iterations` not used. No brief clause was overridden.
- Citation key: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `command.md:N` = the `/sc:spec-panel` definition given to this run.

## Coverage

Covered: all 285 lines of the candidate (sections 1-9, Decisions, UNVERIFIED), `README.md` in full, and all three inventories in full. Spot-checked about 120 `INV-A`, `INV-B` and `CAPS` citations in the candidate against the inventory lines: every one I checked pointed at the claimed row or section.

Not checkable: every citation to a file outside `.dev/orca-command-refactor/` (`src/superclaude/...`, `CLAUDE.md`, `HOW-WE-WORK.md`, `.dev/evals/.../EVIDENCE.md`, `.dev/codegraph-migration/...`, `Makefile`, `pyproject.toml`) is UNVERIFIED here. Where a claim rests only on such a file I say so. I ran one shell test (finding F-3) and no other command.

## Input detection

The input is a spec, not a TDD (no `parent_doc`/`coordinator` frontmatter, no numbered `## N.` headings of the TDD form) and not a PRD (no personas, JTBD or PRD sections). Steps 6a-6d do not apply.

## Panel (review order per `command.md:103-113`)

Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture and adversarial); Crispin (completeness check of the Guard Condition Boundary Table and the acceptance checks, as `command.md:315` requires). Gregory and Hightower: no finding.

## Findings

Grading used: for each blocking finding I wrote the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding that needs a guess about which of two allowed readings the implementer picks, or that is a requirement the document never states, is Medium and sits under `follow-up candidates`.

### Blocking findings (3)

#### F-1. Phase 1 puts `--unattended` and an `## Unattended mode` section on every command, before the phases that make the flag safe
- Severity label: MAJOR. Grade: blocking. Experts: Wiegers (consistency), Nygard (what happens when the flag exists but the gate is not converted), Whittaker (sequence attack). Priority: High.
- Stated texts that collide:
  - P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)", and P1's rationale: "No person gate is involved, so each change is mechanical" (S:159).
  - AC-1.1, a P1 check: the test asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one" (S:195).
  - Gate conversion is P2 (S:160), and P4 "waits for answers to D2-D4" and holds implement, post-release and pr-submit (S:154, S:162).
  - WC-9: "Under `--unattended`, any default that pushes, opens a PR, posts to GitHub ... is off" (S:67). WC-2: under `--unattended` the command never prompts (S:60).
  - Rows that contradict AC-1.1: load has "Report: none" and phase "P1 (usage line only)" (S:112); D3(a), the recommendation, says pr-submit gets "no pr-submit changes in Phase 4" and section 4 says pr-submit "stays a worker candidate only if the user accepts open decision D3" (S:240, S:139).
- Grading sentence: An implementer who follows S:159 and S:195 as written adds `--unattended` plus a section that names `return-contract.yaml` to every command in 3.1 and 3.2 in Phase 1. That includes auggie-review, whose PR-posting default and remediation wait stay on until P2 (S:100, S:160; `INV-A:38`, `INV-A:78`), and implement, post-release and pr-submit, whose gates and outward actions wait for D2-D4 (S:162; `INV-B:33-34`). After P1 passes, those commands accept the flag that WC-9 and WC-2 say turns outward defaults and prompts off, while the defaults are still on. The wrong outcome is a coordinator that trusts the flag and gets a posted GitHub review, a push, or a stalled prompt (the silent stall of S:44). AC-1.1 also cannot pass for load (no contract file to name, S:112) and cannot pass together with D3(a), where pr-submit carries no unattended section.
- Quantity check (FR-19, see flow diagram): P1's flag scope names 37 commands (10 in 3.1 plus 27 in 3.2); P1's own command column names 13 (9 gate-free commands plus 4 fixes, S:159). The other 24 are changed in P2-P4 or not at all, so the "every command" count and the P1 command list diverge.
- Recommendation (narrow, do not add): limit P1's flag and section scope, and AC-1.1's quantifier, to the commands P1 lists; state that a command first accepts `--unattended` in the phase that converts its gates; drop load and pr-submit (while D3 is open) from AC-1.1's universal set.
- Quality impact: safety boundary (outward actions); blocks a correct Phase 1 acceptance run.

#### F-2. AC-0.4 requires a WC-4 contract for P0 smoke runs, but P0 has no command edits and two of the three smoke commands write none at the WC-4 path
- Severity label: MAJOR. Grade: blocking. Experts: Crispin (acceptance criteria), Adzic (concrete example fails), Wiegers (testability). Priority: High.
- Stated texts:
  - P0 is "no command edits" (S:158).
  - AC-0.4: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1 ... a failure here reopens section 1" (S:194).
  - 7.2 step 3 pass condition: "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (S:182). Step 4 is the only step AC-0.4 relaxes.
  - WC-4 defines that path as `<output-dir>/return-contract.yaml` (S:62).
  - Smoke command 1, troubleshoot: its report is `REPORT.md`, and `return-contract.yaml` is written "only when `--caller task-unified`" (`INV-B:242`; S:91 lists only `REPORT.md`). Smoke command 3, adversarial: the contract filename "is not fixed" until the P1 fix (S:83; `INV-A:35`, `INV-A:60`). Smoke command 2, workflow: its contract is at `.dev/tasks/to-do/<id>/return-contract.yaml` (S:92), a run-time id, not an `<output-dir>` the coordinator passed.
- Grading sentence: An implementer who follows AC-0.4 and step 3 as written runs `/sc:troubleshoot` in P0 and must find a contract `status` and a report path equal to the WC-4 contract path; no such file exists (P0 edits no command, troubleshoot writes `REPORT.md`), so step 3 cannot pass, and AC-0.4 says that failure "reopens section 1". The wrong outcome is the spec's central decision being reopened by an inconsistency inside the spec's own check, not by any evidence about Orca workers.
- Recommendation: make AC-0.4 step 3 name the command's existing report file for P0 (as it already does for step 4) and define the outcome check against that file's own verdict; keep the contract check for P1 onward.
- Quality impact: the only live test of the decision (S:43, S:272) is unrunnable as written.

#### F-3. AC-C5 and AC-0.3 use `grep -E '^-[^-]'`, which does not detect a deleted markdown bullet, so "edits are additive" is not proved
- Severity label: MAJOR. Grade: blocking. Experts: Whittaker (zero/empty and sentinel attacks on the guard), Crispin (check completeness), Nygard. Priority: High.
- Stated texts: AC-C5, every phase: `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md | grep -E '^-[^-]'` "prints nothing: edits are additive" (S:176); AC-0.3 uses the same pattern for HOW-WE-WORK.md (S:193). SA-4 and SA-1 depend on additivity (S:146, S:149).
- Evidence: I ran the pattern on a sample diff holding a deleted bullet `-- Will Not: modify specs without consent` and a deleted prose line `-Plain removed line`. It printed only the prose line. A deleted bullet appears in a diff as `-` plus `- ...`, i.e. it starts `--`, which `[^-]` excludes. Command files carry their boundaries and gates as bullets (`command.md:471-481`; the inventories cite "Will Not" and approval-gate bullets throughout, for example `INV-A:35`, `INV-A:43`).
- Grading sentence: An implementer who follows AC-C5 builds a gate that prints nothing and passes when a phase deletes an existing "Will Not" bullet or an approval-gate bullet from a command file, and that is wrong because AC-C5 is the spec's only mechanical proof that standalone behaviour (SA-1) and safety lines are untouched. (AC-0.3 is safe in practice because routing rows start with `|`; AC-C5 is not.)
- Recommendation: replace the pattern with one that lists all removed lines (for example `grep -E '^-' | grep -vE '^---'` on the diff body) and say which removals the named defect fixes allow.
- Quality impact: safety lines can disappear while every acceptance check passes.

### Medium findings (warnings, follow-up candidates)

None of these triggers a revision. Each needs a guess about which reading the implementer picks, or is a requirement the document never states.

- **M-1. Contract path is undefined where `--output` is a file.** WC-4 puts the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", known before dispatch (S:62). But tdd's brief passes `--output <file>` (S:90), init-lite `--output <file>` (S:87), and spec-panel gets "add `--output`" (S:120). The contract location for a file-valued flag is not stated. Workflow's pre-creation STOP has no package directory yet, and S:92 asks for a contract there without a location (`INV-B:272` notes it is not written for pre-creation STOPs). Experts: Wiegers, Fowler.
- **M-2. Section 1.4(2) is stated as fact on evidence the workspace cannot confirm.** The spec says a command's own `AskUserQuestion` "comes *after* readiness, so it does not fail `worker-start`" (S:44). `README:13` states the opposite shape ("a supervised Claude worker that waits on a question fails Orca's 60-second readiness limit"). The supporting `EVIDENCE.md:39` is outside the workspace (UNVERIFIED), and `CAPS:47` shows Claude receives the task on its command line (`promptInjectionMode: 'argv'`), so a command that asks in its first turn may run before the "fresh composer" check is satisfied. The effect on requirements is small because WC-2 removes prompts anyway; the sentence should carry an UNVERIFIED mark. Experts: Nygard, Wiegers.
- **M-3. WC-3 says the worker "may" ask the coordinator; AC-2.2 expects `worker_done --outcome failed` with `status: blocked`.** A worker that takes the optional `ask` path (S:61) ends differently from the outcome AC-2.2 expects (S:200), and the brief template (S:73) does not say which path to use. Expert: Adzic.
- **M-4. No rule for `--unattended` with no output directory.** WC-4 writes the contract "on every outcome" in a directory the coordinator passes (S:62); only post-release is told to block when `--output` is missing (S:113). For the other commands, a missing directory leaves nowhere to write the contract. Expert: Whittaker (zero/empty attack).
- **M-5. Mapping gap in WC-5.** "`--outcome succeeded` otherwise" (S:63) covers an existing contract whose `status` is missing, unknown or empty (7.2 step 4 itself tests `test -s`, S:183). A truncated contract would settle the Task as succeeded and, by `CAPS:86-90`, unblock dependents. Expert: Whittaker.
- **M-6. WC-10 and AC-4.3 use different thresholds.** WC-10 requires splitting only a call "longer than 5 minutes" into waits of "at most 4 minutes" (S:68); AC-4.3 fails any "single tool call [that] exceeds 240 s" (S:210), and the pr-submit row says "stays under 4 minutes" (S:114). A 4.5-minute call passes WC-10 and fails AC-4.3. Experts: Nygard, Crispin.
- **M-7. WC-9 names a mechanism that does not exist for several commands.** Outward actions turn on "only through the command's own explicit flag written in the brief" (S:67), but post-release (S:113) and task commit/push (S:121) have no such flag in the spec, and D4 option (a) says the coordinator "passes the command's explicit flag" (S:245) without defining one. Expert: Wiegers.
- **M-8. Section 6 says "Phases 1-3 need no user decision" (S:154); D1 (flag versus detection, S:227-230) and D4 (auggie-review `--post-pr`, task commit/push, S:244) touch P1 and P2.** Section 9 resolves it ("can proceed on the recommendations", S:225), but the two sentences differ. Expert: Cockburn (who decides).
- **M-9. How a worker runs a slash command is not specified.** WC-7 says the worker "runs the command directly" (S:65) and the brief carries "the exact command line" (S:73), but the worker's task text starts with an Orca preamble, not `/sc:...`. Whether the command loads as a slash command or through the Skill tool is not stated; only AC-0.4 would discover it, and per F-2 that check has a defect. UNVERIFIED either way (`INV-B:323`). Expert: Fowler.
- **M-10. WC-11 versus the "ready" list.** cleanup-audit writes a fixed `.claude-audit/` and index-repo writes `PROJECT_INDEX.md` (S:85-86), which WC-11 ("default output paths carry a timestamp or slug", S:69) rules out; the rows note the clash for cleanup-audit only. A retry (`--retry-of`) into a fresh-directory command also has no stated rule that the coordinator passes a new directory (S:64, S:73). Expert: Newman.
- **M-11. AC-C1 versus P0's own additions.** AC-C1 greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and requires no output (S:172). P0 adds an Orca section to HOW-WE-WORK.md and a contract file that mentions the coordinator's question channel (S:52, S:158); any wording there that names those verbs fails AC-C1, and SA-2 allows only one kind of mention (S:147). The E5 baseline (S:25) cannot be checked here (UNVERIFIED). The pattern is also written with `\|` inside a markdown table, which breaks if copied from source. Expert: Crispin.
- **M-12. AC-C5 cannot pass when a flag is added to an existing Usage line.** Adding `[--unattended]` to a command's one-line Usage changes that line (a `-` line), but SA-4 calls flag additions "additive" (S:149, S:176). Which of the two wins is not stated. Expert: Crispin.
- **M-13. AC-2.4 counts reviews and comments with `gh api ... --jq length`** (S:202). The API returns 30 items per page by default, so a PR with more than 30 would show 30 before and after. Needs `--paginate`. Expert: Crispin.
- **M-14. Section 1.1 says commands change only in three ways (S:16); section 3.2 lists further required changes** (explain adds Write, validate-tests target, cli-portify checkout-only, save per-session keys, S:108, S:125, S:105, S:119) that SA-4 names (S:149). Cosmetic; widen the sentence. Expert: Cockburn.
- **M-15. Possible stale premise for spec-panel (UNVERIFIED).** S:120 says to "add `--output`". The `/sc:spec-panel` definition this run uses already has `--output <file>` (`command.md:22-23`) and an unattended mode that uses `--report-dir` with `<report-dir>/return-contract.yaml` (`command.md:455-465`). `cmd/spec-panel.md` is not in the workspace, so I cannot say which version the spec's inventory read. Worth a check against the repo before P2. Expert: Newman (API evolution).
- **M-16. Session skill listing includes commands the inventories do not cover (UNVERIFIED).** The skill list shown to this session includes `sc:issue` (whose description says it creates an Orca worktree and launches an agent), `sc:impact` and `sc:graph`, none of which appears among the 43 commands in the inventories or in E5's "no command calls Orca" claim (S:25). This comes from the session environment, not a workspace file, and may reflect a different repo version. If true, E5 and AC-C1's baseline need re-running. Expert: Fowler.

### Minor notes

- `partial` mapped to `succeeded` (S:263) is explained and mitigated by the coordinator opening the report (S:73); no action.
- "Two mirrored copies" of HOW-WE-WORK.md (S:158) are checked by AC-0.2 for only one (`cmp`, S:192); the other is "the level-table test the repo already runs". Fine if that test exists (UNVERIFIED).
- Section 6 line 164 and SA-1's HOW-WE-WORK line numbers (S:146, S:164) cite files outside the workspace (UNVERIFIED).
- The spec states its own UNVERIFIED list well (S:271-285); items 1 and 13 are the ones that bear on the decision.

## === REQUIREMENTS ANALYSIS ===

- **Wiegers (lead).** The requirement set WC-1 to WC-12 is clear and each has an owner and evidence (S:57-70). Weaknesses: the contract location (M-1, M-4), the undefined authorization flag (M-7), and the phase scope that conflicts with the safety requirement (F-1). Traceability from each section-3 row to a check is good, except that AC-1.1 quantifies over rows it should not (F-1).
- **Adzic.** The examples are concrete (`/sc:tdd "auth" --unattended --output <file>`, `/sc:cli-eval run --unattended`, S:200). The P0 example for troubleshoot cannot satisfy its own step 3 (F-2). No example shows the `ask` path in WC-3 (M-3).
- **Cockburn.** The primary actors are named (coordinator, worker session, command, person) and the "who decides" structure of D1-D5 is clear. The only gap is M-8.

## === ARCHITECTURE ANALYSIS ===

- **Fowler (lead).** The boundary is sound: Orca above, commands as units of work, one shared contract file instead of per-command Orca logic (S:16, S:52, S:264). The rejected alternative has five reasons, each with a cited line (S:31-37) that matches `CAPS:97-103, 145-150` and `INV-A:90`, `INV-B:285-286`. The one structural weakness is the phase plan, where interface changes (the flag) are scheduled apart from the behaviour that makes them safe (F-1).
- **Newman.** Versioning: the spec adds flags and a section, keeps standalone defaults (SA-1 to SA-6), and keeps reflect's headless rule (SA-6). Command/skill interface drift is acknowledged and scheduled (P3). See M-15 on a possibly stale spec-panel premise.
- **Hohpe.** Message exchange is specified: one `worker_done`, exactly once, from the top-level session; `ask` resumed by message ID; `check` before done; no lifecycle messages from subagents (S:61, S:63, S:65, S:70). Ordering and delivery are covered by the Orca facts in `CAPS:58-67`.
- **Nygard.** Failure modes mostly covered: blocked, partial, failed, retry and fresh-directory re-run, stalled worker visible through `agentWait` (S:60, S:64, S:181). Gaps: invalid contract status (M-5), missing output directory (M-4), threshold mismatch (M-6).

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Template per `command.md:82`. Each of the five methodologies was applied to the spec's invariants; findings that did not break an invariant are not listed.

1. I can break this specification by **Sequence Attack**. The invariant at **WC-9 (S:67) together with P1 scope (S:159)** fails when **a coordinator dispatches auggie-review after Phase 1 but before Phase 2**. Concrete attack: (before) auggie-review has no unattended handling, outward default "post to GitHub" on (`INV-A:38`); (P1 passes) the command accepts `--unattended` as a no-op; (after) the coordinator runs `/sc:auggie-review 123 --unattended`, the command posts a PR review and offers remediation, outward state changed and the worker waits. Maps to F-1.
2. I can break this specification by **Zero/Empty Attack**. The invariant at **AC-C5 (S:176)** fails when **a phase deletes a bullet**. Concrete attack: (before) a command file has `- Will Not: modify specifications without explicit user consent`; (after) the bullet is removed; the diff line is `-- Will Not: ...`; `grep -E '^-[^-]'` prints nothing; the check passes. Maps to F-3.
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **D1(a) and WC-2 (S:51, S:60, S:228)** ("a person never types it"; the mode applies when the caller passes `--unattended`) fails when **the token appears inside quoted user content**, for example `/sc:tdd "explain the --unattended flag"`. The spec does not say that only a standalone token outside quoted arguments switches the mode (the `/sc:spec-panel` definition does, `command.md:459`), so user data can act as a control signal. Medium (follow-up): see G-8 below.
4. I can break this specification by **Divergence Attack**. The invariant at **WC-10 (S:68)** fails when **a single call lasts between 4 and 5 minutes**. Concrete attack: a 270 s wait: WC-10 requires no split; AC-4.3 rejects it. Maps to M-6.
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-6 and 7.2 step 7 (S:64, S:186)** fails when **retries accumulate**. The circuit breaker counts three failed starts per Task (`CAPS:80`, `CAPS:116`); a fresh-directory command retried three times needs three new directories, and nothing tells the coordinator to pass one (M-10). Low risk.

## === GUARD CONDITION BOUNDARY TABLE ===

Trigger: the spec contains threshold checks and conditional logic (outcome mapping, wait size, resume, flag activation, grep gates), so the table is produced (`command.md:313`). Construction: Nygard; completeness: Crispin; attack: Whittaker. Input classes that cannot occur for a guard are left out with a one-line reason below the table. All guards enumerated: G-1 WC-5 outcome map; G-2 WC-10 wait size; G-3 WC-6 resume; G-4 WC-4 output directory; G-5 WC-9 outward flag; G-6 AC-C5 diff gate; G-7 D3 pr-submit workability; G-8 `--unattended` activation.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| G-1 outcome map | S:63 | Zero/Empty | no contract file | true (failed) | `--outcome failed` | OK |
| G-1 outcome map | S:63 | Zero/Empty | contract exists, empty or `status` missing or unknown | true (succeeded, by "otherwise") | succeeded; no stated handling | GAP (M-5) |
| G-1 outcome map | S:63 | One/Minimal | `status: partial` | true (succeeded) | succeeded, first sentence says partial (S:63, S:263) | OK |
| G-1 outcome map | S:63 | Typical | `status: succeeded` / `failed` | true | succeeded / failed | OK |
| G-1 outcome map | S:63 | Sentinel Value Match | `status: blocked`, `blocked_question` empty | true (failed) | WC-4 requires a question (S:62), AC-2.2 checks non-empty (S:200); worker behaviour when empty not stated | GAP (M-5) |
| G-1 outcome map | S:63 | Legitimate Edge Case | audit report with verdict FAIL | succeeded | succeeded, audit itself succeeded | OK |
| G-2 wait size | S:68 | Zero/Empty | no long wait | n/a | no split needed | OK |
| G-2 wait size | S:68 | Typical | single call 3 min | false | no split | OK |
| G-2 wait size | S:68 | Legitimate Edge Case | single call 4-5 min (270 s) | false (not "longer than 5") | WC-10 allows; AC-4.3 rejects (S:210) | GAP (M-6) |
| G-2 wait size | S:68 | Maximum/Overflow | cli-eval 3600 s wait | true | split into waits of at most 4 min (S:104) | OK |
| G-3 resume | S:64 | Zero/Empty | no resume flag, no prior state | fresh | writes into a fresh directory | OK |
| G-3 resume | S:64 | Legitimate Edge Case | resume flag given, state missing or corrupt | unspecified | not stated (AC-3.2 covers only "state present, no flag", S:205) | GAP (follow-up, with M-10) |
| G-4 output directory | S:62 | Zero/Empty | `--unattended`, no output directory | unspecified | only post-release says blocked (S:113) | GAP (M-4) |
| G-4 output directory | S:62 | Legitimate Edge Case | `--output` is a file (tdd, init-lite, spec-panel) | unspecified | contract location not stated | GAP (M-1) |
| G-4 output directory | S:62 | Typical | directory passed | true | contract at `<dir>/return-contract.yaml` | OK |
| G-5 outward flag | S:67 | Zero/Empty | `--unattended`, no authorization flag | outward off | off | OK |
| G-5 outward flag | S:67 | Legitimate Edge Case | command has no explicit flag (post-release, task commit/push) | unspecified | no flag defined (S:113, S:121) | GAP (M-7) |
| G-5 outward flag | S:67 | Sentinel Value Match | `--post-pr` and `--no-post-pr` both present | unspecified | not stated | GAP (minor, folded into M-7) |
| G-6 AC-C5 diff gate | S:176 | Zero/Empty | no removed lines | prints nothing | pass | OK |
| G-6 AC-C5 diff gate | S:176 | One/Minimal | one removed prose line | prints it | fail | OK |
| G-6 AC-C5 diff gate | S:176 | Legitimate Edge Case | one removed bullet (`-- ...`) | prints nothing | pass (wrong) | GAP (F-3) |
| G-6 AC-C5 diff gate | S:176 | Sentinel Value Match | added flag on an existing Usage line | prints the old line | fail although SA-4 calls it additive | GAP (M-12) |
| G-7 pr-submit as worker | S:139, S:195, S:240 | Legitimate Edge Case | D3(a) chosen | pr-submit unchanged | AC-1.1 still requires its unattended section | GAP (F-1) |
| G-8 flag activation | S:51, S:228 | Typical | standalone `--unattended` | true | unattended mode | OK |
| G-8 flag activation | S:51, S:228 | Sentinel Value Match | `--unattended` inside quoted content | unspecified | not stated | GAP (Medium; see adversarial finding 3) |
| G-8 flag activation | S:51, S:228 | Zero/Empty | no flag | false | today's behaviour (SA-1, S:146) | OK |

Classes left out: Maximum/Overflow for G-1, G-3, G-4, G-5, G-6, G-8, and One/Minimal for G-2, G-3, G-4, G-5, G-8: these guards take a state or a flag, not a quantity, so an overflow or one-item class cannot occur.

FR-8/FR-9 grading: GAP rows that name a concrete wrong outcome and are stated text, not a missing requirement, are carried as F-1, F-3. The remaining GAP rows are missing requirements and are Medium (M-1, M-4, M-5, M-6, M-7, M-12; G-3 and G-8 GAPs listed here as follow-up).

## Pipeline Dimensional Analysis (FR-17 to FR-21)

Trigger met: the document classifies a command set in stages and schedules a rollout in stages where counts change.

```text
[43 commands in cmd/ (21 INV-A:3 + 22 INV-B:3)] --> [Classification (S:76)] --> [10 ready (S:78)]
                                                                           --> [27 needs change (S:94)]
                                                                           --> [ 6 coordinator-only (S:127)]
                                                                               (10 + 27 + 6 = 43: conserved)
[10 ready + 27 changed = 37 commands]
   |--> [P1 flag scope "every command in 3.1 and 3.2" (S:159): 37 commands]      <-- MISMATCH
   |--> [P1 command column (S:159): 9 gate-free + 4 fixes = 13 named]
   |--> [P2 (S:160): 15] [P3 (S:161): 4] [P4 (S:162): 3]
        (27 section-3.2 rows = P1 9 + P2 11 + P3 4 + P4 3: conserved;
         section-3.1 commands: 4 fixed in P1, 4 in P2, 2 unchanged)
[AC-1.1 (S:195): consumes the 37]  [P1 live check AC-1.2 (S:196): consumes the P1 commands only]
```

Divergence: the flag/section step consumes 37 commands in P1 while the work behind it is done for 13; that is F-1. The classification split and the per-phase command counts themselves are consistent (checked by counting the rows of S:81-91, S:97-125 and S:127-137).

## Expert consensus and disagreements

- Consensus: the decision (Orca on top, commands as units of work) is well supported by the checkable evidence (`CAPS:97-103`, `CAPS:145-150`, `INV-A:90`, `INV-B:285-286`, `INV-B:323`), and section 1.4 states its own limits honestly. The panel agrees nothing in sections 1-5 needs structural change.
- Disagreement: Wiegers would grade M-1 and M-4 blocking because "known before dispatch" (S:62) is a hard requirement of the contract; Fowler and Nygard graded them Medium because the spec's own rows supply a location for each command that has a gate and the failure shows up in the first P1 live check. Under the grading rules (a requirement the text never states is Medium) they stay Medium.

## Priority-ranked improvements

1. F-1 (High): limit P1 flag/section scope and AC-1.1 to P1's own commands.
2. F-2 (High): make AC-0.4 step 3 refer to the existing report files in P0.
3. F-3 (High): fix the AC-C5 pattern.
4. Then M-1, M-4, M-5, M-7 (contract and authorization details), then M-6, M-12, M-11 (check hygiene).

## Follow-up candidates

Medium and minor findings, none blocking: M-1 to M-16, the G-3 and G-8 GAP rows, and the minor notes above. The session that ran this review would ask the user once whether to open an issue for them; this run cannot hold a conversation, so no question was asked and no issue was created. The coordinator should ask once for this loop.

## Reviser brief

Blocking finding ids: F-1, F-2, F-3.

Rules for the reviser (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS. The loop allows at most 2 fix cycles (3 reviews).

verdict: FAIL


## Findings block

```findings-v1
{"id": "F-1", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)", "anchor2": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "refs": ["AC-1.1", "WC-9", "WC-2"], "claim": "P1 adds the flag to commands whose gates and outward defaults are still on until later phases."}
{"id": "F-2", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "its report path is the WC-4 contract path", "anchor2": "step 4 uses the command's existing report file, since the contract arrives in P1", "refs": ["AC-0.4", "WC-4"], "claim": "AC-0.4 requires a WC-4 contract for P0 smoke runs that have no command edits."}
{"id": "F-3", "severity": "MAJOR", "blocking": true, "category": "other", "anchor": "grep -E '^-[^-]'", "refs": ["AC-C5", "AC-0.3"], "claim": "The additive-edit check does not detect a deleted bullet."}
```
