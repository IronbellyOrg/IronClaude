# Task: independently label acceptance-check rows of a requirements spec

You are a careful independent reviewer. Do not look for, read or guess anything about how these rows were chosen or about any other reviewer's answer.

Files:
- Packets: `/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p20/label/packets_b1.json` (JSON list of 16 items; each has `label_id`, `spec_path`, `check`, `cited`, `code_stage`)
- Each `spec_path` is the full requirements spec that contains the row. You may read it (read-only) when the packet text is not enough, for example to check that a file, field, flag or state the check needs exists at that point.

For each item decide, for the check executed exactly as written on an implementation that meets the spec:
- `can_pass`: an implementer following the check exactly can run it, observe the stated pass condition, and a wrong or empty result would not satisfy it.
- `cannot_pass`: following the check exactly, the pass condition cannot be met or observed (the command, file, field, flag or state it needs does not exist at that point, or the check contradicts a cited row, or the `code_stage` facts show it fails on a correct implementation).
- `cannot_discriminate`: it can be run and its pass condition met, but a wrong, empty or unrelated result would also pass, so a pass proves nothing.
- `insufficient`: the packet and spec do not let you decide.

Rules: judge the check, not the quality of the spec. Treat `code_stage` as facts a program established. If a shell command is involved and you doubt it, you may run it in a scratch directory under `/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p20/label/scratch_b1` against a tiny fixture you create; never run anything in the repository. Be willing to say `can_pass`; do not assume a check is flawed because it is complex. Give a reason of at most two sentences that quotes the decisive text.

Output: write valid JSON to `/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p20/label/labels_b1.json`: {"batch": 1, "labels": [{"label_id": "...", "label": "can_pass|cannot_pass|cannot_discriminate|insufficient", "confidence": 0.0-1.0, "reason": "..."}, ...]} with exactly one entry per item. Validate that it parses and has 16 entries. Final reply: `DONE <path>` and one line of label counts. Nothing else.
