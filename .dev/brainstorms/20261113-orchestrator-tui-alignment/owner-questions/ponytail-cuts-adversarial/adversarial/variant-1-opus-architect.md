# Variant 1 (opus, architect): aggressive cut list

Saved by the orchestrating session from the agent's returned text (agents cannot write files); evidence cells condensed, verdicts unchanged. Checked itself: C04, C06, C10, C11, C12, C15, C17 (partly), C18, C21, C22.

Stance: delete or stop anything with no live user, no reader and no owner decision behind it. Git keeps history. Where a cut goes against an owner answer, recommend it but do not act on it.

| ID | Verdict | Risk if cut | Reward if cut | Conf |
|---|---|---|---|---|
| C01 | CUT the extra steps around the save | The owner still gives a written OK before an agent copies anything | Pass record stops being a single copy | 80 |
| C02 | CUT (to the 2-command paste) | `agentWait` name unknown until run | No fresh session, worktree or agent | 75 |
| C03 | CUT (close the card) | None if the owner types "Q41: confirm A"; an agent must not write that row | One card fewer | 85 |
| C04 | CUT | Near zero; `_find_orca` requires `orca-cli` in `skills list --json` | One risk acceptance removed | 85 |
| C05 | CUT | Watcher-started session gap stays unwritten until v2 is designed | A decision on a feature that does not exist | 70 |
| C06 | CUT options 2 and 3 | v2 start sentence stays loose | No code change as a planning gate | 80 |
| C07 | DEFER | #409 stays "not met as recorded" | No ten-field record for a dateless release | 75 |
| C08 | DEFER (dies if C18 lands) | Blank stays in the Coder#477 draft | No invented number | 80 |
| C09 | DEFER (CUT if C17 lands) | Panel never ships | No live test for a switched-off panel | 80 |
| C10 | DEFER | First live test still needs a named owner | No rota for sessions that do not exist | 75 |
| C11 | DEFER | `/sc:sweep` unusable here | No workspace update that ends sessions | 85 |
| C12 | CUT the GitHub label and comment input; NEEDS A NEW OWNER DECISION (Decision 3) | No approval from GitHub while the coordinator is away | Plan A Tasks 4 and 5 and parts of 2, 3, 6 never built ("4,000 lines" unverified) | 60 |
| C13 | KEEP | n/a (Task 16 is itself a deletion; Q39 settled) | n/a | 80 |
| C14 | MODIFY: run the throwaway `worker-start`/`ask`/`reply` test before Plan A Tasks 4 to 6 | Delays Plan A; needs a live-test grant | Fixtures from real Orca | 65 |
| C15 | CUT `slo_numbers` and its test | Docs and the hand step FU-10 lose their tool (docs cite it: `issue-watcher-setup.md:470`, `:680`; `issue-watcher.md:232`, `:867`, `:902`) | 48 source lines and a 421-line test | 75 |
| C16 | CUT (stop spending owner time) | None | Owner time | 90 |
| C17 | CUT; NEEDS AN OWNER GO | Decision Desk must restore it from git; reverses the 2026-11-08 staged direction | Q9, Q30 and the gate constant disappear | 55 |
| C18 | CUT (write snapshot only with `--snapshot`) | A future reader must pass the flag | Stops a 387,625-byte rewrite with fsync every 15 s | 75 |
| C19 | MODIFY (add the caveat; keep the stub) | Small change to merged, reviewed code | Report stops saying "none working" falsely | 70 |
| C20 | CUT the design effort | v2 stays undefined | No brainstorm spend before a real collision | 75 |
| C21 | MODIFY: delete the constant and its tests only together with C17; KEEP the owner-written rule | Removing the rule removes the owner's own control | Removes the source of Q7 and Q8 | 80 |
| C22 | KEEP | n/a | n/a | 70 |
| C23a (new) | DEFER, then delete the watcher package if the hand-run launch has not happened within 30 days; NEEDS AN OWNER DECISION (Q35 B1b uses it) | Route B's claim path must be rebuilt | 4,795 source lines (checked) plus about 19,700 test lines (unverified) | 60 |
| C24 (new) | CUT: carry out the owner's 2026-11-16 retirement of `/sc:task` and the task-builder commands; NEEDS ITS OWN GO | Routing guide level 4 and global CLAUDE.md need edits | Two obsolete command chains retired | 60 |

Final list: C16, C04, C03, C06, C02, C01, C15, C18, C20, C05; then with owner decisions: C12, C17 (taking the C21 constant with it), C24.
Biggest single risk: C12 goes against an explicit owner decision (Decision 3 plus the agreed comment rules), and nothing can be approved while the coordinator is down.
