# Reviewer Card 1 — Analyzer (root-cause-analyst)

- Model class: sonnet-alias (gpt-5.5) · Persona: analyzer · Stance: ADVERSARIAL
- Self-reported confidence: 0.93

## Verdict: CLEAN

### Missed-site hunt (repo-wide greps, .claude excluded)
- `1800`, `30 min/~30 min`, monitor `default 0/defaults to 0/default=0`, `omit/without --monitor/open-only` — **none** survive as pr_submit defaults.
- All repo `1800`/`30-min` hits belong to unrelated subsystems (freshness hooks, eval suites, roadmap executor, PRD/tech-ref line-budget tables).
- 5 `tests/pr_submit/*` `1800` refs (test_timeout.py:35,40; test_edge_cases.py:109,220; test_crash_recovery.py:45) pass `timeout=1800` as an **explicit** arg (arithmetic tests), not the default. Not a missed site.

### Correctness (empirically verified)
- fsm.py:65-67 `armed` = `self.monitor >= 1`; with DEFAULT_MONITOR=1 (fsm.py:30) → runtime-confirmed `parse_args([]).armed==True`, `parse_args(["--monitor","0"]).armed==False`, `parse_args([]).timeout==600`.
- fsm.py:74 parser `default=DEFAULT_MONITOR`, choices [0,1,2,3] — explicit 0 still not-armed.
- fsm.py:721 `RunConfig.monitor_ordinal=DEFAULT_MONITOR` — necessary companion; without it bare `RunConfig()` runs L0, contradicting goal. No test relied on old 0 RunConfig default.
- fsm.py:608 `ctx.get("monitor_ordinal", 0)` — **safe defensive floor in the pure `transition()` function**; topology tests (test_auggie_fallback.py:266-290) call `transition()` with no context to assert edge structure under the most-restrictive ceiling. Correctly left at 0.
- Suite: 191 passed; verify-sync clean.

### Deviation table
| Hunk | Class | Rationale |
|------|-------|-----------|
| `DEFAULT_MONITOR=1` constant | necessary | de-magics new default; serves item 1 |
| `DEFAULT_TIMEOUT 1800→600` | authorized | goal "timeout 1800→600" |
| `SkillArgs.monitor 0→DEFAULT_MONITOR` | authorized | core of item 1 |
| parser `default=0→DEFAULT_MONITOR` | authorized | item 1 "parser wiring" |
| `RunConfig.monitor_ordinal 0→DEFAULT_MONITOR` | necessary | default-behavior coherence across pure-core seam |
| test_skill_parse.py edits | authorized | item 2 (preserve explicit `--monitor 0`) |
| pr-submit.md / SKILL.md / augment-poll.md | authorized | items 3/4/5 |

- regression_present: **false**
- Prior "1 drift" disposition: **rejected** — contested hunk is necessary/in-scope, not drift.
