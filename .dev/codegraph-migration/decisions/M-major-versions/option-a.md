# Option A: majors bump exactly like minors and patches

- Same pipeline for every newer release: verify, rewrite pin, prove, open a ready PR when the proof passes.
- The PR title and body say "MAJOR" when the major number changed, and the body carries the release notes.
- Rationale: one code path; the proof plus the human merge is the review; no special state to test.
- Cost: a 2.0 that keeps tool names and the registration shape but changes tool arguments or outputs passes the proof and lands as a normal-looking ready PR; the reviewer must notice the "MAJOR" word.
- Code: no extra branch in the bump logic beyond the title word.
