# ptytest — Quarterly Drift Review Checklist

**Owner:** RyanW (maintainer)
**Cadence:** Quarterly (90-day rolling window from the last completed review)
**Anchor:** See `PROVENANCE.md` §3 *Next review due*
**Satisfies:** AC10 (fork SHA pin + drift policy); R5-mit (ptytest fork drift mitigation)
**Authoring tasks:** T02.03 (initial procedure) + T02.26 (target-date schedule + R5-mit)

This checklist is the standing procedure for the AC10 drift-review obligation on
the vendored `ptytest` fork under `src/superclaude/cli/eval/pty/`. The review
is a *read-only* re-verification of the pinned upstream SHA; resync work is
spun out into its own task only when the checklist surfaces a security- or
behavior-relevant change. The default outcome of a clean review is to roll the
review anchor forward 90 days and record the row in `PROVENANCE.md` §4.

## Target review dates (R5-mit)

The cadence anchor lives in `PROVENANCE.md` §3 (currently `2026-08-20`). The
table below pre-schedules the next four reviews from that anchor so the owner
can put them on a calendar without recomputing the offset. Each row is a
*target* — actual completion may slip up to one calendar week without bumping
the cadence; later than that, record the slip in `PROVENANCE.md` §4 as a row
with outcome *Pin held (late)* and reset the anchor from the actual completion
date.

| # | Target date | Quarter | Owner | Status |
|---|-------------|---------|-------|--------|
| 1 | 2026-08-20 | 2026 Q3 | RyanW | Scheduled (initial cadence anchor) |
| 2 | 2026-11-18 | 2026 Q4 | RyanW | Scheduled |
| 3 | 2027-02-16 | 2027 Q1 | RyanW | Scheduled |
| 4 | 2027-05-17 | 2027 Q2 | RyanW | Scheduled |

When a review row is recorded in `PROVENANCE.md` §4, mark that row above as
`Completed YYYY-MM-DD` and append a new row at the bottom for the next
quarter so the table always covers at least the next two pending reviews.

A review may be triggered out-of-band (i.e. before the next scheduled date) by
any of:

- A CVE published against `pexpect` or `ptytest` upstream.
- An upstream commit touching the prompt-detection or ANSI-stripping code paths.
- A failing CI run on `tests/cli/eval/test_pty_vendor.py` after an unrelated
  refactor (signal that the pin has implicitly diverged from on-disk content).

## Step 1 — Confirm the current pin

1. Open `src/superclaude/cli/eval/pty/PROVENANCE.md` and copy the **Pinned
   upstream SHA** from §2.
2. Confirm the SHA matches the upstream commit it claims by visiting
   `https://github.com/brandon-fryslie/ptytest/commit/<pinned-sha>` and
   verifying the commit page loads (i.e. upstream has not force-pushed the SHA
   out of existence).
3. If the SHA no longer resolves upstream, **escalate to a resync task
   immediately** — a missing pin is a release blocker, not a quarterly review
   item.

## Step 2 — Fetch the current upstream HEAD

1. Query `GET https://api.github.com/repos/brandon-fryslie/ptytest/commits/master`
   (or equivalent) and record the current upstream HEAD SHA and commit date.
2. If `upstream HEAD == pinned SHA`, jump to Step 5 (no drift; record clean
   review).
3. Otherwise, record the diff range `<pinned-sha>..<head-sha>` for Step 3.

## Step 3 — Triage the upstream diff

1. Read the upstream diff range from Step 2 via
   `https://github.com/brandon-fryslie/ptytest/compare/<pinned>...<head>`
   (or `git log --oneline <pinned>..<head>` against an upstream clone).
2. Classify each upstream commit into one of:
   - **Security** — CVE fix, sandbox escape, command-injection patch.
   - **Behavior** — change to prompt detection, ANSI stripping, line buffering,
     timeout semantics, `pexpect.spawn` argument handling.
   - **Maintenance** — docs, CI, formatting, dependency floors, test-only changes.
3. Any **Security** classification escalates to a resync task in the same
   review pass. **Behavior** classifications require a judgment call from the
   review owner (resync if our consumers — `PtyDriver`, `PtyStream` — depend on
   the changed surface; defer otherwise with a recorded rationale).
   **Maintenance** classifications never trigger a resync.

## Step 4 — Re-verify license + attribution alignment

1. Diff the upstream `LICENSE` file at the new HEAD against
   `src/superclaude/cli/eval/pty/LICENSE`. They MUST be byte-identical text
   (whitespace included) for the pin to remain valid.
2. If the upstream LICENSE text changed:
   - Update `src/superclaude/cli/eval/pty/LICENSE` in the same commit as any
     SHA resync.
   - Re-verify the canonical attribution clause in the top-level `NOTICE`
     against any upstream LICENSE text changes; update both `NOTICE` and the
     D-10 ADR body in `.dev/releases/current/cliEval/decisions.md` if the
     clause moved.
3. If the upstream LICENSE text is unchanged but the pin is being held (no
   resync), record this verification in the review log row anyway — it is the
   AC10 commitment.

## Step 5 — Record the review outcome

1. Append a row to `src/superclaude/cli/eval/pty/PROVENANCE.md` §4 with:
   - **Date** of review (`YYYY-MM-DD`).
   - **Reviewer** name.
   - **Upstream SHA at review** (the HEAD captured in Step 2).
   - **Outcome** — one of: *Pin held* / *Resync scheduled* / *Resync landed*.
   - **Notes** — 1-line summary of the triage call (e.g. *"3 maintenance
     commits upstream; no behavior drift; pin held."*).
2. If outcome is *Pin held*: bump the **Next review due** date in §3 by 90 days
   from today.
3. If outcome is *Resync scheduled* or *Resync landed*: open / link a tracked
   resync task, follow the §3 *Resync procedure* steps, and set **Next review
   due** based on whether the resync is in the same window (keep anchor) or
   carries past (bump 90 days from the resync landing date).

---

**Acceptance:** This checklist satisfies AC10 (fork SHA pin + drift policy). It
is intentionally a *procedure* document, not an automation. Automation of the
quarterly trigger (e.g. a calendar reminder or a CI job that opens an issue
90 days after the last review row) is out of scope for T02.03 and may be added
later under a separate R5-mitigation task (per `T02.26` notes in
`phase-2-tasklist.md`).
