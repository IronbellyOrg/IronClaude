# MCP Server Troubleshooting Guide

**MCP Server Focus**: Model Context Protocol (MCP) servers provide enhanced capabilities like documentation lookup (Context7), browser automation (Playwright), and project memory (Serena). This guide covers installation, configuration, and operational troubleshooting for shipped MCP servers.

**Server-Specific Solutions**: Each MCP server has unique requirements and common failure patterns. This guide provides targeted solutions for each server type and general MCP troubleshooting strategies.

## MCP Server Overview

### Available MCP Servers

**Available integrations (runtime use remains optional):**

- **Codebase Memory MCP**: Native graph memory; full user-level setup is a required phase of normal framework installation on Linux amd64/arm64
- **Context7**: Official documentation lookup and framework patterns
- **Playwright**: Browser automation and E2E testing
- **Morphllm**: Pattern-based code editing with token optimization
- **Serena**: Semantic code understanding and project memory

**Selection-specific requirements:**

- Claude CLI for registration; Codebase Memory automation supports Linux amd64/arm64, user scope only
- Codebase Memory requires curl/Bash only for acquisition, not Node/npm, Docker, an API key or a compiler
- npm-based servers require Node.js 18+ and npx/npm (Auggie `0.36.0` requires Node.js 20+); Serena uses uv; AIRIS Gateway uses Docker and curl

The older Node/npm troubleshooting examples below apply only to those servers, not native Codebase Memory.

**Other considerations:**
- Stable network connection for some servers
- Sufficient system memory (2GB+ recommended)

## Codebase Memory Native Lifecycle

Use the current flat command, not the historical generic reset recipes later in this guide:

```bash
superclaude install --list
superclaude mcp --servers codebase-memory-mcp
superclaude mcp --uninstall --servers codebase-memory-mcp --dry-run
superclaude mcp --uninstall --servers codebase-memory-mcp --yes
```

- **Default setup fails:** `superclaude install` runs full native setup after user setup; a failed required phase exits 1 and preserves installed framework work. Resolve the reported acquisition/verification/registration stage, then retry. macOS/Windows automation is unsupported before native effects; use [upstream manual instructions](https://github.com/DeusData/codebase-memory-mcp#installation) separately, not as a bypass for this required phase.
- **Understand what runs:** acquisition downloads the complete `https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh` into a private temporary directory, then runs Bash by argv. It preserves upstream checksum checks and full detected-client instructions/skills/agents/hooks, not binary-only setup. Both `main` bootstrap and latest-release assets move independently and are not pinned; checksums do not authenticate the bootstrap. See the [installation guide](../user-guide/mcp-installation.md) for the 60/300-second bounds and temporary-file cleanup.
- **Missing or stale registration:** a working binary is reused; only the exact user entry is reconciled to stdio, absolute executable and no arguments, without reacquiring companion assets. Same-named project/local registrations are not user-install success and are not removed by IronClaude's reconciliation. Unknown/unreadable configuration fails closed, not as absence. Failed replacement restores the prior user entry or explicitly reports restoration failure; inspect that state before retrying. A stale entry with `env` or `headers` values is refused before any change, so its values never reach a command line; update or remove it by hand, then retry.
- **No upgrade happened:** this is expected. Acquisition happens only when needed, never on every install. `--force` applies to framework files, not native upgrades/index resets; `--target` redirects slash commands only. `update` does not resurrect a removed tool; a later explicit `install` restores the default bundle. No adopt/skip/upgrade lifecycle flags exist.
- **Status is not a handshake:** `install --list` is read-only and reports executable status plus exact user registration (including unknown/stale). MCP `--list` uses legacy installed markers, not ownership/scope/health proof, and rejects selections/lifecycle flags, dry-run or non-user scope combinations. Success reports a verified version; restart clients and test a real tool separately. Installation does not index code or perform a live MCP handshake.
- **Removal refuses a canonical binary:** automatic removal needs the private `~/.local/bin/.superclaude-codebase-memory.json` acquisition receipt matching canonical binary identity/hash. Only actual IronClaude acquisition creates it; reuse of a preexisting/manual/external binary does not adopt it. Missing proof, an upstream-replaced binary, symlinks or uncertain ownership must be resolved through the original installer, not by inventing a receipt.
- **Full removal is account-wide:** user scope only, preview plus default-No consent; `--yes/-y` is the new explicit removal consent, not server selection or index-deletion permission. Upstream receives the canonical binary's `uninstall -y --dir=<canonical-bin-directory>` and owns activation/companion cleanup, which can interrupt sessions. IronClaude never requests index deletion/reset or manually deletes caches/companion assets. After native success it revokes its matching receipt and cleans up only a surviving exact user registration; unrelated names/project scopes remain outside that residual cleanup.
- **Absent or partial state:** no binary and no user entry is a no-op without companion audit; missing binary with a user entry permits confirmed registration-only partial cleanup, not a full-cleanup claim or download just to uninstall. External/custom-only binaries are reported and left to their original mechanism. Nonzero/timeout/postcondition failures report possible partial removal; inspect upstream output before retrying, with no rollback or blind second deletion pass.
- **Updater or another binary remains:** graph indexes stay, the adjacent updater is intentionally left and reported, and alternate PATH binaries are reported, not removed. Do not erase them or the cache as a generic repair step.

Without a terminal, explicit `--servers` selection is required, plus `--yes` for removal. With no selection on a terminal, the menu offers Install (default), Uninstall Codebase Memory, or Cancel; install remains gateway-first and all-individual selection includes Codebase Memory. Repeat `--servers` for multiple names. Dry-run prints choices or a selected plan including full source URL, account-wide effects and retained indexes, without prompts, downloads, lifecycle execution or config/file mutation.

**The disposable-environment live smoke passed on 2026-10-22** for upstream 0.12.1 on Linux amd64 (see the [release gate](../user-guide/mcp-installation.md#release-gate-separately-authorized-live-smoke) for the result and known residuals). Re-run that operator procedure for a materially different upstream release; mocked tests are not merge-safety proof. Stop and revise with the user if upstream overwrites unrelated framework/user assets; never silently switch to binary-only setup.

## Installation and Configuration Issues

### Node.js and npm Problems

#### Issue: Node.js Version Incompatibility

**Error Message**: `ERROR: MCP servers require Node.js 16+ but found Node.js 14.x`

**Diagnosis**:

```bash
node --version
npm --version
```

**Solution 1**: Update Node.js (Linux/Ubuntu)

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Solution 2**: Use Node Version Manager (nvm)

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install node
nvm use node
```

**Solution 3**: Manual Node.js installation

- Download from <https://nodejs.org/>
- Follow platform-specific installation instructions

**Verification**:

```bash
node --version  # Should be 16.0.0+
npm --version   # Should be 8.0.0+
```

**Issue: npm Permission Problems**

```bash
# Error message
ERROR: EACCES: permission denied, access '/usr/local/lib/node_modules'

# Solution 1: Configure npm for user directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile

# Solution 2: Fix npm permissions
sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}

# Solution 3: Use npx for package execution
npx @context7/mcp-server --version

# Verification
npm list -g --depth=0
npm config get prefix
```

### MCP Server Installation Failures

**Issue: Context7 MCP Server Installation Failed**

```bash
# Error message
ERROR: Failed to install @context7/mcp-server

# Diagnosis
npm list -g @context7/mcp-server
node --version

# Solution 1: Clean npm cache and reinstall
npm cache clean --force
npm install -g @context7/mcp-server

# Solution 2: Use alternative registry
npm install -g @context7/mcp-server --registry https://registry.npmjs.org/

# Solution 3: Manual installation verification
npm info @context7/mcp-server
npm install -g @context7/mcp-server@latest

# Verification
npm list -g @context7/mcp-server
node -e "console.log('Context7 installation test')"
```

## Connection and Communication Issues

### MCP Server Connection Failures

**Issue: Context7 Server Not Connecting**

```bash
# Error message
ERROR: MCP server 'context7' failed to connect

# Diagnosis
# Check Node.js installation
node --version  # Should be 16.0.0 or higher
npm list -g @context7/mcp-server

# Check server configuration
cat ~/.claude/CLAUDE.md | grep -i context7

# Solution 1: Restart Claude Code session
# MCP servers restart with Claude Code session restart

# Solution 2: Reconfigure MCP servers
python3 -m SuperClaude install --components mcp --force

# Solution 3: Manual server testing
node -e "console.log('Node.js working')"
npm test @context7/mcp-server

# Solution 4: Check network connectivity
ping context7-server.example.com  # If server requires network
curl -I https://context7-api.example.com/health  # Health check

# Verification
# Try Context7 functionality in Claude Code
# Should respond to documentation requests
```

**Issue: MCP Server Communication Timeout**

```bash
# Error message
ERROR: MCP server request timeout after 30 seconds

# Diagnosis
# Check network connectivity and server health
ping 8.8.8.8  # Basic connectivity
curl -I https://api.example.com/health  # API health

# Check system resources
top
free -h

# Solution 1: Reduce operation complexity
# Break complex tasks into smaller parts

# Solution 2: Restart Claude Code session
# MCP servers restart with Claude Code session restart

# Solution 3: Disable problematic server temporarily
# Use --no-mcp flag for operations

# Solution 4: Increase timeout (if configurable)
# Check MCP server configuration files

# Verification
# Test with simple operations first
# Gradually increase complexity
```

**Issue: Multiple MCP Servers Conflicting**

```bash
# Error message
ERROR: MCP server port conflicts detected

# Diagnosis
netstat -tlnp | grep :8000  # Check port usage
ps aux | grep -E "context7|playwright"

# Solution 1: Sequential server restart
# Restart Claude Code to reset all MCP servers

# Solution 2: Configure different ports
# Edit MCP server configuration files
# Usually in ~/.claude/ or server-specific directories

# Solution 3: Use selective server activation
# Use specific server flags instead of --all-mcp

# Verification
netstat -tlnp | grep -E "8000|8001|8002"  # Check port assignments
```

## Server-Specific Troubleshooting

### Context7 Documentation Server

**Issue: Context7 Not Finding Documentation**

```bash
# Symptoms: Context7 activated but returns no documentation

# Diagnosis
# Test Context7 connection
node -e "const c7 = require('@context7/mcp-server'); console.log('Context7 loaded');"

# Solution 1: Update Context7 server
npm update -g @context7/mcp-server

# Solution 2: Clear Context7 cache
rm -rf ~/.context7/cache/  # If cache directory exists

# Solution 3: Use explicit library keywords
# Use specific framework names in requests

# Solution 4: Verify internet connection
curl -I https://docs.react.dev/  # Example API test

# Verification
# Try specific documentation requests
# Should return relevant framework information
```

**Issue: Context7 Returning Outdated Information**

```bash
# Symptoms: Context7 returns old documentation versions

# Solution 1: Update Context7 server
npm uninstall -g @context7/mcp-server
npm install -g @context7/mcp-server@latest

# Solution 2: Clear documentation cache
rm -rf ~/.context7/  # Clear cache if exists

# Solution 3: Force documentation refresh
# Restart Claude Code session completely

# Verification
# Check documentation dates in responses
# Should return current framework versions
```

### Playwright Browser Automation

**Issue: Playwright Browser Installation Failures**

```bash
# Error message
ERROR: Playwright browser automation failed - browser not installed

# Diagnosis
npm list -g playwright
npx playwright --version

# Solution 1: Install Playwright browsers
npx playwright install
npx playwright install-deps

# Solution 2: Install specific browsers
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit

# Solution 3: Fix browser dependencies (Linux)
sudo apt-get install libnss3 libatk-bridge2.0-0 libdrm2 libgtk-3-0

# Verification
npx playwright --version
ls ~/.cache/ms-playwright/  # Check browser installations
```

**Issue: Playwright Browser Launch Failures**

```bash
# Error message
ERROR: Browser launch failed - display not available

# Diagnosis
echo $DISPLAY  # Check X11 display
ps aux | grep Xvfb  # Check virtual display

# Solution 1: Use headless mode
# Set headless: true in Playwright configuration

# Solution 2: Install virtual display (Linux)
sudo apt-get install xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &

# Solution 3: Use Docker for browser testing
docker run -it --rm playwright:latest

# Verification
# Should successfully launch browsers in headless mode
```

### Morphllm Pattern Editor

**Issue: Morphllm Pattern Application Failures**

```bash
# Symptoms: Pattern-based edits not applying correctly

# Diagnosis
npm list -g @morphllm/mcp-server

# Solution 1: Update Morphllm server
npm update -g @morphllm/mcp-server

# Solution 2: Use more specific patterns
# Provide explicit pattern descriptions

# Solution 3: Check file permissions
ls -la target-files/  # Ensure write permissions

# Verification
# Pattern edits should be applied consistently across files
```

### Serena Project Memory

**Issue: Serena Session Persistence Failures**

```bash
# Symptoms: Project context not persisting between sessions

# Diagnosis
ls ~/.claude/sessions/  # Check session storage
ls ~/.serena/  # Check Serena-specific storage

# Solution 1: Verify session save operations
# Ensure proper session saving before closing

# Solution 2: Check storage permissions
ls -la ~/.claude/sessions/
chmod 755 ~/.claude/sessions/

# Solution 3: Reinstall Serena server
# Remove existing Serena registration
claude mcp remove serena
# Reinstall using uvx
uvx --from serena-agent==1.7.0 serena --help
# Re-register with Claude
claude mcp add serena -- uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false

# Verification
# Session context should persist across Claude Code restarts
```

## Performance and Optimization

### MCP Server Performance Issues

**Issue: Slow MCP Server Response Times**

```bash
# Symptoms: MCP server operations causing delays

# Diagnosis
# Check MCP server installation and health
npm list -g | grep -E "context7|playwright"
top | grep node

# Solution 1: Selective MCP server usage
# Use only needed servers for specific tasks

# Solution 2: Restart Claude Code session
# This restarts all MCP servers fresh

# Solution 3: Local fallback mode
# Use --no-mcp flag for pure native operations

# Solution 4: Update all MCP servers
npm update -g

# Verification
time node -e "console.log('Node.js speed test')"
# Should complete successfully
```

**Issue: MCP Server Memory Leaks**

```bash
# Symptoms: Increasing memory usage over time

# Diagnosis
top | grep node  # Monitor Node.js processes
ps aux --sort=-%mem | head -10

# Solution 1: Regular Claude Code session restarts
# Restart sessions periodically during heavy usage

# Solution 2: Monitor specific servers
htop  # Monitor individual MCP server processes

# Solution 3: Use memory-efficient patterns
# Avoid keeping large data sets in MCP server memory

# Verification
free -h  # Monitor memory usage trends
```

### Resource Management

**Issue: Multiple MCP Servers Competing for Resources**

```bash
# Symptoms: System slowdown when multiple servers active

# Diagnosis
top | grep -E "node|mcp"
iostat 1 3  # Check I/O usage

# Solution 1: Use targeted server activation
# Activate only needed servers per task

# Solution 2: Increase system resources
# Add more RAM or CPU cores if possible

# Solution 3: Queue MCP operations
# Avoid simultaneous heavy operations

# Solution 4: Use MCP server priorities
# Configure resource allocation in MCP settings

# Verification
top  # Monitor resource usage during operations
```

## Advanced MCP Configuration

### Custom MCP Server Configuration

**Issue: Default MCP Configuration Not Optimal**

```bash
# Symptoms: MCP servers not performing optimally for specific use cases

# Solution 1: Locate configuration files
find ~/.claude/ -name "*mcp*" -type f
find ~/.config/ -name "*mcp*" -type f

# Solution 2: Customize server settings
# Edit server-specific configuration files
# Common locations: ~/.claude/mcp-config.json

# Solution 3: Environment variable configuration
export MCP_CONTEXT7_TIMEOUT=60

# Verification
# Test with custom configuration
# Should show improved performance for specific use cases
```

**Issue: MCP Server Load Balancing**

```bash
# Symptoms: Uneven load distribution across MCP servers

# Solution 1: Configure server priorities
# Edit MCP configuration to balance loads

# Solution 2: Use round-robin server selection
# Implement rotation logic in server calls

# Solution 3: Monitor server performance
# Track response times and adjust accordingly

# Verification
# Observe balanced resource usage across servers
```

## Debugging and Diagnostics

### MCP Server Health Monitoring

**Comprehensive MCP Health Check:**

```bash
# MCP Server System Diagnostics
echo "=== MCP Server Health Check ==="

# Node.js environment
echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

# Server installations
echo "=== Installed MCP Servers ==="
npm list -g | grep -E "context7|playwright|morphllm|serena"

# Process monitoring
echo "=== Running MCP Processes ==="
ps aux | grep -E "node.*mcp|mcp.*server" | head -5

# Resource usage
echo "=== Resource Usage ==="
echo "Memory: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "CPU Load: $(uptime | awk -F'load average:' '{print $2}')"

# Network connectivity (if required)
echo "=== Network Status ==="
ping -c 1 8.8.8.8 > /dev/null && echo "✅ Network OK" || echo "❌ Network Issue"
```

**MCP Server Functionality Test:**

```bash
# Test each MCP server individually
echo "=== MCP Server Functionality Test ==="

# Context7 test
if npm list -g @context7/mcp-server > /dev/null 2>&1; then
    echo "✅ Context7 installed"
else
    echo "❌ Context7 missing"
fi

# Playwright test
if npx playwright --version > /dev/null 2>&1; then
    echo "✅ Playwright installed"
else
    echo "❌ Playwright missing"
fi
```

### MCP Server Log Analysis

**Log Collection and Analysis:**

```bash
# Collect MCP server logs
echo "=== MCP Server Logs ==="

# Check common log locations
find ~/.claude/ -name "*.log" -type f 2>/dev/null
find /tmp/ -name "*mcp*.log" -type f 2>/dev/null
find /var/log/ -name "*mcp*.log" -type f 2>/dev/null

# Check npm logs
npm config get logs-max
ls ~/.npm/_logs/ 2>/dev/null | tail -5

# System logs for Node.js processes
journalctl -u node* --since "1 hour ago" 2>/dev/null | tail -10
```

## Emergency Recovery

### Complete MCP Reset

**Full MCP Server Reset Procedure:**

```bash
# Emergency MCP Reset
echo "=== Emergency MCP Server Reset ==="

# Step 1: Stop all Claude Code sessions
echo "Stop all Claude Code sessions and wait 30 seconds"

# Step 2: Backup current state
cp -r ~/.claude ~/.claude.mcp.backup.$(date +%Y%m%d)

# Step 3: Remove all MCP servers
npm list -g | grep -E "context7|playwright|morphllm|serena" | awk '{print $2}' | xargs npm uninstall -g

# Step 4: Clear npm cache
npm cache clean --force

# Step 5: Reinstall MCP servers
python3 -m SuperClaude install --components mcp --force

# Step 6: Verification
npm list -g | grep -E "context7|playwright|morphllm|serena"

# Step 7: Test functionality
echo "Test MCP servers in Claude Code after restart"
```

## Related Resources

### MCP-Specific Documentation

- **Core SuperClaude Guide**: [../user-guide/mcp-servers.md](../user-guide/mcp-servers.md) - MCP server overview and usage
- **Common Issues**: [common-issues.md](./common-issues.md) - General troubleshooting procedures
- **Diagnostic Reference**: [diagnostic-reference.md](./diagnostic-reference.md) - Advanced diagnostic procedures

### External Resources

- **Node.js Official**: [https://nodejs.org/](https://nodejs.org/) - Node.js installation and documentation
- **npm Documentation**: [https://docs.npmjs.com/](https://docs.npmjs.com/) - Package manager documentation
- **Playwright Guide**: [https://playwright.dev/](https://playwright.dev/) - Browser automation documentation

### Support Channels

- **GitHub Issues**: [MCP-specific problems](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues)
- **GitHub Discussions**: [MCP server community support](https://github.com/SuperClaude-Org/SuperClaude_Framework/discussions)

---

**npm-based Server Priority**: For npm-based servers only, check Node.js → npm → individual server → Claude Code integration. For native Codebase Memory, use the lifecycle section above; Node/npm repair and generic reset recipes do not apply.

**npm-based Verification Pattern**: For those servers, verify with:

- ✅ `node --version` - Should be 16.0.0+
- ✅ `npm list -g | grep mcp` - Should show installed servers
- ✅ Test server functionality in Claude Code - Should respond without errors
