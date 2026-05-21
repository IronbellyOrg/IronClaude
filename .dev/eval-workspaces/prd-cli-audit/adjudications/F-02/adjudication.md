# F-02 Adjudication: Static dict cannot express slug-templated artifact names

**Adjudicator**: opus:analyzer + opus:refactorer + sonnet:architect (single-invocation triad)
**Mode**: bug-report-adjudication / depth=standard / focus=reproducibility,blast-radius,severity-calibration
**Anchor**: Bug 2 — confirm or refute

---

## 0. Evidence re-verification

All cited facts independently re-read from the live tree at adjudication time.

| Claim from finding | Verification | Status |
|---|---|---|
| `_STEP_ARTIFACT_FILES: dict[str, str]` is static | `executor.py:246-251` — literal dict-literal with 4 string→string entries, no callables, no patterns | CONFIRMED |
| `_resolve_step_content` uses `rglob(base_name)` on the dict value | `executor.py:271` (`base_name = Path(artifact_name).name`), `executor.py:281` (`for match in root.rglob(base_name)`) | CONFIRMED |
| Prompt writes to `TASK-PRD-{slug}.md` | `prompts.py:381` — `Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}` | CONFIRMED |
| `product_slug = _slugify(product_name) if product_name else ""` | `config.py:121` exact match | CONFIRMED |
| `task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"` | `config.py:124` exact match | CONFIRMED |
| prompts.py:405 and :464 use `task_dir.glob("TASK-PRD-*.md")` as the workaround pattern | `prompts.py:405` — `task_files = list(config.task_dir.glob("TASK-PRD-*.md"))`; `prompts.py:464` identical | CONFIRMED — finding's F-E-2 claim is accurate |
| `_persist_step_artifact` uses the same dict | `executor.py:987` — `artifact_name = _STEP_ARTIFACT_FILES.get(step_id)` with short-circuit at 988-989 | CONFIRMED — finding undersells this; the *same* type defect blocks the write-back path, not just the read path |
| `_slugify` strips shell-unsafe characters | `config.py:152-156` — `re.sub(r"[^a-z0-9]+", "-", slug)` reduces all non-alphanum to `-` | CONFIRMED — kills the "shell-unsafe chars" sub-hypothesis from the finding's reproduction prompt |

No cited fact is wrong. The finding's evidence holds. One under-statement: the type defect bites `_persist_step_artifact` (write side) as well as `_resolve_step_content` (read side), making the structural problem broader than the finding articulates.

---

## 1. Persona 1 — Analyzer (reproducibility)

**Question**: Can the slug-template mismatch be reliably reproduced? What inputs trigger an empty/wrong slug? Are there real production scenarios where `--product` is omitted or contains shell-unsafe chars?

**Findings**:

1. **Mechanical reproducibility is total**, but only *conditional on F-01 being fixed first*. F-01 (missing `build-task-file` key) short-circuits at `executor.py:268` (`if not artifact_name: return ndjson_text`) before F-02's defect can manifest. The F-02 failure mode is "what happens immediately after a maintainer adds `"build-task-file": "TASK-PRD.md"` (or similar literal) to the dict". So F-02 is the *latent successor bug* that ambushes the F-01 fix.

2. **Empty-slug path is live**. `config.py:121` produces `product_slug = ""` whenever `product_name == ""`. Default `parse-request` invocations without `--product` (the LLM is supposed to fill it in, but that lands later in the pipeline, not at config-construction time) hit this branch. Result: writer emits `TASK-PRD-.md` (literal — a leading dash followed by `.md`), `task_dir_name` defensively falls back to `prd-task`, but the filename does NOT get the same fallback (`prompts.py:381` builds `"TASK-PRD-" + "" + ".md"` = `"TASK-PRD-.md"`). Asymmetric defense.

3. **Shell-unsafe chars sub-hypothesis is REFUTED** by `_slugify` (config.py:152-156). The regex `[^a-z0-9]+` → `-` collapses every non-alphanumeric character (including shell metacharacters, spaces, slashes, dollar signs) to a single hyphen. Lowercasing and edge-trim happen as well. There is no path from `--product "Foo; rm -rf /"` to a shell-unsafe filename — the slug becomes `foo-rm-rf`. The finding's narration that "`--product` may contain shell-unsafe chars" is technically wrong for the slug path (and the finding does not actually claim this; the adjudication prompt's reproduction-cue does). Down-grade this sub-claim, but it does not affect the core defect.

4. **The reproduction sketch in the finding is correct**: even a hypothetical literal-key fix (`"build-task-file": "TASK-PRD.md"`) cannot match `TASK-PRD-20260520-userauth.md` via `rglob("TASK-PRD.md")` because `rglob` matches the *whole* basename, not a prefix. This is mechanically verifiable from the `pathlib` semantics. The finding's claim is exact.

5. **Production trigger inputs**:
   - `superclaude prd run "..."` without `--product` → empty slug → `TASK-PRD-.md` writer target, `TASK-PRD-*.md` glob workaround already in place at prompts.py:405/464 still finds it, but the static-dict reader (post-F-01-fix) would search for the *literal* dict value.
   - `--product "User Authentication System"` → slug `user-authentication-system` → `TASK-PRD-user-authentication-system.md`. Any literal value in the dict misses.
   - LLM-derived slug at parse-request time (per finding trace) → unknown until step 2 runs → static dict at module-import time literally cannot encode it.

**Analyzer verdict**: REAL — reproducibility is unambiguous, contingent on F-01 fix. The shell-safety reproduction angle from the prompt cue is refuted; the empty-slug angle is real; the LLM-late-binding angle is the strongest. Drop the "shell-unsafe" framing.

---

## 2. Persona 2 — Refactorer (blast radius)

**Question**: How many other static lookup tables share this slug-templating problem? Investigate `_PHASE_ALLOWED_REFS`, `GATE_CRITERIA`, and any other dict keyed by exact filenames.

**Findings**:

1. **`_PHASE_ALLOWED_REFS`** (`process.py:95-113`): keys are step IDs (`"parse-request"`, etc.); values are lists of **refs** filenames (`"build-request-template.md"`, `"operational-guidance.md"`, etc.). Refs are static SoT files in `skill_refs_dir` — they are NOT per-invocation slug-templated. The `_build_file_args` lookup at `process.py:181` joins `config.skill_refs_dir / ref_name` and checks `is_file()`. **No slug-template problem**. Same *pattern shape* as F-02 but different *domain*: static SoT inputs versus per-run outputs.

2. **`GATE_CRITERIA`** (`gates.py:295-...`): keys are step IDs; values are `GateCriteria` dataclasses (min_lines, required_frontmatter_fields, semantic_checks, etc.). No filename values. Step-ID-keyed only. **No slug-template problem**, but it *does* share F-01's failure mode — any step in `_STAGE_A_STEPS` without a `GATE_CRITERIA` entry would hit the `.get(step_id)` short-circuit at executor.py:382, 530, etc. That's an orthogonal concern (gate-criteria coverage) not the F-02 type defect.

3. **`_STEP_ARTIFACT_FILES`** is the *only* dict in `src/superclaude/cli/prd/` that maps step IDs to **output filenames the subprocess generates**. Its three sister dicts (`_PHASE_ALLOWED_REFS`, `GATE_CRITERIA`, the implicit step-tuple list `_STAGE_A_STEPS`) all key by step ID, but none of them treat per-invocation filename templating as part of their value type.

4. **Consumers of the defective dict**: `_resolve_step_content` (executor.py:267) AND `_persist_step_artifact` (executor.py:987). Both use the same `.get(step_id)` short-circuit pattern and both treat the value as a literal filename. The finding focuses on the read path; the write path has the identical defect. Fix must touch both call sites.

5. **The glob workaround already exists in this codebase** at `prompts.py:405` and `:464` — `list(config.task_dir.glob("TASK-PRD-*.md"))`. Refactor cost is therefore *not* "invent a new pattern"; it is "hoist an existing in-repo pattern into the dict-value contract". That sharply lowers fix difficulty.

6. **Negative claim verified**: `grep -rn "_STEP_ARTIFACT_FILES\|_resolve_step_content" src/superclaude/cli/prd/ tests/` returns five hits, all inside `executor.py`. No external coupling; the change is localised to one module.

**Refactorer verdict**: Blast radius is **narrow on dicts** (only `_STEP_ARTIFACT_FILES` is structurally broken) but **wide on consumers** (two call sites in one module). The fix has no cross-module ripple. The "make dict values express templates" change is single-module, single-file. Risk surface is small; test coverage is the main gap (per the finding's Agent F note — no test exercises slug-templated artifact resolution).

---

## 3. Persona 3 — Architect (severity calibration)

**Question**: Is the preliminary CRITICAL rating right? This is structurally linked to F-01 — should it be folded in, or does it deserve standalone status? What does the fix actually require — static dict → callable, or new resolution mode?

**Findings**:

1. **F-01 vs F-02 relationship**: F-01 = "dict missing the key"; F-02 = "even with the key added, the value type can't express the filename". F-01 is the *symptom-cause* (current halt); F-02 is the *next-fix-blocker* (the naive fix for F-01 doesn't work). They are nested defects on the same data structure but at different layers (presence vs. expressiveness). A reviewer who merges them would lose the architectural distinction: F-01 is a maintenance oversight, F-02 is a type-design flaw.

2. **Folding decision**: Do NOT fold. They warrant separate tracking because:
   - The fixes are different: F-01 = add an entry; F-02 = change the value type.
   - The risk profiles differ: F-01 fix could be a one-line patch that silently fails to resolve (because of F-02). F-02 fix requires consumer-side changes at two call sites.
   - The test obligations differ: F-01 needs a coverage test for the step; F-02 needs property tests across slug variations.
   - Adversarial value: if the team patches F-01 in isolation, the pipeline still fails on `build-task-file` at the gate. F-02 must be visible as a standalone gating bug.

3. **CRITICAL rating — calibrated**: I concur with CRITICAL. Reasons:
   - **User-visible failure**: post-F-01 fix, pipeline still halts at step 7 with a misleading "no artifact found" gate failure for every non-empty product slug. This is the same user-impact tier as F-01.
   - **Blast on the canonical work product**: `TASK-PRD-*.md` is the *primary deliverable* of Stage A. Failing to locate it means no PRD ever completes.
   - **Latent / ambush severity**: precisely because F-02 is invisible until F-01 is fixed, it has high "second-strike" cost — it would burn another debug cycle after a maintainer thinks they've fixed the halt.
   - **No workaround at the consumer side** (the gate evaluator can't see disk files), unlike prompts.py:405 which has the right pattern locally.

4. **Fix design — required form**:
   - **Minimal viable fix**: change `_STEP_ARTIFACT_FILES` value type from `str` to `str` *with glob semantics*, and update `_resolve_step_content` to use `root.glob(pattern)` (already does `rglob`, but the value must be a glob like `"TASK-PRD-*.md"` instead of `"TASK-PRD.md"`). Update `_persist_step_artifact` to write to a derived path (`config.task_dir / f"TASK-PRD-{config.product_slug}.md"`), not blindly to the dict value, since the persist path needs the actual instantiated filename. This is the *split-value* approach: pattern for read, template for write.
   - **More principled fix**: change the value type to `Callable[[PrdConfig], str]` (or a small dataclass with `read_pattern` and `write_filename(config)` fields). Lets each step declare its own naming policy. Slightly more code, much clearer contract.
   - **Architect's recommendation**: the dataclass approach. The current `dict[str, str]` is already a poor man's struct; promoting it to `dict[str, ArtifactSpec]` costs ~20 lines and removes the type-expressiveness gap permanently. Avoids re-introducing the same defect when the next slug-templated step lands.

5. **One subtle point on `_persist_step_artifact`**: it writes the *captured NDJSON content* to `task_dir / artifact_name`. For `build-task-file`, the subprocess already writes the file to disk (per prompts.py:381 instruction). So `_persist_step_artifact` for `build-task-file` should probably be a *no-op* (or a *verify-exists*), not a write-back. The finding does not surface this design wrinkle, but it bears on the fix design — the simple "add a glob pattern" fix could *overwrite* the real task file with NDJSON commentary, which is *worse* than the current failure. This raises the implementation-care bar for the fix and supports CRITICAL.

**Architect verdict**: CRITICAL is correctly calibrated. Standalone status — do not fold into F-01. Fix difficulty is **MEDIUM**: not a one-liner, requires either a new value type or split read/write logic plus careful handling of the "subprocess-writes-to-disk-itself" case to avoid clobbering.

---

## 4. Convergence

**Verdict**: **REAL** (confirmed bug)

**Convergence score**: 3/3 personas independently confirm a real, structural, separately-tracked defect. Analyzer confirms reproducibility (post-F-01-fix), Refactorer confirms localized blast radius with a clear existing-pattern fix, Architect confirms severity and recommends standalone tracking.

**Final severity**: **CRITICAL** (unchanged from Stage 2 preliminary)
- Justification: primary-deliverable failure, latent-after-F-01-fix ambush, no consumer-side workaround, gate-blocking.

**Fix difficulty**: **MEDIUM**
- Single module, two call sites, an in-repo precedent pattern exists (prompts.py:405/464), but the persist path needs care to avoid clobbering a subprocess-written file. Recommended fix: promote `_STEP_ARTIFACT_FILES` value type from `str` to a `dataclass` (or callable) declaring read-pattern and write-filename separately. Estimated effort: ~30-60 LOC plus tests.

**Confidence**: 0.97 (matches the finding's aggregated confidence; one downward adjustment — the "shell-unsafe characters" repro angle is refuted by `_slugify`'s regex — does not materially change the bug.)

**Synthesis (one paragraph)**: F-02 is a real, structurally distinct, CRITICAL-severity bug that is causally adjacent to F-01 but must remain separately tracked. F-01 ("dict missing key") and F-02 ("dict value type cannot express templated filenames") sit on the same data structure at different layers; merging them would let a naive F-01 patch ship and re-fail the pipeline. The evidence in the finding is accurate as cited at all four anchor lines (`executor.py:246-269`, `executor.py:271`, `executor.py:281`, `prompts.py:381`, `config.py:121-125`), and the workaround precedent the finding points to (`prompts.py:405` and `:464` using `task_dir.glob("TASK-PRD-*.md")`) is verbatim correct — the same pattern needs to land in `_resolve_step_content`, and a symmetric change needs to land in `_persist_step_artifact` (which the finding does not foreground but which carries the identical defect). The recommended fix is to promote the dict value type from `str` to a small artifact-spec dataclass (read-glob + write-filename), localizing the change to one module without cross-cutting ripples. The only sub-hypothesis to drop is the "shell-unsafe character" repro framing — `_slugify` (`config.py:152-156`) reduces all non-alphanumerics to hyphens, so that vector is closed; the live triggers are empty-slug and LLM-late-binding-slug paths, plus any non-empty product name.

---

## 5. Disposition recommendations (advisory, not binding)

- Keep F-02 as standalone CRITICAL.
- Fix sequence: must ship before or atomically with F-01; shipping F-01 alone re-fails the pipeline.
- Cross-reference required between F-01 and F-02 in the consolidated findings doc.
- Test obligation: parameterized test over slug variants (empty, single-word, multi-word, unicode-stripped) verifying `_resolve_step_content` returns the on-disk file and `_persist_step_artifact` does not clobber a subprocess-written file.
- Consider an audit pass for any *other* step whose Write target is per-invocation templated — none found today, but the dataclass refactor future-proofs this class of defect.
