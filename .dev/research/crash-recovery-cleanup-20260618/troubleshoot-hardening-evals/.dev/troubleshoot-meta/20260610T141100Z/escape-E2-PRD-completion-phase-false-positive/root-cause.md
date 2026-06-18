# Root cause: E2 PRD completion-phase false positive

## Verdict

The strongest merged root cause is a generated-artifact contract miss: the `parallel_instructions` gate was verified as a local phase-keyword rule instead of as a contract between the heavyweight PRD task-file template and the parser scope. The parser treated every `Phase N` section with `N >= 2` as executable parallel work, while the generated heavyweight task file used a different semantic topology: Phase 1 setup, middle executable work phases, and a final sequential completion/presentation bookend.

That mismatch became operationally fatal because the rule was attached to the STRICT `build-task-file` gate. A well-formed generated task file could therefore fail the gate solely because its final anti-orphaning completion phase intentionally omitted parallel-execution keywords.

## Surviving claims from the hypothesis cards

1. The defect was not simply missing keyword text in Phase 7. The evidence shows Phase 7 was intentionally sequential: `Present to User & Complete Task`, while Phases 2-6 were the real parallel work phases.
2. The parser boundary was syntactic rather than semantic. It used phase number and heading matches, not phase role, so final completion/presentation content was indistinguishable from a real work phase missing parallel instructions.
3. The verification gap was artifact-level. Existing review/test evidence modeled small helper snippets and local keyword enforcement, but did not include a live/generated seven-phase heavyweight PRD task-file fixture with setup and completion bookends.
4. The docstring/implementation contradiction was a warning sign but not an enforced invariant: the documented narrower phase range did not prevent implementation from checking all phases `>=2`.
5. STRICT gate severity amplified the escape. The brittle heuristic did not merely warn; it halted a live heavyweight PRD run at `build-task-file`.

## Refuted or weakened claims

- The broad claim that off-path review absence caused the escape is too strong. The PR #154 summary indicates adversarial option artifacts existed around the fix decision, so the better claim is that review artifacts were off the critical contract: they adjudicated or inspected local behavior and fix options, not the full generated artifact invariant before the live failure.
- A pure runtime-entrypoint explanation is incomplete. The live runtime path explains why the failure was fatal, but the underlying escape was the missing template/parser contract. A runtime-only test with another small synthetic fixture could still miss the same semantic boundary.
- A fixed positional range such as phases 2-5 is not a valid general root-cause answer. Evidence shows real heavyweight work ran through Phase 6, and short tasks can place completion or work phases at different positions. The durable invariant is role-based: enforce parallel instructions on executable work phases, not setup/completion bookends.

## Evidence chain

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row PRD-E05 identifies the missed contract directly: work phases are parallel, setup/completion bookends are intentionally sequential, and the implementation checked every phase `>=2` despite a narrower docstring.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 60-70 records the live failure message, the ground-truth phase topology, and the selected role-sensitive exemption.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 81-96 confirms the same boundary: only Phase 7 was sequential completion, while Phases 2-6 were parallel work phases.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` line 21 places the escape in live runtime: the PRD `build-task-file` gate halted on final sequential completion/presentation Phase 7.

## Generalized root cause

Generated workflow validators were not tested against the semantic topology of the artifacts they validate. The gate's parser made a local syntactic assumption, `Phase N >= 2 means parallelizable work`, that was not true for the generated PRD task-file contract. Review did not force parser scope, template phase roles, and gate severity to agree through a representative generated-artifact fixture.

## Pipeline check that should have caught it

A regression fixture should have evaluated the actual `build-task-file` gate against a representative generated heavyweight PRD task file containing:

- setup bookend phase without a parallel keyword, expected to pass;
- middle executable work phases with parallel/concurrent/batch language, expected to pass;
- final completion/presentation bookend without a parallel keyword, expected to pass;
- at least one true executable work phase without a parallel keyword, expected to fail.

The key invariant is not a hard-coded phase number range. It is that strict parallel-instruction enforcement applies only to executable work phases in the generated artifact, and excludes setup/completion bookends by role.
