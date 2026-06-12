# Effective-Input Proof (H4)

H4 applies when an independent review / audit / reflect gate consumes an **indirect selector** to choose the surface it reviews. It proves the reviewer actually consumed the runtime-produced surface. It closes **E5** (a POST-reflect selector that audited a range omitting the dirty `/task` work, possibly including foreign commits). The H4 status feeds the §5.4 aggregation in [`hardening-output-contract.md`](hardening-output-contract.md).

## Fail-closed rule (FR-10)

H4 **fails closed** when the effective input is:

- **absent**,
- **empty despite known changes**,
- **non-reproducible**, or
- **non-empty but the wrong surface**.

`E > 0` is **not** sufficient. The correctness of `|E ∩ true_runtime_surface|` (the intersection of the selected input with the true runtime surface) must be **proven**, not merely shown non-empty (fixes adversarial F-D1 — the real E5 mechanism). The proof records dirty/staged/unstaged inclusion **and** foreign-commit exclusion via a machine-checkable manifest.

## H4 Effective-Input Manifest schema (§5.6)

| Field | Required | Meaning |
|-------|----------|---------|
| `selector_command` / `selector_cwd` | yes | Command and working directory that selected the review surface |
| `base_ref` / `head_ref` | yes | Revision endpoints used by the selector |
| `dirty_files` / `staged_files` / `unstaged_files` | yes | Working-tree state at review time |
| `included_files` | yes | Files/commits/artifacts actually consumed |
| `excluded_foreign_commits` | yes | Foreign/stale commits excluded, or an explicit empty list |
| `runtime_surface_claim` | yes | The true surface requiring review |
| `intersection_proof` | yes | Machine-checkable proof that `included_files ∩ runtime_surface_claim` is correct |
| `validation_command` / `validation_result` | yes | How the manifest was checked |
