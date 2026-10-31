# Decision M-b context: minimum release age before bumping

System: as in M-major-versions/context.md (scheduled monitor that bumps IronClaude's codegraph pin after verify + proof, then opens a PR a human merges; a merged pin reaches every Coder workspace).
Facts (gh api repos/colbymchenry/codegraph/releases, read 2026-10-30): v1.3.0 2026-07-07, v1.3.1 07-09, v1.4.0 07-10, v1.4.1 07-10, v1.5.0 07-21, v1.6.0 08-26, v1.6.1 09-29, v1.6.2 10-03. Quick follow-up patches happen (1.6.1 -> 1.6.2 in 4 days; 1.4.0 -> 1.4.1 same day). Upstream may delete or re-tag a bad release. The user's global rules use about two weeks as the minimum age for new dependency versions (coordinator-stated; the closest rule found on disk is the harness rule that script versions must be at least two weeks old).
Question: how old must a release be before the monitor bumps to it, and what does it pick when the newest release is too young?
