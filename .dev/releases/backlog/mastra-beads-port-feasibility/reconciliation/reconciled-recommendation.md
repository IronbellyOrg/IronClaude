<!-- Provenance: produced by /sc:adversarial --compare (panel mode) -->
<!-- Base: Variant 1 (merged-requirements.md, structure) + Variant 2 (revised-recommendation.md, judgments) -->
<!-- Panel: opus:architect, sonnet:analyzer (source-verified), haiku:QA (fault-finder) + Round 2.5 invariant probe -->
<!-- Convergence: 0.93 (panel-internal convergence on the merged output — NOT a HYBRID-vs-DEFER source-agreement score) | Merge date: 2026-06-03 -->
<!-- Audit-response revision: 2026-06-03 — /sc:reflect --mode post --depth deep (Tier 2) Drift findings D1-D6 implemented as Changes #13-#18:
     #13 (D1) V/C/L/R demoted to ordinal directional composites + per-axis breakdown (INV-008);
     #14 (D6) strata-LOC partition reconciled to verified 72,906; ~62K reuse-eligible separated as a cross-cutting estimate;
     #15 (D3) G-A hardened (regression corpus + version-bump re-validation, INV-003); G-B given a numeric loop-aggregate SLO;
     #16 (D2/D3) new gates G-D coupled-stress (INV-011), G-E MCP-backend-security, + pre-Phase-5 tenant-isolation design gate (INV-012);
     #17 (D4) Phase-0 Mastra-value-vs-thin-client deliverable added (closes Phase-4 dangling dependency);
     #18 (D5) new gate G-F cross-model output equivalence; transport≠equivalence stated in §5/§9. -->
---
topic: "Stack D (Mastra + Backlog.md + Beads) port feasibility — reconciled recommendation"
domain: architecture
base_documents: ["merged-requirements.md (HYBRID)", "review/revised-recommendation.md (DEFER)"]
reconciled_recommendation: "DEFER — gated on a standalone, time-boxed Phase-0 intelligence sprint"
prior_recommendations: {study: hybrid, red_team: defer}
convergence_score: 0.93
source_verification: "6/6 of the DEFER review's load-bearing code citations independently re-confirmed"
created: 2026-06-03
generated_by: "/sc:adversarial --compare --depth deep (panel: opus:architect,sonnet:analyzer,haiku:QA)"
---

# Reconciled Recommendation: Replatforming SuperClaude/IronClaude Orchestration onto Stack D (Mastra + Backlog.md + Beads)

**Decision document for engineering leadership — multi-tenant orchestration replatforming go/defer/no-go**
**Status: DEFER — run a standalone Phase-0 intelligence sprint first. Reconciled from a HYBRID study and a DEFER red-team (0.93 panel convergence).**
**Date: 2026-06-03**

<!-- Source: Base (original, modified) — recommendation flipped per Change #1; framing reconciled per QA sufficiency challenge -->

---

## 1. Executive Summary & Recommendation

**Recommendation: DEFER the multi-phase port. First run a standalone, time-boxed (~2-week) Phase-0 *intelligence sprint* whose deliverable is an evidence report, not a port.** Go / defer / no-go is then decided from that report. This supersedes the original study's "HYBRID conditional-go," **not because the reuse thesis is wrong, but because the study over-merges three projects with different risk profiles** — (a) swapping the Claude subprocess seam, (b) service-ifying the ~62K LOC of reuse-eligible orchestration IP [sampled estimate — see §2] behind MCP/HTTP, and (c) delivering paid-or-DIY multi-tenant RBAC — into a single optimistic recommendation. Only (a) has strong source support. (b) and (c) carry the strategic value but rest on unverified, partly-commercial unknowns. **You do not start a multi-phase strangler roadmap on that footing.**

<!-- Source: Variant 2 §1, merged per Change #1 -->

**Why this is "defer" and not merely "go, but carefully":** a Phase-0 spike with standalone value (licensing intel, ACP parity report, a throwaway thin ACP client) is worth running regardless. The substantive difference between "DEFER until Phase-0 evidence" and the study's "conditional-go gated on Phase-0" is **organizational**: "go" tells the org it is building (momentum accrues before the commercially-gated driver is validated — the trap); "defer" forces the evidence to clear *before* commitment. We keep the study's continuity instinct by making Phase-0 a **named, scoped sprint with explicit pass/fail**, so "defer" does not mean "shelve."

<!-- Source: Variant 2 §1 + Variant 1 conditional-go spirit, reconciled per QA sufficiency challenge (Change #1) -->

**The source-verified core finding (sustained):** the codebase *is* partially built for runtime substitution — but unevenly. `pipeline/executor.py` runs against a genuine injected `StepRunner(Protocol)` (the one clean seam). **`roadmap/executor.py` is only PARTIAL** — ordinary steps instantiate `ClaudeProcess(...)` directly (`:1107-1118`); only the semantic-layer/convergence path is factory-wrapped (`:1358-1365`). **`sprint/executor.py` is NOT substitution-clean** — its `_subprocess_factory` is a test-only hook (`:927-955`) while production hardcodes `ClaudeProcess(...)` + `CLAUDE_WORK_DIR` (`:1320-1324`). These were independently re-confirmed this session (6/6 load-bearing citations).

<!-- Source: Variant 2 §2 (source-confirmed by analyzer judge), merged per Change #4 -->

**The "1.2K LOC" headline, corrected (Change #3):** the arithmetic is literally true — `pipeline/process.py` (244) + `sprint/process.py` (385) + `sprint/monitor.py` (571) = **1,200 LOC** of a 72,906-LOC tree. But "only 1.2K is Claude-coupled" is **misleading as a feasibility headline**: the *behavioral* coupling is broader — `shutil.which("claude")` preflight, `TurnLedger(initial_budget = max_turns × active_phases)`, `CLAUDE_WORK_DIR` isolation, and Claude-specific CLI permission flags (`commands.py:88-117`). The honest framing is **"a narrow file seam plus a broad behavioral contract,"** not "a tiny seam."

<!-- Source: Variant 2 §2 knocked-down list, merged per Change #3 -->

**Headline V/C/L/R** — **directional composite indicators on an ordinal 0–40 band, NOT measured metrics** (Likelihood higher = better; Complexity/Risk higher = worse):

| Value | Complexity | Likelihood | Risk |
|---|---|---|---|
| **~28** | **~34** | **~20** | **~26 → ~34** |

> **Scoring methodology (audit response — Change #13, addresses INV-008).** These four numbers are **ordinal directional composites** expressing the panel's relative judgment, **not cardinal measurements** — there is no weighted formula, and the exact integers carry no precision beyond "which side of the V-vs-R line the posture sits, and how far." `invariant-probe.md` **INV-008 (UNADDRESSED)** correctly flagged that the consensus never stated whether the three added gates (G-A/G-B/G-C) change Likelihood/Risk cardinally or act as separate non-scored blockers. We resolve this by **demoting the scores to directional indicators** and treating the new gates as **non-scored hard blockers** (they gate go/defer regardless of where they would "move a number"). The decisive claim is the **ordinal inversion** (V no longer exceeds R), not any specific delta. Each axis below lists its contributing components so the direction is auditable; the components are qualitative, and a reader who weights them differently may land a few points either way without changing the V<R conclusion.

| Axis | Direction vs study | Contributing components (qualitative) |
|---|---|---|
| **Value ~28** (was 33) | ↓ lower | The ~50K LOC of gates/FMEA/audit (see §2/§6 LOC note) *already works today*, so the net-new prize is **conditional** multi-tool/multi-tenant operation, not unlocking dormant IP. |
| **Complexity ~34** (was 30) | ↑ higher | Study undercounts `sprint/executor.py`, `monitor.py` telemetry reconstruction, auth/RBAC, Backlog mapping, and **permanent polyglot ops**. |
| **Likelihood ~20** (was 29) | ↓ lower | Roadmap only partly wrapped; sprint not clean; ACP parity unproven; EE licensing a gating commercial unknown. |
| **Risk ~34** (was 26) | ↑ higher | Highest-risk items — telemetry reconstruction, permission semantics, tenant isolation, source-of-truth integrity — are **load-bearing invariants**, not peripheral. |

<!-- Source: Variant 2 §1 re-score, replacing Variant 1's 33/30/29/26 per Change #2; demoted to ordinal directional indicators + per-axis component breakdown per audit Change #13 (INV-008) -->

The original's favorable **V(33) > R(26)** inverts to **V(~28) < R(~34)**. That **ordinal** inversion — Value no longer exceeds Risk — is the *directional* reason (not a precise quantitative one) the posture moves from go-ish to defer. The inversion is robust to reasonable re-weighting of the components above; the integers are not.

<!-- Source: Variant 2 §1 rationale, reframed per audit Change #13 -->

---

## 2. Current-State Architecture

SuperClaude/IronClaude is a **~72.9K-LOC Python orchestration layer** (confirmed by `wc`) driving the Claude Code CLI. Three strata:

- **Stratum 1 — portable IP (structural size ~50K LOC):** pipeline base types + sequencer, the FMEA suite, the static audit suite (`audit/*`), sprint/roadmap/tasklist domain models, the checkpoint system, the convergence engine, semantic/structural checkers, the cosmetic remediator, all 24 `SKILL.md` files, all 39 agent `.md` personas. Verified runtime-agnostic for the load-bearing sampled files (`pipeline/gates.py`, `roadmap/gates.py`, `audit/wiring_gate.py`, `pipeline/fmea_classifier.py` carry zero pipeline/Claude imports). **Caveat (honesty, sustained):** runtime-agnosticism is verified by *representative sampling*, not an exhaustive line-by-line census — the direction is sound; the precise per-stratum denominator is an estimate.

<!-- Source: Variant 1 §2 stratum 1, qualified by Variant 2 §2 "survived" + coverage caveat -->

- **Stratum 2 — adaptable orchestration (~12K LOC):** `sprint/executor.py` (~2,148 LOC flagship) and `roadmap/executor.py` (~3,700 LOC). **Correction (Change #4):** these are *not* uniformly substitution-clean. `roadmap` is partly factory-wrapped (semantic-layer only); `sprint` is entangled with the monitor/TUI/tmux/`TurnLedger` machinery behind a test-only injection hook. The orchestration *logic* (budget accounting, gate enforcement, convergence control, parallel dispatch, stall watchdog) is pattern-portable; the *seams are not clean*.

<!-- Source: Variant 1 §2 + Variant 2 §2 critical correction, merged per Change #4 -->

- **Stratum 3 — Claude-Code-specific (~11K LOC):** `ClaudeProcess` + sprint subclass, the stream-json monitor, tmux/TUI, the `install_hooks/commands/agents/mcp` plumbing, prompt files.

> **LOC reconciliation (audit response — Change #14, addresses strata-vs-total arithmetic).** Two distinct measures were being conflated; they are now separated:
> - **Structural partition (sums to the verified total):** Stratum 1 **~50K** + Stratum 2 **~12K** + Stratum 3 **~11K** ≈ **~73K**, consistent with the `wc`-verified **72,906 LOC** of `src/superclaude/cli` (this exact total *is* confirmed, not estimated).
> - **Cross-cutting "reuse-eligible IP" ≈ ~62K** is a *different lens*: it counts runtime-agnostic LOC across **all of Stratum 1 plus the pattern-portable logic inside Stratum 2** (gate/convergence/models/checkpoint logic that survives the runtime swap). It legitimately exceeds Stratum 1's ~50K structural size because reuse-eligibility cuts across strata. The earlier "~50–62K" band collapsed these two measures; they are now stated separately.
> - **Estimate discipline:** wherever the **~62K reuse-eligible** figure drives a decision below (§§1, 4, 9, 10, 12) it is a **sampled estimate** (per the Stratum-1 caveat), whereas the **72,906** total and the per-file counts (1,200 / 3,701 / 2,148) are exact. Treat any "~62K" in this document as `~62K [sampled estimate — see §2]`.

**The runtime seam (`pipeline/process.py::ClaudeProcess`)** builds and spawns `['claude','--print','--verbose',<perm>,'--no-session-persistence','--tools','default','--max-turns',N,'--output-format','stream-json'|'text','--model',M]` via `subprocess.Popen` (`process.py:114-146`), delivering the prompt over stdin (to bypass `MAX_ARG_STRLEN`), setting `os.setpgrp` for kill-tree teardown, and stripping `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` to defeat nested-session detection.

**`sprint/monitor.py` is reclassified (Change #3/#5): not "a stream-json parser to replace" but a *load-bearing reliability signal source*.** Lines 398-407 and 434-442 bind turn counting (F2: "each assistant event is exactly one turn"), token accumulation (F6), and tool-error attribution (F4) to the `claude --print --output-format stream-json` event shape. These signals feed the `TurnLedger` economic model and the stall watchdog — they are the budget/stall/error provenance for sprint reliability, **not a swappable parser**. Whether ACP events can reconstruct them is the single highest-uncertainty technical question.

<!-- Source: Variant 1 §2 seam + Variant 2 §2 monitor.py survivor (source-confirmed), merged per Change #5 -->

---

## 3. Target Stack D Assessment

Confidence per research: Mastra **medium**, Backlog.md **high**, Beads **high**. *(Assessment of the three components is carried from the study; it was not disputed in the red-team and survives intact.)*

<!-- Source: Variant 1 §3 (undisputed), carried verbatim in substance -->

### 3.1 Mastra — runtime + multi-tenant front
- **Maturity:** `@mastra/core` 1.0.0 (2026-01-20) → 1.16.0 (2026-03-23); ACP support requires `@mastra/core >= 1.34.0` (floor confirmed; exact head UNVERIFIED). ~22k stars.
- **License:** Apache-2.0 main framework; anything under `ee/` is the custom Mastra Enterprise Edition License (written commercial agreement; redistribution forbidden).
- **Runtime-seam match:** `@mastra/acp` `AcpAgent` spawns an ACP coding-agent CLI as a subprocess subagent (`command`/`args`/`cwd`/`workspace`, runtime `model`, `persistSession`; `AcpAgent.stream()` normalized chunks). The documented example drives Claude Code via `npx -y @agentclientprotocol/claude-agent-acp`. Structural replacement for `ClaudeProcess`.
- **Durable workflows:** `createWorkflow`/`createStep` with `.then`/`.branch`/`.parallel`/`.foreach`/`.dountil`; Zod-typed IO; `suspend()`/`resume()` snapshots — functional analog of MDTM checkpoints.
- **Multi-tenancy/RBAC (strategic blocker):** `server.auth` SimpleAuth (API-key→role) is license-free; **SSO, `StaticRBACProvider`, default roles, permission-based Studio, Agent Builder import from `@mastra/core/auth/ee` → paid EE for production.**

**Gaps:** RBAC/multi-tenancy is EE-paid (the whole strategic driver); ~62K LOC domain logic is *not* replaced by Mastra; Claude hooks have no Mastra equivalent; verified API churn 1.0→1.16. **UNVERIFIED:** whether `@mastra/acp` itself is Apache or `ee/` (now a **day-zero gate** — §9 Phase 0); ACP parity for `max_turns`/permissions/`CLAUDE_WORK_DIR`; per-tool parity for Cursor/Gemini/Copilot.

### 3.2 Backlog.md — MIT
v1.45.2 (2026-05-30); MIT; TS/Bun; built-in spec-aligned MCP server (`backlog mcp start`, **stdio only**). Git-committed `.md` + YAML frontmatter; fields map onto MDTM (`--ac`, `--plan`, `--dep` with cycle guard, `-p` parent). Concurrency-hardened (task-ID locking). **Gaps:** no multi-tenancy/RBAC/auth/remote transport (single-user, single-repo, stdio-local by design); no dependency-graph engine; rich MDTM gate/convergence semantics have no native schema. **UNVERIFIED:** whether the *official* MCP server exposes `decision.*`/milestone tools (vs CLI-only) — probe live before depending on `decision.add`.

### 3.3 Beads — MIT
`gastownhall/beads` v1.0.4 (2026-05-09); MIT; **Dolt-only** as of 1.0; embedded vs server modes; agent-native `--json` CLI. **Verified ops risk:** orphaned `dolt sql-server` daemons, embedded-mode nil-pointer panics, migration `bd dolt pull` failures, a Rust fork freezing the classic architecture. No RBAC/tenancy. **Disposition unchanged: drop/defer for v1** (both source docs agree).

---

## 4. Component Port Matrix

`reuse-as-is` = keep as Python behind MCP/HTTP. `adapt` = mechanical port/thin wrapper. `rewrite` = genuine new-runtime work. `drop` = retire. **Corrected per source verification (Change #4):** roadmap/sprint dispositions reflect their *actual* (uneven) seam cleanliness.

| Component | Disposition | Rationale |
|---|---|---|
| **`pipeline/process.py` + `sprint/process.py`** (~630 LOC) — THE SEAM | **rewrite** | Replace with an ACP/stdio driver behind the same `build_command/start/wait/terminate` + `on_spawn/on_exit` interface. Cheapest path = a thin Python ACP client preserving the `StepRunner` contract. Parity UNVERIFIED → Phase-0 gate. |
| **`sprint/monitor.py`** (~571 LOC) | **rewrite — highest risk** | Load-bearing reliability signals (F2/F4/F6) bound to stream-json shape. A new ACP-event adapter must reconstruct `TurnLedger`/stall/budget. **The true risk concentration.** |
| **`sprint/executor.py`** (~2,148 LOC) | **rewrite — very-high, sequence LAST** | Seam is a test-only `_subprocess_factory` (`:927-955`); prod hardcodes `ClaudeProcess` + `CLAUDE_WORK_DIR` (`:1320-1324`). Gated on a `monitor.py` telemetry-reconstruction report. |
| **`roadmap/executor.py`** (~3,700 LOC) | **rewrite — PARTIAL seam** | Ordinary steps direct `ClaudeProcess` (`:1107-1118`); only semantic-layer factory-wrapped (`:1358-1365`). Re-target the wrapped path first; the direct path needs work. **Second flagship, after pipeline.** |
| **`pipeline/executor.py`** (`StepRunner`-injected) | **adapt — the one clean seam** | Runtime-agnostic via the Protocol (`:41-72`). Swap the injected factory to the ACP driver; logic stays. **First flagship.** |
| **`*/models.py`** (`TurnLedger`, `GateCriteria`, `TaskEntry`, FSMs) | **reuse-as-is** | Pure data, zero runtime imports. |
| **`*/gates.py` + `validate_gates.py`** (~1.7K LOC) | **reuse-as-is** | Pure-Python validators; highest-value reusable IP. Rewriting to TS = value destruction. |
| **`roadmap/convergence.py`** | **reuse-as-is** | **Confirmed runtime-agnostic** — constants are plain ints, `TurnLedger` is a *conditional* import. (The red-team's own "inherits Claude-era turn semantics" charge was conceded as overreach — this stays in the agnostic column.) |
| **FMEA + structural/semantic/fidelity/obligation/cosmetic checkers + `spec_parser`** (~12.7K LOC) | **reuse-as-is** | Pure regex/AST/graph; the anchor of the hybrid. |
| **`audit/*`** (~6.7K LOC) | **reuse-as-is** | Wrap as an MCP tool server. |
| **prompts (`roadmap/prd/certify/validate/remediate`)** (~3.5K LOC) | **reuse-as-is** | Model-agnostic text; carry verbatim. |
| **`checkpoints/config/kpi/retrospective/diagnostics/logging`** (~1.9K LOC) | **adapt** | Checkpoint→suspend/resume; KPI/retro→OTel spans + Backlog docs. |
| **`skills/*/SKILL.md` (24) + `agents/*.md` (39)** | **reuse-as-is** | Crown-jewel prompt IP; re-target the loader only. |
| **`/sc:*` dispatch loader** | **drop (re-home)** | Bodies survive as skill content; dispatch surface does not. |
| **`install_hooks/commands/agents/mcp.py` + `freshness-*.sh`** (~1.4K LOC) | **drop (re-home)** | Irreducibly Claude-specific. |
| **`sprint/tmux.py` + `tui.py` + `summarizer.py`** (~1.6K LOC) | **drop** | Single-user-local; replaced by Mastra Server + OTel. |
| **`*/commands.py`** (Click CLIs) | **rewrite/adapt** | → Mastra Server HTTP endpoints + optional CLI wrapper. |
| **`eval/*`** (~8.5K LOC) | **adapt** | Re-point the PTY/isolation driver at the ACP driver. |
| **`cli_portify/*`** (~6K LOC) | **adapt/drop** | Self-referential; retire after the port. |
| **Backlog.md** (MIT) | **adapt — derived MIRROR (not task-of-record)** | See §6 — demoted to a mirror until a lossless MDTM round-trip is proven. |
| **Beads** (MIT) | **drop/defer (v1)** | Dolt instability + dual-source drift outweigh value. |
| **Mastra runtime** | **adapt** | Apache core as ACP driver + HTTP front; EE features = a separate paid decision (§7), pulled forward to a Phase-0 *decision* (§9). |
| **Existing CLI surfaces** | **reuse-as-is (benchmark/fallback)** | Live benchmark + rollback throughout. |

<!-- Source: Variant 1 §4 matrix, dispositions corrected per Variant 2 §2/§3 (Change #4); convergence.py concession per Change #3 -->

---

## 5. The Runtime Seam

`@mastra/acp`'s `AcpAgent` is the structural twin of `ClaudeProcess`. The swap re-implements `ClaudeProcess` as an ACP/stdio driver behind the identical lifecycle interface so the bulk of callers are unchanged — **for the pipeline path**. Roadmap (partial) and sprint (not clean) need more than a factory swap.

**The hard part is not the seam — it is `monitor.py` telemetry reconstruction.** Claude Code's stream-json is a richer wire format than ACP's normalized event stream; the system derives turn boundaries, per-turn tokens, tool-call inventory, error signatures, and stall timing from it, and those signals are load-bearing for `TurnLedger` and recoverable reruns. **Whether ACP events can reconstruct them gates the entire recommendation** (Phase-0 blocker 2).

**Multi-tool implications:** ACP is JSON-RPC 2.0 over stdio with adapters for Claude Code, Codex, Gemini (native `--acp`), Cursor, Copilot, Amp, Goose, Auggie — the multi-tool generalization Stack D promises — but it is a **lossy lowest-common-denominator contract** over Claude-specific knobs. Per-tool parity for Cursor/Gemini/Copilot is UNVERIFIED in Mastra's own docs (only Claude Code/Amp/Codex named). **Scope the Phase-0 spike to Claude + exactly one second tool** (Change #9); record the others' ACP status as a procurement fact, not a build dependency. **Transport ≠ equivalence (audit Change #18, addresses D5):** driving Claude + one tool through ACP proves the **transport abstraction** (the seam swaps and a second tool can be spawned) — it does **not** prove **output equivalence**. The env is heterogeneous (`opus=claude-opus-4-8`, `sonnet=gpt-5.5`, `haiku=qwen3.6-plus`), so non-Claude models will *drive the work*; whether they produce **gate-equivalent artifacts** (vs G-C's Claude-baselined "0% gate-correctness drift") is a separate, deeper question gated by new **G-F** (§9 Phase 0). Do not let a passing transport spike be read as proof of cross-model equivalence.

> **Shared blind spot, newly surfaced (gate G-A):** both source docs scrutinized *Mastra's* churn but treated the **ACP spec itself** as a stable substitution target. ACP's own maturity, governance, and version stability were never verified. A `monitor.py` telemetry rewrite that targets a moving spec is a compounding risk. **Pin an ACP spec version and verify its governance in Phase 0.**

<!-- Source: Variant 1 §5 + Variant 2 monitor reclassification + panel A-001 (new gate G-A), merged per Changes #5/#9/#10 -->

---

## 6. Task-of-Record Decision

**Decision (revised — Change #6): Backlog.md is a *derived mirror*, NOT the task-of-record, until a lossless MDTM round-trip is demonstrated.** The MDTM `tasklist-index.md` + the Python layer remain authoritative; Backlog.md mirrors task *state* only.

- Map MDTM phase items → backlog tasks (`AC→--ac`, `plan→--plan`, `deps→--dep`, phases→labels/parent, checkpoints/KPI→notes/docs, decisions→`backlog decision create`) behind the existing `checkpoint`/`TaskEntry` models via a thin sync adapter — but **enforce a single-authoritative-write-path rule** so the mirror cannot diverge.
- **Gate before promotion:** Backlog.md becomes task-of-record only after a proven lossless round-trip of the rich gate/convergence/checkpoint schema. The original study's own rollback path already conceded this ("MDTM remains source until the mirror is proven lossless") — contradicting its "sole task-of-record" headline. The mirror-first posture resolves that tension and contains the verified dual/triple-store drift failure mode.
- **Beads** stays dropped/deferred for v1 (Dolt instability + dual-source drift); re-evaluate only on a demonstrated `bd ready` advantage over the MDTM phase model.
- **Probe live in Phase 3:** confirm official Backlog.md MCP `decision`/`milestone` tool exposure (the `obligation_scanner → decision.add` dependency); CLI fallback if absent.

<!-- Source: Variant 1 §6 demoted per Variant 2 §3 Phase 3 (Change #6) -->

---

## 7. Multi-Tenancy & Licensing

**The strategic crux is commercially gated, and its *decision* is now pulled forward to Phase 0 (Change #7).** The whole reason for the port — company-wide multi-tenant RBAC — is **Mastra Enterprise Edition (paid)** and lives *outside* the reuse story:

| Layer | OSS (Apache/MIT) capability | What multi-tenancy requires |
|---|---|---|
| Mastra runtime | SimpleAuth (API-key→role) + app-level scoping | **EE:** SSO, `StaticRBACProvider`, permission Studio, Agent Builder |
| Tenant-fair concurrency | none in core | Inngest integration (3rd-party) or DIY |
| Backlog.md | single-repo, stdio, no auth | one repo/dir per tenant behind an external authz gateway |
| Beads (if used) | one un-permissioned graph per Dolt DB | per-tenant DBs/prefixes above Beads |

**Consequence:** a technically successful seam swap can deliver **multi-USER (SimpleAuth, $0)** and still **not deliver the multi-TENANT company goal.** The EE-buy-vs-DIY decision is the hardest-to-reverse, most commercially-gated choice in the whole program — so its **decision and evidence (EE quote, support terms, `@mastra/acp` license status) move to day-zero Phase 0**, even though the tenancy **build** remains the last engineering phase (§9 Phase 5). **UNVERIFIED and material:** whether `@mastra/acp` is Apache or `ee/` — if the seam driver itself is EE, the "vendor-free seam swap" premise weakens immediately.

> **Newly surfaced (INV-012): a day-zero EE-buy-vs-DIY *decision* does not prove tenant isolation, noisy-neighbor protection, or fair scheduling work.** Those need an end-to-end pilot (§9 Phase 5 control-plane gate). Pulling the *decision* forward de-risks sunk cost; it does not de-risk the *build*.

<!-- Source: Variant 1 §7 + Variant 2 §3 Phase-5-kill reframed to decision-forward/build-last (Change #7) + invariant INV-012 (Change #11) -->

---

## 8. What Is Lost Leaving Claude Code

| Lost capability | Severity | Mitigation |
|---|---|---|
| Freshness hooks (`freshness-pre-edit.sh`, session-context injection) | Dev-ergonomics | Re-implement as Mastra processors/middleware where needed; accept loss for non-Claude tools. |
| `/sc:*` command dispatch | Medium | Bodies survive as skill content via skills.sh; only dispatch lost. |
| Permission modes (`--dangerously-skip-permissions` etc.) | **High — load-bearing** | ACP must expose equivalent permission semantics; **UNVERIFIED → Phase-0 blocker 3.** |
| `max_turns` + stream-json telemetry | **High — load-bearing** | `TurnLedger` depends on it; reconstruct from ACP events in the rewritten `monitor.py`; **UNVERIFIED → Phase-0 blocker 2.** |
| `CLAUDE_WORK_DIR` isolation | High | Map to AcpAgent `workspace`; verify in Phase 0 (blocker 4). |
| `verify-sync` / SoT enforcement | Dev-ergonomics | CI/middleware governance. |
| tmux/TUI UX | Low (single-user) | Mastra Server endpoints + OTel + optional Studio (net-positive for multi-tenant). |

**Framing discipline (sustained from both docs):** the genuine moat is the **runtime-agnostic gate/convergence/FMEA/audit IP — which the port preserves.** Hook loss and `/sc:*` loss are dev-ergonomics, not the moat; do not let them inflate the no-go case. The two load-bearing losses (permission semantics, turn/stall telemetry) are exactly what Phase 0 exists to de-risk.

<!-- Source: Variant 1 §8 (undisputed; both docs agree on the moat framing) -->

---

## 9. Phased Roadmap

Strangler-fig, **re-sequenced per the verified seam cleanliness (Change #5) and with the commercial gate pulled to day-zero (Change #7).** The existing Python CLI stays fully operational as the live benchmark and rollback throughout. **Read Phase 0 as a standalone deliverable: its success authorizes the *next bounded validation phase*, it does not certify end-to-end port feasibility (INV-013).**

<!-- Source: Variant 1 §9 restructured per Variant 2 §3 + invariant probe (Changes #5,#7,#8,#9,#10,#11,#12) -->

### Phase 0 — Standalone intelligence sprint (DECIDES go/defer/no-go)
- **Deliverable:** an evidence report, not a port. Time-boxed (~2 weeks), reversible, valuable regardless of the decision.
- **Commercial blockers (day-zero, decidable now):** obtain a Mastra EE quote + support terms; **verify the `@mastra/acp` license (Apache vs `ee/`)**. If the seam driver is EE-gated, the vendor-free premise dies immediately.
- **Four split ACP-parity blockers** (replacing the study's single vague "ACP parity" gate): (1) **permission semantics**, (2) **turn/token telemetry reconstruction** against current stream-json output (F2/F4/F6), (3) **process lifecycle / cancellation**, (4) **workspace isolation** (`CLAUDE_WORK_DIR`→`workspace`). Drive Claude Code **+ exactly one second tool** (Codex or Gemini) through a throwaway ACP driver behind the existing `ClaudeProcess` interface. **Scope discipline (audit Change #18, addresses D5):** this proves the **transport abstraction** (the seam swaps cleanly), **NOT output equivalence** — see new gate G-F.
- **Deliverable (audit Change #17, addresses D4 — closes the Phase-4 dangling dependency):** a **Mastra-value-vs-thin-client evaluation** — implement the throwaway ACP driver in *both* forms (a thin Python ACP client preserving `StepRunner`, and a minimal Mastra-workflow harness) and record whether Mastra's `createWorkflow`/`suspend`/`resume` machinery earns its keep over the thin client. This is the named producing gate that Phase 4's "proceed only if Phase 0 proved Mastra-specific value" precondition depends on; without it, Phase 4's gate references evidence nothing produces.
- **New gate G-A — ACP spec maturity + maintenance regime (hardened per audit Change #15, addresses D3/INV-003):** pin an ACP spec version AND verify its governance/stability (not just Mastra's). **Not a point-in-time pin:** define a **regression corpus + a re-validation rule that re-runs telemetry/parity checks on every ACP or Mastra version bump** after Phase 0 — a `monitor.py` telemetry rewrite targeting a moving spec needs a continuous-compatibility posture, not a one-time snapshot.
- **New gate G-B — MCP boundary latency, with a numeric SLO (hardened per audit Change #15, addresses D3):** benchmark **aggregate boundary wall-time across a full multi-cycle convergence loop / FMEA / audit sweep** (the architecturally-material N-round-trip number), **not a single representative call**. **Numeric SLO (replaces "does not turn seconds into minutes"):** aggregate added boundary latency over a representative convergence run MUST be **≤20% of the in-process baseline wall-time** (tune the threshold in Phase 0, but it MUST be a number with a pass/fail rule — an unfalsifiable prose SLO is the same defect G-C fixes).
- **New gate G-C — typed differential spec:** replace the unfalsifiable "5% tolerance" with a **typed acceptance metric** — 0% drift on gate-correctness; a schema-bounded artifact diff; advisory-only economic/token drift — including sample size, baseline direction, and pass/fail decision rules.
- **New gate G-D — coupled end-to-end stress test (audit Change #16, addresses D3/INV-011):** G-A/G-B/G-C/telemetry **interact** — a pinned ACP version can still emit lossy telemetry; telemetry can pass on small samples but fail under convergence-loop load; latency can alter timeout/stall behavior and therefore gate-correctness. Require **one combined run that exercises telemetry reconstruction, gate verdicts, and boundary latency together** under convergence-loop load. Independent per-gate passes are necessary but NOT sufficient; G-D is the masking-failure-mode check.
- **New gate G-E — MCP/HTTP backend security model (audit Change #16, addresses D2):** the recommendation wraps the reuse-eligible IP (audit/FMEA/gates) "as an MCP tool server" (§4). For a multi-tenant system that backend is the **real attack surface** — Mastra's front-door SimpleAuth/EE RBAC (§7) does NOT secure it. Phase 0 (design) / Phase 1 (proof) MUST gate the MCP boundary's **authn/authz, input validation, and per-tenant data isolation** before any broad extraction. An unauthenticated MCP server exposing tenant filesystems is a non-starter regardless of front-door auth.
- **New gate G-F — cross-model output equivalence (audit Change #18, addresses D5):** the env is heterogeneous (`opus=claude-opus-4-8`, `sonnet=gpt-5.5`, `haiku=qwen3.6-plus`) — non-Claude models will *drive the work*, yet G-C's "0% gate-correctness drift" is implicitly baselined on Claude. Schedule a **cross-model gate-equivalence probe**: run the same gate/convergence fixtures through Claude and through ≥1 non-Claude model and measure whether qualitatively different models produce **gate-equivalent artifacts**. "Claude + one tool" proves transport; this proves equivalence — the deepest multi-tool risk.
- **New gate (operating model / staffing, promotes A-003):** explicit org commitment to durable Python+Node+MCP+HTTP ownership (dual tracing, schema versioning, cross-runtime failure translation). If absent, "hybrid" collapses to rewrite-or-no-go.
- **Effort:** **S→M** (throwaway, but the expanded gate set G-A…G-F + the Mastra-value deliverable realistically pushes the spike toward the upper end of the ~2–3 week box; size it honestly rather than assuming the original "S"). **Dependencies:** none. **Rollback:** trivial — if any commercial or load-bearing-parity gate fails, the recommendation hardens to **no-port** with <3 weeks sunk.

### Phase 1 — A thin slice of domain logic behind MCP/HTTP
- **Goal (narrowed — Change #8):** expose **3–5 highest-value verified-pure checkers first** (`gates.py`, `wiring_gate.py`, `fmea_classifier.py`) and prove schema/error/latency/observability contracts (G-B) before any broad extraction. **Do NOT wrap all ~62K LOC [sampled estimate — see §2] up front** — and note (INV-009) that a 3–5 checker trial does *not* yet prove the broader ~62K boundary under representative convergence/audit/FMEA load; that proof is a Phase-1-exit criterion, not an assumption.
- **Effort:** **M→L.** **Dependencies:** Phase-0 G-B + staffing gate. **Rollback:** functions remain in-process for the existing CLI; MCP layer is additive.

### Phase 2 — Swap the seam, in verified order, with a typed parallel-run gate
- **Goal:** start with the **pipeline `StepRunner` path** (the one verified-clean seam); then the **roadmap semantic-layer** path (factory-wrapped); **sprint LAST**, gated on a `monitor.py` telemetry-reconstruction report. Run the new path in parallel with the Python CLI under the **G-C typed differential gate** (not the old "5% tolerance").
- **Effort:** **L** (sprint is the very-high tail). **Dependencies:** Phase-0 parity + Phase-1 thin slice. **Rollback:** existing CLI is the benchmark; cutover only on passing the typed gate; reversible per flagship.

### Phase 3 — Backlog.md as a derived mirror (not task-of-record)
- **Goal:** behind `checkpoints.py` + `TaskEntry`, add a sync adapter mirroring MDTM state into Backlog.md via its MCP server, with a single-authoritative-write-path rule. Probe official MCP `decision`/`milestone` exposure live before committing `decision.add`. **Promote to task-of-record only after a proven lossless round-trip.**
- **Effort:** **M.** **Dependencies:** Phase 2 (one flagship). Independent of Mastra EE. **Rollback:** MDTM stays source of truth; reject if the mirror is lossy.

### Phase 4 — Mastra Server multi-USER (SimpleAuth, OSS) — conditional
- **Goal:** front the runtime with Mastra Server + OTel; **SimpleAuth (API-key→role) for multi-user on the free Apache tier.** Retire tmux/TUI for HTTP endpoints + run visualization. **Proceed only if Phase 0 proved Mastra-specific value over a thin Python ACP client** — an HTTP front around the existing CLI is the fallback if Mastra workflows don't earn their keep. Delivers multi-user at **$0 license**.
- **Effort:** **L.** **Dependencies:** Phase 2 + Phase-0 Mastra-value evidence. **Rollback:** Python CLI still operational; Mastra Server is additive.

### Phase 5 — Multi-tenant RBAC BUILD (decision already made in Phase 0)
- **Goal:** execute the EE-buy-or-DIY-build chosen at day-zero: either Mastra EE (SSO/`StaticRBACProvider`/Agent Builder + Inngest for tenant-fair concurrency) OR DIY RBAC + per-tenant isolation on the Apache server + per-tenant Backlog.md repos behind an authz gateway.
- **Tenant-isolation DESIGN gate (pre-build, audit Change #16, addresses D2/INV-012):** **before any Phase-5 build begins**, produce and review a concrete **tenant-isolation architecture** — data-isolation boundaries, noisy-neighbor protection, and fair-scheduling design — as a *design artifact gated independently of the build*. A day-zero EE-buy-vs-DIY *decision* (§7) and the end-to-end pilot below are necessary but do NOT substitute for an up-front isolation design; licensing is not architecture. This design gate is the control-plane complement to G-E (which secures the MCP backend boundary). Without it, the roadmap proceeds toward a tenancy build with no isolation design of record.
- **New control-plane gate (INV-012/INV-014):** an end-to-end pilot of 2–3 internal tenants proving isolation, noisy-neighbor protection, fair scheduling, and **throughput advantage over the current CLI + worktrees/subagents baseline** before decommissioning anything.
- **Effort:** **XL.** **Dependencies:** Phase 4 + the Phase-0 EE/DIY decision + staffing gate. **Rollback:** Phases 0–4 deliver real multi-tool + multi-user value independent of this gate, so "defer the tenancy build" stays live if pricing/parity/throughput disappoints.

*(This is a re-sequencing, not a deletion of the study's Phase 5: the build stays last; only its commercially-gated decision moved to day-zero.)*

---

## 10. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| stream-json → ACP event impedance (`monitor.py`/`TurnLedger` signals unreconstructable) | Medium | **High** | Phase-0 blocker 2; rewrite `monitor.py` as an ACP-event adapter; keep CLI benchmark. **Highest-uncertainty technical risk.** |
| Strategic-driver / scope mismatch (multi-tenant RBAC is EE-paid, outside the reuse swap) | High | **High** | Pull EE decision to day-zero (§7/§9); deliver multi-user first. |
| **MCP boundary latency under convergence load (G-B) unbenchmarked** | Medium | **High** | New Phase-0 gate G-B; a slow boundary turns "keep Python" into a perf regression. |
| **ACP spec itself immature/churning (G-A)** | Medium | High | New Phase-0 gate; pin spec version + verify governance. |
| `@mastra/acp` license UNVERIFIED (Apache vs `ee/`) | Medium | Medium-High | Phase-0 commercial blocker. |
| ACP parity for permission flags / `CLAUDE_WORK_DIR` UNVERIFIED | Medium | High | Phase-0 blockers 1, 3, 4. |
| Sprint flagship harder than framed (test-only `_subprocess_factory`, monitor/tmux entanglement) | High (verified) | Medium-High | Sequence sprint LAST; gate on telemetry report; typed parallel-run gate. |
| **"5% tolerance" gate unfalsifiable as written** | High | Medium-High | Replace with G-C typed differential spec (metric/sample/direction/pass-fail) before Phase 2. |
| Mastra API churn (1.0→1.16 breaking; quarterly codemods; Node 22.13 floor) | High | Medium | Version-pin + codemod discipline + an abstraction seam over Mastra; Mastra-late sequencing. |
| **Permanent-polyglot staffing/ownership absent (A-003)** | Medium | High | Phase-0 operating-model gate; if unmet, hybrid collapses to rewrite-or-no-go. |
| Per-tool ACP parity (Cursor/Gemini/Copilot) UNVERIFIED | Medium | Medium | De-prioritized; Claude+1 in Phase 0; others recorded as procurement facts. |
| Backlog.md MCP `decision`/`milestone` exposure UNVERIFIED | Medium | Medium | Live `/mcp` probe in Phase 3; CLI fallback. |
| Python↔TS boundary tax (permanent two-runtime ops) | High (by design) | Medium | Treat the MCP boundary as permanent architecture; budget polyglot ops. |
| Beads / Dolt instability + dual-source drift | Medium | Medium | Drop/defer Beads v1; Backlog.md mirror is the single store. |
| MDTM semantics have no Backlog.md schema | Medium | Medium | Keep in Python; mirror task state only; reject if lossy. |
| **Tenant pilot fails to beat current CLI + worktrees/subagents throughput** | Low-Medium | High (sunk cost) | Phase-5 control-plane gate with measured side-by-side before decommissioning. |
| **Phase-0 success misread as full-port feasibility (INV-013)** | Medium | Medium-High | State explicitly: Phase-0 authorizes only the next bounded validation phase; G-A/B/C/D are necessary, not sufficient. |
| **MCP/HTTP backend security boundary ungated (D2)** — ~62K LOC of audit/FMEA/gates exposed as an MCP server with no authn/authz, input validation, or per-tenant isolation | Medium | **High** | New gate **G-E**; front-door SimpleAuth/EE RBAC does not secure the backend; gate the MCP boundary security model in Phase 0 (design) / Phase 1 (proof). |
| **Tenant-isolation / noisy-neighbor / fair-scheduling design absent pre-build (D2/INV-012)** | Medium | **High** | New **pre-Phase-5 tenant-isolation DESIGN gate**; the EE-vs-DIY decision and the pilot do not substitute for an up-front isolation architecture. |
| **Cross-model output non-equivalence (D5)** — non-Claude models (gpt-5.5/qwen3.6-plus) may produce non-gate-equivalent artifacts; G-C baselined on Claude | Medium | Medium-High | New gate **G-F** cross-model gate-equivalence probe; "Claude + one tool" proves transport, not equivalence. |
| **Coupled gate-failure masking (D3/INV-011)** — G-A/G-B/G-C pass individually but interact (pinned spec + lossy telemetry + load-dependent latency) | Medium | **High** | New gate **G-D** combined end-to-end stress test; independent passes are necessary but not sufficient. |
| **ACP/Mastra version drift after Phase 0 (D3/INV-003)** — telemetry rewrite targets a moving spec with no re-validation rule | Medium | Medium-High | **G-A hardened:** regression corpus + re-validate-on-version-bump rule, not a point-in-time pin. |
| **Phase-4 "Mastra-value" gate references evidence nothing produces (D4)** | Medium | Medium | New Phase-0 **Mastra-value-vs-thin-client deliverable** produces the comparison the Phase-4 precondition depends on. |

<!-- Source: Variant 1 §10 register + Variant 2 reordered gates + invariant-probe HIGH items folded in (Changes #10,#11,#12); audit-response rows D2-D5 added (Changes #15-#18) -->

---

## 11. Decision Gates (ordered by what decides go / defer / no-go)

1. **`@mastra/acp` licensing (day-zero, decidable NOW).** If EE-gated, "Mastra-late / vendor-free" is dead and the recommendation hardens toward no-go-on-Mastra. Procurement evidence, not architecture.
2. **Telemetry-reconstruction parity (blocker 2).** Can ACP events reproduce `monitor.py`'s F2/F4/F6 turn/token/tool-error/stall semantics? If not, sprint reliability degrades silently. Hard blocker.
3. **Permission semantics parity (blocker 3).** The CLI relies on Claude-specific permission flags (`commands.py:88-117`); multi-tool ACP risks lowest-common-denominator semantics. Hard blocker.
4. **Process lifecycle / cancellation + workspace isolation (blocker 4).** `CLAUDE_WORK_DIR` isolation (`:1320-1324`) and cancellation must survive the swap.
5. **MCP boundary latency under convergence load (G-B).** Unbenchmarked; a slow boundary negates the "keep Python" thesis.
6. **ACP spec maturity (G-A).** Pin a version; verify governance — neither source doc checked the spec itself.
7. **Typed acceptance metric (G-C).** Replace the unfalsifiable "5% tolerance" before any parallel-run gate can mean anything.
8. **Permanent-polyglot operating model / staffing (A-003).** A pre-Phase-1 architecture decision, not a "later philosophical" question.
9. **MDTM→Backlog round-trip losslessness.** Gate before Backlog can ever become task-of-record.
10. **Tenancy control-plane pilot (Phase 5).** Isolation + noisy-neighbor + throughput-vs-baseline before decommissioning the CLI.

**Audit-added gates (2026-06-03 reflect response — slot into the ordering at the indicated priority):**

- **G-D — Coupled end-to-end stress test (priority ~7.5, audit Change #16 / D3 / INV-011).** Run telemetry reconstruction, gate verdicts, and boundary latency *together* under convergence-loop load. Independent passes of blockers 2/5/6 (G-A/G-B/G-C) are necessary but **not sufficient** — they mask coupled failure modes. Hard blocker before Phase 2.
- **G-E — MCP/HTTP backend security model (priority ~4.5, audit Change #16 / D2).** The reuse-eligible IP wrapped "as an MCP tool server" (§4) is the real multi-tenant attack surface; front-door SimpleAuth/EE RBAC does not secure it. Gate authn/authz + input validation + per-tenant data isolation in Phase 0 (design) / Phase 1 (proof). Hard blocker before broad extraction.
- **G-F — Cross-model output equivalence (priority ~5.5, audit Change #18 / D5).** "Claude + one tool" proves the **transport** abstraction; it does not prove that gpt-5.5 / qwen3.6-plus produce **gate-equivalent** artifacts. Probe gate-equivalence across Claude + ≥1 non-Claude model. The deepest multi-tool risk.
- **Tenant-isolation DESIGN gate (priority ~9.5, audit Change #16 / D2 / INV-012), pre-Phase-5 build.** A concrete isolation / noisy-neighbor / fair-scheduling architecture, gated *before build* and independently of the EE-vs-DIY decision and the end-to-end pilot. Licensing is not architecture.
- **G-A hardening (folds into gate 6 / D3 / INV-003).** Gate 6 (ACP spec maturity) is not a point-in-time pin: it requires a regression corpus + re-validate-on-version-bump rule for the telemetry rewrite.
- **Mastra-value-vs-thin-client deliverable (folds into Phase 0 / D4).** Produces the evidence Phase 4's "proceed only if Phase 0 proved Mastra-specific value" precondition depends on; without it that precondition is unsatisfiable.

**De-prioritized:** per-tool ACP parity for Cursor/Gemini/Copilot — it front-loads uncertainty irrelevant to the go/defer decision. Claude + one tool is sufficient to prove the **transport** abstraction (output equivalence is gated separately by G-F).

**Sufficiency caveat (INV-013/INV-014):** gates 1–7 passing **authorizes the next bounded validation phase** — it does not certify that the full ~62K-LOC port re-hosts cleanly or that the company-wide throughput goal is met. Those are proven only by Phase-1-exit (broader boundary load) and the Phase-5 pilot.

<!-- Source: Variant 2 §4 reordered gates + panel new gates + invariant sufficiency framing (Changes #10,#11,#12) -->

---

## 12. Recommendation Recap

**DEFER the multi-phase port; run a standalone, time-boxed Phase-0 intelligence sprint first.** The codebase is *partially* built for runtime substitution — **`pipeline` is a clean injected `StepRunner` seam; `roadmap` is only partly factory-wrapped (1107 direct vs 1358 wrapped); `sprint` is not substitution-clean** (test-only `_subprocess_factory`; hardcoded prod `ClaudeProcess` + `CLAUDE_WORK_DIR`) — all source-re-confirmed this session (6/6 citations). The "1.2K LOC coupled" headline is arithmetically true but reframed to **"a narrow file seam plus a broad behavioral contract."** The favorable **V33 > R26** inverts to **V~28 < R~34** — the **ordinal/directional** basis for moving from go-ish to defer (the scores are directional composites, not measured metrics, and the new gates are non-scored hard blockers — see §1 scoring methodology / INV-008).

Sequence (when the port is authorized): swap the **pipeline** seam first, **roadmap** second, **sprint last** (gated on a `monitor.py` telemetry-reconstruction report); expose **3–5 verified-pure checkers** behind MCP before any broad extraction; adopt Backlog.md (MIT) as a **derived mirror, not task-of-record**, until a lossless round-trip is proven; **drop Beads for v1**; pull the **`@mastra/acp` license + EE-buy-vs-DIY *decision* to day-zero**, while the tenancy **build** stays last.

**The load-bearing caveat:** the strategic driver — multi-tenant RBAC — is **Mastra-EE-paid and outside the reuse swap**, so the technical port can fully succeed and still not meet the company goal without the separate, day-zero-decided EE-buy-vs-DIY gate. **The highest technical risk is `monitor.py`'s stream-json→ACP reconstruction.** Three gates neither source document caught — **ACP-spec maturity (G-A), MCP boundary latency (G-B), and a typed acceptance metric (G-C) replacing the unfalsifiable "5% tolerance"** — plus an operating-model/staffing gate and an end-to-end tenancy control-plane pilot, are now first-class. **Phase-0 success authorizes only the next bounded validation phase; it does not certify end-to-end feasibility.** If any commercial or load-bearing-parity gate fails, the recommendation hardens to **no-port** with under two weeks sunk. Headline directional composites **V ~28 / C ~34 / L ~20 / R ~34** (ordinal, not measured — §1).

<!-- Source: Variant 1 §12 recap rewritten with Variant 2 conclusions + all new gates (Changes #1-#12) -->
