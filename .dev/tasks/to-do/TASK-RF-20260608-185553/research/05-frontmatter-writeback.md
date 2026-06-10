# Research: Frontmatter Parse + Atomic Write-back
**Status:** Complete
**Date:** 2026-06-08
**Scope:** FR-6 (atomic race-safe frontmatter write-back) + FR-7 (wrapper-result.yaml sidecar) — read/parse/serialize MDTM `reflect_post:` block, write back only that block, preserve body byte-for-byte.
---

## TL;DR / Headline findings

1. **`frontmatter.py` is PARSE-ONLY.** `extract_frontmatter(content) -> dict[str,str] | None` reads *top-level scalar* keys only; it has **no serializer, no body separation, no write-back, and discards nested/indented YAML** (e.g. `deviations: {authorized: N}` mapping values and any nested block). It is **not** sufficient to round-trip the §6 `reflect_post:` block (which contains a nested `deviations` mapping). `src/superclaude/cli/pipeline/frontmatter.py:90-125`.
2. **A yamllint-safe SafeDumper subclass overriding `increase_indent` ALREADY EXISTS and is importable:** `_IndentDumper` in `src/superclaude/cli/recommend/cache.py:37-48`. The KNOWN HINT is **confirmed**. It is module-private (leading `_`) — reusable by import but the wrapper should either import it or copy the 12-line class (see Recommendation).
3. **Atomic same-dir-temp + `os.replace` is the pervasive house pattern** — ~12 call sites. Canonical YAML variant: `cache.py:127-166` (`LookupCache.save`). Canonical mkstemp variant: `audit/checkpoint.py:74-88`.
4. **Compare-before-write (FR-6 race guard) has a direct precedent:** `sprint/rerun_tasks.py` hashes the on-disk tasklist (`_content_sha256_excluding_rerun_block`, `rerun_tasks.py:683-694`) as a mid-flight-edit guard. `spec_patch.py:200` also recomputes `sha256(read_bytes())` before mutating. **No single existing helper does "compare on-disk bytes == bytes-read then os.replace" in one shot** — the wrapper must compose it (precedents exist for each half).
5. **YAML dependency is PyYAML (`pyyaml>=6.0`), NOT ruamel.** `pyproject.toml:38`. No `ruamel` import anywhere in `src/`. So write-back uses `yaml.dump(..., Dumper=_IndentDumper, sort_keys=False)`, not ruamel round-trip.
6. **"Replace ONLY the reflect_post block in-place" precedent:** `rerun_tasks._split_rerun_block` (`rerun_tasks.py:675-680`) does exactly the regex-locate-one-block / splice-the-rest pattern for the SUPERCLAUDE-RERUN block. This is the body-byte-preservation model to copy for `reflect_post:`.

---

## 1. `pipeline/frontmatter.py` — full API (file:line)

Single canonical parser module. Pure Python, no subprocess (`frontmatter.py:43`). Header docstring states it deliberately **replaced two divergent parsers** to fix Contract #6 brittleness (`frontmatter.py:1-44`).

**Only public function:**
```python
def extract_frontmatter(content: str) -> dict[str, str] | None:   # frontmatter.py:90
```
- **Returns** `dict[str, str]` of **top-level** `key -> value`, values stripped of whitespace and matching outer YAML quotes; or `None` if no `---...---` block with at least one top-level key is found (`frontmatter.py:90-125`).
- **Ordering:** insertion order of a plain `dict` (Python 3.7+ ordered), built by iterating `frontmatter_text.splitlines()` (`frontmatter.py:117-124`). NOT a guaranteed YAML-semantic order, just source line order of top-level keys.
- **Nested values are DROPPED.** Explicit by design: "Nested / indented lines (e.g. `  - id: M1`) are intentionally ignored — only top-level keys" (`frontmatter.py:36-39`, enforced at `frontmatter.py:118-122` via `_TOPLEVEL_KEY_RE.match(line)` skipping indented lines). **Consequence for FR-6:** the §6 block has `deviations: { authorized: N, ... }` — a nested mapping. `extract_frontmatter` would return `deviations` only if written inline-flow on one top-level line; a block-style nested mapping's children would be lost. **Do not use `extract_frontmatter` to round-trip `reflect_post`.**

**Internals (not for reuse but informative):**
- `_FRONTMATTER_RE = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*$", re.MULTILINE | re.DOTALL)` — preamble-tolerant, non-greedy first block with a top-level key (`frontmatter.py:57-60`).
- `_TOPLEVEL_KEY_RE = re.compile(r"^([A-Za-z_][\w\-]*)\s*:", re.MULTILINE)` (`frontmatter.py:67`).
- `_strip_yaml_quotes(value)` strips matched outer quotes only (`frontmatter.py:70-87`).
- CRLF/CR normalized to `\n` **before** matching (`frontmatter.py:99-105`). **FR-6 caveat:** this normalization is a *parse-time* transform; for byte-for-byte body preservation the write-back path must operate on the **raw bytes/text actually read**, not the normalized copy `extract_frontmatter` works on internally.

**No serialize / no write function exists in this module.** Confirmed by full read (126 lines total). There is no `dump_frontmatter`, `write_frontmatter`, or body accessor.

**Body separation:** NOT provided. The module returns only the parsed dict; it never returns `(frontmatter, body)`. The wrapper must split the body itself (use the `_FRONTMATTER_RE` span or the `rerun_tasks._split_rerun_block` model — §4).

---

## 2. yamllint-safe SafeDumper (KNOWN HINT — CONFIRMED)

**Exists:** `src/superclaude/cli/recommend/cache.py:37-48`
```python
class _IndentDumper(yaml.SafeDumper):                                  # cache.py:37
    """SafeDumper that indents block sequences under their key (yamllint-conformant)."""
    def increase_indent(self, flow=False, indentless=False):  # noqa: N802  # cache.py:47
        return super().increase_indent(flow, False)
```
Docstring confirms the memory exactly: "PyYAML's default places a block sequence's `-` at the parent key's indent, which the repo yamllint config (`indent-sequences: true`) rejects. Overriding `increase_indent` to never go indentless emits `key:\n  - item`" (`cache.py:38-45`).

- **Only this one** such subclass in the whole `src/` tree (grep `increase_indent|class.*Dumper|SafeDumper` returned a single match). Memory hint **verified true**.
- **Reusable/importable?** Yes mechanically — `from superclaude.cli.recommend.cache import _IndentDumper`. But: (a) it's underscore-private (signals not-API); (b) importing the `recommend.cache` module pulls its module-level surface-hash globs/logging. **Recommendation:** the new `reflect/` package should define its own identical `_IndentDumper` (12 lines, no deps) OR a shared dumper should be promoted to a neutral util. Note for builder: a tiny copy is the lower-coupling choice and matches how `cache.py` itself was authored ("YAML adaptation of `convergence.py`", `cache.py:3`) rather than importing.

**Canonical dump-call invocation** (copy these kwargs — they are load-bearing for §6 field order & yamllint): `cache.py:150-156`
```python
yaml.dump(data, Dumper=_IndentDumper, sort_keys=False,
          default_flow_style=False, allow_unicode=True)
```
`sort_keys=False` is called "non-negotiable — it preserves the authored per-row field order" (`cache.py:12-13`). FR-6 needs the same to keep the §6 field order (verdict, status, run_id, tier_reached, report, contract, reason, deviations, head, reviewed_at).

**FR-6 nuance on `deviations`:** §6 shows `deviations: { authorized: N, necessary: N, drift: N, regression: N }` in **inline flow** style. `default_flow_style=False` forces block style, which would expand it to a nested block mapping. If the spec wants the literal inline-flow shape preserved, the builder must either (a) accept block expansion (still valid YAML, yamllint-clean under `_IndentDumper`), or (b) emit `deviations` as a pre-serialized flow string. **Flag for builder — verify against spec intent; default recommendation: block style, it round-trips and is yamllint-safe.**

---

## 3. Atomic write + same-dir temp + os.replace — precedents

The pattern is house-standard (~12 sites). Best references for the wrapper:

**A. YAML atomic write w/ randomized same-dir temp + finally cleanup** — `cache.py:127-166` (`LookupCache.save`):
- `parent.mkdir(parents=True, exist_ok=True)` (`cache.py:144`)
- `tmp = parent / f".{self.path.name}.tmp.{os.getpid()}.{id(self)}"` — **randomized same-dir** name "bounds the worktree-concurrency last-write-wins window (spec Risk #12)" (`cache.py:145-147`)
- `tmp.write_text(yaml.dump(...), encoding="utf-8")` then `os.replace(tmp, self.path)` (`cache.py:149-159`)
- `finally:` unlink leftover tmp on crash (`cache.py:160-165`)

**B. mkstemp same-dir variant** — `audit/checkpoint.py:74-88`: `tempfile.mkstemp(dir=str(self._path.parent), prefix=".progress_", suffix=".tmp")` → `os.fdopen` write → `os.replace(tmp_path, ...)` → except: unlink+raise.

**C. Minimal `.tmp`-suffix variant (NOT race-isolated)** — `rerun_tasks._atomic_write_text` (`rerun_tasks.py:659-663`) uses `path.with_suffix(path.suffix + ".tmp")` (deterministic name → two concurrent writers collide). **Do not use the deterministic-name form for FR-6** under parallel sessions; prefer the randomized same-dir name from (A) per memory `feedback_parallel_sessions_share_index`.

Other os.replace sites for reference: `install_hooks.py:443-455`, `init_lite.py:222-235`, `roadmap/envelope.py:425-441`, `roadmap/convergence.py:305-317`, `roadmap/remediate_executor.py` (multiple).

---

## 4. Compare-before-write (FR-6 race guard) — precedents (no all-in-one helper)

FR-6 requires: read bytes → ... → **compare on-disk bytes still equal the bytes read** → `os.replace()`; on mismatch write sidecar + exit nonzero. **No existing helper does the full sequence**, but both halves exist:

- **Recompute hash of on-disk bytes before mutating:** `spec_patch.py:200` — `current_hash = hashlib.sha256(spec_file.read_bytes()).hexdigest()` then compares to a saved hash before deciding to write (`spec_patch.py:200-205`). `recommend/dispatch.py:123` — `compute_source_hash(src.read_bytes()) != row.get("source_hash")` is the same validate-then-trust pattern.
- **Mid-flight-edit guard on a tasklist (closest analogue):** `rerun_tasks._content_sha256_excluding_rerun_block` (`rerun_tasks.py:683-694`) hashes the tasklist (minus the engine's own provenance block) to "detect a real *operator* edit while ignoring the engine's own provenance write" (`rerun_tasks.py:684-690`). This is conceptually FR-6's compare guard, applied to MDTM tasklists already.

**Recommended FR-6 composition (builder):**
```
raw = path.read_bytes()                     # capture exact bytes
fm, body = split_frontmatter(raw_text)      # see §5 / rerun_tasks model
new_text = splice reflect_post into fm + body (byte-identical body)
# RACE GUARD:
if path.read_bytes() != raw:                # on-disk changed since read
    write <output>/wrapper-result.yaml sidecar(write_status="frontmatter-stale"); exit nonzero
tmp = parent/f".{path.name}.tmp.{os.getpid()}.{uuid}"   # cache.py model
tmp.write_text(new_text); os.replace(tmp, path)         # finally: unlink tmp
```
Note the read→compare→replace has an unavoidable TOCTOU window; that is acceptable per spec (it says "compare on-disk bytes still equal the bytes read → os.replace") — `os.replace` itself is atomic, the compare just shrinks the lost-write window. This matches the cache.py "bounds the last-write-wins window" framing (`cache.py:145-146`), not "eliminates."

---

## 5. How the project currently writes frontmatter back / splices one block

**No code currently round-trips MDTM YAML frontmatter via a parser.** `extract_frontmatter` is read-only (§1). Frontmatter *mutation* today happens in `sprint/rerun_tasks.py` via **regex-locate-one-block + string splice**, not YAML re-serialization:

- `_RERUN_BLOCK_RE = re.compile(r"<!-- SUPERCLAUDE-RERUN\b.*?-->\n?", re.DOTALL)` (`rerun_tasks.py:655-656`)
- `_split_rerun_block(content) -> (existing_block_or_empty, content_without_block)` (`rerun_tasks.py:675-680`):
  ```python
  match = _RERUN_BLOCK_RE.search(content)
  if match is None: return ("", content)
  return (match.group(0), content[:match.start()] + content[match.end():])
  ```
- Re-assembled as `block + body` and atomic-written (`rerun_tasks.py:831, 871, 916`).

**This is the byte-preservation model FR-6 should follow:** locate the existing `reflect_post:` sub-block (or the whole frontmatter), splice the new serialized `reflect_post:` in place, leave everything else (the entire markdown body and all other frontmatter keys) **as the original characters** — never round-trip the whole frontmatter through `yaml.dump` (which would reorder/reflow other keys and break byte-for-byte). i.e. serialize **only** the `reflect_post:` value with `_IndentDumper`, then string-splice it; do not re-dump sibling keys.

`sprint/preflight.py` and `sprint/executor.py` also reference `reflect_post`/frontmatter (grep hit) but for **reading** the gate state, not writing it (they consume the PENDING/verdict signal). [Unverified — not read line-by-line; relevant to R06/R08, out of this track's scope.]

---

## 6. ruamel vs PyYAML

- `pyproject.toml:38` → `"pyyaml>=6.0"`. **PyYAML is the dependency.**
- `grep -rn "import ruamel\|from ruamel" src/` → **zero matches.** ruamel is NOT available.
- Therefore: no comment-preserving round-trip dumper exists; use PyYAML `yaml.dump` + `_IndentDumper` for the `reflect_post` value only, and **string-splice** to preserve everything else (§5). Do not assume ruamel round-trip semantics.

---

## 7. Direct answers to track questions

| Question | Answer | Cite |
|---|---|---|
| frontmatter.py parse fn / return type | `extract_frontmatter -> dict[str,str] \| None`, top-level scalars only, source-line order | `frontmatter.py:90-125` |
| serialize fn in frontmatter.py? | **None** | full read (126 lines) |
| body byte-preservation supported there? | **No** — no body accessor/split | `frontmatter.py` (none) |
| yamllint-safe Dumper exists? | Yes, `_IndentDumper` | `cache.py:37-48` |
| importable/reusable? | Yes, but private; recommend local copy | `cache.py:37` |
| atomic same-dir temp + os.replace helper? | Yes, multiple; canonical YAML = `LookupCache.save` | `cache.py:127-166`; `audit/checkpoint.py:74-88` |
| compare-before-write precedent? | Halves exist (hash-of-disk + mid-flight guard); no all-in-one | `spec_patch.py:200`; `rerun_tasks.py:683-694` |
| current frontmatter write-back path? | regex-splice-one-block (rerun), not YAML round-trip | `rerun_tasks.py:655-680, 831` |
| ruamel or pyyaml? | **PyYAML** (`pyyaml>=6.0`), no ruamel | `pyproject.toml:38` |

---

## Summary / Recommendations for the builder

- **Do NOT reuse `extract_frontmatter` for write-back** — it drops nested `deviations` and offers no serialize/body split. Use it only if you need to *read* an existing scalar key. For FR-6, parse the frontmatter region yourself (regex on the `---...---` span, modeled on `_FRONTMATTER_RE` and `rerun_tasks._split_rerun_block`) and operate on the **raw text read from disk** (not the CRLF-normalized copy) to preserve the body byte-for-byte.
- **Serialize ONLY the `reflect_post:` value** with PyYAML `yaml.dump(value, Dumper=_IndentDumper, sort_keys=False, default_flow_style=False, allow_unicode=True)` and **string-splice** it into the existing frontmatter — never re-dump the whole frontmatter (would reflow sibling keys and lose byte-for-byte).
- **Dumper:** copy the 12-line `_IndentDumper` (`cache.py:37-48`) into the new `reflect/` package rather than importing the private symbol from `recommend.cache` (lower coupling; matches house authoring style). KNOWN HINT confirmed.
- **Atomic write:** copy `LookupCache.save`'s randomized same-dir-temp + `os.replace` + `finally`-unlink (`cache.py:144-165`). Avoid the deterministic `.tmp`-suffix form (`rerun_tasks._atomic_write_text`) under parallel sessions.
- **Race guard (FR-6):** compose read-bytes → splice → `read_bytes() == original?` → `os.replace`; on mismatch, write `<output>/wrapper-result.yaml` sidecar (FR-7) with a `write_status` like `frontmatter-stale` and exit nonzero. Precedents: `spec_patch.py:200`, `rerun_tasks.py:683-694`. TOCTOU window is bounded, not eliminated — consistent with spec wording and `cache.py:145-146`.
- **YAML lib:** PyYAML only; no ruamel; no comment-preserving round-trip available — string-splice is the byte-preservation mechanism.
- **Open verify-against-spec item:** §6 shows `deviations` in inline-flow `{ }`; `default_flow_style=False` expands to block. Block is yamllint-clean and round-trips; confirm the spec doesn't require the literal inline shape.
