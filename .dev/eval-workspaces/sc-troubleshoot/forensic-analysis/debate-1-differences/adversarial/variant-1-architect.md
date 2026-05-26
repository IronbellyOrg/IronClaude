# Variant 1 — Architect Advocate Card

**Stance**: structural / dependency / long-term-impact framing
**Output**: catalogue of architectural divergences between forensic and v2 bundle
**Mandate**: surface differences that shape system topology; debate-relevant for L2 (structural) and L3 (state-mechanics) levels

## Position summary

The forensic design and the v2 bundle express two fundamentally different *systems*: the former is a multi-process pipeline with a strict in-process/out-of-process boundary and a hard ≤8k orchestrator-token discipline; the latter is an in-session Claude-Code skill with a participant orchestrator that itself does the reading, dispatching, and validation. These are not refinements of one another. From an architectural-divergence standpoint, the most consequential differences are: (1) the execution model (subprocess pipeline vs in-session Task), (2) the orchestrator role (dispatcher vs participant), (3) the integration surface (`sprint/tfep.py` CLI module vs skill/command only), and (4) the tier/phase shape (8 numbered phases bound by data-flow contracts vs 7 waves bound by conditional escalation gates).

## Steelman of the v2 bundle (Variant B)

The strongest version of the v2 bundle's architectural choice is that *the cost of subprocess orchestration is real and non-trivial*. Each `claude --print` spawn pays cold-start latency, loses in-context efficiency, and requires file-based IPC for everything that would otherwise be a function return. For a symptom-driven diagnosis that needs to complete in 1-3 minutes on the common path, that overhead is exactly wrong. v2's in-session Task dispatch keeps the wall-clock cheap for the Tier 1 case (the case the rubric exists to optimise for) and only escalates when the rubric says the cost is justified.

The participant-orchestrator choice is similarly defensible: the orchestrator is the only entity in the v2 design with the union of all context (Wave 0 flags + Wave 1 hypothesis + Wave 3 cards + Wave 4 adversarial output + Wave 5 evidence validation). Forcing it to read everything through file artifacts only — as the forensic dispatcher requires — would re-create the same blob that the skill was structured to avoid. The v2 design accepts the hallucination risk and pays for it with the dedicated `evidence-validator` agent.

## Architectural differences I am championing as significant

1. **Execution model (C-004) — L3.** Subprocess vs in-session is the single largest divergence in the two designs. It dictates the IPC contract (file-based vs return-dict), the parallelism mechanism (`ThreadPoolExecutor` vs single-message Task parallel calls), and the failure surface (subprocess crash + SIGTERM/SIGKILL vs Task failure + retry). Every downstream architectural choice (rollback, resume, NDJSON markers, `PhaseStatus.TFEP_HALT`) is downstream of this one.

2. **Orchestrator role (C-005, U-003) — L3.** Forensic's hard ≤8k orchestrator-token cap, with the prohibition that Opus NEVER reads source, is a *structural* hallucination contract: by construction, the synthesising agent cannot fabricate a `file:line` reference because it doesn't have the file. v2 replaces this with a *behavioural* hallucination contract: the orchestrator can read, but the `evidence-validator` agent re-Reads every cited line and drops mismatches. These are not equivalent — the first is enforced by the architecture, the second by an agent that can fail (and has a documented fallback).

3. **Integration surface (C-015, U-002) — L2.** The forensic design ships a full CLI module — `sprint/tfep.py` — and modifies six other sprint-runner files. It is wired into the `superclaude sprint` pipeline, scans NDJSON stdout for `TFEP_TRIGGERED`/`TFEP_RESOLVED`/`TFEP_ESCALATED`, and has its own `PhaseStatus.TFEP_HALT` exit code. v2 has zero CLI integration. This is the largest *surface* divergence — forensic adds a runtime; v2 ships an interactive skill only.

4. **Tier/phase shape (C-003, C-010) — L2.** Forensic's 8-phase numbered pipeline is shaped by *data flow* (Phase N produces artifact A, Phase N+1 consumes A); v2's 7-wave structure is shaped by *escalation gates* (W2 confidence gate, W4 ≥2-competing-fixes gate, W6 user-accept gate). Forensic's `--tier × --depth` two-axis model is a direct consequence of needing to scale the pipeline scope (which phases run) independently of debate quality; v2 collapses both into `--depth`.

5. **Adversarial coupling (C-009) — L3.** Forensic *always* delegates Phase 2 and Phase 3b to `sc:adversarial`. v2 delegates Wave 4 only when ≥2 competing fixes survive Wave 3 — on consensus, the debate is skipped to avoid token waste. This is a quality-vs-cost trade: forensic prefers always-debate (token cost paid for design certainty); v2 prefers maybe-debate (token saved when the signal already converged).

6. **Lifecycle / checkpointing (C-018, U-002) — L3.** Forensic has `progress.json`, stale-codebase detection on resume, dry-run, and a documented resume protocol borrowed from `sc:cleanup-audit-protocol`. v2 has no checkpoint primitive — re-running creates a new slug+timestamp output dir. This is a deliberate divergence (forensic is a long-running multi-phase batch job; v2 is a 1-15 minute interactive diagnosis), but it shapes how the two systems recover from interruption.

## Concessions

- The two-axis `--tier × --depth` model is genuinely complex to use; v2's single-axis approach has real usability merit for the symptom-driven case.
- v2's `evidence-validator` and `confidence-calibrator` agent files are explicit, addressable, and reusable in a way that forensic's "phase Sonnet agent doing self-review" pattern is not.
- The lazy-ref-loading pattern (U-006) is an architectural improvement v2 has that forensic does not (forensic's whole spec is loaded at once in `forensic-breakdown.md`; v2 loads only what each wave needs).

## If my framing is wrong, it's probably because

I am over-weighting the *systems* aspect of this comparison and under-weighting the *user-facing UX* aspect. The forensic design's architectural rigor (≤8k orchestrator, subprocess isolation, NDJSON marker detection) may be exactly the wrong fit for the Tier 1 symptom-triage case, where the user pays for the latency in seconds and wants the answer back in chat, not in a phase-N artifact dir.
