# Research: Doc cross-validation (R7 — DOC CROSS-VALIDATOR)

Status: Complete
Date: 2026-07-03

Cross-validated `FINAL-remediation-plan.md` (§2 fix table + §3 residual + §5 BUILD_REQUEST)
and `CONSOLIDATED-root-cause.md` (F1–F4 loci) against ACTUAL code at
`/config/workspace/IronClaude/.dev/worktrees/pr209-harden` (branch
`harden/qa-reflect-blindspot-pr209`, HEAD `46a787da`).

Every claim tagged: [CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED].

---

## ⚠️ TWO HEADLINE CONTRADICTIONS THE BUILDER MUST NOT PROPAGATE

### HL-1 — "contract_setup + tests/pr_submit live on master" is FALSE [CODE-CONTRADICTED]

Plan §5 (line 78) and the BUILD_REQUEST premise state FX3/FX5 target
`contract_setup` + `tests/pr_submit/` "which live on **master**, not this
`QAHardening` branch."

Reality (verified via git):
- `git ls-tree -r origin/master --name-only | grep -c contract_setup` → **0**. There is **zero** `contract_setup` on `origin/master`. `origin/master` HEAD = `156f2829`.
- `git ls-tree -r HEAD --name-only | grep -c contract_setup` → **15**. The package + tests exist **only on this branch** (`harden/qa-reflect-blindspot-pr209`, HEAD `46a787da`).
- The package was introduced by `dc507305` ("feat(pr-submit): locked detection-contract setup flow"), which `git branch -r --contains dc507305` reports lives on `origin/DetectionContractBranch` (NOT origin/master).
- This harden branch is built on top of that lineage: `dc507305` → `f6a32e9a` → `21d4b8e0` → … → `46a787da`.

**Correct branch fact for the builder:** the FX3/FX5 deterministic backstops must be
built on **this branch (`harden/qa-reflect-blindspot-pr209`)** or its
`DetectionContractBranch` base — **NOT** off `origin/master`. A task built "from a
branch off `origin/master`" (plan §5 line 78) would have **no `contract_setup`
package to target** and FX3/FX5 would have nothing to introspect.

### HL-2 — F1–F4 are ALREADY FIXED at worktree HEAD → FX2/FX3/FX5 are REGRESSION-GUARDS, not live-bug catchers

The branch includes fix commits `f6a32e9a` ("fix(contract_setup): address Augment
review findings on PR #209") and `21d4b8e0` ("…round-2 Augment review findings").
I read the current source of every F1–F4 locus. **All four bugs are remediated at
HEAD**, with fix-documenting comments AND regression tests present. Details in the
per-finding sections below.

**Consequence for the builder:** the plan/post-mortem narrate F1–F4 as if live. At
this HEAD they are NOT live. FX3 (AST field-resolution), FX5 (negative/differential
helper tests), and FX2 (cross-symbol lens) would therefore land as **regression
guards / additive hardening** that lock in the already-shipped fixes — they are NOT
catching an open bug. This is a legitimate and valuable framing (prevent the class
from recurring), but the task items must be worded as "prevent recurrence / guard
the fix," not "fix the live bug." Any item asserting a live F1–F4 defect is stale.

---

## Deliverable 2 — F1 loci (diagnosis.py ⟂ evidence.py) [CODE-VERIFIED, bug FIXED]

Claim: `diagnose()` has a file-only evidence guard conflicting with sibling
`load_evidence()` / `_evidence_sha256()` which accept a directory.

- `diagnose()` — EXISTS at `diagnosis.py:63`. [CODE-VERIFIED]
- `load_evidence(probe_dir)` — EXISTS at `evidence.py:56`; requires a **directory** (`if not root.exists() or not root.is_dir(): raise FileNotFoundError`, lines 59–60). [CODE-VERIFIED]
- `_evidence_sha256()` — EXISTS at `diagnosis.py:294`; explicitly handles **both** file and dir: `probe_dir = path.parent if path.is_file() else path` then `load_evidence(probe_dir)` (lines 296–298). [CODE-VERIFIED]
- The ⟂ conflict is **RESOLVED at HEAD**: `diagnose()` lines 134–138 accept file-OR-dir (`evidence_path is None or not evidence_path.exists()`), with an explicit fix-comment at 135–137: "probe_evidence may be a captured payload FILE or the probe DIRECTORY … both are valid evidence sources (load_evidence()/_evidence_sha256() accept either)." Validation-report resolution at 159 also normalizes via `evidence_path.parent if is_file() else evidence_path`. **The file-only guard the post-mortem describes no longer exists.** [CODE-CONTRADICTED as a LIVE bug — it is fixed]

## Deliverable 3 — F3 loci (questions.py probe_pr deriver) [CODE-VERIFIED, bug FIXED]

Claim: `probe_pr` question reads `answers.pr_number` (nonexistent) not `answers.probe_pr`.

- `SetupAnswers` has field `probe_pr: int | None` (questions.py:22) and has **no** `pr_number` field. [CODE-VERIFIED]
- The `probe_pr` `SetupQuestion` deriver at questions.py:133–139 is now
  `_evidence_attr("pr_number", answer_attr="probe_pr")`. [CODE-VERIFIED]
- `_evidence_attr(attr, answer_attr=None)` (questions.py:64–76) reads the **answer**
  under `answer_key = answer_attr or attr` (so `probe_pr`), then falls back to the
  **evidence** field `pr_number`. Fix-comment at 65–68 documents exactly this. **The
  bug (reading a nonexistent `answers.pr_number`) is FIXED at HEAD.** [CODE-CONTRADICTED as a LIVE bug — fixed]
- Regression test present: `grep` confirms `probe_pr`/`pr_number` answer-flow coverage
  in `tests/pr_submit/test_contract_setup_questions.py`. [CODE-VERIFIED]

## Deliverable — F2 (app-slug bucket) [CODE-VERIFIED, bug FIXED]

Post-mortem: app-slug override read from `answers.decline_detection_fields[...]`;
no dedicated field; no test.

- `SetupAnswers` now has a **dedicated** `augment_app_slug: str | None` field
  (questions.py:28) with a comment noting it must not be tunnelled through
  `decline_detection_fields`. [CODE-VERIFIED]
- `candidate.py:_selected_app_slug` (161–189) prefers `answers.augment_app_slug`,
  falling back to the legacy `decline_detection_fields` bucket only for back-compat
  (169–171). [CODE-VERIFIED]
- Tests referencing `augment_app_slug`/`app_slug` now exist in
  `tests/pr_submit/test_contract_setup_questions.py` and `…_validation.py`. **F2 fixed with test.** [CODE-CONTRADICTED as a LIVE bug — fixed]

## Deliverable 4 — F4 loci (candidate.py `_path_resolves` + lockgate) [CODE-VERIFIED, bug FIXED]

- `_path_resolves()` — EXISTS at `candidate.py:360`. The all-None-list-as-resolved
  bug is **FIXED**: the list branch (365–376) keeps only elements where the key is
  present-and-not-None (`value := item.get(part)) is not None`), and the `if current
  in (None, []): return False` guard (379) collapses an all-None list to `[]` →
  unresolved. Fix-comment at 369–371 documents it. [CODE-CONTRADICTED as a LIVE bug — fixed]
- `findings_locus` ∈ `MUST_OBSERVE_FIELDS` — VERIFIED at `candidate.py:18–25` (set
  literal includes `"findings_locus"`). [CODE-VERIFIED]
- Gated by `lockgate.py` — VERIFIED: `_paths_resolve()` (lockgate.py:119–126) requires
  `findings.observed and signal.observed`; wired into the 12-check `LockGate.evaluate`
  as `paths_resolve` (CHECK_IDS line 32, invoked line 59). [CODE-VERIFIED]

**F1–F4 net status: all four FIXED at HEAD `46a787da` (via `dc507305`/`f6a32e9a`/`21d4b8e0`), with fix-comments and regression tests.**

---

## Deliverable 5 — §5 BUILD_REQUEST target paths + symbols

| Target (plan §5 SCOPE) | Status |
|---|---|
| `src/superclaude/agents/rf-qa-qualitative.md` | EXISTS [CODE-VERIFIED] |
| `src/superclaude/agents/reflect-reviewer.md` | EXISTS [CODE-VERIFIED] |
| `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` | EXISTS [CODE-VERIFIED] |
| `tests/pr_submit/conftest.py` | EXISTS [CODE-VERIFIED] |
| `tests/pr_submit/test_setup_questions_resolution.py` (FX3 NEW file) | Correctly MISSING — it is the new file FX3 creates, not a stale ref. [CODE-VERIFIED as intended-new] |
| `contract_setup/{lockgate,candidate,diagnosis,validation}.py` (FX5 scan set) | ALL EXIST [CODE-VERIFIED] |
| `SETUP_QUESTIONS` derivers + `SetupAnswers` (FX3 introspection target) | EXIST (questions.py:129–216, :14–38) [CODE-VERIFIED] |
| "reflect return-contract builder + `reflect_post` frontmatter validator" (FX7 target) | Maps to `src/superclaude/cli/reflect/contract.py` (verdict map + FR-11 degradation routing). EXISTS — but see CONTRADICTION FX7 below. [CODE-VERIFIED path; symbol semantics CONTRADICT the fix] |

No §5 target path is stale except the intentional new-file `test_setup_questions_resolution.py`.

---

## Deliverable 6 — "internal-consistency lens only checks doc/CLI string parity (B14)" [CODE-CONTRADICTED / mischaracterized]

Plan §2 line 24 and post-mortem Mechanism 1 assert the `internal-consistency` lens
"only checks doc/CLI string parity." Verified against `rf-qa-qualitative.md`:

- The lens appears three times (lines 92, 307, 755). In every instance it is a
  **DOCUMENT-prose consistency** lens: "Claims in one section must not contradict
  claims in another. Numbers must match across sections. Terminology must be
  consistent" (line 92); the TDD "Internal Consistency" block (307–315) checks
  API-contract/data-model/component-boundary/dependency-graph consistency **across
  document sections** (API schema `{token,expires_at}` vs flow diagram
  `{access_token,refresh_token}`, ER-diagram field vs API response, etc.).
  [CODE-VERIFIED]
- This is **broader than "doc/CLI string parity"** and it is **not** a code
  symbol-to-symbol lens. The "doc/CLI command-string parity" characterization
  describes the **PR #209 QA-RUN artifact** (`final-qa-internal-consistency.md`,
  cited by the post-mortem), i.e. how the lens was *applied on that run* — NOT the
  charter in the agent brief. [CODE-CONTRADICTED — the brief's lens is a document-prose lens, not a string-parity lens]

**Scope-mismatch flag for FX2 (P1):** `rf-qa-qualitative.md`'s own description
(line 3) scopes it to **"assembled documents (PRDs, research reports, tech
references)"** — it verifies whether *content makes sense as a product document*. It
does **not** review Python code modules. FX2's plan text ("rename/augment the
internal-consistency lens … to check code function-to-function invariants (sibling
functions sharing an input)") would graft a **Python-code cross-symbol lens onto a
document-QA agent** — a real scope mismatch. The builder should either (a) target a
different, code-reviewing surface (e.g. `rf-qa` structural or a new code lens), or
(b) explicitly note the agent's charter is being widened from documents to code.
The plan treats this as a rename; it is actually a scope expansion. [CODE-CONTRADICTED as a clean rename]

---

## ADDITIONAL CONTRADICTIONS FOUND (not in the seed list, but load-bearing)

### FX7 CONTRADICTS an existing deliberate exemption in `contract.py` [CODE-CONTRADICTED]

FX7 (plan §2 row + §5) prescribes: "`verification_ran:false => status:degraded +
regression:unknown`." The current reflect verdict engine already handles this — and
**deliberately exempts the post-mortem's exact smoking-gun case**:

- `src/superclaude/cli/reflect/contract.py:35–38` defines
  `_VERIFICATION_SKIP_EXEMPTIONS = frozenset({"read-only-project", "tool-unavailable", "--no-verify"})`
  with the comment "verification_ran == False is exempt (NOT degradation) for these
  skip reasons." [CODE-VERIFIED]
- The FR-11 routing at `contract.py:287–291` (Trigger 12) returns `"verification-skipped"`
  (→ degraded) **only if** `verification_skip_reason not in _VERIFICATION_SKIP_EXEMPTIONS`.
  [CODE-VERIFIED]
- The post-mortem's `return-contract.yaml` smoking gun was `verification_skip_reason:
  tool-unavailable` → silent `regression: 0`. **`tool-unavailable` is one of the
  three exemptions**, so the current code intentionally does NOT degrade it. FX7 as
  written therefore **modifies an existing, deliberate FR-11 guard** (it would have
  to remove `tool-unavailable` from the exemption set) — it is **NOT purely
  additive**, directly conflicting with the BUILD_REQUEST constraint "additive only;
  weaken no existing gate." The builder must treat FX7 as a **reconciliation with
  existing FR-11 exemptions**, and flag the design tension for a human decision
  (why was `tool-unavailable` exempted, and does making it degrade over-HALT
  legitimate read-only/tool-unavailable runs?). [CODE-CONTRADICTED as additive]

### FX1's "5th correctness-gap dimension" CONTRADICTS an explicit taxonomy design statement [CODE-CONTRADICTED]

FX1 (plan §5) prescribes "add a 5th 'correctness-gap' dimension to
`deviation-taxonomy.md`." The taxonomy file **explicitly resists a 5th category**:

- `deviation-taxonomy.md:5`: "The taxonomy is **4 categories** — `evidence-insufficient`
  findings route to a parallel artifact (see *Grounding-gaps parallel artifact*
  below), **not a 5th category**." [CODE-VERIFIED]
- The 4 categories (Authorized/Necessary/Drift/Regression) and their precedence are
  fixed design (lines 26–97). Adding a 5th "correctness-gap" category directly
  contradicts this explicit statement. The builder should route a correctness-gap
  finding to a **parallel artifact** (mirroring the existing `evidence-insufficient`
  pattern) rather than a 5th taxonomy category, OR flag the contradiction for human
  decision. [CODE-CONTRADICTED]

### Post-mortem Mechanism 3 partially already addressed [CODE-VERIFIED context]

Mechanism 3 ("regression=0 was vacuous and unrun; regression is a delta metric")
is partially mitigated already: `deviation-taxonomy.md:80,83,101–107` describe a
default-on §6.1 step-5.5 **verification triangle** (`execute_shell_command` exit
codes → `verification_regressions_detected`), with a documented
exit-code→deviation-class mapping and a fallback-to-task-log-claim-with-Grounding-Gap
when verification is unavailable. So the "tests unrun ⇒ silent pass" story is
already structurally softened in the current taxonomy — the residual gap is the
`_VERIFICATION_SKIP_EXEMPTIONS` behavior above, not a total absence of verification
accounting. The builder should not over-state Mechanism 3 as fully open. [CODE-VERIFIED]

---

## Summary of stale / contradicted plan claims (for the builder to avoid)

1. **[CONTRADICTED]** "contract_setup + tests/pr_submit live on master." → They live
   on `harden/qa-reflect-blindspot-pr209` (this branch) / `DetectionContractBranch`;
   **zero** copies on `origin/master`. Build on THIS branch, not off `origin/master`.
2. **[CONTRADICTED as live]** F1, F2, F3, F4 are **all ALREADY FIXED** at HEAD
   `46a787da` (fix commits `f6a32e9a`/`21d4b8e0`), with fix-comments and regression
   tests. FX2/FX3/FX5 are **regression-guards / recurrence-prevention**, not live-bug
   fixes. Word items accordingly.
3. **[CONTRADICTED as additive]** FX7 "`verification_ran:false ⇒ degraded`" conflicts
   with the deliberate `_VERIFICATION_SKIP_EXEMPTIONS` (incl. `tool-unavailable`) in
   `cli/reflect/contract.py:35–38,287–291`. Not purely additive — reconcile / human-decide.
4. **[CONTRADICTED]** FX1 "add a 5th correctness-gap dimension to deviation-taxonomy.md"
   contradicts taxonomy line 5 ("4 categories … not a 5th category"). Use the parallel-artifact pattern instead.
5. **[CONTRADICTED as a rename]** FX2 "rename/augment the internal-consistency lens" in
   `rf-qa-qualitative.md` — that agent is a **document-QA agent** (PRDs/TDDs/research
   reports/tech refs); its internal-consistency lens is a document-prose lens, not a
   code lens and not "doc/CLI string parity." Grafting a Python cross-symbol lens is a
   **scope expansion**, not a rename. Consider a code-reviewing surface instead.
6. **[VERIFIED]** All §5 BUILD_REQUEST target paths/symbols exist except the
   intentional new file `test_setup_questions_resolution.py`.

## Files read (evidence base)

- `src/superclaude/pr_submit/contract_setup/{diagnosis,evidence,questions,candidate,lockgate}.py`
- `src/superclaude/cli/reflect/contract.py`
- `src/superclaude/agents/rf-qa-qualitative.md` (lines 1–60, 92, 295–333, 755)
- `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`
- git: `ls-tree origin/master|HEAD`, `log`, `branch -r --contains dc507305`
