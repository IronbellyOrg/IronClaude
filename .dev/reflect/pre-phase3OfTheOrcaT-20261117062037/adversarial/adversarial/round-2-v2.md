# Round 2 rebuttal — V2 (qa)

## Position and grading rule

The plan still fails pre-execution review. My final blocking set is **C-001, C-002 and C-003**. I withdraw my Round 1 BLOCKING grades for C-006 and C-011, and my MEDIUM grades for C-008 and C-015.

I use the requested rule: BLOCKING requires a correction to a named decision, behaviour, acceptance check or quoted number **the plan rests on**, a missing required deliverable, or a broken safety boundary. MEDIUM means a real weakness without that dependency; NOTE means form only. A possible bad implementation is not, by itself, proof that the plan must be blocked.

I read the transcript and tally, V1's rebuttal, the diff analysis, all three original cards, and the plan. I separately searched the current tests and re-Read the source and spec passages cited below. This is a static audit, not a test run or proof that unimplemented changes pass.

## 1. Answers to criticism of V2

### C-003: I overstated the fixture claim; the blocking contradiction remains

**Concede the overstatement.** A question can have a valid payload dispatch id and no matching collected worker. The plan explicitly requires that missing-row case. A payload marked `linked` therefore does not necessarily share an id with an exported worker row. My original phrase “necessarily shares” was wrong.

The actual contradiction is narrower and sufficient: the plan requires the **found-worker** case as well. Its Task 6 check forbids *any* question dispatch id anywhere in the snapshot, while preserving the snapshot implementation. The current exporter includes every collected worker's dispatch id:

- `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/export.py:25-26,131-145,195` defines and exports `rows[].dispatchId`.
- `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/release-gates.md:60-62` records all 18 question dispatches in the 144 worker rows and defines that join as the link evidence.
- `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md:78,99-103` requires the found-worker case, preserves the exporter, and states the incompatible exclusion.

This is **BLOCKING Gap**, not my original Regression classification: it is an unsatisfiable acceptance check on a representative found-worker fixture, not an already-observed code regression. Limit the dispatch-id exclusion to the snapshot's `questions` group, keep the whole-snapshot ask exclusion and byte equality, and include the matching worker in the fixture. Do not remove legitimate worker identifiers or evade the check with an absent worker.

### Missed C-004, C-005 and C-006

**Concede all three omissions.** Calling INF-008 “partial” did not identify the missing source of link state or the first-selection problem. Saying INF-003 to INF-006 had explicit tests did not prove the data path or the typed join was adequately specified.

- `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/collector.py:38-68` has no link-state field. A desk that exists only after selection cannot itself authorize the first selection. Keep C-004 MEDIUM and name the link-state source.
- `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/render.py:304-317,377-388` gives the panel renderer no selection input and collapses the panel when spare height falls below one. Keep C-005 MEDIUM; make selection reach the renderer and budget the fallback desk notice before sacrificing the question list. The short-height acceptance check should expose the budget problem, but that does not make the missing data path disappear.
- C-006 is a genuine typed-identity hazard; my subsequent Round 1 escalation was too strong under the frozen rule. See the final ruling below.

My original 0.97 confidence was not justified by these omissions. It must not become a weight in the merge.

### C-002: V1's reachability qualification is right, not a downgrade

**Accept the qualification.** Once the new guard is True, the normal questions-on command path will also have linking on after C-001 is fixed. The link-off regression primarily affects rollback and explicitly link-disabled collectors. But link-off compatibility is expressly required, not hypothetical scope invented by the reviewers. Updating an unconditional questions help constant changes that named behaviour. BLOCKING stands; V1 now agrees.

### C-007, C-008, C-011 and C-015

V1's narrower evidence changes my earlier grades. I accept C-007 as NOTE; concede C-008 to NOTE, C-011 to MEDIUM and C-015 to NOTE for the reasons in section 3. “Would strengthen testing” is not itself a missing required test.

### C-009 and confidence in coverage

I retain **MEDIUM Gap** for desk missing-value and freshness assertions. Nine labels alone do not check that absent values remain honest or that retained worker evidence carries its stale/as-of qualification. Those behaviours are named in Task 4, but their implementation is already required; the weakness is the test coverage, not a contradictory behaviour instruction or missing feature deliverable. No basis to promote it to BLOCKING.

## 2. Responses to V1's open-point rulings

| Point | Ruling | Reason |
|---|---|---|
| S-001 | **ACCEPT** | Merge verified findings, not card size. Finding counts are not votes or quality measurements. With my severity concessions, C-001/C-002/C-003 are the blocking set. |
| S-002 | **ACCEPT** | Discard self-reported confidence as a merge weight. My 0.97 was overconfident; attach verification limits to each claim instead. |
| S-003 | **COUNTER-RULING: preserve verified coverage and exclusions, not unchecked statements verbatim** | Agree that checked/not-checked information matters. However, V1 repeats V3's inaccurate statement that register line 33 “exists only after execution.” The line exists now; its proposed payload-shape amendment is future work. Do not turn a claimed read or a mistaken existence statement into evidence. |
| X-004 | **ACCEPT — Necessary deviation, no additional finding** | The prototype does not define C fully; the plan explicitly chooses a stacked block, updates the contract first, and preserves the owner-confirmed dispatch-level scope. The two-column layout is expressly excluded, not silently omitted. Keep genuine stale-spec findings separately; do not invent another scope-drift blocker. |
| A-002 | **ACCEPT V1's focus table and deletion of “resetting inspector_scroll” from question navigation** | This is the smallest explicit rule consistent with existing routing. Link-on, not desk existence, enables the initial question selection. |
| A-003 | **ACCEPT the qualified assumption, with the frozen severity rule controlling** | Ambiguity does not inevitably become wrong code. Do not infer execution failure from prose alone. Conversely, a passing test is not permission to violate a named constraint, omit a required deliverable or cross a safety boundary. |

### S-003 correction, with direct evidence

`/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md:29-37` already contains the message-row section and its line-33 envelope/key list. Only the requested 39-of-41 payload-shape wording is not yet written there. `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md:61-64` ends the numbered table at T56 before the snapshot section; T57–T66 are genuinely future additions. Preserve those two different facts accurately.

For X-004, the supporting passages are `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md:8,43,104-105`, the dispatch-level owner record at `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/release-gates.md:58-62`, and the plan's explicit exclusion and contract-first change at `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md:25,34-35`.

### A-002: exact accepted focus behaviour

| Focus | `n` / `p` | Esc |
|---|---|---|
| List | Next/previous retained question, only with a nonempty question panel and linking enabled; otherwise unchanged state returned as a new Session. With no selection, `n` starts oldest and `p` newest; stop at the ends. | Clear question selection, otherwise no change. |
| Filter | Append ordinary text to the filter; leave question selection unchanged. | Leave filter focus only; preserve filter text and question selection. |
| Inspector | Ignore; leave question selection unchanged. | Return to list and retain question selection; a subsequent list-focus Esc clears it. |

My original REJECT answered the literal claim “free in every focus,” which is false for text entry, but did not distinguish that from compatibility of the proposed bindings. V1's qualified table resolves that distinction, so I accept it. There is no need for a competing key scheme.

Evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/view.py:982-999,1027-1038` routes filter input first and treats inspector Escape separately. The proposed deletion applies only to the new question-navigation wording; keep the existing inspector exit/reset behaviour. `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_session.py:273-313,396-413` pins existing focus transitions and fresh Session objects. Add per-focus assertions for the new bindings.

One correction to V1's test argument: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_session.py:359-393` does exercise printable keys in all focuses, but asserts return types and permitted effects, **not** that `n`/`p` leave selection unchanged. Their no-op behaviour without a question panel follows the proposed contract; that existing test does not by itself prove it. Keep A-002 with C-004 as MEDIUM clarification, not an extra blocker.

For A-003, I accept V1's rejection of literal-executor determinism, not an automatic rule that “an existing test would catch it” converts every real defect to NOTE. Here C-007 is NOTE because the instruction to add a sentence is compatible with retaining the pinned sentence; C-015 is NOTE because the claimed coverage gap is already covered. Those are evidence-based reasons, not confidence in an executor guessing correctly.

## 3. Final severity rulings

| Point | Final ruling | Reason under the frozen rule |
|---|---|---|
| C-002 | **BLOCKING Regression** | Task 4 expressly edits the questions keys line, selected for every question panel, while the constraints promise exact link-off compatibility. Correcting it changes that named instruction to choose a separate link-enabled keys line and adds the missing link-off comparison. Rollback reachability is sufficient. |
| C-003 | **BLOCKING Gap** | Correcting the whole-snapshot dispatch-id prohibition changes a named, contradictory acceptance check. A found-worker fixture must preserve its worker id. |
| C-006 | **MEDIUM Gap — concede** | Display-text equality can fabricate a match for an unknown-identity row, and even quote a legitimate literal `unknown` id differently. But specifying the typed comparison implements, rather than changes, the already-named dispatch-id equality rule. No missing deliverable or read-only/privacy boundary is shown. My “false authoritative link” argument established a real risk, not the extra criterion needed for BLOCKING. |
| C-007 | **NOTE — accept** | “Module docstring” is the wrong location name; the specified range is HELP. Task 3 says add a sentence, not rewrite the pinned one. Append a conditional explanation of link-enabled question text; do not weaken the existing assertion. |
| C-008 | **NOTE — concede** | The plan already requires invalid ids to be unlinked and fixes the available reason vocabulary. Assigning a present-but-invalid/non-string id to `payload has no dispatchId` makes that existing category explicit without changing the behaviour or introducing a sixth state. A new distinct reason is not required. |
| C-011 | **MEDIUM Drift — concede** | AD-18 really names a later module and field group. However, this plan expressly relies on screen-only question text and an unchanged snapshot, not on that module split or a link field group. Amending the architecture description to record this phase's chosen implementation preserves the plan's named behaviour. Real stale architecture documentation, not a missing plan deliverable or a reason to add an unnecessary module. |
| C-015 | **NOTE — concede** | The existing command test pins exact message argv, one worker call and no peek. With the new constant True and C-001 corrected, it exercises the link-enabled command path; Tasks 3 and 7 run it. A distinctive linked-payload command assertion is useful within C-001, not a separate uncovered INF-009 blocker. |

Supporting source details:

- **C-002:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/view.py:78-81,914` shows the constant and unconditional panel-based choice. `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/render.py:359-388` shows footer wrapping affecting panel space. `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_render.py:748-758` compares with the imported constant or fallback key tokens, not old bytes. Do the questions-on, link-off comparison at 160/116/80; the R1 questions-off comparison is not a substitute.
- **C-006:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/view.py:322-329,445-447` distinguishes sentinel UNKNOWN from the literal string and makes RowView ids presentation text. Use raw typed dispatch ids, skip UNKNOWN, and normalize missing question ids before record formatting. This is not a source-id sanitization redesign.
- **C-007:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/commands.py:78-94` is HELP; `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_commands.py:728-743` pins its existing disclosure. Preserve the sentence and add the conditional qualification.
- **C-008:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md:34,50-53` specifies validity, unlinked fallback and the five-state vocabulary. Make the mapping explicit; do not claim parser code already exists.
- **C-011:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/ARCHITECTURE-SPINE.md:174-178,285` is the genuine mismatch. Extend Task 7's documentation closure to reconcile both passages with the screen-only, no-snapshot-change implementation. Do not interpret “optional field group” as authorization to override the plan's export decision.
- **C-015:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_commands.py:652-668` is the existing exact argv assertion. Its question payloads are currently absent; the additional distinctive linked payload remains part of C-001's command-wiring proof, not evidence that INF-009 has no tests.

## 4. Independent test search: exact record question lines and one-shot screen output

**Result: I found no existing assertion that compares a complete record question line, requires its old ending, or otherwise fails merely because Task 6 appends ` | dispatchId=... | link=...`. I also found no existing one-shot question-screen assertion requiring the old subject when Task 4 provides real question text. V1's narrowly stated claim is supported.**

Search scope was all of `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe`, using `record_text`, `--once`, `reason unknown`, line splitting/ending checks, output equality checks, and golden/export/file-read paths. I followed the record helper and command-output helpers rather than assuming the literal search covered aliases. The closest assertions are:

| Re-read assertion | What it pins | Why the proposed change does not invalidate it |
|---|---|---|
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_commands.py:669-674` | Exact panel title/run/count lines; substring count of four `reason unknown` lines. | These are not complete question-line comparisons. Appending the suffix after the subject-form text leaves the substring count and structural lines unchanged. |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_commands.py:687-690` | One-shot screen exit status, width bound, panel title and gap-notice absence. | No exact question text. It does not test payload question display. |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_export.py:269-284` | Full question id, inert markup, disclosure/count lines, and three lines containing both ` | ` and `reason unknown`. | No delimiter-count or ending assertion; the suffix does not change those predicates. Its collector is explicitly questions-on with the future link default off, at lines 263-265. |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_export.py:295-309` | Retained failed-state disclosure and a count of two `reason unknown` occurrences. | Again substring/count checks, not exact question lines; collector remains link-off by default. |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_question_cap.py:71-84,124-134` | Window-full disclosure and absence of a fabricated total in combined screen/record/snapshot output. | Neither check is tied to the question-line ending. |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_export.py:50-58,71-81,84-97` | Full worker ids, worker-line counts and equality across filter sessions. | These select lines **starting** `dispatchId=`. The new question suffix contains that text inside a line starting with a question id. These tests also build questions-off views. |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_render.py:611-624` | Exact equality of the entire R1 surface, including saved record text. | Important near-counterexample, but `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/release1_surface.py:41-54` uses a questions-off collector. There are no question record lines for the suffix to change. |

Two nearby checks must not be misreported:

1. `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_view.py:943` checks `QuestionLine.text.endswith("reason unknown")`, not a record line. Task 4 explicitly preserves `text` as the subject form and adds separate `screen_text`; Task 6 appends only when building the record. This assertion is not a counterexample.
2. `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_parse.py:586-591` forbids a parsed `dispatch_id` attribute today. It really will need changing, and Task 2 expressly names the rewrite. It is neither a record-output assertion nor a newly omitted migration.

Why the command tests are weak proof of new question display: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_commands.py:612-616` builds rows through the existing helper; `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/conftest.py:255-267` gives them subjects and `payload: None`. After the gate wiring is corrected they exercise the intended `no payload` suffix, but Task 4's fallback still renders the subject. They cannot prove that a nonempty payload question reaches a one-shot screen. This supports retaining C-001's distinctive-payload command check, not inventing an existing-test regression.

There are **no changed exact record-question assertions to name**. The table identifies the actual candidate file/line assertions and why each survives. This is a search finding, not a claim that the unimplemented patch or full suite has passed.

## 5. Merge recommendation and limits

Carry **C-001/C-002/C-003 as BLOCKING**. Keep C-004/C-005/C-006/C-009/C-011/C-012/C-013 as MEDIUM. Keep C-007/C-008/C-010/C-014/C-015 as NOTE. X-001 and X-002 follow C-002/C-003; X-003 is settled by the existing argv test, with linked-payload hardening folded into C-001. Use V1's A-002 focus table and qualified A-003 reasoning, with the test-proof qualifications above. Preserve S-003's verification limits after correcting the register-line existence error.

Only this rebuttal file was written. No plan, source, test, spec or ledger was edited; no tests or live Orca calls were run. The next step is V3's sequential rebuttal and then per-finding merge, not implementation. Residual risk: these are pre-execution static findings, not runtime evidence.
