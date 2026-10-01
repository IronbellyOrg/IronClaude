# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** flat `superclaude reflect run` O1/O2 gate-wiring + skip guard + frontmatter + Layer-A test rewrite (Option A)
**Date:** 2026-06-11
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false

---

## Status: COMPLETE — VERDICT: PASS

## Files in scope (read)
- research/01-o1-taskbuilder-edit-surface.md (217 lines) — READ
- research/02-o2-sctasklist-edit-surface.md (364 lines) — READ
- research/03-acceptance-test-and-guard-shape.md (385 lines) — READ
- research-notes.md (at task root, not in research/) (97 lines) — READ
- contract: reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md (200 lines) — READ

## Note on contract location
Research cites the contract at `reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md`.
A SECOND copy exists at `ReflectGateWiring/.dev/handoffs/reflect-wrapper-contract.md` (this worktree).
Need to confirm they agree (drift risk if research quoted the wrong copy). — PENDING

## Spot-check of cited file:line anchors — COMPLETE

I opened the real source files and compared verbatim quotes + line numbers. Far exceeds
the 25% spot-check floor: 20+ distinct anchors verified across all 3 research files +
contract + CLI.

### R1 (01-o1-taskbuilder-edit-surface.md) — task-builder/SKILL.md
| Cited anchor | Claim | Verified result |
|---|---|---|
| L2193-2198 | POST item template N.{X-1} verbatim block | EXACT MATCH (incl. full Action prose) |
| L2200-2205 | `N.X — Update task status to Done` item | EXACT MATCH (anti-orphaning context true) |
| L2312 | Critical Rule 20 verbatim | EXACT MATCH |
| L1073-1076 | A.9 `POST_REFLECT_GATE: ENABLED` block | EXACT MATCH |
| L2137-2156 | generated frontmatter template | EXACT MATCH (confirms NONE of start_commit/executor_model_class/reflect_post present) |
| L2253 | validation-checklist SELF-RUN line | EXACT MATCH |
| L1722-1724 | A.11 banner REFLECT GATES block | EXACT MATCH |
| L2318/L2320 | Reflect Depth header + intro sentence | EXACT MATCH ("PRE … and the templated POST item both derive … `--depth` from … TCS") |
| L2356 | O4 POST-gate depth floor verbatim | EXACT MATCH |
| ZERO-occ: `superclaude reflect run` | absent | CONFIRMED grep -c = 0 |
| ZERO-occ: `executor_model_class` | absent | CONFIRMED = 0 |
| ZERO-occ: `SUPERCLAUDE_REFLECT_WRAPPER` | absent | CONFIRMED = 0 |
| `start_commit` only at L2195 | 1 occurrence, in POST Action prose | CONFIRMED grep -c = 1, at L2195 |

### R2 (02-o2-sctasklist-edit-surface.md) — sc-tasklist SKILL.md + phase-template.md
| Cited anchor | Claim | Verified result |
|---|---|---|
| SKILL L1036-1083 | POST intro prose + fenced template (heading, spawn directive, steps, AC) | EXACT MATCH |
| SKILL L1041 | heading `… Post-Execution Reflection: sc:reflect --mode post` | EXACT MATCH |
| SKILL L1062-1064 | spawn directive `/sc:reflect --mode post --remediate …` | EXACT MATCH |
| SKILL L1169-1171 | structural checks #18/#19/#20 | EXACT MATCH (incl. #18 heading-prefix assertion) |
| SKILL L9 | argument-hint `[--no-reflect]` | EXACT MATCH |
| phase-template L132 | mirror heading | EXACT MATCH (mirror confirmed) |
| ZERO-occ (ST): superclaude reflect run / start_commit / executor_model_class / --no-promote / --base / SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE | all absent | CONFIRMED all = 0 |
| No `--reflect` value-dial in ST (Surface 5) | abandoned dial never present | CONFIRMED grep `--reflect[ =<]` → 0 hits |

### R3 (03-acceptance-test-and-guard-shape.md) — test + commands.py + contract
| Cited anchor | Claim | Verified result |
|---|---|---|
| test L49-60 | `_extract_wrapper_branch` w/ stale Mode-2 marker | EXACT MATCH |
| test L63-84 | xfail decorator + test body | EXACT MATCH |
| commands.py:44 | `_WRAPPER_MARKER_ENV = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` | EXACT MATCH |
| commands.py:36 | `_BLOCKED_EXIT = 2` | EXACT MATCH |
| commands.py:69 | truthiness `.strip() == "1"` | EXACT MATCH |
| commands.py:71 | echo "reflect-wrapper recursion breaker: nested gate suppressed" | EXACT MATCH (skip-guard text matches CLI verbatim) |
| commands.py:101-106 | `--depth` Choice(standard,deep) default standard | EXACT MATCH |
| commands.py:127-132 | `--fix/--no-fix` default False | EXACT MATCH |
| commands.py:89-94 | `--promote/--no-promote` default True | EXACT MATCH |
| commands.py:139-147 | `--base` base_override default None | EXACT MATCH |
| commands.py:235 | `exit_code = result.verdict.exit_code` | EXACT MATCH |
| contract §2 L37-39 (O1) | `superclaude reflect run <ABS> --depth deep --fix --promote` | EXACT MATCH |
| contract §3.2 L99-104 (skip guard) | full bash block | EXACT MATCH |
| contract §2 L65-73 (exit table) | 0/10/11/2 table | EXACT MATCH |
| contract dial-abandoned (cited "line 16") | "`--reflect` dial is ABANDONED (PR #157 closed)" | EXACT MATCH (spans L15-16) |
| md5 ReflectGateWiring + reflectWrapper | `124549e6…` byte-identical | CONFIRMED both = 124549e67dd25258c7739371b4a89cb2 |
| md5 wrapper-onto-master | `9017231d…` stale | CONFIRMED = 9017231d8ff5c59ac0b6e879310c34a7 |

### Contract-copy drift check (my own addition, not in research)
Two on-disk copies of the contract exist:
- `reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md` (research cites this one)
- `ReflectGateWiring/.dev/handoffs/reflect-wrapper-contract.md` (this worktree)
`diff` → **IDENTICAL**. No drift risk. Either path is authoritative-equivalent.

---

## LENS-focus findings (evidence-quality)

1. **Claims evidence-based?** YES. Every surface in R1/R2/R3 carries a file:line anchor +
   verbatim fenced block. Contract shapes carry contract line numbers. CLI flags carry
   commands.py line numbers. This is dense evidence (>95% evidenced), not prose assertion.

2. **Spot-check drift?** ZERO drift on content. Every verbatim block I opened matched
   byte-for-byte. Line numbers were accurate at every anchor checked.

3. **Unsupported assertions stated as fact?** None material. The "frontmatter has no
   start_commit/executor_model_class/reflect_post" assertion (R1 Surface 7) is VERIFIED true
   (template read + grep). The "no `--reflect` dial anywhere" assertion (R2 Surface 5) is
   VERIFIED true.

4. **Contract shapes quoted correctly?** YES — O1/O2 flag strings, skip-guard text, and the
   0/10/11/2 exit table all match the contract AND the live CLI (`commands.py`) verbatim. The
   skip-guard echo string even matches `commands.py:71` exactly, so the SKILL emission will be
   self-consistent with the wrapper.

5. **Any research grounded in the ABANDONED dial taxonomy?** NO. All three files correctly
   treat `Mode 2 / auto-resolved-2 / §6.3` as the stale/abandoned markers to be REMOVED
   (R3 §1b/§3a explicitly; R1/R2 never invoke the dial as a target shape). grep for
   revive/reinstate/restore-dial → 0 hits. LENS #5 PASSES.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | R3 §1 line 24 ("135 lines total") and §5 table | Test file is 134 lines per `wc -l` (134 newlines; likely no trailing newline on last line). Off-by-one. | Cosmetic — does not affect any edit. The in-scope range "lines 49-84" is correct regardless. No builder action needed; note only. |
| 2 | MINOR | research-notes.md L54 | research-notes summary says `--fix/--no-fix (default --fix)` but commands.py:130 is `default=False`. R3 §6 (the authoritative researcher file) CORRECTLY states default `False`. The notes line is a loose paraphrase. | Builder should follow R3 §6 (default False); O1/O2 emit explicit `--fix` regardless, so default value is moot for emission. No correctness impact. |

Both issues are MINOR and do NOT block the builder. No CRITICAL or IMPORTANT issues.

---

## Cross-file consistency (within assigned subset)

- R1 ↔ R3 coordination point: R3 §3a proposes the new anchor heading `#### POST reflect gate (O1`
  for `_extract_wrapper_branch`, and flags it as an R1/R3 coordination point. R1 Surface 1 does
  NOT yet name a specific new heading string. This is correctly surfaced as an OPEN coordination
  item in R3, not a contradiction — the builder must ensure R1's emitted heading matches R3's
  anchor. **Recommend the task file pin one exact heading string used by BOTH the emission and
  the test extractor.** (Forward-looking note for builder; not a research defect.)
- R2 ↔ contract: R2's O2 line (`--no-promote --base <sha>`) matches contract §2 L50 + §5 exactly.
- R3 xfail disposition is correctly flagged as an OPEN QUESTION (keep strict=False→XPASS vs
  remove→PASS), consistent with research-notes §AMBIGUITIES_FOR_USER. No premature decision.

[PARTITION NOTE: I was assigned all 3 research files + research-notes, so cross-file checks span
the full set — no partition limitation applies.]

---

## Confidence Gate

Checklist items for research-gate evidence-quality lens (the 5 LENS questions + evidence-density
+ scope + no-fabrication + contradiction + dial-taxonomy):

- [x] Evidence-based claims (file:line + verbatim) — VERIFIED (20+ anchors opened)
- [x] ≥25% spot-check by opening real source — VERIFIED (far exceeded; ~20 anchors)
- [x] No unsupported assertions as fact — VERIFIED (frontmatter-absence + no-dial both grep-confirmed)
- [x] Contract shapes quoted correctly — VERIFIED (O1/O2/guard/exit-table vs contract + CLI)
- [x] No dial-taxonomy-grounded recommendation — VERIFIED (grep + read)
- [x] Contract-copy drift — VERIFIED (diff IDENTICAL)
- [x] ZERO-occurrence claims — VERIFIED (grep -c on all to-be-ADDED tokens)
- [x] md5 / byte-identical copy claims — VERIFIED (md5sum)
- [x] Cross-file contradictions — VERIFIED none (R1/R2/R3 mutually consistent + consistent w/ contract)

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 14 | Grep: 0 (folded into Bash grep -c) | Glob: 0 | Bash: 3
(Tool-call count 17 ≥ 9 checklist items — engagement floor satisfied. Each Read targeted a
specific cited anchor; each Bash verified a specific grep/diff/md5 claim. No padding.)

No web research performed (all claims were source-truth-local; no external URL/standard/API to verify).

---

## Overall Verdict: PASS

The research is evidence-dense, accurate, and internally consistent. Every spot-checked file:line
anchor matched verbatim with correct line numbers. Contract shapes (O1/O2 flags, skip-guard text,
exit-code table) are quoted correctly against BOTH the contract file and the live CLI. No claim is
grounded in the abandoned dial taxonomy. The two MINOR issues (134-vs-135 line count; a loose
`default --fix` paraphrase in research-notes that R3 itself corrects) do not affect any edit and do
not block the builder.

**Green light for the builder.** One forward-looking coordination note (not a defect): the task file
should pin ONE exact heading string shared by R1's O1 emission and R3's `_extract_wrapper_branch`
anchor, since R3 flagged this as an open R1/R3 coordination point.

## QA Complete
