from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timezone
from typing import Any


@dataclass
class TenderDecision:
    decision: str
    score: int
    matched_capabilities: list[str]
    blockers: list[str]
    review_reasons: list[str]
    evidence_record: dict[str, Any]


def _text(opportunity: dict[str, Any]) -> str:
    parts = [
        str(opportunity.get("title", "")),
        str(opportunity.get("description", "")),
        " ".join(map(str, opportunity.get("requirements", []))),
        " ".join(map(str, opportunity.get("tags", []))),
        str(opportunity.get("buyer", "")),
    ]
    return " ".join(parts).lower()


def _deadline_passed(deadline: Any, now: datetime | None = None) -> bool:
    """True only when the deadline is a valid date-time that is already in the past."""
    if not deadline:
        return False
    try:
        target = datetime.fromisoformat(str(deadline).replace("Z", "+00:00"))
    except ValueError:
        return False
    if target.tzinfo is None:
        target = target.replace(tzinfo=timezone.utc)
    return target <= (now or datetime.now(timezone.utc))


def score_opportunity(opportunity: dict[str, Any], profile: dict[str, Any], now: datetime | None = None) -> TenderDecision:
    corpus = _text(opportunity)
    score = 20
    matched: list[str] = []
    blockers: list[str] = []
    review_reasons: list[str] = []

    # Capability fit: bounded contribution so keyword stuffing cannot dominate.
    capability_hits = 0
    for capability, keywords in profile.get("capabilities", {}).items():
        if any(keyword.lower() in corpus for keyword in keywords):
            matched.append(capability)
            capability_hits += 1
    score += min(capability_hits * 8, 40)

    # Explicit SME / pilot / council signals.
    for signal, weight in profile.get("positive_signals", {}).items():
        if signal.lower() in corpus:
            score += int(weight)

    # Known delivery risks.
    for signal, penalty in profile.get("risk_signals", {}).items():
        if signal.lower() in corpus:
            score -= int(penalty)
            review_reasons.append(f"Risk signal: {signal}")

    # Hard blockers always force NO_BID unless the profile is updated with evidence.
    for blocker in profile.get("hard_blockers", []):
        if blocker.lower() in corpus:
            blockers.append(blocker)

    value = opportunity.get("estimated_value_gbp")
    commercial = profile.get("commercial", {})
    if isinstance(value, (int, float)):
        min_value = commercial.get("preferred_min_value_gbp")
        max_value = commercial.get("preferred_max_value_gbp")
        if isinstance(min_value, (int, float)) and value < min_value:
            score -= 8
            review_reasons.append("Contract value below preferred range")
        if isinstance(max_value, (int, float)) and value > max_value:
            score -= 8
            review_reasons.append("Contract value above preferred range; inspect delivery scale")

    if not opportunity.get("source_url"):
        score -= 20
        review_reasons.append("Missing source URL / provenance")
    if not opportunity.get("deadline"):
        score -= 8
        review_reasons.append("Missing deadline")
    elif _deadline_passed(opportunity.get("deadline"), now):
        blockers.append("Deadline has passed")

    score = max(0, min(100, score))

    if blockers:
        decision = "NO_BID"
    elif score >= 65 and len(matched) >= 2:
        decision = "BID"
    elif score >= 40:
        decision = "REVIEW"
    else:
        decision = "NO_BID"

    evidence_record = {
        "source_url": opportunity.get("source_url"),
        "buyer": opportunity.get("buyer"),
        "notice_id": opportunity.get("notice_id"),
        "published_date": opportunity.get("published_date"),
        "deadline": opportunity.get("deadline"),
    }

    return TenderDecision(
        decision=decision,
        score=score,
        matched_capabilities=matched,
        blockers=blockers,
        review_reasons=review_reasons,
        evidence_record=evidence_record,
    )


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python tender_intelligence.py OPPORTUNITY.json CAPABILITIES.json")
        return 2

    opportunity = load_json(sys.argv[1])
    profile = load_json(sys.argv[2])
    result = score_opportunity(opportunity, profile)
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
