const PLAN_NAMES = ["plus", "pro", "business", "enterprise", "edu", "team", "free", "go"];
const FIVE_HOUR_MARKERS = ["5-hour", "5 hour", "5h", "5 h", "5 heures"];
const WEEKLY_MARKERS = ["weekly", "week", "hebdo", "semaine"];
const REMAINING_MARKERS = ["remaining", "available", "left", "restant", "restants", "disponible", "disponibles"];
const RESET_PATTERN = "(?:reset(?:s|ting)?|renouvel(?:le|lement)|reinitialis(?:e|ation)|réinitialis(?:e|ation))";
const USED_PATTERN = "\\b(?:used|utilis(?:e|ee|é|ée)s?|consomm(?:e|ee|é|ée)s?)\\b";

function compact(text) {
  return text.replace(/\r/g, "").replace(/[ \t]+/g, " ").trim();
}

function normalizeText(text) {
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
  let normalized = value.trim();
  if (/^\d+,\d{1,2}$/.test(normalized)) {
    normalized = normalized.replace(",", ".");
  } else {
    normalized = normalized.replace(/,/g, "");
  }
  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? parsed : null;
}

function cleanResetValue(value) {
  const normalized = compact(value);
  const isoMatch = normalized.match(/\d{4}-\d{2}-\d{2}T[0-9:.]+(?:Z|[+-]\d{2}:\d{2})?/);
  if (isoMatch) {
    return isoMatch[0];
  }
  return normalized.replace(/\.\s+(?:5(?:-|\s)?(?:hour|h|heures?)|weekly|week|hebdo|semaine)\b[\s\S]*$/i, "").replace(/\.$/, "");
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
    const match = progressbar.valueText.match(/(\d+(?:[.,]\d+)?)\s*%/);
    if (match) {
      return parseNumber(match[1]);
    }
  }
  return null;
}

function parsePercentFromText(text, markers, keywords = []) {
  const lines = text.split("\n");
  for (const line of lines) {
    const normalized = compact(line).toLowerCase();
    if (!markers.some((marker) => normalized.includes(marker))) {
      continue;
    }
    if (keywords.length > 0 && !keywords.some((keyword) => normalized.includes(keyword))) {
      continue;
    }
    const match = line.match(/(\d+(?:[.,]\d+)?)\s*%/);
    if (match) {
      return parseNumber(match[1]);
    }
  }
  return null;
}

function parseResetFromText(text, markers) {
  const expressions = markers.some((marker) => marker.includes("week"))
    ? [new RegExp(`(?:weekly|week|hebdo|semaine)[\\s\\S]{0,120}?${RESET_PATTERN}(?:\\s+(?:at|on|in|a|à|le|dans))?\\s*[:\\-]?\\s*([^\\n]+)`, "i")]
    : [new RegExp(`5(?:-|\\s)?(?:hour|h|heures?)[\\s\\S]{0,120}?${RESET_PATTERN}(?:\\s+(?:at|on|in|a|à|le|dans))?\\s*[:\\-]?\\s*([^\\n]+)`, "i")];

  const lines = text.split("\n");
  for (const line of lines) {
    const normalized = compact(line).toLowerCase();
    if (!markers.some((marker) => normalized.includes(marker))) {
      continue;
    }
    const match = firstMatch(line, expressions);
    if (match) {
      return cleanResetValue(match[1]);
    }
  }

  const globalMatch = firstMatch(text, expressions);
  return globalMatch ? cleanResetValue(globalMatch[1]) : null;
}

function parseUsedValue(text, markers) {
  const lines = text.split("\n");
  for (const line of lines) {
    const normalized = compact(line).toLowerCase();
    if (!markers.some((marker) => normalized.includes(marker))) {
      continue;
    }
    if (!new RegExp(USED_PATTERN, "i").test(normalized)) {
      continue;
    }
    const match = line.match(new RegExp(`${USED_PATTERN}[^0-9]*(\\d+(?:[.,]\\d+)?)`, "i"));
    if (match) {
      return parseNumber(match[1]);
    }
  }
  return null;
}

function parsePlan(text) {
  const planAlternatives = PLAN_NAMES.join("|");
  const match = firstMatch(text, [
    new RegExp(`\\b(?:plan|subscription|abonnement|forfait)\\b\\s*(?:actuel|current)?\\s*[:\\-]?\\s*(?:chatgpt\\s+)?(${planAlternatives})\\b`, "i"),
    new RegExp(`\\b(?:chatgpt\\s+)?(${planAlternatives})\\b[\\s\\S]{0,32}\\b(?:plan|subscription|abonnement|forfait)\\b`, "i"),
    new RegExp(`\\bchatgpt\\s+(${planAlternatives})\\b`, "i")
  ]);
  if (!match) {
    return null;
  }
  return match[1].toLowerCase();
}

function parseCredits(text) {
  const match = firstMatch(text, [
    /\bcr[eé]dits?\b(?:\s+(?:available|balance|remaining|restants?|disponibles?|solde))?\s*[:\-]?\s*(\d+(?:[.,]\d+)?)/i,
    /(\d+(?:[.,]\d+)?)\s+cr[eé]dits?\b/i
  ]);
  return match ? parseNumber(match[1]) : null;
}

function parseLimitStatus(text) {
  const normalized = text.toLowerCase();
  if (normalized.includes("limit reached")) {
    return "limit_reached";
  }
  if (normalized.includes("limite atteinte")) {
    return "limit_reached";
  }
  if (normalized.includes("near limit") || normalized.includes("proche de la limite")) {
    return "near_limit";
  }
  if (normalized.includes("available") || normalized.includes("disponible")) {
    return "available";
  }
  return "unknown";
}

function snapshotStatus(snapshot, text) {
  if (!text) {
    return "empty_page";
  }
  const expectedFields = ["plan", "5h_remaining_percent", "weekly_remaining_percent", "limit_status"];
  const missingFields = expectedFields.filter((field) => snapshot[field] === null || snapshot[field] === "unknown");
  return {
    extraction_status: missingFields.length === 0 ? "ok" : "partial",
    missing_fields: missingFields
  };
}

export function buildCodexSnapshot(artifacts) {
  const text = normalizeText(artifacts.text || "");
  const progressbars = artifacts.progressbars || [];
  const fiveHourRemaining =
    parsePercentFromProgressbars(progressbars, FIVE_HOUR_MARKERS) ??
    parsePercentFromText(text, FIVE_HOUR_MARKERS, REMAINING_MARKERS);
  const weeklyRemaining =
    parsePercentFromProgressbars(progressbars, WEEKLY_MARKERS) ??
    parsePercentFromText(text, WEEKLY_MARKERS, REMAINING_MARKERS);

  const snapshot = {
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
    page_title: artifacts.title || null
  };
  return {
    ...snapshot,
    ...snapshotStatus(snapshot, text)
  };
}
