# Command nuance: /sc:swarm-wizard

**Generated**: 2026-10-27 by nuance-swarm-wizard (read-only analysis; only this file written)
**Sources read in full**: `~/.claude/commands/sc/swarm-wizard.md`, `~/.claude/skills/sc-swarm-wizard-protocol/SKILL.md`, `refs/cli-contract.md`, `refs/interview.md`, `refs/run-monitor-summarize.md`, `templates/summary.md`, `~/.claude/skills/sc-bare-review/SKILL.md`, plus the relevant parts of `~/.claude/HOW-WE-WORK.md` and `command-value-by-phase.md`.
**Citation shorthand**: CMD = `~/.claude/commands/sc/swarm-wizard.md`; SKILL = `~/.claude/skills/sc-swarm-wizard-protocol/SKILL.md`; CC = `.../refs/cli-contract.md`; INT = `.../refs/interview.md`; RMS = `.../refs/run-monitor-summarize.md`; HWW = `~/.claude/HOW-WE-WORK.md`; CVP = `command-value-by-phase.md`; BARE = `~/.claude/skills/sc-bare-review/SKILL.md`.
**Labels**: (J) = my judgment, no file states it. UNVERIFIED = not confirmed from a file.

## 1. Status and role
- **What it does**: "Plain-language interactive guide to the superclaude swarm CLI" that interviews, picks a lens, proves it with a stub dry run, then launches a real multi-model review only after a yes (CMD:3, SKILL:121-153). It reviews ONE target file or path per run (INT:27-31). Phase: Review (CVP 2.3 row); two lenses touch other phases (`troubleshoot-hypothesis` = Bug fix, `spec-completeness` = Spec review: CC:46,48).
- **Standalone-invokable, not retired.** User-facing command (CMD:17-22). Lists no dependency on `/sc:task` or `/sc:tasklist`: neither name appears in any file read (checked by reading all six files in full).
- **Overlaps**: `/code-review` (HWW:199), `/sc:auggie-review`, `bmad-code-review`, `bmad-review-edge-case-hunter` (same job as the `edge-case-hunt` lens), `/sc:troubleshoot`, `/sc:reflect`, `/sc:spec-panel`. Downstream consumer, not rival: `/sc:adversarial` (CC:43; BARE:17-19).

## 2. Flags
### 2a. Flags on `/sc:swarm-wizard` itself (CMD:47-55; identical `argument-hint` at SKILL:8)

| Flag | Values | Default | What it changes | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `--goal <text>` | free text | none; asked in interview (CMD:28, INT:10-25) | Pre-seeds the goal so Q1 is skipped; a clear match is confirmed, not menu-picked (INT:23-25) | You already know what to ask the other models | Goal fits two lenses (wizard will ask anyway: SKILL:95-96) |
| `--target <path>` | file or path | none; asked (CMD:29) | Pre-seeds the review target; must exist and hold >=50 non-whitespace bytes or the wizard STOPs (SKILL:49-50, CC:77-78) | Always, when the file is known | Tiny/empty file; a whole feature (one target per run; default cap 4000 lines, `--target-line-cap`, CC:24) |
| `--output <dir>` | directory | `.dev/swarm-runs/<lens>-<ts>/`, `-N` appended if it exists, never overwrites (CMD:51, SKILL:114-116) | Where all run artifacts land | You want the evidence under a task-file or story folder | Reusing the dry-run folder for the real run (real run needs a fresh dir: RMS:33) |
| `--real` | on/off | off (CMD:52) | Signals intent to use real models; a stub dry run STILL runs first (CMD:52, SKILL:126-128). Real run needs go-ahead + green dry run + env contract (SKILL:141-144) | The second-family opinion is worth the cost (section 3) | Proxy not configured: wizard downgrades to a stub run (SKILL:59-60, 193) |
| `--detached` | on/off | off (CMD:53) | Prefers a background tmux run (`swarm-<job_id>`) over a live dashboard (CMD:53, CC:28). Needs tmux on PATH and not nested in tmux (CC:86) | Long real run you will come back to | Already inside tmux; mutually exclusive with `--tui` (CC:83,27-28) |
| `--advanced` | on/off | off (CMD:54) | Unlocks custom-lens / hand-authored JobSpec branch with trust-boundary warnings; `custom-py:` recipes run arbitrary host code (SKILL:103-107, CC:55-57) | Maintainer testing a custom prompt dir | Normal reviews: the 7 shipped lenses cover them |
| `--yes` | on/off | off (CMD:55) | Asks only goal + target, defaults the rest (INT:4, SKILL:85-86) | Repeat runs by someone who knows the lenses | Whether `--yes` also skips the real-run go-ahead is not stated: UNVERIFIED (U9); assume it does not (CMD:87) |

No positional argument. Pre-seed flags are passed to the skill as context (CMD:70-73).

### 2b. Settings the wizard chooses and passes to `uv run superclaude swarm run` (not wizard flags; CC:17-32)

| Setting | Values | Default | What it changes | Notes |
|---|---|---|---|---|
| `--lens` | `bare-review`, `refactor-find`, `edge-case-hunt`, `spec-completeness`, `feasibility-probe`, `troubleshoot-hypothesis`, `doc-completeness` | from interview Q1 (INT:10-21) | Which review prompt/recipe runs; `custom` rejected as a shortcut (CC:41-55) | Only `bare-review` is `stable`; the other six are `experimental` (CC:51) |
| `--transport` | `stub`, `openai_compat` | `stub` on the lens path (CC:22) | `stub` = placeholder text, no network; `openai_compat` = real models via proxy (CC:61-66) | Dry run is always `stub` (SKILL:126) |
| `--reviewers` | 2-4 | 3; 4 for `edge-case-hunt` and `troubleshoot-hypothesis` (CC:23) | Number of independent reviewers; outside range = exit 2 | "More = broader but slower" (INT:43-46) |
| `--target-line-cap` | integer | 4000 (CC:24) | Truncation of the target | Rarely changed |
| `--timeout-sec` | integer | 180 per worker (CC:25) | Per-reviewer time limit | |
| `--label` | text | `swarm-run-lens-<lens>` (CC:26) | Cosmetic; tmux-legal when detached | |
| `--tui` | on/off | off | Live dashboard; real TTY + `--output` only; exclusive with `--detached` and `--resume` (CC:27) | Not for a wizard tailing in a non-TTY (RMS:57-58) |
| `--resume <JOB_ID>` | job id | none | Re-runs only failed workers from `manifest.json` (CC:29, RMS:108-112) | After `partial`/`failed` (SKILL:196) |
| `--force-relens`, `--stdin`, `--auto-inject-guard`, `scaffold`, `validate` | | | In the CLI contract (CC:30-37) but the wizard flow uses them only on the `--advanced` branch (SKILL:103-107) or not at all: `--force-relens`, `--stdin`, `--auto-inject-guard` are not mentioned in SKILL, INT, or RMS | |

### 2c. Does not exist (people may assume)

- `--depth` on the wizard: absent from CMD and SKILL. Depth equivalent is the lens choice plus `--reviewers` 2-4.
- A flag to skip the dry run: none. The stub dry run is a mandatory gate (SKILL:121-128, CMD:87-88).
- `--lens`, `--reviewers`, `--transport` as wizard flags: not in CMD:47-55; the wizard sets them from the interview.
- `--custom-prompt-dir` on `swarm run`: stale doc claim; it is a JobSpec field (CC:117). `--recipe`: no such flag, recipe follows the lens (CC:51).
- Waiting on `done.json` for an inline run: never written there (CC:93-95, 118).
- `/sc:bare-review`: no command exists; `sc-bare-review` is delegate-only (BARE:24).

## 3. Scope x complexity matrix
**Does the command vary by complexity?** Its mechanics do not (same interview, same mandatory dry run, `--reviewers` 2-4 is the only size knob: CC:23). What varies is whether running it is worth the cost. No file gives a threshold for that: HWW lists it once as a choice ("You want reviewers from other AI model families", HWW:154), never inside a level, a numbered workflow step, or 3.11 review/PR steps (HWW:196-199). CVP O8 calls it "extra assurance" (CVP:234). Every cell below is therefore (J) except where a file is cited.

**What a real run costs (all that files state)**: real models via a proxy, "may take a bit" (SKILL:144); up to 180 s per reviewer (CC:25); 2-4 reviewers (CC:23); ONE file per run, truncated at 4000 lines by default (CC:24). A dry run is "free, instant, no setup" (INT:37). No token or money figure appears anywhere (U7). The output is not a verdict: findings are unscored, undeduped, unordered and, for `bare-review`, tagged `suspect: true` and meant for `/sc:adversarial --suspect-source` (CC:51-53; BARE:17-19,54-55). A run is only worth it if someone then triages that output.

**Band definitions for this command (J; signals are the brief's list)**
- LOW: author can name the one file; no secrets, permissions, user input, paths or infrastructure in it; no drift sensitivity. (Analogue only: task-builder TCS <=12 = quick, `task-builder/SKILL.md` around 2406-2441.)
- MEDIUM: 2-5 files in one subsystem, or the file handles user input or file paths, but no secrets/permissions/infrastructure; a driving spec may exist.
- HIGH: the file touches secrets, permissions, auth, infrastructure/deploy scripts or data-loss paths; or "must not drift"; or shared interfaces between stories; or a root cause that `/sc:troubleshoot` could not confirm. (Analogue: task-builder forces `--depth deep` for refactor/remediation `type:` and TCS >=35: same file, O2 and threshold table.)

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J) | SKIP (J) | OPTIONAL (J): `bare-review`, 3 reviewers, on the one risky file |
| B bug fix | SKIP (J) | SKIP (J) | OPTIONAL (J): `troubleshoot-hypothesis` (4 reviewers) only after `/sc:troubleshoot` reports "cause not confirmed" and `--depth deep` did not settle it (HWW:134); experimental lens (CC:51) |
| S single story | SKIP (J) | SKIP (J) | OPTIONAL (J): `bare-review` on the single riskiest file |
| F multi-story feature | SKIP (J) | OPTIONAL (J): `bare-review` on the one or two files with the most risk | WORTH IT (J): one run per high-risk file (not per feature); `edge-case-hunt` (4) where input handling is the risk. Flags: `--real --reviewers 3` |
| R multi-feature release | SKIP (J) | OPTIONAL (J) | WORTH IT (J): before the push, on release-critical files (deploy/install scripts, migrations, permission or secret handling). Flags: `--real`; add `--detached` if several files are queued |
| N new product | N/A (J): a new product has no LOW band | OPTIONAL (J) | WORTH IT (J) on security-foundational files only (auth, payments, data model). `spec-completeness` on a PRD/TDD is OPTIONAL (J): `/sc:spec-panel` is the guide's spec reviewer (HWW:153) |

Every cell assumes real models are reachable. If the proxy is not configured, the wizard only produces a stub run (HWW:154, SKILL:59-60), which is not a cross-model review.

## 4. Choose this or the neighbour
| Neighbour | Decision rule by complexity signal | Cited basis |
|---|---|---|
| `/code-review` (built-in bug review) | Default for every scope: HWW step "Bug review. `/code-review`" (HWW:199) and "One bug review plus the PR monitor is enough" (CVP:234). Add swarm only on top, never instead, and only at HIGH (secrets, permissions, infrastructure, data loss) on a named file. | HWW:199; CVP:234 |
| `/sc:auggie-review` | Auggie gives a whole-branch view (CVP:234); swarm sees one file. Use auggie for breadth across a branch, swarm for a second model family on one risky file. | CVP:234; CC:24 |
| `bmad-code-review` | BMad-lane equivalent of `/code-review` (CVP:234). Same rule: swarm is extra assurance on top. | CVP:234 |
| `bmad-review-edge-case-hunter` | Same job as swarm's `edge-case-hunt` lens. Use the BMad skill by default (no proxy needed); use the swarm lens only when you specifically want other model families to probe input/state boundaries on a HIGH-risk file. | CVP:128; CC:47 |
| `/sc:adversarial` | Not an alternative: it is the next step. `bare-review` and `edge-case-hunt` hand off to it (CC:43,45; BARE:55). Rule: if you ran swarm `bare-review`, running `/sc:adversarial --suspect-source` (or reading `merged.md` yourself) is what turns raw suspect findings into something to act on. A swarm run nobody triages has no value. | CC:51-53 |
| `/sc:troubleshoot` | Always first for a bug (HWW:124-126). `/sc:troubleshoot` already runs its own parallel hypothesis agents on low confidence (HWW:125). Swarm `troubleshoot-hypothesis` only adds other model families when the cause stays unconfirmed. | HWW:125,134; CC:48 |
| `/sc:reflect`, `/sc:spec-panel` | For spec or plan checks these are the routed tools (HWW:153,190-194). Swarm `spec-completeness` hands off to `/sc:reflect` (CC:46); it does not replace the spec trace (`--spec`, `reflect_pre`). | HWW:153,194; CC:46 |
| `/sc:research` / `/tech-research` | Lens `feasibility-probe` hands off to `/sc:research` (CC:47) but HWW routes feasibility of OUR system to `/tech-research` (HWW:142). Prefer `/tech-research`. | HWW:142; CC:47 |
| `/sc:code-review --apply` (named hand-off of `refactor-find`) | No `code-review.md` exists under `~/.claude/commands/sc/` (directory listing); the session skill list shows `code-review` with `--comment`, `--fix`, `--max-findings`, no `--apply`. Do not rely on the `refactor-find` hand-off; use `/sc:cleanup` or `/sc:improve` per HWW 3.7. | CC:44, INT:65; HWW:157-168 |

## 5. What a scheduled checker can see
The wizard writes no task-file frontmatter, no ledger line, and no `.dev/tasks/` entry. Its evidence is a run folder (default `.dev/swarm-runs/<lens>-<ts>/`, CMD:51) or a folder the engineer chose with `--output`.

| Footprint | Path / key | Meaning | Cite |
|---|---|---|---|
| Run state | `<OUT>/.swarm-state.json` keys `job_id`, `state`, `updated`; `state` ends at `terminal` | The run finished | CC:99-102 |
| Run contract | `<OUT>/return-contract.yaml`: `status` (`success`/`partial`/`failed`), `workers_requested/succeeded/failed`, `output_files[]` (`model_label`, `status`, `final_path`), `merged_path`, `recommended_next_command` | How many reviewers finished | CC:103-107 |
| Merged findings | `<OUT>/merged.md`, per-reviewer `*.final.md`, `*.meta.json`, `*.raw.md` | The findings | CC:91-95 |
| Logs | `<OUT>/execution-log.jsonl` and `.md`, `<OUT>/manifest.json` | Event trail | CC:91-95 |
| Detached/resume only | `<OUT>/done.json` | Not written on an inline run | CC:93-95 |

**Stub vs real is the catch.** The mandatory dry run leaves the same file set as a real run (SKILL:129-132), with placeholder text `stub:<model>:<hash>` in the reviewer output (CC:62). A checker must NOT count a dry-run folder as a cross-model review. Whether `manifest.json` or `return-contract.yaml` records the transport is UNVERIFIED (U8); the content marker above is the only documented difference. The wizard's own `cancelled` status (user declined the real run) exists only in the skill's returned fields, not on disk (SKILL:173-175).

Observed 2026-10-27: `.dev/swarm-runs` does not exist in this worktree, and `.gitignore` has no line matching "swarm". No run has been made here, and nothing says whether run folders are committed (CLAUDE.md names only `.dev/tasks/` as always staged). Interview answers and the go-ahead are transcript only.

## 6. Expected-step rule
- **Never an expected step at any scope x complexity.** No level, workflow step, or routing-table step requires it (HWW:154,309,317; the routing row `multi-model-review` has level `-` and `changes_files` no). Absence must never be flagged, including in HIGH cells: those are (J) recommendations, not file rules.
- **Count it as present, not required, only when** a run folder exists with `status` success/partial, real-model content (no `stub:` marker), and a follow-up triage (e.g. `/sc:adversarial --suspect-source`). A stub-only folder means "wizard practised", not "second-family review done". Expected only if a task file or spec explicitly names multi-model review for that work (J; no such file seen).

## 7. Proposed changes to command-value-by-phase.md
**P1. Row at CVP:132 (Review phase, `/sc:swarm-wizard`).**
- Current: `SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | Guide 3.6: real runs need a model proxy set in ~/.aienv (T2ProxyUrl, T2ProxyKey, T2Model01). Whether it is configured here is UNVERIFIED`
- Proposed: keep the six letters as the LOW/MEDIUM baseline, add a complexity qualifier in Notes: `Never required. One file per run (cap 4000 lines), 2-4 reviewers, output is unscored and suspect: needs /sc:adversarial --suspect-source. Judgment: OPTIONAL at HIGH complexity for T, B, S; WORTH IT at HIGH for F, R, N on named high-risk files (secrets, permissions, infrastructure, data loss). Dry run alone is not a cross-model review. Real runs need T2ProxyUrl, T2ProxyKey, T2Model01; configured here UNVERIFIED.`

**P2. R re-rating under "multi-feature release".** No letter changes for this command: R stays OPTIONAL at LOW/MEDIUM and becomes WORTH IT (J) at HIGH. The old R reading in CVP 2.4 ("a release assembles and ships work already built") was about build commands and never applied to this row, so nothing moves because of the redefinition.

**P3. Row O8 at CVP:234.** Current text lists `/sc:swarm-wizard` among "the other four are for extra assurance". Proposed: append "swarm only at HIGH complexity, on one named file, and only if someone will triage its output".

**P4. Row U5 at CVP:289.** Current: "Not checked (env values must not be read or printed). Presence check of variable names only." Proposed: keep, and add a second unknown: whether `uv run superclaude swarm` runs from this repo (no `pyproject.toml` at the repo root; `uv`, `superclaude`, `tmux` are on PATH).

**P5. Note on HWW:291 vs wizard files.** HWW says `sc-bare-review` "is internal (used by /sc:swarm-wizard...)". No wizard file mentions `sc-bare-review`; the wizard drives `swarm run --lens bare-review` itself (CC:43). Record as a documented contradiction in the merged file (not resolvable from files).

**P6. Section 3 or Section 4 of CVP (pairs).** Add: "swarm `edge-case-hunt` is the same job as `bmad-review-edge-case-hunter`; use the BMad skill by default."

## 8. Unverified items
| # | Item |
|---|---|
| U1 | Whether `T2ProxyUrl`, `T2ProxyKey`, `T2Model01` are set in this workspace: not checked, by instruction (names only come from HWW:154 and CC:63-66). |
| U2 | Whether `uv run superclaude swarm ...` works from this repo: not run; no `pyproject.toml` at repo root. SKILL grants only `Bash(uv run superclaude swarm *)` (SKILL:7). |
| U3 | Whether the installed swarm CLI matches `refs/cli-contract.md`: contract was verified 2026-06-19 (CC:5); live `--help` not run (read-only rule). |
| U4 | `/sc:code-review --apply` hand-off for `refactor-find` (CC:44, INT:65): no `~/.claude/commands/sc/code-review.md`; flag set seen only in the session skill list, not a file. |
| U5 | Callers named in BARE:20-21 (`/sc:troubleshoot`, `/sc:reflect`, `/sc:auggie-review`, `/sc:code-review`, `/sc:adversarial`): a grep of `~/.claude/commands/sc/*.md`, `skills/*/SKILL.md` and `skills/*/refs` found no reference to `bare-review` outside BARE and the wizard files, so no evidence any command runs cross-model review implicitly. |
| U6 | HWW:291 says `sc-bare-review` is used by `/sc:swarm-wizard`; no wizard file says so (contradiction, section 7 P5). |
| U7 | Any token, money, or wall-clock cost of a real run: no file states one; only 180 s per-reviewer timeout and "may take a bit". Number of proxy calls per reviewer not stated. |
| U8 | Whether `manifest.json` / `return-contract.yaml` records `stub` vs `openai_compat`; the `stub:<model>:<hash>` marker is stated only at CC:62 and not observed. |
| U9 | Whether `--yes` skips the real-run go-ahead (CMD:55 vs CMD:87, SKILL:143-144). |
| U10 | Whether the team commits or ignores `.dev/swarm-runs/`: no instruction found. |
| U11 | Quality of the six experimental lenses (CC:51): no accuracy evidence in any file. |
| U12 | Any file giving a threshold for "when is a cross-model review worth its cost": none found; section 3 is entirely (J). |
| U13 | Contents of the IronClaude `docs/swarm/wizard-guide.md` linked at HWW:154 and `.dev/swarm-wizard/SWARM-WIZARD-FACTS.md` cited at CC:3: not installed here, not read. |
