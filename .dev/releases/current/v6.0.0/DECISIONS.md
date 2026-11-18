# Release decisions (6.0.0)

Source of the numbered rows: the decision table in IronClaude issue 571. Times are UTC where known.

| # | Decision | Answer | Decided by | Date |
|---|---|---|---|---|
| 6.1 | Version 6.0.0 (a major version) | **Proposed 6.0.0.** Work proceeds on it. Ryan's confirmation is still open; asked once on issue 571 on 2026-11-18 03:15Z (https://github.com/IronbellyOrg/IronClaude/issues/571#issuecomment-6967825967), recommendation yes. | Ryan, Clay | OPEN |
| 6.2 | `integration` branch or a `release/6.0.0` branch | **`integration`.** Branch created from master at `8c21ac41f`; kept by Clay | Ryan, Clay | 2026-11-16, kept 2026-11-17 |
| 6.3 | Are the task and documentation bundle (Part B) and the agents (Part C, issue 572) in 6.0.0 | **Part B: answered by Clay, 2026-11-18 16:37 UTC (relayed by GeneralIronFlow): Part B is part of release six but ships as an update, 6.1.0, not in 6.0.0;** tracked by a new issue GeneralIronFlow files (number recorded in PROCESS-LOG entry 33). **Part C (agents, #572): not decided yet;** nothing in it was mapped or changed, and the release notes say the agents evaluation is not part of 6.0.0. (I asked Ryan once on issue 571 on 2026-11-18 03:15Z; he has not answered, and Clay decided Part B himself.) | Clay (Part B); Ryan, Clay (Part C) | Part B 2026-11-18; Part C OPEN |
| 6.4 | Open PR 570 (ccsession) | **Merge it.** Merged as `8c21ac41f` | Clay | 2026-11-16 |
| 6.5 | Tag on green | **Yes.** If G1 to G9 pass on the release PR's merge commit, tag `v6.0.0`, push the tag, publish the GitHub release without asking again. A failed check stops and goes to Clay. Then `/sc:post-release v6.0.0` | Clay | 2026-11-16 |
| 6.6 | Scope of `/sc:post-release v6.0.0` | **OPEN.** Asked once on issue 571 on 2026-11-18 03:15Z (same comment). Recommendation: docs sync and the install and upgrade runs only, no new hand-test guides for removed items. Known docs work for it: `docs/getting-started/upgrading.md` still says 5.0.0 in its title, `@v5.0.0` and its counts | Ryan, Clay | OPEN |
| 6.7 | Where the approved small fixes ship | **Option A: in 6.0.0, on `integration`.** Items: #505, #506 (cleanup half only; the improve half goes with PR 8), #510, #536 (fix the false promise only), #542, #543, #544, #545 | Clay | 2026-11-16 |
| W1 | Start wave 1 (PRs 1, 2, 5) | **Approved** | Ryan | 2026-11-17 07:27 |
| S1 | Swarm | **Stays, with its attached skills** (`cli/swarm`, `/sc:swarm-wizard`, `sc-swarm-wizard-protocol`, `sc-bare-review`, `docs/swarm`, `tests/swarm`, swarm CI jobs). PR 3 dropped. G8 (c) and (e) dropped | Ryan | 2026-11-17 13:06 |
| S2 | Snapshot fork and where `/sc:review-translation` moves | **`ironbelly/IronClaudeV5`** (created 2026-11-16 17:34Z) | Ryan | 2026-11-17 18:32 |
| S3 | Keep `integration` | **Kept.** Every removal PR targets it; master is reached only by the release PR | Clay | 2026-11-17 |
| S4 | How PRs are merged into `integration` | **Orchestrator merges without asking** when every check is green, Augment and Codex have finished on the final head, and no review thread is open | Clay | 2026-11-17 |
| S5 | Historical records | **Not edited** (`docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries). One `CHANGELOG.md` entry in the release PR | Ryan (proposed), Clay | 2026-11-17 |
| S6 | Coordinator started by Clay's coordinating session | **Allowed for this session only**, overriding the "a coordinator is person-opened" line in `~/.claude/CLAUDE.md` | Clay | 2026-11-17 |
| S7 | Ryan's request to fold the eight analysis documents into the docs (2026-11-17 14:40), the task and documentation bundle, issue 572's agents, the new repo | **Out of scope for the waves.** Logged in `PROCESS-LOG.md` under "Out of scope, for later" | Clay (brief) | 2026-11-17 |
