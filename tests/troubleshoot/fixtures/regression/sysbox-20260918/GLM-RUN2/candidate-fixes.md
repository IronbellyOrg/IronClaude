# Candidate Fixes — Wave 3 distillation

| # | Fix | Supporting agents (calibrated conf) | Verdict |
|---|-----|--------------------------------------|---------|
| 1 | Re-apply 6863ecc verbatim on 45f75c2: Dockerfile.coder four same-dest/same-mode COPY group merges (82→68 layers) + `Check Sysbox image-layer headroom` step (budget 1..70) in coder-ci-aidev02-contract.yml after `Build AIDev02 image` (:328-341), before Phase-0 probe | devops-architect (0.30), root-cause-analyst (0.80), system-architect (0.30) | **consensus** |
| 2 | Image flattening (export/import or --squash in main.tf) | none (devops + sys-arch both REJECT: export/import drops USER/ENV config; --squash needs legacy builder + daemon experimental = host mutation; breaks content-addressed tag truth and D-02 bump isolation) | outlier-rejected |
| 3 | Wait for sysbox upstream fix | none (fails owner repair-now; no repo-side effect) | outlier-rejected |
| 4 | Deeper COPY consolidation (~44→~10) | none (sys-arch: ceiling structurally unreachable due to USER/RUN interleaving; triples stale-comment surface; gate already catches growth) | outlier-rejected |

## Calibration summary

- All three cards CONVERGE on fix #1 — substantively identical proposals (cherry-pick 6863ecc). Under Wave 4 preconditions this is **consensus with ≥2 distinct proposals debated internally**, i.e. the debate precondition (≥2 *competing* fixes) is NOT met.
- Calibrated confidences: 0.30 / 0.80 / 0.30. The low scores are driven by the rubric's runtime-check gate: no agent captured runtime evidence of the FIXED state (the 68-layer image was never built+started under sysbox by this session; bounded-repro authorization was consumed pre-session). The root-cause card scores highest (0.80) because the *symptom-side* runtime evidence (76/78 probe, captured error string) is present and the mechanism is line-verified upstream.
- Residual risk carried by all cards: layer count is a proxy for mount-data bytes; discriminating check (failing-container mountinfo `upperdir=<id>/diff`, or built-image lowerdir byte length on prod host) not run — authorization-consumed / post-merge read-only.
