from __future__ import annotations

import pytest

from shared.policy import (
    ApprovalReceipt,
    SideEffect,
    ToolPolicy,
    canonical_hash,
    enforce_tool_policy,
    require_allowed_url,
    validate_identifier,
)


def test_canonical_hash_is_stable_for_key_order() -> None:
    assert canonical_hash({"b": 2, "a": 1}) == canonical_hash({"a": 1, "b": 2})


def test_identifier_validation_rejects_spaces_and_shell_characters() -> None:
    assert validate_identifier("dataset-123", field="dataset") == "dataset-123"
    with pytest.raises(ValueError):
        validate_identifier("bad value;rm", field="dataset")


def test_url_allowlist_is_https_and_exact_host() -> None:
    good = "https://api.beta.ons.gov.uk/v1/datasets"
    assert require_allowed_url(good, ["api.beta.ons.gov.uk"]) == good
    with pytest.raises(ValueError):
        require_allowed_url("http://api.beta.ons.gov.uk/v1/datasets", ["api.beta.ons.gov.uk"])
    with pytest.raises(ValueError):
        require_allowed_url("https://evil.example/v1/datasets", ["api.beta.ons.gov.uk"])


def test_read_only_policy_does_not_require_approval() -> None:
    policy = ToolPolicy("ons", "fetch", SideEffect.READ_ONLY, ("api.beta.ons.gov.uk",))
    enforce_tool_policy(policy, target_url="https://api.beta.ons.gov.uk/v1/datasets")


def test_write_policy_requires_matching_approval() -> None:
    policy = ToolPolicy("business", "create_booking", SideEffect.WRITE_REQUIRES_APPROVAL)
    with pytest.raises(PermissionError):
        enforce_tool_policy(policy)

    wrong = ApprovalReceipt("a1", "send_message", True, "n1")
    with pytest.raises(PermissionError):
        enforce_tool_policy(policy, approval=wrong)

    correct = ApprovalReceipt("a1", "create_booking", True, "n2")
    enforce_tool_policy(policy, approval=correct)


def test_prohibited_tool_is_always_denied() -> None:
    policy = ToolPolicy("unsafe", "arbitrary_exec", SideEffect.PROHIBITED)
    with pytest.raises(PermissionError):
        enforce_tool_policy(policy)


def test_input_budget_is_enforced() -> None:
    policy = ToolPolicy("evidence", "hash", SideEffect.PREPARE_ONLY, max_input_chars=5)
    with pytest.raises(ValueError):
        enforce_tool_policy(policy, input_text="123456")


def _doc_tools():
    from servers import document_mcp as doc

    split = getattr(doc.split_document_chunks, "fn", doc.split_document_chunks)
    find = getattr(doc.find_exact_terms, "fn", doc.find_exact_terms)
    return split, find


@pytest.mark.parametrize("chunks", [1, 199, 200])
def test_split_document_chunks_not_truncated_up_to_200(chunks):
    split, _ = _doc_tools()
    text = "".join(chr(97 + i % 26) * 500 for i in range(chunks))
    result = split(text, max_chars=500)
    assert result["chunk_count"] == chunks
    assert result["returned_chunks"] == chunks
    assert result["truncated"] is False
    assert "".join(result["chunks"]) == text  # nothing lost


@pytest.mark.parametrize("chunks", [201, 400])
def test_split_document_chunks_reports_truncation_above_200(chunks):
    split, _ = _doc_tools()
    text = "".join(chr(97 + i % 26) * 500 for i in range(chunks))
    assert len(text) <= 200_000  # stays inside the server size budget, so truncation (not the budget) is tested
    result = split(text, max_chars=500)
    assert result["chunk_count"] == chunks
    assert result["returned_chunks"] == 200
    assert len(result["chunks"]) == 200
    assert result["truncated"] is True
    assert "".join(result["chunks"]) == text[: 200 * 500]  # the returned part is exact; the rest is flagged, not hidden


def test_split_document_chunks_rejects_text_over_budget():
    split, _ = _doc_tools()
    with pytest.raises(ValueError):
        split("a" * 200_001, max_chars=500)


@pytest.mark.parametrize("occurrences, truncated", [(1, False), (100, False), (101, True), (150, True)])
def test_find_exact_terms_full_count_and_truncation_flag(occurrences, truncated):
    _, find = _doc_tools()
    hit = find("x " * occurrences, ["x"])["findings"][0]
    assert hit["count"] == occurrences
    assert len(hit["positions"]) == min(occurrences, 100)
    assert hit["positions_truncated"] is truncated
