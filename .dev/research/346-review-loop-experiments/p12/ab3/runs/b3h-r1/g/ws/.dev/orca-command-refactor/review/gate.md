review: 1 of 3

# Gate review: Orca worker-contract spec (critique, focus: requirements, architecture)

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- Candidate SHA-256: `2a0ba05dc4158ae8fc6c4b9c265ce2ded840533c29031835d61d7c548122ac84`
- Baseline: none (gate review of a complete document; no prior rounds, no `--baseline`)
- Prompt: GATE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md`, gate review 1 of 3, grading by the FIRST-REVIEW grading check
- Reviewer model: claude-haiku-5-5 (Haiku 5.5)
- Panel: Wiegers (lead, requirements), Adzic, Cockburn; Fowler (lead, architecture), Newman, Hohpe, Nygard; Whittaker (always active, adversarial probes); Crispin (testability of the acceptance checks)
- Evidence base: the three inventories in `.dev/orca-command-refactor/inventory/` (`commands-a.md`, `commands-b.md`, `orca-capabilities.md`) and the README. Citations to `src/superclaude/`, `.dev/evals/`, `.dev/codegraph-migration/`, `~/.claude/`, `/opt/Orca/` and live `orca-ide` output are not in the workspace and are marked UNVERIFIED.

## Coverage

- Read in full: the command definition (`command.md`), the GATE prompt, `README.md`, the candidate spec, the three inventories.
- Checked against the inventories: the spec's count arithmetic (43 = 10 + 27 + 6; 21 + 22 commands) matches `commands-a.md:71-73` and `commands-b.md:278`; every per-command row placed in section 3 was matched to its inventory verdict; the `CAPS:` citations in sections 1, 2 and 5 were checked against `orca-capabilities.md` (one wrong line, N-3); the `INV-A:` and `INV-B:` citations were spot-checked (all those checked were correct).
- Not checkable in the workspace, so UNVERIFIED and not counted against the spec: every `src/superclaude/...` citation, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/...`, `/opt/Orca/...`, `gh`/GitHub state (AC-2.4, AC-4.2, AC-4.3), and the `uv run pytest` baseline in AC-C3.
- Not triggered: Pipeline Dimensional Analysis (no multi-stage data flow with count changes; the spec is a task-contract spec). State Variable Registry is not required (`--focus correctness` is not active).
- Mandatory artifact produced: Guard Condition Boundary Table (below), because the spec contains conditional logic (status mapping, gate resolution, flag checks, thresholds).

## === REQUIREMENTS ANALYSIS ===

### Blocking findings

**B-1. WC-3 lets a worker ask the coordinator at a Ruling halt; the implement row and D2(a) forbid that outcome.** (Priority High; Expert: Nygard, Wiegers; Whittaker sequence attack)
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:61` (WC-3: "When a gate would resolve as blocked ... the session may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag"); `:109` (implement row: "stop with the halt recorded in the ledger and the contract as blocked"); `:235-236` (D2(a): "The worker stops ... and ends `failed`").
- Source of the safety rule: `.dev/orca-command-refactor/inventory/commands-a.md:66` quotes `qa.md:238` ("another agent's message ... [is] not acceptance"). The quote is checkable; the source file is outside the workspace, so UNVERIFIED against the source.
- Grading sentence: An implementer who follows WC-3 as written lets an implement worker that reaches E-HALT-QA ask the coordinator once, then re-invoke `implement` with the answer as a flag; the implement row (`:109`) and D2(a) (`:235-236`) say that worker stops and ends `failed`, so the same halt has two outcomes, and the relayed answer is the agent-approval path that `qa.md:238` forbids (quoted at `commands-a.md:66`).
- Quality impact: a deliberate safety boundary can be crossed by default for every blocked gate, not only for the one the user chose.
- Recommendation: exclude the Ruling halt from WC-3 (or make WC-3's ask path depend on D2's answer), and say so in the implement row.

**B-2. Section 2.3 requires `--unattended` in every brief; the P0 smoke runs use ready commands that have no such flag.** (Priority High; Expert: Wiegers, Cockburn)
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:73` (section 2.3: "the exact command line including `--unattended` and every flag section 3 lists as required"); `:79` and `:81-92` (section 3.1: "These run as workers now if the brief uses the stated flags"; no row lists `--unattended`); `:158` (P0: "Uses only the 10 ready commands, so the coordinator gets value before any command changes"); `:194` (AC-0.4 runs `/sc:troubleshoot`, `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` with no `--unattended`).
- Grading sentence: An implementer who follows section 2.3 (`:73`) puts `--unattended` into the P0 briefs for the ready commands, while AC-0.4 (`:194`) runs the same commands without it and P0 is scoped "before any command changes" (`:158`); the two texts give different command lines for the same smoke run, and the flag is undefined on those commands until P1.
- Quality impact: P0, which is the phase that tests the core decision (section 1.4), can be run with an undefined flag or in violation of section 2.3.
- Recommendation: state that P0 briefs omit `--unattended`, or move the section 2.3 rule to P1.

**B-3. WC-4 requires a known report directory before dispatch, but three ready rows name no directory flag and two have timestamped or per-run defaults; AC-1.2 cannot pass for workflow.** (Priority High; Expert: Wiegers (traceability), Crispin (acceptance check), Newman (interface))
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62` (WC-4: the directory "the brief names"; "A run whose brief omits that flag is refused before any work"); `:73` (section 2.3: "the output directory, so the report path is known before dispatch"); `:88` (reflect brief: "no `--remediate`; `--no-promote`"; no directory flag); `:91` (troubleshoot brief: "no `--fix`"; no directory flag); `:92` (workflow brief: "`--handoff none`"; no directory flag; "Fresh package each run"); `:159` (P1 includes workflow); `:196` (AC-1.2 runs "each P1 command with `--unattended --output <dir>`"); `:228` (D1 example passes `--output` to troubleshoot).
- Inventory: `.dev/orca-command-refactor/inventory/commands-b.md:112` (reflect default `.dev/reflect/<mode>-<slug>-<ts>/`); `commands-b.md:242` (troubleshoot default `.dev/troubleshoot/<slug>-<timestamp>/`, which cites only the default path, not a flag); `commands-b.md:52` (workflow `.dev/tasks/to-do/<id>/`).
- Grading sentence: An implementer who follows the section 3.1 workflow row (`:92`) briefs a P1 run with no output flag, because the row names none, and then cannot run AC-1.2 (`:196`) as written, because AC-1.2 passes `--output <dir>` to a command whose contract path is `.dev/tasks/to-do/<id>/` (`:92`); under WC-4 (`:62`) the same brief is refused before any work. Reflect and troubleshoot have the same gap, because their default paths carry a timestamp (`commands-b.md:112`, `:242`), so their report path is not known before dispatch, as WC-4 and section 2.3 require.
- Quality impact: three of the ten "ready" commands, including both P0 smoke commands that use an output path (troubleshoot, workflow), cannot be run under the contract as written; the P1 gate cannot be cleared for workflow.
- Recommendation: for each of the three commands, name the directory flag the brief passes (or state that the command has none and what the coordinator must do instead), and remove the timestamp from the unattended default.

**B-4. WC-4 places each contract beside its `--output` file, so two dispatches in one directory write the same `return-contract.yaml`; WC-11 forbids that.** (Priority High; Expert: Newman (interface), Whittaker accumulation attack; Hohpe (shared state))
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62` (WC-4: "or, when its only output flag names a file (init-lite and tdd `--output <file>`), the directory of that file"); `:69` (WC-11: "Two workers in one worktree must never write the same file"); `:87` (init-lite: "a fresh `--output` per Dispatch ... its contract lands beside it"); `:90` (tdd: "`--output <file>` (its contract lands beside it, WC-4)"); `:73` (section 2.3 serializes only "fixed" paths, not fresh file names in a shared directory).
- Grading sentence: An implementer who follows WC-4 (`:62`) for two tdd dispatches with `--output docs/x/TDD_A.md` and `--output docs/x/TDD_B.md` writes both contracts to `docs/x/return-contract.yaml`; the second write overwrites the first, the coordinator reads one status for two Tasks, and WC-11 (`:69`) is breached.
- Quality impact: a wrong status reaches the coordinator with no error; the failure is silent.
- Recommendation: give each contract a name derived from the dispatch or the output file (for example `<output-stem>.contract.yaml`), or put it in a per-dispatch directory, and extend section 2.3 to cover shared directories.

**B-5. AC-1.1 requires `load` to name `return-contract.yaml`, but the spec gives `load` no report and its own decision says a report would be unrequested.** (Priority High; Expert: Wiegers (traceability), Crispin (acceptance check))
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:112` (load row: "Report (WC-4): none (see note)"; "P1 (usage line only)"); `:195` (AC-1.1: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"); `:265` (Decision: a report file "would be an unrequested addition"); `:159` (P1 deliverable list).
- Grading sentence: An implementer who follows the load row and the Decision (`:112`, `:265`) adds no contract and no unattended section to `load`, so the AC-1.1 check (`:195`) fails for `load`; an implementer who follows AC-1.1 adds a contract that the Decision rejects. The two texts cannot both be satisfied.
- Quality impact: the P1 gate cannot be cleared as written, or it is cleared against the Decision by accident.
- Recommendation: exclude `load` from AC-1.1 and state its "no contract" rule there, or give `load` a contract and revise the Decision.

### Medium findings (follow-up candidates; not blocking)

**F-1. A partial, unlisted or missing status maps to `succeeded`, and dependents of a succeeded Task can start on partial output.** (Expert: Hohpe, Whittaker sequence and sentinel attacks; Nygard)
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:63` (WC-5: "`--outcome succeeded` otherwise, including `partial`"); `:263` (Decision: partial maps to succeeded); `:73` (section 2.3 has the coordinator open the report "then release or reuse the worker", not before starting dependents).
- Inventory: `commands-b.md` and `orca-capabilities.md:33-34` (`--deps` and ready waves: Orca does not auto-start ready Tasks, but a settled Task is what unblocks a dependent); `orca-capabilities.md:90` (a failed Task keeps its dependents blocked).
- Note: the "otherwise" rule also covers a missing or unrecognised status, so a malformed report settles as succeeded. A GAP under FR-8; not blocking because the coordinator is expected to open the file (`:73`), but the spec does not require that before dependents start.
- Recommendation: map unlisted or missing status to `failed` for dependency gating, and require the coordinator to read `status` before it starts any dependent Task.

**F-2. AC-0.4 claims a check of WC-7 (no Agent-tool wrapper) that step 5 does not perform.** (Expert: Crispin)
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:194` (AC-0.4: "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)"); `:184` (step 5 searches only for `AskUserQuestion`); `:65` (WC-7).
- Quality impact: a worker that wraps the command in a subagent passes AC-0.4 while breaching WC-7.
- Recommendation: add an explicit check for a subagent or Agent-tool call in the transcript at step 5.

**F-3. Section 7.2 step 2 requires a `worker-show` at least every 5 minutes "while it runs", but step 3 blocks in one `check --wait` of up to 900000 ms.** (Expert: Nygard, Crispin)
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:181` (step 2: "at least once per 5 minutes"; pass: "`observation.agentWait` is never non-null"); `:182` (step 3: "`check --wait ... --timeout-ms 900000`").
- Inventory: `orca-capabilities.md:127` (after three empty waits, run `worker-list`; the guide interleaves the calls).
- Quality impact: as written, step 2 never runs during the blocking wait, so its pass condition ("never non-null") can hold vacuously and a parked worker goes unseen until the 900 s timeout.
- Recommendation: use shorter `check --wait` slices (for example 4 minutes) with a `worker-show` between them.

**F-4. Several requirements have no owner or acceptance check: WC-1, WC-3, WC-6, WC-12, and WC-11 beyond `save`.** (Expert: Wiegers (traceability))
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:59` (WC-1: owner "Launch setup, not commands"); `:61` (WC-3); `:64` (WC-6); `:70` (WC-12); `:69` (WC-11, checked only for `save` at `:207`); `:210` (WC-10, checked only in the conditional AC-4.3). Phases in `:158-162` assign no phase to WC-1, and the checks in `:191-210` do not test it.
- Quality impact: a retry that corrupts output (WC-6), a wrapper that prompts before readiness (WC-1), or a relayed question (WC-3) can pass every acceptance check.
- Recommendation: give WC-1 an owning phase and check, and add an acceptance check for each of WC-3, WC-6 and WC-12.

**F-5. The wait-splitting change for `cli-eval` applies to standalone runs, which SA-1 forbids.** (Expert: Fowler, Wiegers)
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:104` (cli-eval: "split the eval wait into waits of at most 4 minutes (WC-10)"); `:160` (P2 lists WC-10 wait splitting for cli-eval without an unattended condition); `:146` (SA-1: without `--unattended`, every behaviour stays as it is today, with two named exceptions in SA-3).
- Quality impact: a person who runs `/sc:cli-eval run` by hand sees changed wait behaviour, which SA-1 says must not happen.
- Recommendation: scope the wait split to `--unattended`, or add it to SA-1's named exceptions.

**F-6. The outward-action rule for installs is absolute in WC-9, but the post-release row and AC-4.2 handle installs differently.** (Expert: Wiegers, Crispin)
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:67` (WC-9: "installs ... is off"); `:113` (post-release: "VM, real-target install, commit and PR off"; a throwaway install is not mentioned); `:209` (AC-4.2: "no install, VM, commit or PR").
- Quality impact: an implementer cannot tell whether the throwaway venv install that post-release's core check uses is allowed under `--unattended`.
- Recommendation: state whether throwaway installs are allowed and make WC-9, the row and AC-4.2 say the same thing.

**F-7. WC-2 and WC-4 depend on an installed `~/.claude/WORKER-CONTRACT.md` that is refreshed only by `superclaude install`; the spec has no detection or fallback.** (Expert: Newman, Nygard)
- Where: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:52` (contract installed to `~/.claude/WORKER-CONTRACT.md`); `:60` (WC-2 relies on the contract's rules); `:62` (WC-4 report rules).
- Quality impact: on a machine with an older install, the new commands point to a missing or stale contract, the WC-2 rules are absent, and gates stall, which is the failure this spec exists to prevent.
- Recommendation: add a check that the installed contract exists and matches the expected version, and make a command with no contract stop as `blocked` rather than fall back to prompting.

### Architecture notes

Architecture findings beyond F-1 to F-7 (Fowler, Newman, Hohpe, Nygard): the decision in section 1 and the rejected alternative in section 1.3 are sound and supported by `orca-capabilities.md:33-35` and `:97-102` (depth 1); the coordinator-only classification in section 4 matches `commands-a.md:90-92` and `commands-b.md:285-287`. The architectural problems are the shared-directory contract collision (B-4), the report-path rules that cannot be met for timestamped defaults (B-3), and the install-freshness dependency (F-7).

### Minor notes

- **N-1.** WC-10 splits calls "longer than 5 minutes" (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:68`), but the Decision justifies 4 minutes as "a margin under the 5-minute heartbeat cadence" (`:266`). A 4 min 59 s call is unsplit under the rule and close to the heartbeat limit. Boundary unclear.
- **N-2.** `R2-01` (`:182`) is an undefined identifier. Its meaning is inferable from the sentence, but a reader outside the review history cannot check it.
- **N-3.** Citation error. Section 1.2 E2 (`:22`) cites `CAPS:161` for `[H:worker-start]` line 38 (`--agent claude`). In `orca-capabilities.md`, line 161 is the pr-submit top-level bullet (`:161`); the `--agent` statement is at `orca-capabilities.md:136`. The verdict is unaffected.
- **N-4.** Section 1.1 (`:16`) says command changes are "limited to" a worker mode, a report file and resume. Section 3 and SA-4 (`:149`) add drift fixes, tool additions, frontmatter moves and flag reconciliation. The text should say so.
- **N-5.** `pr-submit` is counted in the 27 needs-change commands (`:114`, `:75`) and kept as a worker candidate (`:139`), while D3 recommends coordinator-only (`:240`). The count and the recommendation should agree.
- **N-6.** WC-9 covers outward actions only (`:67`). Cleanup and improve (`:103`, `:110`) and reflect's auto-accept (`:88`) apply local edits under `--unattended`. That is allowed, but the spec does not say so.

## Guard Condition Boundary Table

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | `spec:63` | Zero/Empty (no report file) | no file | failed | `--outcome failed` when no report exists (`:63`) | OK |
| WC-5 outcome mapping | `spec:63`, `:263` | One/Minimal (`status: partial`) | `partial` | succeeded | `succeeded`, dependents may unblock (F-1) | GAP (F-1) |
| WC-5 outcome mapping | `spec:63` | Sentinel (missing, unlisted or malformed status) | absent, `complete` | succeeded | "otherwise succeeded" (`:63`); REPORT.md has no status (`:182`) | GAP (F-1) |
| WC-4 directory | `spec:62` | Missing directory flag (reflect, troubleshoot, workflow rows) | no flag in brief | refused before work | refused, per `:62`; the rows name no flag | GAP (B-3) |
| WC-2 / WC-3 gate resolution | `spec:60-61`, `:109` | Ruling halt (E-HALT-QA) with preamble | halt | blocked, or ask | "may ask" (`:61`) versus "stop" (`:109`, D2a) | GAP (B-1) |
| WC-10 wait threshold | `spec:68`, `:266` | Boundary: single call 4 min to 5 min | 4 min 59 s | not split | split only over 5 min (`:68`); 4-min margin (`:266`) | GAP (N-1) |
| WC-12 ownership fence | `spec:70` | `consumer_fenced` returned by `check` | fenced | stop, no `worker_done` | as stated (`:70`) | OK |
| WC-9 outward default | `spec:67`, `:113`, `:209` | `--unattended` with a throwaway install in post-release | install run | off per `:67` and `:209`; unstated per `:113` | conflicting | GAP (F-6) |
| Section 7.2 step 3 match | `spec:182` | Contract status differs from `--outcome` (`partial`) | partial | succeeded | waiver "R2-01" undefined (`:182`) | GAP (N-2) |
| WC-6 retry | `spec:64` | Retry with no resume flag | same directory | fresh directory | fresh directory per retry (`:64`) | OK |
| WC-7 subagent wrapper | `spec:65`, `:184`, `:194` | Worker wraps command in an Agent-tool subagent | wrapper present | not allowed | step 5 cannot detect it (F-2) | GAP (F-2) |
| WC-11 shared directory | `spec:62`, `:69` | Two dispatches, same directory, contract beside each file | same directory | distinct contracts | WC-4 and WC-11 conflict | GAP (B-4) |

## === ARCHITECTURE ANALYSIS ===

Covered under B-3, B-4, F-7 and the architecture notes above. The section 1 decision (Orca coordinates; commands stay units of work) and the section 5 standalone rule are consistent with the inventories: `orca-capabilities.md:97-102` (depth 1) and `:145-149` (`runtime_unavailable`, no preamble) support section 1.3's rejected alternative and the SA-2 rule.

## Adversarial probes (Whittaker)

- Sentinel collision: the report status field is the only signal for the outcome, and "otherwise succeeded" makes every unlisted value a success (F-1).
- Sequence: a worker that calls `ask` at a halt and then resumes the command is the ordering that B-1 identifies.
- Accumulation: two dispatches that share a directory overwrite one contract (B-4).

## Follow-up candidates

Medium and minor findings are not blocking and do not trigger a revision. The reviewing session asks the user once whether to open an issue for them; none is created here.
- Medium: F-1, F-2, F-3, F-4, F-5, F-6, F-7
- Minor: N-1, N-2, N-3, N-4, N-5, N-6

## Reviser brief

Blocking finding ids: B-1, B-2, B-3, B-4, B-5.

Repair only these blocking findings in the candidate. Revise only text a blocking finding names. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

The gate loop applies: one REVISE pass on these ids, then one RE-REVIEW with this report as PRIOR. A FAIL on that re-review escalates to the user with the open blocking findings.

verdict: FAIL
