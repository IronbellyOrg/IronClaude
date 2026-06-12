<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (Solution 2 — Prompt-side path pinning) -->
<!-- Merge date: 2026-06-06 -->
<!-- Convergence: 0.86 | Status: success | Unresolved conflicts: 0 (2 items deferred by design) -->

# Merged Solution: PRD-Pipeline Document-Step Gate-Failure Hotfix

<!-- Source: Base (original, modified) — scoped to merged decision -->

## Status

Unified hotfix for the confirmed `superclaude prd run` defect (REPORT.md, confidence 0.95): document-producing steps fail their line-count gates because `_resolve_step_content` (executor.py:266-365) rglobs the exact canonical filename under `task_dir`/`task_dir.parent`, misses the agent's real document (wrong name **and** wrong location → `.dev/specs/`), and falls back to ~24 lines of NDJSON commentary. Compounding defect: agents write outputs into the writable `WHERE` dir and later steps re-ingest them as source (contamination loop).

This merged solution is a **layered defense**: a primary at-source fix (prompt path pinning), a defense-in-depth backstop (hardened recovery), and two explicitly-deferred follow-ups (cwd isolation, result-event capture) that the adversarial debate + invariant probe showed to be hazardous as part of a hotfix.

## Summary

| Layer | Mechanism | Source | Fixes | Risk |
|-------|-----------|--------|-------|------|
| **1. Primary (at source)** | Pin canonical absolute output path in document prompts | Solution 2 | Capture + contamination | Low |
| **2. Backstop (consumer)** | Hardened `_resolve_step_content` (pattern map + bounded WHERE roots + deterministic tiebreak) | Solution 1 | Capture (recovery for non-compliance) | Medium |
| **3. Guard** | Truncation detection + preserve NDJSON↔disk split | Solution 3 + probe | Silent-incompleteness / sentinel integrity | Low |
| **Deferred A** | cwd isolation + repo-root read injection | Solution 3 | Contamination (structural) | High — out of hotfix scope |
| **Deferred B** | result-event capture behind `capture_mode` flag | Solution 3 | Capture (reliable channel) | High — unverified, out of hotfix scope |

---

## Layer 1 — Primary Fix: Prompt-Side Path Pinning

<!-- Source: Base (original) — Solution 2 §1-2 -->

### 1a. Shared helper `_artifact_path_for_step`

Add to `prompts.py` (~line 53). A read-only mirror of `_STEP_ARTIFACT_FILES` (which lives in `executor.py` and cannot be imported without a circular import). Cross-reference comments in both files; a unit test asserts the two dicts stay identical.

```python
def _artifact_path_for_step(config: PrdConfig, step_id: str) -> Path | None:
    """Canonical artifact path for a step, or None if not applicable.

    Read-only mirror of _STEP_ARTIFACT_FILES in executor.py so prompt-side
    pinning and executor-side recovery agree on one source of truth.
    Guarded by test_prompt_executor_mapping_sync.
    """
    mapping = {
        "parse-request": "parsed-request.json",
        "scope-discovery": "scope-discovery-raw.md",
        "research-notes": "research-notes.md",
        "sufficiency-review": "sufficiency-review.md",
        "research-qa": "qa/qa-research-gate-report.md",
        "synthesis-qa": "qa/qa-synthesis-gate-report.md",
        "structural-qa": "qa/qa-report-validation.md",
        "qualitative-qa": "qa/qa-qualitative-review.md",
    }
    name = mapping.get(step_id)
    return None if name is None else config.task_dir / name
```

### 1b. Pin the output path in the four un-pinned document builders

For `build_scope_discovery_prompt`, `build_research_notes_prompt`, `build_sufficiency_review_prompt`, and `build_preparation_prompt`, inject before the `OUTPUT FORMAT` section:

```
CRITICAL -- Output Location:
Write the document to EXACTLY this path:
{config.task_dir / "<canonical-name>"}

Do NOT write it to any other directory or filename. The pipeline depends
on finding it at this exact location. Do NOT write into any source or
spec directory listed in your scope.
```

This matches the established, already-working idiom used by `build_task_file_prompt` (prompts.py:439) and ~12 other builders that pin `Output path:` and **do not** exhibit this bug. Because `task_dir` is a dedicated workspace outside the `WHERE` source dirs, this prevents `.dev/specs/` contamination at the source.

<!-- Source: Base (original, modified) — DROPPED frontmatter mandate per INV-001 -->
> **Dropped (INV-001)**: an earlier draft added a prompt edit *mandating* the `[Date, Scenario, Tier]` frontmatter. This is removed: the research-notes prompt **already** emits that frontmatter (prompts.py:224-228), and the PRD `_evaluate_gate` (executor.py:678-715) **never reads** `required_frontmatter_fields` — it is a dead constraint in the PRD pipeline. The load-bearing STRICT criteria are `min_lines=100` + the two semantic-section checks (`_check_research_notes_sections`, `_check_suggested_phases_detail`).

---

## Layer 2 — Backstop: Hardened `_resolve_step_content`

<!-- Source: Variant 1 (Solution 1) §1-4 — merged per Change #2,#3,#4 -->

Defense-in-depth for the residual agent-non-compliance risk (X-003): if the agent ignores the pinned path, the executor still recovers the real document. Keep `_STEP_ARTIFACT_FILES` and the `build-task-file`/`assembly` special cases untouched.

### 2a. Per-step pattern map (executor.py ~252)

```python
_STEP_ARTIFACT_PATTERNS: dict[str, list[str]] = {
    "scope-discovery": ["scope-discovery*.md"],   # agent may drop the -raw suffix
    "research-notes":  ["research-notes*.md"],
    "sufficiency-review": [],                       # stable; exact match
}
# Empty/missing entry → fall back to exact-name behavior.
```

### 2b. Bounded WHERE search roots + containment (executor.py ~339, INV-005)

```python
search_roots: list[Path] = [task_dir]
if task_dir.parent.exists():
    search_roots.append(task_dir.parent)

parsed_path = task_dir / "parsed-request.json"
if parsed_path.exists():
    try:
        parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        parsed = {}
    repo_root = task_dir.parent if task_dir.parent.exists() else task_dir
    for where in parsed.get("WHERE") or []:
        where_path = (repo_root / where)
        # realpath containment (INV-005): reject traversal AND symlink escapes
        try:
            real = where_path.resolve(strict=True)
            real.relative_to(repo_root.resolve())
        except (ValueError, OSError):
            continue
        if where_path.is_symlink():        # reject symlinked roots outright
            continue
        if real.is_dir() and real not in search_roots:
            search_roots.append(real)
```

> **INV-005**: WHERE-broadening reverses a hard-won narrowing (see the anti-widening comment at executor.py:290-292 guarding against stale matches from prior failed runs in sibling dirs). The `realpath` containment + symlink rejection + the freshness tiebreak (2d) keep the widening safe.

### 2c. Pattern-aware search (executor.py ~351)

```python
patterns = _STEP_ARTIFACT_PATTERNS.get(step_id) or [Path(artifact_name).name]
candidates: list[tuple[Path, str]] = []
for root in search_roots:
    if not root.exists():
        continue
    for pattern in patterns:
        for match in root.rglob(pattern):
            if "-output.txt" in match.name or (
                {"node_modules", ".git", "__pycache__"} & set(match.parts)
            ):
                continue
            try:
                content = match.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if content.strip():
                candidates.append((match, content))

best_content = _pick_best_candidate(candidates, preferred_root=task_dir)
# Zero-match (INV-006a/INV-009): best_content == "" → caller falls back to
# ndjson_text exactly as today (the only non-regressing default).
```

### 2d. Deterministic tiebreak `_pick_best_candidate` (Solution 1 §4, INV-006)

<!-- Source: Variant 1 §4, modified — freshness raised above content length per INV-006 -->

```python
def _pick_best_candidate(
    candidates: list[tuple[Path, str]], *, preferred_root: Path
) -> str:
    """Stable multi-match tiebreak.

    Priority (INV-006 — freshness MUST outrank raw size, else a stale longer
    file from a prior failed run silently wins over the current output):
      1. Inside preferred_root (task_dir) over external dirs.
      2. Most recently modified (mtime).
      3. Longest content.
      4. Most specific path (fewest parts).
    """
    if not candidates:
        return ""

    def _key(item: tuple[Path, str]) -> tuple[int, float, int, int]:
        path, content = item
        try:
            in_pref = 1 if path.resolve().is_relative_to(preferred_root.resolve()) else 0
        except ValueError:
            in_pref = 0
        return (in_pref, path.stat().st_mtime, len(content), -len(path.parts))

    return max(candidates, key=_key)[1]
```

> **INV-006**: this replaces the current `len(content) > len(best_content)` "largest wins" logic (executor.py:360). Freshness (mtime) is raised above content length so a stale prior-run artifact cannot outscore the current run on size alone.

---

## Layer 3 — Guards

<!-- Source: Variant 3 (Solution 3) + invariant probe — merged per Change #5,#6 -->

### 3a. Truncation-detection check (gates.py, Solution 3 / U-005)

```python
def _check_no_truncation_marker(content: str) -> bool | str:
    if "[TRUNCATED" in content or content.rstrip().endswith("..."):
        return "Content appears truncated — model output limit may have been reached"
    return True
```

Cheap, harmless guard; catches silently-incomplete documents.

### 3b. Preserve the `output_text` ↔ `gate_content` split (INV-010)

<!-- Source: invariant probe — preserves an existing-correct invariant -->

`_determine_status` (executor.py:645-676) detects the `EXIT_RECOMMENDATION`/verdict sentinels from the **NDJSON** `output_text` (executor.py:609,618); the gate evaluates the **disk** `gate_content` (executor.py:613). These are independent inputs and MUST stay independent. Add a guarding comment/assertion so a future refactor cannot collapse them — doing so would silently strip sentinel detection of its input.

---

## Deferred Follow-Ups (explicitly out of hotfix scope)

<!-- Source: Variant 3 (Solution 3), deferred per debate + invariant probe -->

### Deferred A — Working-directory isolation (Solution 3, U-004)

`cwd=task_dir` + `CLAUDE_WORK_DIR` is the only *structural* contamination prevention and remains the architecturally-correct end state. **Deferred** because **INV-011 (HIGH)**: task_dir is a `.dev/tasks/` leaf; setting cwd there breaks scope-discovery/investigation codebase reads ("Read actual files", prompts.py:192) → degraded scope-discovery → thin research-notes → *causes* the STRICT gate to fail. Prerequisite before adoption: inject an explicit absolute repo-root for input reads and add `task_dir.mkdir(parents=True, exist_ok=True)` before `Popen(cwd=...)` (INV-004). Layer 1's absolute output-path pinning already delivers the contamination benefit without this risk (INV-003).

### Deferred B — Result-event capture (Solution 3, behind `capture_mode` flag)

Two-pass `_extract_text_from_stream_json` preferring the CLI `result` event. **Deferred** because **INV-008**: no `result`-event handling exists in source today (grep-confirmed by two independent debate agents); the contract is unverified across CLI versions/platforms; blast radius spans all 15 steps including `parse-request` (must stay valid JSON) and the 800-line `assembly` PRD (token-truncation risk). Adopt only after: (1) verifying the CLI emits a usable full `result` event; (2) confirming sentinels survive in it (INV-010); (3) `capture_mode = "result" | "legacy"` flag defaulting to `legacy`; (4) full 15-step test matrix.

---

## Why This Approach

The adversarial debate (3 independent advocates) reached **unanimous** consensus — including Solution 3's own advocate — that the hotfix is **Solution 2 + Solution 1**, with Solution 3 deferred. This merged solution implements exactly that, then the invariant probe hardened it further: it dropped a redundant frontmatter edit (INV-001), demoted cwd-isolation out of the hotfix (INV-011), fixed the multi-match tiebreak to prefer freshness over size (INV-006), bounded the WHERE-search widening (INV-005), and scoped the sufficiency claim honestly (INV-002).

The result fixes both reported defects (capture + contamination) at the source with a recovery backstop, while keeping the genuinely valuable-but-risky architectural improvements (structural cwd isolation, reliable result-event capture) as well-scoped follow-ups gated on verification rather than shipped blind.

## Sufficiency Note (INV-002)

This fix guarantees the gate **evaluates the agent's real document** instead of NDJSON commentary. It does **not** author content: if the agent genuinely produces a thin research-notes (<100 lines or missing a required section), the STRICT gate *correctly* HALTs. Reproduction evidence (REPORT: a real 197-line doc) shows content was not the problem in the observed failure — the failure was purely capture/location. Content-completeness is correctly the existing semantic checks' concern, not the capture fix's.

## Backward Compatibility

- No public-API changes. `_resolve_step_content` signature and return type unchanged.
- `_STEP_ARTIFACT_FILES`, `_persist_step_artifact` canonical-name writes (resume probes), and the `build-task-file`/`assembly` special cases all untouched (INV-005 persist-half confirmed).
- Steps without a `_STEP_ARTIFACT_PATTERNS` entry keep exact-name behavior.
- Deferred items B's flag defaults to legacy → zero behavior change until explicitly enabled.

## Test Plan (hotfix scope)

1. `test_prompts.py`: `test_artifact_path_for_step_*` (mapped/unmapped), `test_prompt_executor_mapping_sync`, `test_<step>_prompt_contains_pinned_path` for the 4 builders.
2. `test_resolve_step_content.py`: variant-name recovery; bounded-WHERE inclusion; **freshness tiebreak prefers current over stale-longer** (INV-006); symlink/traversal WHERE rejection (INV-005); zero-match → NDJSON fallback (INV-006a).
3. `test_gates.py`: truncation-marker check; research-notes semantic checks pass on recovered real content / fail on thin content (INV-002 scoping).
4. `test_executor.py`: gate receives resolved disk content; `_determine_status` sentinel still detected from NDJSON after gate content moves to disk (INV-010); `_persist_step_artifact` still writes canonical name.
5. `test_e2e.py`: pipeline completes without HALT when agent writes a variant filename; no `.dev/specs` contamination when prompts pinned.

Per IronClaude CLAUDE.md: implement in `src/superclaude/cli/prd/`, then `make sync-dev && make verify-sync`; verify with `uv run pytest tests/cli/prd/`.

## Effort Estimate

| Layer | Effort |
|-------|--------|
| Layer 1 (pinning + helper + tests) | ~3h (Solution 2 base) |
| Layer 2 (hardened recovery + tiebreak + bounded WHERE + tests) | ~4-5h (Solution 1) |
| Layer 3 (truncation check + split guard) | ~1h |
| **Hotfix total** | **~8-9h** |
| Deferred A (cwd + repo-root injection) | follow-up, ~4h |
| Deferred B (result-event + flag + 15-step matrix) | follow-up, ~20h |
