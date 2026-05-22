# Evidence — T02.02 (DOC-OQ4 NOTICE/LICENSE attribution for ptytest)

**Task:** T02.02 (Phase 2)
**Roadmap row:** 132 (DOC-OQ4)
**ADR ID:** D-10 (decisions.md)
**Tier:** EXEMPT
**Date:** 2026-05-20

This directory captures the evidence artifacts for task T02.02. The full evidence body lives in the deliverable artifact directory:

- **Primary spec:** `../../artifacts/D-0024/spec.md` — acceptance-criteria matrix, attribution clause, files touched.
- **Implementation notes:** `../../artifacts/D-0024/notes.md` — planning observations, design choices, failure modes considered.
- **Evidence body:** `../../artifacts/D-0024/evidence.md` — E1..E6 verification checks.

## Files created or modified by T02.02

| Path | Change |
|------|--------|
| `NOTICE` | CREATED — top-level attribution; references `src/superclaude/cli/eval/pty/LICENSE`. |
| `.dev/releases/current/cliEval/decisions.md` | EDITED — R4 revision log entry; D-10 ADR body added; Sign-off table row added. |
| `.dev/releases/current/cliEval/artifacts/D-0024/spec.md` | CREATED |
| `.dev/releases/current/cliEval/artifacts/D-0024/notes.md` | CREATED |
| `.dev/releases/current/cliEval/artifacts/D-0024/evidence.md` | CREATED |
| `.dev/releases/current/cliEval/evidence/T02.02/README.md` | CREATED (this file) |
| `.dev/releases/current/cliEval/evidence/T02.02/notice-grep.txt` | CREATED — proof that NOTICE references ptytest. |

## Quick verification

```bash
# Acceptance criterion 1: NOTICE exists and references ptytest LICENSE.
test -f NOTICE && grep -c ptytest NOTICE  # expect >= 1; observed 4

# Acceptance criterion 2 + 3: decisions.md records D-10 + OQ-4 resolution.
grep -n "D-10\|OQ-4" .dev/releases/current/cliEval/decisions.md

# Acceptance criterion 4: artifact spec records the attribution clause.
test -f .dev/releases/current/cliEval/artifacts/D-0024/spec.md
```

All four acceptance criteria from `phase-2-tasklist.md §T02.02` are MET. See `../../artifacts/D-0024/evidence.md` for the full table.
