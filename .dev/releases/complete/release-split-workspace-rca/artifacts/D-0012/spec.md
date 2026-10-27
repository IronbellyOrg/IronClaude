# D-0012 — AC1 Acceptance Test Spec

**Task:** T05.01 — AC1 test: skill-creator + M1-M3 yields correct destination or hook redirect
**Roadmap Item:** R-012
**Acceptance Criterion:** AC1
**Probe name:** `__ac1_probe__`

## Acceptable outcomes (either satisfies AC1)

- **Outcome A** — Addendum-only path: Claude reads the CLAUDE.md addendum (lines 108-116) and writes the workspace directly to `.dev/eval-workspaces/<name>/`. No PreToolUse hook fire.
- **Outcome B** — Hook-redirect path: Claude attempts to write to `.claude/skills/<name>-workspace/`; the PreToolUse hook (`reject-workspace-writes.sh`) rejects with exit 2 + a redirect message naming `.dev/eval-workspaces/<name>/`; Claude retries against the correct path; retry succeeds.

## Hard acceptance gates (from phase-5-tasklist.md §T05.01)

1. Final workspace directory exists at `.dev/eval-workspaces/__ac1_probe__/` AND does NOT exist at `.claude/skills/__ac1_probe__-workspace/`.
2. Session transcript shows either Outcome A (no hook fire) or Outcome B (hook fired with redirect message).
3. If Outcome B, the hook message contains the substring `.dev/eval-workspaces/`.
4. Transcript captured in `evidence.md`.

## Prerequisites (M1-M3 must be landed)

- **M1 (T01.01-T01.03)** — CLAUDE.md addendum + doc pointer repair: verified via `grep -n "skill-creator\|eval-workspaces\|sibling-workspace" CLAUDE.md` returning the four-paragraph block at lines 110-116.
- **M2 (T02.01-T02.03)** — sync guardrails: `.gitignore` matches `.claude/skills/*-workspace/` (line 205); Make/lint targets and CI workflow present (validated by T05.02).
- **M3 (T03.01-T03.03)** — PreToolUse hook: `.claude/hooks/reject-workspace-writes.sh` installed and registered in `.claude/settings.json` PreToolUse:Write|Edit.
