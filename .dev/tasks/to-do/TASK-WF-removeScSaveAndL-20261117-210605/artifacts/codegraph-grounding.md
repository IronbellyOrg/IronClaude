# Codegraph grounding

## Run state

- index_state: unavailable (the codegraph MCP server disconnected during this session; no lookup was run)
- token: graph:unavailable
- floor used: git grep, Glob and Read (permanent floor, normal evidence)

## Resolved symbols

The change touches Markdown, JSON fixtures and test lists only; no code symbol is changed. Every file the tasks name was found with `git grep` and read. See ../../../../cleanup/save-load/dependency-map.md (sections A and B).

## Dependents

Dependents of the two commands are the files in the dependency map, found with `git grep` for `sc:save`, `sc:load`, `sc-save`, `sc-load`, `save.md`, `load.md` and quoted bare names. `src/superclaude/cli/`, hooks, Makefile, pyproject.toml, .github and the installer name neither command (checked).

## Pre-check

Every file named in Tasks 1 to 8 exists at plan time (checked against the dependency map, same commit). No dependent is left unnamed by a task; section C of the map lists the references deliberately kept.
