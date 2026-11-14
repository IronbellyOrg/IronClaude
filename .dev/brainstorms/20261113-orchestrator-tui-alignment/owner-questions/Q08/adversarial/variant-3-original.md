# Proposal C: write the one-paragraph direction-selection record now

## Answer

The owner writes one dated paragraph, in their own words, naming the staged direction that was chosen, their reading of "production integration" and the command name (`superclaude observe`); #409's acceptance criterion 1 stays as written and is then met by citing that record.

## What happens next if the owner picks it

- The owner writes the paragraph in a file at a location of the owner's choosing (UNVERIFIED where; `merged-requirements.md:250`) and the ledger records its path and date (OB-02).
- Agents cite it and never edit it (`release-gates.md:22`).
- OB-08 (the #409 correction pass) posts BC-18 changed to point at the record (the status line becomes "met by the owner's record of <date>, path"), instead of "not met as recorded".
- OB-09 (release 3) is no longer blocked by OB-02.

## What it unlocks

- Closes the one open item the debate found on the observer's direction (ADJ A-003, 96 percent: "only the selection record is open").
- Keeps the acceptance criterion unchanged, so no one can say the bar was moved.
- The paragraph can cite the owner's existing decisions (2026-11-08 "Stage it", 2026-11-11), so it is short to write.
- Fixes the meaning of "production integration" in the owner's words, which later releases and #409 readers can rely on.

## What it costs or risks

- Owner writing time (one paragraph), and the owner must choose where the file lives.
- The gate rule (`release-gates.md:22`) lists more fields than the three this answer names (for example "fallback date", "post-link choice or explicit deferral", "stack confirmation"); a three-item paragraph may not satisfy the gate as written, and the owner must either include those fields or say the gate is met without them.
- It records retroactively a selection already acted on (releases 1 and 2 shipped first), so it documents rather than precedes the decision.
- If it cites the 2026-11-08 record, that file must first be saved from the sibling worktree (Q7).

## What stays unresolved

Where the record lives; whether release 3's later choices (post-link, fallback date) need a second dated record.
