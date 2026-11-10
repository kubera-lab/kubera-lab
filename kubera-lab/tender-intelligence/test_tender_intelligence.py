import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from tender_intelligence import score_opportunity

BEFORE_DEADLINES = datetime(2026, 9, 1, tzinfo=timezone.utc)  # fixtures use October 2026 deadlines


HERE = Path(__file__).resolve().parent


class TenderIntelligenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = json.loads((HERE / "capabilities.json").read_text(encoding="utf-8"))

    def test_good_ai_council_opportunity_is_bid(self):
        opportunity = json.loads((HERE / "example_opportunity.json").read_text(encoding="utf-8"))
        result = score_opportunity(opportunity, self.profile, now=BEFORE_DEADLINES)
        self.assertEqual(result.decision, "BID")
        self.assertGreaterEqual(result.score, 65)
        self.assertIn("ai", result.matched_capabilities)
        self.assertIn("automation", result.matched_capabilities)
        self.assertEqual(result.blockers, [])

    def test_closed_deadline_forces_no_bid(self):
        opportunity = json.loads((HERE / "example_opportunity.json").read_text(encoding="utf-8"))
        after = datetime(2026, 11, 10, tzinfo=timezone.utc)
        result = score_opportunity(opportunity, self.profile, now=after)
        self.assertEqual(result.decision, "NO_BID")
        self.assertIn("Deadline has passed", result.blockers)

    def test_hard_blocker_forces_no_bid(self):
        opportunity = {
            "notice_id": "BLOCK-1",
            "title": "AI platform",
            "buyer": "Example Public Body",
            "description": "AI automation project. Must hold ISO 27001 at submission.",
            "requirements": [],
            "tags": ["AI", "automation"],
            "estimated_value_gbp": 50000,
            "deadline": "2026-10-01",
            "source_url": "https://example.invalid/BLOCK-1"
        }
        result = score_opportunity(opportunity, self.profile)
        self.assertEqual(result.decision, "NO_BID")
        self.assertTrue(result.blockers)

    def test_missing_provenance_is_penalised(self):
        opportunity = {
            "notice_id": "NO-SOURCE",
            "title": "Website discovery",
            "buyer": "Example Council",
            "description": "SME website and accessibility discovery pilot",
            "requirements": [],
            "tags": ["website", "accessibility"],
            "estimated_value_gbp": 20000,
            "deadline": "2026-10-01"
        }
        result = score_opportunity(opportunity, self.profile)
        self.assertIn("Missing source URL / provenance", result.review_reasons)


if __name__ == "__main__":
    unittest.main()
