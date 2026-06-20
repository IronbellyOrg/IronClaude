# QA Report — Operational Actionability (Phase Gate 6 content lens)

**Topic:** sc-bare-review M8/M9 migration — 6 OPS docs + env-readiness script
**Date:** 2026-06-16
**Phase:** ops-guide-qualitative (operational-actionability lens)
**Fix cycle:** N/A (fix_authorization: FALSE — report only)
**Reviewer stance:** ADVERSARIAL — assumed >=5 vague/wrong procedures existed; hunted for them.

---

## Overall Verdict: FAIL

One **CRITICAL** operational-accuracy defect in `rollback-procedure.md`: the entire rollback
premise (what was deleted, by which commit, and which SHA to restore from) is factually wrong
when checked against git. An operator who follows it during a real incident will NOT recover the
legacy path the doc promises. Plus two IMPORTANT actionability gaps (an un-shown "collection
script" the metrics doc leans on, and an untestable date placeholder). The env-readiness
script ↔ doc 1:1 parity check **PASSES** and the script executes cleanly.

---

## Script run result (raw)

```text
== MultiModelSwarm environment readiness ==
   (OPS-002 preflight — see docs/swarm/env-readiness.md)

[ OK ] Python 3.12 (>= 3.10) via 'python3'.
[ OK ] UV present (uv 0.9.17).
[ OK ] httpx importable ('uv run python -c "import httpx"').
[ OK ] Click importable ('uv run python -c "import click"').
[ OK ] Rich importable ('uv run python -c "import rich"').
[WARN] tmux not found — OPTIONAL. The default inline 'swarm run' works without it; only '--detached' requires tmux.
[ OK ] T2 proxy env contract complete (T2ProxyUrl, T2ProxyKey, 4 model slot(s)).

-- summary --
   warnings: 1   failures: 0
[ OK ] environment ready for swarm run.
   (1 optional warning(s) — non-blocking.)
exit=0
```

Exit 0, no bash syntax error, clean execution → meets the script-health bar.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | env-readiness script ↔ doc 1:1 (same checks, same required/optional, same T2 vars) | PASS | 7 checks in both; tmux warn-only in both (script L97-101 / doc §1 row 6); T2ProxyUrl/T2ProxyKey/T2Model01..09 in both; slot max 9 in both. |
| 2 | Script executes cleanly (no syntax error) | PASS | exit=0, output above. |
| 3 | Script constants match source of truth | PASS | `T2_MODEL_MAX_SLOTS=9`, `T2_PROXY_URL_ENV="T2ProxyUrl"`, `T2_PROXY_KEY_ENV="T2ProxyKey"`, `T2_MODEL_ENV_PREFIX="T2Model0"` all confirmed in `config.py:51-63`. |
| 4 | operator-runbook commands are invocable / subcommands exist | PASS | `run_cmd/status_cmd/logs_cmd/attach_cmd/kill_cmd/scaffold_cmd` in commands.py; `validate-lenses` registered in `__init__.py:179`; `bare-review` lens registered in `lenses/__init__.py:106`. |
| 5 | observability recipes cite accurate artifact constants + enums | PASS | All 5 filename constants confirmed in commands.py:85-113; `SwarmStateValue` (models.py:71-77), `EventType` (78-84), `WorkerStatus` (69) cited line ranges are EXACT; log line shape (`logging_.py:167,186`) verbatim correct. |
| 6 | watch-interval default/min claim | PASS | runbook claims default `2.0`, min `0.01`; commands.py:2519-2520 `FloatRange(min=0.01), default=2.0`. |
| 7 | rollback-procedure: "what was deleted, by which commit, restore-from SHA" | **FAIL** | See CRITICAL-1. Files were NEVER `git rm`'d; b0de1479 is 28 commits back, not the parent. |
| 8 | rollback Option A actually restores the legacy path | **FAIL** | See CRITICAL-1. `git revert 2355bfe1` only un-modifies SKILL.md; scripts are still in HEAD. |
| 9 | post-release-metrics: "collection script" is runnable as described | FAIL (IMPORTANT) | "aggregation/collection script" referenced 4× (§Collection model, §Review window, §Backlog loop step 1) but never provided or located; operator cannot run it. |
| 10 | post-release-metrics review-window date is actionable | FAIL (MINOR/IMPORTANT) | `<set on M9 exit: release_date + 14 days>` is an un-resolvable placeholder; correctly flagged HUMAN-DECISION, but no review can be scheduled until bound. |
| 11 | rollback tabletop sign-off honesty | PASS | Correctly left PENDING/UNSTAMPED; explicitly NOT validated. Good operational honesty. |
| 12 | lens-contribution-policy pointer resolves | PASS | `docs/dev/lens-contribution-policy.md` exists; `_validate.py` + `swarm validate-lenses` exist. |

---

## Summary

- Checks passed: 8 / 12
- Checks failed: 4 (1 CRITICAL cluster spanning items 7+8, 2 IMPORTANT, 1 MINOR)
- Critical issues: 1 (rollback factual model is wrong)
- Issues fixed in-place: 0 (report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | **CRITICAL** | `rollback-procedure.md` L33-44, L62-133, L148-149 | The rollback doc's factual model of the migration is wrong on three independently-verifiable points. (a) It states the 5 legacy files were "retired (**deleted via `git rm`**) by MIG-003 (T08.07)" — but `git log --all --diff-filter=D` finds **NO commit** that ever deleted any of them; they still exist byte-identical in committed HEAD (`2355bfe1`). The deletions exist **only as uncommitted staged `D` entries in the working-tree index** (`git status --short` shows `D` for all 5), not in history. (b) `git show 2355bfe1 --name-status` shows the migration commit only **Modified** `SKILL.md` plus added `.dev/` artifacts — it `git rm`'d nothing. (c) The doc calls `b0de1479` "the commit immediately before the thin-caller migration"; the actual parent of `2355bfe1` is **`00576c43`**, and `b0de1479` is **28 commits** back (`git rev-list --count b0de1479..HEAD` = 28). **Operational consequence:** Rollback Option A (`git revert 2355bfe1`) will only revert the SKILL.md text edit — the legacy scripts are *already in HEAD*, so the revert does not "re-introduce the deleted scripts/refs in one operation" as L65-67 promise. Option B (`git checkout b0de1479 -- …`) restores files that already exist (no-op for content, since they are byte-identical) while implying recovery from deletion that never happened. An operator in a real incident acts on a false mental model and does not get the recovery the doc guarantees. | Re-derive the rollback model from actual git state. Either (i) if the intended end-state is that the legacy files ARE deleted, land that deletion as a real commit first, then the doc's `git rm`/restore narrative becomes true; or (ii) rewrite the doc to state the real situation: the legacy files remain committed in HEAD and are only staged-for-deletion in the working tree, so "rollback" = `git restore --staged` + `git checkout` of the working-tree deletions (or simply not committing them), NOT a `git revert`/`git checkout b0de1479`. Fix the parent-SHA claim (`00576c43`, not `b0de1479` as "immediately before"). Add `refs/templates/bare-review-output.md` to the file inventory (it existed at b0de1479 and still exists, modified — the doc omits it entirely). |
| 2 | IMPORTANT | `post-release-metrics.md` L37-40, L128-129, L139-140 | The metrics framework's entire collection step depends on "an ad-hoc script" / "the aggregation script" / "the collection script over the window's `--output` directories" — referenced 4 times as the operational mechanism — but no script is provided, named, or located, and no per-metric jq/parse recipe is given (contrast observability-procedure.md, which gives concrete `jq` one-liners per recipe). An operator cannot execute M1–M7 collection without first inventing the tooling. This is "names a command without showing how to invoke it." | Either ship the aggregation script and cite its path, or replace each metric's "Source" line with a concrete copy-pasteable `jq`/parse recipe (the artifact fields are already enumerated — they just need to become runnable commands, as observability-procedure.md already does). |
| 3 | IMPORTANT | `post-release-metrics.md` L122-126 + `rollback-procedure.md` L162-183 | Two procedures end in unresolved HUMAN-DECISION placeholders (review-window date `<release_date + 14 days>`; tabletop sign-off table all blank). The HONESTY is correct and should stay — but as written, neither procedure is *executable to completion* today, so an operator validating "is the ops handoff done?" gets an ambiguous answer. | Acceptable to leave PENDING, but add an explicit operator-facing line in each: "This deliverable is NOT operationally complete until [date bound at M9 exit / tabletop run + table stamped]." The metrics doc has this; the rollback doc has it for the tabletop but should also state the doc's *factual claims* are unverified until the rehearsal exercises them (which would have caught CRITICAL-1). |
| 4 | MINOR | `rollback-procedure.md` L116-120 | Option B's paste-ready block ends with `git add src/.../scripts/ refs/prompts.md refs/output-template.md` + a `git commit`. This is a multi-line composed command sequence; per the project's no-multiline-paste constraint the commit step is fine single-line, but the `git checkout b0de1479 -- \` continuation (L105-110) uses backslash line-continuation which the operator's terminal cannot paste as one unit. | Collapse the `git checkout … -- <paths>` into a single physical line (no `\` continuation), or instruct the operator to run it via a script file. |

---

## Adversarial-axis attribution

- **CRITICAL-1** is an **AX-1 (drift)** + **AX-2 (contradiction)** finding: the doc's cited facts (deletion commit, parent SHA, "immediately before") have drifted out of sync with the actual git history, and they internally contradict the verifiable repository state. This is exactly the stale-citation pattern the drift axis exists to catch — and it is the highest-impact class because rollback docs are consulted under incident stress where a false model is most dangerous.
- **IMPORTANT-2** is an **AX-3 (omission)**: a required operational touchpoint (the collection tooling) is absent from the plan.

---

## Tool-engagement summary

- Read: 6 (script + 5 of the 6 OPS docs in full; 6th doc lens-contribution-policy read)
- Bash/Grep: 8 (script run; config.py constants; commands.py constants + subcommands; models.py enums; logging_.py shape; git history forensics ×4; lens/validator existence)
- Web research: none required (all claims local-file / git-verifiable). Tavily not invoked.

**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

Every pass/fail condition above is backed by a specific tool result (git SHA, file:line, or
command output), not judgment. The CRITICAL finding in particular was re-tested three independent
ways (`--diff-filter=D` history scan, `git show --name-status` of the migration commit, and
`rev-list --count` of the SHA distance) to rule out a false positive.

## QA Complete
