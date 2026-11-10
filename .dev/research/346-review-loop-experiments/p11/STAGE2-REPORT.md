# Stage 2: real S1 spec review loop (issue #346)

Spec under review: the S1 frozen packet (Orca worker-contract spec, 57,763 bytes, sha256 d3cdbe57...25200d).
Workers: sonnet subagents acting as /sc:spec-panel in per-run sandboxes (no Orca, no live repo; repo-path citations UNVERIFIED).
Loop: review, revise, re-review, revise, re-review (stop on PASS), then an identical whole-document audit (first review, new design command + rules file) on the final spec.

| Arm | Command | Briefs | n |
|---|---|---|---|
| 1 | master (#427) | original coordinator briefs ("any finding of any severity is FAIL", "apply all findings") | 3 |
| 2 | master (#427) | new FIRST-REVIEW / RE-REVIEW / REVISE prompts pasted inline | 6 |
| 3 | PR #484 design | rules file + hard gate, short pointer briefs | 6 |

| Metric | Arm 1 | Arm 2 | Arm 3 |
|---|---|---|---|
| Loops ending in PASS within 3 reviews | 0 of 3 | 6 of 6 | 6 of 6 |
| Mean reviews to finish | 3.0 | 2.0 | 2.2 |
| Mean spec growth | +66.7% (+56 to +79) | +0.6% (0 to +1.5) | +1.4% (+0.2 to +3.8) |
| Mean output tokens per replicate (loop + one audit, each message counted once) | 0.56M | 0.17M | 0.17M |
| Whole-document audit PASS | 2 of 3 | 1 of 6 | 1 of 6 |
| Mean blocking findings in audit | 0.33 | 1.83 | 1.50 |

Per-run rows: see harness state files under runs/*/state.json.


CORRECTION (2026-11-10): the first version of this table reported 1.25M / 0.33M / 0.33M output tokens. That figure double-counted messages (each message is logged once per content block) and missed steps ingested before token capture existed. Recounted from the raw transcripts with each message id counted once: loop only = 0.48M / 0.105M / 0.100M; audit = 0.077M / 0.064M / 0.069M. Arm 1 costs about 3.3x arms 2 and 3 (loop plus audit), not 3.8x.
