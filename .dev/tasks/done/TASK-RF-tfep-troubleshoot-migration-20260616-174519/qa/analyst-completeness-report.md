# Research Completeness Verification — BREADTH Lens

**Topic:** TFEP /sc:forensic → /sc:troubleshoot migration tasklist
**Date:** 2026-06-16
**Lens:** BREADTH (per-step coverage with anchored detail for self-contained checklist items)
**Files analyzed:** 4 (01-file-inventory.md, 02-troubleshoot-surface.md, 03-integration-and-sync.md, 04-template-and-examples.md)

---

## Method

For each of the 8 pipeline changes I checked: (a) is there a concrete `file:line` anchor a builder could turn into a granular self-contained checklist item; (b) is the *target state* (what the edited text should become) specified or at least decidably scoped; (c) is the change covered by at least one researcher with no orphaned sub-requirement. I then separately verified the cross-cutting enablers: the sync/verify-sync verification strategy and the MDTM Template-02 mechanics. Adversarial posture: I actively hunted for steps that have a "where" but no "what", and for the two genuinely-additive changes (2 and 3) where anchors alone are insufficient.

---

## Per-Step Coverage Matrix (the 8 changes)

| # | Change | Primary researcher(s) | Anchor depth | Target-state depth | Verdict |
|---|--------|----------------------|--------------|--------------------|---------|
| 1 | Rename forensic→diagnostic escalation | R1, R3 | Strong | Strong | PASS |
| 2 | Troubleshoot return-contract adapter | R2, R3 | Strong | Adequate (design-decision flagged, not pre-decided) | PASS (with caveat) |
| 3 | --context/--caller ingestion | R2 | Strong | Strong | PASS |
| 4 | Remediation ownership decision | R1, (R3) | Strong (anchors) | WEAK (decision unmade) | PASS-WITH-GAP |
| 5 | task-protocol consumes troubleshoot output | R1, R3 | Strong | Adequate | PASS |
| 6 | Preserve TFEP freeze semantics | R1 | Strong | Strong | PASS |
| 7 | Update incident reporting | R1, R3 | Strong | Adequate | PASS |
| 8 | Update escalation budget language | R1, R3 | Strong | Adequate | PASS |

---

## Per-Step Findings

### Step 1 — Rename forensic→diagnostic escalation — PASS
Fully anchored. R1 §B gives the complete 8-occurrence "forensic" bare-term worklist with verbatim surrounding text: SKILL.md lines 172, 205, 206, 213, 215, 216, 250, 253, plus task.md line 48 ("structured forensic analysis"). R3 §1A independently corroborates the same line set as the LIVE surface and explicitly separates incidental/historical "forensic" prose (§1C/§1D) that must be LEFT ALONE — this prevents the builder from over-reaching. R1 §E even notes the overlap (line 216 / 212 satisfy both rename and command-swap concerns → edit once). A builder can write one granular item per anchored line. Target state ("diagnostic"/"troubleshoot" terminology) is decidable from context. No gap.

### Step 2 — Troubleshoot return-contract adapter — PASS (with caveat)
Donor surface is exhaustively anchored. R2 §B3 enumerates all 30 Output Contract fields with `file:line` (SKILL.md 41–72), maps each TFEP-needed field to donor-present/missing, and identifies the 5 MISSING structured fields (`recommended_escalation`, `tasklist_insertion_path`, `remediation_target`/block-path, `root_cause_summary`, `solution_summary`). R2 §B4 anchors the additive-versioning governance (line 62, `contract_version`, NFR-6). R2 §B5 anchors the Wave 5 emission insertion point (between footer ending 457 and surface step 459, "step 4.5"). R3 §4 independently re-derives the same contract mismatch and lists 5 concrete adapter gaps. **Caveat (not a gap):** the design fork — (a) ADD the 5 fields to the troubleshoot Output Contract vs (b) synthesize them in an adapter shim — is correctly surfaced by BOTH R2 (§B3 "Recommend (a)") and R3 (§4.2 "(a) or (b)"), but is left as a builder/author decision. This is appropriate research scoping (research anchors options; the build decides), and there is enough anchored detail to write self-contained items under EITHER branch. Acceptable.

### Step 3 — --context/--caller ingestion — PASS
The strongest-covered change. R2 §A1–A5 + §B1–B2 + §B6 give every anchor a builder needs: argument-hint (troubleshoot.md:8), Options-table insertion point with exact row format to mirror (after troubleshoot.md:58, format from line 57, `(none)` sentinel from line 52), command parse step (line 64), surface list (line 67), Wave 0 parse sentence (SKILL.md:115) with a proposed RESOLVE sub-step, the audit-header `caller:`/`context_path:` insertion (after SKILL.md:136), exit/STOP additions (lines 141/143), and the SUMMARY footer sibling (lines 446–455). Target-state strings are proposed verbatim. R2 §C also surfaces default-interaction caveats (`--no-doc-discovery`, `--no-diagnosability-audit` tensions) so the builder doesn't naively auto-set conflicting flags. No gap.

### Step 4 — Remediation ownership decision — PASS-WITH-GAP (IMPORTANT)
**Anchors: strong. Target-state decision: UNMADE.** R1 §C("Change #4") precisely anchors the ownership logic: SKILL.md Step 4 branches (lines 215–222, esp. 219 `test_is_wrong==true → present to user, do NOT auto-fix`, 220–222 status branches) + Step 5 insertion (224–229, the `## Failure Remediation Plan (Adjudicated)` block, append-not-replace, line 225 reads `tasklist_insertion_path`). R3 §4.3 corroborates the field-level consumer reads. **What is missing:** none of the four files actually DECIDES the ownership outcome — i.e. *who owns remediation after the swap*: does task-protocol keep adjudicating/inserting (status quo, Step 4/5 preserved), or does troubleshoot's own remediation chain (`--fix`, Tier 3, `remediation_offered`/`remediation_accepted` fields at SKILL.md 56–57) take over? R2 §C2/C3 raises the adjacent tension (whether `--caller task-unified` auto-sets `--fix`, and the Wave 1.6 hard-stop interaction) and explicitly defers: "decision belongs to R1 (consumer side) / task author." R1 anchors the lines but does not state the target ownership model either. So a builder has the WHERE but not the WHAT for the actual decision. This is writable as a self-contained *decision* item (it can be framed as "decide and document ownership: option A keep task-protocol adjudication, option B delegate to troubleshoot --fix; edit lines 215–229 accordingly"), so it is not a hard blocker — but the research leaves the decision open rather than recommending one, which is a substantive content gap for a step whose entire name is "decision." Flagged IMPORTANT.

### Step 5 — task-protocol consumes troubleshoot output — PASS
Anchored on both ends. R1 §B + §C anchor the consumer side (SKILL.md:216 read `return-contract.yaml`; 219–222 status/`test_is_wrong` branches; 225 `tasklist_insertion_path`; 203 `context.yaml` write). R3 §4 reconciles producer↔consumer field names and §5 gives an explicit "adapter contract gate" grep cross-check (every consumer token must have a producer in sc-troubleshoot-protocol/ after the change). R2 §B5 anchors where troubleshoot would emit the file. The producer-fields-missing problem is the SAME as Step 2 (correctly — 2 and 5 are two sides of one contract) and is enumerated. Enough to write self-contained items. No independent gap beyond the Step 2 caveat.

### Step 6 — Preserve TFEP freeze semantics — PASS
Tightly anchored. R1 §C("Change #6") pins the freeze block to SKILL.md lines 185–188 (187 STOP, 188 FREEZE), explicitly notes the block "contains NO forensic/troubleshoot terminology and must be left semantically intact." Target state = preserve verbatim except any heading-word rename. This is the easiest self-contained item to write (a preserve/verify-unchanged item). No gap.

### Step 7 — Update incident reporting — PASS
Anchored. R1 §C("Change #7") pins the incident-report fenced template (SKILL.md 241–251), the "Forensic artifacts" field (line 250), and the "committed to git alongside other forensic artifacts" sentence (line 253). R3 §4.5 adds the substantive content requirement: the template fields currently pull forensic-pipeline filenames (`rca-verdict.md`/`solution-verdict.md`) and must be re-sourced from troubleshoot's artifacts (`REPORT.md` + hypothesis cards + `audit.log`). So both the WHERE (R1) and the WHAT-changes-in-content (R3) are present. Sufficient for self-contained items. No gap.

### Step 8 — Update escalation budget language — PASS
Anchored. R1 §C("Change #8") pins the heading (SKILL.md:255) and fenced block (257–261), with verbatim forensic invocations at 258–259 and the FULL STOP line 260. R3 §4.4 supplies the content requirement: the block hardcodes forensic token bands (~5-8K, ~15-20K) that must be restated against troubleshoot tiers, and R3 cites troubleshoot's own per-wave budget table (sc-troubleshoot-protocol/SKILL.md L559–567, ~3–9K Tier-1 band) as the re-sourcing reference. Both WHERE and WHAT present. Sufficient. No gap.

---

## Cross-Cutting Enabler 1 — Sync / verify-sync verification strategy — PASS (well covered)
R3 §3 is thorough and authoritative: `make sync-dev` (Makefile L109–163) and `make verify-sync` (L166+) with exact invocations, what each syncs (skills incl. refs/, commands), drift/orphan checks, and mtime evidence that the `.claude/` copies are sync outputs. R3 §5 gives a per-step verification strategy (edit gate, residual-reference grep gates with expected-0 results, adapter-contract gate, report-template gate, no-`.claude`-staging gate). R4 §PART-A (I18) independently confirms `make verify-sync` is the docs/skill-edit verification analog and that `.claude/` must never be staged. CLAUDE.md ABSOLUTE RULE is correctly cited by both R3 and R4. A builder can write concrete verification items (`make sync-dev` → `make verify-sync` expect exit 0, plus the `rg` residual gates). No gap.

## Cross-Cutting Enabler 2 — MDTM Template-02 mechanics — PASS (well covered)
R4 §PART-A maps Template-02 PART-1 rules with line refs: frontmatter fields (L1–61), A3 granular breakdown (108–112), B2 six-field self-contained item format (159–166), anti-orphaning E1/E2/E3 + D3 (292–405), M3 lens-based QA sequence (1059–1096) with standard lenses and I22 intensity scaling, M4 fidelity gate (1098–1121) with the I21 applicability test correctly applied to a rename-vs-reinterpret decision, POST reflect gate shape, Post-Completion ordering (I13/I17), and I18 TESTING_REQUIREMENTS=NONE for docs/skill edits. R4 §PART-B grounds all of this in a same-day, directly-analogous worked example (TASK-RF-bare-review-migration) showing phase headers, self-contained item shape with `file:line` anchors, per-phase M3 gate encoding, M4 gate, and the POST-reflect-wrapper→status-to-Done terminal ordering. This is more than enough for a builder to produce a conformant tasklist. No gap.

---

## Contradictions / Inconsistencies Found
- **None substantive across files.** R1 and R3 agree precisely on the LIVE SKILL.md line set (172–261 block; dispatch 212, consumer 216, fields 219–225, incident 237–253, budget 255–261). R2 and R3 agree on the contract mismatch and the 5 missing fields. R4 is independent (template mechanics) with no overlap to contradict.
- **Minor naming note (not a contradiction):** R2 §B5 places the troubleshoot-side emission "step 4.5" while R3 §2 places the report-template `## TFEP Consumer` block after Next Steps (line 154). These are two different files (SKILL.md Wave 5 vs refs/report-template.md) and two different artifacts — complementary, not conflicting.

## Completeness-of-Research Flags (file-level)
- **R4 (04-template-and-examples.md) status field is inconsistent:** line 4 says `Status: In Progress`; line 169 says `Status: Complete`. Content is clearly complete (full PART A + PART B + SUMMARY). MINOR — the stale `In Progress` header should be reconciled, but does not affect coverage.
- R1, R2, R3 each carry a clean `Status: Complete` and a builder-facing SUMMARY section. All four have a usable summary/takeaway block.

---

## VERDICT: PASS

All 8 pipeline changes have corresponding research coverage with concrete `file:line` anchors a builder can turn into granular, self-contained checklist items, and both cross-cutting enablers (sync/verify-sync verification strategy; Template-02 mechanics) are well covered with an analogous worked example. The research is anchor-complete on the BREADTH lens: no step lacks a "where," and 7 of 8 also have a sufficient "what." The single substantive content gap (Step 4 ownership decision is anchored but the decision itself is left open) is writable as a decision-item and does not block tasklist construction — it is recorded below as an IMPORTANT gap the builder MUST resolve, not defer.

PASS is conditional on the builder explicitly resolving Gap G1 during construction (frame it as a decide-and-document item, not a silent default).

---

## Structured Gap List

### IMPORTANT (must be resolved during build, does not block starting)
- **G1 — Step 4 remediation-ownership decision is unmade.** Anchors are strong (SKILL.md Step 4 lines 215–222, Step 5 lines 224–229; troubleshoot `--fix`/Tier-3/`remediation_offered`/`remediation_accepted` at sc-troubleshoot-protocol/SKILL.md 56–57), but no researcher recommends an ownership model (task-protocol keeps adjudicating + inserting vs delegate to troubleshoot's remediation chain). R2 §C explicitly defers to "R1 / task author"; R1 anchors but does not decide. **Required action:** the builder must author a decide-and-document checklist item that picks option A (preserve task-protocol Step 4/5 adjudication) or option B (delegate to troubleshoot --fix), then edit lines 215–229 accordingly. Tie-in: also decide whether `--caller task-unified` auto-sets `--fix` (R2 §C2/C3 tension) consistently with the chosen ownership model.

### MINOR (cosmetic / hygiene, non-blocking)
- **G2 — R4 status header inconsistency.** `04-template-and-examples.md` line 4 says `Status: In Progress`; line 169 says `Status: Complete`. Content is complete. Reconcile the line-4 header to `Complete`.
- **G3 — Step 2 design fork left open (acceptable).** The "ADD 5 fields to Output Contract" vs "synthesize via adapter shim" decision is surfaced by both R2 (§B3, recommends ADD) and R3 (§4.2) but not finalized. This is appropriate research scoping; the builder should pick one branch and write items accordingly. Not a true gap — recorded for the builder's awareness so the contract-version bump (SKILL.md:62, NFR-6) is included if the ADD branch is chosen.
- **G4 — Stale `--caller task-unified` literal.** R3 §1D flags `--caller task-unified` at sc-task-protocol/SKILL.md:212 as a stale caller-id worth reconsidering during the swap. Builder should confirm whether the migrated dispatch keeps `task-unified` or updates it (the skill is now `sc-task-protocol`); ensure the adapter's `--caller` value and troubleshoot's expected value agree (ties to Step 3).
