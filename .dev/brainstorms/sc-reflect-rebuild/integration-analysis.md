# /sc:analyze: Integration of sc:reflect with sprint / roadmap / task pipelines

**Date**: 2026-05-27
**Worktree**: `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2`
**Cross-reference**: `.dev/brainstorms/sc-reflect-rebuild/merged-requirements.md` §14.5 (Wave 7 Promotion Gate)
**Method**: Direct file reads + grep across `src/superclaude/cli/`, `src/superclaude/commands/`, `src/superclaude/skills/`.

---

## Executive Summary

**None of the three pipelines currently invoke `/sc:reflect` as a phase-validation step.** The string "reflect" appears in roadmap-pipeline code only in the unrelated sense of `validate_executor.py`'s adversarial-validation step name (`build_reflect_prompt` — a roadmap-internal "reflection report" for fidelity validation, not the `/sc:reflect` skill). External references to `/sc:reflect --type task --analyze|--validate` exist only in `sc-auggie-review-protocol/refs/remediation-handoff.md` (Phases C/E of the remediation chain) and `sc-troubleshoot-protocol/refs/report-template.md` (Tier 3 post-`/task` recommendation). Neither sprint CLI, roadmap CLI, nor the `task` skill itself wires reflect anywhere in its execution path.

The **highest-leverage single wiring point** is `src/superclaude/cli/sprint/executor.py:1605` (immediately after `notify_phase_complete(phase_result)` at end of each phase) and `:1728` (after `notify_sprint_complete(sprint_result)` at end of sprint) — these are the canonical "phase complete / sprint complete" boundaries with full `PhaseResult` / `SprintResult` context already aggregated, and the §14.5.1 `sprint-release` adapter is explicitly designed to consume `.dev/releases/current/<release>/results/`, which is exactly where `notify_sprint_complete` fires. For `task`, the equivalent point is `src/superclaude/skills/task/SKILL.md:262` (the "mark task Done" decision after structural+qualitative QA), which corresponds to the §14.5.1 `task` adapter (`.dev/tasks/to-do/TASK-*` → `.dev/tasks/done/TASK-*`).

---

## Findings by Pipeline

### Sprint CLI

#### Current state — `/sc:reflect` reference scan

```
$ grep -rn "sc:reflect\|sc-reflect\|/sc:reflect" src/superclaude/cli/sprint/
(no matches)
```

The string `reflect` appears in `src/superclaude/cli/sprint/monitor.py:443` and `src/superclaude/cli/sprint/executor.py:879` only in code comments ("reflects the displayed input tokens", "reflects task_result.turns_consumed") — semantic prose, not the skill. **No reference to `/sc:reflect` exists anywhere in `src/superclaude/cli/sprint/`.**

#### Phase boundaries identified

The sprint pipeline has a clean phase-iteration model centered on `Phase` (data class) and `PhaseResult` (outcome):

| Boundary | File:line | Description |
|---|---|---|
| Sprint entry point | `src/superclaude/cli/sprint/commands.py:189` | `def run(...)` click command — loads config, dispatches to tmux or foreground |
| Sprint orchestrator | `src/superclaude/cli/sprint/executor.py:1135` | `def execute_sprint(config: SprintConfig)` — top-level loop over `config.active_phases` |
| Per-phase execution | `src/superclaude/cli/sprint/executor.py:927` | `def execute_phase_tasks(...)` — runs tasks within a single phase |
| `Phase` class | `src/superclaude/cli/sprint/models.py:282` | Discovered from tasklist index |
| `PhaseResult` class | `src/superclaude/cli/sprint/models.py:159` | Per-phase outcome (re-exported as `PhaseStatus` enum at `:211`) |
| `SprintResult` aggregate | (re-exported via `models.py`) | All phase results + sprint-level outcome |

#### Post-phase / validation hooks (the wiring surface)

The sprint pipeline ALREADY has a well-defined post-phase hook chain. From `src/superclaude/cli/sprint/executor.py` (lines 1567-1605 of `execute_sprint`):

```python
# Line 1567-1574: post-phase wiring hook (anti-instinct integration_contracts check)
phase_result = run_post_phase_wiring_hook(
    phase, config, phase_result,
    ledger=ledger, remediation_log=remediation_log,
)

sprint_result.phase_results.append(phase_result)  # :1576

# Line 1584-1592: async per-phase summary worker (Haiku narrative -> results/phase-N-summary.md)
_summary_worker.submit(phase, phase_result)

# Line 1594-1601: structured debug log
debug_log(_dbg, "phase_complete", phase=phase.number, ...)

# Line 1603-1605: phase logger + notify
logger.write_phase_result(phase_result)
notify_phase_complete(phase_result)   # <-- canonical end-of-phase signal
```

The end-of-sprint hook chain (lines 1654-1728) is:

```python
sprint_result.finished_at = datetime.now(timezone.utc)   # :1655
# ... outcome reconciliation
_summary_worker.wait(timeout=90.0)                        # :1669
RetrospectiveGenerator(config).generate(...)              # :1679 — writes retrospective.md
# ... checkpoint manifest write (:1705-1721)
logger.write_summary(sprint_result)                        # :1727
notify_sprint_complete(sprint_result)                      # :1728 — canonical end-of-sprint signal
```

| Hook name | File:line | Purpose |
|---|---|---|
| `run_post_phase_wiring_hook` | `executor.py:748` (def) / `:1289`, `:1568` (call sites) | Anti-instinct integration_contracts validation |
| `run_post_task_wiring_hook` | `executor.py:458` (def) / `:1043` (call site) | Per-task wiring validation |
| `notify_phase_complete` | `notify.py:34` (def) / `executor.py:1605` (call) | Desktop notification on phase end |
| `notify_sprint_complete` | `notify.py:50` (def) / `executor.py:1728` (call) | Desktop notification on sprint end |
| `RetrospectiveGenerator.generate` | `retrospective.py:345` (def) / `executor.py:1679` (call) | Aggregate `phase-N-summary.md` files into a release retrospective |

#### Results-directory validation entry points

The "results/" directory is the canonical artifact location and lines up exactly with §14.5.1's `sprint-release` adapter trigger (`--scope or --tasklist resolves under .dev/releases/current/<release>/`, "typically `.dev/releases/current/<release>/results/`"):

- `config.results_dir / f"phase-{phase.number}-summary.md"` — written by `SummaryWorker` (executor.py:1582)
- `config.results_dir / f"phase-{phase.number}-diagnostic.md"` — written by `DiagnosticCollector` on failure (executor.py:1619-1621)
- `config.results_dir / "gate-kpi-report.md"` — KPI roll-up (executor.py:1699-1700)
- `config.release_dir / "manifest.json"` — checkpoint manifest (executor.py:1709-1710)
- Retrospective written via `RetrospectiveGenerator(config).write(...)` (`retrospective.py:339`)

`_resolve_release_dir` (`src/superclaude/cli/sprint/config.py:236`) is the authoritative function that returns the path that `sprint-release` adapter would mutate. This is the lock-and-key match: when reflect promotes, it moves exactly the directory this function returns.

#### Cleanest wiring point for reflect-as-validator (per-phase)

**Recommendation**: hook after `notify_phase_complete(phase_result)` at `executor.py:1605` (BEFORE the `status.is_failure` branch at `:1610` so a reflect-detected drift can mark the phase as halted).

Pseudocode insertion (executor.py, after line 1605):

```python
# Line 1606: NEW — optional /sc:reflect phase-validation hook
if config.reflect_per_phase:  # new SprintConfig field, default False
    from superclaude.cli.sprint.reflect_hook import invoke_reflect_per_phase
    reflect_result = invoke_reflect_per_phase(
        phase=phase,
        phase_result=phase_result,
        tasklist_path=phase.file,
        scope_dir=config.results_dir,
        mode="post",
        tier="auto",   # let §5 rubric decide T1 vs T2
    )
    # Honor reflect's promotion-gate verdict for THIS phase
    if reflect_result.status == "failed" or reflect_result.deviation_class == "regression":
        phase_result.status = PhaseStatus.HALT
        sprint_result.halt_reason = f"reflect verdict: {reflect_result.summary}"
```

The hook is opt-in via a new `SprintConfig.reflect_per_phase` flag (matches existing pattern of `shadow_gates`, `stall_action`). Per-phase reflect is high-token (10-25k Tier 2), so default-off; default-on is reserved for end-of-sprint.

#### Cleanest wiring point for reflect-as-promotor (release current→complete)

**Recommendation**: hook AFTER `notify_sprint_complete(sprint_result)` at `executor.py:1728` and BEFORE function return. This is the natural end-of-sprint boundary; all artifacts are flushed, retrospective written, manifest sealed.

Pseudocode insertion (executor.py, after line 1728):

```python
# Line 1729: NEW — end-of-sprint /sc:reflect promotion gate (default-on per §14.5.2)
if sprint_result.outcome == SprintOutcome.SUCCESS and not config.no_reflect:
    from superclaude.cli.sprint.reflect_hook import invoke_reflect_promotion
    promotion_result = invoke_reflect_promotion(
        scope_dir=config.results_dir,         # -> sprint-release adapter resolves to release_dir
        tasklist_path=config.index_path,
        commit_range="HEAD",                  # diff since sprint start (captured at :1655)
        mode="post",
        promote_mode="sprint-release",        # forces §14.5.1 sprint-release adapter
        depth="standard",
    )
    # The §14.5.2 strict gate decides whether to mv release_dir → complete/
    if promotion_result.promotion_action == "moved":
        notify(f"Sprint release promoted: {promotion_result.promotion_destination}")
    elif promotion_result.promotion_action == "rejected":
        # Drift or regression detected — release stays in current/
        sprint_result.outcome = SprintOutcome.PARTIAL  # new enum value if needed
```

This is the canonical Wave 7 wiring point for the `sprint-release` adapter. Source path = `config.release_dir` (resolved by `_resolve_release_dir` at config.py:236); destination path = same parent with `current` → `complete` (per §14.5.1 adapter table). The §14.5.2 8-condition gate (success status, no drift, no regression, no grounding gaps, no input drift) acts as the canonical "should we graduate this release?" decision.

**Critical**: `notify_sprint_complete` writes the final desktop notification at :1728 BEFORE the reflect hook fires. If reflect rejects the promotion, the operator will see the notification first ("Sprint complete!") then the reflect rejection. Consider swapping order so the notification carries the promotion verdict, OR amend `notify_sprint_complete` to consume the reflect outcome.

---

### Roadmap pipeline

#### Current state — `/sc:reflect` reference scan

The grep across `src/superclaude/cli/roadmap/` returns 21 hits for "reflect" — **but every one of them is an internal roadmap-pipeline use of "reflection" as a synonym for "adversarial validation step"**, NOT a call to the `/sc:reflect` skill. The collision exists because both systems use the word "reflect":

| File:line | Internal use |
|---|---|
| `roadmap/validate_prompts.py:7,16,25` | `build_reflect_prompt()` — generates the prompt for `Step(id="reflect")` |
| `roadmap/validate_prompts.py:149` | `build_merge_prompt(reflect_reports: list[str])` — merges N reflection reports |
| `roadmap/validate_executor.py:248,259,289,300,303,305,307,328,337` | "reflect" is the Step ID for single/parallel reflection in roadmap validate |
| `roadmap/remediate_parser.py:22,51,273,275` | Parses `reflect-merged.md` and `reflect-*.md` files (roadmap-internal artifacts) |
| `roadmap/executor.py:3534` | Defaults to `reflect-merged.md` for report path |

**Conclusion**: `roadmap` has its OWN reflection step (a single-agent or N-agent validation pass against fidelity dimensions) which is structurally similar to but operationally distinct from `/sc:reflect` UC-1/UC-2. There is NO invocation of the `/sc:reflect` skill anywhere in the roadmap CLI.

#### Does the generated roadmap artifact include phase-gate definitions?

**Partial yes — milestones have entry/exit criteria, but not formal phase-gates that reference validators.**

From `src/superclaude/examples/roadmap_template.compressed.md:72`:

```markdown
## M{{SC_PLACEHOLDER:N}}: {{SC_PLACEHOLDER:milestone_name}}

**Objective:** {{SC_PLACEHOLDER:milestone_objective}} | **Duration:** {{SC_PLACEHOLDER:duration_estimate}}
| **Entry:** {{SC_PLACEHOLDER:entry_criteria}} | **Exit:** {{SC_PLACEHOLDER:exit_criteria}}
```

The roadmap schema has:
- **Milestones** (`## M{N}: <name>`) with `Entry:` and `Exit:` fields — these are free-text bullet conditions, not structured validator handles.
- **9-column deliverable table** (`#|ID|Title|Description|Comp|Deps|AC|Eff|Pri`) per milestone (line 92) — AC = "semicolon-separated terse testable conditions", machine-parseable strings but not validator references.
- **Integration Points table** per milestone (line 98) — `Wired` column tracks artifact wiring status.
- **Open Questions** subsection (line 105) — milestone-blocking decisions.

**There is NO field in the current schema that names a phase-gate validator (e.g., no `gate_validator: /sc:reflect --type post` field).** Exit criteria are prose strings interpreted by humans/downstream tools.

The downstream tasklist artifact (`tasklist_phase_template.md:136-151`) does have a structured **"Checkpoint: End of Phase {N}"** block with explicit `**Verification:**` and `**Exit Criteria:**` 3-bullet lists, plus a `Checkpoint Report Path` field. This is more structured than the roadmap's milestone exit criteria — but still free-form bullets, no validator reference.

#### Is the schema extensible to add a phase-gate field that references /sc:reflect?

**Yes, with low blast radius.** The roadmap template is markdown-based with a documented "9-column schema" contract (template comment at line 11: "Every milestone deliverable table MUST use the 9-column schema below. Do not add, remove, or reorder columns."). Adding a phase-gate field would NOT touch the 9-column contract — it would add a sibling field next to `Entry:`/`Exit:`. Specifically:

Suggested addition to `roadmap_template.compressed.md:72`:

```markdown
**Objective:** {{...}} | **Duration:** {{...}} | **Entry:** {{...}} | **Exit:** {{...}} | **Gate:** /sc:reflect --mode post --tasklist <tasklist-path>
```

Or a structured form (one line per gate):

```markdown
### Gate — M{{N}}

- **validator**: `/sc:reflect --mode post`
- **inputs**: `--tasklist {{path}} --diff {{milestone_commit_range}} --spec {{spec_path}}`
- **promotion_adapter**: `sprint-release`
- **block_on**: deviation_class in (Drift, Regression)
```

The sentinels (`{{SC_PLACEHOLDER:*}}`) are checked post-generation by `grep -c '{{SC_PLACEHOLDER:' <output-file>` (template comment line 8), so adding new sentinels doesn't break the validation contract — they'd just need to be substituted.

**Trade-off**: tasklist generation (`src/superclaude/cli/tasklist/`) consumes the roadmap; if the schema adds a structured `Gate:` field, tasklist must learn to forward it into `tasklist_phase_template.md`'s `Checkpoint: End of Phase {N}` block. This is a 1-2 day refactor: extend `RoadmapMilestone` model, extend `tasklist_phase_template.md` to render gate metadata, extend `sprint/executor.py` to honor it (consume the gate metadata in the new per-phase reflect hook above).

#### Cleanest wiring point for roadmap

**Two options, both viable:**

1. **Pure-schema (no Python change)**: extend `roadmap_template.compressed.md` to include a `Gate:` annotation per milestone. Downstream tasklist + sprint code consumes it. This is the lowest-blast-radius option but requires three files coordinated (roadmap template, tasklist template, sprint executor).

2. **Schema + roadmap-side validate hook**: the roadmap `validate` subcommand (`roadmap/validate_executor.py`) already does a "reflection" pass against roadmap output. Add a wave-2 cross-validation that ALSO invokes `/sc:reflect --mode pre` against the generated roadmap + the spec, to catch coverage gaps before the operator runs `sc:tasklist`. Insertion point: `roadmap/validate_executor.py:248` (the `_build_steps_single_agent` function — add a step before `id="reflect"` that calls `/sc:reflect --mode pre`).

Recommendation: **option 1 (schema extension) — the roadmap-side validate hook is a duplicate concern with §14.5 promotion-gate**. Roadmap's job is to define gates; reflect's job is to enforce them.

---

### /sc:task command + skill

#### Current state — `/sc:reflect` reference scan

```
$ grep -n "reflect" src/superclaude/commands/task.md src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/commands/task-builder.md src/superclaude/skills/task-builder/SKILL.md src/superclaude/skills/task/SKILL.md
src/superclaude/skills/task-builder/SKILL.md:1284: (only "reflected" prose, no skill reference)
```

**`task.md`, `sc-task-protocol/SKILL.md`, `task-builder/SKILL.md`, and `task/SKILL.md` contain ZERO references to `/sc:reflect` as a skill invocation.** The only mention of reflect in the entire `sc-task` / `task` / `task-builder` surface is the unrelated phrase "task completion items ... are reflected as corresponding" at `task-builder/SKILL.md:1284`.

#### End-of-task hook present?

**Yes — in `src/superclaude/skills/task/SKILL.md`. This is the executor skill, distinct from `sc-task-protocol/SKILL.md` (the unified `/sc:task` command).**

Two complementary end-of-task hook chains exist:

1. **Phase-Gate QA Verification** (`task/SKILL.md:192-222`): after every Phase 2+ in the tasklist, spawn `rf-qa` adversarial agent. PASS / FAIL with-fixes / FAIL-unfixable verdict gates the next phase. Max 3 fix cycles.

2. **Post-Completion Validation** (`task/SKILL.md:224-262`): runs ONCE after the final phase's gate passes, BEFORE marking task "Done". Two adversarial QA agents:
   - `rf-qa` structural validation (`task/SKILL.md:232`) — writes `${TASK_DIR}reviews/qa-final-validation-report.md`
   - `rf-qa-qualitative` operational validation (`task/SKILL.md:242`) — writes `${TASK_DIR}reviews/qa-qualitative-review.md`
   - Both must PASS (or have fixes verified) before frontmatter goes to `status: "🟢 Done"`.

The `sc-task-protocol/SKILL.md` (the unified `/sc:task` command, distinct from `task/SKILL.md`) has a much lighter "Verification Phase" (line 118) routing to direct test execution by tier — no rf-qa, no post-completion adversarial validation. It only invokes `/sc:forensic` on test-failure escalation (TFEP, line 212).

#### Final-step semantics

The `task/SKILL.md` skill's final-step decision (`task/SKILL.md:256-262`):

> **Handling verdicts:**
> - Both PASS → proceed to mark task "Done"
> - Either FAIL with all fixes applied → verify fixes, then proceed
> - Either FAIL with unfixable issues → log issues, present to user, ask for guidance before marking done
>
> **Read both QA reports. If any issues found (CRITICAL, IMPORTANT, or MINOR), verify fixes were applied correctly. If issues remain unfixed, address ALL of them before marking the task done. Zero leniency — no severity level is exempt.**

Frontmatter "task completion" event (`task/SKILL.md:179`) is then: `status: "🟢 Done", completion_date: [today], updated_date: [today]`.

The `task-builder/SKILL.md:1930-1932` corresponds — task completion item is `N.X — Update task status to Done` whose action is `Update frontmatter: status to "🟢 Done", set completion_date.`

**Critical observation**: `task/SKILL.md` does NOT move the task folder from `.dev/tasks/to-do/TASK-*` to `.dev/tasks/done/TASK-*`. It only updates the frontmatter `status` field. The §14.5.1 `task` adapter is therefore a NEW capability — currently no code moves the directory. The "to-do/" and "done/" filesystem layout is a convention the user maintains manually (likely via `git mv` or shell).

#### Cleanest wiring point for reflect-as-final-QA

**Recommendation**: insert reflect AS the Post-Completion Validation step (Step 3, after the existing structural + qualitative QA agents at `task/SKILL.md:240`-262), OR replace the entire Post-Completion Validation block with `/sc:reflect --mode post`.

Two variants:

**Variant A (additive, lower risk)**: keep `rf-qa` + `rf-qa-qualitative`, ADD `/sc:reflect` as Step 3 of Post-Completion. Inside `task/SKILL.md`, after line 252 (`qa-qualitative-review.md` output path), insert:

```markdown
**Step 3: /sc:reflect promotion gate (§14.5)**

After both structural and qualitative QA pass, spawn /sc:reflect as the final canonical gate:

- **Command**: `/sc:reflect --mode post --tasklist ${TASK_FILE} --diff HEAD~N..HEAD --output ${TASK_DIR}reflect/`
- **Purpose**: independent, heterogeneous-reviewer audit of the entire executed tasklist against its driving spec. Verifies 100% completion, classifies deviations under the §10 taxonomy, and (when --no-promote not set) automatically moves the task folder from `.dev/tasks/to-do/TASK-*` to `.dev/tasks/done/TASK-*` per the §14.5.1 `task` adapter.
- **Verdict handling**:
  - `status: success` AND `promotion_action: moved` → task is automatically promoted; mark frontmatter `🟢 Done` (already done by the move).
  - `status: success` AND `promotion_action: skipped` (e.g., user passed --no-promote) → mark frontmatter `🟢 Done` manually.
  - `status: partial` with non-empty deviation register → present reflect report to user, ask for guidance.
  - `status: failed` → halt; do NOT mark Done.
```

**Variant B (replacement, higher leverage)**: replace `task/SKILL.md:224-262` (the entire "Post-Completion Validation" section) with a single `/sc:reflect --mode post` call that subsumes both rf-qa passes via reflect's Wave 3 heterogeneous reviewer ensemble. This consolidates structural+qualitative+coverage+deviation-taxonomy into ONE adversarial pass. The trade-off: reflect's reviewers run on different model classes (haiku/sonnet/qwen), which is more rigorous than two same-model rf-qa calls — but the existing rf-qa machinery already works, and reflect is new + unproven.

**Recommendation**: Variant A initially (additive, safe), with Variant B as a follow-on once reflect proves out across `.dev/eval-workspaces/sc-reflect/evals/`.

For `sc-task-protocol/SKILL.md` (the lighter `/sc:task` unified command), reflect should be wired into the STRICT tier's Verification Phase (line 118-127 table) as a new row:

| Compliance Tier | Verification Method | Token Cost | Timeout |
|---|---|---|---|
| STRICT | Sub-agent (quality-engineer) **+ /sc:reflect --mode post** | 3-5K **+ 10-70K** | 60s **+ 10min** |

This makes reflect default-on for STRICT, opt-in for STANDARD via `--verify reflect`.

---

## Cross-Pipeline Recommendation

Three concrete changes, mapped to §14.5 of the rebuild spec:

### Change 1 — Sprint CLI: end-of-sprint reflect promotion gate (HIGH priority)

**File**: `src/superclaude/cli/sprint/executor.py`
**Insertion**: after line 1728 (`notify_sprint_complete(sprint_result)`), before function return at end of `execute_sprint`.
**New module**: `src/superclaude/cli/sprint/reflect_hook.py` (thin wrapper that spawns `/sc:reflect` via the standard claude-subprocess pattern used elsewhere in the sprint CLI).
**Config addition**: `SprintConfig.reflect_promote: bool = True` (default-on per §14.5.2), `SprintConfig.no_promote: bool = False`, mirror CLI flag `--no-reflect-promote` in `commands.py:189`.
**Rationale**: closes the loop `sprint run` → `notify_sprint_complete` → `/sc:reflect --mode post --promote-mode sprint-release` → release graduated from `current/` to `complete/`. Matches §14.5.1 adapter table exactly.

### Change 2 — Roadmap schema: add structured Gate annotation per milestone (MEDIUM priority)

**Files**:
- `src/superclaude/examples/roadmap_template.compressed.md:72` — add `**Gate:**` field to milestone header line.
- `src/superclaude/cli/roadmap/spec_parser.py` — parse new field into milestone model.
- `src/superclaude/cli/roadmap/models.py:94` — extend roadmap model (currently `RoadmapConfig`; need to find/add a per-milestone model).
- `src/superclaude/examples/tasklist_phase_template.md:136` — render gate metadata into End-of-Phase Checkpoint block.
**Schema addition**: per-milestone `Gate:` field naming the validator + invocation flags.
**Rationale**: makes the gate machine-readable so the sprint CLI (Change 1) can pick the right reflect invocation per phase from the roadmap-generated tasklist, rather than hardcoding `/sc:reflect --mode post --promote-mode sprint-release` for every sprint.

### Change 3 — Task skill: wire /sc:reflect as Post-Completion Step 3 (HIGH priority)

**File**: `src/superclaude/skills/task/SKILL.md`
**Insertion**: after line 252, before line 256 (the "Handling verdicts" block), add new Step 3 (Variant A pseudocode above).
**File**: `src/superclaude/skills/sc-task-protocol/SKILL.md`
**Insertion**: extend STRICT row of Verification Phase table at line 122-128 to chain `/sc:reflect --mode post` after the quality-engineer sub-agent.
**Rationale**: matches §14.5.1 `task` adapter. Currently there is NO code that moves `.dev/tasks/to-do/TASK-*` → `.dev/tasks/done/TASK-*`; reflect's Wave 7 promotion becomes the canonical promoter. The existing rf-qa + rf-qa-qualitative validation remains as a pre-filter; reflect adds the cross-model heterogeneous-reviewer ensemble + the §10 deviation taxonomy + the automatic folder move.

---

## Open Questions / Trade-offs

1. **Per-phase reflect cost in sprint**: §15 of merged-requirements puts Tier 2 reflect at 35-70k Claude tokens + 10-25k auggie. A 6-phase sprint would burn 200-400k tokens just on per-phase reflect at default-on. Recommendation: default per-phase reflect to OFF, default end-of-sprint reflect to ON. Open question: should per-phase reflect use Tier 1 (3-8k) by default?

2. **Notification ordering in sprint**: `notify_sprint_complete` at `executor.py:1728` currently fires BEFORE any reflect hook. If reflect rejects promotion, the operator gets a misleading "sprint complete" notification first. Should reflect be hoisted BEFORE `notify_sprint_complete`, or should `notify_sprint_complete` accept a `promotion_status` arg?

3. **Roadmap schema gate format**: the `Entry:` / `Exit:` field at template line 72 is a single inline string. Adding a `Gate:` field of similar form is low-risk; adding a structured multi-line block (the second option in the Roadmap section) is more rigorous but requires parser changes. Which form does the user prefer?

4. **task-builder generated frontmatter promotion**: `task-builder/SKILL.md:1930` generates a "Update task status to Done" checklist item at the END of the final phase. If reflect's Wave 7 promotion runs automatically via the `task` skill's Post-Completion Step 3, does the task-builder-generated final item conflict (try to update status after the folder has already moved)? Recommendation: task-builder should generate a "Done" status item that runs BEFORE the spawned reflect call, and reflect's promotion gate verifies the frontmatter agrees (gate condition 4 in §14.5.2).

5. **Sprint `release_dir` resolution vs §14.5.1 adapter glob**: `sprint/config.py:236` (`_resolve_release_dir`) resolves the release dir from the index path. §14.5.1 adapter specifies source path glob `.dev/releases/current/<release>/`. Need to verify (manual check) that `_resolve_release_dir` always returns a path matching this glob — otherwise the `sprint-release` adapter won't fire. The integration must either (a) document a convention that sprint indexes always live under `.dev/releases/current/<release>/...`, or (b) extend the adapter glob to handle alternative layouts.

6. **rf-qa vs reflect overlap**: `task/SKILL.md`'s rf-qa + rf-qa-qualitative passes already do adversarial validation. Reflect's Wave 3 heterogeneous reviewers cover similar ground. Risk: doing both is 2-3× the token cost of doing one well. Open question: should Variant B (replace rf-qa with reflect) be the target end-state, or is Variant A (additive) the permanent shape?

7. **`/sc:task` (unified, sc-task-protocol) vs `/task` (executor, `task/SKILL.md`) confusion**: these are two different surfaces. `/sc:task` (commands/task.md → sc-task-protocol) does inline classification + tier-routed execution. `/task` (skills/task → task/SKILL.md) executes a pre-built MDTM task file via the F1 loop. They have DIFFERENT verification chains. Wiring reflect into both is the right move (both surfaces touch end-of-task), but document which is which to avoid downstream agent confusion.

---

## Severity Summary

- **HIGH (must wire)**:
  - Sprint CLI end-of-sprint promotion gate (Change 1) — directly satisfies §14.5.1 `sprint-release` adapter; closes the `releases/current/` → `releases/complete/` graduation loop.
  - Task skill Post-Completion Step 3 (Change 3) — directly satisfies §14.5.1 `task` adapter; currently NO code performs the `to-do/` → `done/` move, so reflect becomes the canonical promoter.

- **MEDIUM (should wire)**:
  - Roadmap schema Gate annotation (Change 2) — enables machine-readable gate metadata for downstream consumers. Lower priority because Change 1 + Change 3 can hardcode invocations initially.
  - `sc-task-protocol/SKILL.md` STRICT-tier reflect chain — extends the unified `/sc:task` command. Lower priority because the heavier rf-qa-based `task` skill is the main vector for high-stakes task execution.

- **LOW (nice to wire)**:
  - Per-phase reflect hook in sprint (insertion after `executor.py:1605`) — high token cost, default-off; useful for safety-critical sprints but not load-bearing.
  - Roadmap-side `/sc:reflect --mode pre` cross-validation in `validate_executor.py` — risks duplicating roadmap's internal reflection step; skip unless gap analysis shows it adds unique value.
  - Move `notify_sprint_complete` AFTER reflect verdict (or thread the verdict through it) — UX polish, not functionality.
