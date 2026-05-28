# Diff Analysis — Cross-Variant Comparison

## Comparison axes

| Axis | V1 (analyzer/opus) | V2 (architect/sonnet) | V3 (scribe/haiku) | Merge resolution |
|------|--------------------|------------------------|--------------------|------------------|
| Decision framing | Workload-scoped | Workload-scoped + architecture-fit | Decision rule + exit criteria | Workload-scoped + decision rule + exit criteria |
| Performance treatment | Real but workload-dependent | Real but secondary to compatibility | Risk row | Real but workload-dependent; not primary driver |
| Ecosystem axis | One bucket | Native-module / APM / hosting elevated | One bucket | Native-module / APM / hosting elevated |
| Operations axis | LTS / security WG / vendor support | Hosting platform support inline | LTS + risk register | All three combined |
| Tooling / DX | Real selective-adoption driver | Secondary | Listed | Real driver under FR / NFR; not sole adoption case |
| Risk register | Implicit | Partial | Formal | Formal `## Risks` (table) |
| Pilot framing | Recommended | Recommended | Mandatory with exit criteria | Mandatory with exit criteria |
| Recommendation | Adopt / pilot / defer / reject | Pilot per workload class | Pilot + decision rule | Pilot + decision rule per workload class |

## Dropped content (with rationale)

- **V1's "single-recommendation summary"** dropped — the merged output uses a decision-rule framing instead. Rationale in `merge-log.md`.
- **V2's separate "hosting platform appendix"** absorbed inline into the operations / hosting requirements. Rationale in `merge-log.md`.
- **V3's "scoring matrix" prototype** absorbed as the "decision rule" pattern in FR-5. Specific scoring weights not adopted (workload-specific).

## Added content (relative to V1 base)

- Explicit native-module / APM / FaaS hosting requirement under NFR (from V2).
- Formal `## Risks` table with likelihood + mitigation (from V3).
- Pilot exit criteria as a measurable acceptance criterion (from V3).
- Hosting platform compatibility as part of operations requirement (from V2).
