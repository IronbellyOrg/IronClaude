# Round 2 - rebuttals and verdicts (watcher plan v3, Q-1 to Q-10)

Inputs: `diff-analysis.md`, `variant-1-opus-security.md` (V1), `variant-2-opus-architect.md` (V2), `variant-3-sonnet-analyzer.md` (V3), `round1-advocate-1.md` (A1), `round1-advocate-2.md` (A2), `round1-advocate-3.md` (A3), all in `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/remediation/watcher-plan-v3/adversarial/`. Repo paths below are relative to `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/`. `guard` = `src/superclaude/hooks/scripts/launch-level-guard.sh`; `plan` = `.dev/tasks/to-do/TASK-WF-requirements-20261119-012839/TASK-WF-requirements-20261119-012839.md`.

Settled in Round 1 and not reopened: D-02 narrow V2 pattern, D-03 bump the guard version stamp to 2, D-09 compare-and-set (V1) plus V2 refusal words, D-12 reject `$owner: String = "IronbellyOrg"`, C-2 no config key for the ship gate, A-001, A-002, A-007, and the convergent items Q-9 and Q-10. Section 3 scores them for the overall convergence figure.

Convergence rule used: a point scores the number of advocates (of 3) whose stated Round 1 position equals the verdict without a further concession. An advocate who never addressed the alternative does not count as agreeing (strict). Lenient figures are given where it matters.

## 0. Facts I read or ran this round

| Fact | Result | Where |
|---|---|---|
| H3 case is on the two words `"$LL_GG $LL_GA"`; row 652 allows `*' view' \| *' list' \| ...`; row 653 is SUBMIT; row 654 is UNKNOWN in command position only | CONFIRMED | guard:646-655 |
| Decision loop only evaluates classes named in its `for` list; a class not in the list is never denied | CONFIRMED | guard:788 (`for LL_C in BIG TAMPER MERGE ...`); the closing `*) ll_deny LL-BROKEN` covers only listed classes |
| Bash `case` run: `issue close`, `label create`, `project item-edit` hit a catch-all after row 652; `issue view`, `project list/view`, `label list` stay allowed; **`project item-list` and `project field-list` do NOT end in ` list`, so a `'project '*` catch-all would refuse those reads** | CONFIRMED by run | my probe, same glob forms |
| Pattern run on 13 commands: V1/V3 `*issue_pipeline*complete*` refuses `uv run pytest tests/issue_pipeline/test_complete.py` and `test_complete_cli.py`; V2 allows both; V2 allows `p.complete.run()` after `from superclaude.cli import issue_pipeline as p`; V2 plus `*issue_pipeline*complete.run*` refuses it | CONFIRMED by run | my probe |
| Every hyphen alternative `*issue-pipeline*complete*` (all three variants keep it) also refuses `superclaude issue-pipeline plan-hash d complete.md`, so a path argument containing the letters "complete" (for example a `completed` directory) blocks `plan-hash` for a bound worker | CONFIRMED by run | my probe |
| Same-style precedent: `tests/issue_pipeline/test_approval_record.py` and `test_release.py` exist and are already caught by `*issue_pipeline*approval_record*` / `*issue_pipeline*release*` | CONFIRMED | guard:444, `ls tests/issue_pipeline` |
| `approval_of` has no exclusion; actor gates are User type, not `[bot]`, int id, `in approvers` | CONFIRMED | predicates.py:216-223 |
| Approvers file lists the launch account 7361222; `self.account_id = who.account_id` | CONFIRMED | source.md:64; cycle.py:767-768 |
| Config keys are a closed set; `check-config` prints only "configuration is valid" and three info lines, no warning concept today | CONFIRMED | cycle.py:58-69; cli.py:185-198 |
| `_examine` returns `edited_after_approval` (949-956) then `project_mismatch` (957-960); `_revalidate` raises `revalidation_failed` at 990, 1011, 1016 and via `_rv` (977); `edits` are not re-read in `_revalidate` (comment at 1006) so `unchanged_since` cannot run there | CONFIRMED | cycle.py:935-1016 |
| `PROJECT_ITEMS_QUERY` reads only Status `name`; `ProjectItem` has `is_archived`, `project_id`, `status_name` and no time | CONFIRMED | github.py:84-100; predicates.py:111-118 |
| GitHub docs: `ProjectV2ItemFieldSingleSelectValue` fields table lists `createdAt (DateTime!)`, `creator`, `databaseId`; `updatedAt (DateTime!)` is shown for sibling value types (`TextValue`, `NumberValue`); the single-select `updatedAt` row was cut off in the extract | PARTIAL: `createdAt` confirmed, `updatedAt` on single-select not seen; whether changing an option moves either time stays unobservable without Task 3/3a | docs.github.com/en/graphql/reference/projects (Tavily extract) |
| `build_claim_prompt(n)` takes only `n` and returns `... --pipeline none`; `launch_argv` rejects any prompt not matching `PROMPT_PATTERN` | CONFIRMED | launch.py:33, 84-102 |
| plan:102 makes `build_claim_prompt` take Status and Pipeline and plan:108 tests a prompt per allowed Status | CONFIRMED | plan:102, 108 |
| `--pipeline none` literal count in `tests/issue_watch` (pyc excluded) | 45 lines in 7 files: test_launch 14, test_security_invariants 15, test_cycle 6, test_no_text 4, test_cli 3, test_cli_e2e 2, test_crash_injection 1 | grep -c, recount |
| No test outside `tests/issue_watch` carries the old prompt literal | CONFIRMED (the grep for the literal in `tests` and `src` hits only those 7 files) | grep |
| `_PENDING` has 12 entries: OB-H1 items 1-9, OB-H2, OB-H3, OB-CTX; each is `pytest.skip` | CONFIRMED | tests/hooks/test_launch_level_observations.py:79-84 |
| Ship-gate text disagrees between design and claim.md: design §7 U1 needs item 1 only for `full`/`--submit` and item 5 for any level; `refs/claim.md:133` says no governed claim (`worktree` or `full`) until item 1, OB-H2 and OB-H3 have passed | CONFIRMED | docs/designs/sc-issue-launch-level-hook.md:201, 625; claim.md:133 |
| Store entry: `operation_id: str \| None` and `approval_event_id: int \| None`; `mark_pending` validates the approval triple; `mark_pending` allows only from no entry or `failed`; unknown launch outcome stores `outcome.operation_id` possibly empty | CONFIRMED | record.py:76-78, 538-547; cycle.py:1100-1107 |

Not verified: GitHub's runtime behaviour on field-value times (A-004); `refs/review-retrigger.md:27` and `reply-resolve-thread.sh:131` (carried from variants).

---

## 1. Point-by-point (the eight contested points)

### (1) D-04 self-approval by the launch account: hard-refuse vs warn-first vs residual-only

**Side H (hard-refuse `excluded_ids`, V1 as written).** Evidence from A1: `approval_of` accepts any `actor_id in approvers` (predicates.py:216-223); the approvers file holds the launch account (source.md:64); the claim session has no store record so the guard exits 0 for it (guard:153-154, 391); Part A is text-only (guard:774-775), so a script can still apply the label. Only Part B does not depend on text matching.
**Rebuttal to H (from A1's and A2's own evidence).** The same facts that prove the hole prove the cost: the owner's config lists 7361222 as both launch account and approver, and the owner set that workflow (A2 cites R2, source.md:28). A default-on exclusion makes every approval by that login return `not_approved` on the first cycle, a total launch outage for a one-login workspace, delivered by an agent-authored plan change. A1 itself concedes "0.5 that the hard-refuse form is right" and calls warn-first "an acceptable retreat". GitHub cannot tell the owner from an agent holding the same token (A1), so enforcement without credential separation is partial anyway.

**Side W (warn-first: default-empty list plus `check-config` warning `approver_is_launch_account`, owner opts in).** Evidence: A1's own retreat; A2 "put it to the owner as a decision, V1's mechanism as Option A"; A3 "needs the owner". It keeps the fact visible, the mechanism ready, and the workflow unchanged until the owner rules. Cost: `_TOP_KEYS` is a closed set (cycle.py:58-69) so a key is added deliberately; `check-config` has no warning output today (cli.py:185-198), so the warning line is new code.
**Rebuttal to W (from A1/V1 evidence).** A warning nobody reads is residual-risk-only with extra code. Answer: print it in `check-config` and in the Task 17 first-run report (V1 lists that report), so the owner sees it at enable time.

**Side R (residual risk only, V2 and V3 as written).** Evidence: Q-1 part A already narrows the vector; A-006 (own-login comments never void an approval) is unrelated; the owner may not want a workflow change.
**Rebuttal to R (A1, A2).** V2's own residual risk 1 says Q-1 "narrows but does not close self-approval"; A2 withdrew to "V2 under-handles this". The claim session is ungoverned (guard:153-154, 391), so for it prose is the only limit. Naming a risk without a switch to turn the fix on leaves the owner without a decision path.

**Verdict: warn-first, owner decision recorded.** `approval_of` gets `excluded_ids` (default empty). A new config key (closed-set addition) feeds it. `check-config` and the Task 17 first-run report print `approver_is_launch_account` when the approvers file holds the launch account. The plan records one open owner decision: switch enforcement on and approve from a second login, or accept the residual. The Task 15 generator never writes the account id into a generated approvers file (V1). One caveat to state in the plan: the exclusion list lives in `~/.config/superclaude`, which the guard's tamper list does not name (guard:763-765), the same directory as the approvers file, so an agent able to edit one can edit the other; Part B limits an honest-but-injected session, not a hostile one.
**Confidence 0.70.** Decided by: source.md:64 plus predicates.py:216-223 (hole is real), and the one-login outage under default-on (cost is real).
**Convergence 3/3** (A1 accepts warn-first, A2 and A3 ask for an owner decision; none defends hard-refuse by default).

### (2) C-1 / D-08 reason precedence in `_revalidate`: specific reason first (V1/V2) vs collapse to `revalidation_failed` (V3)

**Side V1/V2.** Time rule after the items reread gives `edited_after_approval`; equality and `project_check` give `revalidation_failed`. Evidence: plan:71 (the owner-derived R31 acceptance) says the refusal is `edited_after_approval` "both at examine time and between examine and launch"; the reread already carries the Project items (cycle.py:1012-1014), so the time rule is computable there; `edited_after_approval` tells the owner the remedy (approve again).
**Rebuttal to V1/V2 (A3's evidence).** Convention: examine gives specific reasons, revalidate collapses to one (cycle.py:957-960 versus 1015-1016); both reasons are `("skip", 0)`, so exit code and store effects match; the next cycle's `_examine` reports the specific reason anyway; once the time rule works the equality check is reachable only through contrived fixtures.
**Rebuttal to V3.** The collapse changes plan:71, an owner-derived acceptance, while V1/V2 only touch plan:108 fixtures. The equality check is a deliberate backstop for a fail-open time rule, and A3 concedes the time rule is unverified (A-004), so a backstop that fires `revalidation_failed` is exactly its job. A3 also concedes "if the plan author treats plan:71 as fixed, V2's wording is right". Order: A1 and A2 agree the approval reread (cycle.py:1007-1011, `revalidation_failed`) wins first, then the time rule, then project_check/equality.

**Verdict: V1 order.** (1) approval reread (existing, `revalidation_failed`); (2) time rule, `edited_after_approval`; (3) `project_check` and examined-versus-reread equality, `revalidation_failed`. Condition that decides whether it holds: the Task 6 fixtures for plan:108 must keep every field time before the approval so the equality check is reached, and the plan adds the overlap case (Pipeline lowered with a late field time ends `edited_after_approval`).
**Confidence 0.65.** Decided by plan:71 versus 108 (which sentence is the owner's) and cycle.py:1012-1016 (the reread data is present).
**Convergence 2/3** (A1, A2; A3 stays at 0.45 for V3 and concedes the conditional).

### (3) D-05 gate form: single constant vs frozenset module, coupling test kept or not

**Side V1 (module `ship_gate.py`, `REQUIRED`/`PASSED` frozensets, Task 4b, coupling test).** Evidence: the coupling test turns the flip into a visible two-file change tied to un-skipping the observation (test_launch_level_observations.py:79-84).
**Rebuttal (A1 and A2, own evidence).** A1: "`REQUIRED - PASSED` is overkill for a boolean" and the module plus new task is heavier than the problem; A2 and A3 take the constant. The coupling idea survives without a module.
**Side V2 (constant `GOVERNED_LEVELS_ALLOWED = False` in `launch.py`, reason `level_gated`; A2 splits per level).** Evidence: about 6 lines, one reason row; a code constant needs a reviewed commit in the package the cron runs. **Rebuttal to the A2 split:** the sources disagree on what the split is. Design §7 U1 (design:201) needs item 1 only for `full` or `--submit`, but `refs/claim.md:133` says no governed claim of any kind (`worktree` or `full`) until item 1, OB-H2 and OB-H3 pass. Encoding two constants would pick a side in a documentation conflict the plan does not own. One boolean matches the stricter text (claim.md:133) and can be split later when the docs agree.

**Verdict: V2 Option A single constant, plus a ~5-line coupling test.** The test (in `tests/hooks/test_launch_level_observations.py`, beside `_PENDING`) asserts that when the constant is True, none of `OB-H1 item 1`, `OB-H1 item 5`, `OB-H2`, `OB-H3` appears in `_PENDING`. Add one `level_gated` row to `audit.REASON_TABLE` (`("skip", 0)`). The gate sits in `_examine` before `_launch` (A3: `_launch` sets `c.launching` and halts the cycle, cycle.py:833-834, 1028). Plan records the claim.md:133 versus design:201 mismatch as an owner note. The per-level split (A2) stays an owner option, not a default.
**Confidence 0.75.** Decided by: claim.md:133 versus design:201 (split not safely derivable) and A1's size argument.
**Convergence 3/3.**

### (4) D-07 default: field-value times only (V2) vs field times plus item time (V1)

**Side V1.** Latest of field times and item `updatedAt`; unreadable voids; owner observation drops the item time if a label moves it. Evidence: fail closed; also covers any other change to the item.
**Rebuttal to V1 (A1, A3, A2).** The item time is the part V1 itself expects to drop; shipping it by default risks the total-outage case V3 ranks #2 (a label apply bumping the item time voids every approval). The approval label is applied after the Project change, so any label-moves-item-time behaviour makes every approval fail. A1: "the shipped default should not include a signal we suspect".
**Side V2 (Option C).** Read `createdAt` and `updatedAt` of the Status and Pipeline value objects through the two `fieldValueByName` aliases Task 3 adds; void when the later time is at or after the approval; confirm once through the owner Task 3a. Evidence: GitHub docs list `createdAt` on `ProjectV2ItemFieldSingleSelectValue`, and `updatedAt` on sibling value types; labels and comments touch neither object.
**Rebuttal to V2 (A2's concession).** V2 is silent on an unreadable time; V1's rule is better.

**Verdict: V2 Option C with V1's "unreadable time voids" rule and V3's same-second test case; item time excluded from the default.** Task 3 introspection must still confirm `updatedAt` on the single-select type (the docs extract cut it off) and Task 3a must observe whether changing an option moves the value time (unobservable offline).
**Confidence 0.75.** Decided by: github.py:84-100 (nothing is read today, so the choice is open), the docs extract (`createdAt` confirmed), and the asymmetry of failure (an item-time default can lock out everything; a value-time default cannot be moved by a label).
**Convergence 3/3.**

### (5) D-02 extra alternative `*issue_pipeline*complete.run*`

**For (A1, 0.5).** The V2 list is a negative-space decision: it accepts a known bypass to protect pytest. My run shows `python -c "from superclaude.cli import issue_pipeline as p; p.complete.run()"` is allowed by V2 and refused with the extra alternative; `pytest tests/issue_pipeline/test_complete.py` stays allowed with it.
**Against (derived from A1's own A-002 and guard:774-775).** The guard is text-only; `getattr`, `importlib` or a script defeat every pattern, so one more alternative closes one spelling, not the hole. False positives exist: `grep -rn issue_pipeline -e complete.run` is refused by my run (fail closed, rare).
**Verdict: add it.** Cost is one glob alternative and one must-refuse test line; it covers the module-call spelling next to `-m`, `from ... import complete` and `from ... .complete import`; the only false positive found is an odd `grep -e` order. The plan must say it is best-effort, not a control (A-002).
**Confidence 0.55.** A2 and A3 did not address it; no advocate opposes it.
**Convergence 1/3 strict** (A1 only; lenient 3/3 since no one opposes).
Related finding for the same Task 10 line (not a Round 1 point): all alternatives keep `*issue-pipeline*complete*`, which refuses `superclaude issue-pipeline plan-hash <dir> complete.md` and any `plan-hash` path containing "complete" (for example a `completed` directory). Add one must-allow test for `plan-hash` with such a path, or anchor the hyphen alternative on the verb word.

### (6) D-01 merged scope: catch-all `'issue '*` after guard:652 plus `label` and `project` verbs

**Side narrow (V3: create/edit/comment only).** Rebuttal (all three advocates): close, reopen, delete, transfer, lock, pin, develop fall to the command-position-only UNKNOWN row (guard:654), so `flock x gh issue close 5` passes.
**Side V2 catch-all (`'issue '*` after 652).** Verified: row 652 allows view/list/status first, so reads stay allowed; the catch-all fires wherever `gh` appears, like SUBMIT.
**Side V1 (adds `label` and `project`).** Evidence: the plan itself says a launched agent never changes a Project field (plan:23, an owner decision) and `gh project item-edit` is how; V3's own residual risk cites R17 (tests/hooks/test_launch_level_guard.py:2736). A3 treats it as optional scope; A1 and A2 take it.
**New finding.** `project item-list` and `project field-list` do not match `*' list'`; a naive `'project '*` refuses them. Add them to the allow rows (they are read-only) before the catch-all, or accept the refusal knowingly.

**Verdict: `'issue '*`, `'label '*` and `'project '*` as one blocked class placed after row 652, with `'project item-list' | 'project field-list'` allowed before it.** Add the class to the precedence `for` list at guard:788 (a class missing there is never evaluated) and to the case table at all four levels, with a message that names issue, label and project writes. It enforces an existing owner decision (plan:23), so it is not scope creep; mark it in the plan as the one place Q-1 goes beyond issue verbs.
**Confidence 0.75.** Decided by guard:646-655 plus my case run.
**Convergence: catch-all 3/3; label/project 2/3** (A3 optional). Scored 2/3 for the merged scope.

### (7) D-11 Q-7 scope: 1 file (V1/V3) vs 7 files (V2)

**Side 1 file (V1/V3, `test_security_invariants.py` only).** Smaller diff; V1 adds the useful tip of writing the new `_PROMPT_RE` into the test rather than importing it.
**Side 7 files (V2).** My recount: 45 lines in 7 files, exactly V2's per-file numbers. `launch_argv` rejects any prompt that does not fullmatch `PROMPT_PATTERN` (launch.py:101), `build_claim_prompt(n)` only builds `--pipeline none` (launch.py:84-92), and plan:102 changes it to take Status and Pipeline. So `test_cli.py:605-610` (calls `launch_argv` with the literal), `test_crash_injection.py:38,191` (compares the cycle-built prompt with the literal), `test_no_text.py:66,560-562`, `test_cycle.py:2383,3772-3784,4365,4487` and `test_launch.py` break when Task 6 lands. V1/V3 leave six files red between Task 6 and Task 7, and `/sc:implement` grades each task alone (V2).
**Rebuttal to V2.** Some of the 7 may only pass the literal through a fake launcher and survive; the exact red set is known only after Task 6. V2's own acceptance (`uv run pytest tests/issue_watch -q` at Task 6) settles it, so moving all 7 is the safe superset.

**Verdict: V2's 7 files, plus V1's tip (write the new `_PROMPT_RE` in the test, do not import it).** Task 6 acceptance becomes `uv run pytest tests/issue_watch -q`; Task 7 keeps commands, skills, WORKER-CONTRACT.md and docs.
**Confidence 0.85.** Decided by the recount and launch.py:101.
**Convergence 3/3.**

### (8) D-10 marker choice

**Side constant `<!-- sc:issue:result -->` (V2/V3 as written; A1 and A2 conceded to it).** Evidence: simple; both avoid `CLAIM_MARKER` (predicates.py:14), the real finding.
**Side per-run (V1: `op=<id>`; A3 argues for it).** Evidence (A3): plan:141 makes `complete` idempotent by "finds only the marker comments written by the watcher's own login and posts no second comment", scoped to the issue. A second run on the same issue happens by design: `mark_pending` allows a new launch from `failed` (record.py:545), and Q-10 says a retry needs a fresh approval. With one static marker the second run's result comment is silently suppressed.
**Rebuttal to A3/V1 (A1).** `op=none` for an unknown launch outcome makes two unknown outcomes suppress each other, and the coordinator must plumb the op id. Verified: `operation_id` can be empty or None (cycle.py:1100-1107; record.py:76).
**Resolution not argued by any advocate.** Key the marker on the approval event id instead: `mark_pending` validates the approval triple (record.py:547), and each relaunch needs a fresh approval, so it is unique per run and known whenever a run exists. `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->` still never contains `CLAIM_MARKER`.

**Verdict: per-run marker (V1's idea), keyed on approval event id rather than op id.** A static marker is rejected on the unrebutted idempotency evidence; the op-id key is rejected on A1's `op=none` objection.
**Confidence 0.65.** Decided by record.py:545-547 and plan:141. This verdict overrules 2 of 3 advocates; the deciding point (A3) was not answered by A1 or A2.
**Convergence 1/3 strict** (A3 only; A1 and A2 for the constant).

---

## 2. Verdict summary

| # | Point | Verdict | Conf | Agree |
|---|---|---|---|---|
| 1 | D-04 | warn-first, default-empty `excluded_ids`, `check-config` warning, owner decision | 0.70 | 3/3 |
| 2 | C-1/D-08 | V1 order: approval reread, then time rule (`edited_after_approval`), then equality (`revalidation_failed`) | 0.65 | 2/3 |
| 3 | D-05 | single constant (A) plus coupling test; split per level left to owner | 0.75 | 3/3 |
| 4 | D-07 | field-value times only, unreadable voids, Task 3a kept | 0.75 | 3/3 |
| 5 | D-02 extra | add `*issue_pipeline*complete.run*`, best-effort | 0.55 | 1/3 |
| 6 | D-01 | `'issue '*`, `'label '*`, `'project '*` after row 652, read verbs `item-list` and `field-list` allowed | 0.75 | 2/3 |
| 7 | D-11 | 7 files into Task 6 | 0.85 | 3/3 |
| 8 | D-10 | per-run marker keyed on approval event id | 0.65 | 1/3 |

---

## 3. Convergence

Rows scored (all debated points, including those settled in Round 1):

| Row | Agreeing advocates | Fraction |
|---|---|---|
| D-01 catch-all | 3 | 1.00 |
| D-01 label/project | 2 | 0.67 |
| D-02 V2 narrow pattern | 3 | 1.00 |
| D-02 extra `complete.run` | 1 | 0.33 |
| D-03 version bump to 2 | 3 | 1.00 |
| D-04 warn-first | 3 | 1.00 |
| D-05 constant plus coupling test | 3 | 1.00 |
| D-06/C-2 no config key | 3 | 1.00 |
| D-07 field-value times | 3 | 1.00 |
| D-08/C-1 precedence | 2 | 0.67 |
| D-09 compare-and-set plus V2 refusals | 3 | 1.00 |
| D-10 marker | 1 | 0.33 |
| D-11 seven files | 3 | 1.00 |
| D-12/C-4 reject default-value trick | 3 | 1.00 |
| A-001 | 3 | 1.00 |
| A-002 | 3 | 1.00 |
| A-007 (owner confirms, messages owner-readable) | 3 | 1.00 |
| D-13/D-14 (convergent) | 3 | 1.00 |

- Overall: 48 agreeing votes of 54 possible = **0.889 (reaches 0.80)**. Rows below 0.80: 4 of 18 (D-01 label/project and D-08 at 0.67; D-02 extra and D-10 at 0.33).
- Contested eight only (D-04, C-1, D-05, D-07, D-02 extra, D-01 merged at 2/3, D-11, D-10): 18 of 24 = **0.750 (does not reach 0.80)**.
- Lenient (silent advocates counted as non-opposed): D-02 extra becomes 3/3, so the contested eight reach 20 of 24 = 0.833 and overall 50 of 54 = 0.926.

The pipeline gate is met on the overall figure. Two rows would go to a third round only if the owner wants unanimity: D-10 (verdict overrules two advocates on evidence they did not answer) and D-02 extra (never debated by two of three). Neither blocks the merge.

## 4. Orchestrator notes (not advocate output)

- Items the merge executor must carry that no variant stated: the new guard class must be added to the `for LL_C in` list at guard:788; `project item-list` and `project field-list` need allow rows; `plan-hash` with a path containing "complete" is refused by the hyphen alternative.
- The D-10 key (approval event id) and the D-05 claim.md:133 versus design:201 mismatch are my reading of the files; no advocate argued either.
