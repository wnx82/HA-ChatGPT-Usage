import test from "node:test";
import assert from "node:assert/strict";

import { buildCodexSnapshot } from "./codex-page-parser.mjs";

test("buildCodexSnapshot parses visible usage text", () => {
  const snapshot = buildCodexSnapshot({
    title: "Codex Usage Dashboard",
    url: "https://chatgpt.com/codex/cloud/settings/analytics",
    text: `
      Plan: Pro
      5-hour usage used 42
      5-hour usage remaining 18%
      5-hour usage resets at 2026-07-07T15:00:00Z
      Weekly usage used 310
      Weekly usage remaining 44%
      Weekly usage resets at 2026-07-13T00:00:00Z
      Credits available 12.5
      Status available
    `,
    progressbars: []
  });

  assert.equal(snapshot.plan, "pro");
  assert.equal(snapshot["5h_used"], 42);
  assert.equal(snapshot["5h_remaining_percent"], 18);
  assert.equal(snapshot["5h_reset"], "2026-07-07T15:00:00Z");
  assert.equal(snapshot.weekly_used, 310);
  assert.equal(snapshot.weekly_remaining_percent, 44);
  assert.equal(snapshot.weekly_reset, "2026-07-13T00:00:00Z");
  assert.equal(snapshot.credits, 12.5);
  assert.equal(snapshot.limit_status, "available");
});

test("buildCodexSnapshot can use progressbars as a fallback", () => {
  const snapshot = buildCodexSnapshot({
    title: "Codex Usage Dashboard",
    url: "https://chatgpt.com/codex/cloud/settings/analytics",
    text: "Plan Pro",
    progressbars: [
      { label: "5-hour usage remaining", valueNow: 22, valueText: "22%" },
      { label: "weekly usage remaining", valueNow: 63, valueText: "63%" }
    ]
  });

  assert.equal(snapshot["5h_remaining_percent"], 22);
  assert.equal(snapshot.weekly_remaining_percent, 63);
});
