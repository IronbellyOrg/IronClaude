## Re-review findings on changed lines

Grading check used for each finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding is blocking only when that sentence holds with no further guess (two stated texts that contradict, harm to a safety boundary, or an acceptance check that cannot pass). Where the sentence needs a guess between two readings the text allows, or the finding is a requirement the text never states, it is Medium. No finding below passed the check for blocking.

=== REQUIREMENTS ANALYSIS ===

Experts: Wiegers (lead), Adzic, Cockburn. What holds: SEC-22 has an id, a "shall" sentence, five named checks and a source (Q04), and matches the Q04 verdict's one-sentence rule, its end conditions and its per-class table (verified line by line against the verdict). FR-84 has the three edits, a check and sources, and the phrases it removes exist in the restored contract text (verified). The grant list is four names everywhere (G1 resolved).

**H1 (MAJOR, Medium) The run line is "the go" for the first push of worker commits, and the duty to show those commits first is not tied to it.** origin=changed (FR-32, SEC-22, 3.1, row Q04). Experts: Wiegers, Nygard.
- FR-32: "push the worker commits only on a typed go, after showing them to the person, in a person-opened session; the person's typed `/sc:pr-submit --monitor 3` line is the go for that run's own pushes only (SEC-22)". SEC-22: the run line is "the go for that one run's first push, PR and fast-forward fix-round pushes only". The contract text the spec quotes (`WORKER-CONTRACT.md:245`): "Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go". The Q04 verdict says both things: its table lets the run line cover the first push (row 1), and its item 6 says the run line "covers the tool's fix commits only, not worker commits the person has not seen".
- The first push of a `/sc:pr-submit` run is the push that publishes the worker commits. The spec carries the table row and drops item 6, so no text says whether the person must have been shown the commits before typing the line.
- Grading: an implementer can build the run-line check so that a typed line alone is enough to publish worker commits the person never saw, or build it with a prior "shown" record. FR-32's own first clause supports the second reading, so the text allows the better one. Medium. No owner rule is broken: a person still types the line in their own session.
- Recommendation: one clause in FR-32 or SEC-22: "the run line is typed after the coordinator showed the worker commits (WC:245); it never covers commits not shown". Priority Medium.

**H4 (MAJOR, Medium) The Full Submit field is called a go without condition in four places; only SEC-15 says it waits on the owner.** origin=changed. Experts: Wiegers, Cockburn.
- 3.1: "the person's own typed `/sc:pr-submit --monitor 3` line (or the Full Submit field) is the go for that one run's pushes (SEC-22)"; row Q04, section 8 rules and SEC-22 say the same. SEC-15 alone says "the exception waits on the owner's chat approval of R25, OA-7". The Terms table (header) defines a go as "A person's typed answer in live chat that permits one named outward action (one push, one merge, one cleanup apply)", and SEC-14 says every go is given in chat. A GitHub Project field set earlier, and a run line that covers several pushes, fit neither definition. The Terms row was not updated.
- SEC-22 also drops two limits the verdict states for the Full Submit go: it runs in a top-level session (item 4), and a worker never types the run line (so who runs `/sc:pr-submit` under the field is left open).
- Grading: the field cannot act today: FR-52 keeps the Pipeline field unread while `GOVERNED_LEVELS_ALLOWED` is false, and OA-20 (level FS) is not flipped by default. An implementer of SEC-22 at S14 could still accept the field as a go before OA-7 is answered; the text allows the better reading through SEC-15. Medium (a safety-boundary reading would need the gate to be open, which no stage opens).
- Recommendation: put "inactive until OA-7 (R25) and OA-20" into SEC-22's first sentence, and make the Terms row say "one named outward action, or the one `/sc:pr-submit` run of SEC-22". Priority Medium.

**H6 (MAJOR, Medium) "S17 does not include ... label writes" against an S17 pass list that includes one.** origin=changed (S17 row) against unchanged text (8.2 closing paragraph). Expert: Wiegers.
- 8.2 closing: "S17 does not include raising the cap, Pipeline-field governed launches, label writes, `claim_by: coordinator` or a second polling host". S17 row (changed): "the six `first_run` checks green on the throwaway repo (its trigger label first made on the owner's chat OK naming that repo, or by hand; the label check only reads, FR-82)"; 10.4: "create each repo's trigger label only on a chat OK naming that repo, the throwaway repo's included (OA-28b)".
- Grading: "label writes" can mean the poll's label writer (stripped by FR-06) or any label creation. Under the second reading S17's own pass list cannot be met by the program, and falls back to "by hand". Two readings; the S17 row states the better one. Medium.
- Recommendation: "the poll's label writes". Priority Low within Medium.

=== ARCHITECTURE ANALYSIS ===

Experts: Fowler (lead), Newman, Hohpe, Nygard. What holds: SEC-01 and SEC-22 now divide the work cleanly (a push go never covers a merge, a merge go never covers a push; merge bound to the 40-character head sha); the label check (read) and label creation (write) are separate steps, which keeps the cycle and `github.py` read-only (owner rule 1); FR-29 and FR-84 name one adoption file with one writer (NFR-02 holds).

**H3 (MAJOR, Medium) SEC-22's five NEW checks have no stage and no component that could refuse a push made by `/sc:pr-submit`.** origin=changed. Experts: Fowler, Nygard, Crispin.
- SEC-22's checks: "a push with no run line, Full Submit field or go record is refused; a second run on the same PR needs a new line; a push after merge or close, or after a head move outside the run, is refused; a push after a rebase without old and new sha is refused; `push_count` above `max_rounds` + 1 cannot happen". The Q04 verdict's action row says "Build the run-go record and the end-of-go checks ... new coordinator code (merge path unit, spec S14)". The spec's S14 row lists "SEC-01 to SEC-13, FR-30 to FR-32" and L-11 lists "SEC-01 to SEC-13, SEC-21": SEC-22 is in no stage row, no L row and no verb of FR-26.
- Nothing in the architecture sits in the path of the tool's own pushes: the launch guard (L1) reads commands of launch-bound sessions only, L2 refuses only `main` and `master`, `/sc:pr-submit` runs in an ordinary person-opened session, and the verdict says to leave the tool and its fence unchanged. The project memory note the verdict cites says the tool's own guard missed a merged PR (PR 368). So "a push after merge or close ... is refused" has no enforcer.
- Grading: same shape as review 2's G2. The checks can be written as unit tests of a function the coordinator owns, so they can pass; the live pushes of the tool are not refused. 4.5 says "None is built; each narrows a risk and none closes it", and SEC-18 lists the residual risks. Medium.
- Recommendation: add SEC-22 to the S14 requirement column with the tests, and say in one sentence what refuses (a coordinator verb the person's session calls before the run line, or a hook), or say SEC-22's end-of-go rules are a record the coordinator reads at the merge go and refuse nothing earlier. Priority Medium.

**H2 (MAJOR, Medium) The fence and the count bound name only fix-round pushes.** origin=changed. Experts: Fowler, Whittaker (accumulation attack).
- SEC-22: "fast-forward fix-round pushes only, while the tool's fence holds (one fix commit per cycle, halt on `push_range_mismatch`, no force push, no push to the default or a protected branch, `push_count` at most `max_rounds` + 1)". The tool also makes CI pushes and Tier 2 conflict merge commits (counted in `push_count`, `SKILL.md:262`) and one Tier 1 sync push (`sync_push_count`, `SYNC_CAP = 1`, never in `push_count`, `SKILL.md:265`, `refs/state-machine.md` section 5.2d); `SKILL.md` bars only a merge commit "whose parents are not exactly the PR head and the recorded base tip", so a merge commit with those two parents is allowed.
- Trace (accumulation): `max_rounds` = 2; the run makes 2 fix pushes, 1 fallback push (so `push_count` = 3 = `max_rounds` + 1) and 1 Tier 1 sync push; the run has made 4 pushes against a stated bound of 3.
- Grading: an end-of-go check built from SEC-22's list refuses or ends the go at the tool's own sync or merge push, or lets a count of 3 stand for the run's total. Both are guesses between readings; the text names the tool's fence as the condition and the fence is the tool's. Medium.
- Recommendation: "the tool's own pushes of a run (fix, CI, sync and merge-commit pushes; `push_count` plus `sync_push_count`)". Priority Medium.

**H8 (MAJOR, Medium) One adoption record now holds the start state, but the creator-only-starts rule and the replay case are not carried over.** origin=changed. Experts: Nygard, Whittaker (sequence attack).
- FR-84 (1) replaces the restored "Create the adoption row (`adopt-create`) before `worker-start`; only a `created` result may start a worker" with a record that is "the FR-29 file ... created before `worker-start`, with `started` and `uncertain` as fields of it; the `adopt-create` row and `adopt-mark` store are not kept". FR-29: "save `issues/<repo-key>__<N>.json` by exclusive create (the one adoption record, FR-84), then ack". 3.1: "a wake may arrive twice, and handling a round twice must have no second effect".
- Trace: wake W arrives; handling 1 creates the file, then the coordinator dies before `worker-start`. Handling 2 (a replay or the restart of FR-34) finds the file by exclusive create; it has neither `started` nor `uncertain`. No text says whether handling 2 starts the worker, nor that only the call that created the file may start one. The restored sentence "only a `created` result may start a worker" is the rule that said so, and the FR-84 check bans the verb it used.
- Grading: either outcome is a reading of silence (skip leaves the issue stranded until a person looks; start is right here but wrong if handling 1 had reached `worker-start`). Medium.
- Recommendation: one clause in FR-84 (1): "only the call that created the file may run `worker-start`; a replay that finds the file reads `started` and `uncertain` and never starts a second worker". Priority Medium.

=== TESTING ANALYSIS ===

Experts: Crispin (lead), Gregory, Adzic. What holds: every changed requirement has a named check; the F10 and F14 fixes added named tests (`test_label_check_never_creates`, `test_label_create_needs_a_named_repo_ok`, `test_fixtures_carry_no_refused_grant`) and S8 and S9 list them.

**H5 (MAJOR, Medium) The label-create step has no named entry point, and at S9 nothing exists that can read the owner's OK.** origin=changed. Experts: Crispin, Hightower.
- FR-82: "Creating the trigger label is a separate step of `repo_init.py`, run only on the owner's chat OK that names that one repo, recorded by an agent (SEC-14)"; check `test_label_create_needs_a_named_repo_ok`; the S9 row lists the test. SEC-14's ledger is a file in a task package until S13; `answer-check` and the go entries arrive at S13 and S14 (FR-26, SEC-08, SEC-09). No verb in FR-26 creates a label. Planb's `first_run.py:193` calls `ensure_trigger_label` today, and `run-all` reaches `first_run` unattended (OAG3), so the planb behaviour has to change at S9 (L-08 says so).
- Grading: at S9 the test can only pass against an argument the implementer invents (for example a `--confirm-repo` flag); what "the owner's OK" is, and who calls the step, is left to a guess. The check can pass; the requirement is thin. Medium.
- Recommendation: name the entry point ("`issue-watch init-label --repo <R> --confirm <R>`" or the like, UNVERIFIED) and say the S9 test uses the explicit argument while the recorded-OK check arrives at S14. Priority Low within Medium.

**H7 (MAJOR, Medium) The new FR-07 check needs a loader that does not exist at S11, and half of it collides with SEC-06.** origin=changed. Experts: Crispin, Wiegers.
- FR-07 (L-10, S11): "NEW `test_fixtures_carry_no_refused_grant` (no fixture or reference config holds `pr.merge`, `issue.close` or `issue.hold`; a loader given `pr.merge` refuses it)". At S11 no grants loader exists: pr-a's `repos.py` (the only parser of `grants`; no `pr.merge` appears in pr-a `src/`) is dropped by FR-73, and FR-12 says a key gets loader support "in the PR that first reads it", which for `grants` is S14 (SEC-07, "one `E-NO-GRANT` case per entry"). SEC-06 ("refuse both as grant names") needs a negative case that holds `pr.merge`; the first half of the FR-07 check, read over every fixture file, would fail on it unless the case is built inline.
- Grading: the first half passes at S11; the second half has nothing to run against. Medium.
- Recommendation: "(the loader half is SEC-06's test, at S14)". Priority Low.

=== COMPLIANCE ANALYSIS ===

Experts: Wiegers (lead), Nygard, Hightower. The five owner rules, checked against the changed text:

| Owner rule | Where the spec states it | Result after the third pass |
|---|---|---|
| 1 The poll writes nothing to GitHub outside the named writers | FR-06, FR-82, FR-23, MC-8, OA-28b, 3.2 | Holds, and is stronger: the `first_run` label check only reads whatever `auto_enable` says; creation is its own step, behind a per-repo OK; the cycle, `github.py` and the poll never write. (Wording issue G3 of review 2 is unchanged.) |
| 2 A person's typed go before every push and merge | 3.1, 8 rules, FR-32, SEC-01, SEC-15, SEC-22, Q04 | Holds for merge (SEC-01 now says a push go never covers a merge and the reverse). For push the spec names one exception: the person's own typed `/sc:pr-submit --monitor 3` line, which is a typed go by a person and which the project's own rule already says "pushes the fixes without asking". The second part of the exception, the Full Submit field, is not a typed go; it is stated unconditionally in four places and conditionally only in SEC-15 (H4). The coordinator's own push stays strict (FR-32). H1 is the one place the first push is not tied to the show-first duty. |
| 3 Workers never run `/sc:pr-submit` | SEC-05, FR-32, FR-38, SEC-22 | Holds: SEC-22 says "A worker or the coordinator never types the run line; a worker's own script push is covered by no go (SEC-13)". The Full Submit route is the one open question (who runs the tool under the field, H4); it is dormant (FR-52, OA-20). |
| 4 No standing merge or close grant | SEC-06, SEC-12, OD-10, SEC-22 | Holds. SEC-22 creates no grant; the run go ends with the run; a push go never covers a merge (SEC-01). The four grant names (G1) contain neither `pr.merge` nor `issue.close`, and FR-07 now removes both from fixtures. |
| 5 Approvals given in chat, recorded by an agent | SEC-14, SEC-08, FR-82, FR-84, OA-28b | Holds in the changed text: label creation names the repo and is "recorded by an agent (SEC-14)"; FR-84 takes plan approval "from the owner's words in chat, recorded by the agent (SEC-08)". The Full Submit field is the one approval that is not a chat answer (H4). |

Worker-contract text the spec quotes, checked against the installed copy: line 23 (never-as-worker list), line 57 ("still written by the owner"), line 244 (PRs only through `/sc:pr-submit --monitor 3` in an ordinary session), line 245 ("no earlier pre-authorization waives this") and lines 296, 298, 300 (the three duties FR-84 amends). SEC-15 and FR-84 describe them accurately. SEC-22 does not contradict SEC-01, SEC-15 or FR-32; H1 and H4 are the two places where it is silent on a condition they state.

=== CORRECTNESS ANALYSIS ===

Experts: Nygard (lead), Fowler, Adzic, Crispin, Whittaker. Scope: changed lines only (re-review rule for FR-8 to FR-10).

### State Variable Registry (changed surface)

| Variable | Type | Initial value | Invariant | Read by | Written by |
|---|---|---|---|---|---|
| run go (SEC-22) | record: run id, PR, branch head shas made by the run, start time | absent | valid only from the typed run line until the run ends, the PR is merged or closed, or the head moves to a sha the run did not make; covers the tool's own pushes only; never covers a merge | the push check (no component named: H3) | the person's typed line; the recorder (not named: H3) |
| `push_count`, `sync_push_count` (tool) | int, int | 0, 0 | `push_count` <= `max_rounds` + 1; `sync_push_count` <= 1 (`SYNC_CAP`) | the run | the tool |
| per-issue adoption file `issues/<repo-key>__<N>.json`, fields `started`, `uncertain` (FR-29, FR-84) | JSON file | absent | one file per issue, exclusive create, one writer (coordinator); `uncertain` never restarts a worker | poll (phase), coordinator | coordinator |
| trigger label (per repo) | present or absent | absent | the poll and `first_run` never create it; creation needs an OK naming that repo | `first_run` label check (`label_present` or `would_create`) | `repo_init.py` create step on a named OK |
| `auto_enable` | bool | false | false until the S17 throwaway run; its flip is not an OK for any label | `first_run` | the owner once, in chat |
| `grants` | list of strings | empty | subset of four names; `pr.merge`, `issue.close` refused | verbs, `complete` | `repos grant` on a recorded chat go |
| fixture `grants` lists (FR-07) | list | n/a | none holds `pr.merge`, `issue.close`, `issue.hold` | tests | tests |

### Guard Condition Boundary Table (changed guards only)

An input class with no row is left out because it cannot occur for that guard; reasons are in the last row.

| Guard | Location | Input condition | Variable value | Guard result | Specified behavior | Status |
|---|---|---|---|---|---|---|
| run-go present | SEC-22 | Zero/Empty | no run line, no field, no go record | refuse | "a push with no run line, Full Submit field or go record is refused" | OK (enforcer: GAP, H3) |
| run-go push class | SEC-22 | Typical | fix-round fast-forward push within the count | allowed | covered | OK |
| run-go push class | SEC-22 | Legitimate edge | CI push, Tier 1 sync push, Tier 2 merge commit | not stated | whether the go covers them | GAP (H2) |
| run-go count | SEC-22 | Maximum/Overflow | `push_count` = `max_rounds` + 1; plus one sync push | "cannot happen" for `push_count` only | total of 4 at `max_rounds` 2 not addressed | GAP (H2) |
| run-go end | SEC-22 | Legitimate edge | PR merged or closed mid-run; head moved by another actor | refuse | stated; detection and enforcer not stated | GAP (H3) |
| run-go first push | SEC-22, FR-32 | Legitimate edge | worker commits not shown to the person | not stated | whether the run line covers them | GAP (H1) |
| Full Submit field | SEC-22 | Sentinel Value Match | field set, Pipeline field unread (FR-52) | not stated | accepted as a go or inert | GAP (H4) |
| label check | FR-82 | Zero/Empty | label absent | read only | `would_create`; repo stays off with a visible reason | OK |
| label create | FR-82 | Legitimate edge | OK names another repo, or none | refuse | "names that one repo"; test named | OK (mechanism at S9: GAP, H5) |
| adoption file | FR-29, FR-84 | Legitimate edge | exclusive create finds the file (replay) | not stated | who may start a worker | GAP (H8) |
| grants gate | SEC-06, SEC-07 | Sentinel Value Match | `pr.merge`, `issue.close`, leftover `issue.hold` | refuse | closed list; refusal case per name | OK |
| fixture rule | FR-07 | Legitimate edge | loader half of the check at S11 | no loader exists | not stated | GAP (H7) |
| all changed guards | n/a | One/Minimal, Typical where not shown | n/a | n/a | left out: they compare presence, an enum or a count; no input class beyond those rows exists | n/a |

Seven rows are GAP. All seven are the Medium findings above; none names a concrete wrong outcome without a guess between readings. The table is complete for the changed guards.

### Quantity Flow Diagram (the run's pushes, SEC-22)

```text
[one /sc:pr-submit run at --monitor 3, max_rounds = 2]
   --> [fix pushes F <= 2, plus fallback push (<= 1)]        push_count <= max_rounds + 1 = 3   (counted)
   --> [CI pushes and Tier 2 merge commits]                  inside push_count
   --> [Tier 1 sync push S <= 1 (SYNC_CAP)]                  sync_push_count, NOT in push_count  <-- N != M
   --> [run total = push_count + sync_push_count <= 4]       SEC-22 bounds 3
   --> [go ends: run end | PR merged or closed | head moved outside the run]
```

One divergence (the sync push); recorded as H2.

### Whittaker adversarial analysis (changed surface)

1. **Zero/Empty Attack.** The invariant at SEC-22 ("a push with no run line ... is refused") fails when the push is made by the tool in a session nobody guards: there is no component to refuse. Trace: person types the line; the PR is merged by someone else; the loop pushes the next fix to a recreated branch (the PR 368 case). Before: go ended at merge (stated). After: push lands, because no enforcer sits in the tool's path. (H3.)
2. **Divergence Attack.** FR-32 requires the show-first step and SEC-22 makes the run line the go for the first push. Both can apply at once to the first push of worker commits. (H1.)
3. **Sentinel Collision Attack.** "Full Submit field" is a go in SEC-22 and an unread field in FR-52. Trace: owner sets the field on an issue; level FS stays closed; SEC-22's check sees "field present" and accepts a push by a script that reads the field. (H4.)
4. **Sequence Attack.** Handling a wake twice (FR-29, FR-84): create file, crash, replay finds the file with no `started`: the order create, start, mark has a hole between the first two steps. (H8.) Also: label creation before `auto_enable` on, by hand or on an OK, then the S17 pass list needs it; the order is stated (S17 row) and consistent.
5. **Accumulation Attack.** The run's pushes can reach `push_count` + 1 sync push; SEC-22 bounds only `push_count`. (H2.)
