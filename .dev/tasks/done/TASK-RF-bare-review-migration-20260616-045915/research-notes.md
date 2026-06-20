# Research Notes: sc-bare-review M8/M9 migration completion

**Date:** 2026-06-16
**Scenario:** A (explicit — BUILD_REQUEST carries verified facts + paths + 5 work-streams)
**Depth Tier:** Deep
**Track Count:** 1 (WS-A→B→C sequentially dependent; shared sc-bare-review/swarm context)

---

## EXISTING_FILES

- `src/superclaude/skills/sc-bare-review/SKILL.md` — **231 lines**, legacy script orchestrator (refs scripts at L35-36, 89, 113, 127). TARGET of WS-A rewrite → ~60-line thin caller.
- `src/superclaude/skills/sc-bare-review/scripts/t2_preflight.sh` (9976 B), `t2_dispatch.sh` (5068 B), `t2_normalize.py` (10429 B) — the 3 legacy scripts to retire (WS-C). Present → legacy golden baseline capturable. (NOTE: under the SKILL dir, NOT repo-root `scripts/`.)
- `src/superclaude/cli/swarm/commands.py` — `run_cmd` + `--lens` option (L1199-1213); `superclaude swarm run --lens bare-review` is the thin-caller target (FR-020 shortcut).
- `src/superclaude/cli/swarm/lenses/bare_review.py` — `bare-review` LensEntry (recipe_name="bare-review-v1", 3 workers, suspect:true, T2, §11.5 guard).
- `src/superclaude/cli/swarm/lenses/__init__.py` — LENSES registry (8 entries incl. "bare-review").
- `src/superclaude/cli/swarm/recipes/bare_review_v1.py` — the recipe backing the lens.
- `tests/swarm/test_bare_review_parity.py` — parity gate, docstring-scoped "T08.11"; compares LIBRARY surfaces not CLI end-to-end; `skipif(LEGACY_SCRIPT.exists())` currently FALSE (17 passed). TARGET of WS-B rebuild.
- `docs/swarm/` — existing: command-reference, lens-catalog, monitoring-patterns, oq-resolutions, README, release-notes-v1, runbook, transport-limits, user-guide. `release-notes-v1.md` FALSELY claims thin-caller shipped (L16-25).
- `docs/dev/lens-contribution-policy.md` — ALREADY EXISTS (T02.27). WS-D item is relocate/reference, not net-new.
- `.dev/releases/complete/MultiModelSwarm/tasklist/phase-8-cp1.md`, `phase-8-cp2.md` — false attestations (WS-E). NOTE: under `complete/`, currently git-untracked.
- Evidence REPORTs: `.dev/reflect/mms-phase-8-postaudit/REPORT.md`, `.dev/reflect/mms-phase-9-postaudit/REPORT.md`, `.dev/reflect/mms-postaudit-SUMMARY.md`.
- Spec: `.dev/releases/complete/MultiModelSwarm/merged-requirements.compressed.md` (Migration §16 steps 8+9 at ~L688-703).

## PATTERNS_AND_CONVENTIONS

- **Source-of-truth + sync:** edit `src/superclaude/skills/…` then `make sync-dev`; pre-commit `scripts/precommit_verify_bare_review_sync.sh` (MIG-001, `.pre-commit-config.yaml:112-124`) requires src↔`.claude/` parity on any `src/superclaude/skills/sc-bare-review/` change. NEVER stage `.claude/`.
- **UV-only** Python (`uv run …`); no bare python/pip.
- **No Anthropic SDK** in swarm transports; T2 proxy env per `~/.aienv` only.
- **Lens shortcut** expands FR-020 defaults into a full JobSpec → preflight-valid without a spec file.
- Swarm tests live in `tests/swarm/`, pytest; `make verify-sync` gates component parity; `uv run pytest tests/swarm/` is the suite.

## GAPS_AND_QUESTIONS

- Exact thin-caller shape: how does the legacy skill's option surface (--reviewers/--target-line-cap/--timeout-sec/--label) map onto `swarm run --lens` flags? (commands.py option names need confirming by researcher.)
- A/B parity design: the legacy side disappears at WS-C. Need a frozen golden-baseline strategy (run legacy scripts on a fixed fixture pre-deletion; permanent gate = CLI vs frozen golden). Confirm determinism (stub transport vs proxy).
- OPS doc reconciliation: operator-runbook vs existing runbook.md; observability-procedure vs monitoring-patterns.md; lens-contribution-policy already at docs/dev/.
- `swarm_env_readiness.sh` home: scripts/ vs docs/swarm/ — confirm project convention.

## RECOMMENDED_OUTPUTS

- `research/01-skill-and-scripts-inventory.md` — File Inventory: SKILL.md structure, the 3 scripts' arg surfaces, what each Wave does.
- `research/02-swarm-cli-thin-caller-surface.md` — Integration Points: `swarm run --lens` full flag surface + how legacy options map; confirm `--reviewers/--target-line-cap/--timeout-sec/--label/--transport`.
- `research/03-parity-test-and-swarm-test-conventions.md` — Test & Verification: current parity test internals, swarm test patterns, fixtures, how to drive the CLI subprocess deterministically; golden-baseline approach.
- `research/04-docs-and-release-notes-staleness.md` — Doc Cross-Validator: docs/swarm inventory, release-notes-v1 false claims, OPS-doc overlaps, lens-contribution-policy location.
- `research/05-mdtm-template-and-sync-discipline.md` — Template & Examples: MDTM template 02 rules; sync-dev/verify-sync/MIG-001 hook mechanics; prior MMS phase tasklists as examples.

## SUGGESTED_PHASES

- R1 (File Inventory) → `01-…`: SKILL.md + 3 scripts under `src/superclaude/skills/sc-bare-review/`. Other researchers cover CLI/tests/docs/template.
- R2 (Integration Points) → `02-…`: `src/superclaude/cli/swarm/commands.py` run_cmd/--lens, lenses/bare_review.py, recipes/bare_review_v1.py.
- R3 (Test & Verification) → `03-…`: `tests/swarm/test_bare_review_parity.py` + tests/swarm conventions + CLI-subprocess test patterns.
- R4 (Doc Cross-Validator) → `04-…`: `docs/swarm/*` + `docs/dev/lens-contribution-policy.md`; tag CODE-VERIFIED/CONTRADICTED/UNVERIFIED.
- R5 (Template & Examples) → `05-…`: `.claude/templates/workflow/02_mdtm_template_complex_task.md` + `.pre-commit-config.yaml` MIG-001 + prior `.dev/releases/complete/MultiModelSwarm/tasklist/phase-8-tasklist.md`.

## TEMPLATE_NOTES

- Template 02 (complex) — discovery + build + test + retire + docs + verification + reflect phases. Tier Deep. QA_GATE_REQUIREMENTS: PER_PHASE. TESTING_REQUIREMENTS: UNIT+INTEGRATION (parity gate is integration via CLI subprocess). VALIDATION: `make sync-dev` + `make verify-sync` + `uv run pytest tests/swarm/`.
- STRICT compliance per work-stream: WS-A/B/C STRICT (skill exec path + script deletion + parity gate); WS-D STANDARD; WS-E LIGHT (archived attestations).
- Sequencing: WS-A → WS-B (capture legacy golden while scripts exist) → parity green → WS-C; WS-D/WS-E parallel.

## AMBIGUITIES_FOR_USER

None blocking — intent is clear from the BUILD_REQUEST + two post-audit REPORTs. Design choices (golden-baseline mechanism, OPS-doc reconciliation, env-readiness script home) are resolvable from codebase conventions by the researchers; any residual goes to the task file's Open Questions.
