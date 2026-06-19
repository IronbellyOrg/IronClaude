# Swarm Bug Review — Pre-flight Stopped Before Run

## What I was asked to do

Run a swarm bug review (correctness/bug-finding) on `/tmp/swarm-wizard-probe/tiny.py`,
practice/stub run first.

## What happened: I stopped before dispatching

Following the swarm-wizard protocol's Input Contract and Wave 2 pre-flight, I checked the
target **before** firing any swarm command. The target is too small to review, so I stopped
rather than launching a run that would fail.

### Why I stopped (plain language)

The swarm tool needs something substantial to review. It enforces a **minimum size floor of
50 non-whitespace bytes** — roughly a few lines of real code. Anything smaller can't produce a
meaningful multi-reviewer analysis, so the CLI rejects it up front.

Your file is essentially empty for review purposes:

- Path: `/tmp/swarm-wizard-probe/tiny.py`
- Total size: **4 bytes**
- Non-whitespace bytes: **3** (the file is just `x=1`)
- Required minimum: **50 non-whitespace bytes**

So it's about 47 non-whitespace bytes short of the floor. If I had launched the run anyway, the
swarm CLI would have failed its internal size check and printed a terse rule code on stderr
instead of a helpful message — which is exactly the confusing failure this wizard exists to
prevent.

(For the record, the internal name for that floor is the CLI's "IMM-4" rule — but you don't need
to know that to fix it; the point is just "the file's too small to review.")

## Helpful next step — pick one

1. **Point me at a real file.** Give me a source file with at least a handful of lines of actual
   logic (a function or two — comfortably past ~50 non-whitespace characters) and I'll run the
   bug-review practice (stub) run on it immediately, then offer the real multi-model run.

   Example: `Run a swarm bug review on src/superclaude/cli/swarm/<file>.py`

2. **Point me at a directory entry / larger module.** If `tiny.py` was just a placeholder, tell
   me which real module under `/tmp/swarm-wizard-probe/` (or anywhere) you actually want reviewed.

3. **Grow the probe file.** If you specifically want to test against this path, add real code to
   `/tmp/swarm-wizard-probe/tiny.py` so it clears ~50 non-whitespace bytes, and I'll re-run the
   pre-flight and proceed.

I did **not** dispatch a swarm run, and nothing was launched against the proxy. The validated
plan (3-reviewer `bare-review` lens, stub practice run first) is ready to fire the moment we have
a large-enough target.

## Resolved plan (held, not executed)

- Goal: find bugs / correctness issues
- Lens: `bare-review` (the stable lens for "review my code for bugs")
- Transport: `stub` first (safe practice run), then real only on your go-ahead
- Reviewers: 3 (lens default)
- Target: BLOCKED — `/tmp/swarm-wizard-probe/tiny.py` is below the 50-non-whitespace-byte floor
- Status: **cancelled / not run** — awaiting a valid target
