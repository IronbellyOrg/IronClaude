"""F-TRANSCRIPT-RL (TESTING section 2): run transcripts in the shape of a real `claude -p --output-format json` run.

A transcript is a list of events: one `system` init, then `assistant` events (`message.content` blocks `text` and
`tool_use`), each followed by the `user` event that holds its `tool_result` blocks, and a final `result` event with
`result`, `usage` and `modelUsage`. Everything is invented. `build(name, final="")` returns the events of one case;
`write_all(folder)` writes each as `<name>.json`.

Cases (REQ-16 corpora, REQ-28):
  search_done                a Bash grep whose result holds SEARCH_HIT
  search_claimed_not_done    the assistant text says it searched; there is no tool call of any kind
  no_tool_call               the assistant answers from the prompt alone
  none_found_with_search     a Bash grep that prints nothing (the result is "")
  none_found_without_search  the assistant says nothing was found and ran nothing
  luna_array_results         luna's shape: tool names beyond Bash/Read, `content` an array of text blocks
  assistant_text_only        ASSISTANT_ONLY appears in assistant text and in no tool result
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EMBER = "muse-ember-1.0"
LUNA = "gpt-6-luna"
# text that no plan or source fixture holds, so a quote of it can only come from a transcript
SEARCH_HIT = "tests/test_retention.py:7:def test_purge_keeps_held():"
ASSISTANT_ONLY = "src/exporter/retention.py:21:    if report.legal_hold:"

CASES = (
    "search_done",
    "search_claimed_not_done",
    "no_tool_call",
    "none_found_with_search",
    "none_found_without_search",
    "luna_array_results",
    "assistant_text_only",
)


def run(model, steps, final=""):
    """Events of one run. steps: ("text", s), ("tool", name, input, result) where result is a string or a block array."""
    events = [
        {"type": "system", "subtype": "init", "model": model, "tools": ["Bash", "Read"]}
    ]
    n = 0
    for step in steps:
        if step[0] == "text":
            events.append(_assistant(model, [{"type": "text", "text": step[1]}]))
            continue
        _, name, tool_input, result = step
        n += 1
        tid = f"toolu_{n:02d}"
        events.append(
            _assistant(
                model,
                [{"type": "tool_use", "id": tid, "name": name, "input": tool_input}],
            )
        )
        block = {"type": "tool_result", "tool_use_id": tid, "content": result}
        events.append({"type": "user", "message": {"role": "user", "content": [block]}})
    usage = {"input_tokens": 120, "output_tokens": 80}
    events.append(
        {
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "result": final,
            "usage": usage,
            "modelUsage": {model: dict(usage, costUSD=0.0)},
        }
    )
    return events


def _assistant(model, content):
    return {
        "type": "assistant",
        "message": {"model": model, "role": "assistant", "content": content},
    }


def bash(command, result):
    return ("tool", "Bash", {"command": command, "description": "search"}, result)


def build(name, final=""):
    steps = {
        "search_done": (
            EMBER,
            [
                ("text", "I will search the tests for the purge test."),
                bash("grep -rn 'purge_keeps_held' tests/", SEARCH_HIT),
                ("text", "The search found one test."),
            ],
        ),
        "search_claimed_not_done": (
            EMBER,
            [("text", "I ran grep -rn over the tests and found the purge test.")],
        ),
        "no_tool_call": (EMBER, [("text", "Reading the plan only; no search needed.")]),
        "none_found_with_search": (
            EMBER,
            [
                bash("git grep -n 'retention_hold' -- tests docs", ""),
                ("text", "Nothing found."),
            ],
        ),
        "none_found_without_search": (
            EMBER,
            [("text", "NONE FOUND: nothing refers to it.")],
        ),
        "luna_array_results": (
            LUNA,
            [
                (
                    "tool",
                    "mcp__codegraph__codegraph_node",
                    {"file": "src/exporter/retention.py", "projectPath": "/tmp/x"},
                    [{"type": "text", "text": SEARCH_HIT}],
                ),
                bash("ls tests", "test_retention.py"),
            ],
        ),
        "assistant_text_only": (
            EMBER,
            [
                ("text", f"The retention module has the line {ASSISTANT_ONLY}"),
                bash("ls src/exporter", "report.py"),
            ],
        ),
    }[name]
    return run(steps[0], steps[1], final)


def write_all(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    for name in CASES:
        (folder / f"{name}.json").write_text(json.dumps(build(name)), encoding="utf-8")
    return folder
