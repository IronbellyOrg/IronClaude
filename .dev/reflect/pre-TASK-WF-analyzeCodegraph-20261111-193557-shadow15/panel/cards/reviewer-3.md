persona: refactorer
model_class: opus
model: claude-opus-5-5
model_observed: claude-gw-tier1b[1m]

## Findings block

```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Guide section 7 says it is the only section that names the forbidden verbs, but analyze.md line 68 restates init, index, sync, explore and context. A guide change to that list must now be mirrored here or the two drift.","refs":["INF-005","INF-012"],"citations":[{"role":"plan","path":"src/superclaude/commands/analyze.md","line_start":68,"line_end":68,"quote":"never run `codegraph init`, `index`, `sync`, `explore` or `context`"},{"role":"spec","path":"src/superclaude/core/CODEGRAPH.md","line_start":87,"line_end":89,"quote":"The only section that names these:"}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"analyze.md line 30 states the 60 s build wait unconditionally. Guide section 2 step 3 applies it only when the primitive's Bash allowlist permits pgrep. The command is a second statement of a guide rule and drops that condition.","refs":["INF-005"],"citations":[{"role":"plan","path":"src/superclaude/commands/analyze.md","line_start":30,"line_end":30,"quote":"on the MCP path it first waits up to 60 s for a running `init` or `index`"},{"role":"spec","path":"src/superclaude/core/CODEGRAPH.md","line_start":13,"line_end":13,"quote":"when the primitive's Bash allowlist permits `pgrep`"}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"The 10-line section meets the 25-line budget only because the Leads bullet packs about six rules into one long line. The line-count AC is met, but the rules are hard to maintain and partly duplicate guide sections 3 and 5.","refs":["INF-012"],"citations":[{"role":"plan","path":"src/superclaude/commands/analyze.md","line_start":67,"line_end":67,"quote":"a caller list shorter than its total is `graph:truncated`"},{"role":"spec","path":"src/superclaude/core/CODEGRAPH.md","line_start":58,"line_end":64}]}
```

calibration:
  per_finding:
    F1: 0.8
    F2: 0.75
    F3: 0.6
