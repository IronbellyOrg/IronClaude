---
verdict: FAIL
confidence: 0.88
---

# Card 2 — Tests & Contract Adequacy (WS-0 + WS-A)

## Summary

Eight findings across test vacuity, SKILL.md contract divergence, and doc accuracy. The thin-caller migration is structurally sound but the contract YAML in SKILL.md does not match the actual CLI schema, one test guards nothing, and the release notes claim a "single `swarm run --lens bare-review` command" that silently implies `--transport openai_compat` without documenting the flag.

---

## Finding 1 — `test_target_line_cap_and_timeout_flags_accepted` is vacuous

- **severity**: medium
- **file**: `tests/swarm/test_e2e_user_guide.py:186-197`
- **claim**: "B-2 / B-3: `--target-line-cap` and `--timeout-sec` are accepted and the run completes successfully"
- **evidence**: The test asserts only `exit_code == EXIT_OK` (line 196) and that `return-contract.yaml` exists (line 197). The docstring itself admits "their behavioral effect is not observable via the stub stdout." The stub transport ignores both flags — the test proves nothing about truncation or timeout enforcement. It is a usage-surface guard, not a behavioral gate.
- **suggested deviation_class**: `test_vacuous_assertion` — add a second test path using a scripted transport or inspect the manifest's `target.truncation.truncation_line_cap` and `workers.timeout_sec` to prove the values threaded through. The parity test (`test_bare_review_parity.py`) covers this indirectly but the e2e suite should own its own invariants.

## Finding 2 — SKILL.md return contract YAML shape does not match actual `ResultContract`

- **severity**: high
- **file**: `src/superclaude/skills/sc-bare-review/SKILL.md:49-54` vs `src/superclaude/cli/swarm/models.py:997-1015`
- **claim**: SKILL.md line 50 declares `contract_version: "1.0"; status: ...` using semicolon-separated inline YAML syntax; line 51 declares `target: { path: <abs>, checksum: <sha256>, truncated: <bool>, truncation_line_cap: <N> }`; line 52 declares `workers_requested: <N>; workers_succeeded: <M>; workers_failed: <N-M>`; line 54 declares `caller_metadata: { suspect: true, tier: T2 }` as a flat object.
- **evidence**: The actual `ResultContract` dataclass (models.py:997-1015) carries 19 top-level keys including `job_id`, `started`, `finished`, `elapsed_ms`, `caller`, `lens`, `lens_source`, `amalgamation_mode`, `merged_path`, `artifacts` — none of which appear in the SKILL.md contract block. The `target` field is a nested `ContractTarget` dataclass with the right sub-fields (`path`, `checksum`, `truncated`, `truncation_line_cap`) per models.py:1006, but the YAML example's semicolon syntax on line 50 (`contract_version: "1.0"; status: success | partial | failed`) is not valid YAML — it reads as a string value, not a mapping. The `caller_metadata` is correctly a two-field object in both, but `suspect: true` is presented as a constant in SKILL.md when it is actually dynamic (stamped from the lens at preflight, `CallerMetadata` at models.py:1674-1675).
- **suggested deviation_class**: `contract_schema_mismatch` — the SKILL.md contract block should use proper YAML mapping syntax and at minimum note the 19-key shape or explicitly scope the block to "fields relevant to callers" to avoid misleading consumers.

## Finding 3 — `test_quickstart_emits_normalized_artifacts` asserts `"--suspect-source" in contract` but contract is YAML, not the rendered next-command

- **severity**: medium
- **file**: `tests/swarm/test_e2e_user_guide.py:148-151`
- **claim**: Line 151: `assert "--suspect-source" in contract, "bare-review contract must carry the suspect-source next command"`
- **evidence**: The test reads `return-contract.yaml` as a raw text string (line 148-149) and checks substring presence. This works only because `recommended_next_command` is a YAML scalar value containing `--suspect-source`. The assertion is fragile: if the YAML serializer changes quoting style or line wrapping, it still passes; but it would also pass on a false positive if `--suspect-source` appeared in any other field. More importantly, lines 156-157 check that `{suspect_files}` and `{compare_files}` placeholders are NOT present, and line 158 checks `.final.md` IS present — these prove template rendering occurred. This finding is borderline but worth noting: the assertion string-level check on YAML is structurally weaker than parsing and checking `recommended_next_command`.
- **suggested deviation_class**: `brittle_assert` — parse the YAML and assert on `contract["recommended_next_command"]` specifically.

## Finding 4 — `--reviewers=4` test does not prove INV-005 model-pool guard survived

- **severity**: low
- **file**: `tests/swarm/test_e2e_user_guide.py:276-288`
- **claim**: "the value must survive both the (test-only) `count == 4` reset and the INV-005 model-pool guard, proving it reached the post-expansion spec"
- **evidence**: The test asserts `exit_code == EXIT_OK` (line 285), `dispatched job (mode=lens, workers=4, results=4) in result.output` (line 286), and `manifest["preflight"]["workers_requested"] == 4` (line 288). These prove the flag value reached the manifest and the stdout dispatch line, but the INV-005 model-pool guard is about matching `workers.count` to `len(workers.models)` — the test does not verify that the manifest's `workers.models` array has exactly 4 entries. With the stub transport, the pool is padded to match regardless of actual configured models. The INV-005 guard is tested in the parity suite (`test_bare_review_parity.py`) but not in the e2e guide.
- **suggested deviation_class**: `incomplete_invariant_coverage` — add an assertion on `manifest["preflight"]["pool_size"]` or equivalent to prove the model-pool resizing occurred.

## Finding 5 — SKILL.md `--transport openai_compat` invocation block claims preflight env vars but does not document the flag in the SKILL's own flag surface

- **severity**: medium
- **file**: `src/superclaude/skills/sc-bare-review/SKILL.md:29-38`
- **claim**: Line 29-32 lists flags: `--target`, `--output`, `--reviewers`, `--target-line-cap`, `--timeout-sec`, `--label`, `--c7*`. Line 32-33 mentions `--transport openai_compat` in prose ("For `--transport openai_compat` the swarm preflight requires...") but `--transport` is NOT listed as a SKILL.md boundary flag. The invocation block (line 35-38) includes `--transport openai_compat` on the command line.
- **evidence**: The swarm CLI's `--transport` flag defaults to `stub` (per `swarm run --help`), and `openai_compat` is the production default per FR-022. The SKILL.md invocation block (lines 35-38) hardcodes `--transport openai_compat` but does not declare `--transport` as a caller flag. If a caller omits `--transport`, the swarm CLI will default to `stub` (hermetic dry-run) — which is NOT what the SKILL.md intends. Conversely, the SKILL.md says `--c7*` are "accepted at the skill boundary but are a no-op, NOT forwarded to swarm run" (line 31-32) but the CLI `swarm run` has no `--c7*` flags, so this claim is vacuously true but misleading — it implies a forwarding relationship that does not exist.
- **suggested deviation_class**: `flag_documentation_gap` — SKILL.md should either (a) list `--transport` as a caller flag with the production default `openai_compat`, or (b) the invocation block should omit `--transport openai_compat` and instead document that the swarm CLI defaults require explicit override for production.

## Finding 6 — AC-1.5 "single-message parallel dispatch" guarantee dropped from SKILL.md

- **severity**: low
- **file**: `src/superclaude/skills/sc-bare-review/SKILL.md` (new, 80 lines) vs old SKILL.md (Wave C, lines ~110-130 of the 231-line version)
- **claim**: The old SKILL.md had a mandatory structural assertion (AC-1.5 / IMM-3) requiring the Claude agent to emit exactly N `Bash` tool calls in ONE single message for parallel dispatch. This is gone from the new 80-line version.
- **evidence**: The new SKILL.md line 43-44 states "The CLI fans out the N reviewers internally (no manual single-message dispatch)". This is legitimate — the CLI owns fan-out now via `dispatch_wave1`, not the skill. The old AC-1.5 was an agent-behavioral constraint that only mattered when the skill orchestrated Bash calls directly. Dropping it is correct because the Claude agent no longer dispatches reviewers. However, the old SKILL.md's "allowed-tools" header listed `Read, Glob, Grep, Bash, Write` while the new lists only `Read, Bash` (SKILL.md line 4). The removed tools (`Glob`, `Grep`, `Write`) are no longer needed for orchestration, which is correct.
- **suggested deviation_class**: `legitimate_removal` — not a defect, but the old AC-1.5 acceptance criterion (AC-1.5 in old SKILL.md acceptance list) should be removed from the acceptance pointers if it still references single-message dispatch. Checking SKILL.md line 74-76: the acceptance pointers now say "AC-1.1..1.12 ... are enforced by the swarm CLI" — this correctly re-attributes enforcement.

## Finding 7 — Release notes claim skill invocation is "unchanged" but the invocation mechanism fundamentally changed

- **severity**: medium
- **file**: `docs/swarm/release-notes-v1.md:29-34`
- **claim**: "Skill invocation shape from caller pipelines (`/sc:troubleshoot`, `/sc:reflect`, `/sc:auggie-review`, `/sc:code-review`, `/sc:adversarial`) is unchanged."
- **evidence**: While the flag surface is preserved, the invocation mechanism changed from `Skill sc-bare-review --target ...` (which triggered a multi-wave Bash orchestration) to the thin caller invoking `superclaude swarm run --lens bare-review` via Bash. Caller pipelines that previously did `Skill sc-bare-review ...` must now invoke `Bash` with the swarm CLI command. The "shape" (flags) is preserved, but the "invocation mechanism" (skill dispatch vs Bash CLI call) is fundamentally different. The release notes conflate "flag surface" with "invocation shape." Lines 29-32 correctly say "The skill's user-facing flag surface ... is preserved" but line 33's "invocation shape ... is unchanged" is misleading — callers that scripted `Skill sc-bare-review` must now script `Bash` with the swarm CLI.
- **suggested deviation_class**: `doc_accuracy_issue` — rephrase line 33 to "Caller flag surface ... is unchanged; callers must now invoke via `Bash` with `superclaude swarm run --lens bare-review` instead of the `Skill sc-bare-review` delegation."

## Finding 8 — SKILL.md invocation block hardcodes `--transport openai_compat` but SKILL.md line 33 says `--transport stub` is a hermetic dry run

- **severity**: low
- **file**: `src/superclaude/skills/sc-bare-review/SKILL.md:32-38`
- **claim**: Line 32-33: "For `--transport openai_compat` the swarm preflight requires `T2ProxyUrl`/`T2ProxyKey`/`T2Model0N` and STOPs naming any missing var; `--transport stub` is a hermetic dry run." The invocation block (lines 35-38) hardcodes `--transport openai_compat`.
- **evidence**: This is not contradictory but is worth noting: the SKILL.md shows the production invocation (with `openai_compat`) as the canonical example, but does not show the test/staging invocation (with `--transport stub`). Callers reading only the invocation block will try `openai_compat` and fail if env vars are unset. The old SKILL.md had separate "Prerequisites" (env vars) and "Behavioral Protocol" sections that made the distinction clearer. The new SKILL.md collapses these together.
- **suggested deviation_class**: `doc_clarity` — add a `--transport stub` example alongside the production one.

---

## Verification checklist (what I verified, not just asserted)

1. `tests/swarm/test_e2e_user_guide.py` — Read all 440 lines. Each test's assertions examined against claimed behavior.
2. `src/superclaude/skills/sc-bare-review/SKILL.md` — Read current 80-line version. Contract YAML block (lines 49-56) compared against actual `ResultContract` dataclass at `src/superclaude/cli/swarm/models.py:997-1015`.
3. Old 231-line SKILL.md retrieved via `git show 0f9c8d36:src/superclaude/skills/sc-bare-review/SKILL.md`. AC-1.5 single-message dispatch (old Wave C) confirmed dropped and legitimately so.
4. `docs/swarm/release-notes-v1.md` — Read all 361 lines. Claim at lines 29-34 ("invocation shape ... unchanged") evaluated against the actual invocation mechanism change.
5. `swarm run --help` — Verified all flags the SKILL.md claims are present on the CLI: `--target`, `--output`, `--reviewers`, `--target-line-cap`, `--timeout-sec`, `--label` all confirmed. `--transport` confirmed as a CLI flag but NOT documented as a SKILL boundary flag.
6. `src/superclaude/cli/swarm/lenses/bare_review.py` — Read 76 lines. `recommended_next_command_template` at line 65-68 confirmed carrying `--suspect-source` and `{suspect_files}`/`{compare_files}` placeholders.
7. `src/superclaude/cli/swarm/reduce.py` — Contract emission at lines 699-724 confirmed: `ResultContract` construction matches the 19-key dataclass, not the 8-field SKILL.md YAML block.
8. `src/superclaude/cli/swarm/preflight.py:1082-1122` — Failure contract (env-missing path) confirmed carrying the full 19-key envelope, not just the SKILL.md's claimed fields.
