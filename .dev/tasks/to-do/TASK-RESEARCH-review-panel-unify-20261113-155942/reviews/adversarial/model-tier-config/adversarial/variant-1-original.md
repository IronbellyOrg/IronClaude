# Proposal A: central panel targets anthropic-only, launching by class name (sonnet, opus, haiku), for C03

**Position.** The central Review Panel supports exactly one launch contract: a reviewer is started by passing a class name (`sonnet`, `opus` or `haiku`) to the in-session Agent call. Reflect's anthropic-only gate becomes the gate for every consumer. Gateway models are reached by binding a class to a gateway model through the three `ANTHROPIC_DEFAULT_*_MODEL` variables before the session starts, and the binding is recorded. The gateway environment stays in the tier file as a record-only cell with `launch: {}`; a consumer that selects it runs the legacy path and records the reason (reflect rule D4, `SKILL.md:320`).

**Source of the conflict.** `synthesis/synth-04-options-conflicts.md` C-03, Option A (lines 172-184); open owner item O-2 (`gaps-and-questions.md:207`).

**Evidence tags.** Citations of the form `04 §4.1` mean `research/04-panel-resolution-identity.md` section 4.1. `CR` is E2's `COMBO-REPORT.md` and `RR` is E2's `tools/run-reviewer.sh`, both read with `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<file>` on the day this proposal was written; the E2 numbers are the study's own report text and are not re-aggregated (`synth-04` evidence rules). `[external]` marks a source outside the repository, with its URL.

## Design

### Core (panel resolver, tier file, run manifest)

1. **One supported launch cell.** `environments.anthropic-only` in `review-tiers.default.json` is the only environment whose `launch` map is filled (model id to class name, `:35`). The core treats a resolved reviewer as dispatchable only when `launch` is one of `sonnet`, `opus`, `haiku`. Reflect already enforces this for `reflect-*` templates (`_REFLECT_LAUNCH`, `panel.py:72`; `_check_reflect_resolution`, `:153-156`). The other consumers get the same rule from the dispatcher (the C09 resolution, "the pin is enforced"), not from a second copy in `panel.py`.
2. **Default environment becomes the supported cell.** `select_env` (`panel.py:485-494`) loses its `T3Model01` rule and falls through to `anthropic-only`. `--env` and `SUPERCLAUDE_REVIEW_ENV` stay as the explicit ways to pick `gateway`. This removes the D12 single-variable detection that research 04 flags (04 §4.2, §10 item 4) instead of patching it with an alias check, because there is no gateway dispatch to protect.
3. **Tier file bytes do not change.** No alias, class or environment entry is added. The packaged-tier golden (`tests/review/fixtures/panel-golden-packaged-tiers.json`, which breaks on any tier-file byte change, `research/12` section 5) stays valid. The `gateway` entry keeps `launch: {}` and its note "dispatch mechanism per model not defined yet" (`review-tiers.default.json:26`); under this option that note is an accepted fact, not a to-do.
4. **The class binding is recorded outside the resolution.** `panel/resolution.json` stays the unmodified stdout of `review panel resolve` (`SKILL.md:340`). The three `ANTHROPIC_DEFAULT_{SONNET,HAIKU,OPUS}_MODEL` values as Wave 0 resolved them (`SKILL.md:232`, the "Wave 0 alias set is canonical" rule at `:1507`) go into the run manifest as an extra key of the `resolved` stage payload, `launch_binding`. `manifest.advance_stage` hashes the payload and validates only `reviewers_requested`, `reviewers_resolved` and `outputs` (`manifest.py:277-316`), so the key needs no manifest schema change.
5. **Gateway models are an operator binding, not a resolver feature.** To run a gateway model in a panel slot, the operator sets the class variable to that model id before launch. The combination experiment did exactly this (`PLAN.md:83-89`; served models in `results.md:39-47`). The resolver keeps resolving the Anthropic-class record; the recorded binding and the observed identity (C08) say what actually served.

### Consumer modules

| Consumer | What it does under this option |
|---|---|
| Reflect Tier 2 (skill path) | No change to the shadow step 1 command (`SKILL.md:340`, `--env anthropic-only`, `--hard-exclude-class`, `--strict-distinct`). Dispatch passes `model` from `reviewers[N].launch` on every Agent call (C09), so the `reflect-reviewer` frontmatter default (`agents/reflect-reviewer.md:6`) can no longer replace the panel. `launch_binding` is added to the `resolved` payload. |
| Tasklist and spec review loop (E3, `rules/prompts/document_review_loop_prompts.md:70`) | The prompt text does not change: it calls `panel resolve` without `--env`, and the new default (core item 2) makes that call resolve in anthropic-only. A first review gets the template's panel by class; a re-review gets the anchor only (`panel.py:600-605`). |
| Future consumers (brainstorm and design hooks, PR review, rf-qa, `research/10`) | Declare a template (and, per C04, a distinctness and replica policy). They launch by class. rf-* agents carry no `model:` and inherit the caller (`research/10` X12), which is compatible with a per-call class. |
| Code-driven Tier 2 engine behind the tasklist post gate (`superclaude reflect run`) | Out of C03. C17 is decided: fix in place now, replace at UC-2 Stage 5. It keeps launching `T2Model0N` proxy models through `openai_compat` (`research/13` section 9.2, C12 row; `cli/reflect/ensemble.py:154-182`). When Stage 5 replaces it, its reviewers must be expressible as classes (see Risks). |
| E2-style evaluation harness | Not a consumer of the central panel. It stays a subprocess runner on raw model ids (`RR:48`). It is a measurement tool, and C20 keeps it as the quality benchmark beside shadow mode. |

## How it works

### Data flow for one run

1. The consumer starts a session. The operator's environment fixes the class bindings (`ANTHROPIC_DEFAULT_SONNET_MODEL`, `_HAIKU_`, `_OPUS_`). Wave 0 reads them once and treats that set as canonical for the run (`SKILL.md:232`, `:1507`).
2. The consumer runs `superclaude review panel resolve --template @<name> --run-id <id> --kind first|re-review [--env anthropic-only] [--hard-exclude-class <executor class>] [--strict-distinct]`. With no `--env`, the result is the anthropic-only cell. The resolver is unchanged: pure, sha256-frozen, stdout only (`panel.py:565-707`, `panel_cmd.py:18-108`).
3. The resolution lists each reviewer with `model` (the pin in the tier file's terms), `launch` (a class), `fallbacks` (empty in this cell, `04 §4.1`) and `stand_in`.
4. The orchestrator advances the manifest stage `resolved` with `{"reviewers_requested": N, "reviewers_resolved": M, "launch_binding": {"sonnet": "<value>", "haiku": "<value>", "opus": "<value>"}}`.
5. The dispatcher makes one Agent call per reviewer with `model = reviewers[i].launch` and refuses to dispatch a reviewer whose `launch` is null or outside the class set (a dispatch error, not a frontmatter default; `results.md:35` shows the collapse this prevents).
6. Observation, where the run is driven through `claude -p --output-format stream-json`: the served model of each Agent call is the most common `message.model` among events whose `parent_tool_use_id` is that call's id (`.dev/eval-workspaces/shadow-model-combos/analysis/extract.py:56-58`). It is stored as `observed` next to `requested` and `launch` (C08). Where no stream is available, `observed` is `unknown` with `identity_source: requested-pinned`, and the record says so (`SKILL.md:348`).

### Contract fields

| Field | Where | Status under this option |
|---|---|---|
| `reviewers[].launch` | `panel/resolution.json` | Existing; value is a class name |
| `environment` | `panel/resolution.json` | Existing; `anthropic-only` unless overridden |
| `launch_binding` | manifest `resolved` payload | New key, no schema change (`manifest.py:277-316`) |
| `requested`, `launch`, `observed`, `identity_source` | attempt payload | Decided in C08; not C03-specific |
| `panel_fallback_reason` | reflect telemetry | Existing (D4); written when a consumer selects `gateway` or hits a null `launch` |

### CLI surface

No new command and no new flag. One default changes: `panel resolve` without `--env` and without `SUPERCLAUDE_REVIEW_ENV` resolves `anthropic-only` on every machine. `--env gateway` still works for generic templates and still prints `launch: null` (`tests/review/test_review_panel.py:303-305`); for `reflect-*` templates it still fails closed with `launch None is not one of sonnet, opus, haiku` (`04 §4.1`).

## Evidence

Tags: `[CODE-VERIFIED]` means I read the cited code in this checkout (branch `ironbelly/shadow-runs`, HEAD `792cf8c52`) while writing; `[RUN]` means I ran the command while writing; `[OBSERVED-RUNTIME]` is a dated runtime fact from an experiment record; `[DOC-SOURCED]` is E2's own report text; `[external]` is outside the repository.

**Group 1: the gateway cell cannot dispatch today.**

- **EV-1.** The gateway environment has `launch: {}`, so every gateway reviewer carries `launch: null`. Code: `review-tiers.default.json:25-30`; `panel.py:595` and `:679`. Research: `04 §4.1`. [CODE-VERIFIED] [RUN] With no `--env` in this shell, `superclaude review panel resolve --run-id run1` printed `environment: gateway` and `launch: null` for all four reviewers of the default template (`claude-sonnet-5-5`, `muse-spark-1.3`, `glm-5.3`, `Qwen3.8-max`).
- **EV-2.** No reflect template resolves in the gateway. [RUN] `superclaude review panel resolve --template @reflect-pre --env gateway --run-id run1` printed `invalid reflect resolution: t1b-1: launch None is not one of sonnet, opus, haiku; ...`. Code: `panel.py:153-156`. Research: `04 §4.1`.
- **EV-3.** The environment is picked by one variable. `select_env` returns `gateway` when `$T3Model01` is non-empty and reads nothing else (`panel.py:485-494`); the shell here has `T3Model01=glm-5.3` (research dates the same value 2026-11-13, `04 §4.2`). Two tests pin the rule: `tests/review/test_review_panel.py:339` and `tests/review/test_review_cli.py:83-88`; the uncovered neighbour is `T2bModel01` (`research/12` section 4, D12 row). [CODE-VERIFIED]
- **EV-4.** The anthropic-only cell has one model per tier, so every `fallbacks` list is empty there. Code: `review-tiers.default.json:33-35`. Research: `04 §4.1`. [CODE-VERIFIED] [RUN] The default template in anthropic-only printed `sonnet, haiku, haiku, haiku` with `launch` `sonnet, haiku, haiku, haiku` and `stand_in` true for the three haiku slots.

**Group 2: class names are the launch form the platform gives an in-session orchestrator.**

- **EV-5.** [external] The Claude Code subagent documentation, https://code.claude.com/docs/en/sub-agents, states: "On an Agent tool call, that parameter takes a model alias: `sonnet`, `opus`, `haiku`, or `fable`. Claude can't pass a full model ID or `inherit` on that call." (Fetched on the day this proposal was written; the page also says frontmatter `model:` accepts a full model ID, which is a different mechanism, see Risks.)
- **EV-6.** Reflect already dispatches by class: the shadow combination extractor reads `input.model` of each Agent call as `sonnet`, `haiku`, `opus` or `None` (`.dev/eval-workspaces/shadow-model-combos/analysis/extract.py:60-62`), and the tier file's anthropic-only `launch` values are exactly those names (`review-tiers.default.json:35`). Research: `04 §4.1` last bullet, `04 §6`. [CODE-VERIFIED]
- **EV-7.** Fifteen of fifteen combination runs reached manifest stage `published` with three of three reviewers complete (`.dev/eval-workspaces/shadow-model-combos/FINDINGS.md:3`; `results.md:5-19`). Fourteen passed a class on every reviewer call; A3 passed none and collapsed to one model (`results.md:35`, EV-12). [OBSERVED-RUNTIME 2026-11-13] The runs are descriptive and carry no quality score (`FINDINGS.md:3`, `:40-42`); they show that the class path completes, not that any panel is better.

**Group 3: a class can be bound to any model the gateway serves, so gateway models stay reachable.**

- **EV-8.** The class-to-model mapping is set by `ANTHROPIC_DEFAULT_{SONNET,HAIKU,OPUS}_MODEL`, outside the resolver (`PLAN.md:44-52`; `SKILL.md:123-131`). The combination runs changed only those values and the resolution stayed byte-identical (`PLAN.md:54-58`; `04 §7.2` first bullet). [OBSERVED-RUNTIME 2026-11-13]
- **EV-9.** Raw model ids work as class values. Combination C's haiku slot was served by `claude-haiku-5-5`; D's opus slot by `gpt-6-luna`; E's haiku and opus slots both by `gpt-6-luna` (`results.md:39-47`). `PLAN.md:98` and `:103` had marked "raw id as env alias" UNVERIFIED before the runs; the runs verified it for these two ids. [OBSERVED-RUNTIME 2026-11-13] Untested: `muse-ember-1.0` (not in the gateway list that day, EV-14) and any other id.
- **EV-10.** E2's best replicated real-blocking panel, `haiku + 2x luna` (`CR:367`, `CR:428`), has the shape of combination E (two distinct models, three reviewers, `FINDINGS.md:13`; `PLAN.md:104-107`) and E ran through class values. [DOC-SOURCED for E2's panel quality, E2 at 4a22d742; OBSERVED-RUNTIME for the reachability]

**Group 4: where the anthropic-only label misleads, and what that costs.**

- **EV-11.** On this machine the haiku class is bound to the tier2 gateway alias (`ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]`, read from the shell), tier2's first model is `gpt-6.1-sol` (`review-tiers.default.json:7`), and combination runs A1-A2 and B1-B3 served the haiku slot with `gpt-6.1-sol` (`results.md:33-38`; `FINDINGS.md:15`). Research: `04 §4.1` (last bullet), `04 §7.2`. [CODE-VERIFIED for the tier list; OBSERVED-RUNTIME 2026-11-13 for the routing] The name `anthropic-only` is not true at serving time here.
- **EV-12.** The record cannot see this. `FINDINGS.md:15`: "The panel record (`panel/resolution.json`, card headers, `panel_parity`) never shows this; only the transcripts do." Parity was `True` for E1-E3 although two distinct models served (`results.md:17-19`), and A3 collapsed to one model because the orchestrator passed no class (`results.md:35`; frontmatter default `model: sonnet`, `src/superclaude/agents/reflect-reviewer.md:6`). Research: `04 §7.2`, `04 §7.3`. [OBSERVED-RUNTIME 2026-11-13] This is a recording defect (C08, C09, both decided), not a defect of class launch itself: the same swap would be invisible under any launch form that records only the request.
- **EV-13.** No in-session tool returns the served model of an Agent call. The served model comes from stream-json events (`extract.py:56-58`) or from a `claude -p` reviewer's top-level events (`RR:51`). `identity_source: observed` has no code (`SKILL.md:348`). Research: `04 §6`, `04 §7.1` and key takeaways. [CODE-VERIFIED by grep in research `04 §6`]

**Group 5: what E2 measured, read at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only.**

- **EV-14.** `muse-ember-1.0`, E2's default panel member, is in no alias, name or class of the packaged tier file (`review-tiers.default.json:4-23`; `04 §4`). E2's own ladder registered it on 2026-11-12 as "being added as Tier 04 Model 02" (`RR:19-26`), and the combination plan records it as absent from the 2026-11-13 gateway list (`PLAN.md:109`, list read with `GET /v1/models`, `PLAN.md:42`). [CODE-VERIFIED for the tier file; DOC-SOURCED for the gateway list]
- **EV-15.** Model choice is not E2's lever. "No panel catches designSpec GT1, GT2, GT10 or alias GT4, so model choice cannot lift the ceiling past ~2.5/14" (`CR:371`); "All panels sit at about 2-2.5 of 14" (`CR:428`). Panels of five reviewers gave "no gain for 2-4x the cost" (`CR:369`). `sonnet + 2x luna` was "statistically indistinguishable" from `ember + 2x luna` on found defects, real blocking, wrong blockers and control found (`CR:428`, permutation tests, n=6). The biggest named levers were harness fixes: the 200-character anchor limit and naming `source.md` (`CR:371`). [DOC-SOURCED; one gateway, 2026-11-12 to 2026-11-13]
- **EV-16.** The surviving effect is a repeat, not an environment: "second luna raises control found +0.83 (p 0.004 Welch, 0.048 permutation, baseline all zeros)" (`CR:298`). That is a replica policy (C04), and class slots can carry it (two slots bound to the same model, combination E).
- **EV-17.** E2's model knowledge is dated and volatile. The ladder carries owner orders dated 2026-11-12 (`RR:19-26`); the exclusion list `glm-5.3 Qwen3.8-max` is at `RR:69`; the combination plan lists Qwen3.8-max as disqualified (3 of 3 timeouts) and glm as the largest spend with retries (`PLAN.md:20-23`). A cyclic-ladder incident on 2026-11-12 ran a review on Qwen3.8-max until guards were added (`RR:66-71` comment). E2 used raw ids because "tier aliases serve only the first model of a tier" (`manifest.md:11` at the commit; [UNVERIFIED] here, cited from research `04 §4.2`). [DOC-SOURCED]
- **EV-18.** The packaged gateway lists put those excluded models first in tier3 and in the default template: [RUN] the default template in the gateway resolved `t3-1 glm-5.3` and `t3-2 Qwen3.8-max`. Research: `04 §8` ("The packaged tier lists contradict E2's dated findings").

**Group 6: the other consumers and the test surface.**

- **EV-19.** The code-driven Tier 2 engine launches `T2Model0N` proxy models through `openai_compat`, so applying a class-only rule to it would remove its reviewer pool (`research/13` section 9.2, C12 row; `cli/reflect/ensemble.py:154-182`). C17 (decided) keeps it as is until UC-2 Stage 5. [CODE-VERIFIED]
- **EV-20.** The loop prompt calls the resolver without `--env` (`src/superclaude/rules/prompts/document_review_loop_prompts.md:70`), and a test pins that sentence (`tests/review/test_review_rules_text.py:21`, `:31`). With no `--env` the call resolves gateway here (EV-1), so the E3 loop's reviewers currently carry no launch instruction at all (`04 §4.1`, third bullet). [CODE-VERIFIED] [RUN]
- **EV-21.** The run manifest accepts extra keys in a stage payload: `advance_stage` hashes the payload and validates only `reviewers_requested`, `reviewers_resolved` and `outputs` (`manifest.py:277-316`). [CODE-VERIFIED]
- **EV-22.** The two golden fixtures are `tests/review/fixtures/panel-golden-packaged-tiers.json` (breaks on any tier-file byte change) and `panel-golden-default-live7.json` (keys name the environment explicitly); `research/12` section 5. [CODE-VERIFIED for existence; behaviour from research]

## Correctness argument

The claim is that Option A is the smallest design in which every dispatched reviewer has a launch value the platform accepts, a recorded binding that says what the value means on this machine, and no silent default. Each step below rests on the evidence items named.

1. **The launch value is valid by construction.** The in-session Agent call takes only a class alias (EV-5), and the cell this option supports fills `launch` with exactly those aliases (EV-6). The dispatcher rule (launch must be a class, and the call's `model` must equal it) turns the three observed failure shapes into errors: a `launch: null` reviewer (EV-1), a missing class that falls to the frontmatter default (EV-12, A3), and a Fable value where a profile forbids it (existing test, `test_review_panel_reflect_profile.py:183-186`).
2. **The default cell is a dispatchable cell.** Today a consumer that omits `--env` on a ccsession machine gets `gateway` and a panel with no launch instruction (EV-1, EV-3, EV-20). After the `select_env` change, forgetting `--env` yields a panel that can run. A failure that was silent can no longer happen by omission, and the unsupported cell is reached only by naming it (`--env gateway`, `SUPERCLAUDE_REVIEW_ENV=gateway`), where reflect templates still fail closed (EV-2).
3. **Gateway models stay reachable without a second dispatch path.** A class can be bound to a raw gateway id, and the runs show the bound model serving the slot (EV-9). E2's best real-blocking shape is expressible this way (EV-10). So Option A does not remove the gateway's models from reach; it moves the choice of model from a packaged data file to the operator's launch environment, where the model fact is created.
4. **The record is made honest by recording, not by renaming.** The mismatch seen on 2026-11-13 (a haiku slot served by `gpt-6.1-sol`, EV-11) was invisible because only the request was recorded (EV-12). `launch_binding` in the manifest says what each class was bound to (EV-8, EV-21), and the C08 triple adds `observed` where a stream exists (EV-13). A built-in check that compares `launch`, binding and `observed` (SC-4 and SC-7 of `synthesis/synth-02-target-gaps.md`, lines 55 and 58) fails the run when they disagree. This repair is needed under every option, because observed identity is a property of the dispatch record, not of the environment name.
5. **The measured benefit of a gateway adapter is small.** E2's own conclusion is that model choice does not lift the ceiling and that harness fixes come first (EV-15); its one surviving effect is a repeat (EV-16), which a class slot carries. A design that spends an L-size, High-risk change (the synth rating of Option B) to widen model choice is spending on the lever E2 found weakest. This is DOC-SOURCED, one gateway, 2026-11-12 to 2026-11-13, and I use it only as supporting evidence, as the evidence rules in `synth-04` require.
6. **Facts that rot stay out of packaged data.** The gateway list moved within a day (EV-14, EV-17), and the packaged gateway lists already disagree with E2's dated findings (EV-18). With this option nothing dated enters `review-tiers.default.json`; the dated fact is the run's own `launch_binding`.
7. **Nothing decided elsewhere is contradicted.** C04 (replicas and distinctness declared per slot) is carried by class slots. C08 and C09 (identity triple, enforced pin, one dispatcher interface) are built on the class adapter. C17 keeps the proxy engine until Stage 5 (EV-19). C20 keeps E2's harness as the quality benchmark. The dispatcher interface of C09 allows another adapter later; this option ships one.

**What this argument does not show.** It does not show that class launch gives better review quality than a gateway adapter. Neither that nor its opposite was measured: the combination runs carry no ground-truth score (EV-7), and E2's runs used raw ids in subprocesses, not reflect (`PLAN.md:36-38`: "Transfer to reflect is a hypothesis"). The argument is about correctness of dispatch and proportion of effort, and the preference for A rests on those two grounds only.

## Risks and mitigations

**The weakest point.** The environment is named `anthropic-only` and the launch values are Anthropic class names, but on this machine the haiku class serves `gpt-6.1-sol` (EV-11), and the resolution, the card headers and the parity check all describe Anthropic models that did not serve (EV-12). Option A does not make the label true. It makes the label a statement about the launch contract, and it relies on two recordings (binding and observed identity) to say what served. Until C08's observation exists, an interactive session cannot observe the served model at all (EV-13) and the record carries `requested-pinned`; an option that dispatches through a `claude -p` adapter can observe at the top level (`RR:51`) and so has a stronger identity story. That is a real advantage of the opposing design, and the mitigation below narrows it without removing it.

| # | Risk | Likelihood and impact | Mitigation |
|---|---|---|---|
| R1 | Label and record differ from the served model (weakest point). | Observed in 5 of 15 combination runs (A1, A2, B1-B3, `results.md:33-38`); Medium impact (misleading parity and telemetry). | Record `launch_binding` at Wave 0; add the C08 triple; add the launch-versus-observed built-in check; where no stream exists, write `identity_source: requested-pinned` and make no independence claim (`SKILL.md:348`). Wave 0 step 0.5 already counts distinct bound models (`:232`); warn when two classes bind the same model. |
| R2 | Documentation says a family alias on an Agent call can run on the parent's exact model when the parent belongs to that family [external, https://code.claude.com/docs/en/sub-agents]. Whether this applies to classes bound to gateway ids here is untested [UNVERIFIED]. | Unknown; would add a second path to a silent swap. | Treat the binding as a statement of intent, never as proof of the served model; observation (R1) is the only proof. |
| R3 | No model failover: every `fallbacks` list is empty (EV-4); E2's owner order of 2026-11-12 asked for a fallback for every model (`RR:19`). | Medium: an outage in one class fails that reviewer. | Mark the reviewer partial and keep the others (C15, decided); one re-dispatch of the same class. Failover ladders have a recorded cost: the 2026-11-12 cyclic incident (`RR:66-71`) and the overwritten attempt files (`04 §5`). E2 ran its final batch with `NOFALLBACK=1` (`CR:422`). |
| R4 | At most three distinct models per panel (three classes; Fable excluded by the reflect profile). | Low: reflect caps at 3 (`panel.py:73`), and E2 found no gain beyond three reviewers (EV-15). The proxy engine allows 2 to 4 reviewers (`research/13` C11 row). | State the ceiling in the dispatcher contract. At UC-2 Stage 5 decide the cap together with C14. |
| R5 | The `select_env` change alters behaviour for E3 users on ccsession machines: they now get a class panel where they got a panel with no launch values. | Low impact (the old result had no dispatch instruction, EV-20), Medium visibility. | Release note; `SUPERCLAUDE_REVIEW_ENV=gateway` and `--env gateway` still work. Alternative that keeps `select_env`: add `--env anthropic-only` to the loop prompt at `:70`, which changes the pinned sentence (`test_review_rules_text.py:21`) and the plugin mirror (`tests/skills/test_review_brief_placement.py:132`). I prefer the code change because it protects every future consumer. |
| R6 | The default template resolves `sonnet + 3x haiku class` in anthropic-only (EV-4): three reviewers on one bound model, flagged only by `stand_in: true`. In the gateway the same template gave `glm-5.3` and `Qwen3.8-max` (EV-18), which E2 excluded. | Medium: duplicate reviewers become the default loop panel. | Not caused by this option but made visible by it. C04 requires declared replicas and flagged duplicates; the E3 template descriptions must say so (the `live7` description gap, `04` stale-doc list). Template data change, not a tier-file change. |
| R7 | The proxy engine's `T2Model0N` pool does not fit a class-only rule when UC-2 Stage 5 replaces it (EV-19). | Deferred; High if ignored. | Out of C03. Record as an open item for the Stage 5 decision; a later adapter is additive. |
| R8 | The owner picks the gateway under O-2. | Possible. | Nothing is deleted: tier file, `gateway` cell and `launch` schema are untouched. A gateway adapter is then an additive change (new launch kinds, filled `launch` entries, a golden regeneration), and the `select_env` default is flipped back by one line. |
| R9 | A frontmatter `model:` accepts a full model id [external, same URL], so per-model agent definitions could give per-call raw ids without a subprocess. | Not a risk to this option; a rival mechanism. | Out of scope here: it needs one agent file per model and its own read-only allowlist (C18). It is reachable later as an adapter and does not conflict with this option. |
| R10 | All gateway evidence is one gateway on 2026-11-12 and 2026-11-13 (G-33). | Applies to every option. | Date every model fact and re-probe at launch; this option stores no model fact in packaged data. |

## Test coverage needed

### Existing tests that change

| Test | Change |
|---|---|
| `tests/review/test_review_panel.py::test_select_env_precedence` (`:331-341`) | Line 339 flips: `select_env(None, {"T3Model01": "x"})` is now `anthropic-only`. Keep the explicit-argument, `SUPERCLAUDE_REVIEW_ENV` and empty-environment assertions. |
| `tests/review/test_review_cli.py::test_panel_resolve_gateway_when_t3model01_is_set` (`:83-88`) | Rename and flip: with `T3Model01` set and nothing else, `environment == "anthropic-only"`. Add its pair: `SUPERCLAUDE_REVIEW_ENV=gateway` gives `gateway`. |

### Existing tests that must stay green unchanged (they are the guard that nothing else moved)

- `tests/review/test_review_panel.py:303-305` (gateway prints `launch: null`), the 17 reflect-profile tests including `:183-186`, both golden fixtures (the tier file is untouched), the explicit-`gateway` live7 tests (`test_review_panel_live7.py:109-132`, `:203-238`), `tests/review/test_review_rules_text.py` (prompt text untouched), and the shadow contract and exit tests that pass `--env anthropic-only` (`tests/cli/reflect/test_shadow_skill_contract.py:245`; `tests/cli/reflect/test_shadow_exit_script.py:27`).

### New tests

1. **Default cell is dispatchable.** With `T3Model01` and `T2bModel01` set and no other variable, every packaged template (8) resolves for `first` and `re-review` with `environment == anthropic-only` and every `launch` in `{sonnet, opus, haiku}`.
2. **Gateway stays fail-closed for reflect.** Through the CLI, `--env gateway` with each `reflect-*` template exits non-zero with `launch None is not one of sonnet, opus, haiku`. No test pins this today (grep of `tests/` for `launch None`, `is not one of` finds only the Fable case at `:183-186`).
3. **D4 fallback record.** A consumer that selects `gateway` or hits a null `launch` runs the legacy path and writes `panel_fallback_reason`. No test in `tests/` mentions `panel_fallback_reason` today; the rule exists only as skill text (`SKILL.md:320`).
4. **Dispatcher precondition (shared with C09).** A reviewer with `launch` null, outside the class set, or `fable` is a dispatch error; every Agent call carries `model == launch`; an absent class never falls to the frontmatter default (the A3 collapse, `results.md:35`).
5. **Binding record.** The `resolved` payload with `launch_binding` is accepted and replay-identical; a second advance with a different binding raises `Conflict` (`manifest.py:295-298`); two classes bound to the same model produce a warning.
6. **Swap fixture.** A recorded stream in which the haiku slot is served by `gpt-6.1-sol` (the 2026-11-13 case) makes the launch-versus-observed check fail, and a stream with no served-model events yields `observed: unknown` with `identity_source: requested-pinned`, never `observed`.
7. **Class-ceiling test.** A template whose resolved reviewers need more than three distinct classes is rejected by the dispatcher check with a message naming the ceiling.

Run set for the change: `uv run pytest tests/review/test_review_panel.py tests/review/test_review_panel_live7.py tests/review/test_review_panel_exclusion.py tests/review/test_review_panel_reflect_profile.py tests/review/test_review_reflect_templates.py tests/review/test_review_cli.py tests/cli/reflect -q` (the panel-resolution gate G3 of `research/12` section 8, plus the CLI and reflect directories).

## Cost

| Item | Size | Note |
|---|---|---|
| `select_env` default and docstring (`panel.py:485-494`) | XS | Two lines removed. |
| Two existing tests flipped, one renamed | XS | Listed above. |
| `launch_binding` in the `resolved` payload, and the reflect skill step 1 text | XS | No manifest schema change (EV-21); skill text edit in `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and `make sync-dev`. |
| New tests 1, 2, 3, 7 | S | Pure resolver and CLI tests. |
| New tests 4, 5, 6 and the launch-versus-observed check | Shared with C08 and C09 | Needed under every option; not charged to C03. |
| Tier file, goldens, templates | none | No byte change to `review-tiers.default.json`; both goldens stay valid. |
| New files, new CLI surface | none | |
| **C03-specific total** | **XS to S** | `synth-04` rates Option A as XS with Medium risk; the `select_env` change and the new tests are the reason for "to S". |

Recurring cost: the operator sets three environment variables per session to change the panel's models. The cost of widening later, if the owner chooses the gateway under O-2, is the additive adapter work listed in R8; none of this option's changes has to be undone for it.

Items I did not check: whether `claude -p` without `--forward-subagent-text` exposes sub-agent `message.model` in the parent stream (`04` gap 6, UNVERIFIED), and whether class bindings to ids other than `claude-haiku-5-5` and `gpt-6-luna` serve as expected.
