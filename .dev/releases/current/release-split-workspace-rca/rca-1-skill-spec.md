# RCA #1 — Skill-spec / output-path hypothesis

## Investigation method

Files read:
- `/config/workspace/IronClaude/src/superclaude/skills/sc-release-split-protocol/SKILL.md` (full, 447 lines)
- `/config/workspace/IronClaude/src/superclaude/skills/sc-release-split-protocol/refs/phase-templates.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-release-split-protocol/refs/adversarial-integration.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-release-split-protocol/refs/verification-protocol.md`
- `/config/workspace/IronClaude/src/superclaude/commands/release-split.md` (full, 131 lines)
- Comparison: `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` and `/config/workspace/IronClaude/src/superclaude/skills/sc-adversarial-protocol/SKILL.md` (output-path sections)
- Relocated workspace at `/config/workspace/IronClaude/.dev/eval-workspaces/sc-release-split-protocol/` (frontmatter and report files in `iteration-1/*/with_skill/outputs/`)

Searches performed (case-insensitive, recursive):
- `\.claude/skills` — across skill, refs, command file
- `workspace`, `-workspace`, `eval-`, `iteration-`, `fidelity-stress`, `trigger-eval` — across skill spec
- `output`, `--output`, `save`, `write to`, `directory`, `path` — across skill refs
- `release-split-protocol-workspace` — across `src/` and `.claude/`

## Findings (with evidence — file paths, line numbers, quotes)

### F1. The skill spec contains ZERO references to `.claude/skills/`, `-workspace/`, eval/iteration paths, or sibling-of-skill conventions.

A recursive grep across `src/superclaude/skills/sc-release-split-protocol/` for `(\.claude/skills|workspace|eval-|fidelity-stress|trigger-eval|iteration-)` returned no matches. The skill spec is silent on these patterns.

### F2. The default output path defined by the skill is `<spec-dir>/release-split/`, NOT a sibling of `.claude/skills/`.

`src/superclaude/commands/release-split.md:53`:
```
| `--output` | `-o` | No | `<spec-dir>/release-split/` | Output directory for all artifacts |
```

The skill SKILL.md uses the placeholder `<output>` consistently (e.g., `SKILL.md:171`, `SKILL.md:243`, `SKILL.md:298-299`, `SKILL.md:359`, `SKILL.md:391`) and never substitutes a `.claude/...` or `-workspace` literal. Example output references:
- `<output>/split-proposal.md` (line 171)
- `<output>/split-proposal-final.md` (line 243)
- `<output>/release-1-spec.md` (line 298)
- `<output>/release-split-report.md` (line 391)

### F3. The skill spec follows project conventions correctly — `<spec-dir>/release-split/`. Compare to siblings:

- `sc-cleanup-audit-protocol/SKILL.md:46`: writes to `.claude-audit/` (a project-root sibling, NOT under `.claude/skills/`).
- `sc-adversarial-protocol/SKILL.md:325,581-582`: `--output` default = "Auto-derived from input file directory" — same pattern as release-split.

None of the three skills instruct callers to write under `.claude/skills/`.

### F4. The `--output` example in the command file points to `.dev/`, reinforcing the "not under .claude" expectation.

`src/superclaude/commands/release-split.md:28-29`:
```
# With explicit output directory
/sc:release-split path/to/release-spec.md --output .dev/releases/current/v3.1/
```

The example explicitly uses `.dev/` — which is exactly where the workspace was supposed to live per the project's CLAUDE.md output-paths rule.

### F5. CRITICAL — In-tree breadcrumbs in the relocated workspace point back to `.claude/skills/sc-release-split-protocol-workspace/...`, but those paths come from the EVAL HARNESS, not the skill spec.

Evidence from generated artifacts (frontmatter and report bodies inside the eval scenarios):
- `iteration-1/learning-loop-observability/with_skill/outputs/release-1-spec.md:3`:
  ```
  parent-spec: .claude/skills/sc-release-split-protocol-workspace/evals/files/spec-learning-loop-observability.md
  ```
- `iteration-1/ambiguous-large-plugin-system/with_skill/outputs/release-2-spec.md:3-4`:
  ```
  parent-spec: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/evals/files/spec-ambiguous-plugin-system.md
  split-proposal: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/iteration-1/ambiguous-large-plugin-system/with_skill/outputs/split-proposal-final.md
  ```
- `iteration-1/nosplit-bugfix-hardening/with_skill/outputs/release-split-report.md:73,82`:
  ```
  All artifacts in: `/config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/iteration-1/nosplit-bugfix-hardening/with_skill/outputs/`
  output_dir: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/iteration-1/nosplit-bugfix-hardening/with_skill/outputs/
  ```

The skill *correctly* recorded the `--output` value it was given. The value passed in by the harness was `/config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/...`. The skill is downstream of the misnaming, not upstream.

### F6. `fidelity_checker.py` (the eval-harness Python script that lived in the workspace) is path-agnostic.

The script accepts `--outputs <path-to-split-output-dir>` as a CLI argument (`fidelity_checker.py:13-15`). It does not hardcode `.claude/skills/` either — that path is supplied by whoever invokes it.

### F7. `trigger-eval-set.json` and `evals/evals.json` contain no `.claude/skills` references.

Grep across these files returned zero matches — the path was injected by whatever orchestrator drove the eval, not by the eval data itself.

## Root cause (one-paragraph hypothesis)

The skill spec did NOT cause the misplacement. The skill (`sc-release-split-protocol/SKILL.md`) is properly parameterized via `--output <dir>` with a sane default of `<spec-dir>/release-split/`, contains no hardcoded paths, no `-workspace` convention, and no `.claude/skills/` references anywhere in the spec, refs, or command file. The skill faithfully wrote to whatever directory it was told to write to. The misplacement originated upstream in the eval orchestration: someone (or some harness/script — outside the skill's control) chose to create an eval workspace named `sc-release-split-protocol-workspace/` as a sibling of the skill itself under `.claude/skills/`, and then passed that path as `--output` to the skill. The breadcrumbs inside the workspace artifacts (which all explicitly cite `.claude/skills/sc-release-split-protocol-workspace/...`) are output from the skill faithfully echoing the input path it was given — they are evidence of, not a cause of, the misplacement.

## Confidence in this hypothesis (0.0 – 1.0, with reasoning)

**Confidence in the negative claim ("the skill spec did NOT cause this"): 0.95.**

Reasoning:
- Exhaustive grep across SKILL.md, all three refs files, and the command file produced zero matches for `.claude/skills`, `workspace`, `-workspace`, or sibling-of-skill conventions. Absence of evidence is unusually strong here because the search space is small (~600 total lines) and the search terms are exact strings that would have to be present to implicate the spec.
- The default in `release-split.md:53` is `<spec-dir>/release-split/`, which would have placed output under `.dev/releases/...` if the harness had passed `.dev/.../spec.md` as the spec file (which CLAUDE.md output-paths rule requires).
- The example at `release-split.md:29` explicitly uses `.dev/releases/current/v3.1/` — directly endorsing the project's intended output location.
- Comparison to two sibling skills confirms a consistent pattern: outputs go either to a project-root dir (`.claude-audit/`) or to a spec-dir-relative path. None point at `.claude/skills/`.

The 0.05 residual uncertainty covers: I did not exhaustively read every line of `phase-templates.md` and `verification-protocol.md` line-by-line — only grep + spot-reads. Any missed instruction would have to be very subtle to flip this, but I cannot rule it out at 1.00.

**Confidence that the cause lies elsewhere (eval harness / naming convention): 0.9.** The breadcrumbs in F5 strongly implicate an external harness or script that constructed the `.claude/skills/sc-release-split-protocol-workspace/` path and fed it to the skill. RCA #2 (eval harness) and RCA #3 (naming/governance) should pursue this.

## Refactor proposal

This hypothesis dead-ends as a *cause*, but defensive guardrails in the skill can prevent future recurrence regardless of what the harness does. Two concrete edits:

### Edit 1 — Add an output-path safety gate to Prerequisites (SKILL.md)

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-release-split-protocol/SKILL.md`

**Location**: Section 4, "Prerequisites (before Part 1)", Behavioral Instructions list (currently steps 1-6 around lines 122-133).

**Old (excerpt, line 124):**
```
2. Validate output directory is writable; create if needed.
```

**New:**
```
2. Validate output directory is writable; create if needed.
2a. **Output-path policy guard** (per project CLAUDE.md "output paths" rule):
    - If the resolved `--output` path begins with `.claude/skills/`, `.claude/agents/`, `.claude/commands/`, or any subpath thereof, STOP with:
      "Output directory '<path>' is inside the Claude framework tree (.claude/skills/...). Skill artifacts must not be written here. Use a path under `.dev/eval-workspaces/<skill-name>/`, `.dev/releases/...`, or `<spec-dir>/release-split/`. Re-invoke with --output set to a permitted location."
    - If the resolved path contains the segment `*-workspace/` AND lives outside `.dev/eval-workspaces/`, WARN: "Workspace-style output directory detected outside .dev/eval-workspaces/. Verify this is intentional."
```

### Edit 2 — Document the output-path policy explicitly in the command file

**File**: `/config/workspace/IronClaude/src/superclaude/commands/release-split.md`

**Location**: Options table (line 53).

**Old:**
```
| `--output` | `-o` | No | `<spec-dir>/release-split/` | Output directory for all artifacts |
```

**New:**
```
| `--output` | `-o` | No | `<spec-dir>/release-split/` | Output directory for all artifacts. MUST NOT be inside `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`. For eval/benchmark runs, use `.dev/eval-workspaces/sc-release-split-protocol/<run-id>/`. |
```

Add a new note section directly under the Options table:

```
## Output Path Policy

Per the project CLAUDE.md output-paths rule, this skill writes only to:
1. `<spec-dir>/release-split/` (default — alongside the source spec)
2. An explicit `--output` path the user specifies (e.g., `.dev/releases/current/<version>/`)
3. `.dev/eval-workspaces/sc-release-split-protocol/<run-id>/` (eval/benchmark harness convention)

The skill REFUSES `--output` paths under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`.
The Claude framework tree under `.claude/` is for installed components only — never for generated artifacts or eval data.
```

### Edit 3 (sibling-skill consistency, optional but recommended)

**Files**:
- `/config/workspace/IronClaude/src/superclaude/skills/sc-adversarial-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`

Add the same Prerequisites-level output-path guard so any skill that receives an `--output` value enforces the same policy. This puts the safety check at the *skill* level rather than relying on every caller (harness, command, user) to do the right thing.

After all three edits, run `make sync-dev` and `make verify-sync` per CLAUDE.md component-sync workflow.

## Acceptance criteria

1. **Static check**: Grep for `\.claude/skills` across `src/superclaude/skills/sc-release-split-protocol/` returns hits only inside the new policy guard text — never as an output destination.

2. **Behavioral check (positive)**: Invoke the skill with `--output .dev/eval-workspaces/sc-release-split-protocol/test-run/` — succeeds, artifacts land in `.dev/eval-workspaces/sc-release-split-protocol/test-run/`.

3. **Behavioral check (negative — the regression case)**: Invoke the skill with `--output .claude/skills/sc-release-split-protocol-workspace/` — STOPS with the policy-guard error message, no files written under `.claude/`.

4. **Default check**: Invoke without `--output` on a spec at `.dev/releases/current/v4.0/spec.md` — artifacts land at `.dev/releases/current/v4.0/release-split/`, never under `.claude/skills/`.

5. **Sibling-skill check (if Edit 3 applied)**: `sc-adversarial-protocol` and `sc-cleanup-audit-protocol` exhibit the same refusal behavior for `.claude/skills/...` outputs.

6. **Sync check**: `make verify-sync` reports `src/` and `.claude/` are in sync after the edits.

7. **Test addition**: A new unit test (e.g., `tests/unit/test_release_split_output_policy.py`) exercises the guard with both permitted and forbidden paths.

## Limitations / what this hypothesis can't explain

1. **Does not explain why the workspace was named `sc-release-split-protocol-workspace/` (skill-name + `-workspace` suffix) and placed adjacent to the skill.** That convention came from somewhere — either an eval harness script, a naming convention in `scripts/`, or operator habit. RCA #2 (eval harness/tooling) and RCA #3 (naming convention/governance) should investigate.

2. **Does not explain the specific path `/config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/...` recorded in the artifact frontmatter.** The skill recorded what it was given; whatever produced that path string is the actual culprit. Likely candidates the other agents should look at:
   - Any test/eval orchestrator script under `scripts/`, `tests/`, or `.dev/`
   - Workflow metrics or A/B testing harness referenced in CLAUDE.md ("scripts/ Analysis tools (workflow metrics, A/B testing)")
   - `fidelity_checker.py` callers (the script itself is path-agnostic, but the invoking harness may default to `.claude/skills/<skill>-workspace/`)

3. **Does not address whether other skills' eval data currently lives under `.claude/skills/`.** A repo-wide search for `.claude/skills/*-workspace/` directories should be performed by RCA #2 to detect any analogous artifacts that escaped the relocation.

4. **The defensive guard proposed above is a forward-looking fix only.** It will not retroactively detect or relocate already-misplaced artifacts. A separate one-time cleanup task is needed for any other affected skills.

**Recommendation**: Defer to RCA #2 (eval harness/tooling) for the actual root cause. The skill-spec angle is a dead end as a cause — but the proposed guardrail is still worth landing as defense-in-depth against the same class of bug recurring.
