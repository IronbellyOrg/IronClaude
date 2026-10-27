# D-0011 — Notes & Skip Rationale

**Task:** T04.02
**Status:** Done (with one in-scope skill exempt by design)

## Per-Skill Outcome

### sc-adversarial-protocol — Guard applied

- **`--output` exposure:** Yes. Documented in the Configurable Parameters (FR-003) table as `Output dir | --output | Auto-derived | Any path | Where artifacts are written`. Multiple downstream sections write artifacts under the resolved `<output-dir>/` (variant files, adversarial sub-artifacts, pipeline phase outputs).
- **Edits applied:**
  1. New `## Prerequisites (before Step 1)` section inserted between `## Required Input` and `## Triggers`. The section enumerates three behavioural instructions, with the policy guard as instruction 1 (matching the priority ordering used in `sc-release-split-protocol` step 2a).
  2. New `output_path_forbidden:` entry placed at the top of the `error_handling:` YAML block, mirroring the row added by T04.01 to `sc-release-split-protocol`.
- **Sync propagation:** Verified via `make sync-dev` and `make verify-sync`. Both `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and `.claude/skills/sc-adversarial-protocol/SKILL.md` contain identical guard text.

### sc-cleanup-audit-protocol — Exempt

- **`--output` exposure:** No. The skill's `argument-hint` accepts `[target-path] [--pass …] [--batch-size N] [--focus …]` only. There is no `--output` flag.
- **Output destination:** Hardcoded to `.claude-audit/`. Repeated in three places in the SKILL.md: "Initialize output directory at `.claude-audit/`", "Report generation restricted to `.claude-audit/` output directory", and "Audit reports written to `.claude-audit/` directory only".
- **Why exempt:** The output-path policy guard refuses `--output` values under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`. Since `sc-cleanup-audit-protocol` has no user-controllable `--output`, there is no value to inspect and no surface that could route audit artifacts into a reserved distributable directory. The hardcoded `.claude-audit/` destination is outside the three forbidden prefixes and is already documented as the canonical sink for this skill.
- **Implication for defense-in-depth:** Even if a future change ever wired this skill to accept `--output`, the L1 hook (`reject-workspace-writes.sh`) and L2 CI gate (`make verify-sync`) would still block any write under the reserved prefixes. The skill-level guard would only need to be added if the skill grew that flag — out of scope for T04.02 per the task's "if a skill does not, document the skip" clause.

## Cross-Cutting Notes

- The refusal clause inserted into `sc-adversarial-protocol` is textually consistent with T04.01's clause: same three forbidden prefixes, same redirect destination, same pointer to `.dev/README.md`. Only the example sub-paths were swapped (`.dev/eval-workspaces/<skill-name>/` paired with `.dev/releases/current/<release-name>/` rather than vice versa) to match the skill's typical workspace use case.
- `sc-release-split-protocol` (T04.01) and `sc-adversarial-protocol` (T04.02) now have parity on this policy. The two skills are commonly chained — `sc-release-split-protocol` invokes `sc-adversarial-protocol` for Mode B variant generation — so the guard fires regardless of entry point.
- This task is marked optional in the roadmap with the `defer-pending-capacity` flag. It is being completed within Phase 4 since the changes are small and reduce future drift risk. T04.03 will record this as `T04.02 status: done`.

## Validation Caveat (R-04 mitigation)

Per phase-4 R-04 guidance, this notes file deliberately keeps file-path citations behavioural rather than positional: it cites the *presence* of the `## Prerequisites (before Step 1)` heading and the `output_path_forbidden` entry, both of which can be grep-located by name regardless of position. The policy itself does not depend on line numbers — only on those two named anchors.
