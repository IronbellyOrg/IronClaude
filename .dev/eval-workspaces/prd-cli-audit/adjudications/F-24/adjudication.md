# F-24 Adjudication — `check_existing_work` ALREADY_COMPLETE false positive

**Finding**: `src/superclaude/cli/prd/inventory.py:55-59`
**Preliminary severity**: MEDIUM
**Pattern tags**: P7

---

## Re-verification (file:line)

### 1. `check_existing_work` content-free check
`src/superclaude/cli/prd/inventory.py:55-59`:
```python
results_dir = task_dir / "results"
if results_dir.is_dir():
    prd_files = list(results_dir.glob("*.md"))
    if prd_files:
        return ExistingWorkState.ALREADY_COMPLETE
```
**Confirmed**: No frontmatter parse, no `status: Final` requirement, no line-count
threshold, no recency/mtime check, no filename filter (e.g. it does not even
require the file to look like a PRD — any `.md` qualifies, including a stray
`notes.md` or a previous-tier artifact).

### 2. Assembly prompt writes `status: "Draft"` first
`src/superclaude/cli/prd/prompts.py:919-928`:
```
Output path: {config.output_path}
...
CRITICAL -- Incremental File Writing Protocol:
1. FIRST ACTION: Create the output file with PRD frontmatter
   Set status: "Draft", populate created_date, tags, etc.
2. As you assemble each section, IMMEDIATELY write it using Edit
3. Never rewrite from scratch
```
**Confirmed**: The very first edit produces a Draft-status PRD. A crash any
time after that first Edit leaves a Draft `.md` on disk. The trace in F-24 is
correct on the mechanism.

The executor's `_resolve_step_content` docstring confirms subprocesses
"write their real output to disk … at unpredictable locations
(``task_dir/results/``, ``.dev/``, etc.)" — so the assembly subprocess
can and does deposit artifacts into `task_dir/results/`
(`src/superclaude/cli/prd/executor.py:255-265`).

### 3. Downstream effect of ALREADY_COMPLETE
`src/superclaude/cli/prd/executor.py:897-914`:
```python
def _run_check_existing(self) -> PrdStepResult:
    state = check_existing_work(self._config)
    if state == ExistingWorkState.ALREADY_COMPLETE:
        return PrdStepResult(status=PrdStepStatus.SKIPPED)
    ...
    return PrdStepResult(status=PrdStepStatus.PASS)
```

`SKIPPED` semantics in `src/superclaude/cli/prd/models.py:120-153`:
- `is_terminal` → **True** (line 130)
- `is_failure`   → **False** (lines 144-153)
- `is_success`   → **False**

Main run loop in `src/superclaude/cli/prd/executor.py:371-389`:
```python
for step_id, step_name, builder_name, _ in _STAGE_A_STEPS:
    ...
    step_result = self._execute_step(step_id, step_name, builder_name)
    ...
    if step_result.status.is_failure:
        gate = GATE_CRITERIA.get(step_id)
        if gate and gate.enforcement_tier == "STRICT":
            result.outcome = "halt"
            ...
            break
```

**Downstream effect — corrected from the finding's wording**: When step 1
returns `SKIPPED`, the run loop does **not** halt and does **not**
short-circuit. SKIPPED is not `is_failure`, so the `break` branch is
never taken. The pipeline proceeds to step 2 and continues through
Stage A → Stage B → present-complete. The only observable consequence is
that step 1 is marked "skipped" in the TUI/diagnostics, and the
`_context_summaries["check-existing"]` value is the generic
"check-existing: skipped" line written at executor.py:465 (the
RESUME_STAGE_A/_B summaries at lines 904-912 are not assigned in the
ALREADY_COMPLETE branch, but the catch-all at 465 still records the
status string).

This is materially different from the finding's "Already complete" /
"user gets a draft PRD" claim. The pipeline does not return early and
does not present the draft as the final artifact — it simply runs
through every subsequent step.

---

## Persona 1 — Analyzer (reproducibility)

**Scenario**: Crash-truncated draft (`status: "Draft"`, a few sections,
no closing) sits in `task_dir/results/`. User re-runs.

**Trace**:
1. `check_existing_work` finds the matching `TASK-PRD-*` dir
   (inventory.py:78-97), looks at `results/`, sees one `.md`, returns
   `ALREADY_COMPLETE` (inventory.py:55-59).
2. `_run_check_existing` returns `SKIPPED` (executor.py:902).
3. The run loop sees a non-failure status and continues to step 2
   (`parse-request`) and onward (executor.py:371-389).
4. Each subsequent step runs as normal. The assembly step (`14a`) will
   re-execute, instructed to write to `config.output_path` again
   (prompts.py:919). The assembly prompt says "Never rewrite from
   scratch" (line 928), so behaviour now depends on the LLM's
   interpretation when a partial `status: "Draft"` file already exists
   at the output path — it may extend the truncated file, overwrite it,
   or skip portions assuming they are done.
5. Final QA (`14b`/`14c`) and `present-complete` will run regardless,
   reporting their own pass/fail signal.

**Reproducibility**: HIGH for the **first-order** behaviour (the
`SKIPPED` outcome on step 1 — deterministic from a single `.md` in
`results/`). LOW–MEDIUM for the **second-order** behaviour (whether
the final assembled PRD ends up corrupted by the leftover draft) —
that depends on LLM behaviour against the incremental-edit protocol
and is non-deterministic.

**Key correction to the finding's repro sketch**: "Re-run -- gets
'Already complete' with a draft PRD" is **incorrect**. The user does
not get an "Already complete" terminal message; they get a re-run of
steps 2-15 with step 1 silently skipped, and may or may not end up
with a corrupted final artifact depending on what the assembly
subprocess does with the pre-existing draft file.

---

## Persona 2 — Refactorer (blast radius)

Looking for sibling completeness checks that key on file existence
without content validation:

| Location | What it checks | Has content check? |
|---|---|---|
| `inventory.py:55-59` `check_existing_work` (results) | any `*.md` in `results/` → ALREADY_COMPLETE | **No** — bare glob |
| `inventory.py:138-160` `discover_research_files` | `research/*.md` → completion list | **Yes** — non-empty + no `[INCOMPLETE]` marker |
| `inventory.py:163-168` `discover_synth_files` | `synthesis/synth-*.md` | **No** — bare glob, filename prefix only |
| `filtering.py:74` (research filtering loop) | `research/*.md` enumeration | (filtering pass — separate gate) |

**Findings**:
1. `discover_research_files` is the **only** completeness check in the
   PRD module that validates content (non-empty, `[INCOMPLETE]` marker
   skip). The pattern exists in the codebase — F-24's check is the
   outlier.
2. `discover_synth_files` (inventory.py:163-168) has the **same anti-pattern**
   as F-24: any file matching `synth-*.md` is treated as a synthesis
   artifact regardless of whether it is empty or truncated. It feeds
   `build_assembly_prompt` (prompts.py:903-906), so a crash-truncated
   synth file would silently appear in the assembly file list. This is
   a **sibling defect** of the same shape, not previously catalogued by
   F-24.
3. There is no `status: Final` / frontmatter-aware completeness check
   anywhere in `prd/inventory.py` despite frontmatter being parsed
   elsewhere in the same file (`_frontmatter_matches`,
   inventory.py:100-118). The plumbing exists; the
   `check_existing_work` path simply does not use it.

**Blast radius**: 2 functions in `inventory.py` exhibit the
content-free-completion pattern; 1 (`discover_research_files`) does
not. The pattern is local to `inventory.py` — call sites are limited
to `executor.py:899` and `prompts.py:903-905`.

---

## Persona 3 — Architect (severity calibration)

**Original severity**: MEDIUM, on the assumption that ALREADY_COMPLETE
causes a "silent skip of legitimate work" (i.e., user is told the PRD
is done when it is not).

**Corrected impact model** (per Re-verification §3):
- ALREADY_COMPLETE does **not** short-circuit the run; it only marks
  step 1 as `SKIPPED`. All other steps execute.
- The user does **not** see an "Already complete — done" terminal
  message at the top of the pipeline.
- The risk is therefore **not** "silent skip of legitimate work" at
  the pipeline level. It is two narrower risks:
  1. **Misleading status reporting**: the TUI/diagnostics show step 1
     as "skipped" with no context summary explaining why, masking the
     fact that a stale/draft artifact exists in `results/`.
  2. **Cross-talk into step 14a assembly**: a pre-existing
     `status: "Draft"` file at `config.output_path` interacts with the
     "Never rewrite from scratch" rule (prompts.py:928). The
     subprocess may extend a truncated file, leading to a corrupted
     or hybrid PRD. This is the real user-facing harm, and it is
     gated by LLM behaviour, not by the check itself.

**Calibration factors**:

| Factor | Direction | Magnitude |
|---|---|---|
| Likelihood (crash mid-assembly) | ↑ | Moderate — `_signal_handler` exists (executor.py:359), but external crashes (OOM, kill -9, machine reboot) are real |
| User-visible silent failure | ↓ | Pipeline still runs end-to-end; only step 1 is marked skipped |
| Data corruption potential | ↑ | Mid; depends on LLM behaviour against a stale draft at output_path |
| Recovery difficulty | ↓ | Low — user can `rm task_dir/results/*.md` and re-run |
| Sibling defect (`discover_synth_files`) | ↑ | Confirmed same pattern, also unguarded |
| Cost to fix | ↓ | Low — add frontmatter parse + `status: Final` check; mirror `discover_research_files`'s non-empty check |

**Net**: MEDIUM is **slightly hot**. The finding's stated impact
("user gets 'Already complete' with a draft PRD") overstates the
behaviour; the corrected behaviour is "silent SKIPPED on step 1 +
potential assembly corruption", which is meaningful but narrower.
However, the sibling defect in `discover_synth_files` is unflagged
and shares the root cause, so the **systemic** weight of the pattern
holds steady. I land at **MEDIUM (LOW-leaning)** with an explicit
note that the fix should address both inventory.py:55-59 and
inventory.py:163-168 together.

---

## Convergence

| Field | Value |
|---|---|
| **Verdict** | **CONFIRMED (with corrected impact)** |
| **Convergence score** | **0.78** |
| **Final severity** | **MEDIUM (low-leaning)** |
| **Fix difficulty** | **LOW** (small, well-localised) |

**Convergence rationale**: All three personas agree the defect is real
(content-free completeness check at inventory.py:55-59, deterministic
to reproduce on step 1). They diverge on user-visible impact: the
Analyzer trace shows the finding's "user gets a draft PRD" claim is
not accurate — SKIPPED does not short-circuit the pipeline. The
Architect re-calibrates from MEDIUM toward LOW on the basis of that
correction but holds at MEDIUM once the sibling defect in
`discover_synth_files` is folded in (Refactorer evidence).
Convergence score 0.78 reflects unanimous agreement on existence and
fix shape, with the residual disagreement on impact magnitude.

### Synthesis

1. **Root cause**: `check_existing_work` uses raw file existence
   (`results_dir.glob("*.md")`) as a proxy for completion, with no
   frontmatter, status, recency, or content checks. The same anti-pattern
   exists in `discover_synth_files` (inventory.py:163-168).

2. **Real impact** (corrected from finding):
   - Step 1 silently returns `SKIPPED` (not `is_failure`,
     models.py:144-153) so the pipeline continues normally through
     steps 2-15.
   - There is no terminal "Already complete" message presented to
     the user; the user sees a normal end-to-end run with step 1
     marked skipped.
   - The real harm is downstream: the assembly subprocess
     (prompts.py:919-928) is told "Never rewrite from scratch" and
     may extend or interleave with the stale draft file at
     `config.output_path`, producing a corrupted PRD. This harm is
     LLM-behaviour-gated, not deterministic.

3. **Fix shape** (LOW difficulty):
   - In `check_existing_work` (inventory.py:55-59), parse frontmatter
     of the candidate `.md` files (reuse the regex from
     `_frontmatter_matches`, inventory.py:100-118) and require
     `status: Final` (or equivalent). Also apply the same non-empty
     and `[INCOMPLETE]`-marker filter used by
     `discover_research_files` (inventory.py:148-159).
   - Mirror the same hardening in `discover_synth_files`
     (inventory.py:163-168) — strip empty files and files with
     `[INCOMPLETE]` markers from the synthesis input list.
   - Optional: add an mtime check (file newer than the task dir's
     last log entry) to avoid treating stale unrelated `.md` files as
     completion artifacts.

4. **Test surface**: A regression test placing a `status: "Draft"`
   file in `task_dir/results/` should expect a non-ALREADY_COMPLETE
   return value (RESUME_STAGE_B is the natural choice if research and
   synthesis exist; otherwise RESUME_STAGE_A).

### Source citations
- `src/superclaude/cli/prd/inventory.py:55-59` — the defect
- `src/superclaude/cli/prd/inventory.py:163-168` — sibling defect (`discover_synth_files`)
- `src/superclaude/cli/prd/inventory.py:138-160` — counter-example with content check (`discover_research_files`)
- `src/superclaude/cli/prd/inventory.py:100-118` — frontmatter-parse plumbing already in module
- `src/superclaude/cli/prd/executor.py:897-914` — SKIPPED branch
- `src/superclaude/cli/prd/executor.py:371-389` — main run loop, no halt on SKIPPED
- `src/superclaude/cli/prd/models.py:120-153` — SKIPPED is is_terminal but not is_failure
- `src/superclaude/cli/prd/prompts.py:919-928` — assembly writes `status: "Draft"` first
- `src/superclaude/cli/prd/executor.py:255-265` — subprocesses write to `task_dir/results/`
