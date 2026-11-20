<!-- stub: copy the block below, replace every placeholder (the text in angle brackets) with its value, and print the one filled block last; every key stays, none is added -->

```yaml
closeout:
  pr: <number or null>
  status: complete | partial | stopped
  verdict: MERGED | OPEN | CLOSED | NONE | UNKNOWN
  merged_by: <name or null>
  merge_commit: <first 7 characters or null>
  match: same | differs | unchecked | null
  pr_links_issue: closing | refs | none | null
  issue:
    number: <number or null>
    status: <settled | already_final | none_found | escalated | null>
    detail: <how or why token or null>
    note: <posted | already_there | none | null>
    handback: <remaining | none | null>
    remaining_file: <path of the verdict file or null>
    remaining: [<one line per unmet criterion>]
    handback_text: <the hand-back sentence of refs/settle.md or null>
  entry:
    key: <key or null>
    status: <settled | already_final | none_found | escalated | null>
    detail: <how or why token or null>
  task:
    id: <id or null>
    status: <settled | already_final | none_found | escalated | null>
    detail: <how or why token or null>
    dispatch: <state read or null>
  escalations: ["<item>: <one sentence: why not, and the one next step>"]
  stop: <STOP code or null>
```
