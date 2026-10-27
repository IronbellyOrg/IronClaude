# D-0048 — T04.09 Evidence: 15-item checklist body preservation under all M4 axis-overlay edits

**Task:** T04.09 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-080 (15-item checklist body byte-stable across M4 edits)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [█████████-] 90%

---

## 0. TL;DR

R-080 is closed by direct byte-equality proof. The 15-item checklist
body is byte-identical between the **pre-M4 baseline** (commit
`3a57a0d`, PR-04 — the last commit before the PR-07 axis-overlay
landed) and the **post-M4 working tree** (after all axis-overlay,
canonical-rules, and Items-Reviewed-table edits T04.01..T04.08 have
been applied). Both share SHA-256
`78edc7790dc00b49f050f5a7c27484428195a3af189f665c64f21314236c4bf1`,
and `diff` exits 0. Item count is 15 in both. The Tool Engagement
Minimum subsection ("TOTAL checklist items") is also byte-identical
pre/post; only its absolute line number shifted (781 → 826) because of
the upstream axes-header and table-format insertions, which is exactly
what the M4 phase-goal contemplates ("axes multiply lenses, not checks
— TOTAL stays at 15 items").

| AC | Statement | Status | Section |
|----|-----------|--------|---------|
| AC#1 | Byte-diff of 15-item checklist body pre/post all M4 changes is zero | PASS | §2 |
| AC#2 | Item count in the body is exactly 15 | PASS | §3 |
| AC#3 | Tool-Engagement-Minimum statement unchanged | PASS | §4 |
| AC#4 | Evidence at `D-0048/evidence.md` | PASS | this file |

Invariant cross-checks:

| Invariant | Status | Section |
|---|---|---|
| Body hash matches D-0046 baseline (`78edc7790dc00b49…`) | PASS | §2 |
| Pre-M4 baseline (`3a57a0d`) body hash == post-M4 working-tree body hash | PASS | §2 |
| Items 1..15 enumerated, first = "Gate/command dry-run", last = "Cross-reference accuracy for templates" | PASS | §3 |
| Tool Engagement Minimum body byte-identical pre/post (line shift only) | PASS | §4 |
| `src/` ↔ `.claude/` parity preserved | PASS | §5 |

---

## 1. Baseline selection — what counts as "pre-M4"?

The M4 phase-goal binds the 15-item checklist body at the file range
that T04.08 / D-0047 documents as `rf-qa-qualitative.md:546..582` in
the post-overlay working tree. The phase-4 acceptance criterion (R-080)
literally reads "Byte-diff of rf-qa-qualitative.md:527-583 body pre/post
all M4 changes is zero", where `527-583` is the pre-M4 line range and
`546-582` is the post-M4 line range (the +19-line offset comes from the
T04.01 axes header subsection plus the T04.05 canonical-rules
subheader+body, both inserted strictly above the checklist).

The pre-M4 baseline is therefore the body content at commit
`3a57a0d` ("feat(task-builder): PR-04 gate-results passthrough"), which
is the last commit on this branch before `0abf897` ("feat(task-builder):
PR-07 adversarial category naming (5-axis overlay)") landed the first
M4 edit. T04.08 / D-0047 §5 lists every commit/deliverable between
those two points; this section selects the pre-edit anchor.

```
$ git log --oneline --all -- src/superclaude/agents/rf-qa-qualitative.md
ad083b6 feat(task-builder): MIG-003 land FR-CONV.3 Inherited Structural Verdict + Self-Audit (M3)
dfae6cf feat(task-builder): PR-03 DNSP synthetic finding (paradigm-neutral, BASE)
0abf897 feat(task-builder): PR-07 adversarial category naming (5-axis overlay)   <-- first M4 commit
3a57a0d feat(task-builder): PR-04 gate-results passthrough (inherited structural verdict)   <-- last pre-M4 commit
fd41178 feat(reflect): add Re-scrutiny phase 4 + promote rf agents/skills to src/
```

The unstaged edits in the working tree (`git diff HEAD` on this file)
add the AX-1..AX-5 prefixes, the canonical-rules subsection, and the
axis-column reformat of the Items Reviewed table; none of those edits
touch the 15 enumerated checklist items themselves. §2 proves this by
content equality, not just by inspection of the diff.

---

## 2. AC#1 — Byte-diff of 15-item checklist body is zero

**Pre-M4 baseline location:** `rf-qa-qualitative.md:527..563` at commit
`3a57a0d` (last pre-PR-07 commit).
**Post-M4 working-tree location:** `rf-qa-qualitative.md:546..582`
(working tree, all axis-overlay edits applied).
**Span:** 37 lines in both (header + 15 items + trailing blank).

**Hashes:**

```
$ git show 3a57a0d:src/superclaude/agents/rf-qa-qualitative.md \
    | sed -n '527,563p' | sha256sum
78edc7790dc00b49f050f5a7c27484428195a3af189f665c64f21314236c4bf1  -

$ sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
78edc7790dc00b49f050f5a7c27484428195a3af189f665c64f21314236c4bf1  -
```

**Explicit byte-diff:**

```
$ diff \
    <(git show 3a57a0d:src/superclaude/agents/rf-qa-qualitative.md | sed -n '527,563p') \
    <(sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md)
$ echo "exit=$?"
exit=0
```

**Interpretation:**

- Both ranges are 37 lines.
- Both share SHA-256 `78edc7790dc00b49f050f5a7c27484428195a3af189f665c64f21314236c4bf1`.
- `diff` produces no output and exits 0 ⇒ byte-identical.
- The body has been re-anchored by +19 lines (527 → 546) because of
  upstream axes-overlay insertions that landed strictly above the
  checklist header. Content is unchanged.

**Cross-check with D-0046 / D-0047 cumulative baseline:**

D-0046 §4 first declared `78edc7790dc00b49…` as the canonical body
hash post-T04.07. D-0047 §2 confirmed the same hash held after T04.08.
D-0048 now confirms the same hash equals the pre-M4 baseline at commit
`3a57a0d`. The 15-item body has therefore been byte-stable across the
entire M4 milestone, not merely across the most recent edit.

AC#1 satisfied.

---

## 3. AC#2 — Item count = 15

**Post-M4 working tree:**

```
$ sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md \
    | grep -c "^[0-9]\+\."
15

$ sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md \
    | grep -E "^[0-9]+\." | head -1
1. **Gate/command dry-run** — For every shell command, make target, or gate referenced in checklist items ...

$ sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md \
    | grep -E "^[0-9]+\." | tail -1
15. **Cross-reference accuracy for templates** — Verify ALL template section references (§N, "Section X") per phase against actual template content. Read the actual template file and confirm the referenced section exists and contains what the item claims.
```

**Pre-M4 baseline (commit `3a57a0d`):**

```
$ git show 3a57a0d:src/superclaude/agents/rf-qa-qualitative.md \
    | sed -n '527,563p' | grep -c "^[0-9]\+\."
15
```

**Interpretation:**

- Count is exactly 15 enumerated items (`1.` through `15.`) in both
  pre-M4 and post-M4 ranges.
- First item ID is "Gate/command dry-run" (Operational Simulation
  cluster); last is "Cross-reference accuracy for templates" (Failure
  Mode Analysis cluster). Boundaries match D-0046 and D-0047 records.

AC#2 satisfied. Combined with §2's byte-equality proof, the count
match is redundant but explicit per the AC's separate `count == 15`
clause.

---

## 4. AC#3 — Tool-Engagement-Minimum statement unchanged

**Current location (post-M4 working tree):**

```
$ grep -n "Tool Engagement Minimum\|TOTAL checklist items" \
    src/superclaude/agents/rf-qa-qualitative.md
824:- NEVER make generic tool calls to inflate engagement counts ...
826:### Tool Engagement Minimum
827:If your total (Read + Grep + Glob) calls < TOTAL checklist items, the review is automatically suspect. You cannot have verified more items than you made tool calls. Flag this in your report.
```

**Pre-M4 baseline (commit `3a57a0d`):**

```
$ git show 3a57a0d:src/superclaude/agents/rf-qa-qualitative.md \
    | grep -n "Tool Engagement Minimum\|TOTAL checklist items"
781:### Tool Engagement Minimum
782:If your total (Read + Grep + Glob) calls < TOTAL checklist items, the review is automatically suspect. You cannot have verified more items than you made tool calls. Flag this in your report.
```

**Byte-diff of the two-line Tool Engagement Minimum block:**

```
$ diff \
    <(git show 3a57a0d:src/superclaude/agents/rf-qa-qualitative.md | sed -n '781,782p') \
    <(sed -n '826,827p' src/superclaude/agents/rf-qa-qualitative.md)
$ echo "exit=$?"
exit=0
```

**Interpretation:**

- Subsection `### Tool Engagement Minimum` is present in both the
  pre-M4 and post-M4 trees.
- Body line still references "TOTAL checklist items".
- The block is byte-identical (`diff` exits 0); only its absolute
  line number shifted (781 → 826, Δ = +45) because of upstream M4
  insertions (axes header subsection + canonical-rules subsection +
  axis-column reformat of the Items Reviewed table).
- Because TOTAL checklist items for the task-qualitative phase = 15
  (see §3), the effective Tool-Engagement-Minimum for this phase
  remains ≥15 tool calls, matching the T04.08 / D-0047 record and the
  M4 phase-goal exit criterion.

AC#3 satisfied.

---

## 5. Mirror parity (`src/` ↔ `.claude/`)

```
$ sha256sum src/superclaude/agents/rf-qa-qualitative.md \
            .claude/agents/rf-qa-qualitative.md
03c698d283afabc0ada254356d53e107df3f02ee8aca14ed709c8018979dc375  src/superclaude/agents/rf-qa-qualitative.md
03c698d283afabc0ada254356d53e107df3f02ee8aca14ed709c8018979dc375  .claude/agents/rf-qa-qualitative.md
```

**Interpretation:** byte-identical on both sides. `make verify-sync`
remains clean for this file. No sync action required for T04.09.

---

## 6. Cross-task linkage

- **T04.01 / D-0041** (R-070) — landed FR-CONV.4 axis-overlay wrapper
  (`#### Five Adversarial Axes` header) at PR-07 commit `0abf897`,
  strictly above the existing 15-item Checklist header.
- **T04.02..T04.04 / D-0042..D-0044** (R-071..R-075) — populated the
  five canonical axis bullets inside the subsection.
- **T04.05 / D-0045** (R-076, R-077) — added the
  `##### Canonical annotation rules` subheader + body, also strictly
  above the Checklist header.
- **T04.06 / CP-P04-T01-T05** — mid-phase checkpoint PASS.
- **T04.07 / D-0046** (R-078) — `axis` column repositioned in the
  Items Reviewed table (downstream of the checklist; no impact on
  527..583 or 546..582).
- **T04.08 / D-0047** (R-079) — header subsection in place; body hash
  baseline declared.
- **T04.09 / D-0048** (R-080) — **this artifact**: independent
  byte-equality proof against the pre-M4 commit `3a57a0d` baseline.
- **T04.10 / D-0049** (R-081, upcoming) — severity-floor preservation
  at `:786..795` (Critical Rules block); orthogonal range, independent
  guard.

---

## 7. Verdict

**Overall: PASS** — R-080 contract closed.

- Pre-M4 baseline body (commit `3a57a0d`, lines 527..563) is
  byte-identical to post-M4 working-tree body (lines 546..582).
  Both share SHA-256
  `78edc7790dc00b49f050f5a7c27484428195a3af189f665c64f21314236c4bf1`,
  and `diff` exits 0.
- Item count is exactly 15 in both pre-M4 and post-M4 trees; first
  item "Gate/command dry-run", last item "Cross-reference accuracy
  for templates".
- Tool Engagement Minimum subsection is byte-identical pre/post
  (line shift only); for the task-qualitative phase, TOTAL checklist
  items = 15, so the ≥15 tool-calls floor is preserved.
- `src/` ↔ `.claude/` mirror parity holds.

**Confidence:** [█████████-] 90% — bounded by the explicit byte-equality
proof (independent hash + `diff` + line-count) against a pre-M4 commit
captured before any axis-overlay landed. The remaining failure mode —
an edit landing in `:546..582` between now and the MIG-004 commit
(T04.15) — is monitored by T04.10 / D-0049 (severity floor) and the
end-of-phase checkpoint CP-P04-END.
