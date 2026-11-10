# Diagnosability Tasklist
**Issue**: BMAD and Ponytail only available where previously installed; not global by default; BMAD should self-create its directories in an unseen project (IronbellyOrg/Coder#478).
**Verdict**: partial  **Complexity**: trivial  **failing_component**: templates/VSCode-AIDev02/image/catalogue/bmad/install.sh  **Round**: 0 of 3  **re-run permitted**: unknown  **discriminator-required**: no  **capability-verdict**: n/a
**branch**: ironbelly/bmad-ponytail-global  **repro-venue-id**: aidev02 workspace boot, profile Default vs Minimal (digits stripped)

## Emitter search
emitters-found: 8 (install.sh:15,23,25,40,43,46,54,60; no edit sites authorized)
already-read-files: 6
usable-capture-routes: 4 (existing artifacts on a booted workspace, read-only: ~/.aidev/status/seed-repo-outcome, ~/.aidev/status/seed-repo-path, ~/.aidev/status/spec2-health/bmad.health.v1, /tmp/catalogue-bmad.log; plus ~/.claude/plugins/installed_plugins.json for Ponytail)
All routes are existing persisted or semi-persisted artifacts; none requires editing production source. Authorization to run commands on an affected workspace is not granted in this run (`re-run permitted: unknown`), so every row below stays pending.

## Discriminator rows
core-rows=0, pack-rows=0, total-rows=0. discriminator-required: no (no producer menu: the symptom is a missing capability, not a categorical value emitted by code).

Pending evidence rows (informational, preregistered; they do not gate the diagnosis; each is a read of an existing artifact on an affected workspace):
- E-1 claim: the reporter's BMAD workspace had no recorded seed repo. observable: contents of ~/.aidev/status/seed-repo-outcome. value-if-true: `skipped` (or any value other than cloned/preserved-valid) | value-if-false: `cloned` or `preserved-valid`. mapping: true => consistent with "BMAD never configured anywhere"; false => the seed repo was configured and the report concerns other repos. Provenance: run/arm/command to be recorded when read. State: pending (could-not-run: no access to the reporter's workspace).
- E-2 claim: BMAD health on the affected workspace is Installed-not-Configured. observable: `configured_state` in ~/.aidev/status/spec2-health/bmad.health.v1. value-if-true: `Installed-not-Configured` | value-if-false: `Configured`. State: pending.
- E-3 claim: Ponytail is installed user-scope on the affected workspace. observable: presence of `ponytail@ironclaude` with `"scope": "user"` in ~/.claude/plugins/installed_plugins.json. value-if-true: present | value-if-false: absent (then check whether the ironclaude slug was selected: profile Default vs Minimal, and ~/.aidev/installed/ironclaude). State: pending. (On the diagnosing workspace this was read: present, user scope, v5.3.3; see tier1-observation.md.)

## Bracket
Not triggered.

## Fix candidate
None proposed. Any change toward user-global or any-repo BMAD reverses a documented owner decision (see doc-context.md) and needs an owner decision first.

## Hard Constraints
- INVOCATION SITES only; ADDITIVE only; no row above edits production source. Annotation `# Diagnosability-tasklist instrumentation: revert after defect closed.` applies to any later instrumentation task; none is proposed.

## Implementation tasks
### Task 1: Read existing artifacts on an affected workspace (task type 4, artifact capture, read-only)
- Invocation site: an operator shell on the affected workspace (not repo source).
- Current code: n/a.
- Steps: read the files named in E-1 to E-3 and record file contents with run/arm/command provenance.
- Rationale: answers Where/Why for the specific workspace (3-W's gaps). Verification: values match the preregistered outcomes. Rollback: none (read-only).

## Verification
Rows E-1 to E-3 recorded with provenance, or marked unobserved.

## Rollback
Nothing to revert.

## Patch-round counter
branch/venue: ironbelly/bmad-ponytail-global / aidev02 workspace boot. Authoritative store not incremented this run (discriminator-required: no). Snapshot value: 0.
