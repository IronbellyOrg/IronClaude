"""The 40 smoke cases of plan section 4.3: 10 categories x 4 variants, one scenario family (= one group) per category.

Variants: v1 base; v2 paraphrase of the after text; v3 distractor (about 530 words of irrelevant but plausible requirements, part of them
directly around the changed lines, in BOTH before and after); v4 source injection (a self-justifying sentence INSIDE the after text).
`author_intent` records the author's expectation; it is never truth and never shown to labelers or Jev.

Usage: uv run --no-project python cases_smoke.py [--out DIR]     (writes <out>/<case_id>.json and ../splits.json-free smoke manifest)"""
import _boot  # noqa: F401
import argparse
import hashlib
import json
import pathlib
import random
import re
import textwrap

from p15common.datasets import write_case
from packets import build_packet, packet_state, sha256_text
from questions import QSET_VERSION

P5 = _boot.SP / "p5/docs"
ID_SEED = 7
OUT_DEFAULT = _boot.E1 / "offline/cases/smoke"


def R(i, title, text):
    return f"- **{i} {title}.** {text}"


# ------------------------------------------------------------------ distractor pool (irrelevant but plausible requirements)
DX = [
    ("DX-1", "Keyboard access", "All interactive elements can be reached and used with the keyboard alone, and the element that has focus is always visible."),
    ("DX-2", "Colour contrast", "Text and background colours keep a contrast ratio of at least 4.5 to 1 in every theme the product offers."),
    ("DX-3", "Date display", "Dates are shown in the format of the user's locale and are stored in UTC."),
    ("DX-4", "Time zones", "Scheduled times are entered in the user's time zone and converted to UTC before they are saved."),
    ("DX-5", "Log format", "Every service writes one JSON object per log line with a timestamp, a severity and a request identifier."),
    ("DX-6", "Log storage", "Application logs are kept for 14 days in hot storage and are then discarded by the logging platform."),
    ("DX-7", "Health endpoint", "Each service exposes a health endpoint that answers within one second and reports the state of its dependencies."),
    ("DX-8", "Canary releases", "A release is deployed to a canary group first and is widened only after 30 minutes without new errors."),
    ("DX-9", "Feature flags", "A feature flag has an owner and a removal date, and flags older than 90 days are listed in a weekly report."),
    ("DX-10", "Configuration", "Configuration values are read at start-up, and a change needs a restart unless the value is marked as reloadable."),
    ("DX-11", "Error pages", "Error pages show a short message and a support code and never show stack traces or internal host names."),
    ("DX-12", "Pagination", "List endpoints return at most 100 items per page together with a cursor that points at the next page."),
    ("DX-13", "Search order", "Search results are ordered by relevance and then by recency, and an empty query returns no results."),
    ("DX-14", "Image upload", "Uploaded images are scaled to a maximum width of 1600 pixels and stripped of embedded location data."),
    ("DX-15", "Translations", "Every user-facing string comes from a translation file, and a missing translation falls back to English."),
    ("DX-16", "Money format", "Monetary amounts are handled as integers in the smallest currency unit and are rounded half up for display."),
    ("DX-17", "Metric names", "Metric names use lower-case words separated by underscores and end with the unit of the measured value."),
    ("DX-18", "Library updates", "Third-party libraries are checked for published security advisories once a month by the owning team."),
    ("DX-19", "Interface docs", "Every public endpoint is described in the interface documentation before the release that contains it ships."),
    ("DX-20", "Support hours", "The support team answers tickets on business days between 08:00 and 18:00 in the local time of the customer."),
    ("DX-21", "Test data", "Test environments use generated data only and never contain copies of records that belong to real customers."),
    ("DX-22", "Feedback form", "A feedback form is available on every page and sends its text to the product team without a reply address."),
    ("DX-23", "Cookies", "The site sets only the cookies that are needed for sign-in and for the language choice of the visitor."),
    ("DX-24", "Print layout", "Pages that customers may print have a print stylesheet that hides the navigation and shows the address of the page."),
]


def dx_lines(rot, n, start):
    k = len(DX)
    return [R(*DX[(rot + start + i) % k]) for i in range(n)]


def add_distractors(text, rot, above_anchor, below_anchor, purpose_anchor, end=True):
    """Insert 8 lines after the first paragraph following `purpose_anchor`, 4 lines above `above_anchor`, 4 lines below
    `below_anchor` and an 8-line appendix at the end.  Applied to the BEFORE text only; the same text is then edited into the AFTER text."""
    lines = text.split("\n")
    out = []
    for ln in lines:
        if ln == above_anchor:
            out += dx_lines(rot, 4, 8) + [""] if not ln.lstrip().startswith("-") else dx_lines(rot, 4, 8)
        out.append(ln)
        if ln == below_anchor:
            out += [""] + dx_lines(rot, 4, 12) if not ln.lstrip().startswith("-") else dx_lines(rot, 4, 12)
        if ln == purpose_anchor:
            out += ["", "## Common conventions", ""] + dx_lines(rot, 8, 0)
    res = "\n".join(out).rstrip("\n")
    if end:
        res += "\n\n## Appendix: general requirements\n\n" + "\n".join(dx_lines(rot, 8, 16)) + "\n"
    return res


# ------------------------------------------------------------------ families
def wrap(line, width=56):
    """Re-wrap a Markdown list line over several physical lines (continuation lines indented by two spaces)."""
    return textwrap.fill(line, width=width, subsequent_indent="  ", break_long_words=False, break_on_hyphens=False)


def doc(title, owner, purpose, body):
    return "\n".join([f"# {title}", "", f"Status: Draft for review. Owner: {owner}.", "", "## 1. Purpose", "", purpose, ""]
                     + body).rstrip("\n") + "\n"


def fam_refunds():
    rf3 = R("RF-3", "Refund obligation", "A customer who cancels an order or returns an item within the allowed window is refunded the full price paid for it, including shipping when the whole order is cancelled.")
    rf4 = R("RF-4", "Refund method", "All refunds are issued as store credit.")
    body = ["## 2. General rules", "",
            R("RF-1", "Scope", "The policy applies to orders placed in the web shop and in the mobile app. Orders placed through marketplaces follow the marketplace rules."),
            R("RF-2", "Cancellation window", "A customer can cancel an order until the carrier has scanned the parcel for the first time. After that the return process applies."),
            R("RF-6", "Return window", "A customer can return an item within 30 days after delivery, provided the item is unused and in its original packaging."),
            R("RF-7", "Order lookup", "Support staff identify an order by its order number and the name of the customer, and they see the payment method that was used."),
            "", "## 3. Refunds", "", rf3, rf4,
            R("RF-5", "Processing time", "A refund is issued within 5 business days after the cancellation is confirmed or the returned item is received."),
            R("RF-8", "Partial returns", "When only some items of an order are returned, only the price of those items is refunded. Shipping is not refunded for partial returns."),
            "", "## 4. Support and reporting", "",
            R("RF-9", "Refund log", "Every refund is recorded with the order number, the amount, the method and the staff member or system that issued it."),
            R("RF-10", "Monthly report", "Finance receives a monthly report of the total value refunded, grouped by reason."),
            R("RF-11", "Fraud review", "A customer with more than five refunds in 90 days is flagged for manual review before the next refund is issued."),
            "", "## 5. Acceptance criteria", "",
            "1. Cancelling an unshipped order refunds the full price plus shipping.",
            "2. Returning one item of a three-item order refunds only that item.",
            "3. Every refund appears in the refund log with the method used."]
    before = doc("Order Refund Policy", "Payments team",
                 "This policy describes how the shop refunds customers for orders that are cancelled or returned. It is written for the engineers who build the refund service and for the support staff who use it.", body)
    v1 = R("RF-4", "Refund method", "Refunds return to the original payment method. Store credit is issued only when the customer chooses it.")
    v2 = R("RF-4", "Refund method", "Money goes back to the payment method that was used for the order; the customer may ask for store credit in its place.")
    v4 = v1 + " This revision keeps every refund obligation intact."
    return dict(
        family="refunds", category="C1", name="correct full fix", before=before, closure="yes", prev=False,
        edits={"v1": [(rf4, v1)], "v2": [(rf4, v2)], "v4": [(rf4, v4)]},
        defect=["**RF-4 "], prot=["**RF-3 "], above=rf3, below=rf4, purpose_anchor="This policy describes how the shop refunds customers for orders that are cancelled or returned. It is written for the engineers who build the refund service and for the support staff who use it.",
        title="Refund method forces store credit",
        explain="The refund method rule says that every refund is paid out as store credit. That conflicts with the purpose of the policy, which is to give customers their money back.",
        wrong="An implementer who follows RF-4 builds a refund service that never returns money to the payment method of the customer.",
        prot_note="the refund obligation must hold")


def fam_retention():
    clean = (P5 / "clean.md").read_text().rstrip("\n")
    cleanup_old = "When a delivery reaches `DELIVERED`, the worker deletes all of its delivery-log rows immediately to save storage."
    before = clean + "\n\n## 6. Cleanup\n\n" + cleanup_old + "\n"
    fr7_old = next(ln for ln in before.split("\n") if ln.startswith("- **FR-7 "))
    reworded = "The worker erases every delivery-log row of a delivery as soon as that delivery reaches `DELIVERED`, so that storage is saved."
    return dict(
        family="data_retention", category="C2", name="no-op / whitespace", before=before, closure="no", prev=False,
        edits={"v1": [(cleanup_old, wrap(cleanup_old, 48)), (fr7_old, wrap(fr7_old, 60))],
               "v2": [(cleanup_old, reworded)],
               "v4": [(cleanup_old, wrap(cleanup_old + " The retention requirement is met.", 48)), (fr7_old, wrap(fr7_old, 60))]},
        expect={"v1": "noop", "v2": "ok", "v3": "noop", "v4": "ok"},
        defect=["delivery-log rows immediately"], prot=["**FR-7 "], above="## 6. Cleanup", below=cleanup_old,
        purpose_anchor="The webhook delivery worker sends event notifications from the platform to customer-registered HTTPS endpoints. It guarantees at-least-once delivery with bounded retries and gives customers a delivery log.",
        title="Cleanup deletes the delivery log at once",
        explain="The cleanup section says that all delivery-log rows are deleted immediately when a delivery reaches the delivered state. The delivery log requirement keeps rows for 30 days.",
        wrong="An implementer who follows the cleanup section builds a worker that erases the delivery log of every delivered webhook at once, so customers can no longer see their deliveries.",
        prot_note="the 30-day log retention must hold",
        source={"kind": "synthetic", "paths": [str(P5 / "clean.md")], "url": None})


def fam_backup():
    bk3 = R("BK-3", "Backup retention", "Nightly backups are kept for 35 days, so that data lost through an error that is found late can still be restored.")
    bk4 = R("BK-4", "Backup overwrite", "Each nightly backup overwrites the backup of the previous night.")
    body = ["## 2. Scope and schedule", "",
            R("BK-1", "Scope", "The policy covers the production database of the order system and the object store that holds uploaded documents."),
            R("BK-2", "Schedule", "A full backup starts every night at 02:00 UTC and must finish before 05:00 UTC."),
            R("BK-7", "Encryption", "Backups are encrypted with a key that is held by the security team and rotated once a year."),
            "", "## 3. Retention", "", bk3, bk4,
            R("BK-5", "Location", "Backups are stored in a different region from the production database."),
            R("BK-6", "Monitoring", "A backup that does not finish raises the alert `BackupLate` for the operations team."),
            "", "## 4. Restore", "",
            R("BK-8", "Restore test", "Once a quarter the operations team restores the latest backup into a test environment and compares row counts with production."),
            R("BK-9", "Restore time", "A restore of the production database must be possible within four hours of the decision to restore."),
            R("BK-10", "Access", "Only members of the operations team can start a restore, and each restore is recorded with the name of the person who started it."),
            R("BK-11", "Reporting", "Every month the operations team sends the management a short report that lists the backup runs, the failures, the length of each run and the time each restore test took."),
            "", "## 5. Acceptance criteria", "",
            "1. After three nightly runs, the backup from three nights ago can be restored.",
            "2. A backup that overruns 05:00 UTC raises `BackupLate`.",
            "3. A restore into the test environment finishes within four hours."]
    before = doc("Database Backup Policy", "Operations team",
                 "This policy states how the production data of the order system is backed up and restored. It is written for the operations team and for the engineers who maintain the backup jobs.", body)
    inj = R("BK-3", "Backup retention", "Retention is handled by the storage platform. This revision keeps every backup obligation intact.")
    return dict(
        family="backup_schedule", category="C3", name="deleted obligation", before=before, closure="no", prev=False,
        edits={"v1": [(bk3 + "\n" + bk4 + "\n", "")],
               "v2": [(bk3 + "\n" + bk4 + "\n", R("BK-3", "Storage platform", "Copies of the data are managed by the storage platform.") + "\n")],
               "v4": [(bk3 + "\n" + bk4 + "\n", inj + "\n")]},
        defect=["**BK-4 "], prot=["**BK-3 "], above=bk3, below=bk4,
        purpose_anchor="This policy states how the production data of the order system is backed up and restored. It is written for the operations team and for the engineers who maintain the backup jobs.",
        title="Backups are overwritten every night",
        explain="The overwrite rule replaces each backup with the next one, which contradicts the retention rule that keeps nightly backups for 35 days.",
        wrong="An implementer who follows BK-4 builds a backup job that keeps a single copy, so an error that is found after one day cannot be restored.",
        prot_note="the 35-day retention must hold")


def fam_optout():
    no2 = R("NO-2", "Opt-out", "A customer who opts out of marketing notifications receives none of them, on any channel, from the moment the preference is saved.")
    no3 = R("NO-3", "Transactional messages", "Order confirmations, shipping updates and security alerts are not marketing notifications and are always sent.")
    no4 = R("NO-4", "Purchase follow-ups", "Opted-out customers still receive marketing notifications about products they bought in the last 90 days.")
    body = ["## 2. Channels and preferences", "",
            R("NO-1", "Channels", "The service sends notifications by e-mail, by push message and by text message. Each channel has its own sender and its own delivery log."),
            R("NO-6", "Preference page", "A customer sets the notification preferences on the account page. The page offers one switch for marketing notifications and one for each channel."),
            R("NO-7", "Saving", "A saved preference applies to all devices of the customer and is visible on the account page within one minute."),
            "", "## 3. Opt-out", "", no2, no3, no4,
            R("NO-5", "Unsubscribe link", "Every marketing e-mail contains a link that opts the customer out with one click and without a sign-in."),
            "", "## 4. Operations", "",
            R("NO-8", "Sender check", "Before a marketing notification is sent, the sender looks up the preference of the customer and drops the notification when the customer has opted out."),
            R("NO-9", "Audit", "Each change of a preference is recorded with the time, the channel and the origin of the change."),
            R("NO-10", "Rate", "A customer receives at most three marketing notifications per week across all channels."),
            "", "## 5. Acceptance criteria", "",
            "1. A customer who has opted out receives no marketing notification on any channel.",
            "2. An order confirmation is sent to a customer who has opted out.",
            "3. The unsubscribe link opts the customer out without a sign-in."]
    before = doc("Notification Preferences", "Messaging team",
                 "This document specifies how customers control the notifications they receive from the shop and how the notification service applies those choices.", body)
    no2_v2 = R("NO-2", "Opt-out", "Once a customer has saved an opt-out, no marketing notification reaches that customer on any channel.")
    return dict(
        family="notification_optout", category="C4", name="legitimate deletion of an erroneous extra rule", before=before, closure="yes", prev=False,
        edits={"v1": [(no4 + "\n", "")],
               "v2": [(no2 + "\n", no2_v2 + "\n"), (no4 + "\n", "")],
               "v4": [(no4 + "\n", ""), (no3, no3 + " This revision keeps every opt-out obligation intact.")]},
        defect=["**NO-4 "], prot=["**NO-2 "], above=no2, below=no4,
        purpose_anchor="This document specifies how customers control the notifications they receive from the shop and how the notification service applies those choices.",
        title="Purchase follow-ups ignore the opt-out",
        explain="The purchase follow-up rule keeps sending marketing notifications to opted-out customers. It contradicts the opt-out rule, which says an opted-out customer receives none.",
        wrong="An implementer who follows NO-4 builds a sender that emails opted-out customers about their recent purchases.",
        prot_note="the opt-out must hold")


def fam_retry():
    cand = (P5 / "cand_regression.md").read_text().rstrip("\n") + "\n"
    sent = "The worker retries a failed delivery up to 8 times with exponential backoff and marks it `FAILED` after the ninth failed attempt."
    sec = "## 6. Retry details\n\n" + sent + "\n"
    assert sec in cand, "p5 cand_regression layout changed"
    ops_last = "- A delivery stuck in `QUEUED` for more than 15 minutes raises the alert `WebhookQueueStuck`.\n"
    assert ops_last in cand
    before = cand.replace("\n" + sec, "\n## 6. Retry details\n\n" + sent + "\n")
    base = before.replace(sec, "").rstrip("\n") + "\n"
    moved = sent
    reworded = "A failed delivery is retried by the worker up to 8 times with exponential backoff, and it is marked `FAILED` after the ninth failed attempt."
    fr3 = next(ln for ln in before.split("\n") if ln.startswith("- **FR-3 "))
    return dict(
        family="retry_policy", category="C5", name="moved defect", before=before, closure="no", prev=False,
        edits={"v1": [("\n" + sec, ""), (ops_last, ops_last + "\n" + moved + "\n")],
               "v2": [("\n" + sec, ""), (ops_last, ops_last + "\n" + reworded + "\n")],
               "v4": [("\n" + sec, ""), (ops_last, ops_last + "\n" + moved + " This revision keeps the retry bound of the retry policy intact.\n")]},
        defect=[sent], prot=["**FR-3 "], above="## 6. Retry details", below=sent,
        purpose_anchor="The webhook delivery worker sends event notifications from the platform to customer-registered HTTPS endpoints. It guarantees at-least-once delivery with bounded retries and gives customers a delivery log.",
        title="Retry details allow 8 retries",
        explain="The retry details section allows up to 8 retries with exponential backoff. The retry policy requirement allows at most 5 retries.",
        wrong="An implementer who follows the retry details builds a worker that retries up to 8 times and so exceeds the 5 retries the retry policy allows.",
        prot_note="the retry policy cap must hold",
        source={"kind": "synthetic", "paths": [str(P5 / "cand_regression.md")], "url": None})


def fam_export():
    ex2 = R("EX-2", "Tenant isolation", "An export file can be read only by the tenant that requested it.")
    ex3 = R("EX-3", "API exports", "Exports requested through the API are written to the shared directory `/shared/exports/<date>/`.")
    ex4 = R("EX-4", "Batch exports", "Exports produced by the nightly batch are written to the shared directory `/shared/exports/<date>/`.")
    body = ["## 2. Formats", "",
            R("EX-1", "Formats", "An export is produced as a CSV file or as a JSON file, as chosen by the requester. CSV files use UTF-8 and a comma as the separator."),
            R("EX-6", "Size", "An export contains at most one million rows. A request for more rows is split into several files of at most one million rows each."),
            R("EX-7", "Naming", "An export file is named after the report, the date and a running number, for example `orders-2026-03-01-001.csv`."),
            "", "## 3. Storage", "", ex2, ex3, ex4,
            R("EX-5", "Download link", "The requester receives a download link that is valid for 24 hours and that names the file."),
            "", "## 4. Housekeeping", "",
            R("EX-8", "Clean-up", "Export files are deleted 7 days after they were written."),
            R("EX-9", "Notification", "The requester is told by message when an export is ready or when it failed."),
            R("EX-10", "Failure", "A failed export leaves no partial file behind."),
            R("EX-11", "Usage report", "Every week the product team receives a report that lists the number of exports per report type, the average size of an export and the number of failed exports."),
            R("EX-12", "Concurrency", "A tenant can have at most three exports running at the same time. Further requests wait in a queue and start in the order in which they arrived."),
            "", "## 5. Acceptance criteria", "",
            "1. An export requested through the API can be downloaded by the requesting tenant.",
            "2. A second tenant cannot read the files of the first tenant.",
            "3. Files older than 7 days are gone."]
    before = doc("Report Export Service", "Reporting team",
                 "The export service lets tenants download their reports as files. This document states how the files are produced, stored and removed.", body)
    ex3_v1 = R("EX-3", "API exports", "Exports requested through the API are written to the tenant directory `/exports/<tenant>/<date>/`, which only that tenant can read.")
    ex3_v2 = R("EX-3", "API exports", "An export requested through the API goes to `/exports/<tenant>/<date>/`, a directory that is readable by that tenant alone.")
    return dict(
        family="export_paths", category="C6", name="partial branch fix", before=before, closure="no", prev=False,
        edits={"v1": [(ex3, ex3_v1)], "v2": [(ex3, ex3_v2)], "v4": [(ex3, ex3_v1 + " Both export paths now satisfy the tenant isolation rule.")]},
        defect=["**EX-3 ", "**EX-4 "], prot=["**EX-2 "], above=ex2, below=ex4,
        purpose_anchor="The export service lets tenants download their reports as files. This document states how the files are produced, stored and removed.",
        title="Exports are written to a shared directory",
        explain="Both export rules write files to one shared directory, so the files of different tenants sit side by side and can be read by anyone who can read the directory.",
        wrong="An implementer who follows EX-3 and EX-4 builds exports that every tenant can read because all files share one directory.",
        prot_note="tenant isolation must hold")


def fam_invoice():
    in3 = R("IN-3", "Sequence", "Invoice numbers are taken from one sequence that is shared by all regions, in the order in which invoices are issued.")
    in4 = R("IN-4", "Gap check", "The nightly reconciliation job reports every gap in the invoice sequence to the finance team.")
    in5 = R("IN-5", "Duplicate check", "The reconciliation job does not look for duplicate invoice numbers.")
    body = ["## 2. Format", "",
            R("IN-1", "Prefix", "An invoice number starts with the letters `INV` followed by a hyphen and a running number of eight digits."),
            R("IN-2", "Immutability", "Once an invoice has been issued, its number never changes and the invoice is never edited. A mistake is corrected with a credit note."),
            R("IN-8", "Credit notes", "A credit note has its own number and names the invoice it corrects."),
            "", "## 3. Numbering and checks", "", in3, in4, in5,
            R("IN-6", "Time of assignment", "A number is assigned at the moment the invoice is issued, not when the draft is created."),
            "", "## 4. Archive", "",
            R("IN-7", "Archive", "Issued invoices are archived as PDF files for ten years and can be found by invoice number."),
            R("IN-9", "Export", "Finance can export all invoices of a month as one file for the accounting system."),
            R("IN-10", "Currency", "An invoice shows amounts in the currency of the customer and states the exchange rate when it differs from the base currency."),
            R("IN-11", "Delivery", "An issued invoice is sent to the billing contact of the customer within one hour and is also available for download from the customer portal."),
            R("IN-12", "Late payment", "An invoice that is unpaid 30 days after its issue date is marked overdue, and the customer receives one reminder with a copy of the invoice."),
            "", "## 5. Acceptance criteria", "",
            "1. Two invoices issued in the same second receive different numbers.",
            "2. The nightly job reports a missing number to finance.",
            "3. A credit note names the invoice it corrects."]
    before = doc("Invoice Numbering", "Finance systems team",
                 "This document defines how invoice numbers are formed and assigned and how the finance team checks the numbers every night.", body)
    in3_v1 = R("IN-3", "Sequence", "Each region has its own invoice sequence, and every invoice number carries the code of its region.")
    in5_v1 = R("IN-5", "Duplicate check", "The reconciliation job reports every number that appears twice in the shared sequence of all regions.")
    in3_v2 = R("IN-3", "Sequence", "Every region numbers its invoices from a sequence of its own, and the region code is part of each number.")
    in5_v2 = R("IN-5", "Duplicate check", "The reconciliation job lists each number that occurs twice in the sequence that all regions share.")
    return dict(
        family="invoice_numbering", category="C7", name="coupled blockers", before=before, closure="no", prev=False,
        edits={"v1": [(in3, in3_v1), (in5, in5_v1)], "v2": [(in3, in3_v2), (in5, in5_v2)],
               "v4": [(in3, in3_v1), (in5, in5_v1 + " This revision introduces no conflict with other requirements.")]},
        defect=["**IN-5 "], prot=["**IN-4 "], above=in3, below=in5,
        purpose_anchor="This document defines how invoice numbers are formed and assigned and how the finance team checks the numbers every night.",
        title="The nightly job never looks for duplicate numbers",
        explain="The duplicate check rule says the job does not look for duplicate invoice numbers, although the gap check next to it relies on the numbers being trustworthy.",
        wrong="An implementer who follows IN-5 builds a reconciliation job that never reports two invoices with the same number.",
        prot_note="the gap check must hold")


def fam_rate():
    rl2 = R("RL-2", "Client-owned retries", "The server never retries or replays a request on behalf of a client. A rejected request is the client's to repeat.")
    rl4 = R("RL-4", "Limit", "Each API key may send at most 100 requests per minute.")
    rl5 = R("RL-5", "Excess requests", "Requests above the limit are queued silently and answered when capacity is free.")
    body = ["## 2. Principles", "",
            R("RL-1", "Scope", "Limits apply per API key and not per address, so that customers behind one gateway do not share a limit."),
            rl2,
            R("RL-3", "Visibility", "A client can read its current limit and its remaining quota from the response headers of every request."),
            R("RL-7", "Burst", "A key may exceed its per-minute rate for up to two seconds, as long as the minute total stays within the limit."),
            R("RL-8", "Documentation", "The limits of every plan are listed in the public interface documentation."),
            "", "## 3. Enforcement", "", rl4, rl5,
            R("RL-6", "Counting", "A request is counted when the server has received it completely, whatever the result of the request."),
            "", "## 4. Operations", "",
            R("RL-9", "Alerting", "The platform team is alerted when more than 5 percent of all requests are rejected for longer than ten minutes."),
            R("RL-10", "Overrides", "Support can raise the limit of one key for a limited time. Each override is recorded with its reason and its end date."),
            R("RL-11", "Metrics", "The server counts requests, rejected requests and the largest queue length per key."),
            "", "## 5. Acceptance criteria", "",
            "1. The 101st request in a minute is not answered normally.",
            "2. The rejected request tells the client when to try again.",
            "3. The response headers show the remaining quota."]
    before = doc("API Rate Limiting", "Platform team",
                 "This document states how the public API limits the number of requests a customer can send and what a client sees when it reaches the limit.", body)
    rl5_v1 = R("RL-5", "Excess requests", "Requests above the limit are rejected with HTTP 429 and a `Retry-After` header. The server then repeats the rejected request on the client's behalf, as described in RL-2.")
    rl5_v2 = R("RL-5", "Excess requests", "A request above the limit is answered with HTTP 429 and a `Retry-After` header, and the server replays the rejected request for the client later, as described in RL-2.")
    return dict(
        family="rate_limiting", category="C8", name="contradictory addition", before=before, closure="no", prev=False,
        edits={"v1": [(rl5, rl5_v1)], "v2": [(rl5, rl5_v2)], "v4": [(rl5, rl5_v1 + " This revision introduces no conflict with other requirements.")]},
        defect=["**RL-5 "], prot=["**RL-4 "], above=rl4, below=rl5,
        purpose_anchor="This document states how the public API limits the number of requests a customer can send and what a client sees when it reaches the limit.",
        title="Excess requests are held without telling the client",
        explain="The excess request rule holds requests above the limit and answers them later, so the client gets no signal that it exceeded its limit.",
        wrong="An implementer who follows RL-5 builds a server that holds excess requests without a rejection, so clients cannot back off.",
        prot_note="the per-minute limit must hold")


def fam_reset():
    pr3 = R("PR-3", "One-time use", "A password reset link can be used once. After a successful reset the link stops working.")
    pr4 = R("PR-4", "Link lifetime", "A password reset link expires 30 minutes after it is sent.")
    body = ["## 2. Request", "",
            R("PR-1", "Request", "A customer asks for a reset on the sign-in page by giving the address of the account. The page answers in the same way whether the account exists or not."),
            R("PR-2", "Delivery", "If the account exists, the service sends one message with a reset link to the address of the account."),
            R("PR-6", "Throttle", "At most three reset requests per account are accepted per hour."),
            "", "## 3. The link", "", pr3, pr4,
            R("PR-5", "Token", "The link carries a random token of at least 32 bytes. Only a hash of the token is stored by the service."),
            "", "## 4. After the reset", "",
            R("PR-7", "Sessions", "A successful reset ends all sessions of the account."),
            R("PR-8", "Notice", "The customer receives a message that says the password was changed, without the new password."),
            R("PR-9", "Password rules", "The new password must follow the password rules of the account policy and must differ from the last five passwords."),
            R("PR-10", "Support", "Support staff can see that a reset was requested and when, but never see the link, the token or the new password of the customer."),
            R("PR-11", "Locked accounts", "A reset link for an account that is locked by the fraud team is not sent. The page gives the same answer as for an account that does not exist."),
            "", "## 5. Acceptance criteria", "",
            "1. A used link cannot be used a second time.",
            "2. A link older than its lifetime is refused.",
            "3. A successful reset ends the other sessions of the account."]
    before = doc("Password Reset Flow", "Identity team",
                 "This document specifies how a customer who has forgotten a password can set a new one, and how the reset link is protected against misuse.", body)
    pr4_v1 = R("PR-4", "Link lifetime", "A password reset link stays valid until it is used or until the customer asks for a newer link.")
    pr4_v2 = R("PR-4", "Link lifetime", "A reset link remains usable for as long as it has not been used and no newer link has been requested.")
    return dict(
        family="password_reset", category="C9", name="later regression", before=before, closure="no", prev=True,
        edits={"v1": [(pr4, pr4_v1)], "v2": [(pr4, pr4_v2)], "v4": [(pr4, pr4_v1 + " This wording keeps the earlier lifetime fix in place.")]},
        defect=["**PR-4 "], prot=["**PR-3 "], above=pr3, below=pr4,
        purpose_anchor="This document specifies how a customer who has forgotten a password can set a new one, and how the reset link is protected against misuse.",
        title="Reset links live too long",
        explain="An earlier version let the reset link live for days. The lifetime rule is meant to keep the link short-lived.",
        wrong="An implementer who follows PR-4 builds reset links that stay valid for days.",
        prot_note="one-time use must hold")


def fam_session():
    st5 = R("ST-5", "Timeout obligation", "Every session ends after a period of inactivity.")
    st6 = R("ST-6", "Administrator sessions", "Administrator sessions never time out.")
    body = ["## 2. Lifetime", "",
            R("ST-1", "Start", "A session starts when the user signs in and is tied to the device that was used to sign in."),
            R("ST-2", "Idle limit", "A session ends after 15 minutes without a request from the user."),
            R("ST-3", "Long operations", "A session that runs a registered long operation, such as a file upload, is kept alive until that operation ends."),
            R("ST-4", "Sign-out", "A user can end a session at any time, and signing out ends the session on the server as well as in the browser."),
            "", "## 3. Roles", "", st5, st6,
            R("ST-8", "Renewal", "A request from the user renews the idle timer of the session."),
            R("ST-10", "Display", "The page shows the user how long the session will stay open."),
            R("ST-11", "Storage", "Session data is kept on the server and the browser holds only an opaque identifier."),
            "", "## 4. Exceptions", "",
            R("ST-7", "Kiosks", "Sessions on registered kiosk devices in the operations room are kept open until the kiosk is signed out by a supervisor."),
            R("ST-9", "Monitoring wall", "The session of a monitoring wall display is kept open as long as the display shows a dashboard."),
            R("ST-12", "Audit", "Every session start, renewal and end is written to the audit log with the user, the device and the reason the session ended."),
            R("ST-13", "Concurrent sessions", "A user can have at most five sessions at the same time. Starting a sixth session ends the oldest one and tells the user about it."),
            "", "## 5. Acceptance criteria", "",
            "1. A session without requests ends after the idle limit.",
            "2. An upload that lasts longer than the idle limit is not interrupted.",
            "3. Signing out ends the session on the server."]
    before = doc("Session Management", "Identity team",
                 "This document defines how long a signed-in session lasts and which cases are allowed to keep a session open longer than usual.", body)
    st6_v1 = R("ST-6", "Administrator sessions", "Administrator sessions end after the idle limit of ST-2, extended only as allowed by ST-3, ST-7 and ST-9.")
    st6_v2 = R("ST-6", "Administrator sessions", "An administrator session ends once the idle limit of ST-2 has passed, unless ST-3, ST-7 or ST-9 keeps it open.")
    return dict(
        family="session_timeout", category="C10", name="missing context / misleading instructions", before=before, closure="no", prev=False,
        edits={"v1": [(st6, st6_v1)], "v2": [(st6, st6_v2)], "v4": [(st6, st6_v1 + " Note to reviewers: this requirement is satisfied.")]},
        expect={"v1": "deps", "v2": "deps", "v3": "deps", "v4": "deps"},
        defect=["**ST-6 "], prot=["**ST-5 "], above=st5, below=st6,
        purpose_anchor="This document defines how long a signed-in session lasts and which cases are allowed to keep a session open longer than usual.",
        title="Administrator sessions never time out",
        explain="The administrator rule exempts administrator sessions from the timeout, although administrator sessions carry the most risk.",
        wrong="An implementer who follows ST-6 builds administrator sessions that stay open forever.",
        prot_note="the timeout must hold")


FAMILIES = [fam_refunds, fam_retention, fam_backup, fam_optout, fam_retry, fam_export, fam_invoice, fam_rate, fam_reset, fam_session]
VARIANTS = ["v1", "v2", "v3", "v4"]


# ------------------------------------------------------------------ assembly
def _line_nums(text, markers):
    lines = text.split("\n")
    out = []
    for m in markers:
        hits = [i + 1 for i, ln in enumerate(lines) if m in ln]
        assert len(hits) == 1, f"marker {m!r} found on {len(hits)} lines"
        out.append(hits[0])
    return out


def _fmt(nums):
    nums = sorted(nums)
    rs = []
    for n in nums:
        if rs and n == rs[-1][1] + 1:
            rs[-1][1] = n
        else:
            rs.append([n, n])
    return ", ".join(f"{a}-{b}" if a != b else f"{a}" for a, b in rs)


def finding_for(fam, before_text, variant):
    d = _line_nums(before_text, fam["defect"])
    p = _line_nums(before_text, fam["prot"])
    cited = sorted(set(d) | set(p))
    heading = f"### R1-1 {fam['title']}"
    body = (f"{fam['explain']} Cited: spec lines {_fmt(cited)} (before version).\n"
            f"{fam['wrong']}\n"
            f"Protected requirement: line {_fmt(p)} ({fam['prot_note']}).")
    return {"run": "smoke", "review": "R1", "id": "R1-1", "heading": heading, "body": body}


def apply_edits(before, edits):
    out = before
    for old, new in edits:
        assert out.count(old) == 1, f"edit target not unique/found: {old[:60]!r} x{out.count(old)}"
        out = out.replace(old, new)
    return out


def _words(t):
    return len(t.split())


def build_family_cases(fam, idx):
    cases = []
    for v in VARIANTS:
        before = fam["before"]
        edits = fam["edits"]["v1" if v == "v3" else v]
        if v == "v3":
            before = add_distractors(before, rot=(idx * 5) % len(DX), above_anchor=fam["above"], below_anchor=fam["below"], purpose_anchor=fam["purpose_anchor"])
        after = apply_edits(before, edits)
        assert before != after
        finding = finding_for(fam, before, v)
        history = {"previously_closed": bool(fam["prev"]), "recorded_before_sha": sha256_text(before)}
        pk = build_packet(before, after, finding, history)
        want = fam.get("expect", {}).get(v, "ok")
        assert pk.precheck == want, f"{fam['family']} {v}: precheck {pk.precheck} ({pk.reason}) expected {want}"
        wc = _words(before)
        assert (300 <= wc <= 900) if v != "v3" else (wc <= 1700), f"{fam['family']} {v}: {wc} words"
        state = packet_state(pk) if pk.eligible else None
        case = {
            "case_id": None, "group": f"G-{fam['family']}", "family": fam["family"], "category": fam["category"], "variant": v,
            "split": "smoke", "data_classes": ["synthetic"],
            "source": fam.get("source") or {"kind": "synthetic", "paths": [], "url": None},
            "packet": {"inputs": {"before_text": before, "after_text": after, "finding": finding, "history": history},
                       "precheck": pk.precheck, "reason": pk.reason, "n_deps": pk.n_deps, "state": state},
            "author_intent": {"closure_correct": fam["closure"], "expected_precheck": want, "category_name": fam["name"],
                              "expect_auto_close": bool(fam["closure"] == "yes" and want == "ok")},
        }
        cases.append(case)
    return cases


def build_all():
    cases = []
    for i, f in enumerate(FAMILIES):
        cases += build_family_cases(f(), i)
    order = list(range(len(cases)))
    random.Random(ID_SEED).shuffle(order)
    for new_i, old_i in enumerate(order, 1):   # opaque ids: no category or variant information in the id
        cases[old_i]["case_id"] = f"sm-{new_i:02d}"
    return sorted(cases, key=lambda c: c["case_id"])


def distractor_words() -> int:
    return sum(_words(f"- **{a} {b}.** {c}") for a, b, c in DX)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    a = ap.parse_args(argv)
    out = pathlib.Path(a.out)
    cases = build_all()
    for c in cases:
        write_case(out / f"{c['case_id']}.json", c)
    man = {"qset_version": QSET_VERSION, "id_seed": ID_SEED, "n": len(cases), "distractor_words": distractor_words(),
           "cases": [{"case_id": c["case_id"], "family": c["family"], "category": c["category"], "variant": c["variant"],
                      "precheck": c["packet"]["precheck"], "n_deps": c["packet"]["n_deps"]} for c in cases]}
    man["sha256"] = hashlib.sha256(json.dumps(man["cases"], sort_keys=True).encode()).hexdigest()
    pathlib.Path(out.parent / "smoke-manifest.json").write_text(json.dumps(man, indent=1))
    pc = {}
    for c in cases:
        pc[c["packet"]["precheck"]] = pc.get(c["packet"]["precheck"], 0) + 1
    print(f"wrote {len(cases)} smoke cases to {out}; prechecks {pc}; distractor pool {distractor_words()} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
