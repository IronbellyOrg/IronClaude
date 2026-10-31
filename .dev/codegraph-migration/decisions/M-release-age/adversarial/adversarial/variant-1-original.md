# Option A: no minimum age

- Bump to `releases/latest` as soon as it is newer than the pin.
- Rationale: fastest; the proof and the human merge are the safety net.
- Cost: lands same-day releases that upstream fixes days later (1.4.0 and 1.4.1 same day); a pulled or re-tagged release can already be in an open PR; churn of one PR per quick patch.
