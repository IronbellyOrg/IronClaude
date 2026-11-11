You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r3/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r3/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r3/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r3/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### M6
| M6 | open | Line 194 fixes the P0 flag problem (P0 briefs omit `--unattended`), the WC-4 path (existing report used) and the no-wrapper check (step 5). Step 4 still fails on a correct run: line 183 still asserts `d['command']`, and line 194 applies the YAML key check to workflow, whose contract has no `command` key (line 194 cites INV-B:272 for that). Grading sentence: "An implementer who follows line 194 for workflow asserts `command` (line 183) against a contract with no `command` key, so the check raises KeyError and step 4 fails on a correct run." This needs no further assumption, so the finding stays blocking. |
(text of this finding in the prior report)
### M6
#### M6.a, from round1-b.md B-2: B-2 (BLOCKING). AC-0.4 cannot pass as written in P0
- Location: candidate:73 (brief "states the exact command line including `--unattended`"); candidate:180 (7.2 step 1, brief per 2.3); candidate:182 (step 3, "its report path is the WC-4 contract path"); candidate:183 (step 4, asserts `d['status']` and `d['command']`); candidate:194 (AC-0.4 runs `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial --compare ... --output <dir>` with no `--unattended`; says step 4 "uses the command's existing report file, since the contract arrives in P1"); candidate:62 and :158-159 (WC-4 is unattended-only and arrives in P1).
- Issue, four separate failures:
  1. Step 1 requires the brief to carry `--unattended` (candidate:73), but P0 has no such flag (candidate:158 "no command edits"; candidate:159 adds it in P1). The AC's own command lines omit it.
  2. Step 3 requires the WC-4 path, which exists only in unattended mode (candidate:62) and only from P1. Neither P0 run is unattended.
  3. Step 4 asserts YAML keys, but AC-0.4 says step 4 reads the existing report. troubleshoot's existing report is `REPORT.md` (INV-B:49), which is Markdown and fails `yaml.safe_load` as a contract. workflow's contract has `status`, `plan_path`, `reflect_report_path` and no `command` key (INV-B:272), so `d['command']` raises KeyError.
  4. AC-0.4 says "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)", but step 5 (candidate:184) searches only for AskUserQuestion. The no-wrapper clause has no check.
- Grading check: "An implementer who runs AC-0.4 exactly as written in P0, without `--unattended`, finds that step 3 has no WC-4 path and that step 4 raises KeyError on `command` for workflow, so P0 cannot pass, because the flag, the path and the keys are all introduced only in P1."

### N1
### N1 (new; origin=changed; blocking)
- Location: line 76 (changed): "cleanup-audit and index-repo gain `--output-dir <dir>` in P1". Conflicts with line 85 (unchanged row): "output dir is fixed, so one audit per worktree at a time (WC-11) (P1)".
- Grading sentence: an implementer who follows the cleanup-audit row keeps its output directory fixed and adds no flag, while one who follows line 76 adds `--output-dir <dir>` in P1. The spec states both that the directory is fixed and that it gains a flag, so the two texts contradict each other with no further assumption.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
