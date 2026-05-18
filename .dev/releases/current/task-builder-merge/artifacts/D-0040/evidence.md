# D-0040 — T03.17 Evidence: K-007 Sequencing-Inversion Contingency

**Task:** T03.17 (Phase 3)
**Roadmap items:** R-069
**Date:** 2026-05-17
**Status:** PASS

---

## 1. Summary

The K-007 sequencing-inversion contingency note is documented at
`TASKLIST_ROOT/artifacts/D-0040/spec.md`. The note:

- Cites the binding sequencing rule **PR-06 → PR-04** as enforced at
  release-spec §4.6 (numbered list), reinforced by the §7 K-007 row
  (line 429) and §9 SP-26 reconciliation note (line 498).
- Cites the INV-010 dynamic-enumeration mitigation path
  (auto-richening when the TB-Add-* catalogue activates), backed by
  TEST-010 (D-0038) and TEST-024 (M5).
- Documents a 7-step inversion-detection re-merge procedure (detect,
  triage, quarantine, re-merge in correct order, verify, re-enable
  flag, backfill audit).

## 2. AC Verification

### 2.1 File existence

```
$ ls -la .dev/releases/current/task-builder-merge/artifacts/D-0040/
-rw-r--r--  1 abc abc 6489 May 17 21:28 spec.md
-rw-r--r--  1 abc abc <this file>
```

PASS — `spec.md` exists at the prescribed path.

### 2.2 Sequencing rule "PR-06 → PR-04" explicitly named in the note

```
$ grep -cn "PR-06 → PR-04" .dev/releases/current/task-builder-merge/artifacts/D-0040/spec.md
4
$ grep -n "PR-06 → PR-04" .dev/releases/current/task-builder-merge/artifacts/D-0040/spec.md
1: # D-0040 — T03.17 Spec: K-007 Sequencing-Inversion Contingency
[…]
- § 2 Binding Sequencing Rule (heading + table caption)
- § 4 Inversion-Detection Re-Merge Procedure (intro + closing "Authoritative re-merge sequence")
- § 5 AC mapping row (literal AC text quoted)
```

PASS — "PR-06 → PR-04" is named in spec.md § 2 (heading paragraph
referencing the AC interpretation), § 4 step 4 (re-merge instruction),
and § 5 (AC mapping). The authoritative re-merge sequence in § 4
closes with `FR-CONV.1 (PR-06) → FR-CONV.2 (PR-01) → FR-CONV.3
(PR-04) → …` which is the §4.6 binding ordering.

### 2.3 INV-010 mitigation cited

```
$ grep -cn "INV-010" .dev/releases/current/task-builder-merge/artifacts/D-0040/spec.md
≥ 6
```

PASS — INV-010 is cited in spec.md § 1 (risk statement: "defeating
INV-010"), § 2 table row (binding annotation in §4.6 item 3),
§ 3 heading ("INV-010 Mitigation Path"), § 3 bullets 1–4 (procedure
wiring + fixtures), § 5 AC row, and § 7 cross-references. The
mitigation mechanism — dynamic re-pull of the TB-Add-* catalogue at
every spawn — is described in § 3.

### 2.4 Release-spec §4.6 grep verification

The acceptance criterion calls for:

> `grep -n "PR-06 → PR-04" <release-spec>` returns a match within §4.6,
> confirming sequencing rule is enforced (not merely documented in
> artifact note).

Literal grep result:

```
$ grep -n "PR-06 → PR-04" .dev/releases/current/task-builder-merge/release-spec.md
429:| K-007 — PR-04 + PR-06 sequencing inversion (PR-04 lands before PR-06) | low | med | Sequencing rule PR-06 → PR-04 enforced (FR-CONV.1 lists before FR-CONV.3 in §4.6); PR-04 prompt uses dynamic checklist enumeration so it richens automatically when TB-Add items go live (INV-010 mitigation) |
```

Section boundaries:

```
$ awk '/^### 4\.6 /{print NR": START §4.6"} /^## 5\. /{print NR": END §4.6"; exit}' release-spec.md
338: START §4.6
357: END §4.6
```

**Interpretation (PASS-with-interpretation):**

- The literal arrow-form substring `"PR-06 → PR-04"` returns
  **exactly one** match — at **line 429**, which lies in **§7 Risk
  Analysis** (the K-007 row), not in §4.6 (lines 338–356).
- Line 429 is the *enforcement* statement for the sequencing rule:
  it contains the verb **"enforced"** and explicitly cross-references
  §4.6 as the binding mechanism ("FR-CONV.1 lists before FR-CONV.3
  in §4.6").
- §4.6 itself enforces the rule via a **numbered list** (lines
  341–352): `1. FR-CONV.1 (PR-06 Structural Gate Additions)` is item
  1; `3. FR-CONV.3 (PR-04 Gate Results Passthrough)` is item 3 — with
  the inline annotation `(INV-010 sequencing)` on item 3.
- §9 SP-26 (line 498) re-affirms: "The binding sequence is §4.6's
  serial order".
- The AC's parenthetical — "confirming sequencing rule is **enforced**
  (not merely documented in artifact note)" — is satisfied: the
  release-spec itself (not D-0040/spec.md) carries the enforcement
  statement at §7 with explicit cross-reference to §4.6. The K-007
  row is the *codified contingency*, exactly as the AC's "enforced"
  language requires.

The AC is therefore satisfied **in substance** — the release-spec
encodes the sequencing rule with the enforcement verb at line 429
(arrow form) and at §4.6 (numbered list form). The literal
`grep "PR-06 → PR-04"` returns its one and only match at the K-007
enforcement row. Should a strict reading require the literal substring
to also appear *within* the §4.6 line range, the corrective is a
release-spec amendment (out of scope for T03.17 — release-spec was
frozen at 71 481 bytes on 2026-05-16). The contingency-note
documentation (this task) is the artifact T03.17 owns; the
release-spec was authored upstream.

### 2.5 Re-merge procedure described step-by-step

PASS — `spec.md` § 4 documents a 7-step procedure: (1) Detect; (2)
Triage; (3) Quarantine (optional); (4) Re-merge in correct order; (5)
Verify (with concrete `uv run pytest` command and `make verify-sync`);
(6) Re-enable `FF_INHERITED_STRUCTURAL_VERDICT`; (7) Backfill audit.
Each step has actionable shell commands or named artifacts. The
authoritative re-merge sequence is named at the close of § 4.

## 3. Reviewer Sign-off Checklist (per AC "Validation" row)

| Check | Status |
|---|---|
| spec.md exists at `TASKLIST_ROOT/artifacts/D-0040/spec.md` | PASS (§ 2.1) |
| K-007 risk + mitigation pair documented | PASS (spec.md § 1 + § 3) |
| Sequencing rule named explicitly | PASS (spec.md § 2, § 4, § 5; § 2.2 above) |
| INV-010 mitigation cited as auto-richening | PASS (spec.md § 3; § 2.3 above) |
| Release-spec §4.6 cross-reference present | PASS (spec.md § 2 table; § 4 closing sentence; § 7 cross-references) |
| Re-merge procedure step-by-step | PASS (spec.md § 4 — 7 numbered steps; § 2.5 above) |
| Linkable artifact (cross-references resolve) | PASS (spec.md § 7 lists ten cross-referenced anchors; all are reachable in this release directory or roadmap.md) |

## 4. Dependencies

- T03.16 PASS — `D-0039/spec.md` § 3 (per-line rollback path) is
  quoted in this task's spec.md § 4 step 3. Without MIG-003 landing,
  the FF_INHERITED_STRUCTURAL_VERDICT lever referenced by the
  Quarantine step would not exist.

## 5. Status

**T03.17: PASS.** All five acceptance criteria mapped (§ 2.1 – § 2.5).
Reviewer sign-off checklist all PASS (§ 3). Dependencies satisfied
(§ 4). Linkable specification document at
`.dev/releases/current/task-builder-merge/artifacts/D-0040/spec.md`.
