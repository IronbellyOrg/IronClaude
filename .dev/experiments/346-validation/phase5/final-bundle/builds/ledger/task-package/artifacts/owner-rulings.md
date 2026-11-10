# Owner rulings received after the plan was pinned

The plan was pinned (PLAN line in progress.md) and Task 1 had started, so these rulings are applied inside the existing tasks without editing the plan. Every departure from the frozen plan is listed in `.dev/brainstorms/346-ledger/INSTALL.md` and in the worker_done body.

## 2026-11-08, coordinator message "Owner ruling: read-only script calls are allowed in review sessions" (Option A)

Verbatim body: "Owner ruling on scripted steps, for the whole team: Option A. Reviewer and reviser sessions may run ONLY read-only script calls, meaning calls that write no file anywhere (for example status, check --dry-run, fixcheck --dry-run or your script's equivalents), to self-validate and to use the spec's one repair turn. Any call that writes a file (begin, a real check that appends to the report, snapshot, enforce, apply, revert, ledger updates) is run by the coordinator as its own inserted step with its own brief template. A reviser writes any fix map or ledger content only INSIDE its own allowed output file (its disposition file, e.g. as a '## <script name> fixmap' block), and the coordinator's inserted step reads it from there. Plan the dry-run flags so they provably write nothing, and test that they write nothing."

## 2026-11-08, coordinator answer to the worker's question (Proposal A approved)

Verbatim answer: "Approved: Proposal A. Build the dry-run support inside the existing tasks without editing the frozen plan. Conditions: (1) when a task reviewer flags the plan's 'never run the writing script' wording, answer with a scoped operator Ruling in the ledger quoting this message as the owner's acceptance; (2) do not weaken or delete any test, and keep the test that hashes the whole ledger folder, the document and the report before and after a dry-run call and asserts no change; (3) list every departure from the frozen plan in INSTALL.md and in your worker_done body."

Proposal A as asked: add `--dry-run` to `find`, `answer`, `verify` and `sweep --input` (validates the input and the anchors, prints the would-be result, writes no file; a test hashes the whole ledger folder, the document and the report before and after and asserts no change); make `answer --input` accept the reviser's disposition `.md` (one `ledger-input` block); the command text, SKILL.md and ledger-step templates say review and reviser sessions may run only `status`, `verdict` and `--dry-run` calls.

## Departures from the frozen plan (kept current)

1. `--dry-run` on `find` (added in Task 2's diff), `answer` (Task 2), `verify` (Task 3) and `sweep --input` (Task 4).
2. Review and reviser sessions may run `status`, `verdict` and `--dry-run` calls (Tasks 5, 6, 10, 12 text), where the plan says they run no script.
3. The reviser may put an `answer` block (`ledger-input`) inside its disposition file; the coordinator's ledger step runs `answer --input <disposition.md>` before `begin`.
4. `revert-unclaimed --hunk` takes the key `status` lists for a provisional hunk instead of a bare number (the fix for blocking finding F1.1 of the Task 2 review; the plan's `[--hunk k]` names the argument only).

## 2026-11-08, coordinator message "Owner ruling: make lint Check 6 needs an Activation heading"

Conditional ruling: if `make lint` failed on Check 6 (no `## Activation` heading for a command paired with an `sc-*-protocol` skill), add the heading above the activation line and record a Ruling. Not applied: `make lint` passes for this variant (0 errors; Check 6 passes, because the variant activates `sc-review-ledger`, not an `sc-*-protocol` skill). No change was made for it.
