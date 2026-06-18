# KNOWLEDGE.md — accumulated insights and debugging patterns

Project-level lessons captured during development. Add to this file when an
issue's root cause or fix is non-obvious enough that a future contributor
(or future you) would benefit from finding it documented.

Format per entry: short title, one-paragraph context, the rule/pattern,
and a pointer to the originating work (commit, tasklist, RCA).

---

## Freshness system insights (2026-05-13, freshness-system v1)

Captured during the freshness-system tasklist (`.dev/releases/current/freshness-system/`).
Each item below cost ≥30 minutes of debugging — log them now so the next person
doesn't re-pay.

### F1 — Claude Code `FileChanged` is not a filesystem watcher

**Context:** the `phase5.1-context-refresh-design.md` design assumed `FileChanged`
fired on any modification to any file, with a regex matcher. Live probing
(T02.05) captured zero events.

**Rule:** Per [official docs](https://code.claude.com/docs/en/hooks):

- Matcher is `|`-separated **literal filenames** in CWD (e.g., `.env|.envrc`).
  No regex. No globs. `*` ≠ "match all".
- Stdin fields are `file_path` (absolute) and `event` ("change"/"add"/"unlink"),
  not `path` and `change_type`.
- No decision control — FileChanged cannot block anything.
- Dynamic watching via `hookSpecificOutput.watchPaths`, documented for
  CwdChanged/FileChanged responses; unverified from other events.

If a freshness/watch design needs "every file Claude has Read," the only
documented approach is to emit `watchPaths` from the watch-emitting events.
Whether `PostToolUse(Read)` can also emit `watchPaths` is an open probe.

**Source:** `.dev/releases/current/freshness-system/artifacts/D-0008/probe-finding.md`.

### F2 — `grep -c . 2>/dev/null || echo 0` double-counts when nothing matches

**Context:** the UserPromptSubmit hook used this idiom to count entries in a
file. When the file was empty, grep printed `0` AND exited 1 (no matches),
triggering the OR which printed another `0`. The captured value was `0\n0`,
which broke `[ "$count" -gt 0 ]` arithmetic comparison.

**Rule:** Don't use `grep -c | exit-1 fallback`. Either:

```bash
count=$(grep -v '^$' file | wc -l | tr -d ' ')
[ -z "$count" ] && count=0
```

…or capture and validate:

```bash
count=$(grep -c . file 2>/dev/null)
[ -z "$count" ] && count=0
```

**Source:** Phase 2 dry-runs (`CP-P02-END.md` F1).

### F3 — `flock -w N <fd> || true` falls through to unlocked critical section

**Context:** the subagent counter and post-read tracker used `flock -w 1 9 || true`,
expecting that if the lock timed out we'd just skip. Reality: under
`xargs -P 10` contention, several invocations timed out on the 1s wait and
ran the critical section WITHOUT the lock, producing duplicate `tool_call_idx`
values and lost counter updates.

**Rule:** For microsecond-scale critical sections, drop the timeout and
fail-open only on flock binary absence:

```bash
flock <fd> 2>/dev/null || exit 0
```

This blocks indefinitely (no deadlock risk if critical section is brief),
or exits cleanly if `flock` itself isn't on the host (fail-open per NFR-3).

**Source:** Phase 2 concurrency tests (`CP-P02-END.md` F2).

### F4 — Counter-increment and counter-read must share one locked section

**Context:** `freshness-post-read.sh` initially incremented the tool-call-counter
inside a flocked subshell, exited the subshell, then re-read the counter outside
the lock to get the new value. Under `-P 20` parallelism, 4/100 reads got
duplicate `tool_call_idx` because another process incremented between the lock
release and the re-read.

**Rule:** Either do the whole "increment + use" inside one lock:

```bash
(
    flock 9
    new=$(($(cat $COUNTER) + 1))
    echo "$new" > $COUNTER
    # …use $new directly inside the lock, e.g. append to log…
)
```

…or write the locked-section's value to a per-PID tempfile and read it from
there outside the lock:

```bash
TMP=$(mktemp)
(
    flock 9
    new=$(($(cat $COUNTER) + 1))
    echo "$new" > $COUNTER
    echo "$new" > $TMP
)
NEW_IDX=$(cat $TMP)
rm -f $TMP
```

Validated at -P 20 (100 unique idx) and -P 40 (200 unique idx).

**Source:** Phase 2 concurrency stress (`CP-P02-END.md` F3, F4).

### F5 — Fresh Claude Code sessions have empty `reads.jsonl` per-session

**Context:** `freshness-pre-edit.sh` filters `reads.jsonl` by both `path` and
`session_id`. A new session has no rows for itself, so EVERY first-Edit-against-a-file
blocks with `no_prior_read` — even for files the agent created earlier in a
different session.

**Rule:** This is correct behavior (each session validates its own world view).
But it means:

- Workflow is "Read first, then Edit" for every file in every session, no
  exceptions.
- For brand-new files (target path doesn't exist), use Bash heredocs (`cat > new <<EOF`)
  — the gate doesn't run on Bash.

A future v1.5 refinement may "allow Write if target path doesn't exist on disk."
Tracked in `CHANGELOG.md` under "v1.5 work items".

**Source:** Multiple organic catches during this session's own work
(`CP-P05-T05.01.md` Addendum + F10).

---

## Adding new entries

When a debugging session takes >30 minutes and the root cause is non-obvious,
add an entry here in the same format. Keep entries terse — long-form lives in
the originating doc (RCA, checkpoint, finding). This file is a fast-lookup
table that points you AT the long-form when you hit a similar symptom.

Topical sections grow as the project does (e.g., `## MCP integration insights`,
`## Pytest plugin insights`).

---

## Fix B Merged — Anti-Instinct Gate Mechanism-Signature Refactor (2026-05-25)

**Problem framing.** `integration_contracts.py` previously conflated lexical
evidence (raw line text) with semantic mechanism identity (the integration
point itself). This produced three symptoms of one design flaw: over-capture
of bare "dispatch" mentions, per-evidence-line dedup that didn't collapse
semantically-identical contracts, and narrow FR-MOD2.7 coverage that required
literal mechanism-term substrings valid roadmaps may not contain. Per
merged-output.md §1, the fix was a single coherent abstraction, not three
patches.

**Key abstraction.** Introduced `mechanism_signature: tuple[str, frozenset[str]]`
on `IntegrationContract` — a normalized `(mechanism_kind, identifier_set)`
tuple that routes both deduplication and Layer 3 stem-fallback coverage
matching through the same semantic primitive. A new `_signature_subsumed`
helper collapses contracts whose `(mechanism, identifier-set)` is identical
or a subset of an already-seen signature with ≥1 shared identifier.

**Load-bearing detail.** The empty-identifier branch in `_signature_subsumed`
(`if not idents: return sig in seen`) preserves the existing
`test_duplicate_lines_deduplicated` test's exact-match semantics. Without
it, identical evidence lines lacking UPPER_SNAKE/PascalCase identifiers
would no longer dedup.

**Spec-vs-implementation deviations.** Two deviations from merged-output.md
verbatim were necessary because the spec was internally inconsistent in two
places: (1) `PROGRAMMATIC_RUNNERS` had to be added as an explicit alternation
to `DISPATCH_PATTERNS[0]` because `\bRUNNERS\b` and `\b_RUNNERS\b` don't
match inside `PROGRAMMATIC_RUNNERS` (no word boundary at `_`); without this
addition, `TestCliPortifyRegression.*` regressed despite §4 asserting they
would pass. (2) Bare `priority` had to be removed from both §2.2 extraction
and §2.4 Layer 1 `dispatch_family` regexes because Layer 1 matched
"Implement priority dispatch for logging events" and short-circuited before
Layer 3's identifier-overlap guard — directly contradicting t7's design
intent. Both deviations are documented in the task's deviation log.

**Documented limitation.** When a spec's context contains only
single-PascalCase identifiers like `Interactive`/`Bulk` that
`_extract_identifiers` doesn't capture (it requires UPPER_SNAKE
`[A-Z][A-Z0-9_]{2,}` or multi-cap `[A-Z][a-z]+(?:[A-Z][a-z]+)+`),
the Layer 3 identifier-overlap guard short-circuits to an "empty
set = match" branch. Out of scope for this fix; logged as a Follow-Up
Item per merged-output.md §6 secondary counter-argument.

**End-to-end target.** Live re-run against
`/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/{epics,roadmap}.md`
(BEFORE the Fix A workaround in roadmap.md is reverted) yielded
`total=5 uncovered=0` — confirming the merged Fix B alone is sufficient.

**Files touched:** src/superclaude/cli/roadmap/integration_contracts.py, tests/roadmap/test_integration_contracts.py

---

## obligation_scanner Layer 2 vs Layer 5 surface overlap (2026-05-29, TASK-RF-20260529-171029 FU-001)

**Context.** Captured during Layer 5 H3 subsection-context detector work. The task's T03.05 prescribed a Test 4 fixture `- Mitigation: replace the M1 stub with real transport by M5.` to verify the Layer 5 discharge-intent guard preserves HIGH severity inside Risk Assessment H3s. The test failed because the pre-existing Layer 2 `_NEGATION_PREFIX_RE` independently demoted the line to MEDIUM *before* Layer 5 ever ran — verified via Python trace: `_is_discharge_intent_line` True, `_is_descriptive_context` False (its own guard fires), but `_is_meta_context` True via the negation-prefix branch. Resolved via `/sc:adversarial --depth quick` Option A: rewrite the fixture to `- Mitigation: stub needs replacement with real transport by M5.` (canonical form from task overview line 28). Test passes with HIGH preserved.

**The rule.** When authoring a `tests/roadmap/test_obligation_scanner.py` fixture that targets a *specific* meta-context layer's guard (Layer 4 `_is_descriptive_context` discharge guard, Layer 5 `_is_demoted_h3` discharge guard, or any future similar layer), put the scaffold term BEFORE the discharge verb, not after. Use the canonical noun-form pattern `<term> needs <discharge-noun>` (e.g., `stub needs replacement`, `mock needs swap-out`) instead of the verb-form `<discharge-verb> the <term>` (e.g., `replace the stub`, `swap out the mock`). The verb-first form puts the discharge verb in the line PREFIX before the scaffold term, which trips `_NEGATION_PREFIX_RE` upstream and demotes via Layer 2 regardless of whether the layer-under-test would have fired.

**Why.** `_is_meta_context` walks the layers in this order: shell-cmd → risk-warning → gate-criteria → **negation-prefix (via `_NEGATION_PREFIX_RE.search(line[:term_start])`)** → table-cell-imperative → paren-phase-label → descriptive-context. The negation-prefix branch matches discharge verbs sitting BEFORE the scaffold term and treats them as meta-context indicators. Any test fixture that relies on a layer LATER in the cascade (Layer 4 / Layer 5) firing on a verb-prefix discharge sentence is structurally incapable of being exercised — Layer 2 wins.

**Load-bearing test convention.** Tests targeting layer-specific discharge guards MUST use the term-before-verb form. The task overview at task-file line 28 of TASK-RF-20260529-171029 already names "stub needs replacement" as the canonical example; future task templates (especially the BUILD_REQUEST templates for obligation_scanner test additions) should embed this convention in their prescribed-fixture sections.

**Files touched:** src/superclaude/cli/roadmap/obligation_scanner.py (Layer 5 surface), tests/roadmap/test_obligation_scanner.py (`TestLayer5H3SubsectionContext` + tightened e2e), .dev/tasks/to-do/TASK-RF-20260529-171029/ (deviation log + FU-001 origin)

---

## 2026-05-31: Roadmap Spec-Fidelity Validator — M{n}-D{nn} Tokenizer + Canonicalizer Fix (TASK-RF-20260531-044100)

### Symptom

The TUIBBS v1-MVP roadmap pipeline halted at the spec-fidelity convergence gate with FAIL: 51 HIGH + 3 MEDIUM signatures-dimension findings, all false positives. Each finding said either `Roadmap references ID 'D{nn}' not found in spec` (HIGH phantom_id) or `Roadmap ID 'D{nn}' canonicalizes to spec ID 'D{n}' (surface form differs)` (MEDIUM id_schema_drift) for D01..D54 — but those tokens never appear bare in the spec. They are always paired with a milestone prefix as M{n}-D{nn} (e.g., `M1-D01`, `M2-D03`).

### Root cause

Two coupled defects in the structural-signatures checker pipeline at `src/superclaude/cli/roadmap/`:

1. **Tokenizer (`spec_parser.py:_REQUIREMENT_PATTERNS`).** The D-family regex `\bD-?\d+\b` matched only the trailing `D\d+` portion of milestone-prefixed IDs like `M1-D01`, silently stripping the `M{n}-` prefix and emitting a bare-`D01` token. There was no MD-family pattern.
2. **Canonicalizer (`structural_checkers.py:_canonicalize_requirement_id`).** Given the resulting bare `D01`, `D02`, etc., the canonicalizer further collapsed zero-padded forms to `D1`, `D2`, etc. — so milestone-distinct deliverables (`M1-D01`, `M2-D01`, `M3-D01`, ...) all canonicalized to the single key `D1`, then failed to resolve against the spec namespace.

The canonical roadmap annotation at `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md:L657-L665` (Deliverable ID Convention heading + Validator note + Explicit non-references) explicitly states the authorial decision: full M{n}-D{nn} IS the canonical ID and the bare D{nn} suffixes MUST NOT be resolved against spec namespaces. The validator did not honor this annotation.

### Fix

Three coordinated edits per the design decisions captured in `phase-outputs/plans/a-track-patch-design.md`:

1. **D1 (spec_parser.py:324).** Add a new `"MD"` family pattern `\bM\d+-D-?\d+\b` ordered BEFORE the existing `"D"` entry so milestone-prefixed deliverable IDs surface as their own family. Add a post-process dedup in `extract_requirement_ids` so the bare-D regex does NOT re-match the trailing `D\d+` portion of an already-captured MD token.
2. **D2 (structural_checkers.py:_canonicalize_requirement_id).** Extend the canonicalizer with a leading branch for the MD family: preserve the M{n}- prefix and canonicalize only the trailing D{nn} portion (strip leading zeros on the deliverable index). Reuse existing `phantom_id` / `id_schema_drift` mismatch types — no new SEVERITY_RULES / MISMATCH_FILE_ROUTING / FIX_GUIDANCE_TEMPLATES entries.
3. **D3 (structural_checkers.py:_parse_explicit_non_references + check_signatures).** Add a module-level helper that reads the roadmap, finds the canonical `**Explicit non-references (do not resolve against spec):**` anchor, and parses the inline backtick-delimited token list (truncating at the boundary phrase `are **roadmap-internal` to avoid grabbing counter-example tokens). `check_signatures` calls this helper once at the top and skips emission for any roadmap-canonical token whose family is `D`/`G` AND whose raw form is in the allowlist, OR whose family is `MD` AND whose trailing D-suffix is in the allowlist.

### Verification

- Three new unit tests at `tests/roadmap/test_structural_checkers.py` (appended after the existing lock-the-fix 5-test block at lines 309-434; D4 backward-compat invariant honored):
  - `test_phantom_id_honors_explicit_non_references_for_milestone_d_ids` — M{n}-D{nn} multi-milestone IDs + allowlist → 0 findings (the canonical v1-MVP bug-trigger shape).
  - `test_phantom_id_backward_compatible_without_explicit_non_references` — legacy roadmaps without the allowlist annotation → existing canonicalization behavior preserved (D01↔D1 → 3 MEDIUM drift).
  - `test_phantom_id_bare_d_still_resolves_when_spec_uses_bare_d` — spec uses bare D7/D8 → matches D7 in roadmap; D9 still flagged HIGH phantom (false-negative regression check).
- All 13 `TestSignaturesChecker` tests + full `test_structural_checkers.py` file (61 passed, 1 pre-existing skip) GREEN.
- Integration: `superclaude roadmap run /config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/epics.md --output .dev/releases/current/v1-MVP/ --resume` against the same v1-MVP roadmap.md produced `fidelity_status=pass`, `spec-fidelity step=PASS`, `Final HIGH Count: 0`. roadmap.md sha256 preserved at `8c93b8f5157bcb73ede60ddd02aa4c8f6d1d928b927655cfaa2bf1c78a12b5e7`.

### Operational hazard for future devs

`superclaude` is installed via pipx, which performs a real-file copy of the package into a venv at `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/` (NOT an editable install). `pipx reinstall superclaude` is REQUIRED to propagate any IronClaude validator-source edit to the system binary. `make install` only refreshes the project's local `.venv/`; it does NOT touch the system-wide `superclaude` binary. The pipx install metadata at `/config/.local/share/pipx/venvs/superclaude/pipx_metadata.json` records `package_or_url: /config/workspace/IronClaude` — verify this before running `pipx reinstall` to ensure the cached source is correct.

Secondary hazard: the roadmap pipeline's `remediate` step may attempt cosmetic edits to roadmap.md when phantom_id findings persist — if those edits land on a file whose byte-identity is invariant (as in this case, where roadmap.md L657-L665 is the canonical anchor), they violate downstream contracts. The patched validator no longer emits the false positives that would trigger this cosmetic remediation.

### Historical reference

The C-track operational unblock for this issue used class waiver `V-PFX-1` registered in `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/deviation-registry.json` `waivers` array. After the durable A-track fix landed, V-PFX-1 was retired (status `RETIRED` with retirement metadata; entry preserved for audit). The authoring task is `/config/workspace/TUIBBS-scp/.dev/tasks/{to-do,done}/TASK-RF-20260531-044100/`.

**Files touched:** src/superclaude/cli/roadmap/spec_parser.py, src/superclaude/cli/roadmap/structural_checkers.py, tests/roadmap/test_structural_checkers.py

---

## 2026-06-18: Sprint Run 429 / Account-Exhaustion Recovery — re-route, never wait (TASK-RF-429-recovery-20260615-040144)

**Headline rule: a sprint 429 is recovered by RE-ROUTING, never by waiting.** A 429
from the routed CLIProxyAPI means ONE account hit its 5h/7d rate-limit window — the
pool holds ~8 accounts, and because every sprint subprocess launches with
`--no-session-persistence`, *a fresh subprocess is a new session is a new routing
decision is a chance at a different account*. So recovery spawns a fresh subprocess
(account rotation) or suggests a model-alias switch; it never sleeps/backs-off.

### Context

Before this work, a 429 silently halted the sprint (`SprintOutcome.HALTED` + `break`)
with no recovery. The detector + bounded re-spawn loop turn that into automatic
account rotation, with a clean halt + model-switch resume UX only when rotation can't help.

### The load-bearing rules (each cost real design/debugging time)

- **Detect on the LAST `{"type":"result"}` event's `is_error` + `api_error_status`,
  NEVER `subtype`.** A 429's `subtype` is `"success"` (the subtype-trap). The
  `api_retry` event's field is `error_status` (a *different* field — don't confuse it
  with the result event's `api_error_status`).
- **Four-way discrimination:** all-account cooldown (`/All credentials … cooling down
  via provider/`) → **halt + model switch on ANY attempt** (re-spawning is futile);
  single-account limit (`would exceed your account's rate limit`) → **re-spawn
  (rotate), bounded by the reset cap, then halt**; operation timeout
  (`api_error_status==null` + timeout body) and genuine task failure (no 429 body) →
  existing ladder, NO re-spawn.
- **`FAIL_PROVIDER_EXHAUSTED` is infra, not a product bug.** It's a *failure* (in
  `TaskStatus.is_failure` so resume re-runs it) but must NEVER trip the
  DiagnosticCollector/FailureClassifier product-bug bundle. Consequently
  `PhaseStatus.PROVIDER_EXHAUSTED` goes in `is_terminal` but NOT in `is_failure`, so
  the single-session phase path halts WITHOUT writing a spurious
  `phase-N-diagnostic.md` (UX-contract #4).
- **`--max-session-resets` (default 8 ≈ pool size)** bounds the per-task re-spawn loop.
  The spawn is UNLOCKED (the concurrency win); the sprint-wide halt latch is the only
  shared state (checked/tripped under the lock). The K>1 storm bound is therefore
  `≤ cap + (K−1)` AND `< K×cap` — NOT strictly `≤ cap`, because up to K−1 workers may
  be mid-(unlocked-)spawn when the latch trips.
- **Resume gets a fresh reset budget** (a new process = a new `SessionResetPolicy`).
- **Halt UX is wired at the real seam.** The operator-facing resume command lives in
  `SprintResult.resume_command()` (consumed by `tui.py` + `logging_.py`), NOT the
  dead `build_resume_output`. On a `halt_reason=="provider_exhaustion"` halt it emits a
  SINGLE-LINE `superclaude sprint run … --resume <task> --model <suggested>` (the
  terminal can't paste multi-line); the alias suggester (`aienv.py`) reads
  `os.environ` (option A — `~/.aienv` is bash-`source`d only by `scripts/ic`; no Python
  parses the file) and is None-safe (never fabricates an alias).
- **`rerun-tasks` excludes provider-exhausted tasks from auto-nomination.** The
  directed guard in `select_default_recoverable_tasks` is defensive (it only ever
  selects `fail_recoverable`, so a `fail_provider_exhausted` task is already excluded
  by status); the *actual* leak was the legacy transcript-discovery fallback, which is
  filtered at the `run_rerun_tasks` caller.

**Originating work:** `.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/`,
spec `.dev/brainstorms/sprint-429-recovery-spec.md`. **Files:**
`src/superclaude/cli/sprint/{monitor,models,recovery_policy,aienv,executor,commands,config,logging_,rerun_tasks}.py`,
`tests/sprint/{test_monitor,test_models,test_recovery_policy,test_aienv,test_executor,test_cli_contract,test_sprint_docs_cli_parity,test_rerun_tasks,test_resume}.py`,
`docs/guides/sprint-cli-tools-release-guide.md`.
