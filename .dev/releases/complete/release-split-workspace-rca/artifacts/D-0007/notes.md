# D-0007 — Implementation Notes

## Design decisions

### Hook script as a separate file vs inline command

The hook command field in `settings.json` accepts arbitrary shell. Inline-bash would have kept the change to a single file, but a dedicated script (`.claude/hooks/reject-workspace-writes.sh`) was chosen because:

- The redirect message is multi-line and ships with rationale + a pointer to `make eval-skill`; inlining it would obscure the JSON.
- Other freshness hooks in the project already live under `.claude/hooks/` (e.g. `freshness-pre-edit.sh`), so this follows the established pattern.
- Easier to unit-test by piping synthetic stdin (see `evidence.md`).

### Deny semantics (resolves self-review Q3)

Phase 3 thesis L1.1 originally said "rewrite the path", but Claude Code hooks do **not** transparently mutate tool arguments. The contract is:

1. Hook receives the tool call as JSON on stdin.
2. Hook decides: exit 0 = allow, exit 2 + stderr = block (stderr surfaced to Claude as the reason).
3. There is no path-rewrite primitive.

Interpretation adopted here, consistent with task `Notes` line: "rewrites the path" = "names the correct path in the error message". Claude reads the deny reason and is expected to retry with the corrected destination.

### Pattern precision (R-01)

Regex: `\.claude/skills/([^/]+)-workspace/(.*)$`

Anchoring rationale:

- The `\.claude/skills/` literal anchors to the project skills tree. Absolute paths (`/config/.../.claude/skills/...`) match because the regex is unanchored at the start.
- `([^/]+)-workspace/` requires the directory segment to be a non-empty, slash-free token ending in `-workspace`, immediately followed by `/`. This rejects:
  - `.claude/skills/foo/workspace.md` (no `-workspace/` directory)
  - `.claude/skills/foo/bar-workspace.md` (`-workspace.md`, not `-workspace/`)
  - `.claude/skills/my-workspace-test/file.md` (segment is `my-workspace-test`, not ending in `-workspace`)
- `(.*)$` captures the remainder for inclusion in the redirect message.

### Fail-open on missing path

The hook returns exit 0 when `tool_input.file_path` is absent or empty. Rationale: the hook only enforces a path-shape policy; if the tool call has no path to inspect, the policy cannot be violated and the call must not be falsely blocked. Mirrors the fail-open guarantee of `freshness-pre-edit.sh` (NFR-3).

## Risk mitigations

| Risk | Mitigation |
|---|---|
| R-01 pattern over-matching | Mandatory negative tests (negative case 1 and 2) confirmed alongside positive case in `evidence.md`. Two additional edge cases (`my-workspace-test/` and `bar-workspace.md`) also confirmed non-matching. |
| Hook bypass via direct git commit | Out of scope here; covered by M2 CI gate (DEP-002, D-0006). |
| Skill-creator plugin path change (R-04) | Out of scope for the hook itself — the hook keys on the *destination directory pattern*, not the plugin source code. |

## Dependencies

- None for execution.
- Conceptually paired with T03.02 (CLAUDE.md addendum) and T03.03 (`make eval-skill` target) to make the correct destination the path of least resistance.

## Rollback

Remove the `PreToolUse` entry from `.claude/settings.json` and delete `.claude/hooks/reject-workspace-writes.sh`.

## File manifest

- `.claude/hooks/reject-workspace-writes.sh` (new, executable, +x mode)
- `.claude/settings.json` (modified — was `{}`, now contains the PreToolUse registration)
