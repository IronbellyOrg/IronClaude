# F-39: Gate check regexes overly permissive -- self-containment, section matching, phases, parallel keywords

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P2, P3
**Identified by**: B-5, B-6, B-7, B-9, B-10
**File:line**: `src/superclaude/cli/prd/gates.py:83-212` (multiple check functions)

## Evidence

```python
# B-5: self-containment check misses [X] and * bullets
re.finditer(r"^\s*-\s+\[[ x]\]\s+(.+)$", content, re.MULTILINE)  # only lowercase x

# B-6: section matching with leading .* accepts any prefix
rf"^\s*#{{1,4}}\s+.*{re.escape(section)}"  # "How EXISTING_FILES are tracked" matches EXISTING_FILES

# B-7: parsed-request markdown regex requires only :\S
rf"(?:^|\n)\s*\*{{0,2}}{field_name}\*{{0,2}}\s*:\s*\S"  # "GOAL: -" passes

# B-9: phase count requires only 2 headings containing "Phase \d"
re.findall(r"(?:^|\n)\s*#{1,4}\s+.*Phase\s+\d", content, re.IGNORECASE)  # "Phase 1 Recap" counts

# B-10: parallel keyword substring matches inside prose
if any(kw in section_text for kw in parallel_keywords):  # "Avoid parallelizing" matches "parallel"
```

## Trace

Five gate check functions use overly permissive patterns that accept content the spec intends to reject. Individually LOW severity because they are quality gates, not halt-the-pipeline gates, and the heavyweight failure was caused by F-01, not by regex permissiveness. Collectively they represent a pattern of recall-tuned checks that trivially false-positive.

## Reproduction sketch

A task file with `- [X] As mentioned in Phase 1, ...` passes the self-containment gate. A heading `## How EXISTING_FILES, PATTERNS_AND_CONVENTIONS, ... fit together` passes the research-notes section gate.

## Confidence (aggregated)

0.80 -- Agent B verified all five regex behaviors. Severity is low because these are quality-check gates, not halt-the-pipeline gates.

## Cross-agent corroboration

- **Agent B** systematically reviewed all gate check functions and identified five permissive patterns that accept content the spec intends to reject, noting they are individually minor but collectively represent a recall-over-precision tuning.
