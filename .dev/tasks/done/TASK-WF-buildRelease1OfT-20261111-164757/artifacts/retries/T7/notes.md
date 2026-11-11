ae0f4ffa905d631877757f8ae850d56d25f87af6
A1 r1-1 F1.1 minor src/superclaude/cli/observe/collector.py:26 ac=scope n,n,n,n INTERVAL comment says between cycle starts but the loop waits the full interval after a cycle ends, so a long cycle stretches the gap; spec wording is ambiguous
A1 r1-1 F1.2 note src/superclaude/cli/observe/collector.py:218 ac=scope n,n,n,n a PARTIAL cycle that ended in an error (overrun or a later-page failure) resets the wait to the interval; only a cycle that read no page backs off; the spec does not say which is meant
