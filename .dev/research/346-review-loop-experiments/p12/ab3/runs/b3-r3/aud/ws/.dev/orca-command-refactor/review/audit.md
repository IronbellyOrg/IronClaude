review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document audit, first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines
- candidate sha256: `0962971bc5e9e3d54fa29ae20237450890eefb0d54ec5b262606d398c0bb57e2`
- baseline: not given. `--re-review` not given. This is a first review of the full document (label: whole-document audit of the final spec). Not a scoped PASS.
- reviewer model used: claude-sonnet-5-5
- panel (fixed order): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture plus the always-on adversarial seat). Crispin, Gregory, Hightower are outside the `--focus` set and spoke only where noted.

## Coverage statement

Covered: all 285 lines of the spec; `.dev/orca-command-refactor/README.md` (binding context, read first); all three inventories at the line numbers the spec cites as `INV-A`, `INV-B`, `CAPS`.
- Spec citations to `INV-A:N`, `INV-B:N`, `CAPS:N`: I opened and checked about 40 distinct ones (for example `INV-A:14,62,66,90,95-98,106,113,118,120`; `INV-B:36,65,105,107-115,209-215,285-301,311,314,320,323`; `CAPS:44-67,72-80,84-103,107-116,129-130,145-161,177-188`). Each supports its claim. Two small overreaches are in F-06 and N-2.
- Spec citations to `src/superclaude/...`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `orca-data.json`, and the `grep` runs in E5: **UNVERIFIED** here. None of those files exist in the sandbox workspace. Where the spec quotes them through an inventory line, I checked the inventory line only.
- Not covered: the truth of any inventory line against its source; any live Orca behaviour; the "340 citations" claim at spec line 285.
- No git history, parent directory or file outside the workspace was read.

## Guard Condition Boundary Table (Nygard builds, Crispin completes, Whittaker attacks)

Trigger: the spec has thresholds, boolean guards and sentinel flags. The table is complete before synthesis. A class a guard cannot take is left out with a one-line reason under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 readiness limit (WC-1) | spec:59 | Zero/Empty | `--timeout-ms 0` or unset | default 60 s | `CAPS:44` says the caller value is used only when positive and finite | OK |
| G1 | spec:59 | Maximum/Overflow | very large `--timeout-ms` | n/a | upper bound unread (`CAPS:54`) | GAP (does not change any spec requirement; note) |
| G1 | spec:59 | Legitimate Edge Case | fallback of 45 s | fails | `EVIDENCE.md:56` via spec:59 (UNVERIFIED source) | OK |
| G2 `--unattended` switch (D1) | spec:51,227-230 | Zero/Empty | flag absent | standalone | SA-1 (spec:146) | OK |
| G2 | spec:57-60 | Typical | flag present, no person-mode flag | gates resolve per row | section 3 | OK |
| G2 | spec:83,84,89 | Legitimate Edge Case | `--unattended` together with `--interactive` | undefined for adversarial, brainstorm, release-split | rows say "never `--interactive`" as a brief rule, while cleanup, improve, business-panel, explain, test, pr-submit, roadmap say "refused" (spec:100,103,108,110,114,118,123) | GAP (F-03) |
| G3 gate resolution (WC-2) | spec:60 | Sequence | gate hit, then coordinator answers via `ask` (WC-3), then command re-run | resolved by answer as flag | WC-3 does not exclude authorization gates; WC-9 says outward actions turn on only through a flag in the brief | GAP (F-01, blocking) |
| G4 contract path (WC-4) | spec:62 | Zero/Empty | command with no output flag and a fixed output dir (cleanup-audit, index-repo) | none | no row states a path (spec:85,86); WC-4 says a row does | GAP (F-02) |
| G4 | spec:62 | One/Minimal | `--output` names a file (tdd, init-lite) | `X.return-contract.yaml` | stated with an example | OK |
| G4 | spec:62 | Typical | `--output` names a directory | `<dir>/return-contract.yaml` | stated | OK |
| G4 | spec:62 | Legitimate Edge Case | "add a report path" rows where file-or-directory is not stated (spec:99,101,102,103,106-108,110,111,115,119,123) | undefined | WC-4 gives a rule only for directory brief, tdd/init-lite, adversarial, cli-eval, workflow | GAP (F-02) |
| G5 status mapping (WC-5) | spec:63 | Zero/Empty | no report file | `failed` | stated | OK |
| G5 | spec:63 | Typical | `succeeded` | `succeeded` | stated | OK |
| G5 | spec:63,263 | Legitimate Edge Case | `partial`, audit verdict FAIL | `succeeded` | stated, with the first sentence naming it | OK |
| G5 | spec:62,183,262 | Sentinel Value Match | an existing contract whose own `status` is not one of the four values | assertion in 7.2 step 4 fails | "keep their fields" vs fixed four values; no check of existing vocabularies | GAP (F-07) |
| G6 wait size (WC-10) | spec:68 | Typical | 4-minute waits vs 5-minute heartbeat | holds | stated | OK |
| G6 | spec:68,283 | Maximum/Overflow | one poll-script run longer than 4 min | unknown | UNVERIFIED #12 | GAP, already disclosed |
| G6 | spec:68 | Zero/Empty | `--poll-interval 0` | not covered | not stated | GAP (minor, N-4) |
| G7 nesting depth (WC-8, R1) | spec:33,66 | Typical | depth 1, worker starts worker | refused | `CAPS:97-101` | OK |
| G7 | spec:33,252 | Legitimate Edge Case | depth raised (D5) | WC-8 still forbids | stated | OK |
| G7 | spec:66 | Sentinel Value Match | `task-create` from a depth-1 worker | unknown | UNVERIFIED #5; WC-8 forbids either way | OK |
| G8 confidence gate (task row) | spec:121 | Typical | below 0.70 | blocked | stated | OK |
| G8 | spec:121 | Legitimate Edge Case | exactly 0.70 and the 0.70-0.89 band | not stated | the row says only "below 0.70" | GAP (minor, N-4) |
| G9 `--monitor` (pr-submit) | spec:114 | Legitimate Edge Case | `--monitor 1` | refused | stated; 0, 2, 3 not restated | OK |
| G10 additive-edit check (AC-C5) | spec:149,176 | Legitimate Edge Case | adding `--unattended` to a command's Usage line | removes the old Usage line from the diff | pass condition says "prints nothing" | GAP (F-04) |
| G11 repo grep (AC-C1) | spec:147,158,172 | Legitimate Edge Case | the contract file or the new Orca section in `HOW-WE-WORK.md` shows an `orca orchestration ...` example | grep prints a line | SA-2 allows one mention in the contract file; AC-C1 scans `src/superclaude/core` with no exemption | GAP (F-05) |
| G12 phase gate | spec:154,225 | Sequence | P2 command that D4 affects runs before D4 is answered | not stated | "Phases 0-3 can proceed"; D4 lists auggie-review and task, both P2 | GAP (F-08) |

Classes left out: Maximum/Overflow for G2, G3, G5, G8-G11 (a boolean or an enumeration has no capacity); One/Minimal for G1, G5-G12 (no distinct one-element case); Sentinel Value Match for G1, G2, G4, G6, G8-G12 (no reserved value is compared).

Pipeline Dimensional Analysis (FR-17): not triggered. The spec has no multi-stage data filter. Count check done by hand: 43 commands = 21 + 22 (`INV-A:3`, `INV-B:3`) = 10 ready (5+5) + 27 needing change (13+14, `INV-A:73`, `INV-B:289`) + 6 coordinator-only (3+3). Section 3 lists 10 and 27 rows; section 4 lists 6. Phase assignment: P1 9 needing-change plus ready commands, P2 11, P3 4, P4 3 = 27, consistent.

## === REQUIREMENTS ANALYSIS ===

### F-01 (CRITICAL by label, blocking by consequence): WC-3 lets a worker turn a blocked gate into an answered one, which contradicts WC-9 and D2/D4 and breaks a safety rule
- Experts: Whittaker (sequence attack), Nygard, Wiegers.
- Grading sentence: an implementer who follows the stated text as written builds a worker contract in which any gate that "would resolve as blocked" (spec:61) may be answered by the coordinator through `ask`, after which the command is re-run "with the answer as a flag" (spec:61), and that is wrong because two other stated texts forbid it: WC-9 says a default that pushes, opens a PR, posts or installs "turns on only through the command's own explicit flag written in the brief" (spec:67), and the implement Ruling rule says another agent's message is not acceptance (spec:233; `INV-A:66`, `INV-A:51`), which D2(a) wants kept (spec:234-236).
- Concrete attack (state trace):
  1. `/sc:implement <plan> --unattended` hits `E-NO-RULING`. The row resolves it as blocked (spec:109). State: contract `status: blocked`, Ruling absent.
  2. WC-3 (spec:61, a P0 deliverable, spec:158, "need no user decision", spec:154) says the session may `ask` the coordinator once and re-invoke with the answer as a flag. The coordinator is an agent; it answers "approve".
  3. The re-run records a Ruling from an agent message. State: Ruling present, no person involved. That is the case `refs/qa.md:238` excludes and D2(a) says to keep excluded.
  4. Same shape for outward actions: post-release, auggie-review `--post-pr`, task `commit`/`push` all resolve as blocked or off. WC-3 lets a flag such as `--post-pr` appear after dispatch, which is not "written in the brief" (WC-9) and is the question D4 leaves open (spec:244-247).
- Why blocking: a safety-boundary rule (a deliberate Ruling rule per spec:218, 235-236) and a stated outward-action restriction are both weakened by a text that is written into the P0 contract before the user answers D2 or D4.
- Recommendation: narrow WC-3 so `ask` covers only missing inputs (a suite, a target release, a path) and never a Ruling, an approval, or an outward-action authorization; say that authorization answers are accepted only under D2(b) or D4(a) with the user's instruction quoted. Prefer deleting words to adding a section.
- Priority: High. Quality impact: requirements consistency 4/10 to 8/10 on this point.

### F-02 (MAJOR label, Medium by consequence): WC-4's "known before dispatch" path is undefined for many commands
- Experts: Wiegers, Adzic.
- Evidence: WC-4 says "A row in section 3 states any other path" (spec:62). Rows for cleanup-audit and index-repo state no contract path (spec:85-86; both have a fixed output location, `INV-A:42,53`). Ten rows say "add a report path" or "add an output path" without saying file or directory (spec:99,101,102,103,106,108,110,111,119,123 and part of 107), and WC-4 gives the `.return-contract.yaml` rule only for tdd and init-lite. AC-1.2 and 7.2 step 3 require the report path to equal "the WC-4 contract path" (spec:182,196).
- Why Medium: the implementer must guess file versus directory; the text allows more than one reading and none is contradicted.
- Recommendation: add one sentence to WC-4 giving a default for a file-valued flag (as for tdd) and for a command with a fixed output directory (contract beside it), and name cleanup-audit and index-repo in their rows.
- Priority: Medium.

### F-03 (Medium): `--unattended` combined with a person-mode flag is undefined for some commands
- Experts: Whittaker (zero/empty and divergence), Cockburn.
- Evidence: rows for cleanup, improve, business-panel, explain, test, pr-submit, roadmap say the flag "is refused" under `--unattended` (spec:100-123). The rows for adversarial, brainstorm, release-split say only that the brief must never pass `--interactive` (spec:83,84,89). WC-2 says an unattended command "never calls AskUserQuestion" (spec:60).
- Why Medium: a coordinator that follows 2.3 never passes the flag; the failing case needs a mistaken brief.
- Recommendation: one sentence in WC-2: `--unattended` plus any person-mode flag stops with `status: blocked` or is refused, for every command.

### F-04 (Medium): AC-C5 and SA-4 cannot be met by adding flags to Usage lines
- Experts: Fowler, Adzic.
- Evidence: SA-4 says edits are additive, with named exceptions (spec:149). AC-C5 passes only if `grep -E '^-[^-]'` prints nothing (spec:176). Adding `--unattended` or `--output` to a command's `Usage` line removes that line from the diff. The spec itself treats the Usage line as editable text (load row, spec:112).
- Recommendation: either name "Usage line gains flags" as an allowed change in SA-4, or state that the new flags are documented only in the new section.

### F-05 (Medium): AC-C1 and SA-2 disagree on what the contract file may contain
- Experts: Fowler, Newman.
- Evidence: SA-2 allows one mention of Orca "as an example of a caller's question channel inside the contract file" (spec:147). P0 adds an Orca section to `HOW-WE-WORK.md` and writes `WORKER-CONTRACT.md` (spec:158). Both live under `src/superclaude/core`, which AC-C1 scans and which must print nothing for the pattern `orca(-ide)? (orchestration|worktree|terminal|agent)` (spec:172). The only exemption in AC-C1 is `skills/ccsession-tag/`. Also, AC-C1 is narrower than SA-2 ("none runs an `orca` or `orca-ide` command"): `orca status` or `orca open` would pass, and `plugins/superclaude/` is not scanned.
- Why Medium: whether the failing text appears depends on how P0 is written.
- Recommendation: add the two P0 files to the exemption list, or ban command-form examples in them; widen the pattern or narrow SA-2.

### F-06 (Medium): the tasklist and reflect rows rest on an unverified assumption and leave one human halt unmapped
- Experts: Nygard, Whittaker, Hohpe.
- Evidence: the tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" and needs no change (spec:122), citing `INV-A:14`, which is general Claude Code documentation. The inventory that owns the tasklist verdict says nested spawning is UNVERIFIED (`INV-B:210,314,322`) and asks for the per-phase reflect to run at the worker's top level (`INV-B:215`). The spec does not list this in its UNVERIFIED items (spec:271-285). The same inventory notes that Stage 10.5 `needs_human_decision` items HALT (`INV-B:209`); the row gives no resolution for that halt, though WC-2 requires each gate to be listed per command (spec:60). The reflect row makes `--remediate` "follow the existing headless auto-accept rule" (spec:88) without saying what is applied silently (`INV-B:109` says auto-accepts for auto-fixable registers and skips gates).
- Why Medium: the failure needs the nested spawn to be refused, which is unknown.
- Recommendation: add the nesting assumption and the `needs_human_decision` HALT to the tasklist row (resolve as blocked), and one UNVERIFIED line.

### F-07 (Medium): existing contract vocabularies are not checked against the fixed four statuses
- Experts: Wiegers, Hohpe.
- Evidence: WC-4 says commands with a contract "keep their fields and add the missing ones" (spec:62) and fixes `status` to four values (spec:62,262). 7.2 step 4 asserts membership in that set for every command (spec:183). No inventory line records the `status` values of the workflow, brainstorm, reflect or adversarial contracts (`INV-B:272`, `INV-A:39`, `INV-B:112`, `INV-A:35`).
- Recommendation: one line in P1 to check each existing contract's `status` values, or relax the assertion for those four until checked.

### F-08 (Medium): phase gating and WC-9 wording do not line up with D4
- Experts: Cockburn, Newman.
- Evidence: D4 says it affects auggie-review `--post-pr` and task `commit`/`push` (spec:244), both P2 (spec:100,121,160), while the spec says Phases 0-3 proceed without a user decision (spec:154,225). WC-9 also lists "calls a paid external run" among outward actions (spec:67) with no definition and no row mapping it (only cli-eval carries safety flags, spec:104). Reflect Tier 2 external models and spec-panel's MCP are not addressed.
- Recommendation: say P2 only turns defaults off and D4 governs only whether a brief may turn them on; define or delete "paid external run".

## === ARCHITECTURE ANALYSIS ===

Positive findings first, so the panel's pass-through is clear (not scored as findings):
- Fowler/Newman: the split (coordinator owns Tasks, command owns work, shared contract file read by installed path) is coherent, and the rejected alternative R1-R5 (spec:31-37) is argued from `CAPS:97-103,145-161` and the inventories, not asserted. No contradiction found with `README.md:6`.
- Nygard: failure modes are mostly covered (silent stall, readiness limit, retry, fenced consumer: WC-1, WC-2, WC-6, WC-12). The stall case (`INV-A:62`) is handled.
- Hohpe: the report-file pattern gives a single pull channel; WC-5 maps four statuses to Orca's two outcomes (`CAPS:73`).

Findings:
- F-01, F-05, F-06 above are architectural as well (WC-3 vs WC-9 layering; AC-C1 scope; nested-reflect assumption).
- N-1 (MINOR, Newman): the section 3 title says "10 ready today", yet every one of those 10 rows carries a change and a phase (spec:83-92), and the same section says all 10 get `## Unattended mode` (spec:76,159,160). The counts are right; the label "ready" means "runs with the right brief", which spec:79 says. Rename to "runs with a brief today".
- N-2 (MINOR, Fowler): 2.1 calls `--unattended` "the only command-side change the contract asks for besides report files and resume" (spec:51), but the rows also require a Write tool for explain, a frontmatter move for business-panel, a `--resume` flag for cli-portify, and drift fixes for roadmap and validate-roadmap (spec:102,105,108,118,124). Reword.
- N-3 (MINOR, Hohpe): brainstorm's brief rule lists `--output` and "never `--interactive`" but no `--handoff` limit (spec:84), while workflow has `--handoff none` (spec:92). `INV-A:39` records an optional Wave 4 handoff to tasklist or task-builder. Add the limit or say why not.
- N-4 (MINOR, Crispin): two edge cases noted in the table: exactly 0.70 confidence for the task row (spec:121), and `--poll-interval 0` for WC-10 (spec:68).
- N-5 (MINOR, Wiegers): item 14 of "UNVERIFIED items" (spec:285) is a provenance claim ("about 340 citations ... 9 defects fixed"), not an unverified item. It cannot be checked from the workspace. Move it to the citation conventions or mark it as reported, not verified.
- N-6 (MINOR): the E5 and section 1.2 `grep` results (spec:25) are quoted as run on 2026-11-02; unverifiable here.

## Synthesis

- Overall: the document is strong on evidence discipline (every claim cited, gaps stated at spec:41-45 and 271-285) and its decision is well argued. One blocking requirement conflict (F-01) and several Medium consistency gaps.
- Quality (0-10): Clarity 8, Completeness 7, Testability 7 (acceptance checks are concrete; F-04/F-05 make two of them unpassable as written), Consistency 6 (F-01).
- Consensus: Wiegers, Nygard and Whittaker agree on F-01; Fowler and Newman agree the architecture choice stands.
- Disagreement: none recorded; Crispin would grade F-02 higher because of the P1 acceptance checks; held at Medium because the text allows a reasonable reading.

## follow-up candidates (Medium and minor; none fails this review)

Medium: F-02, F-03, F-04, F-05, F-06, F-07, F-08.
Minor: N-1, N-2, N-3, N-4, N-5, N-6.
The question to the user about opening an issue for these (once per loop, per the command's Review Loop bullet 3) is not asked here: this run has no user channel. The coordinator's session should ask it. Nothing was created.

## Reviser brief

Blocking finding ids: F-01.

Rules for the reviser (restated from the command's Review Loop bullet 6; read this, not the command):
- Revise only text a blocking finding names. Here that is WC-3 (spec:61) and, only if needed to remove the contradiction, one cross-reference to WC-9 or D2.
- Add no rule, mechanism or section that a blocking finding does not call for. Each added paragraph or table cites its finding id (F-01).
- Prefer deleting or narrowing to adding. Leave Medium and minor findings alone, including through "apply all findings".
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Return the candidate once; do not award yourself a PASS.

verdict: FAIL
