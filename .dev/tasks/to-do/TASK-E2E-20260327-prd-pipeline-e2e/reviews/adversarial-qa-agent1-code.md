# Adversarial QA Report — Code & Implementation Focus

**Date:** 2026-03-28
**Phase:** Code review of TDD + PRD integration work streams
**Fix authorization:** REPORT ONLY

---

## Overall Verdict: FAIL

---

## Issues Found

### 1. IMPORTANT — `_restore_from_state` missing TDD fallback for `input_type=tdd`

**File:** `src/superclaude/cli/roadmap/executor.py:1744-1764`

**What's wrong:** When resuming a roadmap run with `--resume`, `_restore_from_state()` auto-wires `tdd_file` and `prd_file` from state. However, it does NOT implement the TDD fallback that `tasklist/commands.py:132` does: when `input_type == "tdd"` and `tdd_file` is null in state (because the primary input WAS the TDD), the tasklist code falls back to `spec_file`. The roadmap `_restore_from_state` does not do this.

**Impact:** On `--resume` of a TDD-primary pipeline run, the resumed run will have `config.tdd_file = None`, losing the redundancy guard at executor.py:862 (which would correctly nullify it anyway). But more importantly, downstream consumers that check `config.tdd_file` to decide whether to include TDD supplementary context will miss the TDD context entirely on resume. This is inconsistent with the tasklist auto-wire behavior.

**Required Fix:** Add the same `elif state.get("input_type") == "tdd"` fallback block in `_restore_from_state()` after the `saved_tdd` check, using `state.get("spec_file")` as the TDD file. Alternatively, document this as intentional since the redundancy guard at line 862 would nullify it anyway — but this creates a cross-module inconsistency.

---

### 2. IMPORTANT — `build_extract_prompt` and `build_extract_prompt_tdd` accept `tdd_file` parameter but never use it

**File:** `src/superclaude/cli/roadmap/prompts.py:82-87, 184-189`

**What's wrong:** Both `build_extract_prompt(spec_file, retrospective_content, tdd_file, prd_file)` and `build_extract_prompt_tdd(spec_file, retrospective_content, tdd_file, prd_file)` accept a `tdd_file` parameter but neither function references `tdd_file` in the function body. Only `prd_file` is checked with `if prd_file is not None`. The `tdd_file` parameter is dead code — accepted but discarded silently.

**Impact:** If a user passes `--tdd-file` alongside a spec as primary input (intending supplementary TDD context for extraction), the TDD file IS included in `step.inputs` (embedded into the prompt by the executor), but the extraction prompt itself gives NO instructions for how to use the TDD file. The LLM will see the TDD content embedded but receive no guidance on what to do with it. This may produce inconsistent extraction quality depending on the LLM's heuristics.

**Required Fix:** Either (a) add a conditional block `if tdd_file is not None:` with instructions for how to use TDD content as supplementary context during spec extraction, or (b) remove the `tdd_file` parameter from both functions and remove the `tdd_file=config.tdd_file` kwarg at the call sites in executor.py:903,911 to make the dead code explicit. Option (a) is preferred since the TDD file IS being embedded.

---

### 3. IMPORTANT — `build_generate_prompt` accepts `tdd_file` but never uses it in the prompt body

**File:** `src/superclaude/cli/roadmap/prompts.py:334-406`

**What's wrong:** `build_generate_prompt(agent, extraction_path, tdd_file, prd_file)` accepts `tdd_file` but only uses `prd_file` in the prompt body (lines 388-404). The `tdd_file` parameter is dead code. There is a comment at lines 360-367 noting this is "deferred" per TASK-RF-20260325-cli-tdd Deferred Work Items, but the function signature falsely suggests TDD context is being used.

**Impact:** The executor at line 924 passes `tdd_file=config.tdd_file` and includes the TDD file in `step.inputs` (line 928), so the TDD content IS embedded into the prompt. But the prompt text gives no instructions for using it. The LLM sees two inputs (extraction + TDD) but is only told about the extraction. This is a usability gap — the TDD content is noise in the prompt without instructions.

**Required Fix:** Either (a) implement TDD-aware generate prompt instructions (the deferred work from the comment), or (b) remove `tdd_file` from the function signature AND from the step.inputs list at executor.py:928 to avoid embedding unused content. Option (b) is correct until the deferred work is completed — embedding without instructions wastes context window.

---

### 4. IMPORTANT — `build_score_prompt` accepts `tdd_file` but never uses it

**File:** `src/superclaude/cli/roadmap/prompts.py:461-502`

**What's wrong:** `build_score_prompt(debate_path, variant_a_path, variant_b_path, tdd_file, prd_file)` accepts `tdd_file` but only uses `prd_file` in the prompt body (lines 488-500). The `tdd_file` parameter is dead code. The executor at line 966 passes `tdd_file=config.tdd_file` and includes TDD in step.inputs at line 970.

**Impact:** Same as issue #3 — TDD content is embedded without instructions.

**Required Fix:** Either implement TDD-aware scoring dimensions or remove `tdd_file` from the signature and step.inputs list.

---

### 5. IMPORTANT — `build_test_strategy_prompt` accepts `tdd_file` but never uses it

**File:** `src/superclaude/cli/roadmap/prompts.py:698-764`

**What's wrong:** `build_test_strategy_prompt(roadmap_path, extraction_path, tdd_file, prd_file)` accepts `tdd_file` but only uses `prd_file` in the prompt body (lines 745-762). Dead `tdd_file` parameter. The executor at line 996 passes `tdd_file=config.tdd_file` and includes TDD in step.inputs at line 1000.

**Impact:** Same as issues #3 and #4. For test-strategy specifically, the TDD's Testing Strategy section (S15) contains extremely relevant content (test pyramid, test cases, environments) that is being embedded but not directed toward.

**Required Fix:** Add a conditional block using TDD content for test strategy enrichment. This is arguably the highest-value use of supplementary TDD context after extraction.

---

### 6. IMPORTANT — `build_spec_fidelity_prompt` accepts `tdd_file` but never uses it

**File:** `src/superclaude/cli/roadmap/prompts.py:537-637`

**What's wrong:** `build_spec_fidelity_prompt(spec_file, roadmap_path, tdd_file, prd_file)` accepts `tdd_file` but only uses `prd_file` (lines 618-635). Dead parameter. The executor at line 1006 passes it and includes TDD in step.inputs at line 1010.

**Impact:** Same pattern. For spec-fidelity, the comparison dimensions already include TDD-relevant items (Data Models, API Endpoints, Component Inventory, etc. at lines 580-591) but the prompt doesn't instruct the LLM to compare against the actual TDD content when it's available.

**Required Fix:** Add TDD-aware fidelity validation instructions, or remove the parameter and stop embedding the TDD.

---

### 7. MINOR — Duplicate auto-detection in commands.py and executor._build_steps

**File:** `src/superclaude/cli/roadmap/commands.py:207-215` and `executor.py:852-856`

**What's wrong:** `detect_input_type()` is called twice for the same file: once in `commands.py:run()` for user feedback (line 211), and again in `executor.py:_build_steps()` for actual routing (line 855). The comment at commands.py:206 acknowledges this: "executor also resolves independently for the actual routing." While functionally correct (detection is pure and deterministic), it is wasteful and creates a subtle race: if the file changes between the two calls (unlikely but possible), the user would see one type reported but the pipeline would use the other.

**Required Fix:** Pass the resolved `input_type` from commands.py into config (e.g., set `config.input_type = resolved_type` before calling `execute_roadmap`), so `_build_steps` uses the CLI-resolved value without re-detecting. This also avoids re-reading the file.

---

### 8. CRITICAL — `_restore_from_state` mutates config directly instead of using `dataclasses.replace`

**File:** `src/superclaude/cli/roadmap/executor.py:1725, 1742, 1751, 1762`

**What's wrong:** `_restore_from_state` directly mutates the config dataclass: `config.agents = restored` (line 1725), `config.depth = saved_depth` (line 1742), `config.tdd_file = tdd_path` (line 1751), `config.prd_file = prd_path` (line 1762). In contrast, `_build_steps` at lines 859 and 867 correctly uses `config = dataclasses.replace(config, ...)` to create new instances. This inconsistency means `_restore_from_state` mutates the caller's reference, which works today but violates the immutability pattern established elsewhere and could cause bugs if callers share config references.

**Impact:** Currently functional because `execute_roadmap` holds the only reference. But if config is ever shared (e.g., for parallel validation), mutations would leak across. This is a code quality / correctness-by-convention issue.

**Required Fix:** Use `dataclasses.replace()` for all config modifications in `_restore_from_state` and return the new config (which it already does — `return config` — but it's returning the mutated original, not a new instance). Specifically, collect all overrides and apply them in a single `dataclasses.replace()` call.

---

### 9. MINOR — Step numbering comment error in executor.py

**File:** `src/superclaude/cli/roadmap/executor.py:1003`

**What's wrong:** The comment says `# Step 8: Spec Fidelity` but it's actually Step 9 (test-strategy is Step 8, as labeled at line 993). The comment at line 993 says `# Step 8: Test Strategy` which is correct for the label but then spec-fidelity reuses "Step 8" in its comment.

**Required Fix:** Change line 1003 comment to `# Step 9: Spec Fidelity`.

---

### 10. MINOR — EXTRACT_GATE does not require TDD-specific frontmatter fields

**File:** `src/superclaude/cli/roadmap/gates.py:765-795`

**What's wrong:** When TDD extraction is used (`build_extract_prompt_tdd`), the prompt instructs the LLM to produce 6 additional frontmatter fields: `data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified` (prompts.py lines 223-228). However, `EXTRACT_GATE` only checks the standard 13 fields (gates.py:766-780). The TDD-specific fields are never validated by any gate.

**Impact:** If the LLM omits any TDD-specific frontmatter field, extraction will still pass the gate. Downstream consumers that rely on these fields (scoring formula uses `api_surface` and `data_model_complexity`) may encounter missing data without any pipeline warning.

**Required Fix:** Either (a) create a `TDD_EXTRACT_GATE` with the additional required fields and select it conditionally in `_build_steps`, or (b) make the TDD-specific fields optional in the downstream scoring (which they may already be if the scoring reference says "or 0 if section absent"). Clarify the contract.

---

### 11. IMPORTANT — `detect_input_type` scoring.md detection rule inconsistent with executor.py implementation

**File:** `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md:7-9` vs `src/superclaude/cli/roadmap/executor.py:60-120`

**What's wrong:** scoring.md defines the TDD detection rule as: "contains `## 10. Component Inventory` heading, OR YAML frontmatter with `type` field containing 'Technical Design Document', OR document body contains 20 or more section headings matching TDD pattern."

The actual `detect_input_type()` implementation uses a WEIGHTED SCORING SYSTEM with a threshold of >= 5, not a simple OR of three conditions. The implementation:
- 20+ numbered headings = +3 (not a binary trigger)
- `parent_doc` / `coordinator` frontmatter = +2 each (NOT checking for `type` containing "Technical Design Document" as a frontmatter field match — it checks that as content search at line 111)
- 8 TDD section names = +1 each (not just `## 10. Component Inventory`)
- "Technical Design Document" in first 1000 chars = +2

The scoring.md description oversimplifies and does not match the weighted-scoring implementation. For example, a document with `## 10. Component Inventory` alone (scoring.md says TDD) would score only +1 from section name match, which is below the threshold of 5, so the CLI would classify it as spec.

**Required Fix:** Update scoring.md to accurately describe the weighted scoring system with the threshold, or update the code to match the spec. The current documentation misleads skill-protocol consumers about detection behavior.

---

### 12. IMPORTANT — extraction-pipeline.md detection rule also inconsistent

**File:** `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md:145-147`

**What's wrong:** Same issue as #11. The extraction-pipeline.md states the TDD detection rule as three OR conditions, but the actual implementation uses weighted scoring. The conditional gate description says Steps 9-15 execute "ONLY when TDD-format input is detected" per the OR-based rule, which does not match the actual CLI behavior.

**Required Fix:** Align the documentation with the actual implementation's weighted scoring system.

---

### 13. MINOR — spec-panel.md detection rules inconsistent with CLI implementation

**File:** `src/superclaude/commands/spec-panel.md:32`

**What's wrong:** Step 6a describes TDD detection as: "presence of `## 10. Component Inventory` heading OR `type: ...` in YAML frontmatter OR 20+ TDD section headings." This is the same OR-based rule that conflicts with the weighted-scoring implementation in executor.py. The spec-panel is a skill that may call the CLI, creating a detection behavior mismatch.

**Required Fix:** Update spec-panel.md step 6a to reference the actual detection algorithm or at minimum note that CLI detection uses weighted scoring.

---

### 14. MINOR — `build_tasklist_generate_prompt` may be dead code from CLI perspective

**File:** `src/superclaude/cli/tasklist/prompts.py:144-230`

**What's wrong:** The function's docstring correctly notes it is "NOT currently called by the CLI `tasklist validate` executor" and is used by the skill protocol. This is documented and not a bug per se, but the function lives in the CLI module (`cli/tasklist/prompts.py`) rather than in the skill module. This is a minor organizational concern.

The function is well-implemented for its purpose (skill protocol consumption) with proper TDD/PRD enrichment blocks and a combined interaction note.

**Required Fix:** No code change needed. Consider adding a test that imports this function to prevent accidental deletion during cleanup.

---

### 15. IMPORTANT — `tasklist/commands.py` auto-wire does not handle malformed `read_state` return gracefully for all edge cases

**File:** `src/superclaude/cli/tasklist/commands.py:116`

**What's wrong:** The code does `state = read_state(resolved_output / ".roadmap-state.json") or {}`. The `read_state` function returns `None` on missing/malformed files (executor.py:1652-1662), so `state` is `{}` on failure. Then `state.get("tdd_file")`, `state.get("input_type")`, etc. are called. This handles malformed JSON gracefully (returns None -> {} -> .get returns None).

However, there is a subtle edge: if `read_state` returns a non-dict JSON value (e.g., the file contains a JSON array `[]` or a string `"foo"`), `json.loads()` would succeed, returning a non-dict, and then `state.get("tdd_file")` would raise `AttributeError` on a list or string. The `read_state` function does not validate that the parsed JSON is a dict.

**Impact:** Would crash with an unhelpful `AttributeError` if `.roadmap-state.json` contains valid JSON that isn't a dict object. Very unlikely in practice but violates defensive coding standards.

**Required Fix:** Add a type check in `read_state`: `data = json.loads(text); return data if isinstance(data, dict) else None`.

---

### 16. MINOR — Domain keyword dictionary count inconsistency

**File:** `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md:235-278` and `scoring.md:80,105`

**What's wrong:** The extraction-pipeline.md defines 7 domain keyword dictionaries (Frontend, Backend, Security, Performance, Documentation, Testing, DevOps/Ops). The scoring.md 7-factor TDD formula says `domain_spread` denominator is 7, accounting for "Testing and DevOps/Ops domains" (line 105). However, the standard 5-factor formula uses denominator 5, which does not match any obvious subset — it should be 5 domains (the 7 minus Testing and DevOps/Ops), but the dictionaries section always defines all 7.

This is actually consistent on closer inspection: the standard formula's `min(domains / 5, 1.0)` cap means having 5+ domains gives maximum score, while TDD formula's `min(domains / 7, 1.0)` requires 7 for maximum. This is a documentation clarity issue — the "5 vs 7" denominator relationship to the 7 dictionaries should be explained.

**Required Fix:** Add a brief note in scoring.md explaining why the standard formula uses 5 as denominator when 7 dictionaries exist (because Testing and DevOps/Ops domains are primarily TDD-relevant).

---

### 17. IMPORTANT — PRD supplementary blocks are missing from `build_diff_prompt`, `build_debate_prompt`, and `build_merge_prompt`

**File:** `src/superclaude/cli/roadmap/prompts.py:409-534`

**What's wrong:** PRD supplementary context blocks were added to: extract, generate, score, spec-fidelity, test-strategy. But three prompt builders in the middle of the pipeline were skipped: `build_diff_prompt`, `build_debate_prompt`, and `build_merge_prompt`. Furthermore, the executor does NOT pass PRD or TDD files as `step.inputs` for diff (line 950), debate (line 960), or merge (line 980).

For diff and debate, this may be intentional — these steps compare/debate the two roadmap variants and may not need source document context. But for merge, the lack of PRD context means the final merged roadmap is produced without business context guidance, even though downstream steps (score, spec-fidelity, test-strategy) all have PRD enrichment. The merge step is where the final roadmap is actually synthesized.

**Impact:** The merge step produces the final roadmap without PRD business context, but the spec-fidelity step then validates it WITH PRD context (checking persona coverage, compliance alignment, etc.). This creates a mismatch: the fidelity step may flag deviations that the merge step had no information to avoid.

**Required Fix:** At minimum, add PRD supplementary context to `build_merge_prompt` and pass `prd_file` in merge step.inputs. For diff/debate, document the intentional omission. Consider whether TDD context is also needed for merge.

---

### 18. MINOR — Step 9 comment says "Step 8"

**File:** `src/superclaude/cli/roadmap/executor.py:1013`

**What's wrong:** Line 1013 comment says `# Step 9: Wiring Verification (section 5.7, shadow mode trailing gate)` — this is correct. But line 1003 says `# Step 8: Spec Fidelity (after test-strategy, FR-008 through FR-010)` which duplicates the step 8 numbering from the test-strategy comment at line 993. (Duplicate of issue #9, combined here for reference.)

---

### 19. MINOR — `tdd_file` and `prd_file` not included in tasklist commands.py `validate` function's config when files are auto-wired but already resolved paths

**File:** `src/superclaude/cli/tasklist/commands.py:169-170`

**What's wrong:** At lines 169-170: `tdd_file=tdd_file.resolve() if tdd_file is not None else None`. When `tdd_file` is auto-wired from state at line 126, it is set to `saved_tdd_path` which is already a `Path(saved_tdd)` object (line 120) but NOT resolved. Then at line 169, `.resolve()` is called. This is fine. However, the auto-wired path at line 126 stores the raw `saved_tdd_path = Path(saved_tdd)` which may be a relative path if the state file stored a relative path. The `Path.resolve()` at line 169 will resolve it relative to CWD, which may differ from the original run's CWD.

The roadmap executor's `_save_state` at line 1440 stores `str(config.tdd_file)` which was already `.resolve()`'d at commands.py:195. So state stores absolute paths. This chain is actually correct — state stores absolute, auto-wire reads absolute, .resolve() is a no-op on absolute paths.

**Required Fix:** No fix needed. This is correct. (Including for completeness of analysis.)

---

## Summary

- **Checks analyzed:** 12 source files covering roadmap CLI, tasklist CLI, prompts, gates, models, skills, and reference docs
- **CRITICAL issues:** 1 (mutating dataclass instead of replace — code quality risk)
- **IMPORTANT issues:** 9 (dead tdd_file parameters in 4 prompt builders, missing PRD context in merge, detection rule inconsistencies in 2 docs, missing TDD fallback in resume, read_state type safety)
- **MINOR issues:** 5 (comment numbering, gate coverage, organizational, documentation clarity)

## Recommendations (Priority Order)

1. **Fix dead `tdd_file` parameters** (issues #2-6): Either implement TDD-aware prompt blocks or remove the parameter and stop embedding TDD content in prompts that don't use it. The current state wastes LLM context window on every run.

2. **Add PRD context to `build_merge_prompt`** (issue #17): The merge step produces the final roadmap but lacks business context that downstream validation checks against.

3. **Align detection rule documentation** (issues #11-13): Three reference docs describe TDD detection as simple OR conditions when the implementation uses weighted scoring. This will confuse skill-protocol consumers.

4. **Add type safety to `read_state`** (issue #15): One-line fix prevents potential AttributeError on malformed state files.

5. **Use `dataclasses.replace` consistently** (issue #8): Aligns `_restore_from_state` with the pattern used in `_build_steps`.

6. **Add TDD fallback to `_restore_from_state`** (issue #1): Ensures resume behavior matches tasklist auto-wire behavior.

## QA Complete
