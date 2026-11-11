# Hypothesis: #478's "global" ask cannot work for BMAD as built, because every BMAD skill reads its config from `{project-root}/_bmad/`, and "create directories on first use" is a per-project bootstrap that the spec lists as a non-goal; delivering it means superseding that non-goal

**Agent**: system-architect (lens only; dispatched as troubleshoot-analyst, read-only)
**Tier**: 2
**Timestamp**: 2026-11-07T07:43:28Z
**Cause class**: Other (request conflicts with documented scope; structural constraint in the BMAD project-root contract)
**Claim class**: `doc_contract`
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: conflicts (the proposed fix lies outside `SPEC.md:141,174` and `ARCHITECTURE-SPINE.md:228`; it does not contradict the literal text of OD-1 but may contradict its intent if the trigger is user-level)
runs-in=unknown

## Claim

BMAD is per-project by architecture, not only by decision. `.claude/skills/bmad-help/SKILL.md:25-26` reads `{project-root}/_bmad/_config/bmad-help.csv` and runs `{project-root}/_bmad/scripts/resolve_config.py`, so even user-level skills would fail in any project without its own `_bmad/`. The three asks reduce to one design: a project-scoped bootstrap that runs on first use. Today boot configures only the seed repo (`bmad/install.sh:21-26`), and `SPEC.md:141,174` calls later clones and worktrees a non-goal and a scope expansion. Ponytail is a different mechanism (user-scope plugin) and is not touched by this card.

## Evidence

- E1 `.claude/skills/bmad-help/SKILL.md:25-26`: catalogue and config resolver live under `{project-root}/_bmad/`. Whether `{project-root}` resolves to the cwd at runtime is UNVERIFIED.
- E2 `catalogue/bmad/install.sh:21-26,42`: only target is the seed path; only install call is `bmad install --yes --directory "${D}" --modules bmm --tools claude-code ...`. `manifest.yaml:12-14` manual command for any other repo. behaviour-definition: row 2.
- E3 `owner-decisions.md:5` (OD-1); `ARCHITECTURE-SPINE.md:105` (AD-5 step 1: no path means exit 0 and configure nothing), `:141` (AD-7: bmad is the only reader), `:228` ("BMad in Orca worktrees or later clones ... a scope expansion").
- E4 `test-57-catalogue-configure.sh:446-452` and `test-startup-boot.sh:2209-2224` pin the boot-time path (seedless: writes nothing, `Installed-not-Configured`). `test-19` mentions bmad only in comments/one first_token check; `test-46` has a bmad hook at lines 835-849, 905, 922-947 (grep only).
- E5 user-level skills load in all projects: behaviour-definition: row 3.
- Producer-citation check: skipped (producers.md header-only).

## Proposed Fix

Two designs were considered.

- Design 1 (consistent with current decisions): documentation only, which is Tier 1's fix. Delivers none of the three asks.
- Design 2 (chosen, gated on the owner superseding the non-goal): add a project-scoped first-use bootstrap. Boot behaviour stays unchanged. The `bmad` slug also writes one small user-level skill `~/.claude/skills/bmad-init/SKILL.md` that tells Claude to run AD-5 steps 2-6 against `git rev-parse --show-toplevel` when `_bmad/` is missing (add `info/exclude` lines, run `bmad install ... --directory <root>`, check `git status` unchanged). No BMAD content lives at user level; only the project gets `_bmad/` and `.claude/skills/bmad-*`, so OD-1's "per project" holds. The owner must still confirm a user-level shim is not "user level".

Gate: nothing is built until the owner supersedes the non-goal; if the owner declines, withdraw this card and ship Design 1.

Files that would change:
- Specs/docs: `_bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md:141,174` (non-goal to new FR); `ARCHITECTURE-SPINE.md` (AD-5 step 1, the `:228` deferral, a new AD); `owner-decisions.md:5` (clarifying line).
- Code: `catalogue/bmad/install.sh` (write the skill file outside the seed branch); `catalogue/bmad/manifest.yaml:8-20` (welcome text).
- Tests: `test-57` (new cases; keep `:450,452` valid); `test-startup-boot.sh:2209-2224`, `test-19`, `test-46` no change expected (inference from grep only).

Test to prove it: a new test-57 case where a fixture HOME has no seed and the skill file exists after `install.sh`, with the existing "writes nothing to any repo" assertions still passing. The skill's own behaviour needs a live-boot check (UNVERIFIED).

## Confidence

Self-reported confidence: 0.45 (capped at 0.5: static evidence, `runs-in=unknown`, skill-execution behaviour not defined by a fetched artifact).

Per-dimension self-assessment:
- Evidence grounding: 1.0.
- Runtime check: 0.5 (doc_contract with source_static; nothing executed).
- Symptom coverage: 0.5 (BMAD asks only; Ponytail out of scope).
- Reproducibility fit: 0.5.
- Fix directness: 0.5 (gated on an owner decision and an unverified trigger).
- Domain coherence: 0.5 (spec, installer, Claude Code skill discovery).

## Risks

- A user-level skill file may be removed by `superclaude install --force` (not read; UNVERIFIED).
- An LLM-run bootstrap is not deterministic, so the AD-5 `git status` check could be skipped; a repo script called by the skill would be safer but adds a PATH/image-path question (UNVERIFIED).
- The bootstrap would write into arbitrary repos, exactly what the `SPEC.md:141` non-goal avoided.

## If I'm wrong, it's probably because...

`{project-root}` resolves such that user-level BMAD skills work without a per-project `_bmad/`, or `global_target_dir` is functional in 6.9.0, which would make a true user-level install possible and Design 2 unnecessary.

## Falsification standard

Falsified if a captured run of `bmad install --directory "$HOME" --tools claude-code` (or any `global_target_dir` path) produces `~/.claude/skills/bmad-*` and `bmad-help` then succeeds in a repo with no `_bmad/`; also falsified by an owner statement that `SPEC.md:141,174` stands (withdraws Design 2).

## Evidence classification

- **Claim class**: doc_contract.
- **Evidence class**: source_static.
- **Runtime check performed?**: no.
- **If REFUTE verdict, coverage statement**: Not applicable (AFFIRM).

## Alternatives considered

- Design 1 (docs only): consistent with all decisions, leaves #478 open.
- `bmad install --directory "$HOME"` as a user-level install: rejected (conflicts with OD-1 and per-project `_bmad/`; whether it works is UNVERIFIED).
- A user-level SessionStart hook that installs into every repo: rejected (invasive; touches settings.json which AD-6 `ARCHITECTURE-SPINE.md:128-129` protects).

## Grounding gaps

- Claude Code skill execution of shell commands from a user-level skill is not defined by a fetched artifact.
- Not read this pass: `gap-closure SPEC.md:77`, `startup.sh`; test-19 and test-46 by grep only.
- Ponytail half and the reporter's profile/environment unobserved.
- Diagnosability verdict: partial (diagnosability-context.md).
