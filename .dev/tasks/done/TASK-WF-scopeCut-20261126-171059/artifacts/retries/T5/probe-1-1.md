1aec63c6b8c340fabceb4d511a4753af001cf679
family exit-code-unhandled-oserror
defect form: a file-system or process call whose OSError is not turned into a named failure and exit EXIT_FAILED (a traceback and exit 1 instead)
command: grep -n -E "mkdir|open\(|write_text|read_text|OSError" scripts/apply_org_rulesets.py
before:
62:    return json.loads((RULES_DIR / name).read_text(encoding="utf-8"))
322:        except OSError as exc:
758:        before_file.parent.mkdir(parents=True, exist_ok=True)
759:        with open(before_file, "x", encoding="utf-8") as handle:
coupled sites: line 62 (_load: a missing rule file raises FileNotFoundError through render_branch and render_tags), line 758 to 762 (apply_repo: only FileExistsError is handled), line 322 (Runner._execute: already turns OSError into the result 127), main at line 897 to 907 (catches only RefusedCommand; the one place every path passes through).
after:
62:    return json.loads((RULES_DIR / name).read_text(encoding="utf-8"))
322:        except OSError as exc:
758:        before_file.parent.mkdir(parents=True, exist_ok=True)
759:        with open(before_file, "x", encoding="utf-8") as handle:
904:    except (RefusedCommand, OSError) as exc:
905:        # An OSError is a failed step too (an --out folder that cannot be created, a
