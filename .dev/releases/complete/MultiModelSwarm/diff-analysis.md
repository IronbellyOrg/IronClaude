---
total_diff_points: 9
shared_assumptions_count: 12
---

# Comparative Analysis: Opus vs Haiku Architect Variants

## Shared Assumptions and Agreements

Both variants converge on the foundational architecture and invariants:

1. **Three-layer separation** (mechanism/policy/caller) per AC-001 — orchestrator owns mechanism, lenses+recipes own policy, caller owns choice.
2. **ThreadPoolExecutor via `ParallelExecutor`** — both reject shell-script dispatch, asyncio, and multiprocessing (AC-005, FR-041, NFR-001).
3. **CLI as orchestrator home** — neither variant places orchestration logic in SKILL.md (AC-002).
4. **Bundled lens registry as Python dataclasses** — both reject plugin-system designs (AC-003); 8 lens entries.
5. **Mechanical merge with ≤30 LOC ceiling** — both apply four structural guards; no scoring/dedup/reorder (AC-009, NFR-006).
6. **Manifest-as-source-of-truth for resume** — both default to rehydrating from `manifest.resolved_lens_entry`; `--force-relens` opt-in (INV-001/INV-016, FR-043, FR-044).
7. **§11.5 injection-guard parity across 3 input paths** — STOP default, `--auto-inject-guard` for backward compat (NFR-002, INV-003/INV-014).
8. **Module layout mirrors `cli/sprint/`** — both treat operator continuity as a hard constraint (NFR-007).
9. **Opt-in TUI** — neither defaults to Rich Live; both gate on `--tui` + TTY (NFR-012).
10. **Same 9 subcommands** — run, status, logs, attach, kill, scaffold, validate, validate-lenses (+ implicit help).
11. **Same 16-test invariant suite** — SC-001 through SC-016 with identical semantics.
12. **Same risk register topology** — 9-11 risks largely overlapping (R-01 merge erosion, R-02 lens sprawl, R-03 resume/mutation, R-04 tmux dep, R-05 ThreadPool surprise, R-08 normalizer drift).

## Divergence Points

### 1. **Total Timeline: 16 weeks vs 12 weeks**
- **Opus:** 16 weeks (W1–W16), spreading wave milestones across 2 weeks each.
- **Haiku:** 12 weeks, compressing dispatch (M4=2wk vs Opus M5=2wk) and most waves into single weeks.
- **Impact:** Opus buffers risk on highest-complexity waves (M5 dispatch, M6 normalize+merge, M7 CLI surface gets 3 weeks). Haiku's tighter schedule front-loads risk on the dispatch milestone but may under-buffer the CLI/observability surface (1 week vs 3). Haiku's compression is plausible only if M4 dispatch lands clean on first attempt.

### 2. **Milestone Decomposition: 9-step vs 9-step but different cut lines**
- **Opus:** M1 Foundation → M2 Transport+Recipes → M3 Lens Registry → M4 Preflight → M5 Dispatch → M6 Normalize+Reduce+Merge → M7 CLI+Observability → M8 Tests → M9 Migration.
- **Haiku:** M1 Foundation+Models → M2 Schema+Lenses+Config → M3 Preflight → M4 Dispatch → M5 Normalize → M6 Reduce+Merge → M7 TUI+Detached → M8 Integration+Tests → M9 Migration.
- **Impact:** Opus separates Transport+Recipe protocols (M2) from Lens Registry (M3), enforcing protocol-before-policy ordering. Haiku merges schema+lenses+config into M2, keeping recipes inside M5 (Normalize). Opus is cleaner for parallel team allocation (M2/M3 share only M1); Haiku reduces cross-milestone hand-offs but couples recipe development to normalize.

### 3. **Recipe Layer Placement**
- **Opus:** Recipes get a dedicated foundation milestone (M2 Transport+Recipe Layers, 1 wk) — `RecipeProtocol`, REGISTRY, and all 6 recipes shipped before lens registry is built.
- **Haiku:** Recipes deferred to M5 Normalize (W6–W7) — recipe registry, all 6 recipes, and Wave 2 dispatcher built together.
- **Impact:** Opus's approach surfaces recipe-protocol issues before lens entries reference `recipe_name`, eliminating a class of late-stage rework. Haiku's approach delays validation that `bare_review_v1` ports cleanly from `t2_normalize.py` — a known high risk (R-08) — until week 6+ when it could have been caught at week 3.

### 4. **OQ-007 / OQ-008 Resolution Timing**
- **Opus:** Both open questions tracked under M1; OQ-007 (worker-count guard) and OQ-008 (empty-pool failure path) recommended for resolution during M1 design to avoid `status_policy`/`WorkerSpec` rework.
- **Haiku:** OQ-007 deferred to M2 resolution; OQ-008 deferred to M3 — both pushed past the data-model foundation.
- **Impact:** Opus's earlier resolution prevents downstream churn in M5/M6. Haiku accepts data-model rework risk in exchange for letting OQ resolution discover requirements organically during schema/preflight design. Opus is the safer call; Haiku is faster if resolution comes cleanly.

### 5. **Detached Mode (`tmux.py`) Placement**
- **Opus:** `tmux.py` arrives in M7 (CLI surface, W12–W14) alongside attach/kill/status subcommands as one cohesive lifecycle delivery.
- **Haiku:** `tmux.py` arrives in M4 (Dispatch, W4–W6) — listed as a Dispatch milestone deliverable — separate from attach/kill which arrive in M7.
- **Impact:** Haiku splits detached-mode infrastructure from the subcommands that drive it, creating a 2-3 week gap where tmux.py exists but is not callable. Opus keeps the whole lifecycle (spawn + attach + kill) in one milestone, which is cleaner for the SC-014 end-to-end test gate.

### 6. **CLI Surface Granularity**
- **Opus:** Devotes a single XL-effort milestone (M7, 3 weeks, 34 deliverables) to CLI surface, resume, detached, observability, monitoring patterns, and non-precluding contract surface — explicit emphasis on this being the largest surface-area delivery.
- **Haiku:** Spreads CLI subcommands across M3 (`--lens`, `--custom-prompt-dir`, `--auto-inject-guard`), M4 (`exit codes`, `--detached`), M6 (`--amalgamation-mode`, `--force-relens`, resume), M7 (status/logs/attach/kill/scaffold), and M9 (run, group registration).
- **Impact:** Opus concentrates risk and review burden but allows the wave pipeline (M4-M6) to focus purely on mechanism. Haiku threads CLI surface through every milestone, increasing context-switching but exposing CLI design issues earlier per-wave. Opus's pattern matches mechanism-then-surface engineering discipline; Haiku's matches feature-vertical-slice discipline.

### 7. **Integration-Points Documentation Depth**
- **Opus:** Every milestone includes an explicit "Integration Points" table with artifact, type, wiring status, owning milestone, and consumers. Includes cross-milestone CI rules (merge-boundary CI guard in M8, `recipe_name → REGISTRY` binding in M3).
- **Haiku:** Integration Points tables present but lighter — fewer downstream-consumer rows, no explicit CI-guard wiring callouts.
- **Impact:** Opus's depth supports better cross-team coordination and PR-review checklists. Haiku's lighter touch may rely more on conventions/memory.

### 8. **AC-Coverage Explicitness Per Milestone**
- **Opus:** Embeds AC-001 through AC-017 as line items within milestones (e.g., AC-001/AC-002/AC-004 in M1; AC-005/AC-011 in M5; AC-009 in M6; AC-015/AC-016/AC-017 in M7). 17 ACs traceably mapped.
- **Haiku:** ACs appear sporadically as milestone items (AC-005 in M4; AC-007 in M5; AC-009 in M6; AC-002 in M9) — many AC numbers never surface as line items.
- **Impact:** Opus is more auditable against spec acceptance criteria; reviewer can confirm every AC has an owning milestone+task. Haiku's pattern assumes ACs are implicitly satisfied by their parent FR/NFR items, which is true but harder to verify.

### 9. **Decision Summary Framing**
- **Opus:** 7 decisions covering orchestrator home, concurrency engine, policy curation, merge semantics, resume source-of-truth, injection-guard policy, TUI default.
- **Haiku:** 6 decisions — same topics minus "orchestrator home" but adding "transport protocol pluggable with OpenAI-compat reference."
- **Impact:** Substantive parity; both fairly enumerate alternatives. Haiku's transport-decision callout is slightly more informative for backend-team alignment.

## Areas Where One Variant Is Clearly Stronger

**Opus is stronger on:**
- **Risk buffering** — 16-week schedule + 3-week CLI surface milestone realistically accommodates the highest-risk segments (M5 dispatch, M6 merge boundary, M7 resume+detached).
- **Sequencing discipline** — Protocol-before-policy ordering (M2 recipes before M3 lenses) eliminates late-stage recipe rework.
- **AC traceability** — Every AC-NNN surfaces as a line item; easier reviewer audit.
- **Integration-Points depth** — explicit CI guards (merge-boundary, `validate-lenses`), downstream-consumer mapping per milestone.
- **OQ resolution timing** — pushes OQ-007/OQ-008 to M1 to prevent data-model churn.

**Haiku is stronger on:**
- **Timeline compression** — 12 weeks vs 16 saves 4 weeks if execution lands clean.
- **Vertical-slice feature flow** — CLI flags arrive with their feature milestone (e.g., `--auto-inject-guard` in M3 with preflight), reducing "feature half-built across milestones" feel.
- **Cleaner M1 scope** — combining foundation+data models into M1 (without forcing transport/recipe split) gives a tighter first milestone.
- **Field-level data-model documentation** — DM-001..DM-010 each spelled out with explicit field counts and types as line-item bullets, easier for IDE-driven implementation.

## Areas Requiring Debate to Resolve

1. **Timeline realism (12 vs 16 weeks)** — Is the 4-week compression achievable, or does it under-buffer M7 (CLI/observability/resume/detached) which Opus rightly identifies as the largest surface? Debate needs an honest LOC + integration-points estimate for M7 to settle.

2. **Recipe placement (M2 foundation vs M5 normalize)** — Settling this requires deciding whether recipe-protocol stability is a prerequisite for lens-registry validation (Opus position) or whether recipes can co-evolve with their Wave 2 consumer (Haiku position). The `bare_review_v1` parity risk (R-08) argues for Opus's earlier-is-safer placement.

3. **OQ-007/OQ-008 resolution timing (M1 vs M2/M3)** — If `status_policy` and `WorkerSpec` are stable abstractions tolerant of both warn-and-STOP semantics, Haiku's deferral is acceptable. If field-level churn is likely, Opus's M1-resolution is safer. Architect call.

4. **Detached mode split (M4+M7 vs all-in-M7)** — Haiku's M4 `tmux.py` placement only makes sense if detached mode is dispatch infrastructure rather than CLI lifecycle. Most engineering teams would treat the whole lifecycle as M7 (Opus position); Haiku's split should be justified or merged.

5. **CLI surface granularity (concentrated M7 vs distributed across waves)** — Trade-off between mechanism-first engineering (Opus) and vertical-slice delivery (Haiku). Team structure and review-bandwidth constraints determine winner; neither is universally correct.

6. **Backwards-compat flag scope** — Both reference `--auto-inject-guard` but neither defines a sunset date for the migration window. Debate should produce a fixed deprecation timeline.
