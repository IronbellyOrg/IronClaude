# Scope Estimation: v5.0 Plugin System

## Per-Requirement Estimates

| Req | Description | Est. Lines | Domain | Complexity | Priority |
|-----|-------------|-----------|--------|------------|----------|
| R1 | Package Format | 200-300 | Backend | Medium | P0 |
| R2 | Registry Server | 600-800 | Backend/DevOps | High | P0 |
| R3 | CLI Plugin Manager | 500-700 | Backend | High | P0 |
| R4 | Sandboxed Runtime | 600-800 | Backend/Security | Very High | P0 |
| R5 | Lifecycle Hooks | 300-400 | Backend | Medium | P1 |
| R6 | Marketplace Web UI | 500-700 | Frontend | High | P1 |
| R7 | Migration | 200-300 | Backend | Medium | P1 |
| R8 | PDK | 300-400 | Backend | Medium | P2 |
| R9 | Analytics | 200-300 | Backend/Frontend | Medium | P2 |
| R10 | Enterprise Policies | 200-300 | Backend/Security | Medium | P2 |

**Total: 3,600-5,000 lines** (aligns with the 3000-4000 estimate, trending higher)

## Risk Flags

1. **Size**: At 3000-4000 lines, this is 2-3x a typical release for this project. Single-release delivery increases integration risk.
2. **Domain Spread**: 40% backend, 30% frontend, 20% devops, 10% security — no single team/persona can own everything.
3. **Infrastructure Dependencies**: R2 requires PostgreSQL + S3 + a deployed API server. R6 requires React/Next.js. These are entirely new technology stacks for a project that is currently pure Python + Markdown.
4. **Security Surface**: R4 (sandbox) requires security audit and escape testing. Rushing this into a single release is the highest-risk item.
5. **Rollout Plan Already Phases It**: The spec's own rollout plan (Section 6) already envisions Alpha/Beta/GA phases that align almost perfectly with a split.
