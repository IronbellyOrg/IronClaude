review: 1 of 3

# /sc:spec-panel critique: orca-worker-contract-spec.md (first review)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate SHA-256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not applicable (first review; no `--baseline`, no `--re-review`)
- reviewer model: claude-haiku-5-5
- focus: requirements, architecture (command.md:83 also makes Whittaker active in every panel review)
- brief: FIRST-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, sandbox home copy)
- grading: CRITICAL/MAJOR is blocking only when the grading-check sentence holds with no further assumption; otherwise Medium (follow-up candidate)

## Coverage

- Read in full: `command.md` (the `/sc:spec-panel` definition), `README.md` (shared context), `document_review_loop_prompts.md`, the candidate spec, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`.
- Consistency checks that passed: the 10 / 27 / 6 split (spec:76) reconciles with the inventories (INV-A summary 5 ready / 13 needs-change / 3 coordinator-only at INV-A:73; INV-B summary 5 / 14 / 3 at INV-B:278), and 21 + 22 = 43 commands. The §3 rows I compared against the inventories carry the same facts as their cited rows (for example spec:83 cites INV-A:35, 60-61 and the adversarial row says the same; spec:91 cites INV-B:49, 237-245; spec:112 cites INV-B:31, 57-65).
- Sampled citations that matched the workspace files: `CAPS:44-46, 49, 52, 58-61, 64, 66-67, 72-74, 79-80, 86, 88, 90, 92, 97-103, 107-116, 128, 130, 135-139, 145, 147-149, 151, 155, 158-161, 178, 180, 186-188`; `INV-A:14, 35, 39, 62, 66, 76-83, 94-98`; `INV-B:210, 242, 272, 292`; `README.md:6, 11-17, 12, 31, 35`.
- UNVERIFIED (cannot be checked in this sandbox): every `src/superclaude/...`, `.dev/codegraph-migration/...`, `.dev/evals/...`, `/opt/Orca/...`, `~/.claude/...` and `CLAUDE.md` path the spec cites (for example spec:25, 52, 92, 180-186 and the EVIDENCE lines in spec:23, 45, 59); the external Claude Code docs claim at `INV-A:14`. I judged the spec's logic against the inventory text only and did not confirm those external citations.
- Compliance checks that passed: installed-path lookups follow the CLAUDE.md table (spec:52 names `~/.claude/WORKER-CONTRACT.md`, a core doc; no `src/superclaude` path in the spec's primitive text); outward `gh` calls name `IronbellyOrg/IronClaude` explicitly (spec:202, 209); `uv run` is used (spec:191).
- No file was edited besides this report. No issue, comment or GitHub action was taken.

## Mandatory output artifacts

**Guard Condition Boundary Table** (triggered: the spec has outcome mapping, gate resolution and numeric thresholds). Every guard is enumerated below; input classes not used are noted under the table. Rows marked GAP map to a finding (FR-8).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | spec:63 | Zero/Empty | no report exists | true (failed branch) | `--outcome failed` | OK |
| WC-5 outcome mapping | spec:63 | Zero/Empty | contract file present, 0 bytes | false, falls to "otherwise" | `--outcome succeeded` | GAP (R-5) |
| WC-5 outcome mapping | spec:63, 263 | One/Minimal | `status: partial` | false | `succeeded` | OK (consumer hazard, A-1) |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match | `status: complete` (outside the four values WC-4 defines, spec:62) | false, falls to "otherwise" | `--outcome succeeded` | GAP (R-5) |
| WC-5 / WC-2(c) | spec:60, 63 | Legitimate Edge Case | `status: blocked`, `blocked_question` empty | true (failed branch) | `failed`; empty question not specified | GAP (A-3) |
| WC-4 output path | spec:62, 92 | Zero/Empty | command with no output-directory flag (`workflow`, spec:92) | path undefined | not specified | GAP (R-3) |
| WC-4 output path | spec:62, 83 | Typical | `adversarial --output X` | `X/return-contract.yaml` (WC-4) vs `X/adversarial/return-contract.yaml` (spec:83) | two paths stated | GAP (R-3) |
| `--unattended` switch | spec:51, 60, 228 | Zero/Empty | flag absent from the worker's command line | not unattended | standalone prompts run; no fail-safe stated | GAP (A-2) |
| WC-3 answer as flag | spec:61 | Legitimate Edge Case | answer supplied by the coordinator, not the user | answer becomes a flag | no restriction on the source | GAP (R-1) |
| WC-10 split | spec:68 | Boundary | single blocking call of 240 s | not split | fits the 5-minute cadence | OK |
| WC-10 split | spec:68 | Boundary | single blocking call of 300 s | "longer than 5 minutes" is false, not split | heartbeat due at 5 min cannot be sent during the call | GAP (A-8) |
| WC-1 fallback | spec:59 | Boundary | fallback at 45 s against the 60 s limit | "well inside" undefined | no number given | GAP (R-6) |

Input classes left out, each with its reason: Maximum/Overflow for WC-5 (the status is an enumerated string, no capacity bound); Typical for WC-10 (covered by the 240 s row). Table is complete for the guards the spec enumerates (FR-10 satisfied).

**Pipeline Dimensional Analysis**: not triggered. No stage changes an item count; the WC-5 mapping is a classifier, not a count stage.

**State Variable Registry**: not triggered (`--focus correctness` is not active).

## === REQUIREMENTS ANALYSIS ===

### R-1. WC-3 lets a coordinator's answer become an outward action or a Ruling

- Severity: MAJOR. Grade: BLOCKING. Experts: Wiegers (lead), Whittaker (FR-2.3 sentinel: data becomes control).
- Locations: spec:61 (WC-3), spec:67 (WC-9), spec:245 (D4(a)), spec:109 (implement row, "the Ruling rule itself is unchanged"), spec:234-236 (D2). Source: INV-A:66, quoting `sk/sc-implement-protocol/refs/qa.md:238`: "another agent's message ... [is] not acceptance".
- Issue: WC-3 says a worker "may ask the coordinator ... then re-invoke or resume the command with the answer as a flag". Nothing limits who supplies the answer. D4(a) and WC-9 say an outward action is authorized only by the user's own instruction, and the implement row keeps the Ruling rule even though D2 is still open.
- Attack (Whittaker, FR-2.3): the worker asks "may I open the PR?"; the coordinator answers "yes" on its own; WC-3 turns that into the PR flag.
- Grading sentence: "An implementer who follows WC-3 as written passes a coordinator reply such as 'yes, push' as the command's push flag, and that is wrong because WC-9 and D4(a) allow outward action only on the user's own instruction, which the reply does not establish."
- Recommendation: add to WC-3 that an ask answer may supply only values the user already gave (quoted in the brief, D4(a)); an ask answer never supplies a WC-9 flag or an implement Ruling. Then D2(a) and D4(a) need one statement each.

### R-2. The P0 acceptance check cannot pass as written

- Severity: MAJOR. Grade: BLOCKING. Experts: Wiegers (testability), Cockburn (acceptance scope).
- Locations: spec:182 (§7.2 step 3: "its report path is the WC-4 contract path"), spec:194 (AC-0.4: "steps 1-3 and 5-7 pass"), spec:79 ("the worker reports the named file until Phase 1 adds the contract"), spec:158 (P0 scope).
- Issue: the WC-4 contract is added in P1 (spec:159), so in P0 no file at the WC-4 path exists. Step 3 requires that path, yet AC-0.4 says step 3 passes in P0. Step 4 is then relaxed to the command's own report, but step 3 is not.
- Grading sentence: "An implementer who runs AC-0.4 as written finds §7.2 step 3 failing on each P0 smoke run, because the WC-4 path does not exist before P1, and AC-0.4 says step 3 must pass."
- Recommendation: give §7.2 step 3 a P0 form (the command's existing report path), or defer AC-0.4's live runs until each command's contract exists.

### R-3. The WC-4 contract path cannot be known before dispatch for two commands

- Severity: MAJOR. Grade: BLOCKING. Experts: Wiegers (traceability), Fowler (interface).
- Locations: spec:62 (WC-4: `<output-dir>/return-contract.yaml`, "known before dispatch"), spec:83 (adversarial: `<output>/adversarial/return-contract.yaml`), spec:91 (troubleshoot), spec:92 (workflow: brief passes only `--handoff none`; path `.dev/tasks/to-do/<id>/return-contract.yaml`). Sources: INV-B:242 (troubleshoot contract only with `--caller task-unified`), INV-B:52.
- Issue: WC-4 defines one path for every command. Adversarial's path is one level deeper. Workflow has no output-directory flag, so the rule has nothing to point at. Troubleshoot writes its contract only under a caller flag the brief does not pass.
- Grading sentence: "An implementer who follows WC-4 for workflow has no `<output-dir>` to write into, so the coordinator cannot know the contract path before dispatch, which WC-4 forbids, and the coordinator then opens no report and records the Task as failed under WC-5."
- Recommendation: replace the single rule with one table of exact paths per command (WC-4 default, plus named exceptions for adversarial, workflow and troubleshoot), and state whether workflow gains an output flag.

### R-4. AC-1.1 contradicts §3 and the phase tables, so P1 cannot pass

- Severity: MAJOR. Grade: BLOCKING. Experts: Cockburn (story structure: scope of each requirement), Wiegers (traceability).
- Locations: spec:76 ("Every changed command also gains the `## Unattended mode` section"), spec:84 and spec:87 (brainstorm and init-lite: fix "None"), spec:112 (load: report "none (see note)"), spec:265 (load decision: "a report file would be an unrequested addition"), spec:159-162 (phase lists: brainstorm and init-lite appear in no phase), spec:195 (AC-1.1: every §3.1-3.2 command has the section "naming `return-contract.yaml`"), spec:167 (a phase passes only when every check in its block passes).
- Issue: AC-1.1 asks for the section in every §3.1-3.2 command. §3 says only changed commands get it. Load's row says it writes no report and needs no contract. Brainstorm and init-lite are in no phase, so an implementer following §6 never edits them. AC-1.1 therefore fails and, by spec:167, P1 never passes.
- Grading sentence: "An implementer who follows the P1 list leaves brainstorm and init-lite without the Unattended section, so AC-1.1 fails and P1 cannot pass, and that is wrong because spec:167 makes AC-1.1 a condition of the phase."
- Recommendation: AC-1.1 should name the exact set that gets the section, exclude load, and give brainstorm and init-lite an explicit phase row (even "flag accepted, no gate, no change").

### R-5. WC-5 maps an empty or malformed contract to success

- Severity: MAJOR. Grade: BLOCKING. Experts: Whittaker (FR-2.1 Zero/Empty; FR-2.3 Sentinel), Wiegers (FR-8 GAP).
- Locations: spec:63 (WC-5: "`--outcome succeeded` otherwise, including `partial`"), spec:62 (WC-4: `status` "one of `succeeded`, `partial`, `failed`, `blocked`"), spec:183 (§7.2 step 4 checks status only when run), spec:263 (partial decision).
- Attack (Whittaker, FR-2.1): the run crashes after creating `return-contract.yaml` as a zero-byte file, or writes `status: complete`. WC-5's default branch sends `succeeded`; Orca settles the Task as succeeded, and dependents with `--deps` start on no output (see A-1).
- Grading sentence: "An implementer who follows WC-5 sends `--outcome succeeded` for `status: complete`, because WC-5 sends every status except failed and blocked to succeeded, and that is wrong because WC-4 defines four valid statuses and `complete` is not one of them."
- Recommendation: invert the default. `succeeded` only for an explicit `succeeded` or `partial`; any other, missing or empty status sends `failed` and writes a note that the contract is invalid.

### R-6. "Well inside the readiness limit" cannot be tested

- Severity: MINOR. Grade: Medium. Experts: Wiegers (measurability).
- Location: spec:59 (WC-1). Evidence in the workspace: CAPS:49 (a startup question passed with a 30 s fallback and failed above about 45 s, quoting EVIDENCE:45, 56).
- Issue: the requirement is "fall back on its own well inside the readiness limit (default 60 s)" with no number. The spec's own evidence puts the failure point at about 45 s.
- Recommendation: state a fixed fallback value (for example the 30 s the evidence passed with) and a test for it.

### R-7. §8 non-goal 8 contradicts the fixes scheduled in §3.2

- Severity: MINOR. Grade: Medium. Experts: Cockburn (scope), Wiegers (consistency).
- Locations: spec:220 (non-goal 8: "Only defects that stop a command working as a worker are in scope"), spec:102 (business-panel frontmatter; effect "UNVERIFIED", spec:278), spec:112 (load's usage-line fix), spec:149 (SA-4 allows both).
- Issue: neither fix stops a worker (the usage line is documentation; the frontmatter effect is unknown), yet both are in scope.
- Recommendation: restate non-goal 8 as "worker-blocking defects, plus the cosmetic fixes named in SA-4".

### R-8. WC-4 is not scheduled for the ready commands that lack a contract

- Severity: MINOR. Grade: Medium. Experts: Wiegers (traceability), Adzic (examples).
- Locations: spec:85 (cleanup-audit: `.claude-audit/pass<N>-summary.md`), spec:86 (index-repo), spec:87 (init-lite), spec:89 (release-split), spec:90 (tdd: "the TDD at `--output`"), spec:91 (troubleshoot: `REPORT.md`); phases spec:158-162; AC-2.3 spec:201.
- Issue: none of these commands writes a contract today, and no phase adds one (P1 and P2 list only the fixes in column 5). AC-2.3 requires a full §7.2 pass, which includes step 4 (`return-contract.yaml`), for tdd, troubleshoot and release-split.
- Note: WC-4 itself is generic, so the requirement is not missing; only its phase scheduling is. It becomes blocking if the reviser reads the phase tables as the complete scope.
- Recommendation: list the contract addition in the phase row for each of these six commands.

### R-9. Unattended auto-accept of reflect remediation is not classified under WC-2 or WC-9

- Severity: MINOR. Grade: Medium. Experts: Wiegers (requirements completeness), Nygard (safety defaults).
- Location: spec:88 (reflect: "make `--remediate` follow the existing headless auto-accept rule"). Compare spec:67 (WC-9 lists push, PR, post, install, provision, paid run; remediation handoff is not listed) and spec:59-60 (WC-2 resolutions (a) to (c)).
- Issue: the row does not say whether the auto-accepted remediation is a documented default under WC-2(a), a brief flag under (b), or is blocked under (c). Under WC-9's list it is not outward, but it launches corrective work with no person.
- Recommendation: name the WC-2 resolution, and state whether the brief must authorize it.

## === ARCHITECTURE ANALYSIS ===

### A-1. "Partial" settles a Task as succeeded, which starts its dependents

- Severity: MAJOR (consequence: dependents run on incomplete output). Grade: Medium, because the document never states a consumer rule for partial results (a missing restriction). Experts: Hohpe (message and dependency semantics), Newman (boundaries).
- Locations: spec:63 and spec:263 (partial maps to succeeded). CAPS:88 (blocked start refused until dependencies complete), CAPS:90 (a failed Task keeps dependents blocked).
- Issue: the spec relies on Orca's dependency rule to order work (spec:159-162 and the wave pattern at CAPS:86), and the dependency rule keys on success. A partial run therefore unblocks dependents that expect complete output. The spec gives no consumer rule (for example, dependents read the contract status first).
- Recommendation: add a consumer rule (dependents read `status` and stop on `partial`), or map partial to failed for dependency purposes.

### A-2. No fail-safe when `--unattended` is omitted

- Severity: MAJOR (consequence: a silent stall with no worker_done). Grade: Medium, because the document never states a restriction for an omitted flag (a missing restriction, not a stated text that does harm). Experts: Nygard (failure modes), Hightower (operational visibility).
- Locations: spec:51 (the flag is the only switch, D1(a) spec:228), spec:60 (WC-2), spec:146 (SA-1: without the flag, prompts stay), spec:181 and spec:184 (§7.2 steps 2 and 5 detect a stall only after it starts). Evidence: CAPS:49 (an unanswered start-up question fails at the 60 s limit), CAPS:52 (after start, a worker parked on a question is "healthy, not failed").
- Issue: a worker started without the flag runs standalone behaviour and parks on a question with no `worker_done`. Orca reports that as healthy, so the stall is silent until a person runs step 2.
- Recommendation: make `--unattended` a required field in the brief template (P0), and have §7.2 step 1 refuse to dispatch a brief without it.

### A-3. The blocked path has no coordinator procedure

- Severity: MINOR. Grade: Medium. Experts: Newman (service evolution), Hohpe (exchange pattern).
- Locations: spec:60 (WC-2(c): blocked writes the report and stops), spec:63 (blocked maps to failed), spec:72 (§2.3 has no step for a blocked Task). Evidence: CAPS:116 (`worker-start --retry-of`).
- Issue: after a blocked outcome the Task is failed. The spec never says what the coordinator does next (read `blocked_question`, get the answer, retry with it as a flag), so the path cannot be run as written.
- Recommendation: add to §2.3 the retry step with the answer as a flag, with the R-1 limits applied.

### A-4. The rejected alternative states an unverified mechanism as settled

- Severity: MINOR. Grade: Medium. Experts: Fowler (design rationale).
- Locations: spec:33 (R1: a command calling `worker-start` "would be refused with `nested_worker_depth_exceeded`"; "The two designs exclude each other"), spec:43 (gap 1), CAPS:97-101, CAPS:103 (call-site enforcement "UNVERIFIED").
- Issue: the refusal is stated as fact in the same row that marks its enforcement UNVERIFIED. The rest of R1 (R2 to R5) carries the rejection, so the exclusion sentence is the overstated part.
- Recommendation: "would be refused if the depth fence applies to `worker-start` (UNVERIFIED, CAPS:103)", and drop "the two designs exclude each other".

### A-5. E3 is cited for the direct route but proves only the nested route

- Severity: MINOR. Grade: Medium. Experts: Fowler.
- Locations: spec:23 (E3: "It has worked before ... landed as PR #329") against spec:43 (gap 1: the PR #329 brief used an Agent-tool subagent, "so it proves the nested route, not the direct route"). Source: `README.md:12`.
- Issue: the evidence table presents E3 as support for the decision that workers run commands directly. §1.4 says it does not.
- Recommendation: mark E3 "nested route only" in §1.2 and move it to the gap list.

### A-6. Tasklist fan-out depth is misstated and rests on an UNVERIFIED nesting claim

- Severity: MINOR. Grade: Medium. Experts: Newman (service decomposition and nesting).
- Locations: spec:122 ("its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit", citing INV-A:14). INV-B:210 (Stage 10.5 runs `/sc:reflect` in N subagents, each of which spawns its own agents, which is subagent-to-agent nesting). INV-B:210 and INV-B:314 mark whether nested spawning works as UNVERIFIED. INV-A:14 cites an external docs page (UNVERIFIED here).
- Issue: from the worker's point of view, reflect's agents are two layers down, not one. The spec settles as safe a point its own inventory lists as unverified, and it adds no live check for this path.
- Recommendation: state two layers, mark nested spawning UNVERIFIED, and add a P2 live check for tasklist Stage 10.5.

### A-7. WC-11 is violated by cleanup-audit's fixed output directory, and the workaround is not enforceable

- Severity: MINOR. Grade: Medium. Experts: Hohpe (shared channels).
- Locations: spec:69 (WC-11: default output paths carry a timestamp or the slug), spec:85 (cleanup-audit: fixed output directory; "one audit per worktree at a time (WC-11)"), spec:76 (workers share the worktree by default, CAPS:115).
- Issue: WC-11 does not contain the "one at a time" rule the row cites. Orca does not serialize workers in one worktree (CAPS:115), so the rule depends on coordinator discipline.
- Recommendation: give cleanup-audit a slug from the brief, or add a lock rule to WC-11.

### A-8. The heartbeat boundary leaves a gap at exactly 5 minutes

- Severity: MINOR. Grade: Medium. Experts: Nygard (liveness).
- Locations: spec:68 (WC-10: split waits "longer than 5 minutes" into at most 4), spec:181 (§7.2 step 2: 5-minute observation). Evidence: CAPS:130 (cadence from the preamble, not a guide); the same line marks whether Orca uses heartbeat age UNVERIFIED.
- Issue: a single 300-second call is not split, and the 5-minute heartbeat cannot be sent during it. Whether the gap matters depends on the UNVERIFIED liveness rule.
- Recommendation: use "5 minutes or longer" as the trigger, matching the 4-minute target.

### A-9. The "no command calls Orca today" baseline may be wrong

- Severity: MINOR. Grade: Medium (not blocking: the file could not be read here). Experts: Fowler (baseline), Hightower (operations).
- Locations: spec:25 (E5: "no command, skill or agent calls Orca today"; only `sk/ccsession-tag/`), spec:147 (SA-2), spec:172 (AC-C1 grep).
- Issue: the skill listing supplied to this worker describes `sc:issue` / `sc-issue-protocol` as creating an Orca worktree and launching an agent. If the repository copy does that, E5 is wrong and AC-C1 (spec:172) fails on the first run. UNVERIFIED in this sandbox: the skill file is outside the workspace.
- Recommendation: run AC-C1 before P0 and correct E5 if it matches.

## Follow-up candidates (Medium and minor, not blocking)

Recorded for the coordinator. No issue was created; the session that ran the review asks the user whether to open issues, and this run is unattended, so the list is only recorded.

1. R-6: give WC-1's fallback a number (spec:59).
2. R-7: restate non-goal 8 and reconcile it with SA-4 (spec:220, 149).
3. R-8: schedule the contract addition for tdd, troubleshoot, release-split, cleanup-audit, index-repo, init-lite (spec:85-91, 158-162).
4. R-9: name the WC-2 resolution for reflect's auto-accept (spec:88).
5. A-1: consumer rule for partial results (spec:63, 263).
6. A-2: required `--unattended` in the brief template (spec:51, 60, 146).
7. A-3: coordinator retry procedure for blocked (spec:60, 72).
8. A-4: soften R1 (spec:33).
9. A-5: relabel E3 (spec:23).
10. A-6: tasklist depth and live check (spec:122).
11. A-7: cleanup-audit output path (spec:69, 85).
12. A-8: heartbeat trigger at 5 minutes or longer (spec:68).
13. A-9: verify E5 with the AC-C1 grep (spec:25, 172).

## Reviser brief

Blocking finding ids: R-1, R-2, R-3, R-4, R-5.

Restated bullet 6 of the Review Loop: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser prefers deleting or narrowing to adding and reports the byte size before and after, with the bytes added and deleted per finding id.

Brief narrowing: none. This brief does not override any clause of the command.

verdict: FAIL
