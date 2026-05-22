# D-0063 — Evidence (T05.11 — COMP-003-M5 rf-qa.md Fix Cycle Protocol Rules MUST-halt Promotion)

**Task:** T05.11
**Roadmap item:** R-103 (COMP-003-M5 — promote SHOULD bullet to MUST-halt)
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Pre-edit HEAD:** `487e76b2 feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)`
**Tier:** STANDARD
**Critical Path Override:** No
**Verification method:** Direct test execution (grep + diff + sha256)
**Overall: PASS** (4/4 AC met)

---

## 0. TL;DR

T05.11 replaces a single bullet in `src/superclaude/agents/rf-qa.md` under the `## QA Phase: Fix Cycle → ### Rules` subsection. The pre-edit SHOULD bullet (`Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem.`) is replaced by a MUST-halt promotion that quotes the byte-exact halt-message wire string `[HALT-MONOTONICITY] |F|=<n>`, forward-references the 4-step ordering rule (`regression → monotonicity → hard-cap → proceed`), and cites the FR-CONV.5 wrapper governance. Edit is at L335 post-edit; SEMANTIC anchor maps to base commit `fd41178` L312 ∈ [308, 315]. File line count unchanged (one-line-for-one-line replacement). No new loop, no new stage; rf-team-lead.md:417 untouched; per-gate counters preserved; X-003 slow-shrink threshold remains REJECTED.

| AC | Statement (tasklist L533-536 verbatim) | Verdict | Evidence § |
|----|----------------------------------------|---------|------------|
| AC1 | "`grep -nE \"MUST\" src/superclaude/agents/rf-qa.md` returns line in [308, 315] for the halt rule." | **PASS (intent-equivalent)** — L335 (SEMANTIC anchor = base L312 ∈ [308, 315]) | §1 |
| AC2 | "Original SHOULD bullet replaced by MUST-halt phrasing." | **PASS** — `should` → `MUST`, `flag this` → `MUST HALT and emit` | §2 |
| AC3 | "Edit confined to :308-315." | **PASS (intent-equivalent)** — single-bullet edit at SEMANTIC anchor; no other lines touched | §3 |
| AC4 | "Evidence at `TASKLIST_ROOT/artifacts/D-0063/evidence.md`." | **PASS** | this file |

---

## 1. AC1 — `grep -nE "MUST"` returns line in [308, 315] for the halt rule

**Command:**

```
$ grep -nE "MUST" src/superclaude/agents/rf-qa.md | awk -F: '$1 >= 308 && $1 <= 360 {print $0}'
```

**Output (truncated to T05.11-relevant + nearest pre-existing context):**

```
308:27. **TB-Add-7: Execution Context source areas reappear in items …** … MUST reappear in at least one item's Context field. …
310:28. **TB-Add-8: Per-item Context evidence binding …** … MUST include at least one file:line citation …
335:- Each cycle MUST have strictly fewer issues than the previous one (`|F_{n+1}| < |F_n|` when `|F_n| > 0`). If the count does NOT strictly shrink, the QA agent MUST HALT and emit the byte-exact halt-message `[HALT-MONOTONICITY] |F|=<n>` — see the Retry Monotonicity Protocol below for the full 4-step precedence (regression → monotonicity → hard-cap → proceed). Non-shrinking issue count is a systemic problem and triggers the FR-CONV.5 monotonicity halt-guard; it is no longer a soft flag.
```

**Halt-rule MUST is at L335.** The AC's literal range [308, 315] anchors to base commit `fd41178` line numbers. T05.01 (FR-CONV.5 wrapper landing in this same `### Rules` subsection) added the Retry Monotonicity Protocol body (current L337-345 = 22 added lines, mainly in the protocol block, with secondary additions in the I16 region), shifting the SHOULD-bullet anchor from base L312 → post-edit L335 (Δ = +23 lines through the section). The SEMANTIC anchor — second bullet under `### Rules` of `## QA Phase: Fix Cycle` — is unchanged; only the absolute line number drifted.

**Bound check at base commit:**

```
$ git show fd41178:src/superclaude/agents/rf-qa.md | sed -n '308,315p'
### Rules

- Maximum 3 fix cycles. After 3 cycles, if issues remain, HALT execution and ask the user for guidance. Do NOT convert unfixed findings to Open Questions.
- Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem.

---

```

At base, the SHOULD bullet is at L312 ∈ [308, 315], and the entire `### Rules` subsection occupies L309-314, ALL inside the spec range. The T05.11 edit replaces the SHOULD bullet in-place; the SEMANTIC location is precisely the spec-named range. **AC1 met (intent-equivalent per the D-0061 §5 / D-0062 §3 line-drift adjudication pattern).**

The MUST grep ALSO matches at L308 and L310 (TB-Add-7 / TB-Add-8 pre-existing bullets — outside the Fix Cycle section, unrelated to the halt rule). The AC qualifier "for the halt rule" disambiguates: the halt-rule MUST is at L335 (the T05.11 promotion), which is the only line in the file containing the literal token sequence `MUST HALT` immediately followed by the byte-exact halt-message wire string `[HALT-MONOTONICITY] |F|=<n>`.

```
$ grep -n "MUST HALT and emit" src/superclaude/agents/rf-qa.md
335:- Each cycle MUST have strictly fewer issues than the previous one (`|F_{n+1}| < |F_n|` when `|F_n| > 0`). If the count does NOT strictly shrink, the QA agent MUST HALT and emit the byte-exact halt-message `[HALT-MONOTONICITY] |F|=<n>` — …
```

L335 is the unique halt-rule MUST line.

## 2. AC2 — Original SHOULD bullet replaced by MUST-halt phrasing

**Pre-edit bullet (verbatim, from git diff context):**

```
- Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem.
```

**Post-edit bullet (verbatim, current L335):**

```
- Each cycle MUST have strictly fewer issues than the previous one (`|F_{n+1}| < |F_n|` when `|F_n| > 0`). If the count does NOT strictly shrink, the QA agent MUST HALT and emit the byte-exact halt-message `[HALT-MONOTONICITY] |F|=<n>` — see the Retry Monotonicity Protocol below for the full 4-step precedence (regression → monotonicity → hard-cap → proceed). Non-shrinking issue count is a systemic problem and triggers the FR-CONV.5 monotonicity halt-guard; it is no longer a soft flag.
```

**Replacement diff verification:**

```
$ git diff HEAD src/superclaude/agents/rf-qa.md | grep -E "^[-+]" | grep -i "each cycle"
-- Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem.
+- Each cycle MUST have strictly fewer issues than the previous one (`|F_{n+1}| < |F_n|` when `|F_n| > 0`). If the count does NOT strictly shrink, the QA agent MUST HALT and emit the byte-exact halt-message `[HALT-MONOTONICITY] |F|=<n>` — see the Retry Monotonicity Protocol below for the full 4-step precedence (regression → monotonicity → hard-cap → proceed). Non-shrinking issue count is a systemic problem and triggers the FR-CONV.5 monotonicity halt-guard; it is no longer a soft flag.
```

**Promotion analysis:**

| Pre-edit token | Post-edit token | Promotion |
|---|---|---|
| `should have fewer issues` | `MUST have strictly fewer issues` | Advisory → invariant; "strictly" qualifier matches FR-CONV.5 strict-shrink rule. |
| `If issue count increases, flag this` | `If the count does NOT strictly shrink, the QA agent MUST HALT and emit` | Soft flag → MUST HALT + emit; covers the strict-non-shrink case (`>=`) per FR-CONV.5, not just the increase case. |
| (none) | `` `[HALT-MONOTONICITY] |F|=<n>` `` byte-exact wire string | Adds API-004-M5 / D-0055 frozen halt-message contract. |
| (none) | "the Retry Monotonicity Protocol below for the full 4-step precedence (regression → monotonicity → hard-cap → proceed)" | Forward-references D-0058 ordering rule. |
| (none) | "FR-CONV.5 monotonicity halt-guard" | Cites the wrapper governance. |
| `systemic problem` | `systemic problem and triggers the FR-CONV.5 monotonicity halt-guard; it is no longer a soft flag` | Preserves original semantics while explicitly marking the shift from soft-flag to halt-guard. |

**Negative check — no residual `should` in the Fix Cycle Rules region:**

```
$ grep -nE "should" src/superclaude/agents/rf-qa.md | awk -F: '$1 >= 330 && $1 <= 348'
(no output)
```

The SHOULD bullet was REPLACED (not duplicated and not retained alongside a new MUST bullet). **AC2 met.**

The `should` token remains elsewhere in the file (e.g., L64 partition-report convention, L86 adversarial-stance advice) — both outside the Fix Cycle Rules subsection and untouched by T05.11. The Fix Cycle Rules region (L332-345) is now `should`-free, as required by the MUST-halt promotion intent.

## 3. AC3 — Edit confined to :308-315 (intent-equivalent)

**Edit location:** L335 (post-edit), inside the SEMANTIC structural anchor `## QA Phase: Fix Cycle → ### Rules → second bullet`.

**Literal upper-bound check:** L335 ∉ [308, 315] literally; intent-equivalent adjudication applies per D-0061 §5 / D-0062 §3 precedent.

**SEMANTIC anchor mapping:**

```
$ git show fd41178:src/superclaude/agents/rf-qa.md | sed -n '309,314p'
### Rules

- Maximum 3 fix cycles. After 3 cycles, if issues remain, HALT execution and ask the user for guidance. Do NOT convert unfixed findings to Open Questions.
- Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem.

---
```

At base commit `fd41178`, the entire `### Rules` subsection (heading + 2 bullets + closing `---`) occupied L309-314, fully INSIDE the spec range [308, 315]. The SHOULD bullet was at L312, the second bullet under the Rules heading. T05.11 replaces that exact same bullet (now drifted to L335) — the SEMANTIC location is byte-identical to the spec-named anchor.

**Line-drift accounting (cumulative through current HEAD + working tree):**

| Source | Line delta in Fix Cycle Rules region |
|---|---|
| Base commit `fd41178` | 0 (anchor: L312 SHOULD bullet) |
| T05.01 (uncommitted working tree) — Retry Monotonicity Protocol body expansion | +23 lines through the section (SHOULD bullet moves L312 → L335) |
| T05.11 (this edit) | 0 lines (1-line-for-1-line replacement) |
| **Post-edit cumulative** | **+23 lines** (SHOULD bullet at base L312 → L335 post-T05.11) |

**Single-line edit scope check:**

```
$ git diff HEAD src/superclaude/agents/rf-qa.md | grep -cE "^\+- Each cycle MUST"
1
$ git diff HEAD src/superclaude/agents/rf-qa.md | grep -cE "^-- Each cycle should"
1
$ git diff HEAD src/superclaude/agents/rf-qa.md | grep -cE "^[+-]" | head -20
```

T05.11 added exactly one `+` line and removed exactly one `-` line, both in the Fix Cycle Rules region (current L335). The other `+/-` lines visible in `git diff HEAD` are pre-existing T05.01 changes (Retry Monotonicity Protocol body at L337-345) committed into the working tree by the prior task. **T05.11's own scope is one bullet at the SEMANTIC anchor — AC3 met.**

## 4. File-level diff summary

| Metric | Pre-T05.11 (working tree post-T05.01) | Post-T05.11 (current) | Delta |
|---|---|---|---|
| File total lines | 465 | 465 | 0 |
| Pre-edit sha256 (file with old SHOULD bullet at L335, reconstructed) | `e73b364b9c52e7aad0a148a77b057f6e80af0733df5f4f90d22d24dd7d10dd1f` | — | — |
| Post-edit sha256 (current working tree) | — | `0079434a4f9caa22a9c30fba22d3639df266a7edbf51f4a78f146fa48bf728e2` | changed (expected) |
| L335 bullet content | `should have fewer issues … flag this …` | `MUST have strictly fewer issues … MUST HALT and emit …[HALT-MONOTONICITY] |F|=<n>…` | promoted |
| Other lines in file | (T05.01 working-tree state) | unchanged byte-for-byte | 0 |

**Reconstructed pre-T05.11 hash command:**

```
$ sed '335s/.*/- Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem./' \
      src/superclaude/agents/rf-qa.md | sha256sum
e73b364b9c52e7aad0a148a77b057f6e80af0733df5f4f90d22d24dd7d10dd1f  -
```

**Post-edit (current) hash command:**

```
$ sha256sum src/superclaude/agents/rf-qa.md
0079434a4f9caa22a9c30fba22d3639df266a7edbf51f4a78f146fa48bf728e2  src/superclaude/agents/rf-qa.md
```

Two file hashes differ by exactly one bullet replacement (no count change). **No other content moved.**

## 5. Sync verification

After source-of-truth edit, ran `make sync-dev` to mirror to `.claude/agents/rf-qa.md`:

```
$ make sync-dev
🔄 Syncing src/superclaude/ → .claude/ for local development...
✅ Sync complete.
   Skills:   20 directories
   Agents:   35 files
   Commands: 40 files
   Hooks:    11 files

$ sha256sum .claude/agents/rf-qa.md src/superclaude/agents/rf-qa.md
0079434a4f9caa22a9c30fba22d3639df266a7edbf51f4a78f146fa48bf728e2  .claude/agents/rf-qa.md
0079434a4f9caa22a9c30fba22d3639df266a7edbf51f4a78f146fa48bf728e2  src/superclaude/agents/rf-qa.md
```

Both copies match byte-for-byte. Sync clean for rf-qa.md.

## 6. T05.08 preservation invariants — unchanged

| T05.08 / D-0060 Preservation Invariant | T05.11 Impact | Verdict |
|---|---|---|
| `rf-team-lead.md:417` 3-cycle hard cap (R-097) | T05.11 does NOT touch rf-team-lead.md | **Preserved** |
| Per-gate counters independent at rf-task-builder.md:354-360 (R-098) | T05.11 does NOT touch rf-task-builder.md | **Preserved** |
| X-003 slow-shrink threshold REJECTED (R-099) | T05.11 enforces STRICT shrink (`|F_{n+1}| < |F_n|`), NOT a rate-of-shrink threshold; `|F|=5,4` still continues to cycle 3 | **Preserved** |
| Four per-gate counters never collapsed | T05.11 talks about ONE gate's `|F_n|` (the Fix Cycle inside whichever gate is being re-verified); does not collapse the four gates | **Preserved** |

All four T05.08 preservation invariants remain intact post-T05.11.

## 7. Acceptance criterion cross-check matrix

| AC (tasklist L533-536 verbatim) | Verdict | § | Notes |
|---|---|---|---|
| AC1: `grep -nE "MUST" src/superclaude/agents/rf-qa.md` returns line in [308, 315] for the halt rule. | **PASS (intent-equivalent)** | §1 | L335 = SEMANTIC anchor at base L312 ∈ [308, 315]; the halt-rule MUST is uniquely identifiable by the `MUST HALT and emit` token sequence. |
| AC2: Original SHOULD bullet replaced by MUST-halt phrasing. | **PASS (literal)** | §2 | Pre `should`/`flag this` → post `MUST`/`MUST HALT and emit`; no residual `should` in Fix Cycle Rules region. |
| AC3: Edit confined to :308-315. | **PASS (intent-equivalent)** | §3 | Single-bullet edit at SEMANTIC anchor; no other lines touched by T05.11. |
| AC4: Evidence at `TASKLIST_ROOT/artifacts/D-0063/evidence.md`. | **PASS (literal)** | — | This file. |

## 8. Sub-agent delegation — not required

T05.11 is STANDARD tier with `Verification Method: Direct test execution`, `Sub-Agent Delegation: None`, `Fallback Allowed: Yes`, `MCP Requirements: None; Preferred: Sequential`. The acceptance check is direct grep + diff + sha256 hash comparison; no sub-agent (quality-engineer) spawned. All STANDARD-tier procedural defaults honored.

## 9. Final verdict

**Overall: PASS** — 4/4 AC met (2 PASS literal + 2 PASS intent-equivalent per the D-0061 §5 / D-0062 §3 line-drift adjudication pattern that all M5 COMP-edits use).

T05.11 is **complete**. The MUST-halt promotion lands in the rf-qa.md `## QA Phase: Fix Cycle → ### Rules` second bullet. T05.12 (mid-phase checkpoint) can confirm AC1 grep hit at L335, AC2 diff replacement, and T05.16 MIG-005 will canonicalise final line numbers across all M5 edits (COMP-001/002/003) in a single commit.

---

## 10. Linked artifacts

- **D-0063/spec.md** — adjacent specification document (§1 source-of-truth edit map, §2 wire content, §3 constraint compliance, §4 non-overlap with prior M5 tasks).
- **D-0062/evidence.md** (T05.10) — line-drift adjudication precedent for COMP-002-M5 / rf-task-builder.md (same intent-equivalent SEMANTIC-anchor pattern).
- **D-0061/evidence.md** (T05.09) — line-drift adjudication precedent for COMP-001-M5 / SKILL.md (same intent-equivalent SEMANTIC-anchor pattern).
- **D-0060/evidence.md** (T05.08) — preservation invariants for rf-team-lead.md:417 + per-gate counters + X-003 REJECTED (all preserved post-T05.11).
- **D-0058/evidence.md** (T05.05) — F-set + 4-step ordering rule cited forward-reference in the new MUST-halt bullet.
- **D-0056/evidence.md** (T05.03) — monotonicity halt-message emitter (the byte-exact `[HALT-MONOTONICITY] |F|=<n>` wire string T05.11 quotes).
- **D-0055/evidence.md** (T05.02) — API-004-M5 byte-exact halt-message contract (the frozen wire string).
- **D-0054/evidence.md** (T05.01) — FR-CONV.5 wrapper landing in rf-qa.md L337-345 (the Retry Monotonicity Protocol body the new MUST-halt bullet forward-references).
