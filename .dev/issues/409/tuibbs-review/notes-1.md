# TUIBBS review notes 1: plugin/module surface (questions A and F)

Source: read-only clone /tmp/tuibbs-review, HEAD a6d7e7f (2026-10-20). Paths are relative to the repo root.

## A1. Plugin tiers: implemented vs stub

Four tiers, named `tier1`..`tier4` internally (`internal/plugin/dispatch.go:92-97`) and `compiled_in`/`grpc_subprocess`/`lua`/`wasi` in manifests (`internal/plugin/manifest.go:101-106`).

| Tier | Where | Status | Tests (file: what they cover) |
|---|---|---|---|
| tier1 `compiled_in` | `internal/plugin/tier1.go` (282 lines); sample `internal/plugin/builtin/echo/echo.go` | Implemented. In-process Go; modules self-register at `init` via `Register` (`tier1.go:222`), admitted by `LoadBuiltins(host)` (`tier1.go:267`). | `tier1_test.go` (13 tests: malformed call, tier/name misroute, clean return, module-level failure, dispatch error, registry) |
| tier2 `grpc_subprocess` | `internal/plugin/grpcsub/` (`grpcsub.go` 329, `dispatcher.go` 345, `wire.go` 367); samples `builtin/echogrpc/main.go`, `builtin/statefulgrpc/main.go` | Implemented. go-plugin v1.8.0, gRPC only (`grpcsub/dispatcher.go:137`), AutoMTLS on (`dispatcher.go:138`). | `grpcsub/grpcsub_test.go` (9 tests: WireRoundTrip, DispatchRoundTrip, DispatchViaHost, SubprocessCrashRecovery, CloseThenDispatch, EnvelopeValidation, AutoMTLSNegotiated, HandshakeCookieEnforced; it builds the sample plugin with `go build` at `grpcsub_test.go:75`) |
| tier3 `lua` | `internal/plugin/tier3/` (`tier3.go` 494, `allow.go` 202); sample `builtin/echolua/` | Implemented. gopher-lua, allow-list of base/string/table/math only, per-call timeout, memory cap (`tier3/tier3.go:25-30`). `internal/plugin/lua/` holds only a README marked "Superseded placeholder" (`internal/plugin/lua/README.md:3`). | `tier3/tier3_test.go` (13: sample runs, allowed libs, denied capability audited, runaway script killed at timeout), `tier3/allow_test.go` (2: dangerous functions denied, memory cap), `tier3/allow_internal_test.go` (3: allow-list frozen) |
| tier4 `wasi` | `internal/plugin/wasi/` (`wasi.go` 402, `activate.go`, `activate_seam_only.go`) | Stub by design: loads and signature-checks wasm, but `Dispatch` "always refuses" (`internal/plugin/wasi/README.md:16-18`). | `wasi/wasi_test.go` (10: signature verify, malformed wasm fails closed), `wasi/seam_only_test.go` (1: seam-only build still refuses) |

Shared host tests: `dispatch_test.go` (12: contract shape locked), `host_test.go` (18: load/start/stop, invoke paths, crash), `lifecycle_test.go` (9: state machine), `manifest_test.go` (9: parse, tier mapping, ACS parsed at load, whitelist), `acs_gate_test.go` (5), `metrics_test.go` (5), `metrics_m4_test.go` (3). I counted `func Test` lines; I did not run them.

README-only directories (confirmed by `ls`):
- `internal/module/` contains only `README.md` (12 lines): "a forward-looking contract package, not an implemented registry (this directory ships only this README; it contains no `.go` files)" (`internal/module/README.md:4-5`).
- `internal/doors/` contains only `README.md` (5 lines): "PTY door supervisor — S8 (v1.x heavy)" (`internal/doors/README.md:3`).
- `internal/plugin/lua/` contains only `README.md` (superseded by `tier3/`).

Important wiring gap: the plugin host is NOT wired into the running server. Outside tests, nothing calls `plugin.NewHost`, `LoadManifest`, `LoadBuiltins` or `grpcsub.Open` (grep across the repo's non-test `.go` files matches only the definitions, e.g. `internal/plugin/manifest.go:203`, `internal/plugin/tier1.go:267`). No code walks a `modules/` directory. The only production tier1 module is `internal/ailink` (it calls `plugin.Register`, `internal/ailink/ailink.go:101`), but `internal/serve/` reaches ailink directly (`internal/serve/spawn_handler_unix.go:91`), not through `Host.Invoke`. A crashed tier-2 plugin is not respawned in v1 (`internal/plugin/grpcsub/dispatcher.go:251`).

## A2. Dispatch contract, manifest, lifecycle, ACS gating

Dispatch contract (real names confirmed):
- `ModuleDispatcher` interface with one method `Dispatch(ctx, ModuleCall) (ModuleResult, error)` (`internal/plugin/dispatch.go:235-237`).
- `ModuleCall` fields: `Tier`, `Name`, `Principal` (an `acs.Principal`), `Args []byte`, `ContentType string` (`dispatch.go:115-152`). `Validate` rejects an unknown tier or empty name (`dispatch.go:165-178`).
- `ModuleResult` fields: `Payload []byte`, `ContentType string`, `Code` (registered error code; empty means success) (`dispatch.go:187-204`).
- Payloads are opaque bytes; the encoding is agreed out of band via `ContentType`, e.g. "application/json" (`dispatch.go:146-151`). Two error surfaces: the returned `error` means the boundary broke; `ModuleResult.Code` means the module ran and said no (`dispatch.go:40-51`).
- Frozen for v1 by ADR-X5 and the M5-D22 SDK freeze; only additive changes allowed (`dispatch.go:53-62`).
- One request, one response. The contract has no streaming, no terminal handle, no callback channel.

Manifest: TOML file `modules/<name>/module.toml` (`internal/plugin/manifest.go:14`). Schema (`manifest.go:23-36`): `[module]` name, tier, entry (binary path or compiled-in symbol), version (semver), optional manifest_version (=1); `[acs] required = "<expr>"`; `[[mcp_tools]]` name, schema, acs. Strict decode rejects unknown keys; the ACS expression is parsed at load, not evaluated (`manifest.go:49-56`). No fields for arguments, environment, working directory, or UI/screen hooks.

Lifecycle: five states, Discovered → Loaded → Started → Stopped, with Fail from any active state into Failed (`internal/plugin/README.md:59-65`; code in `internal/plugin/lifecycle.go`, transition table checked by `canTransition` at `lifecycle.go:101`). Host API: `Load`, `Start`, `Stop`, `StateOf`, `Invoke` (`internal/plugin/host.go:226,275,296,319,357`). Only a Started plugin is invokable (`host.go:375-379`). Every transition is audited as `plugin.lifecycle.transition` (`internal/plugin/README.md:70-72`).

Crash handling:
- In-process (tier1/tier3): dispatch runs inside `recover.ModuleCall`; a panic moves the plugin to Failed and returns a registered error (`host.go:417-444`).
- Tier2: a child crash surfaces as a gRPC transport error; the dispatcher audits `plugin.crash` and returns `SessionPluginCrashed` (`internal/plugin/grpcsub/grpcsub.go:64-78`). No respawn (`grpcsub/dispatcher.go:250-251`). A returned error (not a panic) only bumps the error counter and does not move the plugin to Failed (`host.go:446-449`), so after a tier-2 crash the host state likely stays Started while each call fails. Inferred from code, not tested by me.

ACS in plain words: ACS (Access Control System) is TUIBBS's small rule language for "who may do this". A rule is an expression over facts about the caller, for example `GM[staff] & LV>5` = "member of group staff and level above 5" (`internal/plugin/manifest.go:31`). Atoms: `GM[group]`, `LV>N`/`LV<N`/`LV=N`, `AF[N]`, `AI[provider]`, `MOD[name]`, `AGE>N`, plus a rate-limit extension `RL:n/window` (`internal/acs/atoms.go:13-27`). The caller is an `acs.Principal`: session id, user id, role (sysop/op/validated/regular/anon), groups, anonymous flag (`proto/v1/plugin.proto:120-141`; Go type at `pkg/tuibbssdk/acs/acs.go:71`).

Where it is evaluated: at manifest load the expression is only parsed (`manifest.go:51-56`). On every `Host.Invoke`, after the envelope, registry, lifecycle and tier checks and before the plugin runs, `acsGate` calls `sdkacs.EvaluateContext(ctx, principal, expr)` (`internal/plugin/acs_gate.go:76-89`, called from `host.go:398`). It admits only on a clean `(true, nil)`; anything else denies, is audited `plugin.acs_denied`, and returns `RouteACSDenied` (`acs_gate.go:17-31`). An empty expression means a public plugin, no evaluation (`acs_gate.go:77-78`). The engine lives in `internal/acs/engine` with a generation-counter cache (`internal/acs/README.md:3-5`). The plugin never evaluates ACS; the host does.

## A3. pkg/tuibbssdk and proto/

`pkg/tuibbssdk`: files `README.md`, `doc.go`, `apidiff.baseline`, and subpackage `acs/` (`acs.go`, `acs_test.go`, `apidiff.baseline`). The root package "carries no symbols of its own"; the only usable surface today is `acs`: `Evaluate`, `Principal`, five role constants, the `Evaluator` bind seam (`pkg/tuibbssdk/doc.go:3-9`). Frozen by ADR-X6 with an apidiff gate (`doc.go:11-20`). It must not import `internal/` (`doc.go:22-28`).
- Consequence: `ModuleCall`, `ModuleDispatcher`, `Tier1Module` and `grpcsub.Serve` all live under `internal/plugin`, which Go forbids importing from outside the module. A third-party Go author cannot use `grpcsub.Serve` today; they would need `proto/v1/pluginpb` plus go-plugin directly. The line "Modules implement the `pkg/tuibbssdk` interfaces" (`internal/module/README.md:9`) is aspirational: no module interfaces exist there yet.

`proto/`: one schema, `proto/v1/plugin.proto`, package `tuibbs.plugin.v1` (`plugin.proto:52`).
- Service: `ModuleService` with one unary RPC `Dispatch(ModuleCall) returns (ModuleResult)` (`plugin.proto:61-68`).
- Messages: `ModuleCall` (tier=1, name=2, content_type=3, args=4, principal=5) (`plugin.proto:73-95`); `ModuleResult` (content_type=1, payload=2, code=3) (`plugin.proto:101-114`); `Principal` (`plugin.proto:120-141`); `Capability` (MCP tool whitelist entry, not on the wire today, `plugin.proto:143-162`); `ErrorEnvelope` (`plugin.proto:171-197`).
- Frozen, additive-only, checked by `buf breaking` against `proto/v1/plugin.baseline.binpb` (`plugin.proto:34-48`).

`buf.gen.yaml` targets: only `protoc-gen-go` and `protoc-gen-go-grpc` (`buf.gen.yaml:16-24`). Go is the only generated language. Output is committed at `proto/v1/pluginpb/plugin.pb.go` and `plugin_grpc.pb.go` (`proto/README.md:5-7`).
- The generated `pluginpb` package is not used by the running code: the only `.go` file outside `proto/v1/pluginpb/` that mentions it is `tools/analyzers/rawescape/analyzer.go`. The live tier-2 path still uses a hand-written descriptor and codec (`internal/plugin/grpcsub/grpcsub.go:248-264`). The planned swap to generated stubs (`internal/plugin/grpcsub/README.md:30-33`) has not happened at this commit.

## A4. Could a Python program be a gRPC plugin?

Short answer: in principle yes, because the wire is ordinary protobuf over gRPC, but nothing in the repo supports a non-Go plugin, and the host has no production path that would launch one (see A1 wiring gap).

What the host expects (all in `internal/plugin/grpcsub/`):
1. Launch: the host runs `cfg.Cmd` (an `exec.Cmd`) as a child (`dispatcher.go:110-140`). The manifest `entry` is meant to be the binary path (`manifest.go:145-147`), but no code maps a manifest to `Open` yet.
2. Magic cookie: env var `TUIBBS_PLUGIN=tuibbs-tier2-grpc-v1`, app protocol version 1 (`grpcsub.go:115-119`). The child must check it.
3. Handshake line on stdout: go-plugin's own format, `CORE-VERSION|APP-VERSION|NETWORK|ADDR|PROTOCOL|SERVER-CERT`, e.g. `1|1|unix|/path.sock|grpc|<cert>`. This comes from go-plugin, not this repo (UNVERIFIED against go-plugin v1.8.0 source; not in the clone).
4. AutoMTLS: the host sets `AutoMTLS: true` (`dispatcher.go:138`). The child must read the host's client certificate from its environment (go-plugin uses `PLUGIN_CLIENT_CERT`, UNVERIFIED here), generate its own certificate, serve gRPC over mutual TLS, and print its certificate in the handshake line. This is the hardest part for Python.
5. go-plugin side services: the host also talks to go-plugin's own services (health, broker, controller, stdio) on the same connection (`grpcsub.go:228-231`). A Python server must at least serve the gRPC health check for service `plugin`; whether controller/stdio are mandatory in v1.8.0 is UNVERIFIED.
6. Plugin set: single key `module` (`grpcsub.go:102`). In gRPC mode the key does not travel on the wire, so a Python server just serves the right service.
7. The module service: `/tuibbs.plugin.v1.ModuleService/Dispatch` (`grpcsub.go:221-225`). Catch: the host calls with gRPC content-subtype `tuibbs.plugin.v1`, not `proto` (`grpcsub.go:227-236`, `dispatcher.go:341`), so the HTTP/2 content-type is `application/grpc+tuibbs.plugin.v1`. Whether stock Python grpcio accepts that content-type is UNVERIFIED and needs a test. The body bytes are standard protobuf with the field numbers in `plugin.proto`, so Python stubs generated from that file would decode them.

Is the proto language-neutral? As a schema, yes: proto3 with only strings, bytes, bool, repeated string and a string map, no Go-specific types (`plugin.proto:50-197`). Only Go stubs are generated (`buf.gen.yaml:16-24`); no Python or other targets.

What a Python plugin would implement: one handler taking `ModuleCall` (name, principal, content_type, args bytes) and returning `ModuleResult` (payload bytes, content_type, code), wrapped in the handshake, mTLS and health plumbing above. It only runs when the host invokes it; it cannot push data or draw on the terminal.

Fit for an Orca observer: poor for a live dashboard. The contract is one request in, one byte payload out, with no stream and no terminal access, and the host is not wired into `cmd/tuibbs` yet. Separately, TUIBBS already spawns Claude Code sessions under a PTY through `internal/ailink` and `internal/session/spawn`, deliberately not through grpcsub (`internal/session/spawn/spawn.go:12-20`); that subsystem may be the more relevant neighbour for an Orca view (not reviewed further here).

## A5. How modules render screens

Short answer: plugins never draw. A plugin returns opaque bytes in `ModuleResult.Payload` (`proto/v1/plugin.proto:101-114`; ADR-X5 section 2, `docs/decisions/adr-x5-module-dispatch.md:73-81`). Every screen is a compiled-in Go Bubble Tea model.

Stack:
- `internal/tui/README.md:3-7`: "Bubble Tea program shell", one `tea.Program` per SSH session. go.mod pins bubbletea v2.0.6 (line 7), lipgloss v2.0.3 (8) and bubbles v2.1.0 (6). `internal/tui` holds only shell pieces (help.go, keybindings.go, modal_stack.go).
- `internal/render` is the renderer wrapper. It owns the RawRegion contract and the renderer panic boundary (`internal/render/README.md:10-12`). The pipeline is View, then buffer, then diff, then PTY write (`internal/render/pipeline.go:123-128`). Its input is `type Viewer interface { View() string }` (`pipeline.go:133-135`), so any model's text view feeds it. Entry points: `NewPipeline` (`pipeline.go:190`), `Render(v Viewer, region Region)` (`pipeline.go:255`), with `Region` and `Frame` in `render/frame.go:117` and `:151`.
- Colour goes through semantic tokens. `render.NewPalette(session.ColorLevel)` and `NewPaletteFromCaps` are at `render/adaptive.go:165` and `:187`, and `Foreground` / `Background(token)` return `lipgloss.Style` (`adaptive.go:243`, `:252`). `internal/theme/catalog.go` maps theme tokens and Lip Gloss border sets.
- Screens are `tea.Model`s with Init/Update/View: `render/watch/watch_model.go:139/216/245`, `msgbase/model.go:260/300/495`, `ailink/lifecycle_overlay.go:84/89/106`, `serve/menu.go:335/339/806`.
- `internal/route/registry.go:67-73`: a `Route` is metadata only (RouteID, Path, ACSExpressionID, BreadcrumbLabel, ParentRouteID). It holds no model, so the binding from a route to a screen lives in Go code. Where `serve/menu.go` makes that binding is UNVERIFIED.

Could a module read a JSON snapshot and draw it natively in Go? Yes, but only as compiled-in Go code in the TUIBBS tree, not as a plugin. There is already a close precedent: `internal/ailink/lifecycle_overlay.go`, the sysop-only read-only overlay. Its fields hold only value snapshots, a read-only provider and geometry (`lifecycle_overlay.go:46-61`). It re-reads its data source on the `r` key (`:94-97`), handles `tea.WindowSizeMsg` (`:91-93`), and builds its table as a plain string (`:110-135`). The overlay is gated by `DebugOverlayACS = "LV>3"` (`:27-30`), and the check fails closed (`:38-44`). An Orca observer built the same way would be a model that keeps an Orca JSON snapshot and refreshes it on a tick or a key. It would draw through the same pipeline and sit behind an ACS rule. Its data could come in as a tier-1 or tier-2 `Dispatch` returning JSON bytes. Note that tier-2 is not wired into production (A1), and the model would still have to be Go.

## A6. Width, NO_COLOR, ASCII fallback, wide characters, accessibility

Capabilities are worked out per SSH session from the client's own environment, never the host's. `session.DetectCaps(env, size)` is at `internal/session/caps.go:257`. The renderer deliberately avoids Lip Gloss's host-environment writer (`internal/render/colorlevel.go:29-34`).

| Topic | What the code does | Evidence |
|---|---|---|
| NO_COLOR | If `NO_COLOR` is non-empty, or `TERM` is empty or `dumb`, the session drops to the floor: ColorNone, ASCII width, no hints, no mouse, no bracketed paste. | `caps.go:227-228`, `:265`, `:274`; `caps.go:69-72` |
| Colour ladder | ColorNone, then 16, then 256, then truecolor. COLORTERM, the TERM suffix and a TERM_PROGRAM allow-list decide; anything unknown gets 16. ColorNone maps to NoTTY, which strips every ANSI sequence. | `caps.go:73-88`, `:240-245`; `render/colorlevel.go:17-25`, `:102` |
| ASCII / width mode | `UnicodeWidthMode` is ASCII, Strict (East-Asian Wide) or Loose (the default; ambiguous width counts as narrow). It can be forced with `TUIBBS_UNICODE=ascii\|strict\|loose`, and `LANG=C`/`POSIX` forces ASCII. | `caps.go:117-130`, `:229-239`, `:277-303` |
| Is the width mode used? | A grep of non-test `internal/` code found `UnicodeWidthMode` read only in `caps.go` and once more as a log field (`session/program.go:505`). No renderer was found that changes glyphs or measurement because of it. | grep; UNVERIFIED that nothing else reads it |
| Wide-character cell width | No direct `go-runewidth` or `uniseg` import in non-test `internal/`. Both are indirect dependencies (go.mod:81, :94). Measurement uses `lipgloss.Width`, for example `tui/modal_stack.go:304`, `:317-318`. | grep |
| Box drawing under the floor | Border glyphs are Unicode runes and stay even when colour is off. They "carry signal where colour cannot". No ASCII border swap was found. | `theme/catalog.go:63-66` |
| Terminal width / resize | SSH window-change events become `tea.WindowSizeMsg` sent to the session's program. Models such as the lifecycle overlay store the width and height. | `session/resize.go:140-170`; `ailink/lifecycle_overlay.go:91-93` |
| Minimum size | `caps.go:18` mentions a "<80x24 refuse-to-render banner". No code was found for it; the only grep hit is that comment. | UNVERIFIED |
| Contrast | A CI test holds every shipped theme to WCAG 2.1 AA, 4.5:1 for body text. | `theme/palette_wcag_aa_test.go:1`, `:42`, `:81` |
| Motion / screen reader | `TUIBBS_REDUCE_MOTION`, `TUIBBS_REDUCED_MOTION` and `TUIBBS_ACCESSIBLE` turn off animation. The spinner becomes a static "Working… (Ns)" label. There is an a11y test folder at `tests/a11y/`. | `motion/motion.go:1`, `:14`, `:28-35`, `:46-48` |

For an Orca observer, a native TUIBBS module would get NO_COLOR, the colour ladder, WCAG-checked themes, reduced motion and resize handling for free. Wide-character handling is whatever `lipgloss.Width` provides. ASCII mode does not appear to replace box-drawing glyphs.

## F. Roadmap and docs statements about modules, doors, plugins

- **README.md**: no mention of modules, doors, plugins or WASI (grep found nothing).
- **CHANGELOG.md:135-140** (v1.0.0 extension surface, FR-X-01..06): lists tier 1 compiled-in modules, tier 2 "HashiCorp `go-plugin` gRPC subprocess modules with crash isolation", tier 3 Lua, and tier 4 as "WASM **seam only** ... runtime disabled in v1". This conflicts with the code: the host is not wired into production, and a crashed plugin is not restarted (A1).
- **CHANGELOG.md:89-91**: "BBS *applications* (message bases, file bases, doors, federation, AI-session surfaces) are intentionally **not** in v1".
- **CHANGELOG.md:209-212**: "door games (S8/PTY → v1.x), and the 'watch my AI session' surface (S9 → v1.1)". It also says the `FR-V11-01..06` IDs are "forward-hook seams".
- **docs/scope.md:31**: doors are listed under ENiGMA½ parity as "NOT in v1".
- **docs/scope.md:41-43**: the FTN contract reserves "the dispatch seam through `internal/module/`".
- **internal/doors/README.md:3-5**: "PTY door supervisor — S8 (v1.x heavy)". It would spawn door subprocesses over a controlled PTY multiplexed through the session TUI. It is README only.
- **internal/module/README.md:3-5, 11-12**: a "Reserved boundary ... not an implemented registry". S5 (messages) and S7 (files) "will land in v1.x" there. The README says "Modules implement the `pkg/tuibbssdk` interfaces" (line 9), but `pkg/tuibbssdk` exports only `acs` (A3). The doc and the code have drifted apart.
- **docs/decisions/adr-x5-module-dispatch.md** (Accepted, line 3): one frozen typed interface with `[]byte` payloads, the same envelope in every tier (`:40`, `:73-81`).
- **docs/decisions/adr-x6-sdk-freeze.md** (Accepted, line 3): an `apidiff` baseline per `pkg/tuibbssdk` package, "additive-only within a major version" (`:70-80`). The freeze covers Go-importable API only; no ADR mentions non-Go plugin languages (grep).
- **docs/decisions/adr-x7-lua-sandbox-allowlist.md**: Accepted (line 3). It is the tier-3 sandbox allow-list.
- **docs/decisions/adr-x9-v1.4.1-message-base-substrate.md:10**: the messagebase seam is "intentionally outside" the SDK freeze. So the first real BBS application (S5, `internal/msgbase`) shipped as compiled-in Go, not as a plugin.
- **RELEASES.md**: "module" appears only in the Go-module/SBOM sense (`:200`, `:207`, `:217`), not in the plugin sense.

Roadmap reading: doors (S8) are v1.x and unbuilt. AI-session watching (S9) was v1.1 and now exists as `internal/ailink`. The plugin host is documented as shipped, but nothing calls it. Every real feature so far (msgbase, ailink, the watch view) is compiled-in Go.

## Verdict

1. Plugins in TUIBBS cannot draw. They return opaque bytes over a one-shot Dispatch with no stream, and the tier-2 gRPC host is tested but not wired into `cmd/tuibbs`, so a Python gRPC plugin is not a practical path.
2. The realistic TUIBBS form of an Orca observer is a compiled-in Go Bubble Tea model, built like `internal/ailink/lifecycle_overlay.go`, that reads an Orca JSON snapshot and sits behind an ACS rule. It would inherit NO_COLOR, the colour ladder, WCAG-checked themes and reduced motion.
3. So keep the standalone Python + Rich dashboard for the MVP. Make its JSON snapshot schema the stable contract, so that a later Go port to TUIBBS rewrites only the view, not the data source.

## UNVERIFIED

- The go-plugin v1.8.0 stdout handshake line format, the `PLUGIN_CLIENT_CERT` variable name, and which of the broker, controller and stdio services a non-Go plugin must serve.
- Whether stock Python `grpcio` will accept the custom content-subtype `application/grpc+tuibbs.plugin.v1`.
- That the host keeps a crashed tier-2 plugin in the Started state. This is inferred from `host.go:446-449`, not from a test.
- The per-file test counts in A1 come from counting `func Test` lines. The tests were not run.
- That nothing outside `caps.go` and `program.go:505` reads `UnicodeWidthMode`, that no <80x24 banner exists, and that ASCII mode keeps Unicode box-drawing glyphs.
- How `lipgloss.Width` measures wide and ambiguous characters internally.
- Where `serve/menu.go` binds routes to screen models.
