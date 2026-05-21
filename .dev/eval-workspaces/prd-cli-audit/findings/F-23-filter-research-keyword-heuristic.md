# F-23: `_filter_research_for_sections` keyword heuristic silently drops files

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P7
**Identified by**: E-7
**File:line**: `src/superclaude/cli/prd/filtering.py:331-366`

## Evidence

```python
def _filter_research_for_sections(
    research_files: list[Path], mapping_entry: dict
) -> list[Path]:
    ...
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

## Trace

- The filter maps abstract `source_research` descriptors (e.g. `"per-area research files"`) to concrete filenames via "is any keyword from the hint a substring of the filename?"
- After stripping parentheticals and `len(w) > 2`, `"per-area research files"` yields keywords `['per', 'area', 'research', 'files']`. A file named `01-pm-agent-architecture.md` matches none of those.
- The function silently returns empty `matched` list when no keyword hits; downstream `build_synthesis_prompt` receives empty `research_files` and the synth agent is told to "Read the research files: " followed by nothing.
- The synth file is built from nothing, which the synthesis gate (`min_lines=80`) may or may not catch.

## Reproduction sketch

Run a standard-tier pipeline; check which research files map to `synth-04-stories-requirements.md` (hint `"per-area research files"`) -- likely none unless a file is literally named with `per`/`area`/`research`/`files` in its stem.

## Confidence (aggregated)

0.75 -- Agent E confirmed the matcher is brittle; uncertainty is whether the current execution path actually invokes this function.

## Cross-agent corroboration

- **Agent E** traced the keyword-to-filename mapping logic and identified the silent empty-list fallback, noting that most realistic research filenames named after product areas will fail the match.
