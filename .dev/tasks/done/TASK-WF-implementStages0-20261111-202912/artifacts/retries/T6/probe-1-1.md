bde9bfa57c721f216b47e182a98c8b8709295b67
## family inventory-classification
defect form: hit files are left with no producer/validator/consumer role although the task asks to classify each hit.
command: grep -nE 'unclassified|NAMED_ROLES|def classify' scripts/reflect_consumer_inventory.py
before:
27:1. NAMED_ROLES, exact paths from the task's lists and the spec's "Deferred versioned change" list:
40:4. Everything else is "unclassified" (for example this script and its test, which only name the words).
94:ROLE_ORDER = ("producer", "validator", "consumer", "unclassified", "not in scope")
97:NAMED_ROLES = {
162:def classify(rel: str) -> tuple[str, str]:
164:    if rel in NAMED_ROLES:
165:        return NAMED_ROLES[rel]
171:    return "unclassified", ""
335:    named = [(p, r, s) for p, (r, s) in NAMED_ROLES.items()]
coupled sites: the role-count lines of the report header, the classification rules in the module docstring, tests at tests/review/test_reflect_consumer_inventory.py for classify() and the report counts.

after:
29:1. NAMED_ROLES, exact paths from the task's lists, the spec's "Deferred versioned change" list and the review fix:
118:NAMED_ROLES = {
213:def _writes(suffix: str, lines: list[bytes]) -> bool:
231:def classify(rel: str, data: bytes = b"") -> tuple[str, str, str]:
233:    if rel in NAMED_ROLES:
234:        return (NAMED_ROLES[rel][0], "named", NAMED_ROLES[rel][1])
427:    named = [(p, r, s) for p, (r, s) in NAMED_ROLES.items()]
