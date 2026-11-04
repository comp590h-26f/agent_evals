"""Exercise the verifier's independent checks with plausible summary outputs."""

import runpy
from pathlib import Path

import pytest

TASK = Path(__file__).resolve().parents[1] / "tasks/yewons_skill_article_summary"
ATTRIBUTION = "Source: Why Urban Trees Need Healthy Soil\nURL: https://example.org/urban-tree-soil"
BODY = "Urban trees need healthy soil so their roots can absorb water and oxygen."


@pytest.mark.parametrize(
    ("text", "expected_failures"),
    [
        (ATTRIBUTION + "\n\n" + BODY, set()),
        (BODY, {"attribution"}),
        ("Source: Wrong title\nURL: https://example.org/wrong\n\n" + BODY, {"attribution"}),
        (ATTRIBUTION + "\n\n" + ATTRIBUTION + "\n\n" + BODY, {"attribution"}),
        ("Preface\n\n" + ATTRIBUTION + "\n\n" + BODY, {"attribution", "paragraph"}),
        (ATTRIBUTION + "\n" + BODY, {"attribution"}),
        (ATTRIBUTION + "\n\n\n" + BODY, {"attribution"}),
        (ATTRIBUTION + "\n\n" + BODY + "\n\nAnother paragraph.", {"paragraph"}),
        (ATTRIBUTION + "\n\n- " + BODY, {"paragraph"}),
        (ATTRIBUTION + "\n\nBuses carry passengers through the city.", {"topic"}),
        (ATTRIBUTION + "\n\nSoil holds water.", {"topic"}),
        ("", {"exists", "attribution", "paragraph", "topic"}),
        (None, {"exists", "attribution", "paragraph", "topic"}),
    ],
)
def test_verifier_failures_are_independent(tmp_path, text, expected_failures):
    verifier = runpy.run_path(str(TASK / "tests/test_outputs.py"))
    summary_path = tmp_path / "summary.md"
    if text is not None:
        summary_path.write_text(text, encoding="utf-8")
    # The functions share the globals dictionary created by runpy.
    verifier["test_summary_exists_and_is_nonempty"].__globals__["SUMMARY_PATH"] = summary_path
    summary_text = verifier["summary_text"].__wrapped__()
    summary_body = verifier["summary_body"].__wrapped__(summary_text)
    checks = {
        "exists": (verifier["test_summary_exists_and_is_nonempty"], summary_text),
        "attribution": (verifier["test_exact_attribution_at_start_once"], summary_text),
        "paragraph": (verifier["test_body_is_one_paragraph"], summary_body),
        "topic": (verifier["test_body_covers_central_topic"], summary_body),
    }
    failures = set()
    for name, (check, value) in checks.items():
        try:
            check(value)
        except AssertionError:
            failures.add(name)
    assert failures == expected_failures
