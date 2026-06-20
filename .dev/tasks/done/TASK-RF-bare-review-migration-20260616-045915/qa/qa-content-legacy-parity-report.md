# QA Report — task-qualitative (legacy-parity-faithfulness lens)

**Topic:** WS-0 inline-path Wave 1→2→3 migration for `swarm run --lens bare-review`
**Date:** 2026-06-16
**Phase:** task-qualitative (legacy-parity lens)
**Fix cycle:** N/A (`fix_authorization: false` — REPORT ONLY)
**Lens:** legacy-parity-faithfulness (does WS-0 preserve `t2_preflight.sh` / `t2_dispatch.sh` / `t2_normalize.py` legacy semantics?)
**Diff baseline:** `02582ca03ea5a974f4dbab35d9b9cd0033217aca` → working tree

---

## Overall Verdict: FAIL

WS-0 correctly wires the inline (non-`--resume`) path through Wave 1→2→3 and the four
flag claims (#1–#4) are faithfully threaded, BUT live runtime inspection surfaces **two
genuine legacy-parity DRIFTS** (one IMPORTANT, one MINOR) plus three documented narrowings.
The headline drift is in claim #5: the emitted `recommended_next_command` carries
**unsubstituted `{compare_files}` / `{suspect_files}` placeholders** where legacy
`t2_normalize.py:292-295` emits a fully-populated, copy-pasteable command. The literal
`--suspect-source` substring is present (claim #5 as worded passes), but the legacy
*actionable-command* behavior is NOT reproduced.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | `--reviewers` [2,4]/default-3/≤model-count | none | PASS | Live `--reviewers 4` → 4 workers + manifest `workers_requested:4`; `--reviewers 5` → EXIT_USAGE; range guard at commands.py:1640-1647 matches legacy AC-1.4 (t2_preflight.sh:50). Default-3 from lens `default_workers=3` (bare_review.py:61). |
| 2 | `--target-line-cap` default 4000 | none | PASS | Lens `default_target_line_cap=4000` (bare_review.py:62) == legacy `LINE_CAP=4000` (t2_preflight.sh:25). Override threads to `target.truncation.line_cap` (commands.py:1658-1660). |
| 3 | `--timeout-sec` default 180 | none | PASS | Help text + threading correct; legacy default `T2Timeout:-180` (t2_preflight.sh:74). Threaded to `workers.timeout_sec` + `dispatch_wave1(worker_spec=...)` (commands.py:1668-1670, 1785-1791). |
| 4 | `--label` stamped onto frontmatter | none | PASS | Live `--label my-caller-ctx` → frontmatter `caller_label: "my-caller-ctx"` in every body. Recipe reads `args.get("caller_label")` (bare_review_v1.py:255). |
| 5 | IMM-5 success-first / suspect:true / `--suspect-source` next-cmd | AX-1 | FAIL | suspect:true ✓ (contract `caller_metadata.suspect:true` + frontmatter); status:success with M==N==3 ✓; BUT next-cmd = `--suspect-source {suspect_files}` UNSUBSTITUTED vs legacy populated paths. DRIFT. |

<!-- AX-1 (drift): the cited legacy behavior (populated next-cmd) has drifted to an
unsubstituted-placeholder string on the WS-0 inline path. -->

## Summary
- Checks passed: 4 / 5
- Checks failed: 1 (claim #5 — legacy-parity drift in `recommended_next_command`)
- Issues found: 2 (1 IMPORTANT, 1 MINOR) + 3 documented narrowings (informational)
- Issues fixed in-place: 0 (report-only)
- drift-axis baseline: BUILD_REQUEST.GOAL not supplied verbatim in spawn prompt; the legacy
  contract (research 01 + t2_preflight.sh source) served as the parity baseline. AX-1 applied
  against legacy source, not BUILD_REQUEST.GOAL.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | commands.py:1844-1860 (reduce_wave3 call) + lens expansion commands.py:859 | **`recommended_next_command` placeholders are NOT substituted.** Legacy `t2_normalize.py:292-295` derives `compare`/`suspect` from the actual succeeded `final_path`s and emits `/sc:adversarial --compare <existing-review>,<p1>,<p2> --suspect-source <p1>,<p2>` — a copy-pasteable command. WS-0 passes `inline_job.recommended_next_command_substitutions`, which for a `--lens` shortcut is `{}` (commands.py:859), and `_render_recommended_next_command` (reduce.py:467-486) leaves unknown keys verbatim. Live contract emits the literal `--suspect-source {suspect_files}`. The hand-off chain to `/sc:adversarial --suspect-source` (the entire point of the bare-review identity, SKILL.md §3.3) is broken — a caller pasting this command gets a literal `{suspect_files}` token. | Before the `reduce_wave3` call, build a substitutions dict from the stamped/normalized workers' `final_path`s (mirror legacy: `suspect_files = ",".join(succeeded_final_paths)`, `compare_files = ",".join(["<existing-review>", *succeeded_final_paths])`) and pass it as `recommended_next_command_substitutions`. This applies to BOTH the inline and resume branches (the resume branch shares the empty-`{}` defect). |
| 2 | MINOR | commands.py:1828-1832 (recipe_args) + bare_review_v1.py:253-254,298-299 | **Per-reviewer `reviewer_model_id` / `reviewer_model_label` frontmatter is empty** because `normalize_wave2` forwards ONE uniform `recipe_args` dict to every worker and that dict carries no `model_id`. Live frontmatter shows `reviewer_model_id: ""` on all bodies. Legacy `t2_normalize.py` stamps each `bare-review-NN-<model>.md` with its own per-reviewer `model_id` from the manifest's `reviewers[]` entry. Under `--transport stub` this is cosmetic; under a real multi-model `openai_compat` transport the per-reviewer model attribution is LOST in the body frontmatter (the contract `output_files[].model_id` still carries it, but the on-disk body does not). The WS-0 comment at commands.py:1830-1831 acknowledges this ("per-worker model_id is uniform on the single-model stub / parity path") — but the legacy contract was per-reviewer, not uniform. | Thread per-worker `model_id`/`model_label` into normalize_wave2 (either per-worker recipe_args or have normalize_wave2 read them from each `WorkerResult.model_id`/`model_label`), so multi-model runs stamp distinct reviewer models into each body's frontmatter. Verify against a non-stub transport before closing. |

## Documented Narrowings (informational — not parity-breaking, consistent with research G-6)
1. **`≤ model-count` ceiling removed.** Legacy (t2_preflight.sh:70-71) dies when `--reviewers N` exceeds the number of resolvable `T2Model0N` env vars. WS-0's `--reviewers` handler (commands.py:1648-1650) synthesizes `workers.models = ["lens-default-model-{i}" for i in range(N)]`, so the INV-005 `workers_exceed_pool` guard can never trip. The static `[2,4]` clamp subsumes the legacy default 4-model roster ceiling, so for the default config the outcome is identical. Research G-6 (line 195) explicitly accepts "at minimum keep the static [2,4] clamp." Acceptable, but the dynamic env-driven ceiling is gone.
2. **`target_checksum` is 64-hex, not 12-hex.** Legacy t2_preflight.sh:101 uses `cut -c1-12` (12-hex, AC-1.10). Swarm preflight.py:1381 emits full `hashlib.sha256(...).hexdigest()` (64-hex; live body confirmed `6dc0eac0...c156`). This is a pre-existing swarm-preflight property NOT introduced by the WS-0 diff (WS-0 threads `preflight_result.manifest.preflight.target_checksum` verbatim), but it IS a documented legacy-contract divergence the migration should call out. Out of WS-0 fix scope; flag for the SKILL.md contract doc.
3. **IMM-4 empty-target writes no `failed` contract on the inline path.** Legacy (t2_preflight.sh:104-124) writes a `failed`/`target-too-small` `return-contract.yaml` THEN exits 3. The swarm path emits a structured `imm4.target_too_small` rule block on stderr and exits before dispatch — no `return-contract.yaml` is written (live-confirmed: no contract in the empty-target output dir). This is preflight behavior, upstream of the WS-0 pipeline wiring (WS-0 only runs after preflight passes), so out of WS-0 fix scope — but it is a write-on-failure parity gap vs the legacy §8 "contract written on every invocation" guarantee.

## Per-claim disposition (the 5 verification targets)
1. `--reviewers` — **PASS.** [2,4] enforced (5→EXIT_USAGE live), default 3, override reaches post-expansion spec (4 workers dispatched). `≤model-count` narrowed (see Narrowing #1).
2. `--target-line-cap` default 4000 — **PASS.** Matches legacy verbatim.
3. `--timeout-sec` default 180 / T2Timeout — **PASS.** Default + threading to dispatch worker_spec correct.
4. `--label` frontmatter stamp — **PASS.** Live frontmatter `caller_label` populated; recipe reads it. (Note: contract `caller.invocation_label` stayed `''` even with `--label` set — the label reaches the body via `recipe_args.caller_label` but not the contract's caller block; legacy contract schema has no `invocation_label` field, so this is not a parity break, just an internal inconsistency in the new contract surface.)
5. IMM-5 / suspect:true / `--suspect-source` — **PARTIAL→FAIL.** IMM-5 success-first ✓ (M==N==3→success; reduce.py:284-290 matches legacy t2_normalize.py:284-290 verbatim). suspect:true ✓ everywhere. `--suspect-source` literal substring present ✓ BUT command is non-actionable (unsubstituted placeholders) — Issue #1.

## Actions Taken
None — `fix_authorization: false`. All findings documented for the builder.

## Self-Audit
This is a task-qualitative parity review, not an Inherited-Structural-Verdict consumer run
(no `## Inherited Structural Verdict` block in the spawn prompt), so the reliance audit is N/A;
all verification was independent tool engagement.

**(a) Reliance list — items taken from research without independent re-check:** none. Every
research claim (legacy 4000 line-cap, [2,4] AC-1.4, 180s timeout, ≤model-count, 12-hex checksum)
was re-verified against `t2_preflight.sh` / `t2_normalize.py` source directly.

**(b) Independent semantic checks (tool evidence):**
- Legacy defaults — Read t2_preflight.sh:25,49-50,70-71,74,101 (12-hex checksum, [2,4], ≤model-count, 180s).
- Legacy next-cmd — Read t2_normalize.py:292-295 (populated `compare`/`suspect`); IMM-5 at 284-290.
- WS-0 threading — Read/grep commands.py:1640-1682,1801-1802 (flag handlers + dispatch).
- Substitution renderer — grep reduce.py:467-486 (`_Defaults.__missing__` passes placeholders verbatim).
- **Runtime** — 3 live `swarm run --lens bare-review --transport stub` invocations (default, `--label`+`--reviewers 4`, empty-target). Inspected emitted `return-contract.yaml` + per-reviewer `.final.md` bodies. This caught Issue #1 (unsubstituted placeholders) and Issue #2 (empty reviewer_model_id) that static reading alone would have missed.
- Test validity — ran `pytest tests/swarm/test_e2e_user_guide.py` (20 passed); confirmed the new presence test asserts only the `--suspect-source` substring (AX-4 weakened-criteria: it passes against the unsubstituted placeholder, so it does NOT guard against Issue #1).

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 6 | Grep: 6 | Glob: 0 | Bash: 8

If I claimed 0 issues, the user should NOT believe it — and indeed I found 2. The runtime
inspection (not the diff read) is what surfaced both; a purely structural pass over the diff
(which looks clean and well-commented) would have rated this PASS. That gap is exactly why the
adversarial "assume ≥10 divergences" stance + a live run mattered.

## Recommendations
1. **Fix Issue #1 (IMPORTANT) before merge** — populate `recommended_next_command_substitutions` from the succeeded workers' `final_path`s in BOTH the inline and resume `reduce_wave3` calls. This is the bare-review skill's whole output contract (hand-off to `/sc:adversarial --suspect-source <files>`); shipping unsubstituted placeholders defeats the migration's purpose.
2. **Fix or explicitly accept Issue #2 (MINOR)** — decide whether per-reviewer `reviewer_model_id` in body frontmatter is a parity requirement; if so, thread per-worker model ids through normalize_wave2 and re-verify under `openai_compat`.
3. **Document the 3 narrowings** in the migrated SKILL.md contract section so callers know the 64-hex checksum, the removed env-driven model-count ceiling, and the IMM-4 no-contract-on-the-inline-path behaviors are intentional divergences.
4. **Strengthen the new e2e test** — `test_quickstart_emits_normalized_artifacts` should assert the next-command is actionable (e.g., `assert "{suspect_files}" not in contract` and that an actual `.final.md` path appears after `--suspect-source`), not merely that the `--suspect-source` substring exists.

## QA Complete
