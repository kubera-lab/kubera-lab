from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Iterable


FIND_A_TENDER_OCDS = "https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages"
CONTRACTS_FINDER_OCDS = "https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search"
USER_AGENT = "KUBERA-Tender-Intelligence/1.0 (+https://github.com/kubera-lab/kubera-lab)"


@dataclass(frozen=True)
class NormalizedOpportunity:
    source: str
    source_url: str
    notice_id: str | None
    ocid: str | None
    title: str
    description: str
    buyer: str
    published_date: str | None
    deadline: str | None
    estimated_value_gbp: float | None
    currency: str | None
    requirements: list[str]
    tags: list[str]
    cpv_codes: list[str]
    locations: list[str]
    raw_release_id: str | None
    evidence_hash: str
    retrieved_at: str

    def as_tender_input(self) -> dict[str, Any]:
        """Return the stable shape expected by tender_intelligence.score_opportunity."""
        data = asdict(self)
        return {
            "source": data["source"],
            "source_url": data["source_url"],
            "notice_id": data["notice_id"],
            "ocid": data["ocid"],
            "title": data["title"],
            "description": data["description"],
            "buyer": data["buyer"],
            "published_date": data["published_date"],
            "deadline": data["deadline"],
            "estimated_value_gbp": data["estimated_value_gbp"],
            "currency": data["currency"],
            "requirements": data["requirements"],
            "tags": data["tags"],
            "cpv_codes": data["cpv_codes"],
            "locations": data["locations"],
            "raw_release_id": data["raw_release_id"],
            "evidence_hash": data["evidence_hash"],
            "retrieved_at": data["retrieved_at"],
        }


def _http_get_json(url: str, timeout: int = 30) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return json.loads(response.read().decode(charset))


def build_find_a_tender_url(
    *,
    updated_from: str | None = None,
    updated_to: str | None = None,
    stages: Iterable[str] = ("planning", "tender"),
    limit: int = 100,
    cursor: str | None = None,
) -> str:
    if not 1 <= limit <= 100:
        raise ValueError("Find a Tender limit must be between 1 and 100")
    params: dict[str, Any] = {"limit": limit, "stages": ",".join(stages)}
    if updated_from:
        params["updatedFrom"] = updated_from
    if updated_to:
        params["updatedTo"] = updated_to
    if cursor:
        params["cursor"] = cursor
    return f"{FIND_A_TENDER_OCDS}?{urllib.parse.urlencode(params)}"


def build_contracts_finder_url(
    *,
    published_from: str | None = None,
    published_to: str | None = None,
    stages: Iterable[str] = ("planning", "tender"),
    limit: int = 100,
    cursor: str | None = None,
) -> str:
    if limit < 1:
        raise ValueError("Contracts Finder limit must be positive")
    params: dict[str, Any] = {"limit": limit, "stages": ",".join(stages)}
    if published_from:
        params["publishedFrom"] = published_from
    if published_to:
        params["publishedTo"] = published_to
    if cursor:
        params["cursor"] = cursor
    return f"{CONTRACTS_FINDER_OCDS}?{urllib.parse.urlencode(params)}"


def fetch_find_a_tender(**kwargs: Any) -> tuple[dict[str, Any], str]:
    url = build_find_a_tender_url(**kwargs)
    return _http_get_json(url), url


def fetch_contracts_finder(**kwargs: Any) -> tuple[dict[str, Any], str]:
    url = build_contracts_finder_url(**kwargs)
    return _http_get_json(url), url


def _party_name(release: dict[str, Any], party_id: str | None) -> str:
    if not party_id:
        return ""
    for party in release.get("parties", []) or []:
        if party.get("id") == party_id:
            return str(party.get("name") or "")
    return ""


def _buyer_name(release: dict[str, Any]) -> str:
    buyer = release.get("buyer") or {}
    return str(buyer.get("name") or _party_name(release, buyer.get("id")) or "")


def _value(tender: dict[str, Any]) -> tuple[float | None, str | None]:
    value = tender.get("value") or {}
    amount = value.get("amount")
    currency = value.get("currency")
    try:
        parsed = float(amount) if amount is not None else None
    except (TypeError, ValueError):
        parsed = None
    return parsed, str(currency) if currency else None


def _items(release: dict[str, Any]) -> tuple[list[str], list[str]]:
    cpv_codes: list[str] = []
    locations: list[str] = []
    for item in release.get("tender", {}).get("items", []) or []:
        classification = item.get("classification") or {}
        code = classification.get("id")
        if code:
            cpv_codes.append(str(code))
        for additional in item.get("additionalClassifications", []) or []:
            code = additional.get("id")
            if code:
                cpv_codes.append(str(code))
        for address in item.get("deliveryAddresses", []) or []:
            region = address.get("region") or address.get("postalCode") or address.get("locality")
            if region:
                locations.append(str(region))
    return sorted(set(cpv_codes)), sorted(set(locations))


def _requirements(release: dict[str, Any]) -> list[str]:
    tender = release.get("tender") or {}
    fields = [
        tender.get("eligibilityCriteria"),
        tender.get("awardCriteriaDetails"),
        tender.get("submissionMethodDetails"),
    ]
    techniques = tender.get("techniques") or {}
    if techniques:
        fields.append(json.dumps(techniques, sort_keys=True, ensure_ascii=False))
    return [str(value).strip() for value in fields if value]


def _tags(release: dict[str, Any]) -> list[str]:
    tender = release.get("tender") or {}
    values = [release.get("tag"), tender.get("procurementMethod"), tender.get("procurementMethodDetails")]
    return [str(v) for v in values if v]


def _canonical_hash(release: dict[str, Any]) -> str:
    encoded = json.dumps(release, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def normalize_release(release: dict[str, Any], *, source: str, source_url: str) -> NormalizedOpportunity:
    tender = release.get("tender") or {}
    amount, currency = _value(tender)
    cpv_codes, locations = _items(release)
    retrieved_at = datetime.now(timezone.utc).isoformat()

    notice_id = None
    for candidate in (release.get("id"), tender.get("id")):
        if candidate:
            notice_id = str(candidate)
            break

    return NormalizedOpportunity(
        source=source,
        source_url=source_url,
        notice_id=notice_id,
        ocid=str(release.get("ocid")) if release.get("ocid") else None,
        title=str(tender.get("title") or release.get("language") or "Untitled procurement opportunity"),
        description=str(tender.get("description") or ""),
        buyer=_buyer_name(release),
        published_date=str(release.get("date")) if release.get("date") else None,
        deadline=str(tender.get("tenderPeriod", {}).get("endDate")) if tender.get("tenderPeriod", {}).get("endDate") else None,
        estimated_value_gbp=amount if currency == "GBP" else None,
        currency=currency,
        requirements=_requirements(release),
        tags=_tags(release),
        cpv_codes=cpv_codes,
        locations=locations,
        raw_release_id=str(release.get("id")) if release.get("id") else None,
        evidence_hash=_canonical_hash(release),
        retrieved_at=retrieved_at,
    )


def normalize_package(package: dict[str, Any], *, source: str, source_url: str) -> list[NormalizedOpportunity]:
    releases = package.get("releases") or []
    if not isinstance(releases, list):
        raise ValueError("Expected OCDS package field 'releases' to be a list")
    return [normalize_release(release, source=source, source_url=source_url) for release in releases]


def deduplicate(opportunities: Iterable[NormalizedOpportunity]) -> list[NormalizedOpportunity]:
    """Prefer OCID identity, then notice ID, then evidence hash."""
    chosen: dict[str, NormalizedOpportunity] = {}
    for opportunity in opportunities:
        key = opportunity.ocid or opportunity.notice_id or opportunity.evidence_hash
        chosen[key] = opportunity
    return list(chosen.values())


def evidence_record(opportunity: NormalizedOpportunity) -> dict[str, Any]:
    """Ledger-ready, privacy-minimal procurement provenance record."""
    return {
        "kind": "uk_procurement_notice",
        "source": opportunity.source,
        "source_url": opportunity.source_url,
        "notice_id": opportunity.notice_id,
        "ocid": opportunity.ocid,
        "published_date": opportunity.published_date,
        "deadline": opportunity.deadline,
        "buyer": opportunity.buyer,
        "evidence_hash": opportunity.evidence_hash,
        "retrieved_at": opportunity.retrieved_at,
    }
