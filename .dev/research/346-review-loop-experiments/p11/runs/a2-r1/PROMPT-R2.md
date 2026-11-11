You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p11/runs/a2-r1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p11/runs/a2-r1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p11/runs/a2-r1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p11/runs/a2-r1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

COMMAND: you cannot run slash commands. The file /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p11/runs/a2-r1/command.md is the definition of the /sc:spec-panel command. Act as that command: apply its critique mode, its "Review Loop" section and its "Mandatory Output Artifacts" exactly as written, and every other section of it that applies. Read command.md in full first.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Run /sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md . Follow this re-review prompt:
Follow the re-review core below in order (roles, Step 1, review number, self-check), then use this brief.

| ROLE | FILE VALUE | MEANING |
|---|---|---|
| CANDIDATE | the `@file` of the command | the revised text under review |
| BASELINE | the `--baseline` file | the text as it was before the revision |
| PRIOR | the `--re-review` file | the previous review report |
- **Step 1, the evidence block**, before any finding. Roles are fixed: never infer a role from reading order or from memory. Run `diff -w BASELINE CANDIDATE` and copy the changed lines verbatim under `BEFORE (baseline)` (lines starting `<`) and `AFTER (candidate)` (lines starting `>`). Decide each prior blocking finding marked resolved as resolved or regressed by comparing its defect with the AFTER text only. If the diff is empty, every prior blocking finding stays open.
- **Review number**: N is the number in PRIOR's `review: N of 3` header plus 1. Write `review: N of 3` once, as the first line of the report. Example: a prior `review: 2 of 3` gives `review: 3 of 3`. Use no other header variant.
- **Self-check before the verdict**, when commands can be run: `grep -nF` each quoted AFTER line (without its `>`) in CANDIDATE and each quoted BEFORE line (without its `<`) in BASELINE. If any quote is not found, you swapped roles: redo Step 1. A PASS requires the AFTER text to be consistent with every requirement that depends on it.

- Re-review brief: "Review the revised candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file) against .dev/orca-command-refactor/specs/history/spec-v1.md, the spec as it was before the revision (sha256 of the file), using prior report .dev/orca-command-refactor/review/round1.md (sha256 of the file), review 2 of 3, where N is the prior report's review number plus 1. Do Step 1, the evidence block, before any finding. Re-check each prior blocking finding as resolved, open or regressed against the revised candidate. Inspect changed behavior and the dependencies it touches; for inherited text, cite the changed line it depends on. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. Record a severe defect you newly discover even if it is older, and say where it came from. If an input is missing or unreadable, return incomplete. Run the self-check before the verdict. Do not edit the candidate and do not start another review. State what you covered."
Write the full report to .dev/orca-command-refactor/review/round2.md. Do not edit anything else. First read .dev/orca-command-refactor/README.md (binding shared context; the files under .dev/orca-command-refactor/inventory/ are the only evidence you can check, mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
