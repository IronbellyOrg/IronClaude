# P2 fifth review: verification of the fourth-review fixes (issue #323)

Reviewer: independent adversarial verification, read-only, 2026-10-29. Deliverables (under `.dev/codegraph-migration/`):
- A = `specs/phase-2-codegraph-install-spec.md` (734 lines)
- B = `handoff/coder-handoff-prompt.md` (79 lines)
- C = `handoff/coder-handoff-context.md` (139 lines)
- P = `decisions/P2-indexing-sync/probe-results.md` (25 lines)
- DF = `decisions/P2-serena-entry-removal/adversarial/P2-serena-entry-removal-merged.md` (49 lines)

Input: `decisions/P2-review/fourth-review-report.md` §1 (partly-fixed third-review findings 1, 3, 12, 14) and §2 (new findings 1-11).

## Verdict: FAIL

- 15 items: 14 FIXED, 1 PARTLY (third-review finding 3), 0 NOT.
- New findings: 4 (0 CRITICAL, 0 IMPORTANT, 4 MINOR). All four are wording and traceability defects introduced by this round's edits.
- The layer-2 script still passes `bash -n`. The new T0b, T7 and merge-gate lines also pass `bash -n`. The §1 table is valid. The guidance block and the two acceptance `jq` checks are byte-equal between A and C.

## 1. Status of the 15 items

| # | Item | Status | Evidence | Remaining fix (PARTLY only) |
|---|---|---|---|---|
| 1 | Third-review 1: DF still said "no env or headers" | FIXED | DF:5 header: "Amended by Phase 2 spec D23 (§2.12) … `env`/`headers` match when absent **or `{}`** … Where this record differs, the spec wins". DF:12 is superseded by that header. | |
| 2 | Third-review 3: T0b acceptance passed on one mention | PARTLY | A:437 now requires `test "$(rg -c 'codegraph_ready' …phase-1-removal-spec.md)" -ge 7`. Today the count is 0, so the check is not vacuous. But nothing checks the Tier R amendment, the CRITICAL-derived one. A:434 lists "§3.2 … Tier R 'env/headers absent or `{}`'", and A:190 says "Phase 1's Tier R `serena` rows get the same 'absent or `{}`' wording (… T0b)". Phase 1's Tier R line today reads "no `env`/`headers`" (`phase-1-removal-spec.md:315`). That change need not contain `codegraph_ready`, so the count check cannot see it. The fourth review asked for "plus `rg -q 'absent or .\{\}.'` on the Tier R line". | Add to T0b's acceptance: ``rg -q 'Tier R.*absent or .\{\}' .dev/codegraph-migration/specs/phase-1-removal-spec.md`` (fails today, as it should). |
| 3 | Third-review 12: B:79 and DF:33 used the old combined `jq` | FIXED | B:79 now says "the user-scope and local-scope `jq` checks in the context file §2.4 exit 0". C:67 holds both checks with the local-scope note ("a failure means run the printed `claude mcp remove <name> --scope local`"). C's two expressions are byte-equal to A:205 and A:206 (`diff` empty). The old DF:35 check is superseded by DF:5 ("acceptance is the two `jq` checks in spec §2.12"). | |
| 4 | Third-review 14: "never left with neither" overstated | FIXED | D22 (A:715): "gating on codegraph readiness never removes the current-pin Serena entry while codegraph is missing". B:14: "If codegraph is not ready it keeps the current-pin Serena entry". DF:5 narrows DF:14. `grep -i neither` on A, B and C finds only unrelated uses (A:209 residual risk, A:237, A:303, A:670, A:732). | |
| 5 | New 1: DF not marked superseded | FIXED | DF:5 covers all four points from the fourth review: `{}`, the predicate, the "neither" wording and the acceptance. It also adds shape matching and the `startup.sh` location. Traceability gap: new finding 3. | |
| 6 | New 2: T3b tested doctor before T4; output undefined | FIXED | T3b (A:505): "`install` and `install --list` call the same `codegraph_ready()` (doctor's use is tested in T4)". T4 (A:516) adds the shared-function test. The output line `Ready for Serena retirement: yes \| no (<reason>)` is defined in §2.7 (A:125) and §2.8 (A:137). | |
| 7 | New 3: layer-2 run point said "after T4" | FIXED | A:316 says "after task T5". A:401 says "commit T5 first (steps 6-6b need T3b's retire gate and T5's hook)". No "after task T4" remains. | |
| 8 | New 4: C's §3.4 copy lacked the first-minute sentence | FIXED | `diff` of A:259 against C:57 is empty. | |
| 9 | New 5: §3.1 row used the old hook condition | FIXED | A:224: "`.codegraph/codegraph.db` may already exist (hook exits) or not yet (a second `init` starts; harmless, probes 2-3)". | |
| 10 | New 6: probe header, TR source, row order, C "rows 1-10" | FIXED | P:3 now reads "P2 and RR probes ran in the W4 sandbox" and defines "TR = the third review (… §4), which used its own `/tmp/p2-third-review.*` sandbox". Rows run 1-12 in order (P:7-18). C:49 and A:213 both say "rows 1-12". | |
| 11 | New 7: T7 and T9 missing the promised checks | FIXED | T7 (A:563): `! rg -n 'Legacy Serena registration kept' CHANGELOG.md \|\| … \| rg -q 'codegraph'`. T9 Change (A:579) records process-group survival inside Claude Code, or "UNVERIFIED". The A:441 description no longer matches the T7 line: new finding 2. | |
| 12 | New 8: merge gate vs. Coder migration location | FIXED | Both suggested fixes were applied. (a) The migration is placed in `T/scripts/startup.sh`, "not in the bundle `install.sh`", in A:679 (§8 step 2), B:48, C:66 and DF:5/DF:19. (b) The gate is now behavioural: `! grep -E '^SERENA_PIN=\|uv tool install .*serena-agent'` (A:617; B:49 matches). A read-only fetch of today's Coder bundle matches at lines 19 (`SERENA_PIN=1.7.0`) and 161 (`uv tool install … "serena-agent==${SERENA_PIN}"`), so the gate is not vacuous today. A migration that lives in `startup.sh` cannot trip it. | |
| 13 | New 9: layer-2 step 6 could pass without testing | FIXED | The AND-list is split: `jq … > "$S/seed.json"` (A:370) and `cp …` (A:371) are separate lines. A seeding assertion follows (A:372: `jq -e '.mcpServers \| has("serena") and has("codebase-memory-mcp")'`). The printed removed argv is asserted (A:379: `grep -F 'serena-agent==1.7.0'`). Together with A:375 (Serena absent), a "kept" line that prints the argv cannot satisfy the step. | |
| 14 | New 10: §1 table broken (blank line, F19 before F18) | FIXED | A:31-51 has no blank line. F18 (A:50) comes before F19 (A:51). Every row has 5 unescaped pipes, the same as the header (mechanical count, `\|` removed first). | |
| 15 | New 11: match set unstated; acceptance assumes shape; T3b non-`serena` case; T0b `Change:` label | FIXED | A:190: "every user-scope entry other than `serena-local`, matched by shape rather than by key name, whose args contain `start-mcp-server` …, stdio, `env` and `headers` each absent or `{}`". A:205 adds the "reported as kept … runs the printed command" note. T3b (A:505) adds the `foo` case. T0b has `Change:` (A:433). C:65 and DF:5 agree. Wording drift and a syntax slip in that sentence: new findings 1 and 4. | |

## 2. New findings (introduced by this round's edits)

1. **MINOR. A:190 has an unbalanced parenthesis, and the rewritten sentence no longer parses.**
   - Location: A:190.
   - Evidence: the line has 3 `(` and 4 `)`. After "each **absent or `{}`**; Coder's bundle and `claude mcp add` write `"env":{}`, and the live entry on this workspace has it, third review finding 1)" the final `)` has no opening partner. The opening `(` was lost when the match-set clause was rewritten. A reader cannot tell where the match condition ends and the justification begins. This is the normative rule sentence.
   - Fix: "…stdio, `env` and `headers` each **absent or `{}`** (Coder's bundle and `claude mcp add` write `"env":{}`, and the live entry on this workspace has it; third review finding 1), and the kind-B …".

2. **MINOR. The A:441 cross-reference describes a different check from the one T7 now runs.**
   - Location: A:441 against A:563.
   - Evidence:
     - A:441 says T7 checks "`! rg -n 'Serena registration kept' CHANGELOG.md` or the line names `serena-local`/codegraph".
     - T7 (A:563) greps the narrower `'Legacy Serena registration kept'` and accepts only `codegraph`, not `serena-local`.
     - The two texts disagree on both the pattern and the escape condition. An executor following A:441 would write a different, broader check.
   - Fix: change A:441's parenthetical to quote the A:563 line, or point at it ("see T7's last acceptance line").

3. **MINOR. DF:5 attributes changes to D23 that D23 does not record.**
   - Location: DF:5 against A:716 (D23). No decision row was added for the fourth-review fixes.
   - Evidence:
     - DF:5 says "Amended by Phase 2 spec D23 (§2.12)" and lists five changes: shape matching under any name except `serena-local`, the narrowed "neither" claim, the two-check acceptance, the `startup.sh` location, and the predicate.
     - D23's text and rationale cite only `third-review-report.md` §2. It lists `{}`, the `.codegraph/codegraph.db` key, `.gitignore`, T0b, the bundle gate and the predicate. It records none of the fourth-review decisions.
     - The Decisions table ends at D23, so the shape-match rule, the migration location and the behavioural merge gate have no decision row.
   - Fix: add a D24 row ("Fourth-review fixes: shape-based Serena match set; Coder migration in `T/scripts/startup.sh`; behavioural bundle gate; split two-scope acceptance"; method self; source `fourth-review-report.md` §2). Then change DF:5 to "Amended by Phase 2 spec D23 and D24 (§2.12)".

4. **MINOR. The match-rule wording drifts between A, B and C.**
   - Location: B:14; A:190 (last sentences).
   - Evidence:
     - B:14 states the rule as "matched by `start-mcp-server` in its args under any name except `serena-local`, `env`/`headers` absent or `{}`". It omits "stdio", which A:190, C:65 and the DF:5 header all include.
     - A:190 says the rule matches "by shape rather than by key name". It then says "A `serena` entry with a non-empty `env` or `headers` is kept and reported", which is keyed by name. It does not say whether a renamed launcher (for example `foo`) with non-empty `env` is also reported, although T3b (A:505) tests "non-empty `env` or `headers` … kept" without naming a key.
   - Fix: add "stdio," to B:14. In A:190, write "A launcher entry (any name except `serena-local`) with a non-empty `env` or `headers` is kept and reported".

## 3. Checks run and results

- **Layer-2 script.**
  - Extracted A from `#!/usr/bin/env bash` to `echo "LAYER2_OK" | tee -a "$EV"`: 80 lines (77 before; the new lines are 371, 372 and 379). `bash -n` passes.
  - Reasoning under `set -euo pipefail`:
    - A:370 is now a plain redirect, so a failing `jq` aborts the script.
    - A:372 `jq -e` fails the script if seeding did not happen.
    - A:379 `grep -F … >/dev/null` is a plain command (no pipe), so pipefail is not involved.
  - Steps 6b-8 are unchanged from the fourth review's analysis.
- **New acceptance lines.** A:437-439 (T0b), A:563 (T7) and A:615-617 (merge gate) were extracted and pass `bash -n`.
  - T0b semantics: `rg -c` on one file prints a bare count. If nothing matches it prints nothing, and `test "" -ge 7` errors with a non-zero status, so the check still fails correctly. Today's count is 0.
  - T7 semantics: the line parses as `(! rg …) || (rg … | rg -q 'codegraph')`. It passes when the phrase is absent, or when a line containing it names codegraph. Today the repo `CHANGELOG.md` has no "registration kept" line, so the check passes trivially until Phase 1 T12 writes its entry. That is intended.
- **§1 table.** No blank line in A:31-51. All 21 lines have 5 unescaped pipes. F18 precedes F19.
- **Consistency.**
  - The §3.4 guidance block: A:259 and C:57 are equal.
  - Acceptance `jq`: A:205-206 and C:67 are equal.
  - Coder migration location: `T/scripts/startup.sh` in A:679, B:48, C:66 and DF:5/19.
  - Serena match rule: A:190, C:65 and DF:5 agree; B:14 omits stdio (new finding 4).
  - "Neither": only legitimate uses remain in A, B and C. DF:14 and DF:29 are covered by the DF:5 override.
  - "rows 1-12": A:213 and C:49.
- **Merge gate against live Coder.** A read-only `gh api` fetch of `catalogue/mcp-bundle-core/install.sh` on Coder `main` matches the gate pattern at lines 19 and 161. The gate correctly blocks today and would pass once Coder applies step 2.
- **Phase 1 spec, read-only.** `rg -c codegraph_ready` gives 0. The Tier R line `:315` says "no `env`/`headers`". The Tier K printed text at `:325` contains "Legacy Serena registration kept".

## 4. Self-audit

- **Read in full:** the fourth review report, A (lines 1-734 in two reads), B, C, P and DF.
- **Read in part:** Phase 1 spec `:269`, `:307-315`, `:325`, `:354`, `:361`, `:368`, `:376`, `:739-760`, via `rg`/`grep`. The repo `CHANGELOG.md`, via `rg`.
- **Ran (in a private `mktemp -d /tmp/p2-fifth-review.*`, removed by trap):**
  - layer-2 extraction and `bash -n`;
  - `bash -n` on the T0b, T7 and gate lines;
  - pipe counts for the §1 table;
  - `diff` of the guidance block and of the acceptance `jq` between A and C;
  - a parenthesis count on A:190;
  - `grep` for "neither", `startup.sh`, "rows 1-1x", "after task T", and the D23/D24 rows;
  - one read-only `gh api` fetch of the Coder bundle.
- **Not done:**
  - no edits except this report;
  - no `superclaude install`, `claude mcp add/remove`, `update.sh`, `make sync-dev`, test suite, commit or push;
  - the layer-2 script was not executed (it needs T1-T5 code);
  - the acceptance `jq` expressions were not re-run on synthetic cases, because they are byte-identical to the ones the fourth review tested;
  - `shellcheck` is not installed;
  - no history diff was possible: `.dev/codegraph-migration/` is untracked, so "introduced by this round" is judged from the current text against the fourth review's quotes.
- **Limits:** severity is my judgment. Under the "any issue fails" rule, the one PARTLY item and the four MINOR findings make the verdict FAIL.
