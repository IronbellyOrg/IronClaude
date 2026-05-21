# F-13: `_extract_gaps_from_content` double-braced regex in raw string never matches

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P7
**Identified by**: E-8
**File:line**: `src/superclaude/cli/prd/filtering.py:108-112`

## Evidence

```python
gap_section = re.search(
    r"(?:^|\n)\s*#{{1,4}}\s+(?:Gap\s+Analysis|Gaps)\s*\n(.*?)(?=\n\s*#|\Z)",
    content,
    re.DOTALL | re.IGNORECASE,
)
```

## Trace

- This is a plain raw string (`r"..."`), not an f-string. `{{1,4}}` in a raw regex string is interpreted by Python's `re` as the literal characters `{`, `{`, `1`, `,`, `4`, `}`, `}` -- it does NOT compile as the `{1,4}` quantifier (which matches 1 to 4 of the preceding character).
- Python's `re` treats unrecognized `{...}` as literal, so `#{{1,4}}` matches the literal string `#{1,4}`, NOT 1 to 4 `#` characters.
- The pattern therefore **silently never matches** any heading like `## Gap Analysis` or `### Gaps`.
- `compile_gaps` only ever returns explicit `- GAP:` lines from Pattern 1 (direct line matching). The entire heading-based extraction path is dead.
- Likely root cause: refactored from an f-string (where `{{` escapes to literal `{`) to a raw string without undoubling the braces.

## Reproduction sketch

```python
from superclaude.cli.prd.filtering import _extract_gaps_from_content
content = "## Gap Analysis\n- foo is missing\n- bar is broken\n"
print(_extract_gaps_from_content(content, "x.md"))   # -> [] (should find 2 gaps)
```

## Confidence (aggregated)

0.95 -- Agent E verified the regex behavior. The double-brace-in-raw-string is a classic Python regex mistake.

## Cross-agent corroboration

- **Agent E** identified the regex error and traced the consequence: the heading-based gap extraction path is entirely dead, meaning `compile_gaps` only returns explicit `- GAP:` lines and misses any gaps listed under a `## Gap Analysis` heading.
