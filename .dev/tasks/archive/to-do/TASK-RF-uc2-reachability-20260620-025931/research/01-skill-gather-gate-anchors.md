# Research: SKILL.md Gather+Gate Anchors

Topic type: File Inventory / Patterns — SKILL.md GATHER + GATE sites
Scope: src/superclaude/skills/sc-reflect-protocol/SKILL.md (1854 lines)
Status: Complete
Date: 2026-06-20
File under audit: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (1854 lines, verified via `wc -l`)

---

## Site 1 — §5.3 Tier-1 STOP decision table (FIRST-MATCH-WINS)

Header: SKILL.md:386 `### 5.3 Decision logic (applied in order; first match wins)`
Table header rows: SKILL.md:388-389
Rows (verified verbatim):

- **Row 1 (confident-PASS STOP)** — SKILL.md:390
  `| 1 | C ≥ 0.90 AND S_scope ≤ 5 files AND S_domains == 1 AND S_dev_density ≤ 0.05 AND coverage_pct ≥ <coverage-floor> AND NOT coverage_undefined AND NOT coverage_degraded | **STOP at T1** — high confidence, narrow scope, single domain, near-zero ambiguity |`
  This is THE row FR-RSR targets: `surface_unreached` becomes a new table-wide pre-filter that, like `coverage_degraded`, forbids this STOP.
- **Row 2 (medium STOP)** — SKILL.md:391 (`C ≥ 0.85 ... NOT coverage_degraded` → STOP at T1 with WARN if S_dev_density > 0.05)
- **Row 3 (Regression ESCALATE)** — SKILL.md:392 `| 3 | UC-2 AND any single hunk classified as Regression candidate by Wave 1 | **ESCALATE** ... |`
- **Row 3a (Reuse-Miss ESCALATE)** — SKILL.md:393 `| 3a | UC-2 AND a Reuse-Miss at rung L3 mapped to Drift or Regression (§10.8) | **ESCALATE** ... |`
  → 3a is the structural sibling pattern FR-RSR's escalate row most resembles (a separately-numbered ESCALATE row inserted after row 3).
- Rows 4-7 (ESCALATE conditions) — SKILL.md:394-397 (S_domains ≥ 3; S_dev_density > 0.20; C < 0.85; --strategy enterprise)
- **Row 8 (Default STOP)** — SKILL.md:398 `| 8 | Default | STOP at T1 |`

Coverage-floor note: SKILL.md:400 (`Default <coverage-floor> is 0.90`).

NOTE re STOP-row inventory: The forbid-STOP pre-filter (Site 2) explicitly names STOP rows as **"1, 2, or the row-8 default"** (SKILL.md:402). FR-RSR.5's `surface_unreached` must forbid exactly that same set of STOP rows.

---

## Site 2 — Table-wide forbid-STOP **pre-filter precedence paragraph** (the shape FR-RSR.5 mirrors)

Location: SKILL.md:402 (single paragraph, bold lead-in **"Pre-filter precedence (D13)."**).

Verbatim wording:
> **Pre-filter precedence (D13).** `coverage_undefined` and `coverage_degraded` are TABLE-WIDE pre-filters, not row conjuncts alone: when either flag is set, NO STOP row (1, 2, or the row-8 default) may fire and the run routes to Tier 2; the row-1/row-2 conjuncts are redundant safeties, the pre-filter is authoritative. Explicit user pins outrank the pre-filter: `--tier 1`, `--depth quick`, and `--no-escalate` (all §5.1) proceed at the pinned tier and emit a loud WARN naming the overridden flag; the §5.1 calibrator-failure row also proceeds at T1 but already forces `status: partial` with a re-run recommendation, and its WARN names the degraded flag too. The coverage-floor comparison in row 1 reads `coverage_pct` (parsed semantics, §9.1).

EXACT MIRROR TEMPLATE for FR-RSR.5: this is the precedence sentence `surface_unreached` joins as a third TABLE-WIDE pre-filter alongside `coverage_undefined` / `coverage_degraded`. The "Explicit user pins outrank the pre-filter (`--tier 1`, `--depth quick`, `--no-escalate`)" clause is the user-override carve-out FR-RSR.5 inherits unchanged.

Companion in-table conjunct sites (where `NOT coverage_degraded` already appears as a redundant safety): Row 1 SKILL.md:390, Row 2 SKILL.md:391. If FR-RSR adds a redundant `NOT surface_unreached` row-conjunct (matching the existing pattern), these are the two insertion points; the authoritative gate remains the §5.3:402 pre-filter paragraph.

---

## Site 3 — §5.4 `tier_decision.yaml` forced-T2 reason recording

Header: SKILL.md:404 `### 5.4 tier_decision.yaml audit artifact (composite-score recording)`
Artifact path cited: `<output>/artifacts/tier_decision.yaml` (SKILL.md:406).
YAML block: SKILL.md:408-420.

Key field for FR-RSR.5 (the line `surface_unreached` reason joins/mirrors):

- SKILL.md:411 `coverage_degraded: <string> | null # "parsed-sparse" when the Step 1B.2b guard fired (D13); table-wide pre-filter, explains a forced T2 regardless of which STOP row would have fired`

FR-RSR.5 adds a sibling field here (e.g. `surface_unreached: <bool|string> | null`) recording WHY a forced-T2 happened. Other existing fields: `selected_tier` (409), `fired_rule_number` (410), `composite_score` (412), `per_signal_breakdown` (413-418), `escalation_reason` (419).
Grader note: SKILL.md:422 — grader `yaml_field` asserts `fired_rule_number` and `composite_score` present; "The composite is *recording*, not deciding." (relevant: new field is recording, gate decision lives in §5.3).

---

## Site 4 — §6.1 Wave-1A grounding chain (insertion points for steps 4b' tagger / 4b sweep)

Header: SKILL.md:453 `### 6.1 Mandatory evidence-gathering chain (Wave 1A)`
Scope line: SKILL.md:455 ("For every touched file in UC-2, or every spec-referenced module in UC-1").
Numbered chain code block: SKILL.md:457-478.

Existing steps (verbatim line anchors):

- Step 1 activate_project — SKILL.md:458
- Step 2 get_symbols_overview — SKILL.md:459
- Step 2a find_declaration — SKILL.md:460
- Step 3 find_symbol — SKILL.md:461
- Step 3b find_implementations — SKILL.md:462
- **Step 4 find_referencing_symbols** — SKILL.md:463
  Verbatim: `4. mcp__serena__find_referencing_symbols <symbol> include_info:true   # downstream impact + signatures`
  This is the EXACT step the TDD says steps **4b' (tagger)** and **4b (sweep)** insert around. Current framing comment = `# downstream impact + signatures`.
- Step 4a Task(reuse-auditor...) — SKILL.md:464-471 (the existing outward-reuse sub-step that ALREADY sits right after step 4)
- Step 4.5 type_hierarchy — SKILL.md:472
- Step 5 get_diagnostics_for_file — SKILL.md:473
- Step 5.5 execute_shell_command (verification triangle) — SKILL.md:474
- Step 6 Re-Read cited file:line — SKILL.md:475
- Step 7 find_symbol search_deps — SKILL.md:476
- Step 7' summarize_changes — SKILL.md:477
- Closing fence — SKILL.md:478

INSERTION POINTS for FR-RSR new steps 4b'/4b: between step 4 (SKILL.md:463) and the existing step 4a (SKILL.md:464). The driving TDD's approximate anchor for "step 4" matches the CURRENT step 4 at SKILL.md:463 (NO drift — TDD-cited "around step 4" = verified line 463). Note the chain already contains a `4a` sub-step (reuse-auditor) — the new tagger/sweep steps `4b'`/`4b` slot AFTER step 4's referencing call and must be numbered to coexist with the existing `4a`; verify ordering against §6.1:464 when authoring.

Per-step prose paragraphs that follow the block (where a new 4b'/4b prose paragraph would be added, matching the existing pattern):

- Step 2a/3b prose — SKILL.md:480
- Step 4 include_info prose (FR-3) — SKILL.md:482 (`Step 4's include_info: true ... is a parameter add to the existing call`)
- Step 7 prose — SKILL.md:484
- Step 7' prose — SKILL.md:486
- Step 4.5 prose — SKILL.md:488
- Step 5.5 prose — SKILL.md:490
- Step 4a (reuse) prose — SKILL.md:492
- Chain-replaces-think_about closing — SKILL.md:494

---

## Site 5 — §6.1.1 verification triangle (`execute_shell_command`) — UNTOUCHED by FR-RSR

Header: SKILL.md:496 `### 6.1.1 execute_shell_command safety envelope (FR-RV3-MED.4)`
Body begins SKILL.md:498 ("`execute_shell_command` runs **non-mutating verification only**... All nine controls are mandatory:"). The structural-metachar control (c) is at SKILL.md:502.
CONFIRMED present and is OUT OF SCOPE for FR-RSR: the reachability sweep (steps 4b'/4b) adds NO shell execution — it is a static serena symbol/reference walk (tagger + find_referencing_symbols sweep). §6.1.1's safety envelope and its nine controls are untouched.

---

## Site 6 — §6.5 fail-open policy (FR-RSR.8 inherits this)

Header: SKILL.md:563 `### 6.5 Fail-open policy`
Body: SKILL.md:565 (verbatim):
> Every Serena call is fail-open per `sc-validate-roadmap-protocol` convention. Missing Serena → fall back to `Grep`/`Glob` with `degraded: true` in the audit. **The protocol must never abort because Serena is unavailable.**

FR-RSR.8 inherits this: the reachability sweep (a Serena `find_referencing_symbols` walk) must fail-open — Serena unavailable ⇒ `degraded_components` entry + skip, NEVER STOP. The sweep also must NOT set `surface_unreached` from a degraded/unavailable walk (would falsely force-T2); FR-RSR.8 should gate the pre-filter on a SUCCESSFUL sweep, mirroring how §6.1:484/488/490 distinguish "expected absence / unavailable → no degrade-forced-escalation" from genuine signal.

---

## Site 7 — §4 per-step `audit.log` row convention (each new Wave-1A step emits one row)

Header/anchor: SKILL.md:127 (bold lead-in **"Per-step audit emit convention."**, under `## 4. Wave / Tier Architecture` at SKILL.md:125).
Verbatim row shape:
> Every numbered step within every wave emits one row to `<output>/audit.log` with shape: `{wave: <N>, step: <M>, timestamp: <ISO-8601>, outcome: ok|warn|fail|skip, evidence_ref: <path-or-null>}`.

Every new Wave-1A step (4b' tagger, 4b sweep) MUST emit one such row. This convention is referenced throughout §6.1 (e.g. "emits one `audit.log` row per the §4 per-step convention" at SKILL.md:480, 484, 490, 492). The Wave-1A wave number = 1 (chain titled "Wave 1A", SKILL.md:453); step numbers 4b'/4b.

---

## Summary (R1 — gather+gate anchors)

All 7 sites verified against the CURRENT 1854-line SKILL.md. Re-anchor results:

| Site | Section | CURRENT line(s) | Notes vs TDD |
|------|---------|-----------------|--------------|
| 1 | §5.3 STOP table | header 386; rows 390(r1),391(r2),392(r3),393(r3a),398(r8) | first-match-wins; row1 = confident-PASS STOP target |
| 2 | forbid-STOP pre-filter paragraph | 402 | exact shape FR-RSR.5 mirrors; names STOP rows "1, 2, or row-8 default" |
| 3 | §5.4 tier_decision.yaml | header 404; coverage_degraded reason field 411 | `surface_unreached` reason added as sibling here |
| 4 | §6.1 Wave-1A chain | header 453; **step 4 = line 463**; insertion gap 463→464 | TDD "around step 4" verified = line 463; chain already has a 4a |
| 5 | §6.1.1 verification triangle | header 496; body 498 | UNTOUCHED — sweep adds no shell exec |
| 6 | §6.5 fail-open | header 563; body 565 | FR-RSR.8 inherits "never abort because Serena unavailable" |
| 7 | §4 per-step audit.log | 127 (under §4 @125) | new 4b'/4b steps each emit {wave,step,timestamp,outcome,evidence_ref} |

Key callouts for the task builder:
1. The authoritative gate is the §5.3:402 pre-filter paragraph (NOT the row conjuncts) — FR-RSR.5 amends line 402 to add `surface_unreached` as a third table-wide pre-filter alongside `coverage_undefined`/`coverage_degraded`.
2. Redundant in-row `NOT surface_unreached` conjuncts (optional, matching existing `NOT coverage_degraded`) go on rows 1 (390) and 2 (391).
3. Wave-1A new steps insert AFTER step 4 (463) and must coexist with the existing reuse-auditor 4a (464) — number carefully (4b'/4b).
4. The user-override carve-out (`--tier 1`/`--depth quick`/`--no-escalate` outrank the pre-filter) at line 402 is inherited verbatim by FR-RSR.5.
5. No line-number drift detected between TDD approximate anchors and the verified CURRENT file for the step-4 insertion site.
