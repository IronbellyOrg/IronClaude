review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (first review)

- command: `/sc:spec-panel` (critique mode), focus `requirements,architecture`
- review rule: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, sandbox copy at `r1-t3-2/home/.claude/rules/prompts/document_review_loop_prompts.md`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: missing (first review, no `--baseline`); prior report: none
- reviewer: claude-haiku-5-5, one reviewer. `superclaude` is not on PATH, so `superclaude review panel resolve` and `superclaude review merge` were not run; this is the single-reviewer fallback the prompt allows.
- evidence read: `.dev/orca-command-refactor/README.md`, the spec, and the three inventories (`inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`). Every `INV-A`, `INV-B` and `CAPS` citation in the spec was checked against those files. Citations to `src/superclaude/`, `.dev/evals/`, `.dev/codegraph-migration/` and Orca's installed code are outside this workspace and are marked UNVERIFIED below.
- not run: `--unattended`, `--improve`, `--re-review`; no revised specification is written; the candidate was not edited.

## Coverage

- Requirements (Wiegers lead, Adzic, Cockburn): sections 0-9 and the acceptance checks in section 7.
- Architecture (Fowler lead, Newman, Hohpe, Nygard): sections 1, 2, 3, 5 and 6.
- Whittaker (always active, attacks on invariants): WC-4, WC-5 and WC-6, and the section 3 rows that set the flags.
- Mandatory artifacts: the Guard Condition Boundary Table is triggered (the spec contains conditional logic in WC-2 to WC-12 and section 3) and is given below. The Pipeline Dimensional Analysis is not triggered: the spec describes no multi-stage data flow in which counts change. The State Variable Registry is not triggered: the focus is not `correctness`.

## Summary

verdict: FAIL. Five findings are blocking (F1 to F5). Each of them is a stated text that an acceptance check cannot pass, or a pair of stated texts that contradict each other. Ten further findings are Medium or minor and are listed as follow-up candidates.

Quality scores (0-10): Clarity 6, Completeness 7, Testability 4, Consistency 5.

## Guard Condition Boundary Table (hard gate, complete)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | `specs/orca-worker-contract-spec.md:63` | Zero/Empty: no report | no report file | failed | `--outcome failed` when "no report exists" | OK |
| WC-5 outcome mapping | `specs/orca-worker-contract-spec.md:63` | One/Minimal: partial | `status: partial` | succeeded | "otherwise, including `partial`" | OK |
| WC-5 outcome mapping | `specs/orca-worker-contract-spec.md:63` | Typical: blocked | `status: blocked` | failed | "`--outcome failed` when the report says `failed` or `blocked`" | OK |
| WC-5 outcome mapping | `specs/orca-worker-contract-spec.md:63` | Legitimate Edge Case: status key absent or unlisted | `status` missing or `done` | succeeded, by the "otherwise" branch | not specified as a failure | GAP (F8) |
| WC-4 contract written | `specs/orca-worker-contract-spec.md:62` | Zero/Empty: stop before any output | no output directory yet | contract still written | "including stops before any other output exists" | OK |
| WC-4 path known before dispatch | `specs/orca-worker-contract-spec.md:62`, `:92` | Sentinel: workflow package id | `<id>` generated per run | path not known before dispatch | WC-4 requires it known before dispatch | GAP (F4) |
| WC-6 re-run uses fresh directory | `specs/orca-worker-contract-spec.md:64` | Maximum/Overflow: `--retry-of` with the same brief | first-attempt output present | either a per-run subdirectory (path unknown) or the same directory (overwrite) | "writes each run into a fresh output directory", owner not named | GAP (F5) |
| WC-3 ask then resume | `specs/orca-worker-contract-spec.md:61` | Sequence: answer arrives after a blocked report | blocked contract on disk | resume or re-invoke | flag name and outcome not specified | GAP (F7) |
| WC-10 single tool-call size | `specs/orca-worker-contract-spec.md:68` | Boundary: 240 s against the 300 s heartbeat | pr-submit iteration at or over 240 s | split required | split to waits of at most 4 minutes; overrun not specified | GAP (F11) |
| WC-11 parallel-safe default path | `specs/orca-worker-contract-spec.md:69` | Typical: index-repo with no output flag | fixed `PROJECT_INDEX.md` | shared file in one worktree | "Default output paths carry a timestamp or the slug" | GAP (F15) |
| cli-eval run gate | `specs/orca-worker-contract-spec.md:104` | Zero/Empty: `--suite` given, safety flags absent | no safety flags | blocked | "the safety flags" not defined | GAP (F9) |
| auggie-review posting gate | `specs/orca-worker-contract-spec.md:100` | Sentinel: `--post-pr` in brief | flag not in `inventory/commands-a.md:38` | posting enabled | new flag, not in the change column | GAP (F10) |
| WC-2 gate blocked | `specs/orca-worker-contract-spec.md:60` | Legitimate Edge Case: gate with no preamble | no ask possible | blocked, stop | "writes its report with `status: blocked`... and stops" | OK |
| WC-12 ownership lost | `specs/orca-worker-contract-spec.md:70` | Typical: check returns `consumer_fenced` | ownership lost | stop, no `worker_done` | specified | OK |

Every cell is populated. FR-9 (blank behaviour) generates no finding. Each GAP maps to a finding above.

## Requirements analysis

=== REQUIREMENTS ANALYSIS ===

**F1 (CRITICAL, blocking). AC-1.1 cannot pass at P1.** `specs/orca-worker-contract-spec.md:195` requires that "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`". Section 2.1 (`:52`) and section 3 (`:76`) say only *changed* commands gain the section. In section 3, brainstorm (`:84`), init-lite (`:87`) and tdd (`:90`) have no change or are deferred to P2, and release-split (`:89`) is deferred to P2. At P1 the test therefore fails for those commands. Expert: Adzic (testability), Wiegers. Recommendation: scope AC-1.1 to the commands each phase edits, or require the section on every 3.1-3.2 command in the phase that first touches it. Priority: High. Quality impact: high; the P1 gate is unpassable as written.

**F2 (CRITICAL, blocking). AC-0.4 step 4 cannot pass for `/sc:troubleshoot`.** `specs/orca-worker-contract-spec.md:194` says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file". Step 4 (`:183`) asserts that the file parses as YAML with `status` and `command` keys. `/sc:troubleshoot` writes `REPORT.md`, and `inventory/commands-b.md:242` says its return contract is written "only when `--caller task-unified`". The pass condition gives no replacement check for a markdown report. Expert: Adzic, Cockburn (acceptance). Recommendation: define step 4 for existing reports (for example, "file exists and is non-empty") or pass `--caller task-unified` in the P0 brief. Priority: High. Quality impact: high; the P0 gate is ambiguous.

**F3 (CRITICAL, blocking). The P0 brief contradicts section 2.3.** `specs/orca-worker-contract-spec.md:73` says each brief states "the exact command line including `--unattended`". Section 3.1 (`:79` to `:81`) and P0 (`:158`) run the ready commands before any of them accepts `--unattended`, which P1 adds (`:159`). Section 3.1's "Brief must pass" column does not list `--unattended`. Following section 2.3 in P0 passes a flag the command does not yet define, so the P0 smoke runs no longer test the brief the spec defines. Expert: Cockburn (actor and goal), Hohpe (message contract). Recommendation: either state that P0 briefs omit `--unattended`, or move the P0 smoke runs after P1. Priority: High. Quality impact: high.

**F6 (MAJOR, Medium, not blocking). AC-C1 cannot fail.** `specs/orca-worker-contract-spec.md:172` uses `\|` inside an ERE group (`grep -E`), so the pattern matches only a literal `|`. Checked in the sandbox: `echo 'orca orchestration ask' | grep -E ...` exits 1, and only the literal string `orca orchestration|worktree` matches. The common check therefore passes on any command file, and SA-2 (`:147`) is not enforced. Expert: Wiegers (testability). Recommendation: use `\(orchestration|worktree|terminal|agent\)` with `grep -E`, and add a positive fixture that must fail. Priority: High. Quality impact: high, because it is the only mechanical guard for SA-2.

**F7 (MAJOR, Medium, not blocking). WC-3's resume path is undefined.** `specs/orca-worker-contract-spec.md:61` says the session "may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag". It does not name the flag, say whether the blocked contract is replaced, or say which `worker_done` outcome is sent after the resumed run. Under WC-5 (`:63`) the first blocked report already maps to `failed`. Expert: Hohpe (message contract), Nygard (failure path). Recommendation: name the flag and state that the final contract replaces the blocked one before `worker_done`. Priority: Medium. Quality impact: medium.

**F8 (MAJOR, Medium, not blocking). WC-5 maps a missing or unlisted status to success.** `specs/orca-worker-contract-spec.md:63` gives failure for `failed` and `blocked` and a missing report, then "`--outcome succeeded` otherwise, including `partial`". A contract with no `status` key, or with a typo, is sent as succeeded. Expert: Nygard, Whittaker (Divergence attack, FR-2.2). Recommendation: map an absent or unlisted status to failed. Priority: High. Quality impact: medium.

**F9 (MAJOR, Medium, not blocking). The cli-eval run gate uses an undefined term.** `specs/orca-worker-contract-spec.md:104` says `run` "requires `--suite` and the safety flags in the brief, else blocked". "The safety flags" is not defined in section 3, `inventory/commands-b.md` does not list them, and AC-2.2 (`:200`) does not test them. Expert: Wiegers (requirements). Recommendation: list the flags by name. Priority: Medium. Quality impact: medium.

**F10 (MAJOR, Medium, not blocking). The auggie-review change is incomplete.** `specs/orca-worker-contract-spec.md:100` says "posting returns only with an explicit `--post-pr` in the brief". `inventory/commands-a.md:38` shows only `--no-post-pr` and `--no-remediation-offer`. The row's "Other required change" column says "none", so the new flag is not in the change list. AC-2.4 (`:202`) depends on it. Expert: Wiegers (traceability). Recommendation: add the flag to the change column and to P2. Priority: Medium. Quality impact: medium.

**F11 (MAJOR, Medium, not blocking). The pr-submit wait rule has no overrun behaviour.** `specs/orca-worker-contract-spec.md:114` says to "confirm each single iteration (poll script runtime plus sleep) stays under 4 minutes", with the runtime listed as UNVERIFIED (`:283`). AC-4.3 (`:210`) requires that no tool call exceeds 240 s, but nothing says what happens when one does. Expert: Nygard (failure modes). Recommendation: state the action on overrun (split the poll, or end `blocked`). Priority: Medium. Quality impact: medium.

**F15 (MAJOR, Medium, not blocking). index-repo stays "ready" with a fixed output path.** `specs/orca-worker-contract-spec.md:86` keeps index-repo ready with only a location fix. Its default output is a fixed `PROJECT_INDEX.md` (`inventory/commands-a.md:53`). WC-11 (`:69`) says "Default output paths carry a timestamp or the slug the coordinator passes". Two workers in one worktree would write the same file. Expert: Wiegers (consistency), Newman (shared state). Recommendation: make the output a brief-supplied path, or change the verdict. Priority: Medium. Quality impact: medium.

=== END REQUIREMENTS ANALYSIS ===

## Architecture analysis

=== ARCHITECTURE ANALYSIS ===

**F4 (CRITICAL, blocking). The workflow report path is not known before dispatch.** WC-4 (`specs/orca-worker-contract-spec.md:62`) says the contract is at `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed", and section 2.3 (`:73`) says the report path "is known before dispatch". The workflow row (`:92`) gives `.dev/tasks/to-do/<id>/return-contract.yaml`, and `inventory/commands-b.md:273` says the package is never reused, so `<id>` is generated per run. The coordinator cannot open the contract as WC-4 requires. Expert: Fowler (interface), Newman (contract evolution). Recommendation: give `/sc:workflow` an explicit `--output` in P1, or record the exception in WC-4. Priority: High. Quality impact: high.

**F5 (CRITICAL, blocking). WC-6's fresh directory conflicts with WC-4's known path.** `specs/orca-worker-contract-spec.md:64` says a command "writes each run into a fresh output directory so a re-run starts clean". Section 2.3 (`:73`) has the coordinator supply the directory and makes the path known before dispatch. The two readings conflict: if the command creates a fresh subdirectory per run, the WC-4 path is not known before dispatch; if the coordinator reuses `--output` on retry, the first attempt's output is overwritten. Expert: Whittaker (Sequence attack, FR-2.4), Fowler. Recommendation: state that the coordinator passes a new `--output` for each attempt and that WC-6 means the command never reuses a directory it did not create. Priority: High. Quality impact: high (possible loss of the first attempt's output).

**F12 (MAJOR, Medium, not blocking). R1 is stated more firmly than its evidence.** `specs/orca-worker-contract-spec.md:33` says a command that calls `worker-start` "would be refused with `nested_worker_depth_exceeded`". The same row says call-site enforcement was not traced, and UNVERIFIED item 5 (`:276`) says the same. The rejection of the alternative rests on an unchecked claim. Expert: Fowler, Hohpe. Recommendation: write "is expected to be refused (UNVERIFIED, item 5)". Priority: Low. Quality impact: low.

**F13 (MAJOR, Medium, not blocking). E3 is evidence for the route the spec forbids.** `specs/orca-worker-contract-spec.md:23` cites the codegraph run as proof that the direct route works. Section 1.4 gap 1 (`:43`) says that run's brief used Agent-tool subagents, which WC-7 (`:65`) forbids. The evidence supports the nested route, not the direct one. The UNVERIFIED citation `.dev/codegraph-migration/orchestration/README.md:31` could not be read from the workspace. Expert: Fowler (decision evidence). Recommendation: rewrite E3 as "shows that Orca workers can run commands, by the nested route only". Priority: Medium. Quality impact: medium.

**F14 (MAJOR, Medium, not blocking). The tasklist nesting claim is settled too early.** `specs/orca-worker-contract-spec.md:122` says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit". `inventory/commands-b.md:210` and UNVERIFIED item 1 (`:314`) say subagent-in-agent nesting is unverified, and `inventory/commands-a.md:112` says Agent and MCP tools in nested subagents are unverified. Stage 10.5 of tasklist runs reflect inside subagents, which is two layers below the worker. Expert: Nygard (failure mode), Newman. Recommendation: list this under UNVERIFIED and gate Stage 10.5 on AC-0.4-style evidence. Priority: Medium. Quality impact: medium.

=== END ARCHITECTURE ANALYSIS ===

## Adversarial analysis (Whittaker, always active)

- I can break this specification by **Sequence Attack (FR-2.4)**. The invariant at **WC-6 (`specs/orca-worker-contract-spec.md:64`)** fails when **a retry is started with `--retry-of` and the same brief**. Concrete attack: the first dispatch writes partial output and `return-contract.yaml` into `<output-dir>`; the retry receives the same `<output-dir>` from section 2.3 and overwrites both. Before: first-attempt output present. After: only the retry's output remains. Finding F5.
- I can break this specification by **Divergence Attack (FR-2.2)**. The invariant at **WC-5 (`:63`)** fails when **the contract has no `status` key**. Concrete attack: the command writes a contract without `status`; the "otherwise" branch sends `--outcome succeeded`, and the coordinator accepts unverified work. Finding F8.
- I can break this specification by **Zero/Empty Attack (FR-2.1)**. The invariant at **WC-4 (`:62`)** fails when **the command stops before writing anything and the coordinator has passed no `--output`**. The spec requires the contract "including stops before any other output exists", but with no output directory the path is undefined. This is a gap in the coordinator brief, not a separate finding; it is covered by F4 and F5.

## Follow-up candidates (Medium and minor, not blocking)

These do not change the verdict. The session that ran the review asks the user once whether to open an issue for them; this run creates none. Under `--unattended` they are only recorded.

- F6 (AC-C1 grep never matches), F7 (WC-3 resume path), F8 (WC-5 default success), F9 (cli-eval safety flags), F10 (auggie `--post-pr`), F11 (pr-submit overrun), F12 (R1 wording), F13 (E3 evidence), F14 (tasklist nesting), F15 (index-repo output path).
- Minor note 1: `.dev/orca-command-refactor/README.md:13` says the review goes to `review/spec-panel.md`. The brief for this run says `review/round1.md`. This report follows the brief.
- Minor note 2: section 1.2 E5 (`:25`) greps `src/superclaude/{commands,skills,core,agents}` and not the `plugins/superclaude/` mirror. Section 6 (P0) adds the mirror update, so this does not change a verdict.
- Minor note 3: many citations in the spec point outside this workspace (`src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, Orca's installed code). I could not check them and mark them UNVERIFIED. Every `INV-A`, `INV-B` and `CAPS` citation I checked matched its inventory line (for example `CAPS:92`, `CAPS:161`, `INV-A:76-83`, `INV-B:242`, `INV-B:323`).

## Reviser brief

Blocking ids: F1, F2, F3, F4, F5.

Restated bullet 6 of the review loop: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id.

Medium and minor findings (F6 to F15) are not part of this brief. The reviser must not edit them.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "unpassable-check", "anchor": "every command in sections 3.1-3.2 has a", "refs": ["AC-1.1", "2.1", "3", "3.1", "3.2", "6"], "claim": "AC-1.1 at P1 requires an Unattended section in every 3.1-3.2 command, but brainstorm, init-lite, tdd and release-split get none in P1, so the P1 check cannot pass."}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "unpassable-check", "anchor": "step 4 uses the command's existing report file", "refs": ["AC-0.4", "7.2", "6"], "claim": "AC-0.4 step 4 asserts YAML keys status and command, but /sc:troubleshoot without --caller task-unified writes only REPORT.md, and the pass condition gives no replacement check, so the P0 gate cannot pass for that command."}
{"id": "F3", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "the exact command line including `--unattended`", "anchor2": "run three ready commands as real Orca workers, invoked directly", "refs": ["2.3", "3.1", "6", "AC-0.4"], "claim": "Section 2.3 requires every brief to carry --unattended, but the P0 smoke runs use ready commands whose briefs omit it and whose commands do not accept it until P1."}
{"id": "F4", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "is the directory the coordinator passed", "anchor2": "`.dev/tasks/to-do/<id>/return-contract.yaml`", "refs": ["WC-4", "2.3", "3.1"], "claim": "WC-4 requires the contract path to be known before dispatch, but the section 3.1 workflow row gives a per-run <id> path, so the coordinator cannot open the report as section 2.3 requires."}
{"id": "F5", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "anchor2": "is the directory the coordinator passed", "refs": ["WC-4", "WC-6", "2.3"], "claim": "WC-6 has the command write a re-run into a fresh directory, which makes the WC-4 path unknown before dispatch; if the coordinator reuses --output on retry, the first attempt's output is overwritten."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "(orchestration\\|worktree\\|terminal\\|agent)", "refs": ["AC-C1", "SA-2", "WC-8"], "claim": "The AC-C1 grep never matches a real orca orchestration line and matches only a literal pipe, so the common check passes whatever the commands contain and SA-2 is not enforced."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "re-invoke or resume the command with the answer as a flag", "refs": ["WC-2", "WC-3", "WC-5", "D2"], "claim": "WC-3 does not name the flag carrying the answer, whether the blocked contract is replaced, or which outcome is sent after the resumed run, so implementers would send different worker_done outcomes."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "`--outcome succeeded` otherwise, including `partial`", "refs": ["WC-5", "WC-4"], "claim": "A contract with no status key or an unlisted value falls into the otherwise branch and is sent as succeeded, so a malformed report reaches the coordinator as a success."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "requires `--suite` and the safety flags in the brief, else blocked", "refs": ["3.2", "cli-eval", "WC-2", "AC-2.2"], "claim": "The safety flags are not defined anywhere in the spec, so the cli-eval run gate cannot be implemented or tested as written."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "posting returns only with an explicit `--post-pr` in the brief", "refs": ["WC-9", "3.2", "AC-2.4"], "claim": "The auggie-review row requires a --post-pr flag that INV-A:38 does not show, while its Other-required-change column says none, so the P2 change list is incomplete."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "confirm each single iteration (poll script runtime plus sleep) stays under 4 minutes", "refs": ["WC-10", "AC-4.3", "UNVERIFIED 12"], "claim": "The spec defines no behaviour when a pr-submit iteration reaches 4 minutes, and AC-4.3 then fails with no recovery step."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "would be refused with `nested_worker_depth_exceeded`", "refs": ["1.3", "R1", "UNVERIFIED 5"], "claim": "R1 states as fact that a nested worker-start is refused, but UNVERIFIED item 5 says call-site enforcement was not traced, so the rejection rests on an unchecked claim."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Orca workers invoked `/sc:adversarial`, and that work landed as PR #329", "refs": ["E3", "1.4", "WC-7"], "claim": "E3 is offered as evidence for the direct route, but section 1.4 gap 1 says the cited run used Agent-tool subagents, which WC-7 forbids, so the evidence supports the rejected route."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "its reflect fan-out runs one layer below the worker", "refs": ["3.2", "tasklist", "WC-7", "UNVERIFIED 1"], "claim": "The tasklist row states that the reflect fan-out is inside the nesting limit, but the inventories mark subagent-in-agent nesting and nested Agent and MCP tools as unverified."}
{"id": "F15", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Default output paths carry a timestamp or the slug the coordinator passes", "refs": ["WC-11", "3.1", "index-repo"], "claim": "index-repo's default PROJECT_INDEX.md is a fixed path that section 3.1 keeps ready with only a location fix, so two workers in one worktree write the same file, which WC-11 forbids."}
```

Reviser brief (blocking ids F1, F2, F3, F4, F5): see the section above; the reviser reads this report, not the command.

verdict: FAIL
