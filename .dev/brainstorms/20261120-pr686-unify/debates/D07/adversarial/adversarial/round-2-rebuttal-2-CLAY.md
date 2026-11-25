# Round 2 rebuttal, Variant 2 (CLAY), debate D07

Abbreviations as before (DESIGN, REQ, Q26, PR-A `route.py`). "They" means Clay. Read-only; no GitHub or Orca contact.

## Response to the OURS rebuttal

OURS's hybrid takes the cap, the fail-closed count, restart with resume, the settings keys and an optional org search into the per-project layout. I accept that framing. Its concession on the missing `Coordinator` worktree is fair: it is a prerequisite owned by Coder issue 516 (state UNVERIFIED), and CLAY's orchestrator clone is an equal one. One honest difference: CLAY's prerequisite is one clone per host, OURS's is one worktree per project. Once 516 creates it automatically, OURS needs no manual step. Until then `dispatch.py:280` skips every repo. I accept this as a sequencing risk, not a topology defect.

The OURS spec text for (a) is sound and I accept it. OA decision 2 ("direction accepted, naming NOT decided") supports "a coordinator in every project" and nothing more.

**The adoptable text for C-004 and C-005 is not sufficient.** It drops these safety properties of DESIGN 700-718 and `route.py`:

1. **No double count.** `in_flight` counts a store entry only when "no state file exists yet" (`route.py` line 411, `key not in state_files`) and a key "is counted once" (a set per orchestrator). OURS says "store entries ... plus claim files" with no exclusion, so one issue with both counts twice. That wrongly fills the cap and stalls work.
2. **Write before send.** DESIGN 706 and `route.py` docstring lines 6-9: the entry is saved `pending` with its target before anything is sent. This is what makes the "poll killed between routing and delivery" test (line 716) safe. OURS counts `pending` but never requires the write order.
3. **Unknown session state decides nothing.** `end_finished` (lines 582, 595-596): when the terminal list cannot be read, nothing is ended or restarted. OURS "if not running, restart" has no such guard, so one failed `orca` read could start a second session beside a live one.
4. **Resume only for acknowledged work.** `route.py` lines 576-580: a dead session with only unacknowledged wakes is left alone, because the resend starts it. OURS says "work in flight" for both, which can send a resume wake on top of a pending resend.
5. **Bounded restarts.** DESIGN 710: the restart "counts as delivery attempt 1 and the 3-attempt rule of DQ2 applies". OURS has no bound on restarts.
6. **Cap limits new work only.** DESIGN 702: an escalated issue that returns counts again, and the cap "limits new routing, not the resumption of work". OURS says the repo "is skipped with reason `coordinator_full`". If that skips the whole repo, it also skips resends and resume at the moment they matter.
7. **Plan requests in the count** (`route.py` lines 414-425). OURS has no hold or plan-request store (I grepped `issue_watch/` on the owner's branch; the only hits are English uses of "holds"), so this applies only if plan requests are carried in. UNVERIFIED.

Fix: add items 1 to 6 to the adoptable text, one sentence each.

## Rejected items: accept or contest

- **Idle end: accept.** REQ R9 says every project always has a running session. DESIGN 710 itself says an ended session "costs no tokens", so the saving is small.
- **Poll starts extra coordinators: accept.** I have no cited benefit that OURS cannot have. A 4th issue waits. Condition: the wait must be visible (a skip reason or an entry), or an issue sits silently. That is a requirement on OURS, not a CLAY win.
- **`wrong_target`: accept.** One session per project plus `check_origin` leaves nothing to refuse. Residual: two hosts that both start `COORD-<RepoName>` share a tag, and `wrong_target` would not help there either.
- **Separate repo, allow list, `cd`: accept.** The allow list's safety job is done in OURS by three gates: R18 turns a repo on only after its first-run check, the approval label and Project Status stay the gate, and each issue needs its own grant row (REQ lines 44, 103). R15 skips foreign owners.

## Does any part of the topology still win

No. I checked the three candidates.

- **Allow list as a safety gate.** DQ8 shows the user is admin on 11 of 48 IronbellyOrg repos and read-only on 35 (DESIGN line 118). That justifies `can_merge` per repo, which OURS already takes from the collaborator role (R4). It does not need a hand-kept list.
- **Two-organization scope.** `allowed_owners` is a list key (`defaults.py` line 38, `repos.py` line 119); the built default is `("IronbellyOrg",)` (line 30). Adding `IronbellyGroup` is one setting. Not a topology benefit.
- **DQ4 `setup-clone`.** It needs the repo named in `repos.yaml` first (DESIGN line 114), a manual act equal to Orca registration. No capability gap.

## New evidence

- `allowed_owners` as above, which moves C-012 to OURS.
- `route.py` lines 576-582 and 595-596 (items 3 and 4); neither Round 1 paper named them.
- DESIGN line 338: a missing orchestrator repo is `orchestrator_repo_invalid`, a cycle failure, so CLAY's prerequisite fails closed, while OURS currently fails by skipping every repo.

## Shared assumptions

- **A-001 QUALIFY:** one host today; the git claim is the cross-host path, the lease comment the last layer in both.
- **A-002 ACCEPT:** six Orca repos, three allow-listed; the 65-call argument is not binding.
- **A-003 QUALIFY:** restart needs tag detection (U25 UNVERIFIED); item 3 above is the guard when the read fails.
- **A-004 QUALIFY:** `O_EXCL` covers one host, a git create-once file acts at push; neither is tested.
- **A-005 QUALIFY:** per-repo listing avoids the 100-item truncation; an org pre-check must fail open.

## Updated verdicts

| Point | Winner | Confidence |
|---|---|---|
| C-004 cap | CLAY, hybrid, with the six properties added | 85% |
| C-005 lifecycle | Split: restart CLAY with guards, idle end OURS | 75% (was CLAY 70%) |
| C-012 org scope | OURS (one setting) | 65% (was CLAY 50%) |
| X-002 seen but not allowed | OURS | 70% (was 65%) |
| All other points | unchanged from Round 1 | as Round 1 |
