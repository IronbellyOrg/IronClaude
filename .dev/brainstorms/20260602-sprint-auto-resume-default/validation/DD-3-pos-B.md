# Position B — Strongest alternative: report-only-no-mutation (default), with optional copy-to-quarantine-dir

**Claim:** The gate should, by default, **detect and report** suspect next-task artifacts
without renaming anything. The gate's job (FR-2) is to STOP and require an operator
decision; it does not need to mutate the filesystem to do that. When the operator
explicitly opts into cleanup, copy (not rename) the suspect artifacts into a dedicated
`<results>/.resume-quarantine-<ts>/` directory with a manifest — the SAME shape as the
existing `preserved/` stash that `restore_from_bundle` already knows how to reverse.

## Why report-only is the safer default
- The gate already STOPs on `not passed` (design §6). A STOP plus a printed list of suspect
  paths fully satisfies FR-2.4 ("require operator decision") with ZERO filesystem mutation
  and ZERO new restore surface. NFR-1 ("read-only until the gate passes") is honored
  literally instead of carved out with an exception.
- Renaming the next-task output **before** the operator has decided is itself a mutation on
  the suspect seam — the exact thing FR-2 says to treat with "deep suspicion." If the
  classification is wrong (file was actually fine), the rename has already perturbed state
  that the subsequent rerun engine globs by canonical name.

## Why copy-to-quarantine-dir beats rename-in-place when cleanup IS wanted
- `restore_from_bundle` (rerun_tasks.py:1039) restores from a `preserved/` dir + manifest.
  A copy-to-quarantine-dir reusing that exact `preserved/` + `manifest.json` shape is
  reversible by the code that ALREADY EXISTS — no vaporware `sprint resume --restore`.
- A rename scatters `.failed-<ts>` siblings next to canonical files; a quarantine dir keeps
  the canonical results tree clean and makes "what did resume touch?" a single-directory
  question.

## Concession
- Copy doubles bytes for large transcripts; rename is O(1). But per-task transcripts are
  the gitignored, bounded artifacts here, and correctness/reversibility dominates a few KB.

## Against git-stash
- `.gitignore:230` ignores `phase-*-task-*-output.txt`; git stash cannot stash ignored
  files, and the operator's working tree may hold unrelated changes. git-stash is the
  weakest of the three alternatives for this artifact class. (Both positions agree here.)
