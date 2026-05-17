# D-0047 — T04.08 Spec: Insert `### Five Adversarial Axes` header subsection

**Task:** T04.08 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-079 (Five Adversarial Axes header subsection at rf-qa-qualitative.md:527)
**Date:** 2026-05-17
**Tier:** STANDARD
**Confidence:** [█████████-] 90%

---

## 1. Scope

Ensure the **Five Adversarial Axes** header subsection sits in
`src/superclaude/agents/rf-qa-qualitative.md` **before** the
`#### Checklist (15 items)` header, with the 15-item checklist body
preserved byte-for-byte across all M4 edits to date. The R-079 contract
binds the ordering invariant (axes header line N precedes checklist
header line M) and the body preservation invariant (lines 546..582
SHA-256 stable).

The wrapper itself landed at PR-07 commit `0abf897` under T04.01 /
D-0041 ("Land FR-CONV.4 axis overlay wrapper") and was extended by:

- T04.02 / D-0042 — AX-1 + AX-2 canonical entries
- T04.03 / D-0043 — AX-3 + AX-4 canonical entries
- T04.04 / D-0044 — AX-5 canonical entry
- T04.05 / D-0045 — `none` sentinel + `drift-axis-inactive` annotation
  rules (subheader `##### Canonical annotation rules ...`)
- T04.07 / D-0046 — `axis` column repositioned in the Items Reviewed
  table (downstream of the header subsection; no impact on lines
  527..583)

T04.08 / D-0047 closes R-079 by verifying that the header subsection is
in place at the canonical location, that its descendants (the five axis
bullets and the canonical-rules subheader) precede the Checklist header,
and that the 15-item checklist body is byte-identical to the D-0046
baseline.

**No new edits are required.** This task is verification-only;
"insertion" was satisfied by the upstream T04.01..T04.05 sequence, and
T04.08 records the contract closure under the R-079 roadmap row.

## 2. Ordering contract

```
grep -n "Five Adversarial Axes\|Checklist (15 items)" \
  src/superclaude/agents/rf-qa-qualitative.md | sort -t: -k2n
```

Expected output (suppressing the in-body AX-1 finding-example line at
532 which is a bullet body, not a header):

```
528:#### Five Adversarial Axes (PR-07 — applied as a sharpening overlay across all 15 checks below)
546:#### Checklist (15 items)
```

The axes header at line 528 precedes the Checklist header at line 546.
The 18-line gap at 529..545 holds:

- Lines 529..530 — overlay-paragraph prose ("These axes are NOT new
  checks ...")
- Lines 532..536 — the five axis bullets (AX-1 Drift, AX-2
  Contradictions, AX-3 Omissions, AX-4 Weakened-criteria, AX-5
  Invented-content)
- Line 538 — `##### Canonical annotation rules (PR-07 — \`none\`
  sentinel + \`drift-axis-inactive\`)` subheader (T04.05 / D-0045)
- Lines 540..544 — canonical-rules body (vocabulary closure, `N/A`
  forbidden, `drift-axis-inactive` Summary-block annotation rule)

The trailing grep match at line 714 (`subsection under "Five Adversarial
Axes" for the binding spec`) is the HTML comment under the Items
Reviewed table; it is a back-reference to the subsection from a
downstream block and is structurally orthogonal to the ordering
contract.

## 3. Byte-stability contract for the 15-item checklist body

The canonical "15-item checklist body" range is `lines 546..582`,
inclusive of the `#### Checklist (15 items)` header at 546 and ending
at the last numbered item (15. Cross-reference accuracy for templates,
line 581) plus the trailing blank line at 582.

Baseline SHA-256 (captured by T04.07 / D-0046):

```
78edc7790dc00b49f050f5a7c27484428195a3af189f665c64f21314236c4bf1
```

T04.08 re-hashes the same range post-M4-edits-to-date and asserts the
hash matches the baseline byte-for-byte. Any non-zero diff is a CRITICAL
violation of the M4 phase invariant ("axes multiply lenses, not checks
— TOTAL stays at 15 items").

## 4. Acceptance Criteria (from phase-4-tasklist.md T04.08)

| AC | Statement | Evidence section |
|----|-----------|------------------|
| AC#1 | `grep -n "Five Adversarial Axes\|Checklist (15 items)" rf-qa-qualitative.md \| sort -t: -k2n` shows Axes header line precedes Checklist header line | evidence.md §1 |
| AC#2 | Byte-diff of the 15-item checklist body (lines 546..582) pre/post insertion is zero (matches D-0046 baseline `78edc7790dc00b49...`) | evidence.md §2 |
| AC#3 | Evidence at `TASKLIST_ROOT/artifacts/D-0047/evidence.md` | evidence.md (this artifact) |
| AC#4 | Tool-Engagement-Minimum statement at `rf-qa-qualitative.md:826..827` still references "TOTAL checklist items" (= 15 for task-qualitative) | evidence.md §3 |

## 5. Invariants preserved

- 15-item checklist body (lines 546..582) byte-stable — no T04.08 edit
  lands in the range.
- Critical Rules block (lines 786..795 per the phase-goal pin / lines
  834..846 in the current file structure) byte-stable — T04.10 / D-0049
  is the dedicated severity-floor preservation task; T04.08 does not
  touch it.
- Canonical annotation rules subsection (lines 538..544) untouched —
  the `none` sentinel + `drift-axis-inactive` semantics land via
  T04.05 / D-0045.
- Axis column placement (lines 708..711 in the Output Format block)
  untouched — owned by T04.07 / D-0046 and re-applied under
  COMP-004-M4 governance by T04.11 / D-0050.
- `src/` ↔ `.claude/` parity (sha256
  `03c698d283afabc0ada254356d53e107df3f02ee8aca14ed709c8018979dc375`
  matches on both sides).
- Tool Engagement Minimum subsection (`### Tool Engagement Minimum` at
  line 826) unchanged.

## 6. Rollback

No edit lands in this task, so rollback is a no-op. R-079 contract
closure is recorded in `evidence.md` and the FF_FIVE_ADVERSARIAL_AXES
governance entry (T04.15 / D-0053). Reverting the upstream
T04.01..T04.05 sequence reverts R-079 transitively; this task adds no
new content to revert.

## 7. Out of scope (deferred to other phase-4 tasks)

- 15-item body preservation as a standalone evidence artifact —
  T04.09 / D-0048 (covers the same body range under a dedicated
  byte-diff report).
- Severity-floor preservation at `rf-qa-qualitative.md:786..795` —
  T04.10 / D-0049.
- Axis-column COMP-004-M4 edit-site governance — T04.11 / D-0050.
- SKILL.md axis-annotation directive — T04.13 / D-0051.
- TEST-011..014 pytest fixtures — T04.14 / D-0052.
- MIG-004 single-commit landing — T04.15 / D-0053.
