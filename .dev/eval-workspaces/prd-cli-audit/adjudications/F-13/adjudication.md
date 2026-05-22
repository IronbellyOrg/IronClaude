# F-13 Adjudication — `_extract_gaps_from_content` double-braced regex in raw string never matches

**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-13-double-braced-regex-raw-string.md`
**File:line under review**: `src/superclaude/cli/prd/filtering.py:108-112`
**Stage 2 preliminary severity**: HIGH
**Adjudication mode**: /sc:adversarial Mode B (analyzer / refactorer / architect → converge)

---

## Re-verification (read-only)

### 1. Regex source (`src/superclaude/cli/prd/filtering.py:108-112`)

```python
gap_section = re.search(
    r"(?:^|\n)\s*#{{1,4}}\s+(?:Gap\s+Analysis|Gaps)\s*\n(.*?)(?=\n\s*#|\Z)",
    content,
    re.DOTALL | re.IGNORECASE,
)
```

The string is a plain raw string (`r"..."`), not an f-string. In Python's
`re` engine, `{{` is **not** an escape — the engine simply sees `{`, `{`,
`1`, `,`, `4`, `}`, `}`. When `re` encounters `{...}` whose contents are
not a valid `{m}` / `{m,n}` quantifier, it treats the brace as a literal.
So `#{{1,4}}` matches the literal seven-character string `#{1,4}` (one
`#` followed by `{1,4}`), **not** "one to four `#` characters".

### 2. Empirical confirmation

```text
Pattern repr: '(?:^|\\n)\\s*#{{1,4}}\\s+(?:Gap\\s+Analysis|Gaps)\\s*\\n(.*?)(?=\\n\\s*#|\\Z)'
Match against "## Gap Analysis\n- foo is missing\n- bar is broken\n": None
Match against "#{1,4} Gap Analysis\n- literal match\n":            None  (fails on heading regex tail anyway)
Fixed pattern  (single braces)  against "## Gap Analysis\n...":     <re.Match object; span=(0, 49), ...>
```

The buggy pattern returns `None` for the realistic heading. The corrected
pattern (single braces) matches as intended. Finding is reproduced
exactly.

### 3. `compile_gaps` downstream slice

`compile_gaps` (`filtering.py:56`) calls `_extract_gaps_from_content`
(`filtering.py:90`), which runs Pattern 1 (`^- GAP:` lines, lines 95-105)
and Pattern 2 (heading-section, lines 108-123). Pattern 2's outer
`re.search` is the broken one; when it returns `None`, the `if
gap_section:` branch at line 113 is skipped and the entire
heading-extraction path is dead. Only Pattern 1 contributes to the
returned list. Finding's trace at finding.md:23 is accurate.

### 4. Git provenance

`git log -S '#{{1,4}}' src/superclaude/cli/prd/filtering.py` returns a
single commit: `09e2ccc` ("feat: modularized the prd skill and port it
to the cli", 2026-04-13). The defect was present at the initial port of
the PRD skill into the CLI. Consistent with the finding's "refactored
from an f-string without un-doubling the braces" hypothesis — the spec
form in `.dev/releases/complete/v3.67-prd-skill-portify/.../portify-spec.md:1147`
documents `compile_gaps` as part of the port surface.

---

## Persona 1 — Analyzer (reproducibility)

**Question**: What inputs *should* Pattern 2 match, and what is the
user-visible symptom that it silently never matches?

**Pattern 2's intended job (`filtering.py:107-123`, docstring at
`filtering.py:60-66`)**: extract bullet entries that appear under a
markdown heading whose text is "Gap Analysis" or "Gaps" at heading
levels `#` through `####`. Example inputs Pattern 2 should match:

- `## Gap Analysis\n- foo missing\n- bar broken\n`
- `### Gaps\n* Missing observability metrics\n`
- `#### gap analysis\n- inconsistent error codes\n` (case-insensitive)

**Pattern 2's actual job (with `#{{1,4}}` literal)**: would only match
content where the literal seven characters `#{1,4}` appear in the
heading line, e.g. `#{1,4} Gap Analysis\n...`. No human author writes
markdown that way; even the test fixture in
`tests/cli/prd/test_filtering.py:85-111` uses ordinary `## Gap Analysis`
style content for Pattern 1 cases — Pattern 2 has **no test coverage**.

**User-visible symptom**: silent under-extraction. `compile_gaps` returns
gaps from `- GAP: ...` lines (Pattern 1) but drops every gap listed as a
bullet under a `## Gap Analysis` heading. Because `compile_gaps` returns
a list (not an error), nothing downstream knows the result is partial.
The PRD pipeline would assert "0 gaps in research/foo.md" when in fact
the research file lists 6 under `## Gap Analysis`. Failure mode is
data-loss-without-warning — the worst class for an extraction
pipeline.

**Reproducibility verdict**: HIGH. One-line repro in a REPL
(`finding.md:28-32`). The bug is deterministic and platform-independent
because it lives in regex grammar, not runtime state.

---

## Persona 2 — Refactorer (blast radius)

**Question**: Are there other `{N,M}` patterns in raw strings (`r"..."`
without `f`) that share the same defect? Where does the doubled-brace
convention legitimately apply, and where is it a bug?

**Sweep** — `grep -rn '{{[0-9]' src/superclaude/ --include="*.py"`:

| File:line | String prefix | Verdict |
|---|---|---|
| `src/superclaude/cli/prd/filtering.py:109` | `r"..."` (raw, **no f**) | **BUG** — this finding |
| `src/superclaude/compression.py:674` | `rf"..."` | Correct (f-string `{{` → literal `{`) |
| `src/superclaude/compression.py:709` | `rf"..."` | Correct |
| `src/superclaude/compression.py:712` | `rf"..."` | Correct |
| `src/superclaude/compression.py:840` | `rf"..."` | Correct |
| `src/superclaude/compression.py:889` | `rf"..."` | Correct |
| `src/superclaude/compression.py:1009` | `rf"..."` | Correct |
| `src/superclaude/cli/prd/gates.py:92` | `rf"..."` | Correct |
| `src/superclaude/cli/prd/gates.py:119` | `rf"..."` | Correct |
| `src/superclaude/cli/prd/gates.py:229` | `rf"..."` | Correct |
| `src/superclaude/cli/sprint/checkpoints.py:349` | `rf"..."` | Correct |
| `src/superclaude/cli/sprint/executor.py:1917` | `rf"..."` | Correct |
| `src/superclaude/cli/eval/artifact_layout.py:227` | `f"..."` (not regex) | N/A (error message) |

**Conclusion**: F-13 is the **only** plain-raw-string occurrence in the
package. Every other doubled brace lives in an `rf"..."` (raw f-string)
where `{{` is the *required* escape for a literal `{` to survive
f-string interpolation. This sharpens the finding's root-cause
hypothesis to near-certainty: the line at `filtering.py:109` was
authored as `rf"..."` and later demoted to `r"..."` (because no
interpolation was needed) without un-doubling the braces. The git
history confirms the defect was present at first commit, so the
"demotion" likely happened during the port itself, not later.

**Blast radius**:

- **In-tree code paths**: `_extract_gaps_from_content` is called only by
  `compile_gaps` (`filtering.py:80`). `compile_gaps` itself has **zero
  production callers** — `grep -rn "compile_gaps\b" src/` returns one
  hit, its own definition. The executor (`src/superclaude/cli/prd/executor.py:37-39`)
  imports only `load_synthesis_mapping` from `filtering`. The CLI does
  not yet invoke gap compilation in any pipeline.
- **Test surface**: `tests/cli/prd/test_filtering.py:85-115` exercises
  `compile_gaps` with explicit `- GAP:` markers only. The tests pass
  *because* Pattern 1 still works; the dead Pattern 2 is never
  triggered. The test is structurally incomplete, not actively
  failing.
- **Specification surface**: the function is part of the documented PRD
  CLI port surface
  (`.dev/releases/complete/v3.67-prd-skill-portify/.../portify-spec.md:1147`
  and `portify-release-spec.md:369`), so the wiring is expected to land
  later. When it does, the bug becomes user-facing.

**No collateral fixes required** beyond F-13 itself.

---

## Persona 3 — Architect (severity calibration)

**Question**: Stage 2 marked this HIGH on the assumption that a silently
broken extraction path corrupts downstream consumers. Does the actual
downstream consumer tolerate partial results, and is the wiring live?

**Architectural facts**:

1. **The function is dead code in the production pipeline today.**
   `compile_gaps` has no callers in `src/`. The PRD executor imports
   only `load_synthesis_mapping` from `filtering` (`executor.py:37-39`).
   So the broken pattern *cannot* under-extract gaps in any user-facing
   run as of this commit.
2. **It is documented as a required pipeline step.** The portify spec
   describes `compile_gaps()` running "after Step 11" to "merge gaps
   from all research files into a single file"
   (`.dev/releases/complete/v3.67-prd-skill-portify/portify-workdir/prd/portify-analysis.md:382`).
   So this is a latent defect on a feature that is staged for wiring,
   not a permanent dead branch.
3. **The downstream consumer (when wired) will be strict.** The
   gap-filling sub-pipeline (`executor.py:648, 672, 878` —
   `build_gap_filling_prompt`, "Spawn gap-fillers and re-QA") treats the
   gap list as the authoritative input. A silently under-populated list
   means QA passes prematurely, gap-fillers are not spawned for real
   gaps, and the PRD ships with missing sections. There is no schema or
   count assertion that would surface the under-extraction.
4. **The pattern *also* exists in the spec contract.** Per the PRD
   filtering docstring (`filtering.py:60-66`), "Lines under a
   `## Gap Analysis` or `## Gaps` heading" is one of the three
   advertised extraction modes. Shipping `compile_gaps` with mode 3
   broken would violate the contract its own docstring publishes.

**Severity calibration**:

- **If we score severity by present-day blast radius**: LOW — no
  production caller, no failing test, no user-visible symptom today.
- **If we score severity by the function's contract and the imminent
  wiring**: HIGH — silent data loss on a staged pipeline step that the
  downstream consumer cannot detect.

Audit findings should be scored by *correctness of the code as
published*, not by whether a caller happens to exist this week. A
one-line regex bug that silently truncates extraction results inside a
function the spec promises will be wired is HIGH. Discoverability is
also HIGH: it would only surface after the wiring lands and a research
file uses `## Gap Analysis` instead of `- GAP:` lines — at which point
the failure looks like "QA mysteriously didn't catch obvious gaps", not
"regex bug in filtering.py".

**Final architect verdict**: HIGH, with the modifier that
**immediate exploitability is LOW** (dead code today). The fix is a
two-character edit (`{{` → `{`, `}}` → `}`) plus a regression test that
exercises Pattern 2.

---

## Convergence

**Verdict**: **CONFIRMED** — the regex at `filtering.py:109` is
silently broken; Pattern 2 of `_extract_gaps_from_content` is
unreachable in practice.

**Convergence score**: **0.97** (analyzer 0.98, refactorer 0.97,
architect 0.95 — three-persona agreement on the defect; minor
disagreement only on present-day vs. contract-based severity, resolved
in favor of contract-based).

**Final severity**: **HIGH** (confirmed). Stage 2 preliminary stands.
The function is dead in today's executor, but it is part of the
published port surface and its downstream consumer
(`build_gap_filling_prompt`) cannot detect silent under-extraction.
Audit severity = correctness of published code + downstream tolerance,
not present-day callgraph reachability.

**Fix difficulty**: **TRIVIAL** (1-2 lines).

- Change the pattern at `filtering.py:109` from
  `r"(?:^|\n)\s*#{{1,4}}\s+(?:Gap\s+Analysis|Gaps)\s*\n(.*?)(?=\n\s*#|\Z)"`
  to
  `r"(?:^|\n)\s*#{1,4}\s+(?:Gap\s+Analysis|Gaps)\s*\n(.*?)(?=\n\s*#|\Z)"`.
- Add a regression test in `tests/cli/prd/test_filtering.py` (alongside
  `TestCompileGaps`) that writes a research file with
  `## Gap Analysis\n- foo\n- bar\n` and asserts both items appear in
  the returned list. This pins Pattern 2 behavior so the bug cannot
  re-regress on a future refactor back to `rf"..."`.

**Synthesis**:

F-13 is a textbook "leftover f-string escape" defect — a doubled
brace `{{...}}` that was meaningful inside an `rf"..."` but became
inert (and pattern-breaking) when the string was demoted to `r"..."`.
The defect was introduced at the initial port commit (`09e2ccc`,
2026-04-13) and survives because:

1. The function has no production caller yet, so the bug never fires.
2. The existing test (`test_compile_gaps`,
   `tests/cli/prd/test_filtering.py:85-111`) only exercises Pattern 1,
   so the dead Pattern 2 path looks healthy at green-bar.
3. The codebase has many *correct* `rf"..."` patterns with doubled
   braces (compression.py, gates.py, sprint/*.py), making the one
   buggy `r"..."` visually identical to its valid siblings during code
   review.

The refactorer sweep confirmed F-13 is **the sole occurrence** of this
defect class in `src/superclaude/`. The architect's calibration retains
HIGH severity because the function ships as part of the documented PRD
port surface and the downstream gap-filler pipeline is strict (no
count assertion, no warning on empty extraction). Fix is a two-character
edit plus one regression test; no broader refactor is warranted.

**Recommended fix track**: bundle with other PRD-CLI filtering touch-ups
as a small isolated PR; gate on a new `test_compile_gaps_heading_extraction`
test that fails on the current code and passes after the brace fix.
