# Adversarial Debate — Persona Auto-Activation List (D03)

**Task:** T04.03 — `/sc:adversarial` debates: MCP, persona, allowed-tools, compliance gating, triggering surface
**Roadmap Item:** R-013
**Source feature characterization:** `feature-persona-activation.md` (Phase 2 / T02.03)
**Constraint inputs:** `extension-point-contracts.md` (T03.02); INV-01..INV-05 labels from `extension-point-contracts.md:13-17` (sprint specification verbatim)
**Donor catalog tag:** D03 = **NON-TRANSFERABLE** (`donor-feature-catalog.md:49`)
**Generated:** 2026-05-15
**Note on Phase 3 input:** `invariant-bounds.md` (T03.01) was not produced — see `checkpoints/CP-P03-END.md`. INV-02 and INV-05 collision claims below cite the one-line labels at `extension-point-contracts.md:13-17` plus the negative-space row N3 reject criteria at `extension-point-contracts.md:256-262`.

---

## Position A — Steelman for Inclusion

The persona auto-activation list is a **lightweight context-injection surface** that adds a single frontmatter line and offloads "which mental stance/persona should be applied to this work" to the upstream auto-activation layer. For a heterogeneous task stream — some auth work, some refactoring, some frontend — auto-activation amortizes the user's mental load: they describe the work, the framework chooses the persona. Concretely, a `/task` item that touches `auth/` could auto-activate the `security` persona (which brings Sequential MCP as primary, a security-focused review stance, and stricter assumptions per the user's global persona table) without the user typing `--persona-security`.

**Integration sketch:**
- **Attach point:** extension-point row 13 (Required frontmatter schema slot, C5; `extension-point-contracts.md:169-175`) — add `personas:` as an optional metadata field, read-only at pre-loop time. Or, more narrowly, route activation through the **per-item agent dispatcher** at row 15 (Subagent dispatcher — type selection, C3; `extension-point-contracts.md:186-192`) where the spawned subagent's `agent_type` decision is the natural attach surface.
- **Restricted scope:** activation is **per-item, never whole-task**. The F1 loop owner (the main agent) does NOT auto-activate a persona for itself — that would risk relaxing the loop-ownership invariant (N3 / Critical Rule 12). The persona, if any, attaches to a *spawned subagent* invoked from a single checklist item, where row 15's admit criteria already accept new agent types.
- **Optional, off-by-default:** the slot defaults to empty; behavior is unchanged when absent.

**Why this might be a net upgrade:**
- `/task`'s subagent dispatcher at `src/superclaude/skills/task/SKILL.md:291-299` already names agent types (`general-purpose, rf-analyst, rf-qa, rf-qa-qualitative, rf-assembler, rf-task-builder, rf-task-researcher, Explore`). Two of the donor's 10 slugs (`python-expert`, `quality-engineer`) **already exist as subagent types** in `~/.claude/agents/`. There is a *partial* shape-match: the donor's "persona-flavored behavior" can be reified as "spawn a subagent of this type" — which is row 15's native surface.
- For STRICT-tier security items, auto-spawning a `quality-engineer` or `security`-flavored subagent for verification could improve verdict quality at low coupling cost.

**Trade-off acknowledgment (R-RULE-04 anti-sycophancy):**
- **The donor's catalog tag is NON-TRANSFERABLE** (`donor-feature-catalog.md:49`). The catalog's reasoning: "`/task` is persona-neutral by design — the F1 executor owns loop control regardless of persona; attaching a persona-activation table to `/task` has no F1-loop surface and risks reintroducing the delegation pattern prohibited by Critical Rule 12 at `src/superclaude/skills/task/SKILL.md:349`." Position A is arguing *against* the donor catalog's own classification, which is a high bar to clear.
- **The activation layer is invisible from this repo.** Reading `src/superclaude/commands/task.md` in isolation gives a list of 10 slugs and no information on (a) the trigger conditions, (b) the threshold, (c) the observable effect, or (d) the override path. The donor *advertises* the list but does not *implement* the matcher (`feature-persona-activation.md:46, 67`). Adopting the slot without an activation layer is Layer-A-style ceremony (R-RULE-06).
- **No observability for activations.** Even if activation works, there is no header, log line, or sentinel in `/task`'s output that says "auto-activated persona X with confidence Y." Contrast with the classification header — which makes tier choice auditable. Persona activation would be silent.
- **The 10-slug list is heterogeneous.** Two of the ten are subagent types, not personas (`python-expert`, `quality-engineer`). The auto-activation layer must disambiguate; the donor offers no rule (`feature-persona-activation.md:70`).
- **Critical Rule 12 violation risk is named explicitly in the donor characterization itself.** `feature-persona-activation.md:82` warns: "Auto-activation of `quality-engineer` or `python-expert` — both of which exist as subagent types in `~/.claude/agents/` — risks the framework interpreting 'activate `python-expert` for this whole task' as a loop-delegation." Even Position A acknowledges this is a real risk; the mitigation is to constrain activation to per-item scope, but that mitigation has to be *built* — it does not come for free with the slot.

---

## Position B — Steelman for Rejection

**The donor catalog already classified D03 as NON-TRANSFERABLE** (`donor-feature-catalog.md:49`) with reasoning that directly anticipates Position A's argument: "`/task` is persona-neutral by design — the F1 executor owns loop control regardless of persona; attaching a persona-activation table to `/task` has no F1-loop surface and risks reintroducing the delegation pattern prohibited by Critical Rule 12 at `src/superclaude/skills/task/SKILL.md:349`." Position A's "restricted scope per-item" mitigation is essentially "if we constrain it tightly enough, it stops being the donor feature" — at which point what is being adopted?

**Invariant-collision risk (R-RULE-05 / INV-02):** The donor's mechanism is "auto-activate a persona for the lifetime of the command turn." On `/task`, the turn-equivalent is the whole F1 loop. Auto-activating `python-expert` for "this whole task" is the exact failure mode `extension-point-contracts.md:256-262` (N3 — F1 loop is non-delegable) catalogues:

> Features that delegate the READ-IDENTIFY-EXECUTE-UPDATE-REPEAT loop to a subagent. → **INV-01** (loop ownership is the integrity guarantee), **INV-02** (catalogued prohibition).
> Features whose contract spans more than one checklist item per subagent dispatch outside the parallel-spawn exception. → **INV-01**, **INV-02**.

A whole-task persona activation reaches into both bullets — it is a contract that spans the whole loop. N3 is **C1 — auto-REJECT (R-RULE-05)** per `extension-point-contracts.md:262`. Position A's mitigation (per-item only) is structurally equivalent to *not adopting D03* and instead extending row 15 (subagent type roster) — which `/task` could already do without referencing D03 at all.

**Invariant-collision risk (R-RULE-05 / INV-05):** Even at per-item scope, persona auto-activation that *infers* a persona from the item's content is making a *what-to-do* decision (which mental stance applies). INV-05 (`extension-point-contracts.md:17`) — "refusal of definition: `/task` does not decide *what* to do; the MDTM file does. The F1 loop only *executes*" — means the executor must not derive its operating stance from item content; the item itself must specify it. The "auto" in "auto-activation" is exactly the prohibited inference. To survive INV-05, activation would have to be *explicitly declared per item* (e.g., `agent_type: security` inside the item itself), at which point it is not auto-activation — it is just the existing row 15 dispatcher behavior.

**R-RULE-06 (ceremony without behavioral teeth):** Position A admitted that the activation layer is undocumented and unverifiable from this repo, that the matcher does not live in the donor side, and that there is no observability for activations. Adopting `personas:` as a frontmatter slot without an activation layer is ceremony — implementation mass with no behavioral pattern. Per R-RULE-06, REJECT.

**Realistic failure mode #1 (INV-02 / N3 violation):** A future contributor adds `personas: [python-expert]` to a task's frontmatter intending "use the python-expert persona for this task." The auto-activation layer interprets this as "spawn a `python-expert` subagent that drives the whole task." `python-expert` is a real subagent type in `~/.claude/agents/`. The framework happily delegates the F1 loop to it. The contract-span violation in `extension-point-contracts.md:261` fires; INV-01 + INV-02 are both broken; the failure is silent because the F1 loop's halt-on-delegation enforcement is prose, not code.

**Realistic failure mode #2 (INV-05 violation):** A `/task` item reads "Refactor `auth/login.py` for clarity." The activation layer keyword-matches `auth/` to `security` (90% confidence per donor's trigger heuristics, `feature-triggering-surface.md:33`). The spawned subagent now operates with a security-first mental model and produces a hardening change rather than a clarity refactor. The F1 loop ran the item as written, but the *operating stance* came from inference, not from the item text. INV-05 was violated invisibly because no header or log records "this item was executed under the `security` persona." The user wonders why a clarity refactor produced a hardening change; the trail does not reach the activation decision.

**Duplication risk (R-RULE-06 secondary):** `/task` already has a subagent-type roster at row 15. Eight of the donor's 10 persona slugs (the canonical personas like `architect, security, frontend`) have no analog in `/task`'s roster; two of them (`python-expert, quality-engineer`) already do. For the two that do, the donor adds nothing — they are already supported via the existing dispatcher. For the eight that do not, the donor's value depends on (a) Claude Code Core's persona layer existing, (b) the user's CLAUDE.md persona table being installed, (c) the trigger-condition mapping being defined upstream — none of which are in this repo. The eight canonical personas would be inert under D03's adoption.

**Maintenance cost:** Persona activation creates a *second activation surface* on top of `/task`'s existing subagent dispatcher. When the two surfaces disagree (item specifies `agent_type: general-purpose` but the frontmatter `personas:` list includes `quality-engineer`), the recipient must define precedence and document it. The user's mental model now has to span two surfaces. Skills surfaces should narrow over time, not widen.

---

## Evidence-Based Weighing

**Position A's strongest point (partial shape-match via row 15):** Two of the donor's 10 slugs are real subagent types in `/task`'s dispatcher roster. If activation is constrained to "spawn a subagent of this type per-item," the integration *could* attach at row 15 (C3) without collision.

**Position B's answer:** Position A's per-item-row-15 attach is structurally equivalent to "don't adopt D03; just add agent types to row 15 if needed." The donor's value-claim is *auto-activation* — the framework inferring the persona from prompt/item content. If the activation is reduced to "explicitly declared per item," the auto vanishes and the feature collapses to the existing dispatcher. Position A is proposing to adopt the slug list as data without adopting the activation behavior; under R-RULE-06 that is ceremony. The two slugs that match (`python-expert, quality-engineer`) can be added directly to row 15's roster (a C3 enumerated extension) without referencing D03. Position B does not contest that row 15 can grow; it contests that D03 is the means.

**Position B's strongest point (INV-02 / N3 collision + INV-05 collision + donor catalog NON-TRANSFERABLE tag):** Whole-task persona activation collides with N3 (loop non-delegable, C1 / auto-REJECT). Per-item *auto*-activation collides with INV-05 (refusal of definition — the stance must come from the item, not be inferred). The donor catalog itself tags D03 NON-TRANSFERABLE. Three independent rejection lines converge.

**Position A's answer:** Concedes the whole-task case is C1 auto-REJECT. On per-item scope: argues INV-05 only fires if activation is *inferred*; if activation is driven by an explicit per-item field, it does not fire. But this concession is the same one Position B already used — at that point the feature is not auto-activation. Position A has no answer that preserves the "auto" while avoiding INV-05. The NON-TRANSFERABLE tag stands unchallenged.

**Unanswered point against Position A:** Position A did not address the donor catalog's explicit NON-TRANSFERABLE classification with new evidence. Disagreeing with a Phase 1 tag requires either (a) showing the tag's reasoning is wrong, or (b) showing a tag-immune attach path. Position A did neither; the closest thing is the row-15 per-item-explicit attach, which Position B correctly identified as collapsing to a non-D03 extension.

**Unanswered point against Position B:** Position B's failure-mode #1 assumes the auto-activation layer would interpret a task-frontmatter `personas:` field as whole-task. It is possible Claude Code Core's persona layer (which is the actual consumer) interprets it per-turn rather than per-task. But this argument cuts against Position A more than Position B — if the consumer's interpretation is unverifiable from this repo (`feature-persona-activation.md:67`), Position A cannot guarantee the safe interpretation.

**Net effect:** Three convergent rejection lines (Phase 1 NON-TRANSFERABLE tag, INV-02/N3 collision for whole-task scope, INV-05 collision for per-item auto-inference) and a structural collapse of the per-item-explicit alternative into the existing row-15 dispatcher. R-RULE-06 ceremony argument is unrefuted. **R-RULE-05 invariant gate fires** for the whole-task interpretation; per-item auto-inference also collides; per-item-explicit attach is not D03.

---

## Scored Verdict

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **2** | Some marginal value if implemented at per-item-explicit scope (which collapses to the existing row-15 dispatcher). Auto-activation value (the donor's actual claim) is unavailable without the upstream Claude Code persona layer, which is not in this repo. |
| **C (Complementarity, 1–5)** | **1** | C-band **C1** under whole-task scope — collides with N3 (`extension-point-contracts.md:256-262`), INV-01, INV-02. Under per-item *auto*-inference scope, collides with INV-05 (`extension-point-contracts.md:17`). The only non-colliding scope (per-item explicit) is not D03 — it is the existing row-15 dispatcher. **C=1 (auto-REJECT under R-RULE-05).** |
| **K (Cost, 1–5)** | **4** | Four distinct burdens (`feature-persona-activation.md:73-84`): new frontmatter slot, activation layer for non-prompt input, persona-vs-subagent disambiguation, Critical Rule 12 hardening to prevent loop-delegation. |
| **Net = (V × C) / K** | **(2 × 1) / 4 = 0.5** | |

**Verdict: REJECT.**

Triple-locked:
1. **R-RULE-05 invariant gate (`extension-point-contracts.md:262`):** whole-task persona activation is C1 / auto-REJECT.
2. **R-RULE-06 (ceremony without behavioral teeth):** activation matcher is not in this repo (`feature-persona-activation.md:46, 67`); adopting the slug list as data without the activation behavior is implementation mass with no behavioral pattern.
3. **Phase 1 NON-TRANSFERABLE tag (`donor-feature-catalog.md:49`):** the donor catalog already classified D03 NON-TRANSFERABLE and the reasoning anticipates the Critical Rule 12 collision Position A's mitigation attempts to dodge. Net = 0.5 < 1.5 also lands in REJECT independently.

**Stack-rank inputs (for T04.05):**
- D03: V=2, C=1, K=4, Net=0.5, **REJECT** (R-RULE-05 invariant gate primary; R-RULE-06 secondary; Phase 1 NON-TRANSFERABLE tag confirms).

**Phase 5 forwarded question (not a Phase 4 verdict change):** If `/task`'s row 15 subagent dispatcher should be extended to include `security`, `architect`, `analyzer`, or other canonical-persona-shaped agent types, that is a row-15 enumerated extension — debate it as such in a future sprint, not under the D03 banner.

**Note on missing T03.01 evidence:** `invariant-bounds.md` is absent (Phase 3 checkpoint Fail). The N3 / INV-01 / INV-02 collision argument for whole-task scope is sourced from `extension-point-contracts.md:256-262` (the N3 negative-space row with explicit C1 auto-REJECT). The INV-05 collision argument for per-item-auto scope is sourced from `extension-point-contracts.md:17` (the INV-05 label). Both are strong enough to carry the verdict; a worked failure-mode example in `invariant-bounds.md` would strengthen the audit trail but does not change the outcome — Net = 0.5 plus R-RULE-05 + R-RULE-06 + Phase 1 NON-TRANSFERABLE tag is dispositive.
