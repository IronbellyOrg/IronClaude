2bb3ed28741687916e331146e0749b144c871395

## family selftest-clobbers-stop-state
defect form: the self-test reads, writes or deletes the matrix's own stop and pending files
command: grep -n -E -e "STOP_FILE|PENDING_FILE" .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness/run_create.py
before:
43:STOP_FILE = SCRATCH / "STOP"
44:PENDING_FILE = SCRATCH / "PENDING-REVIEW"
121:    if STOP_FILE.exists():
122:        return "STOP file: " + STOP_FILE.read_text(encoding="utf-8").strip()[:300]
123:    if PENDING_FILE.exists():
124:        return "PENDING-REVIEW file (unattributed fork activity is held for the orchestrator): " + PENDING_FILE.read_text(
132:    STOP_FILE.write_text(json.dumps({"reason": reason, "run": run_name, "at": utc()}), encoding="utf-8")
422:        if STOP_FILE.exists():
740:        PENDING_FILE.write_text(json.dumps({"run": name, "unattributed": activity["unattributed"]}), encoding="utf-8")
864:    STOP_FILE.unlink()
875:    PENDING_FILE.write_text("{}", encoding="utf-8")
877:    PENDING_FILE.unlink()
914:        if PENDING_FILE.exists():
915:            (SCRATCH / "pending-cleared.log").open("a").write(f"{utc()} {args.note}\n{PENDING_FILE.read_text()}\n")
916:            PENDING_FILE.unlink()
coupled sites: do_run's first lines that call check_stop, the check-stop and clear-pending subcommands (they must keep using the real files), and the self-test lines that assert the stop and pending behaviour

after: selftest-clobbers-stop-state
43:STOP_FILE = SCRATCH / "STOP"
44:PENDING_FILE = SCRATCH / "PENDING-REVIEW"
121:    if STOP_FILE.exists():
122:        return "STOP file: " + STOP_FILE.read_text(encoding="utf-8").strip()[:300]
123:    if PENDING_FILE.exists():
124:        return "PENDING-REVIEW file (unattributed fork activity is held for the orchestrator): " + PENDING_FILE.read_text(
132:    STOP_FILE.write_text(json.dumps({"reason": reason, "run": run_name, "at": utc()}), encoding="utf-8")
422:        if STOP_FILE.exists():
740:        PENDING_FILE.write_text(json.dumps({"run": name, "unattributed": activity["unattributed"]}), encoding="utf-8")
758:    global STOP_FILE, PENDING_FILE, RUNS
759:    saved = (STOP_FILE, PENDING_FILE, RUNS)
760:    real = {p: (p.read_bytes() if p.exists() else None) for p in (STOP_FILE, PENDING_FILE)}
762:    STOP_FILE, PENDING_FILE, RUNS = sandbox / "STOP", sandbox / "PENDING-REVIEW", sandbox / "runs"
766:        STOP_FILE, PENDING_FILE, RUNS = saved
882:    STOP_FILE.unlink()
893:    PENDING_FILE.write_text("{}", encoding="utf-8")
895:    PENDING_FILE.unlink()
931:        if PENDING_FILE.exists():
932:            (SCRATCH / "pending-cleared.log").open("a").write(f"{utc()} {args.note}\n{PENDING_FILE.read_text()}\n")
933:            PENDING_FILE.unlink()
