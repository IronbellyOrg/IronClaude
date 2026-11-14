# Adversarial Debate Transcript: Q20

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 91% (10 of 11 points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned as separate sub-agents in parallel (general-purpose agent type, current model): Variant 1 qa, Variant 2 security, Variant 3 architect
- Full statements: round1-advocate-1.md, round1-advocate-2.md, round1-advocate-3.md (this folder); summaries below are condensed from them.
- Variant mapping: variant-1 = proposal-A (name no owner yet; hold FU-1), variant-2 = proposal-B (named person owns; person-reviewed top-level sessions), variant-3 = proposal-C (coordinator session owns and reviews)
- Orchestrator spot-check of advocate citations (2026-11-14): `DAY_CAP = 6` at `src/superclaude/cli/issue_watch/cycle.py` line 36 under the comment "module constants, not operator knobs" (line 33); `docs/designs/issue-watcher-setup.md` line 238 (cap fixed in code, a proposal to confirm after the shadow run), line 309 (no runbook command to end a running session), line 571 ("Expect sessions to stay open"); `docs/designs/issue-watcher.md` line 817 (cap "bounds sessions the owner must review"). All confirmed.

## Round 1: Advocate Statements

### Variant 1 Advocate (qa)
**Position**: the failure-producing question is "who ends these sessions", and nothing does: "nothing closes or reaps those sessions" (round2-rebuttal-V2.md line 91); "To end a running session, close it in Orca yourself; this runbook gives no command for that" (setup line 309). But Variant 1 holds the wrong step. Judged Variant 2 best (60%; about 75% with Variant 1's cleanup condition moved to WA-05).
**Steelman of Variant 2**: the spec's answer; matches the design ("a plain process, never an Orca worker", design line 68) and the cap's purpose (design line 817).
**Steelman of Variant 3**: the only variant that puts watcher sessions into a recurring check.
**Strengths claimed**: no unowned-session failure mode; ties ownership to end-of-life; exposes that owning the creation agent is not owning the watcher's later sessions (started by `orca agent launch ... --worktree path:<worktree>`, design lines 619 to 626; whether Orca attributes them to the creator is UNVERIFIED); protects the double-launch guard.
**Weaknesses identified**: Variant 2 assigns a closing duty with no command; launched sessions may stall at the Session Name prompt (WA-04 (h)). Variant 3: the coordinator loop "keeps watching its Run until every Task it created is settled" (WORKER-CONTRACT.md line 288), so ownership lapses when the Run settles; creating the worktree needs a user instruction naming that action (WORKER-CONTRACT.md line 240).
**Concessions**: FU-1 is one session (merged-requirements.md line 306); the 6-a-day exposure starts at WA-05 (line 307); the hold is circular because a cleanup rule needs FU-1's facts.

### Variant 2 Advocate (security)
**Position**: every trust anchor in the watcher points at one human owner: assignee must be the owner's login (setup line 172), bypass mode needs written acceptance (setup line 628), the cap bounds owner review (design line 817). Variant 2 keeps the coordinator, which "performs every outward action" (WORKER-CONTRACT.md line 69), away from transcripts outsiders can influence. Judged Variant 2 best (70%).
**Steelman of Variant 1**: fail-closed; ownership and cleanup are one accountability decision.
**Steelman of Variant 3**: accountability where attention already is.
**Critique of Variant 3**: opens a prompt-injection path into the most powerful session; an agent's review "is not acceptance" (WORKER-CONTRACT.md line 57); review is blind; owner lapses; no contract basis.
**Concessions**: nothing closes sessions under Variant 2 either; adopt Variant 1's pairing as a precondition of WA-05; a read-only count of open sessions in the coordinator's check is acceptable without reading transcripts; a single named person is a single point of failure (name a fallback or disable the schedule while away).

### Variant 3 Advocate (architect)
**Position**: one already-running observer, permitted by the project rule ("The eligible session that creates a worktree owns its agent(s)", CLAUDE.md line 312); but the coordinator's loop is scoped to its Run while the watcher has no end date, a structural mismatch. Judged Variant 2 best (70%).
**Concessions**: lifetime mismatch (decisive); creation-ownership covers one agent, not the stream; contradicts both written recommendations; review is mostly listing; which program's coordinator inherits it is UNVERIFIED; needs an unscheduled WC-16 change.
**Suggested merge**: Variant 2 plus a review cadence for the person and a follow-up on who closes or reaps sessions after FU-1.

## Shared-assumption responses

| Point | Adv 1 | Adv 2 | Adv 3 |
|---|---|---|---|
| A-001 (day cap fixed) | QUALIFY: code constant, but a proposal for the owner to confirm; lowering it is a one-constant code change | QUALIFY: say "the confirmed cap, default 6" | QUALIFY: fixed in code; slower control than it looks |
| A-002 (one shared worktree whatever Q2 says) | QUALIFY: at the default claim level the second agent's ownership gap repeats | QUALIFY: the owner must name who owns `issue-<N>` agents unless Q2 = `--pipeline none` | QUALIFY: holds only under `--pipeline none` |

No omissions.

## Scoring Matrix

| Diff Point | Taxonomy | Adv 1 | Adv 2 | Adv 3 | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | none | 90% | Same five sections |
| C-001 | L2 | V2 65 | V2 75 | V2 70 | Variant 2 | 90% | Person matches the design and the creator rule; V3 advocate conceded |
| C-002 | L3 | V2 55 | V2 60 | V2 65 | Variant 2 | 80% | The cap was sized for owner review (design line 817) |
| C-003 | L3 | V2 60 | V2 70 | V2 70 | Variant 2 | 85% | Unblocks FU-1 without a contract change |
| C-004 | L3 | V1 60 | V1 55 | V3 55 | Variant 1 (2 of 3) | 60% | Only V1 makes cleanup a required decision, at the wrong step |
| C-005 | L3 | V2 55 | V2 60 | V3 60 | Variant 2 (2 of 3) | 60% | States the blind spot without claiming a review it cannot do |
| X-001 | L3 | V2 65 | V2 75 | V2 70 | Variant 2 | 90% | Coordinator loop is Run-scoped; trust boundary; written recommendations |
| X-002 | L2 | V2 70 | V2 70 | V2 65 | Variant 2 | 85% | A person persists and can accept risk |
| X-003 | L3 | V2 60 | V2 60 | V2 70 | Variant 2 | 85% | Gate cleanup at WA-05, not at a one-session FU-1; V1 advocate conceded |
| U-001 | L2 | V1 70 | V1 65 | V1 60 | Variant 1 | 85% | Pairing ownership with end-of-life is the one control on accumulation |
| U-002 | L2 | V2 75 | V2 70 | V2 75 | Variant 2 | 85% | The `.dev/issues/<N>/` runbook note |
| U-003 | L2 | V3 50 | V3 50 | V3 55 | Variant 3 | 70% | Useful only as a read-only count |
| A-001 | L3 | V1 50 | none | V2 60 | split | 50% | All variants missed that the cap is an owner-confirmable proposal |
| A-002 | L3 | V2 50 | none | V2 lean 50 | Variant 2 (2 of 3, weak) | 55% | No variant names the owner of the claim script's second agent |

## Convergence Assessment
- Points in denominator (S + C + X + A): 11. Agreed: 10 (7 unanimous, 3 by 2 of 3). Split: A-001.
- Alignment: 91%
- Threshold: 80%
- Taxonomy coverage: L1 1, L2 2, L3 8 (all covered)
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick)
- Overall verdicts: all three advocates judged Variant 2 best (60%, 70%, 70%); 3 of 3.
- Status: CONVERGED
- Unresolved points: A-001 (the day cap)
