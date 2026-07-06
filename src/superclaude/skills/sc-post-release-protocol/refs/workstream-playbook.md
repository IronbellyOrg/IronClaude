# Per-Workstream Playbook

Detailed procedure for each of the five workstreams. SKILL.md gives the summary; this file is what a workstream lead reads before scanning. Every workstream follows the same spine — **scan → consolidate → update → create → verify** — so the sections below only spell out what differs: what to scan, what "update" means, what counts as a gap, and what "done" requires.

## Table of contents

- [Shared spine](#shared-spine)
- [Discovery glob sets](#discovery-glob-sets)
- [Workstream A — User documentation](#workstream-a--user-documentation)
- [Workstream B — Technical documentation](#workstream-b--technical-documentation)
- [Workstream C — Install & deploy (with real e2e)](#workstream-c)
- [Workstream D — User-facing e2e human-test guides](#workstream-d--user-facing-e2e-human-test-guides)
- [Workstream E — Sysop-facing e2e human-test guides](#workstream-e--sysop-facing-e2e-human-test-guides)

---

## Shared spine

1. **Scan (read-only, parallel).** Partition the workstream's surface across scanner agents (by directory or by feature area — whichever gives non-overlapping slices). Each scanner returns a structured inventory: what exists, what it covers, and — crucially — what it *claims* vs. what the code actually does. Scanners never write source or docs.
2. **Consolidate.** One consolidator merges the inventories into:
   - a **coverage matrix**: rows = the release's features/capabilities; columns = the artifacts that should cover them (doc, guide, script). Each cell is `present-and-current` / `present-but-stale` / `missing`.
   - a **gap list**: the `missing` and `present-but-stale` cells, each with the evidence for the verdict.
3. **Update** the `present-but-stale` artifacts to match `<version>`.
4. **Create** the `missing` artifacts.
5. **Verify.** Run the workstream's acceptance check (below), and — for decompose-path workstreams — a reflection/verification pass (the project's gate if it has one, else a self-review) over the produced/edited files against the coverage plan.

The feature/capability list that seeds the matrix comes from the release: the version's PRD/TDD, `CHANGELOG.md` for `<version>`, and (additive mode) the `<prev_tag>..<this_tag>` code diff. In ground-up mode with no PRD, derive the capability list by scanning the actual feature surface (CLI commands, public API, entry points, user-facing flags).

---

## Discovery glob sets

Run these at the start; treat hits as candidates, misses as findings. Hardcode nothing — a repo that keeps runbooks in `ops/` instead of `docs/runbooks/` should still be found because you glob broadly and then classify by audience/content.

- **User docs (A):** `README*`, top-level `*.md` (excluding contributor/dev files), `docs/user-guide/**`, `docs/getting-started/**`, `docs/guides/**`, `docs/**/quickstart*`, anything whose content addresses "you, the user/operator."
- **Technical docs (B):** `docs/decisions/**`, `docs/adr/**`, `docs/runbooks/**`, `docs/developer-guide/**`, `docs/reference/**`, `docs/architecture/**`, `docs/design*/**`, `ARCHITECTURE*`, `docs/perf*`, `docs/governance*`, `.dev/**` tech notes, `KNOWLEDGE.md`. **API/contract surface** (a documented external interface): `proto/**`, `*.proto`, `*.pb.go`, `api/**`, `openapi*`, `*.graphql` — the wire/plugin contract is a technical surface implementers code against.
- **Install/deploy (C):** `deploy/**`, `install*.sh`, `setup*.sh`, `configs/**`, `config/**`, `systemd/**`, `Dockerfile*`, `docker-compose*`, `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `charts/**`, `helm/**`, `.github/workflows/*deploy*`, `Makefile` (install/deploy/build targets), `update.sh`. **Stateful-service ops:** `migrations/**`, `*.sql`, `db/**`, `schema/**` — DB schema/migrations are part of the new-user deploy path and the upgrade runbook.
- **E2E/VM target (C):** `docs/runbooks/*e2e*`, `docs/runbooks/*deploy*`, `docs/runbooks/*upgrade*`, `**/*vm-access*`, `**/*e2e*vm*`, plus a content grep for "throwaway vm", "deploy vm", "test host", "reference instance", access coordinates.
- **Release (mode + delta):** `.dev/releases/**/post-release-manifest.json` (mode), `.dev/releases/{current,complete}/<version>/**` (PRD/TDD/spec — may be **tag-fuzzy**: `v1.3` for `v1.3.0`, `v1-MVP` for first GA; may all sit under `current/`), `CHANGELOG.md`, `RELEASES.md`. If no per-version dir maps to the tag, seed release intent from `CHANGELOG.md` + `RELEASES.md`.
- **Feature-surface hint (D):** entry points commonly live under `cmd/**`, `bin/**`, `src/**/cli*`, or the package's console-script definitions — reach these when scanning the user-facing capability list, even though they aren't "docs".

Audience classification when a doc could be A or B: **who is the reader and what do they do with it?** A user doc tells someone how to *use* the software; a technical doc tells someone how it's *built* or *operated internally*. When a single file mixes both (common in READMEs), treat the user-facing sections under A and the internals under B rather than forcing the whole file into one bucket.

---

## Workstream A — User documentation

**Scan.** Partition user docs across scanners (e.g. one for `README` + top-level, one per major `docs/` user subtree). For each doc, capture: what version/behavior it currently describes, which features it mentions, and any claim that the code contradicts (stale flags, renamed commands, removed options).

**Coverage matrix rows.** Every user-facing capability in `<version>`. Columns: the user doc(s) that should cover it.

**Update.** Bring stale user docs current: correct changed flags/commands/defaults, add usage for capabilities that changed in `<version>`, fix examples that no longer run. Verify each corrected example against real `--help`/behavior, not memory.

**Create.** For a shipped capability with no user-facing home, create the missing doc (quickstart, feature guide, operator how-to) in the repo's user-doc convention.

**Done when.** Every `<version>` user-facing capability has a `present-and-current` cell, or an explicit, justified deferral in the gap list. No user doc contains a claim the code contradicts.

---

## Workstream B — Technical documentation

**Scan.** Partition technical docs across scanners by subtree (decisions, runbooks, reference, architecture). Apply the **staleness protocol**: a technical doc describes intent or a past state, not necessarily the current one. For every architectural claim, verify against source — services described must have an entry point that exists; call chains must match at least first and last hop; referenced files must exist. Mark each claim `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`.

**Coverage matrix rows.** The implementation surfaces that changed in `<version>` (new/changed subsystems, decisions made, runbooks affected). Columns: the technical doc(s) that should cover them.

**Update.** Reconcile contradicted claims to the actual implementation. Add/append ADRs or design notes for decisions the release embodies. Refresh runbooks whose steps changed.

**Create.** Missing ADR for a significant `<version>` decision, missing runbook for a new operational path, missing architecture note for a new subsystem.

**Done when.** No `[CODE-CONTRADICTED]` claims remain in the touched docs; significant `<version>` decisions/subsystems have technical coverage or a justified gap-list entry.

---

## Workstream C

Install & deploy, **with real end-to-end validation**. This is the only workstream that must actually *run* something to green. It has four target classes; **classify first, then adapt**.

### Classify the install surface

Inspect the discovery hits and pick the class:

| Class | Signal | E2E target |
|---|---|---|
| **VM/e2e** | deploy scripts (`deploy/`, `install.sh`, `systemd/`) **and** an e2e/VM runbook with access coordinates | the throwaway VM described in the runbook |
| **Local-deploy** | deploy scripts / `docker-compose` / container build, but no VM runbook | a clean **local** container or throwaway dir |
| **Package** | ships as a language package (`pyproject.toml`, `package.json`, `Cargo.toml`, …) with no deploy scripts | a **fresh throwaway environment** (clean venv / container) installing the package |
| **No-install-surface** | nothing installable found | none — honest gap + proposed quickstart |

Record the chosen class in the manifest (`install_surface_class`) and report.

### Run to green (the evidence)

The rule is identical across classes: **start from a clean state, follow the documented new-user path for `<version>`, reach a working install, capture the transcript.** What differs is only the target.

- **VM/e2e:** provision/reset the VM per the runbook (get coordinates from the runbook — never hardcode, never store creds in-repo). Build the release artifact for the tag, run the install script(s) clean-state → working, smoke-test the running service, save the transcript. *Worked example (compiled service, e.g. a Go/Rust binary + systemd):* on a clean host, `make build` (or `go build`/`cargo build`) at the tag → run the repo's `deploy/install.sh` (or the deploy runbook's steps) → confirm the service's `--version` reports `<version>` and its start/pre-flight check passes (e.g. `./svc serve --check`, an SSH/HTTP health probe) → capture the transcript. For an N→N+1 release, follow the repo's **upgrade** runbook (signature-verify → drain → swap binary → migration boundary → rollback path) rather than a fresh install.
- **Local-deploy:** build/run in a clean container or throwaway directory. *Worked example (Docker service):* `docker build` (or `make docker`) the tagged source → `docker compose up` (or run the image) → smoke via the service's `--version`/health endpoint (and any `make docker-verify`) → tear down → save the transcript.
- **Package:** create a **fresh** throwaway env (a clean venv / container / temp prefix — *not* the dev environment). Install the package the way a new user would for `<version>` (from the tag/build — `pip`/`pipx install .`, `npm i -g`, `go install`, `cargo install`, as the ecosystem dictates), then exercise the entry point: `--version` (must report `<version>`), `--help`, and one real smoke command. Save the transcript. Validate against the tagged build in an environment that does not inherit the dev install.
- **No-install-surface:** do not fabricate a run. Write an honest gap entry and, where useful, a proposed install-quickstart the maintainers can later make real.

For a **stateful service**, the new-user path includes bringing the schema up — run the repo's migrations the way the deploy path does (a `migrate` step, or in-process auto-migration at boot) and confirm they applied. Missing/broken migrations are a workstream-C failure just like a broken install script.

### Update & create

Fix install scripts/config that the run proved broken or stale for `<version>` (wrong version pins, missing steps, changed prerequisites). Create the guided-setup doc a new user needs (`deploy.md`/quickstart) if it's missing. Every scripted change must be re-validated by another run — **a change you didn't re-run to green is not done.**

### Honesty

A red result is a valid outcome. If the install can't reach green, report exactly where it failed with the transcript, and do not mark C complete. Never write "validated" without a real green transcript behind it. Scrub any secrets from the transcript before saving.

**Done when.** The classified target reached a green install of `<version>` with a saved transcript, **or** the failure is honestly reported with evidence, **or** the class is no-install-surface and that's stated with a proposed quickstart.

---

## Workstream D — User-facing e2e human-test guides

**Scan.** Fan out scanners across the user-facing feature surface (CLI commands, public entry points, user flags, UI flows — whatever this software exposes). For each feature, extract from **real code**: its purpose, correct invocation, inputs, and expected behavior/output. Cite the source (file:line, the command's `--help`, the handler).

**Consolidate.** Coverage matrix rows = every user-facing capability; column = "has a test guide." The gap list is every capability without one.

**Create.** For each capability (or cohesive group), author a walkthrough using `templates/user-test-guide.md`: **preconditions → actions → expected result → pass/fail**, with expected results derived from the code you scanned — never guessed. These are documents a human runs by hand; make each step unambiguous and each expected result checkable.

**Done when.** The set of guides covers the user-facing surface of `<version>` (matrix has no uncovered capability, or gaps are justified), and every expected result traces to real code.

---

## Workstream E — Sysop-facing e2e human-test guides

**Determine existence first.** Before authoring anything, scan for sysop/administrator-only capabilities: gated admin/debug/overlay/spawn/watch/maintenance features, privileged/hidden flags, operator-only commands, capabilities behind an admin role or env gate. Look for the gating mechanism in code (role checks, `--admin`/`--debug` flags, feature gates), not just naming.

**If sysop capabilities exist:** author human-test guides for them with `templates/sysop-test-guide.md`, same rigor as D (preconditions incl. the privilege/gate, actions, expected result from real code, pass/fail).

**If none exist:** state it explicitly — "No sysop-only surface found in `<version>`" — and record it in the manifest (`sysop_capabilities_found: false`). Do **not** invent admin coverage to appear thorough. An honest "none" is the correct deliverable.

**Done when.** Either every discovered sysop capability has a guide, or the absence of a sysop surface is explicitly and truthfully recorded.
