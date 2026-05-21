# Adjudication: F-01 — `_STEP_ARTIFACT_FILES` missing `build-task-file` (proximate halt cause)

## Evidence re-verification (load-bearing, performed before persona analysis)

- `src/superclaude/cli/prd/executor.py:246-251` — `_STEP_ARTIFACT_FILES` literally contains exactly four entries: `parse-request`, `scope-discovery`, `research-notes`, `sufficiency-review`. **No `build-task-file` key.** Confirmed verbatim.
- `src/superclaude/cli/prd/executor.py:267-269` — `_resolve_step_content` does `artifact_name = _STEP_ARTIFACT_FILES.get(step_id)` followed by `if not artifact_name: return ndjson_text`. Confirmed verbatim. The early return is the only fallback path; there is no second lookup.
- `src/superclaude/cli/prd/executor.py:301-316` — `_STAGE_A_STEPS` does include `("build-task-file", "Build Task File", "build_task_file_prompt", False)` at line 313. Confirmed.
- `src/superclaude/cli/prd/executor.py:522-524` — `_run_subprocess_step` calls `_resolve_step_content(step_id, self._config.task_dir, output_text)` where `output_text` is the NDJSON-extracted assistant commentary. The result is bound to `gate_content`. Confirmed.
- `src/superclaude/cli/prd/executor.py:530-540` — `gate_content` is then handed to `_evaluate_gate`; on STRICT failure the step status becomes `HALT`. Confirmed.
- `src/superclaude/cli/prd/executor.py:976-1004` — `_persist_step_artifact` short-circuits at line 988-989 (`if not artifact_name: return`). For `build-task-file` it returns without writing. Confirmed.
- `src/superclaude/cli/prd/gates.py:359-368` — `GATE_CRITERIA["build-task-file"]` has `min_lines=400` and `enforcement_tier="STRICT"`. Confirmed verbatim.
- `src/superclaude/cli/prd/prompts.py:381` — `Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}`. Confirmed: the subprocess is explicitly directed to Write to disk, **not** to emit content via NDJSON.
- Negative claim "no test exercises `_resolve_step_content`": confirmed via grep — `grep -rn "_resolve_step_content" tests/` returns zero hits.
- Negative claim "mock harness defeats the real chain": confirmed at `tests/cli/prd/test_e2e.py:245-247` — `_make_passing_output` writes raw markdown directly into `output_file`. Combined with `_extract_text_from_stream_json` (executor.py:130) falling back to `raw` when no JSON parses, `output_text` is already the 400+ line passing fixture, so the dict miss is irrelevant: the NDJSON-fallback path returns text that satisfies the gate. The test cannot regress this defect.

Every load-bearing claim in the finding matches what is on disk at this revision. No discrepancies.

---

## Persona 1 — Analyzer (opus, depth=standard) — focus: reproducibility

**Can the failure be reliably reproduced from the sketch?**

Yes — the failure is mechanically determined by a dict miss; there is no stochasticity in the trigger condition. The reproduction chain has four sequential, mandatory links and each one holds:

1. Pipeline must reach step 7. Steps 1–6 (`check-existing` through `template-triage`) must succeed. Of these, `check-existing` and `template-triage` are internal (no subprocess; `executor.py:437-440`), and `parse-request`/`scope-discovery`/`research-notes`/`sufficiency-review` are the four steps the dispatch table *does* cover, so they have a working disk-read path. Reaching step 7 is the normal happy path. Not a hidden precondition.
2. Step 7 launches the subprocess. The prompt at `prompts.py:381` explicitly directs the subprocess to Write to `task_dir / "TASK-PRD-{slug}.md"`. The subprocess's NDJSON stdout will contain assistant commentary about *doing* the write, not the 400-line task file itself.
3. `_resolve_step_content("build-task-file", …)` executes the dict lookup; the key is absent; the function returns `ndjson_text` (executor.py:267-269). There is no second search path, no glob fallback. The "best content" disk-search loop at `executor.py:275-291` is **gated behind** the dict membership check and is therefore unreachable for `build-task-file`.
4. `_evaluate_gate` runs `min_lines` against ~30 lines of commentary versus a 400-line floor; STRICT enforcement promotes the failure to `PrdStepStatus.HALT` and `_execute_step`'s caller (`executor.py:380-389`) breaks out of the Stage A loop with `result.outcome = "halt"`.

**Hidden preconditions that could make it rarer than claimed?**

I looked for three escape hatches: (a) Could the subprocess emit the entire 400+ line task file as inline text in NDJSON instead of using Write? In theory yes, but the prompt language ("CRITICAL: Use incremental file writing… Never one-shot the entire file" at prompts.py:392-393) actively discourages it, and the task file with frontmatter typically exceeds the practical NDJSON-comment volume. (b) Could `_extract_text_from_stream_json` overshoot? Inspection of executor.py:99-130 shows it only collects `assistant`/`content[].text` blocks; it does not include Tool-use payloads. (c) Could a prior Stage A step have written `TASK-PRD-*.md` to disk? No — the four covered steps all target different filenames.

The only way to *not* reproduce this is to provide subprocess output already padded past 400 lines (the e2e mock does exactly that — see test_e2e.py:245-247), which is precisely why the test suite missed it.

**Trace verdict**: The chain holds end-to-end. Reproducibility is essentially 1.0 on real subprocess execution at standard tier with default config. Confidence: **HIGH**.

---

## Persona 2 — Refactorer (opus, depth=standard) — focus: blast radius

**What is the shape of this defect, and how many other places share it?**

The shape is: *two parallel registries (one for "is this a step?" and one for "what file does this step persist?") that must be kept in sync, with no compile-time or runtime enforcement of that synchronization.* The defect is a **registry-coherence bug**, not a one-off typo.

**Sibling registries that exhibit the same coupling:**

1. `_STAGE_A_STEPS` (executor.py:301-316) — declares 9 step IDs.
2. `_STEP_ARTIFACT_FILES` (executor.py:246-251) — declares 4 step IDs. Drift: 5 missing.
3. `GATE_CRITERIA` (gates.py:295+) — declares per-step gate config including `build-task-file` (gates.py:359). Drift partially overlaps with `_STEP_ARTIFACT_FILES` but is independently maintained.
4. `process.py:101` (`"build-task-file": ["build-request-template.md", "operational-guidance.md"]`) — yet another per-step lookup, by yet another key set.
5. `config.py:28` step-id regex enumeration — fifth parallel enumeration of the same conceptual set.

That is **five independent enumerations of "the steps"** spread across four files, each maintained by hand. Adding a new step requires editing each one, and the language gives the maintainer zero feedback if any is missed. The `build-task-file` defect is one realized drift; the unrealized variants are:

- `template-triage`, `check-existing` — both legitimately have no artifact (internal steps), so the absence is correct. Not latent bugs but also not distinguishable from the broken case by inspection.
- `verify-task-file`, `preparation` — also absent from `_STEP_ARTIFACT_FILES`. **These are subprocess steps** (`_STAGE_A_STEPS` line 314-315), and they have gate criteria. If their gates are STRICT and depend on disk content, they exhibit the identical bug; if STANDARD, they merely produce wrong gate evaluations silently. Worth confirming before fix.
- Stage B (`_execute_stage_b`) and `present-complete` step 15 — not inspected here but almost certainly use the same dispatch table by symmetry. **Recommend a follow-up sweep.**

**Latent variants in adjacent code:**

`_persist_step_artifact` (executor.py:976-1004) embeds the same lookup pattern (line 987-989) and the same silent fallthrough on miss. So one root cause produces *two* downstream failures per added step: (a) gate sees wrong content, (b) artifact is never persisted to its canonical name, breaking any downstream step that loads it by filename. The verify-task-file prompt at `prompts.py:405` does `list(config.task_dir.glob("TASK-PRD-*.md"))` — it globs rather than reading the canonical name, so it might paper over (a) but only because the subprocess wrote the file directly. The discipline is brittle: a future maintainer who relies on `_persist_step_artifact` to copy the file (per the docstring's contract) will be sandbagged.

**Class-of-defect verdict:** This is a *class* of defect (registry-coherence + silent fallthrough on `dict.get`), not a one-off. The fix that just adds one dict entry is a band-aid; the structural fix is either (i) collapsing the five enumerations into one source of truth keyed by step ID with a typed record, or (ii) replacing `dict.get` + fallthrough with `dict[key]` raising `KeyError` on miss for the registry whose absence corresponds to a real bug. Either makes the next drift loud instead of silent.

Blast radius: **medium-high** structurally; the *currently exploitable* surface in Stage A is at least `build-task-file` + likely `verify-task-file` + `preparation`. Confidence: **HIGH** on the pattern, **MEDIUM** on the exact count of sibling instances pending a sibling-step inspection.

---

## Persona 3 — Architect (sonnet, depth=standard) — focus: severity calibration

**Preliminary severity: CRITICAL. Is that right?**

Severity calibration test: *what does the defect actually break at runtime, and how often?*

- **Halts execution?** Yes — `PrdStepStatus.HALT` propagates to `result.outcome = "halt"` and breaks the Stage A loop (executor.py:380-389), terminating the pipeline before any of steps 8–15 run.
- **Silent corruption vs. loud failure?** Loud, but at the wrong layer. The error message reaching the user will be "STRICT gate failure: HALT" with "Min lines: 30/400" in the diagnostics log — the symptom is gate failure, the root cause is dispatch miss. This is loud-but-misleading, which is worse than a true silent corruption for *time-to-diagnose* but better for *time-to-detect*.
- **Wrong output?** Worse than wrong: no output at all for the primary deliverable. The PRD pipeline's purpose is producing a task file and downstream PRD; halting at step 7 means the user gets zero of the requested artifact even though they paid the cost of running steps 1–6. The pipeline is non-functional at standard tier on the default path.
- **Frequency of trigger?** The reproduction sketch is the *documented entry-point invocation* (`superclaude prd run "…" --tier standard`). This is not an edge case, not a corner config — it is the happy path. F-01's reproduction conditions are met by every standard-tier invocation that reaches step 7.
- **User-visible workarounds?** None at the CLI level. The user cannot pad NDJSON output. Skipping step 7 is not exposed as a flag. The pipeline must be patched to recover.

**Severity comparison against the calibration ladder:**

- LOW: cosmetic, edge case, easily worked around.
- MEDIUM: degraded behavior, default path still works.
- HIGH: default path breaks but a workaround exists, or breakage is confined to a non-primary feature.
- CRITICAL: default path of primary feature halts, no workaround.

This is unambiguously **CRITICAL**. The PRD pipeline is the headline feature of the `superclaude prd` CLI; step 7 (build-task-file) produces the headline artifact; the default invocation is the failing invocation; no workaround exists short of a code patch.

**Should severity move up or down?**

Not down — every demotion criterion fails. Not up — there is no higher tier than CRITICAL in this rubric, but I note for the record that this defect would also satisfy a hypothetical "release-blocker" tier: shipping the binary with this bug means the primary feature is broken on first use. If this audit gates a release, F-01 alone is sufficient grounds to block.

**Severity verdict: CRITICAL confirmed.** No adjustment recommended.

---

## Convergence

- **Verdict**: REAL
- **Convergence score**: 0.97 — All three personas independently confirmed the defect from different angles. Analyzer confirmed mechanical reproducibility. Refactorer found the defect is one instance of a broader registry-coherence pattern (slight scope expansion, not contradiction). Architect confirmed CRITICAL severity stands. The only "split" is Refactorer noting blast radius extends beyond the headline bug — that complements rather than contests the others.
- **Final severity (post-adjudication)**: CRITICAL
- **Fix difficulty**: XS (≤30 min) for the surface fix — adding `"build-task-file": "TASK-PRD-{slug}.md"` to `_STEP_ARTIFACT_FILES` plus handling the slug interpolation (the current dict values are static filenames, so either the value becomes a template or the lookup site interpolates). Realistically S (≤2h) once a regression test that doesn't bypass `_resolve_step_content` is added. The structural fix Refactorer recommends (collapse the five parallel enumerations into one typed registry, audit `verify-task-file` and `preparation` for the same defect) is M (≤1d).

**Synthesis:** All three personas agree this is a real, easily-reproduced, production-halting bug on the default PRD pipeline path. The evidence re-verification confirmed every cited file:line, including the negative claims about test coverage. The dispatch dict at `executor.py:246-251` is mechanically missing the `build-task-file` key, `_resolve_step_content` falls through to NDJSON commentary, the STRICT gate at `gates.py:359-368` fails with "Min lines: 30/400", and the pipeline halts at step 7. The e2e test suite cannot catch the regression because its mock writes pre-padded markdown directly into the subprocess output file, bypassing the dispatch logic entirely (`tests/cli/prd/test_e2e.py:245-247` combined with the raw-text fallback at `executor.py:130`). Refactorer's finding that the defect is the visible instance of a broader registry-coherence pattern (five parallel step enumerations across executor.py, gates.py, process.py, config.py) suggests the minimum fix should be paired with an audit of `verify-task-file` and `preparation` for the identical dispatch miss. F-01 is confirmed as a legitimate anchor bug and a release-blocker.
