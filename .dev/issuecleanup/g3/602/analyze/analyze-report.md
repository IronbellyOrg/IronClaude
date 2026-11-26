# Confidence-check architecture analysis

## Scope and method

Command: `/sc:analyze src/superclaude/skills/confidence-check --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/602/analyze`.

Read-only static architecture pass on the smallest existing capability folder: three files, the 150-line skill, 305-line TypeScript reference and empty Python package marker. Checked the package scorer and its unit tests, adversarial command interface and separate hypothesis calibrator as integration context, not as additional implementation scope. Checkout HEAD: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`.

Codegraph: index_state=stale, checked_at=2026-11-24T13:23:38Z; degraded: graph:stale. The single readiness check reported one pending added file. All analysis used Glob, Grep and Read; no index mutation or runtime execution.

## Severity-rated findings

1. **High, feature gap:** no public confidence command or blocker-confidence protocol was found. Glob `src/superclaude/commands/*confidence*` had no match; Grep `sc:confidence` across `src/` had no match. The existing skill is explicitly readiness-only at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/confidence-check/SKILL.md:8-30,114-122`. This keeps #602 relevant, rather than proving a regression.
2. **High, invalid reuse risk:** the reference scorer adds readiness flags, not calibrated blocker probabilities. The TypeScript sum is at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/confidence-check/confidence.ts:67-119`; its output bands at lines 276-283 recommend implementation actions. Do not use its 90% threshold as an established blocker threshold or apply automated severity demotions from it.
3. **Medium, limited evidence claims:** the skill correctly limits its eight-case perfect-score metric to trigger recognition at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/confidence-check/SKILL.md:14-20`, but line 150 still says unqualified production precision and recall. The TypeScript header repeats perfect results at lines 10-13. Neither is evidence for blocker calibration; narrow such claims when refactoring.

## Metrics and limits

Three files in the target folder, with 455 nonempty-file physical lines reported by line-numbered reads. Empty `__init__.py` has no behaviour. Unit-test source `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/unit/test_confidence.py:15-79` tests readiness scores and five reported checks, not #602's blocker boundary cases. No test execution, external dependency audit, model benchmark, calibrated probability measurement or dynamic verification was performed. Security and performance were not the requested focus; no security or performance guarantee follows from this static architecture pass.

## Recommendations

Keep #602 open. Specify the confidence use cases and scoring meaning before wiring a new thin command and protocol to reusable agents. Reuse existing adversarial model/persona and pipeline configuration where it fits, rather than assuming it needs a rewrite. Establish an evidence-backed blocker threshold and explicit shortfall arithmetic before implementing severity decisions, preserving the independent safety boundary. Review prior Jev evidence, define quick-depth ad hoc debate and the default full debate path, and design automated comparisons across models, personas and topics. Changes and experiments require their own authorization; none were performed here.
