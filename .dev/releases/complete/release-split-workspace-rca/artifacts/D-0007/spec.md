# D-0007 — PreToolUse hook rejecting writes to `.claude/skills/*-workspace/**`

**Task:** T03.01
**Roadmap Item:** R-007
**FR Source:** FR-L1.1
**Phase:** Phase 3 — Occurrence Prevention

## Scope

Block `Write` and `Edit` tool calls targeting `.claude/skills/*-workspace/**` at tool-dispatch time, emitting a deny decision whose message names the corrected destination `.dev/eval-workspaces/<skill-name>/<remainder>`.

Semantics are *reject-with-redirect*, **not** transparent path rewrite — Claude Code hooks emit a deny decision plus an explanatory message; Claude is expected to retry against the corrected path.

## Deliverable

Two artefacts:

1. **`.claude/hooks/reject-workspace-writes.sh`** — bash script invoked by the PreToolUse hook.
   - Reads tool-call JSON from stdin and extracts `.tool_input.file_path`.
   - Matches the regex `\.claude/skills/([^/]+)-workspace/(.*)$` (ERE) against the path.
   - On match: writes the redirect message to stderr and exits `2` (Claude Code's "block" decision).
   - On non-match or missing path: exits `0` (allow / fail-open).

2. **`.claude/settings.json`** — registers the script as a `PreToolUse` hook with matcher `Write|Edit`, timeout `3` seconds.

## Behaviour Contract

- **Positive:** any path containing `<...>/.claude/skills/<X>-workspace/<remainder>` where `<X>` is a non-empty segment without slashes → blocked with the message:
  > Workspace path rejected: write to `.claude/skills/<X>-workspace/<remainder>` blocked. Use `.dev/eval-workspaces/<X>/<remainder>` instead.
- **Negative 1:** `.claude/skills/<X>/<file>` where `<X>` does not end in `-workspace` → allowed.
- **Negative 2:** `.claude/skills/<X>/workspace.md` (single-file `workspace.md`, not a `-workspace/` directory) → allowed.
- **Negative 3:** missing/empty `file_path` → fail-open, allowed.

## Pattern Precision (R-01)

The regex requires a literal `-workspace/` (note the trailing slash) following a non-slash segment, after `.claude/skills/`. This distinguishes:
- a directory segment ending in `-workspace` (matched)
- a filename containing the substring `workspace` (not matched)
- a directory segment containing `-workspace-` infix (not matched — must terminate at `/`)

## Out of Scope

- CLAUDE.md addendum (T03.02 / D-0008).
- `make eval-skill` convenience target (T03.03 / D-0009).
- Path rewriting / transparent redirection — not supported by Claude Code hook contract.
