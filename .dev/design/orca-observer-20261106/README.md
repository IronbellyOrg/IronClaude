# Orca observation design package

Original, offline terminal-design prototypes for the Stably.ai Orca environment. This package is not related to github.com/orca-cli/orca and is not an orchestrator, scheduler, approval service or worktree manager.

## Preview and collaborate on GitHub

**[View all twenty embedded designs](PREVIEWS.md)** · **[Discuss in issue #409](https://github.com/IronbellyOrg/IronClaude/issues/409)**

The preview page renders the actual PNGs inside GitHub. The package includes both PDF portfolios, all ANSI/plain/ASCII/SVG/image exports, scenario fixtures, source ledger and reproducible renderer/tests. Download the complete ZIP linked from #409 to use the self-contained galleries offline: GitHub's repository viewer displays HTML source rather than executing it. This is a design collaboration branch, not a production integration or deployment.

## What is being delivered

Set 1: Signal Bridge, Fleet Quilt, Time Loom, Worktree Atlas, Decision Desk, Proof Gate, Budget Engine, Relay Map, Delta Deck and Watchkeeper.

Set 2, requested subsequently: Leverage Board, Attention Ledger, Handoff Switchboard, Loop Detector, Collision Lens, Outcome Ledger, Revision Drift, Mission Pulse, Owner Load and Shift Brief. These additional agent-supervision compositions share the fixture and renderer, not the first set's layout functions. Their exports, gallery and PDF live under `agent-focus/`.

Each delivered set has a self-contained offline gallery, ten primary PNG/SVG designs, ANSI/plain/ASCII exports, a contact sheet and a PDF portfolio. Designs render separately at 160, 116 and 80 terminal columns. Nothing invokes operational controls. Evidence-inspector navigation and fixture playback are local only.

## Reproduce

From the IronClaude root:

```sh
uv run --with-requirements .dev/design/orca-observer-20261106/requirements.txt python .dev/design/orca-observer-20261106/render.py
uv run --with-requirements .dev/design/orca-observer-20261106/requirements.txt python .dev/design/orca-observer-20261106/render.py --batch 2
uv run --with-requirements .dev/design/orca-observer-20261106/requirements.txt python .dev/design/orca-observer-20261106/tests/test_designs.py
node .dev/design/orca-observer-20261106/tests/test_gallery.cjs
node .dev/design/orca-observer-20261106/tests/test_gallery.cjs .dev/design/orca-observer-20261106/agent-focus/gallery.html
```

Show one terminal snapshot using `render.py --show <concept-slug> --width 116`; slugs are listed in manifest.json after generation. `NO_COLOR=1` disables ANSI styling. The `.ascii.txt` exports are strictly ASCII. No process is started for live observation and no periodic collection occurs.

Open `gallery.html` directly from disk. No web server, network fetch or CDN is required. Arrow keys switch designs, j/k select inspector records, Space holds/resumes the view, Tab moves focus. Changing a fixture while held queues the choice; resume shows the latest choice and discloses skipped intermediate fixture observations. The owner/search filter applies only to the explicitly labeled inspector; overview remains global. All IDs and values are synthetic.

## Design and evidence boundaries

- One deterministic base fixture: eight orchestrators, 80 current sessions and 80 mapped worktrees. This equality is illustrative, never assumed by the data model.
- Scenario variants exercise different scales, unequal ownership, shared/unmapped worktrees, historical sessions, missing fields, stale/disconnected sources and duplicate/out-of-order events.
- Lifecycle settlement, report status, acceptance, current tests and human approval are independent.
- Dirty is not dangerous, stale is not failed, overlap is not a proven merge conflict, and an inspectable evidence packet is not admitted.
- Spend is a measured subtotal with coverage and time window. Unknown cost does not become zero.
- No system-wide installs, production configuration changes, commits, pushes, PRs, deployments or operational controls.

See `data-dictionary.md`, `sources.json`, `integration-gaps.md` and `QA.md` for precise claims and limitations. Previous prototype files are preserved unchanged.

## Framework direction

The prototype renderer is Python/Pillow, not a production-stack commitment. The provided TUIBBS-scp manifest was independently checked at a6d7e7f: Bubble Tea v2.0.6, Lip Gloss v2.0.3 and Bubbles v2.1.0 are pinned there. The Charm stack is the leading production candidate for a separate observer executable after a human chooses a design. No BBS application code or third-party screenshot is copied into this package; optional SSH/forms/animation stacks are not needed for this offline study.

## Honest completion

Check QA.md and the export manifest for observed runs. Five-second readability is a target, not a measured human result. No capacity, latency, operational correctness or live Orca integration benchmark is claimed.
