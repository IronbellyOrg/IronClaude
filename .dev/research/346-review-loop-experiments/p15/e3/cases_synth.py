#!/usr/bin/env python3
"""cases_synth.py  30 synthetic base findings on 6 mini-spec families (plan 4.3).  data_classes = {synthetic}.

Categories (30): 4 CRITICAL canonical exceptions (code path), 6 true contradictions between two sections, 5 valid quotes with a
false consequence, 5 nits disguised as wrong outcomes, 4 omissions (never stated: Medium, blocking = no), 3 clean controls,
3 true single-text harms.  `author_intent` is the author's expectation, NEVER truth: independent labelers decide (J8).
Every quoted text is asserted to be a verbatim substring of its mini-spec at build time.
Usage: uv run --no-project python cases_synth.py     (writes offline/pool/ is NOT touched; writes offline/synth/*.json)"""
import sys

import e3lib
from p15common import datasets

SYNTH = e3lib.OFF / "synth"

SPECS = {
 "pay": ["# Payments service requirements", "",
  "## 1. Scope",
  "The payments service charges customers, issues refunds and records every money movement in the ledger. Terms: a charge is one attempt to collect money for one order; a capture is the point at which the money is taken.", "",
  "## 2. Charges",
  "R1. A charge is created in state pending and moves to captured only after the card network confirms the authorization.",
  "R2. A captured charge is never modified; a correction is made by a new refund entry.",
  "R3. The service retries a failed capture up to 3 times, with 10 minutes between attempts.",
  "R4. After the third failed attempt the charge moves to state failed and the customer is notified by email.", "",
  "## 3. Refunds",
  "R5. A refund may be issued for any captured charge within 90 days of the capture date.",
  "R6. The refund amount may not exceed the captured amount minus refunds already issued for that charge.",
  "R7. A refund request older than 30 days after capture is rejected with the error code REFUND_EXPIRED.",
  "R8. Every refund creates one ledger entry of type refund in the same transaction as the state change.", "",
  "## 4. Ledger",
  "R9. Ledger entries are append-only and carry the charge identifier, the amount in minor units and the UTC timestamp.",
  "R10. The ledger is the source of truth for balances; the daily report is derived from it.", "",
  "## 5. Reports",
  "R11. The daily report lists every captured charge and every refund of the previous UTC day.",
  "R12. The daily report is delivered to the finance mailbox by 06:00 UTC.", "",
  "## 6. Security",
  "R13. Card numbers are never written to the ledger or to logs; only the last four digits may be stored.",
  "R14. Support staff may view the full card number of a charge when a customer asks for it by phone.", "",
  "## 7. Notes",
  "Amounts are integers in minor units, for example cents. All timestamps are UTC. A requirement marked R is mandatory; this document has no optional requirements.",
  "Open items are listed by the product owner in the tracker and are not part of this document."],
 "ret": ["# Data retention policy", "",
  "## 1. Purpose",
  "This policy sets how long the platform keeps user data and how it deletes it. It applies to every service that stores data about a user.", "",
  "## 2. Categories",
  "R1. Account data (name, email address, password hash) is kept while the account is active.",
  "R2. Activity logs record sign-in time, IP address and the pages visited.",
  "R3. Activity logs are kept for 180 days and then deleted by the nightly purge job.",
  "R4. Support tickets are kept for 3 years after the ticket is closed.",
  "R5. Backups are encrypted and kept for 35 days.", "",
  "## 3. Deletion",
  "R6. When a user deletes the account, account data is removed within 30 days.",
  "R7. Deleted account data may remain in backups until the backups expire under R5.",
  "R8. A legal hold suspends deletion for the data it names until the hold is lifted.",
  "R9. The nightly purge job runs at 02:00 UTC and writes a summary line to the audit log.",
  "R10. Closed support tickets are deleted one year after closing.", "",
  "## 4. Exports",
  "R11. A user may request an export of their account data once per calendar month.",
  "R12. Activity logs are included in an export only when the user asks for them.", "",
  "## 5. Access",
  "R13. Only members of the data protection group may read activity logs older than 30 days.",
  "R14. The audit log is kept for 7 years.",
  "R15. Activity logs are kept for 90 days to limit exposure of IP addresses.", "",
  "## 6. Notes",
  "The word kept means that the data can still be read by an authorized person. The word removed means that it can no longer be read by anyone.",
  "Each category above is owned by the team named in the data inventory.",
  "Time periods in this policy are measured from the moment the data was created or the event named in the requirement occurred.",
  "Questions about this policy go to the data protection group."],
 "acc": ["# Access control requirements", "",
  "## 1. Roles",
  "R1. The system has three roles: viewer, editor and admin.",
  "R2. A viewer can read documents but cannot change them.",
  "R3. An editor can create and change documents but cannot delete them.",
  "R4. An admin can do everything an editor can do and can also delete documents and manage users.", "",
  "## 2. Sessions",
  "R5. A session expires after 30 minutes without activity.",
  "R6. After expiry the user must sign in again before any further request is accepted.",
  "R7. Admin sessions expire after 15 minutes without activity.", "",
  "## 3. Sharing",
  "R8. A document can be shared by link with people outside the organization only by an admin.",
  "R9. A shared link grants the viewer role on that single document.",
  "R10. Editors may share a document by link with anyone, to speed up collaboration.",
  "R11. Editors may delete documents that they created themselves.", "",
  "## 4. User management",
  "R12. Only an admin can create, disable or delete a user.",
  "R13. Disabling a user ends all of that user's sessions immediately.",
  "R14. The last remaining admin cannot be disabled or deleted.",
  "R15. When a user is deleted, the documents they own are deleted with them.", "",
  "## 5. Notes",
  "A document has exactly one owner, the user who created it. Teams share documents by adding people to the document, not by sharing a folder.",
  "Roles are assigned per user for the whole organization; there are no per-document roles.",
  "The role names above are fixed by this document. A user has exactly one role at a time and a new user starts as a viewer.",
  "Requests that arrive without a valid session are answered with an authentication error and nothing else. This document does not cover the content of that error.",
  "The audit trail of role changes is out of scope for this document and is described in the security overview."],
 "exp": ["# Export service requirements", "",
  "## 1. Output location",
  "R1. Exports are written to the directory named by the --out option.",
  "R2. If --out is not given, exports are written to the exports folder in the current working directory.",
  "R3. The service creates the output directory if it does not exist.",
  "R4. Existing files in the output directory are never overwritten; a numeric suffix is added to the new file name.", "",
  "## 2. File names",
  "R5. A file name has the form report-YYYYMMDD-NNN.csv, where NNN is a counter starting at 001.",
  "R6. The counter resets to 001 at midnight UTC.",
  "R7. When an export is retried, the retry reuses the file name of the failed attempt and overwrites the partial file.", "",
  "## 3. Formats",
  "R8. The default format is CSV with a header row.",
  "R9. With --format json the service writes one JSON array per file.",
  "R10. Dates in all formats use the ISO 8601 form in UTC.", "",
  "## 4. Limits",
  "R11. A single export file holds at most 100000 rows; larger results are split across files.",
  "R12. The service stops with exit code 2 if the output directory cannot be written.", "",
  "## 5. Cleanup",
  "R13. At the start of every run the service deletes every file older than 14 days from the output directory.",
  "R14. Files in the output directory that were not created by the service are never deleted.", "",
  "## 6. Notes",
  "The service is a command line tool that runs once per invocation and keeps no state between runs other than the files it writes.",
  "Row counts include the header row. Exit code 0 means every requested file was written.",
  "The service reads its data from the reporting database through a read-only account and never writes to that database.",
  "Progress is printed to standard error, one line per file written. Standard output stays empty so that scripts can pipe it."],
 "ntf": ["# Notification rules", "",
  "## 1. Channels",
  "R1. A notification is sent over exactly one channel: email, SMS or push.",
  "R2. The channel is chosen by the user preference stored in the profile.",
  "R3. If the preferred channel fails, the notification is not sent over another channel.", "",
  "## 2. Quiet hours",
  "R4. Between 22:00 and 07:00 in the user's time zone, only notifications of priority urgent are delivered.",
  "R5. Notifications of other priorities created during quiet hours are queued and delivered at 07:00.",
  "R6. Urgent notifications are delivered at any hour.", "",
  "## 3. Limits",
  "R7. A user receives at most 5 notifications per hour over SMS.",
  "R8. Notifications above the limit are dropped without being queued.",
  "R9. Security alerts are priority urgent.", "",
  "## 4. Fallback",
  "R10. If SMS delivery fails for a security alert, the service falls back to email.", "",
  "## 5. Records",
  "R11. Every notification attempt is recorded with its channel, priority and delivery result.",
  "R12. Records are kept for 30 days.",
  "R13. When the hourly SMS limit is reached for a user, security alerts are dropped like any other notification under R8.", "",
  "## 6. Notes",
  "Priorities are urgent, normal and low. A notification has exactly one priority, set by the service that creates it.",
  "The profile holds one preferred channel per user and the user's time zone.",
  "Each notification has a title, a body and a link. The body is plain text with at most 500 characters. Channels may shorten it further to fit their own limits.",
  "The service that creates a notification is called the producer. Producers do not know the channel; they hand the notification to the delivery component.",
  "The delivery component is a single deployable unit that owns the profile cache. It is restarted during the weekly maintenance window, and notifications that arrive in that window are held by the producers until it is up again."],
 "bkp": ["# Backup requirements", "",
  "## 1. Schedule",
  "R1. A full backup runs every Sunday at 01:00 UTC.",
  "R2. An incremental backup runs every other day at 01:00 UTC.",
  "R3. A backup job that is still running when the next one is due makes the next one wait until it finishes.", "",
  "## 2. Storage",
  "R4. Backups are written to the primary storage bucket.",
  "R5. A copy of every backup is replicated to the secondary region within 24 hours.",
  "R6. Backups older than 35 days are deleted from the primary bucket.",
  "R7. Backups in the secondary region are kept for 90 days.", "",
  "## 3. Verification",
  "R8. After each full backup a restore test restores it into an isolated environment.",
  "R9. A failed restore test raises an alert to the on-call engineer.", "",
  "## 4. Retention exceptions",
  "R10. The most recent full backup is never deleted.",
  "R11. Backups are deleted by the cleanup job that runs at 03:00 UTC.", "",
  "## 5. Restore",
  "R12. A restore overwrites the production database with the selected backup after one confirmation click.",
  "R13. The confirmation click is the only check before a restore starts.",
  "R14. Incremental backups run every day at 01:00 UTC.", "",
  "## 6. Notes",
  "The production database is a single primary with one standby. Backups are taken from the standby so that the primary is not slowed down.",
  "The on-call engineer is the person listed in the current rota.",
  "Backup files are named after the job type and the UTC time they started. The names are not parsed by any component.",
  "The restore procedure is run by a member of the database team. The database team keeps a written runbook that is reviewed twice a year.",
  "Storage costs are reviewed every quarter by the platform team. Any change to the schedule above is announced to the engineering mailing list one week before it takes effect."],
}

def spec_text(fam):
    return "\n".join(SPECS[fam])

def ln(fam, needle):
    hits = [i + 1 for i, l in enumerate(SPECS[fam]) if needle in l]
    assert len(hits) == 1, (fam, needle, hits)
    return hits[0]

def sec(fid, label, expert, title, grading, rec, prio="High", extra=()):
    """Render one finding section in the style of the real first reviews (heading, grading sentence, reasoning lines)."""
    head = f"**{fid}. {label}. Expert: {expert}. {title}**"
    body = [head, ""]
    if grading:
        body.append(f"- Grading sentence: {grading}")
    for e in extra:
        body.append(e)
    body.append(f"- Recommendation: {rec}")
    body.append(f"- Priority: {prio}. Quality impact: {title.lower()[:60]}")
    return "\n".join(body)

# category -> (reviewer label, expected truth)
LAB = {"crit": ("CRITICAL (blocking)", "yes"), "contr": ("MAJOR, blocking", "yes"), "false": ("MAJOR, blocking", "no"),
       "nit": ("MAJOR, blocking", "no"), "omit": ("Medium", "no"), "clean": ("Medium", "no"), "harm": ("MAJOR, blocking", "yes")}

def definitions():
    """-> list of (family, n, category, section_text) in a fixed order (30)."""
    d = []
    def add(fam, n, cat, title, grading, rec, expert="Wiegers (testability)", extra=()):
        label = LAB[cat][0]
        d.append((fam, n, cat, sec(f"F{n}", label, expert, title, grading, rec, extra=extra)))
    # ---- pay
    p = "pay"
    add(p, 1, "crit", "Card numbers are both never stored and viewable in full",
        f"an implementer who follows the stated text as written builds a ledger and logs that never hold a card number (`Card numbers are never written to the ledger or to logs; only the last four digits may be stored.`, S:{ln(p,'R13.')}) and a support screen that shows the full card number (`Support staff may view the full card number of a charge when a customer asks for it by phone.`, S:{ln(p,'R14.')}). Both cannot hold, so the full number must be stored somewhere and the security rule is broken, which is wrong because the storage rule is a security boundary.",
        "state that support staff see only the last four digits", expert="Whittaker (Contradiction Attack)")
    add(p, 2, "contr", "The refund window is 90 days in one requirement and 30 days in another",
        f"an implementer who follows the stated text as written builds a refund check that accepts a refund 60 days after capture because `A refund may be issued for any captured charge within 90 days of the capture date.` (S:{ln(p,'R5.')}), and also rejects the same request because `A refund request older than 30 days after capture is rejected with the error code REFUND_EXPIRED.` (S:{ln(p,'R7.')}). No implementation can satisfy both for a request 60 days after capture, and the acceptance test for refunds cannot be written.",
        "keep one window and delete the other")
    add(p, 3, "false", "Retries and the failed state disagree",
        f"an implementer who follows the stated text as written builds a service that marks the charge failed after the first failed capture, because `After the third failed attempt the charge moves to state failed` (S:{ln(p,'R4.')}) is read next to `The service retries a failed capture up to 3 times, with 10 minutes between attempts.` (S:{ln(p,'R3.')}), and the charge is wrong because the retries never run.",
        "say that the retries run before the failed state")
    add(p, 4, "nit", "The meaning of derived is not defined",
        f"an implementer who follows the stated text as written builds the daily report as a query over the ledger (`the daily report is derived from it`, S:{ln(p,'R10.')}), and that is wrong because derived does not say whether the report is a view or a stored copy.",
        "define derived", expert="Adzic (concrete examples)")
    add(p, 5, "omit", "No rule for a refund on a failed charge",
        f"`A refund may be issued for any captured charge within 90 days of the capture date.` (S:{ln(p,'R5.')}) says nothing about a charge that is in state failed. The document never states what happens when a refund is requested for such a charge, so an implementer must guess.",
        "add one sentence for failed charges")
    # ---- ret
    p = "ret"
    add(p, 1, "crit", "Activity logs are kept for 180 days and for 90 days",
        f"an implementer who follows the stated text as written builds a purge job that deletes activity logs after 180 days (`Activity logs are kept for 180 days and then deleted by the nightly purge job.`, S:{ln(p,'R3.')}) and also after 90 days (`Activity logs are kept for 90 days to limit exposure of IP addresses.`, S:{ln(p,'R15.')}). Logs between 90 and 180 days old must both exist and not exist, and IP addresses stay exposed beyond the stated limit, which is wrong for a retention policy.",
        "keep one period", expert="Whittaker (Contradiction Attack)")
    add(p, 2, "contr", "Support tickets are kept for 3 years and deleted after one year",
        f"an implementer who follows the stated text as written builds a ticket store that keeps a closed ticket for 3 years (`Support tickets are kept for 3 years after the ticket is closed.`, S:{ln(p,'R4.')}) and deletes the same ticket one year after closing (`Closed support tickets are deleted one year after closing.`, S:{ln(p,'R10.')}). A ticket closed 18 months ago must be present and absent, so the retention test for tickets cannot pass.",
        "keep one period")
    add(p, 3, "false", "Exports never include activity logs",
        f"an implementer who follows the stated text as written builds an export that never includes activity logs, because `Activity logs are included in an export only when the user asks for them.` (S:{ln(p,'R12.')}), and that is wrong because users cannot get their logs.",
        "state that logs are included on request")
    add(p, 4, "nit", "The summary line is not specified",
        f"an implementer who follows the stated text as written builds the purge job to write one line saying the job ran (`writes a summary line to the audit log`, S:{ln(p,'R9.')}), and that is wrong because the line may need counts of deleted rows.",
        "list the fields of the summary line", expert="Adzic (concrete examples)")
    add(p, 5, "omit", "Nobody is named who may place a legal hold",
        f"`A legal hold suspends deletion for the data it names until the hold is lifted.` (S:{ln(p,'R8.')}) does not say who may place or lift a hold. The document never states this, so an implementer must invent a role.",
        "name the role that places holds")
    # ---- acc
    p = "acc"
    add(p, 1, "crit", "Sharing outside the organization is admin only and open to editors",
        f"an implementer who follows the stated text as written builds a share action that refuses editors (`A document can be shared by link with people outside the organization only by an admin.`, S:{ln(p,'R8.')}) and allows editors to share with anyone (`Editors may share a document by link with anyone, to speed up collaboration.`, S:{ln(p,'R10.')}). An editor sharing outside the organization must be refused and allowed, so either the boundary is open or the feature is dead, which is wrong for a security boundary.",
        "make R10 inside the organization only", expert="Whittaker (Contradiction Attack)")
    add(p, 2, "contr", "Editors can and cannot delete documents",
        f"an implementer who follows the stated text as written builds a delete check that refuses editors (`An editor can create and change documents but cannot delete them.`, S:{ln(p,'R3.')}) and allows an editor to delete documents they created (`Editors may delete documents that they created themselves.`, S:{ln(p,'R11.')}). An editor deleting their own document must be refused and allowed at the same time.",
        "pick one rule")
    add(p, 3, "false", "Admin sessions are said to last 30 minutes",
        f"an implementer who follows the stated text as written builds admin sessions that last 30 minutes, because `A session expires after 30 minutes without activity.` (S:{ln(p,'R5.')}), and that is wrong because admin sessions must end after 15 minutes.",
        "no change needed")
    add(p, 4, "nit", "Sign-in is not defined",
        f"an implementer who follows the stated text as written builds a password sign-in for the re-authentication step (`the user must sign in again before any further request is accepted`, S:{ln(p,'R6.')}), and that is wrong because the sign-in method may be single sign-on.",
        "name the sign-in method", expert="Adzic (concrete examples)")
    add(p, 5, "harm", "Deleting a user deletes the documents they own",
        f"an implementer who follows the stated text as written builds a user deletion that removes every document the user owns (`When a user is deleted, the documents they own are deleted with them.`, S:{ln(p,'R15.')}), including documents shared with a team, and the team loses its data, which is wrong because the deletion destroys data other people rely on.",
        "transfer ownership instead of deleting")
    # ---- exp
    p = "exp"
    add(p, 1, "crit", "Cleanup deletes every old file and never deletes foreign files",
        f"an implementer who follows the stated text as written builds a cleanup that deletes every file older than 14 days in the output directory (`the service deletes every file older than 14 days from the output directory`, S:{ln(p,'R13.')}) and never deletes files it did not create (`Files in the output directory that were not created by the service are never deleted.`, S:{ln(p,'R14.')}). A foreign file older than 14 days must be deleted and kept, so either user data is destroyed or the rule is dead, which is wrong for a cleanup that runs on every start.",
        "limit R13 to files created by the service", expert="Whittaker (Contradiction Attack)")
    add(p, 2, "contr", "A retry overwrites a file that is never overwritten",
        f"an implementer who follows the stated text as written builds a writer that never overwrites (`Existing files in the output directory are never overwritten; a numeric suffix is added to the new file name.`, S:{ln(p,'R4.')}) and a retry that overwrites the partial file (`the retry reuses the file name of the failed attempt and overwrites the partial file`, S:{ln(p,'R7.')}). The retry must add a suffix and reuse the name, so the retry test cannot pass.",
        "say that partial files are the exception")
    add(p, 3, "nit", "ISO 8601 has several forms",
        f"an implementer who follows the stated text as written builds dates as 2026-11-10T00:00:00Z (`Dates in all formats use the ISO 8601 form in UTC.`, S:{ln(p,'R10.')}), and that is wrong because ISO 8601 also allows a basic form without dashes.",
        "name the form", expert="Adzic (concrete examples)")
    add(p, 4, "omit", "Names of split files are not given",
        f"`larger results are split across files` (S:{ln(p,'R11.')}) and the name form in S:{ln(p,'R5.')} do not say how the second file of one export is named. The document never states a rule for split file names, so an implementer must guess.",
        "give the naming rule for split files")
    add(p, 5, "clean", "The reset time of the counter may be unclear", None, "none needed",
        extra=("- Passage: `The counter resets to 001 at midnight UTC.`",))
    # ---- ntf
    p = "ntf"
    add(p, 1, "contr", "A failed channel is never retried over another channel, except for security alerts",
        f"an implementer who follows the stated text as written builds a sender that never uses a second channel (`If the preferred channel fails, the notification is not sent over another channel.`, S:{ln(p,'R3.')}) and falls back to email for a failed SMS security alert (`If SMS delivery fails for a security alert, the service falls back to email.`, S:{ln(p,'R10.')}). A failed SMS security alert must stay unsent and be sent by email, so the fallback test cannot pass.",
        "state the exception in R3")
    add(p, 2, "false", "Urgent notifications are queued until 07:00",
        f"an implementer who follows the stated text as written builds a queue that holds urgent notifications created at 23:00 until 07:00, because `Notifications of other priorities created during quiet hours are queued and delivered at 07:00.` (S:{ln(p,'R5.')}) is read next to `Urgent notifications are delivered at any hour.` (S:{ln(p,'R6.')}), and an urgent alert arrives eight hours late.",
        "none")
    add(p, 3, "nit", "Calendar days or 30 days",
        f"an implementer who follows the stated text as written builds a purge of records older than 30 times 24 hours (`Records are kept for 30 days.`, S:{ln(p,'R12.')}), and that is wrong because 30 days may mean one calendar month.",
        "say 30 times 24 hours", expert="Adzic (concrete examples)")
    add(p, 4, "harm", "Security alerts are dropped when the SMS limit is reached",
        f"an implementer who follows the stated text as written builds a limiter that drops a security alert once the hourly SMS limit is reached (`security alerts are dropped like any other notification under R8`, S:{ln(p,'R13.')}), so a user under attack loses the alert, which is wrong because it breaks a safety boundary.",
        "exempt security alerts from the limit")
    add(p, 5, "clean", "The channel rule may surprise users", None, "none needed",
        extra=("- Passage: `A notification is sent over exactly one channel: email, SMS or push.`",))
    # ---- bkp
    p = "bkp"
    add(p, 1, "contr", "Incremental backups run every other day and every day",
        f"an implementer who follows the stated text as written builds a scheduler that runs an incremental backup on Monday, skips Tuesday (`An incremental backup runs every other day at 01:00 UTC.`, S:{ln(p,'R2.')}) and runs on Tuesday as well (`Incremental backups run every day at 01:00 UTC.`, S:{ln(p,'R14.')}). Tuesday's job must run and not run, so the schedule test cannot pass.",
        "keep one schedule")
    add(p, 2, "false", "A waiting backup is skipped",
        f"an implementer who follows the stated text as written builds a scheduler that skips a due backup while the previous one runs, because `makes the next one wait until it finishes` (S:{ln(p,'R3.')}), and the Sunday full backup is lost.",
        "none")
    add(p, 3, "omit", "No definition of a passing restore test",
        f"`After each full backup a restore test restores it into an isolated environment.` (S:{ln(p,'R8.')}) does not say what makes a restore test pass. The document never states a pass condition, so an implementer must guess.",
        "state the pass condition")
    add(p, 4, "harm", "A restore overwrites production after one click",
        f"an implementer who follows the stated text as written builds a restore that replaces the production database after a single click (`A restore overwrites the production database with the selected backup after one confirmation click.`, S:{ln(p,'R12.')}), so one misclick destroys all writes made since the backup, which is wrong because it causes data loss.",
        "require a second check")
    add(p, 5, "clean", "The primary bucket is not named", None, "none needed",
        extra=("- Passage: `Backups are written to the primary storage bucket.`",))
    return d

def case_for(fam, n, cat, section):
    text = spec_text(fam)
    cid = f"syn-{fam}-{n}"
    fid = f"F{n}"
    # every quoted text must be verbatim (no fabricated quote in this set)
    import packets as pk
    for q in pk.extract_quotes(pk.drop_reasoning(section)):
        if q.startswith("S:"):
            continue
        assert q in text, (cid, q)
    return {"case_id": cid, "group": f"syn-{fam}", "family": f"syn-{fam}", "category": cat, "variant": "base", "split": "synth",
            "data_classes": ["synthetic"], "source": {"kind": "synthetic", "paths": ["cases_synth.py"], "url": None},
            "packet": {"finding_id": fid, "finding_section": section, "candidate_text": text},
            "author_intent": {"expected_blocking": LAB[cat][1], "category": cat,
                              "expected_code_outcome": "EXCEPTION" if cat == "crit" else "OK"}}

def build():
    cases = [case_for(*t) for t in definitions()]
    assert len(cases) == 30
    for fam, spec in SPECS.items():
        words = len(spec_text(fam).split())
        assert 300 <= words <= 900, (fam, words)
    return cases

def main():
    cases = build()
    SYNTH.mkdir(parents=True, exist_ok=True)
    for old in SYNTH.glob("*.json"):
        old.unlink()
    for c in cases:
        datasets.write_case(SYNTH / f"{c['case_id']}.json", c)
    from collections import Counter
    print("SYNTH", len(cases), dict(Counter(c["category"] for c in cases)), {f: len(spec_text(f).split()) for f in SPECS})
    return 0

if __name__ == "__main__":
    sys.exit(main())
