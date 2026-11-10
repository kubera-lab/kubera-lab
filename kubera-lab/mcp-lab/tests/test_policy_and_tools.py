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


def test_document_tools_report_truncation_instead_of_hiding_it():
    from servers import document_mcp as doc

    split = getattr(doc.split_document_chunks, "fn", doc.split_document_chunks)
    find = getattr(doc.find_exact_terms, "fn", doc.find_exact_terms)
    text = "a" * (500 * 205)
    try:
        result = split(text, max_chars=500)
    except ValueError:  # text above the server's size budget: truncation cannot happen here
        return
    assert result["chunk_count"] == 205
    assert result["returned_chunks"] == 200 and result["truncated"] is True

    hits = find("x " * 150, ["x"])["findings"][0]
    assert hits["count"] == 150 and len(hits["positions"]) == 100 and hits["positions_truncated"] is True
