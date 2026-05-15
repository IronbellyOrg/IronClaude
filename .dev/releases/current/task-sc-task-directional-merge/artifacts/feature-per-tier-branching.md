# Feature Characterization — Per-Tier Flow Branching

**Task:** T02.02 — Characterize TFEP & per-tier flow branching
**Roadmap Item:** R-005
**Donor Catalog Anchor:** D10 (command-side dispatch) and D15 (skill-side per-tier execution workflows) — see `donor-feature-catalog.md` lines 56, 66
**Side of Truth (R-RULE-10):** `src/superclaude/commands/task.md` and `src/superclaude/skills/sc-task-protocol/SKILL.md` (both canonical, both byte-identical to their `.claude/` mirrors)
**Generated:** 2026-05-15

---

## 1. What It Is

Per-tier flow branching is the **two-level dispatch mechanism** that converts a tier label (the output of the tier classification model, D09) into different observable execution paths. It has two strictly distinct layers:

- **Layer 1 — Command-side dispatch (D10):** a four-way switch at `src/superclaude/commands/task.md:93-101` (`src/`) that decides whether the command terminates *inside itself* (EXEMPT, LIGHT) or *delegates to the protocol skill* (STANDARD, STRICT).
- **Layer 2 — Skill-side per-tier execution workflows (D15):** four distinct step-lists at `src/superclaude/skills/sc-task-protocol/SKILL.md:76-109` (`src/`) — one per tier — defining exactly what happens once a tier has been routed.

The two layers together answer the question "*which* flow runs for tier X?" *Layer 1 selects the executor* (command vs skill); *Layer 2 selects the procedure* (which step-list runs inside that executor). The combination is the donor's "tier mix → execution cost" routing: a typo (LIGHT) runs four steps inside the command and exits; a security migration (STRICT) runs eleven steps inside the skill plus a verification sub-agent spawn.

## 2. How It Works (Mechanism + Entry/Exit Conditions + `file:line` Evidence)

### Layer 1 — Command-side dispatch

**Mechanism (four-way switch on `TIER`, `src/superclaude/commands/task.md:95-101`, `src/`):**

After the classification header has been emitted as text (D08), the command proceeds based on tier:

- **EXEMPT** (`src/superclaude/commands/task.md:97`, `src/`): "Execute immediately — answer the question or perform the read-only operation. No Skill invocation needed."
- **LIGHT** (`src/superclaude/commands/task.md:98`, `src/`): "Execute the change directly. No Skill invocation needed for trivial changes."
- **STANDARD** (`src/superclaude/commands/task.md:99-100`, `src/`): Invokes `Skill sc:task-protocol` — control transfers to the skill at `src/superclaude/skills/sc-task-protocol/SKILL.md`.
- **STRICT** (`src/superclaude/commands/task.md:99-100`, `src/`): Same `Skill sc:task-protocol` invocation as STANDARD — the skill itself further branches inside its Execution Phase.

**Entry conditions (Layer 1):**
- The classification header has been emitted as the very first output (Critical Rule 4, `src/superclaude/commands/task.md:56`, `src/`).
- The `TIER` value is one of `{STRICT, STANDARD, LIGHT, EXEMPT}` (Critical Rule 3, `src/superclaude/commands/task.md:55`, `src/`); other values are explicitly INVALID.
- If `--compliance` was supplied, the override path was already taken upstream of classification (`src/superclaude/commands/task.md:69`, `src/`) — Layer 1 still runs but on the overridden tier.

**Exit conditions (Layer 1):**
- **EXEMPT/LIGHT branches** terminate the command turn directly inside the command — no Skill tool call is emitted; the model performs the read-only operation or trivial change and the turn ends.
- **STANDARD/STRICT branches** emit a `Skill sc:task-protocol` invocation; control transfers to the skill, which runs Layer 2.

### Layer 2 — Skill-side per-tier execution workflows

**Mechanism (four per-tier step-lists, `src/superclaude/skills/sc-task-protocol/SKILL.md:76-109`, `src/`):**

The Execution Phase (Section 3 of the skill) carries four explicit, tier-keyed procedures. Note that all four are defined even though the command only routes STANDARD/STRICT to the skill — the LIGHT/EXEMPT entries are reachable only via the skill's failsafe emission path (`src/superclaude/skills/sc-task-protocol/SKILL.md:9`, `src/`) where the skill was invoked without prior command-layer classification.

- **STRICT (11 steps, `src/superclaude/skills/sc-task-protocol/SKILL.md:80-91`, `src/`):**
  1. `mcp__serena__activate_project` (project activation)
  2. `git status` (verify working directory clean)
  3. `codebase-retrieval` (load codebase context)
  4. `list_memories` → `read_memory` (relevant-memory check)
  5. Identify all affected files and test files
  6. Make changes with full checklist
  7. Identify all files that import changed code
  8. Update all affected files
  9. Spawn verification agent (`quality-engineer`)
  10. Run comprehensive tests: `pytest [path] -v`
  11. Answer adversarial questions

- **STANDARD (5 steps, `src/superclaude/skills/sc-task-protocol/SKILL.md:93-98`, `src/`):**
  1. Load context via `codebase-retrieval`
  2. Search downstream impacts (`find_referencing_symbols` OR `grep`)
  3. Make changes
  4. Run affected tests OR document manual verification
  5. Verify basic functionality

- **LIGHT (4 steps, `src/superclaude/skills/sc-task-protocol/SKILL.md:100-104`, `src/`):**
  1. Quick scope check (files/lines within bounds)
  2. Make changes
  3. Quick sanity check (syntax valid, no obvious errors)
  4. Proceed with judgment

- **EXEMPT (2 steps, `src/superclaude/skills/sc-task-protocol/SKILL.md:106-108`, `src/`):**
  1. Execute immediately
  2. No verification overhead

**Entry conditions (Layer 2):**
- The skill has been invoked via the command's dispatch (`src/superclaude/commands/task.md:99-100`, `src/`), OR the skill is the failsafe emitter (`src/superclaude/skills/sc-task-protocol/SKILL.md:9`, `src/`).
- A tier value is known — either inherited from the command's classification header (`src/superclaude/skills/sc-task-protocol/SKILL.md:49-51`, `src/`: "Classification was handled by the `/sc:task` command before this skill was invoked") or freshly emitted by the failsafe path.
- The Verification Routing table (`src/superclaude/skills/sc-task-protocol/SKILL.md:114-119`, `src/`) is consulted *after* the Execution Phase to decide verification routing — it does NOT gate entry to Layer 2.

**Exit conditions (Layer 2):**
- **STRICT exit:** the verification agent has returned, comprehensive tests have run, and adversarial questions have been answered — flow proceeds to Verification Phase routing (sub-agent quality-engineer, `src/superclaude/skills/sc-task-protocol/SKILL.md:116`, `src/`).
- **STANDARD exit:** affected tests have run OR manual verification documented — flow proceeds to direct test execution (`src/superclaude/skills/sc-task-protocol/SKILL.md:117`, `src/`).
- **LIGHT exit:** sanity check completed — flow skips verification (`src/superclaude/skills/sc-task-protocol/SKILL.md:118`, `src/`).
- **EXEMPT exit:** immediate execution complete — flow skips verification (`src/superclaude/skills/sc-task-protocol/SKILL.md:119`, `src/`).

### Branch-to-flow mapping (complete)

| Classifier branch | User-input shape that selects it | Layer 1 destination | Layer 2 procedure | Layer 2 step count | Verification routing |
|---|---|---|---|---|---|
| **STRICT** | Prompt contains keywords from `{security, authentication, authorization, database, migration, refactor, breaking change, encrypt, token, session, oauth}` OR matches compound phrases `{"fix security", "add authentication", "update database", "change api"}` OR triggers context boosters (`>2` files +0.3, security paths +0.4); also reachable via `--compliance strict` override. (`src/superclaude/commands/task.md:71-75`, `src/`) | Skill `sc:task-protocol` (`task.md:99-100`) | 11-step STRICT workflow (`SKILL.md:80-91`) | 11 | Sub-agent `quality-engineer`, 3-5K tokens, 60s (`SKILL.md:116`) |
| **EXEMPT** | Prompt starts with `{what, how, why, explain}` OR contains keywords `{explain, search, commit, push, plan, discuss, brainstorm}` OR is read-only (+0.4) / git operation (+0.5) / docs-only path (+0.5); also reachable via `--compliance exempt`. (`src/superclaude/commands/task.md:77-80`, `src/`) | Command-internal (no Skill invocation) (`task.md:97`) | 2-step EXEMPT workflow (`SKILL.md:106-108`) — reachable only via failsafe path | 2 | Skip verification, 0 tokens (`SKILL.md:119`) |
| **LIGHT** | Prompt contains keywords `{typo, comment, whitespace, lint, docstring, formatting, spacing, minor}` OR compound phrases `{"quick fix", "minor change", "fix typo", "refactor comment"}` OR single-file scope (+0.1) / ≤50 lines; also reachable via `--compliance light`. (`src/superclaude/commands/task.md:82-85`, `src/`) | Command-internal (no Skill invocation) (`task.md:98`) | 4-step LIGHT workflow (`SKILL.md:100-104`) — reachable only via failsafe path | 4 | Skip verification, 0 tokens (`SKILL.md:118`) |
| **STANDARD** | Default fallback when no higher-priority match; typically keywords `{implement, add, create, update, fix, build, modify, change}`. (`src/superclaude/commands/task.md:87-89`, `src/`) | Skill `sc:task-protocol` (`task.md:99-100`) | 5-step STANDARD workflow (`SKILL.md:93-98`) | 5 | Direct test execution, 300-500 tokens, 30s (`SKILL.md:117`) |

**Orphan branch check:** every tier in the closed enumeration `{STRICT, STANDARD, LIGHT, EXEMPT}` (`src/superclaude/commands/task.md:55`, `src/`) maps to exactly one Layer 1 destination and exactly one Layer 2 procedure. There are no orphan branches. The EXEMPT/LIGHT Layer 2 procedures are reachable only when the skill is invoked without a prior command-layer classification — under normal command-driven flow they are *unused* but defined for the failsafe path (`src/superclaude/skills/sc-task-protocol/SKILL.md:9`, `src/`).

## 3. What It Produces

**Layer 1 produces** a control-flow effect:
- For EXEMPT/LIGHT: the command turn terminates inside the command without a tool call (other than whatever Read/Edit the inline execution emits for LIGHT).
- For STANDARD/STRICT: a `Skill sc:task-protocol` invocation is emitted; the model's next output is the skill's pre-emission guard block (`src/superclaude/skills/sc-task-protocol/SKILL.md:7-9`, `src/`) followed by the Execution Phase content.

**Layer 2 produces** the per-tier observable artifacts:
- **STRICT:** at minimum, an `mcp__serena__activate_project` call, a `git status` invocation, a `codebase-retrieval` query, a memory check, an Edit/MultiEdit batch covering changed-plus-importing files, an `Agent` (quality-engineer) spawn, a `pytest -v` invocation, and a written answer to the donor's standardised adversarial questions (donor source does not enumerate the questions inline; they are the verification agent's responsibility).
- **STANDARD:** a `codebase-retrieval` query, a `find_referencing_symbols` or `Grep` call, an Edit/MultiEdit, a `Bash`-driven test invocation OR a Notes-block manual-verification record.
- **LIGHT:** a short scope-check assertion, an Edit, a sanity-check assertion.
- **EXEMPT:** the answer text itself, OR the read-only operation (`Read`, `Grep`, `git status`, doc retrieval).

**The combined Layer 1 + Layer 2 produces a *cost gradient*** observable in token spend per task: EXEMPT (≈0 verification tokens) → LIGHT (≈0) → STANDARD (300-500 verification tokens, 30s) → STRICT (3-5K verification tokens, 60s). The gradient is the donor's primary value-axis output.

## 4. What Invokes It

- **Layer 1 invocation:** the `/sc:task` command, immediately after the classification header has been emitted. Sole entry: `src/superclaude/commands/task.md:95` (`src/`) — "After emitting the classification header as text, proceed based on tier."
- **Layer 2 invocation:** the protocol skill's `Behavioral Flow → 3. Execution Phase` (`src/superclaude/skills/sc-task-protocol/SKILL.md:76`, `src/`) — entered after the (no-op for command-driven flow) Section 0 classification block and the optional Confidence Display (`src/superclaude/skills/sc-task-protocol/SKILL.md:59-74`, `src/`).
- **Indirect invocation paths:**
  - The `--compliance` override (`src/superclaude/commands/task.md:69`, `src/`) bypasses the classifier but still feeds Layer 1.
  - The skill's failsafe emission path (`src/superclaude/skills/sc-task-protocol/SKILL.md:9`, `src/`) can produce a header without command involvement, in which case Layer 2 still runs but Layer 1 was never executed.
- **Reader/parser of the dispatch output:** the model itself — there is no external parser of "the model just said `Skill sc:task-protocol`." The dispatch is realised by the LLM's compliance with the worked examples and the explicit instruction.

## 5. What It Depends On

- **The tier classification model (D09).** Both layers consume a tier label; without D09 producing one of `{STRICT, STANDARD, LIGHT, EXEMPT}`, neither layer can route. See `feature-tier-classification.md`.
- **The classification header (D08).** Layer 1 reads the `TIER` field from the header (or from its own classification step) — the dispatch is gated on the header having been emitted (`src/superclaude/commands/task.md:95`, `src/`: "After emitting the classification header as text").
- **The closed tier enumeration** at `src/superclaude/commands/task.md:55, 61` (`src/`) — Layer 1 hard-codes the four-way dispatch on these exact strings.
- **The Skill tool availability.** Layer 1's STANDARD/STRICT branch emits a `Skill sc:task-protocol` call (`src/superclaude/commands/task.md:99-100`, `src/`). The command's frontmatter allowed-tools list at `src/superclaude/commands/task.md:6` (`src/`) declares `Skill` as available — without it, Layer 1's STANDARD/STRICT branch fails silently.
- **Layer 2's tool dependencies (per tier):**
  - **STRICT** depends on: `mcp__serena__activate_project` (serena MCP), `Bash` (git status, pytest), `codebase-retrieval` (auggie MCP), `list_memories` / `read_memory` (serena), `Agent` tool (verification-agent spawn).
  - **STANDARD** depends on: `codebase-retrieval` (auggie MCP), `find_referencing_symbols` (serena MCP) OR `Grep`, `Bash` (tests).
  - **LIGHT** depends on: no external tools (judgment-only).
  - **EXEMPT** depends on: no external tools (immediate execution).
- **The MCP Integration matrix** at `src/superclaude/skills/sc-task-protocol/SKILL.md:253-263` (`src/`) — STRICT *requires* Sequential and Serena with no fallback permitted; STANDARD requires Sequential and Context7 with fallback allowed. If the required servers are unavailable for STRICT, Layer 2 blocks execution per the circuit breaker (D27).
- **The Verification Routing table** at `src/superclaude/skills/sc-task-protocol/SKILL.md:110-119` (`src/`) — runs *after* Layer 2 and provides the cost/timeout discipline for each tier's verification step.

## 6. Standalone Value Claim

**Claim:** Per-tier branching is the *only mechanism* that translates the tier label into observable cost differentiation. Without it, a tier label is metadata with no behavioural consequence. With it, the donor delivers concrete cost-gradient routing:

1. **EXEMPT/LIGHT terminate inside the command and avoid the Skill round-trip.** The `Skill sc:task-protocol` invocation costs ≥1 tool call (the Skill tool itself) and a context switch into the skill's content. For "explain how X works", that round-trip is pure overhead; Layer 1's command-internal branch (`src/superclaude/commands/task.md:97-98`, `src/`) eliminates it.
2. **STRICT spends 11 steps + sub-agent spawn + 60s verification on changes that warrant it, and not on changes that don't.** The 11-step workflow (`src/superclaude/skills/sc-task-protocol/SKILL.md:80-91`, `src/`) plus the 3-5K-token sub-agent (`SKILL.md:116`) is roughly an order of magnitude more expensive than STANDARD; per-tier branching is the gate that decides which tasks pay it.
3. **STANDARD pays a moderate-cost middle path** — `codebase-retrieval` + `find_referencing_symbols` + tests, ~300-500 verification tokens, 30s. This is the donor's default "moderate scope" lane and the most-used path for routine implementation work.
4. **The two-layer split keeps the command lightweight for EXEMPT/LIGHT** (no Skill load) while concentrating the heavyweight execution-and-verification machinery in the skill where STANDARD/STRICT can share it.

For a 20-item mixed-tier batch — 5 typo fixes (LIGHT), 5 documentation explanations (EXEMPT), 8 feature additions (STANDARD), 2 security migrations (STRICT) — per-tier branching is the difference between paying STRICT cost on all 20 items (≈100K verification tokens) and paying it on 2 (≈10K), with the other 18 paying ≈4K total: a 6-7× total verification-cost reduction *if and only if* the tier mix actually contains heterogeneous items.

**Non-value condition (R-RULE-04, concrete, not boilerplate):**

The value claim does NOT hold under any of these specific conditions:

- **Homogeneous-tier batches:** if all 20 items in the example were STANDARD (the default — `src/superclaude/commands/task.md:87-89`, `src/`), Layer 1 always dispatches to the same Skill invocation and Layer 2 always runs the same 5-step procedure. The branching is *evaluated* every turn (token cost ~50-150 per dispatch decision) but never *branches anywhere different*. The cost-gradient claim collapses to "always-STANDARD" with no benefit.
- **The skill is invoked directly without command-layer dispatch.** If a downstream caller invokes `Skill sc:task-protocol` without going through `/sc:task` (the failsafe path at `src/superclaude/skills/sc-task-protocol/SKILL.md:9`, `src/`), Layer 1 never runs — there is no command-internal EXEMPT/LIGHT shortcut, and even EXEMPT items pay the full skill-invocation overhead. The skill's Layer 2 EXEMPT and LIGHT step-lists are present for this case (`SKILL.md:100-108`, `src/`), but the Layer 1 cost-avoidance is lost.
- **The `Skill` tool is unavailable or fails.** The command's frontmatter declares `Skill` (`src/superclaude/commands/task.md:6`, `src/`); if the runtime denies it or the Skill invocation errors, the STANDARD/STRICT branch silently degrades to "command tries to do it inline" — which the worked examples don't cover. The branching value depends on the Skill round-trip *working*.
- **MCP servers required by STRICT are unavailable.** The STRICT step list demands serena (`mcp__serena__activate_project`, `list_memories`, `read_memory`) and codebase-retrieval (auggie) (`src/superclaude/skills/sc-task-protocol/SKILL.md:81, 83-84`, `src/`). The MCP Integration matrix (`SKILL.md:253-263`, `src/`) says STRICT BLOCKS execution when these are unavailable — so on a host without serena/auggie installed, STRICT branching produces a hard halt rather than degraded execution. The "STRICT pays the right cost on the right tasks" value claim becomes "STRICT cannot run at all on minimally-configured hosts."
- **Sessions that invoke `/task` instead of `/sc:task`.** `/task` has no tier-aware dispatch — there is no Layer 1 analog in the recipient's F1 loop, and no Layer 2 per-tier step-list. For an entirely `/task`-driven workflow, per-tier branching does not exist at all and the value claim is vacuous on that surface.

## 7. Coupling Cost Claim

**Claim:** Attaching per-tier branching to `/task` requires the recipient to take on **all six** of the following concrete burdens; partial adoption (e.g. taking the four step-lists without the dispatch layer) collapses to a tier-tag-without-behaviour anti-pattern.

1. **A two-track executor model that `/task` does not have.** `/task`'s F1 loop at `src/superclaude/skills/task/SKILL.md:83-98` (`src/`) is a *single* execution path: READ → IDENTIFY → EXECUTE → UPDATE → REPEAT. Layer 1's "EXEMPT/LIGHT terminate inside the command, STANDARD/STRICT delegate to a skill" model requires either (a) wrapping the F1 loop in a per-item dispatch step that picks a tier-shaped sub-workflow before EXECUTE, or (b) authoring four parallel skills (one per tier) and selecting which to invoke per item. Either way, the recipient must invent a meta-dispatch surface that does not exist today.

2. **A `Tier:` field per-item or per-task.** `/task`'s required frontmatter schema at `src/superclaude/skills/task/SKILL.md:69` (`src/`) requires only `id, title, status, created_date`. Layer 1's dispatch decision consumes a tier per turn; the recipient must extend its schema (either per-task or per-checklist-item) to carry one. This burden is shared with D09 — but it surfaces *again* here because Layer 1 cannot dispatch without a tier source.

3. **A way to invoke or inline four different workflows from inside the F1 EXECUTE step.** Layer 2's four step-lists (`src/superclaude/skills/sc-task-protocol/SKILL.md:80-108`, `src/`) are conceptually four different "what to do" procedures. The F1 EXECUTE step's action-to-tool map at `src/superclaude/skills/task/SKILL.md:89-96` (`src/`) currently has six action verbs (spawn subagent, read+produce, edit, run command, present, update frontmatter). Adding tier-aware behavior means either (a) extending the action verbs with tier-keyed variants (proliferation), (b) wrapping every action verb with a tier-aware pre-step (verbosity), or (c) selecting a different *sub-workflow* per item before entering EXECUTE (new mechanism). None match the donor's "four step-lists indexed by tier" shape directly.

4. **A Phase-Gate QA stance that scales with tier.** `/task`'s Phase-Gate QA at `src/superclaude/skills/task/SKILL.md:182-211` (`src/`) is single-method: spawn `rf-qa` with an adversarial stance, run a 3-cycle fix loop. The donor's Verification Routing table (`src/superclaude/skills/sc-task-protocol/SKILL.md:114-119`, `src/`) varies by tier: sub-agent for STRICT, direct test exec for STANDARD, skip for LIGHT/EXEMPT. To inherit per-tier branching's cost gradient, the recipient must extend Phase-Gate QA to accept a tier hint and select method + cost budget + timeout per item. The current single-method gate is incompatible with the donor's four-way table.

5. **An MCP-availability gate matching the donor's circuit breaker.** STRICT in Layer 2 hard-depends on serena and codebase-retrieval (`src/superclaude/skills/sc-task-protocol/SKILL.md:81, 83`, `src/`); the MCP Integration matrix (`SKILL.md:253-263`, `src/`) blocks STRICT execution when these are unavailable. `/task` has no per-item MCP-availability check — the Task File Validation gate at `src/superclaude/skills/task/SKILL.md:64-73` (`src/`) checks frontmatter and well-formedness only. The recipient must invent a tier-aware MCP gate that runs before EXECUTE for STRICT-tier items; without it, STRICT items can be enqueued on hosts that cannot run them, and the donor's hard-halt safety property is lost.

6. **A LIGHT/EXEMPT "skip verification" semantic compatible with `/task`'s phase-gate model.** `/task` runs Phase-Gate QA between every phase (`src/superclaude/skills/task/SKILL.md:182-211`, `src/`); the donor's LIGHT/EXEMPT branches skip verification entirely (`src/superclaude/skills/sc-task-protocol/SKILL.md:118-119`, `src/`). To inherit the donor's cost-skip behaviour, the recipient must either (a) make Phase-Gate QA conditional on tier (breaks the current invariant that QA always runs), (b) introduce per-item QA-skip annotations (Phase-Gate QA can no longer "see" individual items, only phase outputs), or (c) accept that LIGHT/EXEMPT items still pay Phase-Gate QA cost (loses the donor's cost-gradient value). Each choice trades a different property of the recipient's existing model.

**Net coupling cost:** the recipient must invent a meta-dispatch surface (1), extend its frontmatter schema (2), accept tier-aware behaviour inside EXECUTE (3), make Phase-Gate QA tier-sensitive (4), gate MCP availability per tier (5), and reconcile the skip-verification semantic with the always-run Phase-Gate QA invariant (6) — six distinct extensions, each touching a different `/task` invariant.

---

## Cross-Reference

- D10 in `donor-feature-catalog.md` (command-side dispatch / flow branching) — primary anchor for Layer 1.
- D15 in `donor-feature-catalog.md` (per-tier execution workflows) — primary anchor for Layer 2.
- D09 (tier classification model) — upstream producer; both layers depend on it. See `feature-tier-classification.md`.
- D08 (classification header emission) — upstream gate; Layer 1 dispatches *after* the header. See `feature-classification-header.md`.
- D16 (verification routing table) — downstream of Layer 2; defines verification method per tier.
- D17/D18 (Critical Path / Trivial Path Overrides) — modulate Layer 2's verification routing irrespective of tier.
- D27 (MCP Integration — required servers by tier + circuit breaker) — modulates Layer 2's STRICT entry condition.
- `recipient-extension-points.md` row 4 (F1 EXECUTE item-type dispatch at `src/superclaude/skills/task/SKILL.md:89-96`) — primary attach surface for Layer 1's meta-dispatch on the recipient side.
- `recipient-extension-points.md` row 10 (Phase-Gate QA at `src/superclaude/skills/task/SKILL.md:182-211`) — primary attach surface for Layer 2's verification routing on the recipient side.
- `recipient-extension-points.md` row 13 (Required frontmatter schema slot at `src/superclaude/skills/task/SKILL.md:69`) — where a `Tier:` field would attach.
