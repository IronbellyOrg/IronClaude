# QA Report — Research Depth (research-depth lens)

**Topic:** flat `superclaude reflect run` O1/O2 gate-wiring + skip guard + frontmatter + Layer-A test rewrite
**Date:** 2026-06-11
**Phase:** research-depth (adversarial)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Lens:** Is research DEEP enough to produce surgical, per-file checklist items WITHOUT the builder re-reading source?
**Assigned files:** 01-o1-taskbuilder-edit-surface.md, 02-o2-sctasklist-edit-surface.md, 03-acceptance-test-and-guard-shape.md (+ research-notes.md)

---

## Overall Verdict: PASS

The three assigned research files clear the depth bar decisively. They give the builder
verbatim current blocks with line anchors, precise replacement intent justified per contract
section, fully-mapped cross-cutting consequences (TCS/depth decoupling POST-only, check-#18
heading-prefix, check-#5 frontmatter collision, the L2195 `start_commit` prose reversal,
phase-file no-frontmatter), a concrete test rewrite (new helper + anchor + assertions), and
covered failure/verification modes (exit-code consumption, xfail→XPASS vs PASS, full reflect
suite + verify-sync). I independently verified every load-bearing factual claim against actual
source — line numbers, verbatim blocks, zero-hit token claims, and CLI flag surface all match.

---

## Confidence

Verified: 23/23 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement

Read: 5 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 4

Each Bash batch directly verified a specific cluster of research claims (O1 anchors, O1 remaining
surfaces, O2 anchors + test/CLI, line-count + contract existence). No padding calls.

---

## Items Reviewed (against the 6-point depth lens)

| # | Lens point | Result | Evidence |
|---|------------|--------|----------|
| 1 | Exact old→new Edits derivable (verbatim + intent)? | PASS | R1/R2/R3 quote every target block VERBATIM with line anchors; I re-grepped — L2194/2195/2312 (O1), L1041/1063/1067 (O2), L49-60/63-84 (test) match byte-for-byte. "What must change" prose states precise replacement intent, not "change the POST item". |
| 2 | Cross-cutting consequences understood? | PASS | TCS/depth decoupling scoped POST-only (R1 Surface 6: O4 L2356 + intro L2320 verified; PRE TCS apparatus explicitly preserved). check-#18 heading-prefix constraint (R2 4b, L1169 verified) + check-#5 frontmatter collision (R2 Surface 6, L1128 verified). L2195 `start_commit` "never as diff base" prose-reversal flagged for removal (verified present). Phase-file no-frontmatter confirmed (template starts `# Phase N`). |
| 3 | Contract→emission mapping concrete (each flag justified)? | PASS | R3 §6 maps every flag to commands.py line + contract §: `--depth deep` (L102-103 Choice), `--fix` (L128), `--promote/--no-promote` (L90), `--base` (L140), marker (L44), exit `2` (L36). All re-verified. O1=`--promote`, O2=`--no-promote --base <SHA>` justified per contract §2/§5. |
| 4 | Test rewrite specified to buildable detail? | PASS | R3 §3 supplies new `_extract_wrapper_branch` (heading-anchored), the exact anchor `#### POST reflect gate (O1` to be CARRIED by R1's O1 block (R1 Surface 1 confirms it emits a flat heading), new test body with literal asserts (`superclaude reflect run`, `--depth deep`, `--fix`, `--promote`, `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`, NFR-7 negatives via `_NESTING_TOKENS`). DO-NOT-MODIFY map (L18-46 constants, L87-134 siblings) verified — all 5 sibling fns present. |
| 5 | Failure/verification modes covered? | PASS | Exit-code consumption table quoted verbatim (R3 §4c, contract:72 "Only exit 0" verified); xfail→XPASS vs PASS dispositioned as Open Question with recommendation (R3 §3d); research-notes TEMPLATE_NOTES specifies full `tests/cli/reflect/` suite + `make verify-sync` + `ruff format --check`. |
| 6 | Any builder-guess gaps? | PASS (with 2 surfaced DECISIONS, not gaps) | The two residual choices are EXPLICITLY surfaced as Open Questions with recommendations + tradeoffs, not silent gaps: (a) xfail decorator keep-vs-remove; (b) O2 `executor_model_class` persistence mechanism (prepended frontmatter collides with check-#5 vs alternative). Both are genuine design forks the builder must route to the user, correctly flagged rather than guessed. |

---

## Summary
- Checks passed: 23 / 23 (6 lens points + 17 underlying factual verifications)
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (documented below — non-blocking)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 03-acceptance-test §1 / §5 | R3 states the test file is "135 lines total" and md5-tabulates it; actual `wc -l` is 134 (trailing-newline counting nuance — last test fully present through L134). Does NOT affect any line anchor (helper L49-60, rewrite scope L49-84, siblings L87/97/108/120 all independently verified accurate). | None required for the build. The builder writes exact-string Edits, so the off-by-one line count is inert. Cosmetic. |

## Independent Verification Performed (adversarial — assumed surface until proven deep)

I re-grepped/sed-confirmed every load-bearing claim rather than trusting the research prose:

- **O1 anchors (task-builder/SKILL.md):** L2194 Context, L2195 Action (the long subagent string),
  L2312 Rule 20, L1073-1076 A.9 block, L1722-1724 banner, L2253 validation checklist, L2356 O4,
  L2320 TCS intro, L2137-2156 frontmatter template, L2191 final-phase header, L2200 update-status
  item — ALL match verbatim.
- **O1 zero-hit claims:** `superclaude reflect run` (0), `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` (0),
  `executor_model_class` (0), `start_commit` (1, only L2195) — confirmed. These are the "must be
  INTRODUCED/ADDED" claims; their absence is the precondition the build depends on.
- **O2 anchors (sc-tasklist-protocol):** L1041 heading, L1063 spawn directive, L1067 Step 1,
  L1169-1171 structural checks #18/#19/#20, L1128 check #5, L9 argument-hint — ALL match. New
  tokens (`superclaude reflect run`/marker/`start_commit`/`executor_model_class`/`--base`/`no-promote`)
  all 0 hits. Phase-template confirmed to START with `# Phase N` (no frontmatter) — the check-#5
  collision flag is real.
- **Test (R3):** helper L49-60, xfail L63-74, body L75-84, `_NESTING_TOKENS` L46, all 5 sibling
  functions present (L87/97/108/120 + helper L49). Stale Mode-2 marker present as claimed.
- **CLI (commands.py):** `--depth` Choice `["standard","deep"]` L103, `--fix/--no-fix` L128,
  `--promote/--no-promote` L90, `--base` L140, `_WRAPPER_MARKER_ENV` L44, truthiness `== "1"` L69,
  `_BLOCKED_EXIT = 2` L36 — every R3 §6 citation exact.
- **Contract:** file exists at the cited reflectWrapper handoff path; O1 line at contract:38,
  "Only exit 0" at :72, skip-guard at :101, O1-gate checklist at :192 — all confirm R3 §4 verbatim
  quotes.

## Self-Audit

**(a) Reliance list — items I relied on rather than re-deriving:**
- Relied on the research's contract-section citations (§2/§3.2/§5/§6) for INTENT — but independently
  confirmed the contract file exists and the four most load-bearing lines (:38, :72, :101, :192).

**(b) Independent semantic checks (≥1 required):**
- Verified the depth-decoupling claim is SEMANTICALLY correct, not just present: O4 (L2356) and the
  TCS intro (L2320) really do couple the POST item to TCS today, so R1's "decouple POST-only, keep
  PRE TCS" is a true reading of current source. Tool evidence: Bash sed L2320 + L2356.
- Verified the check-#5 collision is REAL (not speculative): phase-template L11-17 starts with
  `# Phase N`, and check #5 (L1128) literally asserts "starts with `# Phase N`", so prepending
  frontmatter would collide. The kind of cross-cutting consequence a surface inventory would miss;
  R2 caught it. Tool evidence: Bash sed L1128 + phase-template L11-17.
- Verified the `start_commit` prose-reversal: L2195 literally says "`start_commit` ... never as the
  diff base", while the contract (verified :192 + research-notes §6) makes the wrapper USE
  `start_commit` as the base — a genuine reversal the builder must delete, correctly flagged.

## Recommendations
- PASS the research-depth gate. The builder can write surgical old_string→new_string Edits for all
  three files without RE-RESEARCHING the anchors (normal Edit-time freshness Read still applies).
- Carry the two surfaced Open Questions into the generated task as `needs_human_decision` items per
  memory `feedback_human_decision_items_must_halt`: (a) xfail keep/remove; (b) O2
  `executor_model_class` persistence mechanism. Neither should auto-default to a shipped change.
- Builder must honor the R1/R3 coordination point: R1's O1 emission MUST carry the exact heading
  prefix `#### POST reflect gate (O1` that R3's new `_extract_wrapper_branch` anchors on. This is the
  single tightest inter-surface coupling; flag it as a cross-phase dependency (P2 O1 ↔ P4 test).

## QA Complete
