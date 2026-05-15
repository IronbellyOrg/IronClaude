# Solution S1 — Sanitize File-Path Extraction

> Refactored after adversarial review. Scope narrowed, extension filter
> dropped in favor of a structural-token reject list; impact estimate
> downgraded. S1 is now positioned as a **contributing** fix, not a
> standalone resolution of the convergence failure.

## Target root cause

`extract_file_paths_from_tables` in
`src/superclaude/cli/roadmap/spec_parser.py` (~line 407) walks every
table cell with the regex

```python
path_like = re.compile(r'(?:src/|tests/|docs/|scripts/|\./)\S+')
```

and consumes any token containing that infix. Because the table column
that holds "Prior Art / References" frequently embeds full URLs such as
`https://docs.rollbar.com/docs/grouping-algorithm`, the regex captures
the URL **path segment** as if it were a repo-relative file path. The
same regex also captures brace-expansion shell glob prose
(`src/superclaude/{skills,agents}`) and Python-style traceback citations
(`src/x.py:88\``) because none of the noise tokens are filtered.

Verified phantoms reproduced against the live code (see
`agent-reports/S1-debate.md`, Attack-1):

| Source cell contents (verbatim) | Path captured by `path_like` | Real? |
|---|---|---|
| `https://docs.rollbar.com/docs/grouping-algorithm` | `docs/grouping-algorithm` | NO — URL fragment |
| `https://docs.rollbar.com/docs/error-grouping-best-practices` | `docs/error-grouping-best-practices` | NO — URL fragment |
| `sync src/superclaude/{skills,agents} to .claude/` | `src/superclaude/{skills,agents}` | NO — brace prose |
| `` `src/x.py:88` is the line `` | `src/x.py:88\`` | NO — backtick + line ref |
| `src/superclaude/examples/prd_template.md` | `src/superclaude/examples/prd_template.md` | YES — real file |
| `src/superclaude/examples/tdd_template.md` | `src/superclaude/examples/tdd_template.md` | YES — real file |

## Noise contribution to the 10 active HIGHs

Adversarial classification of the deviation registry
(see debate transcript):

| Stable ID | Description | Layer | Verdict |
|---|---|---|---|
| `dd52050c…` | `docs/error-grouping-best-practices` | data_models | NOISE — extractor |
| `9fcc342b…` | `docs/grouping-algorithm` | data_models | NOISE — extractor |
| `97683f80…` | `src/superclaude/{skills,agents}` | data_models | NOISE — extractor |
| `b0e3eb55…` | `src/x.py:88\`` | data_models | NOISE — extractor |
| `c7efc393…` | `prd_template.md` | data_models | LEGIT — roadmap gap |
| `524dada1…` | `tdd_template.md` | data_models | LEGIT — roadmap gap |
| `2be5b51c…` | NFR `encryption` | nfrs | OUT OF SCOPE for S1 |
| `6c16b1b9…` | NFR `hash` | nfrs | OUT OF SCOPE for S1 |
| `3f534425…` | NFR threshold `<1%` | nfrs | OUT OF SCOPE for S1 |
| `a6452d2e…` | NFR threshold `<2%` | nfrs | OUT OF SCOPE for S1 |

**4 of 10 HIGHs (40%)** are removable by S1, **not 5+** as originally
claimed. Two `data_models` HIGHs (`prd_template.md`, `tdd_template.md`)
are genuine roadmap omissions and must remain. Four `nfrs` HIGHs are
beyond this solution's purview.

## Proposal

Add a `_looks_like_file_path()` post-filter applied to every candidate
emitted by `extract_file_paths_from_tables` (the lower-confidence path
— `extract_file_paths` already gates on backticks). Reject rules use
**structural tokens**, not extensions, to avoid dropping legitimate
extensionless paths (`scripts/build`, `docs/CHANGELOG`, `LICENSE`).

### Rejection criteria

A candidate is rejected if **any** of the following holds:

1. **Brace-expansion / glob syntax**: contains `{`, `}`, `*`, `?`.
2. **Embedded backtick**: contains `` ` `` (artifact of overlapping
   backtick boundaries in code-citation prose).
3. **Line/column suffix**: matches `:\d+` after the path body
   (e.g. `src/x.py:88`).
4. **Whitespace**: contains any whitespace character.
5. **URL embedment**: the candidate's starting position in the original
   cell is **preceded by** `://` (within ~12 chars) OR by an
   alphanumeric character (URLs are `https://docs.rollbar.com/docs/...`,
   so the `d` of `docs/` is preceded by `m/` in the URL host, not
   whitespace, `(`, `\`` or `|`). This is the **load-bearing** rule
   that removes the Rollbar phantoms.

### Trailing-punctuation strip (retain existing behavior)

After acceptance, strip trailing `.,;:)`` (already present in current
code) — but do this **before** the line-suffix check so that
`docs/grouping-algorithm.` is normalized to `docs/grouping-algorithm`
*and then evaluated*, and so trailing periods at end of sentences are
not preserved into the manifest.

### Patch sketch

```python
# spec_parser.py, replacing the body of extract_file_paths_from_tables
_URL_PRECEDING_RE = re.compile(r'(?:[A-Za-z0-9]|://)$')

def _looks_like_file_path(candidate: str, cell: str, start: int) -> bool:
    if any(c in candidate for c in '{}*?`') or any(c.isspace() for c in candidate):
        return False
    if re.search(r':\d+', candidate):
        return False
    # URL-embedded check: scan up to 12 chars left of the match
    left = cell[max(0, start - 12):start]
    if _URL_PRECEDING_RE.search(left):
        return False
    return True

def extract_file_paths_from_tables(tables):
    paths: set[str] = set()
    path_like = re.compile(r'(?:src/|tests/|docs/|scripts/|\./)\S+')
    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                for m in path_like.finditer(cell):
                    raw = m.group(0).strip('`').rstrip('.,;:)')
                    if _looks_like_file_path(raw, cell, m.start()):
                        paths.add(raw)
    return sorted(paths)
```

`extract_file_paths` (backtick-anchored, line ~397) keeps its existing
regex but also runs the new filter so that the `src/x.py:88\``
backtick variant is rejected by rule 3.

## Risks / downsides (post-refactor)

- **URL-precedence heuristic is approximate.** A spec author who writes
  the prose `…using docs/foo.md (per the spec)` will have `docs/foo.md`
  accepted (preceded by space). A spec author who writes a URL with the
  trailing slash and then a real path token jammed against it could
  still slip through, but no such pattern appears in the current
  corpus.
- **Does not address NFR phantoms** (4 of 10 HIGHs). Pair with S3
  (NFR-allowlist) or S5 (semantic NFR matcher) for a complete fix.
- **Does not address `prd_template.md` / `tdd_template.md`.** Those
  are LEGIT defects in the **roadmap** (template files are referenced
  in the spec but absent from the roadmap manifest). The remediation
  is a roadmap edit, not a parser change. S1 will *correctly* surface
  these two as HIGHs after the noise is removed — which is the
  intended behavior.
- **Test fixture updates.** `tests/roadmap/test_spec_parser.py:248-260`
  exercises both extractors; add at least the 6 phantom-token cases
  above plus 3 positive cases (`scripts/build`, `docs/CHANGELOG`,
  `src/superclaude/cli/main.py`) to guard against regression.

## Expected impact on the failing case

- Removes **4 of 10** active HIGHs (`dd52050c`, `9fcc342b`, `97683f80`,
  `b0e3eb55`) at Run 1 of the next convergence cycle.
- Leaves **6 HIGHs**: 2 LEGIT data_model gaps + 4 NFR findings.
- **Will NOT alone reach 0 HIGHs.** Convergence requires S1 + a
  roadmap edit (adds template-file rows) + an NFR fix (S3-style).
- **Does** reduce the patch-diff pressure: with fewer phantoms in the
  registry, the auto-patcher's per-finding diff budget is no longer
  consumed by impossible-to-patch noise, which is what tripped the
  30% diff threshold in Runs 2-3.

## Estimated effort

- Code: ~30 LOC in `spec_parser.py` (one helper + filter wiring).
- Tests: 9 new cases in `tests/roadmap/test_spec_parser.py` (6 negative
  + 3 positive).
- Time: 45 min including test authoring and `make verify-sync` pass.

## Files touched

- `src/superclaude/cli/roadmap/spec_parser.py`
- `tests/roadmap/test_spec_parser.py`
