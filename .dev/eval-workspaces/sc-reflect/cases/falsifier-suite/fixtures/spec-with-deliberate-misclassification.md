# PLACEHOLDER — iteration-3 authors full fixture. Spec §12.5 line 1013.

# Spec — Hypothetical Read-Through Cache Feature (placeholder)

## Overview

This is a placeholder specification used by the `T2-converges-on-wrong` falsifier case (`../T2-converges-on-wrong.yaml`). Iteration-3 follow-up will replace this placeholder with a full specification whose `## DELIBERATE_MISCLASSIFICATION` block contains a tasklist-vs-diff misalignment that should be detected as a `regression` deviation by the reflect protocol — *if* the heterogeneous-reviewer-ensemble guarantee actually holds.

The intent is that this fixture will be combined with a deliberately-broken tasklist-vs-diff pair where:

- The tasklist says "extend the existing public API endpoint" (non-breaking change).
- The diff actually changes the return shape of the existing endpoint (breaking — regression).
- A single-model self-review pass would plausibly conclude "no deviation" because the diff implements the *spirit* of the tasklist item.
- The heterogeneous reviewer ensemble, blind-calibrated, MUST recognize the silent contract break and emit `deviation_class: regression`.

## Stub feature description

The hypothetical feature is a small read-through cache helper added to an existing service. Three short paragraphs that an iteration-3 author will replace:

The service currently exposes a `GET /items/{id}` endpoint that returns a single item record as a flat JSON object. The proposed feature adds an LRU-bounded read-through cache in front of the underlying datastore so that repeated reads for the same id return in under 5ms.

The tasklist for this feature has three items: (1) add the LRU helper, (2) wire it into the GET handler, (3) add a cache-hit/cache-miss metric. None of the tasklist items mention changing the return shape of the endpoint.

A correct implementation would leave the response shape unchanged. A subtly-wrong implementation — the one used by this falsifier — wraps the response in `{"cached": <bool>, "item": <record>}` to expose cache status, silently breaking every existing client.

## DELIBERATE_MISCLASSIFICATION

<!--
TODO_ITERATION_3: Iteration-3 fills this block with:

1. The exact tasklist (3 items, none authorizing a return-shape change).
2. The exact diff that wraps the response (silently breaking the API contract).
3. A pre-seeded `expected_deviation_class: regression` annotation against the wrapping hunk.
4. A note explaining why a single-model self-review would plausibly miss this, and why a heterogeneous ensemble + blind calibration should NOT miss it.

The block is intentionally empty in v1.0 because authoring it requires iteration-3-level fixture-design care: the misclassification must be *subtle enough* to fool single-model self-review but *unambiguous enough* that "regression" is the only defensible classification when the protocol is working correctly. Empty in v1.0; populated in iteration-3.
-->
