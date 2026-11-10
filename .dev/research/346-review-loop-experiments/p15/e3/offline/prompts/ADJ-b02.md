You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/ADJ-b02. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/ADJ-b02/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/ADJ-b02/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/ADJ-b02/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
You are an adjudicator. Read /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/ADJ-b02/ws/RUBRIC.md first and apply it exactly.
The directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/ADJ-b02/ws/cases/ holds 10 case directories (a01, a02, a03, a04, a05, a06, a07, a08, a09, a10). Each holds finding.md, document.md (the full document the finding is about) and labels.md (two earlier labels of the same finding with their grading sentences and evidence, which may disagree). Decide each case yourself from document.md; the earlier labels are not evidence.
Write /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/ADJ-b02/ws/adj.jsonl with exactly one JSON line per case directory: {"case_id": "<directory name>", "blocking": "yes|no|undecidable", "reason": "<one sentence>"}. Use undecidable only when the document does not let you decide. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
