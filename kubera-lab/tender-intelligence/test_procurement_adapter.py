import unittest

from procurement_adapter import (
    build_contracts_finder_url,
    build_find_a_tender_url,
    deduplicate,
    evidence_record,
    normalize_package,
)


PACKAGE = {
    "releases": [
        {
            "ocid": "ocds-test-001",
            "id": "000001-2026",
            "date": "2026-09-09T10:00:00Z",
            "tag": ["tender"],
            "buyer": {"id": "GB-LA-MERTON"},
            "parties": [
                {"id": "GB-LA-MERTON", "name": "London Borough of Merton"}
            ],
            "tender": {
                "title": "AI assisted local service discovery pilot",
                "description": "SME-friendly discovery and prototype for a council digital service.",
                "value": {"amount": 85000, "currency": "GBP"},
                "tenderPeriod": {"endDate": "2026-10-01T12:00:00Z"},
                "eligibilityCriteria": "Supplier must demonstrate relevant digital delivery experience.",
                "procurementMethod": "selective",
                "items": [
                    {
                        "classification": {"id": "72262000"},
                        "deliveryAddresses": [{"region": "UKI63"}],
                    }
                ],
            },
        }
    ]
}


class ProcurementAdapterTests(unittest.TestCase):
    def test_find_a_tender_url_is_read_only_ocds(self):
        url = build_find_a_tender_url(updated_from="2026-09-01T00:00:00", limit=25)
        self.assertIn("ocdsReleasePackages", url)
        self.assertIn("updatedFrom=2026-09-01T00%3A00%3A00", url)
        self.assertIn("limit=25", url)

    def test_contracts_finder_url_is_read_only_ocds(self):
        url = build_contracts_finder_url(published_from="2026-09-01", limit=50)
        self.assertIn("Published/Notices/OCDS/Search", url)
        self.assertIn("publishedFrom=2026-09-01", url)
        self.assertIn("limit=50", url)

    def test_normalizes_ocds_into_tender_intelligence_shape(self):
        items = normalize_package(PACKAGE, source="find_a_tender", source_url="https://example.test/source")
        self.assertEqual(len(items), 1)
        opportunity = items[0]
        data = opportunity.as_tender_input()
        self.assertEqual(data["buyer"], "London Borough of Merton")
        self.assertEqual(data["estimated_value_gbp"], 85000.0)
        self.assertEqual(data["deadline"], "2026-10-01T12:00:00Z")
        self.assertIn("72262000", data["cpv_codes"])
        self.assertEqual(len(data["evidence_hash"]), 64)

    def test_non_gbp_value_is_not_mislabeled_as_gbp(self):
        package = {"releases": [dict(PACKAGE["releases"][0])]}
        package["releases"][0]["tender"] = dict(PACKAGE["releases"][0]["tender"])
        package["releases"][0]["tender"]["value"] = {"amount": 100000, "currency": "EUR"}
        item = normalize_package(package, source="contracts_finder", source_url="https://example.test")[0]
        self.assertIsNone(item.estimated_value_gbp)
        self.assertEqual(item.currency, "EUR")

    def test_non_gbp_value_is_not_mislabeled_as_gbp_without_currency(self):
        package = {"releases": [dict(PACKAGE["releases"][0])]}
        package["releases"][0]["tender"] = dict(PACKAGE["releases"][0]["tender"])
        package["releases"][0]["tender"]["value"] = {"amount": 100000}
        item = normalize_package(package, source="contracts_finder", source_url="https://example.test")[0]
        self.assertIsNone(item.estimated_value_gbp)
        self.assertIsNone(item.currency)

    def test_non_gbp_value_is_not_mislabeled_as_gbp_unrecognised_currency(self):
        package = {"releases": [dict(PACKAGE["releases"][0])]}
        package["releases"][0]["tender"] = dict(PACKAGE["releases"][0]["tender"])
        package["releases"][0]["tender"]["value"] = {"amount": 100000, "currency": "XYZ"}
        item = normalize_package(package, source="contracts_finder", source_url="https://example.test")[0]
        self.assertIsNone(item.estimated_value_gbp)
        self.assertEqual(item.currency, "XYZ")

    def test_evidence_record_is_minimal_and_traceable(self):
        item = normalize_package(PACKAGE, source="find_a_tender", source_url="https://example.test")[0]
        record = evidence_record(item)
        self.assertEqual(record["kind"], "uk_procurement_notice")
        self.assertEqual(record["ocid"], "ocds-test-001")
        self.assertIn("evidence_hash", record)
        self.assertNotIn("description", record)

    def test_deduplicate_prefers_single_ocid(self):
        first = normalize_package(PACKAGE, source="find_a_tender", source_url="https://a.test")[0]
        second = normalize_package(PACKAGE, source="find_a_tender", source_url="https://b.test")[0]
        result = deduplicate([first, second])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source_url, "https://b.test")


if __name__ == "__main__":
    unittest.main()
