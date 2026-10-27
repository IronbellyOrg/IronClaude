# D-0002 — Evidence: `commands/validate-roadmap.md` CLI Surface Alignment

| Field | Value |
|---|---|
| Task | T01.02 |
| Roadmap Item | R-002 |
| Drift Item | B-2 |
| Deliverable | D-0002 |
| Date | 2026-05-26 |
| Source File Edited | `src/superclaude/commands/validate-roadmap.md` |
| CLI Reference | `superclaude roadmap validate --help` (`src/superclaude/cli/roadmap/commands.py:327-393`) |
| Decision Posture | Option 1 (CLI-faithful rewrite) — see `design-decision.md` row B-2 |

## Linkage

- **B-2 → D-0002.** B-2 (`release-scope.md:60-74`) called out frontmatter naming drift, command-vs-CLI flag-set drift, output-dir drift, and missing NFR-006 documentation in `src/superclaude/commands/validate-roadmap.md`. The design decision (`design-decision.md` B-2 row) selected Option 1: rewrite the slash-command surface to mirror the CLI 1:1, including frontmatter, flags, output directory, N≥2 adversarial-merge condition, and NFR-006 exit-code documentation.
- **D-0002** is the resulting source-file edit at `src/superclaude/commands/validate-roadmap.md`, plus this evidence record.

## Source-file parity check

CLI surface (canonical) from `src/superclaude/cli/roadmap/commands.py:327-393`:

| Surface Element | CLI value |
|---|---|
| Usage | `superclaude roadmap validate [OPTIONS] OUTPUT_DIR` |
| Positional arg | `OUTPUT_DIR` (must contain `roadmap.md`, `test-strategy.md`, `extraction.md`) |
| `--agents` | Comma-separated `model[:persona]`; default `opus:architect` |
| `--model` | Override model for all validation steps; default `""` |
| `--max-turns` | INTEGER; default `100` |
| `--debug` | Flag; enable debug logging |
| Output dir | `<OUTPUT_DIR>/validate/` (`validate_executor.py:474`) |
| Routing | `len(config.agents) == 1` → single-agent reflection; else → multi-agent reflect + adversarial merge (`validate_executor.py:479-487`) |
| Exit code | Always 0, NFR-006 (`commands.py:385` — `"Surface results as CLI output (exit 0 per NFR-006)"`) |

`src/superclaude/commands/validate-roadmap.md` (post-edit) matches each row above:

- Frontmatter `name:` set to `sc:validate-roadmap` (was `validate-roadmap`).
- Usage line: `/sc:validate-roadmap <OUTPUT_DIR> [options]`.
- Arguments section names `OUTPUT_DIR` and requires the three pipeline artifacts.
- Flag table contains exactly `--agents`, `--model`, `--max-turns`, `--debug` with the CLI defaults and descriptions.
- Output dir documented as `<OUTPUT_DIR>/validate/`.
- Routing-behavior block states N=1 → single-agent reflection and N≥2 → adversarial merge.
- NFR-006 exit-0 behavior stated in the lede, in the flag block, and in the Boundaries / Will Not section.

## Removed inference-only validate flags

The following flags from the prior file have been removed because they have no CLI counterpart (per `verification.md:54-72` and `release-scope.md:60-74`):

| Flag | Reason removed |
|---|---|
| `--specs` / `-s` | No CLI counterpart — CLI takes only `OUTPUT_DIR`. |
| `--output` / `-o` | CLI writes to `<OUTPUT_DIR>/validate/` automatically. |
| `--exclude` / `-x` | No CLI counterpart. |
| `--depth` / `-d` | No CLI counterpart. |
| `--max-agents` | No CLI counterpart — agent count is set by the length of `--agents`. |
| `--skip-adversarial` | No CLI counterpart — adversarial merge auto-runs at N≥2. |
| `--skip-remediation` | No CLI counterpart — CLI validate does not run remediation. |
| `--report` / `-r` | No CLI counterpart — single report at `<OUTPUT_DIR>/validate/validation-report.md`. |
| `--prior-taxonomy` | No CLI counterpart. |

## Added (previously missing) CLI flags

- `--agents` (default `opus:architect`)
- `--model` (default `""`)
- `--max-turns` (default `100`)
- `--debug`

## NFR-006 documentation

The post-edit file states "always exits 0 per NFR-006" in three places (lede paragraph, flag-block exit-code note, and the Boundaries → Will Not section), satisfying the acceptance criterion in `phase-1-tasklist.md:103`.

## Adversarial-merge N≥2 condition

The "Routing behavior" subsection of the Flags block makes the N≥2 condition explicit, matching `validate_executor.py:479-487`. The Boundaries section reiterates the dimension-count rule (7 baseline / 9 input-aware), aligned with the design-decision row for B-9.

## Acceptance criteria check (`phase-1-tasklist.md:99-104`)

- ✅ Frontmatter `name: sc:validate-roadmap`.
- ✅ Mirrors CLI `validate <OUTPUT_DIR>` usage, flags, examples.
- ✅ Output directory documented as `<OUTPUT_DIR>/validate/`.
- ✅ States adversarial merge runs only when N≥2 agents.
- ✅ States CLI validation exits 0 per NFR-006.
- ✅ Evidence at this path links B-2 → D-0002 and lists removed inference-only validate flags.

## Sync follow-up (B-12)

This edit lives only at `src/superclaude/commands/validate-roadmap.md`. A subsequent `make sync-dev` is required (and tracked under B-12 / Phase 5) before `.claude/commands/sc/validate-roadmap.md` reflects the change. Per repo rules, `.claude/` mirrors are not staged or committed.
