# Candidate fixes (Wave 3 distillation)

| # | Fix | Supporting cards (calibrated) | Verdict |
|---|---|---|---|
| F1 | Source check `_is_our_catalog` (dict entry, dict source, source=="directory", absolute path resolving to home/.claude/ironclaude-marketplace; never raises) before add/update; on mismatch report and skip pinned plugins, never touch the user's marketplace. Commands carry their marketplace name; a non-zero or raising marketplace add/update marks it broken and later commands for it are skipped and reported; time-limit check first. Refusal message names an already-installed copy. | tier1 (0.92), root-cause-analyst (0.92), quality-engineer (0.83) | consensus |
| F2 | F1 plus a post-add/post-update re-read gate | security-engineer (0.30) | outlier: its premise (add exits 0 while the entry stays foreign) refuted by the parent probe (tier1-observation.md, Discriminator probe; behaviour row 2) |

Merged constraints into F1: resolved-path comparison and malformed-entry tolerance (quality-engineer); marketplace key separate from report label (quality-engineer, root-cause-analyst); time-limit before broken check (both); refusal wording that does not say "rerun to retry" and names an existing installed copy (root-cause-analyst, security-engineer); `_pinned_home` fixture seeds the real directory source.
