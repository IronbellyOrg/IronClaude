# Blind calibration brief — card 3 (comboA-r3)
You are re-grading a reviewer card WITHOUT its formation context. The card is your only input.
Read: .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboA-r3/panel/cards/reviewer-3.md
Grade the CARD as a whole on the 5-dimension rubric (0-1 each): citation grounding, coverage completeness, deviation-classification clarity (for a pre-execution card: finding-severity appropriateness), risk surface coverage, recommendation actionability.
Then output, as your ENTIRE reply, a fenced yaml block:
calibration:
  per_finding:
    F1: 0.85
(one confidence from 0 to 1 for each finding id of the card's findings block, written exactly as in the block; leave out a finding you cannot score). Your card score is unchanged.
