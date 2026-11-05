# Documentation Context Card

**Generated**: 2026-11-04T16:46:09Z
**Wave**: 1.5
**Scope**: src/superclaude/hooks/scripts/block-bare-python.sh:206

## Release context
- **Release**: TASK-WF-implementIronbel-20261104-130647 (issue #357 plan; .dev/releases empty for this hook)
- **Artifacts**: .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md, .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/artifacts/amendments.md
- **Summary**: The plan defines the command word as the next word after assignments, keywords and wrappers; it does not mention `name()` function definitions or `{fd}` redirections. M-CEILINGS accepted "leading redirections" as a possible ceiling without naming {fd}.
- **Confidence**: 0.85

## Architectural docs consulted
- `src/superclaude/hooks/scripts/block-bare-python.sh` (header) — verdict: `current` — says redirections are tracked (line 27); neither defect is a listed ceiling; the generic false-positive note uses a heredoc example.
- `CHANGELOG.md` (#357 entry) — verdict: `current` — nothing on function definitions or {fd}.
- `CLAUDE.md`, `KNOWLEDGE.md`, `docs/` — verdict: `unknown` — nothing on this hook.
> CAUTION: CLAUDE.md, KNOWLEDGE.md and docs/ are unknown per the Section 2 currency check; treat their claims as advisory, not authoritative.

## Restrictions / decisions that constrain the fix
- `src/superclaude/hooks/scripts/block-bare-python.sh:10` — "allow -> exit 0; block -> one message on stderr + exit 2; never exit 1."
- `tests/hooks/test_block_bare_python.py:101` — `f() { python3 x.py; }` must stay blocked (only the function name is exempt, not the body).
- `.dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md:41` — awk only; 100 KB under 1 s.
- `.dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md:46` — byte-identical mirror.

## Re-frame signals
- Defect 2 contradicts the header's claim that redirections are tracked; defect 1 is an unlisted false positive. Both are code fixes in the awk scanner; the header and CHANGELOG need matching text.
