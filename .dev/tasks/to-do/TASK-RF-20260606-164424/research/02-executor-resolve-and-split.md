# Research

**Topic type:** Data Flow Tracer — executor.py recovery + NDJSON↔disk split
**Scope:** `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py` ONLY
**Status:** Complete
**Date:** 2026-06-06
**File length:** 1197 lines (`wc -l`)

---

## Line-number reconciliation vs BUILD_REQUEST estimates

BUILD_REQUEST approximations were OFF. Confirmed current line numbers:

| Symbol | BUILD_REQUEST estimate | ACTUAL |
|---|---|---|
| `_STEP_ARTIFACT_FILES` | ~252-365 (conflated) | **252-263** |
| `_resolve_step_content` | ~252-365 | **266-365** |
| `output_text` / `gate_content` / `_determine_status` | ~609/618 / ~613 / ~645-676 | **609 / 613-615 / 645-676** |
| `_evaluate_gate` | ~678-715 | **678-715** (exact match) |
| `_persist_step_artifact` | ~1156-1166 | **1145-1173** (def at 1145, not 1156) |
| anti-widening guard | ~290-292 | **289-292** |
| build-task-file/assembly special-cases | ~309-336 | **293-337** (build-task-file 293-304, assembly 306-337) |
| "largest wins" tiebreak | ~360 | **360-361** (and duplicated at 298-299, 329-330) |
| zero-match fallback | ~365 | **365** (exact match) |

---

## 1. `_STEP_ARTIFACT_FILES` (executor.py:252-263)

Full dict verbatim:

```python
252:_STEP_ARTIFACT_FILES: dict[str, str] = {
253:    "parse-request": "parsed-request.json",
254:    "scope-discovery": "scope-discovery-raw.md",
255:    "research-notes": "research-notes.md",
256:    "sufficiency-review": "sufficiency-review.md",
257:    # QA steps write their report to qa/; the NDJSON stdout only holds
258:    # commentary, so gate evaluation must read the report file on disk.
259:    "research-qa": "qa/qa-research-gate-report.md",
260:    "synthesis-qa": "qa/qa-synthesis-gate-report.md",
261:    "structural-qa": "qa/qa-report-validation.md",
262:    "qualitative-qa": "qa/qa-qualitative-review.md",
263:}
```

**8 keys → filenames:**

| key | filename |
|---|---|
| `parse-request` | `parsed-request.json` |
| `scope-discovery` | `scope-discovery-raw.md` |
| `research-notes` | `research-notes.md` |
| `sufficiency-review` | `sufficiency-review.md` |
| `research-qa` | `qa/qa-research-gate-report.md` |
| `synthesis-qa` | `qa/qa-synthesis-gate-report.md` |
| `structural-qa` | `qa/qa-report-validation.md` |
| `qualitative-qa` | `qa/qa-qualitative-review.md` |

**Confirmation vs merged-solution mirror:** The 8 KEYS match exactly the merged-solution list
(parse-request, scope-discovery, research-notes, sufficiency-review, research-qa, synthesis-qa,
structural-qa, qualitative-qa). The keys are identical. This drives the **AC2 sync test** —
the canonical filename VALUES above are the source of truth (note three QA values carry a `qa/`
path prefix, not a bare filename).

**Critical note (load-bearing for the hotfix):** `build-task-file` and `assembly` are
DELIBERATELY ABSENT from this dict (they use dynamic filenames). The comment at lines 283-287
explicitly warns: *"do NOT add 'build-task-file' to _STEP_ARTIFACT_FILES"* because
`_persist_step_artifact` keys on the same dict and would clobber the LLM-authored task file.
Any AC2 sync test must NOT expect these two steps in the dict.

---

## 2. `_resolve_step_content` (executor.py:266-365)

### Signature (line 266)

```python
266:def _resolve_step_content(step_id: str, task_dir: Path, ndjson_text: str) -> str:
```

**Param order/names CONFIRMED:** `(step_id: str, task_dir: Path, ndjson_text: str)`.
The design doc's call `_resolve_step_content("scope-discovery", task_dir, "<ndjson>")` matches —
3rd positional param is the NDJSON/fallback text and is named **`ndjson_text`** (NOT
`output_text` or `fallback`). New code referencing the fallback must use `ndjson_text`.

### Docstring (267-278) — describes current behavior

```python
267:    """Resolve the best content for gate evaluation and artifact persistence.
268:
269:    Subprocesses may write their real output to disk via Write/Edit tools
270:    at unpredictable locations (``task_dir/results/``, ``.dev/``, etc.).
271:    The NDJSON stdout only captures the assistant's commentary.
272:
273:    This function searches for files matching the artifact name under
274:    ``task_dir`` and its parent directory (the project root, where
275:    subprocesses may write to ``.dev/`` or ``results/``).  Picks the
276:    largest match and returns it.  Falls back to NDJSON text if no
277:    disk file is found.
278:    """
```

### Anti-widening guard + comment (executor.py:289-304) — narrows the build-task-file glob

The guard is the COMMENT at 289-292 explaining why the build-task-file glob (line 295) is scoped
to `task_dir` only, NOT `task_dir.parent`:

```python
288:    #
289:    # Glob is scoped to task_dir only (not task_dir.parent) because
290:    # prompts.py:381 writes the task file deterministically into
291:    # task_dir; widening the search would re-introduce multi-match
292:    # ambiguity (e.g. from prior failed runs in sibling directories).
293:    if step_id == "build-task-file":
294:        best_content = ""
295:        for match in task_dir.glob("TASK-PRD-*.md"):
296:            try:
297:                content = match.read_text(encoding="utf-8", errors="replace")
298:                if len(content) > len(best_content):
299:                    best_content = content
300:            except OSError:
301:                continue
302:        if best_content.strip():
303:            return best_content
304:        # Fall through to NDJSON fallback if no task file found.
```

**What it narrows:** Restricts the `TASK-PRD-*.md` glob to `task_dir.glob(...)` (non-recursive,
single dir) instead of `task_dir.parent.rglob(...)`. Prevents matching stale task files from
prior failed runs in sibling directories.

### `build-task-file` / `assembly` special-case blocks — MUST STAY INTACT

**build-task-file block (293-304):** quoted above. Uses `task_dir.glob("TASK-PRD-*.md")`,
non-recursive, largest-wins, falls through to NDJSON on no match.

**assembly block (306-337):**

```python
306:    # Special-case: assembly writes the final PRD to a dynamic path under
307:    # results/ (or output_path). The NDJSON stdout only holds commentary,
308:    # so the gate (min_lines=800 + section checks) must read the PRD file.
309:    if step_id == "assembly":
310:        best_content = ""
311:        search_dirs = [task_dir / "results", task_dir, task_dir.parent]
312:        for d in search_dirs:
313:            if not d.is_dir():
314:                continue
315:            for match in d.glob("*.md"):
316:                if "-output.txt" in match.name:
317:                    continue
318:                # Only a PRD-named file is the assembled PRD. The pipeline
319:                # always writes the assembled document as PRD_*.md; a bare
320:                # markdown-heading probe would false-match Stage A artifact
321:                # files (research-notes.md, sufficiency-review.md, ...)
322:                # that the executor persists into task_dir.
323:                if "prd" not in match.name.lower():
324:                    continue
325:                try:
326:                    content = match.read_text(encoding="utf-8", errors="replace")
327:                except OSError:
328:                    continue
329:                if len(content) > len(best_content):
330:                    best_content = content
331:            # Skip the broader task_dir / task_dir.parent search once a
332:            # candidate has been found in an earlier (more specific) dir.
333:            if best_content:
334:                break
335:        if best_content.strip():
336:            return best_content
337:        # Fall through to NDJSON if nothing found.
```

assembly uses an ordered `search_dirs = [task_dir / "results", task_dir, task_dir.parent]`
(most-specific-first), non-recursive `d.glob("*.md")`, with TWO filters (`-output.txt` skip +
`"prd" not in match.name.lower()` skip), largest-wins, and an early-break once any dir yields a
candidate. NOTE: this `"prd"` substring + ordered-dir + early-break pattern is a precursor to the
"pattern-aware search + bounded WHERE roots" the Layer 2 hotfix generalizes.

### The generic (dict-keyed) path (339-365)

```python
339:    artifact_name = _STEP_ARTIFACT_FILES.get(step_id)
340:    if not artifact_name:
341:        return ndjson_text
342:
343:    base_name = Path(artifact_name).name
344:
345:    # Search task_dir and its parent (project root) — bounded scope
346:    # to avoid searching unrelated directories.
347:    search_roots = [task_dir]
348:    if task_dir.parent.exists():
349:        search_roots.append(task_dir.parent)
350:
351:    best_content = ""
352:    for root in search_roots:
353:        for match in root.rglob(base_name):
354:            # Skip NDJSON output files, node_modules, and .git
355:            skip_parts = {"node_modules", ".git", "__pycache__"}
356:            if "-output.txt" in match.name or skip_parts & set(match.parts):
357:                continue
358:            try:
359:                content = match.read_text(encoding="utf-8", errors="replace")
360:                if len(content) > len(best_content):
361:                    best_content = content
362:            except OSError:
363:                continue
364:
365:    return best_content if best_content.strip() else ndjson_text
```

**Current rglob logic over task_dir / task_dir.parent (343-353):**
- `base_name = Path(artifact_name).name` — strips the `qa/` prefix for QA steps, so QA reports
  are matched by BARE filename (e.g. `qa-research-gate-report.md`) anywhere in the tree.
- `search_roots = [task_dir]` plus `task_dir.parent` IF it exists (348-349).
- `root.rglob(base_name)` — **RECURSIVE** glob over each root (line 353). This is the
  widening that the Layer 2 "bounded WHERE roots" fix is meant to constrain.
- Skip filter: `"-output.txt" in match.name` OR any of `{"node_modules", ".git", "__pycache__"}`
  in `match.parts` (355-356).

**"largest wins" tiebreak (executor.py:360-361):**

```python
360:                if len(content) > len(best_content):
361:                    best_content = content
```

This is the exact `len(content) > len(best_content)` comparison the design replaces with
`_pick_best_candidate`. NOTE it appears in THREE places: 298-299 (build-task-file), 329-330
(assembly), and 360-361 (generic). The generic one at 360-361 is the primary target; the design
should clarify whether the special-case copies also migrate to `_pick_best_candidate`.

**Zero-match fallback (executor.py:365):**

```python
365:    return best_content if best_content.strip() else ndjson_text
```

Returns `best_content` if non-blank, otherwise the **`ndjson_text`** parameter (the NDJSON
fallback). Confirmed variable returned on zero-match = `ndjson_text`. There is also an EARLY
fallback at line 341 (`return ndjson_text`) when `step_id` has no dict entry AND is not one of
the special-cased steps.

### Local variable names (for clean integration)

- `step_id` — param (str), the pipeline step key.
- `task_dir` — param (Path), the task working directory.
- `ndjson_text` — param (str), the NDJSON/commentary fallback. **Use this name for fallback.**
- `artifact_name` — `_STEP_ARTIFACT_FILES.get(step_id)` (may include `qa/` prefix), line 339.
- `base_name` — `Path(artifact_name).name` (bare filename), line 343.
- `search_roots` — list[Path], the rglob roots, line 347.
- `search_dirs` — list[Path], the assembly-only ordered glob dirs, line 311.
- `best_content` — str accumulator for largest-match, reused in all three blocks.
- `match` — loop var (Path) over glob/rglob results.
- `content` — str, current file's text.
- `root` / `d` — loop vars over search roots/dirs.
- `skip_parts` — set of dir names to exclude, line 355.

---

## 3. The `output_text` ↔ `gate_content` split (INV-010) — executor.py:609-637

This is the split that MUST be preserved and get a guard comment.

```python
602:        # Read output and extract assistant text from NDJSON
603:        raw_output = ""
604:        try:
605:            raw_output = output_file.read_text(encoding="utf-8", errors="replace")
606:        except OSError:
607:            pass
608:
609:        output_text = _extract_text_from_stream_json(raw_output) if raw_output else ""
610:
611:        # Resolve best content: prefer files written to disk by the
612:        # subprocess over extracted NDJSON commentary
613:        gate_content = _resolve_step_content(
614:            step_id, self._config.task_dir, output_text
615:        )
616:
617:        # Determine status (uses NDJSON text for sentinel detection)
618:        status = self._determine_status(exit_code, output_text, step_id)
619:
620:        # Gate evaluation (uses resolved content — disk file or NDJSON)
621:        gate = GATE_CRITERIA.get(step_id)
622:        if gate and status.is_success:
623:            gate_passed = self._evaluate_gate(step_id, gate, gate_content)
624:            ...
636:        if exit_code == 0 and gate_content.strip():
637:            self._persist_step_artifact(step_id, gate_content)
```

**The split, precisely:**

| Variable | Source | Computed at | Consumed by |
|---|---|---|---|
| `output_text` | NDJSON stdout via `_extract_text_from_stream_json(raw_output)` | **line 609** | `_determine_status(exit_code, output_text, step_id)` at **line 618** (sentinel/verdict detection); also passed as the `ndjson_text` fallback arg into `_resolve_step_content` at **614** |
| `gate_content` | disk file (or NDJSON fallback) via `_resolve_step_content(...)` | **lines 613-615** | `_evaluate_gate(step_id, gate, gate_content)` at **line 623** AND `_persist_step_artifact(step_id, gate_content)` at **line 637** |

**Why the split must survive (INV-010):**
- `_determine_status` consumes **`output_text` (NDJSON)** so it can detect the
  EXIT_RECOMMENDATION / HALT / CONTINUE sentinels and QA verdict strings in the assistant's
  COMMENTARY stream — these sentinels live in stdout, NOT in the on-disk artifact.
- The gate + persistence consume **`gate_content` (disk)** so they evaluate the real authored
  artifact (which may be far larger / different from commentary), not just the chatter.
- Collapsing these two (e.g. feeding `gate_content` into `_determine_status`) would break
  sentinel detection because disk artifacts don't carry the EXIT_RECOMMENDATION/verdict
  sentinels. The inline comments at 617 ("uses NDJSON text for sentinel detection") and 620
  ("uses resolved content — disk file or NDJSON") already document the intent; the hotfix's
  job is to add a stronger guard comment binding INV-010.

### `_determine_status` (executor.py:645-676) — consumes `output_text`

```python
645:    def _determine_status(
646:        self, exit_code: int, output: str, step_id: str
647:    ) -> PrdStepStatus:
648:        """Classify step outcome from exit code and output content.
649:
650:        NFR-PRD.3/F-007: Sentinel detection with anchored regex,
651:        code block exclusion.
652:        """
653:        # Timeout
654:        if exit_code == 124:
655:            return PrdStepStatus.TIMEOUT
656:
657:        # Crash
658:        if exit_code != 0:
659:            return PrdStepStatus.ERROR
660:
661:        # Sentinel detection (F-007)
662:        sentinel = _detect_sentinel(output)
663:        if sentinel == "HALT":
664:            return PrdStepStatus.HALT
665:        if sentinel == "CONTINUE":
666:            return PrdStepStatus.PASS
667:
668:        # QA steps: check for verdict
669:        if "qa" in step_id or "review" in step_id:
670:            if '"verdict": "FAIL"' in output or "verdict: FAIL" in output:
671:                return PrdStepStatus.QA_FAIL
672:            if '"verdict": "PASS"' in output or "verdict: PASS" in output:
673:                return PrdStepStatus.PASS
674:
675:        # No sentinel found -- pass with caveat
676:        return PrdStepStatus.PASS_NO_SIGNAL
```

NOTE the param is named **`output`** here (the caller passes `output_text` positionally at line
618). Sentinel detection via `_detect_sentinel(output)` (662) → HALT/CONTINUE. QA verdict
detection via substring match on `output` (670-673). All of this operates on the NDJSON stream,
confirming the split.

---

## 4. `_evaluate_gate` (executor.py:678-715) — INV-001 verification

```python
678:    def _evaluate_gate(
679:        self,
680:        step_id: str,
681:        gate,
682:        content: str,
683:    ) -> bool:
684:        """Evaluate gate criteria for a step's output."""
685:
686:        # Check min lines
687:        if gate.min_lines > 0:
688:            line_count = len(content.splitlines())
689:            if line_count < gate.min_lines:
690:                self._diagnostics.record_gate_failure(
691:                    step_id,
692:                    f"Insufficient lines: {line_count} < {gate.min_lines}",
693:                    gate.enforcement_tier,
694:                )
695:                self._logger.log_gate_result(
696:                    step_id,
697:                    False,
698:                    f"Min lines: {line_count}/{gate.min_lines}",
699:                )
700:                return False
701:
702:        # Run semantic checks
703:        if gate.semantic_checks:
704:            for check in gate.semantic_checks:
705:                result = check.check_fn(content)
706:                if result is not True:
707:                    msg = result if isinstance(result, str) else check.failure_message
708:                    self._diagnostics.record_gate_failure(
709:                        step_id, msg, gate.enforcement_tier
710:                    )
711:                    self._logger.log_gate_result(step_id, False, msg)
712:                    return False
713:
714:        self._logger.log_gate_result(step_id, True, "All checks passed")
715:        return True
```

**INV-001 CONFIRMED TRUE:** `_evaluate_gate` NEVER reads `required_frontmatter_fields`.
Evidence: `grep -n "required_frontmatter_fields\|frontmatter" executor.py` returns **NO MATCHES**
(zero hits in the entire file). The method only reads two `gate` attributes:
- `gate.min_lines` (687-688) — line-count floor.
- `gate.semantic_checks` (703-705) — list of check objects, each invoked via
  `check.check_fn(content)`.
- (`gate.enforcement_tier` is read only for failure-logging metadata, 693/709 — not a criterion.)

**STRICT criteria actually applied:** STRICT vs STANDARD does NOT change WHAT `_evaluate_gate`
checks (it always applies `min_lines` + `semantic_checks`). The tier only changes the CALLER's
response to failure — at executor.py:625-628 a failed STRICT gate → `PrdStepStatus.HALT`, a
failed non-STRICT gate → `PrdStepStatus.VALIDATION_FAIL`. So "STRICT criteria" = the same
min_lines + semantic_checks, but a hard HALT on failure.

**Cross-file corroboration (gates.py, in scope only as evidence for INV-001):**
`required_frontmatter_fields` IS a field on the `GateCriteria` dataclass and IS populated for a
few steps (e.g. gates.py:331 `["Date", "Scenario", "Tier"]`, gates.py:368 a populated list), but
since `_evaluate_gate` never reads it, **those declared frontmatter fields are currently DEAD
config** — never enforced. This is consistent with INV-001's claim and worth flagging to R3
(gates.py researcher) for cross-validation.

---

## 5. `_persist_step_artifact` (executor.py:1145-1173) — MUST STAY UNCHANGED

```python
1145:    def _persist_step_artifact(self, step_id: str, output_text: str) -> None:
1146:        """Write step output to the expected artifact file.
1147:
1148:        Downstream prompt builders load artifacts by filename from
1149:        task_dir (e.g. ``parsed-request.json``, ``scope-discovery-raw.md``).
1150:        The subprocess writes to stdout (captured as NDJSON); this method
1151:        persists the extracted text so those files exist on disk.
1152:
1153:        For JSON artifacts, strips markdown code fencing if present so
1154:        ``json.loads()`` succeeds downstream.
1155:        """
1156:        artifact_name = _STEP_ARTIFACT_FILES.get(step_id)
1157:        if not artifact_name:
1158:            return
1159:
1160:        content = output_text
1161:        if artifact_name.endswith(".json"):
1162:            content = _strip_json_fencing(content)
1163:
1164:        artifact_path = self._config.task_dir / artifact_name
1165:        try:
1166:            artifact_path.write_text(content, encoding="utf-8")
1167:        except OSError:
1168:            self._logger.log_step_complete(
1169:                step_id,
1170:                "ARTIFACT_WRITE_FAIL",
1171:                duration_seconds=0,
1172:                exit_code=-1,
1173:            )
```

**CONFIRMED writes the CANONICAL name:** `artifact_name = _STEP_ARTIFACT_FILES.get(step_id)`
(1156) and `artifact_path = self._config.task_dir / artifact_name` (1164). The artifact is
written to `task_dir / <canonical filename from the dict>` — e.g. for `research-qa` it writes to
`task_dir / "qa/qa-research-gate-report.md"`. **Resume probes depend on this exact canonical
path**, so this method must stay UNCHANGED. The param here is `output_text` (the caller passes
`gate_content` into it at line 637 — i.e. the resolved disk content, NOT raw NDJSON). JSON
artifacts get `_strip_json_fencing` (1161-1162). Steps absent from the dict are silently skipped
(1157-1158), which is exactly why build-task-file/assembly must NOT be added (would clobber the
authored file).

---

## 6. Required imports CONFIRMED present (executor.py:20-31)

```python
20:from __future__ import annotations
21:
22:import inspect
23:import json
24:import re
25:import signal
26:import time
27:from concurrent.futures import ThreadPoolExecutor, as_completed
28:from dataclasses import dataclass
29:from datetime import datetime, timezone
30:from pathlib import Path
31:from typing import Optional
```

- `import json` — **line 23** (present). ✅ for WHERE-parsing JSON.
- `from pathlib import Path` — **line 30** (present). ✅ for Path operations.
- Also available for free: `import re` (24), `import inspect` (22). No new import needed for
  json/Path. (If the WHERE-parser needs `os`/`glob`, those are NOT currently imported — verify
  before use; `Path.rglob`/`Path.glob` already cover globbing without `glob`.)

`GATE_CRITERIA` is imported from `.gates` at executor.py:46 (`from .gates import GATE_CRITERIA`).

---

## Status: Complete

### Summary of load-bearing findings

1. **Line numbers re-confirmed** — all BUILD_REQUEST estimates were off by ~10-15 lines; use the
   reconciliation table at the top. `_persist_step_artifact` def is at **1145** (not 1156).
2. **`_STEP_ARTIFACT_FILES` (252-263)** — exactly 8 keys, matching the merged-solution mirror.
   Three QA values carry a `qa/` path prefix. build-task-file/assembly intentionally absent.
3. **`_resolve_step_content` (266-365)** — signature `(step_id, task_dir, ndjson_text)`. Three
   `len()>len()` "largest wins" sites (298-299, 329-330, **360-361** primary). Generic path uses
   RECURSIVE `root.rglob(base_name)` over `[task_dir, task_dir.parent]` (the widening to bound).
   Zero-match returns **`ndjson_text`** (365). build-task-file (293-304) + assembly (306-337)
   special-cases must stay intact.
4. **INV-010 split (609-637) CONFIRMED** — `output_text`(NDJSON, 609) → `_determine_status` (618)
   for sentinel/verdict; `gate_content`(disk, 613-615) → `_evaluate_gate` (623) + persist (637).
   Must be preserved + get a guard comment.
5. **INV-001 CONFIRMED TRUE** — `_evaluate_gate` (678-715) reads ONLY `min_lines` +
   `semantic_checks`; `required_frontmatter_fields` has ZERO occurrences in executor.py (grep
   verified). STRICT differs only in caller's HALT-vs-VALIDATION_FAIL response (625-628), not in
   what's checked.
6. **`_persist_step_artifact` (1145-1173)** — writes canonical `task_dir/<dict-name>`; resume
   probes depend on it; MUST stay UNCHANGED.
7. **Imports present** — `import json` (23), `from pathlib import Path` (30). `os`/`glob` are NOT
   imported (use Path globbing).
