# Spec panel (critique) — workflow v3 SPEC.md

Experts (compressed): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Crispin.

## Applied to SPEC.md

| Sev | Expert | Issue | Fix in SPEC |
|-----|--------|-------|-------------|
| MAJOR | Wiegers | STOP codes only E-LEGACY | Full STOP table |
| MAJOR | Adzic | Empty source after parse | `E-NO-PHASES` |
| MAJOR | Nygard | Re-run same slug | overwrite in place |
| MINOR | Fowler | `Task` in allowlist after YAGNI cut | dropped Task |
| MINOR | Crispin | command size / SKILL cap | 80–150 / ~500 |
| MINOR | Whittaker | Zero phases / missing headings | `E-GATE` |

## Guard table

| Guard | Zero/empty | Typical | Status |
|-------|------------|---------|--------|
| source | E-NO-SOURCE / E-EMPTY-SOURCE | Wave 0 continues | OK after patch |
| phases | E-NO-PHASES | 2–12 phases | OK after patch |
| output path | E-OUTPUT-PATH | `.dev/workflow/<slug>/` | OK |
| plan headings | E-GATE | 03_project_plan headings | OK after patch |

## Consensus

Ship SPEC.md as the design SoT for implement. Do not grow waves or files.

## Not applied (YAGNI)

Newman/Hohpe/Hightower: no services/cloud. Gregory: no spec workshop. Sequence-attack on resume: out of scope.
