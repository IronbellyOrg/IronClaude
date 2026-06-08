# Variant 2 — ANALYZER lens: Evidence-Grounded Reuse-Miss Detection

> Lens: **root-cause analysis + evidence-based reasoning.** The other variants
> will propose *where* to bolt on a reuse check. This variant asks the prior
> question — *why does the duplication keep slipping past every existing gate,
> and what detection SIGNAL actually catches it without crying wolf?* — and
> answers it with a falsifiable overlap metric where **every finding cites
> `file:line` or it does not exist.**

---

## 0. Root-cause analysis — why the duplicate keeps getting built

Before designing a detector, name the failure mode it must catch. Three
independent root causes, each confirmed against the verified concrete case:

| RC | Root cause | Evidence in the concrete case | What it implies for the detector |
|----|-----------|-------------------------------|----------------------------------|
| **RC1 — No neighbour-search is *mandatory*.** | `sc:reflect` §6.1 chain searches the *touched* file's own symbols (overview → declaration → references). It never asks "does a **sibling** module already implement this capability?" | `_bind_specs` (executor.py:1196) was reviewed in isolation; the roadmap `_inject_*` family (roadmap/executor.py:678,715) is two directories away and never entered the evidence chain. | Detection must add an **outward** semantic query keyed on *capability*, not an inward symbol-walk keyed on *name*. |
| **RC2 — The taxonomy has no bin for "built instead of reused."** | §10 has 4 classes — Authorized / Necessary / Drift / Regression — all defined relative to the **driving spec**. A duplicate that *matches* the spec ("bind the specs") is spec-conformant, so it falls through every classifier into `status: success`. | `_bind_specs` does exactly what the prd-spec tasklist asked. No acceptance criterion is contradicted → not Regression. It maps to a tasklist item → not Drift. The taxonomy is **blind to opportunity cost**. | A Reuse Miss is orthogonal to spec-conformance. It needs its own evidence axis: "a cheaper neighbour existed," not "the spec was violated." |
| **RC3 — Pre-build review reads the *target*, never the *neighbourhood*.** | `/tdd` Phase 2 sub-agents "read actual source files, trace actual architectures" of the component **being designed** — inward depth, not lateral breadth. | The TDD for prd-spec would have documented `_bind_specs` thoroughly and *correctly*, and still never asked whether roadmap already solved it. | Pre-stage detection must run a lateral "is this capability already solved nearby?" sweep as a first-class Phase-2 deliverable, not a side-effect of deep-reading the target. |

**The signal that actually catches it.** All three root causes share one missing
primitive: a **capability fingerprint** computed from the *behavioural skeleton*
of a function, queried against the repository, scored by overlap, and **always
carrying the prior-art `file:line`**. Name-matching ("both are called
`_bind_*`") is the trap C3 warns about — `validate_user` vs `validate_token`
share a verb and are `distinct`. The roadmap injectors and `_bind_specs` share
**zero name tokens** (`_inject_*` vs `_bind_*`) yet are the real duplicate. So
the signal MUST be skeleton-based, not lexical. This is the analyzer load-bearing
choice and it sets the false-positive floor for the whole design.

---

## 1. The overlap metric (OQ1) — rigorous, falsifiable, evidence-anchored

The detector's entire credibility rests on one number. Define it precisely so a
reviewer can *reproduce* it and *dispute* it.

### 1.1 The capability fingerprint

For each candidate symbol (a new/changed function in UC-2; a planned component in
pre-stage), compute a **Capability Fingerprint (CFP)** — an ordered tuple of six
behavioural facets, each extracted from real source via the existing
auggie + serena + Read chain (NOT inferred from the name):

| Facet | What it captures | How extracted (evidence tool) | Concrete-case value for `_bind_specs` |
|-------|------------------|-------------------------------|---------------------------------------|
| **F1 — I/O skeleton** | the read→transform→write data-flow shape | serena `get_symbols_overview` + Read of body | `read_text(artifact)` → mutate dict → `write_text(json.dumps)` |
| **F2 — Idempotency idiom** | guard-then-mutate pattern | grep body for guard keywords (`in frontmatter`, `dedup`, `startswith`, `if … not in`) | comment L1234 "dedup, order-preserving, idempotent" + membership guard |
| **F3 — Persistence target** | what artifact is read/written | Read body, resolve the path literal/var | `parsed-request.json` (a persisted pipeline artifact) |
| **F4 — Call-graph role** | when in the pipeline it fires | serena `find_referencing_symbols include_info:true` | post-LLM, post-subprocess injection (called L480) |
| **F5 — Trust rationale** | *why* it exists (docstring/comment intent) | Read docstring + lead comment | "inject what the LLM cannot be trusted to produce" |
| **F6 — Domain nouns** | the entities operated on | tokenize identifiers (stop-word the verbs) | `spec`, `parent dir`, `bound`, `artifact` |

The CFP is `(F1, F2, F3, F4, F5, F6)`. It is written verbatim to
`<output>/reuse-audit/fingerprints.yaml` so the metric is auditable.

### 1.2 The overlap score

For a candidate `C` and a neighbour `N` surfaced by auggie, the **Overlap Score**
`Ω(C,N) ∈ [0,1]` is a **weighted facet-agreement sum** — NOT a name similarity:

```
Ω(C,N) =  0.30 · sim(F1)      # I/O skeleton  — the structural core
        + 0.25 · sim(F2)      # idempotency idiom
        + 0.15 · sim(F4)      # call-graph role
        + 0.15 · agree(F5)    # trust rationale (semantic, auggie-judged)
        + 0.10 · jaccard(F6)  # domain-noun overlap
        + 0.05 · sim(F3)      # persistence-target family
```

- `sim(F1)` = structural match of the read→transform→write skeleton:
  `1.0` identical idiom, `0.5` same family different ordering, `0` unrelated.
- `sim(F2)` = `1.0` if both implement a guard-then-mutate idempotency check,
  `0` if neither, `0.5` if one-sided.
- `agree(F5)` = auggie semantic-equivalence judgement of the two rationale
  strings (the query asks auggie directly: "do these two docstrings describe the
  same responsibility?"), surfaced as `{yes:1.0, partial:0.5, no:0}`.
- `jaccard(F6)` = `|nouns(C) ∩ nouns(N)| / |nouns(C) ∪ nouns(N)|` **after
  stripping shared-verb stop-words** (`validate`, `load`, `build`, `get`, `run`)
  — this is the explicit C3 guard: verbs cannot contribute to the score.

**Weighting rationale (analyzer discipline — every weight defended):** the I/O
skeleton (F1) and idempotency idiom (F2) carry 55% combined because they are what
*actually duplicates* in the concrete case and are the hardest to fake — two
functions can coincidentally share nouns but rarely share a non-trivial
read→guard→inject→rewrite skeleton by accident. Domain nouns (F6) and persistence
family (F3) carry only 15% combined because they are the easiest to coincide on
and the most likely false-positive vector.

### 1.3 Worked example (the ground-truth case — proves the metric fires)

`C = _bind_specs` (executor.py:1196) vs `N = _inject_provenance_fields`
(roadmap/executor.py:715):

| Facet | C | N | sim |
|-------|---|---|-----|
| F1 | read→mutate→write persisted artifact | read→guard→inject→write persisted artifact | **1.0** |
| F2 | dedup/idempotent prepend | per-field idempotency (`if "spec_source:" not in`) | **1.0** |
| F4 | post-LLM injection (L480) | post-subprocess injection | **1.0** |
| F5 | "inject what LLM can't be trusted to produce" | "LLM cannot reliably produce … executor injects post-subprocess" | **1.0** |
| F6 | {spec, parent-dir, bound, artifact} | {spec_source, provenance, field, artifact} | ∩={spec,artifact} → **0.33** |
| F3 | parsed-request.json | roadmap output frontmatter | **0.5** (both persisted pipeline artifacts) |

`Ω = 0.30·1.0 + 0.25·1.0 + 0.15·1.0 + 0.15·1.0 + 0.10·0.33 + 0.05·0.5 = **0.883**`.

`Ω = 0.88` → well above the duplicate threshold (§3). The metric **fires on the
real case** while a pure name match (`_bind_*` vs `_inject_*` = 0 shared tokens)
would have **missed it entirely**. That contrast is the whole proof.

---

## 2. The mandatory neighbour-search step (SC2)

### 2.1 Query construction (the analyzer-precise part)

A neighbour-search is only as good as its query. A vague "find similar code"
query returns name-matches and noise. The mandatory query is **capability-keyed
and skeleton-described**, constructed deterministically from the CFP:

```
QUERY TEMPLATE (auggie codebase-retrieval):
"Find any existing function that <F1 skeleton phrase> on a persisted artifact
 with <F2 idempotency idiom>, acting as <F4 call-graph role>, regardless of
 its name. I am about to introduce <candidate name> that does this. List each
 match with its exact file:line and one sentence on what it does."
```

Concrete instantiation for the ground-truth case:

```
"Find any existing function that reads a persisted pipeline artifact, mutates
 it idempotently (dedup / guard-then-inject), and rewrites it — a post-LLM
 injection step — regardless of its name. I am about to introduce _bind_specs
 in prd/executor.py. List each match with file:line + one-sentence purpose."
```

This query — keyed on *behaviour*, name-agnostic — is what surfaces
`roadmap/executor.py:678,715` even though no name token matches.

### 2.2 What makes a hit CREDIBLE (the evidence bar)

A raw auggie hit is a *lead*, not a finding. It is promoted to a finding **only
after** the orchestrator does ALL of:

1. **Re-Read the hit's `file:line`** (per §6.2 anti-staleness) — confirms the
   symbol exists at the cited location *now*.
2. **Compute `Ω(C,N)` from the re-Read body** — the score is derived from real
   source, never from the auggie summary.
3. **Record the evidence triple** `{hit_file_line, Ω, facet_breakdown}` in
   `fingerprints.yaml`.

A hit that cannot be re-Read (auggie cited a stale/moved line) is **discarded with
a logged `reuse_hit_unverified` row**, never reported. This is the analyzer
invariant: **no finding without a live citation.** It rides the existing §6.2
re-Read discipline rather than inventing a new evidence path.

### 2.3 Insertion point — sc:reflect §6.1

Add as **step 4.6** in the §6.1 mandatory evidence-gathering chain (immediately
after step 4's `find_referencing_symbols`, because the call-graph role F4 is
needed to build the query):

```
4.6. mcp__auggie__codebase-retrieval <CFP-keyed neighbour query>   # FR-RM.1 reuse-miss sweep
     → for each candidate (new/changed function symbol):
       a. build CFP (F1–F6) from steps 2,3,4 evidence already gathered
       b. fire the §2.1 capability-keyed query (NAME-AGNOSTIC)
       c. for each hit: re-Read file:line (step 6 discipline) → compute Ω
       d. retain hits with Ω ≥ 0.60; record all in reuse-audit/fingerprints.yaml
     Fail-open per §6.5: auggie unavailable → emit
       degraded_components: ["reuse_sweep:auggie_unavailable"] and fall back to
       the deterministic grep-skeleton sweep (§7); NEVER block the run.
     Emits one audit.log row: reuse_sweep_invoked: true, candidates_scanned: <n>,
       neighbours_found: <n>, max_overlap: <Ω>.
```

**Scoping (OQ4 — keeps it cheap enough to be mandatory).** The sweep runs ONLY
over **candidate symbols** = functions/methods that are *new* or *body-changed*
in the diff (UC-2) or *named in the proposed design* (pre-stage). Unchanged code
is never swept. One auggie call per candidate, capped at **8 candidates per run**
(`reuse_sweep_budget`); beyond the cap, candidates are ranked by body-line-count
(largest first, since trivial functions rarely duplicate meaningful capability)
and the overflow is logged `reuse_sweep_truncated: true`. auggie is free
(CLAUDE.md), so the cost is latency, not tokens — the cap bounds latency.

### 2.4 Insertion point — /tdd Phase 2

Add a dedicated research-assignment type and a Phase-2 deliverable:

```
NEW research-assignment type (A.3 table):
| Reuse Scout | Detect prior art for each planned component | For every component
  the design proposes to BUILD, fire a capability-keyed auggie query (§2.1)
  across sibling modules + pipelines; for each hit, Read file:line and record
  Ω + the reuse verdict (§5). Output: research/reuse-audit.md. |
```

The Reuse Scout runs in Phase 2 (Deep Investigation), its output is a **mandatory
input** to Phase 5 synthesis, and it populates a new TDD section (§6.4 below).
Pre-stage is the cheaper place to catch the miss — the duplicate has not been
written yet, so the remedy is "design to mirror/reuse," not "rip out and
consolidate."

---

## 3. Consolidation heuristic — thresholds + decision rule (SC4)

The overlap score feeds a **two-axis decision**: overlap strength (`Ω`) × copy
count (`N`). Both axes are evidence-derived; neither is a name heuristic.

### 3.1 Overlap bands

| `Ω` band | Interpretation | Treatment |
|----------|----------------|-----------|
| `Ω < 0.60` | **distinct** — shared idiom at most | No finding. Logged for audit, not reported. |
| `0.60 ≤ Ω < 0.80` | **near-duplicate** — same capability, divergent shape | Advisory finding. Surfaces a `mirror-shape` recommendation (§5). |
| `Ω ≥ 0.80` | **duplicate** — same capability, same skeleton | First-class finding. Blocking-eligible (§4). |

The `0.80` line is where the ground-truth case lands (`Ω=0.88`). The `0.60` floor
is the **false-positive cutoff** — below it, the evidence does not support a
reuse claim and the detector stays silent (C3).

### 3.2 Copy-count → consolidation verdict

`N` = number of *distinct* implementations (including the candidate) with pairwise
`Ω ≥ 0.80`, counted across the repo:

| Condition | Verdict | Where it surfaces |
|-----------|---------|-------------------|
| `N = 2`, both in **one module** | `extract-shared` candidate (advisory) — local helper | reflect advisory finding / tdd reuse-audit |
| `N = 2`, **cross-module** | `mirror-shape` (the new copy should match the existing shape) OR `reuse-by-import` if no import ban | reflect finding (advisory→blocking per §4) |
| `N ≥ 3` (any spread) | **`extract-shared` REQUIRED** — N parallel copies justify a centralized module both depend on | reflect **blocking** finding; tdd reuse-audit "Consolidation Required" |
| `N ≥ 2` cross-module **with an import ban** (NFR-PRD.7-class) | `extract-shared` to a boundary-neutral module (e.g. `cli/pipeline/*`); NEVER `reuse-by-import` | reflect finding + §5 verdict respecting the ban |

**The live test case proves the N≥3 rule.** roadmap already has `_inject_*` ×2
(N=2 in one module → was already an `extract-shared` candidate). `_bind_specs` is
the **third** copy → `N=3` → `extract-shared` is now **REQUIRED**, and because
NFR-PRD.7 bans prd→roadmap imports, the verdict is "extract the
read→guard→inject→rewrite skeleton into `cli/pipeline/artifact_inject.py` that
both depend on" — NOT "import roadmap's helper."

### 3.3 Why N=3 is the blocking threshold (analyzer defence)

Two copies can be a deliberate, reasonable local choice (the cost of a shared
abstraction may exceed the duplication cost). At three, the pattern is
**empirically a pattern**, not a coincidence, and the marginal copy is the moment
to centralize — every further copy compounds the divergence cost. This mirrors
the "rule of three" refactoring heuristic and is defensible to a user who would
otherwise disable an over-eager gate (C7).

---

## 4. Pre-stage vs post-stage differentiation (SC5)

| Axis | **Pre-stage** (`/tdd`, `sc:reflect --mode pre`) | **Post-stage** (`sc:reflect --mode post`) |
|------|--------------------------------------------------|-------------------------------------------|
| **Candidate source** | components/functions *named in the proposed design or tasklist* | new/body-changed symbols in the diff |
| **CFP extraction** | partial — built from the *design description* + any stub; F1/F2 may be `planned` not `observed` | full — built from real shipped source |
| **Evidence** | "neighbour `N` at file:line already does this; design to reuse/mirror it" | "this shipped symbol at file:line duplicates `N` at file:line; Ω=X" |
| **Verdict surface** | TDD reuse-audit section (§6.4) / reflect UC-1 coverage finding | §10.8 Reuse Miss deviation (§6.1 below) |
| **Posture** | **advisory** — cheapest fix is to not build it; recommend mirror/reuse/extract | **advisory → blocking** per §4.1 escalation |
| **Remedy** | edit the design before build | Tier-3 remediation task (rip-out + consolidate) when `--remediate` |

The asymmetry is deliberate: pre-stage is **always advisory** because no debt has
shipped yet — flagging it is pure upside and a blocking pre-gate would be
disabled. Post-stage **escalates to blocking** only at high overlap (§4.1)
because the debt now exists and the cost of leaving it compounds.

### 4.1 Escalation rule — advisory → blocking (hooks §5 rubric rule 3)

A post-stage Reuse Miss escalates exactly like a Regression candidate, reusing the
existing §5.3 rule-3 machinery (which already ESCALATES to T2 for debate):

```
ESCALATE to Tier 2 (debate by ≥2 reviewers) when:
  Ω ≥ 0.80 AND (N ≥ 3 OR the candidate is cross-module duplicate of a
  load-bearing neighbour) AND the verdict is NOT `distinct`.
```

Rationale for hooking rule 3 rather than adding a parallel path: a high-overlap
Reuse Miss has the same asymmetric cost profile as a Regression — cheap to debate
in T2, expensive to ship. One reviewer is exactly the configuration that produced
the miss in the first place (RC1/RC3), so ensemble pressure is the structural fix.

### 4.2 Promotion gate (hooks §14.5.2)

Add a **condition 4-bis** to the 9-condition gate, scoped to high-confidence
misses only (so weak signal never blocks promotion — C7):

```
4-bis. reuse_miss_blocking_count == 0
       where a Reuse Miss is blocking iff Ω ≥ 0.80 AND N ≥ 3 AND verdict ≠ distinct.
       Advisory misses (0.60 ≤ Ω < 0.80, or N=2) are reported but DO NOT gate.
       (maps to gate_evaluation.no_blocking_reuse_miss)
```

This is the principled blocking line (C7): only a *reproducible, high-overlap,
≥3-copy* miss — the exact shape of the ground-truth case — can block promotion.
Everything weaker is advisory and trusted-because-non-intrusive.

---

## 5. Reuse verdict vocabulary (SC7) — honouring NFR-PRD.7-class bans

Each finding carries exactly one verdict, **selected by a deterministic decision
tree** that consults real module-boundary constraints (NOT a guess):

```
def reuse_verdict(C, N, Ω, copy_count):
    if Ω < 0.60:                          return "distinct"          # C3 floor
    import_allowed = not import_banned(C.module → N.module)
                     # import_banned() greps the target module's docstring
                     # invariants (NFR-PRD.7: "No imports from …") + project
                     # dependency rules — EVIDENCE-BASED, cites the ban file:line
    if copy_count >= 3:                    return "extract-shared"    # rule of three
    if import_allowed and Ω >= 0.80:       return "reuse-by-import"   # call it directly
    if not import_allowed:                 return "mirror-shape"      # ban → match the shape
    return "mirror-shape"                                            # 0.60–0.80 default
```

| Verdict | Meaning | Concrete-case applicability |
|---------|---------|------------------------------|
| `distinct` | `Ω<0.60` — legitimately different; no debt | the C3 default for verb-sharers |
| `reuse-by-import` | high overlap + import permitted → call the existing symbol | would apply IF prd could import roadmap — but it **cannot** |
| `mirror-shape` | import banned → name + structure after the neighbour for cross-pipeline consistency | `_bind_specs` should at minimum mirror the `_inject_*` skeleton/naming |
| `extract-shared` | `N≥3` or cross-cutting → promote to a boundary-neutral shared module | **the correct verdict here**: extract to `cli/pipeline/artifact_inject.py`; honours NFR-PRD.7 |

**The NFR-PRD.7 guard is evidence-based, not assumed.** `import_banned()` resolves
by grepping the candidate module's docstring for the literal invariant
(`NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap`),
confirmed present in 8 prd files, and the finding **cites that ban's file:line**
as the reason `reuse-by-import` was downgraded. A detector that recommended
"import roadmap" would be *wrong*, and this guard makes wrongness impossible by
construction — the verdict downgrade is itself a cited finding.

---

## 6. Model-after-for-consistency check (SC3)

Distinct from the duplicate check: even when a new component is *not* a full
duplicate, if it lands in the `0.60 ≤ Ω < 0.80` band against a **dominant
neighbour pattern** (a pattern with ≥2 existing instances), it should *mirror*
that pattern's shape/naming. Divergence here is a **consistency finding**.

The check fires when:
- candidate `C` has `Ω ∈ [0.60, 0.80)` with a neighbour family `F` (≥2 members
  sharing `Ω ≥ 0.80` with each other — i.e. an *established* pattern), AND
- `C`'s naming/structure diverges from `F`'s convention (e.g. `_bind_*` where the
  family is `_inject_*`; positional-arg signature where the family is keyword).

Finding text: `"<C at file:line> diverges from the established <F> pattern
(<member file:lines>): name prefix '<C-prefix>' vs family '<F-prefix>',
<structural delta>. Mirror the family shape for cross-pipeline consistency."`

This is the SC3 deliverable: it catches `_bind_specs` vs the `_inject_*` family
even in the world where you decide *not* to consolidate — at minimum, make the
shapes consistent so the next reader recognizes the pattern.

---

## 7. False-positive guardrails (SC6) — the analyzer strength

The detector is trusted only if it is **falsifiable** and **silent on
legitimately-distinct code**. Four layered guards:

1. **Verb stop-listing (the C3 core).** `jaccard(F6)` strips shared-verb
   stop-words before computing noun overlap. `validate_user` vs `validate_token`
   contribute **zero** from the verb — they can only score on skeleton (F1/F2),
   which they do not share → `Ω` stays low → `distinct`. The signal **cannot** be
   triggered by a shared verb alone.

2. **Skeleton-weight dominance.** 55% of `Ω` is F1+F2 (I/O skeleton +
   idempotency idiom). Two functions must share a *non-trivial behavioural
   skeleton* to clear `0.60`. Coincidental noun/path overlap caps out at ~0.30
   → cannot reach the duplicate band alone.

3. **Live-citation gate (§2.2).** Every retained hit is re-Read at its
   `file:line`; a hit that does not survive re-Read is discarded
   (`reuse_hit_unverified`). No finding can rest on a stale or hallucinated
   auggie summary — the finding is **falsifiable against current source**.

4. **`distinct` exclusion is explicit and recorded.** Sub-`0.60` comparisons are
   written to `fingerprints.yaml` with their facet breakdown and
   `verdict: distinct`, so a reviewer can audit *why* the detector stayed silent.
   Silence is evidenced, not assumed — the analyzer invariant against
   "absence-looks-like-success."

**Deterministic fallback (OQ5 — auggie unavailable).** When auggie is down, the
sweep degrades to a grep-based skeleton probe: grep candidate bodies + sibling
modules for the F2 idempotency keywords (`idempotent`, `dedup`, `startswith("---`,
`if .* not in .*frontmatter`, `read_text` + `write_text` co-occurrence) and
compute F1/F2/F6 only (F4/F5 require semantic judgement). The reduced metric
`Ω' = 0.45·F1 + 0.35·F2 + 0.20·F6` (renormalized) uses a **higher** threshold
(`Ω' ≥ 0.75` for duplicate) because the semantic facets are missing — fewer false
positives at the cost of some recall. Emits
`degraded_components: ["reuse_sweep:grep_fallback"]`. The step **never blocks**.

---

## 8. Concrete spec deltas (SC1) — copy-pasteable

### 8.1 sc-reflect-protocol/SKILL.md — §6.1 chain (insert step 4.6)

> Insert after the existing step 4 line in the §6.1 code block:

```
4.6. mcp__auggie__codebase-retrieval <CFP-keyed neighbour query>   # FR-RM.1 reuse-miss sweep
       For each candidate (new/body-changed function in the diff): build the
       Capability Fingerprint (F1 I/O-skeleton, F2 idempotency-idiom, F3
       persistence-target, F4 call-graph-role, F5 trust-rationale, F6
       domain-nouns) from steps 2–4 evidence; fire the name-AGNOSTIC
       capability query (refs/reuse-audit.md §Query); for each hit re-Read its
       file:line (step 6 discipline) and compute Ω. Retain Ω ≥ 0.60; record all
       in <output>/reuse-audit/fingerprints.yaml. Budget: ≤8 candidates
       (reuse_sweep_budget), largest-body-first. Fail-open (§6.5): auggie
       unavailable → grep-skeleton fallback (refs/reuse-audit.md §Fallback),
       degraded_components += "reuse_sweep:auggie_unavailable", NEVER block.
       Audit row: reuse_sweep_invoked, candidates_scanned, neighbours_found,
       max_overlap.
```

### 8.2 sc-reflect-protocol/SKILL.md — new §10.8 taxonomy entry (slot the "Reuse Miss")

> Insert as a new subsection after §10.7 Reporting (extends the taxonomy without
> disturbing the 4-category ledger — Reuse Miss is an **orthogonal axis**, see RC2):

```
### 10.8 Reuse Miss (orthogonal reuse-debt axis — NOT a 5th deviation class)

**Definition.** A new or changed symbol implements a capability that an existing
symbol already provides (Overlap Score Ω ≥ 0.60 against a neighbour, evidence-
verified), where reuse / mirror / extraction was available and cheaper. A Reuse
Miss is **orthogonal to the 4-category deviation taxonomy**: a duplicate can be
fully spec-conformant (it does what the tasklist asked) yet still be a Reuse Miss.
It therefore does NOT live in deviation-ledger.yaml; it lives in
<output>/reuse-audit/findings.yaml and is reported in its own REPORT.md section.

**Detection signals.**
- §6.1 step-4.6 sweep surfaces a neighbour with Ω ≥ 0.60, file:line re-Read-verified.
- F1 (I/O skeleton) + F2 (idempotency idiom) agreement ≥ 0.5 each (the structural core).
- Copy-count N (distinct impls with pairwise Ω ≥ 0.80) computed across the repo.

**Reuse verdict (refs/reuse-audit.md §Verdict; one of):**
reuse-by-import | mirror-shape | extract-shared | distinct — selected by the
import-aware decision tree; an import ban (e.g. NFR-PRD.7, cited file:line)
downgrades reuse-by-import → mirror-shape / extract-shared.

**Severity & gating.**
- Advisory: 0.60 ≤ Ω < 0.80, OR N = 2. Reported, never blocks.
- Blocking-eligible: Ω ≥ 0.80 AND N ≥ 3 AND verdict ≠ distinct → escalates to
  Tier 2 via §5.3 rule 3 machinery and gates promotion via §14.5.2 cond 4-bis.

**Gold-standard reference.** The neighbour's source at file:line (re-Read-verified)
+ the copy-count census + the import-ban invariant (when applicable, cited file:line).

**Default remediation.** Advisory → REPORT.md recommendation only. Blocking →
Tier-3 consolidation task when --remediate (extract-shared to a boundary-neutral
module, or mirror-shape the existing pattern).

**False-positive guard.** Verb stop-listing in F6; 55% skeleton weight (F1+F2);
live-citation gate; distinct exclusions recorded with facet breakdown. See
refs/reuse-audit.md §Guards.
```

### 8.3 sc-reflect-protocol/SKILL.md — §5.3 rubric (extend rule 3)

> Replace the §5.3 rule-3 row with:

```
| 3 | UC-2 AND (any single hunk classified as `Regression` candidate by Wave 1
        OR any Reuse Miss with Ω ≥ 0.80 AND N ≥ 3 AND verdict ≠ distinct) |
   **ESCALATE** (regression OR high-overlap reuse-debt must be debated by ≥2
   reviewers; structural mechanism, not a confidence question) |
```

### 8.4 sc-reflect-protocol/SKILL.md — §14.5.2 promotion gate (add cond 4-bis)

> Insert after condition 4:

```
4-bis. **`reuse_miss_blocking_count == 0`** — a Reuse Miss blocks iff Ω ≥ 0.80
       AND N ≥ 3 AND verdict ≠ distinct. Advisory misses (lower Ω or N=2) are
       reported but non-gating. *(maps to gate_evaluation.no_blocking_reuse_miss)*
```

### 8.5 sc-reflect-protocol/SKILL.md — §9.1 output contract (new fields)

```
# Reuse-miss (FR-RM)
reuse_miss_count: <int>                 # all findings Ω ≥ 0.60
reuse_miss_blocking_count: <int>        # Ω ≥ 0.80 AND N ≥ 3 AND verdict ≠ distinct
reuse_audit_path: <abs-path> | null     # <output>/reuse-audit/findings.yaml
max_overlap_score: <float 0.0-1.0> | null
reuse_sweep_degraded: <bool>            # true on auggie-unavailable grep fallback
```

### 8.6 tdd/SKILL.md — A.3 new research-assignment type

> Add the "Reuse Scout" row to the A.3 research-assignment-types table (after Doc Analyst):

```
| **Reuse Scout** | Detect prior art before anything is built | For EVERY component
  the design proposes to BUILD, build a Capability Fingerprint and fire a
  name-agnostic capability query across sibling modules + pipelines; for each
  hit, Read file:line, compute Ω, assign a reuse verdict (reuse-by-import /
  mirror-shape / extract-shared / distinct) honouring import bans. Output:
  research/reuse-audit.md with one row per planned component. |
```

### 8.7 tdd/SKILL.md — new mandatory TDD section (Phase 5 synthesis output)

> Add to the synthesized TDD template + the synth mapping table:

```
## Reuse Audit (MANDATORY — populated by the Reuse Scout, Phase 2)

For each component this design proposes to build, the audit answers:
**does it already exist nearby, and if so, what is the reuse verdict?**

| Planned component | Closest prior art (file:line) | Ω | Copy-count N | Verdict | Action |
|-------------------|-------------------------------|---|--------------|---------|--------|
| <name> | <file:line> | <0-1> | <int> | reuse-by-import / mirror-shape / extract-shared / distinct | <design directive> |

**Import-constraint note:** when a reuse-by-import verdict is downgraded by a
module-boundary ban (cite the invariant file:line, e.g. NFR-PRD.7), the verdict
MUST be mirror-shape or extract-shared, NEVER reuse-by-import. A design that
proposes importing across a documented ban is a design defect.

If every planned component is `distinct` (Ω < 0.60 for all), state:
"Reuse audit clean — no prior art above the 0.60 overlap floor; all components
are net-new capability." Silence MUST be evidenced (the audit ran), never assumed.
```

### 8.8 tdd/SKILL.md — A.5 sufficiency gate (add a check)

> Add to the A.5 mandatory research-sufficiency gate checklist:

```
- [ ] Reuse Audit ran for EVERY planned build-component and each has a verdict
      with a cited file:line (or an evidenced `distinct`). A design with an
      un-audited new component fails this gate.
```

---

## 9. Shared sub-spec (OQ6 — dogfooding the heuristic)

Both protocols point at a single `refs/reuse-audit.md` (sections: §Query, §Metric,
§Verdict, §Guards, §Fallback) rather than each embedding the full CFP/Ω
definition. This is itself an `extract-shared` decision (N=2 protocols would
otherwise duplicate the metric spec) — the design **dogfoods its own N≥2 →
extract-shared rule**, which is the strongest evidence that the rule is sound.

---

## 10. Why this variant (analyzer summary, in-spec)

The distinctive bet: **the duplicate is invisible to every existing gate because
it is spec-conformant and name-divergent.** A detector keyed on names or on
spec-violation will never see it. So this variant grounds detection in a
reproducible, falsifiable **behavioural-skeleton overlap metric** (`Ω`, 55%
weighted on I/O skeleton + idempotency idiom, verb-stop-listed) where every
finding cites re-Read-verified `file:line`, every silence is evidenced, and every
`reuse-by-import` downgrade cites the import ban that forced it. The metric is
validated against the ground-truth case (`Ω=0.88`, fires; pure name-match, misses)
before a single byte of the spec is trusted.
