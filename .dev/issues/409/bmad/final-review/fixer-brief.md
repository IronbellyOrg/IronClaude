# Brief for step-5 fixers (orca-observer)

ROOT = /home/coder/workspaces/worktrees/Coder/dashboard-bmad
FR = ROOT/_bmad-output/planning-artifacts/orca-observer/final-review

Read `FR/reviewer-brief.md` first (artifacts, source ranking, binding owner decisions). All of it applies.

## Your job

1. Your task names a CYCLE number, your FILE SET and a FINDINGS INPUT (JSON files with BLOCKING findings, each with `id`, `location`, `fix_in`, `fix`).
2. Take every BLOCKING finding whose `fix_in` is a file in your file set. Ignore every other finding.
3. For each one: Read the cited lines (both sides and the source of truth it depends on), then apply the fix as a minimal text edit with the Edit tool (Read the file first; never sed, never a script). Keep evidence labels (VERIFIED, UNVERIFIED, PROPOSED and so on) and the document's style.
4. Do not apply a fix that would: change a source of truth to match a wrong derivative; resolve an open owner question (OQ-1..15, UX-OQ-1..8, CD-1..16); contradict a binding owner decision; invent an Orca API field. Record such a finding as `skipped` with the reason. If the suggested `fix` is wrong but the defect is real, apply the correct minimal fix and say so in `note`.
5. After your edits, grep your file set for other occurrences of the same wrong text and fix those too (list them in `also_changed`).
6. Log one memlog entry per file you changed, with ONLY this command (workspace = the folder holding that file's `.memlog.md`):
   `uv run ROOT/_bmad/scripts/memlog.py append --workspace <folder> --type decision --text "step 5 fix cycle <N>: <ids>: <one-line summary>"`
   Memlog folders: SPEC `ROOT/_bmad-output/specs/spec-orca-observer`; PRD `ROOT/_bmad-output/planning-artifacts/orca-observer`; UX `ROOT/_bmad-output/planning-artifacts/orca-observer/ux-designs/ux-orca-observer-2026-11-08`; ARCH `ROOT/_bmad-output/planning-artifacts/orca-observer/architecture`.

## Rules

- Edit ONLY files in your file set, plus your one output file. Never edit final-review/ files other than your output. Never touch `_bmad-output/specs/spec-orca-observer/ARCHITECTURE-SPINE.md` (the orchestrator copies it).
- No git, no network. UV only. Read in ranges of at most 150 lines; grep -n first.

## Output (JSON, write once, complete)

`{"fixer": "...", "cycle": N, "file_set": "...", "results": [{"id": "...", "status": "applied|skipped", "file": "path:line after edit", "note": "one sentence"}], "also_changed": ["path:line"], "memlog": ["folder"]}`

Final reply (and nothing else): the output path, then 3 lines: applied/skipped counts; files changed; the riskiest edit.
