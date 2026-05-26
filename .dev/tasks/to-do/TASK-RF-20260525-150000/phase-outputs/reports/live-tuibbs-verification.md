# Live TUIBBS-scp v1-MVP Coverage Verification

Date: 2026-05-25 16:22

## Sources

- Spec: `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/epics.md`
- Roadmap: `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md`

Note: BEFORE the Fix A workaround is reverted — this measures whether the merged Fix B alone is sufficient to green the case.

## Command

```bash
uv run python -c "
from superclaude.cli.roadmap.integration_contracts import extract_integration_contracts, check_roadmap_coverage
spec = open('/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/epics.md').read()
roadmap = open('/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md').read()
contracts = extract_integration_contracts(spec)
result = check_roadmap_coverage(contracts, roadmap)
print(f'total={result.total_count} uncovered={result.uncovered_count}')
for c in result.coverage:
    if not c.covered:
        print(f'  UNCOVERED: {c.contract.id} mech={c.contract.mechanism} loc={c.contract.spec_location}')
"
```

## Result

```
total=5 uncovered=0
```

No UNCOVERED contracts emitted.

## Verdict

**END-TO-END VERDICT: PASS — uncovered_count == 0**

The merged Fix B refactor (mechanism-signature + 3-layer coverage with the cycle-1 and cycle-2 fixes for `PROGRAMMATIC_RUNNERS` extraction and bare-`priority` removal) successfully greens the anti-instinct gate against the live TUIBBS-scp v1-MVP spec + roadmap. The Fix A workaround in roadmap.md can now be reverted in a separate follow-up task.
