# Input Resolution (Wave 0)

Reference for resolving `/sc:reflect` invocation inputs into a concrete `(mode, tier-routing, output-path)` triple. Consumed by Wave 0 (steps 0.1, 0.2, 0.5) of the reflect protocol. Source of truth: `merged-requirements.md` §3.1–§3.4 and §4.0 step 0.5.

## Flag enumeration

The skill accepts 20 flags. Semantics:

- `--mode pre | post` — Explicit use-case selector. RECOMMENDED for non-interactive callers; eliminates auto-detect ambiguity. Any value other than `pre` or `post` is a hard STOP (see §3.2 rule 1).
- `--spec <path>` — Driving spec/PRD/objectives document. Required for UC-1 (pre); recommended for UC-2 (post).
- `--tasklist <path>` — Tasklist file. Required for UC-2; recommended for UC-1 if a tasklist already exists.
- `--diff <ref-or-path>` — Git ref (e.g., `HEAD~1..HEAD`, branch name) or path to a diff file. Required for UC-2.
- `--commit-range <ref-range>` — Alternative to `--diff` for resolving a post-execution diff via git.
- `--scope <path>` — Narrowing scope. When `--scope` resolves to a directory whose tracked files overlap `git diff --name-only HEAD~1..HEAD`, mode auto-detects to UC-2.
- `--task-log <path>` — Task execution log. Optional, UC-2 only.
- `--depth quick | standard | deep` — Tier-1-only / Tier-1-then-rubric / force-Tier-2. Interacts with the rubric in §5.
- `--tier 1 | 2 | auto` — Explicit tier pin; overrides the rubric. `auto` is default.
- `--reviewers N` — Number of Tier 2 reviewers (2–3). Default 3, clamped by `--depth`.
- `--output <dir>` — Output directory. Default `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/`. Must not resolve under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (CLAUDE.md ABSOLUTE RULE).
- `--coverage-floor <float>` — Optional override of the T1 coverage stop floor. Default 0.90; high-safety profile may set to 0.95.
- `--no-mcp` — Debug only; auto-warns. Skips MCP-backed grounding.
- `--no-evidence-validator` — Debug only; auto-warns. Skips the Wave 5 evidence-validator gate.
- `--remediate` — Offer Tier 3 remediation handoff.
- `--budget-remaining <int>` (P5) — Caller-side budget hint (typically `TurnLedger.available()` from a sprint context). When provided, reflect cross-checks against the §15 cost profile and may auto-degrade tier; emits `budget_forced_tier_downgrade: true` in the contract when this happens. See §4.0 step 0.9.
- `--no-promote` — Promotion-gate flag (UC-2 only, see §14.5). Suppresses Wave 7 promotion. Default is *default-on*: when the §14.5.2 strict gate passes, the validated work-unit folder moves to its `done` destination.
- `--promote-anyway` — Promotion-gate flag. Overrides `status: partial` gate condition (all other 7 conditions still apply). No effect on `status: failed`.
- `--promote-dry-run` — Promotion-gate flag. Prints the `mv` command + gate evaluation; performs no mutation.
- `--promote-mode auto | task | sprint-release | none` — Promotion-gate flag. Forces a specific promotion adapter or disables selection. Default `auto`.
- `--promote-resume <checkpoint-path>` — Promotion-gate flag. Resumes an interrupted cross-filesystem promotion from a `promotion-checkpoint.yaml`. See §14.5.5 for partial-state recovery semantics.

## 6-rule mode selection

Applied in order; **first match wins**:

1. **`--mode pre | post`** present → use literal value. STOP if value is anything else.
2. **`--diff` OR `--commit-range`** flag present → **UC-2 (post)**.
3. **`--scope`** resolves to a directory whose tracked files overlap `git diff --name-only HEAD~1..HEAD` → **UC-2 (post)**.
4. Input arguments include both a `--tasklist` file AND a completed-work artifact directory (`.dev/tasks/done/`, `.dev/releases/current/results/`, etc.) → **UC-2 (post)**.
5. `--spec` AND `--tasklist` present with no diff / no done-marker artifacts → **UC-1 (pre)**. If only `--spec` is present → UC-1 with a coverage-only pass.
6. None of the above resolve → **STOP** with: `"Reflect requires --mode pre|post OR a resolvable input combination. See refs/input-resolution.md."`

Worked examples:

- `/sc:reflect --mode post --diff HEAD~3..HEAD` → Rule 1 matches first → UC-2. Rule 2 would have also matched but rule 1 wins.
- `/sc:reflect --diff HEAD~1..HEAD --tasklist t.md` → Rule 1 misses (no `--mode`); rule 2 matches → UC-2.
- `/sc:reflect --scope src/foo` where `src/foo/bar.py` appears in `git diff --name-only HEAD~1..HEAD` → Rule 3 matches → UC-2.
- `/sc:reflect --tasklist .dev/tasks/to-do/TASK-X/tasklist.md --spec spec.md` with `.dev/tasks/done/TASK-X/` existing → Rule 4 matches → UC-2.
- `/sc:reflect --spec spec.md --tasklist t.md` (clean tree) → Rules 1–4 miss; rule 5 matches → UC-1.
- `/sc:reflect --spec spec.md` alone → Rule 5 partial: UC-1 with coverage-only pass.
- `/sc:reflect` with no arguments → All rules miss; rule 6 STOP.

## STOP conditions

Hard-STOP cases that prevent invocation (verbatim from §3.3):

- Neither `--spec`, `--tasklist`, nor `--diff` provided.
- `--mode pre` with no `--spec` (pre-execution reflection has nothing to reflect against).
- `--mode post` with no `--diff` AND no `--task-log` (post-execution reflection has no completed work to audit).
- `--depth deep` with under-specified input (e.g., 1-line spec, empty tasklist).
- `--output` resolves under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (CLAUDE.md ABSOLUTE RULE — distributable paths are not output sinks).

Additional STOP from §4.0 step 0.5 (env routing): zero aliases resolved + `--tier 2` explicit → STOP (see Env routing table below).

## Environment

The skill resolves model aliases from environment at Wave 0 step 0.5:

- `ANTHROPIC_DEFAULT_OPUS_MODEL`
- `ANTHROPIC_DEFAULT_SONNET_MODEL`
- `ANTHROPIC_DEFAULT_HAIKU_MODEL`

Aliases drive Tier 2 reviewer composition (see §7.1 and the alias-routing table below). Missing aliases **do not abort the skill** in the general case; they degrade reviewer topology per the routing table. The skill emits `degraded_components: ["env-aliases"]` into the audit log and surfaces a WARN to the user when running with fewer than 3 distinct classes. The full degraded-mode envelope (env, MCPs, agents) is documented in §14.

MCP availability is also probed at Wave 0:

- `sc-adversarial-protocol` installation probe (step 0.3) — required for Wave 4 adversarial merge; F1/F2/F3 fallback per Change #15 if absent.
- Serena project activation + memory hydrate (step 0.7).
- Auggie + serena availability for Wave 1A grounding chain.

## Env routing table

Step 0.5 routes Tier 2 reviewer count based on (resolved-alias count) × (`--tier` flag). Exact 4-row table from spec §4.0 step 0.5:

| Aliases resolved | `--tier` flag | Routing | Telemetry |
|------------------|---------------|---------|-----------|
| 0 | (any except `--tier 2`) | T1-only path; WARN "T2 requires ≥1 model class"; degraded | `degraded_components: ["env-aliases"]` |
| 0 | `--tier 2` explicit override | **STOP** with explicit message: `"--tier 2 requires ≥1 alias resolved (zero aliases available — set ANTHROPIC_DEFAULT_*_MODEL env vars or omit --tier 2)"` | `degraded_components: ["env-aliases"]`, `stop_reason: "zero-aliases-tier2-conflict"` |
| 1 | (any) | T1-only path; WARN "T2 requires ≥2 model classes" | `t2_model_class_diversity: degraded` |
| 2 | (any) | T2 with 2 reviewers (degraded) | `t2_model_class_diversity: degraded` |
| ≥3 | (any) | T2 with 3 reviewers (full diversity) | `t2_model_class_diversity: full` |

Grader assertion: `yaml_field` asserts `t2_model_class_diversity` is one of `{full, degraded}` when the skill ran to completion (non-STOP).

**Zero-aliases + `--tier 2` STOP rationale:** This row is the only case where alias-resolution itself can STOP the skill — every other zero/one-alias path degrades gracefully. The reasoning: `--tier 2` is a hard override per §5.1, but the rubric cannot satisfy it with zero model classes available; the conflict is irresolvable, so the skill MUST fail loudly rather than silently downgrade against an explicit user request.
