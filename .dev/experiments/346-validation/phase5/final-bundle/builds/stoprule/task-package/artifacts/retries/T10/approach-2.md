Implementer claims (attempt 2, the Q5 fix pass), not verified facts:
- Built tests/skills/test_spec_panel_stoprule.py: static checks of the variant, the skill, the agent and the rubric hash, plus a drift check against the pinned 472-line Arm B base fixture.
- A1's drift check exempted lines by prefix anywhere; A2 replaced it with a mechanical undo of the planned edits (drop the inserted lines and bullet 8, map /sc:spec-panel-stoprule back to /sc:spec-panel, map the name line back) and a line-for-line comparison, blank lines included, with in-place exemptions only for description (lines 1-8), FR-8, FR-9 and Review Loop bullets 2-7.
- Added parametrized negative cases (heading, Examples argument, Usage flag, Integration Patterns edit, smuggled description line, extra blank line).
- Believed T10.AC2 met by those cases (tests/skills/test_spec_panel_stoprule.py:175-203) and AC1, AC3, AC4 met by the logs and the one-line allow-list change.
- What it missed: the undo is position-free, so the same inserted lines or a renamed command placed anywhere else in the file are also undone.
