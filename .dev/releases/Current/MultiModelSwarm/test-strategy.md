---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 9
work_milestones: 9
interleave_ratio: 1:1
major_issue_policy: stop-and-fix
spec_source: merged-requirements.md
generated: "2026-05-31T18:08:56.421814+00:00"
generator: superclaude-roadmap-executor
---

# Multi-Model Swarm Orchestrator — Test Strategy

## 1. Validation Milestones (1:1 Mapping)

HIGH complexity (0.85) mandates a validation milestone for every work milestone. Each V# runs in parallel with the next W#'s implementation work, but its quality gate must close before that work begins.

**V1: Foundation/Models** | 3 days | exit: 20/20 dataclasses JSON round-trip lossless; module-shape mirror test green; OQ-006/008/009 owners on record
**V2: Preflight/Lens/Guard** | 4 days | exit: §11.5 three-path enforcement proven; INV-005/007 branch tests green; `validate-lenses` passes 7/7 non-custom
**V3: Dispatch/Concurrency** | 4 days | exit: IMM-3 parallelism overlap proven; NFR-011 retry matrix exact; JSONL append non-interleaving under contention
**V4: Normalize/Recipes** | 3 days | exit: 6/6 recipes registered; salvage promotion provenance recorded; AC-011 no-judging boundary verified per recipe
**V5: Reduce/Merge/Contract** | 4 days | exit: IMM-5 parametrized status matrix green; TEST-006 boundary test green; FR-018 contract field completeness 100%
**V6: Resume/Manifest** | 3 days | exit: INV-001/010/016 tests green; lens-mutation immunity proven; `--force-relens` opt-in path proven
**V7: Observability/CLI** | 3 days | exit: 8/8 subcommands smoke-pass; INV-012 non-TTY plain-output verified; three monitoring patterns demonstrated
**V8: Migration/Hardening** | 5 days | exit: TEST-001..007 all green; A/B parity byte-equivalence on bare-review corpus; TEST-005 cross-language contract identical
**V9: Operational Handoff** | 3 days | exit: OPS-001..006 published; rollback rehearsed; OPS-002 readiness script CI-green; OPS-001 examples verified against `--help`

## 2. Test Categories

| Category | Tooling | Coverage Target | Scope |
|---|---|---|---|
| Unit | `uv run pytest tests/swarm/unit/` | 90% on models/schema/recipes/merge/lenses | Dataclass round-trip, schema validators, recipe shape transforms, merge LOC+order, lens-registry validators |
| Integration | `uv run pytest tests/swarm/integration/` | All wave transitions | Wave 0→1→2→3 against stub transport; state-file atomicity; JSONL lock-coordination under N=8 workers; resume cycle |
| E2E | `uv run pytest tests/swarm/e2e/ -m e2e` | All 8 subcommands + 3 monitoring patterns | Full `swarm run` against stub; detached+attach+kill cycle; `subprocess.run` cross-language driver |
| Acceptance (IMM/INV) | `pytest -m imm` / `pytest -m inv` | 5 IMM + 7 INV named tests | Per-invariant dedicated assertions (TEST-001, TEST-002) |
| Contract | `pytest -m contract` | All FR-018 fields | Schema validation of `return-contract.yaml`, `done.json`, `manifest.json` against DM-012/017/016 |
| Boundary | `tests/swarm/test_merge_mechanical_only.py` | CI file-touch rule | 3-worker concat slot-order + provenance-header-only; LOC ceiling |
| Parity | `pytest -m parity` | bare-review corpus | A/B byte/structure equivalence (gates MIG-003) |
| Operational | `pytest -m ops` | OPS-002 readiness script | Env vars present; tmux available; T2 proxy reachable check |

## 3. Interleaving Strategy

**Ratio 1:1 justification:** HIGH complexity (0.85) is driven by (a) 5 IMM + 7 INV verbatim invariants that each demand dedicated regression coverage, (b) concurrency correctness (ThreadPoolExecutor + lock-coordinated JSONL + atomic state), (c) a mechanical-merge boundary that erodes silently without continuous protection, and (d) caller-agnostic contract surface that must stay Claude-ism-free. A 1:2 or 1:3 cadence would batch invariant verification too far from introduction, allowing drift between schema, dispatch, and contract layers before validation catches it.

**Continuous-parallel execution model:** V(N) runs concurrently with W(N+1)'s implementation; W(N+1) cannot exit until V(N) is green. Validation engineers consume W(N)'s green CI and the M(N) exit-criteria artifact list; they do not block W(N) from declaring code-complete, but they do block W(N+1) from declaring milestone-complete.

**Sequencing:**

```
Week:  1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17
Work:  W1──W1──W2──W2──W3──W3──W4──W4──W5──W5──W6──W6──W7──W7──W8──W8──W9
Val:        V1──────V2──────V3──────V4──────V5──────V6──────V7──────V8──V9
Gate:             G1      G2      G3      G4      G5      G6      G7    G8 G9
```

Gate G(N) closes V(N) before W(N+1) exit.

## 4. Risk-Based Prioritization

| Tier | Risk Driver | Tests | Rationale |
|---|---|---|---|
| P0 — must-green-before-merge | R-004 merge boundary erosion; R-013 validation gap; §11.5 injection | TEST-006 boundary; TEST-001 IMM suite; TEST-002 INV suite; NFR-003 injection negative tests | Silent failure modes; caller trust violation |
| P0 — must-green-before-W(N+1) | R-001 model churn; R-010 T2 proxy unreachable; R-005 resume+lens | DM round-trip; stub-transport CI lane; INV-001 manifest rehydration | Ripple-effect blast radius |
| P1 — must-green-before-release | R-011 A/B parity; R-016 ops readiness; R-018 source-of-truth | TEST-003 parity; OPS-002 readiness; `make verify-sync` CI gate | Release-quality gates |
| P2 — must-green-before-stable promotion | R-003 lens sprawl; R-014 PR-review erosion | U-008 validator; lens contribution policy enforcement | Long-term maintainability |

## 5. Acceptance Criteria Per Milestone

**V1:** All 20 DM dataclasses round-trip via `dataclasses.asdict`/`from_dict` lossless; `superclaude swarm --help` exits 0 listing 8 subcommands (placeholders OK); NFR-015 module-shape parity assertion green; `make verify-sync` clean.

**V2:** `swarm validate <good-spec.yaml>` exits 0; `swarm validate <missing-§11.5-substring.yaml>` exits non-zero with diagnostic; `swarm validate-lenses` exits 0 for 7 non-custom entries; INV-005 worker>pool branch produces resolved OQ-007 behavior (warn-with-defaults OR STOP per resolution); INV-007 empty-pool produces structured `failed`/`env-missing` contract when output dir creatable; IMM-4 49-byte target produces `failed`/`target-too-small` with no dispatch attempt; INV-003 custom-prompt-dir without §11.5 substring rejected; INV-014 lens-path and custom-dir-path reject identical guard violation.

**V3:** IMM-3 stub-worker parallelism test: 4 workers with 1s stub delay complete in <1.8s wall-clock (overlap proof); INV-002 grep audit confirms zero `swarm_dispatch.sh` references; AC-004 confirms no raw `ThreadPoolExecutor()` instantiation outside ParallelExecutor; NFR-011 retry matrix: 5xx→1 retry, 4xx→0, timeout→0, network→0; NFR-002 8-worker concurrent JSONL append produces 8 parseable lines; NFR-013 path-escape attempt rejected.

**V4:** 6 recipes resolvable via `REGISTRY[name]`; `custom-py:tests.fixtures.recipe:normalize` dynamic loader returns expected output; `parse_error → success` salvage records provenance in meta sidecar; AC-011 per-recipe assertion: input findings count == output findings count, no scoring fields injected; per-lens template path resolves and aligns with recipe output shape.

**V5:** IMM-5 parametrized over (M==N==3→success), (M==N==2→success), (2≤M<N→partial), (M=1→failed), (M=0→failed); merge module body LOC count ≤30 enforced by CI assertion; TEST-006: 3 workers with findings [A], [B], [C] produces `merged.md` containing exactly `## From {label} ... A ... B ... C` in that order with no other content; FR-018 contract YAML parseable, all DM-012 required fields present, `merged_path` null when mode!=normalize+merge.

**V6:** TEST-007 kill-mid-Wave-1, resume, observe: successful workers skipped (meta sidecar respected); remaining re-dispatched; Wave 2 reruns over all; merge regenerated (mtime newer than pre-kill merge); INV-016: mutate `LENSES[bare-review]` between runs, resume, assert resumed job used pre-mutation snapshot from manifest; `--force-relens` ignores manifest and uses current registry.

**V7:** 8 subcommand smoke tests exit 0; `swarm run` without `--tui` on non-TTY produces zero `\x1b[` escape sequences in stdout; `swarm run --tui` on TTY produces Rich dashboard; detached job survives `kill -9 <caller-pid>` and reaches terminal state; all three monitoring patterns documented + automated demonstration script.

**V8:** All TEST-001..007 green; A/B parity: same target through current bare-review and through thin-caller `--lens bare-review` produces normalized output with identical row count, identical findings text (modulo timestamps); TEST-005 Go/Node subprocess driver receives identical YAML contract; `make verify-sync` clean post-migration; legacy `scripts/*.sh` absent from skill package.

**V9:** OPS-001 runbook commands executable verbatim; OPS-002 readiness script returns 0 on properly-configured host, non-zero with diagnostic on missing T2 env vars; OPS-004 rollback rehearsal documented with timestamps; OPS-003 four-artifact monitoring procedure demonstrated end-to-end.

## 6. Quality Gates Between Milestones

| Gate | Blocks | Exit Criteria | Major-Issue Policy |
|---|---|---|---|
| G1 → W2 | M2 entry | V1 acceptance green; DM freeze committed; OQ-006/008/009 owners published | Schema-defining DM field gaps = MAJOR → stop-and-fix |
| G2 → W3 | M3 entry | V2 acceptance green; OQ-007/008/010 resolutions merged; injection-guard three-path test green | §11.5 bypass or INV-005/007 branch gap = CRITICAL → stop-and-fix |
| G3 → W4 | M4 entry | V3 acceptance green; IMM-3 overlap test stable across 10 runs; stub transport CI lane green; live T2 lane gated-on-env documented | Parallelism non-determinism or atomicity gap = CRITICAL → stop-and-fix |
| G4 → W5 | M5 entry | V4 acceptance green; AC-011 per-recipe assertion green; custom-py loader trust boundary documented | Recipe scoring/filter creep = MAJOR → stop-and-fix |
| G5 → W6 | M6 entry | V5 acceptance green; TEST-006 boundary test protected by CI rule on file path; merge LOC ceiling enforced | Merge transforms beyond mechanical concat = CRITICAL → stop-and-fix; LOC>30 = MAJOR → stop-and-fix |
| G6 → W7 | M7 entry | V6 acceptance green; INV-001/010/016 tests green; manifest immunity proven under registry mutation | Resume corruption or stale-merge regen failure = MAJOR → stop-and-fix |
| G7 → W8 | M8 entry | V7 acceptance green; INV-012 non-TTY plain output confirmed; AC-013 grep audit clean (zero Claude-isms in contract surface) | Claude-ism leak into contract = MAJOR → stop-and-fix |
| G8 → W9 | M9 entry | V8 acceptance green; TEST-003 parity gate green (gates MIG-003); MIG-001 source-first sync confirmed | A/B parity divergence or premature `scripts/*.sh` deletion = MAJOR → stop-and-fix; staged `.claude/*` content = CRITICAL → stop-and-fix |
| G9 → Release | Release tag | V9 acceptance green; OPS-001..005 published; rollback rehearsed once | Missing runbook or untested rollback = MAJOR → stop-and-fix |

**Issue handling policy across all gates:** CRITICAL halts current milestone immediately; MAJOR halts next milestone entry; MINOR tracked in backlog without gate impact; COSMETIC backlog only.

## 7. Continuous-Parallel Validation Engineering Notes

- **Stub-first CI lane** is the primary correctness lane (R-010 mitigation). Live-T2 lane is gated on env presence and runs as an additional signal, never as a blocking gate, to keep CI deterministic.
- **Boundary test (TEST-006)** is the protected artifact: any PR touching `tests/swarm/test_merge_mechanical_only.py` triggers extra-reviewer assignment via CI rule (NFR-009).
- **Cross-language harness (TEST-005)** runs from a Go or Node driver under `tests/swarm/e2e/cross_lang/` to enforce AC-013 / NFR-016 without Python-only blind spots.
- **Parity corpus (TEST-003)** sources targets from existing bare-review fixtures; equivalence checker normalizes timestamps + run-IDs before diff to avoid spurious failures.
- **Validation engineers own** OPS-001 example regeneration from final `--help` output (R-019 mitigation) and OPS-002 readiness script CI execution.
