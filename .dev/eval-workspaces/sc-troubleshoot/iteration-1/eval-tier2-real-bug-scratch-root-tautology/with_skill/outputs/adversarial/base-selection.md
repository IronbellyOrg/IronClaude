# Base Selection

**Selected base**: Fix-1 (call-site drop of `output_dir=` kwarg)

Rationale: it carries the minimum-risk, minimum-surface production change that resolves the reported symptom. Fix-3's test plan attaches naturally to that base; Fix-2's helper guard does not attach naturally (it is its own change with its own review concerns) so it is split into a follow-up task.
