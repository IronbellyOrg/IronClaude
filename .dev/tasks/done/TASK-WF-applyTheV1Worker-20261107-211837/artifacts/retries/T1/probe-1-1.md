651fb0e3be5e92da95891c886044a8dde836a78b
family=wording-fidelity
defect: the C-1 text in WC-10 is not word-for-word the design text at merged-requirements.md:577 (the clause "it never stops, retries or releases a worker because a heartbeat is late" was dropped).
command: grep -n -F -e "because a heartbeat is late" -- src/superclaude/core/WORKER-CONTRACT.md tests/skills/test_worker_contract.py .dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/merged-requirements.md
before:
.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/merged-requirements.md:577
coupled: src/superclaude/core/WORKER-CONTRACT.md:46 (WC-10), tests/skills/test_worker_contract.py pin wc10-absence-not-death, merged-requirements.md:577 (design source)
after:
src/superclaude/core/WORKER-CONTRACT.md:46
tests/skills/test_worker_contract.py:233
.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/merged-requirements.md:577
