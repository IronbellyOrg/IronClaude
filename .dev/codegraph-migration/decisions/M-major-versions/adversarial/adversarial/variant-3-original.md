# Option C: majors get the full automated PR, but always as a draft

- Minor and patch: ready PR on a passed proof.
- Major: the same verify + rewrite + proof, and the PR is always opened as a draft with label `codegraph-major` and a checklist (read the breaking changes; check Phase 3 skills that call codegraph tools), even when the proof passes.
- Rationale: the reviewer gets the full evidence (hashes, attestations, proof log, notes) without doing the bump by hand, and a draft cannot be merged until a person marks it ready.
- Cost: draft state is reused for two meanings (major review vs failed proof); the label and title tell them apart.
- Code: one comparison chooses `--draft`; shares every other step.
