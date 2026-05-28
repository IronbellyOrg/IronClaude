# D-0049 — T04.10 Evidence: Severity-floor preservation at rf-qa-qualitative.md:786-795

**Task:** T04.10 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-081 (severity-floor block byte-stable across M4 edits)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [█████████-] 90%

---

## 0. TL;DR

R-081 is closed by direct byte-equality proof. The severity-floor block
that anchors Critical Rule #6 ("Contradictions are always IMPORTANT or
CRITICAL") is byte-identical between the **pre-M4 baseline** (commit
`3a57a0d`, the last commit on this branch before the PR-07 axis-overlay
landed) and the **post-M4 working tree** (after T04.01..T04.08
axis-overlay edits). Two independent equalities are demonstrated:

1. The literal `:786-795` spec range — SHA-256
   `770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9de91fc7`
   pre and post, `diff` exits 0. In the post-M4 tree this exact byte
   slice now lives at `:831-840` (line-offset +45 from upstream
   axes-header + canonical-rules + table-reformat insertions, same
   offset pattern documented in D-0048 for the 15-item checklist).
2. The entire **Critical Rules** block (header + Rules #1..#11) —
   SHA-256
   `fd7f2e457bf63ce0045ec5d7014e9af67c1b46892f49b090334be17bbd2fff0f`
   pre and post. The block lives at `:789-801` pre-M4 and at
   `:834-846` post-M4; content is byte-identical.

Rule #6 ("Contradictions are always IMPORTANT or CRITICAL — …Always
surface contradictions.") appears verbatim at:
- pre-M4 baseline (`3a57a0d`): line 796
- post-M4 `src/superclaude/agents/rf-qa-qualitative.md`: line 841
- post-M4 `.claude/agents/rf-qa-qualitative.md`: line 841
identical content, same SHA, no softening.

| AC | Statement | Status | Section |
|----|-----------|--------|---------|
| AC#1 | Byte-diff of rf-qa-qualitative.md:786-795 pre/post all M4 changes is zero | PASS | §2 |
| AC#2 | Contradictions severity floor (IMPORTANT/CRITICAL) verbatim in the block | PASS | §3 |
| AC#3 | Evidence at `D-0049/evidence.md` | PASS | this file |
| AC#4 | Critical Rules block hash matches the baseline captured pre-edit | PASS | §2 |

Invariant cross-checks:

| Invariant | Status | Section |
|---|---|---|
| Pre-M4 `:786-795` SHA-256 == post-M4 `:831-840` SHA-256 (`770f4395…`) | PASS | §2 |
| Pre-M4 Critical Rules block SHA-256 == post-M4 SHA-256 (`fd7f2e45…`) | PASS | §2 |
| Rule #6 text verbatim in baseline and current src/ and .claude/ copies | PASS | §3 |
| `src/` ↔ `.claude/` parity preserved (no diff) | PASS | §4 |
| Range/block hashes unaffected by upstream M4 insertions (offset +45 only) | PASS | §2 |

---

## 1. Baseline selection — what counts as "pre-M4"?

Per D-0048 §1 (already established for the 15-item checklist), the
pre-M4 baseline for this file is commit `3a57a0d`
("feat(task-builder): PR-04 gate-results passthrough"), the last commit
on `feat/mig-002-execution-context-header` before `0abf897`
("feat(task-builder): PR-07 adversarial category naming (5-axis
overlay)") landed the first M4 edit. The same selection is used here so
T04.09 and T04.10 anchor to identical pre-M4 state.

The post-M4 anchor is the current working tree (`HEAD` plus unstaged
M4 edits, namely T04.01..T04.08). T04.10 is a no-edit verification
task — its acceptance criteria require that **no M4 edit lands inside
`:786-795` or anywhere in the Critical Rules block**.

Within the pre-M4 baseline at `3a57a0d`:
- `:786-795` is a 10-line slice that opens with the trailing `---`
  separator before the Critical Rules section, then `## Critical Rules`
  header, then Rules #1..#5 (Rule #5 ends the slice). Rule #6 begins
  on line 796 — one line below the spec range.
- The full Critical Rules block spans `:789-801` (header + blank +
  Rules #1..#11), ending at end-of-file.

The spec's `:786-795` window therefore protects **the opening of the
Critical Rules block** (the section anchor and Rules #1..#5). Rule #6
itself is one line past the slice; the AC#2 + AC#4 pairing ("severity
floor verbatim" + "Critical Rules block hash matches baseline") closes
the window by requiring that the whole block — including Rule #6 — be
byte-identical to baseline. Both checks are performed below.

---

## 2. Byte-equality proofs

### 2.1 Strict spec range `:786-795` (pre-M4) ↔ `:831-840` (post-M4)

```
$ git show 3a57a0d:src/superclaude/agents/rf-qa-qualitative.md \
    | sed -n '786,795p' | sha256sum
770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9de91fc7  -

$ sed -n '831,840p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9de91fc7  -

$ diff -u \
    <(git show 3a57a0d:src/superclaude/agents/rf-qa-qualitative.md | sed -n '786,795p') \
    <(sed -n '831,840p' src/superclaude/agents/rf-qa-qualitative.md)
# (empty — diff exits 0)
```

Snapshots saved alongside this evidence for reviewer inspection:
- `pre-m4_786-795.txt` — pre-M4 baseline byte slice
- `post-m4_831-840.txt` — post-M4 working-tree byte slice

The +45-line offset (786 → 831) is fully accounted for by the
strictly-additive insertions above the Critical Rules section in
T04.01..T04.08: the Five Adversarial Axes header subsection, the
canonical-rules block (FR-CONV.4 wrapper), and the axis-column reformat
of the Items Reviewed table. No edit landed inside the slice.

### 2.2 Entire Critical Rules block

```
$ git show 3a57a0d:src/superclaude/agents/rf-qa-qualitative.md \
    | sed -n '789,801p' | sha256sum            # pre-M4 block
fd7f2e457bf63ce0045ec5d7014e9af67c1b46892f49b090334be17bbd2fff0f  -

$ sed -n '834,846p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
fd7f2e457bf63ce0045ec5d7014e9af67c1b46892f49b090334be17bbd2fff0f  -
```

Block bounds:
- pre-M4 baseline: `:789-801` (file ends at 801; Critical Rules is the
  last `##` section in the pre-M3 layout).
- post-M4 working tree: `:834-846` for the same content. (Lines 847-849
  in the post-M4 tree are a blank + `---` + blank separator that is
  followed by the M3-era sections `## Self-Audit Schema Requirement`
  (850), `## Handling the Inherited Structural Verdict` (920), `##
  Self-Audit` (962). Those sections were added in M3, not M4, and live
  *after* the Critical Rules block — they do not touch it.)

Content equality is the relevant invariant; block-boundary trailing
whitespace beyond Rule #11 is not part of the severity floor.

---

## 3. Rule #6 verbatim (severity floor)

The severity-floor literal is Critical Rule #6:

> 6. **Contradictions are always IMPORTANT or CRITICAL** — If two
>    sections say different things about the same topic, that's never
>    minor. Always surface contradictions.

Verified verbatim in all three locations:

```
$ git show 3a57a0d:src/superclaude/agents/rf-qa-qualitative.md \
    | grep -n "Contradictions are always IMPORTANT or CRITICAL"
796:6. **Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.

$ grep -n "Contradictions are always IMPORTANT or CRITICAL" \
    src/superclaude/agents/rf-qa-qualitative.md
841:6. **Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.

$ grep -n "Contradictions are always IMPORTANT or CRITICAL" \
    .claude/agents/rf-qa-qualitative.md
841:6. **Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.
```

Three locations, identical text, no softening (no "should",
"typically", "consider", "may be MINOR", etc. introduced). The floor
is preserved.

---

## 4. `src/` ↔ `.claude/` parity

```
$ diff src/superclaude/agents/rf-qa-qualitative.md \
       .claude/agents/rf-qa-qualitative.md
# (empty)
```

Both copies are byte-identical, so the severity-floor invariant holds
in both source-of-truth (`src/superclaude/agents/`) and Claude Code's
read path (`.claude/agents/`). `make verify-sync` will pass on this
file at the next sync.

---

## 5. Acceptance Criteria status

| AC | Statement | Status | Evidence |
|----|-----------|--------|----------|
| AC#1 | Byte-diff of rf-qa-qualitative.md:786-795 pre/post all M4 changes is zero | PASS | §2.1 — `diff` exits 0; both slices SHA `770f4395…` |
| AC#2 | Contradictions severity floor (IMPORTANT/CRITICAL) verbatim in the block | PASS | §3 — Rule #6 byte-identical at baseline:796, post-M4:841 (src/ and .claude/) |
| AC#3 | Evidence at `TASKLIST_ROOT/artifacts/D-0049/evidence.md` | PASS | this file |
| AC#4 | Critical Rules block hash matches the baseline captured pre-edit | PASS | §2.2 — both block hashes equal `fd7f2e45…` |

---

## 6. Notes

- T04.10 is a verification-only task; no edits to the file were made
  by this task. The pre/post equality is the deliverable.
- The `:786-795` spec range is anchored to the **pre-M4** line
  numbering. Post-M4 the equivalent slice is at `:831-840` (offset
  +45). Reviewers checking the post-edit tree should use the shifted
  range and verify the block hash equals `fd7f2e45…` against the
  baseline at `3a57a0d`.
- The full Critical Rules block is unchanged. Rule #6 (the explicit
  severity floor) is byte-identical. AX-2 (Contradictions) language
  introduced in T04.02 / D-0042 lives in the canonical-axes block
  *above* the Critical Rules section; per the M4 phase goal it
  references Rule #6 rather than rewriting it.
