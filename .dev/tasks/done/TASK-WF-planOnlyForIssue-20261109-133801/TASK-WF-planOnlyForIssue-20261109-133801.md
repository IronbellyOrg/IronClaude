---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-planOnlyForIssue-20261109-133801
version: "1"
priority: Medium
created_date: "2026-11-09"
---

# Honor role-permitted defaults in native agent selection

Source: ./source.md
Goal: For the four named native agents and the connected brainstorming/evaluation-to-adversarial calls, use the user's configured, role-permitted default when they did not choose a model. Keep deliberate permitted model choices, reject unavailable choices, and do not silently promote a task to Opus.

## Constraints

- This is an ordinary workflow plan, not implementation approval. The current run changes only planning artifacts. Implementation, tests that exercise new code, model calls, configuration changes, commits, pushes and external posts are not performed by plan generation.
- The historical Orca cause remains undetermined. Preserve the accepted diagnosis, its confidence of 0.30 and its original audit. Static default-selection corrections do not prove why the disputed historical sessions selected Opus. Do not repeat the completed worker completion signal or couple this work to issue #463.
- The smallest complete approach is to bind a validated configured default through the existing native subagent environment setting, remove framework-created model preferences, and retain explicit choices. Simply deleting agent metadata is insufficient: native omission otherwise falls back to the current parent, which may differ from the configured default.
- Planning evidence: ccsession's apply_tier_selection already prefers an allowed ANTHROPIC_MODEL over the role start tier; models.py user_access gives username rules precedence over matching roles and the wildcard. The proxy validates tier routes, while its ordinary _post path forwards non-tier requests after alias conversion. Do not claim that picker filtering or launching an allowed parent already enforces every child request.
- Official native semantics were read on 2026-11-09 at https://code.claude.com/docs/en/sub-agents: per-call model overrides frontmatter; frontmatter overrides CLAUDE_CODE_SUBAGENT_MODEL; that environment default overrides the current parent fallback. Explicit inherit selects the parent, not the saved user default. The forced environment override is an administrative exception. Native per-call selection accepts family aliases, not arbitrary full model IDs or inherit. These are documentation findings, not a local integration result.
- The existing wrapper consumes ANTHROPIC_MODEL as the configured workspace default, with its existing role-permitted start-tier fallback when that value is absent or unavailable. This is the supported starting point, not proof that every saved Claude picker preference is represented by that variable. Task 1 must establish that distinction before shipping a claim about the user's default. Do not introduce a universal tier or model. A deliberate session-only --model/--tier choice must remain the parent choice, not silently become a saved default. Preserve a deliberate, valid subagent environment choice and administrative force setting; never manufacture force=1.
- Coder template sources were inspected read-only: VSCode-AIDev02/orca/runtime.mjs serveEnv loads defaults then per-user files and forwards owner roles and ANTHROPIC_MODEL. Its defaults.sh distinguishes role rules from model slots. These current source observations are not historical launch snapshots. No Coder repository edit, installation or global configuration edit is authorized here.
- Runtime work is bounded to ccsession tier mode and its shim. Outside tier mode preserve native platform behavior and do not invent Coder permissions. No claim of gateway-wide security, direct-gateway enforcement, or automatic policy refresh of already-running sessions is in scope.
- Stop execution before dependent selector edits if the configured-default binding cannot be implemented using the existing role resolver and documented native environment behavior. In particular, a Claude picker setting that differs from ANTHROPIC_MODEL must not be asserted equivalent without supported integration evidence. Record an unresolved requirement rather than replacing it with parent inheritance.
- Canonical delivery files live under src/superclaude and tests. Installed primitives must reference installed/project callable surfaces, never checkout-only source paths. Do not hand-edit installed files or .claude mirrors. Stage .dev/tasks, including this package; do not stage .dev/issues or .claude. Commit only on separate approval.
- Every delegated execution remains subject to the existing verified-Tier1b and restricted-profile requirements. No new model execution is authorized by this planning run. A required independent review that cannot run is blocked, not a self-certified PASS.
- Catalogs, supported-value lists and explicitly labelled examples may retain Opus. Other workflows' independent defaults, reflection escalation, recommendation evaluation matrices and roadmap/release policies remain outside this bounded correction. The connected cli-eval create default enters scope because its W3 directly forwards that default to the affected adversarial dispatcher. Do not call this a repository-wide removal of implicit model choices.
- Use existing launch doubles and local stand-in gateway fixtures for regression checks, not paid requests or historical-command replay. Task evidence, if execution is later approved, belongs under ./artifacts/. Preserve initial failures and intermediate evidence. Final independent verification and archiving belong to the executor.

## Phase 1: Establish the enforceable default-selection boundary

## Task 1: Define the shared selection contract and its regression cases

Goal: Make an omitted native child selection use the validated configured default independently of a parent-session override, with role checks at the shared shim boundary.

Inputs and delivery files:
- src/superclaude/skills/ccsession-tag/ccsession: environment loading, apply_tier_selection, export_selection and the tier-mode launch branch.
- src/superclaude/skills/ccsession-tag/models.py: user_access, tier_access, _my_models, in_my_tiers and the model-resolve/default-tier command branches.
- src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py: curation, _post, alias conversion and _forward_tier.
- tests/unit/test_ccsession_tiers.py: existing _launch doubles, owner/access fixtures, ANTHROPIC_MODEL precedence cases and stand-in proxy tests.
- src/superclaude/skills/ccsession-tag/README.md: the model/environment settings table and tier access explanation.

Change:
- Extend the existing resolver/launcher, not a new selection service. Resolve the configured default before consuming session-only MODEL_ARG/TIER_ARG. When no deliberate child environment selection exists, export the resolved model or tier alias through CLAUDE_CODE_SUBAGENT_MODEL in tier mode. Do not derive it from the overridden parent PROFILE_MODEL. Preserve valid explicit child environment selections and native administrative force semantics; do not add a force assignment.
- Establish the supported saved-default source and native version compatibility from available configuration/code and current official documentation before claiming the integration is complete. Check the installed Claude version without making a model request. If the user's saved picker preference is separate and no supported read path is established, stop this task with that concrete blocker and do not execute dependent tasks. Do not equate the two sources or invent a new configuration precedence.
- Reuse or extract the existing model-resolve access predicate so generic raw-model and picker-alias forwarding is checked against the same owner policy as tier routes. Validate the resolved destination as well as the original selector; reject an unavailable choice before sending its request upstream. Policy parse errors must not fall through to unrestricted forwarding. Preserve the existing unrestricted-owner policy, non-model endpoint behavior, tier fallback order, streaming and error handling. This is enforcement for the existing ccsession shim, not a separate gateway authorization system.
- Extend the existing fake launch capture with the child environment fields. Add stand-in gateway cases that record received requests so a rejected model is shown to have zero upstream requests. Explain the launch-default/parent-override distinction and the shim's enforcement boundary in the README.

Outputs: Updated shared resolution, launch binding, forwarding guard, README and local regression cases. Record the supported-default evidence and exact compatibility limitation with the test output in ./artifacts/task1-default-boundary.md.

Acceptance criteria:
- With distinct allowed configured and parent models, an omitted child uses the configured default; --model and --tier still select the parent without rewriting that child default. A valid explicit child selection remains unchanged. An explicit native inherit or force setting is handled according to documented native semantics, not mistaken for a universal product default.
- Absent, empty and unavailable workspace defaults retain the existing role-start fallback; malformed applicable role policy fails closed. Username, matching-role and wildcard precedence remain covered. No new hardcoded Tier1b, Opus or other universal model is introduced.
- A restricted-owner raw model, resolved picker alias and tier alias each reject denied destinations before forwarding. Permitted destinations still reach the stand-in gateway. Unrestricted-owner behavior and non-model endpoints remain compatible. Membership uses the actual configured model sets, not the words opus/sonnet/haiku as permission proof.
- The capture cases cover different configured and parent models, full-ID and tier defaults, explicit child environment, unavailable mappings, suffix handling and no-tier legacy operation. The stand-in cases cover denied raw/picker/tier models, shared allowed models and invalid policy without real model calls.
- Run uv run pytest tests/unit/test_ccsession_tiers.py. Record observed results and any failures in ./artifacts/task1-default-boundary.md; this command is a later execution check, not a test already run by this plan.
- The output names the actual supported default source and installed native-version compatibility. If either cannot be established without forbidden runtime activity or a new product decision, the task is blocked and dependent selector changes do not start.

## Phase 2: Remove agent-owned capability preferences

## Task 2: Align the four agent definitions and their direct author/reviewer callers

Depends on: Task 1

Goal: Remove the four agents' framework-created capability preferences while keeping direct explicit reviewer overrides intact.

Inputs and delivery files:
- src/superclaude/agents/auggie-reviewer.md: frontmatter model.
- src/superclaude/agents/eval-suite-author.md: frontmatter model and Model Preference.
- src/superclaude/agents/debate-orchestrator.md and src/superclaude/agents/merge-executor.md: Model Preference sections.
- src/superclaude/skills/sc-auggie-review-protocol/SKILL.md: deep-only reviewer spawn, default/revagent selection and retry propagation.
- src/superclaude/commands/auggie-review.md: --revagent help.
- src/superclaude/skills/sc-cli-eval-protocol/SKILL.md: create W4 eval-suite-author delegation only; its W3 model list is handled in Task 4.
- tests/commands/test_auggie_review_revagent.py and tests/skills/test_model_alias_policy.py: static command, caller and agent contracts.

Change:
- Remove the two model: opus fields. Do not replace them with model: inherit, another family, a gateway alias or a full backend ID. Replace the three capability-preference paragraphs with the rule that omitted selection uses the configured native default and explicit permitted selections remain explicit.
- Update the Auggie command and deep reviewer spawn explanation so the omitted --revagent path omits model and relies on Task 1's binding, not frontmatter Opus. Keep the accepted explicit aliases, early invalid-value STOP, quick/standard warning, deep-only dispatch and identical retry model propagation. Do not change the Auggie CLI model or per-persona Auggie calls.
- State explicitly that cli-eval's W4 author dispatch supplies no invented model override. Keep schema loading, author validation and all tool rosters unchanged.
- Update the existing static tests to enforce absence of model metadata on these agents and absence of high-capability fallback prose. Pin the changed caller help/default behavior without weakening explicit-override assertions or banning Opus from supported choices and examples.

Outputs: Updated four agents, two direct caller explanations, Auggie help and regression assertions. Preserve exact test output in ./artifacts/task2-agent-defaults.log.

Acceptance criteria:
- All four named agents have no implicit family preference; omitted native dispatch can reach the environment default. No agent tool capability, review independence rule or author validation is removed.
- The no-override Auggie and author paths omit the native model parameter. Explicit --revagent still passes the selected alias on every reviewer attempt, and never changes the lead or Auggie CLI selection. A disallowed destination is rejected by the shared shim, not silently replaced by a more capable model.
- Existing accepted-alias, invalid-value, depth and retry cases remain covered in tests/commands/test_auggie_review_revagent.py; add assertions for the four model-free definitions using tests/skills/test_model_alias_policy.py. Read the complete existing test assertions before editing them.
- Run uv run pytest tests/commands/test_auggie_review_revagent.py tests/skills/test_model_alias_policy.py and retain observed results. Static tests establish instruction contracts only; do not report them as an observed live native model selection.

## Phase 3: Preserve selection provenance through brainstorming

## Task 3: Replace implicit model rotation without changing explicit lists

Depends on: Task 1

Goal: Carry an unqualified selection through the shared agent-specification format without inventing a native tool model alias or losing persona/instruction data.

Inputs and delivery files:
- src/superclaude/skills/sc-brainstorm-protocol/SKILL.md: option defaults, Wave 0 validation, Wave 2C model rotation/serialization and downstream agent-spec handoff.
- src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md: Model-Rotation, serialization, Validation and round-trip vectors.
- src/superclaude/commands/brainstorm.md: usage and --models default.
- src/superclaude/skills/sc-adversarial-protocol/refs/agent-specs.md: model component, parsing and validation contract.
- src/superclaude/skills/sc-adversarial-protocol/SKILL.md: Mode B specification parsing and generation dispatch that consumes those specifications.
- src/superclaude/commands/adversarial.md: --agents grammar/help.
- tests/skills/test_brainstorm_protocol.py: existing section-scoped source-contract tests. Add tests/skills/test_native_model_defaults.py as a new focused source-contract test file for the shared default-selection representation and dispatch rules.

Change:
- Introduce the reserved specification token default as a protocol-level marker for omitted model choice. This is a proposed grammar extension, not an existing native alias. It retains the current model:persona:instruction shape and is consumed by adversarial before dispatch: omit the native model field for default; pass a validated explicit supported alias only for explicit selections. Never pass model: default, model: inherit or an arbitrary backend ID to the native tool.
- When --models is omitted, assign default to every selected persona, preserving proposal counts, persona ordering, exclusions, custom instructions and instruction escaping. When the user supplies --models, retain the validated order and round-robin behavior. Remove the deep-mode Opus promotion in both branches: depth changes work depth, not model permission or selection.
- Update both producer and consumer grammar/validation sections together so the new marker round-trips without being rejected as an unknown model. A list may intentionally mix default and explicit supported aliases. Keep malformed input rejection, supported explicit choices and persona/instruction preservation. Do not extend native alias support simply because the protocol previously said any available model.
- Replace unqualified default examples with default markers and label retained family-rotation examples as explicitly supplied --models examples. Remove the unverified blanket assertion that Coder no longer sets family aliases; describe resolution as environment-dependent, not proof of an actual backend or role permission. The shim in Task 1 remains the actual permission check.

Outputs: Consistent producer/consumer default grammar, native generation dispatch rule, help and section-scoped regression checks. Preserve the expected input, parsed selection and native-argument outcome for each trace vector in ./artifacts/task3-spec-roundtrip.md.

Acceptance criteria:
- Omitted --models at quick, standard and deep depths produces the requested count of persona/instruction specifications without any automatic family rotation or promotion. Explicit --models sonnet,haiku retains that order at deep depth; an explicitly supplied Opus remains a supported request subject to role access.
- Trace vectors cover default alone, default:persona, default:persona:instruction, mixed default/explicit lists, repeated defaults, escaped instruction quotes and malformed segments. The default marker is preserved until native dispatch and then becomes an omitted model field. No backend ID is fabricated by the specification builder.
- The adversarial generation instructions accept the same grammar emitted by brainstorming. Existing minimum/maximum agent counts, proposal caps, persona exclusion and serialization sanitization remain intact; a structural token cannot become an instruction injection path.
- Add static assertions for each changed producer, builder, consumer and command section in tests/skills/test_native_model_defaults.py, following the existing section-slicing style. Run uv run pytest tests/skills/test_brainstorm_protocol.py tests/skills/test_native_model_defaults.py and retain observed output with the trace vectors.
- Clearly distinguish manual protocol trace evidence and static source-contract checks from an executable parser or a live native dispatch. Do not create a second implementation of a prose parser merely to make a copied algorithm pass a test.

## Phase 4: Apply the selection contract to adversarial dispatch

## Task 4: Align comparison, coordination, advocacy and merge dispatch

Depends on: Task 2
Depends on: Task 3

Goal: Use the same default/explicit distinction for advocates, orchestration, merging and the connected cli-eval create pipeline.

Inputs and delivery files:
- src/superclaude/skills/sc-adversarial-protocol/SKILL.md: Agent Delegation, advocate task_dispatch_config, Mode A/Mode B assignment, Merge Executor Dispatch and model-labelled output/provenance fields.
- src/superclaude/skills/sc-adversarial-protocol/refs/agent-specs.md and src/superclaude/commands/adversarial.md: the shared default marker and explicit-selection grammar delivered in Task 3.
- src/superclaude/skills/sc-cli-eval-protocol/SKILL.md: create input default and W3 adversarial handoff.
- src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md: Mode B handoff example and agent integration descriptions.
- src/superclaude/commands/cli-eval.md: create usage and --agents default.
- tests/skills/test_native_model_defaults.py: extend Task 3's source-contract coverage for these remaining consumers.

Change:
- Make advocate dispatch conditional on parsed selection: default omits model; explicit supported alias passes the model value. Apply it to generation, debate, retries and re-dispatch without filling in a family preference. Mode A without --agents must no longer say current model when the intended behavior is the configured child default.
- Remove capability-ranked model choices from orchestration and merge instructions, including the unconditional merge model field. Those agents omit model by default, rather than inheriting the winning advocate's model. Do not add a coordinator/merge model override flag: preserve supported existing explicit advocate selections without expanding the command surface.
- Update cli-eval create's omitted --agents case to three default specifications, preserving its existing default number of competing designs rather than silently turning off the comparison. A supplied list is preserved, including its personas, instructions, order and permitted models. Both Mode A and Mode B consume the shared dispatcher contract. W4's author default remains as delivered in Task 2.
- Relabel retained family-specific integration examples as explicit requests. Where filenames, blind-mode processing or provenance currently use the requested model token, allow the default marker as a selection label, never as evidence of the served backend. Retain existing output layouts and contract keys; record actual backend only when genuinely observed, otherwise unknown. Keep debate/scoring/merge validation unchanged.

Outputs: Consistent native dispatch rules, connected cli-eval defaults/help and regression assertions. Preserve manual selection traces and observed checks in ./artifacts/task4-dispatch-coverage.md.

Acceptance criteria:
- Source-contract assertions cover omitted and explicit selection for generation and advocacy, Mode A omission, coordinator omission, merge omission and retry consistency. No highest-available family fallback remains in these named dispatch paths.
- Cli-eval create with omitted --agents represents three default-selected competing designs; an explicit list is forwarded unchanged. Its run pipeline, suite schema, loader, existing suite files and actual evaluation runner receive no model-policy changes.
- Default-labelled variants remain distinguishable by their existing variant number/persona and work with blind comparison. Provenance differentiates requested selection from an observed backend. Neither a native alias nor the new protocol marker is presented as backend verification.
- Manual traces include a default-only brainstorming handoff, an explicit sonnet/haiku handoff, a mixed list, direct compare with no agent list and cli-eval create with/without --agents. Every omitted child reaches the shared default binding and every explicit destination remains subject to the shim permission guard. These are contract traces, not new model requests.
- Run uv run pytest tests/skills/test_native_model_defaults.py tests/skills/test_brainstorm_protocol.py tests/commands/test_auggie_review_revagent.py. Preserve observed output and disclose that static protocol checks do not prove live LLM compliance.

## Phase 5: Deliver consistent source contracts and regression coverage

## Task 5: Update affected help, packaging and source-contract checks

Depends on: Task 4

Goal: Deliver a user-visible explanation and a regression guard that keeps the affected source, help and existing plugin surface consistent.

Inputs and delivery files:
- src/superclaude/skills/ccsession-tag/README.md: extend Task 1's settings-table change with a concise native-subagent selection section explaining the configured default, explicit override precedence, role rejection, administrative force exception and supported runtime boundary.
- plugins/superclaude/commands/brainstorm.md: this is the existing plugin-side command surface. Align only its --models usage/default, automatic-example descriptions and active-model composition claims with src/superclaude/commands/brainstorm.md as delivered in Task 3. Do not overwrite unrelated plugin differences or fabricate absent plugin agents/skills.
- tests/skills/test_native_model_defaults.py: extend the focused contracts from Tasks 3-4 with a complete affected-selection inventory and assertions for the existing plugin command.
- Makefile: use sync-dev and verify-sync as delivery checks; do not change the targets. scripts/build_superclaude_plugin.py reads plugins/superclaude, not the canonical source tree, and its build deletes the old distribution directory, so do not run a plugin build or cross-repository synchronization as a side effect of this correction.
- tests/unit/test_install_ccsession.py: use its existing isolated wiring tests as a compatibility check; no real home-directory install is permitted.

Change:
- Write the concise selection section in the existing README. Separate configured child default from parent-session choice, protocol marker from native alias, and requested selection from served backend. State the actual supported saved-default source established in Task 1, not an unverified generic claim about every Claude picker setting.
- Update the existing plugin command's affected model-policy paragraphs/help without creating missing plugin protocols. Report that the inspected plugin tree does not ship the affected protocol packages; this work does not repair the wider incomplete plugin distribution. Do not claim a complete plugin runtime from command parity alone.
- Add section-scoped assertions covering the exact affected source inventory: four agents; Auggie caller/help; brainstorming protocol/builder/help; adversarial grammar/generation/advocacy/coordinator/merge; cli-eval create caller/help/integration map; and the existing plugin brainstorming command. Keep legitimate explicit Opus examples and supported-value catalogs legal. Do not implement a blanket word ban or duplicate the model resolver in tests.
- After approved implementation, generate development mirrors through make sync-dev, then run make verify-sync. Never edit or stage those mirrors directly, never install to the user's home, and never synchronize another repository. Preserve pre-existing unrelated drift as a disclosed failure rather than fixing it under this task.

Outputs: README selection contract, aligned existing plugin command and whole-scope regression assertions. Preserve the observed checks, scope diff and compatibility limits in ./artifacts/task5-delivery.md.

Acceptance criteria:
- The README and named command help describe the same default/explicit behavior and role limitation as the implemented resolver. The explanation makes no historical causal claim, no universal Tier1b claim and no claim that an alias proves a backend.
- Source-contract tests fail if any named implicit selection path reintroduces a family preference, passes the default marker to the native model parameter, changes an explicit list by depth, or leaves the existing plugin command advertising automatic family rotation. Retained explicit examples and supported models are not falsely rejected.
- Run uv run pytest tests/unit/test_ccsession_tiers.py tests/unit/test_install_ccsession.py tests/commands/test_auggie_review_revagent.py tests/skills/test_model_alias_policy.py tests/skills/test_brainstorm_protocol.py tests/skills/test_native_model_defaults.py, then make sync-dev and make verify-sync. Record actual results; do not describe a skipped or failed check as a pass.
- Inspect the final diff for checkout-only source references inside installed primitives, unintended tool/permission changes, changes outside the enumerated delivery files and altered explicit selections. Installed lookups retain the required global/project surfaces. Any new src/superclaude reference inside a primitive must be a justified maintainer instruction or removed.
- Stage generated .dev/tasks evidence and the requested canonical delivery changes only under the later executor's rules. Do not stage .claude, .dev/issues or the project-root artifacts directory. No install, real model call, Coder-source mutation, commit, push, PR or merge is part of this task's checks.
- Final independent verification remains executor-owned. A unit with unresolved default-source compatibility or an unavailable independent reviewer is reported blocked or partial, not complete; a successful static check alone does not establish live model-selection behavior.
