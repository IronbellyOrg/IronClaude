# Adversarial Debate Transcript — DD-2

- Depth: standard (Round 1 parallel + Round 2 rebuttals + Round 2.5 invariant probe)
- Convergence: ~0.83 (threshold 0.80) — CONVERGED on a hybrid
- Positions: A = deterministic-first + downgrade-only Haiku sign-off (DD-2 as written); B = pure-deterministic gate, LLM not in verdict path

## Shared assumptions surfaced (A-NNN)
| ID | Assumption | Classification | Note |
|----|------------|----------------|------|
| A-001 | The last-completed task has a per-task transcript + per-task status at resume | **CONTRADICTED** | True only for the per-task phase path (executor.py:1264-1307). The single-process path (executor.py:1309+) writes one `phase-N-output.txt`, empty `task_results[]`. No per-task object to doubly-validate or to Haiku-judge. |
| A-002 | "downgrade-only ⇒ loop-safe" | STATED/valid | Gate runs once per invocation; STOP exits non-zero; no auto-retry in design §6. No infinite re-validation loop. Probe worry retired. |

## Round 1 (steelman-first)
- **Advocate A**: B is right that NFR-3 mandates an isolated/overridable LLM step. But downgrade-only shrinks the resume-permitted set monotonically — non-determinism that can only ADD a STOP cannot cause an unsafe resume. Operator clears spurious STOPs via `--yes`/`accept_suspect`/`--fresh`.
- **Advocate B**: A is right that deterministic existence checks have a true blind spot — `status=pass`, file exists, but content is empty/wrong. An LLM read is the natural detector. But the gate targets the *last-completed task*; when the boundary's predecessor phase ran the single-process path there is NO last-completed *task* object at all, only a phase-level PASS — so both Signal B and Haiku degrade to judging a whole `phase-N-output.txt`, which is exactly the unbounded/ill-defined call.

## Round 2 (rebuttals)
- **A → REFACTOR self**: scope the Haiku call to `granularity==TASK` with a non-empty last-completed transcript + declared deliverables; skip it entirely for `granularity==PHASE`. Preserves R1 detection where meaningful; avoids the unbounded phase-level call.
- **B → concession**: keep the Haiku read, but make it **advisory** — it annotates the `BoundaryReport` (coherence_warning + review entry) and is surfaced in `print_plan`, but it does NOT flip `passed`. The deterministic layer alone sets the verdict. CI: `invoke_sonnet` returns "" when `claude` absent (summarizer.py) ⇒ advisory mode ⇒ no warning ⇒ gate byte-identical with or without `claude` on PATH. Empty-verdict ambiguity dissolved.

## Round 2.5 — Invariant Probe (fault-finder)
| ID | Category | Assumption | Status (DD-2 as-written) | Status (consensus) | Sev |
|----|----------|------------|--------------------------|--------------------|-----|
| INV-001 | state_variables | "last-completed task" object always exists | UNADDRESSED | ADDRESSED (scope to TASK) | HIGH |
| INV-002 | guard_conditions | truncated last-completed transcript | ADDRESSED — `_classify_transcript` returns INCOMPLETE (rerun_tasks.py:579-580,597-598) ⇒ deterministic suspect | ADDRESSED | MED |
| INV-003 | sufficiency_challenge | Haiku is what makes the gate trustworthy for R1 | UNADDRESSED — wrong-target deliverable caught by `artifacts_ok`; empty output caught by INCOMPLETE; Haiku's unique slice is only "file exists, non-empty, clean result, content semantically wrong" — NARROW | ADDRESSED (Haiku = advisory catch for the narrow residual) | HIGH |
| INV-004 | collection_boundaries | empty `task_results[]` | ADDRESSED — `discover_failed_tasks_from_transcripts` fallback (rerun_tasks.py:604-612) | ADDRESSED | MED |
| INV-005 | interaction_effects | Haiku 30s timeout vs resume flow | ADDRESSED — advisory ⇒ slow/absent Haiku just omits a flag | ADDRESSED | LOW |

Gate: DD-2 as-written has 2 HIGH UNADDRESSED (INV-001, INV-003) ⇒ convergence BLOCKED. The consensus clears both ⇒ CONVERGED.

## Scoring / base selection
- Base = **B** (deterministic gate verdict; NFR-3 is a hard constraint, verdict must be reproducible).
- Incorporate from **A**: the Haiku coherence read for the narrow residual over-claim slice, scoped to `granularity==TASK`, **advisory** (never alters `passed`).
- Verdict: **REFACTOR** (not REJECT — the read survives; not UPHOLD — DD-2 puts the LLM verdict on the gate path and rests on a contradicted assumption).

## Internal-inconsistency note (design self-contradiction)
§8 (design.md:277-278) and §12 (design.md:323) already state the LLM hooks are "advisory, neither can upgrade a deterministic verdict (NFR-3)." But §0/§4(a) (lines 24, 154-157) have the downgrade flip `validated_last=False` → `suspects` → gate STOP, which DOES change the verdict (in the conservative direction). The design conflates "can't upgrade" with "advisory." The REFACTOR makes the code honor the prose: advisory = cannot change `passed` at all.
