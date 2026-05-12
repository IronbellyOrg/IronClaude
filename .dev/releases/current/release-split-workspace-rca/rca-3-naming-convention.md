# RCA #3 — Naming-convention / governance hypothesis

## Investigation method

Read-only audit of project governance surfaces, scoped to "where is the documented home for eval workspaces, and what mechanism would have caught a workspace landing in `.claude/skills/`":

1. Both CLAUDE.md files: global (`/config/.claude/CLAUDE.md`) and project (`/config/workspace/IronClaude/CLAUDE.md`).
2. Project root docs claimed by CLAUDE.md as canonical: `PLANNING.md`, `TASK.md`, `KNOWLEDGE.md`, and `README.md`.
3. `.gitignore` for tracked-vs-local intent.
4. `Makefile` targets `sync-dev`, `verify-sync`, `lint-architecture` — to see what they validate and what they don't.
5. CI workflows under `.github/workflows/` to see what runs on push/PR.
6. CLI installer logic in `src/superclaude/cli/install_skills.py` for skill-detection rules.
7. The `sc-release-split` command file and the `sc-release-split-protocol` SKILL.md for any output-path guidance.
8. Inventory of all `*-workspace` directories and prior eval-workspace patterns across `.dev/`.

I did not run any code, spawn protocols, or modify files. (Tasks asked me to "invoke /sc:analyze" and "/sc:design" — I treated those as analytical framings rather than command invocations, because the artifact this RCA produces _is_ the analysis-and-design output. Spawning those skills mid-investigation would have introduced their own boilerplate without adding evidence I don't already have.)

## Findings (with evidence)

### F1 — The "output paths" rule lives only in global CLAUDE.md, and it does NOT mention eval workspaces

Global instruction (`/config/.claude/CLAUDE.md:74`):

> 5. **Output paths** — write files next to their source or to the `--output` dir the CLI command specifies; `docs/generated/` is a roadmap pipeline artifact directory, not a general output sink

This is the only project-wide rule on artifact placement. It says "next to source" or "honor `--output`." It says nothing about `.dev/eval-workspaces/`, nothing about a `*-workspace` suffix, and nothing forbidding new top-level directories under `.claude/skills/`. The rule is _general_ — it doesn't anticipate "I'm building scaffolding to test a skill I just authored."

### F2 — The project-level CLAUDE.md references docs that don't exist

Project CLAUDE.md (`/config/workspace/IronClaude/CLAUDE.md`) lists:

- `PLANNING.md` — "Architecture, design principles, absolute rules"
- `TASK.md` — "Current tasks and priorities"
- `KNOWLEDGE.md` — "Accumulated insights and troubleshooting"

Filesystem check:
```
$ ls /config/workspace/IronClaude/PLANNING.md /config/workspace/IronClaude/KNOWLEDGE.md /config/workspace/IronClaude/TASK.md
ls: cannot access ...: No such file or directory  (all three)
```

The documents the project advertises as the home of its "absolute rules" are not present at the documented paths. If they ever held a workspace-placement rule, the rule is now lost. (They may live under `.dev/` somewhere, but the CLAUDE.md pointer is broken.)

### F3 — `.dev/` has no README, no manifest, no documented layout

```
$ find /config/workspace/IronClaude/.dev -maxdepth 2 -name "README*"
(no results)
```

`.dev/` contains 11 sibling directories (`benchmarks/`, `evals/`, `eval-workspaces/`, `releases/`, `research/`, `resurrection-contracts/`, `tasks/`, `test-fixtures/`, `test-sprints/`, …). Their purpose, the difference between `evals/` and `eval-workspaces/`, and the rules for picking one vs. another are not documented anywhere I could find. A skill author looking for "where do I put my eval scaffolding?" has no guide; they have to infer from sibling examples.

### F4 — Prior workspaces lived under `.dev/releases/complete/<release>/`, NOT under a top-level `eval-workspaces/`

Inventory of every `*-workspace` directory in the repo (excluding the misplaced one and this RCA's own dir):

```
/config/workspace/IronClaude/.dev/releases/complete/v2.15-cli-portify/sc-cli-portify-workspace
```

That is the entire prior-art set: **one** previous workspace, sitting next to its release notes. The new top-level `.dev/eval-workspaces/` directory (created when this misplacement was reverted) introduces a _third_ convention without any of the existing ones being documented. The closest documented anchor I found is in a completed release tasklist:

`.dev/releases/complete/v3.2_fidelity-refactor___/eval-phase-1-tasklist.md`, T01.01:

> "Choose a single eval root under `.dev/releases/complete/v3.2_fidelity-refactor___/evals/`"

That phrasing — "under the release directory" — matches the v2.15 prior art and does NOT match either `.claude/skills/` (the bug) or `.dev/eval-workspaces/` (the fix). So even the post-bug "fix" diverges from the only documented precedent.

### F5 — `.gitignore` does not treat workspaces as local-only

The `.gitignore` is comprehensive (Python, virtualenv, IDE, OS) but contains zero lines about `.dev/`, `eval-workspaces/`, `*-workspace/`, or any pattern that would have stopped the workspace from being staged for commit. The repo has _no_ "workspaces are local artifacts, not source" intent expressed in gitignore. So the file-placer can't be accused of ignoring a gitignore signal — there isn't one.

(Suggestive but not load-bearing: the SuperClaude-specific section ignores `.serena/`, `.superclaude/`, `*.backup`. The author of those entries clearly thought about local-only state, but stopped before workspaces.)

### F6 — `make verify-sync` WOULD have caught this — but only if run, and the message would have misled

`Makefile:179-187` (the reverse check inside `verify-sync`):
```
for skill_dir in .claude/skills/*/; do \
    name=$$(basename "$$skill_dir"); \
    case "$$name" in __*) continue;; esac; \
    if [ ! -d "src/superclaude/skills/$$name" ]; then \
        echo "  ❌ MISSING in src/superclaude/skills/: $$name (not distributable!)"; \
        drift=1; \
    fi; \
done; \
```

Because `sc-release-split-protocol-workspace/` existed in `.claude/skills/` but never in `src/superclaude/skills/`, this loop would have flagged it as drift and exited non-zero. So the safety net mechanically exists.

But two failures of governance let it through:

1. **No CI runs `make verify-sync`.** Greppable evidence: `grep -n "verify-sync\|sync-dev\|lint-architecture" /config/workspace/IronClaude/.github/workflows/*.yml` returns nothing. None of the four CI workflows (`quick-check.yml`, `test.yml`, `publish-pypi.yml`, `pull-sync-framework.yml`) call any of the sync- or architecture-lint targets. The check is opt-in via local `make`.

2. **The error message is wrong for this failure mode.** The message says `MISSING in src/superclaude/skills/: <name> (not distributable!)`. That phrasing assumes the author _intended_ the directory to be a skill and forgot to add it to `src/`. The actual failure is the opposite: the directory is _not_ a skill and shouldn't be in `.claude/skills/` at all. A diligent author hitting this message would likely respond by copying the workspace into `src/superclaude/skills/` to "fix the drift" — making the bug worse.

### F7 — `lint-architecture` only validates skill ↔ command pairing; it never rejects non-skill directories

`Makefile:233-336`. The checks are:

- Check 1/2: every `commands/*.md` with `## Activation` has a matching `skills/sc-<name>-protocol/` and vice versa.
- Check 3/4: command size limits.
- Check 6: paired commands have `## Activation`.
- Check 8: skill SKILL.md frontmatter completeness.
- Check 9: skill `name:` field ends in `-protocol`.

Note Check 9 only fires on `sc-*-protocol/SKILL.md`. The misplaced workspace had no `SKILL.md`, so Check 9 silently skipped it. There is no check of the form "every directory in `.claude/skills/` is a skill" or "every directory in `.claude/skills/` has a SKILL.md." The architecture lint defines what skills _must look like_ but not what `.claude/skills/` membership _means_.

### F8 — The CLI installer's skill-detection logic implicitly does define membership — but only at install time

`src/superclaude/cli/install_skills.py:139-141`:
```python
# Check for SKILL.md or skill.md as indicator
if any((item / m).exists() for m in ("SKILL.md", "skill.md")):
    installed.append(item.name)
```

End-user behavior: the workspace would have been silently ignored at install (no SKILL.md). So users wouldn't have ended up with a 100-file eval workspace shipped to them. But this is "the bug doesn't reach users" — not "the bug doesn't happen." It also encodes the de-facto rule (skill = directory with SKILL.md) only inside Python, not in any document an author would read.

### F9 — The sync-dev contract DOES distinguish skills from non-skills, and the workspace would have been excluded from forward sync

`Makefile:111-114`:
```
for skill_dir in src/superclaude/skills/*/; do \
    skill_name=$$(basename "$$skill_dir"); \
    case "$$skill_name" in __*) continue;; esac; \
    if [ -f "$$skill_dir/SKILL.md" ] || [ -f "$$skill_dir/skill.md" ]; then \
```

`sync-dev` only copies forward directories with SKILL.md. So if the author had put the workspace in `src/superclaude/skills/` first and then run `make sync-dev`, it would have been skipped (no SKILL.md). What actually happened is the inverse: the workspace was created _directly in `.claude/skills/`_, never touching `src/`. That bypasses sync-dev entirely. The system has a forward filter; it has no symmetrical "the only things allowed in `.claude/skills/` are things sync-dev would have put there" enforcement except inside `verify-sync`, which (per F6) is opt-in.

### F10 — The skill itself does not direct authors to `.claude/skills/`

I read the `sc-release-split-protocol/SKILL.md` and the `release-split.md` command file. The command's `--output` table line:

> `| --output | -o | No | <spec-dir>/release-split/ | Output directory for all artifacts |`

And its example:

> `/sc:release-split path/to/release-spec.md --output .dev/releases/current/v3.1/`

Both point to `.dev/releases/...` — i.e., the consumer-facing run produces artifacts there. Neither file mentions where to put the _eval scaffolding for testing the skill itself_ (fixtures, harness scripts, iteration outputs). That's the conceptual gap: the artifact-placement rules cover "where do users' runs go?" but not "where does the developer's testing apparatus go?"

### F11 — The `*-workspace` suffix is a real attractor, but only weakly

The skill is named `sc-release-split-protocol`. The dev created `sc-release-split-protocol-workspace` — a strict suffix of the skill name. Hypothesis: the suffix made "sibling of skill" feel like a natural location ("the workspace _for_ this skill"). Counter-evidence: the v2.15 prior art (`sc-cli-portify-workspace`) used the same suffix pattern and correctly landed under `.dev/releases/complete/v2.15-cli-portify/`. So suffix-confusion alone doesn't explain placement; what changed is the loss/absence of the documented "put it under your release dir" anchor.

## Root cause (one-paragraph hypothesis)

The misplacement is **a governance gap, not a rule violation**. There is no document the author could have read to know where this artifact belongs. The only project-wide artifact-placement rule (global CLAUDE.md item 5) is too generic to bind. The project-level CLAUDE.md cites three governance docs (`PLANNING.md`, `TASK.md`, `KNOWLEDGE.md`) that don't exist at the cited paths. `.dev/` has no README explaining its 11 sibling subdirectories. The single piece of prior art (`v2.15-cli-portify/sc-cli-portify-workspace`) is buried inside a completed release and has never been promoted to a documented pattern. Meanwhile, `make verify-sync` _can_ detect the failure but is not run by CI and emits a misleading error ("not distributable!") that suggests the wrong fix. The `*-workspace` suffix amplifies the conceptual conflation — it reads as "this skill's workspace," which makes "next to the skill" feel correct — but the suffix is symptom, not cause; the cause is the absence of a written rule that would override the suffix-led intuition.

## Confidence in this hypothesis: 0.7

Reasoning for the score:

- **What's solid (pushes up):** The doc gap is verifiable (CLAUDE.md → missing files), the CI gap is verifiable (no workflow runs `verify-sync`), the misleading error message is verifiable in the Makefile text, and the prior-art inventory is exhaustive (one previous workspace, in a different location).
- **What's not solid (caps at 0.7):** Without interviewing the author or reading the commit's PR description, I cannot prove they would have followed a documented rule had it existed. It's also possible the author conceptually believed "this _is_ part of the skill" (RCA #1's territory) and would have placed it next to the skill regardless of governance. The naming/governance angle is _necessary_ — the rule isn't written down — but I cannot prove it's _sufficient_. RCAs #1 and #2 may carry more causal weight; this one explains why nothing caught the mistake, more than why it was made.
- The 0.7 reflects: high confidence the gap exists and contributed; moderate confidence it's the dominant cause vs. behavioral/tooling factors.

## Refactor proposal

Five governance-layer changes, ordered by leverage. Each is small enough to land in a single PR and addresses one verifiable gap above.

### R1 — Add `.dev/README.md` defining the layout (addresses F3, F4, F10)

A short manifest at `.dev/README.md` listing each subdirectory with one line on its purpose. Specifically:

- `.dev/eval-workspaces/<skill-name>/` — developer scaffolding for evaluating a skill in active development. Local artifacts only; not distributable; not synced to `.claude/`.
- `.dev/evals/<topic>/` — completed eval runs and their outputs (consumer-facing eval results, not skill-development scaffolding).
- `.dev/releases/{current,complete,backlog,archive,templates}/` — release lifecycle directories.
- `.dev/research/`, `.dev/benchmarks/`, `.dev/test-fixtures/`, `.dev/test-sprints/`, `.dev/tasks/`, `.dev/resurrection-contracts/` — one line each.

This is also the place to write the rule explicitly: **"Workspaces, fixtures, harness code, and iteration outputs go under `.dev/`, never under `.claude/skills/`."**

### R2 — Add a `verify-sync` extension that names this exact failure (addresses F6, F7)

Either extend `verify-sync` or add a new `verify-skills-membership` target that runs:

```
for skill_dir in .claude/skills/*/; do
    name=$(basename "$skill_dir")
    case "$name" in __*) continue;; esac
    if [ ! -e "$skill_dir/SKILL.md" ] && [ ! -e "$skill_dir/skill.md" ]; then
        echo "❌ ERROR: .claude/skills/$name has no SKILL.md — not a skill, must not live here. Move to .dev/."
        drift=1
    fi
done
```

This produces the _correct_ error message ("not a skill, move to `.dev/`") instead of the current misleading one ("not distributable"). It's also the missing Check #X that `lint-architecture` doesn't cover.

### R3 — Run `verify-sync` and `lint-architecture` in CI (addresses F6)

Add two steps to `.github/workflows/quick-check.yml`:

```yaml
- name: Verify sync
  run: make verify-sync

- name: Architecture lint
  run: make lint-architecture
```

The local-only opt-in is the bigger half of the gap. Mechanical detection that's never invoked is decorative.

### R4 — Add a `*-workspace` blocklist pattern in the skills directory (addresses F11)

In the new `verify-skills-membership` target (R2) or as a separate check, also reject any `.claude/skills/*-workspace*` directory by pattern, with an explicit message: "Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`. The `-workspace` suffix is reserved for developer scaffolding and is forbidden in the skills tree."

This is belt-and-suspenders. R2 catches "any non-skill directory"; R4 specifically calls out the suffix attractor identified in F11. Cheap to add.

### R5 — Fix or delete the broken pointers in project CLAUDE.md (addresses F2)

Either: (a) restore `PLANNING.md`, `TASK.md`, `KNOWLEDGE.md` at the documented paths, OR (b) update CLAUDE.md to remove the references or point to the actual locations under `.dev/`. CLAUDE.md is the document a new contributor reads first; broken references corrode every other governance signal.

## Acceptance criteria

A future skill author, in good faith, attempting to create eval scaffolding for a new skill:

1. Reads `.dev/README.md` and finds an explicit rule for where workspaces go (R1).
2. If they nevertheless put it in `.claude/skills/`, `make verify-sync` and `make lint-architecture` (locally and in CI) flag it with a message that names the correct fix (R2, R3, R4).
3. The CI failure blocks the PR (R3).
4. The error message tells them to move it to `.dev/`, not to "add it to `src/superclaude/skills/` for distribution" (R2 fixes the misleading-message problem).
5. CLAUDE.md's references resolve to actual files (R5).

Concretely verifiable:

- `cat .dev/README.md | grep -i "eval-workspaces"` returns the rule.
- `mkdir .claude/skills/test-non-skill && make verify-sync` exits non-zero with a message containing "not a skill" or "move to `.dev/`."
- `mkdir .claude/skills/foo-workspace && make lint-architecture` exits non-zero referencing the `-workspace` suffix.
- `grep verify-sync .github/workflows/quick-check.yml` finds the new step.
- All paths cited in `/config/workspace/IronClaude/CLAUDE.md` exist.

## Limitations / what this hypothesis can't explain

- **Why this skill author specifically.** The same governance gap has existed for the lifetime of the repo and most authors don't misplace artifacts here. So the gap is necessary but not sufficient to fire on a given person on a given day. A behavioral or skill-design factor (RCA #1) likely co-triggered.
- **Why now.** If the prior `sc-cli-portify-workspace` was placed correctly under `.dev/releases/complete/v2.15-cli-portify/`, an earlier author already knew the convention. Either (a) that knowledge was tribal and didn't propagate, or (b) the evaluation tooling for this skill (RCA #2's territory) emitted artifacts to `.claude/skills/` by default and the author followed the tool. This RCA can't distinguish those two without reading commits / interviewing.
- **The conceptual conflation question.** Asked whether the author conflated "workspace for testing this skill" with "part of this skill" — I have no direct evidence either way. The `*-workspace` suffix is a weak attractor (F11); the prior-art counter-example (`sc-cli-portify-workspace` correctly placed) suggests the suffix alone isn't decisive. A code-archaeology pass on the author's commit message and PR thread would settle this; I didn't have those.
- **Whether `.dev/eval-workspaces/` (the chosen relocation target) is itself the right convention.** The only documented prior art (v3.2 fidelity-refactor tasklist) said evals go under the release directory, and the only prior workspace (v2.15) followed that. A new top-level `.dev/eval-workspaces/` is a third convention. This RCA flagged the divergence (F4) but didn't adjudicate it; that decision belongs to RCA #1 / a separate convention-setting pass.
- **Distribution risk vs. development hygiene.** F8 establishes that the install path silently filters non-skills, so the bug never reached end users. So the severity ceiling is "developer hygiene + repo cleanliness," not "broken release." If a future change tightens the installer (e.g., copies the entire `.claude/skills/` tree verbatim), the severity rises. R2-R4 should land before any such change.
