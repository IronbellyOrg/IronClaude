# Running "swarm" code review on your file

Good news — yes, `swarm` is exactly the tool for this. It fans your file out to several AI reviewers at once, then merges their findings into one report. I've already done a safe test run on your file, and below I'll explain what I found and the one thing you'll need to do a *real* review.

## First, what I can see in your file

Before involving any AI, I read `/tmp/swarm-wizard-probe/demo.py` myself. It has two small functions, and two things jump out as likely bugs:

1. **`add(a, b)` returns `a - b`** — it subtracts instead of adds. A function named "add" almost certainly should return `a + b`. This is very likely the bug you sensed.
2. **`divide(numerator, denominator)`** has no check for dividing by zero. If `denominator` is `0`, Python will crash with a `ZeroDivisionError`.

So your instinct was right — there's at least one clear bug, plus one risky edge case.

## How I ran swarm on your file (the safe test)

Swarm has different "lenses" — preset review styles. For finding bugs in code, the right one is **`bare-review`** (it's the stable, general-purpose code-review lens; the others are experimental and aimed at things like docs or refactoring).

I ran it in a **safe practice mode** first. Here is the exact command I used:

```
uv run superclaude swarm run --lens bare-review --target /tmp/swarm-wizard-probe/demo.py --output /tmp/swarm-wizard-probe/out --transport stub
```

In plain terms:
- `--lens bare-review` → use the code-review style
- `--target ...demo.py` → review your file
- `--output ...out` → put the report files in this folder
- `--transport stub` → **this is the important one.** "stub" means "don't actually call the real AIs — just run the whole machine with placeholder reviewers to prove everything is wired up correctly." I used this because it's free, instant, and needs no AI account/keys.

It ran successfully — 3 workers, 3 results, no errors — and wrote a merged report to `/tmp/swarm-wizard-probe/out/merged.md`.

## Important: the test run did NOT actually review your code yet

Because I used `--transport stub`, the AIs were *not* really consulted. If you open the report, you'll see the findings table is **empty** and the verdict line literally says `stub:...`. That's expected — the stub is a placeholder/dry-run that only confirms the plumbing works. It is **not** a real review of your bug.

Think of it like test-flushing the pipes before turning on the water: everything's connected, but nothing real has flowed through yet.

## To get a REAL multi-AI review

To actually have the AIs read your file and report the bug, you switch the transport from `stub` to the real one (`openai_compat`):

```
uv run superclaude swarm run --lens bare-review --target /tmp/swarm-wizard-probe/demo.py --output /tmp/swarm-wizard-probe/out --transport openai_compat
```

The one catch: the real mode needs **AI model credentials** configured in your environment (an API endpoint + keys for the models swarm dispatches to). I don't have those available in this session, so I can't run the live version for you right now — it would fail at startup with a "missing environment" error rather than give you a fake answer.

So the next step is on your side or your admin's: make sure the model credentials are set up, then run the command just above. Once those are in place, that single command will give you the genuine several-AIs-at-once review, and the bug in `add()` should show up in the findings table.

## Summary

- Your file does have a bug: `add()` subtracts instead of adds, and `divide()` can crash on zero. (My own read — confirmed without AI.)
- I successfully ran swarm in **safe stub mode** to prove it works on your file. That run is a dry-run with placeholder results, **not** a real review.
- For a real multi-AI review, re-run with `--transport openai_compat`, which requires model credentials to be configured first.
