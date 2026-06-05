#!/usr/bin/env node

const { spawnSync } = require("node:child_process");
const path = require("node:path");

const cliPath = path.resolve(__dirname, "..", "speedai_cli.py");
const candidates = process.platform === "win32" ? ["python", "py"] : ["python3", "python"];

let lastError = null;
for (const candidate of candidates) {
  const result = spawnSync(candidate, [cliPath, ...process.argv.slice(2)], { stdio: "inherit" });
  if (result.error) {
    lastError = result.error;
    if (result.error.code === "ENOENT") continue;
    console.error(result.error.message);
    process.exit(1);
  }
  process.exit(result.status === null ? 1 : result.status);
}

console.error("Python 3 is required to run speedai CLI.");
if (lastError && lastError.code !== "ENOENT") {
  console.error(lastError.message);
}
process.exit(1);
