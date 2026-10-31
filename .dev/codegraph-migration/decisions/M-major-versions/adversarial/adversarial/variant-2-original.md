# Option B: majors never auto-bump; the monitor opens an issue and stops

- Minor and patch releases follow the automated path.
- A newer major: the monitor does not create a branch or PR. It opens (or updates, idempotently by title) one issue "codegraph vX.0.0 available: manual review" with the release notes link and the commands a person runs to bump by hand (the same script with `--allow-major`).
- Rationale: a major can break Phase 3 skills in ways the proof cannot see; a human decides when to adopt.
- Cost: majors need a manual run; a second code path (issue creation); while a major is pending, later minors of the old major still bump (if the script picks the newest release within the pinned major).
- Code: one comparison plus an issue step; the script gains `--allow-major`.
