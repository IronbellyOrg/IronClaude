# Research 05 — Template Rules & Citation Anchors

**Status: In Progress**
**Date: 2026-06-21**
**Topic:** MDTM template-02 rules + verbatim citation anchors for TASK-RF (FR-RH2 R6: wire adversarial seam → build_reflect_contract)

---

## SECTION 1 — MDTM Template-02 Rules the Builder MUST Follow

**Source template (PART 1, lines 68–1127):** `.claude/templates/workflow/02_mdtm_template_complex_task.md`
This is the COMPLEX task template (extends Template 01 with Section L handoff patterns). Use it when tasks require discovery, testing, review, conditional logic, or aggregation between items (template:78-80). The R6 task is code-modifying with adversarial-seam wiring + tests → this template applies.

### 1.1 Required / Mandatory Sections (Section D, lines 250–289)
- `## MANDATORY WORKFLOW COMPLIANCE` — informational only, NO checklist items (D1, template:255-262). [WORKFLOW-DEPENDENT — omit if no `.gfdoc/workflows/` governing doc; see A1 template:89-100. This repo has none → replace with direct requirements.]
- `## Cross-Stage Integration Requirements` — informational only, NO checklist items (D2, template:264-284).
- **D3 CRITICAL RULE (template:286-289):** "NO CHECKLIST ITEMS may appear before Phase 1 begins." Order: Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable). All context-review / previous-stage-input items live IN Phase 1, Steps 1.2–1.4.

### 1.2 B2 Self-Contained Item Pattern (Section B, lines 159–214) — THE core rule
Every checklist item MUST be a complete, self-contained ONE-PARAGRAPH prompt (B3 template:167-170) embedding all 6 elements (B2 template:159-166), VERBATIM:
> 1. **Context Reference with WHY** - What file(s) to read and why that context is needed for this specific action
> 2. **Action with WHY** - What to do with that context and why it needs to be done
> 3. **Output Specification** - The exact output file name, location, what content to produce, and template to follow (if applicable)
> 4. **Integrated Verification** - An "ensuring..." clause that specifies what must be verified (DO NOT assume, hallucinate, or make up any information - all content MUST be derived from source files referenced in the checklist item, 100% accuracy based on source materials, document negative evidence when verification fails)
> 5. **Evidence on Failure Only** - Log to task notes ONLY if unable to complete due to blockers, missing info, or errors (successful completion is evidenced by the output file itself)
> 6. **Explicit Completion Gate** - "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

- **Completion-gate boilerplate** (J1 template:850-854): "If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."
- **B5 FORBIDDEN (template:181-200):** standalone "read context" items with no output; missing-context items; multi-line/bulleted items; SEPARATE verification/confirmation items; overly-granular ("create directory" alone); REMINDER blocks between items.
- **C1–C3 (template:223-240):** Outputs, Success Criteria, and Verification are EMBEDDED in the action item (the "ensuring…" clause) — NEVER separate sections or separate items.

### 1.3 A3 Granular-Breakdown Rule (lines 108–112), VERBATIM
> A3. COMPLETE GRANULAR BREAKDOWN
>    - Break down EVERY workflow phase into atomic, verifiable checklist items
>    - Create individual checklist items for EVERY file, component, or iteration
>    - NO high-level or bulk operations allowed - everything must be granular
>    - Include exact file paths, specific requirements, and measurable outcomes

Reinforced by E1 (flat checkboxes, no nesting, no parent-summary-before-children; template:295-309) and E2 (summary/parent checkboxes come AFTER component items; template:311-365).

### 1.4 M3 Lens-Based QA Sequence (lines 1059–1096) — the mandatory QA gate shape
M3 REPLACES the deprecated M1 single-agent gate (template:1034-1045). Every phase-gate QA checkpoint AND post-completion validation MUST use M3. The 8 steps (template:1062-1090), each an explicit `- [ ]` item (template:1096 "EVERY step above … MUST be an explicit `- [ ]` checklist item"):
1. **Aggregation (L6)** — collect preceding-phase outputs (Glob).
2. **Structural Lens Agents (PARALLEL)** — rf-qa, one per lens, `fix_authorization: false`, reports to `${TASK_DIR}qa/qa-structural-[lens]-report.md`.
3. **Content Lens Agents (PARALLEL)** — rf-qa-qualitative, one per lens, `fix_authorization: false`, reports to `${TASK_DIR}qa/qa-content-[lens]-report.md`. (Steps 2+3 MAY share one parallel batch.)
4. **Domain-Specific Lens Agents (PARALLEL, if applicable)**.
5. **Findings Consolidation** → `${TASK_DIR}qa/qa-consolidated-findings.md` (dedup, severity CRITICAL/IMPORTANT/MINOR + originating lens).
6. **Fix Agent** — ONE rf-qa with `fix_authorization: true`, applies ALL fixes.
7. **Verification Round (PARALLEL)** — min 2 (1 rf-qa + 1 rf-qa-qualitative), `fix_authorization: false` → `qa-verification-structural-report.md` + `qa-verification-content-report.md`.
8. **Conditional Proceed (L5)** — both PASS → proceed; else repeat 5–7 (max cycles per I16).
- Adversarial framing on EVERY lens agent (template:729, 1068): "Assume this document has at least N errors focused on [lens]. Find them." (N: 5 for <500 lines, 10 for 500-1500, 15 for 1500-3000, 20 for >3000).
- Serialized fix protocol I20 (template:745-757) applies at ALL intensity levels: report → consolidate → fix → verify. Parallel fix authorization is PROHIBITED.

### 1.5 I19 / I22 Agent-Count Floors (lines 699–741, 793–840)
**I19 (FULL intensity floors), Final/Assembled-Output QA (template:704-711), VERBATIM:**
> | Output Size | rf-qa Agents (structural lenses) | rf-qa-qualitative Agents (content lenses) | Total Minimum |
> | <500 lines | 3 | 3 | 6 |
> | 500-1500 lines | 4 | 4 | 8 |
> | 1500-3000 lines | 5 | 5 | 10 |
> | >3000 lines | 6 | 6 | 12 |

**I19 Intermediate Gate Minimums (template:733-737), VERBATIM:**
> | Research gate (Phase 3) | 5 | 2 rf-analyst (completeness + cross-validation) + 2 rf-qa (evidence-quality + gap-detection) + 1 rf-qa-qualitative (research-depth) |
> | Synthesis gate (Phase 5) | 5 | 2 rf-analyst (synthesis-accuracy + source-tracing) + 2 rf-qa (structure + content-quality) + 1 rf-qa-qualitative (synthesis coherence) |
> | task-integrity (Phase 5.5) | 5 | 2 rf-qa (structure + evidence-quality) + 2 rf-qa-qualitative (actionability + domain-accuracy) + 1 rf-analyst (completeness) |

**I22 intensity scaling (template:800-804) — the builder selects per qa_intensity:**
> | **lite** | … | 2 (1 rf-qa + 1 rf-qa-qualitative) | 3 (1 structural + 1 content + 1 domain) | 1 agent (combined lenses) | 1 max per gate | 1 |
> | **standard** | … | 3 (1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative) | 7 (3 structural + 3 content + 1 domain) | 2 agents | 2 max per gate | 2 |
> | **full** | … | Per I19 tables (5+ intermediate, 6-12+ final) | Per I19 tables + all domain lenses | Per I21 (2-8 agents) | Per I16 (2-3 per gate) | 2 |

Default mapping (template:806-809): Quick/Lightweight→lite; Standard→standard; Deep/Heavyweight→full.
**Hard prohibition (I15 template:638):** "QA gates using only 1-2 agents are PROHIBITED. For FINAL DOCUMENT / ASSEMBLED OUTPUT QA gates, the absolute minimum is 6 agents … For INTERMEDIATE gates … the absolute minimum is 5 agents … Gates with fewer than these floors will be REJECTED during task file validation."

### 1.6 I18 Testing Requirement for Code-Modifying Tasks (lines 688–697)
R6 modifies `ensemble.py`/`contract.py` (source code), so I18 MANDATES ≥1 testing item using the **L3 Test/Execute pattern** (template:695): specify test command (e.g. `uv run pytest tests/cli/reflect/ -v`), define pass criteria (all pass, no regressions), capture results to a test-results file in `phase-outputs/`, follow B2.

### 1.7 I17 Post-Completion Validation (lines 675–686)
Before status→Done, MUST include items verifying: all `- [ ]`→`- [x]`; all output files exist (Glob); blocker entries have resolution notes; **if code modified: all relevant tests pass**; **lens-based QA per M3 on final outputs (mandatory)**; source-fidelity per M4 (only if source-derived — for a code-wiring task M4 is generally NOT required, see I21 template:773-775). These appear in `## Post-Completion Actions` BEFORE the frontmatter-update item.

---

## SECTION 2 — Frontmatter Shape + POST Reflect Wrapper Item

### 2.1 Frontmatter shape (template:1–61 + actual prior-task practice)
Template base (`02_mdtm_template_complex_task.md:1-61`) defines: `id`, `title`, `description`, `status` (🟡 To Do / 🟠 Doing / 🟢 Done …), `type` (enum at template:8), `priority`, `created_date`, `updated_date`, `parent_doc`, `parent_task`, `depends_on`, `spec_path` (template:23 "driving spec/PRD/TDD path; populated by task-builder (A.2)"), `reflect_pre:` block (template:24-31), `reflect_post:` (template:32), `task_type: static` (template:60).

The PRIOR FR-RH2 task ADDS two builder-convention fields the R6 task MUST mirror — VERBATIM from `TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md`:
> id: "TASK-RF-fr-rh2-headless-ensemble-20260620-024238"   (line 2)
> parent_doc: ".dev/reflect-hardening/issue-2-headless-ensemble/spec.md"   (line 15)
> spec_path: ".dev/reflect-hardening/issue-2-headless-ensemble/spec.md"   (line 18)
> start_commit: "63f1a8153d2375e48369059c253dc2a76f73c063"   (line 19)
> executor_model_class: "sonnet"   (line 20)
> # reflect_post: written back by the O1 reflect wrapper after the final-phase POST reflect gate runs — do NOT hand-author or lock.   (line 31)
> task_type: static   (line 59)
> reflect_post:   (line 60 — block written back by the wrapper, NOT hand-authored)

Builder notes: set `id` to `TASK-RF-ensemble-adversarial-seam-<NEW-STAMP>`; `start_commit` to the new HEAD at build time; `parent_task` to `TASK-RF-fr-rh2-headless-ensemble-20260620-024238` (R6 is its follow-up); keep `spec_path`/`parent_doc` pointing at the FR-RH2 spec; leave `reflect_post:` for the wrapper to write back (the `# do NOT hand-author or lock` comment must be preserved).

### 2.2 POST reflect wrapper item (penultimate final-phase item) — VERBATIM from prior task
Stated rule (`TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md:148`):
> **POST reflect gate ENABLED:** the penultimate final-phase item shells out `superclaude reflect run <TASK_FILE> --depth deep --fix --promote` behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker skip guard; only exit 0 proceeds (10/11/2 FAIL + surface + HALT).

The actual encoded item (`TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md:483`) — copy this as the R6 template, swapping the TASK_FILE path to the new task file:
> - [ ] **POST reflect gate (penultimate — runs AFTER the QA gate passes and the Task Summary is written, BEFORE the status-to-Done item).** First check the environment variable `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`: IF it is already set to a truthy value, this task is itself running inside a reflect wrapper — SKIP the shell-out entirely (the recursion-breaker), note "POST reflect skipped: SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE already set (recursion-breaker)" in the ### Phase Gate Findings section, and mark this item complete. OTHERWISE, run the flat wrapper shell-out `superclaude reflect run <TASK_FILE_PATH> --depth deep --fix --promote` (NO `--base`, NO `--reflect`, NO `<base>..HEAD`, NO agent-spawn tokens — this is the flat wrapper form behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard), capturing the output and exit code to `post-reflect-output.txt` at `…/phase-outputs/test-results/post-reflect-output.txt`, then CONSUME the exit code: ONLY exit code `0` permits proceeding to the status-to-Done item; exit code `10` (HALTED), `11` (DEGRADED), or `2` (BLOCKED) is a FAIL — surface the verdict and the wrapper output, write a HALT entry to the ### Phase Gate Findings section with the exit code and reason, set the frontmatter `status` to "🔴 Blocked" with a `blocker_reason` referencing the POST reflect verdict, and HALT (do NOT mark the task Done). Ensuring the recursion-breaker guard is honored, the wrapper is the flat form (no diff-range / agent tokens), only exit 0 proceeds, and any non-zero exit blocks completion. If the wrapper cannot be invoked, log the blocker in the ### Phase Gate Findings section and HALT (do NOT mark Done). Once exit 0 is confirmed (or the recursion-breaker skip applies), mark this item complete.

Exit-code map (must match the reflect verdict map): `pass→0`, `halted→10`, `degraded→11`, `blocked→2`.

---

## SECTION 3 — Ready-to-Paste Citation Anchors (path:line + verbatim quote)

These are the EXACT anchors the generated task MUST cite in its Execution Context / item Context fields. All paths are repo-root-relative to the worktree `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/`.

### 3.1 Spec — FR-RH2.7 "derive_verdict … unchanged" acceptance bullet
**`.dev/reflect-hardening/issue-2-headless-ensemble/spec.md:303`**
> - [ ] `derive_verdict` and the `Verdict` exit-code map (`pass→0`, `halted→10`, `degraded→11`, `blocked→2`) are unchanged.

FR-RH2.7 full description (`spec.md:295-299`):
> ### FR-RH2.7: Downstream return-contract consumers are unaffected
> **Description**: The reflect `return-contract.yaml` shape and the derived `reflect_post:` write-back + `wrapper-result.yaml` sidecar MUST remain compatible: existing fields keep their names/semantics; the verdict map and exit codes (`contract.py`, `models.py`) are unchanged.

FR-RH2.7 companion bullets (`spec.md:304-305`):
> - [ ] `write_reflect_post` produces the same `reflect_post:` field set/order; the sidecar keeps its fields.
> - [ ] Existing reflect contract/verdict tests pass without modification.

**Builder use:** R6 wires the adversarial verdict INTO `build_reflect_contract`'s output, but MUST NOT rename/retype/re-semanticize any existing contract field, and MUST keep `derive_verdict` + the exit-code map byte-identical. This is the hard backward-compat constraint on the R6 fix.

### 3.2 Spec — adversarial seam / Phase C→D consumes the adversarial verdict
**FR-RH2.3 (`spec.md:212-222`)** — the seam the QA CRITICAL #2 says is under-wired:
> ### FR-RH2.3: Swarm normalized artifacts are scored by sc-adversarial-protocol Mode A (not swarm merge)
> **Description**: Reflect MUST consume the N normalized per-reviewer artifacts (swarm `final_path`s) as the input to its existing `sc-adversarial-protocol` Mode A merge. Swarm's `mechanical_merge` (`merge.py`) output MUST NOT be treated as the adversarial verdict.
> **Acceptance Criteria**:
> - [ ] The downstream merge step consumes swarm's per-reviewer `final_path` artifacts (suspect-aware).
> - [ ] No scoring/ranking/dedup logic is added to `swarm/merge.py` (the LOC ceiling + boundary tests stay green).
> - [ ] The adversarial merge produces a convergence score recorded on the reflect contract.

**§2.2 dataflow — Phase (3)→(4), the adversarial verdict the reflect contract must consume (`spec.md:166-175`):**
> ├─(3) /sc:adversarial  (sc-adversarial-protocol Mode A)  ── DOWNSTREAM SCORER ──
> │       │   consumes the N normalized per-reviewer artifacts (suspect-aware)
> │       ▼
> │   adversarial merge verdict + convergence score
> │
> ├─(4) reflect derive_verdict (contract.py, UNCHANGED) over the assembled return-contract.yaml:
> │        tier_reached=2 ; merge_method != single-reviewer-fallback ;
> │        reviewer_count>=2 ; t2_model_class_diversity=full
> │
> └─(5) write_reflect_post + wrapper-result.yaml sidecar (runner.py, UNCHANGED)

**§5.3 contract-fields anchor (`spec.md:437-442`):**
> consumed_by: [contract.derive_verdict, runner.write_reflect_post, runner.write_sidecar]
> verdict_map_unchanged: {pass: 0, halted: 10, degraded: 11, blocked: 2}
> reflect_contract: "<output_dir>/return-contract.yaml"          # the ONLY file reflect.derive_verdict parses

**Builder use:** R6's job is to make Phase (3)'s "adversarial merge verdict" (deviations/regression/human-decision, not just a float) flow into Phase (4)'s `derive_verdict` via `build_reflect_contract`, while keeping (4)/(5) byte-unchanged (FR-RH2.7).

### 3.3 OI-1 mapping table — VERBATIM rows for the four hard-coded fields
**Source: `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/phase-outputs/discovery/oi1-mapping-table-validated.md`** (validated artifact, Status: Complete at line 64).

`deviation_count_by_class` (`oi1-mapping-table-validated.md:35`):
> | `deviation_count_by_class` | `_extract_deviations` `contract.py:90-101`; result via `contract.py:121`; halted `contract.py:323-326` | SYNTHESIZED | Emit `{}`/zero-equivalent inert default unless the adversarial/reflect domain supplies counts. No swarm equivalent. |

`regression_present` (`oi1-mapping-table-validated.md:38`):
> | `regression_present` | bool shape `contract.py:47-57`, `contract.py:200-206`; halted `contract.py:315` | SYNTHESIZED | Omit or emit an explicit boolean only if the downstream adversarial/reflect domain produces it. No swarm equivalent. |

`unauthorized_deviation_present` (`oi1-mapping-table-validated.md:39`):
> | `unauthorized_deviation_present` | bool shape `contract.py:47-57`, `contract.py:200-206`; halted `contract.py:317` | SYNTHESIZED | Omit or emit an explicit boolean only if the downstream adversarial/reflect domain produces it. No swarm equivalent. |

`needs_human_decision` (`oi1-mapping-table-validated.md:40`):
> | `needs_human_decision` | bool shape `contract.py:47-57`, `contract.py:200-206`; halted `contract.py:319` | SYNTHESIZED | Omit or emit an explicit boolean only if the downstream adversarial/reflect domain produces it. No swarm equivalent. |

Closely related (adversarial seam DERIVED/MAPPED fields R6 will also touch):
`adversarial_convergence_score` (`oi1-mapping-table-validated.md:49`):
> | `adversarial_convergence_score` | degraded `contract.py:283-285` | MAPPED | Map from the adversarial child `convergence_score`, renaming it to reflect's `adversarial_convergence_score`. … `None` is only the graceful failure path and triggers null-convergence when `tier_reached == 2`. |
`adversarial_unavailable` (`oi1-mapping-table-validated.md:42`):
> | `adversarial_unavailable` | bool shape `contract.py:47-57`, `contract.py:200-206`; degraded `contract.py:275-277` | DERIVED | Derive from the adversarial child launch/parse outcome. … If adversarial scoring cannot run, set `True` so `derive_verdict` routes `adversarial-unavailable`. |

**The governing rule (the "SYNTHESIZED … unless the adversarial/reflect domain supplies counts. No swarm equivalent." rule):** each of the four fields is SYNTHESIZED (inert default `{}`/`False`) ONLY because, at FR-RH2's resolution time, the adversarial domain did NOT supply counts. R6's PURPOSE is to make the adversarial/reflect domain supply them — at which point the OI-1 rule's own conditional clause ("unless the adversarial/reflect domain supplies counts") flips them from SYNTHESIZED-inert to DERIVED-from-adversarial.

### 3.4 QA CRITICAL #2 — the build_reflect_contract hard-codes finding (the R6 driver), VERBATIM
**Source: `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/qa/qa-content-ensemble-formation-correctness-report.md:39`** (Issues Found table, row #2, severity CRITICAL):
> | 2 | CRITICAL | `src/superclaude/cli/reflect/ensemble.py:64-65, 194-205, 301-320, 384-390`; `src/superclaude/cli/reflect/runner.py:92-116, 190-224`; Spec §2.2/§5.3 | The adversarial scorer output is reduced to `adversarial_convergence_score` only. `build_reflect_contract` hard-codes `deviation_count_by_class` to all zeros, `regression_present=False`, `unauthorized_deviation_present=False`, `needs_human_decision=False`, and `degraded_components=[]`, and `_select_report_path` chooses swarm `merged.md` when present. `write_reflect_post` and `write_sidecar` then publish that mechanical merged report path. A real adversarial finding or human-decision result has no path into the final reflect verdict, so a run can PASS on formation telemetry while ignoring the adversarial verdict the spec says Phase C -> D must consume. | Change the adversarial seam to return/parse the adversarial contract or result object, not only a float. Map adversarial deviation counts, regression/unauthorized/human-decision booleans, degraded components, and adversarial report path into the reflect contract. Do not set `report_path` to swarm `merged.md` for a faithful adversarial run; keep `merged.md` only as a subrun artifact. Add a test where the adversarial seam reports a regression/human-decision and verify `derive_verdict` does not PASS. |

**Recommended fix (report Recommendations 2 + 5, `qa-content-ensemble-formation-correctness-report.md:64, 67`):**
> 2. Expand the adversarial seam from "score-only" to "adversarial result contract/report," and map findings/deviation booleans into the final reflect contract before `derive_verdict`.
> 5. Add a negative adversarial-result integration test: scorer reports a regression or human decision; final `derive_verdict` must not PASS.

Supporting Items-Reviewed row #7 (`…report.md:29`):
> | 7 | … | PASS for formation fields / FAIL for adversarial semantics | … adversarial outcome semantics are not computed: only a float score can cross the `adversarial_score_fn` seam (`ensemble.py:64-65, 194-205`), while deviations and booleans are hard-coded clean in `ensemble.py:301-320`. |

The report's overall verdict is **FAIL** (`…report.md:10`) and the seam defect is failure point #2 in the summary (`…report.md:15`):
> 2. the downstream adversarial result is reduced to a float score only while the final reflect contract hard-codes all deviation/finding fields to clean values and points `report_path` at swarm `merged.md`, not an adversarial verdict/report.

### 3.5 Consolidated R6 finding — the cross-task tension the builder MUST resolve
**Source: `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/qa/qa-consolidated-findings.md:84-85`** — note this lives in the **"REJECTED — with rationale"** section (header at line 56), VERBATIM:
> - **R6. deviation_count_by_class hard-coded zero (spec #3).** SYNTHESIZED per the
>   validated table ("zero-equivalent inert default ... No swarm equivalent").

**CRITICAL interpretation for the builder:** Within the SCOPE of the prior FR-RH2 task, R6 was REJECTED as a defect — the hard-coded zero was correct-by-the-OI-1-table *because the adversarial domain did not yet supply counts*. The per-lens QA report's CRITICAL #2 (§3.4 above) flagged the SAME code as a real semantic gap. The two are not contradictory: the consolidated finding scopes R6 to "not a defect against THIS task's oracle"; the new R6 follow-up task's PURPOSE is to change that oracle — i.e. wire the adversarial domain to actually supply the counts, flipping the OI-1 conditional. The new task MUST cite BOTH (the OI-1 SYNTHESIZED rule's conditional clause + the consolidated R6 rejection rationale) so it is explicit that R6 is a deliberate scope-expansion follow-up, not a re-litigation of a closed finding.

Related rejected rows for scoping awareness:
- R5 (`qa-consolidated-findings.md:81-83`): `report_path` using swarm `merged_path` was table-faithful in FR-RH2 — but QA CRITICAL #2's fix says for a *faithful adversarial run* `report_path` should be the adversarial verdict/report, "keep `merged.md` only as a subrun artifact." R6 should align `report_path` selection with the now-available adversarial report.
- R3 (`qa-consolidated-findings.md:68-72`): adversarial-child failure → score=None → null-convergence DEGRADE (exit 11), NOT `adversarial_unavailable`. R6's new finding-mapping must preserve this null-convergence fallback.

---

## SECTION 4 — Summary for the Builder

**Template:** Use `.claude/templates/workflow/02_mdtm_template_complex_task.md` (complex). Key rules to honor: B2 6-element self-contained one-paragraph items (template:159-214); A3 granular per-file/per-component breakdown (template:108-112); E1/E2 flat checkboxes, summary-after-components (template:295-365); D3 no checklist items before Phase 1 (template:286-289); M3 lens-based QA gate as 8 explicit `- [ ]` items (template:1059-1096); I20 serialized fix (template:745-757); I19/I22 agent-count floors (template:699-741, 793-840 — pick intensity by tier, code-wiring R6 is small so likely standard→7-agent final gate or full per operator); I18 mandatory L3 test item since code changes (template:688-697); I17 post-completion validation incl. M3 on final outputs (template:675-686).

**Frontmatter:** Mirror prior task — add `start_commit` (new HEAD), `executor_model_class: "sonnet"`, `parent_task: TASK-RF-fr-rh2-headless-ensemble-20260620-024238`, `spec_path`/`parent_doc` = FR-RH2 spec, leave `reflect_post:` block for the wrapper (`# do NOT hand-author or lock`).

**POST reflect wrapper:** Copy the penultimate-item shape verbatim (prior task line 483) with the new TASK_FILE path: flat `superclaude reflect run <TASK_FILE> --depth deep --fix --promote` behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard; only exit 0 proceeds; 10/11/2 → FAIL + surface + HALT.

**The four citation anchors the task MUST cite (path:line):**
1. `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md:303` — FR-RH2.7 "derive_verdict … unchanged" (the backward-compat constraint).
2. `…/spec.md:166-175` + `:212-222` + `:437-442` — §2.2 Phase (3)→(4) adversarial-verdict consumption + FR-RH2.3 + §5.3 consumed_by/verdict_map.
3. `…/phase-outputs/discovery/oi1-mapping-table-validated.md:35,38,39,40` — the four SYNTHESIZED rows (deviation_count_by_class, regression_present, unauthorized_deviation_present, needs_human_decision) with the "unless the adversarial/reflect domain supplies counts. No swarm equivalent." conditional clause.
4. `…/qa/qa-content-ensemble-formation-correctness-report.md:39` — QA CRITICAL #2 (build_reflect_contract hard-codes the finding fields; recommended fix = map adversarial result into the contract + negative test). Plus consolidated `…/qa/qa-consolidated-findings.md:84-85` (R6 rejection rationale — proves R6 is a deliberate scope-expansion follow-up, not re-litigation).

**The load-bearing tension to encode:** The OI-1 table and consolidated R6 both call the hard-coded zeros *correct within FR-RH2's scope*; QA CRITICAL #2 calls the same code a real semantic gap. The R6 follow-up resolves this by changing the oracle — wiring the adversarial domain to supply real counts (flipping the OI-1 conditional clause) — while preserving FR-RH2.7 (no contract field rename/retype, `derive_verdict` + exit-code map byte-unchanged) and the R3 null-convergence fallback.

---

**Status: Complete**

**Findings summary:** Extracted the full MDTM template-02 PART 1 ruleset (B2 self-contained pattern, A3 granular breakdown, M3 lens-QA sequence, I17/I18/I19/I22 floors, frontmatter shape) plus the prior FR-RH2 task's two convention fields (`start_commit`, `executor_model_class`) and the verbatim penultimate POST-reflect-wrapper item. Pulled the four exact citation anchors with line numbers and verbatim quotes: FR-RH2.7 derive_verdict-unchanged bullet (spec.md:303), the §2.2/FR-RH2.3/§5.3 adversarial-seam anchors, the four OI-1 SYNTHESIZED rows with the "unless the adversarial/reflect domain supplies counts" conditional, and QA CRITICAL #2 (ensemble.py:64-65,194-205,301-320 + the recommended fix). Flagged the key tension: the consolidated R6 is in the REJECTED section (correct-within-FR-RH2-scope), so the new task must cite both it and OI-1 to frame R6 as a deliberate scope-expansion follow-up, not re-litigation — while preserving FR-RH2.7 backward-compat and the R3 null-convergence fallback.
