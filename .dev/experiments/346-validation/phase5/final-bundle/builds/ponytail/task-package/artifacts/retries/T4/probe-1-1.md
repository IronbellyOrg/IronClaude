125b69b2f6de0d874d511b40fd9272e01399c76a
## family apply-log-format (F1.1)
defect form: apply-log.md SKIP lines carry no bytes before and after
command: grep -n -e 'log.append(f"SKIP' src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py
before:
841:            log.append(f"SKIP {rid} {','.join(r['hunk_ids'])} keep")
845:            log.append(f"SKIP {tag} ({strongest.get(e['hunk'])} wins on {e['hunk']})")
coupled sites: test_shared_hunk_is_not_reverted_and_not_closed (reads apply-log lines)
after:
after: 844:                        f"SKIP {rid} {hid} revert shared with a kept or shrunk id bytes {n_b} -> {n_b}"
after: 849:                log.append(f"SKIP {rid} {hid} keep bytes {n_b} -> {n_b}")
after: 855:                f"SKIP {tag} ({strongest.get(e['hunk'])} wins on {e['hunk']}) bytes {n_b} -> {n_b}"
