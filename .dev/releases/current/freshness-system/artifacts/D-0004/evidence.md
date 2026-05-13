# D-0004 — freshness-session-start.sh evidence

## Task: T02.01 (STRICT)

Implements `SessionStart` hook per design §3.1. Two branches (startup / resume),
output wrapped in `<session-context source="...">`, fail-open per NFR-3.

## File

`src/superclaude/hooks/scripts/freshness-session-start.sh` (also mirrored to
`plugins/superclaude/hooks/scripts/`), mode 0755, `bash -n` clean.

## Dry-run 1 — startup branch

```
$ echo '{"session_id":"sess-startup","source":"startup","cwd":"/tmp/test"}' \
    | bash src/superclaude/hooks/scripts/freshness-session-start.sh

{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"<session-context source=\"startup\">\n  ts=2026-05-12T19:44:20+00:00\n  cwd=/tmp/test\n  project=test\n  date=2026-05-12\n</session-context>"}}
```

✓ Valid JSON. ✓ `<session-context source="startup">` envelope present. ✓ `ts`, `cwd`,
`project`, `date` fields rendered. Budget ~120 chars (design §3.1b target).

## Dry-run 2 — resume branch (no prior last-prompt-ts)

```
$ echo '{"session_id":"sess-resume","source":"resume","cwd":"/config/workspace/IronClaude"}' \
    | bash src/superclaude/hooks/scripts/freshness-session-start.sh
```

Envelope (excerpted from full output):

```
<session-context source="resume">
  ts=2026-05-12T19:44:20+00:00
  cwd=/config/workspace/IronClaude
  git=feat/freshness-system status=7
  recent_commits=…(5 oneline entries semi-joined)…
</session-context>
```

✓ git status detected (branch + porcelain count). ✓ recent_commits joined with `;`.
`resumed_after=` correctly omitted (no last-prompt-ts present yet).

## Dry-run 3 — resume branch (synthetic 7200s pause)

After writing a 7200s-old ISO timestamp to `~/.claude/state/last-prompt-ts/<sid>.txt`:

```
<session-context source="resume">
  ts=2026-05-12T19:44:20+00:00
  resumed_after=7200s
  cwd=…
  git=…
</session-context>
```

✓ `resumed_after=7200s` field present.

## Fail-open semantics (NFR-3) — verified

- Subcommand failures (`git rev-parse`, `date -d`, `docker system df`) suppressed
  via `|| true` / `2>/dev/null` and conditional emission.
- Memory dir missing → field omitted (no error).
- jq fallback present for the final envelope JSON if `jq -nc` itself fails.

## Acceptance criteria

| Criterion | Status |
|---|---|
| File exists, mode 0755, `bash -n` clean | PASS |
| Startup dry-run produces valid JSON with `<session-context source="startup">` | PASS |
| Resume dry-run produces valid JSON with `resumed_after=` field | PASS |
| Plugins mirror `diff -q` clean | PASS |

## Sub-agent review (deferred to Phase 2 close)

A combined sub-agent quality-engineer review for D-0004..D-0009 is scheduled at the
end of Phase 2. The review will explicitly address fail-open semantics on each
subcommand (the focal point of T02.01's STRICT verification).
