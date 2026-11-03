# MCP Server Troubleshooting Guide

**MCP Server Focus**: Model Context Protocol (MCP) servers provide enhanced capabilities like code graph queries (codegraph), documentation lookup (Context7), web search (Tavily) and browser automation (Playwright). This guide covers installation, configuration, and operational troubleshooting for shipped MCP servers.

**Server-Specific Solutions**: Each MCP server has unique requirements and common failure patterns. This guide provides targeted solutions for each server type and general MCP troubleshooting strategies.

## MCP Server Overview

### Available MCP Servers

**Available integrations (runtime use remains optional):**

- **codegraph**: Code graph (symbols, callers, impact, file outlines); installed by default by `superclaude install`
- **context7**: Official library documentation (`npx -y @upstash/context7-mcp`)
- **playwright**: Browser automation and E2E testing (`npx -y @playwright/mcp@latest`)
- **morphllm-fast-apply**: Fast Apply code edits (`npx -y @morphllm/morphmcp`, needs `MORPH_API_KEY`)
- **tavily**: Web search for research (`npx -y tavily-mcp@0.2.22`, needs `TAVILY_API_KEY`)
- **auggie**: Augment Code codebase search (global `@augmentcode/auggie@0.36.0` binary plus a one-time `auggie login`)
- **litellm**: LiteLLM MCP gateway over HTTP (opt-in only: never part of the "0 for all" menu choice; select it explicitly)
- **airis-mcp-gateway**: AIRIS MCP Gateway, a Docker-based gateway (the default choice of the interactive `superclaude mcp` menu)

Install any of them with `superclaude mcp --servers <name>` (repeat `--servers` for several). `superclaude mcp --list` shows the list without changing anything. Registrations use user scope unless you pass `--scope local` or `--scope project`.

**Selection-specific requirements:**

- Claude CLI for registration
- npm-based servers require Node.js 18+ and npx/npm (Auggie `0.36.0` requires Node.js 20+); AIRIS Gateway uses Docker and curl

**Other considerations:**

- Stable network connection for some servers
- Sufficient system memory (2GB+ recommended)

## codegraph lifecycle

codegraph is installed and registered by `superclaude install` (pinned `v1.6.2`, SHA-256 verified, user scope). Setup, costs, removal and the opt-out are in the [MCP installation guide](../user-guide/mcp-installation.md#default-setup-codegraph). Quick checks:

```bash
superclaude install --list    # Executable, Owner, User registration, Ready for Serena retirement
superclaude doctor            # "codegraph MCP registration" fails only if the registered command is gone
claude mcp remove codegraph --scope user   # unregister (see the guide for the files to delete)
```

The tools in a session are limited by `CODEGRAPH_MCP_TOOLS` in the registered entry (`node,search,callers,callees,impact,files,status`); `codegraph_explore` is intentionally hidden.

### codegraph troubleshooting

- **"No CodeGraph project is loaded for this session", or the index belongs to a different working tree**: the checkout has no index yet (the session-start hook starts one in the background) or the session was opened before it finished. Use Read/Grep for now, or run `codegraph init --yes` in the directory printed by `git rev-parse --show-toplevel`. It is safe to repeat.
- **A lock error, or an index that suddenly became empty**: `codegraph status`, `index` and `sync` can empty an index that another process is building. Check with `pgrep -f 'codegraph\.js (init|index)'` first, and use `init` to rebuild.
- **Stale or wrong version**: `superclaude doctor` prints "registered codegraph prints X, the pin is 1.6.2". Run `superclaude install`; it replaces an entry it wrote and keeps one you changed.
- **No index is created in CI or a headless pipeline**: that is intended when `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` is set; unset it, or run `codegraph init --yes` yourself.

## Installation and Configuration Issues

### Node.js and npm Problems

#### Issue: Node.js Version Incompatibility

**Error Message**: `Node.js 18+ required for selected npm servers` (`Node.js 20+` when Auggie is selected)

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
node --version  # Should be 18.0.0+ (20.0.0+ for Auggie)
npx --version   # npx must be on PATH for the npx-based servers
```

**Issue: npm Permission Problems**

Only global installs hit this; of the shipped servers only Auggie is installed globally (`npm install -g @augmentcode/auggie@0.36.0`). The other npm-based servers run through `npx -y` and need no global install.

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

# Verification
npm list -g --depth=0
npm config get prefix
```

### MCP Server Installation Failures

**Issue: Context7 MCP Server Registration Failed**

Context7 is registered as `npx -y @upstash/context7-mcp`; npx downloads the package when Claude Code starts the server, so nothing is installed globally.

```bash
# Diagnosis
node --version          # 18+
npx --version
claude mcp get context7 # shows the registered command, if any

# Solution 1: Re-register the server
claude mcp remove context7 --scope user
superclaude mcp --servers context7

# Solution 2: Clear a broken npx download cache
npm cache clean --force

# Verification
claude mcp get context7
```

## Connection and Communication Issues

### MCP Server Connection Failures

**Issue: Context7 Server Not Connecting**

```bash
# Error message
ERROR: MCP server 'context7' failed to connect

# Diagnosis
# Check Node.js installation
node --version  # Should be 18.0.0 or higher

# Check server registration
claude mcp get context7

# Solution 1: Restart Claude Code session
# MCP servers restart with Claude Code session restart

# Solution 2: Reconfigure the MCP server
superclaude mcp --servers context7

# Verification
# Try Context7 functionality in Claude Code
# Should respond to documentation requests
```

**Issue: MCP Server Communication Timeout**

```bash
# Error message
ERROR: MCP server request timeout after 30 seconds

# Diagnosis
# Check network connectivity
ping 8.8.8.8  # Basic connectivity

# Check system resources
top
free -h

# Solution 1: Reduce operation complexity
# Break complex tasks into smaller parts

# Solution 2: Restart Claude Code session
# MCP servers restart with Claude Code session restart

# Solution 3: Disable a problematic server temporarily
claude mcp remove <name> --scope user   # re-add later with superclaude mcp --servers <name>
# /sc:troubleshoot and /sc:reflect also accept --no-mcp (native tools only)

# Verification
# Test with simple operations first
# Gradually increase complexity
```

**Issue: Multiple MCP Servers Conflicting**

The npx-based servers use stdio transport and open no network ports, so they cannot clash on a port.

```bash
# Diagnosis
claude mcp list   # every registered server and its connection status
ps aux | grep -E "context7|playwright"

# Solution 1: Sequential server restart
# Restart Claude Code to reset all MCP servers

# Solution 2: Remove a duplicate registration
# The same server registered at two scopes (user and project) can both start
claude mcp get <name>
claude mcp remove <name> --scope project

# Verification
claude mcp list
```

## Server-Specific Troubleshooting

### Context7 Documentation Server

**Issue: Context7 Not Finding Documentation**

```bash
# Symptoms: Context7 activated but returns no documentation

# Diagnosis
claude mcp get context7   # command should be npx -y @upstash/context7-mcp

# Solution 1: Restart Claude Code (npx fetches the package again when needed)

# Solution 2: Use explicit library keywords
# Use specific framework names in requests

# Solution 3: Verify internet connection
curl -I https://docs.react.dev/  # Example connectivity test

# Verification
# Try specific documentation requests
# Should return relevant framework information
```

**Issue: Context7 Returning Outdated Information**

```bash
# Symptoms: Context7 returns old documentation versions

# Solution 1: Refresh the cached npx package
npm cache clean --force

# Solution 2: Force documentation refresh
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
claude mcp get playwright   # command should be npx -y @playwright/mcp@latest
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

# Verification
# Should successfully launch browsers in headless mode
```

### Morphllm Fast Apply

**Issue: Morphllm Pattern Application Failures**

```bash
# Symptoms: Pattern-based edits not applying correctly

# Diagnosis
claude mcp get morphllm-fast-apply   # command should be npx -y @morphllm/morphmcp
echo ${MORPH_API_KEY:+set}           # prints "set" when the key is in the environment

# Solution 1: Re-register with the API key
export MORPH_API_KEY=<your-key>
claude mcp remove morphllm-fast-apply --scope user
superclaude mcp --servers morphllm-fast-apply

# Solution 2: Use more specific patterns
# Provide explicit pattern descriptions

# Solution 3: Check file permissions
ls -la target-files/  # Ensure write permissions

# Verification
# Pattern edits should be applied consistently across files
```

## Performance and Optimization

### MCP Server Performance Issues

**Issue: Slow MCP Server Response Times**

```bash
# Symptoms: MCP server operations causing delays

# Diagnosis
# Check MCP server registration and health
claude mcp list
top | grep node

# Solution 1: Selective MCP server usage
# Use only needed servers for specific tasks

# Solution 2: Restart Claude Code session
# This restarts all MCP servers fresh

# Solution 3: Local fallback mode
# /sc:troubleshoot and /sc:reflect accept --no-mcp for native-tools-only runs

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
# Register only the servers you use

# Solution 2: Increase system resources
# Add more RAM or CPU cores if possible

# Solution 3: Queue MCP operations
# Avoid simultaneous heavy operations

# Verification
top  # Monitor resource usage during operations
```

## Advanced MCP Configuration

### Custom MCP Server Configuration

**Issue: Default MCP Configuration Not Optimal**

MCP registrations belong to Claude Code: user-scope entries are stored in `~/.claude.json`, project-scope entries in the project's `.mcp.json`. Inspect and change them with the `claude mcp` commands rather than by editing files.

```bash
# Solution 1: Inspect the registered command, arguments and environment
claude mcp list
claude mcp get <name>

# Solution 2: Change a setting by re-registering
claude mcp remove <name> --scope user
superclaude mcp --servers <name>

# Verification
claude mcp get <name>
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

# Server registrations
echo "=== Registered MCP Servers ==="
claude mcp list

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
if claude mcp get context7 > /dev/null 2>&1; then
    echo "✅ Context7 registered"
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

# Step 2: Backup current state (user-scope registrations live in ~/.claude.json)
cp ~/.claude.json ~/.claude.json.mcp.backup.$(date +%Y%m%d)
cp -r ~/.claude ~/.claude.mcp.backup.$(date +%Y%m%d)

# Step 3: Remove the npm-based MCP registrations
claude mcp remove context7 --scope user
claude mcp remove playwright --scope user
claude mcp remove morphllm-fast-apply --scope user

# Step 4: Clear npm cache
npm cache clean --force

# Step 5: Re-register MCP servers
superclaude mcp --servers context7 --servers playwright --servers morphllm-fast-apply

# Step 6: Verification
claude mcp list

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

- **GitHub Issues**: [MCP-specific problems](https://github.com/IronbellyOrg/IronClaude/issues)

---

**npm-based Server Priority**: For npm-based servers, check Node.js → npx → server registration → Claude Code integration.

**npm-based Verification Pattern**: For those servers, verify with:

- ✅ `node --version` - Should be 18.0.0+ (20.0.0+ for Auggie)
- ✅ `claude mcp list` - Should show the registered servers
- ✅ Test server functionality in Claude Code - Should respond without errors
