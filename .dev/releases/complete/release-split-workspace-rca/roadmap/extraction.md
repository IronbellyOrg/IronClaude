---
artifact_type: extraction
spec_source: .dev/releases/current/release-split-workspace-rca/merged-thesis.md
generated: 2026-05-13
generator: sc-roadmap-protocol v2.0.0
total_requirements: 14
functional_requirements: 11
nonfunctional_requirements: 3
acceptance_criteria: 5
risks_inherited: 5
complexity_score: 0.60
complexity_class: MEDIUM
primary_persona: devops
consulting_personas: [security, architect, refactorer, scribe]
domain_distribution:
  devops: 0.55
  security: 0.20
  architect: 0.15
  scribe: 0.10
compliance_tier: STANDARD
adversarial_predecessor: true
pipeline_diagnostics:
  prereq_checks:
    spec_file_exists: true
    spec_file_nonempty: true
    output_dir_writable: true
    output_collision: false
    adversarial_skill_present: not_required
  fallback_activated: false
validation_score: 0.875
validation_status: PASS
---

# Extraction — Release-Split Workspace Misplacement Remediation

## Spec Provenance

Source: `.dev/releases/current/release-split-workspace-rca/merged-thesis.md`
Predecessor analyses (already adversarially merged):
- `rca-1-skill-spec.md` (defensive guard subset, weighted 0.396)
- `rca-2-eval-harness.md` (proximate cause, base variant, weighted 0.870)
- `rca-3-naming-convention.md` (systemic cause, weighted 0.752)
- `adversarial/debate-transcript.md`, `adversarial/invariant-probe.md`, `adversarial/merge-log.md`

The spec is itself the output of a structured adversarial debate (65/35 RC/Solution weighting). No re-derivation of cause attribution needed; this extraction maps the 11 layered actions to roadmap requirements.

## Functional Requirements

| ID | Layer | Description | Target File(s) | Effort |
|---|---|---|---|---|
| FR-L1.1 | L1 | PreToolUse hook rejecting `Write`/`Edit` to `.claude/skills/*-workspace/**` and rewriting to `.dev/eval-workspaces/<skill-name>/<remainder>` | `.claude/settings.json` | S |
| FR-L1.2 | L1 | Project CLAUDE.md addendum overriding skill-creator's "sibling to skill directory" convention; cites *behavior* not file path | `/config/workspace/IronClaude/CLAUDE.md` | S |
| FR-L1.3 | L1 | `make eval-skill SKILL=<name>` target pre-creating `.dev/eval-workspaces/<name>/` and printing absolute path | `Makefile` | S |
| FR-L2.1 | L2 | Replace `verify-sync`'s misleading `"MISSING in src/superclaude/skills/: <name> (not distributable!)"` with context-aware variant when missing entry has no SKILL.md | `Makefile:179-187` | S |
| FR-L2.2 | L2 | Wire `make verify-sync` and `make lint-architecture` into `quick-check.yml` (closes INV-002 HIGH) | `.github/workflows/quick-check.yml` | S |
| FR-L2.3 | L2 | Add `*-workspace` blocklist pattern to verify-sync or lint-architecture with explicit redirect message | `Makefile` | S |
| FR-L2.4 | L2 | `.dev/README.md` documenting all 11 subdirectories + explicit rule: workspaces, fixtures, harness code, iteration outputs go under `.dev/`, never under `.claude/skills/` | `.dev/README.md` (new) | M |
| FR-L2.5 | L2 | Repair broken `PLANNING.md`/`TASK.md`/`KNOWLEDGE.md` pointers in project CLAUDE.md (lines 51-53, 225-227) | `CLAUDE.md` | S |
| FR-L2.6 | L2 | `.gitignore` entry `.claude/skills/*-workspace/` | `.gitignore` | S |
| FR-L3.1 | L3 | Output-path policy guard in `sc-release-split-protocol/SKILL.md` Prerequisites step 2a refusing `.claude/skills/...`, `.claude/agents/...`, `.claude/commands/...` outputs; document in command Options table | `src/superclaude/skills/sc-release-split-protocol/SKILL.md`, `src/superclaude/commands/release-split.md` | S |
| FR-L3.2 | L3 | (Optional) Same guard applied to `sc-adversarial-protocol` and `sc-cleanup-audit-protocol` | Two SKILL.md files | M |

## Non-Functional Requirements

| ID | Description | Maps to Risk |
|---|---|---|
| NFR-1 | PreToolUse hook must NOT block legitimate writes inside `.claude/skills/<skill>/` (i.e., real skill files) | R-01 |
| NFR-2 | Added CI steps must not materially lengthen PR time (`verify-sync` runs in seconds) | R-02 |
| NFR-3 | Backward compatible — existing relocated workspace at `.dev/eval-workspaces/sc-release-split-protocol/` continues to work with `aggregate_benchmark.py` and `generate_review.py` | AC5 |

## Acceptance Criteria (verbatim from merged-thesis §"Acceptance Criteria")

- **AC1** — L1 fires first: Claude reads project CLAUDE.md, sees override (L1.2), writes to `.dev/eval-workspaces/<name>/` directly. If Claude ignores the override, the PreToolUse hook (L1.1) blocks the write and emits a redirect-pointing error.
- **AC2** — L2 fires if L1 is bypassed (e.g., fresh clone without hooks installed): a `.claude/skills/<X>-workspace/` directory without SKILL.md is flagged by `make verify-sync` (L2.1) with the correct error message, and CI (L2.2) blocks the PR.
- **AC3** — L3 fires if a different code path tries to route a `.claude/skills/...` value through `sc-release-split-protocol --output`: the skill itself refuses (L3.1) before writing.
- **AC4** — Documentation is internally consistent: project CLAUDE.md references resolve (L2.5), `.dev/README.md` exists and names the rule (L2.4), convention is findable by a new contributor without tribal knowledge.
- **AC5** — No regression in the relocated workspace at `.dev/eval-workspaces/sc-release-split-protocol/`.

## Risk Register (inherited from merged-thesis §"Risk Register")

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | PreToolUse hook breaks legitimate `.claude/skills/<skill>/` writes | Medium | High | Pattern must match `*-workspace/**` precisely; positive + negative test cases |
| R-02 | CI wiring lengthens PR time | Low | Low | `verify-sync` runs in seconds; concurrent with existing checks |
| R-03 | New `.dev/eval-workspaces/` convention diverges from prior art (`v2.15-cli-portify`) | Resolved | Medium | L2.4 documents the rule; forward-only |
| R-04 | skill-creator plugin updates upstream → L167 reference goes stale | Low | Low | L1.2 cites behavior not file path |
| R-05 | Future skill *should* legitimately have a workspace inside `.claude/` | Very Low | Low | Hook + Makefile checks emit override-able errors |

## Outstanding Invariant from Round 2.5

- **INV-002 (HIGH, UNADDRESSED in merged-thesis):** `make verify-sync` must run in CI before merge. Drives Priority-0 placement of M2 (FR-L2.2).

## Domain Analysis

- **devops** (55%): CI workflow editing, Makefile targets, hook configuration, settings.json
- **security** (20%): hook precision (R-01), skill output-path guard (FR-L3.1), enforcement-vs-Claude-obedience layering
- **architect** (15%): governance design (.dev/ convention, dependency layering, escape hatches via overridable errors per R-05)
- **scribe** (10%): `.dev/README.md`, CLAUDE.md addendum, pointer repair

## Complexity Scoring (5-factor)

| Factor | Contribution | Note |
|---|---|---|
| Requirement count (11+3+5 = 19 items) | +0.20 | Above LIGHT threshold |
| Cross-cutting touch (6 file classes: settings.json, Makefile, CI yml, CLAUDE.md, skills, gitignore) | +0.20 | Wide blast radius |
| Risk diversity (1 medium, 4 low/very-low) | +0.10 | R-01 dominant |
| Acceptance specificity (AC1–AC5 already concrete) | −0.05 | Reduces ambiguity |
| Adversarial precedent (debate already converged) | −0.05 | No re-litigation needed |
| **Total** | **0.60** | **MEDIUM** |

## Persona Activation

- **Primary**: devops (above threshold @ 0.55)
- **Consulting**: security (R-01 mitigation review), architect (governance signoff on .dev/ rule), refactorer (Makefile/CLAUDE.md cleanup), scribe (.dev/README.md authorship)

## Edge Cases Identified

- 0 actionable requirements → N/A (11 extracted)
- Spec >500 lines → N/A (merged-thesis is 166 lines)
- Malformed YAML in spec → N/A (no frontmatter to parse)
- Empty file → N/A
- Adversarial mode → not active (single-spec invocation)
