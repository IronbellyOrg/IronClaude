review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole document, first review)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `ad7680cf8b39696f9eede626f872afc9b90b8426c6886d766a44d4d26c306157`
- baseline: none given, none needed (first review of the full document)
- command: `/sc:spec-panel --mode critique --focus requirements,architecture`; prompt used: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full)
- reviewer model actually used: claude-sonnet-5-5
- label: whole-document audit of the final spec. A re-review's scoped PASS would not give this assurance; this one covers the whole document.
- Improve step: not run (critique mode, no `--improve`; the candidate is not edited).

## Coverage and evidence limits

Covered: sections 1-9, the Decisions table and the UNVERIFIED list, cross-read against `README.md` and the three inventories (`INV-A` = `inventory/commands-a.md`, 120 lines; `INV-B` = `inventory/commands-b.md`, 323 lines; `CAPS` = `inventory/orca-capabilities.md`, 188 lines).

Checked against the inventories (all matched): the 43 = 21 + 22 command split (`INV-A:3`, `INV-B:3`); the 10 ready / 27 needs-change / 6 coordinator-only totals (`INV-A` 5/13/3, `INV-B` 5/14/3 at `commands-b.md:289` and its summary); the phase lists (P1 = 9, P2 = 15, P3 = 4, P4 = 3, with all 27 needs-change commands placed exactly once); the CAPS citations for the 60 s limit (`CAPS:44-52`), depth 1 (`CAPS:97-103`), `ask` (`CAPS:58-64`), `worker_done` (`CAPS:72-80`), executable names and identity (`CAPS:145-151`), subagents (`CAPS:155-161`), and the open questions (`CAPS:178-188`); the README citations (`README.md:6,11-17,30,31,35`).

UNVERIFIED (not checkable inside this workspace, which holds only the README, the three inventories and the spec): every `path:line` the spec cites into `src/superclaude/**`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `tests/` and `plugins/`. Where the spec reaches them through an inventory line I checked that the inventory says the same, not that the source does.

## Expert panel (review order)

Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower each read the document; findings below carry the expert attribution.

Blocking findings: none. Every candidate finding failed the grading check "An implementer who follows the stated text as written builds X, and X is wrong because Y" without a guess about which of two allowed readings the implementer picks, or is a requirement the document never states. The F-ids below are Medium or minor.

## === REQUIREMENTS ANALYSIS ===

### F-1 (Medium; MAJOR label) Contract rules reach commands that no phase changes. Expert: Wiegers
- Stated texts: WC-4 says that where `--output` is a file, "(tdd, init-lite, spec-panel)" write `<output-file>.return-contract.yaml` (spec line 62). Section 3.1 says init-lite has "None" to change, "Report today: `.dev/superclaude/context-audit.md` or `--output`" (spec line 87). Section 3.1's lead-in says the worker reports the named file "until Phase 1 adds the contract" (line 79), but P1 touches only adversarial, cleanup-audit, index-repo and workflow among the ready commands (line 159); brainstorm and init-lite appear in no phase (lines 158-162). Section 2.3 and the 7.2 step 3-4 check apply the WC-4 contract path and four-value `status` vocabulary to every worker (lines 73, 182-183).
- Why Medium: WC-4 and WC-2 are scoped to "unattended mode" and "the path its section 3 row names", so a reader can conclude that init-lite and brainstorm are outside the contract. That reading needs a guess, and the document never says which commands are outside.
- Wrong outcome if the worse reading is taken: a coordinator records `<output-file>.return-contract.yaml` as init-lite's report path before dispatch (section 2.3), the file is never written, `test -s` fails, and WC-5 maps "no report exists" to `--outcome failed` for a successful audit.
- Related unchecked fact: brainstorm, adversarial and workflow already write `return-contract.yaml` (`INV-A:97`, `INV-B:272`), but the spec never checks that their existing `status` values are in the four-value set `succeeded|partial|failed|blocked` that 7.2 step 4 asserts (line 183). `INV-B:272` lists only the field name `status`.
- Recommendation (follow-up): add one sentence to section 3.1 or 2.1 saying which ready commands stay outside the WC-4 contract and are reported through their named file.

### F-2 (Medium) A fresh-directory retry (WC-6) conflicts with a report path fixed before dispatch (WC-4). Expert: Adzic
- Stated texts: WC-4 "The brief records the path before dispatch" (line 62); WC-6 says a command without a resume flag "writes each run into a fresh output directory so a re-run starts clean" (line 64); 22 of the 27 needs-change rows say "fresh dir" (section 3.2). The spec does not say who creates the fresh directory or whether the retry brief passes a new `--output`.
- Wrong outcome under the worse reading: the retry (`worker-start --retry-of`, `CAPS:116`) writes into the same `--output` as the first attempt and overwrites the first attempt's contract, or the command picks its own new directory and the coordinator opens the old path.
- Recommendation (follow-up): state in WC-6 that the coordinator passes a new output path for a retry and records it.

### F-3 (Medium) Refusals under `--unattended` have no defined contract content. Expert: Whittaker (Zero/Empty attack)
- WC-2 says every gate resolves one of three ways: default, supplied flag, or blocked with the question (line 60). Section 3.2 adds a fourth, "refused" (cleanup and improve `--interactive`, explain `--format interactive`, test `--watch`, pr-submit `--monitor 1`, roadmap `--interactive`, business-panel `--mode socratic`; lines 102-103, 108, 114, 118, 123). A refusal has no question, yet AC-2.2 asserts a non-empty `blocked_question` for gate-trigger runs (line 200).
- Concrete attack: `/sc:test --watch --unattended`. State before: no contract. Under WC-4 a contract is written "including stops before any other output exists", but the spec does not say whether `status` is `blocked` (and `blocked_question` is empty, which AC-2.2 reads as a failure) or `failed`. WC-5 sends both to `--outcome failed`, so the outcome is right; only the contract shape is open.
- Recommendation (follow-up): say that a refusal writes `status: failed` with the refusal reason in `report_path`'s body or a `reason` field.

### F-4 (Medium) The report path is unnamed for commands that have no output flag. Expert: Wiegers
- WC-4 derives the contract path from `--output` / `--output-dir` (line 62). Rows for research, save, task, review-translation, recommend and tasklist (lines 115-122) say "contract naming/pointing at ..." or "contract on every tier" but name neither a flag nor a path. research writes `claudedocs/research_*.md` with a generated name (line 116); task has a contract only on TFEP today (line 121).
- This is a requirement the document never states, so it is not blocking. Without it, "known before dispatch" cannot hold for these six commands.
- Recommendation (follow-up): give each a `--output`-style flag in its row or a fixed contract path.

### F-5 (Medium) `--unattended` is demanded in every brief but most ready commands never accept it. Expert: Cockburn
- Section 2.3: the brief states "the exact command line including `--unattended`" (line 73). Section 6: "no command accepts the flag while its gate still prompts" and a command accepts it only in its row's phase (line 154). The ready commands adversarial, brainstorm, cleanup-audit, index-repo, init-lite and workflow have no gate and no phase that adds the flag (lines 83-92, 158-162), and the P0 smoke commands carry no `--unattended` (AC-0.4, line 194).
- Wrong outcome under the worse reading: a coordinator follows section 2.3 literally and appends `--unattended` to `/sc:workflow "<change>" --handoff none`; the flag is read as prompt text or rejected.
- Recommendation (follow-up): qualify section 2.3 with "for a command whose row gains the flag".

### F-6 (Medium) The load row and AC-1.1 disagree on whether load gets a contract section. Expert: Crispin
- AC-1.1 asserts that "every command in the P1 row" has a `## Unattended mode` section naming `return-contract.yaml` (line 195); the P1 row lists `load (usage line only)` (line 159); section 3.2 gives load "Report: none" and Decisions say "a report file would be an unrequested addition" (lines 112, 265). The parenthetical "(usage line only)" probably resolves this, so the test and the row are consistent only under that reading.
- Recommendation (follow-up): exclude load from AC-1.1's quantifier in words.

### F-7 (Medium) AC-C1 may fail on the spec's own P0 deliverables, and its raw text does not run as a filter. Expert: Crispin
- AC-C1 greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` (line 172). P0 adds `WORKER-CONTRACT.md` with a coordinator brief template and an Orca section in `HOW-WE-WORK.md` (line 158), and SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (line 147). Neither text is shown, so whether they contain a matching phrase is a guess; a natural `orca orchestration ask` example would fail the common check at every phase.
- Raw-text defect: the alternation is written `\|` inside a Markdown table cell. As raw text under `grep -E`, `\|` is a literal pipe, so the pattern would match nothing and the check would pass vacuously. Rendered Markdown shows `|`, so this is only a hazard for a copy from source.
- Recommendation (follow-up): exclude `core/WORKER-CONTRACT.md` and the HOW-WE-WORK Orca section from AC-C1, or limit it to `commands`, `skills` and `agents`; give the command in a fenced block.

### F-8 (Medium) Tasklist departs from its inventory verdict without a recorded decision. Expert: Newman
- `INV-B:215` says Stage 10.5 should call reflect without `--remediate` "and the per-phase reflect fan-out must run at the worker's top level, not inside subagents"; `INV-B:210` marks the subagent nesting UNVERIFIED. The spec's row passes `--unattended` to each reflect so the headless auto-accept rule applies, and asserts the fan-out is "inside Claude Code's nesting limit, `INV-A:14`" (line 122). `INV-A:14` states the Claude Code limit in general terms; it does not trace tasklist, reflect Tier 2 and the Tier 3 handoff to workflow (`INV-B:109`, `INV-B:272`) through the layers.
- The Decisions table keeps the inventory verdicts (line 268) but records no decision for this departure, and the UNVERIFIED list does not include the nesting claim.
- Wrong outcome under the worse reading: N reflects auto-accept remediation inside subagents, and a corrective workflow run starts at the depth limit, where the Agent tool is silently withheld (`INV-A:14`).
- Recommendation (follow-up): either adopt the inventory's `--no-remediate` route or add the nesting claim to the UNVERIFIED list.

## === ARCHITECTURE ANALYSIS ===

### Assessment (Fowler, Nygard, Newman, Hohpe)
The central decision is sound and evidenced. Orca is the coordinator and each command stays a unit of work behind one narrow contract: a switch, one report file and a resume rule (section 1.1). The rejected alternative has five reasons, each tied to a `CAPS` line (R1-R5, lines 33-37), and the strongest, depth 1 refusing nested `worker-start`, is quoted at `CAPS:97-101`. The spec states its own evidence gaps (section 1.4) and puts a live baseline first (P0, AC-0.4). The six coordinator-only commands match both inventories (`INV-A:90-92`, `INV-B:285-287`). Standalone behaviour is protected by SA-1 to SA-6.

### F-9 (minor note) Evidence cited for a standing rule is a one-run rule. Expert: Nygard
- WC-9 and section 4 (`/sc:git`) cite `README.md:31`, "No git commits, pushes, PRs or GitHub comments", as support (lines 67, 133). That line binds the workers of this planning run, not workers in general. The cited support for the standing rule is therefore weaker than presented; the rule itself is separately argued from `cmd/auggie-review.md:51-54` (UNVERIFIED here).

### F-10 (minor note) Phase and count wording. Expert: Hohpe
- The "10 / 27 / 6" headline (line 76) counts pr-submit among the 27; under the recommended D3(a) it is dispatched as nothing (line 139, line 240), so the effective split is 10 / 26 / 7. Separately, the P1 row lists "fixes to ... workflow" (line 159) while the workflow row says "None for the contract" (line 92); AC-1.4 shows the fix is a documentation statement.

### F-11 (minor note) An unverified assumption is stated as fact in WC-4. Expert: Newman
- WC-4 says "Orca does not check the file" (line 62); `CAPS:79` and `CAPS:178` mark it UNVERIFIED, and UNVERIFIED item 3 (line 274) says the spec "assumes". Harmless because the coordinator opens the file regardless.

### F-12 (minor note) Quoted flag token. Expert: Whittaker (Sentinel Collision attack)
- I can break this specification by a **Sentinel Collision attack**. The invariant at **D1(a)** ("cannot misfire on a person", line 228) fails when **`--unattended` appears inside quoted prompt text**. Concrete attack: `/sc:tdd "document how --unattended behaves" --output t.md`. Before: no mode. After: a command that scans arguments by substring enters unattended mode and resolves gates silently. The spec gives no tokenizing rule. Severity: MINOR (behavior inferrable from normal argument parsing).

### F-13 (minor note) Observation from the command definition. Expert: Hightower
- The `/sc:spec-panel` definition used for this review already lists `--output` and an `--unattended` section keyed to `--report-dir`, while the spec's spec-panel row says `--output` must be added and puts the contract at `<output-file>.return-contract.yaml` (lines 62, 120). The definition file is not part of the workspace evidence; mark UNVERIFIED and reconcile when the P2 plan for spec-panel is written.

## Whittaker adversarial summary (other methodologies)

- **Sequence Attack:** WC-5 requires the contract to exist before `worker_done` (the path is passed as `--report-path`), and WC-12 requires `check` before `worker_done`. The spec does not say a worker that hits `consumer_fenced` after writing the contract leaves a stale `status: succeeded` file; the coordinator would open it. MINOR: `consumer_fenced` means the dispatch is no longer the worker's (`CAPS:67`).
- **Accumulation Attack:** retry cap is 3 consecutive `worker-start` failures; a worker's own `failed` or `blocked` report does not count (`CAPS:80`, spec line 263). A blocked command can therefore be retried without limit by a coordinator. The spec does not state a coordinator-side cap. MINOR.
- **Divergence Attack:** the `partial` to `succeeded` mapping (line 63, 263) sends a half-done outward run (post-release, task) to the same outcome as a clean one; the body's first sentence is the only distinction. MINOR, and the spec names the mitigation.

## Guard Condition Boundary Table (FR-8 to FR-10; first review, whole document)

Guards in the spec: the 60 s readiness limit (WC-1), the 4-minute wait split against the 5-minute heartbeat (WC-10), the status-to-outcome mapping (WC-5), the depth-1 nesting limit (R1), the confidence 0.70 gate on task (line 121). Classes left out are given one line each. A GAP is a Medium or minor finding, not a blocking one, because none names a concrete wrong outcome without a guess.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| readiness limit | WC-1 | Zero/Empty | `--timeout-ms` 0 or absent | default 60 s applies (`CAPS:44-45`) | launch path may not wait on a person | OK |
| readiness limit | WC-1 | Typical | prompt falls back at 30 s | passes (spec line 59) | passes | OK |
| readiness limit | WC-1 | Maximum/Overflow | fallback above about 45 s | fails again (spec line 59) | fails at `agent_readiness` | OK |
| wait split | WC-10 | Zero/Empty | wait of 0 s | not reached | no wait, no split | OK |
| wait split | WC-10 | Typical | one poll wait of 3 min | under 4 min | no split | OK |
| wait split | WC-10 | Maximum/Overflow | single call over 5 min (cli-eval up to 3600 s) | true | split into waits at most 4 min | OK |
| wait split | WC-10 | Legitimate Edge Case | a single iteration of poll runtime plus sleep over 4 min (pr-submit) | unknown | "confirm" (UNVERIFIED poll runtime, line 114) | GAP (stated UNVERIFIED; Medium) |
| outcome mapping | WC-5 | Zero/Empty | no contract exists | true | `failed` | OK |
| outcome mapping | WC-5 | Sentinel Value Match | `status: blocked` with empty `blocked_question`, or a refusal | true | contract content not specified (F-3) | GAP (Medium) |
| outcome mapping | WC-5 | Legitimate Edge Case | `partial` | true | `succeeded`, status in body | OK |
| nesting depth | R1/WC-8 | Typical | depth 1 worker calls `worker-start` | refused (`CAPS:97-99`) | refused, `nested_worker_depth_exceeded` | OK |
| nesting depth | R1/WC-8 | Legitimate Edge Case | depth 1 worker calls `task-create` | unknown | forbidden by WC-8 (UNVERIFIED item 5) | OK (hedged) |
| confidence gate | task row | Maximum/Overflow | confidence exactly 0.70 | boundary | "below 0.70 resolves as blocked" (line 121); at 0.70 the source rule is `< 0.70` (`INV-B:199`) | OK |
| confidence gate | task row | Zero/Empty | confidence unavailable | unknown | not stated | GAP (minor) |

Left out: a One/Minimal row for the confidence gate (a single score is the typical case); a Sentinel row for the readiness limit (no sentinel value exists); a Maximum row for the depth limit (the setting is 1 and a larger value is a user decision, D5).

## Pipeline Dimensional Analysis (FR-17 to FR-21)

Trigger: the rollout classifies 43 commands into groups and phases, so the count at each stage can differ. All counts were checked against the tables and conserve.

```text
[Source: 43 commands (21 INV-A + 22 INV-B)]
  --> [Classify: 10 ready, 27 needs-change, 6 coordinator-only] = 43
        |
        +--> [6 coordinator-only] --> no phase
        +--> [10 ready] --> P0 smoke (3 of them), P1 fixes (4: adversarial, cleanup-audit, index-repo, workflow),
        |                   P2 gate fixes (4: reflect, release-split, tdd, troubleshoot), no phase (2: brainstorm, init-lite)
        +--> [27 needs-change] --> P1 9, P2 11, P3 4, P4 3 = 27
```

Consumer check: sections 3.1, 3.2 and 4 each list their own members, and sections 6 and 7 consume the phase lists; no consumer assumes the 43 or the 27 where a subset applies. The only mismatch is the D3(a) effect on pr-submit (F-10, minor). The "no phase" rows for brainstorm and init-lite are the source of F-1.

## follow-up candidates

Medium: F-1, F-2, F-3, F-4, F-5, F-6, F-7, F-8, plus the two Guard Condition Boundary Table GAP rows (the pr-submit iteration time, and the empty `blocked_question`, which is F-3).
Minor notes: F-9, F-10, F-11, F-12, F-13, and the three Whittaker notes above.

The session that ran this review would ask the user once whether to open an issue for these. In this sandbox the reply is limited to the output path, so the question was not asked and no issue was created; the list is recorded here only.

## Brief clauses overridden

None. The brief narrowed nothing and widened nothing; no minor or Medium finding was graded as blocking.

## Reviser brief

None: no blocking finding is open, so no revision is called for.

verdict: PASS
