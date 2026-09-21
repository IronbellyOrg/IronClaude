# Consolidated Qualitative Findings — cycle 1 (A.10.5)

Sources: `qa-qualitative-operational-report.md` (VERDICT FAIL: 1 CRITICAL, 4 IMPORTANT, 3 MINOR), `qa-qualitative-sufficiency-report.md` (VERDICT FAIL: 2 CRITICAL, 4 IMPORTANT, 4 MINOR). ONE fix agent; task file only; max 3 fix-verify cycles.

## CRITICAL

- **Q-C1 (op #1) item 7.2 A5 proxy** — the F-C2 regex `(?im)^\s*[-*]?\s*evidence[_ ]class\**:?\s*\**(none|source_static|doc_static)` does NOT match the real GLM calibration file: `:13` is a markdown table row (`| Runtime check | … |`, so `^\s*[-*]?` fails) and the value is backticked `` `none` ``. Replace with an unanchored, backtick-tolerant proxy: `re.search(r'(?i)evidence[_ ]class\**`?\s*[:=]?\s*`?\**\s*(none|source_static|doc_static)\b', calibration_text)` — verify by running it against `/config/workspace/Coder/.claude/worktrees/sysbox-retry-glm/.dev/troubleshoot/sysbox-deep/run2-tier2-root-cause-analyst-calibration.md` (must match) and against the Fable D3 calibration text (must NOT match, or scope C-side only). Mirror the amended sentence in 1.1's A5 trigger (no `|`). Update 7.46/7.48/9.7/10.8 wherever the old regex is quoted.
- **Q-C2 (suff #1) items 9.14, 9.16, 9.18** — fidelity agent 2a is instructed that every `refs/agent-assertions.md` trigger must byte-match reconcile §X-3, but 1.1 amends the A5 trigger (F-C2) — guaranteed false positive, and 9.20 "applies EVERY fidelity finding" (would revert). Embed in the 9.14/9.16/9.18 prompts an explicit AUTHORISED-AMENDMENTS list: "A5 trigger amended per F-C2 (consolidated QA); Astra-A3 expected {A1,A10} per F-C1; A5 proxy regex per Q-C1 — these are NOT drift; byte-match all other rows." Make 9.20 apply only findings not on that list.
- **Q-C3 (suff #2) Phase 10 gate (10.4-10.9)** — reviews final state of 19 md files + tests/troubleshoot (>3000 lines) ⇒ I19 floor 12 agents (6 rf-qa + 6 rf-qa-qualitative) covering all 8 standard lenses. Add 6 lens items (mirror the Phase 6 prompt shape with the four missing lenses: internal-consistency, completeness, numbers-metrics, domain-accuracy, plus 2 extra partition-split lenses); update Key Objectives 8, Key Constraints, the Phase 10 header, and 10.14's "N lens + 2 verification report paths" arithmetic.

## IMPORTANT

- **Q-I1 (suff #3) Phase 9 tests gate (9.2-9.8)** — reviewed set is ≥1500 lines (harness §4 bodies alone 1558 + modules + ~153 cases) ⇒ tier 1500-3000 ⇒ 10 agents (5+5). Add 3 lens items (or re-tier with an evidence sentence); fix the Phase 9 header tier claim and Key Constraints.
- **Q-I2 (suff #4) items 6.16, 9.13, 9.23, 10.14** — regression halt string uses a comma: must be the byte-exact API-004 wire string `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (em-dash after `X.Y`). Fix all four.
- **Q-I3 (suff #5) verifier/lens prompts 6.4, 6.14, 6.15, 9.11, 9.12, 9.14, 9.21, 9.22, 10.12, 10.13** — embed the absolute paths of the consolidated findings file, the fix summary, and the task file inside the quoted prompt strings (not only in Context).
- **Q-I4 (suff #6) item 10.17 Output** — post-reflect `--remediate` edits can mutate `src/` after the Phase 10 gate; the commit re-runs only pytest-dir + sync. Add to 10.17: after remediation, re-run the HC guard (5.3 command), `make lint`, and `pre-commit run markdownlint --files <19 files>`; if any `src/` file changed, re-run the Phase 10 gate's verifier pair (10.12/10.13) before 10.18; record in Task Log.
- **Q-I5 (op #2) item 3.18 Verify** — `grep -cF '**Round**: <N> of 3' … == 1` is wrong: `da:204` also contains it ⇒ expected 2 (or grep the full composed header line).
- **Q-I6 (op #3) item 7.2** — point also at harness §4.3 "C8 scope note" and the C6/C8 guards (`if not behaviour_text: return False`; C6 silent when `bracket.md` absent) so every fixture's fired set equals `expected_flags`.
- **Q-I7 (op #4) item 7.46 vs 7.48** — 7.46's "every regression param (`fired_ids == expected`)" inherits harness §5.2 Astra `{A10}`; 7.48 pins `{A1,A10}`. Make 7.46 state the three corrected expected sets explicitly (Astra {A1,A10}; GLM {A1,A3,A4,A5,C2,C3}; Fable {}), or have T13 import the expected table from T15's module.
- **Q-I8 (op #5) items 3.17a, 3.22** — shipped ref text carries `R-03`/`R-04`/`R-05`/`R-06` and `(INV-013)` tags; 6.4's evidence-quality prompt greps for exactly those and will FAIL. Strip spec-artefact tags from the `new_string`s (cite the ref section name instead), consistent with 03 I-19 and F-A5.

## MINOR

- **Q-M1 (op #6) 2.6 Verify** — `\d` unsupported in GNU `grep -E`; use `grep -cE '^[0-9]\. \*\*HC[0-5] — ' ${SKILL}` == 6.
- **Q-M2 (op #7) 1.3 Output** — "22 lines" → "the D9 fenced body (16 lines) + trailing newline" or drop the count.
- **Q-M3 (op #8) 10.17 Verify** — `grep -c 'reflect/post/' ≥ 2` is trivially true; use `grep -cE '^reflect_post: .*reflect/post/'` == 1 on the frontmatter.
- **Q-M4 (suff #7) 10.14** — report-path count: "N lens + 2 verification" with N = final agent count (after Q-C3 = 12).
- **Q-M5 (suff #8) 6.4, 6.6-6.11, 9.2-9.7, 9.14-9.18** — lens-report Verify is `test -s`; use the strict `^(VERDICT|\*\*Verdict\*\*): (PASS|FAIL)` grep on every lens report.
- **Q-M6 (suff #9) 9.15/9.17** — add one cross-surface fidelity reader per partition (markdown ↔ its tests for the same R-item) or state in the prompts that 1a/1b and 2a/2b exchange findings before consolidation.
- **Q-M7 (suff #10) 6.12, 9.9, 9.19, 10.10** — consolidation items must record the per-item PASS_n set (not just |F_n|) so the regression check at n+1 has a defined input.

## Fix-agent contract
Small Edits only; task file only; keep all global invariants (all `Verify:` prefixed, no `…`, one `### Open Questions`, frontmatter parses, no `start_commit`/`executor_model_class`); new gate items must be B2-complete with embedded prompts, `fix_authorization: false`, report path under `${TASK_DIR}qa/exec-*/`, and the strict verdict grep. Append `### Qualitative cycle-1 fixes applied` to the Task Log. Return counts + new item count.
