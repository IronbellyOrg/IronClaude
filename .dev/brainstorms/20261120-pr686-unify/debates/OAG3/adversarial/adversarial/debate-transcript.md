# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 68.4% (13 of 19 diff points agreed)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Advocate 1 for Variant 1 OURS, agent id ac5e1c5664a312ce7; Advocate 2 for Variant 2 CLAY, agent id a13a546f8a318c340; both general-purpose agents, read-only)
- Taxonomy coverage (AD-5): L1 covered (S-001, S-002), L2 covered (9 points), L3 covered (8 points). No forced round needed.
- Omission check (A-NNN): both advocates answered A-001 to A-005. No omissions.
- Orchestrator verification: the one new fact the advocates produced (the widened NG-2 test at `tests/issue_watch/test_security_invariants.py:1059-1079` in planb) was read by the orchestrator and matches: `_WRITER_MODULES = {"complete.py", "repo_init.py"}`, `_WRITE_SIGN` includes `"label", "create"`, and `github.py` and `cycle.py` must stay clean.

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)
**Position**: Planb enables a repo only after its checks pass, and the poll cycle is already separate from init in code, so the switch-on should stay automatic once the owner has given the single S17 go. The advocate concedes V2 is stronger on today's evidence: MR lines 91 and 361 say the init label write needs the owner's chat OK, and the S17 proof has not happened.

**Steelman of Variant 2**:
The owner's own rule is that every GitHub write and every switch-on is named by the owner in chat (MR line 91; MR line 416 says no config is switched on before S17). One throwaway repo proves the chain once but not that another repo has the same shape. The brake chain is thinner than V1 says: `GOVERNED_LEVELS_ALLOWED` is one constant, INV-025 says the guard reads command text only, the X-001 claim route is unrun, and Coder 516 is not landed. The cost is small (one defaults key, two tests, MR lines 353 and 503). It keeps "the poll writes nothing" literally true wherever an unattended process runs and it stages risk.

**Key strengths claimed**:
1. Reach is bounded in code: `BUILTIN_ALLOWED_OWNERS = ("IronbellyOrg",)` (`defaults.py:30`), `foreign_owner` skip (`repos.py:141`).
2. Generation is a filter: no Project, unmapped several Projects, unreadable or empty approvers all skip (`generate.py:192-250`).
3. Fail-safe is built: `done()` writes `enabled: true` only when no step failed and `_enable` succeeded; a failed check leaves the config off and writes a report; idempotent (`first_run.py:125-173`, `first_run.py:136-137`).
4. The code already splits cycle from init: `trigger_label_state` "reads only, never creates (the cron loop, R14)" (`repo_init.py:93-94`); `ensure_trigger_label` "Only the first run calls this" (`repo_init.py:108-117`).
5. Being enabled launches nothing: a launch needs the per-issue approval (D01, OA-1); `GOVERNED_LEVELS_ALLOWED = False` (`launch.py:48`); the first-run report prints the gate (`first_run.py:163-168`).
6. Default-on matches the owner's recorded line: R17 "nothing in the setup is manual", R18 `enabled: true`; K24 records "R18 default-on after the throwaway run" as a live owner option (MR line 326).
7. V2's strict rule is narrower than Clay's own design, where the poll writes `hold:plan` (D:410, 436-445).

**Weaknesses identified in Variant 2**:
1. Its own Costs section admits the manual per-repo step and the "not zero" setup, which R17 forbids.
2. NG-2's flat wording belongs to the poller: `docs/designs/issue-watcher.md:48` says the NG-2 test "covers the poller only"; V2 reads line 76 more broadly.
3. A per-repo go does not follow from "shadow run first": `run-all --dry-run` (`dispatch.py:406-410`) already writes nothing.
4. A key that defaults off and is never flipped makes the zero-setup plan a one-repo plan (V2's own Risks section).
5. Its fact 8 cuts both ways: with Coder 516 missing every repo reports `worktree_invalid` and stays off (MR line 577); auto-enable is inert, not dangerous.

**Concessions**:
- X-002 is real: the Claim ("behind the owner's chat OK before the first real run") conflicts with the Costs section ("without a fresh chat go"). Reconcilable only if the S17 go is a class-level go covering later repos' label creation; MR lines 91 and 361 do not say that, so on the merged text V2's reading is closer.
- Label creation is not gated by "checks pass": `ensure_trigger_label` runs at step 2 (`first_run.py:193`), before the dry-run, lock and restart checks; a repo that later fails still has a label.
- `hold:backlog` creation is not built in planb; D09 rule 2 and K18 expect both labels.
- `auto_enable` does not exist in planb (`_enable` runs unconditionally on a pass, `first_run.py:152-153`); the key is NOT BUILT (MR line 353) for either position.
- The brake chain has real holes (INV-025, unrun X-001), so "layered brake" overstates until S17 runs.
- One throwaway run proves one repo's shape, not every later repo's (A-002).

**Shared assumption responses**: A-001 QUALIFY (pass criteria must be written before the run: six checks, the X-001 live check, a recorded owner go). A-002 QUALIFY (only for repos that pass generation and the worktree check). A-003 QUALIFY (registration signals intent only inside the owner and generation filters). A-004 QUALIFY (needs a visible report; `first-run.txt` is written but nobody is told). A-005 ACCEPT (re-check cited lines after the rebase).

### Variant 2 Advocate (CLAY)
**Position**: OA-28a is where V2 is strongest: `auto_enable` ships as a defaults key defaulting to false; the owner flips it only after the S17 throwaway run is a real proof; a repo that passes its checks does not switch itself on before that. The advocate concedes most of OA-28b: planb's widened NG-2 test already permits `repo_init.py` as a writer, so the strict reading is not defensible; only a narrower "do not add a second setup write path" argument survives.

**Steelman of Variant 1**:
The owner decided this in R17 and R18 on 2026-11-18 ("Nothing in the setup is manual"; config created `enabled: true`), repeated in memory `zero-setup-watcher-decisions`. V1 has five real layers: reach (`defaults.py:30`, `repos.py:141`), generation filters (`generate.py:192-250`), failed checks keep it off (`first_run.py:16-17`), start gate (per-issue approval plus `launch.py:48`), and a label write that is one idempotent `gh label create` behind a read with the cycle read separated from the init write (`repo_init.py:93-112`). A per-repo chat go adds a manual step to a path that already needs a human decision before work starts. The strongest single piece is the NG-2 test `test_only_complete_and_repo_init_may_write_to_github` (`tests/issue_watch/test_security_invariants.py:1059-1079`): it already carves out `repo_init.py`, includes `"label","create"` in `_WRITE_SIGN`, and keeps `github.py` and `cycle.py` clean.

**Key strengths claimed**:
1. Switch-on is a write the poll process makes itself: `run-all` goes `ensure_config` then `first_run` (`dispatch.py:411, 417`), which rewrites `enabled: true`; K24 says landing planb and scheduling cron "would, with no per-repo go, write a label to GitHub and switch every new repo on" (MR line 326), which conflicts with "no config is switched on before S17" (MR line 416).
2. The dry run proves the order only if switch-on waits: `dispatch.py:406-410` says generating "writes files and calls GitHub", so a dry run only reports; default-on makes the first real `run-all` the first test for every repo.
3. The brake is thinner than V1 says (partial): constant gate (D14 verdict line 58; `launch.py:48`), INV-025 (MR line 28), V1 admits a Pipeline None claim session still comments and assigns, X-001 unrun (MR lines 311, 550), Coder 516 not landed (MR line 577).
4. The key is cheap and reversible: one defaults key plus two tests (MR lines 353, 503); flipping to true after S17 is a one-line change; choosing the key is not choosing "manual forever".
5. Not building a second setup write path is a fair YAGNI point: planb creates only the trigger label (`first_run.py:193`); `hold:backlog` creation is not built; Clay's D:445 creates it once per repo by hand.

**Weaknesses identified in Variant 1**:
1. Internal contradiction X-002: `run-all` is unattended, so only the S17 repo gets a chat OK; for later repos the claim's wording is false.
2. The layered brake is partly aspirational: `worktree_invalid` safety net (516) missing today; one-constant gate; a wrongly enabled repo still lets a claim session comment and assign, and a posted comment cannot be unposted.
3. One throwaway repo is a thin proof: neither paper defines "passed" (A-001); shape assumed to hold for all later repos (A-002).
4. It leans on R18 as settled while its own staging key admits R33-before-R18 is open; K24 records default-on as the owner's alternative, not a closed decision.

**Concessions**:
- X-003 conceded: fact 3 overreached; the pinned tests scan the cycle, and the Task 12 test (`:1059-1079`) permits `repo_init.py` as a writer; OA-28b goes to V1.
- X-004 conceded: D:1125 governs live tests of PR B in throwaway `orchestrator-e2e-<n>` repos, not production switch-on; the valid Clay evidence for "by hand" is D:445 only.
- Strictness is narrower than Clay's own design (the poll writes `hold:plan` there).
- R17 and R18 are the owner's recorded decision; V2 needs the owner to accept R33 and S17 first, then the default flips.
- With `auto_enable` false and a read-only label step, a new repo's label check cannot pass until someone creates the label by hand; that step is manual too and V2's paper under-costs it. An idempotent, reversible, owner-filtered creation is low risk, so strictness on labels buys little.

**Shared assumption responses**: A-001 QUALIFY (define "passed": six checks, one shadow `run-all --dry-run`, at least one real poll cycle with a recorded owner go). A-002 QUALIFY (only as far as `generate.py` enforces the shape and records a skip). A-003 QUALIFY (inside the allowed-owner filter; registration is not an owner decision). A-004 QUALIFY (cheap to reverse only if self-enabled repos are reported to the owner; a posted comment cannot be undone). A-005 QUALIFY (cite symbols, re-verify after the rebase).

## Round 2: Rebuttals
Skipped: depth=quick.

## Round 3: Final Arguments
Skipped: depth=quick.

## Scoring Matrix

Per-point positions: Adv1 = Variant 1 advocate, Adv2 = Variant 2 advocate. Agreement needs both to name the same superior approach (two advocates, so a 2/3 majority means both).

| Diff Point | Level | Adv1 | Adv2 | Winner | Confidence | Evidence Summary |
|------------|-------|------|------|--------|------------|-----------------|
| S-001 | L1 | HYBRID 50 | HYBRID 50 | HYBRID | 50% | Same sections; list length is cosmetic. |
| S-002 | L1 | HYBRID 50 | HYBRID 50 | HYBRID | 50% | Same two questions, different framing. |
| S-003 | L2 | HYBRID 60 | V1 70 | Unresolved (leans V1) | 55% | V1 cites code and tests; V2 cites requirement rows. |
| C-001 | L3 | HYBRID 60 | HYBRID 60 | HYBRID | 60% | Key ships false until S17 (V2); one owner flip afterwards, no per-repo go (V1 end state); `first_run.py:152-153`, MR line 416, R18. |
| C-002 | L2 | V1 70 | V1 75 | V1 | 82% | `repo_init.py:93-117` splits read from write; NG-2 test at `test_security_invariants.py:1059-1079` carves out `repo_init.py`; V2 conceded (+10). |
| C-003 | L3 | HYBRID 60 | V1 60 | Unresolved (leans V1) | 58% | Filters and checks are real; INV-025 and X-001 are residual risk (both say so). |
| C-004 | L2 | HYBRID 55 | V2 55 | Unresolved (leans V2 or HYBRID) | 55% | `hold:backlog` creation is not built; D:445 has it by hand; V1 admits "a small addition is needed". |
| C-005 | L2 | V2 60 | HYBRID 65 | Unresolved (resolves under C-001) | 60% | Both want the key; dispute is default and who flips it. |
| C-006 | L3 | V2 65 | V2 55 | V2 | 62% | V1 silent; with the key false the label step is read-only; cost: label check stays red until the label exists. |
| C-007 | L2 | V1 70 | V1 65 | V1 | 68% | R17 and R18 say nothing manual; V2's Risks section concedes "not zero". |
| X-001 | L3 | HYBRID 55 | V1 60 | Unresolved (leans V1) | 57% | `launch.py:48` exists; "only a constant" caveat stands. |
| X-002 | L3 | V2 75 | V2 75 | V2 | 85% | V1 conceded the Claim contradicts its Costs; MR lines 91, 361 require the OK (+10). |
| X-003 | L2 | V1 65 | V1 85 | V1 | 88% | Pinned tests scan the cycle; V2 conceded (+10). |
| X-004 | L2 | V1 65 | V1 85 | V1 | 88% | D:1125 is about live tests in throwaway repos; V2 conceded (+10). |
| A-001 | L3 | HYBRID 70 | HYBRID 70 | HYBRID | 70% | Both QUALIFY: write the S17 pass criteria first. |
| A-002 | L3 | HYBRID 70 | HYBRID 65 | HYBRID | 67% | Generalizes only as far as `generate.py` and the worktree check enforce the shape. |
| A-003 | L2 | HYBRID 65 | V1 60 | Unresolved (leans V1) | 62% | Owner and generation filters bound what registration reaches. |
| A-004 | L3 | HYBRID 65 | HYBRID 60 | HYBRID | 62% | Cheap reversal needs an owner-visible report of self-enabled repos. |
| A-005 | L2 | HYBRID 75 | HYBRID 70 | HYBRID | 72% | Cite symbols; re-verify planb lines after the rebase. |

## Convergence Assessment
- Points resolved: 13 of 19
- Alignment: 68.4%
- Threshold: 80%
- Status: NOT_CONVERGED (max rounds reached for depth quick)
- Taxonomy coverage gate: passed (L1, L2, L3 all covered)
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick)
- Unresolved points: S-003, C-003, C-004, C-005, X-001, A-003 (every one leans toward V1 or toward the HYBRID that C-001 already defines; none leans toward a pure V2 outcome on OA-28b)
