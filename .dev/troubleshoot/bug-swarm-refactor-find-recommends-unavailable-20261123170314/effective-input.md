# Effective-Input Manifest

## Selector and working tree
selector_command: explicit artifact paths in evidence-validator brief; no Git range selector
selector_cwd: /home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s
base_ref: db57e231863078dbbb8e4e5fb37a61371c89806c
head_ref: db57e231863078dbbb8e4e5fb37a61371c89806c
dirty_files: only new diagnostic output directory
staged_files: []
unstaged_files: [] (tracked source unchanged)
excluded_foreign_commits: [] (no commit-range review)

## Included runtime evidence
included_files: stub-run/return-contract.yaml, tier1-observation.md captured-output spans, live refactor_find.py, commands.py recommendation substitution, reduce.py renderer/emitter, active adversarial input contract; evidence-validator receives these paths through REPORT.md.draft and explicit observation_paths. Auxiliary context/calibration and all four boundary cards are supplied too.
runtime_surface_claim: original recommendation generation, captured fresh-run artifact and candidate's declared input shape; not repaired source or a paid-model run.

## Intersection and validation
intersection_proof: actual failing artifact selected explicitly, not inferred from a nonempty Git diff. Saved YAML's three successful final_path inputs were checked readable; recommendation was Read at line64. Source remains at original revision, git diff --name-only empty. Evidence-validator must Read actual source/artifacts, not treat this manifest as review completion.
validation_command: local-input-check-1 and git status/diff captured in session; final independent Read validation pending at initial creation.
validation_result: original artifact/input identity verified; no changed runtime surface to infer. No repair input, staged/dirty source, or foreign commit silently substituted.

## Verdict
HC4: N/A for an indirect Git selector, with rationale: this diagnostic review uses direct explicit artifact paths and no product source diff. This manifest preserves actual selected evidence. It does not prove that a later patch or downstream comparison saw the right surface.
