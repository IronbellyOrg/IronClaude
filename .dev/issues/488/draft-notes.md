# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Owner update beyond the original sentence: rename current Tier 3 to Tier 2b; new Tier 3 has GLM 5.3, Grok 4.7 and Qwen 3.8; Tier 4 has GPT 6 Luna and Claude Haiku 5.5. Source: `description.md:5-9` in this draft directory.
- Tier JSON names environment slots; workspace settings supply values, and existing failover has error, cooldown and window rules: `src/superclaude/skills/ccsession-tag/ccsession-models.json:93-119`, `src/superclaude/skills/ccsession-tag/models.py:454-466,650-673`, `src/superclaude/skills/ccsession-tag/README.md:413-432`.
- The wrapper recognizes `--fallback-model` as an option with a value, but its relationship to tier failover was not established: `src/superclaude/skills/ccsession-tag/ccsession-orca:103-108`.
- Existing documentation names IDs for GLM, Grok, Qwen and Luna; the live gateway and all five requested IDs were not verified: `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md:41-42`.
- Issue workers pin Tier 3, Tier 2 and Tier 1a, and the issue protocol describes their use and unavailable-tier behavior: `src/superclaude/agents/issue-worker-t3.md:1-11`, `src/superclaude/agents/issue-worker-t2.md:1-6`, `src/superclaude/agents/issue-worker-t1.md:1-6`, `src/superclaude/skills/sc-issue-protocol/refs/tiers.md:9-17,32-46`.
- Tier 3 and Tier 4 fixture slots and Tier 3 routing are pinned in `tests/unit/test_ccsession_tiers.py:69-84,2877-2898`; worker pins and retry-ladder slot references are tested in `tests/skills/test_issue_worker_agents.py:22` and `tests/skills/test_model_alias_policy.py:30,215-226`. The retry ladder may be affected by a changed slot value: `docs/reference/model-aliases.md:58-63`.
- Related issue context: `gh issue view 384 --repo IronbellyOrg/IronClaude`, `gh issue view 395 --repo IronbellyOrg/IronClaude`, `gh issue view 407 --repo IronbellyOrg/IronClaude`, `gh issue view 462 --repo IronbellyOrg/IronClaude`.
- Observable tests, live launch verification and migration checks are proposed acceptance criteria informed by `src/superclaude/skills/ccsession-tag/README.md:413-432` and `tests/unit/test_ccsession_tiers.py:2877-2898`; details require the owner's decisions.
- Codegraph and auggie tools were unavailable; the pass used Glob, Grep and Read and did not probe the live gateway.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- The original GLM-first, Terra-fallback request differs from the checked-in fixture and routing assertion, which put Terra first and GLM second: `tests/unit/test_ccsession_tiers.py:69-73,2892-2893`. The documented order also differs: `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md:35-41`. Neither proves the current live workspace order.
- The owner update's Tier 2b and revised Tier 3 and Tier 4 do not match the checked-in tier definitions: Tier 2b is not listed, Tier 3 has six slots and Tier 4 has one, `src/superclaude/skills/ccsession-tag/ccsession-models.json:70-120`; the documented Tier 3 and Tier 4 memberships differ, `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md:35-42`.
- The original Terra-fallback sentence and the update's new Tier 3 model list do not explicitly reconcile Terra's absence from that list: `description.md:3-9` in this draft directory. Resolution is an open question, not an assumed contradiction in live behavior.
