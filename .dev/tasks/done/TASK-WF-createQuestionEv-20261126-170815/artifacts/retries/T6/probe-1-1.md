371820fcc57abe51b6ee02a3b5c689784800de05

## family record-keyword-rule
defect form: a record states presence or absence of an addition from a keyword rule without naming the matching line
command: grep -n -E -e "covered|60|sig\(" /tmp/createQuestionEv-scratch/addition_report.py
before:
5:it counts as present in a text when at least 60 percent of its signature tokens occur there (case-insensitive).
21:def sig(text: str) -> set[str]:
25:def covered(item: str, text: str) -> float:
26:    s = sig(item)
38:    rows.append((item, covered(item, body), covered(item, final), covered(item, kept_text)))
coupled sites: record.md of quick-additions-only and quick-contradiction, and every later run record the script writes

## family notes-items-parse
defect form: the notes reader accepts only dash-prefixed lines
command: grep -n -F -e "startswith(\"- \")" .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness/run_create.py
before:
625:        elif on and ln.startswith("- ") and ln[2:].strip() not in ("", "None"):
coupled sites: summary additions and contradictions fields of every run (rederived by --reanalyse)

## family reanalyse-trusts-args
defect form: reanalyse uses command-line arguments instead of saved values
command: grep -n -E -e "args\.(description|mode|type|expect)" .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness/run_create.py
before:
664:    description = f"{args.description} [synthetic run marker: {marker}]"
665:    flags = " ".join(f"--{k} {v}" for k, v in (("mode", args.mode), ("type", args.type), ("depth", args.depth)) if v)
703:    name, flags = args.name, " ".join(f"--{k} {v}" for k, v in (("mode", args.mode), ("type", args.type), ("depth", args.depth)) if v)
729:        "description": args.description,
732:        "expected": {"questions": args.expect_questions, "issue_create": args.expect_create, "issue_comment": args.expect_comments},
747:            "questions": questions == args.expect_questions,
748:            "issue_create": gh["issue_create"] == args.expect_create,
749:            "issue_comment": None if args.expect_comments is None else gh["issue_comment"] == args.expect_comments,
789:    print(f"run {name}: questions={questions} (expected {args.expect_questions}), issue create={gh['issue_create']}, "
coupled sites: finish() reads args for flags and expected counts; reanalyse builds the arguments

after: record-keyword-rule
31:def best_window(item: str, text: str) -> tuple[float, int, str]:
46:def verdict(score: float) -> str:
102:    bs, bl, bt = best_window(item, body)
103:    fs, fl, ft = best_window(item, final)
105:        f"| {number} | {item[:60].replace('|', '/')} | yes | {verdict(bs)} (line {bl} \"{bt.replace('|', '/')}\", {bs:.0%}) | {verdict(fs)} (line 
after: notes-items-parse
629:            if ln.startswith((" ", "\t")) and out:  # an indented line continues the item above it
after: reanalyse-trusts-args
670:    description = f"{args.description} [synthetic run marker: {marker}]"
671:    flags = " ".join(f"--{k} {v}" for k, v in (("mode", args.mode), ("type", args.type), ("depth", args.depth)) if v)
709:    name, flags = args.name, " ".join(f"--{k} {v}" for k, v in (("mode", args.mode), ("type", args.type), ("depth", args.depth)) if v)
735:        "description": args.description,
738:        "expected": {"questions": args.expect_questions, "issue_create": args.expect_create, "issue_comment": args.expect_comments},
753:            "questions": questions == args.expect_questions,
754:            "issue_create": gh["issue_create"] == args.expect_create,
755:            "issue_comment": None if args.expect_comments is None else gh["issue_comment"] == args.expect_comments,
795:    print(f"run {name}: questions={questions} (expected {args.expect_questions}), issue create={gh['issue_create']}, "
816:    saved = argparse.Namespace(  # the saved run's own values, never the command line's
819:        description=old.get("description", args.description),
822:        expect_questions=expected.get("questions", args.expect_questions),
823:        expect_create=expected.get("issue_create", args.expect_create),
824:        expect_comments=expected.get("issue_comment", args.expect_comments),
847:    saved = (STOP_FILE, PENDING_FILE, RUNS)
