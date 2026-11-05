import { chromium } from "playwright";
const [url, out] = process.argv.slice(2);
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
await p.goto(url, { waitUntil: "networkidle" });
await p.evaluate(() => document.fonts.ready);
const problems = await p.evaluate(() => {
  const out = [];
  for (const svg of document.querySelectorAll(".slide svg")) {
    const vb = svg.viewBox.baseVal;
    const rects = [...svg.querySelectorAll("rect")].map((r) => r.getBBox());
    for (const t of svg.querySelectorAll("text")) {
      const bb = t.getBBox();
      if (bb.x < vb.x - 1 || bb.x + bb.width > vb.x + vb.width + 1) out.push({ svg: svg.querySelector("title").textContent, text: t.textContent, issue: "outside viewBox" });
      const cx = bb.x + 2, cy = bb.y + bb.height / 2;
      const host = rects.filter((r) => cx >= r.x && cx <= r.x + r.width && cy >= r.y && cy <= r.y + r.height)
        .sort((a, c) => a.width * a.height - c.width * c.height)[0];
      if (host && bb.x + bb.width > host.x + host.width - 3) out.push({ svg: svg.querySelector("title").textContent, text: t.textContent, issue: `overflows box by ${Math.round(bb.x + bb.width - host.x - host.width + 3)}px` });
    }
  }
  return out;
});
console.log(JSON.stringify(problems, null, 1));
for (const id of ["s2", "s4", "s5", "s6", "s7", "s10"]) await p.locator(`#${id} svg`).screenshot({ path: `${out}/t4-1280-light-${id}-svg.png` });
await b.close();
