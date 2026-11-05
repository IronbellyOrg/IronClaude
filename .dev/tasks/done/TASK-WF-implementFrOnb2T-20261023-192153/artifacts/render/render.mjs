// Throwaway render check for the onboarding deck (Task 4). Usage: node render.mjs <url> <outdir>
import { chromium } from "playwright";
import fs from "node:fs";

const [url, out] = process.argv.slice(2);
const result = { url, runs: [], network: [], console_errors: [] };
const browser = await chromium.launch();

const TOKENS = ["--bg", "--surface", "--surface-2", "--fg", "--muted", "--line", "--accent", "--accent-soft", "--warn", "--warn-soft"];
const PAIRS = [
  ["--fg", "--bg"], ["--fg", "--surface"], ["--fg", "--surface-2"], ["--fg", "--accent-soft"], ["--fg", "--warn-soft"],
  ["--muted", "--surface"], ["--muted", "--surface-2"], ["--accent", "--surface"], ["--accent", "--accent-soft"],
  ["--warn", "--surface"], ["--warn", "--warn-soft"], ["--line", "--surface"],
];

function lum(hex) {
  const c = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map((x) => (x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4));
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m); return (x + 0.05) / (y + 0.05); };

for (const [width, scheme] of [[1280, "light"], [1280, "dark"], [375, "light"], [375, "dark"]]) {
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: scheme });
  const page = await ctx.newPage();
  const errors = [];
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("request", (r) => result.network.push(r.url()));
  await page.goto(url, { waitUntil: "networkidle" });
  const info = await page.evaluate(([tokens]) => {
    const cs = getComputedStyle(document.documentElement);
    const tok = Object.fromEntries(tokens.map((t) => [t, cs.getPropertyValue(t).trim()]));
    const p = document.querySelector(".slide p.lead") || document.querySelector(".slide p:not(.eyebrow)");
    return {
      slides: document.querySelectorAll(".slide").length,
      svgs: document.querySelectorAll(".slide svg").length,
      scrollWidth: document.documentElement.scrollWidth,
      innerWidth: window.innerWidth,
      bodyFontPx: parseFloat(getComputedStyle(p).fontSize),
      tokens: tok,
      splitCode: [...document.querySelectorAll("code:not(.long), code .nw")].filter((c) => c.getClientRects().length > 1).map((c) => c.textContent),
      bodyParaPx: parseFloat(getComputedStyle(document.querySelector(".slide li, .card p")).fontSize),
      svgRendered: [...document.querySelectorAll(".slide svg")].map((s) => Math.round(s.getBoundingClientRect().width)),
    };
  }, [TOKENS]);
  info.contrast = Object.fromEntries(PAIRS.map(([a, b]) => [`${a} on ${b}`, Number(ratio(info.tokens[a], info.tokens[b]).toFixed(2))]));
  info.minContrast = Math.min(...Object.values(info.contrast));
  // Keyboard navigation: End, then Home, then ArrowRight steps the counter.
  await page.keyboard.press("End"); await page.waitForTimeout(900);
  const atEnd = await page.textContent("#counter");
  await page.keyboard.press("Home"); await page.waitForTimeout(900);
  const atHome = await page.textContent("#counter");
  await page.keyboard.press("ArrowRight"); await page.waitForTimeout(900);
  const afterRight = await page.textContent("#counter");
  await page.click("#next"); await page.waitForTimeout(900);
  const afterNextBtn = await page.textContent("#counter");
  const steps = [];
  await page.keyboard.press("Home"); await page.waitForTimeout(900);
  for (let k = 0; k < 14; k++) { await page.keyboard.press("ArrowRight"); await page.waitForTimeout(700); steps.push(await page.textContent("#counter")); }
  info.keyboard = { atEnd, atHome, afterRight, afterNextBtn, forwardSteps: steps };
  // A manual scroll to the very top shows slide 1.
  await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(900);
  info.keyboard.afterManualTop = await page.textContent("#counter");
  await page.keyboard.press("Home"); await page.waitForTimeout(600);
  const shot = `${out}/t4-${width}-${scheme}.png`;
  await page.screenshot({ path: shot, fullPage: true });
  if (width === 375) {
    for (const id of ["s5", "s10"]) {
      await page.locator(`#${id}`).screenshot({ path: `${out}/t4-${width}-${scheme}-${id}.png` });
    }
  }
  info.screenshot = shot;
  info.width = width; info.scheme = scheme; info.console_errors = errors;
  result.console_errors.push(...errors);
  result.runs.push(info);
  if (width === 1280) {
    await page.emulateMedia({ media: "print" });
    await page.pdf({ path: `${out}/t4-print-${scheme}.pdf`, format: "A4", printBackground: true, margin: { top: "14mm", bottom: "14mm", left: "14mm", right: "14mm" } });
    const pdf = fs.readFileSync(`${out}/t4-print-${scheme}.pdf`, "latin1");
    result[`pdf_pages_${scheme}`] = (pdf.match(/\/Type\s*\/Page[^s]/g) || []).length;
    await page.screenshot({ path: `${out}/t4-print-media-${scheme}.png`, fullPage: true });
    // Where each slide starts in print layout, and whether the cheat sheet fits one A4 page.
    result[`print_${scheme}`] = await page.evaluate(() => {
      const fg = getComputedStyle(document.documentElement).getPropertyValue("--fg").trim();
      const muted = getComputedStyle(document.documentElement).getPropertyValue("--muted").trim();
      const s15 = document.getElementById("s15").getBoundingClientRect();
      return { s15_height_css_px: Math.round(s15.height), print_fg: fg, print_muted: muted };
    });
  }
  await ctx.close();
}
await browser.close();
result.network = [...new Set(result.network)];
result.file_bytes = fs.statSync(process.argv[4] || "/dev/null").size;
fs.writeFileSync(`${out}/t4-render-result.json`, JSON.stringify(result, null, 2));
console.log(JSON.stringify({ pdf_pages_light: result.pdf_pages_light, pdf_pages_dark: result.pdf_pages_dark, print_light: result.print_light, print_dark: result.print_dark, network: result.network, errors: result.console_errors,
  runs: result.runs.map((r) => ({ w: r.width, s: r.scheme, slides: r.slides, svgs: r.svgs, sw: r.scrollWidth, iw: r.innerWidth, font: r.bodyFontPx, para: r.bodyParaPx, split: r.splitCode, minContrast: r.minContrast, kb: r.keyboard })) }, null, 1));
