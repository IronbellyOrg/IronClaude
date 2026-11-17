# Shadow engine fallback (rule D4)

Requested `--t2-engine shadow`; effective engine `legacy`. Probed on 2026-11-12:

- `superclaude review panel resolve --template @reflect-pre ...` exits with `no packaged panel template 'reflect-pre' (known: default, live7)`.
- `superclaude review panel resolve` offers only --template/--tiers/--env/--run-id/--kind/--seed/--sequence (no --hard-exclude-class, --strict-distinct).
- `superclaude review` offers only ledger, merge, panel, telemetry: no `manifest`, `cluster` or `verify-citations`.

No `panel/resolution.json` or manifest was written, since writing one without the tool would be invented evidence. Briefs carry no findings-v2 instruction line. The legacy rotation and Wave 4 ran unchanged.
