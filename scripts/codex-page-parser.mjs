const FIVE_HOUR_MARKERS = ["5-hour", "5 hour", "5h"];
const WEEKLY_MARKERS = ["weekly", "week"];

function compact(text) {
  return text.replace(/\r/g, "").replace(/[ \t]+/g, " ").trim();
}

function firstMatch(text, expressions) {
  for (const expression of expressions) {
    const match = text.match(expression);
    if (match) {
      return match;
    }
  }
  return null;
}

function parseNumber(value) {
  if (!value) {
    return null;
  }
  const normalized = value.replace(/,/g, "").trim();
  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? parsed : null;
}

function parsePercentFromProgressbars(progressbars, markers) {
  for (const progressbar of progressbars) {
    const haystack = `${progressbar.label} ${progressbar.valueText}`.toLowerCase();
    if (!markers.some((marker) => haystack.includes(marker))) {
      continue;
    }
    if (typeof progressbar.valueNow === "number") {
      return progressbar.valueNow;
    }
    const match = progressbar.valueText.match(/(\d+(?:\.\d+)?)\s*%/);
    if (match) {
      return parseNumber(match[1]);
    }
  }
  return null;
}

function parsePercentFromText(text, markers, keyword) {
  const lines = text.split("\n");
  for (const line of lines) {
    const normalized = compact(line).toLowerCase();
    if (!markers.some((marker) => normalized.includes(marker))) {
      continue;
    }
    if (keyword && !normalized.includes(keyword)) {
      continue;
    }
    const match = line.match(/(\d+(?:\.\d+)?)\s*%/);
    if (match) {
      return parseNumber(match[1]);
    }
  }
  return null;
}

function parseResetFromText(text, markers) {
  const lines = text.split("\n");
  for (const line of lines) {
    const normalized = compact(line).toLowerCase();
    if (!markers.some((marker) => normalized.includes(marker))) {
      continue;
    }
    const match = line.match(/reset(?:s|ting)?(?:\s+(?:at|on|in))?\s*[:\-]?\s*(.+)$/i);
    if (match) {
      return compact(match[1]);
    }
  }

  const globalMatch = firstMatch(text, [
    /5(?:-|\s)?hour[\s\S]{0,120}?reset(?:s|ting)?(?:\s+(?:at|on|in))?\s*[:\-]?\s*([^\n]+)/i,
    /weekly[\s\S]{0,120}?reset(?:s|ting)?(?:\s+(?:at|on|in))?\s*[:\-]?\s*([^\n]+)/i
  ]);
  return globalMatch ? compact(globalMatch[1]) : null;
}

function parseUsedValue(text, markers) {
  const lines = text.split("\n");
  for (const line of lines) {
    const normalized = compact(line).toLowerCase();
    if (!markers.some((marker) => normalized.includes(marker))) {
      continue;
    }
    if (!/\bused\b/.test(normalized)) {
      continue;
    }
    const match = line.match(/\bused\b[^0-9]*(\d+(?:\.\d+)?)/i);
    if (match) {
      return parseNumber(match[1]);
    }
  }
  return null;
}

function parsePlan(text) {
  const match = firstMatch(text, [
    /\bplan\b\s*[:\-]?\s*(plus|pro|business|enterprise|edu|team|free)\b/i,
    /\b(plus|pro|business|enterprise|edu|team|free)\b[\s\S]{0,24}\bplan\b/i
  ]);
  if (!match) {
    return null;
  }
  return match[1] ? match[1].toLowerCase() : match[0].toLowerCase();
}

function parseCredits(text) {
  const match = firstMatch(text, [
    /\bcredits?\b(?:\s+(?:available|balance|remaining))?\s*[:\-]?\s*(\d+(?:\.\d+)?)/i,
    /(\d+(?:\.\d+)?)\s+credits?\b/i
  ]);
  return match ? parseNumber(match[1]) : null;
}

function parseLimitStatus(text) {
  const normalized = text.toLowerCase();
  if (normalized.includes("limit reached")) {
    return "limit_reached";
  }
  if (normalized.includes("near limit")) {
    return "near_limit";
  }
  if (normalized.includes("available")) {
    return "available";
  }
  return "unknown";
}

export function buildCodexSnapshot(artifacts) {
  const text = compact(artifacts.text || "");
  const progressbars = artifacts.progressbars || [];
  const fiveHourRemaining =
    parsePercentFromProgressbars(progressbars, FIVE_HOUR_MARKERS) ||
    parsePercentFromText(text, FIVE_HOUR_MARKERS, "remaining");
  const weeklyRemaining =
    parsePercentFromProgressbars(progressbars, WEEKLY_MARKERS) ||
    parsePercentFromText(text, WEEKLY_MARKERS, "remaining");

  return {
    "5h_used": parseUsedValue(text, FIVE_HOUR_MARKERS),
    "5h_remaining_percent": fiveHourRemaining,
    "5h_reset": parseResetFromText(text, FIVE_HOUR_MARKERS),
    weekly_used: parseUsedValue(text, WEEKLY_MARKERS),
    weekly_remaining_percent: weeklyRemaining,
    weekly_reset: parseResetFromText(text, WEEKLY_MARKERS),
    plan: parsePlan(text),
    credits: parseCredits(text),
    limit_status: parseLimitStatus(text),
    last_update: new Date().toISOString(),
    source_url: artifacts.url || null,
    page_title: artifacts.title || null,
    extraction_status: text ? "ok" : "empty_page"
  };
}
