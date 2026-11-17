# Control test result: do the graders follow a rule that differs from the injected one?

Written by `analyze.py` from `out/control-1.jsonl`. The criterion was fixed before the run (`PREREGISTERED.md`).

## Result

- Rows graded: 160 (lines 7 to 166 of `in/table-1.md`), one fresh agent, rule C only (blocking only for data loss, exposure, a safety boundary or acting outside the declared scope).
- Blocking under rule C: **25 of 160 (15.6%)**. Blocking under today's rule (A) for the same rows by grader g1: 157 of 160; under the digest (B): 155 of 160.
- Rows where rule C and rule A disagree (g1): 132 of 160.
- Quotes that are verbatim substrings of rule C: 160 of 160.
- Pre-registered reading: **Sensitive: the grader followed the rule it was given despite the injection.**

## The control grader's own report

- Other definition of blocking in its context: True; first words: Grade every review finding as blocking or minor. Blocking is a real defect:
- How it wrote the lines: I wrote each row's line by hand in two heredoc blocks, with no loop or script.

## Rows graded blocking under rule C (25)

| ID | Rule A (g1) | Rule B (g1) | Description brief | Quote applied |
|---|---|---|---|---|
| F-B07-027 | blocking | blocking | A backslash-newline inside a word (for example `gi\` newline `t push origin HEAD:main`) is normalised away so the classifier no longer sees git, gh, … | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B08-026 | blocking | blocking | WC-4's contract write breaks stated write-scope rules: init-lite's safety invariant allows only the marked report as a write, and cleanup-audit write… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B01-007 | blocking | blocking | Task 4 specifies resume_decision(mode, ordinal, guard, read, pending, dangling_branch, published) without target_sha, yet requires a published-push r… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B06-024 | blocking | blocking | The revised line 62 puts the contract for init-lite and tdd in the file that --output names, while the tdd row says the report is the TDD at --output… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B06-028 | blocking | blocking | The default contract location for a file-valued --output is the file's parent directory, so two workers whose output files share a parent write the s… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B04-019 | blocking | blocking | The plan says a bound session whose session file is deleted reads as ordinary, which contradicts AC-5's fail-closed-on-missing-state wording, with no… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B06-013 | blocking | blocking | Auto-fix with promote-by-default would apply and promote work that still has unresolved human-decision items (Grounding Gaps, needs_human_decision). | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B04-024 | blocking | blocking | The revised rollout rule enables unattended save in the report-only phase while its per-session writer ships later, so two workers with separate repo… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B05-011 | blocking | blocking | The plan treats text inside double quotes as never a command word, so a quoted command substitution such as x="$(python3 -c 1)" runs bare python3 wit… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B01-002 | blocking | blocking | The launch-prompt template's submit block can be written as gh pr list --head with no --repo, and the fork-safety scan covers only SKILL.md, refs and… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B06-027 | blocking | blocking | WC-4 says the contract is in the directory the coordinator passed and known before dispatch, while WC-6 says a retry must not corrupt the first attem… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B05-013 | blocking | blocking | WC-6 says a retry must not corrupt the first attempt's output and that a command without a resume flag writes into a fresh directory, but only the re… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B10-020 | blocking | blocking | Two commands keep a fixed output location (`.claude-audit/` and `PROJECT_INDEX.md`), so two workers started in the default shared worktree overwrite … | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B05-024 | blocking | blocking | WC-6 gives the command the job of using a fresh output folder per run, but the folder is fixed in the Task brief at task-create and --retry-of reuses… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B06-033 | blocking | blocking | The claim that Stage 0 is decoupled and a pure win is false: wiring setup_isolation changes Path A's existing CLAUDE_WORK_DIR to release_dir and chan… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B10-016 | blocking | blocking | After phase P1 several gated commands (auggie-review, cleanup, task, cli-eval, implement, post-release, pr-submit) accept `--unattended` while their … | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B03-008 | blocking | blocking | No fold row sets `cycle_id`, and engage row 7 does nothing on a held guard, so a later cycle runs under the earlier cycle's id and resume row 4 can r… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B10-011 | blocking | blocking | Requirement WC-3 lets a worker ask the coordinator and re-invoke the command with the answer as a flag, while the `/sc:implement` row and decision D2… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B01-032 | blocking | blocking | The spec has no precondition that the working directory is an IronClaude project. | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B03-012 | blocking | blocking | A `bypass` test built as the plan says sets only HOME, so on the old launcher it can start the real `claude` with the bypass flag during the red run. | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B06-030 | blocking | blocking | A retry cannot carry a new brief: worker-start --retry-of must name the same failed Task and a Task's spec cannot be edited, so WC-6 "fresh output di… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B05-001 | blocking | blocking | Resume row 4 and RETRY_RELEASE (engage row 5, resume row 7) re-enter release_decision, which needs target_sha, applied_edits and push_completed, but … | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B07-028 | blocking | blocking | A versioned npx spelling of Claude Code (`npx -y @anthropic-ai/claude-code@latest -p ...`) has the basename `claude-code@latest`, so the escape rule … | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B01-010 | blocking | blocking | The spec strips the token only from the prove step's environment, while the monitor design omits persist-credentials: false, so the checkout leaves t… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |
| F-B02-008 | blocking | blocking | `merge_recovery_bundle` derives the results directory from `source_index.parent / "results"` instead of the sprint config's release directory, so for… | delete, overwrite or expose data or a secret, break a safety boundary, or act outside the… |

## What this does and does not show

- It tests the instrument (an agent in this session, with the old rule injected), not the new text. A sensitive result means the near-identical old and new grades are not explained by the injection alone; it does not say what the new text would do without it.
- One agent, 160 of 318 rows, one alternative rule. A different alternative rule could behave differently.
- The owner's go for the next stage is given in chat and not by this file.
