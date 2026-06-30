# QA Report — Crossref-Chain Lens (Phase 6, pr_submit V1.1)

**Date:** 2026-06-12
**Lens:** crossref-chain (FR → ref/script → static test)
**Stance:** adversarial / fix_authorization: false (report only)
**Files read:** review-retrigger.md, auggie-fallback.md, retrigger-review.sh, test_static_grep.py, auggie-review.md (for T-1115 parity verification)

---

## Chains traced

### Chain 1 — FR-8.1/8.5 → re-trigger POST → T-1101 / T-1105

- **POST surface (consistent):** `review-retrigger.md:25` and `retrigger-review.sh:34-36` both emit
  `gh api --method POST repos/IronbellyOrg/IronClaude/issues/<N>/comments -f body="auggie review"`.
  Fork-pinned path, body token exactly `auggie review`. The ref and script agree byte-for-byte on the surface.
- **T-1101** (`test_static_grep.py:210-227`): scans `REVIEW_RETRIGGER_REF` (`:44`) + `RETRIGGER_SCRIPT` (`:43`)
  via `_command_lines` for `_GH_CMD` lines not `_fork_scoped` (`:92-94`). Both POST lines contain `FORK`
  → pass; a bare/upstream path WOULD be caught. **Assertion is real and load-bearing.**
- **T-1105** (`test_static_grep.py:230-243`): asserts `"auggie review" in script` (true — `retrigger-review.sh:36`)
  AND `"auggie review" not in fsm_src`. Genuinely guards token-in-script-not-core. **Assertion is real.**

### Chain 2 — FR-9.3 → auggie-fallback.md flag table → T-1115

- **Flag string:** `auggie-fallback.md:28` = `--depth quick --remediation-offer --auggie-model claude-sonnet-4-6`.
- **T-1115** (`test_static_grep.py:246-271`): byte-exact string asserted in fallback (`:253`), then each token
  asserted present in `auggie-review.md`. Verified against command: `--depth`/`quick` `auggie-review.md:49`,
  `--remediation-offer` `:52`, `--auggie-model`/`claude-sonnet-4-6` `:55`. All real flags. **Assertion holds.**

---

## Findings (broken / weak chains)

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | IMPORTANT | `test_static_grep.py:262` vs `auggie-fallback.md:33` | **T-1115 substring parity is too weak — "quick" passes for the wrong reason.** The test asserts `"quick" in cmd`. But `auggie-fallback.md:33` itself contains "quick" only as a `--depth` *value*; the test never binds `quick` to `--depth`. Worse, the parity check is pure substring containment: it would still pass if `auggie-review.md` defined `--depth standard\|deep` and merely *mentioned* the word "quick" elsewhere. The chain claims "flag parity (no drift)" but only proves "these tokens appear somewhere in the doc," not that `--depth quick` is an accepted value pairing. A real drift (e.g. command renames `quick`→`fast`) is only caught because the literal token `quick` vanishes — accidental, not designed. |
| 2 | IMPORTANT | `test_static_grep.py:262` vs `auggie-review.md:55` | **T-1115 cannot prove `claude-sonnet-4-6` is a valid `--auggie-model` value.** `auggie-review.md:55` lists `claude-sonnet-4-6` only inside a parenthetical *example* ("e.g., `--auggie-model claude-sonnet-4-6`"), and the flag default is "(auggie default)". The token-containment check passes because the example string happens to embed it. If someone deleted the e.g. example (cosmetic edit, no behavior change), T-1115 would FAIL even though the model is still valid — and conversely, an actually-unsupported model would pass as long as the example text retained the substring. The test asserts presence of an example, not validity of a value. |
| 3 | MINOR | `auggie-fallback.md:36` (`--post-pr` row) | **`--post-pr`-defaults-true claim has NO corresponding static test of the default.** The ref asserts "`--post-pr` (default true for a PR target)" and "`--no-post-pr` must NOT be passed." T-1115 (`:263-271`) only checks the invocation *line* does not contain `--no-post-pr`; it never verifies `auggie-review.md` actually defaults `--post-pr` to true for a PR target (which it does — `:50`). The behavioral claim ("default true") is unverified by any test; only the negative (no `--no-post-pr` on the invoke line) is. The chain is partially dangling. |
| 4 | MINOR | `auggie-fallback.md:9-11` (T-N50 self-claim) vs `test_static_grep.py:36,109-120` | **The ref's core-purity self-classification is correct but the test only proves the negative.** `auggie-fallback.md:9-11` claims it carries ZERO shell/VC tokens and IS in `CORE_PURE_FILES`. `test_static_grep.py:36` includes it; T-N50 (`:109-120`) asserts no `gh`/`git` token. This passes today. But note: T-N50's token regex is `\bgh\b\|\bgit\b` (`:111`) — it would NOT catch a re-introduced `> Skill ... --post-pr` style command or any non-gh/git I/O token. The "ZERO shell or version-control command tokens" prose claim (`:9`) is broader than what the test enforces (`gh`/`git` only). Narrow coverage of a broad claim. |
| 5 | MINOR | `review-retrigger.md:53` → `auggie-fallback.md` | **Cross-ref `declined` → S5b is prose-only, untested in this surface.** `review-retrigger.md:53` states a `declined` response "routes to the S5b auggie fallback (`auggie-fallback.md`)." No static test in `test_static_grep.py` asserts this routing linkage exists or that the decline regexes in `auggie-fallback.md:15-19` match the phrasing the App emits. Out of scope for the static-grep file, but the FR-8→FR-9 hand-off edge has no static guard here. |

---

## Self-Audit

**(a) Reliance list — items I did NOT independently re-verify (rf-qa structural scope):**
- Relied on rf-qa for section-numbering / file-existence of the four named files (all opened successfully).
- Did not execute the test suite (static read-only review).

**(b) Independent semantic checks (≥1 required):**
- Verified T-1115 token parity by READING `auggie-review.md:49,52,55` — confirmed each asserted token
  exists but discovered the substring check binds none of them to a flag (Findings 1+2). rf-qa "test exists
  and asserts tokens" PASS was insufficient; semantic read of WHAT the assertion proves was required.
- Verified `review-retrigger.md:25` ⇄ `retrigger-review.sh:34-36` POST surface agreement byte-for-byte.
- Verified the `--no-post-pr` invocation-line guard (`test_static_grep.py:263-271`) against the actual
  invocation line `auggie-fallback.md:28` and prose mention `:36` — guard correctly scopes to invoke line.

**Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 0

---

## Verdict rationale

No fully-broken chain (no FR→ref→test link is missing or asserts the opposite of the ref). However Findings 1
and 2 are IMPORTANT: T-1115's "flag parity / no drift" guarantee is weaker than its docstring (`:247-248`)
claims — substring containment cannot detect value-binding drift and is satisfied by example text rather than
real flag definitions. Per phase rules, ANY issue regardless of severity = FAIL.

VERDICT: FAIL
