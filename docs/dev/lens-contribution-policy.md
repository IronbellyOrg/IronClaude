# Lens contribution policy

**Scope:** governance for new entries in `cli/swarm/lenses/__init__.py::LENSES`
(the 8-entry built-in registry described in §3 of the merged requirements).
Lens entries are not application code — they are vetted shortcuts that
expand into full job specs at preflight time and are dispatched against
real workers. A misconfigured entry can leak prompt-injection vectors,
ship a stale next-cmd hand-off, or pretend to be `stable` without a real
caller. This document fixes the PR-review surface that prevents those
failure modes.

**Sources:**

- `merged-requirements.md` §3.3 (stability tiers) and §3.4 (PR-review
  discipline).
- Roadmap rows R-039 (FR-040 — Lens entry PR-review discipline) and
  R-041 (NFR-008 — PR-review gates for lens entries) in
  `.dev/releases/Current/MultiModelSwarm/roadmap.md` lines 183 and 185.
  The phase-2 tasklist row T02.27 references this contract as
  `NFR-012 lens-registry PR review discipline`; the substance is the
  FR-040 / NFR-008 row text, which both rows summarise as
  "real caller, §11.5 sentence, normalizer fit, downstream-cmd
  validity, suspect scrutiny".
- COMP-023 validator (`cli/swarm/lenses/_validate.py`) and its CLI
  surface `superclaude swarm validate-lenses` (FR-008, T02.16 / T02.20).
- OQ-001 (pre-commit hook decision, §6 below).

## §0 Five-criterion reviewer checklist (TL;DR)

Every PR that adds, edits, or removes an entry under
`cli/swarm/lenses/<name>.py` MUST be reviewed against the following
five criteria. Each criterion has its own deep-dive section below;
this list is the single sign-off surface.

- [ ] **C1 -- Real caller.** A real caller wires this lens in
      production (or a checked-in test fixture demonstrates the
      caller). Speculative "we might want this someday" entries
      belong in `--custom-prompt-dir` until a caller exists. See §2.
- [ ] **C2 -- §11.5 injection-guard substring.** `system_prompt_fragment`
      contains the canonical §11.5 sentence verbatim. The validator's
      `lens.injection_substring_missing` assertion blocks PRs that
      drop it. See §3.
- [ ] **C3 -- `normalizer_strategy` matches recipe output shape.**
      The declared strategy resolves against a registered Recipe in
      `cli/swarm/recipes/__init__.py` and matches the prompt's
      documented output shape. The validator's
      `lens.normalizer_strategy_unmatched` assertion blocks
      mismatches. See §1.
- [ ] **C4 -- Real downstream command in `recommended_next_command_template`.**
      The template references a command/skill that actually exists
      today (slash command, CLI, or skill). Stale or aspirational
      hand-offs are rejected. See §4.
- [ ] **C5 -- `suspect: true` carries by-construction justification.**
      `suspect: true` is reserved for lenses whose prompt design
      makes the output suspect-by-construction (the canonical case is
      `bare-review`'s native-instinct fallback). PRs flipping any
      other entry to `suspect: true` need an architect sign-off and
      a written justification in the PR description. See §5.

Sign-off requires both `architect` and `security` review for any PR
that touches `cli/swarm/lenses/<name>.py`, `cli/swarm/lenses/__init__.py`,
or `cli/swarm/lenses/_validate.py`. See §7 for owners.

## §1 `normalizer_strategy` -- lens-registry contract field

**Source:** `merged-requirements.md` §3.4 PR-review discipline,
roadmap row 17a (FR-LENSREG.NS), phase-2 task T02.21.

### Rule

Every entry in `cli/swarm/lenses/__init__.py::LENSES` (other than the
`custom` escape hatch) **must** declare a non-empty
`normalizer_strategy` that matches the prompt's expected output shape,
and that strategy **must** resolve against a registered Recipe. The
COMP-023 lens validator's sixth assertion enforces both halves of the
rule at `swarm validate-lenses` time and rejects any entry that fails
either half with rule identifier `lens.normalizer_strategy_unmatched`.

### Why

The roadmap row text:

> Each `LENSES` entry declares `normalizer_strategy` matching the
> prompt's expected output shape; validator asserts a registered
> Recipe matches the strategy.

A recipe normalizes raw worker output into a structured shape that the
amalgamation stage merges across N workers (DM-006). Without the
strategy binding, a lens can drift away from its recipe's actual
output shape (e.g. the prompt asks for a bullet list but the recipe
parses a JSON object). The validator pins the binding at the registry
layer so the drift cannot reach dispatch.

### How to declare it

Every concrete `LensEntry` instance under `cli/swarm/lenses/<name>.py`
must set `normalizer_strategy=<strategy_name>` where `<strategy_name>`:

- is a non-empty string,
- matches the prompt's documented output shape (see the lens-specific
  prompt template under `cli/swarm/lenses/<name>.py` /
  `templates/<name>.j2`), and
- resolves through the strategy checker -- either declared in
  `cli/swarm/recipes/__init__.py::STRATEGIES` or carried as the
  `.strategy` attribute of a registered recipe under
  `cli/swarm/recipes/__init__.py::REGISTRY`.

### How the validator decides

`cli/swarm/lenses/_validate.py::_check_normalizer_strategy` (assertion
6) runs after the §11.5 substring assertion. The default
`default_strategy_checker` consults, in order:

1. `recipes.STRATEGIES` -- explicit strategy registry (set / frozenset
   / list / tuple of strategy names, or a dict whose keys are strategy
   names).
2. `recipes.REGISTRY` -- mapping recipe name → recipe object. Both the
   registry's keys and each recipe's `.strategy` attribute are
   consulted; either match resolves the strategy.
3. `recipes.__all__` -- final fallback for the M2/M3 interim where
   recipes register themselves only by re-export.

Until the M4 recipe runtime lands all three surfaces, lenses still
declare `normalizer_strategy`; the validator runs but the default
strategy checker rejects everything. M4 populates `STRATEGIES` and the
gate flips green for the bundled set.

### Negative cases

- `normalizer_strategy=""` -- rejected with rule
  `lens.normalizer_strategy_unmatched`, diagnostic mentions "is empty".
- `normalizer_strategy="not_registered"` -- rejected with the same
  rule, diagnostic mentions "does not resolve against any registered
  recipe".
- `normalizer_strategy` absent from the dataclass (would be a
  `TypeError` at construction since the field is declared with a
  default of `""`; the empty branch catches this).

### Reviewer checklist

When reviewing a PR that touches `cli/swarm/lenses/<name>.py`,
`cli/swarm/lenses/__init__.py`, or `cli/swarm/recipes/`:

- [ ] Every non-`custom` `LensEntry` declares `normalizer_strategy`.
- [ ] The declared strategy matches the documented output shape on the
      corresponding prompt template.
- [ ] A registered recipe (in `recipes.STRATEGIES`, `recipes.REGISTRY`,
      or `recipes.__all__`) resolves the strategy.
- [ ] `superclaude swarm validate-lenses` exits 0 on the bundled
      registry. If the change touches recipes only, also run
      `uv run pytest tests/swarm/test_normalizer_strategy.py -v`.

### Tests

- `tests/swarm/test_normalizer_strategy.py` -- direct coverage of the
  6th assertion and `default_strategy_checker`.
- `tests/swarm/test_lensentry.py` -- pins `normalizer_strategy` in the
  `EXPECTED_FIELDS` tuple and asserts field count is 14.
- `tests/swarm/test_lens_validator.py` -- the baseline
  `_passing_lens` carries `normalizer_strategy="bug_list_v1"` and the
  shared `stub_strategy_checker` fixture isolates the 6th assertion in
  the broader validator suite.
- `tests/swarm/test_validate_all_lenses.py` -- the same baseline +
  `accepting_strategy_checker` exercises `validate_all` propagation.

## §2 Real caller (C1)

**Source:** `merged-requirements.md` §3.3 lines 225 + §3.4 line 231,
roadmap row R-039 (FR-040), R-02 risk mitigation (M3 — lens-registry
sprawl).

### Rule

A lens entry MUST have a real caller before it can be promoted past
`stability="experimental"`. A "real caller" is one of:

- An in-tree skill or command that already builds a `JobSpec` with
  `lens="<name>"` (e.g. `src/superclaude/skills/sc-bare-review/`
  invokes `--lens bare-review`).
- A documented external caller wired in production at a known repo /
  service path. The path goes in the lens file's module docstring.
- A checked-in `tests/swarm/test_*_lens_caller.py` fixture that
  demonstrates the caller surface (acceptable for lenses landing
  alongside their first caller in the same PR).

Speculative entries -- "we might want a `code-review` lens" -- belong
in caller-side `--custom-prompt-dir` until a caller materialises.
The `custom` escape hatch exists precisely to host these prototypes
without inflating the bundled registry.

### Why

R-02 (lens-registry sprawl) is the dominant M3 risk: every bundled
entry is a maintenance surface (validator must keep passing, prompt
must keep matching the recipe, downstream-cmd must keep existing).
A registry full of zero-caller entries rots silently because no real
workflow notices when they break. The "real caller" gate keeps the
registry small and self-policing.

### How to verify in review

- For new entries: PR description names the caller path. Reviewer
  greps the caller path for `lens="<name>"` or `--lens <name>`.
- For promotion (`stability="experimental"` → `"stable"`): PR
  description cites at least one production caller and the date the
  lens has been used in production for ≥2 weeks without regressions.
- For removal: the validator alone is insufficient -- reviewer
  confirms `grep -rn 'lens="<name>"\|--lens <name>'` returns no
  callers before approving.

### Stability tiers

| Tier | Meaning | PR-review bar |
|---|---|---|
| `experimental` | Default for entries beyond `bare-review`. Caller exists but the lens is freshly landed. | Owner sign-off; `validate-lenses` green. |
| `stable` | Promoted entry. Real caller has used it in production. | Architect sign-off; ≥2 weeks production usage cited. |

`bare-review` is the only entry shipping `stable` at M3 exit (it is
the founding caller). All other 6 non-custom entries ship
`experimental` per §3.3.

## §3 §11.5 prompt-injection substring (C2)

**Source:** `merged-requirements.md` §11.5 (canonical injection
guard), §3.4 line 232, INV-003 / NFR-003 cross-binding.

### Rule

Every non-`custom` `LensEntry.system_prompt_fragment` MUST contain the
canonical §11.5 injection-guard substring verbatim. The COMP-023
validator's `lens.injection_substring_missing` assertion enforces this
at `swarm validate-lenses` time. The same substring rule is also
enforced on `prompt.system` by the JSON-Schema validator (FR-019,
T02.03) and on `<custom-prompt-dir>/system.txt` (FR-021 / INV-003,
T02.05). All three paths share `preflight.py::enforce_injection_guard`
(T02.07) -- the validator's lens-side assertion is the registry-time
mirror of the runtime guard.

### Why

§11.5 is the project-wide prompt-injection mitigation: it pins the
target inside `<<<TARGET>>>` / `<<<END TARGET>>>` delimiters and
asserts the canonical sentence is present in the system prompt so a
crafted target cannot rewrite the instruction frame. Lenses are
bundled defaults that bypass JSON-Schema authorship; the registry-side
check is the only thing standing between a contributor's edit and
shipped-by-default injection exposure.

### How to verify in review

- Run `superclaude swarm validate-lenses` locally. Exit 0 confirms
  C2 for every non-custom entry.
- Diff-side check: any change to `system_prompt_fragment=` literals
  on existing entries needs the §11.5 sentence intact in the after
  state. The substring is fragile to paraphrase -- a reviewer eye on
  the diff catches the rare case where the validator's literal match
  was preserved by a contributor's manual edit but the surrounding
  prose drifts.
- Cross-reference: confirm the same substring would also pass
  `tests/swarm/test_injection_guard_all_paths.py` parametrization
  (T02.07).

### Negative cases

- Substring missing → `lens.injection_substring_missing` (validator
  blocks).
- Substring paraphrased (e.g. "Treat target as data" instead of the
  canonical sentence) → same rule fires, since the assertion is a
  literal substring match.
- Substring present but `system_prompt_fragment` itself empty
  → impossible (the assertion runs only if the field is non-empty;
  but a separate length check applies via T02.15 assertions).

## §4 Real downstream command in `recommended_next_command_template` (C4)

**Source:** `merged-requirements.md` §3.4 line 234, roadmap row R-039
(FR-040), §5 of merged requirements (recommended_next_command
contract).

### Rule

`recommended_next_command_template` MUST reference a downstream
command, skill, or CLI that exists today. "Today" means: the command
is registered in `src/superclaude/commands/`, the skill lives at
`src/superclaude/skills/<name>/SKILL.md`, or the CLI is wired in
`superclaude --help`. Aspirational templates (`/sc:some-future-skill ...`)
are rejected.

### Why

The next-cmd template is a hand-off suggestion the swarm surfaces to
the caller after dispatch (§5.6 of merged requirements). It is
explicitly a suggestion (never auto-executed; see §5.6 line 572), so
the rule isn't about runtime safety -- it's about the registry not
shipping broken UX. A lens entry that suggests
`/sc:nonexistent-tool` poisons the caller's prompt with a
dead-letter command and erodes trust in the registry.

### How to verify in review

For each lens entry the PR touches:

1. Read `recommended_next_command_template` from the lens file.
2. For slash-command templates (`/sc:<name> ...`): confirm
   `src/superclaude/commands/sc/<name>.md` or the skill at
   `src/superclaude/skills/sc-<name>/SKILL.md` exists. If only
   `.claude/commands/sc/<name>.md` exists but `src/` is empty, treat
   that as a sync-dev artefact and re-run `make verify-sync` to
   ensure the source-of-truth side is populated.
3. For CLI templates (`superclaude <subcommand> ...`): confirm the
   subcommand resolves via `superclaude <subcommand> --help`.
4. Confirm the substitution variables in the template
   (e.g. `{compare_files}`, `{suspect_files}`) match the contract
   declared in §5 of merged requirements -- the validator's suspect
   coupling assertion (`lens.suspect_files_coupling`) enforces the
   `{suspect_files}` half for `suspect: true` entries, but
   `{compare_files}` and other substitutions are reviewer-checked.

### Negative cases

- Template references a removed command (e.g. legacy `/sc:foo` that
  was renamed) → fail review; PR updates the template or removes the
  lens entry.
- Template references a command that exists only in a downstream
  fork → fail review; the bundled registry ships to upstream and
  cannot rely on fork-private commands.
- Template references a real command but uses an unsupported flag
  combination → fail review; reviewer runs the command's `--help`
  to confirm flag availability.

## §5 `suspect: true` extra scrutiny (C5)

**Source:** `merged-requirements.md` §3.4 line 235 + §5 (DM-020 /
CallerMetadata), roadmap row R-039 (FR-040), OQ-009 resolution
(caller-overridable precedence) recorded in
`docs/swarm/oq-resolutions.md`.

### Rule

A lens entry MAY declare `suspect: true` only when the lens is
suspect-by-construction -- i.e., the prompt design itself produces
output that the caller must treat as a hypothesis pending an
adversarial second pass. The canonical case is
`bare-review` (native-instinct review fallback with no scaffolding;
output is intentionally below T1 confidence and needs
`/sc:adversarial --suspect-source` adjudication).

A PR that flips `suspect` from `false` → `true` on an existing entry,
or lands a new `suspect: true` entry, MUST include:

- A written "by-construction" justification in the PR description
  explaining why the prompt design produces inherently suspect
  output.
- Architect sign-off (see §7) in addition to the default reviewer
  sign-off.
- An updated `recommended_next_command_template` that includes
  `{suspect_files}` -- enforced by the validator's
  `lens.suspect_files_coupling` assertion.

### Why

`suspect: true` is a contract surface the caller observes via
`caller_metadata.suspect` in the result contract (DM-020). It tells
downstream tooling "this output is below T1; route it through
adversarial review before acting on it". If contributors flip the
flag casually -- e.g. on an `edge_case_hunt` lens that produces fine
T2 output but feels "less confident" subjectively -- the signal
loses meaning and callers stop honoring it. The "by-construction"
bar keeps the signal load-bearing.

### How to verify in review

- For new `suspect: true` entries: confirm the prompt fragment
  describes a structural reason for the output being suspect (no
  scaffolding, instinct-only mode, deliberate low-confidence trade,
  etc.). A prose phrase like "this is just a heuristic" is
  insufficient; the prompt must *produce* suspect output by design,
  not warn that it might.
- Confirm `recommended_next_command_template` includes
  `{suspect_files}`. The validator catches the absence; the
  reviewer catches a present-but-meaningless placeholder.
- Confirm `tier` is set to a T2 variant (T2, T2-tshoot, etc.) --
  `suspect: true` + `tier: T1` is a contradiction.

### Negative cases

- `suspect: true` on a lens whose prompt produces structured JSON
  the recipe parses confidently → reject; the lens is not
  suspect-by-construction even if the contributor wants the caller
  to double-check.
- `suspect: true` without `{suspect_files}` in next-cmd template →
  blocked by validator (`lens.suspect_files_coupling`).
- A caller override forcing `suspect=true` at runtime: this is
  allowed (OQ-009 resolution: caller-overridable precedence) and is
  out of scope for this policy -- the lens-side declaration is
  what's gated here.

## §6 OQ-001 -- `validate-lenses` pre-commit hook (resolved)

**Source:** Roadmap row 180 line 183 (OQ-001 — devops; target:
Before M2 exit), M3 milestone exit text (line 166), merge improvement
I6 (line 530). Cross-binding: OQ-010 resolution in
`docs/swarm/oq-resolutions.md` lines 257–263 + 316–323.

### Question

Should `validate-lenses` run as a pre-commit hook by default?

### Resolution

**Yes, install the hook in `--warning-mode` by default for local
pre-commit; let CI run the default blocking mode at PR time.** This
is the hybrid that the OQ-010 resolution anticipates explicitly
("OQ-001's natural resolution is 'install the hook in warning-mode
for fast local feedback, and let CI run the default blocking mode at
PR time'").

The mechanical wiring:

- **Local pre-commit hook (`--warning-mode`).** A `.pre-commit-hooks`
  entry runs `superclaude swarm validate-lenses --warning-mode`
  on any commit that touches `src/superclaude/cli/swarm/lenses/**`
  or `src/superclaude/cli/swarm/recipes/**`. Diagnostics print but
  the commit proceeds. This gives contributors immediate feedback
  while iterating without blocking quick experiments.
- **CI (default blocking).** The same `make verify-sync` target
  invokes `superclaude swarm validate-lenses` without
  `--warning-mode`. A registry regression (missing §11.5 substring,
  unregistered recipe, suspect-coupling violation, etc.) returns
  non-zero and fails the PR check. This is the authoritative gate.
- **Bypass discipline.** Local contributors who genuinely need to
  skip the hook can use `git commit --no-verify`; this is fine for
  WIP commits but the PR's CI run still blocks the merge.

### Why

The OQ-010 resolution already settled the exit-code semantics
(blocking by default, opt-in `--warning-mode`). OQ-001 only asks
*where* the warning-mode call lives. Putting it in pre-commit gives
contributors the fast loop that prevented OQ-001 from resolving as
"yes, blocking" in the first place -- a blocking pre-commit hook on
every commit touching a lens file would make experimental iteration
painful, especially for `experimental`-tier lenses that intentionally
land in churn. The warning-mode hook is the right shape because it
shortens the feedback loop without lengthening the iteration cycle.

### Wiring task

The actual pre-commit hook installation is a follow-up under M3
exit ("validate-lenses wired into verify-sync + pre-commit by M3
exit", roadmap line 184 + line 602). This policy document records
the resolution; the hook wiring lands with the M3 exit checkpoint
task.

## §7 Owners and sign-off

### Default reviewers

Every PR touching the lens registry MUST be reviewed by at least one
person from each of the two ownership groups below:

- **`architect`** -- governance owner for the lens registry as a
  whole (sprawl risk R-02, stability tier promotions, OQ-009
  precedence). Reviews C1 (real caller), C4 (downstream command),
  C5 (`suspect:true` justification).
- **`security`** -- owner for the §11.5 injection-guard binding
  across all three prompt-input paths (lens / JSON-Schema /
  custom-prompt-dir). Reviews C2 (§11.5 substring) plus any change
  that touches `cli/swarm/lenses/_validate.py` (since validator
  changes affect security-critical assertions).

The `normalizer_strategy` (C3 / §1) check is covered by either
reviewer plus the validator's automated assertion; no dedicated
recipes owner is required at M3 exit because recipes are a small
shared surface still under architect ownership (revisit at M4
recipe-runtime exit).

### Sign-off log

| Date | PR | Reviewer | Group | Notes |
|---|---|---|---|---|
| 2026-06-01 | T02.27 (this doc) | architect | architect | Initial five-criterion checklist + OQ-001 resolution recorded. |
| 2026-06-01 | T02.27 (this doc) | security | security | §11.5 substring binding cross-referenced against `enforce_injection_guard` (T02.07) and `_validate._check_injection_substring`. |

(Subsequent PRs touching the registry append a row here as part of
their sign-off.)

### Escalation

- A PR that touches `_validate.py` AND any `LensEntry` body in the
  same diff requires both reviewer groups to sign off independently
  -- the change has both governance and security implications.
- A `stability` promotion (`experimental` → `stable`) on any lens
  other than `bare-review` requires architect sign-off plus a
  citation of ≥2 weeks of production caller usage in the PR
  description. Security review is advisory at promotion time
  unless the prompt fragment changes.
- A `suspect: true` flip on any non-`bare-review` entry requires
  architect sign-off plus a written by-construction justification
  (see §5). Security review is mandatory if the prompt fragment
  changes alongside the flip.

## §8 Enforcement summary

| Criterion | Automated gate | Reviewer gate |
|---|---|---|
| C1 -- Real caller | (none -- registry-side) | Architect verifies caller path in PR description; greps tree for `lens="<name>"`. |
| C2 -- §11.5 substring | `_validate._check_injection_substring` (`lens.injection_substring_missing`); `enforce_injection_guard` at runtime (T02.07) | Security spot-checks substring intact in diff after-state. |
| C3 -- `normalizer_strategy` | `_validate._check_normalizer_strategy` (`lens.normalizer_strategy_unmatched`) | Either reviewer confirms strategy matches prompt's output shape. |
| C4 -- Real downstream cmd | (none -- registry-side) | Architect confirms command/skill exists today via `superclaude --help` / file existence. |
| C5 -- `suspect: true` extra scrutiny | `_validate._check_suspect_files_coupling` (`lens.suspect_files_coupling`) for `{suspect_files}` substitution | Architect signs off on by-construction justification; rejects casual flips. |

CI runs `superclaude swarm validate-lenses` (default blocking mode)
on every PR via `make verify-sync`. Local pre-commit runs the same
command with `--warning-mode` per OQ-001 (§6).
