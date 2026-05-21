# F-36: Inventory/filtering dead code -- `[INCOMPLETE]` filter, non-recursive glob, `load_synthesis_mapping`

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P2, P5, P7
**Identified by**: E-9, E-11, E-12
**File:line**: `src/superclaude/cli/prd/inventory.py:138-160`; `src/superclaude/cli/prd/filtering.py:74, 309-328`

## Evidence

```python
# inventory.py:145 -- [INCOMPLETE] filter never matches actual prompts
if re.search(r"\[INCOMPLETE\]", content, re.IGNORECASE):
    continue  # prompts use "Status: In Progress", not "[INCOMPLETE]"

# filtering.py:74 -- non-recursive glob
for md_file in sorted(research_dir.glob("*.md")):  # misses subdirectories

# filtering.py:309-328 -- argument ignored entirely
def load_synthesis_mapping(refs_dir: Path) -> list[dict]:
    """Load the synthesis mapping table... Falls back to built-in default..."""
    return list(_DEFAULT_SYNTHESIS_MAPPING)  # refs_dir never read
```

## Trace

- `[INCOMPLETE]` filter: The prompts use `Status: In Progress` and never emit `[INCOMPLETE]`. Mid-flight files pass the filter and look "complete." Conversely, files legitimately containing "incomplete" in prose are silently dropped.
- Non-recursive glob: Both `compile_gaps` and `discover_research_files` use flat `*.md` glob. If agents write to subdirectories of `research/`, files are missed.
- `load_synthesis_mapping`: Signature, docstring, and argument suggest dynamic loading from `synthesis-mapping.md`. Body throws the arg away and always returns the hard-coded default. User edits to `synthesis-mapping.md` have no behavioral effect.

## Reproduction sketch

Edit `<skill_refs_dir>/synthesis-mapping.md` to redefine synthesis routing. Run the pipeline. Synth-04 still receives the same set of research files because `_DEFAULT_SYNTHESIS_MAPPING` is hard-coded.

## Confidence (aggregated)

0.80 -- Agent E confirmed all three sites. The filter and glob are low-severity; the ignored argument is definitive dead code.

## Cross-agent corroboration

- **Agent E** identified all three dead-code surfaces in inventory.py and filtering.py, noting the `[INCOMPLETE]` filter never matches actual prompt output, the glob misses subdirectories, and `load_synthesis_mapping` ignores its parameter entirely.
