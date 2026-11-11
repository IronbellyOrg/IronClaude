# Brief for step-5 consolidators (orca-observer)

ROOT = /home/coder/workspaces/worktrees/Coder/dashboard-bmad
FR = ROOT/_bmad-output/planning-artifacts/orca-observer/final-review

Read `FR/reviewer-brief.md` first: it lists the artifacts, the source ranking, the binding owner decisions and the grading rule. All of it applies to you.

## Your job (one artifact, named in your task)

1. Read the raw review files named in your task (JSON, under `FR/raw/`). They are proposals by other reviewers, not facts.
2. Merge duplicates: two findings about the same defect at the same place become one merged finding listing both source ids.
3. For every merged finding, re-read the cited lines yourself (both sides, and the source of truth it depends on) and decide:
   - `BLOCKING`: the defect is real and is wrong behaviour, a false claim, a missing required deliverable, a contradiction between documents or with a source, or a security or data-loss risk.
   - `MINOR`: real but only wording, style, citation format, a nit, or a moved line number on a true claim.
   - `REJECTED`: the claim is false when checked, or it only says an open owner question (OQ-1..15, UX-OQ-1..8, CD-1..16) is open, or it asks a document to contradict a binding owner decision. Give the reason.
   Grade by the definition, not by the reviewer's proposal.
4. For every BLOCKING finding, name `fix_in` (the file that must change) and a concrete `fix` (one or two sentences, exact enough for another agent to apply as a text edit). Rule: never change a source of truth to match a wrong derivative; when two documents disagree, fix the lower-ranked one unless the higher-ranked one is itself wrong against its own source (cite that source line). Never resolve an open owner question in a fix: a fix may only make documents state the question and its default consistently.
5. Check the KNOWN ITEMS listed in your task: for each, read the lines and report `RESOLVED` or `STILL-BROKEN` with evidence; a STILL-BROKEN item becomes a BLOCKING merged finding.

## Rules

- READ ONLY. Never edit any artifact. Write exactly one file: the output path in your task. No git, no network.
- Read in ranges of at most 150 lines; grep -n first.
- Cite `relative/path:line` (relative to ROOT; absolute for IronClaude files).

## Output (JSON, exactly this shape)

```
{"consolidator": "...", "artifact": "SPEC|PRD|UX|ARCH|XDOC",
 "merged": [{"id": "SPEC-01", "sources": ["ar-spec:ID", "ech-spec:ID"], "location": "path:line", "other_side": "path:line or null",
   "finding": "one or two sentences", "evidence": "quote <= 30 words", "grade": "BLOCKING|MINOR|REJECTED",
   "reason": "why this grade, one sentence", "fix_in": "path or null", "fix": "one or two sentences or null"}],
 "known_items": [{"id": "K-..", "status": "RESOLVED|STILL-BROKEN", "evidence": "path:line + short quote", "merged_id": "id or null"}],
 "counts": {"blocking": 0, "minor": 0, "rejected": 0}}
```

Write the file once, complete. Your final reply (and nothing else): the output path, then 3 lines: counts BLOCKING/MINOR/REJECTED; known items resolved/still broken; the single worst BLOCKING finding.
