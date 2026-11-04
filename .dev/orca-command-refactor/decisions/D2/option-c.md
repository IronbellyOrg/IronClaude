# D2 option (c): the person writes the Ruling into the ledger; the coordinator re-dispatches a resume worker

Position: keep the rule exactly as in (a): no agent ever relays a Ruling, and the worker reports the halt as `blocked` and ends `failed` (`SPEC:67`, `SPEC:132`). Then the person gives the Ruling by writing the existing operator-written Ruling line into the ledger themselves (or by running `/sc:implement` in their own session as in (a)). Once the person says the line is written, the coordinator creates a new worker Task with the same plan and `--resume` (WC-6, `SPEC:70`), and the remaining tasks run unattended again.

Citation key: `SPEC:N` = spec line; `QA:N` = `src/superclaude/skills/sc-implement-protocol/refs/qa.md:N`; `LEDGER:N` = `src/superclaude/skills/sc-implement-protocol/refs/ledger.md:N`; `RETRY:N` = `src/superclaude/skills/sc-implement-protocol/refs/retry.md:N`.

## Why this works with no protocol change
- An operator-written Ruling is already valid: "Existing operator-written records remain valid" (`QA:256`); "The earlier operator-written form (`T2: Ruling: drop pagination — AC-2 deferred to next spec — cost-if-wrong: list stays unpaginated`) remains valid" (`LEDGER:195`). The line format is fixed by a regex (`LEDGER:71`).
- Resume consumes it without asking anyone: resume row R, "An eligible Ruling with no `complete` after it → Append the post-ruling `complete` ... with no review", is checked before every other non-complete row (`LEDGER:149-154`). A Ruling written after the halt is eligible (`RETRY:498`).
- `--resume` is implicit when a ledger matches (`src/superclaude/commands/implement.md:57`), so the new Task's brief is the same command line with a fresh report directory.

## Safety
- Same provenance as (a): the words in the ledger are typed by the person, not carried in another agent's message (`QA:254`). The coordinator never writes the line; a line written by the coordinator would be "executor-invented approval" (`QA:249`) and the spec must say so.
- One writer at a time: the ledger has no lock (`LEDGER:145`), so the person writes only after the halted worker has settled, which WC-6 already requires before any retry (`SPEC:70`).

## Reliability
- Deterministic: the resume path is a table row, not a judgement (`LEDGER:149-154`). Checkable live by extending AC-4.1: after the halt, add a hand-written Ruling line, dispatch the resume Task, and expect `complete` for that task with the unchanged non-compliant verdict (`QA:248`).

## How a person works day to day
- The person reads the halt, decides, and either types one ledger line (then tells the coordinator "Ruling written"), or resumes in their own session as in (a). The rest of the plan stays in Orca.
- Weakness: a hand-written line skips the executor's scoped explanation before asking (`QA:254`); the person must read the halt message, which prints the ledger path, task, verdict and missing citations (`QA:247`), and write all three fields (what, why, cost-if-wrong, `LEDGER:65`). A malformed line is ignored and the resume halts again (`LEDGER:156`), which is safe.

## Implementation cost
- Zero protocol change. Spec change: one sentence in D2/WC-3 and one AC-4.1 extension. If people find hand-writing the line awkward, (a) stays available unchanged.
