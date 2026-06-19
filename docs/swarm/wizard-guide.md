# Swarm Wizard — User Guide (`/sc:swarm-wizard`)

> **Who this is for:** anyone who wants to *use* the swarm tool to get several AI models to review their
> code (or docs, or a spec) — **without** having to learn lenses, transports, JobSpecs, or any of the
> jargon in the rest of `docs/swarm/`. If you've looked at the other swarm docs and thought "this is too
> technical," start here.

The wizard is a guided, plain-language front door to the `superclaude swarm` CLI. You answer a few simple
questions; it picks the right settings, proves the setup works with a safe practice run, then offers to run
the real thing, watches it, and explains the results.

---

## 1. The 30-second version

Open Claude Code in your project and type:

```text
/sc:swarm-wizard
```

The wizard will ask, in plain English:

1. **What do you want to do?** (find bugs, find edge cases, audit docs, …)
2. **What should I look at?** (a file or folder)
3. **A safe practice run first, or real AI models?**

That's usually all it needs. It then runs a **free, instant practice run** to prove everything is wired up,
and — only if you say yes — runs the real review, watches it, and gives you a plain-language summary plus a
suggested next step.

You can also pre-fill answers to skip questions:

```text
/sc:swarm-wizard --target src/auth.py
/sc:swarm-wizard --goal "find bugs in my code" --target src/auth.py
```

---

## 2. What is swarm, in one paragraph?

Normally one AI reviews your code. **Swarm** sends your code to *several* independent AI "reviewers" at the
same time, each gives its own findings, and swarm gathers them into one combined report. More independent
eyes = fewer missed problems. The wizard's whole job is to set this up correctly for you and explain what
comes back.

---

## 3. What the wizard asks (and why)

### Question 1 — "What do you want to do?"

Pick the plain-language option that matches your goal. Behind the scenes this chooses a **lens** (swarm's
word for a review style). You never have to memorize lens names — but here's the full menu so you know
what's available:

| You want to… | Lens it uses | Reviewers |
|---|---|---|
| Find bugs / review my code for correctness | `bare-review` *(the solid default)* | 3 |
| Find small, safe cleanups I could apply | `refactor-find` | 3 |
| Find edge cases / inputs that break my code | `edge-case-hunt` | 4 |
| Check whether a spec or design is complete | `spec-completeness` | 3 |
| Check whether an approach will actually work | `feasibility-probe` | 3 |
| Figure out *why* something is failing (root cause) | `troubleshoot-hypothesis` | 4 |
| Audit my documentation for gaps or staleness | `doc-completeness` | 3 |

If your goal could match two of these (e.g. "review *and* tidy up"), the wizard asks which matters more
rather than guessing.

> **Stability note:** `bare-review` is the mature, stable lens. The others are *experimental* — useful, but
> their output shape may still change. The wizard will mention this gently when it applies.

### Question 2 — "What should I look at?"

Give it a file or path. One requirement: the target needs at least a little real content — roughly **50
non-whitespace characters** (a few lines of actual code). A nearly-empty file is rejected, and the wizard
will tell you so *before* running, in plain language, and offer to pick a bigger file.

### Question 3 — "Practice run, or real models?"

- **Practice run (stub):** free, instant, no setup. It produces *placeholder* output — it proves the whole
  pipeline works, but it is **not** a real review. The wizard always does this first.
- **Real models (openai_compat):** uses your configured AI proxy. Requires credentials (see §6). The
  wizard verifies these are present before it offers to run for real.

### Optional questions

- **How many reviewers?** More = broader coverage but slower. The default per lens is fine for most people
  (you can choose 2–4).
- **Watch it live, or run in the background?** For a real run that takes a moment, you can watch a live
  dashboard, or send it to the background and be told when it's done.

---

## 4. What a run produces

Every run writes its results into an output folder (the wizard picks one like `.dev/swarm-runs/<lens>-<timestamp>/`,
and never overwrites an old run). The files that matter to you:

- **`merged.md`** — the combined findings from all reviewers. **Read this first.**
- one file per reviewer (their individual notes)
- `return-contract.yaml` — the machine summary the wizard reads to tell you the outcome

The wizard reads these for you and gives a short, friendly summary — you don't have to open them yourself
unless you want the detail.

---

## 5. How the wizard keeps you safe

These guardrails are why the wizard exists, instead of you running the raw CLI:

- **Always a practice run first.** It proves the pipeline before spending real models. If the practice run
  fails, the wizard stops and explains why — it will not push on to a real run.
- **Never a surprise real run.** A real (paid) run only happens after the practice run passes *and* you
  explicitly say "go ahead."
- **No invented credentials.** If your proxy isn't set up, the wizard tells you exactly what's missing —
  it never makes up a URL, key, or model name.
- **Plain language, always.** If the CLI emits a cryptic code (like `imm4.target_too_small`), the wizard
  translates it ("that file's too small to review") and gives you a concrete next step.
- **Idempotent output.** Re-running never clobbers a previous run's results.

---

## 6. Doing a real run (credentials)

Real model runs go through a T2 proxy. The wizard checks for three environment values and reports which (if
any) are missing — **by name only**, never showing the values:

- `T2ProxyUrl` — your proxy's base URL
- `T2ProxyKey` — your proxy key
- `T2Model01` … `T2Model09` — one model per reviewer slot (at least `T2Model01`)

These live in your `~/.aienv`. The wizard uses **only** what's there — if something's missing it points you
to `~/.aienv` rather than guessing. If they're all present, it offers the real run.

---

## 7. Watching a run

- **Live dashboard:** on a real terminal, the wizard can show a live progress dashboard (`--tui` under the
  hood) as each reviewer finishes.
- **Background:** for a fire-and-forget run, it launches in the background and tells you when it's done.
- **The wizard watching for you:** if you're not at an interactive terminal, the wizard tails the run's
  progress log itself and reports completion.

You never need to know which mode to ask for — the wizard picks the safe one for your situation.

---

## 8. Reading the result

When a run finishes, the wizard gives you something like:

> **🐝 Swarm run complete — looks healthy ✅**
> I ran a 3-reviewer bug review on `src/auth.py` with your real models.
> All 3 reviewers finished. Combined findings: `.dev/swarm-runs/bare-review-…/merged.md`.
> **Recommended next step:** `/sc:adversarial --compare …`
> Want me to run that, or try again with different settings?

Each lens suggests a natural follow-up command (for example, a bug review hands off to `/sc:adversarial`; a
docs audit hands off to `/sc:document`). The wizard surfaces it as a ready-to-run command.

---

## 9. Troubleshooting (in plain language)

| What you see | What it means | What to do |
|---|---|---|
| "that file is too small to review" | the target has almost no real content | point the wizard at a bigger / real source file |
| "the proxy isn't set up for real models" | a `T2…` value is missing | set it in `~/.aienv`, or just do a practice run |
| a real run finishes but **every reviewer failed with a 404** | the proxy is reachable and your key works, but its address doesn't expose the chat endpoint where the tool looks (a known `…/cli` vs `…/cli/v1` mismatch) | this is a proxy-address issue, not your fault — check `T2ProxyUrl` in `~/.aienv`. The practice run already proved the tool itself works |
| "mostly done ⚠️" / some reviewers failed | a few reviewers timed out or erred | the wizard can re-run just the failed ones |
| a yellow `VIRTUAL_ENV … will be ignored` warning | harmless environment noise from `uv` | ignore it — the run is fine |

---

## 10. Advanced: your own prompt

If you run `/sc:swarm-wizard --advanced`, you can supply a **custom prompt** instead of a built-in lens.
The wizard walks you through it — but note two things it will warn you about:

- A custom prompt becomes the review instructions verbatim, so write it carefully.
- A custom *recipe* (`custom-py:…`) **runs code on your machine** — only ever use one you trust.

Most people never need this; the built-in lenses cover the common cases.

---

## 11. Command + flag reference

```text
/sc:swarm-wizard [--goal <text>] [--target <path>] [--output <dir>]
                 [--real] [--detached] [--advanced] [--yes]
```

| Flag | Meaning |
|---|---|
| `--goal <text>` | Pre-fill what you want to do (skips the first question). |
| `--target <path>` | Pre-fill the file/folder to review. |
| `--output <dir>` | Where results go (default `.dev/swarm-runs/<lens>-<timestamp>/`). |
| `--real` | Signal you want real models. A practice run still happens first. |
| `--detached` | Prefer a background run over a live dashboard. |
| `--advanced` | Unlock the custom-prompt path (with safety warnings). |
| `--yes` | Power-user mode: ask only the essential questions, default the rest. |

### Related commands

The follow-up each lens hands off to: `/sc:adversarial`, `/sc:code-review`, `/sc:reflect`,
`/sc:research`, `/sc:troubleshoot`, `/sc:document`. For the raw CLI surface the wizard sits on top of, see
[`command-reference.md`](command-reference.md), [`user-guide.md`](user-guide.md), and
[`lens-catalog.md`](lens-catalog.md).

---

## 12. How the wizard stays correct

The swarm CLI evolves, and some of the older swarm docs have drifted from the code. To avoid giving you
stale advice, the wizard **re-reads the live `superclaude swarm --help`** at the start of every session and
grounds its recommendations there — so even as the CLI changes, the wizard adapts rather than repeating an
out-of-date flag or default.
