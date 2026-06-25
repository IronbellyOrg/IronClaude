# Research — Doc Cross-Validator

**Topic type:** Doc Cross-Validator (design `merged-solution.md` code blocks + invariants vs actual source)
**Scope:** Validate every code-block claim and invariant in `/config/workspace/IronClaude/.dev/troubleshoot/merged-solution.md` against `src/superclaude/cli/prd/{prompts.py,executor.py,gates.py}`.
**Status:** In Progress
**Date:** 2026-06-06

---

## Sources read (this turn)

- `merged-solution.md` (design, full)
- `src/superclaude/cli/prd/executor.py` (full, 1198 lines)
- `src/superclaude/cli/prd/prompts.py` (full, 1455 lines)
- `src/superclaude/cli/prd/gates.py` (full, 515 lines)
- `src/superclaude/cli/prd/models.py` (PrdConfig def, lines 170-211)
- `src/superclaude/cli/prd/config.py` (path resolution, lines 100-139)
- `src/superclaude/cli/pipeline/models.py` (GateCriteria.required_frontmatter_fields def @135-149; work_dir @274)
- `pyproject.toml` (`requires-python = ">=3.10"` @16)

---

## Claim 1 — §1a `_artifact_path_for_step` 8-entry mapping vs `_STEP_ARTIFACT_FILES`

**[CODE-VERIFIED]** — `_STEP_ARTIFACT_FILES` is at **executor.py:252-263**. The 8-entry mapping in the design block (merged-solution.md:44-53) matches the source EXACTLY, key-for-key and value-for-value:

| step_id | design value (line 44-53) | source value (executor.py:253-262) | match |
|---|---|---|---|
| parse-request | parsed-request.json | parsed-request.json | ✓ |
| scope-discovery | scope-discovery-raw.md | scope-discovery-raw.md | ✓ |
| research-notes | research-notes.md | research-notes.md | ✓ |
| sufficiency-review | sufficiency-review.md | sufficiency-review.md | ✓ |
| research-qa | qa/qa-research-gate-report.md | qa/qa-research-gate-report.md | ✓ |
| synthesis-qa | qa/qa-synthesis-gate-report.md | qa/qa-synthesis-gate-report.md | ✓ |
| structural-qa | qa/qa-report-validation.md | qa/qa-report-validation.md | ✓ |
| qualitative-qa | qa/qa-qualitative-review.md | qa/qa-qualitative-review.md | ✓ |

**ZERO DRIFT.** The AC2 sync test (`test_prompt_executor_mapping_sync`) can assert exact equality with the dict as written in the design; no correction needed.

**Importability of `PrdConfig` / `Path` in prompts.py without circular import:**
- `Path`: **[CODE-VERIFIED]** already imported at prompts.py:17 (`from pathlib import Path`).
- `PrdConfig`: **[CODE-VERIFIED — CAVEAT]** prompts.py imports `PrdConfig` only under `TYPE_CHECKING` (prompts.py:26-27: `if TYPE_CHECKING: from superclaude.cli.prd.models import PrdConfig`). All existing builder signatures annotate `config: PrdConfig` and rely on `from __future__ import annotations` (prompts.py:13) so the name is never evaluated at runtime. The design's helper signature `def _artifact_path_for_step(config: PrdConfig, step_id: str) -> Path | None` follows the SAME idiom — the `PrdConfig` annotation is a string under PEP 563, so **no runtime import is needed and no circular import is introduced.** The builder must NOT add a runtime `from ...models import PrdConfig`; keep it TYPE_CHECKING-only. Verdict: feasible as designed.

---

## Claim 2 — §1b CRITICAL Output Location block

**The 4 target builders exist and currently LACK an output pin:**

- `build_scope_discovery_prompt` — **[CODE-VERIFIED]** prompts.py:110-191. No "Output path:"/"Write the document to" pin; the prompt's `OUTPUT FORMAT:` section (prompts.py:154) just says "Write a markdown document with these sections" — no filename/location. CONFIRMED un-pinned.
- `build_research_notes_prompt` — **[CODE-VERIFIED]** prompts.py:194-266. Says "Produce a research-notes.md file" (line 222) but gives no absolute path / directory. No pin. CONFIRMED un-pinned.
- `build_sufficiency_review_prompt` — **[CODE-VERIFIED]** prompts.py:269-319. Asks to "Return JSON" (line 301); no output-path pin at all. CONFIRMED un-pinned.
- `build_preparation_prompt` — **[CODE-VERIFIED]** prompts.py:516-558. Writes a `.preparation-complete` marker but no pin for a gated artifact named `sufficiency-review.md` etc. CONFIRMED un-pinned (note: preparation's gate is LIGHT min_lines=0, so this builder is the weakest beneficiary — see Risk note below).

**`build_task_file_prompt` HAS the idiom (the model to copy):**
**[CODE-VERIFIED]** prompts.py:439: `Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}`. This is the exact established pattern. NOTE: the design (merged-solution.md:72) cites this idiom "at prompts.py:439" — that line number is **CURRENT AND CORRECT**. Other builders with an `Output path:` pin: `build_analyst_completeness_prompt` (prompts.py:887), `build_qa_research_gate_prompt` (956), `build_assembly_prompt` (1197 `Output path: {config.output_path}`), `build_structural_qa_prompt` (1267), `build_qualitative_qa_prompt` (1321), plus the dual-mode render fns (`_render_investigation_prompt` :746, `_render_web_research_prompt` :830, `_render_synthesis_prompt` :1017). So the "~12 other builders" claim is borne out.

**`config.task_dir` renders an absolute path:**
**[CODE-VERIFIED]** config.py:103-125. `output_path` is always `.resolve()`d (line 104 `Path(output).resolve()`, line 109 `Path(".dev/eval-workspaces").resolve()`, line 117 `Path(".").resolve()`), and `task_dir = output_path / task_dir_name` (config.py:125). Therefore `config.task_dir` is absolute and `config.task_dir / "research-notes.md"` interpolates an absolute path into the prompt. CONFIRMED — the pin will be absolute as the design requires.

> **RISK FLAG for builder (not a contradiction):** `build_preparation_prompt` does NOT load or emit any of the 8 canonical artifacts; its gated output is just a `.preparation-complete` status report (gate tier LIGHT, min_lines=0). Pinning a canonical-artifact path into it is semantically odd. The design lists it as one of "four un-pinned document builders," but its inclusion is the loosest fit. Builder should double-check whether preparation needs a pin at all, OR pin the `.preparation-complete` marker path rather than a canonical artifact name. This is the one soft spot in §1b.

---

## Claim 3 — §2a `_STEP_ARTIFACT_PATTERNS` placement (~252) + step_ids

**[CODE-CONTRADICTED — line number]** Design says "executor.py ~252". Line 252 today is the OPENING line of `_STEP_ARTIFACT_FILES` (`_STEP_ARTIFACT_FILES: dict[str, str] = {`). The dict spans **252-263**. Placing `_STEP_ARTIFACT_PATTERNS` "beside" it is feasible, but the correct insertion point is **after line 263** (after the closing `}` of `_STEP_ARTIFACT_FILES`), not at 252. Builder: insert at ~264, before `_resolve_step_content` (def at line 266). Feasibility: ✓; line cite is slightly stale (off by ~12 lines).

**step_ids in the pattern map (`scope-discovery`, `research-notes`, `sufficiency-review`):** **[CODE-VERIFIED]** all three are valid keys in `_STEP_ARTIFACT_FILES` (executor.py:254,255,256) and valid Stage A step_ids (executor.py:376,377,379-383 `_STAGE_A_STEPS`). The design's empty-entry semantics ("Empty/missing entry → fall back to exact-name behavior") aligns with how 2c will use `.get(step_id) or [exact]`. ✓

---

## Claim 4 — §2b bounded WHERE roots

**Does `parsed-request.json` get written to task_dir, and is the key "WHERE"?**
- **[CODE-VERIFIED]** Key name is `WHERE` (uppercase). `build_parse_request_prompt` (prompts.py:60-107) instructs the agent to emit JSON with `"WHERE": [<list of source directories>]` (prompts.py:87). Downstream readers use the same uppercase key: `build_scope_discovery_prompt` reads `parsed.get("WHERE")` / `parsed["WHERE"]` (prompts.py:117-118). So the design's `parsed.get("WHERE")` (merged-solution.md:110) matches the real key. ✓
- **[CODE-VERIFIED]** `parsed-request.json` is written to `task_dir`: `_persist_step_artifact` writes `_STEP_ARTIFACT_FILES["parse-request"]` = `parsed-request.json` to `self._config.task_dir / artifact_name` (executor.py:1156-1166), and JSON artifacts get fence-stripped first (executor.py:1161-1162). Consumers read `config.task_dir / "parsed-request.json"` (prompts.py:116, 201). CONFIRMED written to task_dir with key WHERE.

**`task_dir.parent` semantics:** **[CODE-VERIFIED]** task_dir = `output_path/prd-<slug>` (config.py:124-125), so `task_dir.parent` = `output_path` (the eval-workspace / output root). The design uses `repo_root = task_dir.parent` (merged-solution.md:109) — note this is the OUTPUT root, NOT necessarily the git repo root. WHERE entries from the user are typically source dirs relative to CWD/repo, so resolving `repo_root / where` against `task_dir.parent` (= output dir) may not point at real source dirs when output is `.dev/eval-workspaces/`. **FLAG:** this is a latent semantic mismatch — `task_dir.parent` being `.dev/eval-workspaces` means `(repo_root / where)` for a WHERE like `src/superclaude` would resolve to `.dev/eval-workspaces/src/superclaude`, which won't exist → the containment/`exists()` guards (merged-solution.md:113-121) will simply skip it (`real.is_dir()` false), so it FAILS SAFE (no crash, just no extra root added). Not a contradiction of the code blocks, but the builder should know the WHERE-root widening will frequently be a no-op under the default sandbox output dir. The freshness/containment guards make this safe; it just may not deliver the recovery benefit the design implies in sandbox runs.

**Python >=3.10 for `resolve(strict=True)` + `relative_to` + `is_relative_to`:**
**[CODE-VERIFIED]** pyproject.toml:16 `requires-python = ">=3.10"`. `Path.resolve(strict=...)` (3.6+), `relative_to` (3.4+), and `Path.is_relative_to` (3.9+, used in 2d) are all available on >=3.10. ✓

---

## Claim 5 — §2c pattern-aware search exclusions + current rglob

**Current code already does rglob:** **[CODE-VERIFIED]** `_resolve_step_content` already does `root.rglob(base_name)` over `search_roots = [task_dir, task_dir.parent]` (executor.py:347-353). The design's 2c block (merged-solution.md:131-145) generalizes this to iterate `patterns` and `root.rglob(pattern)`. Feasible — it's a superset of current behavior.

**Exclusions make sense vs current code:** **[CODE-VERIFIED]** current code already skips the SAME set: `skip_parts = {"node_modules", ".git", "__pycache__"}` and `"-output.txt" in match.name` (executor.py:354-356). The design block (merged-solution.md:136-138) reproduces this exactly. CONFIRMED consistent — no new exclusion semantics, just re-expressed. ✓

---

## Claim 6 — §2d `_pick_best_candidate` + sort-key discrepancy

**`Path.is_relative_to` exists (Py3.9+):** **[CODE-VERIFIED]** requires-python >=3.10 (pyproject.toml:16) → available. ✓
**`path.stat().st_mtime`:** stdlib, always available. ✓

**SORT-KEY DISCREPANCY (design vs BUILD_REQUEST) — FLAGGED:**
- merged-solution.md:178 sort key: `return (in_pref, path.stat().st_mtime, len(content), -len(path.parts))` → tuple `(int in_pref, float mtime, int len, int -parts)`.
- merged-solution.md docstring (lines 163-168) describes priority order: (1) inside preferred_root, (2) most recently modified mtime, (3) longest content, (4) fewest path parts.
- The CODE BLOCK and the DOCSTRING in merged-solution.md are **internally consistent** (in_pref → mtime → len → -parts).
- The task brief notes BUILD_REQUEST AC4/§2d phrases the first element as `in_preferred_root` (vs the code's local var `in_pref`). This is a **naming-only** difference, NOT a behavioral one — same field, same position, same ordering. **No behavioral discrepancy.** Builder may keep the variable name `in_pref` (used in the code block) or rename to `in_preferred_root` for readability; either is correct as long as the 4-tuple order is `(in_pref/in_preferred_root, mtime, len(content), -len(path.parts))`. The ONE thing to preserve is **mtime outranks len(content)** (INV-006), which both the design code block and docstring honor. ✓ consistent.

**Contrast with current code (INV-006 change):** **[CODE-VERIFIED]** current `_resolve_step_content` uses pure "largest wins": `if len(content) > len(best_content): best_content = content` (executor.py:360, also :298-299 and :329-330 in the special-cases). The design's `_pick_best_candidate` replaces ONLY the generic-path comparison at executor.py:360 (the design's INV-006 note cites "executor.py:360" — **CORRECT current line**). NOTE: the design does NOT touch the build-task-file (:298) or assembly (:329) "largest wins" loops — backward-compat § stmts confirm those stay untouched. ✓

---

## Claim 7 — §3a `_check_no_truncation_marker` return convention

**[CODE-VERIFIED]** gates.py check functions follow `Callable[[str], bool | str]` — return `True` on pass, return an error string on failure. Documented at gates.py:14-21 ("Return True on pass / Return an error string on failure") and NFR-PRD.2 (gates.py:21). Every existing check matches: e.g. `_check_verdict_field` (gates.py:36-61) returns `True` or `"No verdict field found..."`; `_check_no_placeholders` (gates.py:64-83) same. The design's `_check_no_truncation_marker` (merged-solution.md:194-198) returns a string on detection and `True` otherwise → **EXACTLY matches the convention.** Wiring: it must be registered via `_make_semantic_check(...)` (gates.py:271-281) inside a gate's `semantic_checks=[...]` list to actually run (the design block shows the function but the builder must add the registration; the test plan item 3 implies this). ✓ convention correct.

---

## Claim 8 — §3b split guard INV-010 (`output_text` NDJSON vs `gate_content` disk)

**[CODE-VERIFIED — with line corrections]** The two inputs are genuinely separate in `_run_subprocess_step`:
- `output_text` = NDJSON-extracted assistant text: executor.py:**609** `output_text = _extract_text_from_stream_json(raw_output) if raw_output else ""`. (Design cites ~609 — **CORRECT**.)
- `gate_content` = disk-resolved content: executor.py:**613-615** `gate_content = _resolve_step_content(step_id, self._config.task_dir, output_text)`. (Design cites ~613 — **CORRECT**; spans 613-615.)
- `_determine_status` reads `output_text` (NDJSON) for sentinel detection: executor.py:**618** `status = self._determine_status(exit_code, output_text, step_id)`. (Design cites ~618 — **CORRECT**.) Inside, `_determine_status` calls `_detect_sentinel(output)` on that NDJSON text (executor.py:662).
- Gate reads `gate_content` (disk): executor.py:**623** `gate_passed = self._evaluate_gate(step_id, gate, gate_content)`. (Design says "the gate evaluates the disk gate_content (executor.py:613)" — the *binding* is at 613, the *use* at 623.)
- `_determine_status` definition: executor.py:**645-676**. (Design cites 645-676 — **EXACTLY CORRECT**.)

**INV-010 CONFIRMED:** the NDJSON `output_text` (sentinel/verdict detection input) and the disk `gate_content` (gate min_lines + semantic input) are two distinct variables fed to two distinct functions. They MUST stay separate; collapsing them would strip sentinel detection of its NDJSON input (or feed the gate raw commentary). The design's guard-comment/assertion is sound. **Note:** `_determine_status` also does QA verdict string-matching on the same `output` (NDJSON) at executor.py:669-673 — another reason the NDJSON channel must be preserved. ✓

---

## Claim 9 — INV-001: `_evaluate_gate` never reads `required_frontmatter_fields`

**[CODE-VERIFIED] — INV-001 CONFIRMED CORRECT.** `_evaluate_gate` (executor.py:678-715) reads ONLY: `gate.min_lines` (line 687-689) and `gate.semantic_checks` (line 703-705 → `check.check_fn(content)`). It NEVER references `required_frontmatter_fields`.

**Full grep of the prd package for `required_frontmatter_fields`:**
- **Definition:** `pipeline/models.py:149` `required_frontmatter_fields: list[str | tuple[str, ...]]` (field on `GateCriteria`); docstring at pipeline/models.py:135-148 describes accepted shapes.
- **Population (data only, 18 hits):** gates.py:306,312,325,331,349,362,368,397,410,416,422,435,441,447,460,484,497,510 — all are `required_frontmatter_fields=[...]` assignments inside `GATE_CRITERIA` entries. Three are non-empty: research-notes = `["Date","Scenario","Tier"]` (gates.py:331), build-task-file = `["id","title","status","complexity","created_date"]` (gates.py:368), assembly = `["id","title","status","created_date","tags"]` (gates.py:460).
- **READ at gate time:** **ZERO.** No hit in executor.py. `_evaluate_gate` does not read it; `_determine_status` does not read it; nothing in the PRD pipeline consumes the field. It is a **dead constraint** in the PRD gate path, exactly as INV-001 claims.

**Conclusion:** The design's decision to DROP the frontmatter mandate (merged-solution.md:74-75) is **CORRECT**. The research-notes prompt already emits `Date/Scenario/Tier` frontmatter (prompts.py:**224-228** — design cites 224-228, **EXACTLY CORRECT**), and even if it didn't, the gate would not fail on it. Adding a prompt mandate would be pure noise. ✓✓

---

## Claim 10 — INV-005/INV-006: anti-widening guard + "largest wins" tiebreak

**INV-005 anti-widening guard — [CODE-CONTRADICTED — line number, guard exists but elsewhere]:**
The design (merged-solution.md:124) cites "the anti-widening comment at executor.py:290-292." Reading executor.py:289-292, that comment block IS present:
```
289  # Glob is scoped to task_dir only (not task_dir.parent) because
290  # prompts.py:381 writes the task file deterministically into
291  # task_dir; widening the search would re-introduce multi-match
292  # ambiguity (e.g. from prior failed runs in sibling directories).
```
So the comment spans **289-292** (design says 290-292 — off by one at the top; the load-bearing "widening would re-introduce multi-match ambiguity" sentence is at 291-292, **correct**). NOTE: this guard is in the **build-task-file** special case (executor.py:293-304), NOT in the generic WHERE-search path that §2b widens. The design correctly references it as the *precedent/rationale* for why widening is risky. INV-005's mitigation (realpath containment + symlink reject + freshness tiebreak) is therefore guarding a DIFFERENT code path (the generic `search_roots` at executor.py:347-349) than where the cited comment lives. Substantively fine; the cross-reference is to a rationale comment, not to code being modified. **Also note** the comment at 289-292 references "prompts.py:381" for where the task file is written — but the ACTUAL write-path pin is at **prompts.py:439** (`Write the task file to:`), and prompts.py:378 builds the `existing_task_file` Path. prompts.py:381 today is inside the `_preserve_guard_note` checklist arg, NOT the write instruction. **STALE CROSS-REF in source itself** (executor.py:290 says "prompts.py:381" but the real write is :439) — pre-existing inaccuracy, builder may optionally correct the comment.

**INV-006 "largest wins" tiebreak at ~360 — [CODE-VERIFIED]:** executor.py:**360** `if len(content) > len(best_content):` inside the generic search loop (executor.py:352-363). Design's INV-006 note (merged-solution.md:183) cites "executor.py:360" — **EXACTLY CORRECT**. This is the line `_pick_best_candidate` replaces. ✓

---

## Claim 11 — LINE-NUMBER DRIFT TABLE

For every function/anchor the design or BUILD_REQUEST touches. "Design-cited" = number in merged-solution.md; "Actual" = current source line verified this turn.

| Anchor / function | Design-cited line | Actual current line | Status |
|---|---|---|---|
| `_artifact_path_for_step` insertion (prompts.py) | "~line 53" | helpers end ~53 (`_today` def 50-52); insert after 53 OK | ✓ feasible (after line 53) |
| `_STEP_ARTIFACT_FILES` dict (executor.py) | implied ~252 | **252-263** | ✓ (252 = opening line) |
| `_STEP_ARTIFACT_PATTERNS` placement (executor.py) | "~252" | insert **after 263** (before `_resolve_step_content`@266) | ⚠ stale by ~12 lines |
| `_resolve_step_content` def (executor.py) | 266-365 (status §) | **266-365** | ✓ exact |
| bounded WHERE roots insertion (executor.py) | "~339" | current `search_roots` block **347-349** | ⚠ stale by ~8 lines |
| pattern-aware search (executor.py) | "~351" | current rglob loop **351-363** | ✓ (351 = loop start) |
| "largest wins" line to replace (executor.py) | 360 | **360** | ✓ exact |
| anti-widening comment (executor.py) | 290-292 | **289-292** | ⚠ off-by-one at top |
| `build_task_file_prompt` pin idiom (prompts.py) | 439 | **439** | ✓ exact |
| research-notes frontmatter emission (prompts.py) | 224-228 | **224-228** | ✓ exact |
| `_evaluate_gate` (executor.py) | 678-715 | **678-715** | ✓ exact |
| `_determine_status` (executor.py) | 645-676 | **645-676** | ✓ exact |
| output_text NDJSON assignment (executor.py) | ~609 | **609** | ✓ exact |
| gate_content disk assignment (executor.py) | ~613 | **613**(-615) | ✓ exact |
| `_determine_status` call w/ output_text (executor.py) | ~618 | **618** | ✓ exact |
| `_evaluate_gate` call w/ gate_content (executor.py) | (613) | binding 613, use **623** | ✓ |
| `build_scope_discovery_prompt` (target builder) | named | **110-191** | ✓ exists, un-pinned |
| `build_research_notes_prompt` (target builder) | named | **194-266** | ✓ exists, un-pinned |
| `build_sufficiency_review_prompt` (target builder) | named | **269-319** | ✓ exists, un-pinned |
| `build_preparation_prompt` (target builder) | named | **516-558** | ✓ exists, un-pinned (weak fit) |
| `prompts.py:381` cross-ref (in executor.py comment) | n/a (source comment) | real write at **439**; 381 is unrelated | ⚠ pre-existing stale source comment |

---

## Status: Complete

### Summary

All Layer 1-3 design code blocks and invariants in `merged-solution.md` are **feasible and substantially CODE-VERIFIED** against current `src/superclaude/cli/prd/{prompts.py,executor.py,gates.py}`. The design is sound; the only issues are minor line-number drift (cosmetic, fixed in the drift table above) and two soft semantic flags the builder should note.

**CONTRADICTED / CORRECTED claims (none are blocking):**
1. **§2a placement line "~252"** — `_STEP_ARTIFACT_PATTERNS` should be inserted **after line 263** (end of `_STEP_ARTIFACT_FILES`), not at 252. Off by ~12 lines.
2. **§2b bounded-WHERE roots line "~339"** — current `search_roots` construction is at **347-349**, not 339. Off by ~8 lines.
3. **INV-005 comment "290-292"** — actual anti-widening comment is **289-292** (off-by-one at top); and it lives in the build-task-file special case, referenced as rationale only (not the code being modified — fine).
4. **Pre-existing source staleness (not a design error):** executor.py:290 comment says the task file is written at "prompts.py:381"; the real write instruction is **prompts.py:439**. Builder may optionally fix this comment.

**Soft FLAGS (verify during build, not contradictions):**
- **§1b — `build_preparation_prompt` is the weakest pin target.** It emits only a `.preparation-complete` marker (gate tier LIGHT, min_lines=0) and loads no canonical artifact. Confirm whether it needs a canonical-artifact pin at all, or whether the design meant a different 4th builder. The other three (scope-discovery, research-notes, sufficiency-review) are clean, correct targets.
- **§2b — `task_dir.parent` = the OUTPUT root (e.g. `.dev/eval-workspaces/`), not the git repo root.** So `(repo_root / where)` for source-relative WHERE entries will usually not exist under the default sandbox, making the WHERE-root widening a frequent no-op. It FAILS SAFE (guards skip non-existent/non-dir roots, no crash), so it's not a correctness bug — but the recovery benefit the design implies will rarely fire in sandboxed runs. Layer 1 pinning (the primary fix) is unaffected.

**Fully CONFIRMED design decisions:**
- **Claim 1:** 8-entry mapping is byte-identical to `_STEP_ARTIFACT_FILES` (executor.py:252-263) — **zero drift**; AC2 sync test can use the dict verbatim. `PrdConfig` annotation safe under `TYPE_CHECKING` + `from __future__ import annotations` — no circular import.
- **Claim 2:** all 4 builders exist & lack pins; `build_task_file_prompt` (prompts.py:439) is the working idiom; `config.task_dir` is absolute (config.py:104/125 `.resolve()`).
- **Claim 4:** WHERE key is uppercase `"WHERE"` (prompts.py:87); `parsed-request.json` written to task_dir (executor.py:1156-1166); Python >=3.10 confirmed (pyproject.toml:16) → `resolve(strict=True)`/`relative_to`/`is_relative_to` all available.
- **Claim 5:** current code already rglobs (executor.py:353) with identical exclusions (executor.py:354-356).
- **Claim 6:** sort key `(in_pref, mtime, len, -parts)` is internally consistent design-side; the BUILD_REQUEST `in_preferred_root` vs code `in_pref` is **naming-only, no behavioral discrepancy**; mtime>len (INV-006) honored.
- **Claim 7:** gates.py check convention is `bool | str` (return True / error string) — design's `_check_no_truncation_marker` matches exactly (must be registered via `_make_semantic_check`).
- **Claim 8/INV-010:** `output_text` (NDJSON, executor.py:609) and `gate_content` (disk, executor.py:613) are genuinely separate; `_determine_status` reads output_text (618/662), gate reads gate_content (623). All cited lines (609/613/618, 645-676) **exact**.
- **Claim 9/INV-001:** `_evaluate_gate` (executor.py:678-715) reads ONLY min_lines + semantic_checks; `required_frontmatter_fields` has 18 population sites in gates.py but **ZERO read sites** anywhere in the pipeline — dead constraint. Dropping the frontmatter mandate is correct.
- **Claim 10/INV-006:** "largest wins" at executor.py:360 — **exact**, this is the only generic line `_pick_best_candidate` replaces; special-case loops (298,329) correctly left untouched per backward-compat.
