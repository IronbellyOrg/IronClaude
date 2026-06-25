# Research Completeness Verification

**Topic:** Build MDTM task for `reflect-in-task-builder.md` + `reflect-in-sc-tasklist.md` (incl. S4 token-set trim) against `src/superclaude/`, then `make sync-dev`
**Date:** 2026-06-04
**Files analyzed:** 6 research files (01–06) + research-notes.md (scope context)
**Depth tier:** Deep
**Analyst:** rf-analyst (single instance — no team context)

---

## Verdict: PENDING (appended below after spot-checks + checklist)

---

## Methodology

- Read all 6 assigned research files in full + research-notes.md.
- Spot-checked load-bearing claims against the REAL source files (re-Read this session), per the spawn instruction to verify a sample of cited line anchors.
- Adversarial stance: assume the research has gaps; verify counts; surface contradictions.

(Sections appended incrementally below.)

---

## Spot-Check Results (5 load-bearing claims verified against real source)

The spawn prompt directed me to spot-check 2–3 cited anchors. I checked **5** of the highest-stakes ones. All 5 verified clean — the research's line anchors are re-verified and current, not drifted.

| # | Claim (research file) | Verified against | Result |
|---|-----------------------|------------------|--------|
| SC-1 | **A.10.7 CRITICAL DRIFT** (R1): a NEW `### A.10.6: DM-005 Phase Contract` now sits between A.10.5 and A.11 (1339–1396); PRE gate inserts at L1397, NOT "between A.10.5 and A.11" as proposal claims | `task-builder/SKILL.md` 1335–1404 | ✅ EXACT. A.10.6 @1339; ends L1396 ("Future consumers of `schema_version: 1.0.0`…"); A.11 @1398. Insertion L1397 confirmed. This is the single most important drift catch in the whole research set. |
| SC-2 | **4 checkpoint invariants** (R2): #6 @1073, #18 @1113, #19 @1114, #20 @1115; close-line "check 1-20" @1117; #6 cross-refs "checks 18-20" | `sc-tasklist-protocol/SKILL.md` 1071–1118 | ✅ EXACT, all four verbatim. #6 @1073 literally reads "(per checks 18-20)"; close-line @1117 "If any check 1-20 fails". Zero drift. |
| SC-3 | **S4 trim grep** (R1): only `after Phase` at L1993 (Content-Rules cell); `TCS`/`blockedBy`/`depends_on`/`after N.` = 0 hits | `grep` on `task-builder/SKILL.md` | ✅ EXACT. Single hit L1993; all other tokens 0. Confirms S4 set is new content w/ no existing-anchor collision. |
| SC-4 | **Test break-risk** (R4): rf-qa.md `#### Checklist (28 items)` @298; merge test literal @69+@190; INV-010 `MIN_LIVE_K=8` @88, floor `k1 >= MIN_LIVE_K` @381, density `range(1, len(ns)+1)` @391 | `rf-qa.md`, `test_task_builder_merge.py`, `test_dynamic_enumeration_inv_010.py` | ✅ EXACT. All literals + assertions present at cited lines. R4's "validation-checklist path = NONE break / TB-Add-9 path = HIGH (28→29)" classification is sound. |
| SC-5 | **Critical Rules numbering** (R1/R5): highest rule = 18 @2034; #16 @2030; Precedence @2036; `---` @2038; `## Research Quality Signals` @2040; TCS section inserts L2039 | `task-builder/SKILL.md` 2028–2040 | ✅ EXACT. Rule 16 @2030, 17 @2032, 18 @2034 verbatim, Precedence @2036, section close @2038/2040. New rule #19 + TCS section @2039 confirmed. |

**File-length cross-check:** `wc -l` → task-builder=**2190**, sc-tasklist=**1491**, command=**118**. Matches every research file's stated length exactly (R1 even flags the proposal's off-by-one "2191" vs actual 2190 — evidence-integrity diligence).

**Spot-check verdict:** The research line anchors are genuinely re-verified and current. Confidence in the un-checked anchors is correspondingly high.

---

## Coverage Audit (edit surface vs research)

Every edit site named in the spawn prompt's build-surface enumeration, mapped to the research that covers it with a CURRENT anchor.

### Proposal 1 — task-builder/SKILL.md (R1)

| Edit surface (spawn prompt) | Covered by | Current anchor | Status |
|-----------------------------|-----------|----------------|--------|
| A.10.7 insert point | R1 edit-site 3 | L1397 (after A.10.6 @1396, before A.11 @1398) | COVERED ✅ (spot-checked) |
| BUILD_REQUEST POST_REFLECT_GATE | R1 edit-site 5 | L848 (after EXECUTION_CONTEXT_REQUIREMENTS 827–847, before STALENESS @849) | COVERED |
| Critical Rule # | R1 edit-site 6 + R5 §2.2 | new #19 after L2034 | COVERED ✅ (spot-checked) |
| Output Structure (frontmatter + Phase-N item) | R1 edit-site 7a/7b | frontmatter 1866–1885 (after L1878); Phase-N item between L1929–L1930 (penultimate) | COVERED |
| Validation checklist | R1 edit-site 8 | new TB-Add-9 after L1979 (+ rf-qa.md cross-edit hazard flagged) | COVERED |
| A.11 | R1 edit-site 9a/9b | single-track after L1417; multi-track after L1446 & L1451 | COVERED |
| TCS section home | R1 edit-site 10 | L2039 (between Critical Rules end @2038 and Research Quality Signals @2040) | COVERED ✅ (spot-checked) |
| S4 trim | R1 edit-site 11 | new content, 0 collisions | COVERED ✅ (spot-checked) |
| `--spec` input surface | R1 edit-site 1 | new item 5 after L39 (Input is prose list, NO flag table) | COVERED |
| A.2 spec_path resolution | R1 edit-site 2 | after L197 | COVERED |
| Pipeline-overview steps 12/13 | R1 edit-site 4 | between L160 & L161 | COVERED |

### Proposal 2 — sc-tasklist-protocol/SKILL.md (R2) + command (R3) + templates (R3)

| Edit surface (spawn prompt) | Covered by | Current anchor | Status |
|-----------------------------|-----------|----------------|--------|
| Stage 10.5 | R2 edit-site 1 | between L1386 (gate) and L1388 (`---`) | COVERED |
| Stage 5 emission | R2 edit-site 3 | contract @91/96 + emit-after L1027 (NO `### Stage 5` heading — clarified) | COVERED |
| 4 checkpoint invariants | R2 edit-site 4 | #6@1073, #18@1113, #19@1114, #20@1115 | COVERED ✅ (spot-checked) |
| 10→11 stage table | R2 edit-site 2 | table 1394–1405; "10 stages" prose @1392; + bookkeeping 1424/1444-1449/1457-1462 | COVERED |
| COMPLEXITY_SCORE signals | R2 edit-site 6 | tier-dist @707-718, traceability @765, CPO @425-435, risk @532, n_tasks @682 | COVERED |
| validation/ dir | R2 edit-site 8 | @87, @120 (tree), @700 (index tbl) | COVERED |
| `--no-reflect` (command) | R3 §A.5 | Usage L23 + Arguments table after L38 | COVERED |
| `--spec` already exists (command) | R3 §A.2 | L37 (+ 5 refs) — DO NOT re-add | COVERED |
| phase/index templates | R3 §B/§C | phase after L125; index col after L53 + metadata after L30 | COVERED (read-only-mirror caveat flagged) |

### Cross-cutting (R4, R5, R6)

| Edit surface | Covered by | Status |
|--------------|-----------|--------|
| Tests break-risk + verification commands | R4 | COVERED ✅ (spot-checked) |
| reflect flag surface | R5 Area 1 (15-flag table, all ✅) | COVERED |
| markdownlint MD040 etc. | R5 Area 3 | COVERED |
| memories' binding on edits | R5 Area 4 | COVERED |
| MDTM Template 02 + example patterns | R6 | COVERED |

**Coverage verdict: NO GAPS.** Every edit site in the spawn-prompt enumeration has a research home with a current anchor.

---

## Spawn-Prompt Checklist (a–k)

### (a) All edit sites for BOTH proposals with CURRENT (re-verified) anchors? — PASS

All 11 task-builder edit sites (R1) + all 9 sc-tasklist edit sites (R2) + 3-file command/template surface (R3) carry CURRENT line anchors, each described as re-verified by fresh Read/Grep this session. I independently spot-checked 5 (SC-1..SC-5 above) — all exact. R1's drift banner (A.10.6 now between A.10.5 and A.11) is the highest-value catch and is confirmed real. **Evidence: SC-1..SC-5; coverage tables above.**

### (b) S4-trim resolution unambiguous (final token set, no existing-anchor collision)? — PASS

Final S4 set = **`{after Phase \d+, depends_on:}`** — drop `blockedBy:` (0 corpus hits, inert) and `after N\.\d+`; the kept `depends_on:` uses the underscore/colon literal per the user's exact wording (research-notes §82 flags this for literal encoding). Grep (SC-3) confirms: `TCS`/`Tasklist Complexity`/`blockedBy`/`depends_on` = 0 hits; `after Phase` = 1 hit at L1993 but it is a Content-Rules *description cell*, NOT a generated-MDTM dependency token, so no collision with the S4 *counting surface*. The entire TCS section is NEW content (no existing anchor to edit). **One residual nuance** the builder must encode literally: `depends_on:` (underscore) replaces the proposal's prose `depends on N.\d+`. Flagged clearly in both research-notes §82 and R1 edit-site 11. **Unambiguous.**

### (c) The 4 checkpoint-is-last invariants all located? — PASS

All four found, zero drift, verbatim-quoted (R2 edit-site 4): Self-Check #6 @1073, structural check #18 @1113, gate #19 @1114, gate #20 @1115. R2 additionally surfaces two coupled bookkeeping lines the proposal did NOT cite — #6's "(per checks 18-20)" cross-ref @1073 and the "check 1-20" close-line @1117 — both must be kept consistent if a 21st check is added. **Spot-checked (SC-2) — exact.** This is the lowest-risk edit cluster.

### (d) Test break-risk map concrete? — PASS (with the key decision explicit)

R4 is thorough and load-bearing:
- **Which tests parse SKILL text:** explicit Family-A (text-reading) vs Family-B (pure-Python/fixture) classification, per-test table with break-risk + required action.
- **The rf-qa TB-Add-9 decision:** R4 resolves it cleanly — the proposal as written adds the POST-reflect check to the **task-builder SKILL.md "Task File Validation Checklist"** (producer self-check surface), NOT a structural **TB-Add-9** in rf-qa.md. Default path = no rf-qa.md edit ⇒ INV-010 GREEN, merge-test "28 items" GREEN, break-risk NONE. The OPTIONAL TB-Add-9 path has 4 mechanical lockstep edits (rf-qa:298 28→29, merge-test :69/:190, dense numbered entry, sync-dev) — fully enumerated. **R1 edit-site 8 leans toward TB-Add-9; R4 recommends the validation-checklist path.** This is a genuine inter-file inconsistency in *recommended approach* — see Contradiction C-1 below. It is RESOLVABLE and both paths are documented, so not a blocker, but the builder MUST pick one explicitly.
- **Checkpoint-scanner reality:** R4 proves with CLI source (`checkpoints.py:40-98`, `config.py:386/411-504`, `executor.py:2408+`) that checkpoint discovery is declaration-driven (regex on `### …Checkpoint:` + `Checkpoint Report Path:`), NOT position-driven — so a POST task after the checkpoint is CLI-safe. Directly refutes the proposal's stated "biggest risk." **Concrete + evidence-backed.**

### (e) Exact UV-only verification commands enumerated? — PASS

R4 Table B + §3 give the per-phase command ladder, all UV-only: `make sync-dev` → `make verify-sync` → `uv run pytest tests/audit/ tests/skills/ -q` (after SKILL/rf-qa edits) → `uv run pytest tests/sprint/test_checkpoints.py tests/audit/test_checkpoint.py -q` (after tasklist/checkpoint edits) → `uv run pre-commit run markdownlint --files <md>` → `make test` (final). One-line smoke provided. The memory `make lint ≠ CI ruff format` is honored (`uv run ruff format --check src/ tests/` noted for any Python touch). No bare `python`/`pip`. **Enumerated + correct.**

### (f) Reflect flag surface fully verified (no templated nonexistent flag)? — PASS (strongest deliverable in the set)

R5 Area 1 is a definitive 15-flag table, each flag → exists? → authoritative `file:line` → semantics, checked against the LIVE `reflect.md` + `sc-reflect-protocol/SKILL.md` + refs. **Every templated flag exists with the claimed semantics; zero defects.** Key nuances captured: `--executor-model` is an EXCLUSION (not selection) flag; `--depth quick` disables regression-escalation (so O4 floor = never `quick` at POST is load-bearing and correct); NO model-routing/`--model` flag exists (grep 0 matches) and the proposals correctly introduce none; invocation = `Skill sc:reflect-protocol` (direct skill, mirroring brainstorm→adversarial). **No templated nonexistent flag.**

### (g) Markdownlint constraints (MD040 etc.) captured? — PASS

R5 Area 3 + R4 §3 both capture `.markdownlint.json` (`default:true`; MD013/MD024-siblings/MD029/MD036/MD033 the only deviations). **Top risk correctly identified: MD040 (unlabeled fences)** — task-builder & sc-tasklist SKILL.md have NO inline disable (unlike reflect SKILL.md), so EVERY new fence must be labeled (` ```text ` / ` ```yaml ` / ` ```markdown `). Also MD001/MD024/MD031/MD032/MD009/MD012/MD047 avoid-list. MD013 OFF ⇒ wide tables/long command strings safe. The memory `feedback_no_strategy_pivot_to_avoid_hooks` binding is honored: fix the fence label, do NOT copy a disable comment to escape. **Captured concretely.** Note: `.dev/` is markdownlint-excluded, so the generated task file itself is not linted — only the `src/` edits are.

### (h) MDTM Template 02 documented enough to emit a conformant file? — PASS

R6 Area 1 covers: full frontmatter key set (with allowed emoji/values), PART 2 fixed section order, Rule A3 (granular breakdown — one item per file/delta), A4 (iterative process), **B2 6-element self-contained item shape** (Context+WHY / Action+WHY / Output / "ensuring…" verification / evidence-on-failure / completion gate), B3 single-paragraph rule, B5 forbidden forms, J1 error-handling clause, Section L handoff patterns (L1-L6), M1 phase-gate QA sequence, I16 fix-cycle caps, I17 post-completion validation, D3 "no checklist items before Phase 1," and the anti-orphaning rule (Done-flip is LAST). Three real examples mined for structure (135209 gold-standard edit→sync→verify shape; 031100 lighter ≤50-item model; 024610 code-modifying). **Sufficient to emit a conformant file.**

### (i) Constraining memories' bindings on the EDITS stated? — PASS

R5 Area 4 binds four memories to the edits with quotes + the specific constraint each imposes:
- `feedback_sc_reflect_vs_inline_rfqa` → POST item MUST be fresh-session, executor-disjoint, pass `--executor-model`; never inline.
- `feedback_human_decision_items_must_halt` → PRE gate advisory-blocking (annotate + Open Questions additively, never auto-mutate); POST item HALTs (PENDING) until operator records verdict.
- `feedback-no-sctask-on-task-builder-tasklists` → every paste-ready command uses `/task` (execution) + `/sc:reflect` (gate), NEVER `/sc:task`.
- `feedback_no_strategy_pivot_to_avoid_hooks` → editing workflow: do exactly what the hook says (re-Read on freshness, label fence on MD040, sync-dev on verify-sync drift), never pivot/`--no-verify`/`git add -f`.
Plus `feedback_claude_dir_gitignored` (R4 §3.3, R5 §3.3 — never stage `.claude/`) and `feedback_no_multiline_paste` (R5 §4.3 — the long `/sc:reflect` string is single-line). **Bindings stated on the EDITS, not generic.**

### (j) Contradictions BETWEEN research files? — PASS (one real, resolvable; resolution clear)

See "Contradictions Found" below. The R1-vs-R4 TB-Add-9 approach divergence (C-1) is the one substantive inter-file inconsistency; resolution is clear (default to R4's validation-checklist path). The R1-vs-R6 "bulleted Phase-N item vs single-paragraph B2" point the spawn prompt asks about is NOT a contradiction — R6 explicitly resolves it (proposal's bulleted block must be COLLAPSED into one B2 paragraph). Documented as C-2 with the resolution.

---

## Contradictions Found

### C-1 (REAL, resolvable — Important): TB-Add-9 approach divergence (R1 vs R4)

- **R1 edit-site 8** treats the new "POST reflect item present" check as a **`TB-Add-9`** appended to rf-qa.md's structural-gate catalogue, and flags the rf-qa.md cross-edit as a mandatory integration hazard ("Adding a TB-Add-9 only to this SKILL.md checklist without a matching entry in rf-qa.md will be an orphan… INV-010 fails").
- **R4 §4** argues the proposal as written adds the check to the **task-builder SKILL.md "Task File Validation Checklist"** (a *different* surface — the builder's own pre-write self-check), which does NOT touch rf-qa.md, keeps INV-010 + merge-test GREEN, and is the lowest-risk path. R4 explicitly recommends NOT creating TB-Add-9 unless a reviewer insists.
- **Resolution (clear):** These are two different surfaces and R4 has correctly diagnosed that the proposal's §8 wording ("Task File Validation Checklist: add …") points at the SKILL.md producer-side checklist, not the rf-qa.md structural catalogue. **Default to R4's validation-checklist path** (no rf-qa.md edit, break-risk NONE). R1's TB-Add-9 path remains documented as the optional fallback with its 4 lockstep edits. **The builder MUST make this an explicit decision item** (one or the other), because R1's edit-site 8 as literally written would trigger the rf-qa.md cross-edit + the 28→29 merge-test update. Not a blocker (both paths fully specified), but it must not be left implicit.

### C-2 (NOT a contradiction — the spawn-prompt's R1-vs-R6 question, resolved): bulleted vs single-paragraph POST item

The spawn prompt asks whether R1's bulleted Phase-N item conflicts with R6's single-paragraph B2 item. It does NOT: R1 edit-site 7b cites the proposal's templated item which is authored as a Context/Action/Output/Verification/Completion-gate **bulleted block**; R6 §3.1 explicitly flags that MDTM Template 02 **B3/B5 FORBID multi-line/bulleted items** and the builder must **COLLAPSE** the proposal's 5 bullets into ONE self-contained B2 paragraph (R6 even supplies a ready single-paragraph draft in §3.2). So the apparent tension is pre-resolved: the proposal's bulleted shape is the *source*, the emitted MDTM item is a *collapsed paragraph*. **Resolution is explicit and correct.** R5 §2.4/§2.7 reinforces this and adds the important warning that the task-builder POST item (B2 5-field shape) and the sc-tasklist POST task (Sprint-CLI metadata-table shape) are DIFFERENT shapes and must not be cross-contaminated.

### C-3 (minor — naming consistency, already noted by research): `--spec` arity for the dogfood POST item

R6 §3.2 flags that reflect's `--spec` may be single-valued while THIS build has TWO driving proposals; it defers arity to R5. R5's flag table confirms `--spec <path>` (single path) but does not explicitly resolve "can two be passed." This is a minor open question for the dogfood POST item's command string (pass the larger proposal + name the second in prose), already surfaced by R6 — see Gap G-2. Not a contradiction, a residual question.

**No silent or unresolved contradictions about the same component's behavior.** The one substantive divergence (C-1) is resolvable with both paths documented.

---

## Completeness

| Research File | Status (header) | Summary/skeleton | Gaps/Open Qs | Key Takeaways | Rating |
|--------------|-----------------|------------------|--------------|---------------|--------|
| 01-taskbuilder-skill-anchors | **Complete** | edit-site→line map table | drift banner + per-site notes | summary table + length note | Complete |
| 02-tasklist-skill-anchors | **Complete** | edit-site→line map table | checkpoint-set status + bonus couplings | per-site verdicts | Complete |
| 03-tasklist-command-and-templates | Header says "In Progress" L4 **BUT** ends "Status: Complete" L304 | anchor→action summary table | per-file caveats + omissions | Critical builder facts (4) | Complete-effectively (see N-1) |
| 04-test-verification-impact | **Complete** | TL;DR + 2 tables | TB-Add-9 decision tree | net break-risk verdict | Complete |
| 05-patterns-conventions-sync-reflect | Header says "In Progress" L4 **BUT** ends "Status: Complete" L265 | flag-surface + markdownlint summary tables | memory bindings | flag-surface verdict | Complete-effectively (see N-1) |
| 06-mdtm-template-and-examples | Header says "In Progress" L5 **BUT** ends "STATUS: COMPLETE" L262 | recommended skeleton + frontmatter | TB-Add-2 bound note | reflect-item dogfood finding | Complete-effectively (see N-1) |

**N-1 (Minor, cosmetic):** R3, R5, R6 each carry a stale `Status: In Progress` line in their HEADER while their FOOTER says Complete. The body content is unambiguously complete in all three (full summary tables, verdicts, recommended outputs). This is a header/footer-sync cosmetic defect, not a substantive incompleteness. Does not block synthesis/build. No remediation required beyond awareness; if desired, a one-line header fix in each file.

**All six files have:** a summary/recommended-output section, a gaps/notes treatment, and key takeaways. No file is substantively unfinished.

---

## Depth Assessment

**Expected depth:** Deep (4 target files + large blast-radius test suite + two dense proposals).

**Actual depth achieved:** Meets/exceeds Deep tier. Evidence:
- **Data-flow / enforcement tracing:** R4 traces the Sprint-CLI checkpoint pipeline through real Python (`checkpoints.py`, `config.py`, `executor.py`) to PROVE checkpoint discovery is declaration-driven, refuting the proposal's stated biggest risk with source evidence — not a file-level summary but an actual control-flow trace.
- **Integration-point mapping:** R1 edit-site 8 maps the cross-skill INV-010 hazard (SKILL.md ↔ rf-qa.md ↔ A.10.5 enumeration); R2 maps the 4-way coupled checkpoint invariant set + bookkeeping; R4 maps which of 18 test files are text-reading vs fixture-based.
- **Pattern analysis:** R6 mines 3 real generated tasklists for reusable structural patterns (edit→sync→verify triplet, M1 phase-gate sequence, anti-orphaning Done-flip-last) and derives a sized skeleton.
- **Authoritative verification:** R5's 15-flag table checks every templated flag against live source — the kind of exhaustive cross-validation Deep tier demands.

**Missing depth elements:** None material. The research even self-flags its own residual unknowns (anchor drift requiring build-time re-verification; `--spec` arity) rather than papering over them.

---

## Compiled Gaps

### Critical Gaps (block synthesis/build)

**None.** No gap prevents a builder from emitting a granular, correct, conformant task file.

### Important Gaps (affect quality — builder must handle explicitly)

- **G-1 (from C-1): TB-Add-9 vs validation-checklist approach must be an explicit builder decision.** R1 edit-site 8 and R4 §4 recommend different surfaces for the "POST reflect item present" check. **Remediation:** the task file MUST contain an explicit item choosing the **validation-checklist path (R4-recommended, break-risk NONE, no rf-qa.md edit)** as default, and treat the TB-Add-9 path as an out-of-scope optional fallback. If the builder instead encodes TB-Add-9, it MUST also include the 4 lockstep edits (rf-qa.md:298 28→29, merge-test :69+:190, dense numbered entry, sync-dev) or INV-010 + merge tests break. Severity: **Important.**
- **G-2 (from C-3 / R6 §3.2): `--spec` arity for the dogfood POST item is unresolved.** reflect's `--spec` is documented single-path; this build has two driving proposals. **Remediation:** the dogfood POST item's command string should pass `.dev/proposals/reflect-in-task-builder.md` as `--spec` and name `.dev/proposals/reflect-in-sc-tasklist.md` in the item prose for the operator to add. R6 already drafts this. Severity: **Important** (affects the dogfood item's correctness, not the core edits).

### Minor Gaps (must still be fixed / noted)

- **G-3: `depends_on:` literal encoding (S4 trim).** The kept S4 token is `depends_on:` (underscore/colon) per the user's wording, replacing the proposal's prose `depends on N.\d+`. **Remediation:** builder encodes the literal `depends_on:` token in the new TCS section's frozen S4 extraction rule. Already flagged in research-notes §82 + R1 edit-site 11. Severity: **Minor** (one-token precision).
- **G-4: Companion resume-map entries (R1 edit-site 4).** The A.10.7 PRE gate, if resumable, may need entries in the resume maps (L163-169, L180-188); the proposal §8 does not require it. **Remediation:** builder decides — safest is to add A.10.7 to the overview step list only (required) and leave resume maps unless making the gate resumable. Severity: **Minor.**
- **G-5: Template files are read-only mirrors (R3 §B/§C).** Editing `phase-template.md`/`index-template.md` alone is cosmetic; the live copies are inline in SKILL.md §6A/§6B. **Remediation:** builder edits BOTH the SKILL.md inline copy (functional) and the template mirror (reviewer-sync). Already flagged. Severity: **Minor.**
- **G-6: POST-task template-field reconciliation (R3 §B.3).** The proposal's sc-tasklist POST task substitutes `Reflect Report Path:` + `Spawn Directive:` for the template's `Artifacts (Intended Paths):` + standalone `Deliverables:` blocks. **Remediation:** builder relaxes the template for the EXEMPT POST task (accept REPORT.md as artifact) and verifies SKILL.md self-check/structural gates don't reject the extra `**…:**` blocks. Already flagged. Severity: **Minor.**
- **G-7 (N-1): Stale `Status: In Progress` headers** in R3/R5/R6. Cosmetic; bodies complete. Severity: **Minor/cosmetic.**

---

## Recommendations

1. **Proceed to build.** The research is thorough, evidence-based, and its line anchors are current (5/5 spot-checks exact). A builder can emit a granular per-delta-site task file.
2. **Encode G-1 as an explicit decision item** in the task file: default to the validation-checklist path (no rf-qa.md edit). This is the single most important builder choice — getting it wrong either creates an INV-010 orphan (if TB-Add-9 added to SKILL.md only) or needless break-risk (if TB-Add-9 added without the 4 lockstep edits).
3. **Carry the dogfood POST reflect item** (R6 Area 3) — this build's own tasklist should be the first to template the POST gate it implements; resolve `--spec` arity per G-2.
4. **Honor the markdownlint MD040 discipline** (label every new fence in both SKILL.md files; no disable-comment escape) and the UV-only verification ladder (R4 Table B) after each edit phase.
5. **Encode the S4 `depends_on:` literal** and the four memory bindings (fresh-session POST, HALT-on-PENDING, `/task` never `/sc:task`, no-pivot editing) directly into the relevant items.
6. **Optional cleanup:** fix the three stale `Status: In Progress` headers (G-7) — not required.

---

## Verdict: **PASS**

No critical gaps. All six research files are substantively complete, evidence-based, and carry CURRENT (re-verified) line anchors. Five independent spot-checks against the real source files (the A.10.6 drift, the 4 checkpoint invariants, the S4 grep, the test "28 items" + INV-010 floor, the Critical Rules numbering) were **all exact**. Coverage of both proposals' edit surfaces is complete. The one substantive inter-file divergence (TB-Add-9 vs validation-checklist, C-1/G-1) is resolvable with both paths documented and is captured as a required builder decision. The remaining gaps are Important-but-bounded (G-2) or Minor/cosmetic (G-3..G-7). The research is sufficient for a builder to create a granular, correct, conformant MDTM task file.

**Gap count:** 0 Critical · 2 Important (G-1, G-2) · 5 Minor (G-3..G-7).

### (k) Granularity: enough per-edit-site detail for one checklist item per delta? — PASS

R1 (11 sites), R2 (9 sites + bookkeeping), R3 (per-file landings) each give per-delta-site anchors with exact before/after context. R6 §2.1 pattern 5 explicitly models "per-file/per-delta-site granularity (A3) — each edit is its own item naming the exact file, anchor substring, before→after text, and an 'ensuring…' clause." R6's recommended skeleton (≈33-41 items, within the ≤50 TB-Add-2 single-track bound) maps phases to delta clusters. **Builder can emit one item per delta, not "implement proposal 1."**
