You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/CV-b02. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/CV-b02/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/CV-b02/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/CV-b02/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Assess the supplied relationship and wrong-outcome claim independently. A quoted passage or reviewer assertion is not proof. Judge only the supplied evidence; missing applicability or context means insufficient. Do not infer severity from wording, create findings, demote policy exceptions or claim the full document is clean.

You are a conventional verifier. The directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/CV-b02/ws/packets/ holds 10 packet files (p01, p02, p03, p04, p05, p06, p07, p08, p09, p10). Each packet is a JSON object with `finding` (title and wrong_outcome), `evidence` (one or two quoted texts of a document with their line number and surrounding lines) and `facts`. You see only the packet, never the document.
For every packet answer the judgments below with exactly one of "yes", "no" or "uncertain". Use "uncertain" whenever the packet does not settle the judgment.
- outcome_follows: Does an implementer who follows the texts in `evidence` as written build the outcome described in `finding.wrong_outcome`? yes means: Read as written, the texts in `evidence` lead an implementer to the outcome in `finding.wrong_outcome`. no means: Read as written, the texts in `evidence` lead an implementer to a different outcome from the one in `finding.wrong_outcome`.
- texts_conflict (only for a packet with two evidence texts): Do `evidence.e1.text` and `evidence.e2.text` require incompatible outcomes for the same situation? yes means: No implementation can satisfy `evidence.e1.text` and `evidence.e2.text` in the same situation. no means: One implementation can satisfy both `evidence.e1.text` and `evidence.e2.text`, for example because they apply to different conditions.
- evidence_sufficient: Do the texts in `evidence` contain everything needed to judge whether the outcome in `finding.wrong_outcome` follows, without other parts of the document? yes means: The quoted texts and their surrounding lines in `evidence` are enough to judge the claimed outcome. no means: Judging the claimed outcome needs a part of the document that `evidence` does not include, such as a definition or an exception stated elsewhere.
Write /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e3/offline/sb/CV-b02/ws/answers.jsonl with exactly one JSON line per packet: {"packet": "<file name without .json>", "outcome_follows": "...", "texts_conflict": "... (only for a packet with two evidence texts)", "evidence_sufficient": "...", "note": "<one sentence>"}. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
