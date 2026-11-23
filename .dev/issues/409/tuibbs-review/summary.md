# Summary: TUIBBS review for the issue 409 observer

TUIBBS-scp at a6d7e7f (2026-10-20), cloned read-only to `/tmp/tuibbs-review`. Paths below are relative to that clone. Detail: `assumptions.md`, `architecture-options.md`, `write-back-stage.md`.

## Recommendation
Option (a): build R1 Signal Bridge as the planned standalone Python + Rich observer, and have `export(view)` write a versioned, additive-only JSON snapshot (fields frozen in architecture-options.md). If TUIBBS is chosen later, it gets a compiled-in, read-only Go screen (AGPL, in the TUIBBS repo) that reads the snapshot, modelled on `internal/ailink/lifecycle_overlay.go:46-61`. Why: TUIBBS screens are all compiled-in Go and its plugins cannot draw (`proto/v1/plugin.proto:61-68`), so a Go screen is needed whatever R1 is written in; a stable data contract is the one thing R1 can usefully give it. Write-back stays out of R1 and out of the snapshot.

## Assumptions: 7 validated, 5 refuted, 3 unverified
- Validated: Python stack does not block TUIBBS; port surface is small (`internal/render/pipeline.go:133-135`); snapshot shape matches TUIBBS's own JSON, additive-only habit (`internal/plugin/dispatch.go:53-62`); an in-tree Go screen is feasible; no copying keeps MIT safe; the read-only boundary holds on both sides (`internal/serve/menu.go:637-640`, "FR-X-13: no write-back"); the NO_COLOR caveat is real and TUIBBS overrides it per session.
- Refuted: a separately shipped module (plugin host unwired, `internal/module/README.md:4-5`); the Python gRPC plugin route; a non-AGPL Go screen inside TUIBBS; TUIBBS as a team platform (no teams; group resolver empty, `internal/auth/provider.go:244-257`); TUIBBS as a stable base (hobby, dogfood-only, `docs/scope.md:17-18`; no successful release).
- Unverified: snapshot transport to the TUIBBS host; whether JSON-only exchange keeps MIT and AGPL separate (legal); cell-width handling of `lipgloss.Width`.
- Correction to the brainstorm: the evidence timestamp is `projection.evidence.lastObservedAt` (merged-requirements.md:328 omits `projection.`).

## Owner decisions
1. Confirm Python + Rich for R1 (still only a recommendation).
2. Put the snapshot export and its schema test in R1 scope.
3. Write-back: approve the boundary change for issue 409 and, separately, ask the TUIBBS owner to amend FR-X-13, before any build. Smallest first stage: answer your own agent's pending question with one of its fixed options, relayed through the coordinator, with 9 gates (write-back-stage.md).
4. Get a licence opinion before a Go screen reads the MIT observer's output.
5. Decide later, not for R1, whether TUIBBS is the staff platform.

## Risks
- TUIBBS docs claim more than its code wires (plugin tiers in CHANGELOG.md:135-140 versus no callers); trust the code.
- Who Orca accepts a `reply` from is unproven; `--from` is a caller-supplied claim. Write-back must relay through the coordinator until that is settled.
- TUIBBS audit key sits beside its database, so its audit chain is forgeable by anyone with host access.
- The PTY door (zero-rewrite path) is a v1 non-goal and unbuilt (`internal/doors/` holds only a README).
