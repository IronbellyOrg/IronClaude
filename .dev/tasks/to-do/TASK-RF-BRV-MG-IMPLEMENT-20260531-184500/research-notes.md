# Research Notes: Implement BRV-MG — `sc:pr-bot-validate` sibling skill

**Date:** 2026-05-31
**Scenario:** A (explicit — merged brainstorm proposal at `/config/workspace/Coder/.dev/brainstorm/pr-remediation-pipeline-integration-20260531/MERGED-PROPOSAL.md` is the concrete BUILD_REQUEST)
**Depth Tier:** Standard
**Track Count:** 1

---

## EXISTING_FILES

**Cross-repo binding (inherited from OVM cycle's research/04 — same decision applies here):**

- **Execution repo:** `/config/workspace/IronClaude/` (SuperClaude framework source-of-truth)
- **Planning repo:** `/config/workspace/Coder/` (this task file, the merged proposal, the research)

**Files to create (new in IronClaude):**

- `src/superclaude/skills/sc-pr-bot-validate-protocol/SKILL.md` — main sibling skill file (modeled on `sc-auggie-review-protocol/SKILL.md` per merged §3.1)
- `src/superclaude/skills/sc-pr-bot-validate-protocol/refs/bot-review-sources.yaml` — bot detection patterns (Augment Code, CodeRabbit, sourcery-ai, etc.)
- `src/superclaude/commands/sc/pr-bot-validate.md` — slash command file invoking the skill
- `.github/workflows/pr-bot-validate.yml` — GitHub Actions workflow that triggers on `pull_request_review` + `pull_request.synchronize` and gates merge via status check

**Files to amend (existing in IronClaude):**

- `src/superclaude/commands/sc/reflect.md` (NOT SKILL.md — see §AMBIGUITIES_FOR_USER for content-drift correction): add one entry to the existing `## Related Commands` section (line ~258) referencing the new `/sc:pr-bot-validate` sibling.

**Files to create in eval-workspace (new in IronClaude):**

- `.dev/eval-workspaces/sc-pr-bot-validate/` — entire new eval workspace mirroring `.dev/eval-workspaces/sc-reflect/` structure
- `.dev/eval-workspaces/sc-pr-bot-validate/cases/falsifier-suite/pr-bot-validation-mixed-buckets.yaml` — active iteration-1 falsifier per merged §8

**Source-of-truth file (READ-ONLY for executor):**

- `/config/workspace/Coder/.dev/brainstorm/pr-remediation-pipeline-integration-20260531/MERGED-PROPOSAL.md` — the authoritative BUILD_REQUEST (6,464 words, 9 §6 sections)

**Pattern source files (READ-ONLY templates for executor):**

- `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` — primary template (merged §3.1 explicitly cites)
- `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md` — pattern source for return contract shape, allowed-tools frontmatter, wave architecture
- `/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/` — pattern source for eval-workspace layout + grader.py + falsifier YAML shape
- `/config/workspace/IronClaude/.github/workflows/quick-check.yml` (or another workflow with `pull_request_review` trigger if present) — pattern source for GitHub Actions workflow

## PATTERNS_AND_CONVENTIONS

Same as OVM cycle (all decisions resolved in OVM's research/04-cross-repo-target-resolution.md, which sets the canonical pattern):

- **Source of truth = `src/superclaude/`.** Edit there first; mirror via `make sync-dev`; verify with `make verify-sync`.
- **`.github actions` validation only.** No one-off validation scripts. Acceptance criteria reference CI gates.
- **STRICT-tier:** new sibling skill creation + protocol-text impact → STRICT (prose marker, not frontmatter field).
- **MDTM template 02** required (multi-phase: skill scaffold → ref file → command file → workflow → eval workspace → falsifier → sync/verify → CI → self-validation).
- **Branch strategy:** executor branches off IronClaude `main` into `feat/brv-mg-pr-bot-validate-20260531`.

## GAPS_AND_QUESTIONS

1. **§16 Related Commands content drift** — RESOLVED via this research-notes write. See AMBIGUITIES_FOR_USER §1.
2. **GitHub workflow trigger event support** — Researcher 2 to verify `pull_request_review` event is in IronClaude's accepted triggers + that the runner (self-hosted? GitHub-hosted?) can post status checks.
3. **`sc-pr-bot-validate-protocol/__init__.py`** — Researcher 1 to check if the existing sc-reflect-protocol has an `__init__.py` (it does per OVM research/04) and whether the new skill needs one for parity.
4. **Eval workspace bootstrap** — Researcher 2 to confirm whether `.dev/eval-workspaces/sc-pr-bot-validate/` needs its own `grader.py` (copied/forked from sc-reflect's) or can share infrastructure.
5. **Cost profile mirroring** — merged §3.2 derives ~9 turns/PR from §15 T2-midpoint ÷ 6 parallel PRs ≈ 8.7; researchers should verify this lands inside the sibling skill's own §15 (or reflect's §15 is consulted by reference).

## RECOMMENDED_OUTPUTS

The builder produces ONE MDTM task file at:
`/config/workspace/Coder/.dev/tasks/to-do/TASK-RF-BRV-MG-IMPLEMENT-20260531-184500/TASK-RF-BRV-MG-IMPLEMENT-20260531-184500.md`

The task file's checklist drives the executor to produce these artifacts (in IronClaude source-of-truth `src/superclaude/`, then synced to `.claude/`):

- `src/superclaude/skills/sc-pr-bot-validate-protocol/SKILL.md` — new skill (multi-thousand-line per merged §3 mechanism)
- `src/superclaude/skills/sc-pr-bot-validate-protocol/refs/bot-review-sources.yaml` — new ref
- `src/superclaude/skills/sc-pr-bot-validate-protocol/__init__.py` — module init (parity with existing skills)
- `src/superclaude/commands/sc/pr-bot-validate.md` — new slash command
- `src/superclaude/commands/sc/reflect.md` — one-line addition to `## Related Commands` section
- `.github/workflows/pr-bot-validate.yml` — new workflow
- `.dev/eval-workspaces/sc-pr-bot-validate/cases/falsifier-suite/pr-bot-validation-mixed-buckets.yaml` — active falsifier
- `.dev/eval-workspaces/sc-pr-bot-validate/cases/falsifier-suite/README.md` — falsifier suite README
- `.dev/eval-workspaces/sc-pr-bot-validate/evals.json` — eval registry entry

After all edits: `make sync-dev` → `make verify-sync` → `make lint` → CI on PR.

## SUGGESTED_PHASES

Suggested 7-phase structure for the MDTM task:

1. **Preparation** — read MERGED-PROPOSAL.md; checkout IronClaude main; create feature branch `feat/brv-mg-pr-bot-validate-20260531`; capture pre-task SHA.
2. **Sibling skill scaffold** — create `sc-pr-bot-validate-protocol/SKILL.md` per merged §3.1 + §3.2 (4-wave pipeline) + §3.3 (status check) + §3.4 (workflow) + §3.5 (independent contract version) + §3.6 (ref file). Multi-thousand-line file; build incrementally per the task-builder's INCREMENTAL FILE WRITING protocol.
3. **Ref file + command file** — create `refs/bot-review-sources.yaml` with Augment Code / CodeRabbit / sourcery-ai / GitHub Copilot review / Greptile / codiumai-pr-agent patterns; create `commands/sc/pr-bot-validate.md` slash command.
4. **Reflect command file Related-Commands update** — one-line addition to `src/superclaude/commands/sc/reflect.md` `## Related Commands` section per merged Change 10 (CONTENT-DRIFT-CORRECTED location).
5. **GitHub workflow** — create `.github/workflows/pr-bot-validate.yml` per merged §3.4.
6. **Eval workspace + falsifier** — create `.dev/eval-workspaces/sc-pr-bot-validate/` tree; populate active falsifier YAML per merged §8.
7. **Sync + verify + self-validate + commit** — `make sync-dev` → `make verify-sync` → `make lint` → `Skill sc:reflect-protocol --mode post --diff <pre-task-ref>..HEAD --tasklist <this-task-file>` → commit on the feature branch.

Per-phase QA gates inserted after each. Estimated total: ~50-70 checklist items (skill scaffold phase dominates; multi-thousand-line file builds with many granular items).

## TEMPLATE_NOTES

- **Template 02 (Complex Task)** — required.
- **Compliance tier:** STRICT — sibling skill creation + protocol-text + cross-skill impact + new GitHub Actions workflow.
- **QA_GATE_REQUIREMENTS:** PER_PHASE.
- **VALIDATION_REQUIREMENTS:** `make sync-dev` + `make verify-sync` + `make lint` + post-task `Skill sc:reflect-protocol --mode post`.
- **TESTING_REQUIREMENTS:** The 1 active falsifier YAML IS the test; eval-workspace grader runs it via `make reflect-eval-quick` (or a new `make pr-bot-validate-eval-quick` if the eval-workspace bootstrap creates one).
- **EXECUTION_CONTEXT_REQUIREMENTS:** REQUIRED. Source areas: "sc-pr-bot-validate-protocol skill creation", "GitHub workflow + status check", "eval-workspace bootstrap". Key constraints: "Source-of-truth = IronClaude `src/superclaude/`, never edit `.claude/` directly"; "Reflect SKILL.md unchanged (zero amendments) — only the command file gets a Related-Commands cross-reference"; "PR-layer gate via `gh api .../statuses/<sha>` is distinct from OVM's work-unit-layer cond 10".

## AMBIGUITIES_FOR_USER

1. **§16 Related Commands content drift (RESOLVED).** The merged proposal Change 10 directs the executor to edit "`sc-reflect-protocol/SKILL.md` §16 Related Commands" — but the SKILL.md does NOT have a "Related Commands" section (its §16 is "Refs"). The actual `## Related Commands` section lives in the **command file** at `/config/.claude/commands/sc/reflect.md:258` (source-of-truth: `/config/workspace/IronClaude/src/superclaude/commands/sc/reflect.md`). The task file MUST instruct the executor to edit the command file, NOT the SKILL.md, for Change 10. Builder: do NOT propagate the merged proposal's incorrect "SKILL.md §16" location; use the corrected location.

2. **`pr_bot_validate_*` vs `pr_bot_validation_*` field prefix.** Merged proposal Change 1 explicitly renames A's `pr_bot_validation_*` to `pr_bot_validate_*` for sibling-skill namespace consistency. Builder: enforce the `pr_bot_validate_*` prefix in all field references; the merged proposal's body may still have some legacy `pr_bot_validation_*` strings — flag any to executor.

No other ambiguities. Cross-repo decision is canonical (per OVM research/04). All other research gaps are mechanical and resolvable by the researchers.
