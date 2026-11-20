# Round 1: advocate for Variant 3 (sonnet analyzer)

Root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/. Short names: `guard` = src/superclaude/hooks/scripts/launch-level-guard.sh; `plan` = .dev/tasks/to-do/TASK-WF-requirements-20261119-012839/TASK-WF-requirements-20261119-012839.md; `cycle` = src/superclaude/cli/issue_watch/cycle.py; `audit` = src/superclaude/cli/issue_watch/audit.py; `gh.py` = src/superclaude/cli/issue_watch/github.py; `inv` = tests/issue_watch/test_security_invariants.py. Every file:line below was read in this session. Confidence is 0-1 that V3's position is the better one on that point.

## 1. Steelman of the other two variants

**V1 (security).** V1 treats the plan as an attack surface and finds the one hole the other two miss: the hand-written approvers file lists the launch account 7361222 as an approver (.dev/tasks/to-do/TASK-WF-requirements-20261119-012839/source.md:64), so a Full Submit agent under that login can approve its own next issue. Its fixes are the most tamper-aware: it covers `label`/`project` writes, ties the ship gate to a code edit that a coupling test checks against the real pending observation list (tests/hooks/test_launch_level_observations.py:79), and keys the completion marker to the launch op id. Where V1 is wrong it is usually too wide (new owner workflow, new module), not wrong in direction.

**V2 (architect).** V2 is the most implementable and the most careful about side effects of its own changes: it keeps the diff small (a one-line `'issue '*` class placed after the view/list/status row), it read the guard version check (orca_worktree.py:839) and saw that a changed guard with an unchanged stamp passes preflight, and it noticed the broad `*complete*` pattern would refuse a test run. It labels every addition beyond the finding `[SCOPE+]`, which makes the owner's choices visible. Its Q-3 plan (field-value times, confirmed once by an owner observation) is the best design of the three if the field exists.

## 2. Strengths of V3

- S1. Ranking by consequence of leaving each finding unfixed (V3 table) is the only place a reader sees which fixes block shipping and which are wording. It matches the merged register's own split (3 blocking, 1 owner decision, 3 medium, 3 notes).
- S2. V3 states what each fix breaks and how to roll it back. Examples verified: the `ISSUEW` rows move tests at tests/hooks/test_launch_level_guard.py:2743-2745 and 2875-2876; a typo in the case row falls to `*) ll_deny LL-BROKEN` (guard:804), which fails closed.
- S3. V3 marks every unverified claim (updatedAt behaviour, version stamp, DF-14, gate pass state) instead of building on it.
- S4. V3's same-second test (approval and item time in one second) is real: `unchanged_since` treats an equal time as changed (predicates.py:257 region, read at 245-258: `t >= approved_at`).
- S5. V3 keeps the DF-14 assertion's purpose intact: it rejects "delete line 919" because that line guards the cursor typing. I checked this: DF-14 says "`$after: String` is nullable, `first: 100`, the repository literal embedded, no `mutation`" (.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md:37).

## 3. Point by point

### C-1 / D-08: reason precedence in `_revalidate` (L3)
- **V3 position:** every `_revalidate` failure is `revalidation_failed`; `edited_after_approval` comes only from `_examine`.
- **Evidence.** `_revalidate` (cycle.py:979-1016) raises `revalidation_failed` at 990, 1011 and 1016 and, through `_rv`, at 977. The same conditions at examine time carry specific reasons: `project_check` gives `project_mismatch`/`project_unreadable` at examine (cycle.py:957-960; audit.py:72-73) and collapses to `revalidation_failed` at revalidate (cycle.py:1015-1016). `edits` are not re-read (cycle.py:1006 comment), so `edited_after_approval` from `unchanged_since` (cycle.py:949-956) cannot occur in `_revalidate` today. The code's own convention is: specific reason at examine, one collapsed reason at revalidate. A `_Skip` from either place writes nothing (cycle.py:822-823), the next cycle re-examines and reports the specific reason, and both reasons are `("skip", 0)` (audit.py:71, 80). V2 says the same: "only the audit line differs".
- **Critique of V1/V2.** They add a second reason inside `_revalidate`, so one event (owner lowers Pipeline after approval) reports `edited_after_approval` when GitHub timestamps behave and `revalidation_failed` when they do not. The reason then tells you which check happened to fire, not what happened. In production the equality check becomes unreachable whenever the time rule works; their tests reach it only with fixtures whose times are deliberately stale. V1 and V2 also still have to rewrite plan:108 (the two Task 6 cases end `revalidation_failed`), exactly as V3 has to rewrite half of plan:71.
- **Concession.** Plan:71 is derived from the owner's R31 and says "both at examine time and between examine and launch"; plan:65 says the new predicate is called again in `_revalidate`. V1/V2 keep that sentence true and keep a backstop when the time rule fails open (Q-3 is unverified). If the plan author treats plan:71 as fixed, V2's wording (time rule first, after the items reread, then the equality check) is the right way to do it and V1's three-step order is equivalent.
- **Confidence 0.45** that V3 is better. This is a convention-versus-fidelity call, and either is a small edit.

### C-2 / D-05 / D-06: ship gate switch (L3)
- **V3 position:** one config key `launch_levels_gate`, default closed, reason `launch_gate_closed`, owner flips or waives.
- **Evidence for V1's objection.** guard:764 lists only the store, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config` and `.config/git`; `~/.config/superclaude` is not in it, so a launched agent's Edit or Bash on the config file is not TAMPER. That is true.
- **Why it does not decide the point.** (a) The gate is a readiness check, not an authority: the launch still needs the owner's Pipeline value plus a later approval (plan:25). An agent that flips the gate gains no launch without the owner. (b) The same directory already holds the approvers file (cycle.py:66, 281; source.md:64) and `enabled`; the config surface is already trusted for strictly bigger decisions, so V1's rule would reject `enabled` too. (c) The config key must be added to `_TOP_KEYS` (cycle.py:58-69), a closed set, so the flip is validated, not free text.
- **Where V3 is weaker.** V3 has no evidence tie: the owner flips on assertion, whereas V1's coupling test between `ship_gate.PASSED` and `_PENDING` (test_launch_level_observations.py:79-84) forces a visible two-file edit. V3's text is also inconsistent: the fix says default `closed`, the rollback says default `open`. And V3 does not put the gate before `_launch` explicitly (it must be in `_examine`, because `_launch` sets `c.launching = True` and halts the cycle, cycle.py:833-834, 1028).
- **Best form.** V2's Option A (a code constant, one reason row, ~6 lines) is the smallest control that agents cannot write; V1's coupling test is a good add-on. V3's config key is the most convenient for the owner but is the loosest control.
- **Concede to V2/V1. Confidence 0.35** that V3 is better.

### D-12 / C-4: `String!` (L1)
- **V3 position:** restate line 919; keep the cursor typing rule; the default-value form is an unverified alternative.
- **Evidence.** inv:919 is `assert "$after: String)" in query and "String!" not in query  # DF-14`. Both queries today are `query($number: Int!, $after: String)` with the repository literal (gh.py:74, 88). The DF-14 rationale (research/06 line 37) is that `$after` is nullable (first page has no cursor); the `String!` ban is a blunt proxy for that. inv:918 already forbids `$owner`/`$name`, and plan:166 reverses it. Task 11 therefore must add `$owner: String!` and `$name: String!`.
- **Critique of V3's own aside.** `$owner: String = "IronbellyOrg"` is valid under the GraphQL spec (a defaulted nullable variable may fill a non-null position) but it is the worst option: a missing variable silently reads the fork for any repo. V1's C-4 objection is right. V3 flagged it as unverified, but it should not have been offered.
- **V1 vs V2.** V1's exact header equality plus `count("String!") == 2` pins the cursor, the order and the number of non-null strings; it is brittle to reordering but both queries share one header today. V2's regex `\$(\w+): String!` gives {owner, name} and is looser but order-free. Either is better than V3's prose. V2 and V3 both did not read DF-14 before choosing; I did, and it supports all three.
- **Concede to V1. Confidence 0.25** that V3 is better.

### D-01 / C-3: guard class scope (L3)
- **Evidence.** guard:653 holds `'pr create' | 'pr edit' | 'pr comment' | 'pr ready' | 'issue create' | 'issue edit' | 'issue comment'` as SUBMIT; guard:790 allows `SUBMIT:FS`; guard:654 makes every other verb UNKNOWN only when gh is in command position (`LL_CP`). Lines 649-652 run first (merge, search, `*' view'`, `*' list'`, `*' status'`), so a later `'issue '*` row cannot refuse `issue view|list|status`.
- **V3 position:** move only create/edit/comment. It is the minimal fix for what Q-1 named.
- **Critique.** V3 leaves `issue close|reopen|delete|transfer|lock|pin|develop` writes UNKNOWN in command position only, so `true && gh issue close 5` is not refused. V2's single `'issue '*` row after 652 closes all of them in one line and keeps the view/list/status allowance. V1 goes further (`label`, `project` verbs); that also closes the "agent changes a Project field" policy-only gap that V3 lists as residual (tests/hooks/test_launch_level_guard.py:2735 "Residual R17"), at the price of scope beyond the finding.
- **Concede to V2 (V1 as optional extension). Confidence 0.25.**

### D-02 / C-5: coordinator-only pattern at guard:444 (L3)
- **Evidence.** Line 444 today is `case $T in *release-worker* | *release_worker* | *issue-pipeline*adopt-* | *issue-pipeline*record-* | *issue_pipeline*release* | *issue_pipeline*approval_record*) ... TAMPER`. `$T` is the whole command text, so `*issue_pipeline*complete*` matches `uv run pytest tests/issue_pipeline/test_complete.py`; the plan creates that file and `test_complete_cli.py` (plan:146, 157).
- **V3/V1 position:** `*issue-pipeline*complete* | *issue_pipeline*complete*`, in the style of the existing line.
- **Precedent for V3.** The existing `*issue_pipeline*approval_record*` already refuses `pytest tests/issue_pipeline/test_approval_record.py` (that file exists in tests/issue_pipeline/), and V1 notes the `*record-*` over-match. So the cost is accepted fail-closed behaviour.
- **Still, V2 is better.** It names the module forms (`*issue_pipeline.complete*`, `*issue_pipeline/complete.py*`, `*issue_pipeline*import*complete*`) and adds an explicit must-allow case for the test path. A launched agent working on this repo needs to run its own tests.
- **Concede to V2. Confidence 0.3.**

### D-03: guard version stamp
- **Evidence.** guard:10 is `# launch-level-guard-version: 1` and orca_worktree.py:839 is `GUARD_VERSION_LINE = "# launch-level-guard-version: 1"`. V3 said it had not read the comparison; V2 did, and a changed guard with the old stamp passes preflight on a stale host.
- **Concede to V2. Confidence 0.15.** Bump both and update the tests that pin it.

### D-04: self-approval by the launch account (L3)
- **Evidence.** source.md:64: account 7361222 is in `issue-watch-approvers.txt` together with 193966884 and 254764696, and is the `account` in the config. `unchanged_since` skips comments by `own_login` (predicates.py:253-255 region), so a forged comment under that login never voids anything (A-006, verified).
- **V3 position:** list it as residual risk only.
- **Assessment.** V1 found a real path. But Part B is not in Q-1 as merged, it changes the owner's approval workflow (V1's own Risks section), and it touches `approval_of`, the cycle's two call sites and the Task 15 generator. Under "scope discipline" it should reach the owner as an explicit decision, not be folded into the plan by default. The owner has two other approver ids, so the decision is feasible.
- **Concede V1 is right on the facts; V3 is right that it needs the owner. Confidence 0.35.**

### D-07: `updatedAt`
- **Evidence.** Today PROJECT_ITEMS_QUERY asks the Status value for `name` only (gh.py:95-97) and has no item `updatedAt`. V3 uses the item time with an owner observation and a decision table; V1/V2 read `createdAt`/`updatedAt` of the Status and Pipeline values.
- **Assessment.** Per-field times avoid false voids from labels and comments; V3's item time has the false-void and the fail-open risk, which V3 itself ranks #2. V2's order (C, confirmed once by an owner observation, B only if it fails) is better than V3's. I have not verified that the field-value types expose these fields in GitHub's schema; V1 and V2 cite documentation only. V3's strength is the same-second test and the decision table.
- **Concede to V2. Confidence 0.3.**

### D-09: Status move target (L3)
- **V3:** configured project id and the Task 6 one-item helper, closed refusal word. **V1:** adds a check-then-set: move Status only when the current Status is Research/Spec/Plan/Debug, otherwise comment only. V1 protects a person's later move (for example to Done). It is not atomic (read then mutate), so "compare-and-set" is the wrong name, but it narrows the window. V2 adds three named refusals and a `^PVT_` validation.
- **Concede to V1 on the Status guard, to V2 on the refusals. Confidence 0.3.**

### D-10: marker (L2)
- **Evidence.** plan:141: "a second call finds only the marker comments written by the watcher's own login and posts no second comment"; plan:146 tests it. With V2/V3's one static `<!-- sc:issue:result -->`, a retry after a fresh approval (Q-10 says a retry needs one) would find the first run's marker and post no result comment. V1's marker with the launch op id avoids that.
- **Concede to V1. Confidence 0.3.** All three agree it must not contain `CLAIM_MARKER` (predicates.py:14).

### D-11, D-13, D-14 (L1/L2)
All three agree in substance. V1 gives the best Q-7 detail (the new `_PROMPT_RE` written out, not imported). V2 counted 45 `--pipeline none` hits in 7 files and moves all of them into Task 6; V1 and V3 move only `test_security_invariants.py`. If the count is right, V2 is the only one that keeps the tree green between tasks, since Task 6 changes `PROMPT_PATTERN`. V2's Constraints line (same-file edits in plan order) is the best Q-10 text. **Concede Q-7 and Q-10 to V2, Q-9 equal. Confidence 0.2.**

### Shared assumptions
- **A-001** (pr-submit needs no issue verb): verified by grep of src/superclaude/skills/sc-pr-submit-protocol, which has no `gh issue` call; the comments go through `gh api` in scripts. All three are right, and none of them can claim the guard sees scripts.
- **A-002** (script bypass): all three note it; the only real fix is credential separation (a Coder row), outside this plan. V3 lists it as residual and does not pretend otherwise. Equal.
- **A-007** (extra refusals are acceptable): unstated in all three; V1's and V2's wider classes cost more refusals. The owner should confirm it once.

## 4. Summary for the round

Where V3 holds: C-1 (code convention, small edit), the DF-14 purpose (D-12 primary form), ranking and rollback notes, honest "unverified" marking. Where V3 should yield: D-01, D-02/C-5, D-03, D-05/C-2 (use V2's constant, plus V1's coupling test), D-09, D-10, D-12 default-value aside, Q-7 scope. D-04 and D-07 are the two owner-facing choices; present both to the owner.
