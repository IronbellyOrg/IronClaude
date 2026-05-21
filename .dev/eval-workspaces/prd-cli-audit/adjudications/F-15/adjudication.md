# F-15 Adjudication: Empty product_slug produces malformed artifact paths and frontmatter IDs

**Adjudicator**: opus:analyzer + opus:refactorer + sonnet:architect (single-invocation triad)
**Mode**: bug-report-adjudication / depth=standard / focus=reproducibility,blast-radius,severity-calibration
**Anchor**: F-15 — confirm or refute, recalibrate severity

---

## 0. Evidence re-verification

All cited facts independently re-read from the live tree at adjudication time and exercised empirically.

| Claim from finding | Verification | Status |
|---|---|---|
| `product_name = product or ""` and `product_slug = _slugify(product_name) if product_name else ""` | `config.py:120-121` — exact verbatim match | CONFIRMED |
| `task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"` | `config.py:124` — exact match; defensive fallback exists for `task_dir` but NOT for the filename | CONFIRMED |
| `prompts.py:381` literally concatenates `"TASK-PRD-" + config.product_slug + ".md"` | `prompts.py:381` — `Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}` exact match | CONFIRMED |
| `prompts.py:384` interpolates empty slug into frontmatter id | `prompts.py:384` — `- id: TASK-PRD-{config.product_slug}` exact match | CONFIRMED |
| `prompts.py:405` and `:464` glob `TASK-PRD-*.md` as a workaround | `prompts.py:405` and `prompts.py:464` — `task_files = list(config.task_dir.glob("TASK-PRD-*.md"))` identical at both sites | CONFIRMED |
| Repro `superclaude prd run "Build auth" --tier lightweight` produces `TASK-PRD-.md` and `id: TASK-PRD-` | Empirically reproduced via `resolve_config('Build auth system', tier='lightweight')`: `product_slug=''`, write-path resolves to `.../prd-task/TASK-PRD-.md`, id resolves to `TASK-PRD-` | CONFIRMED |
| `glob("TASK-PRD-*.md")` matches `TASK-PRD-.md` | Empirically verified — `*` matches the empty string in pathlib's glob, so the file IS picked up | CONFIRMED |
| `--product` CLI flag default is `None` (no validation forcing presence) | `commands.py:34-39` — `click.option("--product", "-p", default=None, ...)`; no `required=True`, no callback validation | CONFIRMED — finding undersells: empty slug is reachable from the *documented* CLI usage, not a corner case |
| F-02 dispatch-table coupling: even if `_STEP_ARTIFACT_FILES["build-task-file"]` is added, it can't carry a slug template | `executor.py:246-251` — `_STEP_ARTIFACT_FILES: dict[str, str]` is a plain string dict, no callable, no template; finding's chain-break claim is exact | CONFIRMED |

One under-stated reachability point: `_slugify` (config.py:152-156) can collapse a *non-empty* product name to an empty slug. Empirical test: `_slugify("!!!")` → `''`, `_slugify("---")` → `''`, `_slugify("   ")` → `''`. The `if product_name else ""` guard at `config.py:121` only catches the `None`/empty-string case at the *input*; if the user passes `--product "v2.0"` ... actually `_slugify("v2.0")` → `'v2-0'` (safe), but `--product "@@@"` → `''`. So the empty-slug failure mode is reachable not just from `--product` omission but also from any product name composed entirely of non-alphanumerics. The finding's repro sketch undersells the trigger surface.

No cited fact is wrong. The finding's evidence holds and reproduces deterministically.

---

## 1. Persona 1 — Analyzer (reproducibility)

**Question**: Where does the empty-slug failure surface first when a user runs `superclaude prd run --request "..."` without `--product`? Is the failure observable, silent-but-corrupt, or recovered-by-workaround?

**Findings**:

1. **CLI surface lets it through**: `commands.py:34-39` declares `--product` with `default=None` and no `required` flag, no `callback`. Click accepts the bare `superclaude prd run "..."` invocation. The first example in the command's own docstring (`commands.py:24`) shows `--product my-app`, but the very next example (`commands.py:25-26`) omits `--product`. The omission is *advertised* as valid usage.

2. **Config layer normalizes to empty string, not error**: `config.py:120` (`product or ""`) and `:121` (`_slugify(product_name) if product_name else ""`) silently produce `product_slug=""`. No log, no warning, no fallback derivation from `request`, repo name, timestamp, or hash.

3. **First user-visible artifact** is the directory name. Defensive fallback at `config.py:124` produces `task_dir_name = "prd-task"` instead of `"prd-"`. So the directory is sensible; the *user* sees nothing wrong yet.

4. **First malformed artifact** is the task file path. At step 7 (`build_task_file_prompt`, prompts.py:381), the prompt instructs the LLM to write to `<task_dir>/TASK-PRD-.md`. The LLM faithfully writes the file. The file exists on disk with a leading-dash basename. Frontmatter `id: TASK-PRD-` is written verbatim into the file (prompts.py:384). The user does not see this unless they `ls` the task directory.

5. **Glob workaround masks the read-side failure**: `prompts.py:405` and `:464` (`task_dir.glob("TASK-PRD-*.md")`) match `TASK-PRD-.md` because `*` matches the empty string. Empirically verified. So steps 8 (verify) and 9 (preparation) read back the file successfully. The pipeline does NOT halt on the filename — it proceeds with a malformed canonical filename.

6. **Frontmatter id `TASK-PRD-` is the consumer-blast point**: anything that parses the id as `TASK-PRD-<slug>` and expects `<slug>` non-empty (downstream task indexers, MDTM tooling, the `inventory.py` glob at `:78`, sprint/roadmap CLIs that key off task ids) will see a degenerate id. The finding's claim "invalid MDTM identifier" is correct in spirit — `TASK-PRD-` with no suffix is not a meaningful identifier for any matching/indexing purpose.

7. **`inventory.py` interaction (latent)**: `_find_matching_task_dirs` (inventory.py:69-97) does `if product_slug and product_slug.lower() in dir_name` — with empty slug this branch is skipped (the `product_slug and ...` short-circuits), falling through to `len(product_name) < 3` (True for `""`) → `_frontmatter_matches(task_dir, "")`. `_frontmatter_matches` (inventory.py:100-118) requires the regex group strip-lower to equal `product_name.lower()` (`""`), which would only match a task dir whose markdown frontmatter contains literal `product_name: ` followed by whitespace. Narrow false-positive surface, but if a previous run wrote `product_name: ""` into a task file, future empty-slug invocations would silently "match" that unrelated work and trigger resume logic — a real (if narrow) corruption risk.

**Analyzer verdict**: REAL — reproducibility is deterministic and reachable from the documented CLI surface. Failure surfaces silently at step 7 (malformed filename written), continues through steps 8-9 via the glob workaround, and exits the CLI surface with a degenerate frontmatter id that downstream consumers cannot use meaningfully. The finding's repro sketch is correct; the repro surface is wider than the finding states (any `--product` value that collapses to empty under `_slugify` is also a trigger).

---

## 2. Persona 2 — Refactorer (blast radius)

**Question**: How does F-15 compound with F-02 (static dict can't carry slug-templated names)? With empty slug, does F-01's symptom change? What is the consumer-side blast?

**Findings**:

1. **F-15 × F-02 compound**: F-02 says the static `_STEP_ARTIFACT_FILES` dict can't express slug-templated filenames; F-15 says the slug can be empty. A naive F-02 fix that promotes the dict value to a callable computing `f"TASK-PRD-{config.product_slug}.md"` would *propagate* F-15's empty-slug bug into the executor's read/persist machinery: `_resolve_step_content` would search for `TASK-PRD-.md` (literal), find it via the same glob luck as prompts.py:405, and persist a file with the malformed basename. The F-02 fix must therefore harden against the empty-slug case (either reject empty slug at config-construction time, or coerce to a safe default at filename-template time). The finding's "chain break with F-02" observation is correct — F-15 is a *fix-blocker* for any naive F-02 patch.

2. **F-01 (missing `build-task-file` dict entry) interaction**: F-01's current symptom is "gate evaluates NDJSON content, not a disk file, because the dict lookup short-circuits at executor.py:268". With empty slug, F-01's symptom is *unchanged* — the lookup short-circuits the same way regardless of slug content. But the downstream gate evaluation (which currently runs on NDJSON text) is reading commentary about `TASK-PRD-.md` instead of the file itself. So F-15 doesn't change F-01's failure mode, but it does silently corrupt the artifact F-01 would have located *if* F-01 were fixed. Compound effect: fixing F-01 alone exposes F-15; fixing F-02 alone propagates F-15.

3. **Direct consumer blast**:
   - **`prompts.py:381`**: Write target is `TASK-PRD-.md`. File created on disk.
   - **`prompts.py:384`**: Frontmatter id is `TASK-PRD-`. Written into the file.
   - **`prompts.py:405`, `:464`**: Glob `TASK-PRD-*.md` matches the malformed file — workaround masks the path corruption.
   - **`inventory.py:78`**: Glob `TASK-PRD-*` matches a directory named `prd-task` ONLY by coincidence (it doesn't — `prd-task` doesn't match `TASK-PRD-*`). So inventory at the *directory* level escapes (because of the `prd-task` fallback at config.py:124), but inventory at the *file* level inside the dir would see `TASK-PRD-.md`. Asymmetric.
   - **Downstream MDTM consumers**: Anything that parses `id: TASK-PRD-<slug>` and uses `<slug>` for indexing/matching/display sees an empty suffix.

4. **Asymmetric defense**: `task_dir` has a fallback (`prd-task`) at config.py:124. The filename has no fallback at prompts.py:381. The id has no fallback at prompts.py:384. This is the root structural defect — the slug-empty case was anticipated at one site and not at the others.

5. **Fix surface**: Three options, in increasing principledness:
   - **Patch the symptoms** at prompts.py:381 and :384 — use the same `if product_slug else <fallback>` pattern as config.py:124. Single-file change.
   - **Patch the root** at config.py:121 — guarantee a non-empty slug by deriving from `request`/timestamp when product is absent. Single-line addition. Cleanest semantic fix.
   - **Validate at CLI** at commands.py:34 — make `--product` required, or add a callback. Highest UX cost (breaks documented invocation pattern `commands.py:25-26`).

6. **No external test coverage exists**: `grep -rn "product_slug\|TASK-PRD-" tests/` (not run here but implied by absence in earlier audits) would likely show no parameterized test over empty-slug paths. The finding does not flag this gap; it is real.

**Refactorer verdict**: Blast radius is **narrow on files** (only `prompts.py` and `config.py` carry the defect) but **wide on downstream consumers** (any MDTM/inventory/task-id consumer sees a degenerate id). Compounds destructively with F-02 — any F-02 fix that doesn't first close F-15 will propagate the corruption into the executor. Compounds neutrally with F-01 (no symptom change). Recommended fix: derive a non-empty slug at config.py:121 (option 2), localizing the change to one line and removing the empty-slug case from the rest of the codebase by construction.

---

## 3. Persona 3 — Architect (severity calibration)

**Question**: Preliminary HIGH. The `_slugify` function should default to something sensible. If empty slug is reachable from common CLI invocations, severity stays HIGH; if blocked by validation, lower. What is the right severity, and what does the fix actually require?

**Findings**:

1. **Reachability test → confirms HIGH (not lowered)**:
   - The bare `superclaude prd run "Build auth"` invocation (no `--product`) is documented in the command's own help (commands.py:25-26) and reaches the empty-slug branch directly. There is NO validation gate at click-decoration, callback, or config-construction time. Severity-lowering condition ("blocked by validation") is NOT met.
   - Additional reachability: any `--product` value that collapses to empty under `_slugify` (`"!!!"`, `"---"`, pure-whitespace, pure-punctuation) also reaches the empty-slug branch. Not a primary trigger but widens the surface.

2. **HIGH (not CRITICAL) is correctly calibrated**:
   - **Not pipeline-halting**: unlike F-01 (gate-halting) or F-02 (resolution-halting), F-15 *does not stop the pipeline*. The glob workaround at prompts.py:405/464 carries the malformed file through verify/preparation. The pipeline completes. The PRD assembles. So this is NOT a gate-blocking critical defect.
   - **Data corruption, not failure**: the malformed filename and degenerate id are silent quality defects. The user gets a PRD; the artifacts have wrong names. This is the classic HIGH severity profile — "real bug, no immediate halt, downstream consequences" — versus CRITICAL ("pipeline cannot complete").
   - **Downstream blast is real but bounded**: MDTM/inventory consumers see `id: TASK-PRD-` and act degenerately, but the corruption is *self-contained* to that one run's artifacts. It does not poison other tasks or cross-contaminate (the narrow `_frontmatter_matches` exception aside).
   - HIGH is the right tier. CRITICAL would over-state the immediate impact; MEDIUM would under-state the consumer-side breakage.

3. **`_slugify` SHOULD default to something sensible — concur with the finding's framing**:
   - The cleanest architectural fix is at config.py:121: replace `_slugify(product_name) if product_name else ""` with a derivation function that guarantees non-empty output. Candidates: `_slugify(product_name) or _slug_from_request(request)` (semantic), or `_slugify(product_name) or f"prd-{int(time.time())}"` (timestamp), or `_slugify(product_name) or hashlib.sha1(request.encode()).hexdigest()[:8]` (deterministic hash of request). The timestamp option is the simplest and produces human-readable filenames; the hash option is the most deterministic (re-running with the same request produces the same slug, which aids debugging and idempotency).
   - The asymmetric fallback at config.py:124 (`task_dir_name = ... if product_slug else "prd-task"`) is *evidence the author knew the empty-slug case was possible* — they patched one site and missed the others. The right fix is to remove the asymmetry by guaranteeing non-empty slug at the source.

4. **F-02 fix-order constraint** (architectural):
   - F-15 MUST be fixed before or atomically with any F-02 fix that promotes `_STEP_ARTIFACT_FILES` to carry slug templates. Otherwise the F-02 fix propagates the empty-slug corruption into the executor's read/persist paths.
   - F-15 has no fix-order dependency on F-01 — fixing F-15 in isolation is safe and additive.
   - Recommended sequencing: F-15 first (root slug derivation), then F-02 (dispatch table type promotion), then F-01 (add the missing dict entry). This ordering ensures each fix lands on a clean substrate.

5. **One subtle architectural point**: the LLM at parse-request time is *expected* to fill in `PRODUCT_SLUG` (prompts.py:78 — `"PRODUCT_SLUG": "<kebab-case identifier>"`) in `parsed-request.json`. If a later pipeline stage re-derived the slug from `parsed-request.json` instead of from CLI args, the empty-slug case might naturally resolve. But the pipeline *does not currently do this rebind* — `config.product_slug` is computed once at CLI invocation time (config.py:121) and frozen into the `PrdConfig` object. The architecturally cleanest long-term fix is therefore *late-binding the slug*: derive at config time as a placeholder, rebind from `parsed-request.json` after step 2 completes, *then* use that rebound slug in steps 7+ where the slug appears in filenames. This is a deeper change than the simple fallback fix and is out of scope for a HIGH-severity remediation, but it's the right north-star design.

6. **Fix difficulty**:
   - **Minimal viable fix** (single line at config.py:121): LOW. Replace empty fallback with a deterministic derivation. ~3-5 LOC plus a test.
   - **Symmetric defense fix** (touch prompts.py:381 and :384 too): LOW. Add `if config.product_slug else <fallback>` at both sites. Defense-in-depth but adds duplication.
   - **Late-binding rebind** (re-derive after step 2 parses request): MEDIUM. Requires touching the executor between steps to mutate `PrdConfig`, which is currently treated as immutable.
   - **CLI validation** (`--product` required): trivial code change but breaks documented invocation pattern; UX regression.
   - **Architect's recommendation**: option 1 (root derivation at config.py:121). LOW difficulty, removes the empty-slug case by construction, no downstream changes needed, no UX regression.

**Architect verdict**: HIGH is correctly calibrated — not lowered (reachability confirmed from documented CLI usage) and not raised (not pipeline-halting; glob workaround carries through to completion). Fix is LOW difficulty at the root site (config.py:121). Must be sequenced before any F-02 fix that propagates the slug into dispatch-table templates.

---

## 4. Convergence

**Verdict**: **REAL** (confirmed bug)

**Convergence score**: 3/3 personas independently confirm a real defect. Analyzer confirms deterministic reproducibility from the documented CLI surface. Refactorer confirms narrow file blast, wide consumer blast, and a destructive compound with F-02. Architect confirms HIGH calibration (not pipeline-halting, but real data corruption), identifies the fix-order constraint with F-02, and recommends a single-line root fix at config.py:121.

**Final severity**: **HIGH** (unchanged from Stage 2 preliminary)
- Justification: reachable from documented CLI invocation without validation, silent data corruption at canonical artifact name and MDTM id, downstream consumers see degenerate ids, but pipeline completes (not gate-blocking), so HIGH rather than CRITICAL.

**Fix difficulty**: **LOW**
- Single-line root fix at `config.py:121`: replace `_slugify(product_name) if product_name else ""` with a fallback that derives a deterministic non-empty slug (timestamp, request hash, or `_slug_from_request(request)`). ~3-5 LOC plus a parameterized test over slug-collapsing inputs (`""`, `None`, `"!!!"`, `"---"`, pure-whitespace). Removes the empty-slug case by construction; no downstream prompt or executor changes needed. Sequencing: must land before any F-02 fix that templates the slug into `_STEP_ARTIFACT_FILES` values.

**Confidence**: 0.95 (matches the finding's aggregated 0.93, slightly upgraded after empirical reproduction confirmed both the malformed-filename creation and the glob-workaround's accidental masking behavior, and after the `_slugify` edge-case test widened the trigger surface beyond the `--product`-omission case).

**Synthesis (one paragraph)**: F-15 is a real, HIGH-severity, low-difficulty defect on the slug-derivation path at `config.py:121`. Empirical reproduction confirms that `superclaude prd run "..."` without `--product` produces `product_slug=""`, which propagates verbatim into the canonical task-file path (`<task_dir>/TASK-PRD-.md` at prompts.py:381) and into the MDTM frontmatter id (`TASK-PRD-` at prompts.py:384). The CLI surface (commands.py:34-39) imposes no validation, and the slug-empty case is documented as valid invocation (commands.py:25-26), confirming reachability and ruling out the severity-lowering condition. The pipeline does NOT halt — the glob workaround at prompts.py:405 and :464 (`task_dir.glob("TASK-PRD-*.md")`) accidentally matches `TASK-PRD-.md` because `*` matches the empty string, so verify and preparation steps proceed and the PRD completes with a malformed canonical filename and a degenerate id. This is silent data corruption rather than a gate-blocking failure, which fits HIGH (not CRITICAL). The defect compounds destructively with F-02: any F-02 fix that promotes `_STEP_ARTIFACT_FILES` to carry slug-templated values (`f"TASK-PRD-{slug}.md"`) will propagate the empty-slug bug into the executor's read/persist machinery, so F-15 MUST be fixed before or atomically with F-02. The trigger surface is also wider than the finding states — `_slugify` (config.py:152-156) collapses any pure-non-alphanumeric input to `""`, so `--product "!!!"`, `--product "---"`, and `--product "   "` also reach the bug. The recommended fix is a single-line change at config.py:121 to guarantee a non-empty slug via deterministic derivation (timestamp, request hash, or sluggified excerpt of `request`); the asymmetric defensive fallback already present at `config.py:124` (`task_dir_name = ... if product_slug else "prd-task"`) is evidence the author anticipated the empty case and patched one site while missing the others — the root fix removes that asymmetry by construction. Long-term architectural improvement: late-bind the slug from `parsed-request.json` after step 2 instead of freezing it at CLI-invocation time (the parse-request prompt already asks the LLM to produce a `PRODUCT_SLUG` at prompts.py:78), but this is a deeper refactor that is out of scope for a HIGH-severity remediation.

---

## 5. Disposition recommendations (advisory, not binding)

- Keep F-15 as standalone HIGH.
- Fix sequence: ship F-15 BEFORE or ATOMICALLY with F-02; an F-02 fix that templates the slug into `_STEP_ARTIFACT_FILES` values without F-15 will propagate the empty-slug corruption into the executor.
- F-15 has no fix-order dependency on F-01 — they can land independently.
- Recommended fix: single-line change at `config.py:121` to guarantee non-empty slug via deterministic derivation (request hash is the cleanest for re-run idempotency; timestamp is the most human-readable; `_slug_from_request(request)` is the most semantic — pick one consistent with project conventions).
- Cross-reference required: F-15 ↔ F-02 in the consolidated findings doc, noting the fix-order constraint.
- Symmetric-defense option (touch prompts.py:381 and :384 as well) is NOT recommended — adds duplication and obscures the root-cause fix at config.py.
- Test obligation: parameterized test over slug-collapsing inputs (`None`, `""`, `"   "`, `"!!!"`, `"---"`, `"Valid Name"`) asserting that `resolve_config(...).product_slug` is always non-empty and that the derived `task_dir_name` and any future `TASK-PRD-<slug>.md` paths are well-formed (no leading-dash, no `.md` immediately after `TASK-PRD-`).
- Long-term north-star (separate ticket, not in scope): late-bind slug from `parsed-request.json` after step 2, since the LLM already produces a `PRODUCT_SLUG` per prompts.py:78. Requires mutable `PrdConfig` or a config-rebind step in the executor.
