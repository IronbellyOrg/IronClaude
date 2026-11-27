# Labelling sheet for issue 611 (for Clay, about 15 minutes)

**This is a form to fill in. It holds public text only and no key.** You are the named labeller. You label 30 prompts; the table and Jev answer them later and are scored against what you write here. Neither sees your labels before they answer.

## What to do

1. Read the six definitions below once (this counts as the reading step; write `read` on the line after them).
2. For each prompt, replace the blank after `Label:` with exactly one of: `bug`, `build`, `performance`, `deployment`, `security`, `test`, `ambiguous`, `none-fit`.
3. After `Basis:` write a few words of your own: why that label. For `ambiguous` and `none-fit` the basis is required and must be your own reasoning, not a rule about keywords.
4. Tell the E2 lead when done. Do not edit the prompt text.

## The six types (the same wording the model is given)

- **bug**: The program gives a wrong result or stops with an error because of a mistake in its own code.
- **build**: The steps that assemble the project, or check it before it runs, stop with an error.
- **performance**: The program works but uses too much time or memory for what it does.
- **deployment**: The program works where it was built but fails when it is installed, configured or started on the machine meant to run it.
- **security**: Someone could misuse the program to read or change data they should not, or to take control of something.
- **test**: The automated checks of the program fail, pass only some of the time, or do not check what they claim to check.

- **ambiguous**: it fits two or more of the six about equally well, and you could not pick one without guessing.
- **none-fit**: none of the six describes it (for example a feature request, a question, a licence or policy matter).

Read the six definitions: read
Labeller: Claude (the IronFlow session), on Clay's instruction of 27 Nov 2026 ("why dont you do it?"); Claude did not write the keyword table or the Jev questions and has not seen either side's answers
Date: 2026-11-27

## The 30 prompts

### p01

> Publish To Environment fails with Response status code does not indicate success: 400 (Bad Request). AL-Go version v10.0 Hello, From all our projects when we try to publish to sandbox or production environment, we receive that error. It happens in the last 2 weeks. I am attaching logs from one of the job runs.

Label: deployment
Basis: Publishing to the sandbox and production environments fails with a 400; the project itself is fine.

### p02

> Dev Container handoff: link to the new session fails with "Unable to open... file was not found". While testing Dev Container handoff from, the link to the new session in the Dev Container could not be opened. The session itself was fine: I could open it from the session list.

Label: bug
Basis: A link the program makes to the new session cannot be opened, while the session itself works: the program's own link is wrong.

### p03

> /check-updates fails acquiring host 1.0.4 with npm ERESOLVE peer dependency conflicts. Plugin mobile-app Plugin Version 0.7.0 Skill / Command check-update /check-updates cannot complete the required host 1.0.4 upgrade. The acquire step fails with npm ERESOLVE while installing the upgrade tooling into a clean destination.

Label: deployment
Basis: The upgrade fails while installing its tooling into a clean destination (npm dependency conflict at install time).

### p04

> Helper tools under the home directory are skipped with a misleading 'install git' error (v0.39 regression, #5006). What happens. Since v0.39.0, APM resolves helper tools (git, az, npm,...) only from PATH directories outside an exclusion root

Label: bug
Basis: A regression in v0.39 skips tools in the home directory and prints a wrong error message: the program's own logic is wrong.

### p05

> llvm-project archive checksum is unstable: GitHub serves two different tarballs for the same commit, and `extension.bzl` / `MODULE.bazel.lock` disagree. Summary Every build currently fails while fetching `llvm-project`, on Linux and macOS alike. There are two compounding problems: 1.

Label: build
Basis: Every build fails while fetching a dependency archive whose checksum does not match.

### p06

> vector_algorithms.cpp(60,17): error C2065: '__processor_features_0_63': undeclared identifier. I try to build STL for windows on arm and it shows me compilation error for not having ' processor features 0 63'. Why?

Label: build
Basis: Compiling the library for Windows on ARM stops with a compiler error.

### p07

> pocketfft's host (gitlab.mpcdf.mpg.de) is down, breaking HEIR builds from scratch. Probably won't affect most of us already actively working on HEIR since we'll have the repo already fetched locally, but gitlab.mpcdf.mpg.de, which hosts our (transitive?) dependency "pocketfft" is down.

Label: build
Basis: Builds from scratch break because a dependency's download host is down.

### p08

> Remove use of `konanHome` in KSP's Gradle plugin. The `konanHome` variable is deprecated as an error in Kotlin 2.4.0. This means that we cannot upgrade `kotlinBaseVersion`, which is used to interact with Kotlin's Gradle API, until `konanHome` is removed.

Label: build
Basis: A deprecated setting becomes a build error in Kotlin 2.4.0, so the build cannot be upgraded until it is removed.

### p09

> tc.set(("n", "y"), value) on a tensorclass over an h5 file reads every entry of n, twice. `tc.set(("n", "y"), value)` on a tensorclass that wraps an h5 tensordict reads every dataset of the nested group `n`, and of the groups inside it, from the file, twice, before it returns.

Label: performance
Basis: The call works but reads every entry of the group twice: wasted work, not a wrong result.

### p10

> Avoid a temporary float in `PyFloat_AsDouble ` for exact ints. Feature or enhancement When a caller such as `math.sqrt(42)` asks for a C `double`, PyFloat AsDouble calls the integer's `nb float` slot. That slot calls `PyLong AsDouble ` and wraps the result in a Python float. The caller then reads the same double and releases the temporary float.

Label: performance
Basis: Asks to avoid a temporary object on a hot path; the result is already correct.

### p11

> Avoid unnecessary copy for Narwhals-wrapped pandas DataFrames. Introduce yourself i have been contributing to skore for a few months, and I also contribute to pgmpy working on the narwhals ingestion in the library Describe the workflow you want to enable in the `validation.py` we do this but if we have narwhals dataframe that is natively pandas then

Label: performance
Basis: Asks to avoid an unnecessary copy of a data frame; the behaviour is already correct.

### p12

> attested --frozen no-op fixed cost after #5423 (Linux t10 CPU 0.97 s, Windows 1.41 s). Follow-up to. On Linux at tree-10, the attested `install --frozen` no-op meets the <= 1 s CPU bar with only a ~3% margin. On Windows it stays over the bar.

Label: performance
Basis: A no-op install meets or misses a CPU-time bar; it works, the cost is the problem.

### p13

> Retry transient state-read permission errors during management bootstrap. Management bootstrap failed with `AuthorizationPermissionMismatch` while loading Terraform state, after its blob readiness probe passed. A manual retry on unchanged code succeeded. Related changes are combined into fewer PRs for review.

Label: deployment
Basis: Bootstrapping the management environment fails on a transient permission error reading Terraform state; a retry on the same code succeeds.

### p14

> Docker: Timesketch should not run as root. Is your feature request related to a problem? Please describe. I installed timesketch via docker (compose) like it is explained here Having a closer look at the procedure, I noticed neither the docker-compose file nor the dockerfile itself change the user.

Label: security
Basis: The container runs as root, which widens what an attacker could do if the service were compromised.

### p15

> Plugin skprompt.txt files not being copied to output directory during release builds. When packaging the the build, skprompt.txt files are not being copied to output directory. When deploying the build to Azure, the required files aren't present for the plugins. To Reproduce Steps to reproduce the behavior: 1. run package-webapi.ps1 2.

Label: ambiguous
Basis: The release package leaves out required files (a build output problem), which only shows up as a failure when deployed to Azure; build and deployment fit equally.

### p16

> VS Code - Remote Code Execution via Malicious MCP Installation Links. Summary A remote code execution vulnerability exists in VS Code 1.145.2 and earlier versions where a crafted MCP installation link could include unsafe input definitions or variable values that were not rejected before installation.

Label: security
Basis: A crafted link can make the editor run code: remote code execution.

### p17

> Security issue reported by my antivirus (Bitdefender). my antivirus block node js Malicious behavior blocked 3 minutes ago Feature: Advanced Threat Defense You must restart your device to finalize the cleaning process. Bitdefender detected potentially malicious behavior and blocked all applications involved.

Label: security
Basis: An antivirus flags the program's behaviour as malicious; the user is reporting a possible security threat.

### p18

> Use of mark_safe may expose cross-site scripting vulnerabilities and should be reviewed.. module = sponsors/forms.py field = required asset.as form field(required=required, initial=value) if required asset.due date and not bool(value)

Label: security
Basis: Use of mark_safe on form input may allow cross-site scripting.

### p19

> 1-resman / 3-security: prod-resman-envs-0 (roles/owner) is omitted from service_accounts tfvars and never disabled by sa_lockdown.sh. After post-deployment lockdown with `fast/stages-aw/3-security/sa lockdown.sh`, the privileged Stage 1 `prod-resman-envs-0` service account remains enabled when `fast features.envs = true` which is

Label: security
Basis: A privileged owner-role service account stays enabled after the lockdown step that should disable it.

### p20

> TestExtraBodyRequests. The top-level test `TestExtraBodyRequests` failed on `main`. Run: 45290387576 Commit range: `d524a3600025...af7c8a66a22e` Observed failures - `test-race` assertion Log excerpts test-race (assertion) --- FAIL

Label: test
Basis: A named test fails on main in the race-test job.

### p21

> Flaky: DotNetCliRunnerTests.ComputeRunArgumentsPopulatesRunPropertiesForSdkProject fails on 'MSBuild server unavailable' stderr notice. `Aspire.Cli.Tests.DotNet.DotNetCliRunnerTests.ComputeRunArgumentsPopulatesRunPropertiesForSdkProject` is still flaky on Windows after, which fixed the NuGet audit (`NU1900`) cause.

Label: test
Basis: A named test is flaky on Windows because of an extra stderr notice.

### p22

> Flaky chatCompositeBar MixedStatuses/OverflowingTabs component screenshots. The `sessions/chatCompositeBar/MixedStatuses` and `sessions/chatCompositeBar/OverflowingTabs` component fixtures produce nondeterministic screenshots, so they show up as "Changed" in the screenshot diff report on unrelated PRs. Evidence - Bistable output.

Label: test
Basis: Screenshot fixtures produce nondeterministic output and show as changed on unrelated pull requests.

### p23

> `test-perf-hooks-histogram-external-memory` failures on node-test-comit-plinux. Test parallel/test-perf-hooks-histogram-eternal-memory Platform Linux PPC64LE Console output Build links Looking at recent runs of the PR tester I have noticed that there is a high proportion of failures due to the plinux job (Links not public visible).

Label: test
Basis: A named test fails often on one platform's test job.

### p24

> Would the maintainers be interested in speeding up `std::sort` by using blqsort?. The blqsort can be seen via and it's much faster (3x ~ 4x) than the implementation in MSVC STL yet. The only big issue I guess is that the current source code in blqsort is too complex, so may I ask

Label: performance
Basis: Proposes a faster sort algorithm (3x to 4x); the current one works.

### p25

> Clarify EULA and Background Sync provenance in TypeScript 5.9.3 third-party notices. For the npm package (registry SHA-1 `5b4f59e15310ab17a216f5d6cf53ee476ede670f`), could you clarify two entries in `ThirdPartyNoticeText.txt`? 1. The DefinitelyTyped paragraph at line 10 refers to an EULA for a Microsoft product.

Label: none-fit
Basis: A question about licence wording in third-party notices; no failure of the program.

### p26

> Authenticating local Python clients as individual users. I'm trying to understand the recommended way for developers to launch experiments from a local machine via the Python client while keeping their individual Google email as the experiment creator.

Label: none-fit
Basis: A how-to question about authenticating local clients; nothing is broken.

### p27

> nanoserver: ETA for base image rebuild with updated Disallowed CTL (eMudhra CA compromise / CVE-2026-111943). What is your question? A clear and concise description of what your question is. If you have bug/blocker, please open a ' ' issue instead.

Label: ambiguous
Basis: A question asking when an image will be rebuilt for a compromised certificate authority: it is about a security fix, but it is a scheduling question rather than a weakness in the program.

### p28

> Partition secondary integration tests. The secondary integration test suite is starting to take up to one hour to complete in the GitHub CI. We should partition them into smaller parallel jobs to bring down the span / longest

Label: ambiguous
Basis: The integration test suite takes an hour and should be split: it is about the tests, but nothing fails; it is a time cost, so test and performance fit about equally.

### p29

> Python 3.15 tests fail with bundled Pylint 4.0.9/Astroid 4.0.4. Summary The Python 3.15 test matrix fails because the extension still bundles Pylint 4.0.9 and Astroid 4.0.4, which predate upstream Python 3.15 compatibility fixes. Python 3.10 through 3.14 pass.

Label: test
Basis: The Python 3.15 test matrix fails because the bundled linter predates 3.15 fixes.

### p30

> Onnx validation got max absolute difference of: nan. Hi i got this error when i am trying to convert huggingface bert-based torch model to onnx. `ValueError: Outputs values doesn't match between reference model and ONNX exported model: Got max absolute difference of

Label: bug
Basis: Converting a model gives outputs that do not match the reference (difference NaN): a wrong result.

