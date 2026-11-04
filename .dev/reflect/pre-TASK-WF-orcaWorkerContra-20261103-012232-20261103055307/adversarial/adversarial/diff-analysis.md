# Diff Analysis: reviewer-card Comparison

## Metadata
- Generated: 2026-11-03T06:14:04Z
- Variants compared: 3
  - Variant A = `variant-1-original.md` (reviewer 1, analyzer, verdict PASS)
  - Variant B = `variant-2-original.md` (reviewer 2, qa, verdict PASS)
  - Variant C = `variant-3-original.md` (reviewer 3, refactorer, verdict FAIL, 1 blocking)
- Focus areas: correctness, coverage, deviation-classification
- Total differences found: 33 (30 structural, content, contradiction and unique items, plus 3 promoted shared assumptions)
- Categories: structural (9), content (5), contradictions (4), unique (12), shared assumptions (11 classified; 3 UNSTATED promoted)

Citation key:
- `A:N`, `B:N`, `C:N`: line N of the variant card in this directory.
- `TL:N`: line N of `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md` (the plan).
- `SRC:N`: line N of `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md` (the spec).
- `qa.md:N`: `~/.claude/skills/sc-implement-protocol/refs/qa.md`. `SKILL.md:N` (implement): `~/.claude/skills/sc-implement-protocol/SKILL.md`.
- `H<n>`: hunk in `../../artifacts/grounding-hunks.md`.
- Every line cited below was opened during this analysis.

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Verdict and blocking count | PASS, 0 blocking (A:4; "I found no blocking defect", A:112) | PASS, 0 blocking (B:4; "no blocking finding exists", B:80) | FAIL, 1 blocking: R3-F1 (C:4, C:8, C:208-211) | High |
| S-002 | Number of findings | 5 (R1-F1 to R1-F5) | 3 (R2-1 to R2-3) | 11 (R3-F1 to R3-F11) | Medium |
| S-003 | Severity spread | 4 should-fix, 1 minor (A:8, 27, 48, 68, 87) | 1 should-fix, 2 minor (B:8, 25, 44) | 1 blocking, 5 should-fix, 5 minor (C:8, 30, 49, 72, 92, 113, 129, 144, 157, 171, 186) | Medium |
| S-004 | Deviation-class spread | drift 2, none 3 (A:9, 28, 49, 69, 88) | drift 1, none 2 (B:9, 26, 45) | drift 4, none 7 (C:9, 31, 50, 73, 93, 114, 130, 145, 158, 172, 187) | Low |
| S-005 | Extra blocks beyond findings and self-audit | none | `matrix_omissions` block with 2 spec spans (B:58-64) | none | Low |
| S-006 | Executor rules cited as finding evidence | Only in self-audit (A:107); no finding lists qa.md | Only in self-audit (B:67-68); no finding lists qa.md | Finding evidence cites qa.md:52, qa.md:61 (C:23-24) and qa.md:310 (C:65) to derive severity | Medium |
| S-007 | How a Constraints-level defect is filed | Not applicable (no Constraints finding) | Under `tasks: [0]` for the Constraints block (B:10) | Under the task that collides with the constraint, `tasks: [4]` and `tasks: [2]` (C:10, C:32) | Low |
| S-008 | Task coverage by findings | Tasks 1, 2, 3, 4, 5, 6, 8 (A:10, 29, 50, 70, 89) | Constraints, Task 3, Task 8 (B:10, 27, 46) | Tasks 1, 2, 3, 4, 5, 6, 8 (C:10, 32, 51, 74, 94, 115, 131, 145, 159, 173, 188) | Medium |
| S-009 | Blind calibration result | self 0.70, calibrated 0.86, all 5 severities hold (A:121-124) | self 0.82, calibrated 0.82, all 3 hold (B:89-92) | self 0.6, calibrated 0.88, all 11 hold (C:217-220) | Low |

Notes on structure:
- No card has a finding on Task 7 (S-008). Task 7's environment risk (`/opt/Orca` and the profile file) appears only in A's self-audit (A:110-112) and in the B and C calibrator notes (B:99, C:229).
- C's low self-confidence (0.6) is about R3-F1's severity, not card quality; its calibrator says so (C:230).

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|---|-------|-------------------|-------------------|-------------------|----------|
| C-001 | Task 6: each allowlist entry must carry "the phase that converts its command" (TL:125), but many hits have no converting phase | R1-F3, should-fix, drift (A:47-66). Cause: pr-submit and git are never workers (SRC:61); the pr-submit row applies only under D3 (b) (SRC:174), and SRC:201 says no Phase 4 change. Fix: a closed reason format with "never a worker" and "no command converts it" slots (A:65-66) | Omitted | R3-F5, should-fix, drift (C:91-110). Same cause, plus read-only `gh pr view/list/checks` among the 40 `gh pr` hits (H9 line 102) and line-number keys that break on later edits. Fix: key by path, verb and stripped line; closed category set (C:108-110) | Medium |
| C-002 | Task 3: the evidence that decides the plugin copy of WORKER-CONTRACT.md (TL:69) | R1-F5, minor, none (A:87-104). `scripts/build_superclaude_plugin.py:75` copies only agents, commands, hooks, scripts and skills, so core is not distributed; name that line and the parity tests (verified: build script line 75; `tests/commands/test_routing_plugin_parity.py:3-4` says "Plugin installs never receive core/ files") | R2-3, minor, none (B:42-57). Grounding hunk H4 for that script is empty (grounding-hunks.md:43-45), so the convention evidence was never gathered; tell the executor to read the whole file | Omitted as a finding. C's R3-F4 covers a different Task 3 problem (keeping an added copy in sync); see U-008 | Low |
| C-003 | Task 5 must assert a phrase "quoted from ./source.md" for each rule (TL:104), but the contract wording it tests is not pinned to the spec | R1-F1, should-fix, drift (A:7-25). Concrete case: TL:112 says the fan-in cap "at most 10" is "as written in section 2.3", and TL:56 repeats it. Verified: "at most 10" occurs only at TL:56 and TL:112; SRC:122 says "maximum of 10 inputs" and "never exceeds 10" | Omitted | R3-F3, should-fix, drift (C:48-70). General case: Tasks 1 and 2 require verbatim text only for the reason texts, the WC-4 error and the guard line (TL:45, TL:61), so Task 5 may have no phrase to pin; the only fix is editing a file Task 5 does not own, which can break Task 3's `cmp` (TL:74) and draw a managed FINAL `issues` for "a later change contradicts it" (qa.md:310) | Medium |
| C-004 | No `make verify-sync` baseline before the plan's first edit | Self-audit only, no finding: "I could not verify that `make verify-sync` is clean today, and no baseline is recorded for it" (A:117-118) | Omitted | R3-F11, minor, none (C:185-200). Task 1 records no verify-sync baseline (TL:33-35), so an existing drift would surface as an AC-C2 failure in Task 4 (TL:96); the wider baseline also leaves out `tests/docs` and `tests/unit`, which scan every .md under src (verified: `tests/docs/test_retired_docs_absent.py:40` scans `src/superclaude`, `plugins/superclaude`, `docs`) | Low |
| C-005 | Routing-guide tests constrain the new Orca section in Task 4 (TL:82-90) | Self-audit only, judged not a finding: "the ASCII rule and the marker/heading rules constrain the new Orca section, but Task 4's own test run will surface them" (A:110-111) | Omitted | R3-F6, should-fix, none (C:111-127). Non-ASCII fails `test_guide_is_ascii_except_the_ruling_example` (verified at `tests/core/test_how_we_work_routing_table.py:341`); some tests slice between fixed headings (verified: `"### 3.14 "` to `"## 4. "` is at line 1091, not at the cited line 290, which holds the marker-order assertion; C's calibrator says the same, C:227) | Low |

Matching notes:
- C-003 pairs a specific instance (A) with the general mechanism (C). Only A names the concrete off-spec phrase; only C names the ownership and FINAL consequence.
- The three Task 8 findings (R1-F2, R2-2, R3-F10) name three different problems in the same task, so they are not matched; they appear as U-002, U-004 and U-012.

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|-------------------|-------------------|-------------------|-------------------|--------|
| X-001 | Verdict: can the plan run to completion without a halt? | PASS. "I found no blocking defect" (A:112). Raises no Constraints-versus-task conflict | PASS. "no task instruction breaches the plan's own Constraints" and the halt paths "are not reachable from any defect I could locate" (B:81-85) | FAIL. R3-F1 is "a literal conflict between a Constraints sentence and a direct instruction in Task 4", and "no repair can resolve the conflict, so it can halt the run" (C:208-211) | High |
| X-002 | Is R3-F1 blocking? TL:21 "P0 edits no command, skill or agent file" versus Task 4 writing `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (TL:90) | Silent; implicit no (PASS) | Explicit no, by B's general claim at B:81-82 | Yes, blocking (C:7-28) | High |
| X-003 | Does Task 2 breach TL:22 ("restates only what ./source.md sections 2.1, 2.2 and 2.3 say") by adding section 3.1 flags and the section 6 "from P1" marker (TL:58)? | Silent | No breach (B:81-82) | Yes, but should-fix, not blocking, because spec 2.1 says "including its brief template" (C:29-47, C:212-213) | Medium |
| X-004 | Does a plugin core copy of WORKER-CONTRACT.md have any value (Task 3, TL:69)? | No distribution value: the build script never copies core (A:91-96) | Undecided: the evidence was never gathered, either outcome passes (B:47-53) | Treats an added copy as a live option that then needs a byte-identity test (C:75-90) | Low |

### X-001 and X-002: what the text supports

The text supports Variant C on the existence of the conflict, and supports a conditional blocking rating. A and B's PASS rests on a lenient reading that neither card states.

Evidence for C:
1. The constraint is literal and byte-present. TL:21: "P0 edits no command, skill or agent file (`./source.md` section 6, P0 row: \"no command edits\")."
2. The write is mandatory, not optional. TL:90: "Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`." Task 4's AC requires `cmp` to exit 0 (TL:93). The spec requires the same copy (SRC:220 "its two mirrored copies"; SRC:299 AC-0.2 `cmp`; SRC:212 SA-5).
3. The target is a file inside a skill package. The repo's own test says so: "the guide ships inside the plugin's sc-recommend skill as refs/HOW-WE-WORK.md" (`tests/commands/test_routing_plugin_parity.py:3-4`). The directory also holds the skill's `SKILL.md` (verified by Glob: `plugins/superclaude/skills/sc-recommend/SKILL.md`).
4. The plan widened the spec's wording. The spec's P0 row says only "(no command edits)" (SRC:220). The plan added "skill or agent".
5. The executor's severity rule is mechanical once a reviewer answers yes. B4 fires when "the diff violates a parent `## Constraints` ... item or an explicit task instruction ... and the reviewer can quote that text" (qa.md:52). Its read-back is only that "the quoted text is byte-present in the plan Constraints or a task instruction" (qa.md:61). The reviewer's label is never read (qa.md:79).
6. No repair satisfies both. Dropping the copy fails TL:93; keeping it keeps the breach. A failed repair ends in `E-HALT-QA` `ladder-end` (qa.md:280) or a `dispute` halt (qa.md:281).
7. A second gate C did not cite: even if the Task 4 reviewer is lenient, the managed FINAL reads the plan's `## Constraints` and returns `issues` when "a plan `## Constraints` item is violated" (qa.md:310), which blocks archiving as `E-ARCHIVE-BLOCKED` (qa.md:286).

Evidence for A and B (lenient reading):
1. TL:24 names the plugin copy as allowed for Orca text: "Only `WORKER-CONTRACT.md` and `HOW-WE-WORK.md`, and their plugin copies, may describe the coordinator side." A reviewer can read TL:21 through this line and through its own citation "no command edits".
2. C's calibrator says the same: blocking "is conditional on a reviewer reading the constraint literally; constraint line 24 already names 'their plugin copies'" (C:223).

Finding on X-002: the conflict is real and cannot be repaired inside the plan (TL:21 against TL:90 and TL:93). Whether it halts depends on one reviewer's yes answer, and two independent gates can give it (the Task 4 review and the managed FINAL). B's statement "no task instruction breaches the plan's own Constraints" (B:81-82) is contradicted by the literal text of TL:21 and TL:90. Recommended reading for the debate: treat R3-F1 as must-fix before execution. The fix is one reworded constraint (C:26-28), which also restores the spec's own wording at SRC:220.

### X-003: what the text supports

TL:22 limits the contract to sections 2.1 to 2.3. Task 2 adds section 3.1 flags and a section 6 marker (TL:58). But SRC:59 says the file holds "the coordinator's rules (WC-6 and section 2.3, including its brief template ...)", and SRC:84 (section 2.3) says the brief carries "every flag section 3 lists as required". SRC:220 adds "plus a coordinator brief template listing the section 3.1 flags". Section 2.3 therefore brings in the section 3 flags by reference, so the conflict is weaker than in X-002. C's should-fix rating is supported. B's flat "no breach" (B:81-82) holds only under this by-reference reading, which B does not state.

### X-004: what the text supports

The evidence is mixed. A is right that the build script never copies core (`scripts/build_superclaude_plugin.py:75`), and the parity test says plugin installs never receive core files (`tests/commands/test_routing_plugin_parity.py:3`). But `plugins/superclaude/core/` already holds six core `.md` files (Glob; H5), and `tests/commands/test_impact_command.py:308-309` pins the plugin core copy of CODEGRAPH.md. So the precedent C relies on exists. The conflict does not change any severity; all three ratings are minor or should-fix.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | R1-F4 (should-fix, none; A:67-85). WORKER-CONTRACT.md is an installed core file, but the plan never says to drop the spec's evidence citations, such as `src/superclaude/cli/install_core.py:36` and `CAPS:` ids (SRC:59; `cmd/` and `sk/` paths at SRC:72). The repo forbids `src/superclaude/...` references in installed primitives, `core` included (`CLAUDE.md:72`, `CLAUDE.md:87`). The plan's Constraints (TL:17-27) do not carry that rule, and the managed FINAL reads only the plan plus its Constraints (qa.md:310). | High: a repo ABSOLUTE RULE no other card checks; a literal restatement would ship broken paths to other projects |
| U-002 | A | R1-F2 (should-fix, none; A:26-46). Task 8's AC needs a PASS or FAIL line "with an evidence file" for each of 11 checks (TL:157), but no task saves an evidence file for AC-0.1 (TL:47, TL:72) or for AC-0.2 and AC-0.3 (TL:93-94); Task 8 re-runs only AC-C1 to AC-C6 (TL:147-152). An unmet AC is the B1 blocking trigger (qa.md:49). | Medium: a plausible QA halt route that the executor will usually avoid by saving files |
| U-003 | B | R2-1 (should-fix, drift; B:7-23). TL:19 says "AC-0.8 is a P1 check (section 7.3)". Verified: AC-0.8 appears only at TL:19; SRC:304 (AC-0.7) is followed by SRC:305 (AC-0.9), and the P1 rows start at AC-1.1 (SRC:306). | Low: a false scope statement that no task acts on |
| U-004 | B | R2-2 (minor, none; B:24-41). No plan or spec line makes the P0 live plan carry the static report and the AC-0.7 and AC-C6 artifacts into the phase report (TL:154; SRC:238 puts the phase report in the live plan; SRC:303-304 require results "in the phase report"). The Tier 1 card raised the same point (t1-card.md:10). | Medium: a cross-plan handoff gap that could let P0 pass on incomplete evidence |
| U-005 | B | `matrix_omissions` (B:58-64): no coverage-matrix row anchors SRC:236 (the 39-command closing count) or SRC:188 (section 4's never-as-worker rationale). | Low: matrix bookkeeping; B says it is harmless for this plan |
| U-006 | C | R3-F1 (blocking, drift; C:7-28). TL:21 forbids skill-file edits; Task 4 must write a file inside the sc-recommend skill package (TL:90, TL:93). See X-001 and X-002. | High: the only blocking finding; text-supported and cheap to fix |
| U-007 | C | R3-F2 (should-fix, drift; C:29-47). TL:22 limits the contract to sections 2.1 to 2.3, while Task 2 adds section 3.1 flags and a section 6 marker (TL:58). See X-003. | Medium: same mechanism as U-006 but defensible through SRC:59 and SRC:84 |
| U-008 | C | R3-F4 (should-fix, none; C:71-90). If Task 3 adds `plugins/superclaude/core/WORKER-CONTRACT.md`, nothing keeps it in sync: `make verify-sync` covers Skills, Agents, Commands, Hooks and Templates (verified at `Makefile:170, 202, 228, 254, 280`), not core. Suggests the existing pattern `tests/commands/test_workflow_command.py:93` (`test_plugin_mirror_matches_src`, verified). | Medium: conditional on Task 3 adding the copy |
| U-009 | C | R3-F7 (minor, none; C:128-141). Task 5 hard-codes "no command has an `## Unattended mode` section" (TL:115); AC-1.1 later needs a per-phase positive list (SRC:306). Suggests a cumulative phase map. | Low: maintainability for P1 onward |
| U-010 | C | R3-F8 (minor, none; C:142-155). The brief template copies section 3.1 flags for 12 commands (TL:58), but no test checks them against the command files; the routing guide has such a check for its notes flags (verified: `tests/core/test_how_we_work_routing_table.py:258`). | Low: drift risk once P1 changes flags |
| U-011 | C | R3-F9 (minor, none; C:156-169). The Goal says the routing guide gets an Orca section "in every copy the repo keeps" (TL:15), while Task 4 leaves the CLAUDE.md level-table copy unchanged (TL:90). | Low: wording mismatch inside the plan |
| U-012 | C | R3-F10 (minor, none; C:170-184). Task 8 runs `git add .dev/tasks` (TL:154) before the executor's last ledger lines and the archive move, so staged paths go stale; the next steps omit re-staging, which SRC:90 gives the coordinator ("stages explicit paths plus `.dev/tasks` at every commit and again at the end of the run"). | Low: TL:19 already gives AC-C4 to the coordinator at commit time, which partly covers it |

## Shared Assumptions

All agreement points, classified:

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | All three accept the static/live split | Deferring AC-0.4, AC-0.5, AC-0.6 and the phase report to a live plan is authorized (SRC:238) | STATED (A:114, B:18 and B:79, C:214) | No |
| A-002 | No card finds an ordering defect | The executor runs tasks in source order and ignores Depends-on (SKILL.md:79) | STATED (B:73-74, C:204-205) | No |
| A-003 | No card faults Task 1's core-file pairing | Adding the file and its `KNOWN_CORE_FILES` entry in one task keeps the set-equality test green | STATED (A:115; A's calibrator confirms `test_how_we_work_install.py:43-44`, A:134) | No |
| A-004 | No card faults Task 7 | `/opt/Orca/resources/app.asar.unpacked/out/` and the Orca profile files exist, so Task 7's ACs (TL:140-141) can pass | STATED (A:110-112 says it checked both); B and C do not state it, and their calibrators flag it (B:99, C:229) | No |
| A-005 | C-004 (A and C) | `make verify-sync` may already drift; no baseline exists | STATED (A:117-118, C:190) | No |
| A-006 | All three accept the plugin copy of HOW-WE-WORK.md as required | The Task 4 copy is spec-mandated (SRC:220, SRC:299) | STATED (C:21-22 cites SRC:220; A:113 lists AC-0.2 as mapped) | No |
| A-007 | All cards reason about per-task QA on the plan text | The Task reviewer reads the plan's Constraints and can quote them (qa.md:52) | STATED (C:14-15; A:107 and B:68 read qa.md:40-70) | No |
| A-008 | All three accept AC-C1 as handled by Task 4 and Task 8 | AC-C1 tolerates either Task 3 outcome because it excludes the plugin core copy by name (SRC:252) | STATED (B:51-52) | No |
| A-009 | All three accept Task 3's AC-0.1 install command (TL:72) | `install_core_files` takes `target_path` and returns `(ok, msg)` | UNSTATED (no card checks it; C's calibrator notes the gap, C:229) | Yes |
| A-010 | All three accept AC-0.3's merge-base check (TL:94) | `src/superclaude/core/HOW-WE-WORK.md` has no deletions against the merge base before Task 4 starts | UNSTATED (no card checks it; A's calibrator raises it, A:135) | Yes |
| A-011 | All three accept AC-C1 as a pass condition for Task 4 (TL:96) and Task 8 (TL:148) | The AC-C1 scan prints nothing before the plan starts, so only this plan's edits can make it fail | UNSTATED (no card states or checks it) | Yes |

Promoted [SHARED-ASSUMPTION] points:

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-009 | [SHARED-ASSUMPTION] `install_core_files(target_path=d)` exists and returns a pair, as TL:72 uses it | All three accept Task 3's AC-0.1 command | Low | Holds today: `src/superclaude/cli/install_core.py:30-32` reads `def install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]` |
| A-010 | [SHARED-ASSUMPTION] AC-0.3 starts from a clean merge-base diff for HOW-WE-WORK.md | All three accept TL:94 | Low | Holds today: `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md` printed nothing (merge base `c118b5a5`) |
| A-011 | [SHARED-ASSUMPTION] The AC-C1 scan is clean before the plan | All three accept AC-C1 in Tasks 4 and 8 | Low | Holds today: the SRC:246-253 pipeline, run read-only on the current tree, printed nothing |

No CONTRADICTED assumption was found. A-004 is the one stated by a single card only; it carries the risk the B and C calibrators named (B:99, C:229).

## Summary
- Total structural differences: 9
- Total content differences: 5
- Total contradictions: 4
- Total unique contributions: 12
- Total shared assumptions surfaced: 11 (UNSTATED: 3, STATED: 8, CONTRADICTED: 0)
- Highest-severity items: S-001, X-001, X-002, U-001, U-006
- Key result for the debate: the verdict split (X-001) turns on R3-F1. The plan text supports C that TL:21 and TL:90/TL:93 conflict and that no repair can satisfy both. Blocking needs one reviewer's literal reading, and two gates can give it (Task 4 QA via qa.md:52/61, and the managed FINAL via qa.md:310). A and B's PASS depends on the lenient reading through TL:24, which neither card states.
