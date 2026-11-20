#!/usr/bin/env python3
"""Script checks of a populated overview (FR-14). Prints results; exit 1 if any check fails.

usage: check.py <run_folder> [--links]

Checks (completeness only; wording is never checked, CLAY 2026-11-03):
  placeholders   no {{...}} slot and no "judge each" comment is left
  template       every listed item follows templates/item-template.md: linked identifier heading, a State from
                 the list, a Next line, every section in order and written, each line starting with a capital
                 letter (CLAY, 2026-11-04); no changed item's update marker is left
  sessions       every agent session line ends in "status: <status>: <reason>" with a known status
  carry-forward  every item open in the previous report is listed or under "Closed"
  needs-you      exactly the agent sessions waiting on you (CLAY, 2026-11-05), both ways: every such session has
                 an entry led by its link, and every entry is led by such a session and links the item it works
                 on; each follows templates/needs-you-template.md (every bullet, nothing outside them)
  candidates     every item the rules could not place is judged in "Likely yours", and its line ends with its
                 priority: the set one copied, else a suggested level (CLAY, 2026-11-17: nothing without one)
  links          (with --links) every GitHub link resolves, or its line is marked "(dead link)"
Writes script-checks.md into the run folder, ending with the overview's sha256 (the delivery gate in
run.py accepts these results only for that exact text).
"""

import hashlib
import re
import sys
from pathlib import Path

from common import (
    BULLET_SLOTS,
    ENTRY_SECTIONS,
    ESCALATION_LINES,
    ITEM_SECTIONS,
    ITEM_URL,
    LEVELS,
    NEEDS_PARTS,
    QUIET_REASON,
    SESSION_STATUSES,
    SESSION_URL,
    STATES,
    SUGGESTED,
    UPDATE_MARK,
    CommandError,
    entry_blocks,
    item_parts,
    needs_link,
    read_json,
    run_cmd,
    section,
    waiting_sessions,
)

MINE = ("assigned", "owned", "opened", "inprogress")
STATUS_OK = re.compile(r"status: (" + "|".join(SESSION_STATUSES) + r"): \S")


def linked(url, text):
    return f"]({url})" in text


def capital(text):
    """A written line starts like a sentence: a capital letter or digit, a link, code, a quote, or N/A."""
    t = text.strip().removeprefix("- ").lstrip("*_")
    return (
        not t
        or t[0].isupper()
        or t[0].isdigit()
        or t[0] in "[`\"'("
        or t.startswith("N/A")
    )


def template_problems(url, block, orchestrated=False):
    """Where one item's block departs from templates/item-template.md (CLAY, 2026-11-04: every item follows the
    template every day): its linked identifier, a State from the list, the Next line, and every section, in
    order, written, each written line starting with a capital letter.

    `orchestrated` is for the entry file of an issue the orchestrator holds (its `report-entry` verb checks
    with it): a "Needs you" part that is not "N/A" is an escalation written in the item's own entry, so it
    must also carry the three lines of spec 5.6 (`Why this reaches you:`, `Low-stakes options:` and
    `If you do not answer:`)."""
    if not block:
        return ["no entry"]
    parts, out = item_parts(block), []
    if not re.match(
        r"#### \[[^\]]+\]\(" + re.escape(url) + r"\): \S", parts["heading"]
    ):
        out.append("its heading is not its linked identifier and title")
    if parts.get("state", "").rstrip(".") not in STATES:
        out.append(f"its state '{parts.get('state', '')[:30]}' is not one of the list")
    if not parts.get("next"):
        out.append("no Next line")
    level = parts.get("priority", "")
    if level.startswith(
        SUGGESTED
    ):  # the priority protocol: a suggested level and the rule that fits
        if level.removeprefix(SUGGESTED) not in LEVELS:
            out.append(
                f"its suggested priority '{level[:30]}' is not Urgent, High, Medium or Low"
            )
        if not capital(
            parts.get("Why this priority", "")
        ) or "RF_PLACEHOLDER" in parts.get("Why this priority", ""):
            out.append(
                "'Why this priority' does not give the rule for its suggested level"
            )
    elif level not in LEVELS:
        out.append(f"its priority '{level[:30]}' is neither set nor suggested")
    labels = [lbl for lbl in parts if lbl in dict(ITEM_SECTIONS)]
    if labels != [lbl for lbl, _ in ITEM_SECTIONS]:
        out.append("its sections are not the template's, in its order")
    for label, slot in ITEM_SECTIONS:
        value = parts.get(label, "")
        if not value:
            out.append(f"'{label}' is empty (write N/A if it has nothing)")
        elif slot and not all(capital(ln) for ln in value.splitlines() if ln.strip()):
            out.append(
                f"'{label}' has a line that does not start with a capital letter"
            )
        elif slot in BULLET_SLOTS and not all(
            ln.startswith("- ") for ln in value.splitlines() if ln.strip()
        ):
            out.append(
                f"'{label}' is not all bullets (one point per '- ' line, '- N/A' when empty)"
            )
    if parts.get("next") and not capital(parts["next"]):
        out.append("Next does not start with a capital letter")
    needs = parts.get("Needs you", "")
    if orchestrated and needs.strip() not in ("", "N/A"):
        lacking = [line for line in ESCALATION_LINES if line not in needs]
        if lacking:
            out.append(
                "its 'Needs you' part is an escalation but lacks "
                + ", ".join(f"'{line}'" for line in lacking)
            )
    return out


def needs_problems(block):
    """Where one "Needs you" entry departs from templates/needs-you-template.md: its linked identifier heading,
    and every bullet, in order, written, starting with a capital letter (CLAY, 2026-11-05: bullets, never a
    paragraph)."""
    parts, out = item_parts(block), []
    head = parts["heading"][4:].strip()
    if not re.match(r"\[[^\]]+\]\(" + re.escape(SESSION_URL) + r"[\w-]+\): \S", head):
        out.append("does not start with its linked agent session")
    if [lbl for lbl in parts if lbl in NEEDS_PARTS] != list(NEEDS_PARTS):
        out.append(
            f"its bullets are not the template's ({', '.join(NEEDS_PARTS)}), in that order"
        )
    for label in NEEDS_PARTS:
        value = parts.get(label, "")
        if not value:
            out.append(f"'{label}' is empty")
        elif not all(capital(ln) for ln in value.splitlines() if ln.strip()):
            out.append(
                f"'{label}' has a line that does not start with a capital letter"
            )
    stray = [
        ln
        for ln in block.splitlines()[1:]
        if ln.strip() and not ln.startswith(("- ", "  ", "*Carried"))
    ]
    if stray:
        out.append(f"has text outside its bullets: '{stray[0][:40]}'")
    return [f"'{head[:50]}' {p}" for p in out]


def main(run, links=False):
    run = Path(run)
    text = (run / "overview.md").read_text()
    cmp_ = read_json(run / "compare.json")
    cls = read_json(run / "classified.json")
    results = []

    slots = sorted(set(re.findall(r"\{\{[^}]+\}\}", text)))
    left = [f"the '{c}' comment" for c in ("judge each",) if f"<!-- {c}" in text]
    left += [
        f"an update marker on {u} (update its parts, then delete the marker)"
        for u, b in entry_blocks(text).items()
        if UPDATE_MARK in b
    ]
    left += [f"{len(slots)} slots: " + ", ".join(slots[:8])] if slots else []
    results.append(("placeholders", not left, "; ".join(left[:12]) or "none left"))

    found = entry_blocks(text)
    listed = [u for u in cls["order"] if cls["items"][u]["group"] in MINE]
    broken = [f"{u}: {p}" for u in listed for p in template_problems(u, found.get(u))]
    results.append(
        (
            "template",
            not broken,
            "; ".join(broken[:12]) or "every item follows the item template",
        )
    )

    bad = [
        ln[:100]
        for ln in text.splitlines()
        if "](orca://session/" in ln
        and ln.startswith("  - ")
        and not STATUS_OK.search(ln)
    ]
    results.append(
        (
            "sessions",
            not bad,
            "; ".join(bad[:5]) or "every agent session has a status and reason",
        )
    )

    lost = []
    if cmp_.get("previous_run"):
        old = read_json(run.parent / cmp_["previous_run"] / "snapshot.json", {})
        kept = "".join(
            section(text, h)
            for h in ENTRY_SECTIONS + ("Closed since the previous report",)
        )
        counted = {
            u for u, v in cmp_["closed"].items() if v["reason"].startswith(QUIET_REASON)
        }  # one count line
        # An item that left the daily run for the living report (exclude.py) is not lost.
        excluded = set(read_json(run / "excluded.json", []))
        lost = [
            u
            for u, s in sorted(old.items())
            if s.get("group") in MINE
            and u not in counted
            and u not in excluded
            and not linked(u, kept)
        ]
    results.append(
        (
            "carry-forward",
            not lost,
            ", ".join(lost[:10]) or "every previous item is listed or closed",
        )
    )

    # "Needs you" is exactly the agent sessions waiting on Clay (CLAY, 2026-11-05), checked both ways.
    waiting = waiting_sessions(text)
    entries = [
        b.strip("\n")
        for b in re.split(r"\n(?=### )", "\n" + section(text, "Needs you"))
        if b.startswith("### ")
    ]
    heads = {needs_link(b): b for b in entries}
    dropped = [
        f"session {s} is waiting on you but has no Needs you entry led by its link"
        for s in waiting
        if s not in heads
    ]
    for b in entries:  # the page and the DM carry these, so each stands alone
        u, head = needs_link(b), b.splitlines()[0][4:54]
        if u and u not in waiting:
            dropped.append(
                f"'{head}' is not an agent session waiting on you (its ask belongs in its item's own "
                "Needs you part)"
            )
        elif u and waiting[u] != u and not linked(waiting[u], b):
            dropped.append(
                f"'{head}' does not link the item its session works on ({waiting[u]})"
            )
        dropped += needs_problems(b)
    results.append(
        (
            "needs-you",
            not dropped,
            "; ".join(dropped[:12]) or "every session waiting on you has its entry",
        )
    )

    likely = re.sub(r"<!--.*?-->", "", section(text, "Likely yours"), flags=re.S)
    unjudged = []
    for u in cls["order"]:
        if cls["items"][u]["group"] != "candidate":
            continue
        line = re.search(
            rf"\]\({re.escape(u)}\)[^\n]*: (?:likely yours|not yours), because[^\n]*",
            likely,
        )
        if not line:
            unjudged.append(u)
            continue
        level = cls["items"][u][
            "priority"
        ]  # a set priority is copied as set; none set gets a suggested level
        want = (
            rf"Priority: {level} \(set\)\.?$"
            if level != "Unset"
            else rf"Priority: ({'|'.join(LEVELS)}) \(suggested\)\.?$"
        )
        if not re.search(want, line.group(0).strip()):
            unjudged.append(
                f"{u} (its line must end with "
                + (
                    f"'Priority: {level} (set)'"
                    if level != "Unset"
                    else "'Priority: <level> (suggested)'"
                )
                + ")"
            )
    results.append(
        (
            "candidates",
            not unjudged,
            ", ".join(unjudged) or "every candidate is judged and has a priority",
        )
    )

    if links:
        dead = []
        for line in text.splitlines():
            for url in re.findall(r"\]\((" + ITEM_URL + r")\)", line):
                if not url.startswith("https://github.com/") or "(dead link)" in line:
                    continue
                try:
                    run_cmd(
                        [
                            "gh",
                            "pr" if "/pull/" in url else "issue",
                            "view",
                            url,
                            "--json",
                            "number",
                        ],
                        timeout=30,
                    )
                except CommandError:
                    dead.append(url)
        results.append(
            (
                "links",
                not dead,
                ", ".join(sorted(set(dead))) or "every link resolves or is marked dead",
            )
        )

    lines = ["| Check | Result | Detail |", "|---|---|---|"]
    lines += [f"| {n} | {'PASS' if ok else 'FAIL'} | {d} |" for n, ok, d in results]
    lines += ["", f"overview sha256: {hashlib.sha256(text.encode()).hexdigest()}"]
    (run / "script-checks.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(0 if all(ok for _, ok, _ in results) else 1)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0].startswith("-"):
        sys.exit(__doc__)
    main(a[0], links="--links" in a)
