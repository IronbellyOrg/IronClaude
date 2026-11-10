review: 2 of 3

# Spec-panel re-review, round 2: Orca worker-contract spec

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` |
| Candidate (CANDIDATE) | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `89aa60a626c2210c7e3cd02a711923cbaf3990a333b6398f744d27073b0d61ba` (58012 bytes) |
| Baseline (BASELINE) | `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57763 bytes) |
| Prior (PRIOR) | `.dev/orca-command-refactor/review/round1.md`, sha256 `8aed26581cbda6d41eb9919105c143b08f3b91008291767994d70d115caf6936`, header `review: 1 of 3`, so N = 2 |
| Reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| Prompt followed | RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full first; roles table, Step 1, review number, self-check applied in that order) |
| Mode | critique with `--re-review` and `--baseline`; `--iterations` ignored, Improve step skipped, no revised specification written (command.md:261) |
| Coverage | scoped PASS: changed lines + prior blockers |

Citation shorthand: `SPEC:N` = line N of the candidate; `BASE:N` = line N of the baseline; `R1:N` = line N of `round1.md`; `INV-A:N`, `INV-B:N` = `inventory/commands-a.md`, `commands-b.md`. A citation to a file outside `.dev/orca-command-refactor/` (`src/...`, `cmd/...`, `sk/...`) could not be checked in this sandbox and is UNVERIFIED.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Six lines changed (62, 76, 112, 159, 195, 196); the line count is unchanged, so SPEC:N = BASE:N. Only the changed fragment is bold in the AFTER text; the lines are otherwise copied verbatim from the diff output.

**BEFORE (baseline)**

- BASE:62 `... In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern ...`
- BASE:76 `... "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). ...`
- BASE:112 `| load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; ... | P1 (usage line only) |`
- BASE:159 `... the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); ...`
- BASE:195 `... asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, ...`
- BASE:196 `| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |`

**AFTER (candidate)**

- SPEC:62 `... writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`); **when the output flag names a file (tdd, init-lite), the contract is that path plus `.return-contract.yaml` (B-1), for example `docs/TDD_AUTH.md.return-contract.yaml`**. It follows ...`
- SPEC:76 `... "Contract" means the WC-4 file **(path rule in WC-4, B-1)**. Every changed command **except load (B-2)** also gains the `## Unattended mode` section (section 2.1). ...`
- SPEC:112 `| load | no gate | **none; outside the contract set (B-2)** | n/a | none: use it as a step inside another worker's brief, not as its own Task; ... | P1 (usage line only) |`
- SPEC:159 `... the `--unattended` flag accepted by every command in sections 3.1 and 3.2 **except load (B-2)** (a no-op where a command has no gate); ...`
- SPEC:195 `... asserts that every command in sections 3.1-3.2 **except load (B-2)** has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, ...`
- SPEC:196 `| P1 | AC-1.2 | 7.2 live check on each P1 command **except load (B-2)** with `--unattended --output <dir>` | all steps pass |`

**Self-check (commands run).** For each of the six AFTER lines (without `>`), `grep -nFx` in CANDIDATE found it at the same line number (62, 76, 112, 159, 195, 196) and found it nowhere in BASELINE. For each of the six BEFORE lines (without `<`), `grep -nFx` in BASELINE found it at lines 62, 76, 112, 159, 195, 196 and found it nowhere in CANDIDATE. Roles are not swapped. The six changed line numbers match the line numbers `revise1.md` lists. Net size change +249 bytes (57763 to 58012) matches `revise1.md`'s byte accounting.

## What this review covered

- Read in full: the command definition, the review-loop prompts file, `README.md`, the prior report (`round1.md`, including its verification block at R1:2 and its Reviser brief at R1:237-248), `verify-1.md`'s verdict line (`confirmed: B-1, B-2`), `revise1.md`, and the whole candidate (285 lines).
- Prior blocking findings re-checked against the AFTER text only: B-1 and B-2. The verification block (R1:2) names B-1 and B-2 as the only confirmed blocking ids and rejects none, so there is no noted-and-unactioned id.
- Inspected for changed behaviour and the dependencies it touches: every line that quotes or relies on WC-4's location rule (SPEC:62, 73, 76, 87, 90, 92, 182, 183, 195, 196, 200) and every line that says "every command in 3.1-3.2" or lists load (SPEC:76, 79, 112, 139, 149, 159, 195, 196, 265).
- Guard Condition Boundary Table scoped to guards on changed lines only (command.md:262).
- Not done: no Orca command was run; no `src/`, `cmd/` or `sk/` file was read (not in the sandbox).
- `--focus correctness` is not active, so no State Variable Registry. Pipeline Dimensional Analysis: the only count that changed is the contract-set size (see M-6 note below); no new multi-stage flow appears on a changed line, so no new Quantity Flow Diagram is produced beyond that note.

## Prior blocking findings

| Id | Prior status | Status now | Evidence (AFTER text only) |
|---|---|---|---|
| B-1 | blocking (R1:87-93) | **resolved** | The defect was that WC-4 defined the contract path from a directory while tdd and init-lite pass a file, so no contract path was defined (SPEC:87, SPEC:90 unchanged and still pass `--output <file>`). SPEC:62 now adds the rule "when the output flag names a file (tdd, init-lite), the contract is that path plus `.return-contract.yaml` (B-1), for example `docs/TDD_AUTH.md.return-contract.yaml`". For AC-2.2's own input (`/sc:tdd "auth" --unattended --output <file>`, SPEC:200) the contract path is `<file>.return-contract.yaml`: derivable from the brief alone (so "known before dispatch" holds), never below a regular file, and distinct from the TDD's own path. Step 4 (`test -s <contract>`, SPEC:183) and step 3 ("its report path is the WC-4 contract path", SPEC:182) resolve through WC-4. AC-1.1's substring `return-contract.yaml` is still contained in `.return-contract.yaml` (SPEC:195). SPEC:76 no longer restates the old template. |
| B-2 | blocking (R1:95-101) | **resolved** | The defect was AC-1.1 and AC-1.2 requiring a contract and a live contract-writing run from load while SPEC:112 and SPEC:265 say load has no report and is not its own Task. SPEC:195 now exempts load from AC-1.1 ("except load (B-2)"), SPEC:196 exempts it from AC-1.2, SPEC:159 exempts it from the `--unattended` flag scope, SPEC:76 exempts it from the `## Unattended mode` section, and SPEC:112's report cell reads "none; outside the contract set (B-2)". SPEC:265 (unchanged: "a report file would be an unrequested addition") and the "not as its own Task" text (SPEC:112, unchanged) now agree with every check that mentions load. The remaining P1 mention (SPEC:159 "load (usage line only)", SPEC:112 "P1 (usage line only)") is consistent: load is in P1 for its usage-line fix only. |

No prior blocking finding is open or regressed.

## Findings on lines changed against the baseline

None blocking. One new Medium note on a changed line (below), and one inherited-text note that quotes a changed line.

### Guard Condition Boundary Table (changed lines only)

Guard on changed lines: G1, the WC-4 contract location rule (SPEC:62). The load exemptions at SPEC:76, 112, 159, 195, 196 are scope statements, not guards. Classes that cannot occur for G1 are left out with a reason under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 contract location | SPEC:62 | Zero/Empty | `--output` names a file, tdd (`docs/TDD_AUTH.md`) | file branch | `docs/TDD_AUTH.md.return-contract.yaml` (SPEC:62) | OK |
| G1 | SPEC:62, SPEC:87 | Typical | init-lite `--output <file>` | file branch | `<file>.return-contract.yaml` by SPEC:62; init-lite's default report (`.dev/superclaude/context-audit.md`, SPEC:87) applies only when no `--output` is passed, and SPEC:87 says the brief must pass `--output <file>` | OK |
| G1 | SPEC:62 | Typical | `--output <dir>` (adversarial, brainstorm, reflect) | directory branch | `<output-dir>/return-contract.yaml` (SPEC:62) | OK |
| G1 | SPEC:62, SPEC:99-123 | Legitimate Edge Case | a command that gains a new `--output` in P1 (analyze, document, explain, spec-panel) and whose value may be a file or a directory | undefined which branch | SPEC:62 names only "(tdd, init-lite)" as file-valued; the rows say "add `--output`" without a value type (SPEC:99, 107, 108, 120) | GAP (Medium, M-16) |
| G1 | SPEC:62 | Legitimate Edge Case | the parent directory of `<file>` does not exist | undefined | not stated who creates it | GAP (minor, n-13) |

Classes left out: Maximum/Overflow (a path has no capacity the spec relies on); Sentinel Value Match (no sentinel in the new clause); One/Minimal (covered by the Typical rows).

FR-10: the single guard on a changed line is enumerated and each applicable class has a row or a reason; the table is complete.

### M-16 (Medium, origin=changed): WC-4's file-branch rule lists only tdd and init-lite

- Quoted changed line: SPEC:62 "when the output flag names a file (tdd, init-lite), the contract is that path plus `.return-contract.yaml`".
- Why Medium and not blocking: the sentence "an implementer who follows the stated text builds X, and X is wrong" needs a guess. The rows that add an `--output` in P1 (SPEC:99, 107, 108, 120) state no value type, so the implementer would pick a path; no stated text contradicts another. This is the already-open M-2 (WC-4's location rule has no answer for further row shapes, R1:110-114) seen from the changed line, not a new contradiction. `INV-B:182` and `INV-B:185` show spec-panel has no `--output` today, so the type of the value to add is a free design choice.
- Recommendation (follow-up only): say whether the rule is "a value that is a regular-file path" rather than a closed list, or add a contract-path column to sections 3.1/3.2. Priority: Medium.

### Inherited-text note quoting a changed line (origin=unchanged, minor)

- Carried M-2 (no new id): the new exemption at SPEC:196 for AC-1.2 does not change that cleanup-audit and index-repo have no output flag (SPEC:85-86 "Brief must pass: none" / `--pass <N>`), so AC-1.2's `--unattended --output <dir>` for them is still the M-2 shape. It quotes the changed line SPEC:196 but the dependency is the unchanged brief cell; it stays a Medium carried item (M-2), not a blocker, because the implementer would pick a path and nothing forces a wrong outcome.

## Newly discovered older defects

None severe. The two items worth the coordinator's attention are carried Medium findings, not new blockers:

- M-6 (carried from R1:122-125, origin=unchanged): brainstorm and init-lite are in no phase's Commands column, yet SPEC:159's scope and SPEC:195 (AC-1.1) cover them. The load exemption did not change this: AC-1.1 now applies to 36 of 37 commands, and 35 appear in the Commands columns. An implementer who reads the Commands column omits the two sections and then fails AC-1.1; an implementer who reads the scope sentence adds them. Both readings are allowed by the text, so Medium stays.

## Carried follow-up candidates (unchanged from round 1; Medium and minor never trigger a revision)

Medium: M-1 (retry and stale report), M-2 (location rule for further row shapes), M-3 (status vocabulary collision), M-4 (heartbeat versus Agent-tool waits), M-5 (three wait thresholds), M-6 (two commands in no phase), M-7 (readiness claim), M-8 (P0 uses P1 features), M-9 (`--unattended` with person-mode flags), M-10 (WC checks missing), M-11 (new flags versus additive diff), M-12 (shared contract file with no fallback), M-13 (live check unbounded), M-14 (evidence overstatements), M-15 (`--post-pr` flag unverified), plus new M-16 above.

Minor: n-1 to n-12 from R1:216-229 (unchanged), plus n-13 (parent directory of a file-valued `--output` not stated; `revise1.md` lists the same interaction as left alone).

The session that ran this review asks the user once per loop whether to open an issue for these candidates and creates none without the answer. This run cannot ask; the coordinator should put the question.

## Brief clauses overridden

None. The brief narrowed the checkable evidence to `inventory/` and the workspace and asked for a re-review per the RE-REVIEW prompt; this review followed both. No brief clause graded a minor or Medium finding as blocking or authorized an edit.

## Reviser brief

No blocking finding is open (B-1 resolved, B-2 resolved, no new blocking finding), so there is nothing to revise. Medium and minor findings are not part of any Reviser brief, and the Reviser contract (revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on every addition; prefer deleting or narrowing; report bytes before and after and added/deleted per finding id) applies if a later review opens a blocking finding.

verdict: PASS
