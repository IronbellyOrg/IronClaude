#!/usr/bin/env node

const fs = require('fs');
const os = require('os');
const path = require('path');

const stylePath = path.join(os.homedir(), '.claude', 'output-styles', 'pragmatic.md');

try {
  const source = fs.readFileSync(stylePath, 'utf8');
  const instructions = source.replace(/^---[\s\S]*?---\s*/, '');
  const output = {
    hookSpecificOutput: {
      hookEventName: 'SubagentStart',
      additionalContext: `PRAGMATIC MODE ACTIVE\n\n${instructions}`,
    },
  };
  process.stdout.write(JSON.stringify(output));
} catch (error) {
  process.stderr.write(`Failed to load Pragmatic instructions from ${stylePath}: ${error.message}\n`);
  process.exit(1);
}
