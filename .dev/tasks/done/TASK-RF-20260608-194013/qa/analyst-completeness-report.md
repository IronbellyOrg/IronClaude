# rf-analyst Completeness-Verification Report

- **Analysis type:** completeness-verification
- **Gate:** task-builder research phase (rf-analyst completeness gate)
- **Track:** single-track `--reflect auto|1|2` POST-gate refactor
- **Spec:** `.dev/brainstorms/20260608-191030-reflect-flag-post-gate/merged-requirements.md` (986 lines; 13 FRs, 8 NFRs)
- **Target files:** `src/superclaude/skills/task-builder/SKILL.md` + `src/superclaude/agents/rf-qa.md`
- **Research dir:** `.dev/tasks/to-do/TASK-RF-20260608-194013/research/`
- **Date:** 2026-06-08
- **Stance:** ADVERSARIAL — looking for gaps that would block a builder.

Files read: 01-post-gate-anatomy.md, 02-tcs-auto-fer-machinery.md, 03-rfqa-validation-integration.md, 04-flag-plumbing-precedence.md, 05-template-patterns-examples.md, 06-test-verification-surface.md; spec read in full (986 lines).

---

## Verdict: PASS (0 builder-blocking gaps; 4 advisory items, all already surfaced by the research itself)

The six research files collectively cover every FR, NFR, and edit-seam § the spec implies, with a concrete file:line anchor or buildable approach for each. The byte-for-byte V15 anchor is captured verbatim. All 7 GAPS_AND_QUESTIONS are resolved with evidence. The verification surface (NFR check) lands a defensible `TESTING_REQUIREMENTS` value. The advisory items below are nuances the research already flagged for the builder (an 8th frontmatter value, a cross-file scope clarification, a `:847` back-compat tripwire, and a spec `:2094` imprecision) — none blocks task construction; each is the kind of thing the builder surfaces as a task-file Open Question or encodes directly.

---

## Findings (incremental)

### 1. Spec → research coverage matrix

#### Functional Requirements (13)

| Requirement | Covering research file:section | Status |
|---|---|---|
| FR-1 — one dial, ordinal domain `{none,0,1,2,auto}`, default 2, MALFORMED on unknown | 04 §1/§4 (precedence + parse), 06 AT-FR1 (parse re-impl), 02 §summary | COVERED |
| FR-2 — `none\|0` disables; no item; `reflect_post:` omitted | 01 Surface 4b/5b, 04 §5 (sentinel rules), 06 AT-FR2 | COVERED |
| FR-3 — Mode 1 inline `/sc:reflect --mode post --depth standard`, no remediate/Agent | 03 §E (V5/V6/V9), 05 §2.4, 06 AT-FR3; template body = spec §6.2 | COVERED |
| FR-4 — Mode 2 Bash `superclaude reflect run {TASK_FILE}` | 03 §E (V7/V8), 05 §2.3/§5.2 (no-nesting), 06 AT-FR4 | COVERED |
| FR-5 — `auto` resolves 1/2 deterministically (§4 FER) | 02 §8 (Examples A/B/C independently recomputed), 06 AT-FR5 | COVERED |
| FR-6 — `--reflect` subsumes legacy fields (total §5 map) | 04 §3 (§5.1/§5.2/§5.3 reproduced), 05 §2.2 (sibling contradiction) | COVERED |
| FR-7 — every non-`none` item HALTs + writes `reflect_post` back | 03 §E (V11/V12), 01 Surface 5 (Completion-gate verbatim) | COVERED |
| FR-8 — `--remediate` scope mode-fixed; Tier-3 → Open Questions | 03 §E (V9/V10), 06 AT-FR8 (partial-a noted) | COVERED |
| FR-9 — single producer at A.9; MODE-MATCH oracle | 01 cross-cutting "A.9 maps to", 02 §5 (INV-004), 03 §G (MODE-MATCH) | COVERED |
| FR-10 — Mode-2 wrapper-availability probe + frozen fallback (§8) | 02 §7 (`W` probe), 04 §3 (`2-degraded-halt`), 06 AT-FR10 | COVERED |
| FR-11 — Mode-1 nesting-boundary guard (runtime PRIMARY) | 03 §E (V8 encodes NFR-7), 05 §5.2 (no-nesting test), spec §6.2 body | COVERED |
| FR-12 — `--spec` threading across modes | 01 Surface 1a/1b, 04 §1 (`--spec`/`SPEC_PATH` precedent), 03 §E (V13) | COVERED |
| FR-13 — advisory WARNING on under-rigorous fixed-1 | 04 §6 (verbatim message + emission condition), 06 AT-FR13 | COVERED |

#### Non-Functional Requirements (8)

| Requirement | Covering research file:section | Status |
|---|---|---|
| NFR-1 — no reflect-logic duplication | 02 §summary (auto reuses TCS), 01 Surface 9 (no depth logic in items) | COVERED |
| NFR-2 — back-compat / byte-for-byte reversibility | 01 Surface 5 (V15 anchor verbatim), 05 §4 (reversibility nuance) | COVERED |
| NFR-3 — single SoT field `reflect_post_mode` | 04 §5 (frontmatter authority), 02 §5 (single producer) | COVERED |
| NFR-4 — extensibility (one new row, not a 4th knob) | 03 §C (INV-010 auto-richen), spec §6.5 reuse-bodies | COVERED |
| NFR-5 — determinism (pure arithmetic + W boolean) | 02 §8 (worked-example reproduction), 02 §5 (INV-004) | COVERED |
| NFR-6 — SoT discipline (`src/` → `make sync-dev`) | 05 §3 (verbatim CLAUDE.md + Makefile), 06 §4 (verify-sync gate) | COVERED |
| NFR-7 — no-nesting guard testable | 03 §E (V8), 05 §5.2 (no-nesting-guard test reusable) | COVERED |
| NFR-8 — fail-closed posture | 02 §7 (degraded-halt not silent inline), 04 §3 | COVERED |

#### Edit-seam sections (each implies a concrete edit surface)

| Spec § / surface | Covering research file:section | Status |
|---|---|---|
| §4 auto predicate (RESOLVE_AUTO, 2-stage) | 02 §1-§8 (full trace + recompute) | COVERED |
| §4.4 INV-004 resolved-band | 02 §5 (the band-edge divergence trap, builder-CRITICAL) | COVERED |
| §5 old→new knob map | 04 §3 (truth table reproduced) | COVERED |
| §6.1 `none` | 01 Surface 5b, 04 §5 | COVERED |
| §6.2 Mode 1 body | 03 §E, spec §6.2 (literal); 05 §2.4 | COVERED |
| §6.3 Mode 2 body + §6.3.1 unified diff | 01 Surface 5 (diff base captured), spec §6.3.1 | COVERED |
| §6.4 halt/2-degraded-halt (byte anchor) | 01 Surface 5 (all 6 lines verbatim) | COVERED |
| §6.5 auto-resolved | 02 §6, 03 §F (active-map) | COVERED |
| §7 depth/O4 reconciliation | 02 §6 ("fate of O4"), 01 Surface 9 | COVERED |
| §8 fallback ladder | 02 §7, 04 §3, spec §8.2 ladder | COVERED |
| §8.1 wrapper-availability probe | 02 §7 (`W` shape: `superclaude reflect --help` exits 0) | COVERED |
| §9 V1–V16 + per-mode active map + MODE-MATCH | 03 §E/§F/§G (full reproduction + integration shape) | COVERED |
| §9.3 MODE-MATCH placement (spec cites `:2094`) | 03 §D (resolves the imprecision), 01 Surface 7 | COVERED |
| §10 precedence + build-log note | 04 §4 (4-step order + note string) | COVERED |
| §10.4 advisory WARNING | 04 §6 | COVERED |
| frontmatter `reflect_post_mode` / `reflect_post` | 04 §5 (8-value set), 01 Surface 4 | COVERED |
| BUILD_REQUEST `REFLECT_POST_MODE` (`:853`) | 04 §2 (schema delta), 01 Surface 2 | COVERED |
| `:2051` checklist + `:2108` Rule 19 rewrites | 03 §H (verbatim + rewrite shapes), 01 Surface 6/8 | COVERED |

**No requirement or edit-seam § has zero research coverage.** Every cell is COVERED with a file:line anchor or a buildable approach.

### 2. GAPS_AND_QUESTIONS 1–7 resolution (explicit pass/fail)

| # | Question | Resolved by | Pass/Fail |
|---|---|---|---|
| 1 | Exact A.9 producer site (where `m` resolved/emitted, where `reflect_post_mode` + WARNING written) | 01 "where A.9 concretely maps" (`### A.9` = `:785`; BUILD_REQUEST `:853`; emission via Rule 19 `:2108` + template `:1994-1999`); 04 §4 (parse at flag-resolution, consume at A.9) | **PASS** |
| 2 | Exact `task-integrity` counter line (`:2094`) + surrounding text | 01 Surface 7 + 03 §D: spec `:2094` is **Critical Rule 12** (verified verbatim this session), not a check surface; real cap enumeration at `:1116`. MODE-MATCH is a *check*, not a counter. | **PASS** |
| 3 | rf-qa V1–V16 integration shape (new TB-Add-9 vs parameterized sub-block) | 03 §I: **new `TB-Add-9` (item 29) inside the bounded `#### Structural Gate Additions` region**, decisive ground = INV-010 regex `^[0-9]+\. \*\*TB-Add-([0-9]+):` auto-richens (`SKILL.md:1339`). | **PASS** |
| 4 | `REFLECT_POST_MODE` vs sibling `POST_REFLECT_MODE` collision | 04 §0: grep over live SKILL.md returns NOTHING for either token — sibling NOT merged, **no live collision**; spec §10.1 retires `POST_REFLECT_MODE` to a read-time alias. | **PASS** |
| 5 | Verification approach for a markdown refactor | 06 §5: `TESTING_REQUIREMENTS: UNIT` scoped (verify-sync + markdownlint + one self-consistency walkthrough + one fixture-based pytest modeled on `test_evidence_bound_tb_add_8.py`). Defensible, precedent-grounded. | **PASS** |
| 6 | `{BASE}`/`{EXECUTOR_CLASS}`/`{DEPTH}` placeholder resolution | 01 Surface 5 (placeholders enumerated; `<BASE>` angle-literal in manual item vs `{BASE}` curly in §6.3 — meaningful distinction pinned); 05 §2.1 (`start_commit`/`git merge-base` CODE-VERIFIED) | **PASS** |
| 7 | `auto` `W` wrapper-availability probe shape | 02 §7: build-time boolean = `superclaude reflect --help` exits 0 / `reflect` subcommand registered; computed once at A.9; wrapper itself OUT OF SCOPE. | **PASS** |

**All 7 resolved with concrete file:line or buildable approach. 7/7 PASS.**

### 3. Verification-surface realism (NFR check — research §06)

**PASS.** File 06 lands a defensible `TESTING_REQUIREMENTS: UNIT (scoped)` rather than hand-waving:

- Identifies two in-repo precedents (`tests/skills/test_task_builder_merge.py` content-marker assertions; `tests/audit/test_evidence_bound_tb_add_8.py` fixture-`.md` + Python rule re-impl + verdict matrix) — exactly the AT-VALIDATION-1 / AT-MISMATCH-1 / MODE-MATCH shape.
- Classifies all 22 §13 ATs into (a) mechanical / (b) static-wording / (c) builder-runtime, honestly noting ~7-8 ATs have a (c) core with **no Python entry point** (the builder is an LLM-driven markdown emitter — there is no `build_tasklist()` to call), and that faking those is overkill.
- Pins the gates that actually fire for a SKILL.md/rf-qa.md edit: markdownlint pre-commit (`.dev/` excluded, so the spec is not linted but the two `src/` files are), `make verify-sync` (the highest-probability failure if `make sync-dev` is skipped), full `pytest` in `test.yml` (not quick-check, which is `tests/unit/`-only).

This gives the builder a concrete, bounded `TESTING_REQUIREMENTS` value plus a named fixture set, not a vague "add tests." Strong.

### 4. Byte-for-byte back-compat anchor (NFR-2 / V15)

**PASS.** File 01 Surface 5 captures all 6 lines of `SKILL.md:1994-1999` verbatim (item header + Context + Action + Output + Verification + Completion-gate), re-verified this session at `:1994` (title byte-exact: "Independent post-execution **reflection** gate (**fresh session**, HALT)"). The research correctly pins the V15-critical nuances the builder must preserve:

- Title keeps "reflection" (full word) + "fresh session" — only Mode 2 (§6.3) changes the title to "reflect gate (wrapper subprocess, HALT)".
- `<BASE>` is angle-bracket literal (operator substitutes) in the manual item vs `{BASE}` curly-brace (builder/wrapper resolves) in §6.3 — a distinction the builder must not collapse.
- em-dash `—` (U+2014), `[--spec {SPEC_PATH}]` square-bracket-optional, `{DEPTH}` floored-at-standard clause, HALT clause citing `feedback_human_decision_items_must_halt`.
- `2-degraded-halt` appends exactly one `<!-- wrapper-absent: degraded from Mode 2 -->` comment to Context; gate text otherwise byte-identical.

The builder has an exact snapshot to diff against. The §6.3.1 unified diff (spec lines 545-578) is correctly identified as the authoritative byte-delta.

### 5. Contradictions / cross-file consistency

No contradictions between research files that would mislead the builder. Two cross-file alignments worth noting as strengths:

- **MODE-MATCH placement:** files 01 (Surface 7) and 03 (§D) independently reach the same conclusion — spec `:2094` is Critical Rule 12 (retry counters), not a check surface; MODE-MATCH is authored in rf-qa.md as part of TB-Add-9, not as an edit to Rule 12. Verified verbatim this session. Consistent.
- **Sibling cross-validation (file 05 §2.2):** correctly tags the sibling's `POST_REFLECT_MODE: wrapper|halt`-as-live-field schema design as `[CODE-CONTRADICTED by spec §10.1/§10.2/§5.3]` while preserving the sibling's anchor facts as `[CODE-VERIFIED]`. The doc-staleness discipline (verification tags) is present and correctly applied.

### 6. Advisory items (non-blocking — all already surfaced by the research)

1. **8th frontmatter value discrepancy (file 04 §5, flagged to builder).** Spec §10.3 enumerates 7 `reflect_post_mode` values; §8.2/V16/active-map require an 8th, `auto-resolved-2-degraded-halt`. File 04 correctly flags this and recommends the builder use the **8-value union** as the V2 validator oracle so degraded auto→2 cases pass. This is a real spec internal-inconsistency the builder must encode a decision for — best handled as a task-file Open Question or an explicit "use 8-value set" item. Already caught; advisory.

2. **Cross-file scope clarification (file 01 cross-cutting claim — I down-rate it).** File 01's consequence note states "the per-mode item BODIES (§6.2/§6.3) are emitted by `rf-task-builder.md`, NOT SKILL.md." Adversarial verification this session: `grep` over `src/superclaude/agents/rf-task-builder.md` returns **zero** hits for `POST_REFLECT_GATE`, `reflect_post`, `1994`, `post-execution refl`, or `penultimate`; the only file matching "Independent post-execution refl" is `SKILL.md`. So the byte-anchor body and the Output-Structure template live in **SKILL.md**, and rf-task-builder.md carries no competing copy. The spec's declared two-file scope (`SKILL.md` + `rf-qa.md`) **holds**; the builder does NOT need to edit a third file. File 01's claim is an over-statement of the orchestrator/emitter split — accurate that A.9 resolution is orchestrator-side, but the emitted template text the builder edits is in SKILL.md. Advisory: builder should treat scope as exactly the two declared files and not chase a phantom rf-task-builder.md edit.

3. **`:847` "M1-frozen 15-field BUILD_REQUEST … byte-identical" tripwire (file 01 Surface 2b, verified).** Renaming/retiring `POST_REFLECT_GATE` and adding `REFLECT_POST_MODE` touches the BUILD_REQUEST field set; the `:847` claim that the 15-field behavior is "preserved byte-identical" is a back-compat assertion the builder must reconcile (net-neutral count per spec §5.4, but the literal "15-field … byte-identical" text may need a touch). Real tripwire, already flagged. Advisory.

4. **Spec `:2094` line imprecision (files 01 + 03, resolved).** Not a research gap — the research resolved it — but the builder must be told explicitly that the spec's "`SKILL.md:2094`" citation for MODE-MATCH is wrong (it lands on Critical Rule 12) so the builder does not edit the retry-counter rule. Already resolved; carried forward as a builder note.

---

## Tool-engagement self-audit

- Read the driving spec in FULL (986 lines, two pages).
- Read research-notes.md in full (EXISTING_FILES, GAPS_AND_QUESTIONS 1-7, RECOMMENDED_OUTPUTS).
- Read all 6 research files in full (01–06), not skimmed.
- Adversarial code verification beyond the research (not blind-trust): grep `rf-task-builder.md` for POST-item tokens (down-rated file 01's 3-file claim); `sed`-verified `:2094` = Critical Rule 12, `:847` 15-field text, `:853` = `POST_REFLECT_GATE: ENABLED`, `:1994` title byte-exact. These independent checks confirmed the research's load-bearing anchors and corrected one over-statement.
- No web research (correctly: NFR-1 forbids new external logic; this is a purely internal refactor; no spawn-prompt authorization to fetch).

---

## Recommendations for the builder

1. Proceed to build — research is complete and builder-ready.
2. Encode the **8-value** `reflect_post_mode` set (`{none, 1, 2, auto-resolved-1, auto-resolved-2, halt, 2-degraded-halt, auto-resolved-2-degraded-halt}`) as the V2 validator oracle (resolves the §10.3-vs-§8.2 discrepancy); consider a one-line task-file Open Question noting the spec lists 7.
3. Scope edits to exactly the two declared files (`SKILL.md` + `rf-qa.md`); do NOT edit `rf-task-builder.md` (verified it carries no POST-item body).
4. Add an explicit item to reconcile the `:847` "15-field … byte-identical" text when `POST_REFLECT_GATE` is retired / `REFLECT_POST_MODE` added.
5. Carry the spec-`:2094`-is-Critical-Rule-12 correction as an item note so MODE-MATCH lands in rf-qa.md (TB-Add-9), not in the retry-counter rule.
6. Author the V1–V16 matrix as `TB-Add-9` matching the INV-010 regex shape (`29. **TB-Add-9: …**`) inside the bounded region; bump `#### Checklist (28 items)` → `(29 items)` and fix the `TB-Add-1 through TB-Add-7` heading.
7. Capture `start_commit` in a Phase-1 drift-guard step (also the reversibility-diff base); follow the predecessor's per-seam granularity + per-phase `make sync-dev`/`make verify-sync`/markdownlint discipline.

---

## VERDICT: PASS
