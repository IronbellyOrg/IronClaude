# X04 FINAL: Orca auth token printed in a debate subagent transcript

Status: recommendation only. Nothing here is done until the owner says the sentence in section 7, in chat.

## 1 Unified proposal
Check whether the leaked token is already replaced, restart Orca only if it is not, leave every transcript alone, add a written rule now, and add a small blocking hook as a second, separate pull request.
Order:
1. Owner says the sentence in section 7. An agent records the words. The owner writes no file.
2. Dry run first. Copy the command below into a throwaway form that reads a path from a variable, and point it at three fake files (token matches, token differs, file missing). It must print SAME, DIFFERENT, ERROR. Then the coordinating session (not a debate agent) runs the real check with shell tracing off. It writes no file and prints one word:
   `t=$(jq -er .authToken /home/coder/.config/orca/orca-runtime.json) && [ ${#t} -eq 48 ] || { echo ERROR; exit 1; }; [ "$(printf %s "$t" | sha256sum | cut -c1-10)" = 5220dd2a31 ] && echo SAME || echo DIFFERENT; unset t`
   The constant 5220dd2a31 is the first 10 characters of a SHA-256 hash of the leaked token. It reveals nothing and may sit in the progress log.
3. DIFFERENT: closed. Log "replaced by the Orca start of 2026-11-21 02:08, confirmed by fingerprint". Change the row at `spec/SPEC.md` line 545 and the Appendix B update after PR 700 from "not rotated" to that result. Add one line to the live-enable checklist. ERROR proves nothing and is never read as safe.
4. SAME: the owner names a quiet moment with no worker running, quits and reopens Orca (this closes every terminal and agent session). The coordinator is re-bound and its screen checked (memory notes orca-coordinator-rebind-after-resume and orca-worker-resume-verify-screen). The check is run again and must say DIFFERENT.
5. Rule pull request first. Paragraph under `## Safety Rules` (line 223) of `src/superclaude/core/RULES.md`, then `make sync-dev`. The same text goes at the top of every debate and subagent brief. Text: "Never open, search inside, print or copy /home/coder/.config/orca/orca-runtime.json. stat and ls -l are allowed. For any other file that may hold a secret (a name with token, key, secret, credential or env; ~/.config/gh; ~/.ssh), use it only if the task names that exact file, and print a count (grep -c) or an exit status (grep -q), never the content. Do not hide a value with a filter: do not read it. If a command prints a secret by mistake, stop, tell the coordinator only the file name, and never repeat the value." The one exception is the coordinating session's fingerprint command in step 2.
6. Hook pull request second, merged only after step 3 or 4 is recorded (the hook would block the check). About 25 lines, a PreToolUse guard on Bash, Read and Grep, same pattern as `/home/coder/.claude/hooks/block-bare-python.sh`, registered in `src/superclaude/hooks/hooks.json`. It blocks (exit 2, one line) any call naming `orca-runtime` or `.config/orca/`, except a single plain `stat` or `ls` with no `;`, `&&`, `|`, backtick, `$(`, `>` or newline. It allows on any hook error. Tests: blocks `cat`, `jq .`, a Grep on the file, and `ls -l x; cat file`; allows `ls -l`; allows on error. If it will not stay small and tested, the rule ships alone and the owner is told why.
7. Both pull requests open only with `/sc:pr-submit --monitor 3`. Nothing else writes to GitHub.
No transcript is edited, deleted or scanned further. Nobody edits `orca-runtime.json`. Agents never restart Orca.

## 2 Context
On 2026-11-20 the D02 debate agent printed the `authToken` field of the local Orca runtime file into its own transcript, after its redaction filter failed (DECISIONS.md lines 1176-1178; SPEC.md line 545). The value is in no repository file. The only known copy is one transcript, mode 600, 2,061,029 bytes, last written 2026-11-20 04:18. The token lets a caller control Orca on this machine: terminals, worktrees, agents, typed input. The runtime file was rewritten 2026-11-21 02:08:41 and Orca (pid 481) started 02:08:40, after the leak. Both agents found in the Orca program bundle that the server makes a fresh random 24-byte token for each server object, so it was probably replaced. Probably is not proof, so we compare fingerprints.

## 3 Implications
- Changes: the item gets closed with evidence, not a guess. A written credential rule and later a blocking hook exist. SPEC row 545 and the Appendix B update change from "not rotated" to the check result.
- Stays: transcripts, `orca-runtime.json`, Orca itself, and every GitHub setting are untouched. Orca restarts only on SAME.
- Stays blocked: after the hook merges, any later read of the runtime file (including a re-check) needs the owner's separate go. Protection reaches other workspaces only through the Coder template (memory ironclaude-updates-only-via-coder). The watcher live-enable should wait for the recorded result (panel finding F13 noted that rotation has no stage).

## 4 Benefits
No evidence lost and no outage unless SAME. The answer is a single word. The next leak is stopped by a tool refusal, not by an agent's memory or a filter. The old token's fingerprint stays usable even after the transcript is deleted.

## 5 Risks and containment
- The check holds the token in memory for one command: one word out, tracing off, no file, coordinating session only.
- The hook may block a legitimate use: narrow match, tested, allows on error, its own pull request so a revert is one step.
- A restart (only on SAME) drops sessions: owner picks the time; coordinator re-bound and screen checked.
- The rule can be ignored: the hook is the backstop. A glob such as `~/.config/orca/*.json` or a built-up path passes the hook; the rule covers it.
- The wrong constant would give a false DIFFERENT: it was derived twice, independently (A and B, round 1), and the dry run must pass before the real run. I did not re-derive it, since that means reading the transcript.
- The model service saw the value once; retention unknown. Harmless once the token is replaced.
- Three older name-only matches (2026-11-07 to 11-09 transcripts, values of 29 to 34 characters, not 48 hex) are probably code text and are not explained. Not chased: a 48-character hex token is the Orca shape.

## 6 Costs (estimates; basis: one small edit or one short script per line)
- Dry run plus check: 0.2 h. Log and spec edits: 0.25 h. Rule pull request with one monitor round: 0.75 h. Rule path about 1.2 h.
- Hook pull request with tests and one monitor round: 1.5 to 2 h.
- Restart plus re-check, only on SAME: 0.5 to 1 h.
- Total: about 1.2 h (rule only), about 3 to 3.2 h (rule and hook), up to about 4 h with a restart. The owner's time: one chat line, plus naming a time on SAME.

## 7 The sentence the owner says in chat
"X04 approved: run the Orca token check and tell me SAME or DIFFERENT. If SAME, I will name a quiet moment to restart Orca. Do not edit or delete any transcript. Add the credential-file rule now and the small hook as its own pull request afterwards."

## 8 What an agent does after it
Records the words in the progress log. Runs the dry run, then the check in the coordinating session, and reports one word. Writes the result into the log, SPEC line 545 and the Appendix B update. On SAME, asks the owner for the restart time and re-binds the coordinator. Opens the rule pull request, then (after the result is recorded) the hook pull request, each with `/sc:pr-submit --monitor 3`. Tells the owner when a later read of the runtime file would need a fresh go.

## 9 Consensus
Full on substance. Both agents ended with the same plan and the same fingerprint check. Residual packaging choices for the owner, both with a safe default:
- Rule and hook as two pull requests (default, my choice) or one. Two: the rule goes live when it merges, a faulty hook can be reverted alone, one extra review round (about 0.5 h, estimate). One: about 0.5 h cheaper, but a hook defect delays the rule and a revert undoes both.
- Add a `permissions.deny` entry for `/home/coder/.config/orca/**` in `~/.claude/settings.json`: no (default). Yes adds a layer, but edits user settings and may not stop a Bash `cat` or a Grep (UNVERIFIED).

## 10 Not verified
- Whether Orca makes a new token on every start (read from a minified bundle by both agents; I did not re-open it). The check settles it.
- The constant 5220dd2a31 (I did not hash the transcript; I checked only that `jq` and `sha256sum` exist at /usr/bin).
- Which loopback port takes the token; whether root or the host platform could read the transcript; model-service retention.
- Whether the leak is in other files (a wide scan timed out for A; B scanned `~/.claude/projects` only).
- Where the debate brief template lives (the workflow script builds it).
- Whether `cleanupPeriodDays` is 30 or 90 here: I found no such key in `/home/coder/.claude/settings.json`, so the default of 30 days probably applies, and the leak transcript would then be deleted around 2026-12-20. Not relied on.
- Checked by me: SPEC.md line 545 says "not rotated"; DECISIONS.md lines 1176-1178; runtime file mode 600, 366 bytes, 2026-11-21 02:08:41; leak transcript mode 600, last written 2026-11-20 04:18:20; `~/.claude/projects` and `/home/coder` mode 700; Orca pid 481 started 2026-11-21 02:08:40; `RULES.md` Safety Rules at line 223 with no credential rule; `block-bare-python` is registered in `src/superclaude/hooks/hooks.json`.
