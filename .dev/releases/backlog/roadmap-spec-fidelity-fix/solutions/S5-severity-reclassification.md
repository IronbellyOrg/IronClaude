# Solution S5 — Context-Aware Severity for NFR Soft Findings

**Status:** refactored after adversarial review. Original "blanket
reclassification + co-occurrence on heading_path" mechanism was
falsified by code evidence (see `agent-reports/S5-debate.md`).

## Target root cause

`check_nfrs` (in `src/superclaude/cli/roadmap/structural_checkers.py:518-655`)
emits HIGH for two NFR mismatch types whenever a keyword from the spec's
NFR-tagged sections fails to appear anywhere in the roadmap text:

- `nfrs.security_missing` — emitted for every word in a fixed keyword list
  (`encryption`, `hash`, `auth`, `tls`, …) that the spec mentions in an
  NFR section but the roadmap omits.
- `nfrs.threshold_contradicted` (no-match arm) — emitted for every numeric
  threshold (`<1%`, `<2%`, …) in the spec NFR section that the roadmap
  does not echo verbatim.

The 4 ACTIVE HIGH findings flagged in `deviation-registry.json`
(`2be5b51c…`, `6c16b1b9…`, `3f534425…`, `a6452d2e…`) are all generated this
way. The checker has no notion of "did the spec mark this primitive as a
requirement, or did it merely mention the word in prose?" Every regex hit
becomes a HIGH, so convergence cannot drop below the keyword-hit count.

## What the original proposal got wrong

1. **Co-occurrence on `heading_path` is structurally impossible** as
   currently scoped. `_section_text`
   (`structural_checkers.py:159-161`) joins the content of every
   NFR-tagged `SpecSection` into one string before any regex scan, so the
   match has no carrier for its originating `heading_path`. The
   `SpecSection.heading_path` field exists
   (`src/superclaude/cli/roadmap/spec_parser.py:81`), but it is dropped
   on the floor before the keyword loop.

2. **Hard-coded `SEVERITY_RECLASS` dict in `models.py`** is a global ratchet.
   A real spec that says "encryption-at-rest is P0" gets the same treatment
   as a spec that mentions `auth` once in a sentence about pytest fixtures.
   This is unacceptable for security-sensitive domains.

## Refactored proposal

Three coordinated changes, all in
`src/superclaude/cli/roadmap/structural_checkers.py`.

### Change 1 — Per-section iteration in `check_nfrs`

Replace the current pattern

```python
spec_nfr_text = _section_text(spec_sections)
# regex over the joined blob
```

with per-section iteration that preserves `heading_path` on every match:

```python
for section in spec_sections:
    for m in security_re.finditer(section.content):
        term = m.group(1).lower()
        if term in already_seen:
            continue
        already_seen.add(term)
        if term not in roadmap_full_text:
            severity = _classify_nfr_severity(
                dimension="nfrs",
                mismatch_type="security_missing",
                heading_path=section.heading_path,
                heading=section.heading,
            )
            findings.append(_make_finding_with_severity(..., severity=severity))
```

Apply the same shape to the threshold no-match arm
(`structural_checkers.py:561-570`).

### Change 2 — `_classify_nfr_severity` helper

New helper (~25 LOC). Heuristic:

```python
_STRONG_NFR_TOKENS = (
    "security", "critical", "must", "shall", "required",
    "p0", "nfr-", "compliance", "encryption", "audit",
)

def _classify_nfr_severity(
    dimension: str,
    mismatch_type: str,
    heading_path: str,
    heading: str,
) -> str:
    """Return HIGH if the originating section signals a hard requirement,
    MEDIUM if the keyword appeared in incidental prose.

    Only applies to the two soft NFR types; all other findings continue to
    use `SEVERITY_RULES` directly via `get_severity`.
    """
    if mismatch_type not in ("security_missing", "threshold_contradicted"):
        return get_severity(dimension, mismatch_type)
    haystack = f"{heading_path}/{heading}".lower()
    if any(tok in haystack for tok in _STRONG_NFR_TOKENS):
        return "HIGH"
    return "MEDIUM"
```

`SEVERITY_RULES` itself stays untouched — the baseline definition is still
HIGH, so tests and audits that read the rules table see strict defaults.
Demotion only happens at emission time when the section context is
available.

### Change 3 — Optional YAML allowlist

Read `<output_dir>/roadmap/fidelity-allowlist.yaml` once per check run
(absent file ⇒ empty allowlist). Schema:

```yaml
allowlist:
  - dimension: nfrs
    mismatch_type: security_missing
    location_match: "spec:nfr:security:hash"
    justification: "hash is mentioned only in pytest fixture docs, not a NFR"
  - dimension: nfrs
    mismatch_type: threshold_contradicted
    location_match: "spec:nfr:threshold:<1%"
    justification: "threshold deferred to v3.1 per release plan"
```

Allowlisted findings:

- Severity → `LOW`.
- `deviation_class` → `"PRE_APPROVED"` (already a valid enum value in
  `src/superclaude/cli/roadmap/models.py:18`).
- Still appear in the report under a "Pre-Approved Deviations" section,
  with the justification rendered.

This gives a human-driven escape hatch without the checker silently lying
and without baking spec-specific judgments into source code.

## Risks / downsides

- **Heuristic is fuzzy.** A spec that uses unusual headings (e.g. just
  `## NFRs`) and mentions `encryption` in prose will get MEDIUM instead
  of HIGH. Mitigation: the YAML allowlist (Change 3) is the explicit
  per-release safety valve; if the heuristic is wrong, the human says so
  in YAML.
- **MEDIUM is still rendered** (gate is HIGH-only, per
  `gates.py:193`), so demoted findings are not suppressed. The user sees
  them in the report under "Soft Deviations" / "Pre-Approved
  Deviations".
- **Per-section iteration changes finding determinism.** Must ensure stable
  ordering by sorting on `(heading_path, term)` before emission so
  `stable_id` allocation stays deterministic across runs.
- **The strong-token list is itself a heuristic** that can be gamed by
  unusual heading wording. The YAML allowlist is the relief valve.

## Expected impact on the failing case

- The 4 NFR-soft HIGHs in `deviation-registry.json` are emitted from
  NFR-tagged sections; whether they demote depends on those sections'
  heading_paths. If `task-builder-merge` puts them under a heading like
  `## Non-Functional Requirements` (no strong token), they demote to
  MEDIUM. If the heading is `## Security NFRs`, they stay HIGH and the
  roadmap genuinely needs to address them.
- Combined with **S1** (sanitize bad file_missing entry `src/x.py:88\``)
  and **S6** (skip unfixable findings), HIGH count for this report
  could drop from 10 to ≤ 5 (the 5 legitimate `data_models.file_missing`
  findings), which is then a fixable-by-editing-the-roadmap problem
  rather than a checker pathology.

## Estimated effort

- Code:
  - `structural_checkers.py`: ~30 LOC (per-section iteration in
    `check_nfrs`) + ~25 LOC (`_classify_nfr_severity`) + ~30 LOC (YAML
    allowlist loader).
  - `models.py`: no change to `SEVERITY_RULES`; possibly an
    `AllowlistEntry` dataclass.
- Tests: update existing tests that assert HIGH for these cases;
  add tests for (a) strong-token heading → HIGH preserved,
  (b) weak heading → MEDIUM demotion, (c) allowlist match → LOW +
  PRE_APPROVED, (d) deterministic emission order.
- Time: ~1.5 h (corrected from original 1 h estimate, which omitted the
  per-section refactor cost).

## Files touched

- `src/superclaude/cli/roadmap/structural_checkers.py` — primary change
  in `check_nfrs` plus new `_classify_nfr_severity` and allowlist loader.
- `tests/cli/roadmap/test_structural_checkers.py` — new and revised cases.
- (optional) `src/superclaude/cli/roadmap/models.py` —
  `AllowlistEntry` dataclass if allowlist is implemented in this
  iteration.

## Out of scope (rejected from original S5)

- Demoting `data_models.field_missing` for "generic" field names
  (`id`, `timestamp`, …). The original proposal bundled this in; it is a
  separate, lower-confidence change that needs its own evidence pass and
  should not ride along here.
- Adding `SEVERITY_RECLASS` to `models.py`. Replaced by the
  context-aware helper in `structural_checkers.py`.
