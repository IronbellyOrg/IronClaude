# Cross-Validation Report — Reflect POST/Terminal Gate-Wiring Research

**Date:** 2026-06-10
**Analysis type:** completeness-verification
**Lens:** cross-validation (verbatim quote + line-number spot-check against live source)
**Files analyzed:** 01-o1-taskbuilder-edit-surface.md, 02-o2-sctasklist-edit-surface.md, 03-acceptance-test-and-guard-shape.md
**Plus:** research-notes.md, reflect-wrapper-contract.md, and live source files

---

## Methodology

Each research-file claim about a verbatim block or line number was independently
re-verified by opening the live source file and reading the cited range. Cross-file
consistency was checked for the marker name, contract shapes, and the test anchor.

---

## File 01 — task-builder edit surface — SPOT-CHECK RESULTS

Independently re-read live `src/superclaude/skills/task-builder/SKILL.md`.

| # | Research 01 claim | Live source | Verdict |
|---|-------------------|-------------|---------|
| 1 | POST item `N.{X-1}` at L2193-2198, verbatim 6-field self-run block | L2193 heading exact; L2194-2198 body byte-match; `N.X — Update task status to Done` at L2200 | VERIFIED |
| 2 | Critical Rule 20 at L2312, single para "SELF-RUN reflect item … `/sc:reflect --mode post` … `reflect_post` … MALFORMED" | L2312 byte-match | VERIFIED |
| 3 | A.9 POST_REFLECT_GATE block at L1073-1076 (ENABLED / SPEC_PATH / DEPTH `<max(tcs…,standard)>` / TASK_FILE) | L1073-1076 byte-match incl. `# POST floor per O4, never quick` comment | VERIFIED |
| 4 | Frontmatter template at L2137-2156; declares NONE of `start_commit`/`executor_model_class`/`reflect_post` | L2137-2156 byte-match; none of the three O1 keys present | VERIFIED |

**File 01 cross-check vs contract:**
- O1 shape `superclaude reflect run <abs> --depth deep --fix --promote`, `--base` omitted → frontmatter `start_commit`: research 01 L11, L36 MATCH contract §2 L38, §2 L41-42, §6 L164. VERIFIED.
- `--depth deep` HARDCODED (not TCS): research 01 L121-124 MATCH contract §2 L45. VERIFIED.
- `reflect_post` written back by wrapper (leave room): research 01 L162 MATCHES contract §6 L174. VERIFIED.
- `start_commit` "never as diff base" REVERSAL flag: research 01 L192 correctly flags that live L2195 prose says `start_commit` is "never as the diff base" but contract §6 L164 makes the wrapper USE it as the base. Real reconciliation the builder must perform — correctly surfaced. VERIFIED (flag accurate).

**Note (non-defect):** Research 01 SURFACE 5 prose cites the A.11 banner POST line at "lines 1722-1724" while the summary table says line 1724 — a self-consistent range-vs-anchor reference, not a contradiction. Builder should grep `REFLECT GATES:` to anchor (outside the 4 mandated targets; not independently re-read).

**File 01 verdict: PASS** — all 4 mandated spot-checks exact; contract cross-checks consistent.

---

## File 02 — sc-tasklist edit surface — SPOT-CHECK RESULTS

Independently re-read live `sc-tasklist-protocol/SKILL.md` and `templates/phase-template.md`.

| # | Research 02 claim | Live source | Verdict |
|---|-------------------|-------------|---------|
| 1 | SKILL.md POST section L1036-1083; intro L1036-1038; spawn directive L1062-1064 | L1036 heading, L1038 intro, L1041 task heading `… Post-Execution Reflection: sc:reflect --mode post`, L1062-1064 spawn directive all byte-match | VERIFIED |
| 2 | Check #18 asserts heading prefix `### T<PP>.<NN> -- Post-Execution Reflection:` at L1169 | L1169 byte-match; #19 L1170, #20 L1171 exact | VERIFIED |
| 3 | Self-Check #6 = structural-list item 6 at L1129; no separate "Self-Check #6" | L1129 byte-match | VERIFIED |
| 4 | Check #5 "Every phase file starts with `# Phase N -- <Name>`" at L1128 (frontmatter-collision flag) | L1128 byte-match | VERIFIED |
| 5 | argument-hint `--no-reflect` at L9 (gating toggle, not the dial) | L9 byte-match | VERIFIED |
| 6 | "No YAML frontmatter today; phase file STARTS with `# Phase N`" (Surface 6 structural finding) | phase-template L1/L7/L12 confirm self-contained unit starting `# Phase N -- <Name>`; no frontmatter slot | VERIFIED |
| 7 | phase-template.md mirror L127-174; intro L127-129; spawn directive L153-155; Steps L158-159 | L127 heading, L129 mirror-note, L132 task heading, L154 spawn directive, L158 Step 1 all byte-match | VERIFIED |

**File 02 cross-check vs contract:**
- O2 shape `superclaude reflect run <abs> --depth deep --fix --no-promote --base <PHASE_N_START_SHA>`: research 02 L15-16 MATCH contract §2 L50, §5 L150. VERIFIED.
- `--no-promote` REQUIRED (no per-phase adapter): research 02 L16 MATCHES contract §5 L150-153. VERIFIED.
- `--base` SINGLE ref not range: research 02 L16, L271 MATCH contract §2 L53. VERIFIED.
- Range→base reconciliation: research 02 correctly flags that live L1067/L158 say "git RANGE" + L1063/L154 pass `--diff <phase-commit-range>`, but contract uses single `--base`. Real reconciliation, correctly surfaced. VERIFIED.
- check #18 heading-prefix FLAG: research 02 L224 correctly warns the rewrite must preserve `-- Post-Execution Reflection` prefix or update #18. Accurate and load-bearing. VERIFIED.
- check #5 frontmatter-collision FLAG (Surface 6 / summary row 9): research 02 correctly flags that prepending frontmatter for `executor_model_class` collides with check #5. Accurate. VERIFIED.

**Minor note (non-defect):** research 02 §4b summary uses "L1063, L154" for the two spawn-directive lines (SKILL + template) — both confirmed exact. No drift.

**File 02 verdict: PASS** — all 7 spot-checks exact; contract cross-checks consistent; the two structural FLAGS (#18 heading-prefix, #5 frontmatter collision) are real and correctly raised for the builder.

---

## File 03 — acceptance test + guard shape — SPOT-CHECK RESULTS

Independently re-read live `tests/cli/reflect/test_no_nesting_guard.py` (135 lines) and `cli/reflect/commands.py`.

| # | Research 03 claim | Live source | Verdict |
|---|-------------------|-------------|---------|
| 1 | Module constants L18-46; `_SKILL_SRC` L20, `_NESTING_TOKENS` L46 | L18-46 byte-match; `_SKILL_SRC` = task-builder/SKILL.md (the SRC, not `.claude/`) at L20; `_NESTING_TOKENS = ("Task(", "subagent_type")` at L46 | VERIFIED |
| 2 | `_extract_wrapper_branch` helper L49-60; stale marker `**Mode \`2\` / \`auto-resolved-2\` (§6.3, DEFAULT)…`; end anchor `**Mode \`halt\`` | L49-60 byte-match; marker L56, end anchor L59 exact | VERIFIED |
| 3 | xfail decorator L63-74 + test body L75-84; positive `superclaude reflect run` / `--depth`; negative `_NESTING_TOKENS` | L63-84 byte-match; `strict=False` at L73; asserts at L80-84 exact | VERIFIED |
| 4 | Lines 49-84 = Layer-A rewrite target; 87-134 = DO-NOT-MODIFY (Layer B 87-94; thinness 97-134) | L87-94 Layer B, L97-105 sprint/roadmap, L108-117 async/await, L120-134 apply_remediation — all match | VERIFIED |

**File 03 — CLI flag reality check (commands.py, independently read):**

| Flag asserted by proposed test | commands.py | Verdict |
|--------------------------------|-------------|---------|
| `--depth deep` | L101-106 `Choice(["standard","deep"])`, default `standard` → `deep` is a real choice | VERIFIED |
| `--fix` | L127-132 `--fix/--no-fix`, default `False`, help "gate default --fix" | VERIFIED |
| `--promote` | L89-94 `--promote/--no-promote`, default `True` | VERIFIED |
| `--no-promote` (O2) | L89-94 same option | VERIFIED |
| `--base` | L139-147 var `base_override`, "single ref vs working tree, highest precedence" | VERIFIED |
| `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` marker | L44 `_WRAPPER_MARKER_ENV`; L69 `.strip() == "1"` guard exits 0 | VERIFIED |
| `_BLOCKED_EXIT = 2` | L36 exact | VERIFIED |

Research 03 §6 cites these at `commands.py:101-106 / 127-132 / 89-94 / 139-147 / 44 / 69 / 36` — every line citation is ACCURATE.

**Non-defect nuance:** research 03 L346 states `--fix` Click default is `False` (correct, L130); research-notes L54 phrases it "default `--fix`". These are NOT contradictory — the Click flag defaults False, while the gate-emission convention (and the help string "gate default --fix") is to emit `--fix`. Both files are internally consistent. The proposed test asserts the literal token `--fix` is present in the emitted block, which is the correct check regardless of the Click default.

**File 03 verdict: PASS** — all 4 test spot-checks exact; all 7 CLI-flag/marker citations real and accurately line-numbered.

---

## CHECKLIST RESULTS

### Check 1 — Cross-file consistency (marker name + contract shapes)
**PASS.** The recursion-breaker marker `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` is identical across: contract §3 (L78), research 01 (L12, L35), research 02 (L17), research 03 (L208, L280), research-notes (L27-32), and live `commands.py:44`. The skip-guard one-liner (`if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo …; exit 0; fi`) is byte-identical across all three research files and the contract §3.2. O1 shape (`--depth deep --fix --promote`, `--base` omitted) and O2 shape (`--depth deep --fix --no-promote --base <SHA>`) agree across O1 file, O2 file, test file §4b, contract §2, and research-notes.

### Check 2 — Verbatim quotes & line numbers accurate (≥3 per file)
**PASS.** Spot-checked far more than 3 per file: File 01 = 4/4 anchors exact (L2193-2198, L2312, L1073-1076, L2137-2156). File 02 = 7/7 exact (L1036-1083, L1062-1064, L1169, L1129, L1128, L9, phase-template L127-174). File 03 = 4/4 test anchors + 7/7 commands.py citations exact. ZERO line-number drift, ZERO quote drift detected.

### Check 3 — Research-vs-contract contradictions (depth, promote scope, --base precedence)
**PASS — no contradictions.** Depth: all three files + notes agree POST is fixed `--depth deep` (contract §2 L45), TCS plumbing stays PRE-only. Promote: O1=`--promote` (contract §5 L149), O2=`--no-promote` REQUIRED (contract §5 L150) — research 01/02 match exactly. `--base` precedence: research 02 L262 states `--base` > frontmatter `start_commit` > `git merge-base HEAD master`, matching contract §6 L173 verbatim. The `start_commit` "never as diff base" reversal (research 01 L192) and the "git RANGE → single --base" reconciliation (research 02 L271) are correctly identified as builder reconciliations, NOT contradictions in the research.

### Check 4 — Test anchor (research 03) matches an anchor O1 block (research 01) can carry
**PASS WITH COORDINATION FLAG (non-blocking).** Research 03 §3a proposes the NEW extractor anchor `#### POST reflect gate (O1` heading and explicitly states (L170) "The exact heading text is an R1/R3 coordination point." Research 01's O1 surface (SURFACE 1, the N.{X-1} item replacement) does NOT currently specify that it will emit that exact heading — research 01 describes the replacement as a flat Bash shell-out item but stops short of committing to the literal `#### POST reflect gate (O1` heading string. This is a genuine coordination point the builder MUST reconcile: **the O1 emission (from file 01's surface) and the test extractor anchor (file 03) must agree on one literal heading/marker string.** Both research files flag this as a coordination requirement rather than asserting a settled value, so it is correctly surfaced — but the builder cannot treat either side as authoritative until it picks the literal anchor and emits it in BOTH the SKILL O1 block AND the test helper. Recorded as a reconciliation item below.

---

## RECONCILIATION ITEMS FOR THE BUILDER (not defects in research — surfaced design coordination)

1. **O1 anchor string (Check 4).** Pick ONE literal anchor (research 03 proposes `#### POST reflect gate (O1`). Emit it in the task-builder/SKILL.md O1 block (file 01 SURFACE 1) AND in `_extract_wrapper_branch` (file 03 §3b). They must be byte-identical or the test cannot slice the block.
2. **`start_commit` prose reversal (file 01 L192).** Live L2195 says `start_commit` is "never the diff base"; the wrapper now USES it as the base (contract §6). Remove/rewrite that prose when replacing SURFACE 1.
3. **O2 range→`--base` (file 02 L271).** Live L1067/L158 "git RANGE" + L1063/L154 `--diff <phase-commit-range>` must become single `--base <PHASE_N_START_SHA>` vs working tree.
4. **check #18 heading-prefix (file 02 L224).** Preserve `-- Post-Execution Reflection` prefix (drop only the `: sc:reflect --mode post` suffix) OR update check #18 at L1169.
5. **check #5 frontmatter collision (file 02 Surface 6 / row 9).** Phase files have NO frontmatter today and check #5 (L1128) asserts they START with `# Phase N`. If `executor_model_class` needs a per-phase frontmatter slot, check #5 must be amended; the canonical path (explicit `--base <sha>` on the gate line) sidesteps frontmatter for the SHA but NOT for `executor_model_class`.
6. **xfail decorator disposition (file 03 §3d).** Open question (keep `strict=False`→XPASS vs remove→PASS). Research-notes L96 sets default = keep `strict=False`→XPASS. Builder surfaces as non-blocking Open Question.

These six are correctly raised by the research as coordination/reconciliation points; none is a research defect.

---

## VERDICT: PASS

All three assigned research files (01, 02, 03) are CROSS-VALIDATED CLEAN:
- Every spot-checked verbatim block and line number matches the live source byte-for-byte (15/15 anchors + 7/7 commands.py citations — ZERO drift).
- All contract shapes (marker name, O1/O2 invocation, `--base` precedence, promote scope, exit codes, depth-fixed-deep) are mutually consistent across the three files, the contract, and the live CLI.
- No research-vs-contract contradictions.
- The one inter-file coordination point (Check 4 — the O1 block anchor that the test extractor must slice) is explicitly flagged BY BOTH research files as an R1/R3 coordination requirement, not silently assumed; it is recorded as Reconciliation Item 1 for the builder.

No gaps block task-file construction. The builder has accurate, surgically-actionable Edit targets.
