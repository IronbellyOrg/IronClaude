a8ecbfea4be60c23f0f77b58fbba35829b0d9747
family transcript-integrity
form: transcript matching accepts any tool's result and the joined text of all results
command: grep -n -e 'tool_result' -e 'Agent tool result' -e 'join(texts)' -- src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py tests/skills/test_stoprule_script.py
before:
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1750:def tool_result_texts(node, out):
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1751:    """Collect the text of every tool_result block anywhere in a transcript record."""
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1753:        if node.get("type") == "tool_result":
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1760:            tool_result_texts(value, out)
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1763:            tool_result_texts(value, out)
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1775:                tool_result_texts(json.loads(line), texts)
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1787:        if r["text"].strip() not in "\n".join(texts)
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1791:            f"grader-integrity: mismatch ({', '.join(missing)} not found verbatim in any Agent tool result)"
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1991:        "recorder: are the grade-raw replies verbatim Agent tool results?",
tests/skills/test_stoprule_script.py:1607:                        "type": "tool_result",
coupled sites: tool_result_texts, cmd_verify_transcript, verify-transcript help text, transcript_with test helper
after:
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1754:    """Collect Agent tool_use ids and every tool_result (tool_use_id, text) of a record."""
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1758:        if node.get("type") == "tool_result":
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1796:            "grader-integrity: unverified (the transcript holds no Agent tool result)"
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1799:    # each reply must sit whole inside one Agent tool result, never across results
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1807:            f"grader-integrity: mismatch ({', '.join(missing)} not found verbatim in any Agent tool result)"
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:2007:        "recorder: are the grade-raw replies verbatim Agent tool results?",
tests/skills/test_stoprule_script.py:1594:    """A session transcript: one tool_use per text (named tool) and its tool_result."""
tests/skills/test_stoprule_script.py:1614:                        "type": "tool_result",
tests/skills/test_stoprule_script.py:1655:        out.startswith("grader-integrity: unverified") and "no Agent tool result" in out
