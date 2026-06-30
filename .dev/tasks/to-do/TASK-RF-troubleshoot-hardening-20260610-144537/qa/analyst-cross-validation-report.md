# Cross-Validation Report — Research Files 01..06

**Analysis type:** completeness-verification (cross-validation lens)
**Topic:** task-builder single track — "Pipeline Hardening Closure" mode for sc:troubleshoot-protocol (edit 4 + create 5 markdown files)
**Driving spec:** /config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md
**Date:** 2026-06-10
**Files cross-validated:** 6 (01-skill-structure-inventory, 02-command-and-contract-integration, 03-refs-conventions-and-report-template, 04-mdtm-template-and-examples, 05-doc-crossvalidation-spec-vs-code, 06-sync-verify-and-tests)
**Lens focus:** Cross-validate claims BETWEEN research files where multiple researchers touched overlapping surfaces. Verify consistency, flag contradictions. (read-only; do not resolve silently — surface both versions.)

---

## Summary of Method

This is a between-file consistency audit, not a code re-verification. Where two research files make a claim about the SAME artifact (a SKILL.md line number, a file's EXIST/ABSENT status, a placement seam, a QA floor number), I compared the two versions and recorded agree / diverge. Divergences are flagged with both versions and, where one is checkable from the research evidence itself, a note on which is correct.

For the two SKILL.md line-count claims (the one place the files literally disagree on a number), I additionally re-read the live file to determine which version is correct, because the divergence directly drives every insertion-point line number the task builder will encode.

---

## Cross-Validation Matrix (the 7 lens questions)

| # | Lens question | Files compared | Result |
|---|---------------|----------------|--------|
| 1 | SKILL.md line count + output-contract table location | R1 vs R2 | **DIVERGE** (count) / AGREE (table location) — see Finding 1 |
| 2 | Hardening trigger insertion seam | R1 (authoritative) vs R2/R3 (referential) | AGREE — no contradiction — see Finding 2 |
| 3 | 9 target files: 4 EXIST (edit) / 5 ABSENT (create) | R3 vs R5 | AGREE — exact match — see Finding 3 |
| 4 | H5 placement (fold into pipeline-hardening-closure.md) | R3 (decision) vs R1/R2/R5 | AGREE / no conflict — see Finding 4 |
| 5 | report-template.md insertion line internal consistency | R3 self-consistency | CONSISTENT — see Finding 5 |
| 6 | QA gate floors (I19) | R4 (only source) | NO CONFLICT — single source — see Finding 6 |
| 7 | TESTING_REQUIREMENTS = NONE | R6 vs R4 | AGREE — see Finding 7 |

---

## Finding 1 — SKILL.md line count: R1 says 549, R2 says 548. **R2 is correct (548). DIVERGENCE — MINOR, but must be reconciled.**

**The two claims:**
- **R1** (`01-skill-structure-inventory.md:10`): a callout note — *"File is **549 lines** as of read (brief said 548; off by one — confirmed by Read)."* R1 then repeats "549 lines" at `:134` ("All line numbers verified against the read of ... SKILL.md (549 lines)").
- **R2** (`02-command-and-contract-integration.md:87`): *"`...SKILL.md` (548 lines)"*.

**Live re-verification (this audit, read of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`):**
- `wc -l` = **548 lines**. The last content line (L548) is `Each ref is loaded only by the wave that needs it. Do not pre-load.` — exactly where R1's own §5 says the closing line is ("Closing line L548"). So **R2's 548 is correct; R1's header "549" is wrong.**

**Severity assessment — why this is MINOR, not CRITICAL:** I checked whether R1's pinned insertion-point line numbers are off-by-one as a consequence of its 549 miscount. They are NOT. Every R1 anchor I spot-checked lands correctly against the true 548-line file:

| R1 claimed anchor | R1 line | Live file | Match? |
|---|---|---|---|
| Frontmatter `description` | L3 | L3 | yes |
| Output Contract header | L37 | L37 | yes |
| `Field/Type/Description` table header | L41 | L41 | yes |
| `diagnosability_hard_stop` (last contract row) | L61 | L61 | yes |
| Wave 1.7 header | L251 | L251 | yes |
| Wave 2 Confidence Gate | L271 | L271 | yes |
| Tier 2 calibration completeness gate | L327 | L327 | yes |
| Wave 5 step 1 "Load `refs/report-template.md`" | L391 | L391 | yes |
| Wave 6 header / precondition | L437 / L439 | L437 / L439 | yes |
| `## Will Do` | L470 | L470 | yes |
| `## Will Not Do` | L484 | L484 | yes |
| `## Error Handling` | L499 | L499 | yes |
| `## Token Cost Profile` | L524 | L524 | yes |
| `## Refs` header | L536 | L536 | yes |
| Refs table header `File/When loaded` | L538 | L538 | yes |
| `refs/escalation-rubric.md` first ref row | L540 | L540 | yes |
| `refs/report-template.md` ref row | L544 | L544 | yes |
| `refs/diagnosability-audit.md` last ref row | L546 | L546 | yes |
| Closing "Do not pre-load." line | L548 | L548 | yes |

**Conclusion:** R1's *anchors* were computed against the true 548-line file and are all correct; only R1's prose **"549 lines" header note is an isolated miscount** (R1 even narrates "off by one — confirmed by Read", which is precisely the error — the brief's 548 was right and R1 talked itself into 549). R2's "548" agrees with the live file.

**Action for the builder:** Trust R1's per-anchor line numbers (they are correct) but use **548** as the file length. No insertion-point line number needs shifting. The only correction is cosmetic: read R1's "549 lines" as "548 lines."

**Output-contract table location — AGREE (no divergence):** Both R1 (`:66`, "field table is L41-61") and R2 (`:93`/`:138`, "Output Contract markdown table (lines 37-61)", "after line 61") place the contract table at L37-61 and the append point after L61. Live file confirms: header L37, table header L41, last row `diagnosability_hard_stop` L61. **Consistent across R1, R2, and the live file.**

**Secondary cross-check — the 8 new output-contract fields:** R1 (`:66`), R2 (`:138`), and R5 (`§4`, `:88-101`) all enumerate the SAME 8 spec §6.2 fields in the SAME names: `pipeline_hardening_applicable`, `pipeline_hardening_verdict`, `runtime_entrypoint_card_path`, `contract_ledger_path`, `unmask_sweep_path`, `effective_input_card_path`, `off_path_review_decision`, `known_escapes_caught`. **No naming divergence across the three files.** The mirror-precedent advice also agrees: R1 and R2 both point `pipeline_hardening_verdict` at the `diagnosability_verdict` enum precedent (L58) and the `*_path` fields at the `doc_context_card_path` `string|null` precedent (L52). Consistent.

---

## Finding 2 — Hardening trigger insertion seam: AGREE. No file contradicts R1's Wave 4.5 / L383 recommendation.

**R1 is the authoritative source** (owns the SKILL.md structural map). R1 (`:57`, `:140`) recommends a new `### Wave 4.5: Pipeline Hardening Closure` inserted at the `---` seam at **L383**, before Wave 5 (L385), with a stated alternative of a mandatory pre-step inside Wave 5 before step 1 (L391). Rationale: "after Tier 1 diagnosis (Wave 1.7 ends L267) AND after Tier 2 (Waves 3-4 end L382), and before final report closure (Wave 5 L385)."

**Cross-check against the other files that touch placement:**
- **R2** (`:8`, `:47`, `:150`) independently says Pipeline Hardening Closure "runs after Tier 1 diagnosis, before report closure" and "inserts between Wave 1 diagnosis and Wave 5 report closure" — **same seam, same direction**, framed from the contract/handoff side. R2 explicitly notes it is "NOT a 4th tier" (`:47`), which does not contradict R1's Wave 4.5 (a fractional wave inside the existing flow, not a new tier).
- **R3** (`:219`) says the new mode fires "after Tier 1 diagnosis, before Wave 5 closure" — **same seam**, citing spec §5.2 line 75.
- **R5** does not independently re-derive the seam (it is a spec-vs-code validator) and so raises no competing location.

**Verdict: no contradiction.** R1, R2, R3 all converge on "after diagnosis (through Wave 4), before Wave 5 report closure." R1 owns the exact line (L383) and the Wave 4.5 numbering (consistent with the existing 1.5/1.6/1.7 fractional precedent); R2/R3 corroborate the conceptual placement. Live file confirms Wave 4 header L356 and Wave 5 header L385, so an insertion at the L383-L384 seam between them is structurally valid.

---

## Finding 3 — 9 target files (4 EXIST / 5 ABSENT): AGREE. R3 and R5 match exactly.

**R5 is the authoritative cross-validator** (its whole job is spec-path vs repo). R5 (`§1`) reports:
- **4 EXIST (edit targets) — all `[CODE-VERIFIED]` exist:** `commands/troubleshoot.md`, `skills/sc-troubleshoot-protocol/SKILL.md`, `refs/report-template.md` (16909 bytes), `refs/remediation-handoff.md` (5434 bytes).
- **5 ABSENT (create targets) — all `[CODE-VERIFIED]` absent, parent `refs/` exists:** `pipeline-hardening-closure.md`, `runtime-entrypoint-verification.md`, `contract-enumeration.md`, `unmask-and-sweep.md`, `effective-input-proof.md`.

**Cross-check against R3** (`§6`, `:299-308`): R3's "CREATE 5 refs" list names **the identical 5 filenames**, and R3's "EDIT 2 files" (report-template.md + remediation-handoff.md) plus its flag to R1 for SKILL.md + R2's command edit cover **the identical 4 edit targets**. The 4-edit / 5-create split is **identical** between R3 and R5. No conflict on which files exist vs are absent.

**Corroboration from R6** (`:33`): R6 independently confirms the 5 new refs land at `src/superclaude/skills/sc-troubleshoot-protocol/refs/*.md` and are auto-mirrored by `sync-dev` — consistent with R3/R5's create list and parent-dir-exists finding. R5 also notes the `refs/` dir already holds 8 sibling refs (`:25`); none collide with the 5 new names. **Full agreement across R3, R5, R6.**

---

## Finding 4 — H5 placement (fold into pipeline-hardening-closure.md): AGREE / no conflict.

**R3 owns this decision** (`§4.6`, `:271-281`): H5 is a *Rule*, not a card/gate; it gets a `## Rule H5 — off-path-reviewer` section **inside `pipeline-hardening-closure.md`**, NOT its own 6th ref and NOT inside effective-input-proof.md. R3 gives 4 evidence-based reasons (spec taxonomy types it a "Rule" §7 line 266; no fill-in card; single contract field `off_path_review_decision` not a path; H5 spans all boundary types so it must not be narrowed into H4).

**Cross-check for contradictions in R1/R2/R5:**
- **R1**: registers exactly **5 new refs** in the `## Refs` table (`:111`, `:147`) — `pipeline-hardening-closure.md` + the 4 gate refs. R1 does NOT propose a 6th `off-path-reviewer.md` ref. **Consistent with R3's "5 refs exactly, H5 folded in."**
- **R2** (`:176`): treats H5's off-path reviewer as *already wired* into the existing reflect/auggie-review/adversarial chain and exposes it only via the `off_path_review_decision` contract field — **consistent** with R3's "H5 = a decision token, lives in the hub ref."
- **R5** (`§3`, `:80`): validates H5→R1/R3/R4/R5/R6 as a "cross-cutting / composite rule," matching R3's "H5 spans all boundary types" rationale. **No conflict.**

**Verdict: no file contradicts folding H5 into pipeline-hardening-closure.md.** All four files that touch H5 treat it as a cross-cutting rule producing one contract field, never as a standalone ref/gate. Net new-ref count is consistently **5** across R1, R3, R5.

---

## Finding 5 — report-template.md insertion line internally consistent (R3 self-consistency): CONSISTENT.

R3 (`§2.1` section map + `§2.2` insertion point) is the only file giving report-template.md line numbers, so this is an internal-consistency check of R3 against its own section map:
- R3's section map (`:93-113`) lists `## Follow-up tasks` at lines **122-132**, then `## Grounding Gaps` at **134-144**.
- R3's insertion recommendation (`:120`, `:122`) says insert `## Pipeline Hardening Closure` "immediately AFTER `## Follow-up tasks` (ends line 132) and BEFORE `## Grounding Gaps` (begins line 134)... between current line 132 and 133," anchored after the line `If there are no follow-ups, write "None."` (line 132).
- These are **mutually consistent**: 132 (end of Follow-up tasks) → 133 (blank) → 134 (Grounding Gaps), insert at the 132/133 boundary. The four-backtick fence boundaries R3 cites (opens L7, closes L203) also bracket the insertion point (132 is inside 7-203), and R3 correctly notes the insertion stays *inside* that outer fence while the separate `## Pipeline Hardening Closure rule` prose goes *after* the EOF (line 259). Internally coherent.

**Note (not a contradiction):** R2 (`:112`) references report-template.md frontmatter at "lines ~8-26" with a `~` approximation and explicitly defers to R3 ("R3 owns report-template.md"). R3's precise map says the header field block is lines **8-22**. The `~8-26` is an approximate, deferred figure, not a competing precise claim — no real divergence. The builder should use R3's precise numbers (8-22 header block; insert at 132/133).

---

## Finding 6 — QA gate floors (I19): NO CONFLICT (single source). R4 is the only file quoting I19.

R4 (`§2c`, `:88-106`) is the sole source for the I19 minimum-agent floors. It quotes them verbatim:
- **Final/assembled-output gate:** <500 lines → 6; 500-1500 → 8; 1500-3000 → 10; >3000 → 12.
- **Intermediate gates:** 5 each (research/synthesis/task-integrity, with the stated agent mixes).
- **Adversarial framing N:** 5 / 10 / 15 / 20 by the same size buckets.

**No other research file states different floors.** R1, R2, R3 do not address QA agent counts at all (out of their scope); R5 and R6 mention QA only by reference, not with competing numbers. R6 (`§3`, TESTING_REQUIREMENTS) addresses test surfaces, not gate floors. **There is no second source to contradict, so there is no divergence.** R4's internal application is self-consistent: it classifies this track as ">500 lines → ≥8 final-gate agents (4 structural + 4 content)" and "Deep-tier → qa_intensity = full," which correctly reads off its own quoted I19/I22 tables.

**Caveat for the builder (consistency, not contradiction):** R4 says the output is ">500 lines" and assumes the 500-1500 bucket (→ 8 agents, N=10). The exact final line count is not yet known (the 5 refs + edits are not written). The builder must re-bucket against the *actual* assembled line count at gate time — R4 itself flags this ("scale up per actual line count," `:97`). This is a build-time instruction, not an inter-file conflict.

---

## Finding 7 — TESTING_REQUIREMENTS = NONE: AGREE. R6 and R4 are consistent.

- **R6** (`§3`, `§TESTING_REQUIREMENTS recommendation`, `:112`, `:127-129`) is the authoritative source: *"TESTING_REQUIREMENTS = NONE."* Evidence: zero tests in `tests/` parse the troubleshoot command/skill frontmatter, count/enumerate skill refs, or validate the troubleshoot skill structure (grep for `sc-troubleshoot-protocol` → zero matches). Spec §9's conditional ("targeted tests *if* command/skill metadata is parsed by tests") evaluates FALSE.
- **R4** (`§6`, `:209`) independently reaches the same conclusion from the template/I18 angle: *"I18 testing is N/A (markdown, not code)"* — I18 applies only to tasks that create/modify SOURCE CODE files, and this is a markdown-only documentation transform. R4: "No `uv run pytest` code-test item is required by I18."

**Two independent routes, same answer.** R6 (test-surface inspection) and R4 (I18 template rule) both conclude no automated tests are needed; neither file implies tests ARE required. Both converge on the same VALIDATION surface instead: `make sync-dev` + `make verify-sync` + markdownlint + git-scope check (R6 `§VALIDATION command sequence`; R4 `§6` validation items). **No contradiction.** R5 (`§5`) corroborates the validation mechanism by `[CODE-VERIFIED]`-ing that `make sync-dev` (Makefile:109) and `make verify-sync` (Makefile:166) are real targets — consistent with R6's reliance on them.

---

## Checklist results (the 4 spawn-prompt checklist items)

| # | Checklist item | Result | Evidence |
|---|---------------|--------|----------|
| 1 | Cross-file consistency on shared line refs/counts | **1 MINOR divergence** | SKILL.md count R1=549 vs R2=548 (R2 correct; R1 anchors still correct) — Finding 1. All other shared line refs (contract table L37-61, Wave 4/5 seam, report-template 132/134, refs table L538-546) agree. |
| 2 | No contradictory claims between research files | **PASS** | No substantive contradiction found across Findings 2-7. The only numeric disagreement (Finding 1) is a header miscount with no downstream effect. |
| 3 | Shared dependency (SKILL.md ref-table rows for new refs) documented consistently by R1 + R3 | **PASS** | R1 (`:111`, `:147`) and R3 (`:83-85`, `:310`) both say the 5 new refs each need a row appended to the SKILL.md `## Refs` table (L536-546 region) + a lazy-load mention in the new wave step. R3 explicitly flags this as "R1's territory," and R1 owns it — same instruction, no conflict. Both agree on **5** new rows. |
| 4 | Integration-point descriptions match across researchers | **PASS** | Command-thin / handoff (R2) ↔ SKILL.md seam (R1) ↔ refs detail (R3) ↔ spec-path validation (R5) ↔ sync/test surface (R6) are mutually consistent. The Wave 6 `success`-gates-remediation seam is described identically by R1 (`:91`), R2 (`:159-165`), and R3 (`:182`, `§3.3`). The `pipeline_hardening_verdict=blocked` → force `status: partial` wiring is described consistently by R1 (`:91`), R2 (`:165`), and R3 (`§3.3`). |

---

## Non-blocking spec self-consistency notes (carried from R5 — NOT inter-file contradictions)

R5 surfaced two spec-internal flags (F1, F2) that are NOT research-file contradictions but are worth threading so the builder does not encode them as code-driven items:
- **F1 (cosmetic):** spec §6.2 `pipeline_hardening_verdict` enum includes `not_applicable`, but the spec §8 report "Closure verdict" line lists only `pass | blocked | advisory`. R5 (`:118`, `:150`) and R3 (`§2.3` shows the §8 block with `pass | blocked | advisory`) are CONSISTENT with each other in *reporting* this — both reflect the spec's own text faithfully; neither invents a value. This is a spec-text reconciliation, not a research-file divergence. R3's §8 block and R5's F1 note agree.
- **F2 (naming):** §6.2 `_card_path`/`_ledger_path` fields (per-run artifacts) vs §9 ref filenames (per-skill templates) are different artifact classes. R5 (`:119`, `:151`) and R3 (`§4` template-vs-instance framing) agree these are distinct, not conflicting.

These are recorded so the consolidated gap list does not double-count spec-internal cosmetics as cross-file contradictions.

---

## Gap list (FAIL items requiring builder action)

Only ONE item rises above informational, and it is MINOR:

### MINOR
- **G1 — SKILL.md line-count statement in R1 is wrong (549 → 548).** R1 (`01-skill-structure-inventory.md:10`, `:134`) states the file is 549 lines; the live file is 548 (R2 correct). **Impact: none on insertion line numbers** — R1's per-anchor lines were all computed against the true 548-line file and verified correct in Finding 1. The builder should use 548 as the file length and otherwise trust R1's anchors verbatim. No re-derivation of insertion points needed. (Severity MINOR because it does not propagate to any actionable line number.)

### No CRITICAL or IMPORTANT cross-file contradictions found.
- The 4-edit / 5-create file split is identical across R3 and R5.
- The Wave 4.5 / L383 insertion seam is uncontradicted (R1 authoritative; R2, R3 corroborate).
- H5-folds-into-hub-ref is uncontradicted; new-ref count is consistently 5.
- I19 floors have a single source (R4); no competing numbers.
- TESTING_REQUIREMENTS = NONE agreed by R6 and R4 via two independent routes.
- The downstream integration seams (Wave 6 `success` gate, `blocked`→`status: partial`, ref-table rows, off-path-reviewer field) are described consistently by every file that touches them.

---

## VERDICT: PASS

**Rationale:** The cross-validation lens found **zero CRITICAL or IMPORTANT contradictions** between the six research files. Every shared structural claim — the 4-edit/5-create file split (R3↔R5), the output-contract table location and the 8 new field names (R1↔R2↔R5), the Wave 4.5/L383 insertion seam (R1↔R2↔R3), H5 folding + 5-ref count (R1↔R3↔R5), the SKILL.md ref-table rows (R1↔R3), the QA floors (R4 single-source), and TESTING_REQUIREMENTS=NONE (R4↔R6) — is mutually consistent and, where re-checkable against the live file, correct.

The sole divergence is **G1 (MINOR)**: R1's prose says SKILL.md is 549 lines while R2 (and the live file) say 548. I re-read the live file and confirmed 548 is correct, AND confirmed that R1's *insertion-point line numbers were nonetheless all computed against the true 548-line file* (19/19 anchors verified) — so the miscount is an isolated header statement with **no downstream effect on any builder action**. It does not block the build; the builder should simply treat the file as 548 lines and use R1's anchors as-is.

A single MINOR, non-propagating numeric typo with verified-correct downstream anchors does not warrant FAIL. The research corpus is internally consistent and safe to build from.

**Report file:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260610-144537/qa/analyst-cross-validation-report.md
