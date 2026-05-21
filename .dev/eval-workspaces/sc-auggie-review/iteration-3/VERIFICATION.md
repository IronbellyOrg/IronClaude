# Iteration 3 — `--max-turns` Preamble Pitfall Verification

## Change

Added one new bullet to the "Common pitfalls (read before invoking)" block in
`src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` Wave 2:

> **`--max-turns` preamble**: when `--max-turns N` is passed, Auggie prints
> `Applying --max-turns override: N over agentMaxIterations=500` as the
> **first stdout line** before the JSON envelope. This breaks `jq` if not
> stripped. Pipe through `tail -n +2` (or `grep -v '^Applying --max-turns'`)
> before extracting `.result` and stripping the inner ```json fence.

## Empirical verification (this iteration)

Ran the exact documented pipeline against a real Auggie invocation that
triggered the preamble:

```bash
auggie --print --output-format json --ask \
  --workspace-root $(git rev-parse --show-toplevel) \
  --max-turns 16 \
  --instruction-file /tmp/eval-pr62-iter3/auggie-prompt.txt \
  > /tmp/eval-pr62-iter3/auggie-raw-1.json
```

Output shape confirmed:

```
Line 1: Applying --max-turns override: 16 over agentMaxIterations=500
Line 2: {"type":"result","result":"```json\n{...}\n```",...}
```

Pipeline test (verbatim from skill):

```bash
tail -n +2 auggie-raw-1.json \
  | jq -r '.result' \
  | sed -n '/^```json$/,/^```$/p' \
  | sed '1d;$d' \
  | jq .
```

Result: **clean parse, exit 0, 7 findings + 3 cross-cutting observations
extracted**. No retry, no improvisation, no jq error.

## Conclusion

The iteration-3 one-line documentation addition is sufficient — the
preamble pitfall is now foregrounded and the verified strip recipe works
end-to-end. No further iteration needed before description optimization.
