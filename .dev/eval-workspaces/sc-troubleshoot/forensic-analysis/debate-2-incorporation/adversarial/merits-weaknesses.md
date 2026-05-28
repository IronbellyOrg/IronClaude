# Merits & Weaknesses Analysis — `/sc:forensic` vs `sc:troubleshoot` v2

**Mode**: per-component merits/weaknesses for both designs, against the symptom-driven debugging workload that `sc:troubleshoot` v2 targets.
**Inputs**:
- Forensic design: `.dev/eval-workspaces/sc-troubleshoot/forensic-analysis/forensic-breakdown.md` (713 lines).
- v2 bundle: `src/superclaude/commands/troubleshoot.md`, `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, `refs/{escalation-rubric,triage-checklist,hypothesis-card-template,report-template,remediation-handoff}.md`, `src/superclaude/agents/{evidence-validator,confidence-calibrator}.md`.
- v2 eval evidence: `.dev/eval-workspaces/sc-troubleshoot/iteration-1/*`, `iteration-3/*`.
- Differences catalogue: `debate-1-differences/merged-output.md` (31 substantive diffs).

This is a *workload-anchored* comparison. The metric for "merit" is: does this design choice help diagnose a single reported symptom faster, more reliably, and with less hallucination risk? Forensic optimises for a different workload (project-wide investigation, multi-phase sprint-pipeline), so several of its merits are workload-orthogonal and incur cost without benefit when grafted onto v2.

---

## Component 1: Orchestrator role (dispatcher vs reader) — C-005 + U-003

**Forensic (dispatcher)**

- Merits: Architectural hallucination resistance — Opus orchestrator NEVER reads source, capped ≤8k tokens, Phase 6 consumes only 6 summary artifacts. The synthesizer *cannot* fabricate a `file:line` because the source is not in its context. Cleanly testable: count tokens, assert summary-only inputs.
- Weaknesses: Latency floor — every read goes through a subprocess hop, even trivial ones. Demands rigid phase contracts to work (schemas, manifests). Coordinator-only Opus pays a per-invocation overhead that dominates short investigations. Brittle when phase contracts drift.

**v2 (reader/participant)**

- Merits: Single-turn diagnoses possible (Tier 1 missing-import eval ran in ~60s, confidence 1.00). No file-IPC roundtrip for cheap reads. Orchestrator can iterate on a hypothesis without writing a manifest. Refs lazy-load.
- Weaknesses: Hallucination risk is behavioral, not architectural — the orchestrator *can* fabricate a citation; v2 mitigates with `evidence-validator` (post-hoc) and `confidence-calibrator` (stripped-context re-grading), but those layers can fail. Three eval audit logs explicitly note `evidence-validator` ran "simulated inline" — when the agent isn't available, the inline fallback still relies on the same context that produced the citation.

**Workload fit**: Dispatcher discipline is overkill for symptom triage. v2 already has *behavioral* mitigation that addresses the same failure mode; the architectural mechanism's main advantage (no validator-failure path) is partially undone by the eval evidence that validator-failure has already happened (inline fallback used in 4 of 8 eval runs).

---

## Component 2: Tier/phase model — C-003

**Forensic (8 phases, data-flow gates)**

- Merits: Every phase has a typed artifact contract; Phase 6 has zero-ambiguity inputs. Phases can be tested in isolation. Resume is straightforward (which artifact is missing?).
- Weaknesses: Always runs all phases applicable to the tier — even when Phase 1 returned one high-confidence hypothesis with no need for adversarial debate. No equivalent of v2's Wave 4 *skip-on-consensus*. Cost predictable, but often *predictably wasteful* for the common case.

**v2 (3 tiers, 7 waves, conditional gates)**

- Merits: Wave 2 (confidence gate) and Wave 4 (skip-on-consensus) push the median diagnosis cost down by an order of magnitude. Tier 1 in eval-1 (missing import) was confidence 1.00 and stopped — Wave 3/4/6 never ran. Forensic's light tier would still have run Phase 0 (recon) and Phase 2 (debate).
- Weaknesses: Conditional escalation makes cost less predictable. The rubric for "single-domain" / "intermittent" / etc. is rule-driven; novel signals may slip through. No formal data-flow contract between waves — the orchestrator passes objects in-session, which works for in-session Task agents but doesn't survive a crash.

**Workload fit**: v2's conditional model is the right call for symptom triage. Forensic's always-on phases are right for sprint-runner integration where predictability beats thrift.

---

## Component 3: Agent inventory & lifecycle (in-session Task vs subprocess) — C-004 + C-006

**Forensic (subprocess pipeline)**

- Merits: Each agent gets a fresh context window — no anchoring carryover. Crash isolation. Parallelism via `ThreadPoolExecutor` is honest parallelism (the sprint runner is multi-threaded). Survives `claude --print` non-interactive harness.
- Weaknesses: File-IPC overhead; cannot stream partial results; resume requires manifest schema discipline. Each subprocess pays Claude startup cost. No in-session feedback loop between agents.

**v2 (in-session Task)**

- Merits: Single-message multi-Task parallelism is fast in the interactive harness (eval-3 Tier 2 spawned 3 agents in ~5s). Two new dedicated agent files (`evidence-validator`, `confidence-calibrator`) are independently addressable by other skills. No serialisation tax.
- Weaknesses: Task agents inherit some session state; "anchoring is reduced, not eliminated" per `confidence-calibrator.md:35`. Parallelism is harness-dependent — what counts as "true parallel" varies. No crash isolation between Task spawns; a malformed Task can poison the conversation.

**Workload fit**: In-session Task is correct for v2's interactive use. Forensic's subprocess model is correct for sprint-runner. Neither is intrinsically better; each fits its harness.

---

## Component 4: MCP usage & budgets — C-008 + C-011

**Forensic (explicit per-phase routing + budgets)**

- Merits: Phase-level MCP routing table makes regression-testing cheap. Per-server concurrency cap (NFR-010 ≤3) prevents inadvertent rate-limit ddos. Static per-agent budgets (Phase 1: 3 Serena + 1 Context7 per domain) make token forecasting deterministic.
- Weaknesses: Static budgets are *targets*, not enforced; the harness has no semaphore. Overspec for the symptom-triage case where Tier 1 needs *one* well-aimed query, not a budget envelope.

**v2 (per-tier coverage + rate cap)**

- Merits: `auggie` is the workhorse and is offloaded to a free tier — explicit framing of "Claude tokens are the constrained resource." Tavily rate-cap (≤2/invocation) is enforceable in-prompt. Tier-1 doesn't load context7/tavily at all — the right call when triage usually fits inside one file's worth of context.
- Weaknesses: No per-server concurrency cap. No formal MCP failure-mode matrix beyond "fall back to Grep/Glob." When auggie is down, Tier 1 quality "degrades" without a hard threshold.

**Workload fit**: v2's tier-scoped MCP coverage matches its conditional execution. Forensic's per-phase routing table is overdetailed but its concurrency cap is a genuinely good idea.

---

## Component 5: Failure handling & rollback — C-014

**Forensic (coordinated 3-level chain + selective git rollback)**

- Merits: Coordinated three-level adversarial fallback (retry quick → single Sonnet scoring agent → emit as-is). Selective `git checkout` via `git diff --name-only {baseline}` intersected with `rca-verdict.md` causal files — never reverts prior phases' work. Subprocess SIGTERM→SIGKILL discipline. Stale-codebase detection on resume via `git rev-parse HEAD`.
- Weaknesses: Designed for write-then-rollback workflows; doesn't apply to a diagnosis-first tool that never writes code. The 3-level chain is one mechanism (adversarial-only).

**v2 (per-component matrix)**

- Merits: 10-row error matrix in `SKILL.md:336-350` covering every component (all MCPs down, auggie down, root-cause-analyst fails, all Tier 2 agents fail, `sc:adversarial` fails, self-review blocker, task-builder unavailable, user declines, `evidence-validator` fails, `confidence-calibrator` fails). Each row has a defined fallback. The eval log shows the fallbacks fire correctly under simulated failures.
- Weaknesses: No coordinated retreat — failures are component-local. No git rollback machinery, but the design never auto-applies code, so this is by-design.

**Workload fit**: v2's matrix is the right shape for diagnosis-first. Forensic's chain + rollback is needed only when the tool *also* applies fixes. Importing forensic's rollback into v2 would add complexity for a code path that doesn't exist.

---

## Component 6: Adversarial integration depth — C-009

**Forensic (always-debate in Phase 2 + 3b)**

- Merits: Phase 2 hypothesis debate AND Phase 3b fix debate both invoke adversarial. Phase 3b `fix-selection.md` is the PRIMARY decision point — every fix is debated. Predictable cost per phase.
- Weaknesses: Pays the adversarial cost (15-60k tokens) every time, even when one hypothesis is plainly right. Eval-3 missing-import case had confidence 1.00; debating it would be pure waste.

**v2 (debate-only-on-conflict in Wave 4)**

- Merits: Wave 4 fires only when ≥2 *competing* fixes survive Wave 3. Eval-3 Tier 2 security bug: 2 competing fixes → adversarial fired, picked FIX-A. Eval-1 missing-import: 1 hypothesis, no Wave 4. Token thrift on the consensus path.
- Weaknesses: Skip-on-consensus relies on agents independently arriving at the same fix. If they're all anchored to the Tier 1 hypothesis, the consensus is illusory. The merge-debate-1 invariant probe surfaced exactly this kind of risk (`A-001`).

**Workload fit**: v2's selectivity is the right default for triage. The blind spot (consensus-via-anchoring) is real but is already addressed by `confidence-calibrator`'s stripped-context anchoring mitigation. Forensic's always-debate would harm v2's cost profile and benefit only edge cases.

---

## Component 7: Hallucination contract (withhold-access vs post-hoc validate) — C-016 + U-003 + U-005

**Forensic (withhold access)**

- Merits: Architectural — Phase 6 orchestrator literally cannot fabricate a `file:line` because it doesn't have the file. No validator-failure path. Cleanly enforceable via token cap + manifest-only inputs.
- Weaknesses: Requires the rest of the pipeline to be disciplined enough that summary artifacts don't drop the load-bearing citations. If Phase 4/5 produces a sloppy summary, the orchestrator faithfully relays the sloppiness.

**v2 (post-hoc validate)**

- Merits: `evidence-validator` re-Reads every cited `file:line` in the draft and drops mismatches before REPORT.md ships. If any drop, status → `partial` with a Grounding Gaps section. Independently re-usable by other skills. `confidence-calibrator` adds anchoring-bias mitigation on hypothesis cards.
- Weaknesses: Validator runs in-context — same harness, same model class. Its independence is real but partial (stripped context, not separate process). Eval audit logs show the validator was *simulated inline* in several runs — the fallback path was exercised more than expected.

**Workload fit**: Both approaches target the same failure mode (fabricated citations). v2's two-agent approach is the right shape for in-session execution and gives the symmetry of *grounding* + *calibration*. Forensic's withhold-access approach is the right shape for a multi-phase pipeline. **Genuinely orthogonal** — neither dominates.

---

## Component 8: Activation surface — C-002

**Forensic (explicit + caller-triggered)**

- Merits: Auto-invoked by `task-unified` on TFEP failing-test escalation. Explicit `--caller` flag. Skill pre-step from command file. Predictable: it runs when callers call it.
- Weaknesses: Will never auto-activate on a user's natural-language symptom report. Requires the user to know the tool exists.

**v2 (aggressive auto-activation)**

- Merits: Symptom keywords ("why is X broken", "this used to work", "something's off with"), stack traces, exception names, CI log fragments all trigger. "Pushy because the most common reason users skip a debugging tool is they don't know it would help" (`troubleshoot.md:24`). Eval-tier1-missing-import shows this works — orchestrator pattern-matched the stack trace.
- Weaknesses: Aggressive triggers risk false-positive activation. No formal `--caller` channel, though programmatic skill invocation is supported.

**Workload fit**: v2's surface is correct for an interactive command. Forensic's narrower surface is correct for a sprint-pipeline tool. No conflict.

---

## Component 9: Output contract — C-012

**Forensic (YAML return + `test_is_wrong`)**

- Merits: `test_is_wrong` is genuinely unique — when the debate concludes the test expectations are outdated rather than the code wrong, caller MUST present to user. This is a high-signal flag with clear semantic. Write-on-failure required.
- Weaknesses: YAML is heavier than v2's dict. Several fields are TFEP-specific (`recommended_resume_mode`, `recommended_escalation`).

**v2 (Python dict + `tier_reached` + audit log)**

- Merits: Machine-readable HTML-comment audit blocks (`SC:TROUBLESHOOT:TARGET`, `SC:TROUBLESHOOT:SUMMARY`) — greppable, parseable, present in every eval. `tier_reached` + `escalation_reason` directly answer "what did the tool decide to do, and why?"
- Weaknesses: No `test_is_wrong` equivalent. When the diagnosis concludes the test is wrong, the report says so in prose; the caller must parse to act on it.

**Workload fit**: v2's contract is well-shaped. The `test_is_wrong` flag is a *real* gap — it surfaces a specific, actionable verdict that prose-buries today.

---

## Component 10: CLI / sprint-runner integration — C-015 + U-002

**Forensic (~450-line `sprint/tfep.py` module)**

- Merits: Integrates into the sprint pipeline. Detects TFEP via NDJSON markers. Selective git rollback, remediation task injection, escalation gradient with `EscalationState`. Solves a real problem (sprint phase failed → run forensic → re-launch phase).
- Weaknesses: Zero relevance to v2's symptom-driven workload. v2 is invoked interactively, not by a sprint runner. Importing this would require building a sprint-runner integration that doesn't currently exist for v2.

**v2 (zero CLI integration)**

- Merits: Simpler surface. Shipping cost is just the skill+command+2 agents.
- Weaknesses: Cannot be called by sprint runners. No batch mode. Genuinely a different audience.

**Workload fit**: Orthogonal. Forensic's CLI integration is needed for its workload; v2 doesn't need it for its workload.

---

## Component 11: Test/eval strategy — C-013

**Forensic (10 test files gated at M6, 58 SC, 5-file synthetic fixture)**

- Merits: Schema-conformance tests, canned-artifact fixtures per phase boundary, behavioral-contract testing philosophy (`test-strategy-2.md:16-32`). Single fixture engineered to produce ≥2 domains and observable Phase 0 output. Stop-and-fix severity matrix. Per-milestone gates with explicit M6 rule "ALL tests must pass before release."
- Weaknesses: Heavyweight. Builds in M2 alongside schema definitions, not deferred to M9 — good — but the 58 SC + 6 test types + 10 test files is more machinery than v2's surface needs.

**v2 (eval-workspaces under `.dev/eval-workspaces/`)**

- Merits: Eval cases live as data, not as test code. Audit logs are machine-readable. Easy to add new cases without writing pytest. The current 8 eval logs already demonstrate Tier 1 success, Tier 2 escalation, Wave 0 STOP, dispatch-validation.
- Weaknesses: No schema-conformance tests for hypothesis-card / report templates. No regression suite for the rubric thresholds. The eval cases are read by humans; no automated pass/fail.

**Workload fit**: v2's eval-workspace pattern is more agile but less rigorous. A small subset of forensic's test discipline — specifically the *schema-conformance* idea — could land in v2 without dragging in the rest of the M6 machinery.

---

## Cross-component meta-merits & weaknesses

**Forensic — overall**

- Strong: Architectural discipline (orchestrator-as-dispatcher), data-flow contracts, deterministic resume, sprint-runner integration, coordinated fallback chain.
- Weak: Heavy for short investigations. 22-proposal spec amendment process before authoring even began (Section 16 of breakdown) — signal of residual design ambiguity. Three internal contradictions still standing between checklist and v2 roadmap (P-007, P-008, P-010). M5 is the bottleneck (`roadmap-2.md:376-440`) and absorbs adversarial integration + impl + validation + synthesis — risky concentration.

**v2 — overall**

- Strong: Workload fit (symptom triage), conditional escalation, in-session parallelism, two-agent hallucination contract, evidence-based eval validation, lazy ref loading.
- Weak: No formal output schema for hypothesis cards (a *.md template is suggestive, not enforced). No `test_is_wrong` flag. No per-server MCP concurrency cap. No persistence/resume (re-running creates new slug+timestamp dir; intentional but limits long-running investigations). Adversarial step relies on consensus-skip — vulnerable to anchored consensus.

---

## Mapping to the 31 differences (preview — full classification in `merged-output.md`)

- T1 (5 items, behavior-shaping): mostly REJECT (forensic's choice is workload-mismatched) — C-001, C-003, C-017; one INCORPORATE candidate (C-012 `test_is_wrong`); one SHARED/ADAPT (C-016 hallucination — v2 already has equivalent).
- T2 (5 items, integration-shaping): mostly REJECT (forensic always-debate, two-axis mode, test-strategy heavyweight) — one ADAPT (C-014 add explicit fallback summary in skill); one DEFER (C-013 schema-conformance test for hypothesis card).
- T3 (5 items, infrastructure cluster A): all REJECT (subprocess pipeline, dispatcher, sprint-runner integration are workload-mismatched) — one ADAPT (U-004 escalation-count for repeat-failure detection).
- T4 (4 items, instrumentation-shaping): mostly REJECT or SHARED — one INCORPORATE candidate (NFR-010 per-server MCP concurrency cap as a small enhancement); one INCORPORATE candidate (forensic's prompt-prefix discipline — make `auggie-first` explicit when fixture is real-repo).
- Shared assumptions (2 items): NO ACTION needed — both designs share them.

The classification table with verdicts and rationale lives in `merged-output.md`. The actionable rollup lives in `incorporation-report.md`.
