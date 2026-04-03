---
convergence_score: 0.78
rounds_completed: 1
---

# Structured Adversarial Debate: PRD Skill Refactoring Roadmap

## Round 1 — Key Divergence Points

---

### Divergence 1: Timeline (4.5–7 hours vs. 3.5–4.5 days)

**Variant A (Opus) — Position:**
This is a mechanical decomposition, not a design task. The fidelity index already exists with line ranges, destination mappings, and first/last markers for all 30 blocks. The work is: copy content to 4 new files, remove it from SKILL.md, update 6 path references, verify with diffs and greps. Every verification step is automatable. A skilled implementer with the fidelity index open in a split pane completes this in a focused session. Multi-day estimates introduce context-switching overhead that *increases* risk of content drift — the fewer sessions this spans, the fewer opportunities for the baseline to shift under you (Risk #7). The 4.5–7 hour estimate accounts for careful verification, not just raw editing speed.

**Variant B (Haiku) — Position:**
The 3.5–4.5 day estimate accounts for independent review gates that catch errors the implementer's own verification misses. Fidelity verification is not trivial — diffing 8 agent prompts across ~415 lines requires careful attention, not just running `diff`. The multi-day timeline also provides buffer for the E2E behavioral regression test (NFR-PRD-R.4), which requires actually invoking the PRD skill end-to-end, waiting for subagent execution, and comparing outputs. That alone can take hours depending on the environment. Additionally, if any open question requires stakeholder input, a same-day timeline collapses.

**Assessment:**
Opus has the stronger position. The work is fundamentally copy-paste-verify with a pre-built fidelity index. The E2E test is a valid time concern, but it's a single task within Phase 4, not a reason to inflate the entire timeline to days. Haiku's estimate is calibrated for a multi-person team with formal review gates — appropriate for an organization that requires them, but not inherent to the task's complexity. **Convergence: Opus's hours-scale estimate is more realistic for the mechanical nature of this work, but should include a +2 hour buffer for E2E testing.**

---

### Divergence 2: B05/B30 Merge Phase Assignment (Phase 3 vs. Phase 1)

**Variant A (Opus) — Position:**
The B05/B30 merge modifies the Artifact Locations table, which is a behavioral block (B05) that *stays in SKILL.md*. It does not move to any refs/ file. Therefore, it belongs in Phase 3 (SKILL.md restructuring), where all SKILL.md modifications happen. Performing it in Phase 1 (refs/ creation) would require editing SKILL.md before the extraction phase completes, creating a confusing ordering dependency — you'd be modifying the file you're simultaneously extracting from.

**Variant B (Haiku) — Position:**
If any refs/ file references content from B30 (QA artifact paths), the merged table needs to exist before refs/ files can reference it correctly. Performing the merge in Phase 1 ensures refs/ files are created against a stable, finalized content set. Additionally, Phase 1 is about materializing all content in its final form — the merge is a content operation, not a structural SKILL.md operation.

**Assessment:**
Opus has the stronger position. B30's QA paths are being appended to B05's table in SKILL.md — neither B05 nor B30 moves to refs/. No refs/ file references the Artifact Locations table. The merge is purely a SKILL.md-internal operation and belongs with other SKILL.md modifications in Phase 3. Haiku's concern about refs/ files referencing merged content is hypothetical and not supported by the fidelity index. **Convergence: Phase 3 is the correct placement.**

---

### Divergence 3: Open Question Resolution Authority (Inline vs. Deferred)

**Variant A (Opus) — Position:**
Three of the four open questions have obvious answers that don't require stakeholder input. OQ-3 (fidelity index existence) is confirmed resolved — the file exists. OQ-4 (whitespace normalization) has a clear best practice: allow trailing whitespace and line-ending normalization, disallow indentation and blank-line changes. OQ-1 (token vs. line ceiling) is answerable by reading the spec's own language — 500 lines is a "hard ceiling" while 2,000 tokens is a "soft target." Deferring these creates artificial blockers that stall progress on questions with deterministic answers.

**Variant B (Haiku) — Position:**
A roadmap should not presume to make decisions that belong to the spec author or project lead. Even if the answers seem obvious, documenting them as "requiring sign-off" creates an explicit decision record. If the implementer guesses wrong on OQ-1 and builds to 495 lines at 2,227 tokens, and the stakeholder actually wanted strict token compliance, the rework costs more than a brief sign-off conversation. The conservative approach protects against assumption failures.

**Assessment:**
Split verdict. Opus is right that OQ-3 is definitively resolved and OQ-4 has a clear best practice. Haiku is right that OQ-1 (token vs. line precedence) is a policy decision that could reasonably go either way — "soft target" is Opus's interpretation, not the spec's explicit language. **Convergence: Resolve OQ-3 and OQ-4 inline per Opus. Flag OQ-1 as requiring explicit confirmation before Phase 3 line-count validation. OQ-2 is already resolved by both (coexistence accepted).**

---

### Divergence 4: Staffing Model (Single Implementer vs. 3-Role Team)

**Variant A (Opus) — Position:**
Every verification step in this task is automatable: `diff`, `grep`, `wc -l`. A single implementer running these commands gets the same fidelity assurance as a separate reviewer running them. The value of an independent reviewer comes from *judgment calls* — but there are no judgment calls here. Either the diff is zero or it isn't. Either the line count is 430–500 or it isn't. Adding a reviewer and optional QA person triples coordination overhead for a task with binary pass/fail criteria.

**Variant B (Haiku) — Position:**
Independent review catches classes of errors that self-verification misses: subtle content drift in markdown rendering that doesn't appear in raw diffs, incorrect loading declaration scoping that passes grep but fails semantically, and E2E behavioral regressions that require a fresh perspective to notice. The reviewer role is also a knowledge-sharing mechanism — ensuring more than one person understands the decomposed architecture.

**Assessment:**
Opus has the stronger position for this specific task. The verification criteria are fully automatable with binary outcomes. Haiku's concerns about "subtle content drift in markdown rendering" are valid in general but mitigated here by the word-for-word fidelity requirement — if the diff is zero, the rendering is identical. Knowledge sharing is a valid organizational concern but not a roadmap execution concern. **Convergence: Single implementer is sufficient. If organizational policy requires review, add it as a gate between Phase 3 and Phase 4, not as a separate role throughout.**

---

### Divergence 5: Parallelism Guidance

**Variant A (Opus) — Position:**
Tasks 2.1–2.3 (creating agent-prompts.md, synthesis-mapping.md, validation-checklists.md) are independent extractions from non-overlapping line ranges. They can be executed in parallel. Task 2.4 (build-request-template.md) depends on knowing the destination paths from 2.1–2.3 for the SKILL CONTEXT FILE updates. This sequencing analysis is critical for the hours-scale timeline — parallel extraction is the throughput multiplier.

**Variant B (Haiku) — Position:**
Tasks are listed sequentially. No parallelism analysis provided.

**Assessment:**
Opus is unambiguously stronger. The parallelism analysis is correct — tasks 2.1–2.3 extract from independent, non-overlapping line ranges and have no data dependencies. Omitting this analysis is a missed optimization. **Convergence: Adopt Opus's parallelism guidance.**

---

### Divergence 6: Evidence Artifacts and Risk Burn-Down

**Variant A (Opus) — Position:**
Evidence is a natural byproduct of the verification tasks in Phase 4. The 12-criterion validation table specifies exactly what commands to run and what outputs to expect. Capturing those outputs *is* the evidence. A separate evidence artifact specification is redundant with the success criteria table.

**Variant B (Haiku) — Position:**
Explicitly naming 4 evidence artifact types (fidelity index, diff logs, grep outputs, E2E transcript) creates an auditable deliverables list. Risk burn-down checkpoints (risks 1/5/6 retired after Phase 1, risks 2/3 after Phase 2, risks 4/7 after Phase 3) provide progress visibility. An implementer finishing Phase 1 should know exactly which risks are now retired, not have to mentally trace through the risk table.

**Assessment:**
Haiku adds genuine value here. Opus's success criteria table is more actionable as a runsheet, but Haiku's risk burn-down checkpoints and explicit evidence list complement rather than replace it. **Convergence: Adopt Opus's success criteria table as the primary validation runsheet. Add Haiku's risk burn-down checkpoints as annotations on phase exit criteria. Explicitly name evidence artifacts in Phase 4.**

---

## Convergence Assessment

### Areas of Agreement (Strong Convergence)
- Complexity rating, output structure, line count targets, token budget, content preservation mandate, BUILD_REQUEST changes, loading point, max concurrent refs, atomic commit, component sync, risk inventory, B05/B30 merge strategy, reference implementation — all 14 shared assumptions hold.
- Both agree on the fundamental architecture: SKILL.md as behavioral spine, 4 refs/ files, lazy loading at A.7.

### Resolved in Favor of Variant A (Opus)
1. **Timeline**: Hours-scale (with +2h E2E buffer), not days
2. **B05/B30 merge phase**: Phase 3 (SKILL.md restructuring)
3. **Staffing**: Single implementer with automatable verification
4. **Parallelism**: Tasks 2.1–2.3 parallel, 2.4 sequential after
5. **Open question resolution**: Inline for OQ-2/3/4; flag OQ-1 for confirmation
6. **Frontmatter completeness**: Machine-readable metadata
7. **Dispatch tables**: Tabular integration point documentation

### Resolved in Favor of Variant B (Haiku)
1. **Risk burn-down checkpoints**: Phase-linked risk retirement schedule
2. **Evidence artifact specification**: Explicit named deliverables list
3. **Fidelity index as integration point**: IP-3 recognition

### Remaining Disputes
1. **OQ-1 resolution authority**: Whether 500-line hard ceiling / 2,000-token soft target is self-evident from the spec or requires explicit stakeholder confirmation. Low-stakes — either approach works if documented.

### Recommended Synthesis
Use Opus as the base roadmap. Incorporate from Haiku: risk burn-down checkpoints on each phase's exit criteria, explicit evidence artifact names in Phase 4, and IP-3 (fidelity index) in the integration point registry. Resolve OQ-1 inline with Opus's recommendation but flag it as an assumption that the implementer should confirm if challenged.
