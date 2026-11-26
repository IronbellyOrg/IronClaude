authorized narrowly scoped launcher/harness identity integration so jobs retain their originating session identity across resets and background execution, without restricting human pushes.

once done run /sc:implement to implement and /sc:pr-submit

Context: docs/designs/sc-issue-launch-level-hook.md section 19.1 and the blocked Task 1 evidence in the prior workflow package. Preserve the existing immutable blocked plan; this new authorization permits a scoped identity integration, not silently weakening human isolation or claiming the whole launch-level enforcement hook is built. Use existing hook/launcher distribution and no new dependencies or services. Record supported lifecycle behavior, same-user guardrail limits and any unsupported detached cases explicitly. All Git test targets are disposable local bare repositories, not protected refs on the real fork. Submit the completed work only through /sc:pr-submit --monitor 3 on IronbellyOrg/IronClaude.
