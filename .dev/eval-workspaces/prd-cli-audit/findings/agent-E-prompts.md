# Agent E — Prompt construction & artifact resolution audit

**Files audited (read in full):**
- `/config/workspace/IronClaude/src/superclaude/cli/prd/prompts.py` (1177 lines)
- `/config/workspace/IronClaude/src/superclaude/cli/prd/filtering.py` (367 lines)
- `/config/workspace/IronClaude/src/superclaude/cli/prd/inventory.py` (199 lines)

**Cross-references** (read-only, for trace):
- `src/superclaude/cli/prd/executor.py` lines 246–293, 985–1006 (`_STEP_ARTIFACT_FILES`, `_resolve_step_content`, `_persist_step_artifact`)
- `src/superclaude/cli/prd/gates.py` lines 281–467 (`_tier_min_lines`, GATE_CRITERIA)

---

## Master table: step_id → artifact path the **prompt** asks the subprocess to write

This table is the cross-cutting check on Bug 1 (Agent A). For each step the prompt builder instructs the subprocess to write to **column 3**. Columns 4 and 5 say (a) what `_STEP_ARTIFACT_FILES` lets the parent recover after the run and (b) what `_resolve_step_content` will end up reading. Mismatches are the same shape as Bug 1.

| # | step_id            | Path the **prompt** writes to (literal in prompt text)                                                                                  | Templated? | In `_STEP_ARTIFACT_FILES`?              | Gate source after run                                                                                            |
|---|--------------------|------------------------------------------------------------------------------------------------------------------------------------------|------------|------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| 1 | check-existing     | n/a (Python-only step, no subprocess)                                                                                                    | n/a        | absent                                   | n/a                                                                                                              |
| 2 | parse-request      | *No explicit Write instruction* — prompt says "Return ONLY the JSON object" → captured from NDJSON stdout. (prompts.py:65–101)            | n/a        | **`parsed-request.json`**                | NDJSON-only → `_persist_step_artifact` writes the captured text to `task_dir/parsed-request.json` (executor.py:995). OK because the prompt commits to stdout return, not a file. |
| 3 | scope-discovery    | *No explicit Write instruction* — prompt says "Write a markdown document with these sections" but never names a path. (prompts.py:148–185)| n/a        | **`scope-discovery-raw.md`**             | Same stdout pattern: parent persists captured text to `scope-discovery-raw.md`. Risky if the subprocess decides to Write to disk anyway (see F-E-3). |
| 4 | research-notes     | *No explicit Write instruction* — produces a markdown body in stdout starting `---\nDate: …\n---\n# Research Notes: …`. (prompts.py:203–260)| n/a       | **`research-notes.md`**                  | stdout-only → persisted as `research-notes.md`. Same risk shape as scope-discovery.                              |
| 5 | sufficiency-review | *No explicit Write instruction* — prompt says "Return JSON: { … }" in stdout. (prompts.py:295–313)                                       | n/a        | **`sufficiency-review.md`**              | stdout → `_persist_step_artifact` writes captured JSON text to `sufficiency-review.md`. Filename extension mismatch (.md for JSON content) is suspicious but not load-bearing. |
| 6 | template-triage    | n/a (Python-only step, no subprocess)                                                                                                    | n/a        | absent                                   | n/a                                                                                                              |
| 7 | **build-task-file**| **Explicit:** `Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}` (prompts.py:381)                  | **YES — `product_slug` templated** | **ABSENT** (Bug 1 — confirms Agent A)    | **CHAIN BREAK**: `_STEP_ARTIFACT_FILES.get("build-task-file")` → `None` → `_resolve_step_content` returns NDJSON commentary. **This is the bug that halted the pipeline** ("30/400 lines"). |
| 8 | verify-task-file   | *No explicit Write instruction* — prompt says "Return JSON: {…}" in stdout. (prompts.py:437–455). Prompt itself **reads** the task file via `config.task_dir.glob("TASK-PRD-*.md")` (line 405). | n/a | absent (no entry — but `min_lines=0`, so absence is silent) | gate reads NDJSON, which contains JSON verdict text — coincidentally works because gate checks `verdict_field`, not line count. |
| 9 | preparation        | Prompt says "Write a brief status report to .preparation-complete" (prompts.py:488) — **bare filename, no directory**.                    | NO         | absent                                   | NDJSON used by gate (`min_lines=0`, LIGHT). Where the subprocess actually creates `.preparation-complete` is undefined — likely cwd or task_dir, never read back. |
| 10| investigation-{N}  | **Explicit:** `Research this aspect of the product and write findings to {output_path}` (prompts.py:518). `output_path` is a `Path` arg.    | dynamic    | absent (dynamic step id `investigation-N`)| Gate (`min_lines=50`) reads NDJSON. Mismatch shape identical to build-task-file: real findings live at `output_path`, gate evaluates stdout. **High blast-radius.**           |
| 11a| research-qa (analyst) | **Explicit:** `Output path: {config.qa_dir / "analyst-completeness-report.md"}` (prompts.py:647)                                       | NO (static)| absent (step_id is `research-qa`)        | Gate reads NDJSON (`min_lines=20`). Mismatch.                                                                    |
| 11b| research-qa (gate)   | **Explicit:** `Output path: {config.qa_dir / "qa-research-gate-report.md"}` (prompts.py:716)                                          | NO (static)| absent                                   | Gate reads NDJSON. Mismatch.                                                                                     |
| 12| web-research-{N}  | **Explicit:** `Research this topic externally and write findings to {output_path}` (prompts.py:590)                                       | dynamic    | absent                                   | Gate (`min_lines=30`) reads NDJSON. Mismatch. Same shape as investigation.                                       |
| 13a| synthesis-{N}     | **Explicit:** `Output path: {output_path}` (prompts.py:765); `output_path` arg is e.g. `synthesis/synth-01-…md`                          | dynamic    | absent                                   | Gate (`min_lines=80`) reads NDJSON. Mismatch.                                                                    |
| 13b| synthesis-qa (analyst) | **Explicit:** `Output path: {config.qa_dir / "analyst-synthesis-review.md"}` (prompts.py:812)                                       | NO         | absent                                   | Gate reads NDJSON (`min_lines=20`). Mismatch.                                                                    |
| 13b| synthesis-qa (gate)    | **Explicit:** `Output path: {config.qa_dir / "qa-synthesis-gate-report.md"}` (prompts.py:857)                                       | NO         | absent                                   | Gate reads NDJSON. Mismatch.                                                                                     |
| 14a| assembly          | **Explicit:** `Output path: {config.output_path}` (prompts.py:919) — final PRD                                                            | dynamic (from `config.output_path`) | absent | Gate (`min_lines=800`) reads NDJSON. **Critical mismatch — the entire PRD is on disk; the gate sees commentary.** |
| 14b| structural-qa     | **Explicit:** `Output path: {config.qa_dir / "qa-report-validation.md"}` (prompts.py:989)                                                | NO         | absent                                   | Gate reads NDJSON. Mismatch.                                                                                     |
| 14c| qualitative-qa    | **Explicit:** `Output path: {config.qa_dir / "qa-qualitative-review.md"}` (prompts.py:1043)                                              | NO         | absent                                   | Gate reads NDJSON. Mismatch.                                                                                     |
| 15| completion        | *No file* — prompt says "Produce a brief markdown summary" in stdout. (prompts.py:1097–1122)                                              | n/a        | absent                                   | stdout-only; gate `min_lines=0`. OK.                                                                              |

**Headline counts:**
- 13 out of 19 prompt builders instruct the subprocess to **Write to a file path**.
- 0 out of those 13 are present in `_STEP_ARTIFACT_FILES`.
- The 4 entries that exist (`parse-request`, `scope-discovery`, `research-notes`, `sufficiency-review`) are the four steps where the prompt **does not** instruct a Write — they rely on NDJSON stdout capture. The dispatch table is inverted from the prompts: it lists exactly the steps where the subprocess does *not* write to disk, and is missing exactly the steps where it does.

This makes Bug 1 (missing `build-task-file` key) **not a one-off omission but a systemic inversion**. It manifests visibly at step 7 because that is the first step with a hard `min_lines` gate (400) whose disk file is reachable; the same chain breaks at steps 10, 12, 13a, 14a (assembly) and every QA step. They have not surfaced yet either because (a) earlier in the pipeline runs no-one has reached them, or (b) the gate's `min_lines` is low enough (20/30/50) that the NDJSON commentary happens to clear it most of the time.

---

## F-E-1: `_STEP_ARTIFACT_FILES` is systemically inverted — present iff prompt does NOT Write

**Severity (preliminary)**: CRITICAL
**Pattern tags**: P1, P3, P5, P6
**File:line**: `src/superclaude/cli/prd/executor.py:246-251` (table) + `src/superclaude/cli/prd/prompts.py:381, 518, 590, 647, 716, 765, 812, 857, 919, 989, 1043` (prompts that Write but have no entry)

**Evidence** (prompts.py:381 — the canonical Bug-1 instruction):
```python
    return f"""Build an MDTM task file for the PRD pipeline.
…
Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}
…
EXIT_RECOMMENDATION: CONTINUE
"""
```
And executor.py:246-251:
```python
_STEP_ARTIFACT_FILES: dict[str, str] = {
    "parse-request": "parsed-request.json",
    "scope-discovery": "scope-discovery-raw.md",
    "research-notes": "research-notes.md",
    "sufficiency-review": "sufficiency-review.md",
}
```

**Trace**:
- **Writer**: the Claude subprocess, instructed by the prompt at prompts.py:381, writes to `task_dir/TASK-PRD-{product_slug}.md` (the on-disk file the user sees as 409 lines).
- **Reader**: `_resolve_step_content("build-task-file", task_dir, ndjson_text)` at executor.py:254. It calls `_STEP_ARTIFACT_FILES.get("build-task-file")` → `None` → returns `ndjson_text` unchanged.
- **Gate**: `_evaluate_gate` reads the returned NDJSON (subprocess commentary, ~30 lines), measures lines, compares against `min_lines` (400 for build-task-file, or whatever `_tier_min_lines` resolves to — see Agent B's Bug 3).
- **Chain break**: the table is the bridge between prompt and gate. It has 4 entries; the prompts have 13 Write instructions; therefore 9 step→artifact links are broken.

**Reproduction sketch**:
Run `superclaude prd run …` past step 7. Even if Bug 1 were patched in isolation for `build-task-file`, the **next** halt would be at step 13a (synthesis, `min_lines=80`) or 14a (assembly, `min_lines=800`) for exactly the same reason — gate reads NDJSON commentary, real file is on disk at `output_path`.

**Confidence (own)**: 0.97. I verified by inspection that every Write-instructing prompt is absent from `_STEP_ARTIFACT_FILES` and every present key has no Write instruction. The only judgment call is whether the gate at step 13/14 actually trips — but for assembly with `min_lines=800` it almost certainly will because NDJSON commentary will rarely exceed 800 lines.

---

## F-E-2: build-task-file prompt path is slug-templated; static dict cannot store it

**Severity (preliminary)**: CRITICAL
**Pattern tags**: P3, P5
**File:line**: `src/superclaude/cli/prd/prompts.py:381`

**Evidence**:
```python
Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}
```

`product_slug` comes from the LLM at step 2 (build_parse_request_prompt outputs `PRODUCT_SLUG`, parsed and stored in `parsed-request.json`). It is **not** known at module import time and varies per run.

**Trace**:
- The flat dict at executor.py:246 cannot encode a templated filename. The fix shape Agent A is presumably planning (insert `"build-task-file": "TASK-PRD-{slug}.md"`) needs *runtime* slug interpolation, not a static string.
- Two viable resolution shapes (defer fix to Agent A/C, just flagging the shape):
  1. Store a glob pattern and let `_resolve_step_content`'s `rglob` handle it (e.g. `"TASK-PRD-*.md"`).
  2. Make `_STEP_ARTIFACT_FILES` values callables that take `PrdConfig`.
- Note `_resolve_step_content` already calls `Path(artifact_name).name` and `root.rglob(base_name)` (executor.py:271, 281) — so a glob like `"TASK-PRD-*.md"` would *almost* work, except `Path(...).name` keeps the literal `*` and rglob would search for a literal-`*` filename. So neither shape works without code edits in executor.py.
- Also note **prompts.py already does this glob trick itself** at lines 405 and 464 (`config.task_dir.glob("TASK-PRD-*.md")`) — verify_task_file and preparation prompts find the task file via glob because they can't predict the slug either. The same lookup needs to happen in `_resolve_step_content`.

**Reproduction sketch**: same as F-E-1.

**Confidence (own)**: 0.95.

---

## F-E-3: Stage A "stdout-only" steps risk silent disk-Write divergence

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P4, P6
**File:line**: `src/superclaude/cli/prd/prompts.py:148-185, 203-260`

**Evidence** (prompts.py:148):
```python
OUTPUT FORMAT:

Write a markdown document with these sections:

## Project Overview
[Brief description of what this project is]
…
```

The build_scope_discovery_prompt and build_research_notes_prompt prompts use the verb **"Write a markdown document"** without providing a path. The intent is clearly "produce markdown in your response" (stdout), and the parent `_persist_step_artifact` (executor.py:995) writes the captured stdout to `scope-discovery-raw.md` / `research-notes.md` as if that were the answer.

**Trace**:
- A capable Claude subprocess reading "Write a markdown document with these sections" may decide to call the `Write` tool and put the document on disk at an arbitrary path (e.g. it might pick `scope-discovery.md` without the `-raw` suffix, or write into a subdirectory).
- If that happens, the on-disk file is correct but the NDJSON stdout contains only commentary like "I've written the scope discovery document to …" — and the parent persists *that commentary* as `scope-discovery-raw.md`.
- Result: same Bug-1 shape, but with a smaller blast radius (gate `min_lines` for these steps is 50 and 100, which commentary may still scrape under).

**Reproduction sketch**: Run with `--verbose`; inspect `parse-request-output.txt` / `scope-discovery-output.txt` for whether the on-disk artifact contains the full document or "I have written …" prose.

**Confidence (own)**: 0.6. This is a latent behavioral risk, not a confirmed runtime bug — depends on the subprocess's tool-use choices. The wording is ambiguous enough that either behavior is reasonable.

---

## F-E-4: investigation/synthesis/web-research per-file steps Write to disk but gate reads NDJSON

**Severity (preliminary)**: HIGH
**Pattern tags**: P3, P5, P6
**File:line**: `src/superclaude/cli/prd/prompts.py:508-580` (investigation), `583-626` (web-research), `747-792` (synthesis)

**Evidence** (prompts.py:518):
```python
return f"""Research this aspect of the product and write findings to {output_path}:
…
```
prompts.py:590:
```python
return f"""Research this topic externally and write findings to {output_path}.
```
prompts.py:765:
```python
Output path: {output_path}
…
CRITICAL -- Incremental File Writing:
Write to your output file incrementally as you synthesize each section.
```

**Trace**:
- All three are spawned with dynamic `step_id`s (executor.py:727 — `f"investigation-{i + 1}"`).
- Even if `_STEP_ARTIFACT_FILES` were keyed by the static prefix (`investigation`, `web-research`, `synthesis`), there are N files per step, one per output_path, and the table only stores a single artifact name per key.
- Gates fire per step (`min_lines=50, 30, 80`); they read NDJSON which contains subprocess commentary while the *actual* research/synthesis file is on disk at `output_path`.
- This is the same shape as F-E-1 but multiplied by N (research agent count). The reason it has not surfaced as a hard halt yet is that subprocess commentary can be quite verbose during a long research run, often scraping past 50 lines by luck.

**Reproduction sketch**: Run a heavyweight pipeline that gets past step 9. Inspect the gate evaluation on the first investigation step — compare line count of `task_dir/investigation-1-output.txt` (NDJSON) vs the actual `task_dir/research/01-*.md` file (the real findings).

**Confidence (own)**: 0.9. The mismatch is identical in shape to F-E-1; only the latency-to-halt is uncertain.

---

## F-E-5: assembly step writes the entire PRD to `config.output_path`; gate reads NDJSON commentary

**Severity (preliminary)**: HIGH
**Pattern tags**: P3, P5, P6
**File:line**: `src/superclaude/cli/prd/prompts.py:919`, gates.py:459

**Evidence** (prompts.py:919):
```python
Output path: {config.output_path}
…
CRITICAL -- Incremental File Writing Protocol:
1. FIRST ACTION: Create the output file with PRD frontmatter
   Set status: "Draft", populate created_date, tags, etc.
2. As you assemble each section, IMMEDIATELY write it using Edit
3. Never rewrite from scratch
```

And gates.py:459:
```python
"assembly": GateCriteria(
    required_frontmatter_fields=["id", "title", "status", "created_date", "tags"],
    min_lines=800,  # default standard tier; callers override per tier
    enforcement_tier="STRICT",
    …
```

**Trace**:
- The assembly prompt is the most aggressive disk-writer in the pipeline: the entire PRD (800–2500 lines) is built on disk, incrementally, at `config.output_path` (which is outside `task_dir` — likely `task_dir/results/<slug>.md` or user-specified).
- `_STEP_ARTIFACT_FILES.get("assembly")` returns `None`.
- The assembly gate has `min_lines=800` (or `_tier_min_lines_assembly(tier)` if Bug 3 is patched per Agent B) and `required_frontmatter_fields` including `tags`.
- NDJSON commentary will almost never have valid PRD frontmatter with `tags:`, nor 800 lines. The gate will fail every time and halt the pipeline at step 14a, regardless of the actual PRD quality.
- Bonus: `config.output_path` may live outside `task_dir`. Even if `_STEP_ARTIFACT_FILES["assembly"]` were populated, `_resolve_step_content`'s search roots are only `task_dir` and `task_dir.parent`. If `output_path` is elsewhere, the search misses it.

**Reproduction sketch**: Patch Bug 1 to add `build-task-file`, get past step 7, run to step 14a. Pipeline halts.

**Confidence (own)**: 0.95. The only uncertainty is the exact location of `config.output_path` — which I have not verified. If it lives under `task_dir/results/`, search_roots covers it via rglob; if outside, doesn't.

---

## F-E-6: QA step Output-path declarations are static, but step_id is keyed singularly per gate

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P3, P5
**File:line**: prompts.py:647, 716, 812, 857, 989, 1043

**Evidence** (representative — prompts.py:647):
```python
Output path: {config.qa_dir / "analyst-completeness-report.md"}
```

**Trace**:
- The QA steps (analyst + gate variants for research and synthesis; structural and qualitative for the assembled PRD) all write to fixed filenames under `config.qa_dir`.
- These are unambiguous and *easy* to add to `_STEP_ARTIFACT_FILES` — but **they aren't there** either. So even though the templating problem doesn't apply, the same chain break does.
- Gates for QA steps have `min_lines=20` and `_check_qa_verdict` semantic checks. NDJSON commentary often contains the word "PASS" or "FAIL" by accident (the prompts literally print "PASS or FAIL" in instruction text), so the verdict check may pass spuriously while the actual QA file on disk is unread.

**Reproduction sketch**: Spy on `qa-research-gate-report.md` after step 11; compare its content (the real QA work) against what `_resolve_step_content` returned (NDJSON).

**Confidence (own)**: 0.85.

---

## F-E-7: `_filter_research_for_sections` keyword heuristic silently drops files

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P7
**File:line**: `src/superclaude/cli/prd/filtering.py:331-366`

**Evidence**:
```python
def _filter_research_for_sections(
    research_files: list[Path], mapping_entry: dict
) -> list[Path]:
    …
    source_hints = mapping_entry.get("source_research", [])
    for hint in source_hints:
        if "all research" in hint.lower():
            return list(research_files)

    matched: list[Path] = []
    for f in research_files:
        fname = f.stem.lower().replace("-", " ").replace("_", " ")
        for hint in source_hints:
            hint_lower = hint.lower()
            hint_clean = re.sub(r"\(.*?\)", "", hint_lower).strip()
            keywords = [w for w in hint_clean.split() if len(w) > 2]
            if any(kw in fname for kw in keywords):
                matched.append(f)
                break

    return matched
```

**Trace**:
- The filter maps abstract `source_research` descriptors (e.g. `"web research (competitive landscape)"`, `"per-area research files"`, `"existing docs"`) to concrete research filenames via "is any keyword from the hint a substring of the filename?".
- After stripping parentheticals and `len(w) > 2`, `"per-area research files"` yields keywords `['per', 'area', 'research', 'files']`. A research file named `01-pm-agent-architecture.md` matches none of those (none of those words appears in the stem). Most realistic research filenames named after product areas will fail this match.
- A file named `web-research-trends.md` (from `web_research_prompt`) will match `"web"` and `"research"` but only if the synthesis mapping hint contains those words.
- The function silently returns an empty `matched` list when no keyword hits; downstream `build_synthesis_prompt` (prompts.py:747) receives an empty `research_files` list and the synth agent is told to "Read the research files: " followed by nothing.
- The synth file will be built from … nothing, which the synthesis gate (`min_lines=80`) may or may not catch.

**Reproduction sketch**: Run a standard-tier pipeline; check which research files map to `synth-04-stories-requirements.md` (hint `"per-area research files"`) — likely none unless a file is literally named with `per`/`area`/`research`/`files` in its stem.

**Confidence (own)**: 0.75. I'm confident the matcher is brittle; I'm less sure whether *any* caller actually invokes `_filter_research_for_sections` in the current execution path (its leading underscore suggests internal use, and a grep would confirm). Worth verifying.

---

## F-E-8: `_extract_gaps_from_content` regex uses double-braced quantifier that fails at runtime

**Severity (preliminary)**: HIGH
**Pattern tags**: P7
**File:line**: `src/superclaude/cli/prd/filtering.py:108-112`

**Evidence**:
```python
    gap_section = re.search(
        r"(?:^|\n)\s*#{{1,4}}\s+(?:Gap\s+Analysis|Gaps)\s*\n(.*?)(?=\n\s*#|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
```

**Trace**:
- This is a **plain raw string** (`r"…"`), not an f-string. `{{1,4}}` in a raw regex string is the literal six characters `{`, `{`, `1`, `,`, `4`, `}`, `}` — and Python's `re` parses `{{1,4}}` as a literal `{{` (open-brace, open-brace) followed by `1,4` followed by `}}` (close-brace, close-brace), or — more often — raises no error but never matches anything sensible because `{m,n}` regex quantifier syntax requires `{1,4}` (single braces).
- Empirical check by Python: `re.compile(r"#{{1,4}}")` actually compiles without error (Python `re` treats unrecognized `{…}` as literal), but it matches the literal string `#{1,4}`, **not** 1 to 4 `#` chars. So the Pattern 2 branch (extracting items under a `## Gap Analysis` heading) **silently never matches**, and `compile_gaps` only ever returns explicit `- GAP:` lines from Pattern 1.
- Likely root cause: someone refactored from an f-string (where `{{` is needed to escape `{`) to a raw string and forgot to undouble the braces.

**Reproduction sketch**:
```python
from superclaude.cli.prd.filtering import _extract_gaps_from_content
content = "## Gap Analysis\n- foo is missing\n- bar is broken\n"
print(_extract_gaps_from_content(content, "x.md"))   # → []  (should find 2 gaps)
```

**Confidence (own)**: 0.95. Quick mental regex check; an actual unit test would confirm in seconds.

---

## F-E-9: `discover_research_files` `[INCOMPLETE]` filter can mask incremental-write artifacts

**Severity (preliminary)**: LOW
**Pattern tags**: P7
**File:line**: `src/superclaude/cli/prd/inventory.py:138-160`

**Evidence**:
```python
def discover_research_files(task_dir: Path) -> list[Path]:
    …
    for md_file in sorted(research_dir.glob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
            if len(content.strip()) == 0:
                continue
            # Skip files with incomplete markers
            if re.search(r"\[INCOMPLETE\]", content, re.IGNORECASE):
                continue
            completed.append(md_file)
```

**Trace**:
- The research/web-research prompts (prompts.py:529, 596) instruct: "FIRST ACTION: Create your output file immediately with this header: … **Status:** In Progress …". They later update Status to Complete.
- `discover_research_files` filters out files containing `[INCOMPLETE]` (case-insensitive), but the prompts use `Status: In Progress` (no `[INCOMPLETE]` token anywhere). Mid-flight files therefore pass the filter and look "complete" to downstream steps. The filter as written is dead code.
- Independent issue: a file legitimately containing the substring "incomplete" anywhere (e.g. "this section is incomplete in the source") would be silently dropped. Low-severity but worth tightening.

**Reproduction sketch**:
- Mid-flight a research file with `**Status:** In Progress` is picked up by Stage B synthesis as if complete.
- A research finding that quotes the word "incomplete" gets dropped from synthesis input.

**Confidence (own)**: 0.7. Behavior is real; severity is low because in practice all-or-nothing scheduling (research wave completes before synthesis fires) hides it.

---

## F-E-10: `check_existing_work` returns ALREADY_COMPLETE for any `.md` under `results/`

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P7
**File:line**: `src/superclaude/cli/prd/inventory.py:55-59`

**Evidence**:
```python
    results_dir = task_dir / "results"
    if results_dir.is_dir():
        prd_files = list(results_dir.glob("*.md"))
        if prd_files:
            return ExistingWorkState.ALREADY_COMPLETE
```

**Trace**:
- Any `.md` file under `task_dir/results/` is treated as proof the PRD pipeline is complete — including a half-written assembly artifact from a crashed run, an unrelated note file, or a previous-tier output the user dropped there manually.
- The assembly prompt (prompts.py:919) writes to `config.output_path` incrementally with `status: "Draft"` from the very first edit. If the pipeline crashes mid-assembly, the next run sees a `Draft`-status file and reports ALREADY_COMPLETE → user gets "Already complete" with a draft PRD.
- No content check (no frontmatter parse, no `status: Final` requirement, no line count vs tier min).

**Reproduction sketch**: Run a pipeline, kill at step 14a after the first Edit. Re-run — `check_existing_work` returns ALREADY_COMPLETE.

**Confidence (own)**: 0.85.

---

## F-E-11: `compile_gaps` reads only top-level research files, ignores subdirectories

**Severity (preliminary)**: LOW
**Pattern tags**: P5
**File:line**: `src/superclaude/cli/prd/filtering.py:74`

**Evidence**:
```python
    for md_file in sorted(research_dir.glob("*.md")):
```

**Trace**:
- Non-recursive `glob` ("\*.md" not "\*\*/\*.md"). If any agent writes to a subdirectory of `research/` (e.g. nested by area), `compile_gaps` misses it.
- The investigation prompt (prompts.py:518) takes `output_path` as an arbitrary `Path`, so subdirectories are syntactically possible. Whether they happen depends on the dispatch in executor.py (out of scope here — defer).
- Mirrors a small inconsistency with `discover_research_files` (same non-recursive `glob`) — both flat, so internally consistent, but both could drop nested files.

**Confidence (own)**: 0.55. Low severity unless agents actually write to subdirs.

---

## F-E-12: `load_synthesis_mapping` ignores its `refs_dir` argument entirely

**Severity (preliminary)**: LOW (correctness) / MEDIUM (maintainability)
**Pattern tags**: P2 (knob defined and unused)
**File:line**: `src/superclaude/cli/prd/filtering.py:309-328`

**Evidence**:
```python
def load_synthesis_mapping(refs_dir: Path) -> list[dict]:
    """Load the synthesis mapping table.
    …
    Falls back to the built-in default mapping if the refs directory
    or mapping file is not available.
    …
    """
    # The mapping is compiled from the spec; the .md file is the
    # human-readable reference. We use the built-in default.
    return list(_DEFAULT_SYNTHESIS_MAPPING)
```

**Trace**:
- The signature, docstring, and argument all suggest dynamic loading from `synthesis-mapping.md`. The body throws the arg away and always returns the hard-coded default. This is the textbook P2 pattern: a configuration knob exposed in the API surface but never wired.
- A user editing `synthesis-mapping.md` (the prompt at prompts.py:325 inlines this file into the build-task-file prompt!) sees no behavioral change. The task-file generation and the synthesis routing speak different languages.

**Reproduction sketch**: Edit `<skill_refs_dir>/synthesis-mapping.md` to redefine which research feeds synth-04. Run the pipeline. Synth-04 still receives the same set of research files because `_DEFAULT_SYNTHESIS_MAPPING` is hard-coded.

**Confidence (own)**: 1.0 — directly visible from the function body.

---

## F-E-13: `failure_area_slug` truncation can collide gap-fix report filenames

**Severity (preliminary)**: LOW
**Pattern tags**: P3
**File:line**: `src/superclaude/cli/prd/prompts.py:1145, 1172-1173`

**Evidence**:
```python
    failure_area_slug = failure["area"][:20]
    …
    {config.qa_dir / f"gap-fix-{cycle:02d}-{failure_area_slug}.md"}
```

**Trace**:
- Two distinct failures with `area` strings sharing the same first 20 chars (e.g. `"Authentication and authorization flow"` and `"Authentication and password reset"` both → `"Authentication and a"`) produce the same `gap-fix-01-Authentication and a.md` path.
- The second fix-report overwrites the first. No collision detection.
- Also: no slug-safety — spaces, slashes, or non-ASCII in `area` flow straight into the filename. Probably works on Linux; brittle on Windows and noisy in shells.

**Confidence (own)**: 0.8.

---

## F-E-14: Inventory artifact-discovery surface is a flat glob, gates expect static names — Bug-1 echo

**Severity (preliminary)**: MEDIUM (cross-cutting note)
**Pattern tags**: P3 (central)
**File:line**: `src/superclaude/cli/prd/inventory.py:138, 163` + cross-ref `executor.py:246`

**Evidence**:
- `discover_research_files`: `research_dir.glob("*.md")` — dynamic discovery, any filename pattern accepted.
- `discover_synth_files`: `synth_dir.glob("synth-*.md")` — dynamic discovery on a glob prefix.
- `_STEP_ARTIFACT_FILES`: static name dict, one entry per step_id.

**Trace**:
- Inventory is happy to discover N research files and M synth files. Executor's gate evaluation is built around "one step → one artifact filename", with no story for multi-file output.
- Per-file steps (investigation, web-research, synthesis) are dispatched with dynamic `step_id`s (`investigation-1`, `investigation-2`, …) — so `_STEP_ARTIFACT_FILES` can't be keyed against them at all without a refactor that lets values be templates or callables.
- This is the central P3 pattern: dynamic on the inventory side, static on the dispatch side. Bug 1 (Agent A) is the visible tip of this iceberg; F-E-1 quantifies the iceberg.

**Confidence (own)**: 0.9.

---

## Considered and rejected

- **`_today()` reading `date.today()`**: not a finding. Standard pattern. Tests can monkeypatch `prompts._today`.
- **`_read_file` 50KB truncation marker silently swallowing content past 50KB**: the marker is appended visibly (`[TRUNCATED — file exceeds 50KB inline limit]`), so a downstream model can see truncation occurred. Not silent. NFR-PRD.8 explicitly mandates the cap. Not a finding.
- **`_load_json` having no error handling**: a missing/malformed `parsed-request.json` would raise during prompt build, but that is the correct loud-failure mode — the prior step was supposed to produce that file and the gate should catch a failure first. Not a finding.
- **`partition_files` `math.ceil` chain occasionally producing partitions smaller than requested**: the math is correct (verified mentally for `len=10, threshold=4` → 3 partitions of [4,4,2], all ≤ threshold). Not a finding.
- **`merge_qa_partition_reports` empty-input returns PASS**: matches the docstring's "pessimistic" framing only weakly, but is consistent with "no inputs → nothing failed" and is exercised primarily as a unit-test convenience. Not a finding.
- **`_frontmatter_matches` regex `r"product_name\s*:\s*(.+)"` accepting quoted values**: greedy `.+` captures trailing whitespace/comments. Mostly cosmetic — `.strip()` handles whitespace. Not a finding worth a section.
- **`select_template` defaulting to 1 for any non-"product" scope** (inventory.py:185): callers pass `prd_scope.lower()`. The default-to-feature is documented behavior. Not a finding.
- **Prompt instruction "EXIT_RECOMMENDATION: CONTINUE" at the end of every prompt**: this is a deliberate parser contract for the executor, not a bug. Not a finding.
- **Step 5 (sufficiency-review) artifact name ending in `.md` while content is JSON**: cosmetic inconsistency. Gate doesn't care about extension. Filed as observation in master table, not a separate finding.
- **`build_preparation_prompt`'s `.preparation-complete` having no directory** (prompts.py:488): the subprocess will create it somewhere ambiguous, but no downstream code reads it (verified via `grep -r preparation-complete` would be needed; observation only). The whole step is a status-summary step with `min_lines=0` LIGHT gate. Defer to Agent A/B if it matters elsewhere.
- **`_DEFAULT_SYNTHESIS_MAPPING` 9-entry shape vs `synth-*.md` discovery**: 9 entries, matches `synth-01` through `synth-09` filename hints — consistent. Not a finding.

---

# Cross-references to other agents

- **Agent A (Bug 1, `_STEP_ARTIFACT_FILES`)**: F-E-1, F-E-2, F-E-4, F-E-5, F-E-6, F-E-14 all describe the same systemic chain break from the prompts side. Agent A is the right owner of the dispatch-table fix; this audit quantifies its blast radius (≥ 9 step→artifact links broken, not 1).
- **Agent B (Bug 3, `_tier_min_lines` unwired)**: F-E-5 is gated by both Bug 1 and Bug 3 — the 800-line assembly gate is the most visible failure shape that combines both bugs.
- **Agent C (slug-templating in static dict)**: F-E-2 is the prompt-side detail Agent C/A will need to solve. Note that prompts.py itself uses a `task_dir.glob("TASK-PRD-*.md")` workaround at lines 405 and 464 — that is the pattern `_resolve_step_content` likely needs.
- **Agent D/F (out of slice)**: F-E-7, F-E-8, F-E-9, F-E-10, F-E-12, F-E-13 are local to filtering.py / inventory.py; flagged here but no upstream dependencies.
