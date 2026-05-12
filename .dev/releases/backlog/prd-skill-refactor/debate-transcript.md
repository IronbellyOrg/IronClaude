---
convergence_score: 0.72
rounds_completed: 2
---

# Structured Adversarial Debate: PRD Skill Refactoring Roadmap

## Divergence Points Under Debate

Four contested areas from the diff analysis:

1. **Phase 0 necessity** — explicit baseline/governance phase vs. implicit git baseline
2. **Refs verification ordering** — verify-first (blocking) vs. verify-during (integrated)
3. **Granularity level** — 47-step checklist vs. 20-action plan
4. **Effort expression** — concrete hours vs. abstract Sprint Slots

---

## Round 1: Initial Positions

### D1: Phase 0 Necessity

**Variant A (Opus):**
Phase 0 is ceremony without substance for this task. Git HEAD *is* the baseline — it's immutable, versioned, and recoverable with a single command. Adding an explicit "baseline lock" phase means creating artifacts (acceptance matrices, governance checkpoints) that duplicate what git already provides. The spec scores this at 0.45 complexity with a solo implementer. Every minute spent on governance setup is a minute not spent on the actual decomposition. My rollback plan is one line: `git checkout -- .claude/skills/prd/ .claude/commands/sc/prd.md`. That's a more reliable baseline than any document.

**Variant B (Haiku):**
Phase 0 isn't about git — it's about *cognitive* baselining. Before touching 1,369 lines of content, the implementer needs to confirm constraints, prepare the fidelity map, and establish the acceptance matrix mapping every FR/NFR to a pass condition. Git gives you rollback; Phase 0 gives you *direction*. The Developer Guide is a governance authority — referencing it explicitly prevents drift from architectural mandates. Even solo implementers benefit from a pre-flight checklist. The cost is minimal (one Sprint Slot shared with Phase 1); the protection is structural.

---

### D2: Refs Verification Ordering

**Variant A (Opus):**
Verify before you build. Phase 1 exists specifically to catch drift in the 3 existing refs/ files *before* any new work begins. If `refs/agent-prompts.md` has drifted from SKILL.md lines 553-967, every subsequent phase that references those files propagates the error. My approach adds a blocking gate, yes — but it's 30-45 minutes that prevents potentially hours of rework. The v1 implementation created these refs but never completed the refactor. That's exactly the scenario where drift is most likely.

**Variant B (Haiku):**
Verification and creation are not truly independent concerns — they're both part of the same decomposition work. By folding refs verification into Phase 2 alongside SKILL trimming and build-request creation, you maintain a single coherent mental model of the content flow. The implementer is already reading SKILL.md line ranges during decomposition; verifying refs against those same ranges is natural, not an added burden. A separate blocking phase fragments attention and creates an artificial serialization point. If drift is found, you fix it in the same phase where you're already editing.

---

### D3: Granularity Level

**Variant A (Opus):**
47 steps with per-step verification means zero interpretation required. An agent or implementer can execute this as a literal checklist — step 2.1.3 says "Update 6 SKILL CONTEXT FILE references" and lists all 6. Step 3.6 says "Remove Tier Selection table header rows (lines 79-85, ~7 lines) — table now in command; retain selection rules (lines 87-92)." There's no ambiguity about what stays and what goes. For a content fidelity task where the primary risk is *missing something*, over-specification is a feature, not a bug.

**Variant B (Haiku):**
Over-specification creates rigidity. If the implementer discovers that line ranges have shifted (common after any intervening edit), a 47-step plan with hardcoded line numbers becomes a liability — every step needs mental adjustment. My 20-action plan describes *what* to do at the right level of abstraction: "Trim SKILL.md to behavioral protocol only (400-500 lines)" gives the implementer latitude to handle the actual content structure they find. The requirement IDs (FR-PRD-R.1a-1f) are the real specification; the roadmap should point to them, not try to replicate them at finer grain.

---

### D4: Effort Expression

**Variant A (Opus):**
"3.25-4.75 hours" is actionable. A solo implementer can schedule this in an afternoon. Sprint Slots are a framework abstraction that adds indirection — "Sprint Slot 2" tells you nothing about whether you need 30 minutes or 3 hours. For a concrete, well-scoped task with known inputs and outputs, abstract units sacrifice useful information for no gain. The tasklist pipeline can convert hours to its own units if needed.

**Variant B (Haiku):**
Sprint Slots are the native unit of the SuperClaude sprint pipeline. When this roadmap feeds into `superclaude roadmap run` and `sc:tasklist`, Sprint Slots map directly to pipeline scheduling without conversion. Hours are deceptive precision — "30-45 minutes" for Phase 1 assumes a specific implementer speed, familiarity with diff tooling, and no surprises. Sprint Slots acknowledge that effort varies by executor while still conveying relative sizing. The pipeline is the consumer; speak its language.

---

## Round 2: Rebuttals

### D1: Phase 0 Necessity — Rebuttals

**Variant A rebutting B:**
"Cognitive baselining" is what reading the spec accomplishes — you don't need a phase for it. The acceptance matrix Haiku proposes is literally the success criteria table I already have in Phase 4 (Section 5, 12-row table). Creating it twice — once in Phase 0 and once as the validation gate — is redundant. And the Developer Guide reference: both variants implement identical constraints. Citing the document doesn't make the constraints more enforced; the Phase 4 checks do. Phase 0 is a governance theater tax on an already well-scoped task.

**Variant B rebutting A:**
Opus conflates "rollback capability" with "baseline discipline." Yes, git can undo changes. But knowing *what success looks like* before starting — mapping every FR to a verification method — prevents the implementer from discovering in Phase 4 that they forgot a requirement. My acceptance matrix isn't a duplicate of Opus's success criteria; it's an *input* to implementation that ensures nothing is missed. Opus's approach is "build first, check at the end." Mine is "confirm the target, then build toward it." For a zero-behavioral-change refactor where the entire risk is content fidelity, knowing the target first is cheaper than finding gaps late.

---

### D2: Refs Verification Ordering — Rebuttals

**Variant A rebutting B:**
Haiku says "fix drift in the same phase where you're editing." That's exactly the problem. If you're simultaneously trimming SKILL.md, creating build-request-template.md, and discovering that agent-prompts.md has drifted, you're juggling three concerns with interdependencies. A drifted ref means the fidelity index is wrong, which means your trimming targets are wrong, which means your line counts will be off. Isolating verification as a gate *before* modification ensures you're working from a known-good foundation. The 30-45 minute investment buys certainty.

**Variant B rebutting A:**
Opus assumes drift is likely enough to warrant a blocking phase but provides no evidence. The v1 implementation created refs from SKILL.md — if no intervening edits touched both the refs and SKILL.md, drift probability is near zero. A quick diff at the start of Phase 2 (3 commands, 2 minutes) catches drift without the ceremony of a dedicated phase with 7 sub-steps and a milestone gate. Opus's Phase 1 isn't proportionate to the actual risk. If drift *is* found, the fix is the same in both approaches: re-extract from current SKILL.md.

---

### D3: Granularity Level — Rebuttals

**Variant A rebutting B:**
"Line ranges might shift" — they won't. The spec was written against the current SKILL.md, and the roadmap gates Phase 1 on verifying that the source hasn't changed. If someone edits SKILL.md between roadmap approval and execution, *both* plans are invalidated. Within the execution window, line numbers are stable. The requirement IDs that Haiku relies on still need to be interpreted into concrete actions — my 47 steps *are* that interpretation, done once and correctly, rather than left to the implementer to re-derive under time pressure.

**Variant B rebutting A:**
Opus's 47 steps create a false sense of completeness. If a step is wrong (say, line 85 is actually line 87 after a minor formatting difference), the implementer who trusts the checklist blindly will make an error. My approach trusts the implementer to read the actual file and apply the requirement — "remove Tier Selection table header, retain selection rules" is robust to off-by-two line shifts. For agent execution, the requirement IDs are more parseable than prose steps. For human execution, understanding > rote following.

---

### D4: Effort Expression — Rebuttals

**Variant A rebutting B:**
The sprint pipeline can consume hours as easily as Sprint Slots — it's a configuration parameter, not a hard constraint. And if Sprint Slots are truly the native unit, Haiku should have defined their duration. "Sprint Slot 2" shared between Phase 2 and Phase 3 tells the pipeline nothing about relative sizing *within* the slot. My per-phase hour ranges give the pipeline strictly more information to work with.

**Variant B rebutting A:**
Hours create false commitments. If the roadmap says "30-45 minutes" and Phase 1 takes 60, the implementer feels behind schedule — even if they're proceeding correctly but found drift that needed fixing. Sprint Slots communicate "this is one unit of work" without anchoring to clock time. The pipeline's scheduling is based on task dependency graphs, not hour estimates. Opus's hours are useful for human planning but misleading for automated execution — and this roadmap may be consumed by either.

---

## Convergence Assessment

### Areas of Agreement Reached Through Debate

1. **Verification is mandatory** — both sides agree refs must be verified before the refactor is considered complete. The dispute is *when*, not *whether*.

2. **Git is the rollback mechanism** — Haiku's Phase 0 doesn't replace git; both agree `git checkout` is the recovery path. The disagreement is whether additional governance artifacts justify their cost.

3. **Success criteria are equivalent** — despite different presentation (12-row table vs. 8-item matrix + checks), both validate the same constraints. Convergence is possible by adopting Opus's executable format with Haiku's FR/NFR traceability annotations.

4. **Risk inventory is identical** — 9 risks, same severities, same mitigations. No debate needed.

5. **Integration wiring is functionally equivalent** — both identify the same 5 named artifacts with the same mechanism types. Presentation differs (embedded table vs. standalone section) but content converges.

### Remaining Disputes

| Point | Opus Position | Haiku Position | Resolution Lever |
|-------|--------------|----------------|-----------------|
| Phase 0 | Unnecessary overhead | Cheap insurance | **Executor context**: solo agent → skip; team review → include |
| Verification ordering | Verify-first (blocking gate) | Verify-during (integrated) | **Drift probability**: if refs were edited since v1 → Opus wins; if untouched → Haiku's integration is faster |
| Granularity | 47 steps (executable) | 20 actions (flexible) | **Executor type**: automated agent → Opus; experienced human → Haiku |
| Effort units | Hours (actionable) | Sprint Slots (pipeline-native) | **Consumer**: human scheduler → hours; `sc:tasklist` pipeline → Sprint Slots; **hybrid** → include both |

### Synthesis Recommendation

A merged roadmap should:
- **Adopt Opus's phase ordering** (verify-first) — the safety margin outweighs the time cost given incomplete v1 state
- **Skip Phase 0** for solo execution but note it as an option for team contexts
- **Use Opus's 47-step granularity** as the primary plan with Haiku's FR/NFR requirement IDs annotated per step for traceability
- **Include both effort formats** — hours for human planning, Sprint Slot equivalences for pipeline consumption
- **Add Haiku's Developer Guide reference** as a dependency — minimal cost, better audit trail
- **Use Opus's rollback command** explicitly rather than assuming git knowledge
- **Adopt Opus's embedded integration table** over Haiku's standalone section for execution-time accessibility
