397b62f0e95b6dad3c9c888d7928c60899f86a87
## family h2-line-index (from r2-1)
defect form: the normaliser indexes lines from str.split('\n') with line numbers that _blocks_after computes with str.splitlines(), so any other line separator before the block shifts the rewrite onto the wrong line
command: grep -n -e 'split(' -e 'splitlines' -e 'lines\[' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py
before:
23:    lines = text.split("\n")
40:            lines[lineno - 1] = json.dumps(obj, ensure_ascii=False)
coupled sites: h2_normalize.py normalize() split and join (one function); dropped_lines() uses _blocks_after numbering only (consistent); tests/test_h2.py needs a U+2028 case
after:
23:    # _blocks_after numbers lines with str.splitlines(), so index with the same splitter (it also breaks on \r, \x0c,
25:    lines = text.splitlines(keepends=True)
42:            old = lines[lineno - 1]
43:            ending = old[len(old.splitlines()[0]):] if old.splitlines() else old
44:            # ASCII escapes: a rewritten line can never carry a raw line separator that splitlines would break on
45:            lines[lineno - 1] = json.dumps(obj) + ending
