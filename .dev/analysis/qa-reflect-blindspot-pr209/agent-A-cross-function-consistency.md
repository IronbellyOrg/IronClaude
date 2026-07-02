# Agent A — Cross-Function / Cross-Symbol Consistency Blindspot (PR #209 F1 + F3)

**Question:** Why did a 5-phase Rigorflow (RF) QA process + a Tier-2 `/sc:reflect` post-audit fail to
catch F1 and F3 in the `contract_setup` package, both of which are "two symbols that must agree, don't"
bugs that the external Augment reviewer caught on PR #209?

**Angle:** the cross-function / cross-symbol consistency blindspot.

**Method:** every claim below is grounded in the real source (`mcp__auggie__codebase-retrieval`,
direct `Read`, and `git show`/`git log`). QA-checklist text is quoted verbatim from the phase-2 and
final-QA review artifacts.

**Grounding note (temporal):** the current `diagnosis.py` / `questions.py` already contain the F1/F3
FIXES (landed in commits `f6a32e9a` and `21d4b8e0` on 2026-07-02). This analysis reconstructs the
PRE-FIX state from those commit diffs and the QA artifacts, which were written against the pre-fix tree.

---

## The two bugs, restated as symbol-pair disagreements

- **F1** — `src/superclaude/pr_submit/contract_setup/diagnosis.py`. `diagnose()` gated
  `probe_evidence` on `is_file()`, but the sibling functions `load_evidence()` and
  `_evidence_sha256()` in the SAME package accept a probe *directory*. A locked contract whose
  `probe_evidence` pointed at the probe **dir** got a false `EVIDENCE_MISSING`. Symbol pair that
  disagreed: `diagnose()` ⟂ `load_evidence()`/`_evidence_sha256()`.

- **F3** — `src/superclaude/pr_submit/contract_setup/questions.py`. The `probe_pr` setup question
  derived its default via `_evidence_attr("pr_number")`, which does `getattr(answers, "pr_number")`
  — but `SetupAnswers` has NO `pr_number` field (it is `probe_pr`, `questions.py:21`). A supplied
  `probe_pr` answer was silently ignored. Symbol pair that disagreed: the question's answer-attr
  name (`"pr_number"`) ⟂ the real `SetupAnswers` dataclass field (`probe_pr`). The sibling `repo`
  question works only because its answer-attr and evidence-field happen to share the name `repo`.

Both are the same shape: **a contract encoded in one symbol contradicts a contract encoded in a
sibling symbol in the same module. Neither symbol is wrong against the design in isolation.**

---

## 1. Which QA lens/gate was RESPONSIBLE — and what it actually checked

The task ran **five Phase-2 lenses** (per `phase-2-qa-consolidated.md:9-15`): `template-conformance`,
`evidence-quality`, `no-side-effect-static-boundary`, `qualitative-domain-accuracy`,
`qualitative-actionability-runtime` (+ a `raw-payload-redaction` pass). Plus a **final
`internal-consistency` lens** at report-validation. Here is what each was chartered to check, and why
each missed F1/F3.

### F1 (diagnose ⟂ load_evidence dir/file disagreement) — responsible lens: `no-side-effect-static-boundary`

Its item 1 checklist bullet reads (`phase-2-qa-no-side-effect-static-boundary.md:26`):

> "`diagnose()` / `load_evidence()` / `validate_candidate()` perform no file write, no live GitHub
> call, no `run_skill()`, no Monitor arming" — **PASS**

It read `diagnose()` AND `load_evidence()` in the same pass — the exact two functions that disagreed —
but only to confirm neither has a **side effect**. It never asked "do these two functions agree on what
a valid `probe_evidence` is (file vs dir)?" The lens is a *boundary* lens: it inspects each function
for forbidden operations, not for a shared input contract. **No bullet in any Phase-2 lens asks whether
`diagnose()`'s path-shape assumption matches `load_evidence()`'s.**

The `domain-accuracy` lens came closest — it checks state transitions against requirements
(`phase-2-qa-qualitative-domain-accuracy.md:28`, "The nine UX states are handled") — but it verifies
each state against the **design's meaning**, one function against the spec, never `diagnose()`'s
`is_file()` predicate against `load_evidence()`'s dir-accepting predicate.

### F3 (probe_pr answer-attr ⟂ SetupAnswers field) — responsible lens: `template-conformance`

`template-conformance` is the lens that owns the setup-question table. Its own PASS finding
(`phase-2-qa-template-conformance.md:66`) is the smoking gun:

> "`SETUP_QUESTIONS` contains 16 question IDs matching the design's question sequence."

It verified the **IDs** (`repo`, `probe_pr`, …) match the design's 16-question sequence — and stopped.
It never verified that each `SetupQuestion.derive_default` reads a field that **exists on
`SetupAnswers` and flows through `derive_candidate`**. The lens's charter is name/interface conformance
**against the design** (`phase-2-qa-template-conformance.md:29`, "Module/function/dataclass names match
design public interface exactly"), so it audited `CheckResult`/`ValidationReport`/`EvidenceBundle`
field names vs the design — and found real drift there — but the design has no entry for "the internal
argument string passed to `_evidence_attr` inside a question deriver." `"pr_number"` is a string literal
buried in a factory call, invisible to a design-conformance grep.

### The final `internal-consistency` lens — the one that SHOULD have owned both — operated at doc/CLI level, NOT code level

This is the decisive finding. An `internal-consistency` lens **existed** at report-validation
(`final-qa-internal-consistency.md`), and by name it is exactly the lens that should catch
"two things that must agree, don't." But read its four checklist items
(`final-qa-internal-consistency.md:21-24`) — every one is **document/CLI command-shape parity**:

- Item 1: "command shape `superclaude reflect contract-status [--validate] --repo … --pr …` **identical
  everywhere**" — byte-match across `commands/reflect.md`, `pr-submit.md`, two `SKILL.md`s.
- Item 2: "Reflect readiness surface is exactly ONE … no `/sc:reflect --contract-status` flag alias".
- Item 3: canonical no-side-effect **sentence** is "BYTE-IDENTICAL at `diagnosis.py:245`,
  `commands/pr-submit.md:61`, `skills/…/SKILL.md:90`".
- Item 4: "Ready-state next command consistent across `diagnosis.py::_next_command`,
  `commands.py::_contract_status_next_command`, docs, and tests".

Its own summary frames the whole pass as doc parity (`final-qa-internal-consistency.md:3`):
"cross-surface internal consistency of the detection-contract readiness **surface**" and
(`line 13`) "No contradiction found across helper code, the reflect CLI surface, both command docs,
both skill docs, and the tests."

The ONE code-to-code check it did (item 4, the two `_next_command` functions) is a **string-output
parity** diff, chosen because both functions render the SAME user-facing command string. It is still a
"do two renderings of the same doc-surface agree" check. **It never diffed a function's INPUT contract
against a sibling's** (diagnose's path-shape vs load_evidence's), and it never checked
**answer-attr → dataclass-field** resolution. The lens's mental model is "one surface, many renderings,
they must be byte-identical" — not "two functions, one shared invariant, they must be semantically
compatible."

### Answer to Q1

**No lens, at any phase, contained a bullet for "sibling functions in the same module must agree on
their shared contract" or "a question's answer-attr name must resolve to a real `SetupAnswers` field."**
The `internal-consistency` lens is misnamed relative to what it does: it is a **doc/CLI-surface parity**
lens, not a code-invariant lens.
