# Adversarial Debate — MCP Server Declarations (D02 + D27)

**Task:** T04.03 — `/sc:adversarial` debates: MCP, persona, allowed-tools, compliance gating, triggering surface
**Roadmap Item:** R-013
**Source feature characterization:** `feature-mcp-declarations.md` (Phase 2 / T02.03)
**Constraint inputs:** `extension-point-contracts.md` (T03.02); INV-01..INV-05 labels from `extension-point-contracts.md:13-17` (sprint specification verbatim)
**Donor catalog tags:** D02 = ADAPTABLE; D27 = ADAPTABLE
**Generated:** 2026-05-15
**Note on Phase 3 input:** `invariant-bounds.md` (T03.01) was not produced — see `checkpoints/CP-P03-END.md`. INV-NN references in this debate use the one-line sprint-spec labels carried in `extension-point-contracts.md:13-17`. Where this matters for verdict reasoning, it is flagged inline.

---

## Position A — Steelman for Inclusion

The MCP declaration model is **two distinct capabilities** that should be separated and judged on their merits independently:

**Layer A — frontmatter `mcp-servers:` advertisement.** A single-line declaration that lists the MCP servers a skill expects to use. Even with no in-repo consumer today, it has cheap latent value as a **capability-discovery surface** for upstream tooling (capability auditors, docs generators, MCP-availability pre-flight checks) and as **human-readable documentation** of the skill's MCP intent. Adding it to `/task` would be additive and reversible.

**Layer B — per-tier required-server matrix + circuit breaker.** A safety contract — STRICT items refuse to enter the F1 loop if Sequential / Serena are unavailable; STANDARD degrades gracefully; LIGHT/EXEMPT have no requirement. For a team that runs STRICT-tier work (auth, crypto, migrations) in MCP-dependent workflows, this prevents the failure mode "the agent worked but its critical reasoning server was down and quietly produced lower-quality output."

**Integration sketch:**
- **Layer A attaches at extension-point row 13** — Required frontmatter schema slot (`src/superclaude/skills/task/SKILL.md:69`, C-band C5; `extension-point-contracts.md:169-175`). Add `mcp-servers:` as an *optional* metadata field. No validator enforces it pre-loop; it is read-only metadata. Admit criteria for row 13 are met (additive metadata, evaluated pre-loop, does not define the work).
- **Layer B attaches at extension-point row 1** — Task File Validation gate (`src/superclaude/skills/task/SKILL.md:64-73`, C-band C5; `extension-point-contracts.md:60-67`). The pre-loop validator gains an MCP-availability probe step *for tasks whose tasklist-bundle frontmatter carries a `Tier:` value of STRICT*. The probe runs once before loop entry; on failure it produces a user-facing diagnostic and refuses to enter the loop. The validator writes nothing to the task file beyond a refusal message — admit criteria for row 1 are satisfied verbatim.

**Why this is a net upgrade over the status quo:**
- Today `/task` has no model of MCP availability. A STRICT auth migration runs identically whether Sequential is up or down; the LLM may silently produce thinner reasoning. Layer B closes that gap with a deterministic pre-loop check.
- The probe mechanism is the only piece that needs invention; the *attach surface* (Task File Validation) already accepts pre-loop refusal-on-malformed and is C5-rated for additive validators. The integration sketch does not require relaxing any INV.

**Trade-off acknowledgment (R-RULE-04 anti-sycophancy):**
- **Layer A is dead metadata until a consumer exists.** `grep -r "mcp-servers" src/superclaude/` finds only the donor declaration site, not a consumer. Until a capability-auditor or pre-flight tool reads the slot, Layer A adds zero behavior — it is human-readable documentation pretending to be structured metadata (`feature-mcp-declarations.md:91`). Adopting Layer A *now* is a forward-bet on a consumer that may never ship.
- **Layer B's value is contingent on the user's environment having Sequential/Serena installed by default.** If the user runs base Claude Code without `airis-mcp-gateway`, the STRICT block fires *immediately* and the user must either install the servers or downgrade the tier — at which point the gate has prevented *all* STRICT execution rather than catching genuine outages (`feature-mcp-declarations.md:92`).
- **Layer B specifies behavior without enforcement.** "Block task execution" has no implementation in the donor repo (no test, no runtime check, no error pathway) — enforcement is LLM-discretionary (`feature-mcp-declarations.md:93`). On the recipient side we must invent the probe *and* the block enforcement; Position A is asking for net new mechanism, not for a copy.
- **The two layers are inconsistent.** Layer A advertises six servers (`sequential, context7, serena, playwright, magic, morphllm`); Layer B's STRICT row names only Sequential and Serena (`feature-mcp-declarations.md:18, 94`). Adopting both creates a documentation contradiction the recipient must resolve.

---

## Position B — Steelman for Rejection

**Layer A is ceremony with no behavioral teeth (R-RULE-06).** The donor characterization is unambiguous: there is **no consumer** of the `mcp-servers:` frontmatter list anywhere in `src/superclaude/`. `grep -r "mcp-servers" src/superclaude/` returns only the declaration site (`feature-mcp-declarations.md:91`). Position A's claim that it provides "cheap latent value" relies on a hypothetical future consumer; meanwhile the *immediate* effect of adding the slot is to extend `/task`'s frontmatter convention with a key whose presence or absence changes nothing observable. R-RULE-06 ("absorb patterns, not implementation mass") binds here: this is implementation mass with no behavioral pattern attached.

**Layer B is real safety logic but its coupling cost is structurally large** — `feature-mcp-declarations.md:96-110` enumerates **five distinct burdens**, and four of them touch invariants or extension surfaces in ways that are non-trivial:

1. **A new frontmatter slot in `/task`'s SKILL.md** that requires verifying or building Skill-loader recognition of `mcp-servers:` (the donor lives in a Command, the recipient is a Skill — the loaders' frontmatter semantics are not documented as identical).
2. **A tier-source data path before the gate can run** — `/task`'s validation gate at `src/superclaude/skills/task/SKILL.md:64-73` requires only `id, title, status, created_date`; no `Tier:` slot is intrinsic. Layer B's branch-on-tier presupposes a tier source `/task` does not have today.
3. **A runtime MCP-availability probe** — the donor names *what* to require but not *how* to test. The recipient must define probe (Bash health check? Tool-call rejection? Pre-flight Skill invocation?) and a deadline. Recipients of "probe responsibility" tend to grow (per-server health endpoints, retry policies, cache windows).
4. **A block-vs-degrade decision and an enforcement mechanism.** "Block STRICT" implies the F1 loop must refuse to enter when prerequisites fail. `/task`'s Error Handling at `src/superclaude/skills/task/SKILL.md:170-179` currently handles per-item failures by logging blockers and continuing; it has no concept of "refuse to enter the loop." Adding a hard block requires either a pre-loop early-exit (extending the validation gate's outcomes) or a per-item gate that fails-closed on every STRICT item — **the latter would mutate F1 EXECUTE semantics and is auto-REJECT-able under R-RULE-05 / INV-01** (`extension-point-contracts.md:13`: "EXECUTE exactly as written. No skipping…").
5. **Per-tier MCP requirements have to live somewhere on the `/task` side** — donor's table is hard-coded prose; `/task` has no externalized YAML pattern. The recipient must inline the matrix (couples MCP policy to skill content), extract to YAML (introduces a config-loading dependency the skill currently lacks), or move to a sibling skill (creates a new cross-skill data-flow contract).

**Realistic failure mode #1 (Layer A):** A future contributor adds `mcp-servers: [sequential, serena, context7]` to a task's frontmatter expecting it to *control* MCP loading. Nothing happens, because no consumer reads the field. The contributor's mental model diverges from reality and the next reader of the task file is misled about what infrastructure the task depends on. This is the canonical R-RULE-06 failure: ceremony that creates the *appearance* of a contract without the contract actually existing.

**Realistic failure mode #2 (Layer B at the wrong granularity):** If Layer B is implemented at per-item granularity inside F1 EXECUTE — i.e., each STRICT item probes MCP availability before running — then EXECUTE no longer "executes exactly as written" (`extension-point-contracts.md:13`, INV-01). The probe is a side-channel decision that gates whether the item runs, which (a) inserts a non-checklist control surface into the loop, (b) produces silent skips when the probe fails, and (c) breaks INV-04 resumability (the resumed session may probe differently than the original and reach a different gate decision). This collision is real if the implementer chooses the per-item path; the donor characterization's "block task execution" prose does not specify pre-loop vs per-item, so the failure mode is one design-decision away.

**Duplication risk:** `/task` has Critical Rule 6 (`src/superclaude/skills/task/SKILL.md:337`) which prescribes runtime tool selection ("Use Glob/Grep/Read/codebase-retrieval. Do NOT use bash find/grep/cat/head/tail/rg/awk."). Critical Rule 6 is in a *different namespace* (tools, not MCP servers) but it occupies the same rhetorical space — a runtime prescription about what to call. Adding Layer B introduces a *second* runtime prescription about what reasoning infrastructure must be available, and the two coexist without a precedence rule. Two runtime-prescription surfaces in one skill is a future-drift hazard.

**Maintenance cost:** Layer B's tier matrix is policy that will drift. Today's matrix names Sequential + Serena for STRICT; tomorrow a new MCP server (say, a domain-specific knowledge graph) becomes the standard, and the matrix must be re-shipped through `make sync-dev`. The donor matrix lives in *prose*, not data — every update is a SKILL.md edit, not a config bump. Recipient absorbs that ongoing edit cost.

---

## Evidence-Based Weighing

**Position A's strongest point (Layer B closes a real gap):** `/task` today has no model of MCP availability — a STRICT auth migration runs identically whether Sequential is up or down. This is a genuine safety gap, not a hypothetical.

**Position B's answer:** The gap exists, but the *attach mechanism* is not free — the integration sketch routes Layer B through the Task File Validation gate (row 1, C5), which is an admissible attach point *only if* the implementation stays pre-loop. The implementation surface is one design-decision away from per-item granularity (which collides with INV-01). The acceptance criteria for row 1 in `extension-point-contracts.md:60-67` admit pre-loop validators that "produce a user-facing diagnostic and write nothing to the task file beyond a refusal message"; Layer B can attach there *if* it commits to that shape, but the donor prose does not commit. The gap is real; the safe-attach contract is not yet specified. Position B does not contest that pre-loop attach is admissible — it contests that adopting Layer B without specifying pre-loop semantics is buying a coin-flip on whether the implementation lands at C5 or C1.

**Position B's strongest point (Layer A is ceremony with no consumer; Layer B has high coupling cost):** Layer A is straightforwardly R-RULE-06 — implementation mass with no behavioral pattern. Layer B's coupling cost is five distinct burdens, one of which touches an INV.

**Position A's answer:** On Layer A — *concedes* the R-RULE-06 verdict for Layer A. There is no in-repo consumer; Position A's "latent value" argument reduces to "we might build a consumer later," which is exactly the speculative-future-value pattern R-RULE-06 rejects. Position A withdraws Layer A. On Layer B — accepts the five burdens but argues #4 (block-vs-degrade enforcement) can be handled cleanly at row 1 (pre-loop), avoiding the INV-01 collision; the other four burdens are real but tractable extensions, not invariant violations. Burden #2 (tier-source data path) is *not new* — it is a prerequisite called out in `feature-tier-classification.md` and `feature-compliance-gating.md` coupling cost #1, so the cost is shared across the compliance-gating cluster, not paid uniquely for Layer B. If the cluster is adopted, the marginal cost of Layer B is burdens #1, #3, #4-pre-loop, and #5 — still real, but proportional.

**Unanswered point against Position A:** The donor's tier matrix is policy-as-prose, not policy-as-data. The maintenance cost (Position B's closing point) is ongoing and Position A did not address it. This counts against Position A — Layer B as proposed by the donor is a maintenance liability that the recipient inherits.

**Unanswered point against Position B:** Position B's "two runtime-prescription surfaces" duplication argument is weak — Critical Rule 6 governs *tools* (Glob/Grep/Read/Bash), Layer B governs *MCP servers* (Sequential/Serena/Context7). These are non-overlapping namespaces. The duplication risk is rhetorical, not substantive. This counts against Position B (mildly) — the duplication argument does not survive scrutiny.

**Net effect:** Layer A → R-RULE-06 REJECT (Position A withdrew). Layer B → contested. The integration sketch is admissible at row 1 (C5) *if and only if* the implementation commits to pre-loop semantics. The maintenance-cost concern is unresolved. The five-burden coupling cost is real but partly shared with the compliance-gating cluster.

---

## Scored Verdict

The two layers are scored separately because they have independently shaped value and cost.

### Layer A — Frontmatter `mcp-servers:` advertisement

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **1** | No in-repo consumer (`feature-mcp-declarations.md:91`). Adds zero observable behavior. Forward-bet on a hypothetical capability-auditor that may never ship. |
| **C (Complementarity, 1–5)** | **5** | Native-fit at row 13 (Required frontmatter schema slot, C5; `extension-point-contracts.md:169-175`) — additive metadata field, no F1 change. |
| **K (Cost, 1–5)** | **2** | Low — one frontmatter line plus Skill-loader-recognition verification. No new mechanism. |
| **Net = (V × C) / K** | **(1 × 5) / 2 = 2.5** | |
| **R-RULE-06 override** | — | Layer A is ceremony with no behavioral teeth — **R-RULE-06 REJECT** regardless of arithmetic. Position A withdrew this layer in the weighing round. |

**Verdict: REJECT** (R-RULE-06 / `feature-mcp-declarations.md:91`).

### Layer B — Per-tier required-server matrix + circuit breaker

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **3** | Closes a real safety gap (STRICT items today run identically whether reasoning MCPs are up or down). Value is bounded by (a) the user's MCP install actually including the named servers and (b) the recipient implementing the probe — neither is free. |
| **C (Complementarity, 1–5)** | **3** | C-band C3: attaches at row 1 (Task File Validation gate, C5; `extension-point-contracts.md:60-67`) **but only if** the implementation commits to pre-loop semantics; the donor prose does not specify pre-loop vs per-item, so a per-item implementation would collide with INV-01 and force C1 / auto-REJECT. Net C-band is C3 — "extension surface exists but must be widened with a new hook (the probe)" (`extension-point-contracts.md:25`). |
| **K (Cost, 1–5)** | **4** | Five distinct burdens (`feature-mcp-declarations.md:96-110`): new frontmatter slot, tier-source data path, runtime probe, block enforcement, per-tier matrix location. Burden #2 (tier-source) is shared with the compliance-gating cluster; the other four are paid uniquely. Plus ongoing maintenance of the tier matrix as MCP servers drift (Position B's unanswered point). |
| **Net = (V × C) / K** | **(3 × 3) / 4 = 2.25** | |

**Verdict: DEFER** (Net = 2.25 falls in the DEFER band, `1.5 ≤ Net < 3`).

**Rationale for DEFER (not ADAPT):** Layer B's value is contingent on the compliance-gating cluster providing a tier source (burden #2). If the cluster is ADOPTed in a later debate, Layer B's marginal cost drops by one burden and Net rises to (3 × 3) / 3 = 3.0 (right at the ADAPT/DEFER threshold). The right disposition is to defer Layer B until the cluster's verdict is known, then re-score. The DEFER verdict is *contingent on the compliance-gating cluster*, not unconditional.

### Composite verdict for D02 + D27

- **D02 (Layer A):** REJECT (R-RULE-06).
- **D27 (Layer B):** DEFER (Net = 2.25, contingent on compliance-gating cluster verdict).

**Stack-rank inputs (for T04.05):**
- D02 / Layer A: V=1, C=5, K=2, Net=2.5, **REJECT** (R-RULE-06 override).
- D27 / Layer B: V=3, C=3, K=4, Net=2.25, **DEFER**.

**Phase 5 forwarded question:** If D27 / Layer B is adopted contingent on the compliance-gating cluster, the integration sketch must commit to **pre-loop probe semantics** at row 1 (Task File Validation gate). A per-item probe inside F1 EXECUTE would violate INV-01 and force C1 auto-REJECT. This commitment is load-bearing for the verdict — losing it flips the score.

**Note on missing T03.01 evidence:** `invariant-bounds.md` is absent (Phase 3 checkpoint Fail). The INV-01 collision risk for per-item-probe implementations is sourced from the one-line INV-01 label at `extension-point-contracts.md:13` plus row 4's reject criteria at `extension-point-contracts.md:90-93`. A worked failure-mode example would strengthen Position B's per-item-probe argument; without it, the verdict relies on the row-4 reject criteria as the operative constraint. The verdict above stands either way (DEFER is conservative).
