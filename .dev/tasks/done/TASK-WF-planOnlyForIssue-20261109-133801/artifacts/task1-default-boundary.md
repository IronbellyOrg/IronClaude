# Task 1 default-boundary evidence

Governing structure: Task 1 Acceptance criteria and Outputs in ../TASK-WF-planOnlyForIssue-20261109-133801.md. This is execution evidence, not an independent review.

## Configured default and parent override (T1.AC1)
Current local configuration inspection on 2026-11-09 read only the model field from /home/coder/.claude/settings.json and the named model environment fields. Observed output:

```text
user_settings=/home/coder/.claude/settings.json
saved_model='claude-gw-tier1b[1m]'
ANTHROPIC_MODEL=''
CLAUDE_CONFIG_DIR=None
CLAUDE_CODE_SUBAGENT_MODEL=None
CLAUDE_CODE_SUBAGENT_MODEL_FORCE=None
```

This is a present-day configuration snapshot, not a historical launch snapshot or backend verification. It establishes that the saved user preference is separate from the workspace variable in this environment. The native user-settings file is a documented read source, not an unknown location.

Initial intake, before product edits: the launcher read only the workspace variable before its role-start fallback and passed the parent profile as --model. Implementation now reads the workspace ANTHROPIC_MODEL, or, when empty, the documented saved user settings model. It validates that configured choice against the existing role resolver before parent-only arguments, binds the resolved choice through CLAUDE_CODE_SUBAGENT_MODEL, and then applies parent --model/--tier. No saved preference is written. The launch double captures the two selections separately.

## Role fallback and policy precedence (T1.AC2)
Implementation retains the existing username, matching-role and wildcard resolver and its role-start/default-tier fallback. Unavailable configured values take that fallback. Family aliases are validated through their actual workspace mappings, not their capability names. Deliberate valid child values and the administrative force variable are preserved; environment inherit is treated as unset. Applicable policy parse errors propagate rather than opening access.

## Forwarding permissions (T1.AC3)
Implementation extracts the model-resolve policy check into a shared guard. Generic shim POSTs check the original model before alias discovery, then the resolved destination before forwarding. Tier routing checks the concrete fallback destinations too. Parse errors from policy are handled outside the JSON parser guard. Local stand-in tests record model requests; no real model endpoint is exercised. Unrestricted-owner and no-tier routing remain bounded by the existing contract.

## Regression coverage (T1.AC4)
Added launch captures and runnable regressions for full-ID/tier configured defaults distinct from parent --model/--tier, saved picker settings at default and relocated paths, workspace-vs-saved precedence, valid and denied explicit children, force/inherit, suffixes, unavailable saved defaults, malformed settings and legacy operation. Added stand-in allowed/denied raw/picker/tier requests, malformed policy, shared allowed models and a resolved-destination guard check. Existing role precedence, fallover and stream cases remain in the same suite. Dependent Tasks 2-5 have not started.

## Observed test output (T1.AC5)
Initial command: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/unit/test_ccsession_tiers.py -q`. Observed exit 1: 4 failed, 194 passed in 195.25s. Exact output is preserved in `task1-tests-initial.log`. One introduced regression printed the owner-unknown diagnostic twice because child and parent resolution each emitted it. Three failures came from new test expectations: picker alias normalization preserves decimal dots, and the fixture's tier2 primary is muse-spark-1.3. Corrections retain error reporting while emitting the owner diagnostic only on parent resolution, use the real picker spelling, and assert the actual tier primary. The initial run collected before the latest tests were added and source was edited during that run, so it is not final-tree verification.

The initial UV run built the editable package and reported installing 27 packages in the local environment. No explicit installation command or global configuration change was performed. The stable-tree rerun used `uv run --no-sync pytest tests/unit/test_ccsession_tiers.py -q`: exit 0, 201 passed in 193.62s, preserved in task1-tests-rerun.log. No source edits overlapped that stable run. Lint, formatting, launcher syntax and whitespace checks passed before it. No real model endpoint or historical replay was exercised by these tests.

The first independent review found that a permitted picker alias could remain unresolved after a failed catalog refresh and fall through without a destination check. The fix reuses the shared destination guard for that unresolved literal. Six regression combinations cover restricted/unrestricted/no-tier owners with ordinary and [1m] selectors, plus the existing resolved-destination/non-model case. The scoped rerun passed 7 tests (200 deselected) in 3.04s; ruff format/check and whitespace checks passed. The full stable-source rerun after this fix completed with exit 0: 207 passed in 192.12s, preserved in task1-tests-after-review.log. No source edits overlapped that run. This is local regression evidence, not independent compliance acceptance.

## Supported source, compatibility and execution disposition (T1.AC6)
Observed installed CLI: /usr/local/bin/claude, version output `2.1.319 (Claude Code)`. This exceeds the documented ordinary-precedence cutoff 2.1.251 and force-setting minimum 2.1.257. It establishes documented feature compatibility only, not an observed native child dispatch.

Official sources read on 2026-11-09:

- https://code.claude.com/docs/en/model-config: `/model` normally saves the `model` field in user settings. The shell ANTHROPIC_MODEL value and launch --model are session selections, not writes to that saved preference. Configuration precedence must not be invented from their names.
- https://code.claude.com/docs/en/settings: user settings normally reside at ~/.claude/settings.json; CLAUDE_CONFIG_DIR can relocate them. Project/local/managed settings and --settings participate in native resolution. Worktree local settings can come from the main checkout. The page also names an Agent SDK resolveSettings helper; that is not an existing shell-launcher integration or an installed dependency established by this intake.
- https://code.claude.com/docs/en/sub-agents: ordinary precedence is per-invocation model, frontmatter model, child environment default, then parent. Frontmatter inherit selects the parent; environment inherit behaves as unset. Administrative force changes precedence and must not be manufactured by this fix.

The CLI --help inspection initially captured only 8192 characters through a pipe, ending mid-option. Its apparent absence of a Commands section was incomplete negative evidence, not proof that commands were absent. Repeating the same help-only invocation with a temporary-file stdout capture returned 22336 characters and a Commands section. Its listed commands contain no effective-model/settings resolution command. --settings and --setting-sources are inputs. This bounded help check does not prove that no other integration exists.

The supported saved-default source is the user settings model field, read from CLAUDE_CONFIG_DIR/settings.json or HOME/.claude/settings.json. This integration deliberately reads the saved user preference, not the complete effective native session settings. Workspace ANTHROPIC_MODEL has its documented precedence; an unavailable value retains role fallback. Project/local/managed settings, caller --settings, account-native defaults and changes inside an already-running session are not re-resolved by this wrapper. The README states this ceiling, the minimum native versions, and the shim-local boundary. No SDK dependency, settings write, parent substitution or universal default was introduced. Actual installed CLI compatibility is documentation-based; no paid native child probe was run.

Execution disposition: incomplete, 0/5 tasks complete. Correction after the user's challenge: the supposed retained prohibition on required review calls was an assistant interpretation error. The no-model wording came from assistant-authored planning inputs and applied to that planning run; the user's implementation authorization already permits required implementation reviews. The first fresh audit-validator review ran, with gpt-6.1-sol recorded as its only served model in complete transcript records. It found the unresolved-picker defect described above. Parent Read-back confirmed the quoted Task 1 instruction and actual fallthrough, deriving the noncompliant verdict extra. Raw and parent-derived reviews are preserved under artifacts/retries/T1/. No completion, Ruling, FINAL or archive is claimed. Execution reuses the existing start snapshot.

The reviewer also attempted SendMessage to team-lead, outside its declared Read/Grep/Glob roster. That attempt is recorded in review-1.md and disqualifies this run from demonstrating restricted-tool compliance for completion acceptance. Its independently confirmed product defect is fixed; a fresh independent reviewer is still required on the corrected tree and must use only the declared read tools. Complete-record transcript recovery excluded six malformed/partial JSON records; those records were not used as review evidence. Existing verified-Tier1b/restricted-profile requirements and the prior actual nested-worker-depth refusal remain separate constraints. No depth bypass occurred here.

Dependent selector edits remain gated on Task 1 acceptance. Canonical source referenced above is src/superclaude/skills/ccsession-tag/ccsession. The planning contract and original historical diagnosis remain unchanged. Evidence and managed ledger are staged under .dev/tasks; .dev/issues and .claude are not staged by this run.
