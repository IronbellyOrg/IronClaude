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

---

## 2. Root cause: every lens checks each symbol AGAINST THE DESIGN in isolation; none checks symbols AGAINST EACH OTHER

Map each RF lens to its comparison axis. In every case the **right operand is the design/spec**, and the
**left operand is a single symbol**. There is no lens whose two operands are both *code symbols*.

| Lens | Left operand (audited) | Right operand (oracle) | Axis |
|---|---|---|---|
| template-conformance | one module/dataclass/function name | design public interface | symbol ↔ **design** |
| evidence-quality | one behavior ("does X trace to a requirement") | requirements/design | behavior ↔ **design** |
| no-side-effect-static-boundary | one function's operations | forbidden-op list | function ↔ **boundary rule** |
| domain-accuracy | one state/rule's correctness | requirements meaning | rule ↔ **design** |
| actionability-runtime | one emitted command's runnability | "does the CLI surface exist" | output ↔ **runtime** |
| internal-consistency (final) | a command STRING / sentence | the same string in other files | doc ↔ **doc (parity)** |

The four Phase-2 code lenses form a **star topology**: every spoke points at the design hub, no spoke
connects two code symbols. F1 and F3 live on the **missing edges between spokes**:

- F1 is the edge `diagnose() —(shared probe_evidence contract)— load_evidence()`. Both endpoints
  individually satisfy the design (diagnose returns a legal `ContractState`; load_evidence loads a dir).
  The bug is only visible when you put the two `is_file()`/dir predicates side by side.
- F3 is the edge `probe_pr question —(answer-attr resolves to)— SetupAnswers.probe_pr`. The question ID
  is design-correct; `SetupAnswers` is design-correct. The bug is the *string linking them*.

**Confirmation that the code lenses never form the cross edge, from the artifacts themselves:** the
`no-side-effect` lens literally read both F1 functions in one pass (`…no-side-effect…:26`) and reported
PASS — it had both symbols in context and asked the wrong question. The `template-conformance` lens
literally counted the 16 question IDs (`…template-conformance…:66`) and asked the wrong question. Having
both symbols in view is not enough; **there was no checklist bullet directing the reviewer to compare
them.**

### The `internal-consistency` lens operated at doc/CLI level, not code level — verified

Q2 asks specifically whether the `internal-consistency` lens worked at doc/CLI command-shape level
rather than function-to-function code invariants. **Verified: yes.** Direct evidence quoted in §1:
its four items (`final-qa-internal-consistency.md:21-24`) are all "command string identical across
files" / "sentence byte-identical" / "one CLI surface only." Its single code-to-code item (item 4) is a
**rendered-string** parity diff of two functions that intentionally emit the same user-facing text —
still a doc-surface parity check, not an input-contract or field-resolution check. Its scope sentence
(`line 3`) names the "readiness **surface**," not the package's internal invariants.

### Why the Tier-2 `/sc:reflect` post-audit also missed it (independent second gate)

The `/sc:reflect --mode post` Tier-2 audit (`reflect/post/156f28292b4d/return-contract.yaml`) returned
`status: success`, `tier_reached: 2`, `deviation_count_by_class: {authorized:0, necessary:0, drift:0,
regression:0}`, `regression_present: false`. Its consolidated review
(`t2-adversarial/reflect-review-consolidated.md:29-46`) found only **process-fidelity** deviations:
frontmatter/execution-state drift, a hard gate not executed (Step 5.6), an empty `reflect_post`
artifact, a QA-chain deviation, and broad-vs-scoped test framing. A grep of the entire reflect-post
artifact tree for `is_file`, `probe_pr`, and `_evidence_attr` returns **zero hits** — the audit never
opened those function bodies.

This is by design and by charter: `/sc:reflect --mode post` (UC-2) is a **deviation audit** — "does the
completed work match its driving spec/tasklist, and classify every divergence under the 4-category
taxonomy." It is a fidelity oracle (implementation ↔ tasklist), the same `symbol ↔ design` axis as the
RF lenses, one level up. It is structurally incapable of finding a `symbol ↔ sibling-symbol` bug because
neither the tasklist nor the design encodes the `diagnose/load_evidence` path-shape agreement or the
`probe_pr`/`pr_number` field-name identity. **Both gates share the same blindspot: a spec-anchored oracle
cannot catch a defect that is invisible in the spec.**

---

## 3. "Grep the design, not the call graph" — and the test-coverage gap for the probe_pr answer→default→contract flow

The RF QA method is **design-anchored grep**: to verify a symbol, the reviewer greps/reads the design,
finds the matching entry, and compares. This is powerful for `symbol ↔ design` drift (it correctly
caught the `CheckResult`/`ValidationReport`/`decline_validation="exercised"` drift in
`phase-2-qa-template-conformance.md:52-55` and `phase-2-qa-evidence-quality.md:40-45`). But it is blind
to invariants that live **only in the call graph**, never in the design:

- The design says "question `probe_pr`" and "field `SetupAnswers.probe_pr`" — but the string
  `"pr_number"` passed to `_evidence_attr` is an implementation detail with no design entry to grep.
- The design says `diagnose()` returns `EVIDENCE_MISSING` when evidence is absent — but "absent" being
  decided by `is_file()` vs `.exists()`/dir is an implementation detail with no design entry to grep.

**Confirming the test gap (Q3): did any test exercise the probe_pr answer → default → contract flow
before the fix?** No. Verified via `mcp__auggie__codebase-retrieval` + `git`:

- The ONLY test that exercises `probe_pr_q.derive_default(evidence, SetupAnswers(probe_pr=7)) == 7` is
  `tests/pr_submit/test_contract_setup_questions.py::test_probe_pr_question_default_respects_operator_answer`
  (lines 272-288). Its own docstring says: *"Regression (PR #209 finding F3): the deriver used
  `_evidence_attr("pr_number")`, which read `answers.pr_number` … so a supplied `probe_pr` answer was
  silently ignored."*
- That test was **added by the F3 fix commit `21d4b8e0`** (`git log -S` confirms it appears only in
  that commit; the commit stat shows `+19` lines to `test_contract_setup_questions.py`). It did **not
  exist** during the original RF QA.
- Symmetrically, the F1 directory-valued-`probe_evidence` regression test
  (`test_contract_setup_diagnosis.py`, ~lines 317-350, docstring: *"Regression (PR #209 Augment finding
  F1): diagnose() previously forced EVIDENCE_MISSING unless probe_evidence resolved to a *file*"*) was
  **added by the F1 fix commit `f6a32e9a`** (`+40` lines to that test file).

The pre-fix test suite tested `derive_candidate` provenance thoroughly
(`test_contract_setup_questions.py:136-207` — identity, app-slug, emission observed/unobserved) but
**never asserted that a supplied `probe_pr` answer survives into the derived default/candidate.** It
tested the answer→provenance flow for the fields whose answer-attr name matches; it never tested the one
field (`probe_pr`) whose answer-attr name **differs** from its evidence-field name — which is precisely
the field the bug lived in. The QA verified `SETUP_QUESTIONS` has 16 correctly-named IDs
(`template-conformance` PASS) but never that each question's `derive_default` reads a field that EXISTS
on `SetupAnswers` and FLOWS THROUGH `derive_candidate`.

**Root-cause summary:** RF QA and Tier-2 reflect are both **spec-anchored oracles** on a
`symbol ↔ design` axis. F1 and F3 are `symbol ↔ sibling-symbol` defects that are invisible in the spec
and were untested in the suite. The one lens named for the job (`internal-consistency`) had been scoped
to **doc/CLI command-string parity**, not code-level function-to-function invariants. The external
Augment reviewer caught them precisely because it reads the **call graph and dataclass** directly, with
no design oracle telling it where to look.

---

## 4. Recommendations — concrete, additive RF-protocol changes that would have caught F1 and F3

These are additive (new lens + new static checks + one test-authoring rule); none change existing lenses.

### R1 — Add a `cross-symbol-invariant` code lens to the Phase-2 lens set (highest leverage)

A new adversarial lens whose two operands are **both code symbols in the same package**, not the design.
Charter checklist (illustrative bullets that would have fired on F1/F3):

- **Sibling-function contract parity:** "For every pair of functions that consume the same value
  (`probe_evidence`, an evidence bundle, a path), enumerate each function's assumption about that value's
  SHAPE (file vs dir, tuple vs list, present vs None) and assert they agree. Flag any predicate
  (`is_file()`, `is_absolute()`, `len()==`) that one sibling applies and another does not." → catches F1.
- **Declarative-table field resolution:** "For every entry in a declarative table
  (`SETUP_QUESTIONS`, provenance maps), statically resolve every attribute name the entry reads
  (`getattr` targets, `_evidence_attr` args) to a real field on the target dataclass. Any name that does
  not resolve is a defect." → catches F3.

Because it is adversarial and code-anchored, it fills the missing edges of the star topology.

### R2 — Mandatory static check: "every declarative answer-attr resolves to a real dataclass field"

A tiny, deterministic test (not an LLM lens) that the task must include when it ships a declarative
question/deriver table. Pseudocode:

```python
def test_every_question_deriver_reads_real_setupanswers_fields():
    valid = {f.name for f in dataclasses.fields(SetupAnswers)}
    for q in SETUP_QUESTIONS:
        # call the deriver with a probe SetupAnswers where each field is a sentinel,
        # and assert the deriver's returned default reflects the sentinel it should read
        answers = SetupAnswers(**{real_field_for(q.id): SENTINEL})
        assert q.derive_default(None, answers) == SENTINEL, q.id
```

This is the "answer → default → contract flow" test the suite lacked. It fails hard on `probe_pr` reading
a nonexistent `pr_number`. Make it a `MUST COVER` line in the BUILD-REQUEST whenever a declarative
question/deriver table is in scope. (Note: `getattr(answers, "pr_number", None)` swallowed the
`AttributeError`, so only a *behavioral* assertion — "the answer I set comes back out" — catches it, not
a mere hasattr probe.)

### R3 — Re-charter the `internal-consistency` lens (or split it) to include a CODE-invariant tier

The lens name promises code-invariant coverage but delivers doc/CLI parity. Either (a) rename the current
pass to `doc-surface-parity` and add a distinct `code-invariant-consistency` lens (= R1), or (b) extend
the existing `internal-consistency` checklist with an explicit code tier:

- "Diff each function's INPUT contract against every sibling that consumes the same value (shape,
  nullability, path kind). Rendered-STRING parity of two functions is necessary but NOT sufficient — also
  compare what they READ."

This directly closes the gap that let a lens literally named "internal-consistency" pass a package with
two internal-consistency defects.

### Priority

R2 first (cheapest, deterministic, would alone have caught F3 and — with a dir-vs-file variant —
generalizes to F1), then R1 (the durable structural fix that catches the whole bug CLASS), then R3
(fixes the misnamed lens so the gap can't silently reopen).

## Analysis complete
