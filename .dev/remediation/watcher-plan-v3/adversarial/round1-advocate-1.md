# Round 1 - Advocate for Variant 1 (opus security)

Base path for all `file:line` citations: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/`. `guard` = `src/superclaude/hooks/scripts/launch-level-guard.sh`. Every line cited below was read in this session, not taken from a variant. Confidence is 0-1 and means "confidence that my stated position is the right call".

## 0. Verified facts (read before arguing)

| Claim | Result | Evidence |
|---|---|---|
| guard:444 is a `case $T in ...` that adds TAMPER, for every governed session (not only bound workers) | CONFIRMED. The comment says "a bound worker" but the block sits under `[ "$LL_GOVERNED" = 1 ] \|\| exit 0` (guard:391), so any session with a store record hits it. | guard:391, 441-444 |
| guard:653 puts `issue create/edit/comment` in SUBMIT with the pr verbs, with no command-position test; guard:654 UNKNOWN is command-position only | CONFIRMED | guard:653-654 |
| guard:790 allows SUBMIT at FS | CONFIRMED. So an FS agent can run `gh issue comment`/`gh issue edit --add-label` today. plan:23 ("keeps refusing issue comments") is false for FS. | guard:790 |
| guard:786 precedence list has no ISSUE/ISSUEWRITE class; unmatched `CLASS:LEVEL` falls to LL-BROKEN (fail closed) | CONFIRMED | guard:786-804 |
| guard is text only | CONFIRMED, the in-code comment says it: "text only; variables and quoting tricks still pass, so the real fix is the L2 layer" | guard:774-775 |
| Store protection does not cover `~/.config/superclaude/` | CONFIRMED: the tamper list names the store, `.claude/settings`, `.claude/hooks`, `.gitconfig`, `.git/config`, `.config/git`. Nothing for `.config/superclaude`. | guard:763-765 |
| Ungoverned sessions exit 0 | CONFIRMED | guard:153-154, 391 |
| Guard version stamp is compared as an exact line by the IR-4 preflight | CONFIRMED: `GUARD_VERSION_LINE = "# launch-level-guard-version: 1"` | guard:10; `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:839` |
| `approval_of` has no exclusion of the launch account: the only actor gates are User type, not `[bot]`, int id, and `in approvers` | CONFIRMED | `src/superclaude/cli/issue_watch/predicates.py:216-223` |
| Both `approval_of` call sites exist where V1 says | CONFIRMED: `_approve` (cycle.py:883) and `_revalidate` (cycle.py:998). `self.account_id` exists (cycle.py:553, 767). | cycle.py:878-892, 998-1005 |
| The hand-written approvers file holds the launch account | CONFIRMED | `.dev/tasks/to-do/TASK-WF-requirements-20261119-012839/source.md:64` (ids 7361222, 193966884, 254764696; account 7361222) |
| Every `_revalidate` failure today raises `revalidation_failed` | CONFIRMED (also via `_rv` default, cycle.py:977) | cycle.py:985-1016 |
| `edited_after_approval` and `revalidation_failed` are both `("skip", 0)` | CONFIRMED, so exit code and store effects are identical; only the audit word differs | `src/superclaude/cli/issue_watch/audit.py:71,80` area (REASON_TABLE rows `edited_after_approval`, `revalidation_failed`) |
| Would `uv run pytest tests/issue_pipeline/test_complete.py` match `*issue_pipeline*complete*`? | YES. Tested with the exact `case` glob in bash: V1/V3 pattern gives TAMPER, V2 pattern gives ok. The existing pattern at guard:444 gives ok. | bash `case` run, plus guard:444 |
| The plan creates `tests/issue_pipeline/test_complete.py` | CONFIRMED | plan:146 (and V1's own Files line) |
| `project_check` after plan Task 1 allows only Research/Spec/Plan/Debug | CONFIRMED (plan text) | plan:34 |
| Current `test_security_invariants.py:915,918,919` pin a literal repo, no `$owner`/`$name`, and no `String!` | CONFIRMED | tests/issue_watch/test_security_invariants.py:915-919 |

Extra pattern tests I ran (bash `case`, same glob forms): `superclaude issue-pipeline plan-hash d complete.md` is refused by V1/V3 and by V2 (all over-match on `*issue-pipeline*complete*`); `python -c "from superclaude.cli import issue_pipeline as p; p.complete.run()"` is refused by V1/V3 and allowed by V2.

## 1. Steelman of the other variants

**V2 (architect).** V2 reads the code as a maintainer who will have to live with it. Its guard change is one line (`'issue '*`) that covers every issue verb by construction, it spots that the stale-host guard (version 1) passes the IR-4 preflight (guard:10, orca_worktree.py:839) and so would keep allowing FS issue writes, and its coordinator-only pattern is the only one that survives running this repo's own tests in a launched session. It also presents the ship gate and the updatedAt problem as options with stated implications, adds an owner observation (Task 3a), and flags every scope increase with `[SCOPE+]`, which makes the plan reviewable.

**V3 (sonnet analyzer).** V3 is the most honest about uncertainty and the cheapest to land. It ranks findings by consequence, lists what it did not verify, gives per-finding rollback, and adds the same-second approval test case (the one-second resolution at predicates.py:257/OQ-37). On Q-4 it picks the smallest edit: all `_revalidate` failures keep the one word they already have (cycle.py:985-1016) and the plan text changes, not the code. Its Q-2 config-key gate is the least code and the easiest for the owner to flip without a PR.

## 2. Points, L3 first

### D-01 Q-1 guard class name and scope (L3)
- **Position.** V1's `ISSUEWRITE` with the explicit verb list plus `label` and `project` writes is the right scope. V2's `'issue '*` is the better *mechanism* (it is future-proof for new `gh issue` verbs). Best result: V2's catch-all `'issue '*` placed after the guard:652 allow row, plus V1's `'label '*` and `'project '*` rows. Reject V3 (create/edit/comment only).
- **Evidence.** guard:652 already lets `view|list|status|diff|checks|watch|checkout` through before the SUBMIT row, so a catch-all after it cannot refuse a read. guard:653-654: V3's narrow set leaves `issue close|reopen|delete|transfer|lock|pin|develop` to the guard:654 fallback, which is UNKNOWN only when `gh` is in command position (`[ "$LL_CP" != "$i" ] || ...`). Out of command position (`flock x gh issue close 5`) they pass at every level. SUBMIT/ISSUE rows have no such condition. For `label` and `project`, the same hole exists (V3's own residual risk cites R17 at tests/hooks/test_launch_level_guard.py:2736).
- **Critique of V2.** V2 is silent on `label`/`project` writes. The plan's own constraint says a launched agent "never changes a Project field" (plan Constraints, line 24 area), and `gh project item-edit` is the way to do it. V2's class leaves that at the command-position-only UNKNOWN fallback.
- **Critique of V3.** Leaves close/reopen/lock and every label/project verb as policy, not enforcement. C-3 stands.
- **Confidence.** 0.8 that V1's scope (with V2's catch-all as the mechanism) beats V2 alone; 0.9 that both beat V3.

### D-02 / C-5 coordinator-only pattern at guard:444 (L3)
- **Position. CONCEDE to V2.** My bash `case` run shows `uv run pytest tests/issue_pipeline/test_complete.py` is refused by `*issue_pipeline*complete*` and allowed by V2's pattern. guard:391 shows the block runs for every governed session, so any Worktree/Full/Full Submit agent working on this repo (which is exactly the kind of agent the watcher launches) cannot run Task 9's own test file. V1's choice is a defect, and V1's own risk note ("over-matches... fails closed, the same way `*record-*` does") understates it: `*record-*` is anchored on the hyphenated verb, `*issue_pipeline*complete*` is anchored on nothing.
- **Where V2 is weaker.** V2's `*issue_pipeline.complete* | *issue_pipeline/complete.py* | *issue_pipeline*import*complete*` misses `python -c "from superclaude.cli import issue_pipeline as p; p.complete.run()"` (I tested it: V2 allows it, V1 refuses it). The guard is text-only (guard:774-775), so no pattern is complete, but V2's list is a negative-space decision: it accepts a known bypass to protect pytest.
- **Merged pattern I would propose.** V2's four alternatives plus `*issue_pipeline*complete.run*`; and write the must-allow case for `pytest tests/issue_pipeline/test_complete.py` into the G2 tests (V2 has it; V1 does not).
- **Confidence.** 0.9 V2 better than V1/V3 on this point. 0.5 that the extra `complete.run` alternative is worth adding.

### D-03 guard version stamp (L3)
- **Position. CONCEDE to V2; V1 omits this.** guard:10 says version 1, and `orca_worktree.py:839` compares that exact line. A host with an older installed guard therefore passes the preflight while still allowing `gh issue comment` at FS, which is the very hole Q-1 closes. A bump to 2 (guard, plugin mirror, `GUARD_VERSION_LINE`, and the tests that pin it) is required for Q-1 to take effect on existing hosts. V3 admits it did not read how the stamp is compared.
- **Security note I add.** The bump is itself a control: without it the fix is silently absent on every host that has not reinstalled hooks, with no failing check.
- **Confidence.** 0.9.

### D-04 Q-1 part B: self-approval by the launch account (L3) - V1's unique point
- **Position.** Keep it. V2 and V3 put it in residual risk. The code shows why that is too weak.
- **Evidence.** (1) `approval_of` accepts any `actor_id in approvers` (predicates.py:216-223) and has no concept of who launches agents. (2) The approvers file for this host contains the launch account 7361222 (source.md:64), and `cycle.py:767` shows the watcher takes that same account id as `self.account_id`. (3) Part A cannot cover the claim session: it has no store record and the guard exits 0 for ungoverned sessions (guard:153-154, 391), so the claim session reads untrusted issue text under the approver login with only /sc:issue prose as its limit. (4) Even for governed agents, Part A is a text rule (guard:774-775) and a script can apply the label. Part B is the only control that does not depend on text matching. V2's own residual risk 1 admits "Q-1 narrows but does not close self-approval".
- **Cost, stated honestly.** It changes the owner's workflow: the owner approves from a login other than the launch login, or the workspace gets a dedicated launch login. That is an owner decision and V1 labels it so. A cheaper variant is to ship `excluded_ids` default-empty plus a `check-config` warning `approver_is_launch_account`, and let the owner turn on enforcement. I consider that an acceptable retreat; I do not accept dropping the warning.
- **Weakness I concede.** GitHub cannot tell an agent holding the owner's token from the owner; Part B only helps if credentials are separated (V1 says so). It also adds a Task 15 generator rule (never write the account id into the approvers file) that must not break the already working hand-written config; a migration note is missing from V1.
- **Confidence.** 0.75 that some form of Part B belongs in this plan; 0.5 that the hard-refuse form (rather than warn-first) is right.

### D-05 / D-06 / C-2 Q-2 ship gate mechanism (L3)
- **Position.** The mechanism must not be agent-writable. V3's config key fails that test. Between V1 and V2, V2's single constant is simpler and I concede it is the better size; V1's separate module, new Task 4b and coupling test are heavier than the problem needs.
- **Evidence for rejecting a config key.** The watcher config lives under `~/.config/superclaude/` (source.md:64). The guard's tamper list (guard:763-765, 769-771) names the store, `.claude/settings`, `.claude/hooks`, git config and `.config/git`; it does not name `.config/superclaude`. A launched agent can edit a file there with the Edit tool or a shell redirect, and the guard's text match will not see a path it does not list. A watcher that treats that file as the switch lets an agent open its own gate. V3's claim that the owner "flips the key" is true, but so can anything else running as that user. Code constants live in the installed package, which a launched agent edits only in its own worktree copy, not in the package the cron watcher runs.
- **Evidence the gate is closed.** Observations are all skipped: `tests/hooks/test_launch_level_observations.py:79-84` (`_PENDING`, `pytest.skip(... has not been run)`); the design doc lines V1/V2 cite (docs/designs/sc-issue-launch-level-hook.md:6, :201, :625) were not re-read by me, so I mark those as carried over from the variants.
- **Where V1 is better than V2.** V1's coupling test (`ship_gate.PASSED` and `_PENDING` share no entry) turns the flip into a visible two-file change and ties it to the commit that un-skips the observation. V2's flip is "a reviewed PR after the owner records", which is a process rule. That coupling is worth keeping as a ~5-line test, without the new module.
- **Where V2 is better.** Option A is one constant and a `level_gated` skip row, A2 offers per-level granularity matching design section 7 (item 5 unlocks Worktree, item 1 also unlocks Full/FS), and it frames Option B (waiver) with its true cost (four more files made false). V1's `REQUIRED - PASSED` set is overkill for a boolean.
- **Recommended merge.** V2 Option A (or A2) plus V1's coupling test; reject V3's key.
- **Confidence.** 0.85 against V3's config key; 0.6 that V2's constant beats V1's module for the final plan.

### D-07 Q-3 updatedAt approach (L3)
- **Position. Partial CONCEDE to V2.** V2's Option C (read only the two Status/Pipeline field-value times, confirm once by Task 3a) is the better default. V1 reads field times *and* the item time and takes the latest. The item time is the risky one: applying the approval label may bump the item time, which would be later than `approved_at` and void every approval (V3's total-outage case). V1 mitigates by an owner observation and "drop the item time if the label moves it", but the shipped default should not include a signal we suspect.
- **What V1 gets right.** It treats an unreadable time as a void (fail closed), notes that a cleared Pipeline reads None (lower level, safe), and asks the observation to also list `ProjectV2ItemFieldSingleSelectValue` fields. Those are all also in V2, in different words.
- **Weakness of V1.** It cites a GitHub community discussion for the field names and says "not verified here". I did not verify it either. V2 asserts the fields exist in GitHub's GraphQL reference and also does not prove it. Neither can be settled without the Task 3 read-only introspection, which both plans include. A tie on evidence.
- **Confidence.** 0.7 V2 better on the default; 0.8 that V1/V2 both beat V3's "observe, decide, maybe fall back to level label" because V3 leaves the implementer without an approach until the owner acts.

### D-08 / C-1 Q-4 reason precedence (L3)
- **Position.** V1 and V2 over V3, but it is closer than the debate framing suggests.
- **Evidence.** `_revalidate` raises `revalidation_failed` for each of four failures (cycle.py:985-1016) and `_rv` defaults to it (cycle.py:977). Both reason words are `("skip", 0)` in the audit table, so the store and exit code do not change either way. What changes is the audit word and what the owner is told to do: `edited_after_approval` means "approve again", `revalidation_failed` means "something changed, look". V1 and V2 keep plan:71 and edit plan:108; V3 edits plan:71. The precedence order is identical in V1 and V2 (approval reread first, time rule next, then Status/Pipeline equality); V1 states it more explicitly and keeps the equality check as a backstop for a fail-open time rule, which is the security-relevant property.
- **Concession to V3.** V3 is correct that it is the smaller edit, that no test breaks today, and that the next cycle's `_examine` reports `edited_after_approval` anyway. If the owner cares about audit-word simplicity, V3 is defensible. I weigh the remedy-in-the-reason higher.
- **Confidence.** 0.6 for V1/V2 over V3.

### D-09 Q-5 Status move (L3)
- **Position.** V1's compare-and-set (move Status only if the item is currently Research, Spec, Plan or Debug; otherwise comment only with `status_moved_by_person`) is the only variant that stops the coordinator overwriting a person's later move. V2 and V3 select the right Project item but then write unconditionally.
- **Evidence.** plan:34 makes the allowed set Research/Spec/Plan/Debug and `project_check` (predicates.py:262-271) selects by `project_id` with a single live item. V1 reuses exactly that selection. A write that ignores the current Status can move a Done or In-progress item back to In review.
- **Concede to V2.** V2's validation `^PVT_...` on the id and three distinct refusal words (`project_missing`, `project_ambiguous`, `status_option_missing`) are better-specified than V1's `item_missing`/`item_ambiguous` and also check the `In review` option. Merge them. V2's `--project-id` flag on the verb is also a concrete interface V1 lacks.
- **Confidence.** 0.8 that compare-and-set belongs in the plan; 0.7 that V2's refusal vocabulary should replace V1's.

### D-12 / C-4 Q-8 `String!` (L1)
- **Position.** V1's rejection of `$owner: String = "IronbellyOrg"` is right and V3's option is wrong.
- **Evidence.** The current test pins a literal repository with no variables (`test_security_invariants.py:915,918`) and bans `String!` (919). The plan's Task 11 introduces `$owner`/`$name`. A default value silently reads the fork when the variable is missing, which is exactly the fail-open the DF-14 intent guards against, and V3 itself marks the GraphQL claim "unverified against GitHub".
- **Concede to V2.** V2's `\$(\w+): String!` regex that yields exactly {owner, name} is less brittle than V1's exact header string (a harmless reorder or whitespace change fails V1's test). V1's `count("String!") == 2` already covers the set; I would take V1's count plus V2's regex and V2's instruction to read DF-14 first (V1 did not say it read the rationale either).
- **Confidence.** 0.85 against V3; 0.6 V2's regex is the better pin.

### A-001 pr-submit still works after moving issue verbs out of SUBMIT (L3)
- **Position.** All three share the same STATED-but-incomplete assumption. It holds for the `gh` text the guard can see, and V1 is the one that names the two script call sites (`refs/review-retrigger.md:27`, `scripts/reply-resolve-thread.sh:131`) where issue comments are posted inside scripts. I did not re-grep those lines; I carry them from V1/V2/V3, who agree, so confidence in the fact is high but not independently re-read.
- **Consequence.** Because those calls pass only when the guard cannot read scripts, A-001 and A-002 are the same fact seen from two sides. V1's "Rejected" note for time-window heuristics and its credential-separation residual risk is the right framing. V2's A-003 note (GHWRITE already blocks `gh api` POSTs at every level, guard:798) shows `--monitor 3` cannot reply from a launched agent today; I agree and it should be flagged to the owner (V2 and V3 both do).
- **Confidence.** 0.7.

### A-002 script bypass (L3)
- **Position.** No variant can fix it inside this plan, and none should pretend. guard:774-775 says so in the code. V1 is the only one that names the real remedy (a token with no issues or projects write for launched agents, a Coder row) and scopes Part B as the in-plan mitigation; V2 and V3 list only the limit. I would not add a new control to this plan.
- **Confidence.** 0.85 that "document and escalate" is right; 0.6 that V1's Coder row recommendation is complete (it does not say how a workspace with one `gh` login does that).

### A-007 fail-closed cost is acceptable (L2)
- **Position.** Unstated in all three, and it matters for D-02 (V1 pays it badly, with `pytest` refused). Fail-closed is acceptable for guard text but should be measured against the work the launched agents are meant to do. This is the principle behind my D-02 concession: a refusal that blocks running the repo's own tests is not "safe", it is a defect that pushes the agent toward a script workaround, which the guard cannot see (A-002).
- **Confidence.** 0.75.

## 3. L1/L2 points (brief)
- **D-10 marker (L2).** CONCEDE: V2/V3's constant `<!-- sc:issue:result -->` is simpler. V1's `op=<id>` has two weaknesses: `op=none` for unknown outcomes means two unknown outcomes suppress each other, and the coordinator must plumb the launch op id. Both avoid `CLAIM_MARKER` (predicates.py:14), which is the real finding. Confidence 0.65 for V2/V3.
- **D-11 Q-7 (L2).** V3 and V1 move only the prompt-pin parts of `test_security_invariants.py`; V2 moves seven files (45 hits of `--pipeline none`, taken from V2; I did not recount). V2's scope is likelier to leave the tree green between tasks, V1's is smaller. Without recounting I rate V2 slightly ahead (0.55); V1's tip to write the new `_PROMPT_RE` out in the test rather than import it from `launch.py` is a real security-pin improvement that I keep.
- **D-13 / D-14.** Converge; V1's guard test pinning that an unrecorded session is allowed (guard:153-154, 391) is a useful add (V3 has it too). V2's Constraints line (files edited by several tasks) is better than V1's per-task ordering.

## 4. Summary scorecard

| Point | Best | V1 | V2 | V3 | Conf |
|---|---|---|---|---|---|
| D-01 scope | V1 scope + V2 catch-all | strong | good, misses label/project | weak | 0.8 |
| D-02/C-5 pattern | V2 | defect (refuses pytest) | best, small gap | defect | 0.9 |
| D-03 version stamp | V2 | missing | best | unread | 0.9 |
| D-04 self-approval | V1 | best | residual only | residual only | 0.75 |
| D-05/06/C-2 gate | V2 + V1 coupling test | heavy | best size | agent-writable key | 0.85 vs V3 |
| D-07 updatedAt | V2 default | risky default | best | wait-and-see | 0.7 |
| D-08/C-1 precedence | V1/V2 | good | good | defensible, smaller | 0.6 |
| D-09 target/CAS | V1 + V2 refusals | best (CAS) | best validation | weakest | 0.8 |
| D-12/C-4 String! | V1 + V2 regex | good | good | unsafe default | 0.85 |
| A-002 script bypass | V1 (names the fix) | best | limit only | limit only | 0.85 |
| D-10 marker | V2/V3 | op id over-built | simple | simple | 0.65 |

**Honest net.** V1 wins D-01 (scope), D-04, D-09, and the framing of A-002. V1 loses D-02, D-03, D-07 (default), D-10, and its D-05 mechanism is larger than needed. The strongest final plan is V1's safety scope on top of V2's mechanisms, with V3's same-second test case and per-finding rollback notes.

## 5. Not verified in this round
- design doc lines (docs/designs/sc-issue-launch-level-hook.md:6, :201, :625) and `refs/claim.md:118,122,133`: read by the variants, not by me.
- `scripts/reply-resolve-thread.sh:131`, `refs/review-retrigger.md:27`: carried from the variants.
- GitHub's behaviour for field-value `updatedAt` and whether a label moves the item time (A-004): unverifiable without the Task 3 introspection and owner observation.
- The 45-hit count behind D-11.
