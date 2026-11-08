10d7c8f8dac0d54b499bdfabb570e335c2c3eb2f
family raw-id-cap
defect form: a fixed iteration cap on the failure-path scan for session_id values
command: grep -nE '\{1\.\.[0-9]+\}; do' src/superclaude/hooks/scripts/launch-level-guard.sh
before-output:
222:        for _ in {1..64}; do
coupled sites: the shortcut comment above the loop (removed); the header comment of the failure branch (reworded); no other loop in the script has a cap
after:
(no match)
