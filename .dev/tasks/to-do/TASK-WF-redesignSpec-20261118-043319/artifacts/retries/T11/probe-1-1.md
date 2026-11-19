4842ffc8f60ff1f448fd9487c36e08586f404d21
# Family probe for review r1-1 of T11 (before the first fix)

## family counts-marker-overflow (F1.1) and counts-token-clip (F1.2)
- Defect form: a counts token is cut inside, either by `clip` of a lone token wider than the line, or by `Line.clipped` when the truncation marker does not fit after the last whole token.
- Command: grep -n -F -e "clip(text" -e ".clipped(width" src/superclaude/cli/observe/render.py
- Before-output (lines in the counts function are 261 and 268; the others are outside it):
  - 202: shown = clip(text, width, policy)  (the padded column cell, not a counts token)
  - 261: current = _token_line(clip(text, width, policy), token)
  - 268: current = current.clipped(width, policy)
  - 409: shown = clip(text, width, policy)  (a ledger row cell)
  - 545: shown = clip(text, room, policy)  (a question line)
  - 561: return line.clipped(width, policy)  (a question line)
- Coupled sites: render.py 258-269 (the whole non-protected branch of counts_line_objects); the rule is stated by RR line 20.

## family footer-rule-conditional (F1.3)
- Defect form: the footer rule is counted in the height budget but can be dropped afterwards.
- Command: grep -n -F -e "rule" src/superclaude/cli/observe/render.py
- Before-output: 672 footer_height counts the rule; 777-778 the rule is appended and a later statement could drop it.
- Coupled sites: footer_height (672) and the final return (777-780).

## family signature-drift (F1.4)
- Defect form: the helper does not have the call shape the plan names.
- Command: grep -n -F -e "_heading_rows" src/superclaude/cli/observe/render.py
- Before-output: 437 def _heading_rows(view: View) -> int; 685 and 745 are its two call sites.
- Coupled sites: the two call sites.
after:
- counts-marker-overflow, counts-token-clip (grep -n -F -e "clip(text" -e ".clipped(width"):
    202:    shown = clip(text, width, policy)
    421:            shown = clip(text, width, policy)
    558:    shown = clip(text, room, policy)
    574:    return line.clipped(width, policy)
- footer-rule-conditional (grep -n -F -e "rule"):
    442:    rule = SEPARATOR.join(glyph("hrule", policy) * width for _, width in columns)
    445:        seg(clip(rule, policy.width, policy), "border_secondary"),
    450:    """The column heading and its rule take 2 rows whenever ledger rows are visible, at every
    685:    footer_height = 1 + (  # one rule line above the footer
    759:    # The column heading and its rule at every width, unless that would leave no room for even
    790:    rule = seg(glyph("hrule", policy) * width, "border_secondary")
    791:    return top + body + [rule] + footer_lines
- signature-drift (grep -n -F -e "_heading_rows"):
    449:def _heading_rows(view: View, policy: TerminalPolicy) -> int:
    698:            _heading_rows(view, policy)
    758:    heading = _heading_rows(view, policy)
