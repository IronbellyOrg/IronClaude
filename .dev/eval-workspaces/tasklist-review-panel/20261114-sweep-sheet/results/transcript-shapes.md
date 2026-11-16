# Transcript shapes (step 0.4, run by Task 24)

Method: `jq` over one finished `*.attempt1.json` per reviewer model, under
`.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/`.
The model of each file was taken from its own `assistant` events (`message.model`) and from `result.modelUsage` keys.
Only `*.attempt1.json` files were opened. No ground-truth, score, judge or verdict file was opened.
All four models had a finished run on disk.

| model | file (under `reviews/combos/`) | events |
|---|---|---|
| `muse-ember-1.0` (ember) | `e2-ember-luna2-rep/t2b-1.attempt1.json` | 59: system/init 1, system/thinking_tokens 4, assistant 36, user 17, result/success 1 |
| `gpt-6-luna` (luna) | `e2-ember-luna2-rep/t4-1.attempt1.json` | 31: system/init 1, assistant 18, user 11, result/success 1 |
| `claude-haiku-5-5` (haiku) | `c1-haiku-luna/t4-1.attempt1.json` | 152: system/init 1, system/thinking_tokens 129, assistant 14, user 7, result/success 1 |
| `claude-sonnet-5-5` (sonnet) | `b4-sonnet-luna2/t1b-1.attempt1.json` | 174: system/init 1, system/thinking_tokens 129, assistant 28, user 15, result/success 1 |

## File shape (same for all four)

The file is one JSON array of event objects. Event `type` values seen: `system` (subtype `init`, and `thinking_tokens`
for ember, haiku and sonnet), `assistant`, `user`, `result` (subtype `success`).

- `assistant`: keys `message, parent_tool_use_id, session_id, thinking_duration_ms, timestamp, type, uuid, wire_tool_inputs`.
  `message.content` is an array of blocks of type `thinking`, `text` and `tool_use`. The model name is `message.model`.
- `user`: keys `message, parent_tool_use_id, session_id, timestamp, tool_result_meta, tool_use_result, type, uuid`.
  `message.content` is an array. Luna also has two `user` events with `isSynthetic` and a `text` block (no `tool_result`,
  `tool_use_result` is null).
- `result`: `result` is a string (the final message), plus `usage` (keys include `input_tokens`, `output_tokens`,
  `cache_read_input_tokens`) and `modelUsage` (an object keyed by model name).

## The `tool_result` shape (same for all four)

A `tool_result` is a block inside the array `user.message.content`:

```
{"type": "tool_result", "tool_use_id": "<id>", "content": "<string>", "is_error": false | absent}
```

- `content` is always a JSON **string** in all four runs (no model had an array-of-blocks `content`; the count of array
  `content` values was 0 for each).
- `is_error` is present as `false` on some blocks and absent on others (ember 9 present / 8 absent; luna 0 / 9; haiku 5 / 2;
  sonnet 13 / 2). No `true` value was seen.
- The block types inside `user.message.content` are `tool_result` only (ember, haiku, sonnet) and `tool_result` plus `text`
  (luna, the two synthetic events).
- The sibling field `tool_use_result` on the event is an object whose keys depend on the tool: `Read` gives `file, type`;
  `Bash` gives `interrupted, isImage, noOutputExpected, stderr, stdout`; `Skill` gives `commandName, success`. Sonnet's Bash
  results can also carry `persistedOutputPath, persistedOutputSize`: a long result is stored in a file and the block
  `content` holds only a preview. A flattened-substring test over `content` therefore sees only the preview of such a result.
- Tools used: ember `Bash` 9, `Read` 8; luna `Read` 8, `Skill` 1; haiku `Bash` 5, `Read` 2; sonnet `Bash` 13, `Read` 2.

## What the `transcript` corpus (DESIGN DD-2) reads

For each `user` event, each `message.content` block with `type == "tool_result"` and a string `content`. A reader must also accept
an array `content` of `{"type": "text", "text": ...}` blocks (not seen in these four files, but part of the stream format), and must
skip `user` events whose `message.content` is a plain string.
