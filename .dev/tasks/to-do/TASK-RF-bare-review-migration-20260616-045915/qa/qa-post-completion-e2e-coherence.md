# QA Report — POST-COMPLETION: end-to-end-migration-coherence

**Topic:** sc-bare-review M8/M9 migration (thin caller over `superclaude swarm run --lens bare-review`)
**Date:** 2026-06-17
**Phase:** doc-qualitative (post-completion e2e-coherence lens) / adversarial stance, fix_authorization: FALSE (report only)
**Working dir:** git worktree `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9`

---

## Overall Verdict: FAIL

The SKILL → CLI → contract → normalized-bodies **happy path is coherent and executable**
(an agent reading only SKILL.md can run the right command, and it produces what SKILL.md
promises). But the migration carries **two genuine coherence defects** — a wrong contract
schema in SKILL.md and an OPS-doc-vs-CLI drift on `done.json` — that would mislead a
consumer parsing the contract and an operator following the observability runbook. Under the
adversarial "any defect = FAIL" rule, this is a FAIL with two IMPORTANT findings. Note: my
two strongest initial hypotheses (exit-0-on-preflight-fail; done.json is an unwired bug) were
**disproven on closer inspection** and are documented below as cleared, so the FAIL rests on
the two findings that survived verification.

## E2E Trace (the operator's path, verified live)

| Step | Claim | Verified? | Evidence |
|------|-------|-----------|----------|
| 1. SKILL.md invocation executable | `superclaude swarm run --lens bare-review --target … --output … [flags] --transport …` | YES | `swarm run --help`: `--lens`, `--target`, `--output`, `--transport {openai_compat\|stub}` all real; all 5 caller flags (`--reviewers` B-1, `--target-line-cap` B-2, `--timeout-sec` B-3, `--label` B-4) exist with the documented defaults |
| 2. WS-0 inline path produces promised deliverables | emits `return-contract.yaml` + `bare-review-NN-<model>.*` | YES (with naming nit) | Live stub run wrote `return-contract.yaml` + 3× `bare-review-NN-lens-default-model-0.final.md` (+ `.meta.json`, `merged.md`, `execution-log.{jsonl,md}`, `manifest.json`). Each body carries `suspect: true`, `tier: T2`, `target_checksum`, finding table |
| 2b. suspect + handoff | `suspect:true` always; `recommended_next_command` names `--suspect-source` | YES | Contract `caller_metadata.suspect: true`; `recommended_next_command` contains `/sc:adversarial --compare … --suspect-source …` |
| 3a. env-missing STOP | preflight STOP naming missing var, non-zero exit | YES | `openai_compat` with vars unset → exit **1**, stderr names `T2ProxyUrl, T2ProxyKey`; no contract written |
| 3b. IMM-4 small-target STOP | STOP before dispatch | YES | <50 non-ws-byte target → exit **1**, stderr `imm4.target_too_small … STOP before dispatch`; no dispatch, no contract |
| 4. Guarding tests pass | parity + cited tests green | YES | `test_bare_review_parity.py` 16 passed; `test_recipe_bare_review` + `test_e2e_user_guide` + `test_imm_suite` 46 passed; golden-regen skipped (by design) |
| 5. `.claude/` mirror synced | source-of-truth discipline holds | YES | `make verify-sync` → "All components in sync" |
| 6. env-var name parity | SKILL ↔ config.py ↔ env-readiness.md | YES | `T2ProxyUrl`/`T2ProxyKey`/`T2Model01..09` identical in all three |
| 7. legacy-script orphans | no live pointer to deleted `t2_*.sh`/`refs/prompts.md` | YES (clean) | Deletions are staged (`git status`: D), present-at-HEAD only; rollback-procedure.md's references are intentional rollback targets; template's mention is a historical "were retired" note |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `src/superclaude/skills/sc-bare-review/SKILL.md` lines 49-56 ("Return Contract (§3.3)") | The documented contract schema does **not** match the contract the CLI actually emits. SKILL.md shows top-level `target_checksum`, `reviewers_requested`, `reviewers_succeeded`, `suspect`, and `output_files:[{path,model_id,status}]`. The CLI emits the **nested** schema: `target.checksum`, `workers_requested`, `workers_succeeded`, `caller_metadata.suspect`, and `output_files:[{index,path,raw_path,meta_path,final_path,model_id,model_label,bytes,status,http_code,attempts,elapsed_ms}]`. An agent that reads ONLY SKILL.md to parse the contract would look for `reviewers_succeeded`/top-level `suspect` and find neither. The parity test itself calls this the "nested schema" and asserts `workers_succeeded` / `caller_metadata.suspect` — i.e. the CLI is right and SKILL.md is wrong. | Rewrite the §3.3 block to the real nested schema (`workers_requested`/`workers_succeeded`/`workers_failed`, `target.checksum`, `caller_metadata.suspect`, the full `output_files[]` field set), or explicitly mark it an abridged illustration and point to `docs/swarm/observability-procedure.md` / the schema as authoritative. |
| 2 | IMPORTANT | `docs/swarm/observability-procedure.md` "Layer 4 — done.json" (≈L48-54) + debugging recipes (L72,74,79,91) | The doc presents `done.json` as "Written atomically once the run reaches a terminal state … the single yes/no 'job finished' signal," and its recipes treat a **missing** `done.json` as a stuck/failed symptom — with **no scoping to detached mode**. But the default inline `swarm run` (exactly what SKILL.md + operator-runbook.md tell operators to run) **never writes `done.json`**: `reduce.emit_done_sentinel()` has **zero call sites** in the run path, and `test_e2e_user_guide.py::test_quickstart_does_not_emit_done_sentinel` asserts the inline run produces normalized artifacts *but not* the sentinel. So an operator following the observability runbook's `[ -f "$OUT/done.json" ]` check would mis-diagnose a perfectly successful inline run as stuck/failed. (Spec default is `mode='inline'`, `write_done_sentinel=True`, yet inline emission is unwired by design — the flag is honored only on detached/kill paths.) | In observability-procedure.md, scope `done.json` to detached/kill mode and state that for the default inline run the completion signal is the presence of `return-contract.yaml` (already noted at L92). Reconcile the lens JobSpec `on_completion.write_done_sentinel: True` with the inline path actually not emitting it (either wire inline emission, or document the flag as detached-only and stop setting it True on the inline lens spec). |
| 3 | MINOR | `src/superclaude/skills/sc-bare-review/SKILL.md` line 45 | Says the CLI writes `bare-review-NN-<model>.md`; actual file is `bare-review-NN-<model>.final.md` (a `.raw.md` also exists). Cosmetic but an agent globbing `bare-review-*.md` (not `*.final.md`) per SKILL.md would also pick up `.raw.md` siblings. | Correct to `bare-review-NN-<model>.final.md`. |
| 4 | MINOR | Live contract `artifacts:` block + `target.path`/`target.checksum`/`caller.*` in the **lens** path | On the `--lens` CLI path the contract emits empty `artifacts.{manifest_path,state_path,event_log_jsonl,event_log_md,done_sentinel}: ''` and empty `target.path`/`target.checksum` even though those files exist on disk and the per-body frontmatter has the checksum. Under-populated provenance; consumers can't locate sidecars from the contract alone. (Not on the SKILL happy path, so MINOR.) | Populate `artifacts.*` and `target.{path,checksum}` on the lens-driven contract, matching the per-body frontmatter. |

## Cleared hypotheses (adversarial probes that did NOT hold)

- **"Preflight failure exits 0" (would have been CRITICAL):** my first reading showed `EXIT: 0`,
  but that was the exit code of `tail` in a pipe, not the CLI. Re-run without a pipe: IMM-4 and
  env-missing both exit **1** to stderr. SKILL.md's "Non-zero exit → STOP; surface stderr
  verbatim" is correct. CLEARED.
- **"`done.json` is an unwired bug":** the *absence* on inline runs is **intentional and tested**
  (`test_quickstart_does_not_emit_done_sentinel`). The defect is purely the OPS-doc narrative
  (Finding #2), not the code behavior. Downgraded from bug to doc-drift.
- **Legacy-script orphans:** rollback-procedure.md / release-notes-v1.md reference `t2_*.sh` /
  `refs/prompts.md` deliberately (they are rollback/deletion targets); git shows the deletions
  staged and present-at-HEAD-only, consistent with WS-C. No live dangling pointer. CLEARED.

## Self-Audit

1. **Factual claims verified against source/CLI:** 11 live verifications — `swarm --help`,
   `swarm run --help` (×3 flag groups), live stub run (deliverables on disk), live contract dump,
   live normalized-body dump, env-missing run (exit 1), IMM-4 run (exit 1, no pipe), `make
   verify-sync`, env-var grep across SKILL/config.py/env-readiness, `emit_done_sentinel` call-site
   grep (zero), and 4 test-suite runs (62 tests passed).
2. **Files read/inspected:** `SKILL.md`; `tests/swarm/test_bare_review_parity.py`;
   `tests/swarm/test_e2e_user_guide.py`; `tests/swarm/test_done_sentinel.py`;
   `tests/swarm/test_three_layer_artifacts.py`; `src/superclaude/cli/swarm/commands.py` (exit +
   lens-spec regions); `src/superclaude/cli/swarm/config.py`; `src/superclaude/cli/swarm/reduce.py`;
   `src/superclaude/cli/swarm/lenses/bare_review.py`; `docs/swarm/observability-procedure.md`,
   `operator-runbook.md`, `env-readiness.md`, `rollback-procedure.md`; golden fixture tree.
3. **Why trust this found real issues:** I disproved two of my own strongest hypotheses rather
   than confirm them, and the surviving findings are each backed by a direct contradiction between
   an emitted artifact / passing test and a doc claim (contract keys; `done.json` test name).
4. **Web research:** none required (entirely local-file + CLI bound). Tavily not invoked.

## Confidence

- Verified: 7/7 trace steps + 4/4 findings substantiated | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- Tool engagement: Read: 5 | Grep/Bash(grep): ~14 | Bash(CLI/test runs): ~12

## QA Complete
