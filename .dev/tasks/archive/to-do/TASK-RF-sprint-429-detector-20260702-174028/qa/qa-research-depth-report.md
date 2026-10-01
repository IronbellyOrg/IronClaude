# QA Report — Research Depth Review

**Topic:** sprint 429 detector monitor.py hardening
**Date:** 2026-07-02
**Phase:** research-depth (qualitative, adversarial)
**Fix cycle:** N/A
**Fix authorization:** false

---

## Adversarial Stance

Assume the research is a surface inventory until proven otherwise. A file-name list without
behavioral understanding is shallow and would yield vague task items.

## Assigned Files
- research/01-detector-change-surface.md
- research/02-test-and-fixture-conventions.md
- research/03-template-examples.md
- research/shape2-verbatim-transcript.jsonl

Spec: merged-requirements.md

---

## Verification Log

Independent tool verification (adversarial — every load-bearing research claim re-checked against
live source, not accepted on the research's word):

- **monitor.py:41-43 `_RE_ALL_ACCOUNT`** — VERIFIED verbatim (`... are cooling down via provider`).
  Research-01 §2 exact.
- **monitor.py:44 `_RE_SINGLE_ACCOUNT`** — VERIFIED (`would exceed your account's rate limit`).
- **monitor.py:319-321 locals** (`is_error=bool(...)`, `api_error_status=.get(...)`, `body=str(.get("result",""))`) — VERIFIED verbatim. Research-01 §3 exact; the `body` local is in scope at `:321` as claimed, so the C1 disjunct needs no new symbol.
- **monitor.py:323 entry predicate** `if is_error and api_error_status == 429:` — VERIFIED exact.
- **monitor.py:324-333 branch body + neither-body default** — VERIFIED verbatim (`:332` comment, `:333` `SINGLE_ACCOUNT_LIMIT` return). Research-01 §1b exact.
- **monitor.py:335-343 timeout branch** — VERIFIED (predicate `:335-338`, return `:343`, fall-through NONE `:345`). Research-01 §1c exact.
- **monitor.py:272-275 enum members** (NONE/SINGLE_ACCOUNT_LIMIT/ALL_ACCOUNT_COOLDOWN/OPERATION_TIMEOUT) — VERIFIED. Research-02 §5 exact.
- **rerun_tasks.py:552 `_classify_transcript(text)` + delegation to inner `:592` + `FAIL_PROVIDER_EXHAUSTED` / `PASS_RECOVERED` via `completed_before_overrun_from_text`** — VERIFIED. Research-01 §4 row a/b and Research-02 §4 exact. The shared-inner single-source-of-truth claim (R6) holds.
- **SKILL.md:2205 / 2263 / 2322 POST-reflect wrapper form** — VERIFIED verbatim: flat `superclaude reflect run {TASK_FILE} --depth deep --fix --promote` behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard, NO `--base`/`--reflect`/`--max-turns`/range/subagent, exit-code consumption (0 proceeds; 10/11/2 FAIL+HALT), wrapper writes `reflect_post` back. Research-03 §4 is exact and complete.
- **template:638 (I15) 6-agent floor** + **:704-725 (I19) lens tables** + **:793-838 (I22) intensity** — VERIFIED ("absolute minimum is 6 agents (3 rf-qa + 3 rf-qa-qualitative)"). Research-03 §3 exact.
- **Shape-2 verbatim transcript invariants** — VERIFIED by parse: terminal result event, `is_error:true`, `api_error_status` ABSENT, `rate_limit_error` ∈ body, `All credentials for model gpt-5.5 are cooling down` ∈ body, NO `via provider`. All four R1+R2 key-tokens hold.
- **Fix simulation on the verbatim transcript** — VERIFIED: under R1 predicate + R2 loosened regex, the verbatim line enters the 429 branch and matches ALL_ACCOUNT_COOLDOWN with `model=gpt-5.5`. The engineering is sound and the verbatim file is a correct fixture source.

Tool engagement: Read: 6 | Grep(via grep): 3 | Bash: 6 (targeted verifications, not padding).

---

## Lens Assessment (the four asked questions)

### Q1 — Does research/01 explain WHY the change is surgical (locals in scope, old-match ⊆ new-match back-compat), not just WHAT lines change? → YES (deep)

Research-01 §3 pins all three locals to `:319-321` and explains *why* the `rate_limit_error in body`
disjunct needs no helper (the `body` local already exists at `:321`). §5 gives the back-compat proof
STRUCTURALLY: `api_error_status == 429` stays the FIRST disjunct so `old_match ⊆ new_match` "holds by
construction," and it explains the exact Shape-2 breaker (`api_error_status` uses bare `.get` → absent
→ `None` → `None == 429` is False → old conjunct fails). This is behavioral understanding, not a
file-name inventory. A builder can author the two hunk items with exact before/after strings and a
back-compat "ensuring…" clause without re-reading source. PASS.

### Q2 — Does research/02 give enough to author the contract table AND the parity tests concretely (actual assertion forms, not "add a test")? → YES (deep)

Research-02 gives: the exact test class (`TestDetectProviderFailure`, `:243-344`), the `@pytest.mark.unit`
decorator convention, the `kind is` (identity) vs `resolved_model ==` (equality incl. `None`) assertion
forms with copy-ready method bodies, the inline `tmp_path.write_text` convention for synthetic rows, the
shared-inner parity template (`:336-343`), the full 12-row matrix with per-row `(kind, model, source)`,
a parametrize skeleton, and the offline-parity seam (`test_rerun_tasks.py::TestClassifyTranscriptProviderExhaustion`
`:794-828`) with all 4 §6.3 parity asserts mapped to exact surfaces + `is`/`is not` forms. The C3
scope-boundary (do NOT duplicate the 7-row `decide()` table) is called out with the file that owns it.
This is concrete enough to author every test item without re-reading. PASS.

### Q3 — Does research/03 give the exact POST-reflect wrapper item form + the QA-gate 6-agent floor, so the generated task file's own QA gate is compliant? → YES (deep)

Research-03 §4 reproduces the wrapper form byte-accurately (verified against SKILL.md:2205/2263/2322):
skip guard, `--depth deep --fix --promote`, absolute `{TASK_FILE}`, NO forbidden flags, exit-code
semantics, `reflect_post` write-back prohibition, and the MALFORMED conditions. §3 nails the I19/I15
6-agent FINAL_ONLY floor (3 rf-qa + 3 rf-qa-qualitative), the standard lens names, the 8-step M3
sequence each as its own `- [ ]` item, and I22 intensity scaling. TB-Add-7/8 header-vs-item
file:line discipline is covered. The generated task's own QA gate will be compliant. PASS.

### Q4 — Is the Shape-2 anti-fabrication path unambiguous (build fixture from the verbatim .jsonl, byte-for-byte)? → NO — this is the one real gap.

The verbatim source of truth EXISTS in this research directory: `shape2-verbatim-transcript.jsonl`,
which is byte-authoritative and (verified) classifies correctly under the fix. But research/02 — the
file that instructs the builder how to author the load-bearing fixture — **never references that file
by name** (grep confirms 0 references in research/02 or /03). Instead research/02 §3 tells the builder
the verbatim line "is NOT in the merged spec" and to "source the exact byte-for-byte Shape-2 line from
the July incident raw logs / `.dev/troubleshoot/429-signature-ground-truth.md`" — and then supplies its
OWN hand-reconstructed literal.

Two verified problems with that path:
1. **The pointed-at ground-truth file does NOT contain Shape 2.** `.dev/troubleshoot/429-signature-ground-truth.md`
   has 0 occurrences of `gpt-5.5` and 0 of the `API Error: 429` prefix (research/02 even admits "Shape 1
   only is confirmed present in that file"). A builder following the instruction literally would find no
   verbatim Shape-2 line there and would be pushed toward the hand-reconstruction — the exact
   fabrication failure mode the spec §10 warns against.
2. **The provided reconstruction is NOT byte-equal to the real verbatim.** Byte-compare (verified):
   the reconstruction drops the `"type":"None","param":"None"` fields that the real transcript carries
   inside the nested error envelope. The 4 key tokens still hold so it would *classify* correctly, but
   it is not "byte-for-byte" — and shipping a reconstructed fixture when a verbatim capture is sitting
   in the same directory re-introduces fabrication risk for no reason.

The fix is small and unambiguous, so this is IMPORTANT (yields a genuinely wrong/fabrication-prone task
item), not CRITICAL: research/02 should name `research/shape2-verbatim-transcript.jsonl` as the
authoritative byte source for `all_account_cooldown_apierror429.jsonl` and instruct the builder to copy
its terminal result event verbatim, superseding the "pull from July incident raw logs / ground-truth"
instruction and the hand-reconstruction.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | R01 explains WHY surgical (locals, back-compat) | PASS | §3 locals@319-321; §5 old⊆new structural proof; verified vs source |
| 2 | R02 authors contract table concretely | PASS | 12-row matrix + parametrize skeleton + `is`/`==` forms + class@243 |
| 3 | R02 authors parity tests concretely | PASS | §4 all 4 §6.3 asserts mapped to exact surfaces; seam@794-828 verified |
| 4 | R03 POST-reflect wrapper exact form | PASS | §4 byte-matches SKILL.md:2205/2263/2322 |
| 5 | R03 QA 6-agent floor compliant | PASS | §3 matches template:638/704-725/793-838 |
| 6 | Shape-2 anti-fabrication path unambiguous | FAIL | R02 points at wrong source; verbatim .jsonl unreferenced; reconstruction ≠ byte-verbatim |
| 7 | Consumer chain untouched + correct | PASS | R01 §4 rows a-h all verified at cited lines |
| 8 | Fix actually engages recovery on Shape-2 | PASS | simulated: verbatim → ALL_ACCOUNT_COOLDOWN/gpt-5.5 |

---

## Summary
- Checks passed: 7 / 8
- Checks failed: 1
- Critical issues: 0
- Important issues: 1
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | research/02 §3 (`:137-152`) + §3.1 item 1 | The anti-fabrication path for the load-bearing Shape-2 fixture points the builder at `.dev/troubleshoot/429-signature-ground-truth.md` / "July incident raw logs" (verified: ground-truth contains ZERO Shape-2 data — no `gpt-5.5`, no `API Error: 429`) and then supplies a hand-reconstruction that is NOT byte-equal to the real capture (drops `"type":"None","param":"None"` envelope fields). The byte-authoritative verbatim capture `research/shape2-verbatim-transcript.jsonl` already exists in this task's research dir but is never referenced by name. A builder following the instruction literally is pushed toward fabricating the fixture — the exact failure the spec §10 forbids. | Edit research/02 §3 to name `research/shape2-verbatim-transcript.jsonl` as THE authoritative byte source for `all_account_cooldown_apierror429.jsonl`; instruct the builder to copy that file's terminal `{"type":"result",...}` event verbatim into the fixture. Supersede the "pull from July incident raw logs / ground-truth" instruction and delete/demote the hand-reconstructed literal (keep it only as an illustrative comment, clearly marked non-authoritative). Keep the RED-before-fix / GREEN-after validation step. |

**Note on scope:** the defect is in a research file, not a source/component file, and `fix_authorization`
is false — so this is report-only. It is squarely in-scope (the assigned lens is exactly "is the
Shape-2 anti-fabrication path unambiguous").

---

## Self-Audit

1. **How many factual claims independently verified against source?** 13 distinct load-bearing claims
   (all monitor.py line citations, both regexes, the offline classifier delegation+return, the enum,
   the SKILL.md wrapper form across 3 line ranges, the I15/I19/I22 floors, the Shape-2 verbatim
   invariants, and a full fix-simulation). None accepted on the research's word.
2. **Specific files read to verify:** `src/superclaude/cli/sprint/monitor.py` (:38-44, :270-276,
   :318-345), `src/superclaude/cli/sprint/rerun_tasks.py` (:550-606),
   `.claude/skills/task-builder/SKILL.md` (:2205/2263/2322 + recursion-breaker grep),
   `.claude/templates/workflow/02_mdtm_template_complex_task.md` (:638/827/1367/1435),
   `research/shape2-verbatim-transcript.jsonl` (parsed), `.dev/troubleshoot/429-signature-ground-truth.md`
   (grepped for Shape-2 tokens — absent), all four assigned research files, and the merged spec.
3. **Why trust the review found a real issue?** The failing check is backed by three independent
   verified facts a reader can re-run: (a) grep shows research/02 and /03 have 0 references to the
   verbatim `.jsonl`; (b) grep shows the ground-truth file research points to has 0 Shape-2 tokens;
   (c) a byte-compare shows the reconstruction ≠ the verbatim (missing `type`/`param` None fields).
   This is not a "seems shallow" judgment — it is a concrete misdirection with verified evidence.
4. **Web research?** None performed; all verification was local-file-bound. Tavily-first N/A this review.

---

## Recommendations

1. Apply Issue #1's fix to research/02 before the builder runs — it is the single change that closes
   the fabrication-risk gap the whole task exists to prevent.
2. Otherwise the research is genuinely deep: a builder can author every monitor.py hunk, fixture,
   contract-table row, parity assert, QA-gate agent, and the POST-reflect wrapper item WITHOUT
   re-reading source. Research-01/03 are PASS as-is; research-02 is PASS except for the §3 fixture-source
   misdirection.

---

## QA Complete

VERDICT: FAIL

Severity-rated issues: 1 IMPORTANT (research/02 Shape-2 anti-fabrication path points at a source with no
Shape-2 data + supplies a non-byte-verbatim reconstruction, while the authoritative verbatim `.jsonl`
sits unreferenced in the same research dir). 0 CRITICAL, 0 MINOR. All other depth checks PASS.
