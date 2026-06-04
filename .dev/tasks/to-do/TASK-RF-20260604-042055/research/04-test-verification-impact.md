# Research: Test & Verification Impact

Status: Complete
Date: 2026-06-04

Topic: What breaks when we edit `task-builder/SKILL.md`, `sc-tasklist-protocol/SKILL.md`,
`commands/tasklist.md`, the tasklist templates, and possibly `src/superclaude/agents/rf-qa.md`.

Researcher: R4 (CRITICAL gate) — owns tests + verification + rf-qa.md TB-Add catalogue.

---

## TL;DR (highest-risk finding first)

**The single biggest test break is a HARD-CODED `"#### Checklist (28 items)"` string assertion**
in `tests/skills/test_task_builder_merge.py:69` AND `:190`, paired with the literal heading at
`src/superclaude/agents/rf-qa.md:298`. This breaks **only if** the POST-reflect-present check is
implemented as a structural **`TB-Add-9`** in rf-qa.md's catalogue (which bumps the checklist
heading to `(29 items)`). If — as the proposal's own implementer checklist (§8 item 1) actually
specifies — the check is added only to the **task-builder SKILL.md "Task File Validation Checklist"**
(a different surface, not the rf-qa structural-gate catalogue), then **rf-qa.md is not touched, the
"28 items" heading does not move, and ZERO audit/skill tests break.**

**Checkpoint-is-last is NOT a Sprint-CLI risk.** Checkpoint discovery is purely *declaration-driven*
(regex scan for `### ... Checkpoint: <name>` headings + `Checkpoint Report Path:` lines), not
position-driven. No scanner assumes the highest-numbered task is the checkpoint. A POST-reflect
task placed *after* the checkpoint heading does not break phase discovery, manifest building, or the
checkpoint gate. (Evidence below, §2.)

---

## 1. Audit-test break-risk classification (does the test parse the SKILL TEXT?)

Two fundamentally different families:

- **Family A — TEXT-READING tests** read the live `src/superclaude/.../*.md` files and grep for
  literal strings / structural anchors. These break if our edits move/duplicate/rename an anchor.
- **Family B — PURE-PYTHON detector tests** re-implement the TB-Add-1..8 checks as in-file Python
  functions and run them against **fixtures** under `tests/audit/fixtures/`. They do NOT read
  rf-qa.md's catalogue prose; adding `TB-Add-9` to rf-qa.md does not affect them.

### The INV-010 dynamic-enumeration test (HIGH PRIORITY)

`tests/audit/test_dynamic_enumeration_inv_010.py` — **Family A (reads both rf-qa.md SRC+MIRROR and
SKILL.md).** This is the test the task brief flagged. Key facts:

- It extracts the catalogue **dynamically** from rf-qa.md's bounded `#### Structural Gate Additions`
  region via regex `^[0-9]+\. \*\*TB-Add-([0-9]+):` (`test_...inv_010.py:70`). It does **NOT**
  hard-code a count of 8.
- Floor assertion is `>=`, not `==`: `MIN_LIVE_K = 8` (`:88`); `test_cycle1_catalogue_meets_min_floor`
  asserts `k1 >= MIN_LIVE_K` (`:381`). **K=9 passes.**
- Density assertion uses a dynamic range: `assert ns == list(range(1, len(ns) + 1))`
  (`:391`, `test_cycle1_catalogue_is_dense`). A dense `TB-Add-1..9` passes; only **gaps** fail.
- **Synthetic-stub arithmetic self-adjusts but has a latent coupling.** `two_cycle` computes
  `synth_n = k1 + 1` and `synth_num = 28 + (synth_n - 8)` (`:235-236`). With TB-Add-9 added (K1=9),
  `synth_n=10`, `synth_num = 28+2 = 30`. The real catalogue would then end at numbered item 29
  (TB-Add-9), so the synthetic stub at list-index 30 is still sequentially correct → the
  grow-by-exactly-one assertions (`:412`, `:458`) still pass. **Verified: INV-010 stays GREEN with a
  numbered TB-Add-9 added, provided TB-Add-9 is appended as numbered item 29 inside the bounded
  region with no gap.**
- AC-4 guard (`TestNoHardCodedEnumerationInA105`, `:301`): the SKILL.md §A.10.5 enumeration block may
  contain ONLY `TB-Add-1` / `TB-Add-2` symbolic tokens. **Do NOT mention `TB-Add-9` (or any other
  TB-Add-N) inside the A.10.5 enumeration block** — that would trip `:337`.
- **Risk: MEDIUM** if TB-Add-9 is added to rf-qa.md (passes, but the catalogue must be dense + the
  A.10.5 block must stay symbolic-only). **Risk: NONE** if no rf-qa.md edit.

Quoted load-bearing assertions:
```
:381  assert k1 >= MIN_LIVE_K
:391  assert ns == list(range(1, len(ns) + 1))
:412  assert k2 == k1 + 1
:293  assert src_bytes == mirror_bytes  # rf-qa SRC == .claude/ MIRROR (needs make sync-dev)
```

### Per-test classification table

| Test file | Reads `.md`? | What it asserts | Break-risk | Required action |
|---|---|---|---|---|
| `test_dynamic_enumeration_inv_010.py` | YES — rf-qa.md SRC+MIRROR, SKILL.md | dynamic catalogue size `>=8`, dense `1..K`, grow-by-1, `src==mirror` byte-identical, A.10.5 block symbolic-only | **MEDIUM** (if TB-Add-9 added) / NONE (if not) | If TB-Add-9 added: append as **dense** numbered item 29 in bounded region; keep A.10.5 block symbolic; run `make sync-dev` so SRC==MIRROR. |
| `test_task_builder_merge.py` | YES — SKILL.md, rf-qa.md, rf-*.md | `"#### Checklist (28 items)" in rf_qa_text` (`:69`,`:190`); TB-Add-1..7/8 present in both surfaces; `skill_text.count(tag) >= 2` | **HIGH** (if rf-qa heading moves to 29) / LOW (if not) | If TB-Add-9 added to rf-qa: update `:69` + `:190` literal to `(29 items)`. Do NOT remove/rename TB-Add-1..8 anchors. New validation-checklist items must not displace existing TB-Add mentions. |
| `test_evidence_bound_tb_add_8.py` | reads **fixtures** under `fixtures/execution_context/` (`:198`); cites SKILL.md lines in docstring only | TB-Add-8 evidence-binding behavior on fixtures | **LOW** | Don't reorder/renumber TB-Add-8. Behavior untouched by reflect edits. |
| `test_inherited_verdict_present.py` | YES — SKILL.md SRC+MIRROR | verbatim `BLOCK_HEADER` "## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)" appears **exactly once** (`:87`,`:93`) | **LOW** | Do not duplicate or alter that block header. Reflect edits are elsewhere. |
| `test_inherited_verdict_freshness_inv_002.py` | YES — SKILL.md SRC+MIRROR | INV-002 freshness re-entry anchors present; uses **synthetic in-test verdict tables** (`:60-78`) not real rf-qa parse | **LOW** | Keep `FIX_CYCLE_HEADER` / `BLOCK_HEADER` strings intact. |
| `test_self_audit_inv_019.py` | YES — **`rf-qa-qualitative.md`** SRC+MIRROR (`:46`) | self-audit prose in a **different file we are NOT editing** | **NONE** | none — wrong file. |
| `test_nfr_conv_6_self_contained.py` | reads rf-qa.md for one line cite + **fixtures** `fixtures/nfr_conv_6/`; defines `tb_add_1..8` as **pure Python** (`:141-362`) | full-fields fixture PASSes the 8 detectors; `run_all_tb_add` is a fixed 8-key dict (`:352-362`) | **NONE** | The 8 detectors are self-contained; TB-Add-9 in rf-qa does not add a 9th detector here. |
| `test_nfr_conv_9_zero_trust.py` | YES — rf-qa.md SRC+MIRROR | PASS/FAIL bullet strings at rf-qa.md byte-identical to frozen baseline | **LOW** | Do not edit the PASS/FAIL verdict-bullet region of rf-qa.md (we won't). |
| `test_invariant_preservation_NFR_6_through_10.py` | imports detectors from the conv_6/conv_9/tb_add_8 modules → **fixtures** | composite wiring of the 5 invariants; `len(INVARIANTS)==5` (`:135`); 8 detectors PASS full-fields fixture | **NONE** | Pure-Python composite; unaffected. |
| `test_dnsp_*` set (`all_agents_fail_bypass`, `dedup_collapse`, `does_not_serialize_cohort`, `twice_exhaust`, `synthetic_dnsp_dedup_not_regression`) | DNSP = "does-not-serialize-parallel" cohort logic; not catalogue-count coupled | parallel-spawn dedup invariants | **NONE** | unrelated to reflect/checkpoint/TB-Add count. |
| `test_monotonicity_halt_F_5_5_5.py` | YES — SKILL.md SRC (`:102`) | §A.9 API-004 halt wire-template **byte-exact**; payload len==25 (`:175`); "regression > monotonicity" prose present (`:147`) | **MEDIUM** | The A.9 halt-loop region is **adjacent** to where the POST gate/Critical Rule prose lands. Do NOT touch the API-004 contract table / wire template bytes. New Critical Rule must be additive, not edit row 1. |
| `test_regression_halt_pass1_fail2.py` | YES — SKILL.md SRC (`:162`) | §A.9 API-004 row-2 byte-exact wire template; one em-dash (`:202`); precedence prose (`:209`) | **MEDIUM** | Same as above — keep §A.9 byte-stable. |
| `test_sequencing_PR06_before_PR04.py` | YES — rf-qa.md SRC+MIRROR, SKILL.md | strip-catalogue→empty then activate→`MIN_LIVE_K=8` floor (`:92`,`:433`), dense `1..K` (`:443`); "zero edits to SKILL.md" K-007 prose present | **MEDIUM** (if TB-Add-9 added) / NONE | Same shape as INV-010: K=9 passes the `>=` floor + dynamic density. Keep SKILL.md K-007 prose anchors intact; keep catalogue dense. |

**Net:** With the **proposal's specified approach (validation-checklist item, no rf-qa.md edit)**,
the only Family-A tests touching task-builder SKILL.md (`test_inherited_verdict_present`,
`...freshness`, `monotonicity`, `regression_halt`, merge) break **only if the new prose collides
with an existing anchor** — additive insertion in new §A.10.7 / new `## Reflect Depth` section /
new Critical Rule avoids all of them. With the **TB-Add-9 approach**, add the "28→29 items"
update to merge-test + rf-qa heading.

---

## 2. Tasklist / checkpoint tests — is "checkpoint = highest-numbered task" assumed? NO.

The proposal's stated "biggest risk" (Sprint scanner assumes highest-numbered task is the
checkpoint) is **not borne out by the code.** Checkpoint handling is declaration-driven:

- `extract_checkpoint_paths()` (`src/superclaude/cli/sprint/checkpoints.py:40-98`) scans the WHOLE
  phase file with two regexes and pairs each `Checkpoint Report Path:` line with the *nearest
  preceding* `### Checkpoint:` heading (`_nearest_heading`, `:119-130`). Position relative to task
  numbers is irrelevant.
  ```
  checkpoints.py:26  CHECKPOINT_PATH_PATTERN = re.compile(r"Checkpoint\s+Report\s+Path:\s*\*{0,2}\s*`?([^\s`\n*]+)`?", re.IGNORECASE)
  checkpoints.py:34  CHECKPOINT_HEADING_PATTERN = re.compile(r"^#{2,5}\s*(?:T\d{2}\.\d{2}\s*--\s*)?Checkpoint:\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)
  ```
- `build_manifest()` (`checkpoints.py:138-170`) iterates `discover_phases()` and collects every
  declared checkpoint per phase. No "last task" logic.
- `discover_phases()` (`src/superclaude/cli/sprint/config.py:58-146`) discovers **phase FILES** from
  the index table / directory scan; it never inspects intra-phase task ordering. `end_phase =
  max(p.number for p in phases)` (`config.py:323`) is over **phase numbers**, not task numbers.
- `parse_tasklist()` (`config.py:411-504`) returns tasks in **document order** via
  `_TASK_HEADING_RE = ^###\s+(T\d{2}\.\d{2})\s*(?:--|-—|—)\s*(.+)` (`config.py:386`). A checkpoint
  heading written as `### T07.09 -- Checkpoint: End of Phase 7` **matches this regex** (title =
  "Checkpoint: ..."), so it parses as a normal task entry in its document position. A POST-reflect
  task with a *higher* task number placed *after* the checkpoint heading is simply the next task in
  document order — no breakage.
- `_verify_checkpoints()` (`executor.py:2408+`) checks the declared checkpoint FILE PATHS exist and
  reacts per `checkpoint_gate_mode` (off/shadow/soft/full; default **shadow** = never alters status).
  `last_task_id` (`executor.py:1165`, `models.py:743/853`) is purely a TUI/monitor "most recent
  task" field — NOT a checkpoint identity.

**Checkpoint tests are fixture-synthetic.** `tests/sprint/test_checkpoints.py` builds tiny phase
files in `tmp_path` (e.g. `:48-60`) — it does NOT load the repo's real tasklist templates. Editing
`commands/tasklist.md` / `sc-tasklist-protocol/SKILL.md` / templates does not feed these tests.

**Conclusion:** The "checkpoint-is-last" amendment is a **tasklist-authoring convention** (which task
the human/agent labels as the end-of-phase checkpoint), with **no Sprint-CLI enforcement coupling**.
Placing a POST-reflect handoff task after the checkpoint is CLI-safe. **Break-risk: NONE** for the
Sprint checkpoint subsystem. (Verify regardless with the smoke command in §3.)

---

## 3. Does editing a `.md` skill trigger any test/lint? YES — markdownlint + verify-sync.

- **markdownlint (pre-commit, `--fix`)** runs on every `.md` EXCEPT `.dev/`, `CHANGELOG.md`,
  `node_modules`, `*.min.md` (`.pre-commit-config.yaml:71-82`). So `src/superclaude/skills/
  task-builder/SKILL.md`, `sc-tasklist-protocol/SKILL.md`, `commands/tasklist.md`, and the
  templates ARE linted at commit. Config (`.markdownlint.json`): `default:true` with `MD013:false`
  (line-length OFF — long prose lines are fine), `MD024:{siblings_only}`, `MD029:false`,
  `MD036:false`, `MD033:false`. **Watch for:** MD025 (single H1), MD040 (fenced-code language),
  blank-line-around-list/heading rules. `--fix` auto-repairs many but the hook still fails the commit
  if anything is unfixable.
- **`make verify-sync`** (`Makefile:166`) diffs `src/superclaude/{skills,agents}` against `.claude/`
  mirrors and fails on drift. Editing a skill in `src/` without `make sync-dev` fails this gate.
  `test_dynamic_enumeration_inv_010.py:293` and `test_inherited_verdict_present.py` ALSO assert
  SRC==MIRROR byte-identity → **`make sync-dev` is mandatory after editing rf-qa.md or any SKILL.md.**
- **`block-claude-generated-mirrors`** (`.pre-commit-config.yaml:104`) rejects staging `.claude/`
  mirrors — edit `src/` only, never stage `.claude/` (consistent with CLAUDE.md ABSOLUTE RULE).
- **`make lint` / `make format`** = `ruff check .` / `ruff format .` (`Makefile:48-55`) — Python only;
  irrelevant to pure `.md` edits, but run if any test fixture or CLI code is touched. NOTE (memory):
  `make lint` does NOT run `ruff format --check`; CI does separately.
- **`make test`** = `uv run pytest` (`Makefile:15`) — full suite; the audit + skills + sprint tests
  above run here.

### Verification commands to run after each edit phase (UV only)

| After editing… | Run (in order) | Why |
|---|---|---|
| any `src/superclaude/.../*.md` (SKILL/agent/command/template) | `make sync-dev` | propagate to `.claude/` mirror (SRC==MIRROR byte tests) |
| → then always | `make verify-sync` | confirm no drift; catches the byte-identity audit tests early |
| task-builder SKILL.md / rf-qa.md edits | `uv run pytest tests/audit/ tests/skills/ -q` | INV-010 enumeration, merge-test "28 items", verdict-header, A.9 halt byte-templates |
| tasklist protocol / command / templates / checkpoint-is-last amendment | `uv run pytest tests/sprint/test_checkpoints.py tests/audit/test_checkpoint.py -q` | confirm checkpoint discovery/manifest unaffected (expected: still green) |
| any `.md` (before commit) | `uv run pre-commit run markdownlint --files <edited.md>` (or `pre-commit run --all-files`) | MD-rule compliance; `--fix` auto-repairs then re-stage |
| final gate | `make test` | full suite incl. `tests/sprint/`, `tests/audit/`, `tests/skills/` |

**Single-line smoke (paste-ready):**
`make sync-dev && make verify-sync && uv run pytest tests/audit/ tests/skills/ tests/sprint/test_checkpoints.py -q`

---

## 4. rf-qa.md TB-Add catalogue — is a numbered TB-Add-9 required?

### Current catalogue (exact line region)

`src/superclaude/agents/rf-qa.md`:

- Heading: `#### Structural Gate Additions (TB-Add-1 through TB-Add-7, …)` at **line 330**.
- Numbered entries **21–28** map to **TB-Add-1 … TB-Add-8**:
  - `:334` `21. **TB-Add-1: Placeholder scan…`
  - `:341` `22. **TB-Add-2: Item count bounds… ADVISORY…`
  - `:343` `23. **TB-Add-3: Clarification adjacency…`
  - `:345` `24. **TB-Add-4: Circular dependency…`
  - `:347` `25. **TB-Add-5: Granularity / XL splitting…`
  - `:349` `26. **TB-Add-6: Confidence/Verification format…`
  - `:351` `27. **TB-Add-7: Execution Context source areas…`
  - `:369` `28. **TB-Add-8: Per-item Context evidence binding…`
- Catalogue region ends before the `---` / `## QA Phase: Fix Cycle` heading at `:380-382`.
- The parent checklist heading is `#### Checklist (28 items)` at **line 298** (the count = 20 base
  task-integrity items + 8 TB-Add). A numbered TB-Add-9 ⇒ this MUST become `(29 items)`.

### Is TB-Add-9 required? — NO, per the proposal as written.

The proposal's implementer checklist (`reflect-in-task-builder.md:274`) specifies:

> "Task File Validation Checklist: add 'POST reflect item present + positioned when enabled'"

— i.e. a new entry in the **task-builder SKILL.md "Task File Validation Checklist"** surface
(the producer-side, ~SKILL.md:1969 region per the proposal's §7-risk-5 cite), NOT a structural
**TB-Add** gate in rf-qa.md. These are different surfaces:

- The **rf-qa.md "Structural Gate Additions" (TB-Add-N)** catalogue = checks rf-qa runs *against a
  produced tasklist* and feeds to INV-010 dynamic enumeration.
- The **SKILL.md "Task File Validation Checklist"** = the builder's own pre-write self-check list
  (Rule #16-style MALFORMED guards).

The "POST reflect item present + positioned" check is naturally a **validation-checklist** item
(it validates the builder emitted the reflect handoff), so **the default, lowest-risk path is to add
it ONLY to the SKILL.md validation checklist and leave rf-qa.md untouched.** Under that path:
**INV-010 is GREEN unchanged, merge-test "28 items" is GREEN unchanged, no rf-qa sync needed.**

### IF the implementer elects to make it a structural TB-Add-9 (optional, NOT required)

Then to keep INV-010 + merge tests green, the following must change in lockstep:

1. `rf-qa.md`: append `29. **TB-Add-9: POST-reflect handoff item present (sc:task reflect gate).** …`
   as a **dense** numbered item inside the bounded `#### Structural Gate Additions` region (no gap —
   density check `range(1, K+1)`), citing its source check for traceability.
2. `rf-qa.md:298`: change `#### Checklist (28 items)` → `#### Checklist (29 items)`.
3. `tests/skills/test_task_builder_merge.py:69` and `:190`: change the `"#### Checklist (28 items)"`
   literal → `"#### Checklist (29 items)"`.
4. `rf-qa.md:330` heading text says "TB-Add-1 through TB-Add-7" (prose label, already understated vs
   the actual 8) — optionally update, but no test asserts that exact span, so not required.
5. SKILL.md A.10.5 enumeration block: do **NOT** add a literal `TB-Add-9` token there (AC-4 guard
   `test_dynamic_enumeration_inv_010.py:337` permits only `TB-Add-1`/`TB-Add-2` symbolic tokens).
6. `make sync-dev` so rf-qa SRC==`.claude/` MIRROR (byte-identity tests `inv_010.py:293`,
   `:484`; `nfr_conv_9`).

**Recommendation to the task author:** default to the validation-checklist approach (proposal as
written) = TB-Add-9 NOT created → break-risk drops from MEDIUM/HIGH to NONE for rf-qa-coupled tests.
Reserve TB-Add-9 only if a reviewer insists the gate must run structurally against produced
tasklists; if so, the four lockstep edits above are mechanical and fully testable.

---

## TABLE A — Break-risk summary

| Test / gate | Reads `.md`? | Risk (validation-checklist path) | Risk (TB-Add-9 path) | Required action |
|---|---|---|---|---|
| `test_dynamic_enumeration_inv_010.py` | rf-qa SRC+MIRROR, SKILL | NONE | MEDIUM→pass | dense TB-Add-9, symbolic A.10.5 block, `make sync-dev` |
| `test_sequencing_PR06_before_PR04.py` | rf-qa SRC+MIRROR, SKILL | NONE | MEDIUM→pass | same (floor `>=8`, dense) |
| `test_task_builder_merge.py` | SKILL, rf-qa | LOW (don't collide anchors) | **HIGH** | update "28 items"→"29 items" at `:69`,`:190` + rf-qa:298 |
| `test_inherited_verdict_present.py` | SKILL SRC+MIRROR | LOW | LOW | keep BLOCK_HEADER unique+verbatim |
| `test_inherited_verdict_freshness_inv_002.py` | SKILL SRC+MIRROR | LOW | LOW | keep FIX_CYCLE/BLOCK headers intact |
| `test_monotonicity_halt_F_5_5_5.py` | SKILL SRC | MEDIUM | MEDIUM | additive prose only; keep §A.9 API-004 bytes |
| `test_regression_halt_pass1_fail2.py` | SKILL SRC | MEDIUM | MEDIUM | keep §A.9 row-2 wire template byte-exact |
| `test_evidence_bound_tb_add_8.py` | fixtures | LOW | LOW | don't renumber TB-Add-8 |
| `test_nfr_conv_6_self_contained.py` | fixtures (+1 cite) | NONE | NONE | pure-Python 8 detectors |
| `test_invariant_preservation_NFR_6_through_10.py` | fixtures (imports) | NONE | NONE | composite wiring |
| `test_nfr_conv_9_zero_trust.py` | rf-qa SRC+MIRROR | LOW | LOW | don't edit PASS/FAIL bullet region |
| `test_self_audit_inv_019.py` | **rf-qa-qualitative.md** | NONE | NONE | different file — not edited |
| `test_dnsp_*` set | none (cohort logic) | NONE | NONE | unrelated |
| `tests/sprint/test_checkpoints.py` | tmp_path fixtures | NONE | NONE | checkpoint discovery is declaration-driven, position-independent |
| `tests/audit/test_checkpoint.py` | (audit-side) | NONE | NONE | run to confirm green |
| markdownlint (pre-commit) | all edited `.md` | LOW | LOW | `pre-commit run markdownlint --files <md>`; MD013 off so prose OK |
| `make verify-sync` / SRC==MIRROR byte tests | rf-qa+SKILL | MED if `sync-dev` skipped | MED if skipped | **always `make sync-dev` after editing `src/`** |

---

## TABLE B — Verification commands (executor checklist; UV only)

| Phase | Command | Pass criterion |
|---|---|---|
| After editing any `src/superclaude/.../*.md` (SKILL/agent/command/template) | `make sync-dev` | mirrors regenerated |
| Immediately after | `make verify-sync` | "✅" all skills/agents, no DIFFERS/MISSING |
| After SKILL.md / rf-qa.md edits | `uv run pytest tests/audit/ tests/skills/ -q` | 0 failures |
| After tasklist/command/template/checkpoint-amendment edits | `uv run pytest tests/sprint/test_checkpoints.py tests/audit/test_checkpoint.py -q` | 0 failures (expected unchanged) |
| Before commit (each edited `.md`) | `uv run pre-commit run markdownlint --files <path.md>` | hook passes (re-stage after `--fix`) |
| Python touched (fixtures/CLI) | `make lint` then `uv run ruff format --check src/ tests/` | clean (memory: `make lint` ≠ CI format) |
| Final gate | `make test` | full suite green |
| One-line smoke | `make sync-dev && make verify-sync && uv run pytest tests/audit/ tests/skills/ tests/sprint/test_checkpoints.py -q` | all green |

NOTE on staging: per CLAUDE.md ABSOLUTE RULE, never `git add .claude/...` — edit `src/superclaude/`
only, then `make sync-dev`. The `block-claude-generated-mirrors` pre-commit hook + `.gitignore`
enforce this; `verify-sync` confirms parity.
