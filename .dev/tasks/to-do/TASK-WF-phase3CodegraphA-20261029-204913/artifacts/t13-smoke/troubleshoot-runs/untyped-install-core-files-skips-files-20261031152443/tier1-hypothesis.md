# Hypothesis: Existing targets without force follow the preservation branch
**Agent**: root-cause-analyst (inline fallback: invalid restricted profile)
**Tier**: 1
**Timestamp**: 2026-10-31T15:24:43Z
**Cause class**: Other: intentional overwrite protection, conditional incident explanation
**Claim class**: runtime_behavior
**Evidence class**: source_static
**Verdict direction**: AFFIRM
**Consistency with docs**: aligned
consistency_with_docs: aligned
runs-in=unknown
## Claim
The implementation explicitly appends a name to skipped and continues when its existing-target condition is true and force is false. This is one conditional explanation, not an established cause of the user's run.
## Evidence
- src/superclaude/cli/install_core.py:66-68: `if dest_file.exists() and not force:` followed by `skipped.append(src_file.name)` and `continue`.
- src/superclaude/cli/install_core.py:83-88: returned skip message says existing files and use --force to overwrite, listing each name.
- tests/cli/test_how_we_work_install.py:53-75: test_install_never_touches_existing_files_without_force asserts seeded files retain original bytes. Execution state: not-run.
- docs/getting-started/installation.md:263: force is the overwrite option.
No external primitive behavior is asserted as incident cause: the local branch and message body are directly read defining artifacts. No behaviour-definition fetch is required for an external primitive assertion.
## Proposed Fix
No causal fix established; no files to change. Obtain original arguments and returned message first. Preserve the non-overwrite default; the existing preservation regression test covers that contract but was not run.
## Confidence
Self-reported confidence: 0.30 (incident explanation unverified).
Evidence grounding: 1.0, exact source read. Runtime check: 0.0, source-only and not-run test. Symptom coverage: 0.5, filenames and invocation absent. Reproducibility fit: 0.5, deterministic branch but no reproducer. Fix directness: 0.0, no incident-specific fix established. Domain coherence: 1.0, installation only.
## Risks
Overwriting can discard user customizations. Never auto-enable overwrite to suppress a preservation message.
## If I'm wrong, it's probably because...
The user's omitted transcript describes missing source files or copy failures rather than the explicit existing-target skip branch.
## Falsification standard
A provenance-bound original call with force=True returning this function's skipped-files message would refute this branch explanation for that call. No command or original result was supplied.
## Evidence classification
Runtime behavior; source-static only; runtime check not performed because the run site and authorization are unknown. No passing arm claimed.
## Alternatives considered
Copy failures are recorded separately in the implementation; no failing-run evidence establishes or excludes them. Source selection uses top-level Markdown only, but no missing filename was supplied.
## Grounding gaps
No failing-run capture, exact filenames, force argument or environment supplied. Auggie unavailable. Native hypothesis worker unavailable because its shadowing project profile contains tools beyond the loaded protocol's roster. Documentation and observability branch workers unavailable; parent fallback used. Diagnosability is partial; capture/control rows remain pending in diagnosability-tasklist.md. Producer citation check skipped: empty menu. No primitive-behavior or environment-property causal claim established.
