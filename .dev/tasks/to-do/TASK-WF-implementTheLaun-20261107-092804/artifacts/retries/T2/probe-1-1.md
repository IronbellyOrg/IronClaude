2912b48a697fa9d54be994797c7af6d1262ebe85
family readme-live-probe-claim
defect form: a sentence of ob_h1/README.md that says what ../live_probe.py captures or does not capture
command: grep -nE 'live_probe' tests/hooks/fixtures/launch_level/ob_h1/README.md
before-output:
5:`log-only-probe.sh` is the hook a person registers ... The existing opt-in probe `../live_probe.py` captures job-identity selector results only; it does not capture the items below, so the two do not overlap.
coupled sites: none (README.md is the only file that describes live_probe.py; the observation test file never mentions it)
after:
5:`log-only-probe.sh` is the hook a person registers for a real observation. It appends each hook input as one line to the file named by `LAUNCH_LEVEL_PROBE_LOG`, always exits 0 and never blocks. The 
