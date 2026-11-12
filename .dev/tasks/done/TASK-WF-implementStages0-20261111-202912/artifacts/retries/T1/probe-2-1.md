d784e95e408da85b9ccea0aa739ddd3c2ec75391
## family v2-unhashable-field-crash
defect form: a membership test against a dict or set on an untrusted JSON value (no isinstance check first) raises TypeError for a list or dict value.
command: grep -nE ' (not )?in (REFLECT_CATEGORIES|CATEGORIES|SEVERITIES|LENSES|DEVIATION_CLASSES|CHANNELS|COMPLETION_STATES)\b' src/superclaude/cli/review/findings_v2.py
before:
74:    if obj.get("severity") not in SEVERITIES:
80:    if obj.get("category") not in CATEGORIES:
114:    if lens is not None and lens not in LENSES:
117:    if dclass is not None and dclass not in DEVIATION_CLASSES:
123:        if rcat not in REFLECT_CATEGORIES:
125:        if obj["category"] not in REFLECT_CATEGORIES[rcat]:
142:    if obj.get("channel") is not None and obj["channel"] not in CHANNELS:
coupled sites: the test_optional_fields_validated_and_channel_default test and the check_finding docstring.

after:
74:    if obj.get("severity") not in SEVERITIES:
80:    if obj.get("category") not in CATEGORIES:
114:    if lens is not None and lens not in LENSES:
117:    if dclass is not None and dclass not in DEVIATION_CLASSES:
123:        if not isinstance(rcat, str) or rcat not in REFLECT_CATEGORIES:
125:        if obj["category"] not in REFLECT_CATEGORIES[rcat]:
142:    if obj.get("channel") is not None and obj["channel"] not in CHANNELS:
