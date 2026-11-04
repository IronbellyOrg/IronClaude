# Behaviour definitions

| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | `claude plugin marketplace add <dir>` (Claude Code 2.1.318) | records the marketplace in known_marketplaces.json as `{"source": {"source": "directory", "path": "<dir as passed>"}, "installLocation", "lastUpdated"}` | direct observation this run (throwaway HOME, 2026-11-04T16:17:53Z): `{"source":{"source":"directory","path":"/tmp/t14c-known.U3MAuB/.claude/ironclaude-marketplace"},"installLocation":"/tmp/t14c-known.U3MAuB/.claude/ironclaude-marketplace","lastUpdated":"2026-11-04T16:17:53.851Z"}` | n/a (observed directly, no fetch) | observed:this-run |
| 2 | `claude plugin marketplace add <dir>` when the name is already registered from another source | rebinds the name to the new source (exit 0) and keeps installed plugins, which then update from the new source | direct observation this run (tier1-observation.md, Discriminator probe) | n/a (observed directly) | observed:this-run |
