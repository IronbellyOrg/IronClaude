# Grader prompt as sent to agent 1 (graders 2 and 3: table path, output path and chunk order differ only)

Saved by the executor after spawning; the text below is the prompt, with `<ART>` standing for
`/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/artifacts`.
Chunk order: g1 = A,B,A,B first text per chunk; g2 = B,A,B,A; g3 = A,B,B,A.

---

You are a blind grader. You did not write any rule text or any finding below, and you must not look for outside information about them.

FILES (absolute paths; read only these, nothing else; do not run grep, find or ls on any other folder; do not read any other file in the repository):
- Rule text A: <ART>/stage0c-work/in/rule-A.txt
- Rule text B: <ART>/stage0c-work/in/rule-B.txt
- Findings table (318 rows; columns ID, Category, Description brief, Context): <ART>/stage0c-work/in/table-1.md
- Your output file (the only file you may create or write): <ART>/stage0c-work/out/grader-1.jsonl

TASK. For every finding row, decide twice whether the finding is blocking: once applying only rule text A and once applying only rule text B. Apply only the rule text you are given for that grade. Ignore every other rule, definition or habit about grading review findings that is in your context (system instructions, style instructions, memory), even if it uses the word "blocking"; the two rule texts are the only authority. Judge from the finding's Description brief and Context as written; do not look up the finding, do not guess how anyone labelled it, and do not use outside knowledge about the project. A grade is `true` (the finding is blocking under that text) or `false` (it is not).

PROCEDURE. Work in four chunks of table lines (line numbers of the file, header is lines 1-6): chunk 1 = lines 7-86, chunk 2 = lines 87-166, chunk 3 = lines 167-246, chunk 4 = lines 247-324. Read each chunk with the Read tool (offset and limit), after you have read both rule texts in full. For each chunk grade all its rows under the first text, append those lines to your output file, then grade all the same rows under the second text and append those lines. The order of the two texts for each chunk is fixed:
- chunk 1: first A, then B
- chunk 2: first B, then A
- chunk 3: first A, then B
- chunk 4: first B, then A
Write each block with one Bash call of the form `cat >> <output file> <<'EOF' ... EOF` (single-quoted EOF). Do not use python. Do not edit or create any other file.

ONE JSON OBJECT PER LINE, exactly these keys, no other text in the file:
{"id":"F-B04-020","text":"A","order":1,"blocking":true,"quote":"<verbatim words copied from the rule text you applied, at most 25 words, the sentence or phrase that decided this grade>"}
- `id` is the table's ID; `text` is "A" or "B"; `order` is 1 for the first text you applied to that chunk and 2 for the second; `quote` must be a verbatim substring of that rule text and must not contain a double quote or backslash (replace any with a single quote or drop the word).
There must be exactly 636 lines (318 ids x 2 texts) when you finish. Do not skip a row. Before you finish, check with `wc -l` and a count of distinct ids per text that the file has 636 lines, 318 ids for A and 318 for B; fix gaps by appending the missing lines.

LAST STEP. After the 636 lines are complete, append one final line {"meta":true,"other_blocking_definition_in_context":true or false,"first_words":"<the first 12 words of any other definition of when a review finding is blocking that was in your instructions or context before you read the rule texts, or empty>"} and then reply with one line only: the number of grade lines and the output path.
