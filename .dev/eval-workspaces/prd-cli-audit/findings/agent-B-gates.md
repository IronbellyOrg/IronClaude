# Agent B — Gates & verification findings

Scope: `src/superclaude/cli/prd/gates.py` (read in full, 506 lines).
Cross-references into executor / pipeline models annotated and deferred to the
owning agents where appropriate.

---

### F-B-1: `_tier_min_lines` / `_tier_min_lines_assembly` have zero call sites — heavyweight runs silently use the standard default (Bug 3, confirmed)

**Severity (preliminary)**: CRITICAL
**Pattern tags**: P2, P7
**File:line**: `src/superclaude/cli/prd/gates.py:281-292`; consumer side
`src/superclaude/cli/prd/executor.py:587-624` (`_evaluate_gate`)

**Evidence**:

```python
# gates.py:281
def _tier_min_lines(tier: str) -> int:
    """Return tier-dependent minimum line count for task file gate."""
    return {"lightweight": 200, "standard": 400, "heavyweight": 600}.get(tier, 400)


def _tier_min_lines_assembly(tier: str) -> int:
    """Return tier-dependent minimum line count for assembly gate."""
    return {
        "lightweight": 400,
        "standard": 800,
        "heavyweight": 1500,
    }.get(tier, 800)
```

And in the gate constructors:

```python
# gates.py:367 (build-task-file)
min_lines=400,  # default standard tier; callers override per tier
# gates.py:459 (assembly)
min_lines=800,  # default standard tier; callers override per tier
```

**Trace**:
- Defined in `gates.py:281` and `gates.py:286`.
- `grep -rn "_tier_min_lines" src/ tests/` returns only the two definition lines.
  No call site anywhere in `src/superclaude/**` or `tests/**`.
- The "callers override per tier" comment is aspirational. The only code path
  that consumes `gate.min_lines` is `_evaluate_gate` at `executor.py:596-609`,
  which reads `gate.min_lines` straight from the dataclass — no tier lookup, no
  override seam, and `PrdExecutor.__init__` never mutates `GATE_CRITERIA`.
- `self._config.tier` IS read elsewhere (`_build_investigation_steps:717`,
  `_build_web_research_steps:735`) but never near gate evaluation.

**Reproduction sketch**: Run `superclaude prd run --tier heavyweight ...`. The
`build-task-file` gate threshold stays at 400 (instead of 600); a 500-line task
file passes a heavyweight run that the spec says should require 600. Symmetric
miss on `assembly` (heavyweight expects 1500, gets 800). Lightweight runs are
also silently over-strict — a 250-line task file passes lightweight even though
the function would have allowed 200.

**Confidence (own)**: 0.99 — the absence of consumers is mechanically
verifiable; only mild uncertainty is whether a future caller would patch
`GATE_CRITERIA["build-task-file"].min_lines` at runtime, but no such code
currently exists.

---

### F-B-2: `_evaluate_gate` never reads `gate.required_frontmatter_fields` — every frontmatter declaration in `GATE_CRITERIA` is dead code

**Severity (preliminary)**: HIGH
**Pattern tags**: P1, P2, P7
**File:line**: consumer expected in `src/superclaude/cli/prd/executor.py:587-624`;
declarations in `src/superclaude/cli/prd/gates.py:298, 304, 317, 323, 341, 354,
360-366, 388, 402, 408, 414, 426, 433, 439, 452-458, 475, 488, 502`

**Evidence**:

```python
# executor.py:_evaluate_gate (only checks performed)
if gate.min_lines > 0:
    line_count = len(content.splitlines())
    ...
if gate.semantic_checks:
    for check in gate.semantic_checks:
        ...
```

vs.

```python
# gates.py:359 (build-task-file)
"build-task-file": GateCriteria(
    required_frontmatter_fields=[
        "id", "title", "status", "complexity", "created_date",
    ],
    min_lines=400, ...
)
# gates.py:451 (assembly)
"assembly": GateCriteria(
    required_frontmatter_fields=[
        "id", "title", "status", "created_date", "tags",
    ], ...
)
# gates.py:323 (research-notes)
required_frontmatter_fields=["Date", "Scenario", "Tier"],
```

**Trace**:
- `grep -n "required_frontmatter_fields\|frontmatter" src/superclaude/cli/prd/executor.py`
  returns zero matches.
- The only consumer in the repo for `required_frontmatter_fields` is in the
  generic `src/superclaude/cli/pipeline/gates.py` evaluator, which the PRD
  pipeline does NOT use. PRD has its own bespoke `_evaluate_gate` that ignores
  that field.

**Reproduction sketch**: Run a heavyweight PRD pipeline that produces a task
file without `created_date` in its frontmatter. The gate still passes (line
count + semantic checks were satisfied). Downstream consumers that assume
those frontmatter fields exist would crash with `KeyError`. The original
heavyweight failure (30-line NDJSON commentary read as a task file) would
also have failed the frontmatter check if it had ever been wired — but it
isn't, so the only line that actually halted was the min_lines check.

**Confidence (own)**: 0.97 — pattern is unambiguous; only outstanding
question is whether some other module wraps `_evaluate_gate` and adds
frontmatter validation. Auggie sweep + grep do not find one in the PRD
slice.

---

### F-B-3: `GATE_CRITERIA` keyed only on static step IDs — every dynamically-named step (`investigation-N`, `web-research-N`, `synthesis-N`, `*-fix-N`) silently has no gate

**Severity (preliminary)**: HIGH
**Pattern tags**: P1, P3, P7
**File:line**: `src/superclaude/cli/prd/gates.py:295-506` (table); consumers
`src/superclaude/cli/prd/executor.py:530` and `:864`

**Evidence**:

```python
# gates.py: only these dynamic-family base keys exist
"investigation":   ...,   # line 407
"web-research":    ...,   # line 426
"synthesis":       ...,   # line 432
```

```python
# executor.py:530
gate = GATE_CRITERIA.get(step_id)
if gate and status.is_success:
    gate_passed = self._evaluate_gate(step_id, gate, gate_content)
```

```python
# executor.py:727-729, 745, 757
step_id = f"investigation-{i + 1}"
f"web-research-{i + 1}"
f"synthesis-{i + 1}"
# executor.py:886
f"{qa_step_id}-fix-{cycle + 1}"   # e.g. "research-qa-fix-1"
```

**Trace**:
- Stage-B generates `investigation-1 … investigation-N`, `web-research-1 …`,
  `synthesis-1 …`. Gate lookup is exact-match on `step_id`.
- `GATE_CRITERIA.get("investigation-1")` returns `None`. `_evaluate_gate`
  is never invoked for any Stage-B parallel step.
- Fix-cycle steps `research-qa-fix-1`, `synthesis-qa-fix-2` likewise get no
  gate.

**Reproduction sketch**: A `synthesis-3` agent emits a 5-line stub
("Synthesis pending."). No gate runs (no `min_lines=80` check, no semantic
checks). Status is `PASS_NO_SIGNAL` because exit_code==0. Pipeline proceeds
to `assembly` with a fatally thin synthesis input. The original
heavyweight bug 3 failure would have surfaced earlier in Stage B if these
gates had fired with proper tier thresholds.

**Confidence (own)**: 0.96 — verified by reading the dynamic step-ID
generation against the static dict keys. Could only be wrong if some
upstream pre-normalizes the step_id (it doesn't; `_evaluate_gate` receives
the raw `step_id` as its first argument).

---

### F-B-4: `enforcement_tier="EXEMPT"` and `"LIGHT"` are declared in gates.py but unrecognized in PRD `_evaluate_gate` — they fail like STANDARD instead of being skipped

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P2, P7
**File:line**: `src/superclaude/cli/prd/gates.py:300, 356, 404, 504`;
consumer `src/superclaude/cli/prd/executor.py:531-540`

**Evidence**:

```python
# gates.py
"check-existing": GateCriteria(..., enforcement_tier="EXEMPT")    # :300
"template-triage": GateCriteria(..., enforcement_tier="EXEMPT")   # :356
"preparation": GateCriteria(..., enforcement_tier="LIGHT")        # :404
"present-complete": GateCriteria(..., enforcement_tier="LIGHT")   # :504
```

```python
# executor.py:530-540
gate = GATE_CRITERIA.get(step_id)
if gate and status.is_success:
    gate_passed = self._evaluate_gate(step_id, gate, gate_content)
    if not gate_passed:
        if gate.enforcement_tier == "STRICT":
            status = PrdStepStatus.HALT
        else:
            status = PrdStepStatus.VALIDATION_FAIL
```

**Trace**:
- `grep -n "EXEMPT\|LIGHT" src/superclaude/cli/prd/executor.py` returns
  zero hits. The generic `src/superclaude/cli/pipeline/gates.py:29,42`
  treats `EXEMPT` as "always pass" and `LIGHT` as "report-only", but
  PRD's bespoke `_evaluate_gate` ignores both.
- Net behavior: `EXEMPT` and `LIGHT` gates ARE evaluated and CAN set
  status to `VALIDATION_FAIL`. The label is decorative.
- Because these four steps all have `min_lines=0` and no `semantic_checks`,
  they happen to pass today — but adding any check (e.g. someone bumping
  `present-complete`'s `min_lines`) would silently start failing the run
  contrary to the declared "EXEMPT" intent.

**Reproduction sketch**: Add `min_lines=10` to the `"preparation"` entry
("LIGHT"). A step producing 5 lines of output would set
`PrdStepStatus.VALIDATION_FAIL` and surface as a pipeline failure, even
though `LIGHT` semantically means "informational only".

**Confidence (own)**: 0.9 — verified by grep; lower than other findings
because the latent failure requires a future config change to manifest
(today, the four exempt/light gates all have nothing to check).

---

### F-B-5: `_check_b2_self_contained` does not match uppercase `[X]` checklist marks; misses any item phrased differently from the four hard-coded phrases

**Severity (preliminary)**: LOW
**Pattern tags**: P2 (mild)
**File:line**: `src/superclaude/cli/prd/gates.py:162-179`

**Evidence**:

```python
# gates.py:169
for match in re.finditer(r"^\s*-\s+\[[ x]\]\s+(.+)$", content, re.MULTILINE):
    item_text = match.group(1)
    for phrase in ["see above", "as mentioned", "refer to", "as described"]:
        ...
```

**Trace**:
- Character class `[ x]` accepts only space or lowercase `x`. `[X]` (the
  GitHub-style "checked" marker that many editors produce) silently
  bypasses the self-containment check. Items rendered as `* [ ] …` (asterisk
  bullet) are also skipped because the regex hard-codes `-`.
- Phrase list is exact-substring lowercase only — `"See the section above"`
  is fine ("see above" never appears), as is `"refer back to"`.

**Reproduction sketch**: A task file with `- [X] As mentioned in Phase 1,
…` passes the self-containment gate. So does `* [ ] Refer back to the prior
step.`.

**Confidence (own)**: 0.85 — regex behavior is unambiguous; severity is
low because this is a quality check, not a halt-the-pipeline check, and
the heavyweight task-file in question failed for a different reason.

---

### F-B-6: `_check_research_notes_sections` accepts ANY heading whose text contains a section keyword anywhere on the line — false positives on prose headings

**Severity (preliminary)**: LOW
**Pattern tags**: P2 (mild), P3
**File:line**: `src/superclaude/cli/prd/gates.py:113-126`

**Evidence**:

```python
heading_pat = re.compile(
    rf"^\s*#{{1,4}}\s+.*{re.escape(section)}", re.MULTILINE | re.IGNORECASE
)
bold_pat = re.compile(rf"\*\*{re.escape(section)}\*\*", re.IGNORECASE)
```

**Trace**:
- The leading `.*` before `{section}` means a heading like
  `## How EXISTING_FILES are tracked` matches the `EXISTING_FILES`
  requirement even though it's not the canonical section. Coupled with
  `IGNORECASE`, prose mentioning `feature_analysis` in any heading
  (e.g. inside a code-fenced block that happened to start with `#`)
  counts. The check is not anchored to a section heading at the
  start-of-content position.
- `_check_prd_template_sections` at gates.py:224 has the same shape and
  the same loose match.

**Reproduction sketch**: A research notes file with a top-level
`# How EXISTING_FILES, PATTERNS_AND_CONVENTIONS, FEATURE_ANALYSIS,
RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES,
AMBIGUITIES_FOR_USER fit together` (i.e. a single heading naming all
seven) passes the gate without any of the actual sections being present.

**Confidence (own)**: 0.8 — regex is permissive in this exact way; real-
world manifestation requires an LLM to produce that shape of heading,
which is plausible but not common.

---

### F-B-7: `_check_parsed_request_fields` JSON regex requires `: "non-empty"` but markdown regex requires only `: \S` — schemas drift

**Severity (preliminary)**: LOW
**Pattern tags**: P3
**File:line**: `src/superclaude/cli/prd/gates.py:83-99`

**Evidence**:

```python
json_pat = re.compile(rf'"{field_name}"\s*:\s*"[^"]+"', re.IGNORECASE)
md_pat = re.compile(
    rf"(?:^|\n)\s*\*{{0,2}}{field_name}\*{{0,2}}\s*:\s*\S",
    re.IGNORECASE,
)
```

**Trace**:
- JSON form: value must be a quoted non-empty string. Markdown form: value
  must be a single non-whitespace character. A markdown parsed-request
  with `GOAL: -` (literally a hyphen, no goal) passes.
- Bigger issue: `_check_parsed_request_fields` is wired to the
  `parse-request` gate which has `min_lines=0` and `enforcement_tier=STRICT`.
  An empty / near-empty parsed-request only needs each field's name to
  appear with a colon and one glyph after it. This is a HIGH-impact gate
  with a soft check.

**Reproduction sketch**: An LLM emits a "parsed request" markdown file
with stub values (`GOAL: ?`, `PRODUCT_SLUG: x`, …). All four fields
satisfy `\s*:\s*\S`. Gate passes STRICT.

**Confidence (own)**: 0.85.

---

### F-B-8: `_check_qa_verdict` delegates to `_check_verdict_field`, but `_check_verdict_field`'s markdown regex matches PASS|FAIL embedded inside arbitrary lines, not just the verdict declaration

**Severity (preliminary)**: LOW
**Pattern tags**: P3
**File:line**: `src/superclaude/cli/prd/gates.py:36-53, 239-241`

**Evidence**:

```python
md_match = re.search(
    r"(?:^|\n)\s*\*{0,2}[Vv]erdict\*{0,2}\s*:\s*(PASS|FAIL)",
    content,
)
```

**Trace**:
- Regex requires the literal word "Verdict" followed by `: PASS` or
  `: FAIL`. That part is sound.
- But the JSON path at line 43 is a substring match anywhere in the
  document: `re.search(r'"verdict"\s*:\s*"(PASS|FAIL)"', content)`. If a
  QA report quotes an earlier failed verdict (e.g. inside a fenced code
  block showing prior output: `"verdict": "FAIL"`), the gate would
  resolve `FAIL` as a successful detection — and then `_determine_status`
  at executor.py:579 separately decides `QA_FAIL`. Conversely, a report
  that QUOTES a prior PASS in commentary but then writes
  `**Final Verdict**: BLOCKED` would be scored PASS by the verdict-field
  check.
- Same regex is reused across `verify-task-file`, `research-qa`,
  `synthesis-qa`, `structural-qa`, `qualitative-qa`, `sufficiency-review`.

**Reproduction sketch**: A QA report containing this prose:
```
Earlier the verdict was: "verdict": "PASS"
Current state: **Final Verdict**: REJECTED
```
…passes `_check_verdict_field` because the regex finds `"verdict": "PASS"`
verbatim in the commentary line.

**Confidence (own)**: 0.8.

---

### F-B-9: `_check_task_phases_present` requires only 2 headings containing the string `Phase \d` — a task file with `Phase 1` and `Phase 1.5` passes; case-insensitive `phase 99` also passes

**Severity (preliminary)**: LOW
**Pattern tags**: P3
**File:line**: `src/superclaude/cli/prd/gates.py:149-159`

**Evidence**:

```python
phase_headings = re.findall(
    r"(?:^|\n)\s*#{1,4}\s+.*Phase\s+\d", content, re.IGNORECASE
)
if len(phase_headings) < 2:
```

**Trace**:
- `\d` matches a single digit; "Phase 10" matches, "Phase 1.5" matches,
  "Phase A" doesn't. The 2-heading floor is generous and not anchored to
  sequential numbering.
- `_check_parallel_instructions` then iterates over the same regex but
  requires `Phase \d+` — slight inconsistency (`\d` vs `\d+`) between
  the two functions; both find `Phase 12` but only the second one keeps
  `12` as the captured group (lines 192-197).

**Reproduction sketch**: A task file with one canonical `## Phase 1`
heading plus an accidental `## Phase 1 Recap` would yield 2 matches and
pass the gate even though there is functionally one phase.

**Confidence (own)**: 0.75.

---

### F-B-10: `_check_parallel_instructions` substring-matches keywords inside the lowercased section text — false positives on words like "batch_size" or "parallelize" in unrelated prose

**Severity (preliminary)**: LOW
**Pattern tags**: P3
**File:line**: `src/superclaude/cli/prd/gates.py:182-212`

**Evidence**:

```python
parallel_keywords = ["parallel", "concurrent", "simultaneously", "batch"]
...
section_text = content[start:end].lower()
if not any(kw in section_text for kw in parallel_keywords):
```

**Trace**:
- `"parallel" in section_text` is a substring test; "non-parallel",
  "parallelism", "anti-parallel", or even a code identifier
  `batch_size` in a code fence counts as parallel instructions.
- `"batch" in section_text` matches "batched", "batches", "batchnorm"
  (in ML phase content), or the literal word "batch" in a comment.
- This is a recall-tuned check that probably won't false-NEGATIVE, but
  trivially false-positives.

**Reproduction sketch**: A Phase 3 section that says
"Avoid parallelizing this; it must run sequentially" passes the gate
because `"parallel"` is a substring of `"parallelizing"`.

**Confidence (own)**: 0.75.

---

### F-B-11: Cross-reference — `_resolve_step_content` at executor.py:254-293 is incomplete relative to `GATE_CRITERIA` keys, which is what caused the observed "30 lines of NDJSON" symptom

**Severity (preliminary)**: HIGH (out of slice — defer to Agent A or executor owner)
**Pattern tags**: P1, P4, P6
**File:line**: `src/superclaude/cli/prd/executor.py:246-251` (`_STEP_ARTIFACT_FILES`)

**Evidence**:

```python
# executor.py:246
_STEP_ARTIFACT_FILES: dict[str, str] = {
    "parse-request": "parsed-request.json",
    "scope-discovery": "scope-discovery-raw.md",
    "research-notes": "research-notes.md",
    "sufficiency-review": "sufficiency-review.md",
}
```

**Trace**:
- `_resolve_step_content("build-task-file", …)` falls through to "no mapping
  → return ndjson_text" because `build-task-file` is missing from the
  registry. The gate then evaluates 30 lines of subprocess commentary
  instead of the 409-line file the agent actually wrote.
- Missing from `_STEP_ARTIFACT_FILES`: `build-task-file`, `verify-task-file`,
  `assembly`, `investigation`, `web-research`, `synthesis`, all QA steps.
- This is the proximate cause of the heavyweight halt. It is OUT of my
  slice (executor.py), but the gate-evaluation chain in my slice
  (`_evaluate_gate`) is the wrong layer to fix it — the content source
  selection sits in the executor. Flagging here so Agent A picks it up.

**Reproduction sketch**: Already reproduced by the failing run that
prompted this audit.

**Confidence (own)**: 0.95.

---

## Considered and rejected

- **Encoding / BOM handling in `_check_*` functions** — All checks take the
  raw `content: str` after `read_text(encoding="utf-8", errors="replace")`
  upstream; BOM would appear as a leading character but no check anchors
  with `^` at byte 0 in a way that would be broken by it. Not a defect.
- **`_safe_check` wrapper swallowing exceptions** — It returns the exception
  as a failure-string, which is the intended F-005 behaviour. Not a defect.
- **`enforcement_tier` typo risk** — `Literal["STRICT","STANDARD","LIGHT","EXEMPT"]`
  in `pipeline/models.py` enforces at typecheck time. Not a defect.
- **`_PRD_CRITICAL_SECTIONS` list completeness vs PRD template** — Out of
  slice (template ownership belongs to whoever owns
  `cli/prd/prompts.py` or the template files). Noted for Agent C/D.
- **`_check_suggested_phases_detail` "no later phases → return True"**
  short-circuit (gates.py:198) — that branch is for
  `_check_parallel_instructions`, not the suggested-phases check; verified
  by re-reading. Not a defect.
- **Race condition in `GATE_CRITERIA` mutation** — `GATE_CRITERIA` is
  module-level and never mutated at runtime (confirmed by grep for `=`
  assignment to `GATE_CRITERIA[` anywhere in `src/`). Not a defect — but
  it IS the structural reason `_tier_min_lines` has no obvious place to
  be wired in: the executor would have to either patch the dataclass or
  pass tier into `_evaluate_gate`. Deferring fix design.
- **`_check_no_placeholders` whole-word matches `\bTBD\b`** — fine; ITBD
  wouldn't match. Not a defect.
- **Empty `required_frontmatter_fields=[]` on most gates** — those entries
  are deliberately empty; the dead-code finding in F-B-2 only matters for
  the four gates that DO populate it (`research-notes`, `build-task-file`,
  `assembly`).
