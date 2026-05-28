# D-0001 — Evidence: `commands/roadmap.md` CLI Surface Alignment

| Field | Value |
|---|---|
| Task | T01.01 |
| Roadmap Item | R-001 |
| Drift Item | B-1 |
| Deliverable | D-0001 |
| Date | 2026-05-26 |
| Source File Edited | `src/superclaude/commands/roadmap.md` |
| CLI Reference | `uv run superclaude roadmap run --help`; `src/superclaude/cli/roadmap/commands.py` `run` command |
| Decision Posture | Option 1 (CLI-faithful rewrite) — see `design-decision.md` row B-1 |

## Linkage

- **B-1 → D-0001.** B-1 called out `/sc:roadmap` command-surface drift from the shipped `superclaude roadmap run` CLI. The design decision selected CLI-faithful convergence for usage, flags, examples, output wording, and cosmetic-remediation controls.
- **D-0001** is the resulting source-file edit at `src/superclaude/commands/roadmap.md`, plus this evidence record.

## Source-file parity check

Canonical local CLI surface from `uv run superclaude roadmap run --help`:

| Surface Element | CLI value represented in `src/superclaude/commands/roadmap.md` |
|---|---|
| Usage | `superclaude roadmap run [OPTIONS] INPUT_FILES...` → `/sc:roadmap [OPTIONS] INPUT_FILES...` |
| Positional input | `INPUT_FILES...` accepts 1-3 markdown files: spec, TDD, and/or PRD in any order |
| Output default | `--output PATH`; default is parent dir of spec-file / first input file |
| `--agents` | Comma-separated `model[:persona]`; default `opus:architect,haiku:architect` |
| `--depth` | `quick`, `standard`, or `deep`; default `standard` |
| `--resume` | Skip steps whose outputs already pass their gates; re-run from first failing step |
| `--dry-run` | Print step plan and gate criteria without launching subprocesses |
| `--model` | Override model for all steps; default per-agent model for generate steps |
| `--max-turns` | INTEGER; default `100` |
| `--debug` | Debug logging to `output_dir/roadmap-debug.log` |
| `--no-validate` | Skip post-pipeline validation step |
| `--allow-regeneration` | Allow FR-9 over-threshold regeneration patches |
| `--no-convergence` | Disable spec-fidelity convergence engine |
| `--retrospective` | Optional advisory retrospective context; missing file is not an error |
| `--input-type` | `auto`, `tdd`, or `spec`; default `auto` |
| `--tdd-file` | Supplementary TDD context path |
| `--prd-file` | Supplementary PRD context path, auto-wired from `.roadmap-state.json` on `--resume` when omitted |
| `--no-compress` | Disable lossless markdown compression for LLM-consumed inputs |
| `--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` | Default enabled; auto-fix pure-cosmetic gate failures before halting |
| `--strict-no-remediation` | Disable cosmetic-failure auto-remediation entirely; alias for strict high-stakes runs |
| `--help` | Show help and exit |

`src/superclaude/commands/roadmap.md` (post-edit) matches the CLI surface above:

- Frontmatter `name:` remains `sc:roadmap`.
- Usage line is `/sc:roadmap [OPTIONS] INPUT_FILES...`.
- Arguments and flag table describe 1-3 positional markdown inputs and the parent-directory default output.
- The flag table includes the current CLI run flags, including source enrichment, convergence, compression, and cosmetic-remediation controls.
- Examples use positional inputs, `--output`, `--resume`, `--dry-run`, `--agents`, `--depth`, and `--strict-no-remediation`.
- The output layout states `--output` wins and otherwise the parent directory of the first input file is used.

## Deprecated inference-only flags

The following prior slash-command flags are explicitly marked unsupported because they have no current `superclaude roadmap run` CLI counterpart:

| Flag | Replacement / status |
|---|---|
| `--specs` | Unsupported; use positional `INPUT_FILES...` for 1-3 markdown inputs. |
| `--template` / `-t` | Unsupported; the CLI uses content detection and prompt builders rather than template selection. |
| `--multi-roadmap` | Unsupported; use `--agents` and CLI debate depth controls. |
| `--interactive` / `-i` | Unsupported; no current CLI run counterpart. |
| `--compliance` / `-c` | Unsupported; no current CLI run counterpart. |
| `--persona` / `-p` | Unsupported; use `--agents model[:persona]`. |

## Cosmetic gate auto-remediation lane

The post-edit file names all required cosmetic-remediation controls:

- `--allow-cosmetic-remediation`
- `--no-allow-cosmetic-remediation`
- `--strict-no-remediation`

This satisfies the B-1 requirement to name the cosmetic gate auto-remediation lane in the command surface.

## Acceptance criteria check (`phase-1-tasklist.md` T01.01)

- ✅ Usage, flag table, examples, and output wording mirror the local current `superclaude roadmap run --help` surface.
- ✅ `--specs`, `--template/-t`, `--multi-roadmap`, `--interactive/-i`, `--compliance/-c`, and `--persona/-p` are explicitly marked unsupported/deprecated rather than documented as active flags.
- ✅ Parent-directory default output behavior is documented.
- ✅ `--allow-cosmetic-remediation`, `--no-allow-cosmetic-remediation`, and `--strict-no-remediation` are documented.
- ✅ Evidence at this path links B-1 → D-0001 and summarizes the source-file parity check.

## Sync follow-up (B-12)

This edit lives at `src/superclaude/commands/roadmap.md`. A subsequent `make sync-dev`, global command refresh, `make verify-sync`, parity check, and affected roadmap tests are required after this evidence is written.
