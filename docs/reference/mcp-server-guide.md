# MCP Server Troubleshooting Guide

**MCP Server Focus**: Model Context Protocol (MCP) servers provide enhanced capabilities like documentation lookup (Context7), and browser automation (Playwright). This guide covers installation, configuration, and operational troubleshooting for shipped MCP servers.

**Server-Specific Solutions**: Each MCP server has unique requirements and common failure patterns. This guide provides targeted solutions for each server type and general MCP troubleshooting strategies.

## MCP Server Overview

### Available MCP Servers

**Available integrations (runtime use remains optional):**

- **codegraph**: Code graph (symbols, callers, impact, file outlines); installed by default by `superclaude install`
- **Context7**: Official documentation lookup and framework patterns
- **Playwright**: Browser automation and E2E testing
- **Morphllm**: Pattern-based code editing with token optimization

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
npm list -g | grep -E "context7|playwright|morphllm"

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
npm list -g | grep -E "context7|playwright|morphllm" | awk '{print $2}' | xargs npm uninstall -g

# Step 4: Clear npm cache
npm cache clean --force

# Step 5: Reinstall MCP servers
python3 -m SuperClaude install --components mcp --force

# Step 6: Verification
npm list -g | grep -E "context7|playwright|morphllm"

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

**npm-based Server Priority**: For npm-based servers, check Node.js → npm → individual server → Claude Code integration.

**npm-based Verification Pattern**: For those servers, verify with:

- ✅ `node --version` - Should be 16.0.0+
- ✅ `npm list -g | grep mcp` - Should show installed servers
- ✅ Test server functionality in Claude Code - Should respond without errors
