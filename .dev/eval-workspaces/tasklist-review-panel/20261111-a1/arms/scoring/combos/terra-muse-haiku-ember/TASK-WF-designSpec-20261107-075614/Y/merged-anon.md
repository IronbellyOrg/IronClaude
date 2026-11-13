review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R2, R3 |
| L2 | open | no | overlap | MAJOR | - | R2, R3 |
| L3 | open | no | overlap | MAJOR | - | R2, R3 |
| L4 | open | no | overlap | MAJOR | - | R2, R3 |
| L5 | open | no | overlap | MINOR | - | R2, R3 |
| L6 | open | yes | single | MAJOR | - | R3 |
| L7 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L6

#### L6.R3 (F1)

- claim: The acceptance text limits the mode OFF rule to ordinal below 3, so mode OFF at ordinal 3 with no record reports released where section 4.1 says off.
- anchor: "mode `OFF` and ordinal below 3 with no record (`off`), and no record at ordinal 3 (`released`)"
- anchor2: "implementing the first-match mapping of section 4.1"

#### L6.R3 (F6)

- claim: In the checkout read, merge_guard.py, set-draft-state.sh, test_set_draft_state.py and the _RESOLUTION_SCRIPTS entry already exist, so the Create steps and the clean base record do not match that tree.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py` following"

## Other findings

- L1 (MAJOR, open, overlap): Resume row 4 never states how applied edits, target sha and cycle id reach the release re-entry, so a crash after a normal push could hold instead of release or release with cause no edits.
- L2 (MAJOR, open, overlap): The bullet must also state the at L3 with off line, so whether the draft gate wording test forbids L3 or draft text needs a guess.
- L3 (MAJOR, open, overlap): The artifacts files use dot slash with no package or root anchor, and root artifacts is not ignored, so the cleanliness check depends on where dot slash is taken to mean.
- L4 (MAJOR, open, overlap): The text never states what happens when a held draft is reused by a later cycle, so the guard could stay bound to the earlier cycle id.
- L5 (MINOR, open, overlap): The not open case states the JSON error but not the exit code, so a script test must guess 0 or 1.
- L7 (MAJOR, open, single): The text never says where the guard mode comes from on --resume, so a resumed off run has no stated mode source.

## Reviser brief

Blocking finding ids: L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
