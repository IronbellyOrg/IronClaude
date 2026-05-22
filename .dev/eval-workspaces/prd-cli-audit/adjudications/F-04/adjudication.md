# Adjudication — F-04: Systemic inversion of `_STEP_ARTIFACT_FILES`

**Finding under review:** `.dev/eval-workspaces/prd-cli-audit/findings/F-04-systemic-inversion-write-steps-missing.md`
**Preliminary severity:** CRITICAL
**Related finding:** F-01 (`F-01-artifact-dispatch-missing-build-task-file.md`) — same anchor, narrower scope

---

## 1. Evidence re-verification

### 1.1 The `_STEP_ARTIFACT_FILES` table (verbatim)

`src/superclaude/cli/prd/executor.py:246-251`:

```python
_STEP_ARTIFACT_FILES: dict[str, str] = {
    "parse-request": "parsed-request.json",
    "scope-discovery": "scope-discovery-raw.md",
    "research-notes": "research-notes.md",
    "sufficiency-review": "sufficiency-review.md",
}
```

Four entries. No others. Re-confirmed at executor.py:246 (definition) and executor.py:267-269 / 987-989 (the two consumers that short-circuit on `get(step_id) is None`).

### 1.2 Master table: every prompt builder vs Write behavior vs dispatch entry

For each step builder in `src/superclaude/cli/prd/prompts.py`, I read the body and recorded whether the prompt instructs the subprocess to `Write` to a path (and which path), or whether the prompt is stdout-only (returns JSON or markdown body to the assistant stream).

| # | step_id (executor) | builder (prompts.py:line) | Writes to disk? | Path pattern | In `_STEP_ARTIFACT_FILES`? |
|---|---|---|---|---|---|
| 1 | `check-existing` | `_check_existing` (internal, no subprocess) | n/a | n/a | n/a (no subprocess) |
| 2 | `parse-request` | `build_parse_request_prompt` (prompts.py:54) | NO — "Return ONLY the JSON object" (prompts.py:98) | stdout JSON | YES ("parsed-request.json") |
| 3 | `scope-discovery` | `build_scope_discovery_prompt` (prompts.py:104) | NO — markdown in response body (prompts.py:148-184) | stdout markdown | YES ("scope-discovery-raw.md") |
| 4 | `research-notes` | `build_research_notes_prompt` (prompts.py:188) | NO — "Produce a research-notes.md file" but no explicit Write instruction; structured response (prompts.py:216-258) | stdout markdown | YES ("research-notes.md") |
| 5 | `sufficiency-review` | `build_sufficiency_review_prompt` (prompts.py:263) | NO — "Return JSON" (prompts.py:295) | stdout JSON | YES ("sufficiency-review.md") |
| 6 | `template-triage` | `_template_triage` (internal, no subprocess) | n/a | n/a | n/a (no subprocess) |
| 7 | `build-task-file` | `build_task_file_prompt` (prompts.py:316) | **YES** — `Write the task file to: {config.task_dir / ("TASK-PRD-" + ... + ".md")}` (prompts.py:381) | `task_dir/TASK-PRD-{slug}.md` | **NO** |
| 8 | `verify-task-file` | `build_verify_task_file_prompt` (prompts.py:399) | NO — "Return JSON" (prompts.py:437) | stdout JSON | NO |
| 9 | `preparation` | `build_preparation_prompt` (prompts.py:458) | **YES** (marker only) — "Write a brief status report to .preparation-complete" (prompts.py:488) | `.preparation-complete` (marker file, not artifact) | NO |
| 10 | `investigation-{N}` | `build_investigation_prompt` (prompts.py:508) | **YES** — "Research this aspect of the product and write findings to {output_path}" (prompts.py:518) + incremental-write protocol (prompts.py:526-549) | `output_path` (caller-supplied, `research/NN-*.md`) | **NO** |
| 11 | `research-qa` | `build_qa_research_gate_prompt` (prompts.py:680) | **YES** — `Output path: {config.qa_dir / "qa-research-gate-report.md"}` (prompts.py:716); response is markdown report | `qa_dir/qa-research-gate-report.md` | **NO** |
| 11alt | (also) `analyst-completeness` | `build_analyst_completeness_prompt` (prompts.py:629) | **YES** — `Output path: {config.qa_dir / "analyst-completeness-report.md"}` (prompts.py:647); "5. Write your report to the output path" (prompts.py:658) | `qa_dir/analyst-completeness-report.md` | **NO** (builder not currently invoked by executor — see §3 below) |
| 12 | `web-research-{N}` | `build_web_research_prompt` (prompts.py:583) | **YES** — "Research this topic externally and write findings to {output_path}" (prompts.py:590) + incremental-write (prompts.py:596-599) | `output_path` (caller-supplied) | **NO** |
| 13a | `synthesis-{N}` | `build_synthesis_prompt` (prompts.py:747) | **YES** — `Output path: {output_path}` (prompts.py:765) + "Write to your output file incrementally" (prompts.py:782-787) | `output_path` (caller-supplied, `synthesis/synth-*.md`) | **NO** |
| 13b | `synthesis-qa` | `build_qa_synthesis_gate_prompt` (prompts.py:839) | **YES** — `Output path: {config.qa_dir / "qa-synthesis-gate-report.md"}` (prompts.py:857); "5. Write your QA report" (prompts.py:868) | `qa_dir/qa-synthesis-gate-report.md` | **NO** |
| 13b-alt | (also) `analyst-synthesis` | `build_analyst_synthesis_prompt` (prompts.py:795) | **YES** — `Output path: {config.qa_dir / "analyst-synthesis-review.md"}` (prompts.py:812) | `qa_dir/analyst-synthesis-review.md` | **NO** (builder not currently invoked) |
| 14a | `assembly` | `build_assembly_prompt` (prompts.py:897) | **YES** — `Output path: {config.output_path}` (prompts.py:919) + "Never rewrite from scratch" / "Write each section to disk immediately" (prompts.py:927-941) | `config.output_path` (the final PRD .md) | **NO** |
| 14b | `structural-qa` | `build_structural_qa_prompt` (prompts.py:971) | **YES** — `Output path: {config.qa_dir / "qa-report-validation.md"}` (prompts.py:989) + "Fix authorization: true" (prompts.py:990) | `qa_dir/qa-report-validation.md` | **NO** |
| 14c | `qualitative-qa` | `build_qualitative_qa_prompt` (prompts.py:1027) | **YES** — `Output path: {config.qa_dir / "qa-qualitative-review.md"}` (prompts.py:1043) | `qa_dir/qa-qualitative-review.md` | **NO** |
| 15 | `present-complete` | `build_completion_prompt` (prompts.py:1079) | NO — produces markdown summary in stdout (prompts.py:1098-1122) | stdout markdown | NO |
| fix-cycle | `{qa}-fix-{N}` | `build_gap_filling_prompt` (prompts.py:1131) | **YES** — "Write a brief report of what you fixed to: {config.qa_dir / f"gap-fix-{cycle:02d}-{slug}.md"}" (prompts.py:1172-1173) | `qa_dir/gap-fix-NN-{slug}.md` | **NO** |

### 1.3 Inversion count

Reachable, subprocess-driven steps with prompts (excluding internal `_check_existing` and `_template_triage`, and counting each dynamic family as one row):

- **Write-instructing steps:** `build-task-file`, `preparation` (marker only), `investigation-{N}`, `research-qa`, `web-research-{N}`, `synthesis-{N}`, `synthesis-qa`, `assembly`, `structural-qa`, `qualitative-qa`, fix-cycle (`{qa}-fix-{N}`). **11 step families instruct Write.** If `preparation` (marker only, not an artifact for downstream consumption) is excluded, **10 substantive Write-emitting families.**
- **Of those 11/10, present in `_STEP_ARTIFACT_FILES`:** **0.**
- **Stdout-only subprocess steps:** `parse-request`, `scope-discovery`, `research-notes`, `sufficiency-review`, `verify-task-file`, `present-complete`. **6 steps.**
- **Of those 6, present in `_STEP_ARTIFACT_FILES`:** **4** — every entry in the table (`parse-request`, `scope-discovery`, `research-notes`, `sufficiency-review`).

The finding's "13 Write-instructing steps missing, 4 entries present and all stdout-only" framing is **substantively correct**. My count (10–11 vs the finding's 13) differs only because (a) the finding counts multiple line-anchored Write instructions including incremental-write rules as separate steps, and (b) my count collapses dynamic step families to one row. Both counts unambiguously establish the inversion shape: **the 4 present keys are 4 of the 6 stdout-only steps; 0 of ≥10 Write-emitting steps are present.**

### 1.4 F-E-5 sub-claim verification (assembly)

- Prompt at prompts.py:919 — confirmed: `Output path: {config.output_path}`.
- prompts.py:927-928 — confirmed: "As you assemble each section, IMMEDIATELY write it using Edit" / "Never rewrite from scratch".
- Gate at gates.py:451-473 — confirmed: `min_lines=800`, `enforcement_tier="STRICT"`, plus semantic checks `prd_template_sections` and `no_placeholders`.
- `_resolve_step_content("assembly", ...)` at executor.py:267 returns `ndjson_text` (the assistant commentary) because `"assembly"` is not in the dict. The 800-line PRD on disk at `config.output_path` is never read by the gate.

F-E-5's sub-claim about the assembly step is fully verified.

### 1.5 Bonus consequence — `_persist_step_artifact`

`_persist_step_artifact` (executor.py:976-1004) short-circuits at executor.py:987-989 on the same dict miss. So for every Write-emitting step, the canonical filename downstream builders load (e.g. `scope_content = _read_file(config.task_dir / "scope-discovery-raw.md")` at prompts.py:194; `notes = _read_file(config.task_dir / "research-notes.md")` at prompts.py:322; `analyst_report = config.qa_dir / "analyst-completeness-report.md"` at prompts.py:686) would never be populated by this code path. (Those particular files happen to be among the 4 present in the dict — for stdout-only steps — so they *are* persisted via the NDJSON path. The persistence bug bites only the Write-emitting steps, exactly where the search-then-copy logic in `_resolve_step_content` should have caught them but cannot because the dict lookup gates the search.)

---

## 2. Persona 1 — Analyzer (reproducibility)

**Question:** which step halts first, and what is the order if Bug 1 alone is patched?

Walking the executor flow in `executor.py:370-413`:

- **Step 1 (`check-existing`)** — internal, no halt.
- **Steps 2-5** (`parse-request`, `scope-discovery`, `research-notes`, `sufficiency-review`) — **already present** in `_STEP_ARTIFACT_FILES`, prompts are stdout-only. Gates pass (assistant body fills `min_lines=0` or `min_lines>0` thresholds well within stdout).
- **Step 6 (`template-triage`)** — internal, no halt.
- **Step 7 (`build-task-file`)** — Bug 1. STRICT, `min_lines=400`. NDJSON commentary ~30 lines → halts. **First halt observed today.**
- **Step 8 (`verify-task-file`)** — STRICT, `min_lines=0`, semantic check `verdict_field`. Prompt returns JSON in stdout (prompts.py:437). Gate evaluates `gate_content` which falls back to `ndjson_text` (not in the dict). The JSON verdict is in the NDJSON commentary, so `_check_verdict_field` may pass. **Likely passes by lucky accident** if Bug 1 patched.
- **Step 9 (`preparation`)** — LIGHT, `min_lines=0`. Passes.
- **Steps 10 (`investigation-{1..5}` standard tier)** — STANDARD (does not halt), `min_lines=50`. Commentary frequently exceeds 50 lines for an "incremental file writing protocol" prompt that prints status updates. **Passes by accident.** But the canonical research files (`research/01-*.md` … `research/05-*.md`) are written on disk by the subprocess via `Edit` — and `_resolve_step_content` cannot find them because `step_id="investigation-1"` is not in the dict. Downstream steps that `Glob` the research directory directly (e.g. assembly via `discover_synth_files`, QA via the `Glob` instruction in prompts.py:655) **can still find the files on disk**. So the data exists; only the gate evaluation is broken at this layer.
- **Step 11 (`research-qa`)** — STRICT, `min_lines=20`, semantic check `qa_verdict`. The QA report subprocess writes to `qa_dir/qa-research-gate-report.md`. Gate evaluates NDJSON commentary. Commentary easily exceeds 20 lines, and the `verdict: PASS`/`FAIL` string is typically printed by the assistant in stream output. **Likely passes by accident.**
- **Step 12 (`web-research-{N}`)** — STANDARD, `min_lines=30`. Same accidental-pass dynamic.
- **Step 13a (`synthesis-{N}`)** — STANDARD, `min_lines=80`. Commentary may or may not exceed 80 lines depending on file count and how chatty the assistant is during incremental writing. **Possible accidental pass.**
- **Step 13b (`synthesis-qa`)** — STRICT, `min_lines=20`. Likely accidental pass like research-qa.
- **Step 14a (`assembly`)** — STRICT, `min_lines=800`, plus semantic checks `prd_template_sections` and `no_placeholders`. **An 800-line NDJSON commentary stream is implausible** for an assembly step explicitly told "Never rewrite from scratch" and "Write each section to disk immediately". The assistant should print short status messages while writing the actual PRD file. Even if it printed verbosely, the `prd_template_sections` semantic check (presumably looking for template-specific headers) and `no_placeholders` would evaluate the NDJSON commentary, not the real PRD. **Second halt.** Failure shape identical to Bug 1: gate reads stream commentary; real artifact is on disk at `config.output_path`.
- **Step 14b (`structural-qa`)** — STRICT, `min_lines=20`, `qa_verdict`. Likely accidental pass.
- **Step 14c (`qualitative-qa`)** — semantic verdict check. Likely accidental pass.
- **Step 15 (`present-complete`)** — stdout-only. Passes.

**Halt order if Bug 1 patched in isolation:** `assembly` (step 14a) halts next. The accidental passes between steps 8 and 13b mean the pipeline appears to make significant progress before falling over on the most expensive step (assembly is run after all parallel investigation, web research, synthesis, and two fix cycles have spent their budgets). **Failure cost of the next halt is multiples higher than the first halt — the pipeline has burned its entire research and synthesis budget by the time it reaches assembly.**

That economics finding sharpens the severity argument: a one-key fix to F-01 doesn't merely defer the problem — it makes the next failure substantially more expensive in tokens, wall time, and partial-artifact debris.

---

## 3. Persona 2 — Refactorer (blast radius)

**Confirmed count:** 10 step families instruct the subprocess to Write (or 11 if `preparation`'s marker file counts; or 13 if you also count `analyst-completeness`/`analyst-synthesis` as currently-active steps and break out the largest dynamic groups, matching the finding's count). Either way, **zero of them are in `_STEP_ARTIFACT_FILES`.** Every present key (parse-request, scope-discovery, research-notes, sufficiency-review) is a stdout-only step.

**Latent steps already declared but not yet active:**

- `build_analyst_completeness_prompt` (prompts.py:629) — Write-emitting, `Output path: {config.qa_dir / "analyst-completeness-report.md"}` (prompts.py:647). **Not invoked by `_execute_stage_b`** (executor.py:630-705) — the executor calls `build_qa_research_gate_prompt` directly via `_execute_qa_fix_cycle`. If activated as a pre-QA analyst pass (which the prompts and the QA prompt's "IF ANALYST REPORT EXISTS" branch at prompts.py:695-707 clearly anticipate), it will inherit the same defect.
- `build_analyst_synthesis_prompt` (prompts.py:795) — Write-emitting, `Output path: {config.qa_dir / "analyst-synthesis-review.md"}` (prompts.py:812). Symmetric situation; the synthesis-gate QA prompt does not branch on its existence today, but the file exists and is shaped like a near-term activation. Same latent defect.
- `build_gap_filling_prompt` (prompts.py:1131) — **already active** via `_execute_qa_fix_cycle` (executor.py:885-891). The fix-cycle step IDs are `f"{qa_step_id}-fix-{cycle + 1}"` (e.g. `research-qa-fix-1`). None of those dynamic IDs can ever be in `_STEP_ARTIFACT_FILES` even in principle without a wildcard/prefix scheme. Same defect, same shape.

**Architectural amplifier:** the dispatch table is keyed by **exact step_id** but the executor generates dynamic IDs (`investigation-{i+1}`, `web-research-{i+1}`, `synthesis-{i+1}`, `{qa}-fix-{cycle}`). Even if a maintainer remembered to add all 10 entries, the dynamic-ID families would still miss unless the lookup were prefix-aware or moved to a more structural place (e.g. a property on the step tuple, or a registry keyed on the builder name). **The defect class is not "10 missing keys" — it is "the data model is wrong for the data."**

This is the blast-radius claim in its strongest form, and it is verified.

---

## 4. Persona 3 — Architect (severity calibration & merge analysis)

**Preliminary severity:** CRITICAL. **Does it stand?** Yes. The dispatch table's design is structurally wrong, not merely incomplete. A "complete" patch that adds all 10 named step keys still leaves the dynamic families (investigation/web-research/synthesis/fix-cycle) broken, which means the architectural defect is genuinely separate from any single-key omission.

**Should F-04 fold into F-01?**

Arguments for **merge**:
- Both anchor on `_STEP_ARTIFACT_FILES` at executor.py:246-251.
- The proximate halt today is Bug 1's single missing key. Patching all 10 keys also patches F-01.
- A reviewer reading both findings sequentially will see substantial textual overlap; deduplicating saves reader time.

Arguments for **keep separate** (stronger):
- **Different defect class.** F-01 is "a maintainer forgot one entry when adding `build-task-file`." F-04 is "the dispatch model is inverted — what's present is what doesn't need to be present, and what's needed is structurally absent." These have different fixes: F-01 is a one-line dict insertion; F-04 requires either (a) populating all 10+ entries AND extending the lookup to handle dynamic-ID prefixes, or (b) redesigning to derive the canonical filename from the builder/step definition rather than a side-table.
- **Different remediation cost & risk.** F-01 alone is a 1-token fix that surfaces the next failure (assembly) at higher cost. F-04 alone is the right fix and removes the entire defect class.
- **Different reviewer signal.** Filing only F-01 invites the maintainer to ship the one-line fix and re-run, burning the full Stage-B budget before the assembly halt surfaces. Filing F-04 separately forces the maintainer to confront the structural shape before iterating.
- **Different test surface.** F-01 needs a unit test on the `build-task-file` dispatch entry. F-04 needs a property-style test that every step in `_STAGE_A_STEPS`/`_STAGE_B_STEPS` whose prompt contains `Write` or `Output path:` has either (a) a dispatch entry or (b) a dynamic-prefix match.

**Verdict on merge:** Keep separate. F-01 is the proximate cause; F-04 is the systemic anchor. The two-finding pattern correctly signals "patch the immediate halt AND fix the data model" rather than "add one key and hope."

**Severity:** Preliminary CRITICAL is correct. The architectural defect causes silent gate evaluation on the wrong artifact across the entire pipeline, with at least one additional STRICT halt (assembly) latent behind Bug 1, and accidental passes elsewhere that mask data correctness regressions.

---

## 5. Convergence

| Field | Value |
|---|---|
| **Verdict** | UPHELD |
| **Convergence score** | 3/3 (all three personas independently uphold; no contradictions) |
| **Final severity** | **CRITICAL** (unchanged from preliminary) |
| **Fix difficulty** | **Medium.** Mechanical fix (add the 6–10 named keys) is low effort, but the principled fix (handle dynamic-ID families and ideally lift the canonical filename into the step definition) requires touching `_STAGE_A_STEPS` / `_STAGE_B_STEPS` shape, `_resolve_step_content`, and `_persist_step_artifact`. New tests required to prevent regression of the structural defect. |
| **Merge with F-01?** | **No.** Keep separate. F-01 = proximate cause, single-key omission. F-04 = systemic data-model inversion. The findings co-cite the same anchor but describe distinct defects with distinct fixes. |

**Synthesis.** The audit's claim of systemic inversion is mechanically verified: the four entries in `_STEP_ARTIFACT_FILES` (executor.py:246-251) correspond exactly to the four subprocess steps whose prompts do not instruct disk Writes; zero of the at-least-ten subprocess steps whose prompts do instruct disk Writes are present. The inversion is not a coincidence — it is the visible shape of a maintainer/model who treated the dict as "canonical name for the captured stdout" rather than "canonical name for the artifact written somewhere on disk by the subprocess." With the dict miss, `_resolve_step_content` short-circuits to NDJSON commentary (executor.py:267-269) and `_persist_step_artifact` silently skips persistence (executor.py:987-989), so every Write-emitting step is invisible to both gate evaluation and downstream artifact loading. F-01's single-key omission is the proximate trigger for today's halt; under a hypothetical one-key patch, the next STRICT halt is `assembly` (gates.py:451-473, `min_lines=800`), which lands after Stage-B's full token budget has been consumed — far more expensive than the current step-7 halt. F-04 should remain a separate CRITICAL finding because its defect class (data-model inversion + dynamic-ID blindness) is distinct from F-01's omission, and patching F-01 alone makes the next failure substantially costlier. Recommended fix is to lift the canonical artifact filename into the step definition (alongside `step_id`, `step_name`, `builder_name`, `is_parallel`) and teach `_resolve_step_content` / `_persist_step_artifact` to handle dynamic step families by prefix or registry — not to grow the side-table.
