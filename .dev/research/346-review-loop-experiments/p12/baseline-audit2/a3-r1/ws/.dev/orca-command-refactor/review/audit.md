review: 1 of 3

# /sc:spec-panel audit: Orca worker-contract spec (first review, whole document)

```yaml
specification_review:
  command: "/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture"
  kind: "labelled whole-document audit of the final spec; first review (no --re-review, no --baseline given)"
  candidate: ".dev/orca-command-refactor/specs/orca-worker-contract-spec.md (285 lines)"
  candidate_sha256: "d1f34e4bb75f645e00e9b421dc8abdf0366d981ef45c7dfcc8f6689db8833a6a"
  baseline: "none (first review)"
  prior_report: "none"
  reviewer_model: "claude-sonnet-5-5 (Sonnet 5.5)"
  review_date: "2026-11-10"
  focus_areas: [requirements, architecture]
  expert_panel: "Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower (fixed review order of the command)"
  prompt_followed: "FIRST-REVIEW prompt of ~/.claude/rules/prompts/document_review_loop_prompts.md (read in full before reviewing)"
  input_type: "implementation spec; not a TDD (9 numbered headings, no TDD frontmatter) and not a PRD (no PRD headings): no TDD/PRD adjustments apply"
  improve_step: "not run: the brief assigns only this report file and --improve was not passed; the candidate was not modified"
```

## Coverage (what was and was not checked)

- Read in full: the candidate, `.dev/orca-command-refactor/README.md`, `inventory/commands-a.md` (INV-A, 120 lines), `inventory/commands-b.md` (INV-B, 323 lines), `inventory/orca-capabilities.md` (CAPS, 188 lines), and `command.md` (the `/sc:spec-panel` definition).
- Citation check against the workspace. Verified: all 236 numeric `INV-A:N`, `INV-B:N` and `CAPS:N` references in the candidate resolve to a line inside the cited file (script run, none out of range). Spot-checked for meaning: the per-command rows of spec section 3 (lines 83-92, 99-125) against the INV rows they cite (INV-A:35-55, INV-B:31-52 and the matching note ranges), section 4 (lines 132-137) against INV-A:90-92 and INV-B:285-287, the 10 / 27 / 6 split (INV-A 5 / 13 / 3 plus INV-B 5 / 14 / 3, matches spec line 76; the 27 rows of 3.2 count to 27, the phase rows P1 9+4, P2 11+4, P3 4, P4 3 reconcile), the WC rows against CAPS:44-130, and README lines 6, 11-17, 12, 30, 31. No mismatch found.
- UNVERIFIED (not checkable inside the workspace, so taken as cited): every `src/superclaude/...` path:line in sections 2.1, 3, 4, 5 and 7, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/...`, `CLAUDE.md`, `HOW-WE-WORK.md`, `pyproject.toml`, `Makefile`, `install_core.py`, `tests/`, and the Orca guide output (carried only through CAPS lines). Candidate line 11 and line 285 claim two independent re-read passes; this review could not reproduce them.
- Not run: no live Orca, no command, no test. Every acceptance check (section 7) was read, not executed, except the AC-C5 regex, which was run on a two-line sample (finding M7).
- Auto-suggestion: the candidate has numeric thresholds (60 s, 5 min, 4 min, 0.70) and a multi-stage flow. The panel advises a later `--focus correctness` pass. Advisory only, not run here.

## Expert pass (fixed order, one line each)

1. **Wiegers (requirements foundation).** IDs (WC-, SA-, AC-, D-) and the table form are good. Traceability is incomplete: WC-1, WC-11 (beyond `save`), WC-12 and the cli-eval part of WC-10 have no acceptance check (M17). One flag is used with two meanings (F1).
2. **Adzic (examples).** Strong examples for D1 and the AC-2.x gate triggers. There is no example `return-contract.yaml`, only the field list in WC-4 and a Python assertion in 7.2 step 4 (note n3).
3. **Cockburn (actors and goals).** Primary actor (the coordinator) and the person are clear; the blocked-then-answer loop (WC-3) is only half specified (M15).
4. **Fowler (architecture).** One shared contract file plus a per-command section is the right seam. The phase boundaries do not follow the dependency boundaries: P1 touches commands whose behavior P2 to P4 define (F2). Nested commands are not covered by the contract (M1).
5. **Nygard (failure modes).** The silent-stall failure is recognised (section 1.4 point 2), but the coordinator gets no deadline or stall policy (M16), and a stale contract from an earlier attempt can be read as current (M3).
6. **Whittaker (adversarial).** Attacks are in the Adversarial Analysis section; they produced F1, M1 to M4, M7, M8.
7. **Newman (interfaces and evolution).** Reusing `return-contract.yaml` while forcing a four-value `status` has no versioning story (M5, n3).
8. **Hohpe (message flow).** Claim-check pattern (a `worker_done` that points at a file) is sound; ordering (file complete before `worker_done`) and nested producers sharing one path are not specified (M1, n9).
9. **Crispin (testing).** The static test only greps for a heading (AC-1.1), and three acceptance checks are weak or contradictory (M6, M7, M8).
10. **Gregory (quality conversation).** The five open decisions are well framed; D3 lacks one fact the user needs (M13).
11. **Hightower (operations).** Heartbeat and wait sizing are covered for pr-submit and cli-eval only (M9).

Consensus: the decision (Orca coordinates, commands stay units of work), the rejected alternative (section 1.3) and the non-goals are well supported by the checked evidence. Disagreement: Wiegers and Fowler both want the P1 scope narrowed to what P1 can finish (F2); Whittaker would add the output-path and nesting rules before any P1 work (F1, M1).

```yaml
quality_assessment:   # 0-10, whole document
  clarity: 7
  completeness: 6
  testability: 6
  consistency: 5
  overall: 6
```

## Grading used

Per the FIRST-REVIEW prompt: a finding is blocking only if the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption (two stated texts that contradict, a safety or data-loss break, or an acceptance criterion that cannot pass). A requirement the document never states, or a reading that needs a guess, is Medium and goes under follow-up candidates even when its label is MAJOR. Minor findings are notes.

=== REQUIREMENTS ANALYSIS ===

### F1. MAJOR, blocking. `--output` is a directory in WC-4 and a file in the rows and checks that use it
- **Expert:** Wiegers (consistency), Whittaker (sentinel collision, FR-2.3).
- **Location:** WC-4 (spec line 62) and 2.3 (line 73) versus 3.1 `tdd` (line 90), 3.1 `init-lite` (line 87), AC-2.2 (line 200), AC-1.2 (line 196), 7.2 step 4 (line 183).
- **Issue:** WC-4 says the contract is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". The same spec says `/sc:tdd` and `/sc:init-lite` take `--output <file>` (lines 90, 87), and AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and then requires a contract with `status: blocked` and a non-empty `blocked_question`. For these commands the flag the coordinator passes is a file, so there is no directory the text can resolve `<output-dir>` to.
- **Grading check:** An implementer who follows WC-4 as written for `/sc:tdd` with `--output <file>` builds a contract path of `<file>/return-contract.yaml`, and that is wrong because the TDD (or audit) file occupies that path, so no contract can be written; AC-2.2's `contract status: blocked` check and 7.2 step 4 (`test -s <contract>`) therefore cannot pass for `/sc:tdd`, and AC-1.2 (`--output <dir>` for every P1 command) hands a directory to `init-lite`, whose `--output` is a file. Two stated texts (WC-4 and the 3.1/AC-2.2 rows) contradict on what `--output` is.
- **Cross-check, not relied on:** the `/sc:spec-panel` definition used for this audit resolves the same clash with a separate flag: `--report-dir <dir>` only, because `--output` is file-valued (`command.md:460`; usage at `command.md:22-23`). Its relation to the spec's baseline command text is UNVERIFIED.
- **Recommendation:** state in WC-4 one rule for file-valued `--output` commands (for example, a separate directory flag, or the contract goes beside the file under a fixed name), name the rule per command in 3.1 and 3.2, and make AC-1.2 and AC-2.2 pass the matching flag. Rationale: the contract is the one place the coordinator learns about failure (WC-5), so its location has to be computable before dispatch.
- **Priority:** High. **Quality impact:** consistency +1.5, testability +0.5.

### F2. MAJOR, blocking. P1 scope and AC-1.1 require unattended support in commands whose behavior P2 to P4 and D2 to D4 decide
- **Expert:** Fowler (phase boundaries follow dependencies), Wiegers.
- **Location:** section 6 P1 row (line 159) and intro (line 154), AC-1.1 (line 195), P4 row (line 162), section 9 intro (line 225), D3 (lines 238-242), section 4 last paragraph (line 139), 3.2 rows `pr-submit`, `post-release`, `implement`, `auggie-review` (lines 100, 109, 113, 114).
- **Issue:** P1 is "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". AC-1.1 requires a `## Unattended mode` section in every command of 3.1 and 3.2 except `load`. That includes `pr-submit`, `post-release` and `implement` (P4) and the gate commands of P2. Section 6 says P4 "waits for answers to D2-D4", and section 9 says phases 0 to 3 proceed on the recommendations. The recommendation for D3 is (a), "no pr-submit changes in Phase 4", and line 139 says `pr-submit` is a worker candidate "only if the user accepts D3".
- **Grading check:** An implementer who follows P1 and AC-1.1 as written adds `--unattended` and a contract-naming `## Unattended mode` section to `/sc:pr-submit`, `/sc:post-release` and `/sc:implement`, and that is wrong because (1) under the recommended D3 (a) `pr-submit` must not become a worker command at all, so AC-1.1 cannot pass without contradicting D3 (a); (2) section 6 says each phase is "independently useful", yet after P1 a brief containing `--unattended` reaches `post-release` and `auggie-review` still prompting and still taking their outward defaults, which violates WC-2 and WC-9 ("under `--unattended` ... any default that pushes, opens a PR, posts ... is off") until P2 or P4 ships. The parenthetical "no-op where a command has no gate" leaves the gated commands undefined at P1.
- **Recommendation:** limit P1 (flag, section, AC-1.1) to the commands P1 lists in its Commands column; add each remaining command in the phase that delivers its gate resolution; make the pr-submit row of AC-1.1 conditional on D3 (b). Prefer deleting the "every command in 3.1 and 3.2" wording over adding a new rule.
- **Priority:** High. **Quality impact:** consistency +1.5, completeness +0.5.

=== ARCHITECTURE ANALYSIS ===

No architecture finding reaches blocking. Medium and minor architecture findings are M1, M3, M5, M9, M12, M13 and n3, n9 below. The core decision (sections 1.1 to 1.3) holds against CAPS:97-103, 147-150, 155 and INV-A:13-14.

## Mandatory artifact: Guard Condition Boundary Table

Guards enumerated: the conditional rules the spec itself defines (switch, output location, outcome mapping, resume rule, wait sizing, confidence threshold, and the two regex and count checks). Orca's own limits (readiness 60 s, depth 1) are inputs to the spec, not guards it defines, and are left out. Classes left out per guard are listed under the table with a one-line reason (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `unattended_switch` | D1, WC-2 (lines 51, 60, 228) | Zero/Empty | flag absent | false | today's behavior unchanged (SA-1, line 146) | OK |
| `unattended_switch` | P1 row (line 159) | One/Minimal | flag present, command has no gate | true | no-op (line 159) | OK |
| `unattended_switch` | P1 row vs P2/P4 rows (lines 159-162) | Typical | flag present on a gated command (auggie-review, post-release) after P1 only | true | flag accepted; gate and outward-default handling arrive in P2/P4 | GAP (F2) |
| `unattended_switch` | D1 (lines 227-230) | Sentinel Value Match | the text `--unattended` inside quoted user content, e.g. `/sc:tdd "parse --unattended flags"` | unspecified | no token rule; D1 (a) claims it "cannot misfire on a person" but only for a typed flag | GAP (M4) |
| `unattended_switch` | section 4 (line 128) | Legitimate Edge Case | flag passed to a section-4 command, e.g. `/sc:git --unattended` | unspecified | "get no `--unattended` mode"; refuse versus ignore not stated | GAP (M4) |
| `contract_path` | WC-4 (line 62) | Zero/Empty | no output directory passed, or `""` | unspecified | none: "written on every outcome" and "require an explicit output ... else blocked" (lines 107, 113) both need a directory that does not exist | GAP (M2) |
| `contract_path` | WC-4 (line 62) | One/Minimal | one directory passed, empty | true | `<dir>/return-contract.yaml` | OK |
| `contract_path` | WC-4 (line 62) | Typical | existing directory | true | `<dir>/return-contract.yaml` | OK |
| `contract_path` | WC-4, WC-11 (lines 62, 69) | Maximum/Overflow | two producers (parent and nested child, or N parallel children) given the same directory | unspecified | none for nested invocations | GAP (M1) |
| `contract_path` | WC-4 vs 3.1 `tdd`, `init-lite` (lines 62, 87, 90) | Sentinel Value Match | the passed value is a file path | unspecified | none | GAP (F1) |
| `contract_path` | WC-4, WC-6 (lines 62, 64) | Legitimate Edge Case | directory already holds a contract from an earlier attempt (resume or retry) | unspecified | none: no rule to remove or invalidate it at start | GAP (M3) |
| `outcome_mapping` | WC-5 (line 63) | Zero/Empty | no report file | true | `--outcome failed` | OK |
| `outcome_mapping` | WC-5 (line 63) | One/Minimal | `status: failed` or `blocked` | true | `--outcome failed` | OK |
| `outcome_mapping` | WC-5 (line 63) | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| `outcome_mapping` | WC-5, WC-4 (lines 62-63) | Sentinel Value Match | file present but `status` outside the four values, or unparseable YAML (for example an existing contract's own vocabulary) | unspecified | none | GAP (M5) |
| `outcome_mapping` | WC-5, decisions (lines 63, 263) | Legitimate Edge Case | `status: partial` | true | `--outcome succeeded`, body states `partial` | OK (see note n11) |
| `resume_or_fresh` | WC-6 (line 64) | Typical | command has a resume flag and it is given | true | resume from disk | OK |
| `resume_or_fresh` | WC-6 vs 3.1 `index-repo`, `init-lite`, `cleanup-audit` (lines 64, 85-87) | Zero/Empty | command has no resume flag and writes a fixed location | unspecified | WC-6 requires "a fresh output directory", but these rows keep a fixed location or "overwrite" | GAP (M12) |
| `wait_split` | WC-10 (line 68) | Typical | one tool call under 4 minutes | false | no change needed | OK |
| `wait_split` | WC-10 vs WC-7 (lines 65, 68) | Maximum/Overflow | one Agent-tool call (fan-out) running over 5 minutes, or a call of 4 to 5 minutes | unspecified | WC-10 targets "a poll wait, a long eval"; the Agent call cannot be split and WC-7 keeps fan-out unchanged | GAP (M9) |
| `confidence_gate` | 3.2 `task` (line 121) | Zero/Empty | confidence 0 | true | blocked | OK |
| `confidence_gate` | 3.2 `task` (line 121) | Legitimate Edge Case | confidence exactly 0.70 | false | proceeds (the gate is "below 0.70", INV-B:199) | OK |
| `diff_additive_check` | AC-C5, AC-0.3 (lines 176, 193) | Typical | deleted table row (`-\| a \|`) | true | detected | OK |
| `diff_additive_check` | AC-C5 (line 176) | Sentinel Value Match | deleted markdown bullet `- x` (diff line `-- x`) | false | not detected; passes as "additive" | GAP (M7) |
| `review_count_unchanged` | AC-2.4 (line 202) | Zero/Empty | PR has 0 reviews or comments | true | counts compared | OK |
| `review_count_unchanged` | AC-2.4 (line 202) | Maximum/Overflow | PR with 30 or more comments | unspecified | `gh api ... --jq length` has no `--paginate`, so the count stops at the first page | GAP (M8) |

Classes left out (reason, FR-10): `unattended_switch` Maximum (a boolean has no capacity); `contract_path` none (all six classes have a row); `outcome_mapping` Maximum (the status set is fixed at four values); `resume_or_fresh` One, Maximum, Sentinel (resume is a presence test with no count or magic value) and Legitimate Edge (a retry of a still-running dispatch is Orca's concern, CAPS:116); `wait_split` Zero, One, Sentinel (no empty wait exists; a wait of 0 s is not a wait); `confidence_gate` One, Maximum, Sentinel, Typical (a single numeric cut, covered by Zero and the boundary); `diff_additive_check` Zero, One, Maximum, Legitimate Edge besides the usage-line case folded into M7 (the check is line-based); `review_count_unchanged` One, Typical, Sentinel, Legitimate Edge (a count has no sentinel).

FR-8 / FR-9 grading: GAP rows tied to F1 and F2 name a concrete wrong outcome and are blocking; the other GAP rows need a guess or state a requirement the document never gives, so they are Medium (follow-up candidates). FR-10: the table is complete.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21)

Triggered: the spec describes a Task to worker to report to outcome flow where counts can diverge.

```text
[Coordinator Tasks: N] --> [worker-start: N dispatches]
                              |
                              v
                        [commands run: N]  (blocked or failed stops included)
                              |
              +---------------+----------------+
              v                                v
   [contracts written: M, M <= N]      [worker_done sent: K, K <= N]
   (fewer if a stop happens before     (fewer on a silent stall or
    any output dir exists: M2)          consumer_fenced, WC-12)
              |                                |
              v                                v
   [coordinator opens M contracts]     [coordinator reads K outcomes]
   Consumer 7.2 step 3 expects exactly one worker_done per dispatch (K = N) <-- holds only on the happy path
```

No dimensional mismatch is assumed by the requirements text: WC-5 maps "no report" to `failed`, and section 1.4 point 2 names the silent stall. The gap is the missing stall deadline (M16), which is Medium, not a count-conservation CRITICAL. The 43 → 10 / 27 / 6 split is conserved (see Coverage).

## Adversarial Analysis (Whittaker)

Five methodologies applied once per invariant that mattered. Format per the command (FR-3).

- **A1. I can break this specification by Sentinel Collision (FR-2.3).** The invariant at **WC-4 and 3.1 `tdd` / `init-lite` (lines 62, 87, 90)**, "the contract is at `<output-dir>/return-contract.yaml` and `--output` is that directory", fails when **the command's `--output` already means a file**. Concrete attack: before: brief `/sc:tdd "auth" --unattended --output .dev/tdd/auth.md`, contract path derived = `.dev/tdd/auth.md/return-contract.yaml`. After: the TDD writer creates the file `.dev/tdd/auth.md`; the contract write targets a path under a regular file and fails; worker maps "no report" to `failed` (WC-5) although the topic was bare and the intended result was `blocked`. State trace: output-dir = unresolved; contract = absent; outcome = failed instead of blocked. (F1)
- **A2. Sequence Attack (FR-2.4), phases.** The invariant at **section 6 intro and AC-1.1 (lines 154, 195)**, "a phase ends only when its checks pass and later phases wait", fails when **a P1 check needs content that P4 produces**. Concrete attack: before: D3 answered (a). P1 adds the section to `pr-submit` to satisfy AC-1.1. After: D3 (a) says no pr-submit changes, so the P1 section is either removed in P4 (the P1 check then fails again) or kept (a worker declaration the user rejected). (F2)
- **A3. Accumulation Attack (FR-2.5), shared path.** The invariant at **WC-4 and WC-11 (lines 62, 69)**, "one contract per output directory, parallel workers never write the same file", fails when **a command spawns nested unattended invocations**. Concrete attack: `/sc:tasklist` Stage 10.5 runs N reflects in parallel and passes them `--unattended` (line 122; INV-B:211). Before: the parent passed one directory D. After: N children each write `D/return-contract.yaml`, the last writer wins, and the parent's own write on every outcome may be overwritten by a child's `status: succeeded`. Same shape: `release-split` runs nested brainstorm and adversarial (INV-B:119, 121), `roadmap` calls `sc:save` at every wave (INV-B:154) and `save` writes single-owner keys unless told otherwise (line 119). (M1)
- **A4. Sequence Attack (FR-2.4), retry.** The invariant at **WC-4 and WC-6 (lines 62, 64)**, "the contract reflects the latest outcome", fails when **a resume or retry reuses the directory**. Concrete attack: attempt 1 for `/sc:implement --resume` writes `status: blocked`; the retry in the same directory crashes before it writes; `test -s <contract>` (7.2 step 4) passes on the old file, and a worker that reads the report after the command ends reports the stale status. State trace: contract = blocked (attempt 1), command = failed (attempt 2), report read = blocked. (M3)
- **A5. Zero/Empty Attack (FR-2.1), output.** The invariant at **WC-4 "written on every outcome ... including stops before any other output exists" (line 62)** fails when **no output directory was passed**: lines 107 and 113 resolve the gate "require an explicit output" as `blocked`, and `blocked` means writing the contract, which needs the directory just found missing. (M2)
- **A6. Sentinel Collision (FR-2.3), switch.** The invariant at **D1 (a) (line 228)** fails when **`--unattended` appears inside quoted content** (a symptom text for `/sc:troubleshoot`, a pasted command line for `/sc:tdd`). The command definition used here had to add a token rule for exactly this (`command.md:459`). (M4)
- **A7. Accumulation Attack (FR-2.5), count check.** AC-2.4 compares `gh api ... --jq length` before and after; on a PR with 30 or more comments the first page stays at 30 and a new comment passes unnoticed. (M8)

## Medium findings (graded by consequence; follow-up candidates, never block)

- **M1. Nested invocations have no contract rule.** MAJOR label, Medium grade (needs a guess about which child gets which directory). WC-4 and WC-11 do not say where a nested unattended command writes its contract or whether the parent passes `--unattended` down. Evidence: lines 62, 69, 118, 122; INV-B:119, 121, 154, 211. Expert: Hohpe, Whittaker. Recommendation: one sentence in WC-4: a nested command writes its contract only when given its own directory, and a parent passes `--unattended` and a child directory under its own. Priority: High.
- **M2. No fallback when the output directory is missing or empty.** Lines 62, 107, 113; A5. Medium (a requirement never stated). Recommendation: say where a `blocked` contract goes when no directory exists (refuse before work, printed in chat, as `command.md:460` does). Priority: Medium.
- **M3. Stale contract after resume or retry.** Lines 62-64; A4. Medium. Recommendation: the command removes or marks any existing contract before it starts work. Priority: Medium.
- **M4. The `--unattended` token has no parsing rule.** Lines 51, 128, 228; A6. Medium. Recommendation: define the token as a standalone argument outside quoted content, and say what a section-4 command does with it. Priority: Medium.
- **M5. Status vocabulary versus existing contracts.** Lines 62, 261-262. WC-4 says commands with a contract "keep their fields and add the missing ones" while `status` must be one of four values; the existing `status` values of workflow, brainstorm, reflect and adversarial are not listed in INV-A or INV-B (INV-B:272 gives only the workflow field names), so whether they clash is UNVERIFIED. AC-1.2 step 4 asserts the four-value set on every P1 command, workflow included. Recommendation: list existing values and a mapping, or version the contract. Priority: Medium. Expert: Newman.
- **M6. AC-C1 and the allowed mention of Orca.** Lines 147, 150, 172. SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file", and SA-5 adds an Orca section to `HOW-WE-WORK.md`, but AC-C1 greps all of `src/superclaude/core` (both files live there) for `orca orchestration|worktree|terminal|agent` with only `ccsession-tag` excluded. If either file spells the command out, the common check fails every phase. Recommendation: exclude the two named files in AC-C1 or forbid the spelled-out form. Priority: Medium. Expert: Crispin.
- **M7. AC-C5 detects additions badly in both directions.** Lines 149, 176. `grep -E '^-[^-]'` misses a deleted bullet (diff line `-- x`; run on a sample, printed nothing) and flags an edited Usage line that only gains a flag. Recommendation: `grep -E '^-' | grep -v '^---'`, and say how a new flag in a Usage line is allowed. Priority: Medium.
- **M8. AC-2.4 count comparison saturates.** Line 202; A7. Recommendation: add `--paginate` or compare IDs. Priority: Low-Medium.
- **M9. WC-10 versus fan-out.** Lines 65, 68, 202-210. WC-10 splits "a single tool call" over 5 minutes into waits of at most 4, but WC-7 keeps Agent-tool fan-out unchanged and an Agent call cannot be split (tdd, cleanup-audit, adversarial, troubleshoot Tier 2). AC-4.3 uses 240 s while WC-10 triggers at 300 s. Whether a late heartbeat harms is UNVERIFIED (CAPS:182). Recommendation: say WC-10 covers waits the command controls only. Priority: Low-Medium.
- **M10. "Phases 1-3 need no user decision" conflicts with D4.** Lines 100, 121, 154, 225, 244. D4 "affects ... auggie-review `--post-pr`, task `commit`/`push`", both P2 rows; under D4 (b) ("never") the P2 `auggie-review` text "posting returns only with an explicit `--post-pr` in the brief" changes. Recommendation: move the explicit-flag clauses to P4 or mark P2 as depending on D4. Priority: Medium.
- **M11. `tasklist` Stage 10.5 still has an unresolved human stop.** Line 122; INV-B:209 (`needs_human_decision` items HALT) and INV-B:109 (headless auto-accept "skips the gates"). The row resolves only the `[yes / no]` offer. The HALT outcome under `--unattended` and what "skips the gates" does to non-auto-fixable items are not stated, against WC-2 ("each gate resolves ... listed per command"). Recommendation: add the blocked resolution. Priority: Medium.
- **M12. WC-6 does not fit fixed-location commands.** Lines 64, 85-87, 119. `index-repo` (`PROJECT_INDEX.md`, `mode=update`), `init-lite` ("re-run overwrites"), `cleanup-audit` (fixed `.claude-audit/`) and `save` ("it writes resume state") are listed with neither a resume flag nor a fresh directory. Recommendation: state the retry rule for them. Priority: Low-Medium.
- **M13. D3 omits a stated Will-Not of `pr-submit`.** Lines 238-242, 114; INV-B:90 quotes "Will Not: run headless / imply a daemon" (`cmd/pr-submit.md:85`, `SKILL.md:225`). Whether `--unattended` is "headless" in that sense is UNVERIFIED, but D3 (b) would change that line and the user is not told. Recommendation: add the fact to D3. Priority: Low-Medium.
- **M14. Non-goal 8 versus two edits in 3.2.** Lines 102, 112, 220. Non-goal 8 limits scope to defects "that stop a command working as a worker"; the `load` usage-line fix and the `business-panel` frontmatter move (effect on loading UNVERIFIED, INV-A:120) do not, yet both are scheduled in P1 and listed in SA-4. Recommendation: reconcile the wording. Priority: Low.
- **M15. WC-3 relies on "the answer as a flag" that section 3 never defines.** Line 61. Most gates (implement Ruling, cli-portify approvals, pr-submit HALTs) have no answer flag in 3.2, so the ask-then-rerun path is undefined for them; it is "may", so no wrong outcome. Priority: Low.
- **M16. No stall policy for the coordinator.** Lines 44, 72-73, 282. Section 1.4 names the silent stall; section 2.3 lists what the coordinator owes but gives no deadline or action when no `worker_done` arrives (Orca's run-time bound is UNVERIFIED, CAPS:188). Expert: Nygard. Recommendation: add a per-brief deadline field. Priority: Medium.
- **M17. Traceability gaps (Wiegers).** WC-1 (owner "Launch setup", line 59) has no acceptance check; WC-12 (line 70) none; WC-11 is checked only for `save` (AC-3.4); WC-10 only for `pr-submit` (AC-4.3), not `cli-eval`. Priority: Low.

## Minor notes

- n1. Labels `[F1]` (lines 182, 194) and `(F2)` (lines 195, 196) are not defined in the document; they look like finding IDs from a review file this audit cannot see (`review/spec-panel.md`, README line 26). A reader of the spec alone cannot resolve them.
- n2. "The 43 commands in `cmd/`" (line 76) is backed by the two scope lists (INV-A:3, INV-B:3), not by a directory listing; completeness of `cmd/` is UNVERIFIED.
- n3. No example `return-contract.yaml` and no version field in WC-4 (workflow's contract carries one, INV-B:272).
- n4. P0 adds `tests/skills/test_worker_contract.py` (line 158) but no P0 check runs it.
- n5. AC-C3 runs only `tests/skills/` (line 174) while P0 edits `install_core.py` (line 52).
- n6. UNVERIFIED item 8 (line 279, the `plugins/superclaude/commands/` mirror) has no acceptance check in section 7.
- n7. E2 (line 22) says the worker "reached ... and answered"; CAPS:49 quotes only `state: ready, stage: input_accepted`. "and answered" is UNVERIFIED.
- n8. 7.2 step 5 (line 184) greps the transcript for the string `AskUserQuestion`; loaded protocol text contains the word, so the check must say "tool call".
- n9. WC-4 does not require writing the contract completely before `worker_done` (write then rename).
- n10. 3.2 `save` and `recommend` list "n/a" or prose in the WC-6 column rather than one of the two WC-6 options.
- n11. `partial` maps to `succeeded` (lines 63, 263); a succeeded Task releases its dependents (CAPS:88, 90), so the coordinator brief (2.3) should say it checks `status` before starting a dependent.

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15, M16, M17, n1 to n11.
No issue was opened. An `--unattended`-style worker run only records this list; the question whether to open issues is left to the session that owns the loop.

## Downstream propagation (structured, NFR-5)

| Source | Target | Item |
|--------|--------|------|
| Guard Condition Boundary Table GAP rows | `sc:adversarial` AD-1 | `unattended_switch` (token), `contract_path` (file value, nested, stale, missing), `outcome_mapping` (unknown status), `wait_split`, `diff_additive_check`, `review_count_unchanged` |
| Whittaker A1 to A7 | `sc:adversarial` AD-2 | assumptions: "`--output` is always a directory", "one writer per contract path", "a phase can finish before its dependent decisions" |
| Quantity Flow Diagram | `sc:roadmap` RM-3 | risk: K < N `worker_done` on stall with no coordinator deadline (M16) |

## Reviser brief

Blocking finding ids: F1, F2. (The reviser reads this report, not the command.)
- Revise only text a blocking finding names (F1: WC-4 and the rows or checks that pass `--output`; F2: the P1 row, AC-1.1 and the rows they cover).
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing over adding.
- Report the candidate's byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone (M1 to M17, n1 to n11), even under "apply all findings".
- Return the candidate once; do not award yourself a PASS.
- No brief clause overrode this scope in this run.

verdict: FAIL
