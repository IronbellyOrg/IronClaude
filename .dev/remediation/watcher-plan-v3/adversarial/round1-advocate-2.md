# Round 1: advocate for Variant 2 (opus architect)

Scope: debate points from diff-analysis.md section 7. Paths relative to /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/. Confidence is 0 to 1 for my position.

## 1. Steelman of the other variants

**V1 (security).** V1 is the only variant that sees that the approver set and the launch account are the same person today. source.md:64 lists 7361222 as the watcher account and as an approver, and predicates.py:216-223 accepts any approver id, so an agent launched under that login can approve its own next issue. V1 also treats every control that an agent can reach (config key, env var) as untrusted, and it makes the Status write compare-and-set, so the coordinator never overwrites a person's move. These are the two places where V1 closes a hole that V2 only names.

**V3 (analyzer).** V3 ranks the findings by what breaks if each is left alone, which is the right order for an owner with limited review time. It is also the most honest about what it did not read (version stamp, DF-14, the design doc), and it adds a same-second test case for approval and item time. Its Q-4 rule (one reason, `revalidation_failed`, from `_revalidate`) is the smallest code change: it matches how `_rv` and `_revalidate` already collapse every failure (cycle.py:977, 990, 1011, 1016).

## 2. Points (L3 first)

### D-01 Q-1 class name and match scope
- **Position.** Keep V2's `'issue '*` line after guard:652, class `ISSUE`. Concede that V1 is right to also cover `label` and `project` writes; V2 should add them (a second line, same class).
- **Evidence.** guard:652 allows `view|list|status|diff|checks|watch|checkout`. guard:653 puts the three issue verbs in SUBMIT. guard:654 makes every other verb UNKNOWN only when `gh` is in command position (`[ "$LL_CP" != "$i" ] ||`). So `close|reopen|delete|transfer|lock|pin|develop`, `label create` and `project item-edit` are not refused when gh follows a wrapper. `'issue '*` after 652 fires at any position, like SUBMIT, and keeps read verbs allowed because first match wins.
- **Against V3.** V3 refuses only create/edit/comment (C-3). A Full Submit agent can still `gh issue close` or `reopen` when gh is not in command position, and those change the issue state that `_revalidate` reads (cycle.py:985-986).
- **Against V1.** V1's list is an enumeration; a new gh verb escapes it. `'issue '*` with read verbs allowed first is deny-by-default for the issue noun. For `label` and `project` I accept V1's "all except list/view".
- **Confidence 0.8.**

### D-02 / C-5 coordinator-only pattern (guard:444)
- **Position.** V2's narrow patterns are right. V1 and V3 use `*issue_pipeline*complete*`.
- **Evidence.** guard:444 globs the whole command text `$T`. `uv run pytest tests/issue_pipeline/test_complete.py` contains `issue_pipeline` and later `complete`, so `*issue_pipeline*complete*` matches it, and TAMPER is denied at every level (guard:802). A launched agent working on this repo could not run the new test. V2's `*issue_pipeline.complete*`, `*issue_pipeline/complete.py*` and `*issue_pipeline*import*complete*` cover the module, path and `from ... import complete` forms and still allow the test path.
- **Concession.** The hyphen form `*issue-pipeline*complete*` still over-matches `issue-pipeline plan-hash x complete.md` in V2 too (fails closed, same as the existing `*record-*`). I did not read whether `$T` normalises whitespace, so a tighter `*issue-pipeline\ complete*` is only a candidate.
- **Confidence 0.85.**

### D-03 version stamp (guard:10)
- **Position.** Bump to 2 in Task 10. V2 is right; V3 left it as "check"; V1 missed it.
- **Evidence.** guard:10 reads `# launch-level-guard-version: 1`. orca_worktree.py:839 sets `GUARD_VERSION_LINE` to the same text, and :987 tests `GUARD_VERSION_LINE not in (line.rstrip() for line in lines)`, an exact-line membership test. An installed old guard that still allows Full Submit issue writes passes the preflight unless the stamp changes. Cost: pins at tests/hooks/test_launch_level_guard.py:251, tests/skills/test_issue_orca_worktree.py:1283 and :1914-1916 move with it (seen by grep only).
- **Confidence 0.9.**

### D-04 self-approval by the launch account
- **Position.** Concede to V1: V2 under-handles this (residual risk 1 only). It is a real hole. I would not make V1's code mandatory silently; V2 should be amended to put it to the owner as a decision with V1's mechanism as Option A.
- **Evidence.** source.md:64 lists approvers 7361222, 193966884, 254764696 and account 7361222. predicates.py:216-223 checks only `actor_id in approvers`. A Full Submit agent runs under the same login. Q-1 stops the `gh issue edit --add-label` text route but not a script (A-002).
- **Why not silent.** `excluded_ids` forces the owner to approve from another login, which changes a workflow the owner already set (R2, source.md:28). That needs an owner Ruling.
- **Confidence 0.7.**

### D-05 / D-06 / C-2 ship gate mechanism
- **Position.** V2 Option A (code constant) over V3's config key. Concede V1's coupling test is worth taking.
- **Evidence.** The approvers file and `issue-watch.json` live in `~/.config/superclaude` (source.md:64) and Task 15 writes them; V1 says guard:764 protects only the store, `.claude` and git config (I did not re-read 764). If so, a launched agent can flip a config key, so V3's `launch_levels_gate` is agent-writable. A constant in `launch.py` needs a reviewed commit. V1's `REQUIRED`/`PASSED` frozensets plus a coupling test against `_PENDING` (tests/hooks/test_launch_level_observations.py:79) show the gate opened in the right commit. I take the coupling test, but a bool gives the same check without a new module and Task 4b. V2's A2 (per-level split) is the better granularity.
- **Confidence 0.75.**

### D-07 Q-3 updatedAt approach
- **Position.** V2 Option C, confirmed once by owner Task 3a.
- **Evidence.** github.py:88-103 reads only `isArchived`, `project { id }` and the Status `name`; no time is read today. predicates.py:112-118 `ProjectItem` has no time field, so every variant changes the dataclass. V1 voids on the latest of the item time and the field times, so if a label apply moves the item time (A-004, unverified), every approval is voided; V1's own fix is to drop the item time after observation, so V1's default is the part that may be dropped. V2 never uses the item time, so labels and comments cannot cause false voids.
- **Concession.** V1's "an unreadable field time voids the approval" rule is better than V2's silence; V2 should adopt it. That `createdAt/updatedAt` exist on `ProjectV2ItemFieldSingleSelectValue` is believed, not verified here; Task 3 introspection settles it.
- **Against V3.** V3 has no working path if the item time moves on labels; it stops and returns to level labels.
- **Confidence 0.7.**

### D-08 / C-1 reason precedence in `_revalidate`
- **Position.** V2 and V1 (specific reason first). V3's collapse changes plan:71, not the code, and loses the owner's remedy.
- **Evidence.** cycle.py:1007-1011 and 1015-1016: every reread failure is `_Skip("revalidation_failed")`. `_examine` already returns `edited_after_approval` (cycle.py:949-956) and `project_mismatch` (957-960). Both reasons are `("skip", 0)` per V3's audit.py citation (not re-read), so code cost is equal; only the text differs. `edited_after_approval` tells the owner to approve again.
- **Against V3.** The audit line of this cycle still hides the cause; V3's rollback ("revert the plan wording") shows it is a wording choice, not a safety gain.
- **Concession.** V1's order (approval reread, then time rule, then project_check) is slightly better than V2's: a voided or replaced approval (cycle.py:1007-1011) should win over a time reason. V2 should adopt it.
- **Confidence 0.75.**

### D-09 Q-5 Project target and Status compare-and-set
- **Position.** Concede the compare-and-set to V1; keep V2's refusal words and `^PVT_` check.
- **Evidence.** predicates.py:268-269 selects exactly one live item of the configured Project with Status `Backlog`; V2's `project_missing/ambiguous` mirror that. V1's "move only from Research/Spec/Plan/Debug" stops the coordinator overwriting a person's later move (Done, for example). complete.py is not in the tree yet, so no line to cite. Merge it into V2.
- **Confidence 0.75.**

### D-12 / C-4 Q-8 `String!`
- **Position.** V1 and V2 agree in shape; reject V3's `$owner: String = "IronbellyOrg"`.
- **Evidence.** github.py:74-76 and 88-90 hardcode `owner: "IronbellyOrg", name: "IronClaude"` and declare only `$number: Int!, $after: String`. Task 11 must parameterise them. A default on `$owner` silently reads the fork for any repo when the variable is missing, the failure the repo's fork rule fears. V2's regex gives exactly {owner, name}; V1's exact header equality is stricter. Merge: V2's "read DF-14 first" plus V1's exact header. Neither V1 nor V2 read DF-14; V2 says so.
- **Confidence 0.8.**

### A-001 issue verbs out of SUBMIT do not break pr-submit
- **Position.** True for the text path; the residual is the script path the guard cannot see. V1, V2 and V3 agree and cite review-retrigger.md:27. guard:798 refuses `gh api` writes at every level.
- **Confidence 0.8** (pr-submit not re-grepped this round).

### A-002 script bypass
- **Position.** No fix inside this plan (guard is text-only, guard:774-775 per all three, not re-read). V1 alone names the real control, credential separation (a Coder row); V2 only says out of scope. The plan should state it as an owner-visible risk. Concede V1's wording.
- **Confidence 0.8.**

### A-007 fail-closed cost is acceptable
- **Position.** Accept, provided each fail-closed rule gives the owner its message text. V2 (`LL-ISSUE` text) and V1 (`LL-ISSUE-WRITE`) do; V3 gives none beyond the code name.
- **Confidence 0.6** (unstated; the owner has not ruled).

## 3. Where V2 is weaker

1. D-04: no self-approval control beyond a residual note.
2. D-01: no `label` / `project` write verbs.
3. D-09: no compare-and-set on the Status move.
4. D-05: no coupling test between the gate and the observation tests.
5. D-07: no "unreadable time voids" rule.
6. D-08: the order puts the time rule before the approval reread.

## 4. Where V2 is stronger

D-02 (narrow patterns keep pytest working), D-03 (stale-guard preflight, verified at orca_worktree.py:839 and :987), D-07 default (field-value times, not item time), D-08 (specific reason kept), Q-7 counted hits (45 in 7 files), Q-10 Constraints line for shared files, and the `[SCOPE+]` flags that let the owner see which edits go beyond a finding.

Not verified this round: guard:764, guard:774-775, guard:153-154 (cited from the variants), audit.py reason table, the `ProjectV2ItemFieldSingleSelectValue` field list.
