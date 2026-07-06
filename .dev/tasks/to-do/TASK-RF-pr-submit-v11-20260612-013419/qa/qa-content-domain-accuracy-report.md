# QA Report — pr_submit V1.1 Domain-Accuracy Lens (Phase 3)

**Topic:** Augment decline-detection semantics, regexes, bot login, trigger phrases
**Date:** 2026-06-12
**Phase:** report-qualitative (domain-accuracy lens)
**Fix cycle:** N/A
**Stance:** Adversarial. fix_authorization: false (report only — nothing modified).

---

## Overall Verdict: FAIL

Seven domain-accuracy defects found, two CRITICAL (factually wrong against real Augment
behavior, verified by web evidence + executed regex tests). The test suite passes, but it
passes against a **factually incorrect login constant** and **never exercises the real
backtick-delimited decline phrasing** — so the suite's green status does not certify
real-world correctness.

---

## Tool-engagement summary
- Read: 6 (classifier.py, detection.py, 3 fixtures, detection-contract.md, test_detection_contract.py)
- Grep/Bash: 5 (login grep, regex-execution probe, watermark probe, fixture-consumer grep, test-assertion grep)
- Tavily MCP: 3 searches (Tavily-first honored; no fallback to WebSearch/WebFetch needed — Tavily server loaded and responded)
- Independent regex execution: `uv run python` (verified MISS/MATCH against real + variant bodies)

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Decline semantics (both-regex, decline-first) | PASS | classifier.py:124-129 checks decline BEFORE clean/findings/polling; is_decline requires BOTH regexes (lines 89-92). Logic is correct. |
| 2a | Retrigger regex matches REAL phrasing | **FAIL** | Real Augment body uses markdown **backticks**: ``Comment `augment review` to trigger a new review``. Regex allows only `"`/`'`/none — backtick NOT matched. Executed probe = MISS. |
| 2b | Phrase regex captures real decline wording | **FAIL** | Real declines say "too large"/"exceeds the size limit", not literally "abnormally large". Probe: 4 of 6 realistic variants MISS on phrase. |
| 2c | Benign false-match possible | **FAIL** | Executed probe: a clean review body containing "abnormally large" + `comment "augment review"` guidance falsely classifies as `declined`. |
| 3 | Fixture bot login matches real convention | **FAIL (CRITICAL)** | Fixtures + test constant use `augment-code[bot]` (hyphen). Real login = `augmentcode[bot]` (NO hyphen). |
| 4 | accepted_trigger_phrases correct | PASS | `["auggie review","augment review","augmentcode review"]` matches official docs exactly. Not conflated with decline bait. |
| 5 | Watermark comparison robustness | FAIL (MINOR) | Lexicographic `>` on ISO strings is correct only for uniform `…Z`; mixed UTC offsets compare wrong. |
| 6 | Login vs app-slug conflation | FAIL (IMPORTANT) | Contract ref's own example comment `# e.g. "augment-code[bot]"` is wrong; conflates app *slug* `augment-code` with bot *login* `augmentcode[bot]`. |

---

## Summary
- Checks passed: 2 / 8 sub-checks
- Checks failed: 6
- CRITICAL: 2 | IMPORTANT: 3 | MINOR: 1

---

## Issues Found

### CRITICAL-1 — Fixture + test bot login is factually wrong (`augment-code[bot]` ≠ real `augmentcode[bot]`)
**Location:** `tests/pr_submit/fixtures/decline-comment.json:5`, `decline-initial-poll.json:5`,
`stale-decline-pre-watermark.json:5`; `tests/pr_submit/test_detection_contract.py:28`
(`AUGMENT = "augment-code[bot]"`); contract ref `detection-contract.md:16` example.

**Evidence (web, multiple independent real Augment PRs):**
- `https://github.com/ai-code-review-evaluations/augment-grafana/pull/3` — renders
  `[augmentcode[bot]](https://avatars.githubusercontent.com/in/1027498...)` and `@augmentcode`.
- `https://github.com/ai-code-review-evaluations/augment-discourse/pull/10` —
  `@augmentcode [augmentcode[bot]](/apps/augmentcode). augmentcode[bot] left review comments.`
- `https://github.com/ai-code-review-evaluations/augment-cal_dot_com/pull/9` — same `augmentcode[bot]` login + avatar `/in/1027498`.

The real GitHub **login** is `augmentcode[bot]` (no hyphen). The hyphenated `augment-code`
is the App **slug** (`/apps/augmentcode` is the app URL; the slug appears as `augment-code`
in `augment_app_slug`), a DIFFERENT identifier. The classifier keys on
`contract.augment_bot_login` (classifier.py:81,117), so if the operator's locked contract is
populated with the slug-style `augment-code[bot]` from the wrong example, **every real
Augment review will be classified `polling` forever** (T-211 "different bot → not detected")
and the loop never advances. The tests give false confidence because the fixtures and the
`AUGMENT` constant agree with each other on the wrong value.

Note the internal contradiction: `test_detection_contract.py:107,119` and
`reference_augment_review_triggers.md` BOTH use the correct `augmentcode[bot]`, while the
fixtures + `AUGMENT` constant use the wrong `augment-code[bot]`. The repo holds both spellings.

**Required fix:** Standardize on `augmentcode[bot]` (no hyphen) in all three decline fixtures,
the `AUGMENT` test constant (line 28), the `decline-comment`-adjacent fixtures
(`review-clean.json:4`, `review-with-findings.json:4,13`, `review-interleaved.json:11`), and
the `detection-contract.md:16` example comment. Keep `augment_app_slug: "augment-code"`
(slug is correctly hyphenated). Add a comment distinguishing login-vs-slug so a future probe
operator does not copy the slug into `augment_bot_login`.

### CRITICAL-2 — Retrigger regex misses the REAL decline phrasing (backtick-delimited token)
**Location:** `detection.py:79-81` / `classifier.py:71` / `detection-contract.md:27`
`decline_retrigger_regex = comment\s+["']?(augment|auggie|augmentcode)\s+review["']?`

**Evidence:** Every real Augment comment observed renders the instruction as
``Comment `augment review` to trigger a new review at any time.`` — the token is wrapped in
markdown **backticks** (` `` ` `` `), confirmed verbatim across grafana PR#1/2/3/6/7/9,
discourse PR#10, cal.com PR#9, sentry PR#12. The regex character class `["']?` permits only
double-quote, single-quote, or nothing — **not the backtick**. Executed probe
(`uv run python`): body ``This diff is abnormally large. Comment `augment review` ...`` →
`retrig=False` → MISS → classified NOT-declined.

This is the core V1.1 feature failing on the single most common real decline shape. The
"take the bait" guard the task is meant to implement will silently fail to fire on the actual
App message, because the regex was written against the synthetic straight-quote fixtures,
not the real backtick body.

**Required fix:** Extend the delimiter class to include the backtick:
`comment\s+[\"'\x60]?(augment|auggie|augmentcode)\s+review[\"'\x60]?` (or `[\"'`]`). Add a
fixture whose body uses the literal real phrasing
``Comment `augment review` to trigger a new review at any time.`` so the suite would have
caught this. The asymmetry should also be considered (open vs close delimiter can differ),
but at minimum backtick MUST be accepted.

### IMPORTANT-1 — Phrase regex too narrow; misses non-"abnormally large" decline wordings
**Location:** `detection.py:78` `decline_phrase_regex = abnormally\s+large`
**Evidence:** Executed probe — realistic declines "this pull request is **too large** to
review automatically" and "the diff **exceeds the size limit** for automatic review" both
return `phrase=False` → not classified as decline. The official docs
(`https://docs.augmentcode.com/codereview/overview`) do not publish the exact decline string,
so anchoring on the single literal "abnormally large" is fragile. If Augment phrases the
decline as "too large" (a common variant), the guard never fires.

**Required fix:** Broaden to an alternation, e.g.
`(abnormally\s+large|too\s+large|exceeds.{0,20}(size|diff)\s+limit|too\s+big)` OR — more
robustly — make the decline predicate key primarily on the re-trigger instruction from the
Augment bot WITH a "could-not / won't auto review" negative-completion signal, rather than a
single brittle phrase literal. Document the chosen phrasings' provenance (probe-captured JSON)
in `probe_evidence`.

### IMPORTANT-2 — Benign clean-review body can falsely classify as `declined`
**Location:** `classifier.py:89-92` (both-regex AND with no completion/negation gate)
**Evidence:** Executed probe — body
`I noticed an abnormally large allocation. You could comment "augment review" docs for guidance.`
matches BOTH regexes → `is_decline=True` → would short-circuit a real findings review to
`declined`. Because decline is checked FIRST (classifier.py:127-129) and scans Augment
**reviews** too (not just comments), an Augment review that legitimately *discusses* a large
allocation and mentions the re-trigger phrase in prose would be miscounted as a decline and
its real findings dropped. There is no "this is a non-completion / decline" structural signal
gating the match — only two substring regexes.

**Required fix:** Add a negative-completion guard (the decline body asserts it did NOT review:
"won't review automatically" / "could not" / "skipped"), or restrict decline detection to
comments that are NOT formal reviews with findings, or require the re-trigger instruction to
be the operative imperative (start-of-line / standalone sentence) rather than appearing
anywhere in prose.

### IMPORTANT-3 — Contract ref conflates app slug with bot login (root cause of CRITICAL-1)
**Location:** `detection-contract.md:16` ` # e.g. "augment-code[bot]" — NOT hard-guessed`
vs line 18 `augment_app_slug: "augment-code"`.
**Evidence:** The ref's own worked example hands the operator the slug-shaped login. A probe
operator following this example would lock the wrong `augment_bot_login`. The real login
(`augmentcode[bot]`) and slug (`augment-code`) differ; the ref does not warn of this.
**Required fix:** Change the example to `# e.g. "augmentcode[bot]" (login; NOT the slug
"augment-code")` and add a one-line note that the bracketed login drops the hyphen while the
app slug keeps it.

### MINOR-1 — Watermark `>` lexical comparison is offset-fragile
**Location:** `classifier.py:93-96` `created > watermark` (string comparison)
**Evidence:** Executed probe — for uniform `…Z` timestamps the lexical compare is correct
(stale fixture verified: `08:00Z > 09:30Z` → False → ignored, as expected). But a mixed-offset
pair (`2026-06-12T10:00:00+02:00` vs `2026-06-12T09:00:00Z` — same instant 08:00Z) compares
`True` lexically though the real instant is earlier. `gh`/REST normally emit `Z`, so the live
risk is low, but a non-`Z` `createdAt` would silently break EC-23 staleness.
**Required fix:** Parse to timezone-aware datetimes before comparing (or assert/normalize `Z`),
or document that the contract relies on `gh`-normalized `…Z` timestamps only.

---

## Self-Audit
1. **Claims independently verified against source:** 6 file reads + 5 grep/bash probes; every
   regex finding executed live via `uv run python` (not asserted from reading) — backtick MISS,
   phrase-variant MISS, benign false-match, watermark stale/offset all empirically reproduced.
2. **Files read:** classifier.py, detection.py, the 3 decline fixtures, detection-contract.md,
   test_detection_contract.py.
3. **Why trust this found real issues:** The two CRITICAL findings are backed by multiple
   independent real Augment PRs (avatar `/in/1027498`, `@augmentcode`, `augmentcode[bot]`
   verbatim) AND by executed regex probes — not by reading alone. The suite passes precisely
   because its fixtures encode the same wrong login and omit the real backtick phrasing, which
   is the false-confidence trap this lens exists to break.
4. **Web research / Tavily-first:** 3 Tavily MCP searches; Tavily server was loaded and
   responded on every call — no fallback to WebSearch/WebFetch was triggered or needed.

## Recommendations (before proceeding)
1. Fix CRITICAL-1 (login) and CRITICAL-2 (backtick) first — both make the V1.1 feature fail on
   real Augment output. Add fixtures encoding the REAL bot login + REAL backtick phrasing so the
   suite would catch regressions.
2. Broaden phrase regex (IMPORTANT-1) and add a non-completion gate (IMPORTANT-2).
3. Correct the contract-ref example (IMPORTANT-3) to stop propagating the slug-as-login error.
4. Harden watermark comparison (MINOR-1) or document the `…Z`-only assumption.

## QA Complete

VERDICT: FAIL
