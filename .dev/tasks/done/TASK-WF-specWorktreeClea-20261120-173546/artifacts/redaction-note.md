# Redaction note

An early attempt of Tasks 9 and 10 spelled a placeholder credential shape in a test (an AWS style
sample id). The final tests build every token shape from two pieces at run time and hold no such
literal. The placeholder still sat inside the saved review prompts and one probe file of those two
tasks (the copy of that early diff), so it was replaced there by `AKIA<REDACTED>` before the package was
committed (rule NFR12: no credential shaped literal in any file). It was never a real credential.
No other change was made to those files.
