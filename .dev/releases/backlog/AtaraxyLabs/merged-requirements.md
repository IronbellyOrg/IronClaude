---
title: "Ataraxy-Labs Tool Incorporation — Evaluation Release Plan (sem → inspect → weave)"
status: merged-requirements
source: brainstorm (Socratic + 3-variant adversarial merge)
convergence: 0.88
base_variant: opus/architect
graft_variants: [sonnet/analyzer, haiku/devops]
created: 2026-06-04
domain: research
strategy: systematic
order: sem → inspect → weave
integration: hybrid (MCP stdio servers + framework-native skill wiring)
eval_scope: framework-native first, generalization gated behind native success
cost_lens: all-in (tokens + latency + install + maintenance + rollback)
tools:
  - {name: sem,     role: foundation, surfaces: "CLI + 6 MCP tools + sem-core lib"}
  - {name: inspect, role: review,     surfaces: "CLI + 6 MCP tools"}
  - {name: weave,   role: merge,      surfaces: "CLI + weave-driver + MCP (names TBD)"}
provenance_legend: "[V1]=architect [V2]=analyzer [V3]=devops [MERGE]=synthesis"
---

# Ataraxy-Labs Tool Incorporation — Evaluation Release Plan

> Unified requirements merged from three adversarial proposals (architect / analyzer /
> devops lenses) at convergence 0.88. This is a **requirements specification**, not an
> implementation. It defines *how to evaluate and conditionally incorporate* three
> entity-level Rust/tree-sitter tools — `sem`, `inspect`, `weave` — into IronClaude,
> one at a time, each gated by a falsifiable, baseline-anchored, all-in-cost eval.

## 1. Thesis & Governing Principles [MERGE]

**One sentence:** Treat incorporation as a *reversible state machine gated by falsifiable
evidence and measured all-in cost* — never let a tool become load-bearing until a
predeclared scorecard proves it beats concrete IronClaude baselines, and make every
coupling a single-command rollback.

Three lenses, fused:

1. **[V1] Reversibility-first architecture.** Each tool passes an identical 5-stage state
   machine (Spike → Shadow → Gated decision → Integration → Re-eval) with a hard
   kill/keep gate *between* tools. Every coupling is a **seam, not a weld**; the
   `sem-core` Rust library is **never linked directly** — only CLI and MCP boundaries are
   used, so the whole initiative reverts in an afternoon.
2. **[V2] Falsifiable, baseline-anchored evaluation.** Every vendor benchmark is a
   *hypothesis* to confirm or refute on IronClaude data. No metric without a baseline; no
   value metric without a cost metric; the tools' own judges (especially inspect's
   keyword matcher) are rejected. Kill gates are first-class — the plan does **not** assume
   all three graduate.
3. **[V3] All-in cost is the deciding lens.** Three Rust binaries in a UV-only Python
   framework is *infrastructure*, not a feature. Every gate answers: does measured
   `tokens + latency + install + maintenance + rollback` justify the value? Token savings
   are **provider-conditional** — worthless if reviews route to a cheap model.

**Dependency order is methodological, not cosmetic:** `sem-core` is the shared
entity-extraction substrate. `inspect`'s danger scoring and `weave`'s semantic merge both
consume it. So sem's gate doubles as *"is the shared substrate trustworthy on our code?"*
A sem failure poisons the well (see CP-1).

## 2. Phase 0 — Pre-Flight Gates (mandatory, before any tool eval) [MERGE]

Four UNSTATED shared assumptions surfaced in the adversarial debate are promoted to
**hard pre-flight gates**. If any fails, the dependent eval is capped or blocked.

| Gate | Question | Pass criterion | Failure consequence |
|------|----------|----------------|---------------------|
| **G0-1 Corpus** [A-001] | Does this repo have enough real PR/merge history for a native eval? | **FIRST Phase-0 action** = the fork PR/merge-count inventory (below); pass = ≥20 PRs + ≥10 merges (stratified) real, OR real count + the defined synthetic-backfill top-up | All verdicts capped at `shadow_only` / Low confidence until supplemented |
| **G0-2 Provider** [A-002] | Does framework review actually route to an expensive provider often enough for token savings to matter? | Confirm review model (gpt-5.5/qwen/claude split) | If qwen-default: token-value gate becomes **advisory only**; tools must justify on latency/precision |
| **G0-3 Install** [A-003] | Can the tools be installed without making CI unusable? | Install matrix passes on Ubuntu-headless/macOS/Docker/GHA; **prebuilt binary available** OR cargo-from-source <5 min/tool | No prebuilt + cargo-in-CI >5 min/tool → **install gate fails before value is measured** |
| **G0-substrate prep** [A-004] | (Feeds CP-1) Is sem-core reliable on this repo's Markdown-heavy `.md` skill files? | Deferred to sem S1, but stratified by file type from the start | `.md`/skill-file entity reliability measured explicitly, not averaged away |

**G0-1 is the FIRST Phase-0 action — fork merge-count inventory before any spend [MERGE].**
Before the harness is built or any tool installed, inventory the *actual* fork corpus: count
this fork's merge commits and PRs (the IronClaude fork hosts its own PRs per the CLAUDE.md
PR-target rule, so PRs are local, not upstream). The corpus is **not empty** — on the order of
~30 merge commits + ~150 Python commits already exist — so the inventory establishes the real
baseline; it does not start from zero. Record the counts in the corpus manifest as the gate's
evidence. **Synthetic-backfill construction (only to top up beyond the real count):** if the
real inventory falls short of the §7 graduation tier (20 PR / 10 merge), seed synthetic cases
from the **§11 curated-defect list** — the named defect classes (wrong PR target, `.claude/`
SoT violation, UV-only violation, missing sync-dev, token-budget omission, silent semantic
merge) plus the §11 synthetic conflict classes (same-file independent edits, same-function
conflicts, rename+callsite, cosmetic-only, over-budget entity, unsupported/binary/>1MB) —
reported **separately** from native results and never mixed (per §11). Synthetic cases top up
to the tier; they never replace the real-merge baseline.

**Phase 0 deliverables:** corpus manifest (with the G0-1 real PR/merge inventory as its first
entry); provider-routing confirmation; install-matrix results; the cost-measurement harness
(`.dev/eval-workspaces/cost-measurement/`); the `sem`↔GNU-parallel collision guard.

## 3. The Incorporation State Machine (per tool) [V1]

```
 S0 SPIKE → S1 SHADOW → S2 GATED DECISION → S3 INTEGRATION → S4 RE-EVAL
 (build,     (compare,    (scorecard →        (flag-gated      (steady-state +
  enumerate,  log, NO      keep/kill)          advisory→live)   usage monitor)
  rollback    action)          │                    │                │
  dry-run)         └── ROLLBACK ▼ KILL ◄── ROLLBACK ─┴──── DEGRADE ───┘
                              S-KILL (deregister, unsetup, flag off, archive evidence)
```

| State | Entry | Exit artifact | Rollback |
|-------|-------|---------------|----------|
| **S0 Spike** | prior tool at S4 (or this is sem) + Phase 0 passed | builds; MCP tools enumerated; rollback dry-run passes; C1 toolchain-cost logged | nothing wired |
| **S1 Shadow** | S0 clean | comparison dataset (tool vs baseline), **zero production effect**; C2–C5 measured | delete logs; uninstall |
| **S2 Gate** | S1 dataset complete + min samples | filled Value+Cost+Risk+TCO scorecard → keep/kill/defer/shadow_only | decision only; no code touched |
| **S3 Integration** | S2 = KEEP | skill wiring behind feature flag, advisory soak → live | flip flag off → status-quo restored |
| **S4 Re-eval** | S3 live ≥ soak | steady-state confirm; maintenance burden re-measured; **usage monitor** (2-wk zero-call → deregister) | flag off |
| **S-KILL** | any gate fail | `claude mcp remove` + `unsetup` + flag off + evidence to `decisions/<tool>-KILL.md` | this **is** the rollback |

**Between-tool gate (terminal-state rule):** the next tool's S0 may begin only once the prior
tool reaches a **terminal state** — KEEP-and-live at S4 **OR** an explicit KILL at S-KILL.
inspect S0 is blocked until sem reaches a terminal state; weave S0 is blocked until inspect
reaches a terminal state. [V1] Crucially, weave depends on the `sem-core` substrate (§1),
**not** on inspect — so an inspect KILL is itself a terminal state that *satisfies* this gate
and lets weave's S0 proceed directly (a KILLed inspect never strands weave). The asymmetric
case is sem: because both downstream tools consume `sem-core`, a sem KILL on substrate-trust
trips **CP-1** (halt; default = archive the initiative) rather than merely releasing the next
tool. Exercise one tool in real use — or reach a clean, evidence-archived KILL — before adding
the next.

## 4. Eval Harness — Scenario Matrix [V2]

Start as `.dev/` scenario scripts (NOT a `superclaude eval` product); promote to a CLI
subcommand only after one full tool-decision cycle proves the harness repeatable.
*(Unanimous across all three variants; aligns with "prefer simpler proposals".)*

| Scenario | Baseline A | Baseline B | sem | inspect | weave |
|----------|-----------|-----------|-----|---------|-------|
| PR review triage | raw `git diff` | current `sc:auggie-review` Auggie pass | context supplier | risk comparator | n/a |
| Worktree merge | native `git merge` | manual resolution | conflict explain | n/a | **candidate** |
| Entity diff | `git diff --stat` + unified | human-labeled entities | **candidate** | risk overlay | n/a |
| Cross-file impact | grep/import/manual | Auggie retrieval | **candidate** | risk consumer | n/a |
| LLM-context extraction | full diff + files | Auggie context | **candidate** | downstream | n/a |
| Cleanup-audit / roadmap diff | line diff + scanner | current flow | structural signal | prioritizer | n/a |
| Large-PR risk ranking | LOC/file heuristic | Auggie output | feature source | **candidate** | n/a |
| Unsupported-file fallback | raw git | reviewer behavior | fallback | fallback | fallback |
| MCP integration stability | no server | Auggie MCP precedent | server | server | server |

**Harness components:** corpus manifest · baseline runners · tool runners · token meter ·
latency meter · output normalizer (JSON) · finding deduplicator · adjudicator scoresheet ·
scorecard generator · decision-record template.

**Runner I/O contract [MERGE].** Every harness component (each baseline runner and tool runner)
conforms to one contract so outputs are directly comparable:

- **Input record (per scenario case):** `{ case_id, scenario, tool, baseline, corpus_ref
  (commit/PR/merge sha), input_artifact (diff | worktree | file-set), provider (pinned in
  shadow), run_index }`.
- **Normalized JSON output:** `{ case_id, tool, findings: [{ id, entity, file, severity,
  evidence_ref }], tokens: { prompt_in, output }, latency_ms: { cold, warm }, exit_status,
  raw_ref }`. The output normalizer emits exactly this schema; the finding deduplicator,
  adjudicator scoresheet, and scorecard generator all consume it. A run is **invalid** if its
  output cannot be coerced to this schema.

**Concrete Phase-0 harness artifacts (restored from V3) [V3].** The Phase-0 1–2 day estimate
(§14) is the time to build these *named, runnable* deliverables — not abstractions:

- **`latency-harness.sh` [V3]** — a bash harness that times each tool/baseline **cold vs warm**
  and sweeps input size to expose **O(n) scaling** (per-loop delta in s/op, feeding cost domain
  C2 in §6). Lives in `.dev/eval-workspaces/cost-measurement/`; it is the one artifact runnable
  on day 1.
- **Install matrix [V3]** — the G0-3 install gate's concrete grid: each tool ×
  {Ubuntu-headless, macOS, Docker, GHA} × {prebuilt-binary, cargo-from-source} × **{glibc,
  musl}** libc target, each cell recording install wall-clock and pass/fail. The **glibc/musl**
  rows are explicit because a musl-only or glibc-only prebuilt binary flips the G0-3 verdict.
- **token-counter [V3]** — the per-call token meter that emits the `tokens.prompt_in/output`
  fields of the contract above, enabling the §5/§8.1 Auggie-token-isolation measurement (separating Auggie's token share from the multi-wave review prompt).

## 5. Metric Catalog (units · baselines · thresholds) [V2]

Five groups. Each metric names its baseline; graduation requires **beating the current
Auggie/git status quo, not raw git diff**.

**Review quality (RQ):** finding recall (%, vs Auggie pass) · actionable precision (%) ·
false-positive burden (count/PR) · critical-miss count (0 tolerated for baseline-caught) ·
risk-ranking quality (NDCG@20, recall@60).

**Structural accuracy (SA):** entity-detection recall (≥90% supported langs) · entity
boundary precision (≥85%) · cosmetic-suppression accuracy · impact recall (≥70%) /
precision (≥50%).

**Merge correctness (MC):** false-conflict reduction (% vs native git) · **true-conflict
preservation (100%, hard)** · clean-merge correctness (≥95%) · resolution-time saved (min).

**Cost & performance (CP):** prompt-input token delta (vs Auggie) · output token delta ·
wall-clock latency (median/P90/P95) · setup latency (<15 min) · dependency burden (0–5,
≤3) · maintenance touchpoints (<10).

**Auggie-token isolation method (how "vs Auggie" is measured) [MERGE].** The headline sem
metric — `sem context` cuts prompt tokens ≥30% vs Auggie (§8.1 H-sem-2) — requires separating
Auggie's token share from the surrounding multi-wave prompt. Method: run the SAME review
scenario in two metered configurations on identical input — **(A) baseline:** the current
`sc-auggie-review` path with its Auggie retrieval pass; **(B) candidate:** the same path with
`sem context` substituted for the Auggie retrieval step. Attribution is **per-call**: the
harness `token-counter` (§4) meters only the Auggie-retrieval call in (A) and only the
`sem context` call in (B), holding the rest of the multi-wave prompt fixed. The reported delta
is `(A.auggie_call_tokens − B.sem_call_tokens)` over the shared prompt — NOT a whole-run diff —
so the wave scaffolding cancels and only the Auggie-vs-sem substitution is measured. Both
configs pin the same provider (§8.2) so the counts are comparable.

**MCP reliability:** startup success (≥95%) · schema stability (weave names must be
enumerated) · error clarity (≥4/5).

**Scorecard ownership & decision authority [V2+MERGE]:** every per-tool S2 scorecard
(Value + Cost + Risk + TCO) carries an explicit ownership header:

| Field | Value |
|-------|-------|
| **Owner** | the solo release operator — IronClaude fork maintainer (`RyanW`) — the single accountable decider who fills the scorecard and records the keep/kill verdict |
| **Decided-by** | the same Owner; no separate review panel exists (see §7 solo-operator blinding) |
| **Decision record** | `decisions/<tool>-<VERDICT>.md` (date + evidence links) |

**Decision Authority & Tie-Break:** the Owner calls **keep** vs **kill** against the
predeclared S2 gate. When a tool's score lands in the **ambiguous / borderline band** — any
required gate metric within its measurement error of its threshold, OR Value and Cost both
marginal — the **tie-break resolver** is: **default to KILL-pending-second-pass.** The tool
does NOT graduate on a borderline result; instead the Owner runs one additional
high-confidence evidence round (toward the §7 20PR/10merge tier) and re-decides. If the second
pass is still borderline, the verdict is a hard **KILL** (kill-first doctrine: ambiguity is
not a pass). This borderline-confidence tie-break resolver is the **single source of truth**
for borderline gate handling — it is defined here in §5 and nowhere else; the CP-1 checkpoint
(§10) and the §12 risk register both rely on this definition rather than redefining it.

## 6. Cost Model — All-In TCO [V3]

| Domain | Metric | Unit | Measured |
|--------|--------|------|----------|
| C1 Install | binary fetch/build wall-clock | s | first install + CI cold start |
| C2 Latency | per-loop delta (cold vs warm, O(n) scaling) | s/op | shadow runs (latency harness) |
| C3 Token | LLM token delta **weighted by provider** | tokens × $/M | shadow runs |
| C4 Maintenance | quarterly upkeep (~10.5 hr/qtr for all 3) | hr/qtr | ongoing |
| C5 Rollback | mean time to deregister + clean | min | documented + tested |

**[V3-KEY] Multi-vendor token economics (resolves contradiction X-005).** The framework
routes `ANTHROPIC_DEFAULT_*` → gpt-5.5 (~$10/$40 per M) / qwen3.6-plus (~$0.40/$1.20) /
claude (~$15/$75). A 30% token cut is worth ~7.5× more on Claude than on qwen. **The token
gate is provider-weighted:** if reviews run on a cheap provider, a 30% reduction may save
~$0.40/qtr against ~$1,500/qtr maintenance — economically irrelevant. In that case the
token gate is advisory and tools justify themselves on **latency or precision** alone.

**sem ↔ GNU-parallel collision (4-step neutralization, before any `sem setup`):**
(1) always invoke `sem-cli` / full npm path, never bare `sem`; (2) MCP registry uses the
non-colliding binary name; (3) patch any `setup`-written gitconfig to `sem-cli`;
(4) install-script detection guard warns if both `sem` binaries resolve.

## 7. Judging Protocol & Statistical Validity [V2]

**Ground-truth tiers:** *strong* (curated defects, controlled merges, human-labeled
entities) · *medium* (accepted historical findings, post-merge test failures) · *weak*
(LLM-only, tool self-labels, keyword matching). **Graduation cannot rely on weak ground
truth.** inspect's `bench` keyword judge is explicitly **not** accepted.

**Blind adjudication — solo-operator mechanism [MERGE].** Because IronClaude is a
**solo-operator** eval — the same person runs the tools and would otherwise label the findings —
human-panel blinding is impossible and self-labeling is contaminated. The mechanism is therefore
**automated, not a human panel**: (1) **randomized tool naming** — each engine's output is
relabeled to an opaque token (`engine-A`/`engine-B`, shuffled per run) so neither the adjudicator
nor the operator sees which tool (inspect vs the Auggie baseline) produced a finding; (2) an **LLM
adjudicator receives provenance-stripped artifacts** — tool identity, banners, and scoring
metadata removed — and scores findings against the independent ground-truth labels, mirroring
reflect's own **evidence-validator** pattern (re-verify each cited finding against the real diff,
drop the unfounded ones); (3) the operator only sees the de-anonymized mapping *after* scoring is
committed. Human involvement is confined to **ground-truth construction done before the tools run**
(§7 strong-tier labels), never to scoring tool output. If human adjudication is ever preferred
instead, it must be explicitly staffed and budgeted with a named reviewer — otherwise the
automated mechanism above is the default. Across all of it: hide tool source from the judge;
dedupe findings before precision/recall; require evidence citation; label severity
(Critical/High/Medium/Low) — a tool cannot offset a missed Critical with many Lows.

**Statistical guards:** report **stratum-level** pass/fail (avoid Simpson's paradox — e.g.
sem saves tokens on small diffs but omits target entity on large ones); use **effect sizes**
not just pass/fail; assign **confidence labels** (High/Medium/Low) — graduation needs the
**High** band (the unconditional 20PR/10merge floor; see the interpolation table below),
replacement also needs High; a strong-Medium (Medium+) sample earns only a provisional
KEEP/soak, never graduation; **repeated-run stability** ≥3 runs.

**Tiered minimum evidence:** *shadow (directional, Low-confidence)* = 5 PRs + 3 merges
[V3]; *graduation (High-confidence)* = 20 PRs + 10 merges + 5 curated high-risk diffs +
stability pass + rollback proof [V2].

**Confidence interpolation between the two tiers [V2].** Sample counts that fall *between* the
shadow floor (5PR/3merge) and the graduation target (20PR/10merge) are not undefined — they map
to graded bands, and a verdict's band is the **minimum** of its PR-derived and merge-derived
band (the scarce axis governs, so a 20-PR / 4-merge sample is Low, not High):

| Sample size (PRs / merges) | Confidence band | What it licenses |
|----------------------------|-----------------|------------------|
| < 5 PR / < 3 merge | **Insufficient** | no verdict; `shadow_only`, supplement first |
| 5–9 PR / 3–4 merge | **Low** (directional) | shadow direction only; never graduation |
| 10–14 PR / 5–7 merge | **Medium−** | defer / keep-shadow; graduation still blocked |
| 15–19 PR / 8–9 merge | **Medium+** | strongest provisional KEEP (advisory→soak) with a stability pass (≥3-run) + strong-tier ground truth; **graduation still blocked** — the 20PR/10merge floor is unconditional |
| ≥ 20 PR / ≥ 10 merge | **High** | full graduation / replacement eligibility |

**Graduation floor is unconditional:** full graduation requires the **High** band (≥20 PR / ≥10
merge), matching the tiered-minimum line above, §13's resolved sample-size question, and §14's
generalization-promotion threshold. No interpolated band — including Medium+ — lifts a verdict to
graduation below that floor; a Medium+ sample may earn a strong provisional KEEP and soak, but it
re-decides at the 20/10 tier (consistent with the §5 default-to-KILL-pending-second-pass resolver).
A **replacement** decision likewise always requires the **High** band — no interpolation lifts a
replacement verdict from a lower tier. Synthetic-backfilled cases (§2 G0-1 / §11) are counted
toward the band only when reported separately and never blended into the native count.

## 8. Per-Tool Plans

### 8.1 sem — the foundation [V1+V2+V3]
- **S0:** install (prebuilt > cargo); enumerate 6 MCP tools (`sem_entities/diff/blame/impact/log/context`); apply collision neutralization; rollback dry-run; characterize chunk-fallback + **target-entity-omission-over-budget** footgun.
- **S1 hypotheses to test:** H-sem-1 entity diff > line diff for review units · H-sem-2 `sem context` cuts prompt tokens ≥30% **vs Auggie** · H-sem-3 impact graph improves test/review selection · H-sem-4 27-lang ≠ equal quality on our `.md`-heavy mix · H-sem-5 chunk fallback is safe.
- **S2 KEEP gate (all required):** token reduction ≥30% vs Auggie (provider-weighted) at recall within 5pp · **substrate trust: entity extraction ≥95% correct on changed entities, stratified by file type (protects inspect+weave)** · latency <2s p95 interactive · TCO ≤12 (C2+C3 ≤4 combined) · rollback re-confirmed. KILL → **CP-1**.
- **S3 seams:** (1) optional `sem context` pre-step in `code-review`/`simplify` (flag off = byte-identical raw-diff path); (2) `sem-mcp` in `install_mcp.py MCP_SERVERS`, Rust-availability-gated. Roadmap-scanner/cleanup-audit deferred to S4+ as additive-only.
- **`sem-core` Rust lib: NOT linked.** CLI/MCP boundaries only.

### 8.2 inspect — the review tool (highest-overlap, lowest-precision) [V1+V2]
- **S0:** `cargo install`; enumerate 6 MCP tools (`inspect_triage/entity/group/file/stats/risk_map`); **reproduce danger formula** (classification_weight + blast_ratio×0.3 + ln(1+dependents)×0.1 + public_api_boost 0.15 + change_type_weight; cosmetic ×0.3; tiers Critical≥0.7/High≥0.5/Medium≥0.3); pin a fixed LLM provider in shadow for clean attribution.
- **S1:** runs as a **second, parallel review engine** beside Auggie — logged, never shown, never filtering. Distrust inspect's judge; use independent ground-truth labels.
- **S2 — gate decides the seam (advisory-only, never gating):**
  - *KEEP-as-prefilter:* top-60 saves ≥25% Auggie tokens while dropping <5% real findings, AND all critical entities land in top-60 on large PRs (recall@60), AND precision ≥55% among top-20.
  - *KEEP-as-second-engine:* advisory precision ≥45% on native corpus + surfaces ≥1 true finding/M PRs Auggie missed + FP burden ≤8/large-PR.
  - *KILL* if precision ≈33% native AND complementarity below threshold AND FP noise above budget. An inspect KILL is a **terminal state** under the §3 between-tool gate, so it does **not** block weave — weave depends on `sem-core`, not inspect, and weave's S0 proceeds once inspect is terminal (KEEP-live OR KILL).
- **S3:** wire into `sc-auggie-review-protocol` Wave 1 behind a flag, advisory soak first; precision-caveat banner; **never merge-blocking or PR-gating.**

### 8.3 weave — the merge tool (last, most cautious) [V1+V2+V3]
- **S0:** `brew`/`cargo` + `weave-driver`; **enumerate undocumented MCP tool names** (if impossible → CLI-only, MCP dropped, non-blocking); rollback dry-run (`setup --local` in throwaway worktree → `unsetup` → confirm native merge restored **before** trusting setup); characterize >1MB/binary/unsupported fallback.
- **Scope & measurability [V2+V3]:** weave acts on **Python only** — for `.md` and other non-Python files it **falls back to plain `git` merge by design**, so the `.md`/git path is *intended behavior, not a measurability flaw*. Because ~92% of this repo is `.md`, weave's evaluable surface is the Python-bearing subset. **Phase-0 check (gates weave eval):** confirm enough Python-bearing worktree merges exist in the §2 G0-1 inventory to reach the §7 sample band for weave (≥3 merges shadow / ≥10 graduate); if Python merges are too few, weave's verdict is capped at `shadow_only` and synthetic Python-conflict cases (§11) backfill toward the band — never the `.md` corpus, which weave does not act on.
- **S1:** `weave preview` only — **never a live merge.** Replay this repo's historical worktree merges vs the known human-resolved result.
- **S2 KEEP gate (all required):** false-conflict reduction ≥60% vs native git on our worktree corpus (90% stretch on synthetic independent-function cases) · **true-conflict preservation 100% + zero semantic-corruption divergences outside fallback envelope — one corruption = automatic KILL** · `weave unsetup` restores byte-identical native merge · **per-worktree `setup --local` scope, never global** · TCO ≤10 (tightest; C2+C3 ≤2).
- **S3:** per-worktree local-scoped driver via opt-in `sc:git` flag; advisory `weave preview` shown before commit during soak, native-git fallback one keystroke away.

## 9. Integration Map [V1]

| Tool | Surface | Plugs into | Seam type |
|------|---------|-----------|-----------|
| sem | `sem context` CLI | `code-review`/`simplify` pre-step | flag-gated optional |
| sem | `sem-mcp` | `install_mcp.py MCP_SERVERS` | optional stdio, Rust-gated |
| sem | `sem-core` lib | **NOT used** | — (irreversible coupling, rejected) |
| inspect | `inspect_triage` | `sc-auggie-review` Wave 1 | advisory pre-filter/2nd-engine, never gating |
| weave | `weave preview`/`weave-driver` | `sc:git`, per-worktree | opt-in, local-scoped, never global |
| weave | weave MCP (TBD) | `MCP_SERVERS` (if enumerated) | optional, droppable |

**Surface doctrine:** prefer CLI at latency-sensitive/easy-revert seams; use MCP for
on-demand Claude queries; never link the Rust lib. SoT discipline: edit `src/superclaude/`,
`make sync-dev`, never stage `.claude/`.

## 10. Reversibility & Plan-Level Checkpoints [V1+V3]

**Full-initiative kill switch:** 3 flags off + 3 `claude mcp remove` + 1 `weave unsetup`.
No status-quo code is ever deleted — only conditionally bypassed.

**First-class plan assumption — the `.md`-substrate ceiling [V1+MERGE].** The single
most-probable outcome of the whole initiative is **sem KILLED at CP-1 on `.md`/skill-file
substrate-trust**: this repo is ~92% Markdown, tree-sitter's Markdown entity model is the
weakest of the supported languages, and the skills *are* the repo. This is not a tail risk
buried in the register — it is a **load-bearing plan assumption**: plan for sem-on-`.md` to fail
the substrate gate as the **base case**, and treat a sem PASS on `.md` as the upside. When a
substrate-trust gate result lands in the borderline band, resolve it with the **§5 Decision
Authority & Tie-Break resolver** (default-to-KILL-pending-second-pass) — the §5 resolver is the
single source of truth; CP-1 **cites** it rather than defining its own borderline rule.

- **CP-1 (post-sem):** if sem KILLED on substrate-trust (esp. on `.md`/skill files),
  **halt** — re-evaluate whether inspect/weave make sense without a trustworthy entity
  substrate. Default = archive the initiative. Borderline substrate-trust results are resolved
  by the §5 tie-break resolver (not redefined here).
- **CP-2 (after each S4):** re-tally cumulative Rust-toolchain maintenance (~10.5 hr/qtr
  projected). If it crosses budget, **freeze further admissions** even if the next tool's
  value gate would pass.
- **Usage monitor (S4):** 2 weeks of zero MCP/hook invocations → tool is dead weight →
  deregister.

## 11. Data Sources & Corpus [V2]

Tiered, never mixed without separate reporting: **native** (fork PRs, feature/worktree
branches, backlog diffs, skill edits) → **curated** (defects with known findings: wrong PR
target, `.claude/` SoT violation, UV-only violation, missing sync-dev, token-budget
omission, silent semantic merge) → **synthetic** (same-file independent edits, same-function
conflicts, rename+callsite, cosmetic-only, over-budget entity, unsupported/binary/>1MB) →
**generalization** (external repos, multi-language — **gated behind native success; external
success cannot rescue native failure**).

## 11.5 Security & Data-Handling [MERGE]

The eval sends real IronClaude code to external services: inspect's `review` pipes changed
entities to third-party LLM providers (gpt-5.5 / qwen / claude per the §6 routing), and all
three tools read the whole working tree during shadow runs. This section governs that egress —
it is a hard pre-condition on any `inspect review` / external-provider call, not advisory. It
is placed beside the §12 risk register because uncontrolled egress is a first-class risk.

**Data-egress path & provider retention.**
- The only sanctioned external egress is inspect `review` → the pinned LLM provider (§8.2 pins
  a fixed provider in shadow for clean attribution). No tool may post repo content to any
  endpoint outside that one declared path.
- Treat every provider as **retaining** submitted content unless its data-processing terms
  state zero-retention / no-train. Record the chosen provider's retention posture in the
  Phase-0 provider-routing confirmation (the G0-2 deliverable) before any `review` call.

**Secret-scrubbing (mandatory pre-flight before any external call).**
- Run a secret scan (`gitleaks`/`trufflehog`-class detection) over the candidate diff and any
  file context **before** it leaves the machine; abort the `review` call on any hit.
- Strip `.env`, credential files, `~/.aienv`, tokens, and `ANTHROPIC_*` / provider API keys
  from any context window assembled for a provider. Entity/context extraction (`sem context`)
  must exclude secret-bearing paths.

**Stance on private-fork code → third-party providers: CONDITIONAL (controlled).**
- Sending IronClaude private-fork code to a third-party provider is **permitted only** under
  ALL of: (1) a zero-retention / no-train provider tier confirmed in G0-2; (2) secret-scrubbing
  passed; (3) egress limited to the changed-entity slice inspect needs, never the whole repo;
  and (4) the egress logged to the decision record so it is auditable.
- If any control fails, the outcome is **forbidden** — run inspect against a local/self-hosted
  model or drop the `review` egress for that case, and cap the token-value gate accordingly.
  This is a security gate, not a value trade-off.

## 12. Risk Register (top items) [MERGE]

| Risk | Severity | Mitigation |
|------|----------|------------|
| Rust toolchain becomes unmaintainable load-bearing dep | High | CLI/MCP-only seams; never link sem-core; CP-2 freeze; full kill switch |
| Token savings marginal/irrelevant on cheap provider | High | provider-weighted token gate (G0-2); justify on latency/precision if qwen-default |
| Native corpus too small for valid claims | High | G0-1 inventory; confidence-capping; curated+synthetic with separate reporting |
| inspect 33% precision → reviewer fatigue | High | advisory-only, never gating; FP budget; S4 fatigue-DEGRADE |
| inspect top-60 misses large-PR criticals | High | recall@60 gate; disclose "N entities beyond cap not reviewed" |
| **weave silently corrupts a merge** | **Critical** | preview-only shadow; 100% true-conflict preservation; single-corruption auto-KILL; per-worktree scope; unsetup proven first |
| cargo-in-CI makes pipeline unusable | High | G0-3 prebuilt-binary requirement; exclude cargo-from-source from CI |
| `sem` ↔ GNU-parallel collision | Med | 4-step neutralization before any setup |
| weave MCP names never enumerable | Low | clean CLI-only fallback |
| **sem-core weak on Markdown/`.md` skill files — FIRST-CLASS plan assumption / most-probable sem-KILL (see §10)** | **High (base case)** | CP-1 substrate gate stratified by file type; plan for `.md` substrate failure as the base case; borderline gate results use the **§5** Decision Authority & Tie-Break resolver |

## 13. Resolved Open Questions [MERGE]

| Question | Resolution |
|----------|-----------|
| `superclaude eval` CLI vs `.dev/` scripts? | **`.dev/` scripts first**; promote only after one full cycle proves the harness. |
| inspect: pre-filter or replacement? | **Never replacement.** Advisory pre-filter or second-engine only. |
| weave global vs per-worktree? | **Per-worktree `setup --local`.** Never global. |
| inspect provider routing? | **Pin fixed provider in shadow** for clean attribution; framework routing at S3 with provider-weighted accounting. |
| Token baseline: raw diff or Auggie? | **Both measured; graduation requires beating the Auggie pass** (raw diff is informative lower bound only). |
| Sample size for a meaningful native set? | **Tiered** — 5PR/3merge shadow (directional); 20PR/10merge graduate (High-confidence); G0-1 inventory decides if synthetic backfill is needed. |

## 14. Phased Timeline (cost-gated, kill-first) [V2+V3]

1. **Phase 0** (1–2d): Pre-flight gates G0-1/2/3; harness + collision guard. *Exit: gates pass or scope capped.*
2. **sem** S0–S2 (2–4d) → S3–S4 (1–3d if KEEP). *Exit: sem verdict; KILL → CP-1 halts chain.*
3. **inspect** S0–S2 (2–4d) → S3–S4 (1–3d if KEEP). *Blocked until sem reaches its releasing terminal state (S4 live+KEEP); a sem KILL is the asymmetric case — it trips CP-1 and halts the chain (§3) rather than releasing inspect.*
4. **weave** S0–S2 (2–5d) → S3–S4 (1–3d if KEEP). *Blocked until inspect reaches a terminal state (KEEP-live OR KILL) per the §3 between-tool gate — weave depends on `sem-core`, not inspect, so an inspect KILL releases weave.*
5. **Generalization appendix** (native-first; skeleton below): only tools at KEEP+clean-S4; never destabilizes native path.

**Generalization appendix — skeleton (native-first; promoted only on a clean native KEEP) [MERGE].**
The user's "broad variety of scenarios" ask is scoped **native-first**: this appendix is built
ONLY once a tool reaches KEEP + clean S4 on the native corpus. It is not an unstructured
"optional" stub — it has a fixed shape and explicit promotion thresholds:

- **Promotion thresholds (ALL required before any generalization work starts):** the tool is at
  KEEP + clean-S4 natively · its native graduation reached High-confidence (§7 20PR/10merge
  tier) · the CP-2 maintenance budget is not breached. Generalization **cannot rescue a native
  failure** (§11) — an external win never overrides a native KILL.
- **Scenario inventory (the "broad" set — each run only after promotion):** (1) multi-language
  external repos for sem entity recall beyond the `.md`-heavy native mix; (2) large OSS PRs for
  inspect risk-ranking at scale; (3) cross-repo / multi-branch worktree merges for weave;
  (4) non-Python language coverage for sem + inspect; (5) high-volume regression set for
  latency / O(n) scaling.
- **Per-scenario thresholds:** reuse the §5 metric catalog + §7 confidence tiers unchanged; an
  external result is reported **separately** (§11) and never feeds a native verdict.

**Final stance:** the first deliverable is **not** an MCP-registry patch — it is a baseline
report of current review/context/merge cost. If the harness cannot prove these tools beat
IronClaude's status quo on IronClaude data, the correct outcome is a documented no-go, a
preserved eval corpus, and a clean rollback — not partial enthusiasm.
