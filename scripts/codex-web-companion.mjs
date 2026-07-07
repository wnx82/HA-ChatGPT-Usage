import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import readline from "node:readline/promises";
import { chromium } from "playwright";

import { buildCodexSnapshot } from "./codex-page-parser.mjs";

const DEFAULT_DASHBOARD_URL = "https://chatgpt.com/codex/cloud/settings/analytics";
const DEFAULT_OUTPUT_PATH = "/config/chatgpt_usage_codex.json";
const DEFAULT_PROFILE_DIR = path.resolve(".codex-web-companion/profile");

function parseArgs(argv) {
  const options = {
    out: DEFAULT_OUTPUT_PATH,
    profileDir: DEFAULT_PROFILE_DIR,
    url: DEFAULT_DASHBOARD_URL,
    watchSeconds: 0,
    headless: false
  };

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];
    const next = argv[index + 1];
    if (current === "--out" && next) {
      options.out = next;
      index += 1;
    } else if (current === "--profile-dir" && next) {
      options.profileDir = next;
      index += 1;
    } else if (current === "--url" && next) {
      options.url = next;
      index += 1;
    } else if (current === "--watch-seconds" && next) {
      options.watchSeconds = Number(next);
      index += 1;
    } else if (current === "--headless") {
      options.headless = true;
    } else if (current === "--help") {
      options.help = true;
    }
  }

  return options;
}

function printHelp() {
  process.stdout.write(
    [
      "Usage: npm run codex:companion -- [options]",
      "",
      "Options:",
      "  --out <path>            Output JSON path. Default: /config/chatgpt_usage_codex.json",
      "  --profile-dir <path>    Persistent Chromium profile directory.",
      "  --url <url>             Initial page to open. Default: Codex usage dashboard.",
      "  --watch-seconds <n>     Refresh and rewrite JSON every n seconds after capture.",
      "  --headless              Launch headless Chromium.",
      "  --help                  Show this help."
    ].join("\n"),
  );
}

async function ensureParentDirectory(filePath) {
  await fs.mkdir(path.dirname(path.resolve(filePath)), { recursive: true });
}

async function capturePageArtifacts(page) {
  return page.evaluate(() => {
    const progressbars = Array.from(document.querySelectorAll('[role="progressbar"], progress')).map((element) => {
      const parentText = element.parentElement?.innerText || "";
      const nearbyText = parentText.split("\n").slice(0, 4).join(" ");
      const valueNow = element.getAttribute("aria-valuenow");
      return {
        label: nearbyText,
        valueNow: valueNow === null ? null : Number(valueNow),
        valueText: element.getAttribute("aria-valuetext") || ""
      };
    });

    return {
      title: document.title,
      url: window.location.href,
      text: document.body?.innerText || "",
      progressbars
    };
  });
}

async function waitForEnter(promptText) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  try {
    await rl.question(promptText);
  } finally {
    rl.close();
  }
}

async function writeSnapshot(outputPath, snapshot) {
  await ensureParentDirectory(outputPath);
  await fs.writeFile(outputPath, JSON.stringify(snapshot, null, 2) + "\n", "utf-8");
}

async function run() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }

  const context = await chromium.launchPersistentContext(options.profileDir, {
    headless: options.headless,
    viewport: { width: 1440, height: 1000 }
  });

  const page = context.pages()[0] || (await context.newPage());
  await page.goto(options.url, { waitUntil: "domcontentloaded" });

  process.stdout.write(
    [
      "",
      "Codex web companion ready.",
      `1. Log in to ChatGPT in the opened browser if needed.`,
      "2. Open Codex Settings > Usage Dashboard if the browser is not already there.",
      "3. Wait until the 5h/weekly usage information is visible.",
      "4. Press Enter in this terminal to capture the page and write the JSON snapshot.",
      ""
    ].join("\n"),
  );

  await waitForEnter("Press Enter when the usage page is ready...");

  async function refreshOnce() {
    const artifacts = await capturePageArtifacts(page);
    const snapshot = buildCodexSnapshot(artifacts);
    await writeSnapshot(options.out, snapshot);
    process.stdout.write(`Snapshot written to ${options.out}\n`);
    process.stdout.write(`${JSON.stringify(snapshot, null, 2)}\n`);
  }

  await refreshOnce();

  if (options.watchSeconds > 0) {
    process.stdout.write(`Watching page every ${options.watchSeconds} seconds. Press Ctrl+C to stop.\n`);
    // Keep the browser and profile alive while periodically refreshing the file.
    for (;;) {
      await new Promise((resolve) => setTimeout(resolve, options.watchSeconds * 1000));
      await refreshOnce();
    }
  }

  await context.close();
}

run().catch((error) => {
  process.stderr.write(`${error.stack || error.message}\n`);
  process.exitCode = 1;
});
