(function () {
  // The daily report page, adapted from Clay's open-work page (page.js). Text in D is HTML that page.py
  // escaped and built from the checked writing sheet; plain fields are escaped here.
  const D = JSON.parse(document.getElementById("data").textContent);
  // ClickUp tasks tied to no GitHub issue, pull request or repository go in their own section at the bottom
  // (CLAY, 2026-11-05); everything else is the main list.
  const items = D.items.filter((it) => !it.clickupOnly);
  const cuOnly = D.items.filter((it) => it.clickupOnly);
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const $ = (id) => document.getElementById(id);
  const STATE = {
    "Waiting on you": "s-bad", "Needs work": "s-bad", "Waiting on others": "s-warn", "Blocked": "s-warn",
    "In progress": "s-open", "Ready to merge": "s-ok", "Can close": "s-ok", "Done": "s-ok", "Not started": "s-idle"
  };
  const STATE_ORDER = Object.keys(STATE);
  const PRI = ["Urgent", "High", "Medium", "Low", "Unset"];
  const stateOf = (it) => it.state || "No notes yet";
  const statePill = (s) => `<span class="pill ${STATE[s] || "s-idle"}">${esc(s)}</span>`;
  const priPill = (it) => `<span class="pri pri-${esc(it.priority)}" title="${esc(it.suggested ? "Suggested by the helper: nothing set a priority" : it.prioritySource)}">${it.suggested ? "Suggested " : ""}${PRI.includes(it.priority) && it.priority !== "Unset" ? esc(it.priority) : "No priority"}</span>`;
  const chg = (it) => `<span class="chg ${it.change === "No change" ? "chg-none" : ""}">${esc(it.change)}</span>`;
  const anchor = (it) => "i-" + it.url.replace(/[^\w]+/g, "-");
  // The priority protocol's order (templates/item-template.md): level, set or suggested, then state; page.py
  // gives each item its [level, state] rank.
  const byPri = (a, b) => a.rank[0] - b.rank[0] || a.rank[1] - b.rank[1] || (b.updated || "").localeCompare(a.updated || "");

  $("date").textContent = D.date;
  $("gen").textContent = D.generated;
  $("lede").innerHTML = `Sources read: ${D.sources}.` + (D.previous ? ` Compared with the previous report, ${esc(D.previous)}.` : " First report.");
  $("missed").innerHTML = D.missed.map((m) => `<div class="panel alert">${m}</div>`).join("");

  // Needs you: every entry laid out by templates/needs-you-template.md, every bullet shown (no click).
  $("needs-n").textContent = D.needs.length;
  $("needs").innerHTML = D.needs.length ? D.needs.map((n) => `<div class="item need">
      <div class="item-head"><span class="pill s-bad">Needs you</span>${n.carried ? '<span class="chg chg-none">Carried</span>' : '<span class="chg">New</span>'}</div>
      <h3 class="item-title">${n.title}</h3>${n.body}</div>`).join("")
    : `<div class="panel empty">No agent session is waiting on you.</div>`;

  // State tiles: each filters the list below.
  const state = { st: "", change: "", source: "", pri: "", q: "" };
  const counts = {};
  items.forEach((it) => { counts[stateOf(it)] = (counts[stateOf(it)] || 0) + 1; });
  const tiles = [...STATE_ORDER, "No notes yet"].filter((s) => counts[s]);
  $("tally").innerHTML = `<button type="button" data-v=""><span class="n">${items.length}</span><span class="l">All your work</span></button>` +
    tiles.map((s) => `<button type="button" data-v="${esc(s)}"><span class="n">${counts[s]}</span><span class="l">${statePill(s)}</span></button>`).join("");
  $("tally").addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    state.st = state.st === b.dataset.v ? "" : b.dataset.v;
    render();
  });
  $("changes").innerHTML = D.changes ? `Since the previous report: ${D.changes}` : "";

  // What changed: new and changed items, each a jump to its card.
  const jump = (it) => `<li>${priPill(it)} <a href="${esc(it.url)}">${esc(it.ref)}</a>: <a href="#${anchor(it)}" data-jump="${anchor(it)}">${esc(it.title)}</a>${it.next ? `<br><span class="why"><strong>Next:</strong> ${it.next}</span>` : ""}</li>`;
  const moved = [["New", "Showed up since the previous report.", items.filter((i) => i.change === "New")],
    ["Changed", "Something happened on these since the previous report.", items.filter((i) => i.change === "Changed")]];
  $("moved").innerHTML = moved.filter((m) => m[2].length).map(([h, why, list]) =>
    `<div class="panel"><h3>${h} <span class="pill s-open">${list.length}</span></h3><p class="why" style="margin:0 0 8px">${why}</p><ul>${list.sort(byPri).map(jump).join("")}</ul></div>`).join("") ||
    `<div class="panel empty">Nothing new or changed.</div>`;
  $("moved").addEventListener("click", (e) => {
    const a = e.target.closest("a[data-jump]");
    if (!a) return;
    e.preventDefault();
    Object.assign(state, { st: "", change: "", source: "", pri: "", q: "" });
    render();
    const el = document.getElementById(a.dataset.jump);
    if (el) { el.scrollIntoView({ behavior: "smooth", block: "start" }); }
  });

  // One item laid out by templates/item-template.md: heading, status, people, Next, then every part as a
  // bullet, all shown with no click (CLAY, 2026-11-05).
  function card(it) {
    const s0 = it.sessions[0];
    const people = it.source === "session" && s0
      ? [["Branch", s0.branch || "None"], ["Claude", s0.running ? "running" : "not running"], ["Last activity", s0.last || "Unknown"]]
      : [["Opened by", it.author || "Unknown"], ["Assigned to", it.assignees.length ? it.assignees.join(", ") : "Nobody"],
        ["Owner", it.owner || "Unknown"], ["Board", it.board || "Not on a board"]]
        .concat(it.reviewers.length ? [["Review asked of", it.reviewers.join(", ")]] : []);
    return `<div class="item" id="${anchor(it)}">
      <div class="item-head">${statePill(stateOf(it))}${priPill(it)}${chg(it)}${it.asOf ? `<span class="why">written ${esc(it.asOf)}</span>` : ""}</div>
      <h3 class="item-title"><a href="${esc(it.url)}">${esc(it.ref)}</a>: ${esc(it.title)}</h3>
      <p class="people">${people.map(([k, v]) => `<strong>${k}:</strong> ${esc(v)}`).join(" · ")}</p>
      ${it.next ? `<p class="next"><strong>Next:</strong> ${it.next}</p>` : ""}
      ${it.parts}
    </div>`;
  }

  const fPri = $("f-pri");
  fPri.innerHTML = `<option value="">Any priority</option>` + PRI.filter((p) => items.some((i) => i.priority === p)).map((p) => `<option value="${p}">${p === "Unset" ? "No priority" : p}</option>`).join("");
  fPri.onchange = () => { state.pri = fPri.value; render(); };
  $("f-change").onchange = (e) => { state.change = e.target.value; render(); };
  $("f-source").onchange = (e) => { state.source = e.target.value; render(); };
  $("q").oninput = (e) => { state.q = e.target.value.trim().toLowerCase(); render(); };

  function render() {
    fPri.value = state.pri; $("f-change").value = state.change; $("f-source").value = state.source;
    if ($("q").value.trim().toLowerCase() !== state.q) $("q").value = state.q;
    $("tally").querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.v === state.st)));
    const shown = items.filter((it) =>
      (!state.st || stateOf(it) === state.st) &&
      (!state.change || (state.change === "moved" ? ["New", "Changed"].includes(it.change) : it.change === state.change)) &&
      (!state.source || it.source === state.source) && (!state.pri || it.priority === state.pri) &&
      (!state.q || `${it.ref} ${it.title} ${it.author} ${it.assignees.join(" ")}`.toLowerCase().includes(state.q)));
    $("count").textContent = `Showing ${shown.length} of ${items.length}`;
    $("list").innerHTML = grouped(shown) || `<div class="panel empty">Nothing matches these filters.</div>`;
  }

  function grouped(list) {
    const level = (i) => (PRI.includes(i.priority) ? i.priority : "Unset");
    return PRI.map((p) => [p, list.filter((i) => level(i) === p).sort(byPri)]).filter(([, l]) => l.length).map(([p, l]) =>
      `<div class="group"><div class="group-head"><h3>${p === "Unset" ? "No priority" : p}</h3><span class="meta">${l.length} item${l.length === 1 ? "" : "s"}</span></div>${l.map(card).join("")}</div>`).join("");
  }
  $("cuonly-n").textContent = cuOnly.length;
  $("cuonly").innerHTML = grouped(cuOnly) || `<div class="panel empty">None.</div>`;

  const lines = (id, list, none) => { $(id).innerHTML = list.length ? list.map((l) => `<li>${l}</li>`).join("") : `<li class="why">${none}</li>`; };
  lines("likely", D.likely, "No other item names you.");
  lines("closed", D.closed, "Nothing closed or left your list.");
  lines("notchecked", D.notChecked, "Every source was read.");
  lines("how", D.how, "");
  render();
})();
