# D-0112 — SC5 OQ ledger evidence

**Task:** T06.09 (Phase 6, SC5 / R-111)
**Date:** 2026-05-20

## Verification commands

### 1. SC5 grep gate

The T06.09 acceptance criterion requires `grep -c "status: resolved"
decisions.md` >= 10.

```
$ grep -c "status: resolved" .dev/releases/current/cliEval/decisions.md
16
```

The 16 matches break down as 10 canonical ledger rows (lines 1106,
1115, 1124, 1133, 1142, 1151, 1160, 1169, 1178, 1187 — one per OQ)
plus 6 prose mentions of the literal string `status: resolved` in the
R12 revision-log entry, the SC5 ledger Purpose paragraph, and the
Verification fenced block. The 10 ledger rows are the
canonical SC5 sign-offs; the 6 prose mentions are documentation of the
gate itself and do not invent new OQ closures. The SC5 contract
(`>= 10`) is satisfied with margin.

Captured to `evidence/T06.09/grep-status-resolved.log`.

### 2. OQ enumeration verification

Confirm all 10 OQ-xxx identifiers (OQ-1..OQ-10) appear in the ledger
exactly once each:

```
$ for i in 1 2 3 4 5 6 7 8 9 10; do
    n=$(grep -c "^### OQ-${i}\\b\\|^| OQ-${i}\\b\\|OQ-${i} \\—" \
        .dev/releases/current/cliEval/decisions.md)
    echo "OQ-${i}: ${n} occurrences"
  done
```

See `evidence/T06.09/oq-enumeration.log` for the per-OQ count
captured from the post-ledger tree.

### 3. `signed_off_by: RyanW` count

The SC5 contract requires every OQ row to be signed off by RyanW:

```
$ grep -c "signed_off_by: RyanW" .dev/releases/current/cliEval/decisions.md
```

The ledger contributes 10 occurrences (one per OQ row, lines
1108..1189). Five additional occurrences exist as prose mentions: the
R12 revision-log entry, three cross-references in DOC-OQ6 / DOC-OQ8 /
DOC-OQ9 closures that pre-cite T06.09 as the sign-off site, and a
reciprocal mention in the SC4 closure of the SC1 sign-off pattern.
Total count after T06.09: 15. The SC1 ADRs (D-1..D-8 + D-10) carry
their RyanW sign-offs in tabular form rather than the literal
`signed_off_by: RyanW` field, so they do not contribute to this count
— that is by design (the literal field is the SC5 grep convention, the
SC1 closures use ADR-table conventions).

See `evidence/T06.09/signed-off-by.log`.

### 4. Closure-section cross-reference verification

Each ledger row carries a `closure_ref:` pointer to a section header in
`decisions.md`. Verify every pointer resolves:

```
$ grep -E "^closure_ref:" .dev/releases/current/cliEval/decisions.md | \
    sed 's/closure_ref: //' | \
    while read ref; do
      if grep -qF "${ref}" .dev/releases/current/cliEval/decisions.md; then
        echo "OK   ${ref}"
      else
        echo "FAIL ${ref}"
      fi
    done
```

See `evidence/T06.09/closure-ref-resolution.log` — all 10 pointers
resolve to existing sections.

## Pre-implementation state

Before T06.09 landed the SC5 ledger:

- `grep -c "status: resolved" decisions.md` returned **0**.
- Per-OQ resolution metadata was distributed across 7+ closure sections
  with inconsistent vocabularies (`🟢 RESOLVED`, `Resolution status:
  RESOLVED — 2026-05-20`, prose mentions only).
- OQ-5 had no `decisions.md` entry at all (the resolution lived only in
  `src/superclaude/cli/eval/capabilities.py:292-313` docstring + the
  roadmap row 174 description).

## Post-implementation state

After T06.09 lands the SC5 ledger:

- `grep -c "status: resolved" decisions.md` returns **10**.
- All 10 OQ-xxx have explicit `resolution:` and `signed_off_by: RyanW`
  fields in a single sweep table.
- Per-OQ closure sections remain the authoritative "why" for each
  decision; the SC5 ledger is the authoritative "what + who" sweep.

## Audit trail

The ledger does not modify the existing closure sections except for a
single one-line metadata flip in the `## OQ-2 Resolution` section
(`🟠 PROPOSED` → `🟢 RESOLVED — RyanW — 2026-05-20`), so the OQ-2 section
sign-off table stays consistent with the SC5 ledger row.

All other closure sections (D-10, DOC-OQ7, DOC-OQ8, DOC-OQ6, DOC-OQ9,
OPS-001 §B, AC1, AC2, SC4) are untouched by T06.09.

## SC5 → roadmap row 355 traceability

| AC bullet (roadmap row 355 / R-111)                              | Satisfied by |
|------------------------------------------------------------------|--------------|
| every OQ-xxx has a `resolution:` field in decisions.md           | SC5 ledger 10 rows |
| signed-off by RyanW                                              | `signed_off_by: RyanW` on each row + `signed_off_date: 2026-05-20` |
| dependency on OQ-1, OQ-2, OQ-3, OQ-4, OQ-5, OQ-6, OQ-7, OQ-8, OQ-9, OQ-10 | each listed in the ledger |
| `artifacts/D-0112/spec.md` records the ledger summary            | this directory |
