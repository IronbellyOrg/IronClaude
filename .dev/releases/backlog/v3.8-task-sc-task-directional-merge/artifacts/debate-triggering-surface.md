# Adversarial Debate — Triggering Surface (D06 + D13)

**Task:** T04.03 — `/sc:adversarial` debates: MCP, persona, allowed-tools, compliance gating, triggering surface
**Roadmap Item:** R-013
**Source feature characterization:** `feature-triggering-surface.md` (Phase 2 / T02.03)
**Constraint inputs:** `extension-point-contracts.md` (T03.02); INV-01..INV-05 labels from `extension-point-contracts.md:13-17`; `task-builder-adjacency.md` (T03.03) — definition-vs-execution routing rule.
**Donor catalog tags:** D06 = ADAPTABLE; D13 = **NON-TRANSFERABLE** (`donor-feature-catalog.md:64`)
**Generated:** 2026-05-15
**Note on Phase 3 input:** `invariant-bounds.md` (T03.01) was not produced — see `checkpoints/CP-P03-END.md`. INV-05 collision claims cite the label at `extension-point-contracts.md:17` plus the routing rule in `task-builder-adjacency.md` (T03.03 verified passing per CP-P03-END).

---

## Position A — Steelman for Inclusion

The donor's triggering surface (auto-trigger heuristics + auto-suggest keywords) offers **low-friction entry from free-text** — a user mid-conversation can invoke `/sc:task "fix the SQL injection in login.py"` and the system handles classification, dispatch, MCP routing, verification, TFEP without first authoring a task file (`feature-triggering-surface.md:134`). For ad-hoc work, this is order-of-magnitude faster than building a task file via `task-builder` then invoking `/task`.

**The donor surface advertises four heuristic conditions** (`src/superclaude/commands/task.md:29-36`):
- Complexity Score > 0.6 with code modifications (90% confidence)
- Estimated affected files > 2 (85%)
- Security domain paths `auth/`, `security/`, `crypto/` (95%)
- Refactoring keywords (refactor, remediate, multi-file) (90%)

Plus an Auto-Suggest Keywords table at `src/superclaude/skills/sc-task-protocol/SKILL.md:33-35`:
- High confidence: "implement feature", "refactor system", "fix security", "add authentication", "update database schema"
- Moderate confidence: "add new", "create component", "update service", "modify API"

**Integration sketch (the right attach surface is NOT `/task`):**

The honest position is the one Position A is steelmanning *with* the donor characterization itself (`feature-triggering-surface.md:163`): the donor's heuristics belong **upstream of `task-builder`**, not as a direct attach to `/task`. The mechanism:

- A free-text prompt matching one of the four heuristic conditions surfaces `task-builder` as a recommended invocation (not `/task`).
- `task-builder` generates a task file at `.dev/tasks/to-do/TASK-*/TASK-*.md` populated from the prompt.
- The generated task file's frontmatter carries a `Tier:` field (inherited from the heuristic match: security domain → STRICT; multi-file refactor → STANDARD).
- The user is then prompted to invoke `/task <path>` (or the framework auto-invokes it).

This integration sketch:
- **Preserves `/task`'s input-shape invariant** (task-file path, not free-text prompt) — `task-builder-adjacency.md` §2 line 168: "features shaping *what* work is defined route to `task-builder`; features shaping *how* work executes route to the `/task` executor." Heuristic auto-triggering shapes *what* work is defined (a new task file) — it routes to `task-builder`.
- **Does not extend `/task`'s skill description** (which is already a sophisticated trigger surface with multiple phrases, path-detection, and identifier-detection — `src/superclaude/skills/task/SKILL.md:3`).
- **Does not collide with INV-05** (refusal-of-definition) — `task-builder` defines the work, then writes it to the task file, then `/task` executes the file. Definition and execution stay separated.

**Why this is a (very narrow) net upgrade:**

- Today the flow is: user authors task file manually OR runs `task-builder` manually OR types `/sc:task <prompt>` and abandons the task-file workflow. The friction is real for ad-hoc one-off work.
- The donor's *upstream-of-task-builder* heuristics could close that gap: ad-hoc prompts that match the heuristics auto-suggest the build-then-execute pipeline. The user gets `/sc:task`-style low-friction entry while preserving `/task`'s F1-loop durability and resumability.

**Trade-off acknowledgment (R-RULE-04 anti-sycophancy):**

- **The donor's heuristics live in donor prose, not implemented anywhere in this repo.** `grep -r "Complexity Score" src/superclaude/` finds the table and references but no executable rule (`feature-triggering-surface.md:144`). If the heuristic layer is not provided by Claude Code core, the donor's "low-friction entry" reduces to "user must remember to type `/sc:task`" — which is no friction reduction over typing `/task <path>`. Position A's integration sketch presupposes a heuristic matcher that does not yet exist on either side.
- **The two surfaces are non-substitutable** (`feature-triggering-surface.md:103, 146`). A user with a task file who accidentally types `/sc:task "execute this task"` triggers classification on the prompt-text (probably classifies EXEMPT/LIGHT) rather than executing the file. Conversely, a user with a free-text request who says "/task fix the bug" triggers the skill loader on `/task`, which then searches for a "fix the bug" task file, fails to find one, and offers the discovery menu. Position A's integration sketch (route heuristics to `task-builder`) sidesteps this by *not* attaching to `/task`, but the cost is paying the heuristic matcher elsewhere.
- **`/task`'s description-based trigger phrases overlap with non-task work.** Phrases like "continue the task" and "run this task" are common in conversational programming work that has nothing to do with MDTM task files (`feature-triggering-surface.md:145`). Layering donor heuristics on top of `/task`'s description (rather than routing to `task-builder`) would create two layered trigger systems whose precedence is undefined.
- **The donor's characterization explicitly recommends rejection for direct `/task` attach** (`feature-triggering-surface.md:163`): "The honest answer to the Phase 4 net-upgrade question is likely 'the triggering surface should NOT transfer' — instead, the donor's heuristics belong upstream of `task-builder`." Position A is *aligned* with the characterization's recommendation, not arguing against it.

---

## Position B — Steelman for Rejection (for direct `/task` attach)

**The donor and recipient have fundamentally incompatible input shapes.** Donor consumes free-text prompts; recipient consumes task-file paths or identifiers (`feature-triggering-surface.md:18`). The two surfaces share the *word* "task" but otherwise share almost nothing. Adopting donor-side triggering on the recipient side dissolves the recipient's input-shape invariant (`feature-triggering-surface.md:161`).

**Invariant-collision risk (R-RULE-05 / INV-05):** INV-05 (`extension-point-contracts.md:17`) — "`/task` does not decide *what* to do; the MDTM file does. The F1 loop only *executes*." Donor heuristics that classify a free-text prompt and produce a task definition are exactly the *what-to-do* decision INV-05 prohibits. If donor heuristics attach *at* `/task` (rather than upstream of `task-builder`), the executor's input is no longer "execute this file" — it is "infer what to do from this prompt, then execute." That collides with INV-05 head-on.

The task-builder-adjacency analysis (T03.03 / `task-builder-adjacency.md` §2 line 168) makes this explicit: "features shaping *what* work is defined route to `task-builder`; features shaping *how* work executes route to the `/task` executor." Auto-trigger heuristics that decide whether a prompt warrants `/sc:task`-style work *and* what tier to assign are shaping the *definition* of work. They route to `task-builder` — not to `/task`. T03.03 §3 line 267 calls this out as "exactly the failure mode INV-05 prevents."

**Four coupling burdens for direct `/task` attach** (`feature-triggering-surface.md:151-161`):

1. **A free-text prompt-handling layer on a path-driven skill.** `/task` consumes a task-file path or identifier. Adding heuristic auto-triggering to `/task` requires either (a) extending `/task` to accept free-text prompts (which duplicates `task-builder`) or (b) routing the heuristic to `task-builder` instead (which is the upstream-attach Position A advocates — i.e., it's not really a `/task` adoption).
2. **Heuristic-matcher implementation.** Four heuristic conditions advertised but not implemented; building them adds a new responsibility area entirely.
3. **Reconciliation with the existing skill-description trigger phrases.** `/task`'s description is already a sophisticated trigger surface. Adding donor-style heuristics on top creates two layered trigger systems with no precedence rule.
4. **A non-substitutability disclaimer at the trigger boundary.** Position A's mitigation is to *not* attach donor heuristics to `/task` — but that means the cluster of D06 + D13 is not being adopted by `/task`. It's being routed to `task-builder`, which is a separate adoption decision and a separate skill.

**D13 is NON-TRANSFERABLE per `donor-feature-catalog.md:64`:** "`/task` is not surfaced via prompt-auto-suggest — it is invoked on a task-file path; this list has no consumer in the F1 model." D13 brings nothing to `/task`. Position A does not contest this.

**D06 is ADAPTABLE per `donor-feature-catalog.md:52`:** "`/task` is invoked by user supplying a task-file path, not by heuristic match on a bare prompt; trigger model would have to be re-shaped to a 'should I emit a task file' pre-step." That re-shaping is exactly what Position A's integration sketch does — but the *attach* is to `task-builder`, not to `/task`. From `/task`'s perspective, D06 is also effectively NON-TRANSFERABLE. The ADAPTABLE tag references the upstream-of-`task-builder` adaptation, not the `/task` attach.

**Realistic failure mode #1 (INV-05 collision on direct attach):** A future contributor extends `/task`'s SKILL.md description to include donor heuristic phrases ("the user mentions auth/, security/, or crypto/ paths → invoke `/task`"). The Claude Code skill loader then triggers `/task` on bare prompts like "what does the auth flow do?" `/task` enters its discovery protocol (no path → search `.dev/tasks/to-do/` for "🟠 Doing"), finds an unrelated in-progress task, and starts executing *that*. The user wanted information, not execution. The trigger surface decided the *what* (which task to execute) from inference, not from the user — INV-05 fails invisibly because the discovery protocol's auto-selection is the *what-to-do* leak.

**Realistic failure mode #2 (two-system trigger conflict):** Donor heuristics fire on a prompt that *also* matches `/task`'s existing description trigger phrases. Both fire. The skill loader has no precedence rule between description-based phrases and content-based heuristics. The user gets one of: (a) `/task` invoked with no path (discovery protocol), (b) `/sc:task` invoked (the donor command), or (c) ambiguity-prompting the user. The system's behavior under collision is undefined; the maintenance cost is debugging undefined behavior.

**Duplication risk:** The donor's heuristic conditions overlap with `task-builder`'s job (decide what work to define). `task-builder-adjacency.md` is unambiguous: that decision lives on the builder side, not the executor side. Adding the same decision to `/task`'s trigger surface duplicates `task-builder`'s function badly — the executor would now have *two* paths to deciding work (one via task file, one via heuristic match). Two paths means two contracts to keep in sync.

**Maintenance cost:** Heuristic conditions drift. "Security domain paths" today is `auth/`, `security/`, `crypto/`; tomorrow a new compliance area (say `kyc/`) joins. The donor matrix lives in prose; every drift is a multi-file edit. If the recipient inherits the matrix on its trigger surface, it inherits the drift cost. Better to keep the matrix upstream of `task-builder` (single owner) than to duplicate it on `/task`.

---

## Evidence-Based Weighing

**Position A's strongest point (low-friction entry has real value, AND donor heuristics CAN attach safely upstream of `task-builder`):** The friction-reduction value is real; routing heuristics upstream of `task-builder` preserves `/task`'s INV-05 while still delivering ad-hoc-prompt-to-task-file conversion.

**Position B's answer:** Accepted as real — but the upstream-of-`task-builder` attach is *not a `/task` adoption*. From `/task`'s perspective, the donor's triggering surface is REJECTed. From `task-builder`'s perspective, it is a separate debate, separately scoped. The triggering-surface feature characterized in `feature-triggering-surface.md` is the *donor's* trigger surface, which is fundamentally `/sc:task`-shaped (free-text → command turn). That shape does not transfer to `/task`. The shape that *does* survive is "should `task-builder` auto-build a task file when prompted text matches these patterns?" — but that is a `task-builder` extension, not a `/task` absorption, and it should be debated under `task-builder`'s banner in a future sprint (Phase 5 net-upgrade question).

**Position B's strongest point (INV-05 collision on direct attach + non-substitutable input shapes + D13 NON-TRANSFERABLE + donor characterization itself recommends rejection):** Five convergent rejection lines: (1) INV-05 collision on direct attach (`extension-point-contracts.md:17` + `task-builder-adjacency.md` §3 line 267); (2) input-shape invariant dissolution (`feature-triggering-surface.md:161`); (3) D13 explicitly NON-TRANSFERABLE (`donor-feature-catalog.md:64`); (4) the donor characterization itself recommends rejection (`feature-triggering-surface.md:163`); (5) duplication with `task-builder`'s function.

**Position A's answer:** Concedes all five. The position A is steelmanning is the upstream-of-`task-builder` attach, which is *not contradicted by any of Position B's five points*. Position A's integration sketch deliberately routes the heuristics away from `/task`. The verdict for `/task`-direct-attach is REJECT; the question of `task-builder`-upstream-attach is forwarded to Phase 5 as a net-upgrade question.

**Unanswered point against Position A:** Position A's upstream-of-`task-builder` integration sketch presupposes the heuristic matcher being built somewhere. The donor advertises but does not implement; the recipient side does not implement either. The friction-reduction value depends on a matcher that does not exist on either side. Position A did not pre-pay the matcher's cost; this is a real liability for any Phase 5 adoption.

**Unanswered point against Position B:** Position B's "two-system trigger conflict" failure mode (#2) is contingent on the implementer attaching heuristics *to `/task`*. Position A's integration sketch routes them away from `/task`, so #2 does not apply to the position A is defending. This counts against Position B (mildly) — failure mode #2 is real only for the strawman direct-attach implementation, not for the upstream-of-builder approach Position A actually advocates.

**Net effect:** For the **`/task` direct-attach question** (the actual scope of this Phase 4 debate), the verdict is unambiguous REJECT. The triggering surface is structurally incompatible with `/task`'s input-shape invariant and collides with INV-05. For the **`task-builder` upstream-attach question** (forwarded to Phase 5), the verdict is DEFER for further debate under `task-builder`'s banner. D13 is NON-TRANSFERABLE either way (no auto-suggest consumer for `/task`).

---

## Scored Verdict

The verdict is for the **`/task` direct-attach** scope only (the donor feature as characterized in `feature-triggering-surface.md`). The `task-builder` upstream-attach alternative is a Phase 5 forwarded question.

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **1** | For direct `/task` attach, value is zero — the surfaces are non-substitutable. The friction-reduction value Position A defends is real but accrues to `task-builder`, not to `/task`. From `/task`'s perspective, the donor's triggering surface adds nothing. |
| **C (Complementarity, 1–5)** | **1** | C-band **C1** — collides with INV-05 (`extension-point-contracts.md:17`) and dissolves `/task`'s input-shape invariant (`feature-triggering-surface.md:161`). The skill-description trigger surface (`src/superclaude/skills/task/SKILL.md:3`) is not in the extension-point inventory (rows 1-19, N1-N3) but functions as a constraint surface analogous to N1-N3 — admits nothing donor-shaped. **Auto-REJECT per R-RULE-05.** |
| **K (Cost, 1–5)** | **4** | Four burdens (`feature-triggering-surface.md:151-161`): free-text-handling layer, heuristic matcher, reconciliation with existing trigger phrases, non-substitutability disclaimer. |
| **Net = (V × C) / K** | **(1 × 1) / 4 = 0.25** | |

**Verdict: REJECT.**

Triple-locked:
1. **R-RULE-05 invariant gate** — INV-05 collision (`extension-point-contracts.md:17`; `task-builder-adjacency.md` §3 line 267).
2. **Phase 1 D13 NON-TRANSFERABLE tag** (`donor-feature-catalog.md:64`) — no auto-suggest consumer on `/task`.
3. **Net = 0.25 < 1.5** — REJECT band independently.

**Stack-rank inputs (for T04.05):**
- **D06 (direct `/task` attach)**: V=1, C=1, K=4, Net=0.25, **REJECT** (R-RULE-05 + input-shape invariant + Phase 1 / `feature-triggering-surface.md:163`).
- **D13 (auto-suggest keywords)**: V=1, C=1, K=2, Net=0.5, **REJECT** (Phase 1 NON-TRANSFERABLE; no `/task` consumer).

**Phase 5 forwarded questions:**

1. **`task-builder` upstream attach (the real net-upgrade question).** Should `task-builder` adopt the donor's four heuristic conditions (Complexity Score, Multi-file Scope, Security Domain, Refactoring Scope) as auto-build triggers — i.e., when an ad-hoc prompt matches one of the conditions, `task-builder` auto-generates a task file with the inferred `Tier:` populated, and the user is then routed to `/task`? This is a `task-builder` extension, not a `/task` absorption. It should be debated separately (likely as a future sprint scoped to `task-builder`) and is *not* dispositive for this debate.
2. **Heuristic matcher ownership.** Position A's integration sketch (and any `task-builder` adoption above) presupposes a heuristic matcher that lives somewhere. The donor advertises but does not implement. Neither does the recipient. If `task-builder` adopts the heuristics, the matcher must be built — that cost is a precondition, not free.

**Note on missing T03.01 evidence:** `invariant-bounds.md` is absent (Phase 3 checkpoint Fail). The INV-05 collision argument cites `extension-point-contracts.md:17` (the INV-05 label) plus `task-builder-adjacency.md` §3 line 267 (T03.03 — passed per CP-P03-END), which explicitly identifies "routing-rule violation as exactly the failure mode INV-05 prevents." A worked failure-mode example in `invariant-bounds.md` would reinforce this but is not load-bearing — the routing-rule analysis from T03.03 is sufficient and well-evidenced.
