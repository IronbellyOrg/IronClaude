# Round 1 advocate: Variant 2 (owner runs the live reads by hand)

Persona: security (authority, attack surface, least privilege). Paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with `D/` (this Q24 folder). ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`.

## Position summary

V2 keeps every live Orca call, and above all OB-03's seeded writes, in the hands of the one actor whose authority needs no delegation: the owner, at a plain terminal the owner opens. Its security case is strongest for OB-03 and for the hand-typed parts of XC-03, and weakest on owner time and on XC-04's need for master code. Judged honestly across all points, V1 (with OB-03 left to the owner, as V1 already says) is the better overall answer; V2's lasting value is the authority rule it pushes into V1.

## Steelman

**V1 (fresh master-based capture session).** Strongest form: a single-purpose agent in a new `origin/master` worktree is the least-privileged *agent* runner available. It has no history, no unpushed commits to protect, no other permission rows, and it runs XC-04's sweep on master code natively (MR line 452 requires "the sweep run as `superclaude sweep run --run <id>` on master code"). It reads `run-current` back at W0 instead of assuming the terminal holds no Run, which is the right response to the unknown D-A (D/adversarial/variant-1-original.md step 2; diff-analysis U-001). It also already leaves OB-03, the only write, with "the owner or a session the owner names" (variant-1 line 5), so it captures V2's best security point. It costs the owner almost nothing, which matters because "Owner latency is the real schedule" (MR line 523). This is a genuinely strong design.

**V3 (the 409 session).** Strongest form: it is the spec's own recommendation (MR line 551; ADJ line 794), and the session that wrote the observer's parser is the reader least likely to misread `dispatchId` values or `projection.attention` fields. One runner for all observer-tied live work gives one clean actor in the records. V3 is also candid: it states that "one sitting" no longer holds (variant-3 line 24) and keeps the three permission rows separate (line 25).

## Strengths claimed

1. **No delegated live authority; nothing to launder.** Under V2 "a person, not an agent, makes every live Orca call, so no permission row is delegated to an agent for live reads" (variant-2 line 16). MR already plans each agent action behind a per-item row (`GRANT(XC-03,live-read)`, `GRANT(XC-04,live-read)`, `GRANT(OB-03,seeded-write)`; MR lines 451, 452, 966, 967). Those rows are instructions, not fences: on this host live `claude` runs with `--dangerously-skip-permissions --allowedTools=Grep` and both permission knobs are unset (ADJ INV-011). An agent told "read verbs only" in that mode can still type any verb. The owner is the one actor for whom the question "who authorized this?" has no second hop.
2. **OB-03's writes belong with the owner.** OB-03 is the only item that writes (seeded messages into a throwaway Run; MR line 251, line 575: "Q24's read capture does not authorize seeded message writes"). ADJ names "the owner or the 409 session" as its runner (ADJ lines 192, 459, 470), and the gate's pass record must be owner-written (ADJ line 192 (d), INV-014: "the owner supplies it"). When the owner runs the test, the actor and the author of the pass record are the same person; evidence and authority do not split.
3. **V2 avoids D-A by construction.** Whether `orca agent launch` binds a Run is unknown (MR line 128; D/question.md line 36). V1 and V3 both depend on an agent terminal that holds no Run. V2 uses the arrangement that has actually been exercised: Q-1 was run from "A plain Orca terminal spawned by the owner for this test: it has a terminal handle ... and holds no Run" (`.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/q1-result.md`, "What was run"). That is the only recorded precedent for "a terminal that holds no Run".
4. **No dependence on the 409 session and no risk to its worktree.** The 409 session's survival is UNVERIFIED (D/question.md line 31), and the `issue-409-mvp` worktree holds unpushed commits and records that must survive until OB-01 (MR lines 234, 264). V2 touches neither (variant-2 line 17).
5. **Smallest new attack surface.** V2 creates no worktree, no agent, no new session holding live rows. V1 adds one worktree plus one agent to create, track and remove (variant-1 lines 13, 23); V3 concentrates three rows, one of them a write, in one long-lived session (variant-3 line 25).
6. **XC-04's tools are already mechanically fenced, so a hand run of XC-04 is low risk.** The sweep only runs ten allow-listed Orca templates (`src/superclaude/cli/sweep/probes.py:49-60`, NFR-014), and the observer refuses `check`, `--ack`, `--wait`, `run-use`, `run-create`, `send` and more by prefix (`src/superclaude/cli/observe/adapter.py:34-50`). The owner typing `superclaude sweep run --run <id>` and the observer command cannot drift into a consuming call. This narrows V2's own "hand-typed drift" risk (variant-2 line 23) to XC-03's raw Orca reads.

## Weaknesses identified in other variants

1. **V1 and V3: read-only is policy, not mechanism, for XC-03.** XC-03's reads (attention values, `worktree ps` agent row, Orca's event help, build string; MR line 451) are raw Orca commands outside both programs' allow-lists. An agent running them under bypass permissions (ADJ INV-011) is fenced only by its prompt. One plain `check` consumes messages (ADJ line 192 (b) treats consumption as the open risk). V2 has the same exposure in principle, but a person reading a written procedure is the authority the row would have come from anyway.
2. **V1 and V3: D-A is a live risk they must detect, not avoid.** V1 admits it ("If a launched agent's terminal is bound to a Run (D-A), the session must use a different plain terminal or the capture is held", variant-1 line 25). V3 relies on an existing agent session whose terminal binding is unknown (variant-3 line 29). Both need the XC-10 (1) read-back (MR line 458) before anything runs.
3. **V3: one session holds three rows including a write, in a worktree that must not be disturbed.** V3 concentrates `live-read` x2 and `seeded-write` in one actor (variant-3 line 25) whose worktree is on an unmerged branch with `origin/master` not an ancestor (MR line 234), so XC-04's "master code" requirement forces it to "run the installed CLI or switch code" (variant-3 line 23). Switching code in that worktree endangers the unpushed records OB-01 protects (MR line 264). That is the widest blast radius of the three.
4. **V3: its availability is unverified and its fallback is "nothing runs".** If the 409 session has ended, V3 "falls back to the default (nothing runs)" (variant-3 line 22; MR line 551 default: "XC-03, XC-04, OB-03 do not run; V2-02 cannot pass").
5. **V1: OB-03 is left open.** V1 "only names the owner's default" for OB-03 (variant-1 line 31). That is safe but not an answer; V2 answers it.

## Concessions

1. **Owner time is V2's decisive weakness.** Three live sittings (variant-2 line 22) cost the scarcest resource in the program (MR line 523). V1 and V3 cost the owner almost nothing.
2. **XC-04 under V2 has no defined master-code environment.** XC-04 must run the sweep "on master code" and record `--root` and the report path; the sweep writes `<root>/.dev/sweeps/` (MR line 452). V2 does not say which checkout the owner uses (diff-analysis C-003). V1 fits this natively.
3. **The authority gain is smaller than it first looks.** MR already gives each agent action its own owner-recorded `GRANT` row (MR lines 966-967), and the owner can approve a narrow, allow-listed procedure. The real residual risk is limited to XC-03's raw reads, and an agent can be handed the same written procedure the owner would follow.
4. **Pasted records cannot be re-run by an agent** (variant-2 line 24). An agent-run capture is no more re-runnable against live state, but it does keep exact command lines and exit codes automatically.
5. **V1 already contains V2's best point.** V1 leaves OB-03 with the owner by default (variant-1 line 5). Combined with V1's read-back of `run-current`, V1 delivers most of V2's security value at a fraction of the owner time.

## Shared assumption responses (A-001)

**A-001: QUALIFY.** Q-1 does not show that a Run-less terminal cannot run `worker-list --run <id>`. Q-1 tested one verb, `orca orchestration check --all --types question --run run_c1badaa6576b --json`, and got `consumer_fenced` (q1-result.md, "What was run" and "Observed"). It never tested `worker-list`. The sweep is designed for an unbound terminal: when `run-current` reports no binding it raises "no Run bound: pass --run <id>" (`src/superclaude/cli/sweep/probes.py:365-375`) and then calls `worker-list --run <run> --json` (`probes.py:51`, `:1047`). Sweep reports on disk show `orca worker-list run_a4723d345399 read` (`.dev/sweeps/20261112-034511-sweep.md` line 4), but they do not record whether that terminal was bound to that Run, so the Run-less case is UNVERIFIED. The observer's default worker-list has no `--run` and returns host-wide rows (513 rows on this host, ADJ INV-017; template `adapter.py:29`), so it can list a Run's `dispatchId` values without being bound. ADJ's Q-1 gloss "an unbound terminal cannot read another terminal's Run" (ADJ line 87) is broader than the evidence. The assumption is not refuted, but no variant may treat it as settled. Whoever runs XC-03 and XC-04 should first read back one `worker-list --run <id>` from the Run-less terminal and record the result. The same check applies to all three variants.

## Per-point verdicts

| Point | Superior | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| C-001 | V1 | A fresh master-based agent avoids the 409 dependency and costs little owner time; V2's authority gain is real but mostly covered by the per-item GRANT rows. |
| C-002 | V2 | The only write (seeded messages) and its owner-authored pass record (INV-014) belong with the owner; V1 defaults the same way but leaves it open. |
| C-003 | V1 | A master-based worktree meets XC-04's "master code" requirement natively; V2 leaves the checkout unspecified and V3 must switch code. |
| C-004 | tie | V1 and V2 both leave the `issue-409-mvp` worktree untouched; V3 alone carries the risk. |
| C-005 | tie | V1 and V3 both cost the owner little; V2 costs three sittings. |
| X-001 | V2 | From a least-privilege view, no agent holding live rows is the strictest answer, given bypass permissions on this host (INV-011). |
| X-002 | V1 | A clean single-purpose runner beats familiarity; observer output can be read from a written procedure, and familiarity does not offset the worktree risk. |
| X-003 | tie | All three agree "one sitting" no longer holds; V3 states it most plainly. |
| A-001 | tie | All three share the unstated assumption; none checks `worker-list --run` from a Run-less terminal. |

Overall: V1
