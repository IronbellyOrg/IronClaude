---
variant: 1
lens: architect
title: "Ataraxy-Labs Incorporation — Phased, One-Tool-at-a-Time Integration Architecture with Hard Kill/Keep Gates"
author_model: opus
created: 2026-06-04
order: sem → inspect → weave
integration: hybrid (MCP stdio servers + skill wiring)
eval_scope: framework-native first
cost_lens: all-in (tokens + latency + maintenance)
thesis: >
  Treat incorporation as a reversible state machine, not a feature rollout. Each
  tool passes through an identical 5-stage pipeline (Spike → Shadow → Gated decision →
  Integration → Re-eval) with a HARD kill/keep gate between tools. sem-core is the
  load-bearing foundation: everything downstream depends on the entity-extraction
  contract sem establishes, so sem's gate is the single most important decision in
  the plan. Nothing replaces a status-quo surface until shadow mode proves the
  replacement is safe; everything is removable in one command.
---

# Variant 1 (Architect Lens): Phased Incorporation Architecture

## 0. Core Thesis

The dominant failure mode this plan exists to prevent is **silent coupling**: you
register three MCP servers, wire `inspect_triage` into the Auggie review pass,
make `weave` the global git merge driver, and six months later the framework
cannot function without a Rust toolchain that nobody on the team can debug — and
backing out means surgery across five skills.

The architectural answer is to **never let a tool become load-bearing until a gate
proves it earns its coupling**, and to make every coupling point a **seam, not a
weld**. Concretely:

1. **One tool at a time, gated.** sem must clear its keep-gate before inspect's
   spike begins. inspect before weave. The gate is not a vibe — it is a scorecard
   with go/no-go thresholds defined *before* the eval runs.

2. **Five identical stages per tool.** Spike → Shadow → Gated decision →
   Integration → Re-eval. Identical structure means the eval harness, the
   decision-record template, and the rollback runbook are written once and reused
   three times. Architectural uniformity is the point.

3. **Shadow/advisory before replacement, always.** A tool runs *alongside* the
   status-quo surface and its output is logged-and-compared, never acted upon,
   until the comparison data clears the gate. `inspect` never gates a PR in shadow
   mode. `weave` never resolves a real merge in shadow mode (`weave preview` only).

4. **Every coupling is a documented, single-command rollback.** `claude mcp
   remove`, `sem unsetup`, `weave unsetup`, and a skill-level feature flag that
   reverts to the status-quo code path. Reversibility is a *tested* property, not
   an aspiration — the rollback runbook is executed once per tool during the spike
   as a dry-run.

5. **sem-core is the foundation; honor the dependency order.** sem establishes the
   entity-extraction contract (what counts as an entity, how the token budget is
   computed, the 27-language coverage envelope). inspect's danger scoring and
   weave's semantic merge both *consume* entity-level structure. If sem's entity
   model is unreliable on this repo's code, inspect and weave inherit that
   unreliability. So sem's gate is not just "is sem useful" — it is "is the shared
   substrate trustworthy enough to build two more tools on top of."

This proposal is deliberately **opinionated about structure and reversibility** and
deliberately **thin on eval statistics** (sample-size power analysis, judge
calibration) — those are the analyzer lens's job, and I flag exactly where my plan
defers to it (§9 Open Questions, §10 Honest Weaknesses).

---

## 1. The Incorporation State Machine

Each tool is a state machine. States are sequential; backward transitions
(rollback) are always available and always cheap.

```
                  ┌─────────────────────────────────────────────────────┐
                  │                                                       │
   ┌─────────┐   ┌▼────────┐   ┌──────────────┐   ┌─────────────┐   ┌────▼──────┐
   │ S0 SPIKE│──▶│ S1      │──▶│ S2 GATED     │──▶│ S3          │──▶│ S4        │
   │ (build, │   │ SHADOW  │   │ DECISION     │   │ INTEGRATION │   │ RE-EVAL   │
   │ enumerate,│  │ (compare,│  │ (scorecard   │   │ (flag-gated │   │ (steady-  │
   │ dry-run  │   │ log, no  │  │ → keep/kill) │   │ wiring +    │   │ state     │
   │ rollback)│   │ action)  │  │              │   │ shadow→live)│   │ confirm)  │
   └────┬────┘   └────┬─────┘   └──────┬───────┘   └──────┬──────┘   └────┬──────┘
        │             │                │ KILL             │                │
        │ ROLLBACK    │ ROLLBACK       ▼                  │ ROLLBACK       │ DEGRADE
        └─────────────┴────────────▶ S-KILL ◀─────────────┴────────────────┘
                                   (deregister,
                                    unsetup,
                                    flag off,
                                    archive evidence)
```

**State definitions (identical for all three tools):**

| State | Entry condition | Exit artifact | Rollback cost |
|-------|-----------------|---------------|---------------|
| **S0 Spike** | Prior tool reached S3+ (or this is sem) | Tool builds; MCP tools enumerated; rollback dry-run passes; toolchain-cost log | N/A (nothing wired) |
| **S1 Shadow** | S0 clean | Comparison dataset (tool output vs status-quo baseline), logged side-by-side, **zero production effect** | Delete log dir; uninstall binary |
| **S2 Gated decision** | S1 dataset complete + N scenarios met | Filled scorecard + decision record (keep/kill + evidence citations) | Decision is the gate; no code touched yet |
| **S3 Integration** | S2 = KEEP | Skill wiring behind a feature flag, defaulting to advisory; then flag flipped to live after a soak window | Flip flag off → status-quo path restored |
| **S4 Re-eval** | S3 live ≥ soak window | Steady-state confirmation; toolchain-maintenance burden re-measured against S0 estimate | Same as S3 |
| **S-KILL** | Any gate fails / rollback invoked | `claude mcp remove`, `sem/weave unsetup`, flag removed, evidence archived to `.dev/releases/backlog/AtaraxyLabs/decisions/<tool>-KILL.md` | This **is** the rollback |

**The between-tool gate (the most important rule):** inspect's S0 cannot begin
until sem reaches **S3 (Integration, live)** AND sem's S2 verdict is KEEP. weave's
S0 cannot begin until inspect reaches S3 live AND KEEP. Rationale: we want each
tool's integration to be *exercised by real use* before we add the next tool's
complexity, so that if the toolchain-maintenance cost is going to bite, it bites
with one tool in play, not three.

**Escape hatch:** If sem is KILLED at S2, the plan does **not** automatically
proceed to inspect — because inspect and weave both depend on the entity-extraction
substrate sem validates. A sem KILL triggers a **plan-level checkpoint** (§8): do
inspect/weave still make sense if the shared foundation failed on our code? Default
answer: no — archive the whole initiative. This is the dependency-ordering payoff.

---

## 2. sem — Phase Plan (the foundation tool)

sem is evaluated first because **everything downstream consumes its entity model**.
sem's gate answers two questions at once: (a) is sem itself useful? (b) is the
sem-core substrate trustworthy on *our* code?

### S0 — Spike (build + enumerate + rollback dry-run)

**Goals:** prove sem builds in this environment, enumerate its real surface,
resolve the binary-name collision, and *execute the rollback once* before any
wiring exists.

- **Install** via `cargo install --git ... sem-cli` (primary; the framework will
  acquire a Rust toolchain here — log build time, disk, transitive crate count as
  the first toolchain-cost data point). Record `npm i -D @ataraxy-labs/sem` and
  `brew install sem-cli` as fallback acquisition paths for the maintenance matrix.
- **Resolve the `sem` ↔ GNU-parallel collision NOW, before anything else.** The
  architectural decision: **never invoke bare `sem` from any framework code.**
  Always invoke by absolute path or as `sem-cli` (npm-installed binary name). The
  MCP server binary is `sem-mcp` (no collision). Document this as a hard rule;
  the collision must never reach a skill or a `setup` git-integration step.
- **Enumerate the 6 MCP tools** against a live `sem-mcp` stdio server:
  `sem_entities / sem_diff / sem_blame / sem_impact / sem_log / sem_context`.
  Capture each tool's input/output schema into
  `.dev/releases/backlog/AtaraxyLabs/spikes/sem-mcp-schema.md`.
- **Rollback dry-run:** register `sem-mcp` via `claude mcp add --transport stdio
  --scope user sem -- sem-mcp`, confirm it appears, then `claude mcp remove sem`
  and confirm clean removal. This proves the rollback path *before* we rely on it.
- **Known-limitation probes:** confirm chunk-based fallback on unrecognized file
  types (this repo has `.md`, `.py`, `.json`, `.toml`); confirm `sem context`
  **omits the target entity when it exceeds the token budget** (a correctness
  footgun for the `code-review` use case — must be caught here, not in prod).

**S0 exit gate (kill if any fail):** sem builds; `sem-mcp` registers+deregisters
cleanly; collision-avoidance rule documented; 6 MCP schemas captured; the
target-entity-omission behavior is characterized.

### S1 — Shadow eval (compare, never replace)

sem runs **alongside** the status-quo, producing parallel artifacts that are logged
and compared but **never fed to a model or a user decision**.

**Scenario matrix (framework-native first):**

| # | Scenario | sem capability | Status-quo baseline | Primary metric |
|---|----------|----------------|---------------------|----------------|
| sem-A | LLM-context extraction for `code-review`/`simplify` | `sem context <entity>` | raw `git diff` of changed files piped to model | review-prompt **token delta** at equal-or-better finding recall |
| sem-B | Entity diff vs line diff on real PRs | `sem diff` | `git diff` | entities-changed precision; noise reduction |
| sem-C | Cross-file impact on a worktree branch | `sem impact <entity>` | manual grep / Auggie retrieval | dependents found vs ground truth; latency |
| sem-D | Structural signal for roadmap scanner / cleanup-audit | `sem entities`/`sem impact` | current Layer-5 detectors | added-signal value; false-positive rate |
| sem-E | Entity-blame for `sc:git` provenance | `sem blame` | `git blame` | attribution accuracy at entity granularity |

**All-in cost columns (every scenario, no exceptions):** (a) LLM token delta vs
baseline, (b) wall-clock latency added, (c) maintenance burden increment (build
upkeep, version drift, collision-handling overhead).

**Data source:** this repo's recent merged PRs and active worktree branches.
*(Sample-size adequacy and synthetic-scenario design → deferred to analyzer lens;
see §9.)*

### S2 — Gated decision (scorecard → keep/kill)

**sem KEEP requires ALL of:**

- **G-sem-1 (the headline claim):** `sem context` cuts review-prompt tokens **≥30%**
  vs the raw-diff baseline at **equal-or-better finding recall** (recall measured
  by the analyzer-lens methodology). If recall drops, KILL regardless of token win.
- **G-sem-2 (substrate trust):** entity extraction is correct on **≥95%** of this
  repo's changed entities across scenarios sem-A/B (Python primary; mixed `.md`/
  `.toml`/`.json` handled gracefully via documented fallback). This is the gate
  that protects inspect and weave.
- **G-sem-3 (latency):** added wall-clock **< 2s p95** per invocation for the
  interactive `code-review` path.
- **G-sem-4 (cost ceiling):** all-in token+latency cost does not exceed the value
  delivered (analyzer lens supplies the value/cost ratio; architect sets the
  structural requirement that the ratio be **> 1** with a documented margin).
- **G-sem-5 (reversibility, re-confirmed):** rollback runbook re-executed clean.

**KILL → plan checkpoint (§8): re-evaluate whether inspect/weave proceed at all.**

### S3 — Integration (flag-gated, advisory → live)

On KEEP, wire sem behind a **feature flag** in two seams only (smallest blast
radius first):

- **Seam 1 — `code-review`/`simplify` context supplier.** Add an *optional*
  `sem context` pre-step that, when the flag is on, supplies entity-scoped
  token-budgeted context to the review prompt. Flag off → existing raw-diff path,
  byte-identical to today. Soak for the defined window in **advisory** (sem context
  attached but the reviewer still sees full diff) before flipping to **live** (sem
  context replaces raw diff).
- **Seam 2 — MCP server registration** in `src/superclaude/cli/install_mcp.py`
  `MCP_SERVERS` (entry: `name=sem`, `transport=stdio`, `command=sem-mcp`,
  `required=False`, behind a Rust-availability check). `make sync-dev` after the
  `src/` edit; **never** stage `.claude/`.

**Explicitly NOT wired yet:** roadmap scanner and cleanup-audit (scenario sem-D).
Those are deferred to S4+ as *additive* signals only after the interactive path is
proven — they are lower-leverage and higher-surface-area.

### S4 — Re-eval (steady-state)

After the soak window: re-measure G-sem-1/3/4 on accumulated real usage; re-measure
the **toolchain-maintenance burden** against the S0 estimate (did a sem version bump
break the build? did the collision rule hold?). Confirm or DEGRADE (flag back to
advisory). Only a clean S4 unlocks **inspect S0**.

---

## 3. inspect — Phase Plan (the review tool)

inspect is the **highest-risk integration** because it overlaps the most valuable
existing surface (`sc-auggie-review-protocol`) and its **precision is only 33%**.
The architecture's answer to 33% precision is uncompromising: **inspect is
advisory/pre-filter only — never a replacement for the Auggie pass, never a
PR-gating authority.**

### S0 — Spike

- **Install** `cargo install --git ... inspect-cli`; enumerate the 6 MCP tools
  (`inspect_triage / inspect_entity / inspect_group / inspect_file / inspect_stats /
  inspect_risk_map`) → schema capture.
- **Verify the danger formula reproduces** the documented tiers (Critical ≥0.7 /
  High ≥0.5 / Medium ≥0.3 / Low <0.3) on a hand-built fixture, so we trust the
  score we're about to shadow.
- **Provider routing decision (architectural):** inspect's `review` calls an LLM
  (anthropic/openai/ollama/openai-compatible). The framework routes
  `ANTHROPIC_DEFAULT_*` → gpt-5.5/qwen/claude. **Decision: in shadow, pin inspect
  to a fixed provider for clean cost attribution; do NOT let it inherit the
  framework's multi-vendor routing until S3.** Otherwise token-cost attribution is
  uninterpretable.
- **Rollback dry-run** (register/deregister `inspect-mcp`).

### S1 — Shadow eval (run BESIDE Auggie, compare, never act)

The critical architectural constraint: **inspect runs as a second, parallel review
engine whose output is logged next to the Auggie pass but never shown to a reviewer
and never used to filter the diff.**

| # | Scenario | inspect capability | Status-quo baseline | Primary metric |
|---|----------|--------------------|--------------------|----------------|
| ins-A | PR risk triage | `inspect_triage` / `inspect pr` | `sc-auggie-review` 5-wave findings | precision/recall vs Auggie findings as reference; **independent** ground-truth labeling (analyzer lens) |
| ins-B | Pre-filter token savings | top-60 entity selection feeding a hypothetical reduced Auggie prompt | full-diff Auggie pass | token delta **AND** finding-recall delta (does pre-filter drop real findings?) |
| ins-C | Large-PR recall ceiling | `inspect_triage` on PRs with >60 risky entities | full Auggie pass | **missed-entity rate** (the top-60 cap is a known recall hole) |
| ins-D | Untangling | Union-Find entity grouping | manual diff reading | grouping usefulness (qualitative) |

**Distrust the vendor judge.** inspect's own benchmark uses heuristic keyword
matching and only 3 Rust repos. The shadow eval **must not** reuse inspect's judge;
ground-truth labeling methodology is the analyzer lens's deliverable. Architect's
requirement: the eval is **falsifiable against an independent label set**, period.

### S2 — Gated decision

inspect has **two possible KEEP outcomes** and one KILL — the gate decides *which
seam*, not just keep/kill:

- **KEEP-as-prefilter (preferred if G-ins-PF holds):**
  - **G-ins-PF-1:** pre-filtering to top-60 entities saves **≥25%** Auggie-pass
    tokens while dropping **< 5%** of real findings (ins-B + ins-C combined). The
    5% finding-loss ceiling is hard — review is a recall-critical surface.
  - **G-ins-PF-2:** large-PR missed-entity rate (ins-C) is bounded and *disclosed*
    to the reviewer (the integration must surface "N entities beyond triage cap not
    reviewed").
- **KEEP-as-second-engine (fallback):** inspect's findings are shown to the
  reviewer as a *supplementary advisory pane* — never replacing Auggie — if it
  surfaces ≥1 true finding per M PRs that Auggie missed (complementarity), and its
  false-positive volume stays under a defined reviewer-tolerance budget.
- **KILL:** if pre-filter drops findings *and* second-engine complementarity is
  below threshold *and* the 33% precision produces reviewer-fatigue noise above
  budget. inspect KILL does **not** block weave (weave depends on sem, not inspect),
  but it does remove inspect's MCP registration cleanly.

### S3 — Integration (advisory-only, flag-gated)

Wire into `sc-auggie-review-protocol` behind a flag, in the **chosen** seam:

- **Pre-filter seam:** `inspect_triage` runs in Wave 1, narrows the entity set fed
  to Wave 2's `auggie --print --output-format json`. **Advisory soak first:** log
  what *would* have been filtered without actually filtering, compare findings, then
  flip to live filtering only after the soak confirms G-ins-PF-1 holds on live PRs.
- **Second-engine seam:** inspect findings posted as a clearly-labeled
  *supplementary* section in the PR review, visually distinct from Auggie findings,
  with a precision caveat banner ("advisory; ~33% precision — confirm before
  acting").

**Hard architectural rule carried into prod:** inspect output is **never** a
merge-blocking or PR-gating authority. It informs; humans and Auggie decide.

### S4 — Re-eval

Re-measure precision/recall on accumulated live PRs (the live set is larger and more
representative than the shadow set). Watch for **reviewer-fatigue signal** (are
reviewers ignoring the inspect pane? → DEGRADE to off-by-default). Clean S4 →
weave S0.

---

## 4. weave — Phase Plan (the merge tool)

weave is **last and most cautious** because it touches the **irreversible-by-default
surface**: an actual git merge. A bad merge driver silently corrupts history. The
architecture's answer: **weave is `preview`-only in shadow, scoped per-worktree in
integration, and never a global driver until a long soak proves zero regressions on
our merges.**

### S0 — Spike (enumerate the undocumented surface FIRST)

- **Install** `brew install weave` / `cargo install --path crates/weave-cli`
  + `weave-driver`.
- **CRITICAL spike task: enumerate weave's MCP tool names** — they are
  **undocumented**. Until enumerated, weave MCP wiring is *blocked*. Capture schemas
  into `spikes/weave-mcp-schema.md`. If the MCP surface cannot be reliably
  enumerated, weave is **CLI-only** (`weave preview` / `weave setup --local`) and
  the MCP registration is dropped from scope — a clean architectural fallback.
- **Rollback dry-run is paramount here:** `weave setup --local` in a throwaway
  worktree, then `weave unsetup`, confirm `.git/config` merge-driver entries are
  cleanly removed and native git merge is restored. **Prove `unsetup` works before
  trusting `setup`.**
- **Characterize the fallback envelope:** weave falls back to line merge for
  unsupported types, files >1MB, binaries. Confirm this on our repo's largest files.

### S1 — Shadow eval (`weave preview` only — NEVER a live merge)

weave runs in **preview mode** against **historical, already-resolved merge events**
from this repo's worktree-parallel-dev history. We replay known merges and compare.

| # | Scenario | weave capability | Status-quo baseline | Primary metric |
|---|----------|------------------|--------------------|----------------|
| wv-A | False-conflict resolution on real worktree merges | `weave preview` on replayed merges | native `git merge` outcome (conflict count) | **conflict-reduction %** vs Git on OUR merges (vendor claims ~95% — confirm/refute) |
| wv-B | Correctness — no semantic corruption | `weave preview` resolved output | the actual human-resolved merge result (ground truth) | **divergence rate** from the known-good resolution (this is the safety metric) |
| wv-C | Fallback behavior | preview on >1MB / binary / unsupported | line merge | graceful fallback confirmed; no silent corruption |
| wv-D | Jujutsu path (if used) | weave + jj | native jj | parity |

**The safety metric (wv-B) is the gate-maker.** Conflict reduction is worthless if
weave produces a *different* (wrong) resolution than the human did. Architect's
non-negotiable: **a single semantic-corruption case in shadow = automatic KILL**
unless it is provably a fallback-envelope case.

### S2 — Gated decision

**weave KEEP requires ALL of:**

- **G-wv-1 (value):** conflict reduction **≥50%** vs native git on our replayed
  worktree merges (we don't need the vendor's 95% — we need materially better than
  Git on *our* false-conflict pattern).
- **G-wv-2 (safety, hard):** **zero** semantic-corruption divergences (wv-B) outside
  the documented fallback envelope. Non-negotiable. One corruption → KILL.
- **G-wv-3 (reversibility, re-confirmed):** `weave unsetup` restores native merge
  byte-identically; tested in the integration-target worktree config.
- **G-wv-4 (scope containment):** the integration plan uses `setup --local`
  (per-worktree) NOT global `weave setup`, bounding blast radius. *(Open question
  in seed brief — architect resolves it: local-scoped, see §9.)*

### S3 — Integration (per-worktree, advisory preview → opt-in driver)

- **Scope decision (resolving seed-brief open question):** register weave as a
  **per-worktree, local-scoped merge driver** (`weave setup --local`) wired through
  an *opt-in* `sc:git` flag — **never** a global `weave setup` that changes merge
  behavior repo-wide. This bounds the blast radius to exactly the worktree-parallel-
  dev use case where weave's value lives, and leaves every other merge on native git.
- **Advisory-first:** even after `setup --local`, the first soak runs weave in a
  mode where it produces a `weave preview` shown to the user *before* the merge
  commits, with native-git fallback one keystroke away. Only after the soak confirms
  G-wv-2 (zero corruption on live merges) does weave become the default resolver for
  that worktree's merges.
- **MCP wiring** only if S0 enumerated the tool names; otherwise CLI-only.

### S4 — Re-eval

Re-measure conflict reduction and (critically) corruption rate on accumulated live
worktree merges. Any live corruption → immediate `weave unsetup` + DEGRADE to
preview-advisory. Clean S4 → weave graduates; plan moves to the generalization
appendix (§7).

---

## 5. Integration Map (where each surface plugs in)

The architectural principle: **each tool touches the minimum number of seams, each
seam is flag-gated, and CLI/MCP/Rust-lib surfaces are assigned by latency and
reversibility — not by what's most powerful.**

| Tool | Surface used | Plugs into | Seam type | Why this surface |
|------|--------------|-----------|-----------|------------------|
| **sem** | `sem context` (CLI) | `code-review`/`simplify` context pre-step | flag-gated optional pre-step | interactive latency-sensitive path; CLI is simplest to gate/revert |
| **sem** | `sem-mcp` (MCP) | `MCP_SERVERS` registry (`install_mcp.py`) | optional stdio server, Rust-availability-gated | gives Claude on-demand entity queries without hard-coding into a skill |
| **sem** | `sem entities`/`sem impact` (CLI) | roadmap scanner / cleanup-audit (DEFERRED to S4+) | additive signal only | lower leverage; added only after interactive path proven |
| **sem** | `sem-core` (Rust lib) | **NOT used directly** | — | linking a Rust lib into a UV-Python framework = maximal coupling; explicitly rejected. Use CLI/MCP boundaries only. |
| **inspect** | `inspect_triage` (MCP/CLI) | `sc-auggie-review-protocol` Wave 1 | advisory pre-filter OR supplementary engine, flag-gated, never gating | overlaps the review surface; advisory-only due to 33% precision |
| **weave** | `weave preview` / `weave-driver` (CLI) | `sc:git`, per-worktree merge | opt-in, local-scoped driver, never global | merge is irreversible-by-default; CLI + local scope = smallest blast radius |
| **weave** | weave MCP (names TBD) | `MCP_SERVERS` (conditional on S0 enumeration) | optional, droppable | MCP wiring is a nice-to-have, not load-bearing |

**Surface-selection doctrine (the reusable architectural rule):**
- **Prefer CLI** at latency-sensitive, easy-to-revert seams (a CLI call behind a
  flag is the cleanest possible rollback).
- **Use MCP** for on-demand, Claude-initiated queries that shouldn't be hard-wired
  into a skill's control flow (a deregistered MCP server simply disappears).
- **Never link the Rust lib (`sem-core`) directly** — that is the one irreversible
  coupling. The CLI and MCP boundaries are the seams that keep this whole initiative
  removable. This single rule is what makes "rip it all out in an afternoon"
  achievable.

---

## 6. Reversibility & Rollback Runbook

Reversibility is a **tested property**, exercised as a dry-run during each tool's S0
and re-confirmed at each gate. The runbook is identical in shape per tool.

### Per-tool rollback (single-command where possible)

| Tool | Wiring rollback | MCP rollback | Git-integration rollback | Toolchain rollback |
|------|-----------------|--------------|--------------------------|--------------------|
| **sem** | flag off → raw-diff path (byte-identical) | `claude mcp remove sem` | n/a (sem never `setup`s a git driver in this plan) | uninstall `sem-cli`/`sem-mcp` |
| **inspect** | flag off → Auggie-only review | `claude mcp remove inspect` | n/a | uninstall `inspect-cli` |
| **weave** | flag off → native git merge | `claude mcp remove weave` | **`weave unsetup`** (per-worktree) → native merge restored | uninstall `weave-cli`+`weave-driver` |

### Rollback ordering (when ripping a tool out)

1. **Flip the skill feature flag off first** (immediate: framework reverts to
   status-quo code path; no user impact).
2. **`weave unsetup` / no-op for sem/inspect** (restore native git for weave).
3. **`claude mcp remove <tool>`** (deregister MCP server).
4. **Uninstall the binary** (optional; framework already functions without it).
5. **Archive evidence** to `decisions/<tool>-KILL.md` (or `-KEEP.md`).
6. **`make sync-dev` + `make verify-sync`** if any `src/superclaude/` flag code
   changed. Never stage `.claude/`.

### The full-initiative kill switch

Because no tool links `sem-core` directly, and every wiring point is a feature flag
defaulting to status-quo, **the entire initiative reverts by flipping three flags
off + three `mcp remove` + one `weave unsetup`.** No skill logic is *deleted* on
rollback — the status-quo path was never removed, only conditionally bypassed. This
is the architectural payoff of advisory-first, flag-gated integration.

---

## 7. Generalization Appendix (gated behind native success)

Multi-repo / multi-language generalization is **out of scope until all three tools
clear native S4**, and is itself gated:

- Only tools that reached **KEEP + clean S4** get a generalization spike.
- Generalization reuses the same 5-stage state machine against external repos
  (the 27-language sem envelope, weave's Py/TS/Rust/Go/Java/C claims).
- Generalization is **explicitly lower priority** than maintaining the native
  integration; it never destabilizes the framework-native path.

---

## 8. Plan-Level Checkpoints (dependency-ordering safety)

Two checkpoints exist *above* the per-tool gates, enforcing the dependency order:

- **CP-1 (post-sem):** If sem is KILLED at S2 — especially on **G-sem-2 (substrate
  trust)** — the plan halts and asks: *do inspect and weave still make sense without
  a trustworthy shared entity substrate?* Default = **archive the initiative**;
  inspect's danger scoring and weave's semantic merge both inherit sem-core's entity
  model, so a substrate failure poisons the well. Override requires explicit
  evidence that inspect/weave's *own* entity handling is independently sound.
- **CP-2 (toolchain-cost review, after each S4):** Re-tally cumulative Rust-toolchain
  maintenance burden (build breakage, version drift, collision incidents, CI
  additions). If cumulative maintenance cost crosses a defined budget, **freeze
  further admissions** even if the next tool's value gate would pass. This is the
  guard against "each tool individually pays for itself but collectively the
  toolchain sinks us."

---

## 9. Open Questions (architect's resolutions + deferrals)

| Seed-brief question | Architect's stance |
|---------------------|--------------------|
| New `superclaude eval` CLI subcommand vs one-off `.dev/` scripts? | **Start as `.dev/` scenario scripts.** Building a reusable `superclaude eval` subcommand is speculative until we know the eval pays off — that's premature machinery. If all three tools reach S4 KEEP, *then* harden the scripts into a subcommand. (Prefer-simpler-proposals discipline.) |
| inspect false-positive budget: pre-filter only or full replacement? | **Never full replacement.** Pre-filter (advisory) or supplementary second-engine only. 33% precision categorically disqualifies inspect from gating authority. |
| weave global driver vs per-worktree scope? | **Resolved: per-worktree `setup --local`.** Bounds blast radius to the exact use case; never global `weave setup`. |
| inspect Anthropic routing vs framework multi-vendor? | **Pin a fixed provider in shadow** for clean cost attribution; only inherit multi-vendor routing at S3 with token-cost attribution explicitly accounting for the routing. |
| Token baseline: raw `git diff` vs current Auggie pass? | **Both, as two baselines.** sem-A measures vs raw-diff (its natural comparator); inspect-B measures vs the Auggie pass (its natural comparator). Defer the statistical framing to analyzer lens. |
| How many real PRs/merges for a meaningful native set? | **DEFERRED to analyzer lens** — sample-size adequacy and synthetic-scenario design are an eval-methodology question, not an architecture one. My plan provides the scenario *structure*; the analyzer provides the statistical *power*. |

---

## 10. Risks (architect lens)

| Risk | Severity | Mitigation in this plan |
|------|----------|-------------------------|
| Rust toolchain becomes load-bearing, nobody can maintain it | High | CLI/MCP-only seams, never `sem-core` lib; CP-2 cumulative-cost freeze; full kill switch |
| `sem` ↔ GNU-parallel collision reaches a `setup` step | Med | Hard rule: never bare `sem`; absolute-path/`sem-cli`/`sem-mcp` only; sem never installs a git driver in this plan |
| inspect 33% precision creates reviewer fatigue | High | advisory-only, never gating; precision caveat banner; S4 fatigue-signal DEGRADE |
| weave silently corrupts a merge | Critical | preview-only shadow; wv-B safety metric; single-corruption auto-KILL; per-worktree scope; `unsetup` proven first |
| weave MCP tool names never enumerable | Low | clean CLI-only fallback; MCP dropped from scope, not blocking |
| `sem context` omits target entity over token budget | Med | characterized in S0; advisory soak surfaces it before live |
| Coupling creep across three tools at once | High | one-at-a-time gate; next tool's S0 blocked until prior tool's S4 clean |

---

## 11. Honest Self-Assessment (architect-only lens limits)

This proposal is **strong on structure and reversibility, deliberately thin on
eval rigor**:

- **Eval-methodology depth is shallow.** I specify *that* recall must be measured
  and *that* the vendor judge is distrusted, but I do not design the ground-truth
  labeling protocol, sample-size power analysis, or judge calibration. Those gate
  thresholds (≥30% tokens, ≥95% extraction, ≥50% conflict reduction) are
  architecturally-motivated *placeholders* — the analyzer lens must validate they
  are statistically achievable and meaningful on this repo's limited PR/merge
  population. If our native PR set is too small for ≥95% extraction to be a
  meaningful claim, my gate is theater.
- **Cost accounting is structural, not quantitative.** I demand all-in cost columns
  and a >1 value/cost ratio, but I don't model the actual token economics of
  inspect's multi-vendor LLM routing or weave's near-zero LLM cost vs sem's
  context-extraction savings. The scribe/cost lens should supply real per-invocation
  dollar/token figures; my plan only provides the *slots* for them.
