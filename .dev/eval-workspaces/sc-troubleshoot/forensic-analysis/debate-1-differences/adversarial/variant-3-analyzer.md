# Variant 3 — Analyzer Advocate Card

**Stance**: practical impact / frequency-weighted / what-actually-ships framing
**Output**: catalogue of differences ranked by behavior-shaping significance
**Mandate**: surface differences whose effect users / callers will feel; rank by how much each shapes day-1 behavior

## Position summary

The differences between the two designs cluster into a small set of *behavior-shaping* divergences and a much larger set of *infrastructure-shaping* divergences. The behavior-shaping divergences — scope, activation, tier shape, orchestrator role, output contract, remediation chain — determine what a user experiences when they invoke the tool. The infrastructure-shaping divergences — CLI module, NDJSON markers, subprocess pattern, checkpoint protocol, test strategy — determine how the tool is built, maintained, and reasoned about, but the user only sees them when the tool breaks. For a debate focused on *substantive divergence*, both matter, but the behavior-shaping ones rank higher because they propagate further into how callers integrate.

## Steelman of both designs

Each design is locally coherent — forensic at the "project-wide investigation, multi-phase pipeline, sprint-integration" scope; v2 at the "single-symptom diagnosis, tiered escalation, interactive remediation" scope. The differences are not flaws in either; they are choices about which problem to optimise for. The job of this debate is *not* to declare a winner but to catalogue the divergences crisply enough that a downstream consumer can decide which design's pattern to adopt where.

## Differences I am championing as significant — ranked by behavior-shaping impact

### Tier 1: shapes what users see (highest behavior-shaping impact)

1. **Scope of problems addressed (C-001) — L2.** Forensic auto-discovers domains across the codebase ("3-10 domains, risk-scored"); v2 requires a symptom and a scope. A user invoking forensic with no symptom gets a project-wide sweep; a user invoking v2 the same way is rejected with STOP. This is the single most consequential difference — the two tools answer different questions.

2. **Activation mechanism (C-002) — L2.** v2 has a *substantially* broader auto-activation surface: symptom keywords ("why is X broken"), pasted stack traces, exception names (`NameError`, `TypeError`), CI log fragments, profiler readouts. Forensic activates by explicit command, `--caller` flag, or `task-unified` TFEP escalation. v2 is "pushy because the most common reason users skip a debugging tool is they don't know it would help"; forensic is invoked when the caller knows it's needed.

3. **Tier / phase structure (C-003) — L2.** 8 numbered phases vs 7 named waves is the most immediate UX difference. Forensic's phases are data-flow gates ("phase 1 produces findings, phase 2 debates them, phase 3 proposes fixes"); v2's waves are escalation gates ("wave 2 decides if you need wave 3 at all"). A user who runs `--depth deep` on v2 gets 7 waves; a user who runs `--tier deep` on forensic gets 8 phases regardless of debate depth.

4. **Output contract (C-012) — L1/L2.** Forensic emits `final-report.md` from Phase 6 + per-phase manifests + (for TFEP) `tfep-report.md` + `tasklist-insertion.md` + a YAML return contract with `test_is_wrong` (critical flag — when the debate concludes the test expectations are outdated rather than the code wrong, caller MUST present to user). v2 emits `REPORT.md` + audit.log + structured return dict (`status`, `tier_reached`, `confidence`, `escalation_reason`, `hypothesis_cards`, `adversarial_artifacts_dir`, `task_file_path`, `remediation_offered`, `remediation_accepted`) + machine-readable audit-log header/footer. Different return-contract shapes; forensic's `test_is_wrong` flag is genuinely unique — it elevates "the test is the bug" to a first-class outcome.

5. **Remediation chain (C-017) — L2.** Forensic's remediation auto-injects `T{XX}.50+` tasks into the failing phase's tasklist and re-launches `task-unified --compliance strict` (sprint-runner re-runs the phase). v2's remediation is interactive: task-builder produces the MDTM task file, reflect analyzes it, the user runs `/task` themselves (never the skill), reflect validates before commit. Forensic loops back into automated execution; v2 hands off to a user-initiated execution loop. This is the largest behavior divergence after "scope of problems addressed."

### Tier 2: shapes how callers integrate (medium behavior-shaping impact)

6. **Adversarial coupling pattern (C-009) — L3.** Forensic always invokes `sc:adversarial` at Phase 2 (deep) and Phase 3b (standard); v2 conditionally invokes it in Wave 4 only when ≥2 competing fixes exist (depth quick or standard based on diagnosis similarity). For most-common cases (a single fix proposal), forensic still runs Phase 3b debate; v2 skips. This propagates into token cost predictability (forensic = bounded, v2 = variable).

7. **Two-axis vs single-axis mode (C-010) — L2.** Forensic has `--tier × --depth` two-axis decoupling — the same debate-depth can be paired with light or deep pipeline scope. v2 has `--depth` only — escalation control is collapsed with debate depth. Callers wiring forensic via `task-unified` rely on the decoupling (`--tier light --depth quick`); v2 callers can't express that combination.

8. **Hallucination contract (C-016, U-003) — L3.** Forensic enforces "orchestrator never reads source" as an architectural invariant; v2 enforces "every cited line gets re-Read by `evidence-validator`" as a behavioural invariant with a fallback path. Behavior-shaping impact: callers asking "how do I know the report didn't hallucinate?" get different answers — forensic says "the synthesizer couldn't have", v2 says "the validator re-Read every citation."

### Tier 3: shapes how the tool is built (low immediate UX impact, high long-term)

9. **Execution model (C-004) — L3.** Subprocess pipeline vs in-session Task. Visible mostly through wall-clock latency (subprocess cold-start) and failure mode (subprocess crash vs Task return).

10. **CLI/sprint-runner integration (C-015, U-002) — L2.** Forensic ships a CLI module; v2 doesn't. Users invoking via `superclaude sprint` get forensic auto-on-TFEP; users invoking via Claude Code get either depending on what they call.

11. **Test strategy (C-013) — L2.** 10 test files + 58 success criteria + canned artifacts vs eval workspaces. Maintenance and contribution velocity downstream.

12. **Lifecycle/checkpointing (C-018) — L2.** `progress.json` + `--resume` + `--dry-run` vs slug+timestamp output dirs. Matters when long-running invocations are interrupted; forensic recovers, v2 starts over.

### Tier 4: instrumentation / inventory shifts

13. **Agent inventory (C-006) — L1/L2.** Forensic spawns role-typed subprocess agents per phase (no new `src/superclaude/agents/` files); v2 ships two new dedicated agent files (`evidence-validator.md`, `confidence-calibrator.md`).
14. **Model tiering (C-007) — L1.** Haiku/Sonnet/Opus matrix vs sonnet defaults + `--models` overrides.
15. **MCP usage (C-008) — L1/L2.** Per-phase MCP table + concurrency cap vs per-tier MCP coverage + tavily rate-cap.
16. **Token budget profile (C-011) — L1.** Forensic's per-phase budget table vs v2's per-tier target band.
17. **Refs strategy (S-003, U-006) — L1.** Inline spec vs lazy-load refs per wave.

### Shared unstated assumptions (worth surfacing for debate completeness)

- A-001: Both designs assume adversarial debate is the right adjudication primitive for competing fixes (neither justifies it from first principles).
- A-002: Both designs assume a static Markdown report is the right terminal artifact (neither evaluates alternatives).

## Concessions

- The forensic design's CLI integration, `test_is_wrong` flag, two-axis mode, and project-wide auto-discovery are genuinely unique capabilities the v2 bundle does not have.
- The v2 bundle's `evidence-validator`/`confidence-calibrator` agent pair, lazy-ref loading, machine-readable audit blocks, and Tier 3 user-mediated remediation are genuinely unique capabilities forensic doesn't have.
- The "ranked by behavior-shaping impact" ordering is my analysis — other reasonable orderings exist (e.g. an architect would rank C-004 execution model higher; a QE would rank C-016 hallucination contract higher).

## If my framing is wrong, it's probably because

I am treating each difference as independent when in fact several cluster: C-004 + C-005 + C-015 + U-002 + U-003 are all consequences of forensic's "dispatcher orchestrator + subprocess pipeline + sprint integration" design choice; treating them as 5 separate differences may overstate their independence. The merged output should preserve the cluster structure in its ranking.
