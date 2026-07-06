---
name: post-release
description: "Post-release follow-through: synchronize and create a shipped version's entire external surface — user docs, technical docs, install/deploy scripts (validated by real end-to-end runs), and human-run e2e test guides. Runs AFTER the release gate tags a version."
category: documentation
complexity: high
allowed-tools: Read, Glob, Grep, Skill
mcp-servers: [sequential, serena]
personas: [scribe, devops, qa, analyzer]
---

# /sc:post-release - Post-Release Follow-Through

## Required Input

- A release `<version>` that has an existing tag (e.g. `v1.4.1`). This command runs **after** the release gate tags the version.

```bash
/sc:post-release <version> [options]
```

## Usage

```bash
# Basic: bring the external surface of a tagged release current
/sc:post-release v1.4.1

# Send artifacts to an explicit output directory
/sc:post-release v1.4.1 --output docs/testing/v1.4.1/
```

## Options

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `<version>` | Yes | — | An existing release tag (e.g. `v1.4.1`) |
| `--output` | No | `docs/testing/<version>/` | Output directory for report, manifest, and test guides |

## Behavioral Summary

Drives five workstreams over the tagged release, each following **scan → consolidate → update → create → verify**:

- **A — User documentation**, **B — Technical documentation**, **C — Install & deploy scripts** (proven by a real end-to-end run), **D — User-facing e2e human-test guides**, **E — Sysop-facing e2e human-test guides**.

Auto-detects **ground-up vs additive** mode from prior manifests, anchors every scan to the **tagged commit** (not the working tree), classifies the install surface into one of four classes (`vm-e2e`, `local-deploy`, `package`, `no-install-surface`), and writes a manifest that makes the next release additive. Honesty is the whole point: a documented gap or a genuinely-failing install is a correct outcome, never fabricated coverage.

## Examples

### Ground-up first run

```bash
/sc:post-release v1.0.0
```

### Additive follow-up with explicit output dir

```bash
/sc:post-release v1.4.1 --output docs/testing/v1.4.1/
```

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:post-release-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.

## Boundaries

**Will:**

- Provide the interface only: required input, usage, options, examples, and the Activation handoff to `sc:post-release-protocol`.
- Point new users at `/sc:post-release` as the primary surface.

**Will Not:**

- Contain the five-workstream protocol body, lazy ref-loading instructions, return-contract fields, or the `SC:POST-RELEASE:RUN` / `SC:POST-RELEASE:RESULT` machine-readable headers — those live only in the protocol skill.
- Advertise the legacy standalone invocation surface. The deprecated `post-release-update` skill is retained only as a **compatibility wrapper** for one cycle; new invocations go to `/sc:post-release`.
- Rename the protocol skill directory to bare `sc-post-release`. The protocol skill MUST live at `sc-post-release-protocol` (the Activation handoff above targets `sc:post-release-protocol`); the installer's `_has_corresponding_command` in `src/superclaude/cli/install_skills.py` strips only the `sc-` prefix, so a bare `sc-post-release` would be silently skipped as "served by the `post-release` command" and never installed standalone.

## Related Commands

| Command | Integration | Usage |
|---------|-------------|-------|
| `Skill sc:post-release-protocol` | Activation target | Full Wave 0–5 post-release protocol |
