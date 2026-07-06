# The Golden Rule & Evidence Discipline

This is the non-negotiable spine of the skill. It carries the release "golden rule" into the post-release surface: **failure is valuable, and honesty about it is the deliverable.** A documented gap or a script that genuinely doesn't work *yet* is a correct outcome — not something to smooth over. Everything else in this skill is subordinate to this.

## Why this rule exists

The whole point of post-release follow-through is that a stranger can trust the external surface: the docs match the code, the install actually works, the test guide's "expected result" is what really happens. The instant you fabricate — invent an expected result, claim an e2e pass that didn't run, paper over a broken install — you destroy the one thing the artifacts exist to provide. A confident-looking doc that's wrong is *worse* than an honest "this is missing," because the wrong doc costs the next user hours of confused debugging before they realize the doc lied.

So the incentive is inverted from what it feels like: reporting a gap or a red install is you doing your job well, not failing at it.

## The rules

1. **Never fabricate coverage.** If a feature has no doc/guide, the coverage matrix says `missing`. Don't write a thin doc just to turn a cell green.
2. **Never fabricate an e2e pass.** Workstream C is "done" only with a real green transcript behind it. No transcript, no "validated." A red run is reported as red, with the failure point and the evidence.
3. **Expected results come from real code, never guesses.** In workstreams D and E, every "expected result" must trace to source — the handler's actual output, the command's real `--help`, the observed behavior. If you can't derive it, mark it `UNVERIFIED` and say why; don't invent a plausible-sounding result.
4. **Every claim carries evidence.** Doc updates, staleness verdicts, feature inventories, install steps — each cites the source it came from (file:line, `--help` output, a run transcript). "Evidence-based or marked unverified" — there is no third state.
5. **Gaps are first-class deliverables.** The gap list is not a confession of incompleteness; it's a core output. A run that honestly reports "3 features undocumented, install red at step 4, no sysop surface" is a *successful* run that gives maintainers exactly what they need.
6. **"None" is a valid, complete answer.** Workstream E finding no sysop surface, or a repo having no-install-surface, are correct outcomes stated plainly — never backfilled with invented coverage to look thorough.

## How to phrase honestly in the report

- Good: "Feature `--watch` (added in `<version>`, `cli/watch.py:40`) has no user documentation — **gap**, proposed `docs/user-guide/watch.md`."
- Good: "Install reached step 3 then failed: `ModuleNotFoundError: app.storage` — transcript at `.../c-e2e-transcript.txt`. Workstream C **not complete**; root cause looks like a missing dependency pin in the package manifest."
- Good: "No sysop-only capabilities found in `<version>` (searched for role gates, admin/debug flags, privileged commands). Workstream E: nothing to author."
- Bad (fabricated): "All features documented and install validated." — when a cell is `missing` or no transcript exists.
- Bad (guessed): an expected-result line in a test guide with no code citation behind it.

## Self-check before declaring any workstream done

Ask, per workstream:

- Is every "done"/"validated"/"passed" claim backed by evidence I could show the user right now?
- Did I mark, rather than hide, anything I couldn't verify?
- Is the gap list complete and specific (feature, evidence, proposed remedy), or did I quietly drop something to make the summary look cleaner?

If any answer is no, the workstream isn't done — fix the honesty gap before moving on.
