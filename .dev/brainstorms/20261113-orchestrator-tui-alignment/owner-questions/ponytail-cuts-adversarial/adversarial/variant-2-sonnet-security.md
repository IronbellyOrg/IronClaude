# Variant 2 (sonnet, security): conservative cut list

Saved by the orchestrating session from the agent's returned text; evidence condensed, verdicts unchanged. Checked itself: C01, C03, C04, C05, C06, C10 (labels), C11, C14, C15, C17, C18, C19, C21, C22.

Stance: cut only what is provably unused, duplicated paperwork, or pure owner-time; keep every gate on the trust boundary and every decision the owner made; flag two candidates riskier than the source says.

| ID | Verdict | Risk if cut | Reward if cut | Conf |
|---|---|---|---|---|
| C01 | MODIFY: back up with a local copy and a sha256 list outside git, no push; the owner still writes the confirming line before any flip | A pushed backup could carry agent-made commit `1ae72e1a1`, which sets `QUESTION_GATE_PASSED = True` and cites an owner record git cannot attribute | Records stop being single copies | 80 |
| C02 | CUT (shrink); keep the pasted output untracked (public repo) | Pasted output lists paths and session names; message-write test dropped | No fresh session, worktree or agent | 75 |
| C03 | MODIFY: do not mark closed; fold "confirm A" into the owner's next reply | Closing means an agent writes an owner answer; `owner-answers.md` twelfth batch covers Q35 to Q40, not Q41 | None worth it | 75 |
| C04 | CUT | Only the case of an `orca` on PATH that answers `skills list --json` with `orca-cli`; a planted `orca-ide` is equally possible | One card fewer | 85 |
| C05 | MODIFY: cut the card, keep a one-line caveat on the #423 rewrite | Without it, nothing says watcher-started sessions are never messaged; v2 could push text into permission-off sessions | One card fewer (default is already "report only") | 70 |
| C06 | CUT | v2 sequencing wording stays loose | No false gate on unbuilt work | 85 |
| C07 | DEFER | #409 correction posts no status line; release 3 stays blocked as now | No ten-field record | 75 |
| C08 | DEFER | Blank stays in the Coder#477 draft | No number for a reader that does not exist | 80 |
| C09 | DEFER | Panel never ships while deferred | Avoids a live test that might consume a real question ("does not mark read" untested, 61%) | 85 |
| C10 | DEFER (conditional) | If the first watcher launch is scheduled, Q20 is needed first | No rota for sessions that do not spawn | 70 |
| C11 | DEFER | A first coordinator would be told by WC-16 to run `/sc:sweep` and hit "No such command" | No workspace update that ends sessions | 80 |
| C12 | KEEP (OVERRIDE) | Cutting needs a new owner decision. The source's risk is backwards: with no GitHub input there is nothing for a stranger to forge. Put the question to the owner once; do not cut | About 4,000 lines (unchecked) | 70 |
| C13 | KEEP (OVERRIDE) | Bare `approved` still releases a governed session (`launch-level-guard.sh` lines 343-353): the self-approval hole Task 16 closes | About 13 files untouched | 85 |
| C14 | MODIFY: adopt only the throwaway `worker-start`/`ask`/`reply` test, keep Task 16 first and unblocked | Delaying Plan A delays Task 16, a security fix | Real Orca facts | 70 |
| C15 | DEFER | Docs `issue-watcher-setup.md:453-474` and FU-10 (line 680) tell the owner to call `slo_numbers`; deleting breaks that step and the AC-24 test | About 470 lines | 75 |
| C16 | CUT (process) | None | Owner time | 85 |
| C17 | DEFER | Hard to revive; question code spans `collector.py`, `view.py`, `render.py`, `commands.py`, `parse.py`; 26 dedicated test functions, not 56 | About 2,500 lines | 70 |
| C18 | DEFER | Behaviour change to a merged tool; file is 0600 in a 0700 folder, so no leak | Stops a 387 KB rewrite with fsync each cycle | 70 |
| C19 | MODIFY: one text line only, no new rule | A coordinator reading "working: 0" acts on a false "nothing is running" | A report that stops lying | 80 |
| C20 | DEFER (do not close #423) | v2 stays undefined | No design effort on an unproven need | 75 |
| C21 | KEEP | Cutting removes the guard on a live read of coordinator messages | Removes the source of Q7 and Q8 | 90 |
| C22 | KEEP | Merging forces the sweep onto a bare `orca` fallback; the sweep deliberately never uses it. Two finders, not three (observer imports the first) | Less duplication | 85 |
| C23b (new) | KEEP: do not carry commits `1ae72e1a1` or `f104ca51a` from `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp` into any PR or merge until the owner writes the confirming record | n/a | Prevents an agent-authored gate flip | 85 |

Final list: C04, C06, C02, C16.
Biggest single risk: C02, because pasted Orca output goes into a public repo unless the file stays untracked, and each read still needs its own permission row.
