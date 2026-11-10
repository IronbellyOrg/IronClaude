You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e1/offline/sb/CC-smoke-b01. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e1/offline/sb/CC-smoke-b01/ is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e1/offline/sb/CC-smoke-b01/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e1/offline/sb/CC-smoke-b01/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Evaluate only the supplied prior finding and mapped change. Distinguish removing the original defect from preserving the accepted obligation. Check supplied dependent passages. Reviewer/reviser assertions are not proof. Missing, conflicting or insufficient evidence means uncertainty for generative verification. Do not certify untouched global text.

For each packet in /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e1/offline/sb/CC-smoke-b01/packets.json, answer each question below with `yes`, `no` or `uncertain`, using only that packet: defect_still_present (does `after.passage` still lead an implementer to the wrong outcome in `defect.wrong_outcome`?), obligation_still_required (does `after.passage` still require what `obligation.text` requires?), contradicts_dK for each supplied dependency dK (does `after.passage` contradict it?), context_sufficient (do the supplied passages suffice to decide whether the requirement of `obligation.text` is still in force?). Write one JSON line per packet to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p15/e1/offline/sb/CC-smoke-b01/answers.jsonl: {"packet_id": "...", "defect_still_present": "...", "obligation_still_required": "...", "contradicts_d1": "...", "context_sufficient": "...", "quote": "<the after text you relied on>"}. Add one contradicts_dK key per dependency the packet supplies and none for a packet without dependencies. Edit nothing else.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
