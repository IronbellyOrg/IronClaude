review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (review 1 of 3)

## Header

- Command: `/sc:spec-panel --mode critique --focus requirements,architecture`, FIRST-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before this review).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines, 57763 bytes).
- Candidate SHA-256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.
- Baseline: none. This is a first review, so no baseline or prior report applies.
- Reviewer model: claude-haiku-5-5, one reviewer. `superclaude review panel resolve` and `superclaude review merge` are not on PATH in this sandbox, so the panel and merge steps did not run.
- Outcome: FAIL, with two blocking findings (F1, F2).
- Note on order: the bullets require the findings block as the last section and the Reviser brief just above the final verdict line. Both cannot be literally last, so I kept the verdict as the final line, placed the Reviser brief directly above it, and put the findings block directly above the brief.

## Coverage

- Read in full: `command.md` (the command definition), `.dev/orca-command-refactor/README.md:1-39`, the review-loop prompt file, and the candidate spec (lines 1-286).
- Read for evidence: `inventory/orca-capabilities.md` (CAPS lines), `inventory/commands-a.md` (INV-A lines 14, 30-56, 60-66, 74-98, 106, 113-120) and `inventory/commands-b.md` (INV-B lines 29-52, 65, 105, 207-215, 285-323). Each inventory line I read matched the spec's use of it. I did not read every cited inventory line, so the coverage is a sample, not a full citation check.
- Ran in the sandbox: the AC-C1 grep (spec:172) and the AC-C5 diff filter (spec:176) against probe text. Results are under F2 and F10. The probe files were deleted.
- Not checkable in this workspace, so UNVERIFIED here: every path under `src/superclaude/`, `tests/`, `cmd/`, `sk/`, `.dev/evals/`, `.dev/codegraph-migration/`, `plugins/`, `pyproject.toml`, `CLAUDE.md`, and the `EVIDENCE.md` lines. Where the inventories quote the same text, I note that as secondhand agreement only. No Orca was run, so no Orca behavior is verified beyond the inventory's numbered command output.
- Coverage limit: I did not check every citation in the spec. The sample covers the citations that the findings below rely on.

## Mandatory Output Artifacts

### Guard Condition Boundary Table

Triggered: yes. The spec has conditional and threshold rules (WC-1, WC-2, WC-3, WC-5, WC-6, WC-9, WC-10, WC-4, the 7.2 pass conditions). The table is complete under FR-10: every guard is enumerated and each input class is either given a row or left out with a one-line reason. Each GAP row is graded with the FIRST-REVIEW grading check, under which a GAP is Medium when following the text needs a choice between two readings. Each GAP row maps to a numbered finding.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | spec:63 | Zero/Empty: no report file | no `return-contract.yaml` | `--outcome failed` | "or no report exists" | OK |
| WC-5 outcome mapping | spec:63 | Zero/Empty: 0-byte contract file | size 0 | "otherwise" gives succeeded | not stated whether an empty file is a report (F3) | GAP |
| WC-5 outcome mapping | spec:63 | One/Minimal: `status: blocked` | `blocked` | `--outcome failed` | stated | OK |
| WC-5 outcome mapping | spec:63 | Typical: `status: partial` | `partial` | `--outcome succeeded` | stated (spec:263) | OK |
| WC-5 outcome mapping | spec:63 | Sentinel: status missing or outside the four values | `Succeeded`, no key | "otherwise" gives succeeded | no rule for unknown status (F3) | GAP |
| WC-5 outcome mapping | spec:63 | Legitimate edge: audit verdict FAIL | `succeeded` | `--outcome succeeded` | stated | OK |
| WC-5 outcome mapping | spec:63 | Maximum/Overflow | n/a | n/a | left out: `status` is a closed four-value enum, no numeric bound | n/a |
| WC-1 readiness fallback | spec:59 | Typical: prompt fallback | 30 s (secondhand, EVIDENCE quoted at CAPS:49) | passes | "well inside the readiness limit" has no number (F4) | GAP |
| WC-1 readiness fallback | spec:59 | Maximum: fallback at the limit | 60 s (CAPS:44) | not "well inside" | implied fail, not stated | GAP |
| WC-1 readiness fallback | spec:59 | Zero/Empty: no prompt | none | passes | implicit | OK |
| WC-10 wait split | spec:68 | Typical: one call 3:00 | 180 s | not split | stated | OK |
| WC-10 wait split | spec:68 | Legitimate edge: one call 4:30 | 270 s | not split | rule says split only above 5 min; rationale (spec:266) wants 4 min (F5) | GAP |
| WC-10 wait split | spec:68 | Maximum/Overflow: one call exactly 5:00 | 300 s | not split | "longer than 5 minutes" excludes 5:00, so the heartbeat window is not protected (F5) | GAP |
| WC-2 gate resolution | spec:60 | Zero/Empty: required flag absent | `--suite` absent | blocked, contract written | stated (c) | OK |
| WC-2 gate resolution | spec:60 | Legitimate edge: flag present, empty value | `--suite ""` | not defined | not stated (Medium, folded into F15) | GAP |
| WC-3 ask | spec:61 | Maximum/Overflow: coordinator never answers | timeout, unanswered | "resumes the same message ID" only | no next step, no bound (F15) | GAP |
| WC-9 outward defaults | spec:67 | Zero/Empty: brief authorizes nothing | none | off | stated | OK |
| WC-4 report path | spec:62 | Zero/Empty: unattended run with no `--output` | none | not defined | no rule for the path (F9) | GAP |
| WC-6 resume or fresh | spec:64 | Typical: retry with the same output dir | same dir | overwrites attempt 1 unless the command makes a new dir | who chooses the fresh dir is not stated (F6) | GAP |
| WC-12 check | spec:70 | Sentinel: `check` returns `consumer_fenced` | value | stop, no `worker_done` | stated | OK |
| WC-12 check | spec:70 | Other: `check` returns an error or empty result | other | not defined | only `consumer_fenced` is named (F15) | GAP |
| 7.2 step 2 | spec:181 | Zero/Empty: `worker-show` has no `agentWait` field | field absent | counts as pass | absent means "never looked" (CAPS:129, `[H:worker-show]` line 16), not null (F16) | GAP |

Summary: 9 GAP rows; each maps to F3, F4, F5, F6, F9, F15 or F16. None is graded blocking under the grading check.

### Pipeline Dimensional Analysis

Not triggered. The only multi-hop flow is command output, then `return-contract.yaml`, then the `worker_done` outcome, then the coordinator read (spec:62-63, spec:73). It carries one record per Task and changes no count, so no Quantity Flow Diagram is needed.

### Correctness-focus artifacts

Not required. The focus is requirements and architecture, so no State Variable Registry is produced.

## Findings

=== REQUIREMENTS ANALYSIS ===

### F1. Contradiction between the P0 smoke runs and the brief rule. CRITICAL, blocking.
- Expert: Wiegers (lead), Adzic.
- Issue: section 2.3 says every Task brief carries "the exact command line including `--unattended`" (spec:73). P0 says it runs "the 10 ready commands ... before any command changes" (spec:158). P1 is where `--unattended` first appears: "the `--unattended` flag accepted by every command" (spec:159). The ready commands are listed as running "if the brief uses the stated flags" (spec:79), and those flags do not include `--unattended`.
- Grading sentence: an implementer who follows section 2.3 for P0 passes `--unattended` to `/sc:troubleshoot` (spec:158), which does not accept it yet, and that is wrong because the P0 test then exercises a flag that does not exist. An implementer who follows spec:79 omits the flag, and that is wrong because section 2.3 then fails. The two texts cannot both be satisfied in P0.
- Recommendation: state in 2.3 that P0 briefs omit `--unattended` (and say the P0 run tests the unmodified commands), or move the P0 smoke runs to P1.
- Priority: High. Quality impact: high, because P0 is the decision test (spec:158, AC-0.4 spec:194).

### F2. AC-C1 cannot fail, so the SA-2 and WC-8 gate always passes. CRITICAL, blocking.
- Expert: Whittaker (attack), Crispin (test validity).
- Issue: AC-C1 (spec:172) is `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'`. Under `-E`, `\|` is a literal pipe, not alternation. I ran the pattern on probe text containing `orca orchestration task-create` and `orca-ide worktree list`: the grep printed nothing and exited 1. The corrected pattern with `|` printed both lines and exited 0.
- Attack: I can break this specification by **FR-2.1 Zero/Empty Attack**. The invariant at spec:172 (and SA-2, spec:147; WC-8, spec:66) fails when a command file contains `orca orchestration worker-start`. Concrete attack: the check prints nothing and reports a pass, so the phase gate in spec:169-175 accepts the breach.
- Grading sentence: an implementer who runs AC-C1 as written gets no output and records SA-2 as satisfied, and that is wrong because the pattern cannot match any Orca call. No further assumption is needed.
- Recommendation: replace `\|` with `|` in the pattern, and add a positive self-test (the check must match a planted line) to AC-C1.
- Priority: High. Quality impact: high, because every phase (spec:169, "every common check") depends on it.

=== ARCHITECTURE ANALYSIS ===

### F3. WC-5 defaults to succeeded for an empty or unknown-status contract. MAJOR, Medium (non-blocking).
- Expert: Whittaker (attack), Hohpe.
- Issue: WC-5 maps the outcome to `failed` only when the report "says `failed` or `blocked`, or no report exists", and to `succeeded` "otherwise" (spec:63). A 0-byte file exists, and a file with no `status` key is neither a failed nor a blocked report.
- Attack: I can break this specification by **FR-2.3 Sentinel Collision Attack**. The invariant at spec:63 fails when the contract `status` is missing or outside the four values. Concrete attack: a contract with `status: Succeeded`, or a 0-byte file, yields `--outcome succeeded` under the "otherwise" clause.
- Grading: a guess is needed to read "no report exists" as "no non-empty report". Medium.
- Recommendation: make "otherwise" apply only to `status` in {`succeeded`, `partial`}, and map any other content to `failed`.
- Priority: High.

### F4. WC-1 fallback has no number. MAJOR, Medium (non-blocking).
- Expert: Nygard.
- Issue: spec:59 requires the prompt to "fall back on its own well inside the readiness limit (default 60 s)". The evidence gives 30 s passing and above about 45 s failing (secondhand, EVIDENCE quoted at CAPS:49-50). "Well inside" has no threshold.
- Recommendation: state the fallback value and its maximum, for example 30 s with the 60 s limit.
- Priority: Medium.

### F5. The WC-10 trigger and the wait target disagree. MAJOR, Medium (non-blocking).
- Expert: Nygard, Hohpe.
- Issue: spec:68 splits only waits "longer than 5 minutes", into waits of at most 4 minutes. The Decisions row (spec:266) says 4 minutes "leaves a margin under the 5-minute heartbeat cadence". A 4:30 or 5:00 single call is not split, which removes the margin the Decisions row describes.
- Recommendation: make the trigger "longer than 4 minutes", the same figure as the target.
- Priority: Medium.

### F6. Fresh output directory versus known contract path, with no retry rule. MAJOR, Medium (non-blocking).
- Expert: Nygard, Fowler.
- Issue: WC-6 says a command "writes each run into a fresh output directory so a re-run starts clean" (spec:64). WC-4 says the contract is at `<output-dir>` "the directory the coordinator passed" (spec:62), and section 2.3 says the coordinator passes it (spec:73). Nothing says who creates the fresh directory on a retry (`worker-start --retry-of`, spec:64 cites CAPS:116).
- Attack: I can break this specification by **FR-2.4 Sequence Attack**. The invariant at spec:64 fails when the coordinator reuses the same `--output` on retry. Concrete attack: attempt 1 writes `<dir>/return-contract.yaml`, attempt 2 with the same `--output` overwrites it, and the first attempt's report is lost.
- Grading: a guess is needed about whether the coordinator or the command chooses the directory. Medium. If the brief template reuses the directory, this becomes data loss, which is blocking.
- Recommendation: state that the coordinator passes a new `--output` on every retry, and say what the command does if `--output` already holds a contract.
- Priority: High.

### F7. P0 step 4 cannot pass for the command the P0 run uses. MAJOR, Medium (non-blocking).
- Expert: Crispin, Adzic.
- Issue: 7.2 step 4 requires a YAML contract with `status` and `command` (spec:183). AC-0.4 then says "step 4 uses the command's existing report file, since the contract arrives in P1" (spec:194). `/sc:troubleshoot` writes `REPORT.md` (INV-B line 49, `report_path` REPORT.md), which is not YAML and has no `status` key. Step 4 as defined cannot pass, and AC-0.4 does not say what passes instead.
- Recommendation: define the P0 pass condition for a non-YAML report, or limit P0 to commands that already write a YAML contract (adversarial, brainstorm, workflow).
- Priority: High.

### F8. AC-2.2 depends on an optional path, so its outcome is not fixed. MAJOR, Medium (non-blocking).
- Expert: Adzic, Fowler.
- Issue: WC-3 lets the worker "instead ask the coordinator once" when a gate would be blocked (spec:61). AC-2.2 expects `worker_done --outcome failed` with `status: blocked` and no `agentWait` (spec:200). If the worker chooses `ask`, the run ends with an answer and possibly `succeeded`, so the acceptance outcome depends on a choice the spec leaves open.
- Recommendation: either make `ask` the only path for gates (drop the "may"), or state the AC-2.2 expected outcome for both paths.
- Priority: Medium.

### F9. Unattended run with no output directory. MAJOR, Medium (non-blocking).
- Expert: Cockburn, Fowler.
- Issue: WC-4 says "In unattended mode the command writes `<output-dir>/return-contract.yaml`" (spec:62), and most section 3.2 rows say to add an output path (for example spec:99, spec:107). No rule says what an unattended run without `--output` does (refuse, default path, or stop).
- Recommendation: add the refusal rule: without `--output`, the command writes nothing and reports `blocked`, as the spec-panel command already does for its own report directory.
- Priority: Medium.

### F10. AC-C5 misses removed blank lines and `---` lines. MAJOR, Medium (non-blocking).
- Expert: Crispin.
- Issue: AC-C5 (spec:176) uses `grep -E '^-[^-]'` to find removed lines. A removed blank line appears as `-` alone, and a removed `---` line appears as `----`. Both fail the filter. I ran the pattern on a probe diff that removed a blank line and a `---` line: nothing matched (exit 1). A removed YAML or frontmatter delimiter would then pass as "additive".
- Recommendation: use `grep -E '^-'` and exclude only the `---` file header (`grep -vE '^---( |$)'`), or check `git diff -U0 ... | grep -c '^-[^-]*$'` against the expected count.
- Priority: Medium.

### F11. The tasklist row contradicts INV-B and the nesting claim is not counted. MAJOR, Medium (non-blocking).
- Expert: Fowler, Newman.
- Issue: the 3.2 row for tasklist says no change, because "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit" (spec:122, citing INV-A:14). INV-B's tasklist verdict is needs-change: "the per-phase reflect fan-out must run at the worker's top level, not inside subagents" (INV-B:215). The spec does not record this disagreement in its Decisions (spec:255-269). The depth claim is also not counted: tasklist stage (depth 1), reflect's reviewers (depth 2), and reflect's Tier 3 path into `sc:workflow`, which runs reflect Wave 4 again (INV-B:52, workflow row), can reach depth 3 or more. INV-A:14 says the Agent tool is withheld at the limit. The reflect Tier 3 hand-off to `sc:workflow` is not in this workspace and is UNVERIFIED here.
- Recommendation: count the depth for each nested chain, or change the row to needs-change and record the decision.
- Priority: High.

### F12. P1 accepts `--unattended` on gated and outward commands before their behavior exists. MAJOR, Medium (non-blocking).
- Expert: Nygard, Fowler.
- Issue: P1 requires the flag on "every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (spec:159). Post-release, implement and pr-submit are in 3.2 (spec:113, 109, 114) and have gates and outward defaults that the spec moves to P4 (spec:162). For those commands the parenthetical does not license a no-op, so P1 leaves their behavior undefined. WC-9 says outward defaults are off under `--unattended` (spec:67).
- Recommendation: have P1 make `--unattended` fail fast for any command whose unattended behavior is not yet implemented, until its phase lands.
- Priority: Medium.

### F13. The `## Unattended mode` section sits in the command, but the gates sit in skills. MAJOR, Medium (non-blocking).
- Expert: Fowler, Newman.
- Issue: spec:52 says each changed command adds a short `## Unattended mode` section listing its gate resolutions. The gates the spec names are in the protocol skills (for example cli-eval W0 at SKILL.md:55-58 and auggie-review at SKILL.md:314-336, both cited by INV-A:74-98 and spec:104, 100). The spec does not say how `--unattended` reaches the skill, and AC-1.1 checks only the command files (spec:195: "every command in sections 3.1-3.2 has a `## Unattended mode` section").
- Recommendation: state the flag's propagation path into each skill, and add an acceptance check that a skill with a gate names the flag.
- Priority: High.

### F14. The pr-submit classification and the count of 27 assume the option the spec recommends against. MAJOR, Medium (non-blocking).
- Expert: Fowler, Adzic.
- Issue: the spec recommends D3 (a), coordinator or person only (spec:240), and says pr-submit "stays a worker candidate only if the user accepts open decision D3" (spec:139). Yet pr-submit is counted among the 27 "needs a change" commands (spec:94, 114) and the 10/27/6 split (spec:76) assumes it is a worker. Under the recommended option it is effectively coordinator-only, and the counts would be 10, 26, 7.
- Recommendation: state the counts for both D3 outcomes, or move pr-submit to section 4 under the recommended option.
- Priority: Medium.

### F15. The coordinator's duties do not cover a missing `worker_done`, an unanswered `ask`, or other `check` results. MAJOR, Medium (non-blocking).
- Expert: Nygard, Hohpe.
- Issue: section 2.3 says what the coordinator does after `worker_done` (spec:73). It does not say what it does when no `worker_done` arrives, when a worker stalls, when `check` returns something other than `consumer_fenced` (spec:70), or when an `ask` is never answered (WC-3, spec:61). The ask timeout default is UNVERIFIED (spec:281, item 10, CAPS:68).
- Attack: I can break this specification by **FR-2.4 Sequence Attack**. The invariant at spec:61 fails when the coordinator never replies. Concrete attack: the worker resumes its `ask` by message ID indefinitely, and no rule ends the wait or records a blocked outcome.
- Recommendation: add the coordinator's policy for each case, including a bound on the wait and a `blocked` record.
- Priority: High.

### F16. An absent `agentWait` field counts as a pass. MAJOR, Medium (non-blocking).
- Expert: Crispin, Nygard.
- Issue: 7.2 step 2 passes when "`observation.agentWait` is never non-null" (spec:181). Orca's guide says an absent field means it never looked (CAPS:129, `[H:worker-show]` line 16). An absent field therefore passes vacuously.
- Recommendation: require the field to be present and null at each observation.
- Priority: Medium.

=== ARCHITECTURE ANALYSIS (minor) ===

### F17. The return contract has no schema version. MINOR, non-blocking.
- Expert: Newman.
- Issue: WC-4 says the contract "carries at least" the listed fields (spec:62), and "Commands that already write a contract keep their fields and add the missing ones" (spec:62). With several writers, a version field would let the coordinator reject an unknown shape.
- Priority: Low.

### F18. The contract status and the Orca outcome are two sources of truth. MINOR, non-blocking.
- Expert: Hohpe.
- Issue: WC-5 requires the outcome to match the contract `status` (spec:63), but the only check of the match is in the test run (spec:182, step 3). Production coordinators "open the report file" (spec:73) and are not told to compare.
- Priority: Low.

## Follow-up candidates (Medium and minor)

These are not blocking and never fail the review. The session that ran the review asks the user once whether to open an issue for them. None has been created. The list is F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18.

## Reviser brief

Blocking finding ids: F1, F2.

Restated rule: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "the exact command line including `--unattended` and every flag section 3 lists as required", "anchor2": "Uses only the 10 ready commands, so the coordinator gets value before any command changes", "refs": ["2.3", "3.1", "P0", "P1"], "claim": "Section 2.3 requires --unattended in every Task brief, but P0 runs the ready commands before the flag exists, so P0 cannot satisfy both texts."}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "other", "anchor": "(orchestration\\|worktree\\|terminal\\|agent)", "refs": ["AC-C1", "SA-2", "WC-8"], "claim": "AC-C1 uses backslash-pipe under grep -E, which matches literal pipes, so the check never matches an Orca call and always passes."}
{"id": "F3", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "`--outcome succeeded` otherwise, including `partial`", "refs": ["WC-5"], "claim": "An empty or status-less contract falls into the otherwise clause and is reported as succeeded, which needs a guess about what counts as a report."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "must fall back on its own well inside the readiness limit", "refs": ["WC-1"], "claim": "The fallback has no numeric bound, so an implementer cannot tell whether a 50 s fallback is compliant."}
{"id": "F5", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "A command step that blocks a single tool call for longer than 5 minutes", "anchor2": "4 minutes leaves a margin under the 5-minute heartbeat cadence", "refs": ["WC-10", "Decisions"], "claim": "The split trigger is 5 minutes while the rationale wants 4 minutes of margin, so a 4:30 or 5:00 call is left unsplit."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "anchor2": "where `<output-dir>` is the directory the coordinator passed", "refs": ["WC-4", "WC-6", "2.3"], "claim": "A retry that reuses the coordinator's output directory overwrites the first attempt, and no rule says who makes the fresh directory."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "step 4 uses the command's existing report file, since the contract arrives in P1", "anchor2": "`test -s <contract>` and `uv run python -c", "refs": ["AC-0.4", "7.2"], "claim": "Step 4 requires YAML with status and command, which a REPORT.md from troubleshoot cannot satisfy, and AC-0.4 does not define the replacement pass condition."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "the session may instead ask the coordinator once with the preamble's `ask` command", "anchor2": "contract `status: blocked` with a non-empty `blocked_question`", "refs": ["WC-3", "AC-2.2"], "claim": "The optional ask path makes the AC-2.2 expected outcome depend on the worker's choice rather than on the spec."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "In unattended mode the command writes `<output-dir>/return-contract.yaml`", "refs": ["WC-4", "SA-3"], "claim": "No rule covers an unattended run that has no output directory, so the contract path is undefined for that case."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "grep -E '^-[^-]'", "refs": ["AC-C5", "SA-4"], "claim": "The diff filter misses removed blank lines and removed lines beginning with two dashes, so non-additive edits pass."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "runs one layer below the worker, inside Claude Code's nesting limit", "refs": ["3.2", "WC-7", "INV-B:215", "INV-A:14"], "claim": "The tasklist row keeps reflect fan-out in subagents against INV-B's needs-change verdict, and its depth is not counted against the three-layer limit."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "accepted by every command in sections 3.1 and 3.2", "refs": ["P1", "WC-9", "P4"], "claim": "P1 accepts the flag on gated and outward-default commands before their unattended behavior exists, so a P1 run can take outward actions."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Each changed command adds a short `## Unattended mode` section", "anchor2": "every command in sections 3.1-3.2 has a `## Unattended mode` section", "refs": ["SA-4", "AC-1.1"], "claim": "The flag does not reach the protocol skills where the gates live, and the acceptance check covers only the command files."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "stays a worker candidate only if the user accepts open decision D3", "anchor2": "**Coordinator or person only (recommended).**", "refs": ["D3", "3.2", "section 4"], "claim": "The 27-command count and the pr-submit row assume D3 option (b), while the spec recommends option (a), so the classification is not stable."}
{"id": "F15", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "After `worker_done`, the coordinator opens the report file", "anchor2": "On an `ask` timeout it resumes the same message ID", "refs": ["2.3", "WC-3", "WC-12"], "claim": "The coordinator has no policy for a missing worker_done, an unanswered ask, or a non-consumer_fenced check result, so a worker can wait indefinitely."}
{"id": "F16", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "`observation.agentWait` is never non-null", "refs": ["7.2", "CAPS:129"], "claim": "An absent agentWait field counts as a pass, though Orca's guide says absence means the field was never read."}
{"id": "F17", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "It follows the return-contract pattern several commands already use", "refs": ["WC-4"], "claim": "The contract has no schema version, so mixed writers cannot be told apart."}
{"id": "F18", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "The first sentence of the body states the report's status and verdict", "refs": ["WC-5", "7.2 step 3"], "claim": "The contract status and the Orca outcome are two sources of truth, and only the test run compares them."}
```

verdict: FAIL
