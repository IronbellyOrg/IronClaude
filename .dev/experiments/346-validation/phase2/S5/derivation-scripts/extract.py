"""Extract verbatim tool_use inputs / tool_results from the I5 executor session log.
usage: extract.py <log> <mode> <line> <outfile>
  mode use_field:<tool>:<field>   write input[field] of the tool_use on that line
  mode use_cmd                    write Bash command of the tool_use on that line
  mode result_of_use              write the tool_result text for the tool_use that is on <line>
  mode text                       write the assistant/user text on that line
"""
import json
import sys

log, mode, line, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]


def content_blocks(rec):
    c = rec.get("message", {}).get("content")
    if isinstance(c, str):
        return [{"type": "text", "text": c}]
    return c or []


def result_text(block):
    c = block.get("content")
    if isinstance(c, str):
        return c
    return "".join(b.get("text", "") for b in c if isinstance(b, dict))


with open(log, encoding="utf-8") as fh:
    lines = fh.readlines()
rec = json.loads(lines[line - 1])

if mode.startswith("use_field:"):
    _, tool, field = mode.split(":")
    uses = [b for b in content_blocks(rec) if b.get("type") == "tool_use" and b["name"] == tool]
    text = uses[0]["input"][field]
elif mode == "use_cmd":
    uses = [b for b in content_blocks(rec) if b.get("type") == "tool_use"]
    text = uses[0]["input"]["command"]
elif mode == "result_of_use":
    uses = [b for b in content_blocks(rec) if b.get("type") == "tool_use"]
    uid = uses[0]["id"]
    text = None
    for ln in lines[line:line + 40]:
        r = json.loads(ln)
        for b in content_blocks(r):
            if b.get("type") == "tool_result" and b.get("tool_use_id") == uid:
                text = result_text(b)
                break
        if text is not None:
            break
    if text is None:
        sys.exit("no result found within 40 lines")
elif mode == "text":
    text = "".join(b.get("text", "") for b in content_blocks(rec) if b.get("type") == "text")
else:
    sys.exit("bad mode")

with open(out, "w", encoding="utf-8") as fh:
    fh.write(text)
print(f"{out}: {len(text.encode('utf-8'))} bytes, {text.count(chr(10))} newlines")
