# Adjudication: F-21 — Dual slug sources with no reconciliation

**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-21-dual-slug-sources-no-reconciliation.md`
**Preliminary severity**: MEDIUM
**Mode**: B (reproducibility / blast-radius / severity-calibration)

---

## Re-verification (file:line evidence)

### Writer A — CLI-derived slug
`src/superclaude/cli/prd/config.py:120-125`:

```python
product_name = product or ""
product_slug = _slugify(product_name) if product_name else ""

# Task directory: derived from output_path + product_slug (or 'prd-task')
task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"
task_dir = output_path / task_dir_name
```

`_slugify` at `src/superclaude/cli/prd/config.py:152-156` lowercases, kebab-substitutes `[^a-z0-9]+`, strips edge dashes.

### Writer B — LLM-emitted slug
`src/superclaude/cli/prd/prompts.py:73-84` (parse-request prompt to LLM):

```text
Extract these fields and return valid JSON:
{
  "PRODUCT_NAME": "<human-readable product name>",
  "PRODUCT_SLUG": "<kebab-case identifier>",
  ...
}
```

Output is persisted as `parsed-request.json` (executor.py:247 confirms artifact name).

### Reconciler — searched, none exists
`grep -rn "reconcile\|reconciliation\|slug.*match\|slug.*compare" src/superclaude/cli/prd/` returns **zero hits**. No code path compares `config.product_slug` against `parsed["PRODUCT_SLUG"]`.

### Downstream consumer map (the load-bearing detail)

`grep -rn "PRODUCT_SLUG" src/superclaude/cli/prd/` returns only **three sites**:

| Site | Role |
|------|------|
| `src/superclaude/cli/prd/prompts.py:78` | Writer (prompt asks LLM to emit it) |
| `src/superclaude/cli/prd/gates.py:84-85` | Presence-only gate (`required = ["GOAL", "PRODUCT_SLUG", "PRD_SCOPE", "SCENARIO"]`) — checks the key *exists*, never reads the value |
| (no third reader) | — |

By contrast, **every functional downstream consumer reads `config.product_slug`** (the CLI-derived value):

- `src/superclaude/cli/prd/config.py:124` — `task_dir_name` directory
- `src/superclaude/cli/prd/prompts.py:381` — task file write path `TASK-PRD-{config.product_slug}.md`
- `src/superclaude/cli/prd/prompts.py:384` — frontmatter `id: TASK-PRD-{config.product_slug}`
- `src/superclaude/cli/prd/inventory.py:46,84` — resume-matching (`product_slug.lower() in dir_name`)
- `src/superclaude/cli/prd/models.py:179` — `PrdConfig.product_slug` field

Other `parsed-request.json` keys (`GOAL`, `PRODUCT_NAME`, `SCENARIO`, `WHERE`, `PRD_SCOPE`) **are** read downstream (e.g. `prompts.py:110-129`, `195-225`). `PRODUCT_SLUG` is the only key that is written, gated for presence, then never consumed.

**Divergence-winner conclusion**: CLI slug always wins. The LLM-emitted `PRODUCT_SLUG` is *dead data* in the current pipeline.

---

## Persona 1 — Analyzer (reproducibility)

**Likelihood the two slugs diverge**: HIGH per invocation when both inputs are present.

- `_slugify("User Auth Module")` → `user-auth-module` (deterministic, predictable).
- LLM prompt at `prompts.py:73-84` says "kebab-case identifier" with zero algorithmic constraint. It will routinely emit `user-auth`, `auth-module`, `userauth`, `auth`, or paraphrase the goal entirely. Even with `--product` echoed in the user request, LLM compression/abbreviation is statistically near-certain on multi-word names.
- For single-word lowercase products (`auth`, `billing`), divergence drops to noise — the LLM and `_slugify` will agree by coincidence.

**Trivial-vs-semantic split**:
- **Trivial typo** (`user-auth-module` vs `user_auth_module`): rare — LLM follows the kebab-case instruction; punctuation drift is the lower-probability failure.
- **Semantic mismatch** (`user-auth-module` vs `auth`): common — LLM editorializes to a shorter "natural" slug. This is the dominant divergence mode.

**Reproduction (from finding) is sound**: `superclaude prd run "Build auth for v2" --product "User Auth Module"` → `config.product_slug = "user-auth-module"`, `parsed["PRODUCT_SLUG"]` likely `auth` or `user-auth`. Confirmed by static reading of writer A and writer B; no runtime needed.

**Reproducibility score**: HIGH (deterministic CLI side + high-variance LLM side = divergence on most multi-word `--product` invocations).

---

## Persona 2 — Refactorer (blast radius)

**Direct blast radius**: NARROW.

The downstream-consumer audit (above) shows that **no functional code reads `parsed["PRODUCT_SLUG"]`**. Every artifact path, frontmatter id, and inventory resume-match goes through `config.product_slug`. So today, divergence produces:

- A `parsed-request.json` whose `PRODUCT_SLUG` cosmetically disagrees with the surrounding `task_dir` name and `TASK-PRD-*.md` filename.
- No broken file resolution, no mis-routed writes, no inventory false-negatives, no gate failures (the gate at `gates.py:84-85` only checks *presence*, not consistency).

**Pattern-level blast radius — related dual-source defects in the pipeline**:

Searching for the same "CLI value + LLM-re-extracted value, no reconciler" pattern:

- `PRODUCT_NAME` (prompts.py:77) vs `config.product_name` (models.py:178, config.py:120). Same shape: both written, prompts at `prompts.py:205, 224, 385` read **`parsed.get("PRODUCT_NAME", "Unknown")`** (LLM wins) while `prompts.py:385` writes frontmatter `title: Create PRD for {config.product_name}` (CLI wins). This is a **second, more dangerous instance of the same defect** — divergence here means the frontmatter `title` and research-notes header disagree.
- `PRD_SCOPE` (prompts.py:79) and `SCENARIO` (prompts.py:80): LLM-only, no CLI counterpart — not dual-source.
- `WHERE` (prompts.py:81) vs `config.where` (models.py:180, populated from `--where`): same dual-source pattern. `prompts.py:112` reads `parsed["WHERE"]` (LLM wins) but `config.where` is also stored on the config object — needs separate audit to confirm whether `config.where` is consumed anywhere.
- `TIER_RECOMMENDATION` (prompts.py:83) vs `config.tier`: LLM emits an *advisory* tier, `config.tier` is the authoritative resolved tier (prompts.py:208, 221 read `config.tier`). This one is intentional and documented as "recommendation," so probably not a defect — but it confirms the pattern is endemic.

**Net pattern verdict**: F-21 is the **least dangerous** instance of a recurring dual-source-of-truth pattern. `PRODUCT_NAME` is the same defect but actively load-bearing (LLM value wins in user-visible prompt text while CLI value wins in frontmatter), and deserves its own finding if it doesn't already have one.

**Blast-radius score**: NARROW for F-21 in isolation; the pattern itself is MEDIUM-WIDE.

---

## Persona 3 — Architect (severity calibration)

The finding's preliminary MEDIUM rests on the framing "some prompts cite the CLI slug, others cite the parsed slug." Re-verification falsifies that framing for `PRODUCT_SLUG` specifically: **no prompt or downstream module cites `parsed["PRODUCT_SLUG"]`**. The only consumer is the presence-check gate.

Calibration matrix:

| Scenario | Severity implication |
|---|---|
| LLM extraction silently overrides CLI (claimed risk) | Would be HIGH — surprise dir/filename divergence |
| CLI always wins, LLM extraction wasted (actual state) | LOW — pure dead data; correctness preserved, work wasted |
| Both wins inconsistently across consumers | MEDIUM — the finding's framing |

The actual state is row 2: the LLM is being asked to produce a value that is never read. This is a **prompt-economy / least-astonishment defect**, not a correctness defect. Costs:

1. **Token waste** — every parse-request invocation budgets output for `PRODUCT_SLUG`.
2. **False-coupling signal** — the gate at `gates.py:85` requires `PRODUCT_SLUG`, implying downstream dependence that does not exist. Future maintainers reading the gate will reasonably assume the value matters and may add a consumer that reads `parsed["PRODUCT_SLUG"]`, at which point the latent divergence becomes a live bug.
3. **Documentation lie** — the parse-request prompt advertises slug extraction as a primary output; readers of the prompt will assume the slug is authoritative.

The **landmine framing** is the right one: F-21 is not currently broken, but it is wired to break the moment anyone "fixes" the missing-consumer side without first deciding which slug is canonical.

**Recalibrated severity**: **LOW-MEDIUM** (downgrade from preliminary MEDIUM).
- LOW on current-behavior correctness.
- MEDIUM on latent-defect / maintenance-trap dimension.
- Compromise: **LOW-MEDIUM**, with explicit note that the related `PRODUCT_NAME` instance (same pattern, actively load-bearing) should be filed separately if not already covered.

---

## Convergence

**Verdict**: VALID finding, **recalibrated**. The defect is real and accurately localized, but the preliminary severity over-states current-behavior impact and under-states the maintenance-trap dimension. The framing "LLM extraction silently overrides CLI" is not what is happening today; the actual state is "LLM extraction is dead data, gated for presence, primed to become divergence the moment someone adds a consumer."

**Convergence score**: 0.85
- All three personas agree the defect exists and that no reconciler exists.
- Disagreement only on severity wording, resolved by splitting into current-impact (LOW) and latent-impact (MEDIUM).
- Independent corroboration via downstream-consumer grep removes ambiguity from the original finding's "Impact depends on downstream readers not exhaustively traced" hedge (confidence 0.80 → effectively 0.95 after re-verification).

**Final severity**: **LOW-MEDIUM** (downgrade from MEDIUM)
- Current functional impact: LOW
- Latent / maintenance-trap impact: MEDIUM
- Pattern-level impact (counting sibling defects like `PRODUCT_NAME`): MEDIUM-HIGH but belongs to separate findings

**Fix difficulty**: **LOW** (1-2 hours)

Three viable fixes, pick one:

1. **Remove the dead field** (simplest): drop `PRODUCT_SLUG` from the parse-request prompt (`prompts.py:78`) and from the gate's required list (`gates.py:85`). Zero downstream consumers, zero behavior change. ~5 LOC, ~5 minutes.
2. **Reconcile and warn**: after parse-request completes, compare `parsed["PRODUCT_SLUG"]` against `config.product_slug`; on mismatch, log a warning and overwrite `parsed["PRODUCT_SLUG"]` with the CLI value. Preserves the LLM signal for future use but enforces CLI-wins policy. ~15 LOC in executor.py post parse-request step.
3. **Make LLM-only when CLI omitted**: when `--product` is not provided, accept `parsed["PRODUCT_SLUG"]` as authoritative and rebuild `task_dir` from it (currently `task_dir` falls back to `prd-task` literal at config.py:124, which is itself a UX paper-cut). ~25 LOC, needs an executor hook between parse-request and any artifact write.

Recommendation: **Option 1** unless there is a documented future need for the LLM slug. The prompt-economy and least-astonishment wins are immediate, and removing the gate field eliminates the future-maintainer landmine.

**Synthesis**:

F-21 is a genuine dual-source-of-truth defect with a *latent* rather than *current* failure mode. The CLI slug is the de-facto canonical source; the LLM slug is dead data gated for presence by `gates.py:84-85`. The finding's reproduction sketch is correct, but its impact framing ("some prompts cite the CLI slug, others cite the parsed slug") is not currently true for `PRODUCT_SLUG` — it *is* true for the sibling field `PRODUCT_NAME` (prompts.py:205, 224, 385), which should be a separate finding if not already filed. Recommended fix: remove `PRODUCT_SLUG` from the parse-request prompt and the gate, eliminating both the wasted LLM work and the latent maintenance trap.

---

## Artifacts cited

- `src/superclaude/cli/prd/config.py:120-125, 152-156`
- `src/superclaude/cli/prd/prompts.py:73-84, 110-129, 195-225, 381-388`
- `src/superclaude/cli/prd/gates.py:83-99`
- `src/superclaude/cli/prd/inventory.py:40-97`
- `src/superclaude/cli/prd/models.py:178-180`
- `src/superclaude/cli/prd/executor.py:247`
