review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `0962971bc5e9e3d54fa29ae20237450890eefb0d54ec5b262606d398c0bb57e2`
- baseline: not applicable (first review; no `--re-review`, no `--baseline` given)
- reviewer model: claude-sonnet-5-5
- scope label: whole-document audit, first review
- shared context read first: `.dev/orca-command-refactor/README.md:1-38`

## Coverage and verification limits
- Covered: all 285 lines of the spec (sections 1-9, Decisions, UNVERIFIED list), checked against `inventory/commands-a.md`, `inventory/commands-b.md` and `inventory/orca-capabilities.md` (cited `INV-A`, `INV-B`, `CAPS` as the spec does).
- Checked and found as cited: the 10/27/6 split and its phase assignment (P1 9 + P2 11 + P3 4 + P4 3 = 27 needing change, plus 10 ready, 6 coordinator-only = 43; `INV-A:73`, `INV-B:278`, spec lines 76, 159-162); `CAPS:73`, `CAPS:80` (own `failed` does not trip the breaker), `CAPS:97-103` (depth 1, call sites UNVERIFIED), `CAPS:129-130`, `CAPS:156`, `CAPS:186-188`.
- UNVERIFIED (not inside the workspace, cannot be read): every `src/superclaude/...` path:line, `CLAUDE.md:N`, `EVIDENCE.md:N`, `.dev/codegraph-migration/...`, `pyproject.toml:38`, `Makefile:68-74`, and the grep runs in E5. They were not graded as defects.
- Not covered: the Orca guide text itself (`[G]`, `[H:*]`), which is reachable only through the `CAPS` quotes.
- Focus areas applied: requirements (Wiegers, Adzic, Cockburn), architecture (Fowler, Newman, Hohpe, Nygard); Whittaker attacks applied to the guards in the table below. `--focus correctness` is not active, so no State Variable Registry. Pipeline Dimensional Analysis does not trigger: the spec describes no multi-stage data flow whose item count changes (the phases P0-P4 are a rollout order, spec lines 156-162).

## Findings table (ids used by the Reviser brief)
| id | severity (label) | grade | one line |
|---|---|---|---|
| B-1 | MAJOR | blocking | WC-4 gives no contract path for cleanup-audit and index-repo, yet P1 and AC-1.1/AC-1.2 require one |
| M-1 | MAJOR | Medium | AC-C1 forbids any Orca command text in `core/`, but SA-2 and SA-5 add Orca text there |
| M-2 | MAJOR | Medium | Fixed status set versus "existing contracts keep their fields" |
| M-3 | MAJOR | Medium | "Fresh dir" retry rule collides with a brief-fixed `--output` |
| M-4 | MAJOR | Medium | WC-11 "must never" versus cleanup-audit and index-repo fixed output paths |
| M-5 | MAJOR | Medium | `--post-pr` and other authorization flags are assumed, not evidenced |
| M-6 | MAJOR | Medium | tasklist row claims nesting is safe; inventory flagged it as nested fan-out to remove |
| M-7 | MAJOR | Medium | "Phases 1-3 need no user decision" versus open choices in P3 and the D-series |
| M-8 | MINOR | Medium | AC-2.2 expects `failed` on every gate, WC-3 lets the worker `ask` instead |
| M-9 | MINOR | Medium | WC-3, WC-6, WC-12 have no acceptance check |
| N-1 | MINOR | note | `--output` meaning (file or directory) unstated for the newly added flags |
| N-2 | MINOR | note | finding ids F-01, F-02, GF-01 are cited but never defined in the document |
| N-3 | MINOR | note | pr-submit top-level rule cited at two different lines |
| N-4 | MINOR | note | `master...HEAD` in AC-C5/AC-0.3 versus the fork's `origin/master` rule |

## === REQUIREMENTS ANALYSIS ===

### B-1 (blocking) WC-4 cannot produce a contract path for cleanup-audit and index-repo
- Expert: Wiegers (testability), Adzic (example), Cockburn (actor/goal).
- Grading sentence: An implementer who follows the stated text as written builds a cleanup-audit and an index-repo contract with no determinable path, and that is wrong because WC-4 requires the path to be "known before dispatch" and AC-1.2 requires "its report path is the WC-4 contract path".
- Stated texts that clash:
  - WC-4 (spec line 62) derives the path only from a directory flag (`--output` / `--output-dir`), a file `--output` (tdd, init-lite), adversarial, and the new `--output <dir>` of cli-eval and workflow; "A row in section 3 states any other path".
  - The cleanup-audit row (line 85) says the brief passes `--pass <N>` only, the output dir "is fixed", and the small fix is only to "Name the `--pass all` final report". The index-repo row (line 86) says the brief passes "none" and the fix is to "State the output location". Neither row states a contract path, and neither adds an output flag.
  - P1 (line 159) names both commands in the row that adds "the WC-4 contract in unattended mode" and the `## Unattended mode` section. AC-1.1 (line 195) tests that every command named in the P1 row except `load` has a section naming `return-contract.yaml`. AC-1.2 (line 196) runs the live check "with `--unattended` and its `--output` as WC-4 gives it", and 7.2 step 3 (line 182) requires the worker's report path to be the WC-4 contract path.
  - Neither command has an `--output` in the evidence: `INV-A:42` (cleanup-audit, fixed `.claude-audit/`), `INV-A:53` (index-repo, `PROJECT_INDEX.md`, location "implied, UNVERIFIED", `INV-A:117`).
- Concrete wrong outcome: AC-1.2 step 3 cannot be evaluated for these two commands, so P1 cannot pass as written (and AC-C3-style gating, "Later phases do not start until the earlier phase's checks pass", line 154, blocks P2).
- Recommendation (delete or narrow, no new mechanism): state in the two 3.1 rows the contract path (for example beside the fixed output), or remove cleanup-audit and index-repo from the P1 contract scope and from AC-1.1/AC-1.2. Priority: High. Quality impact: Testability 5 to 8.

## === ARCHITECTURE ANALYSIS ===
(Architecture decision itself, section 1: sound given its stated evidence gaps in 1.4; the stated gaps are honest and Phase 0 tests the decision first, lines 43-45, 158. No blocking architectural finding.)

## Medium findings (warnings; listed under follow-up candidates)

### M-1 AC-C1 versus SA-2 and SA-5
- Expert: Fowler. SA-2 (line 147) allows an Orca mention "as an example of a caller's question channel inside the contract file"; SA-5 (line 150) adds an Orca section to the routing guide; P0 (line 158) adds a coordinator brief template to the contract file. AC-C1 (line 172) greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` and demands no output, excluding only `ccsession-tag`. If the example or the Orca section writes a literal command, the common check fails every phase. Medium because it needs a guess that the text uses the lowercase command form (the spec writes the placeholder `ORCA`, line 167, which the case-sensitive grep would not match).
- Fix: exempt `core/WORKER-CONTRACT.md` and the Orca section of `core/HOW-WE-WORK.md` in AC-C1, or state the placeholder form is required.

### M-2 Status vocabulary versus existing contracts
- Expert: Wiegers. WC-4 (line 62) fixes `status` to `succeeded|partial|failed|blocked` and AC step 4 (line 183) asserts it, but also says commands with a contract "keep their fields and add the missing ones". The existing contracts' status values are not stated: the workflow contract is described only as having `status` incl. `failed` (`INV-B:272`), reflect, brainstorm and adversarial contracts are not quoted. If any uses another vocabulary, "keep" and "assert one of four" contradict. Evidence for the existing values is UNVERIFIED (`sk/.../return-contract.md` is outside the workspace). Medium: needs a guess about those files.

### M-3 Fresh-directory retry versus a brief-fixed `--output`
- Expert: Nygard. WC-6 (line 64) says a retry "must not corrupt the first attempt's output" and that a command without resume writes "each run into a fresh output directory"; most 3.2 rows say "fresh dir". But WC-4 and section 2.3 (lines 62, 73) make the coordinator pass one `--output` before dispatch, so a `--retry-of` worker given the same brief writes the same directory and the same contract path. The spec never says the coordinator must pass a new `--output` on retry, or that the command derives a sub-directory. Medium: the implementer picks one of two readings.

### M-4 WC-11 "must never" versus fixed output paths
- Expert: Whittaker (sequence/accumulation attack). Attack: dispatch two cleanup-audit workers in one worktree. WC-11 (line 69) says two workers "must never write the same file" and that default output paths carry a timestamp or slug. The cleanup-audit row (line 85) keeps the fixed `.claude-audit/` dir and cites WC-11 as the reason for "one audit per worktree at a time", which is a coordinator restriction, not a command property; section 2.3 (line 73) does not list that restriction in the brief. index-repo writes one fixed `PROJECT_INDEX.md` (`INV-A:53`) with no such note. State the restriction in 2.3 or relax WC-11 for these two.

### M-5 Authorization flags assumed to exist
- Expert: Nygard, Hohpe. WC-9 (line 67) says outward actions turn on "only through the command's own explicit flag". The auggie-review row (line 100) says posting returns "only with an explicit `--post-pr`", but the evidence shows only the negative flag: `--no-post-pr` (`INV-A:38`, "Off with `--no-post-pr` (C:52)"); a positive `--post-pr` is not shown. Likewise task `commit`/`push` (line 121, D4 line 244) and post-release (AC-4.2, line 209, "no authorization flags") name flags nobody evidenced. If the flag does not exist, D4 option (a) has no mechanism. UNVERIFIED (command files outside the workspace).

### M-6 tasklist nesting claim
- Expert: Fowler. The tasklist row (line 122) says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`" and passes `--unattended` to each reflect. But `INV-B:46` records Stage 10.5 running reflect "inside subagents" (UNVERIFIED), and `INV-B:295` lists it under "Remove a nested fan-out or remediation offer that runs inside subagents". Each such reflect itself spawns agents (`INV-B:36`, 2-3 reviewers plus validators), and under the headless auto-accept rule it may remediate (line 88). The spec drops the inventory's removal recommendation without evidence for the depth count. `INV-A:14` says only "up to three layers"; the layer count for tasklist to reflect to its agents is not shown.

### M-7 "No user decision" in Phases 1-3
- Expert: Cockburn. Line 154 says "Phases 1-3 need no user decision"; line 225 says "Phases 0-3 can proceed on the recommendations". They differ, and P3 contains an unmade choice: roadmap and validate-roadmap are to be "reconciled" (lines 118, 124) without saying which side (command or skill) wins, while the inventory states no file says which wins (`INV-B:309`). AC-3.1 (line 204) passes under either choice, so a wrong pick is not caught. D1 also precedes P0-P3 (line 227).

### M-8 AC-2.2 versus WC-3
- Expert: Adzic. AC-2.2 (line 200) expects, for a gate-trigger input, `worker_done --outcome failed` and a blocked contract. WC-3 (line 61) lets a worker holding a preamble "ask the coordinator once" instead, which a conformant worker may do. The result then depends on the worker's choice, and 7.2 step 3 (line 182) waits on `question` messages but passes only on exactly one `worker_done`. Say that the AC brief tells the worker not to `ask`, or accept the question path.

### M-9 Requirements without acceptance checks
- Expert: Crispin. WC-3 (ask path, resume by message ID), WC-6 (retry safety, `--retry-of`) and WC-12 (`consumer_fenced`) have no check in section 7. Only WC-7 (step 5, line 184) and WC-10 (AC-4.3 for pr-submit only) are exercised. A retry check would also expose M-3.

## Notes (minor)
- N-1: for the added flags "add `--output`" (analyze, spec-panel) and "add a report path / output path" (build, design, explain, index, test, cleanup, improve; lines 99-123), the spec never says whether the value is a directory or a file, while WC-4 handles file-valued `--output` only for tdd and init-lite (line 62). AC-1.2 (line 196) reads all P1 flags as directories except init-lite. The sandbox copy of the `/sc:spec-panel` definition (`command.md`, outside the evidence set, so not graded) already uses `--report-dir` with `<report-dir>/return-contract.yaml` and a file-valued `--output`, which differs from the spec's spec-panel row (line 120) and WC-4 vocabulary; whether that is newer or divergent is UNVERIFIED.
- N-2: "F-01", "F-02", "GF-01" (lines 76, 83-92, 159, 162, 194) are review-finding ids with no definition in the spec; a reader of the final document cannot resolve them.
- N-3: the pr-submit top-level rule is cited as `SKILL.md:37-39` in the spec (lines 11, 65) and `INV-B:34`, but `CAPS:161` quotes it from `SKILL.md:47-49`. One is wrong; UNVERIFIED which.
- N-4: AC-C5 and AC-0.3 (lines 176, 193) diff against `master...HEAD`; the repo rule is to rebase on `origin/master` first (project CLAUDE.md pre-PR check 2, UNVERIFIED here), so the base ref may be stale.

## Guard Condition Boundary Table
Guards found in the spec: G1 outcome mapping (WC-5, line 63); G2 wait-size guard (WC-10, line 68); G3 unattended switch (WC-2 / D1, lines 60, 228); G4 contract path derivation (WC-4, line 62). Classes left out: Maximum/Overflow for G1, G3 and G4 (no numeric capacity is stated); Sentinel for G2 (no sentinel); Typical rows for G1 and G3 are omitted because the happy path is specified in prose at lines 63 and 60.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 outcome mapping | WC-5, line 63 | Zero/Empty | no report file | true ("no report exists") | `--outcome failed` | OK |
| G1 outcome mapping | WC-5, line 63 | One/Minimal | report exists but `status` missing or not in the four values | unspecified | not stated; AC step 4 (line 183) would fail the check, but the worker's `--outcome` is not defined | GAP (Medium) |
| G1 outcome mapping | WC-5, line 63 | Legitimate Edge Case | `partial` or audit verdict FAIL | `succeeded` branch | `--outcome succeeded`, body says status | OK |
| G2 wait size | WC-10, line 68 | Typical | single tool call 3 min | under 4 min | allowed | OK |
| G2 wait size | WC-10, line 68 | Legitimate Edge Case | one poll-script run alone exceeds 4 min | split impossible | `INV`/spec item 12 (line 283) lists it UNVERIFIED; no fallback behavior stated | GAP (Medium) |
| G2 wait size | WC-10, line 68 | Maximum/Overflow | eval timeout 3600 s (line 68, `INV-A:65`) | exceeds 4 min | split into waits of at most 4 minutes | OK |
| G3 unattended switch | WC-2 / D1, lines 60, 228 | Zero/Empty | flag absent | false | today's behavior (SA-1, line 146) | OK |
| G3 unattended switch | WC-2 / D1, lines 60, 228 | Sentinel Value Match | the text `--unattended` inside quoted specification content or a topic string | unspecified | not stated whether it must be a standalone token | GAP (Medium) |
| G4 contract path | WC-4, line 62 | Zero/Empty | command has no output flag (cleanup-audit, index-repo) | no rule applies | none | GAP (blocking, see B-1) |
| G4 contract path | WC-4, line 62 | One/Minimal | file `--output` with no extension (`--output .dev/tdd/auth`) | extension replace undefined | not stated | GAP (Medium) |
| G4 contract path | WC-4, line 62 | Legitimate Edge Case | two file outputs sharing a stem (`a.md`, `a.txt`) | same contract path | not stated; collides (see WC-11) | GAP (Medium) |

FR-8/FR-9 grading applied: only the G4 Zero/Empty row names a concrete wrong outcome (B-1); the other GAP rows need an assumption about the implementer and are Medium (follow-up candidates).

## Expert consensus
- Agreement: the decision (Orca on top, commands as workers, section 1) is supported by the cited inventories and its weak points are stated (lines 41-45).
- Disagreement: none recorded between experts.
- Quality scores (0-10): Clarity 8, Completeness 7, Testability 6 (B-1, M-8, M-9), Consistency 7 (M-1, M-2, M-7).

## Follow-up candidates
Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, and the Medium GAP rows G1 (invalid status), G2 (poll longer than 4 min), G3 (quoted `--unattended`), G4 (no extension, shared stem).
Minor: N-1, N-2, N-3, N-4.
Whether to open an issue for these: to be asked of the user once by the session that ran this loop (not an `--unattended` run); none was created.

## Brief clauses overridden
None. The brief asked for a first review of the whole document and did not widen or regrade any finding.

## Reviser brief
Repair only the blocking findings B-1 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
