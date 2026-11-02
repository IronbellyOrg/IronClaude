# Round 1: Variant 3 advocate (option (c): person writes the Ruling line; coordinator dispatches a resume Task)

Citation key: as in `diff-analysis.md` (`SPEC:N`, `QA:N`, `LEDGER:N`, `RETRY:N`, `SKILL:N`, `CAPS:N`, `IMPL:N`). Every citation below was re-read in this run.

## Position summary
Keep the Ruling rule word for word, and add one route back into Orca: after the worker ends `failed`, the person either types the operator Ruling line into the ledger or resumes in their own session (V1's route), and the coordinator then dispatches a new resume Task, which ledger row R consumes with no review. I accept the diff analysis's framing (S-005) that this is (a) plus an extra path, not a disjoint option; the claim is that the extra path is worth adding because it needs no protocol change and keeps the rest of the plan unattended.

## Steelman
### Variant 1 (a)
The strongest case for (a): the person gives the Ruling in the very conversation where the executor has just explained "the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong" (`QA:254`). The decision is informed, and the executor formats the line, so there is no typing error to recover from. It needs no change anywhere: WC-3 and the implement row already carry the exception (`SPEC:67`, `SPEC:132`), and it is the spec's recommendation (`SPEC:335`, `SPEC:337`). Halts are rare by design: minors and notes never halt (`QA:274`, `QA:288`) and `E-HALT-QA` needs a confirmed blocker a repair could not close (`QA:280`), so moving one plan's remaining tasks into an attended session is a small, infrequent cost.

### Variant 2 (b)
The strongest case for (b): the person never leaves the coordinator conversation. Orca's `ask` is the designed channel for a blocking worker question (`CAPS:61`), it survives a timeout and resumes by message ID (`CAPS:60`), and no heartbeat is needed while blocked (`CAPS:64`). The person's words are quoted verbatim, and the Ruling line already allows "user confirmation provenance" in `<what>` (`QA:259`). For a person running many workers at once, one answer in one place with no file to open is the least friction of the three.

## Strengths claimed
1. **Same provenance as (a).** The person types the words; no agent message carries them. "another agent's message ... not acceptance" (`QA:254`) stays untouched, and a coordinator-written line is "executor-invented approval", a STOP (`QA:249`). Non-goal 6 holds (`SPEC:319`).
2. **The ledger already names this as the post-halt form.** "after a `halt`, the task gets only operator `Ruling:` lines, the post-ruling `complete` that Resume row R writes, operator-review `blocked` and `halt` records" (`LEDGER:110`). The Halt table accepts a "valid existing operator Ruling" as an alternative to confirmation (`QA:248`), the spec itself lists it as today's second route (`SPEC:334`), and "the user need not hand-write a ledger record" (`QA:254`) implies the user may.
3. **Deterministic consumption.** Row R ("An eligible Ruling with no `complete` after it → Append the post-ruling `complete` ... with no review", `LEDGER:154`) sits before P and H, and "First match wins; the row order is part of the rule" (`LEDGER:149`). Every ladder halt writes a `halt` record (`RETRY:441`), so a line after it is eligible under clause (a) of `RETRY:498`. Diff spot-check 3 confirms this.
4. **The plan stays in Orca.** The resume Task is a new Task (WC-6, `SPEC:70`) whose command line is unchanged because `--resume` is implicit when a ledger matches (`IMPL:57`). This falsifies V1's "the remaining tasks of that plan leave Orca" (X-002).
5. **Cheaper resume than V1's described path.** V1's person resumes with no Ruling yet, so resume falls to row H: a fresh operator review, then `halt ... reason=operator-review` and STOP `E-HALT-QA` (`LEDGER:156`), before the executor can explain and ask. A hand-written line skips that extra reviewer run.
6. **No person wait inside a worker.** The wait sits between Tasks, so no session is held open (contrast `CAPS:64`), and nothing depends on an answer arriving before the worker settles (`SPEC:67`).
7. **Single writer by construction.** The ledger has no lock (`LEDGER:145`); the person writes only after the worker has settled, which WC-6 already requires before any retry (`SPEC:70`).
8. **Checkable live.** Extend AC-4.1 (`SPEC:274`): append a hand-written line after the halt, dispatch the resume Task, expect `complete` with the unchanged non-compliant verdict (`QA:248`, `LEDGER:82`).
9. **Strictly no less safe than (a).** It removes nothing from (a); (a) remains available when the person wants the executor's explanation.

## Weaknesses identified
### Variant 1 (a)
1. **Its main cost claim is wrong.** "the remaining tasks of that plan leave Orca" (V1 line 19) does not follow from the rule: row R plus a resume Task returns them (`LEDGER:154`, `SPEC:70`, X-002). V1 adopts a cost it does not have to pay.
2. **It omits the extra review on its own path.** Resuming with no Ruling hits row H (`LEDGER:156`): one fresh operator review, then a re-halt with `reason=operator-review`, before the executor explains and asks (C-005). V1 says only "resumes from the ledger".

### Variant 2 (b)
1. **It breaks the rule it relies on.** By its own text, "It contradicts the rule as written" (V2 line 13; `QA:254`), so it needs a protocol edit against non-goal 6 (`SPEC:319`), and the worker cannot tell a paraphrase from the person's words (`CAPS:62`; X-004).
2. **It has no resume path.** Any `halt` is terminal (`RETRY:488`) and the command has already stopped. WC-3's ask route is limited to "a gate that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag" (`SPEC:67`); a Ruling halt fails both, and `/sc:implement` has no Ruling flag (`IMPL:6`). "keeps its session, its ledger position and its retry state" (V2 line 8) needs a new route that V2 does not design (X-003).
3. **Uncounted cost.** Asking mid-command either makes the command run an `orca` command, which SA-2 forbids (`SPEC:170`), or needs a redesigned re-invoke route (C-007).

## Concessions
1. **Spot-check 4 (WRONG) is right.** A hand-appended line is the ledger's last line; if malformed (for example hyphens for em dashes, against `LEDGER:71`), resume stops at `E-LEDGER-CORRUPT` (`LEDGER:123`; `SKILL:36`, "No further"), not at row H. It is still a safe stop (ledger "Unchanged", `SKILL:36`), and the fix is one edit to a line the person typed, but my variant said "ignored" and that is wrong. Fix that keeps the rule: the coordinator's brief requires a read-only check of the ledger's last line against `LEDGER:71` and of eligibility (`RETRY:498`) before dispatching the resume Task; on failure it tells the person and never edits the line. This is a coordinator rule, so SA-2 is untouched.
2. **Spot-check 2 (OVERSTATED) is right.** "Existing operator-written records remain valid" (`QA:256`) and "The earlier operator-written form ... remains valid" (`LEDGER:195`) read as backward compatibility, and the section heading is "user-authorized, executor-recorded" (`LEDGER:62`). Restated claim: a newly hand-written line is mechanically valid (`LEDGER:71`, `LEDGER:110`, `RETRY:498`) and permitted by implication (`QA:254`, `QA:248`), but no line explicitly sanctions it as a route. The D2/WC-3 sentence must state it, which is a spec change, not a protocol change.
3. **V1 is better on the informed decision (C-003).** A hand-writer sees only the halt message (ledger path, task, verdict, missing citations, `QA:247`; full list `RETRY:490`), not the executor's scoped explanation (`QA:254`). For a `dispute` halt about the AC itself (`RETRY:107`), (a) is the better route.
4. **Provenance is policy, not mechanism (A-010).** Eligibility is positional (`RETRY:498`); any agent with file access can append a line. This is equally true of every operator-written line today, and V3's "coordinator-written line is invalid" rule is text only.
5. **Not a separate option (S-005).** The real choice is (a) alone, (a)+(c), or (b).

## Shared assumption responses

| A-NNN | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | `QA:254` lists "another agent's message"; the answer arrives as the coordinator's `reply` (`CAPS:62`) |
| A-002 | ACCEPT | `QA:248` "unchanged non-compliant verdict"; `LEDGER:82` post-ruling `complete` preserves all verdict fields; row R writes it (`LEDGER:154`) |
| A-003 | ACCEPT | "Trust ledger + git history after compaction" (`LEDGER:137`); the per-task table is first-match (`LEDGER:149`) |
| A-004 | QUALIFY | True as codes, but `dispute` is an `E-HALT-QA` reason (`RETRY:107`, `RETRY:441`), so it is inside the set; `E-RESUME-NEEDED` needs a re-run, never a Ruling (`QA:250`) |
| A-005 | ACCEPT | The coordinator is an Orca coordinator session, an agent (`SPEC:316`, `SPEC:334`) |
| A-006 | ACCEPT | `QA:274`, `QA:288`, `QA:280`; rarity also keeps V3's per-halt hand-writing cost small |
| A-007 | ACCEPT | `CAPS:62` |
| A-008 | QUALIFY | A real gap, but the contract carries `blocked_question` (`SPEC:66`) and "the coordinator opens it" (`SPEC:68`); the spec should require the coordinator to show the person the halt text and ledger path. V3 needs this more than V1, since the person writes from the halt text alone |
| A-009 | QUALIFY | Equal for V1 and V3. Placement is the coordinator's explicit `--worktree` choice (`CAPS:116`) and orchestration verbs never delete a worktree (`CAPS:115`), so the ledger survives; remote workers are out of scope (`SPEC:322`). The spec should say the person needs local access to the worker's worktree |
| A-010 | QUALIFY | Eligibility is positional (`RETRY:498`); the person-only rule is policy in every variant, and V3 at least states it (concession 4) |
| A-011 | REJECT | Not out of scope: a dispute writes `halt review=<k> reason=dispute` and STOPs `E-HALT-QA`, "A dispute is the operator's call (Ruling path)" (`RETRY:107`); all variants cover it through `E-HALT-QA`. V1's route is better for it (concession 3) |
| A-012 | QUALIFY | Holds for every `E-HALT-QA`, which always writes a `halt` (`RETRY:441`). Where no `halt` follows a `blocked` but `retry` records exist, the line is ignored with a note (`RETRY:500`) and resume continues by other rows: safe, and caught by the pre-dispatch eligibility check (concession 1) |

## Per-point positions

| ID | Superior approach | Reason |
|---|---|---|
| S-001 | equal | Section layout only (L1) |
| S-002 | V3 | Only variant citing the eligibility rule (`RETRY:498`) and the resume rows |
| S-003 | V1 | Drift note applies whatever wins; stale anchors also at `SPEC:67,132,319` |
| S-004 | V2 | Most self-critical, though V3's weakness bullet is now extended by concessions 1-3 |
| S-005 | V3 | Superset of (a): adds a route, removes none |
| S-006 | V3 | Gives a concrete AC-4.1 extension with an expected ledger result |
| C-001 | equal (V1, V3) | Both keep the person's own words; V2's arrive as an agent message (`CAPS:62`) |
| C-002 | V1 | Executor-formatted line removes the typing risk; V3 keeps provenance but adds that risk |
| C-003 | V1 | Executor explanation before acceptance (`QA:254`); V3 offers (a) for when it is wanted |
| C-004 | V3 | Remaining tasks return to Orca via row R and a new Task (`LEDGER:154`, `SPEC:70`) |
| C-005 | V3 | Row R before H skips the extra operator review (`LEDGER:149-156`); V2 has no resume path |
| C-006 | V3 | No worker session held during the person's wait |
| C-007 | V1 | Zero spec change; V3 needs one sentence, one AC, one coordinator check; V2 edits the rule |
| C-008 | V3 | Deterministic table-row check; V2's relay fidelity is uncheckable |
| C-009 | V3 | Only variant to state the single-writer precondition (`LEDGER:145`) |
| C-010 | V1 | V3 was wrong (`LEDGER:123`); fixed by the pre-dispatch check, but V1 has no such risk |
| C-011 | V1 | Only variant to argue frequency (`QA:274,280,288`); the argument helps V3 too |
| C-012 | V3 | Adds a route while keeping (a) unchanged; easiest to drop if unused |
| X-001 | equal (V1, V3) | Neither relays; V2 concedes the conflict |
| X-002 | V3 | Rule kept and plan stays in Orca, falsifying V1 line 19 |
| X-003 | equal (V1, V3) | WC-3's ask route does not fit a Ruling halt (`SPEC:67`, `IMPL:6`) |
| X-004 | equal (V1, V3) | V2's internal conflict; V1 and V3 are not party |
| A-008 | V1 | The executor's explanation partly fills the gap; all need a spec rule to surface the halt |
| A-009 | equal | V1 and V3 both need local ledger access |
| A-010 | equal (V1, V3) | Positional eligibility in both; V3 at least states the rule |
| A-011 | V1 | A dispute about the AC is best answered with the executor's explanation |
| A-012 | V3 | Explicit about the eligibility condition and adds a pre-dispatch check |
