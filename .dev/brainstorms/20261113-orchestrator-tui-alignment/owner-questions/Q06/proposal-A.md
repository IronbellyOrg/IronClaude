# Proposal A: keep the questions read switched off and park the live tests

## Answer

Do not switch the questions read on, and do not schedule the seeded consumption test or the live-layout attempt in this program; the guard stays off until a later release (Decision Desk, release 3) actually needs the panel, and the scope question is asked again then.

## What happens next if the owner picks it

- `QUESTION_GATE_PASSED` stays `False` on master (`observe/commands.py:67`); `--questions` keeps making no Orca call.
- OB-03 (seeded test), OB-04 (live-layout attempt), OB-05 (build pin) and OB-06 (flip pull request) are recorded in the ledger as "parked by owner, Q6, date", with the trigger "release 3 is opened".
- No throwaway Run is created and no seeded messages are written; no `GRANT(OB-03,seeded-write)` or `GRANT(OB-04,live-read)` row (a ledger permission row for one item and one outward action) is needed.
- The sweep keeps its caution text, and Q10 (whether the sweep may read messages) keeps its "observer's alone" answer with nothing behind it.

## What it unlocks

- Removes two live Orca lanes from wave W1, so the program does not depend on the Orca app being reachable (it was not reachable on 2026-11-13, `merged-requirements.md:604`) or on Q24 and Q30 (who runs live reads, which Run OB-04 reads).
- Zero risk of losing a coordinator's questions: nothing reads any mailbox.

## What it costs or risks

- The built panel stays dark; the human gets no in-terminal view of coordinator questions from this program.
- The consumption question (ADJ X-016, unproven both ways at 61 percent) stays open, so the sweep's caution and the observer's caution both remain unverified claims.
- The owner records the flip would cite still sit only in the sibling worktree `issue-409-mvp`; parking the flip removes one reason to commit them soon (Q7), raising the risk of losing them if that worktree is cleaned (`merged-requirements.md:264`).
- The two unpushed switch-on commits in the sibling age further against master.

## What stays unresolved

Whether `check --all --types question` consumes on a live Run; whether the panel is usable in the terminal that holds a Run (Q-1 failed); the scope sentence itself.
