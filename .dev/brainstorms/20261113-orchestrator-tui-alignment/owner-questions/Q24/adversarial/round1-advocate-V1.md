# Round 1 advocate: Variant 1 (fresh master-based capture session), persona devops

Paths: D = `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q24`; MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; PROBE = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/invariant-probe.md`. All reads were made in this round; no Orca command was run.

## Position summary

The live reads (XC-03 in W1, XC-04 in W3) should be run by a fresh top-level agent in its own `origin/master`-based Orca worktree. That runner can be created on demand, matches XC-04's "master code" requirement by construction, and cannot damage the unpushed `issue-409-mvp` evidence if it fails or is cleaned up. The seeded test (OB-03) stays a separate owner-named grant, as MR line 575 requires.

## Steelman

**Variant 2 (owner by hand).** Its strongest form: live Orca on this host is shared state that the owner alone is accountable for, and every past live surprise (Q-1 fenced; 35 of 53 Runs rebound, ADJ line 459) argues for the smallest possible set of actors. With the owner making every call, no `GRANT(...,live-read)` row is delegated to an agent (variant-2 lines 16-17), there is no new worktree to create or clean, and it matches ADJ's own phrasing "owner or 409 session" for the seeded test (question.md facts table; ADJ lines 192, 459, 470). It also sidesteps D-A, because a person's plain terminal is known to hold no Run. That is a real simplification. Critique: it spends the one resource MR line 523 calls the schedule ("Owner latency is the real schedule") on three sittings, and it fixes no code revision for XC-04 (diff-analysis C-003: "Owner's environment, unspecified"), while MR line 452 requires the record to name "the executable revision, `--root`, and the report destination". Pasted output also cannot be re-run by a checker (variant-2 line 24), which weakens a record that V2-02 depends on.

**Variant 3 (the 409 session).** Its strongest form: it is the spec's own recommendation (MR line 551; ADJ line 794); the 409 session built the observer's parser and adapter (`observe/parse.py`, `observe/adapter.py`) and knows which `dispatchId` and `projection.attention` fields matter; and one runner for all observer-tied live work keeps the audit trail to one actor (variant-3 lines 16-17). It is also honest about its limits: it states that "one sitting" no longer holds (line 24) and that its survival is UNVERIFIED (line 22). Critique: the recommendation predates the move of XC-04 to W3 (MR line 861, "the JOIN comparison moved to W3, Change 7"), so its "one sitting" premise is gone. Its worktree is on an unmerged branch where "`origin/master` is not an ancestor of that HEAD" (MR line 234), so XC-04 on "master code" forces either an installed CLI of unstated provenance or a code switch inside a worktree that holds the only copy of the owner's pass record in unpushed commit f104ca51a (PROBE INV-001) and untracked `owner-decisions-20261108.md` and `live-test-guide.md` (PROBE INV-002). MR line 264 calls cleaning that worktree before OB-01 "Evidence loss". And if the session has ended (UNVERIFIED), the default is that nothing runs (MR line 551).

## Strengths claimed

1. **Revision fit for XC-04 by construction.** MR line 452 requires the sweep "as `superclaude sweep run --run <id>` on master code (never the unfixed sweep)" and a record naming "the executable revision, `--root`, and the report destination". A worktree created from `origin/master` and rebased after #539 merges gives one `git rev-parse HEAD` as the revision and the worktree path as `--root`. Variant 3 must run code from a revision other than its checkout's (variant-3 line 23); variant 2 leaves the environment unspecified (diff-analysis C-003).
2. **Blast-radius isolation.** The only copy of the owner's pass record is in unpushed commit f104ca51a (PROBE INV-001), and several records are untracked (PROBE INV-002). A sweep run with that worktree as `--root` runs `git status --porcelain=v1 -z --branch --untracked-files=all` there (`sweep/probes.py:65-67`) and writes a report into its `.dev/sweeps/` (`sweep/commands.py:237-241`). Variant 1 puts all of that in a disposable checkout; nothing touches `issue-409-mvp` (variant-1 lines 18-19).
3. **Availability is produced, not assumed.** XC-10 item (1) requires that "the Q24 runner is confirmed live" (MR line 458). Variant 1's runner is created at W0 by the coordinator through the sanctioned path (`orca worktree create ... --agent claude`: CLAUDE.md "Parallel Development with Git Worktrees"; MR line 457 item (3)), so this check can pass on demand. Variant 3's runner may not exist (question.md: "Whether the 409 session is alive today is not checked here", UNVERIFIED).
4. **Reads binding state instead of trusting it (U-001).** Variant 1 is the only proposal that names D-A as a risk to the runner itself and requires `run-current` to be read back before any capture (variant-1 line 10; diff-analysis U-001, rated High). This matters because the sweep without `--run` calls `bind_run` (`sweep/commands.py:264-266`, `sweep/probes.py:365-375`), so the terminal's binding state changes what the tool does.
5. **Correct actor type for the sweep.** `/sc:sweep` is on the never-as-worker list (`core/WORKER-CONTRACT.md:23`). Variant 1 uses a top-level agent made with `worktree create --agent`, not a supervised worker, and runs the CLI `superclaude sweep run`, so no worker-contract rule is bent.
6. **Keeps the seeded-write grant separate.** MR line 575: "Q24's read capture does not authorize seeded message writes". Variant 1 does not bundle OB-03 into the capture runner (variant-1 line 5), so the read-only session never holds a write row.
7. **Low owner cost.** One grant row per item and one W0 confirmation; no owner sittings (diff-analysis C-005: Low).

## Weaknesses identified in other variants

1. **V3: stale premise.** Its answer is ADJ's "one sitting" recommendation, but MR lines 451-452 and 861 split CAP (W1) and JOIN (W3). Variant 3 concedes this (line 24) yet keeps the runner chosen for the old premise.
2. **V3: master-code conflict on an evidence-bearing worktree.** MR line 234 ("`origin/master` is not an ancestor of that HEAD") plus MR line 452 ("on master code") means XC-04 cannot run from the 409 checkout as it is. Switching code there risks the unpushed f104ca51a and the untracked records (PROBE INV-001, INV-002; MR line 264). Running the installed CLI instead leaves the revision to whatever `superclaude` is installed, which the record must still name.
3. **V3: single point of failure with a do-nothing default.** If the 409 session has ended, MR line 551's default applies: "XC-03, XC-04, OB-03 do not run; V2-02 cannot pass". Variant 3 accepts that (line 22) and supplies no fallback runner.
4. **V3: one terminal holds a write row and two read rows.** Variant 3 gives the 409 session `GRANT(OB-03,seeded-write)` too (line 11). The rows stay separate, but the same session creates a throwaway Run (`run-create`) and later runs reads; if its terminal is then bound to the throwaway Run, later reads are no longer from "a terminal that holds no Run" (MR line 458). Variant 3 records `run-current` around OB-03 (line 11) but does not say to re-check it before XC-04.
5. **V2: unspecified revision and unrepeatable records.** No revision or `--root` is fixed for the owner's XC-04 run (diff-analysis C-003), and pasted output "an agent cannot re-run" (variant-2 line 24).
6. **V2: owner latency on the critical path.** Three sittings (variant-2 lines 9-12) against MR line 523, with V2-02 (issue #423) gated on XC-03 (question.md, "What it gates").
7. **V2: higher procedure-drift risk.** Variant 2 itself names a `check` run by mistake as a risk (line 23); MR line 451 item (6) forbids any `check` in CAP. An agent run can be held to fixed argv shapes, as the sweep already is (`ALLOWED_ORCA`, `sweep/probes.py:49-60`); a person typing commands cannot.

## Concessions

- Variant 1 is more coordinator work: a worktree, an agent, a rebase after #539 merges, and a cleanup (variant-1 line 23).
- The fresh session has no observer history (variant-1 line 24). For XC-03 item (1) (`projection.attention` meaning, D-8) the 409 session's familiarity is a genuine advantage; Variant 1 should hand its runner the observer's own verified field list (`observe/parse.py`, "the verified worker-list keys") to compensate.
- D-A is unresolved for Variant 1 too: if `agent launch` binds a Run to the new agent's terminal, the capture is held until a plain terminal is used (variant-1 line 25). Variant 2 does not have this problem.
- Variant 1 step 5 ("The worktree is removed after XC-04 is recorded", line 13) is a flaw as written: the sweep report lands in that worktree's `<root>/.dev/sweeps/` (`sweep/commands.py:237-241`), and removing the worktree deletes it, the same evidence-loss pattern as INV-002. Fix: copy the report into the always-staged ledger package (MR line 449) before removal and record the copy path.
- XC-03 itself needs no worktree (it runs no git and no sweep: MR line 451, "no TB-GIT: CAP runs no git and no sweep"). The worktree earns its cost only at XC-04.
- Variant 2 has the strongest authority story: no agent holds a live-read grant at all.

## Shared assumption responses (A-001)

**QUALIFY.** The assumption holds for the verbs XC-03 and XC-04 actually use, as far as the record shows, but it is not fully proven.

- Q-1 tested a different verb. The Q-1 failure was `orca orchestration check --all --types question --run run_c1badaa6576b --json`, refused with `consumer_fenced` (`.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/q1-result.md` lines 12 and 19). That is the mailbox read. ADJ line 87 summarises it as "an unbound terminal cannot read another terminal's Run", which is broader than what was tested.
- `worker-list --run` from an unbound terminal was not fenced. PROBE INV-027 records "Live `worker-list --run run_c1badaa6576b`: n=0, `total` 0, `hasMore` false" against the same probe Run on which Q-1 was fenced, and INV-013 and INV-017 record unscoped `worker-list` "from an unbound terminal" returning 100 of 513 rows. PROBE "Method and limits" lists `worker-list` "(unscoped, per Run, and cursor paging)" among its calls.
- Both tools call `worker-list --run` and need no binding when a Run id is given: the sweep skips `bind_run` when `--run` is passed (`sweep/commands.py:264-266`) and its allow-list entry is `("orchestration", "worker-list", "--run", "<run>", "--json")` (`sweep/probes.py:51`); the observer appends `--run` to its worker-list argv without binding (`observe/adapter.py:194-197`) and "never runs run-use and never binds to a Run" (`observe/commands.py:89-90`).
- The qualification: the per-Run read returned zero rows, so whether a Run-less terminal can list a non-empty Run bound to another terminal is still UNVERIFIED (zero rows cannot distinguish "no workers" from "filtered"). XC-04 should record the per-Run `page.total` next to the unscoped count for the same Run, and XC-03 must not use `check` (already forbidden by MR line 451 item (6)). This applies to all three variants equally.

## Per-point verdicts

| point | superior | reason |
|---|---|---|
| S-001 | tie | Same five-section layout in all three. |
| C-001 | V1 | Only runner certain to exist at W0 and to run on master without touching the 409 evidence; V3 has the knowledge edge but UNVERIFIED existence and a revision conflict. |
| C-002 | V1 | Keeps the seeded-write grant away from the read runner (MR line 575) and leaves it to the owner's choice; V3 puts it in the same session. |
| C-003 | V1 | A master-based worktree gives XC-04 its required revision and `--root` directly; V2 is unspecified, V3 needs a code switch or an installed CLI. |
| C-004 | tie (V1, V2) | Neither touches `issue-409-mvp`; V3 carries the risk named in MR line 264. |
| C-005 | tie (V1, V3) | Neither needs owner sittings; V2 adds three. |
| X-001 | V1 | Agents already run read-only Orca calls under fixed argv allow-lists (`sweep/probes.py:49-60`), which is safer than hand-typed commands; V2's purity costs owner time and repeatability. |
| X-002 | V1 | A clean runner on the right revision matters more for a gate record than familiarity, which a handed-over field list can supply; V3 wins only on D-8 interpretation. |
| X-003 | tie | All three accept two sittings; none can restore "one sitting" after Change 7. |
| A-001 | tie | Shared by all three; QUALIFY as above, and the remedy (record per-Run `page.total`, no `check`) is the same for every runner. |

Overall: V1
