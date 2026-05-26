---
persona: security
model: sonnet
stance: "every mitigation is a security event — audit the recovery, not just the breakage"
---

# Proposal 2 — Security Lens

## Core Stance

The incident report is framed as a deployment failure. From a security perspective, it's also a **recovery integrity incident**: a human used a shared admin credential to execute an unlogged `ALTER TABLE` at 3am, recovering an environment under time pressure. Even in staging, this is the rehearsal for what happens in production — and the gaps it exposes are real attack surface. My priority push: **audit the mitigation as carefully as the bug, treat the on-caller's emergency as a hostile-environment scenario, and quantify the exposure window before declaring "no impact."**

## Blast Radius Across Four Planes

The seed brief says "no customer impact." That's a *user-visible* claim, not a *security* claim. Map the blast radius across four planes:

1. **Data plane** — what data was readable / writable during the broken window? Even on staging, staging often contains synthetic-PII or copied prod fixtures. Was the broken `orders` schema in a state where reads returned partial rows, leaking data through error messages? Were error traces shipped to a third-party (Sentry, Datadog) that captured row contents in the exception payload?

2. **Credential plane** — the manual recovery used a *shared* admin DB credential. Who has it? When was it last rotated? Is the credential keystroke-loggable in the engineer's shell history (`~/.psql_history`)? Is it captured in any synced dotfiles repo? Does it have production parity (i.e., does the same human now possess a credential that works against prod)?

3. **Network plane** — during the 54-minute window, what services upstream of the broken `api` retried into it? Did the retry storm trigger any rate-limit bypasses or fallback paths that have lower security posture (e.g., a "degraded mode" that skips auth checks)? Review middleware logs for auth-skip code paths fired during the window.

4. **Identity plane** — the on-caller assumed elevated privilege (admin DB write) outside the normal change-management flow. Was there break-glass logging? Was a second engineer notified? Is there a record of *who* did *what* that would survive a hostile insider claim of "I didn't do that"?

## Exposure Window Quantification

For each plane, compute: **exposure_duration = (time_first_observable - time_mitigation_complete)** and **exposure_severity = f(data_classification, credential_blast, identity_attribution_gap)**. Even if all numbers come back at "low," the *act of quantifying* is the discipline that catches the case where we'd otherwise have hand-waved "staging only, no impact."

## Audit Trail Completeness

This is my **non-negotiable finding**: the manual `ALTER TABLE` left no audit trail beyond shell history and Slack timestamps. Specific gaps to close:

- **Mitigation actions must flow through a logged, attributable channel.** Options: a break-glass CLI wrapper that logs to SIEM before exec; a Slack-bot-mediated SQL runner that captures the command, author, justification, and timestamps; a session-recording tool (e.g., Teleport) for any admin shell.
- **Shared admin credentials must be eliminated or vaulted with checkout/return.** If shared creds remain, every checkout writes to audit, and every use produces a per-session credential that's attributable.
- **Schema mutations in staging must follow the same change-management path as prod.** If we're willing to let an engineer hand-write `ALTER TABLE` in staging at 3am, we're rehearsing the failure mode for prod.
- **Reconstruction test**: 30 days after the incident, can you produce a complete audit of who-did-what during the window from authoritative logs alone (not Slack, not human memory)? If no → finding is unaddressed.

## Credential Review Under Stressed Mitigation

When humans are tired and paged at 3am, they take shortcuts. They paste credentials into Slack channels "just for a second." They share screens with creds visible. They run commands they'd never run during business hours. The post-mortem should explicitly review:

- Did any credential leave a secure store during the mitigation? (Slack search for `postgresql://`, `password=`, env var names.)
- Did any credential get pasted into a logging system, ticketing system, or browser history that wasn't designed to hold secrets?
- Are there any credentials that the on-caller *now* knows that they didn't know before the incident? (If yes, treat as a rotation event.)

## Supply Chain & Least Privilege

Adjacent findings worth surfacing:

- **Supply chain**: the new release that broke staging — was its dependency tree reviewed? A migration bug is often a symptom of a tooling regression (e.g., a migration framework update silently changed the default nullability behavior). Diff the lockfile from last-good to this release.
- **Least privilege for deploy automation**: does the cron-driven deploy pipeline have the *minimum* DB privileges needed to run migrations, or does it run as a superuser? If superuser, this incident is a near-miss for "deploy pipeline runs malicious migration via compromised dependency."

## What I'd Disagree With

- I'd push back on framing the post-mortem as purely a "release engineering" story. A mitigation that requires shared credentials and unlogged shell access is a security finding, full stop.
- I'd push back on rushing to "automate the rollback" without first answering: *does the automated rollback path have audit logging?* An automated rollback that quietly mutates schema is the same risk in a more dangerous package.
- I'd be cautious about "MTTR speed at all costs" — there's a real tradeoff between recovery speed and audit completeness. A 60-second automated revert with no logs is worse than a 5-minute revert with full attribution, in the long run.

## What's Out of Scope For Me

- The root-cause investigation discipline → analyzer lens.
- The on-call ergonomics / burnout pattern → devops lens.
- The deploy-time / canary policy debate → devops lens (though I'd note: canaries also reduce blast radius, which is a security win).
