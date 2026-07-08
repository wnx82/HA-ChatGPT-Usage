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
  assert.equal(snapshot.extraction_status, "ok");
  assert.deepEqual(snapshot.missing_fields, []);
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

test("buildCodexSnapshot preserves zero percent values from progressbars", () => {
  const snapshot = buildCodexSnapshot({
    title: "Codex Usage Dashboard",
    url: "https://chatgpt.com/codex/cloud/settings/analytics",
    text: "5-hour usage remaining 90% Weekly usage remaining 80%",
    progressbars: [
      { label: "5-hour usage remaining", valueNow: 0, valueText: "0%" },
      { label: "weekly usage remaining", valueNow: 0, valueText: "0%" }
    ]
  });

  assert.equal(snapshot["5h_remaining_percent"], 0);
  assert.equal(snapshot.weekly_remaining_percent, 0);
});

test("buildCodexSnapshot parses ChatGPT subscription wording", () => {
  const snapshot = buildCodexSnapshot({
    title: "Codex Usage Dashboard",
    url: "https://chatgpt.com/codex/cloud/settings/analytics",
    text: "Current subscription: ChatGPT Plus",
    progressbars: []
  });

  assert.equal(snapshot.plan, "plus");
});

test("buildCodexSnapshot parses French usage wording", () => {
  const snapshot = buildCodexSnapshot({
    title: "Tableau d'utilisation Codex",
    url: "https://chatgpt.com/codex/cloud/settings/analytics",
    text: `
      Abonnement actuel : ChatGPT Go
      Utilisation 5 heures utilisés 42
      Utilisation 5 heures restant 18,5%
      Utilisation 5 heures réinitialisation le 2026-07-08T15:00:00Z
      Utilisation semaine utilisés 310
      Utilisation semaine restants 44,5%
      Utilisation semaine réinitialisation le 2026-07-13T00:00:00Z
      Crédits restants : 12,5
      Statut disponible
    `,
    progressbars: []
  });

  assert.equal(snapshot.plan, "go");
  assert.equal(snapshot["5h_used"], 42);
  assert.equal(snapshot["5h_remaining_percent"], 18.5);
  assert.equal(snapshot["5h_reset"], "2026-07-08T15:00:00Z");
  assert.equal(snapshot.weekly_used, 310);
  assert.equal(snapshot.weekly_remaining_percent, 44.5);
  assert.equal(snapshot.weekly_reset, "2026-07-13T00:00:00Z");
  assert.equal(snapshot.credits, 12.5);
  assert.equal(snapshot.limit_status, "available");
});

test("buildCodexSnapshot reports missing fields for partial captures", () => {
  const snapshot = buildCodexSnapshot({
    title: "Login",
    url: "https://chatgpt.com/",
    text: "ChatGPT Plus",
    progressbars: []
  });

  assert.equal(snapshot.plan, "plus");
  assert.equal(snapshot.extraction_status, "partial");
  assert.deepEqual(snapshot.missing_fields, ["5h_remaining_percent", "weekly_remaining_percent", "limit_status"]);
});

test("buildCodexSnapshot does not mix fallback reset windows", () => {
  const snapshot = buildCodexSnapshot({
    title: "Codex Usage Dashboard",
    url: "https://chatgpt.com/codex/cloud/settings/analytics",
    text: "5-hour window resets at 2026-07-08T15:00:00Z. Weekly window resets at 2026-07-13T00:00:00Z.",
    progressbars: []
  });

  assert.equal(snapshot["5h_reset"], "2026-07-08T15:00:00Z");
  assert.equal(snapshot.weekly_reset, "2026-07-13T00:00:00Z");
});
