review: 1 of 3

# Spec panel critique, round 1: orca-worker-contract-spec.md

## Report header

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- Candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review; no `--re-review`, no `--baseline`)
- Prompt: FIRST-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full)
- Mode and focus: `--mode critique`, `--focus requirements,architecture`
- Review number: 1 of 3; fix cycles so far: 0
- Reviewer model: claude-haiku-5-5, single reviewer. The `superclaude` CLI is not installed in this sandbox, so `superclaude review panel resolve` and `superclaude review merge` were not run. This is stated again in the loop summary.
- Candidate edited: no. Only this file was written.
- Verdict: FAIL. Five blocking findings are open (F1 to F5).

## Scope and evidence

- Read in full: `command.md` (the `/sc:spec-panel` definition), `.dev/orca-command-refactor/README.md`, the candidate spec, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, and the FIRST-REVIEW prompt. Also read `command.md:22-23` and `command.md:455-465` (the command's own usage and unattended section).
- Checkable here: the candidate and the three inventories under `.dev/orca-command-refactor/`. Every quote used in a finding was matched verbatim in the candidate (`grep -F`), and each inventory line cited was read.
- UNVERIFIED in this review: every citation to `src/superclaude/`, `~/.claude/`, `/opt/Orca/`, `.dev/evals/`, `.dev/codegraph-migration/`, `CLAUDE.md`, `pyproject.toml` and `EVIDENCE.md`. None of those files is in this workspace, so I did not treat them as checked. Where the inventories quote them (for example `CAPS:44`, `CAPS:49`), I cite the inventory line.
- Covered: all 11 sections of the candidate (§1 decision and evidence, §2 worker contract WC-1 to WC-12, §3 per-command changes, §4 coordinator-only, §5 standalone rules SA-1 to SA-6, §6 phases, §7 acceptance checks, §8 non-goals, §9 decisions D1 to D5, the Decisions table, UNVERIFIED list), the 10/27/6 command split against both inventories, and the cross-references between §3, §7 and the inventories.
- Not covered: whether any Orca or IronClaude behaviour is true as stated. Nothing was run; the sandbox has no Orca and no repository.

## Mandatory output artifacts

- Guard Condition Boundary Table: triggered (the candidate has conditional rules and thresholds in §2.2 and §7.2). Produced below.
- Pipeline Dimensional Analysis: not triggered. The candidate describes coordination and file contracts. No stage changes an item count (WC-5 maps status values, not counts), so no Quantity Flow Diagram is required.
- State Variable Registry: not required, because the focus is not `correctness`.
- Advisory: the candidate has mutable state (Task and Dispatch status, the contract `status`, the ask message ID) and numeric thresholds (60 s, 4 min, 5 min). A later round with `--focus correctness` would be useful. This is advisory only.

## Expert panel

Lead experts: Wiegers, Adzic and Cockburn (requirements); Fowler, Newman, Hohpe and Nygard (architecture). Whittaker is active in every panel review and is reported under the adversarial heading.

Grading applied: each blocking finding has the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" in its claim. Findings whose sentence needs an extra assumption, or that describe a requirement the candidate never states, are Medium and listed under follow-up candidates.

---

=== REQUIREMENTS ANALYSIS ===

### F1. BLOCKING. MAJOR. unpassable-check. Expert: Adzic (acceptance checks)

- Issue: The P0 gate cannot pass as written. AC-0.4 (`specs/orca-worker-contract-spec.md:194`) runs `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial` directly, and requires steps 1-3 and 5-7 to pass. Step 3 (`:182`) requires the report path to be "the WC-4 contract path". WC-4 (`:62`) writes that contract only in unattended mode, and `--unattended` does not exist until P1 (`:159`). §3.1 (`:83`, `:91`, `:92`) lists the brief flags without `--unattended`. Step 4 (`:183`) then parses a YAML file with `d['status']`, but AC-0.4 allows `REPORT.md`, a markdown file, in its place (`:194`).
- Sentence: an implementer who runs AC-0.4 as written on `/sc:troubleshoot` gets a `worker_done` whose report is `REPORT.md`, which fails step 3's contract-path condition and step 4's YAML parse, so the P0 gate that decides evidence gap 1.4(1) can never pass.
- Recommendation: state how P0 checks the report without a contract (for example, step 3 checks that the report path equals the command's documented report, and step 4 is skipped for P0). Alternatively, move the live smoke runs to P1, after the flag exists. Also correct §2.3 (`:73`), which requires `--unattended` in every Task brief, so that it does not apply to P0.
- Priority: High. Quality impact: high (Phase 0 cannot close).

### F2. BLOCKING. MAJOR. data-loss. Expert: Nygard (failure modes)

- Issue: WC-6 (`:64`) requires that a retry must not corrupt the first attempt's output, and that a command either resumes or writes each run into a fresh output directory. The init-lite row (`:87`) has no resume flag and says "Re-run overwrites its marked report", with "None" as the required change. Its input is `--output <file>`, and §3.1 says the report lives at `.dev/superclaude/context-audit.md` or `--output`.
- Sentence: an implementer who follows §3.1 leaves init-lite unchanged, and a `--retry-of` attempt overwrites the first attempt's report at the same `--output` path, which WC-6 forbids and which loses the first attempt's output.
- Recommendation: give init-lite a fresh output path per run, or add a resume rule, and name the change in the row. The same row should be checked against WC-6 for the other fixed-path commands (see F7).
- Priority: High.

### F3. BLOCKING. MAJOR. contradiction. Expert: Fowler (interfaces)

- Issue: WC-4 (`:62`) defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)". But §3.1 passes `--output <file>` for tdd (`:90`), and the TDD is the file named by `--output` (`inventory/commands-b.md:222`). init-lite (`:87`) also uses a file. The spec-panel row adds `--output` (`:120`), and the command definition makes `--output` file-valued (`command.md:23`, `command.md:460`).
- Sentence: an implementer who follows WC-4 for `/sc:tdd --output <file>` writes the contract to `<file>/return-contract.yaml`, which cannot be created, so `worker_done --report-path` has no valid contract to point at.
- Recommendation: define where the contract goes for file-valued `--output` (for example, beside the file, or in a separate `--contract-dir`), and list the choice per command in §3.
- Priority: High.

### F4. BLOCKING. MAJOR. safety. Expert: Wiegers (rule conflict); safety rule from Decision D2

- Issue: WC-2 (`:60`) lists three ways a gate resolves: default, flag, or blocked. WC-3 (`:61`) adds a fourth: when a gate would resolve as blocked, the session "may instead ask the coordinator once", then "re-invoke or resume the command with the answer as a flag". Nothing in WC-3 excludes the Ruling gate. The implement row (`:109`) keeps the Ruling rule, and D2(a) (`:234`) says the worker stops and a person gives the Ruling. The Ruling rule says another agent's message is not acceptance (`inventory/commands-a.md:66`, quoting `refs/qa.md:238`).
- Sentence: an implementer who follows WC-3 at the implement E-HALT-QA gate sends the Ruling question through `ask`, receives the coordinator's reply, and re-invokes implement with that reply as the answer, so an agent's message is recorded as the Ruling.
- Recommendation: exclude Ruling gates from WC-3 (state that a blocked Ruling always stops with `failed`, as D2(a) recommends), or make the relayed-Ruling route an explicit D2(b) choice. Add the fourth resolution to WC-2 so the list is complete.
- Priority: High. Safety boundary.

### F5. BLOCKING. MAJOR. unpassable-check. Expert: Adzic (acceptance checks)

- Issue: §2.1 (`:52`) says "Each changed command adds a short `## Unattended mode` section". §3.1 brainstorm (`:84`) has "Small fix: None", so it is not changed. AC-1.1 (`:195`) requires the section in every command of §3.1-3.2.
- Sentence: an implementer who follows §2.1 and the brainstorm row does not add the section, and AC-1.1 then fails for brainstorm, so AC-1.1 cannot pass as written.
- Recommendation: add the section to brainstorm. Its gate behaviour (auto-proceed, `inventory/commands-a.md:39`) must be documented under WC-2 anyway. Or change AC-1.1 to cover only changed commands. The first option is the better fit with WC-2.
- Priority: High (cheap fix).

### F6. MEDIUM (follow-up). MAJOR label. missing-requirement. Expert: Wiegers (measurability)

- Issue: WC-1 (`:59`) says a prompt must fall back "well inside the readiness limit (default 60 s)". The spec gives no number. Its own evidence says a 30 s fallback passed and a fallback above about 45 s failed again (`inventory/orca-capabilities.md:49`, quoting `EVIDENCE.md:45,56`). A fallback at 50 s is "inside" 60 s but fails on that evidence.
- Recommendation: state a numeric fallback (for example, 30 s) and the readiness budget used in §7.2 step 1.

### F7. MEDIUM (follow-up). MAJOR label. missing-requirement. Expert: Wiegers, Hohpe

- Issue: WC-11 (`:69`) says default output paths "carry a timestamp or the slug the coordinator passes". cleanup-audit (`:85`), index-repo (`:86`) and init-lite (`:87`) keep fixed paths. The cleanup-audit row relies on "one audit per worktree at a time (WC-11)", but WC-11 states no such serialisation rule.
- Recommendation: state the serialisation rule in WC-11, or require a slug for these commands, and carry it into the §2.3 brief.

### F8. MEDIUM (follow-up). MAJOR label. contradiction. Expert: Hohpe (message contracts)

- Issue: §2.3 (`:73`) says "the report path is known before dispatch (WC-4)". research (`:116`) names "the generated `claudedocs/research_*.md` path", which is set at run time (`inventory/commands-b.md:132`). workflow (`:92`) writes its contract under `.dev/tasks/to-do/<id>/`, and it does not write one for pre-creation STOPs (`inventory/commands-b.md:272`). The row (`:92`) says "Write the contract for pre-creation STOPs too", but gives no path for that case.
- Recommendation: give research and workflow an explicit `--output`, and name the location for a pre-creation STOP.

### F9. MEDIUM (follow-up). MAJOR label. missing-requirement. Expert: Whittaker (FR-2.1, see adversarial section)

- Issue: WC-5 (`:63`) maps every status other than `failed` or `blocked` to `--outcome succeeded` ("otherwise, including `partial`"). WC-4 (`:62`) fixes four status values, but states no rule for a contract whose status is missing or outside those values.
- Recommendation: map a missing or unknown status to `failed`, and state that the coordinator treats it as a contract error.

### F10. MEDIUM (follow-up). MAJOR label. missing-requirement. Expert: Hohpe, Whittaker (FR-2.4)

- Issue: WC-4 (`:62`) says the contract is written on every outcome and passed to `worker_done`, but gives no order. §2.3 (`:73`) says the coordinator reads the file after `worker_done`. `worker_done` settles the Task automatically and the worker then idles (`inventory/orca-capabilities.md:77-78`).
- Recommendation: state that the contract is written and closed before `worker_done` is sent, and that the coordinator treats a missing file as `failed`.

### F18. MINOR. contradiction. Expert: Wiegers

- Issue: reflect is "ready today" (§3.1, `:88`), but the same row needs a P2 change (`--unattended` must follow the headless auto-accept rule).
- Recommendation: move reflect to needs-change, or say that it is ready only without `--unattended`.

---

=== ARCHITECTURE ANALYSIS ===

### F11. MEDIUM (follow-up). MAJOR label. missing-requirement. Expert: Nygard (failure modes)

- Issue: WC-3 (`:61`) resumes the same `ask` message ID after each timeout, with no cap. §7.2 step 2 (`:181`) fails a run when `observation.agentWait` is non-null, but says nothing about what the coordinator then does. §7.2 step 3 (`:182`) waits for `worker_done` with a 900000 ms budget and has no timeout branch. Whether Orca bounds a Dispatch's run time is UNVERIFIED (`inventory/orca-capabilities.md:188`).
- Recommendation: cap the ask retries, and define the coordinator's action for a parked worker and for a `check --wait` timeout, pointing to the liveness and attention rules quoted in the capabilities inventory (`inventory/orca-capabilities.md:120-131`).

### F12. MEDIUM (follow-up). MAJOR label. missing-requirement. Expert: Newman (service boundary)

- Issue: §2.1 (`:52`) says the contract is "installed to `~/.claude/WORKER-CONTRACT.md`". The spec does not say what an unattended command does when that file is missing, for example after `superclaude install` was run before this change. AC-0.1 (`:191`) checks only the repository's `KNOWN_CORE_FILES`.
- Recommendation: state the failure behaviour (for example, `status: blocked` with an install instruction), and add a check for it.

### F13. MEDIUM (follow-up). MAJOR label. contradiction. Expert: Fowler

- Issue: The spec-panel row (`:120`) says "add `--output`; contract", and `inventory/commands-b.md:182` says no `--output` flag exists (citing `cmd/spec-panel.md:22`). The command definition in this sandbox already has `--output <file>` (`command.md:23`), a `--report-dir <dir>` flag (`command.md:23`, `command.md:460`), an `## Unattended mode` section (`command.md:455-465`), and a reference to `~/.claude/WORKER-CONTRACT.md` (`command.md:457`). WC-4 names the directory flag `--output-dir`, which differs from `--report-dir`.
- Note: it is UNVERIFIED whether the sandbox `command.md` is the same as the repository's `src/superclaude/commands/spec-panel.md`, which is not in the workspace.
- Recommendation: re-check the spec-panel row against the current command file, and use one directory flag name in WC-4.

### F14. MEDIUM (follow-up). MAJOR label. missing-requirement. Expert: Wiegers

- Issue: Stage 10.5 of tasklist has a HALT on `needs_human_decision` items (`inventory/commands-b.md:209`). The tasklist row (`:122`) resolves only "passes `--unattended` to each reflect". WC-2 (`:60`) says every gate is listed per command in §3, and this one is not.
- Recommendation: list the HALT and give its (a), (b) or (c) resolution.

### F15. MEDIUM (follow-up). MAJOR label. other. Expert: Nygard, Newman (nesting)

- Issue: The tasklist row (`:122`) says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit", citing `INV-A:14`. The spec does not count the layers. Stage 10.5 subagents (layer 1) run reflect Tier 2 reviewers (layer 2), and the adversarial merge under reflect may reach layer 3 or deeper. `inventory/commands-a.md:14` says that at the depth limit the Agent tool is withheld, so the fan-out would fail without an error. The inventory summary also lists this as a required change, "Remove a nested fan-out ... that runs inside subagents" (`inventory/commands-b.md:295`), and the spec drops it with no entry in Decisions.
- Recommendation: count the layers and record the decision, or change Stage 10.5 so the reflect fan-out runs at the worker's top level.

### F16. MEDIUM (follow-up). MAJOR label. contradiction. Expert: Fowler (scope)

- Issue: §1.1 (`:16`) says "What changes in the commands is limited to the worker contract in section 2". §2.1 (`:51`) says the unattended mode is "the only command-side change the contract asks for besides report files and resume". §3.2 contradicts both: for example, the roadmap row (`:118`) requires "reconcile the flag surface the command calls unsupported with the flags the skill still defines", and several other rows add tools or fix frontmatter. SA-4 (`:149`) calls these defect fixes.
- Recommendation: state the scope as "the contract, plus the named defect fixes in SA-4" in §1.1 and §2.1.

### F17. MEDIUM (follow-up). MAJOR label. unpassable-check. Expert: Newman, Fowler (boundaries)

- Issue: AC-C1 (`:172`) scans `src/superclaude/core`. P0 adds an Orca section to `HOW-WE-WORK.md` and the new `WORKER-CONTRACT.md` in that directory (`:158`). SA-2 (`:147`) allows an Orca mention "inside the contract file" for changed commands. AC-C1 has no exemption for either file, and its only filter excludes `ccsession-tag`.
- Sentence: an implementer who writes the contract as SA-2 allows, or writes the routing-guide Orca section that SA-5 requires, fails AC-C1 in P0, so the every-phase check cannot pass.
- Recommendation: limit AC-C1 to commands, skills and agents, or name the two files as exemptions.

### F19. MINOR. other. Expert: Wiegers (evidence wording)

- Issue: §1.2 E4 (`:24`) states as evidence that Agent-tool subagents "are not counted by Orca's nesting limit". The inventory says only that no such limit was found and marks the point UNVERIFIED (`inventory/orca-capabilities.md:155`).
- Recommendation: change the wording to "no limit found (UNVERIFIED)".

### F20. MINOR. other. Expert: Wiegers (verifiability)

- Issue: §2 cites many locations outside this workspace (see the scope note). The candidate says at `:11` that 11 locations were re-read on 2026-11-02, which this review could not check.
- Recommendation: keep the statement, and have the coordinator check those citations in a later round.

---

=== ADVERSARIAL ANALYSIS (James Whittaker, FR-3 format) ===

- I can break this specification by **FR-2.1 Zero/Empty Attack**. The invariant at **WC-5 (`specs/orca-worker-contract-spec.md:63`)** fails when **the contract's `status` is missing, empty, or outside the four values**. Concrete attack: **before: a worker writes `status: "done"`; after: WC-5 maps "otherwise" to `--outcome succeeded`, so a failed run is reported as success.** Severity: MAJOR (ambiguous under attack). See F9.
- I can break this specification by **FR-2.4 Sequence Attack**. The invariant at **WC-4 (`:62`)** fails when **`worker_done` is sent before the contract file exists**. Concrete attack: **before: the Dispatch is open; after: `worker_done` settles the Task and the worker idles (`inventory/orca-capabilities.md:77-78`), the contract is written late or not at all, and the coordinator opens a missing file (`:73`).** Severity: MAJOR. See F10.
- I can break this specification by **FR-2.5 Accumulation Attack**. The invariant at **WC-3 (`:61`)** fails when **the `ask` timeout repeats without limit**. Concrete attack: **before: a question is pending; after: each timeout resumes the same message ID with no cap, and §7.2 (`:181-182`) defines no exit, so the Dispatch waits indefinitely.** Severity: MAJOR. See F11.

---

## Guard Condition Boundary Table

Rows cover every guard in §2.2, §3 and §7.2 that the candidate states as a condition or threshold. Status values: OK, or GAP (with its finding; blocking GAPs are marked).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | `:63` | Zero/Empty | no report file | no report exists: true | `--outcome failed` | OK |
| WC-5 outcome mapping | `:63` | One/Minimal | status `partial` | partial: true | `--outcome succeeded` (`:263`) | OK |
| WC-5 outcome mapping | `:63` | Typical | status `succeeded`, audit verdict FAIL | failed/blocked: false | `--outcome succeeded` | OK |
| WC-5 outcome mapping | `:63` | Sentinel Value Match | status missing, empty or `done` | outside the four values | "otherwise" gives `succeeded` | GAP (F9) |
| WC-5 outcome mapping | `:63` | Legitimate Edge Case | status `blocked` with a usable deliverable | blocked: true | `--outcome failed` | OK |
| WC-4 contract location | `:62` | Zero/Empty | run stops before any output | contract required | pre-creation STOP location not named (`:92`) | GAP (F8) |
| WC-4 contract location | `:62` | Typical | `--output <dir>` | directory | `<dir>/return-contract.yaml` | OK |
| WC-4 contract location | `:62` | Maximum/Overflow | `--output <file>` (tdd, init-lite, spec-panel) | not a directory | `<file>/return-contract.yaml` cannot be created | GAP (F3, blocking) |
| WC-4 contract location | `:62`, `:73` | Sentinel Value Match | research: generated `claudedocs/research_*.md` | path unknown before dispatch | candidate requires known-before-dispatch | GAP (F8) |
| WC-2 gate resolution | `:60` | Zero/Empty | gate with no documented default and no flag | blocked: true | status blocked, with question | OK |
| WC-2 gate resolution | `:60` | Typical | documented default applies | default: true | proceeds with the default | OK |
| WC-2 gate resolution | `:60` | One/Minimal | flag supplied (for example `--post-pr`) | flag: true | proceeds (`:100`) | OK |
| WC-2 and WC-3 gate resolution | `:60-61`, `:109` | Sentinel Value Match | implement Ruling gate (E-HALT-QA) | ask route allowed by WC-3 | D2(a) forbids a relayed Ruling (`:234`) | GAP (F4, blocking) |
| WC-6 resume or fresh dir | `:64` | Zero/Empty | no resume flag, fixed output (init-lite) | retry overwrites | "must not corrupt" (`:64`) | GAP (F2, blocking) |
| WC-6 resume or fresh dir | `:64` | Typical | resume flag (cleanup-audit `progress.json`) | resumes | OK (`:85`) | OK |
| WC-1 readiness fallback | `:59` | Maximum/Overflow | fallback between 30 s and 60 s | 30 s passes; above about 45 s fails (`inventory/orca-capabilities.md:49`) | "well inside" gives no number | GAP (F6) |
| WC-10 wait split | `:68` | Maximum/Overflow | cli-eval eval up to 3600 s | more than 300 s | split into waits of 240 s or less | OK (`:104`) |
| WC-10 wait split | `:68`, `:283` | Sentinel Value Match | pr-submit poll-plus-sleep iteration | runtime unknown | 240 s or less required | open (UNVERIFIED) |
| WC-11 parallel writes | `:69` | Two | two workers, same worktree, fixed output dir | same path | clobbering possible | GAP (F7) |
| WC-9 outward action | `:67` | Zero/Empty | no authorising flag | absent | off | OK |
| WC-12 ownership check | `:70` | Sentinel Value Match | `consumer_fenced` returned | fenced: true | stop, no `worker_done` (`inventory/orca-capabilities.md:67`) | OK |
| §7.2 step 2 | `:181` | Sentinel Value Match | `agentWait` non-null | parked: true | fail; no coordinator action | GAP (F11) |
| §7.2 step 3 | `:182` | Zero/Empty | no `worker_done` before the timeout | none | fail implied; no timeout action | GAP (F11) |
| §7.2 step 3 | `:182` | Two | duplicate `worker_done` | two | fail (exactly one) | OK |
| §3.1 brief | `:83-92` against `:73` | Zero/Empty | brief lacks `--unattended` | absent | standard mode, no contract | GAP (F1, blocking) |
| SA-1 standalone | `:146` | Zero/Empty | no `--unattended` | absent | today's behaviour | OK |

Classes left out, with reasons: WC-9, WC-12, SA-1 and the WC-2 flag row are presence checks, so One/Minimal and Maximum classes do not apply. Status fields are enums, so the Maximum/Overflow class does not occur for WC-5. The WC-6 circuit breaker is enforced by Orca (`inventory/orca-capabilities.md:116`), not by the command, so it has no row.

---

## Follow-up candidates (Medium and minor; not blocking)

F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F17 (Medium); F18, F19, F20 (minor).

The session that ran this review asks the user once whether to open an issue for these. None is created without the user's answer. `--unattended` was not given, so the run only records the list.

## Decisions made by this reviewer

- One reviewer, because the `superclaude` panel CLI is not installed here. Stated in the header.
- Findings F1 to F5 are blocking because each has a sentence that holds without an extra assumption (contradiction, or an acceptance criterion that cannot pass). The others need a guess, or they state a requirement the candidate never gives, so they are Medium.
- Placement: the Findings block is placed before the Reviser brief so that the brief sits directly above the verdict line, as Review Loop bullet 6 requires. The verdict line is the last line.

## Reviser brief

Blocking findings: F1, F2, F3, F4, F5.

Restated rule (Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "step 4 uses the command's existing report file, since the contract arrives in P1", "anchor2": "its report path is the WC-4 contract path", "refs": ["AC-0.4", "7.2 step 3", "7.2 step 4", "3.1", "2.3", "WC-4"], "claim": "An implementer who runs AC-0.4 as written on /sc:troubleshoot gets a REPORT.md report that fails step 3's contract-path condition and step 4's YAML parse, so the P0 gate can never pass."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "data-loss", "anchor": "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output.", "anchor2": "Re-run overwrites its marked report", "refs": ["WC-6", "3.1 init-lite"], "claim": "An implementer who follows the init-lite row unchanged lets a --retry-of attempt overwrite the first attempt's report at the same --output path, which WC-6 forbids."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "the directory the coordinator passed (`--output` / `--output-dir`)", "anchor2": "a precise component prompt, not a bare topic; `--output <file>`", "refs": ["WC-4", "3.1 tdd", "3.2 init-lite", "3.2 spec-panel"], "claim": "An implementer who follows WC-4 for /sc:tdd with --output <file> writes the contract to <file>/return-contract.yaml, which cannot be created."}
{"id": "F4", "severity": "MAJOR", "blocking": true, "category": "safety", "anchor": "re-invoke or resume the command with the answer as a flag", "anchor2": "The worker stops, writes the halt to its ledger and contract, and ends `failed`.", "refs": ["WC-2", "WC-3", "3.2 implement", "D2"], "claim": "An implementer who follows WC-3 at the implement E-HALT-QA gate sends the Ruling question through ask and re-invokes implement with the coordinator's reply, recording an agent message as the Ruling."}
{"id": "F5", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "anchor2": "Each changed command adds a short `## Unattended mode` section", "refs": ["AC-1.1", "2.1", "3.1 brainstorm"], "claim": "An implementer who follows §2.1 and the brainstorm row of §3.1 adds no Unattended mode section to brainstorm, so AC-1.1 fails as written."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Any such prompt must fall back on its own well inside the readiness limit (default 60 s).", "anchor2": "passes with a 30 s fallback; above about 45 s it fails again", "refs": ["WC-1", "7.2 step 1"], "claim": "WC-1 gives no numeric fallback, so an implementer cannot tell whether a 50 s fallback is acceptable, although the cited evidence says it fails."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Default output paths carry a timestamp or the slug the coordinator passes", "anchor2": "one audit per worktree at a time (WC-11)", "refs": ["WC-11", "3.1 cleanup-audit", "3.1 index-repo", "3.1 init-lite"], "claim": "The cleanup-audit row relies on a serialisation rule that WC-11 does not state, so two workers in one worktree can clobber fixed-path reports."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "so the report path is known before dispatch (WC-4)", "anchor2": "contract naming the generated `claudedocs/research_*.md` path", "refs": ["2.3", "WC-4", "3.2 research", "3.1 workflow"], "claim": "WC-4 requires a path known before dispatch, but research and workflow produce their contract path at run time, and no location is given for workflow pre-creation STOPs."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "`--outcome succeeded` otherwise, including `partial`", "anchor2": "One report file, known before dispatch, written on every outcome.", "refs": ["WC-5", "WC-4"], "claim": "A contract with a missing or unknown status maps to --outcome succeeded, so a failed run can be reported as success."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "It is written on success, failure, blocked and partial outcomes, including stops before any other output exists.", "anchor2": "The worker passes the contract path as `worker_done --report-path`.", "refs": ["WC-4", "2.3"], "claim": "WC-4 gives no order for writing the contract and sending worker_done, so the coordinator can open a missing file."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "On an `ask` timeout it resumes the same message ID and never creates a duplicate.", "anchor2": "observation.agentWait` is never non-null", "refs": ["WC-3", "7.2 step 2", "7.2 step 3"], "claim": "Ask retries have no cap and the checks define no coordinator action for a parked worker or a check timeout, so a Dispatch can wait indefinitely."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "installed to `~/.claude/WORKER-CONTRACT.md`", "anchor2": "a command switches to when its caller passes `--unattended`", "refs": ["2.1", "AC-0.1", "AC-1.1"], "claim": "The spec does not say what an unattended command does when ~/.claude/WORKER-CONTRACT.md is not installed."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "`target_release` required as a flag for TDD inputs, else blocked", "anchor2": "the improved-spec step stays off unless the brief asks", "refs": ["3.2 spec-panel", "WC-4", "INV-B:182"], "claim": "The spec-panel row asks to add --output, but the sandbox command definition already has --output and an unattended section, so the row is stale (UNVERIFIED which copy is current)."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies", "refs": ["3.2 tasklist", "WC-2", "INV-B:209"], "claim": "The tasklist HALT on needs_human_decision items has no resolution, so a tasklist worker can stop without worker_done."}
{"id": "F15", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "inside Claude Code's nesting limit", "anchor2": "its reflect fan-out runs one layer below the worker", "refs": ["3.2 tasklist", "INV-A:14", "INV-B:295"], "claim": "The tasklist nesting claim is not counted: at the depth limit the reflect Agent tool is withheld and the fan-out fails silently, and the inventory's required change is dropped without a recorded decision."}
{"id": "F16", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "What changes in the commands is limited to the worker contract in section 2", "anchor2": "reconcile the flag surface the command calls unsupported with the flags the skill still defines", "refs": ["1.1", "2.1", "3.2 roadmap", "SA-4"], "claim": "The scope statement says only the contract changes commands, but §3.2 requires other changes such as the roadmap flag reconciliation."}
{"id": "F17", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file.", "anchor2": "prints nothing (SA-2, WC-8)", "refs": ["AC-C1", "SA-2", "SA-5", "P0"], "claim": "AC-C1 scans src/superclaude/core, so the contract file or the routing-guide Orca section fails it in P0 wherever it names an Orca command."}
{"id": "F18", "severity": "MINOR", "blocking": false, "category": "contradiction", "anchor": "make `--remediate` follow the existing headless auto-accept rule", "refs": ["3.1 reflect", "P2"], "claim": "Reflect is labelled ready today, but its row requires a P2 change."}
{"id": "F19", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "are not counted by Orca's nesting limit", "refs": ["1.2 E4", "CAPS:155"], "claim": "E4 presents as evidence a point the inventory marks UNVERIFIED."}
{"id": "F20", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "This worker re-read 11 of the load-bearing locations on 2026-11-02", "refs": ["§2 citation conventions"], "claim": "Many citations point to files outside the workspace, so this review could not check them."}
```

verdict: FAIL
