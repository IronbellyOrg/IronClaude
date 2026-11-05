a24bee3484cfe56ddbb5f08758649b66709e5d2a
family=notes-accuracy
defect form: a sentence in t5-notes.md that contrasts old and new adviser behaviour and is not backed by the ladder text in retry.md
command: grep -n -E "haiku|sonnet|opus|instead|used to" .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-051649/artifacts/t5-notes.md
before:
18:the fallback ladder (`haiku`, `sonnet`, `opus`) was always used.
23:`T1Model01=claude-opus-5-5`) runs the primary ladder instead:
30:| 3 (top) | `T1Model01` | `claude-opus-5-5` | Claude |
35:  model id. A `claude-sonnet-*` executor matches no primary rung, so its tier is
43:  escalations that used to reach `haiku`, `sonnet` and `opus` now reach those
44:  models instead. A workspace that does not export all four variables keeps the
coupled sites: t5-notes.md lines 14-17 (claim that the fallback ladder was always used before the change)
after:
18:the fallback ladder (`haiku`, `sonnet`, `opus`) was always used.
23:`T1Model01=claude-opus-5-5`) runs the primary ladder instead:
30:| 3 (top) | `T1Model01` | `claude-opus-5-5` | Claude |
35:  model id. A `claude-sonnet-*` executor matches no primary rung, so its tier is
44:  (`claude-opus-5-5`), the GPT T1 model `T1Model02` (`gpt-6.1-sol`), and
46:  adviser A. Under the fallback ladder the advisers were `sonnet` (for a `haiku`
47:  executor) and `opus`, plus the GPT T1 model (`refs/retry.md`, fallback table);
48:  no adviser ran on `haiku`. A workspace that does not export all four
