899d63c1792e090ec3f76d4691057618edb155d6
## family support-denominator
defect form: the denominator of support(c) is not the sum of calibrated confidences of all complete reviewers that the source names.
command: grep -nE 'support|n_complete|best\[' src/superclaude/cli/review/cluster.py
before:
13:  finite number from 0 to 1 (not a bool); a finding with no usable entry has no support value.
35:- support(c) = sum, over the distinct reviewers in c, of the highest calibrated confidence of that reviewer's members
37:  that has no calibrated confidence has support None and is listed in uncalibrated.
41:- disputed: support below 0.5, or members disagree on blocking, or members carry two different non-null
44:  mean support over blocking clusters that are not chained and have a support value, or None when no such cluster
316:def _cluster(index: int, group: list[dict], n_complete: int) -> dict:
326:            best[m["reviewer_id"]] = max(
330:    support = None if uncalibrated else sum(best[r] for r in reviewers) / n_complete
341:        (support is not None and support < 0.5)
365:        "support": support,
385:    counted = [c for c in blocking if not c["chained"] and c["support"] is not None]
392:            sum(c["support"] for c in counted) / len(counted) if counted else None
coupled sites: the module docstring lines about support, the disputed rule (support < 0.5), the cluster_agreement mean, and the tests of support/disputed/agreement in tests/review/test_review_cluster.py.

after:
13:  finite number from 0 to 1 (not a bool); a finding with no usable entry has no support value.
39:- support(c) = sum, over the distinct reviewers in c, of the highest calibrated confidence of that reviewer's members
40:  in c, divided by the sum of w(r) over all complete reviewers. support is at most 1, and is 1 when c holds, for every
42:- support is None, and the cluster is listed in uncalibrated, when a member has no calibrated confidence. When a
44:  denominator is unknown: every cluster has support None and is listed in uncalibrated.
48:- disputed: support below 0.5, or members disagree on blocking, or members carry two different non-null
51:  mean support over blocking clusters that are not chained and have a support value, or None when no such cluster
333:            best[m["reviewer_id"]] = max(
337:    support = None if uncalibrated else sum(best[r] for r in reviewers) / total
348:        (support is not None and support < 0.5)
372:        "support": support,
404:    counted = [c for c in blocking if not c["chained"] and c["support"] is not None]
411:            sum(c["support"] for c in counted) / len(counted) if counted else None
