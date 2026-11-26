# Task 5 report: remaining rule files checked against the WC-3 definition

Repo-wide search (Markdown under src/superclaude, outside core/WORKER-CONTRACT.md and refs/qa.md, refs/ledger.md, refs/retry.md): `grep -rn -E "Ruling|grant row|pass record"`, `grep -rn -i -E "executor-invented|another agent's message|clear user confirmation|person's own chat|in chat"` and the E-NO-RULING row. Hits that state who may confirm are listed below; the other hits (the "Report directory ... printed in chat only" lines of the command files, remediation-chain confirmations in troubleshoot, auggie-review and task, "Surface to the user in chat") are unrelated to Ruling, grant row or pass record confirmation and were left unchanged.

| File and place | Decision | Reason |
|---|---|---|
| src/superclaude/skills/sc-implement-protocol/SKILL.md line 41 (`E-NO-RULING` row) | edited | It said "clear current-conversation confirmation is sufficient"; it now names chat message or dashboard response and points to the qa.md Halt table. The row still stops for `--force`, missing or ambiguous confirmation and executor-invented approval. |
| SKILL.md lines 39, 58, 149-150, 193 | unchanged | Mention a Ruling or `--force` mechanically and point to the qa.md Halt table; they state no channel. |
| src/superclaude/core/HOW-WE-WORK.md line 114 | edited | It said the lead accepts "in the current conversation"; it now names the chat or the dashboard response once the dashboard answer path is released, and says no other channel counts. The plugin copy plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md was copied byte for byte (cmp exits 0). |
| src/superclaude/core/CLAUDE.md | unchanged | The sentence is not in it; the level-table copy is not affected because the edit is outside that table. |
| src/superclaude/skills/sc-implement-protocol/refs/retry.md lines 498-500 (Ruling eligibility rule) | unchanged | About when a Ruling line is eligible (halt and blocked ordering), not about who confirms. |
| src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md lines 76 and 92-93 | unchanged | Line 76 says "Do not ask the user ... hand-write records" and points to the qa.md Halt table; lines 92-93 are the enforcement map ("genuine informed user confirmation") and state no channel. |
| src/superclaude/commands/implement.md line 107 | unchanged | Says "an operator `Ruling:`"; states no channel. |
