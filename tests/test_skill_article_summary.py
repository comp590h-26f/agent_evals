"""Exercise the verifier's independent checks with plausible summary outputs."""

import runpy
from pathlib import Path

import pytest

TASK = Path(__file__).resolve().parents[1] / "tasks/yewons_skill_article_summary"
ATTRIBUTION = "Source: Why Urban Trees Need Healthy Soil\nURL: https://example.org/urban-tree-soil"
BODY = "Urban trees need healthy soil so their roots can absorb water and oxygen."


@pytest.fixture
def verifier(tmp_path):
    checks = runpy.run_path(str(TASK / "tests/test_outputs.py"))
    # The functions share the globals dictionary created by runpy.
    checks["test_summary_exists_and_is_nonempty"].__globals__.update(
        SUMMARY_PATH=tmp_path / "summary.md",
        ARTICLE_PATH=tmp_path / "article.md",
    )
    (tmp_path / "article.md").write_bytes((TASK / "environment/article.md").read_bytes())
    return checks


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
def test_verifier_failures_are_independent(tmp_path, verifier, text, expected_failures):
    summary_path = tmp_path / "summary.md"
    if text is not None:
        summary_path.write_text(text, encoding="utf-8")
    verifier["test_source_article_is_unchanged"]()
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


@pytest.mark.parametrize("source_state", ["original", "modified", "missing"])
def test_valid_summary_requires_unchanged_source(tmp_path, verifier, source_state):
    (tmp_path / "summary.md").write_text(ATTRIBUTION + "\n\n" + BODY, encoding="utf-8")
    article_path = tmp_path / "article.md"
    if source_state == "modified":
        article_path.write_text("Replacement article.\n", encoding="utf-8")
    elif source_state == "missing":
        article_path.unlink()

    summary_text = verifier["summary_text"].__wrapped__()
    summary_body = verifier["summary_body"].__wrapped__(summary_text)
    verifier["test_summary_exists_and_is_nonempty"](summary_text)
    verifier["test_exact_attribution_at_start_once"](summary_text)
    verifier["test_body_is_one_paragraph"](summary_body)
    verifier["test_body_covers_central_topic"](summary_body)

    if source_state == "original":
        verifier["test_source_article_is_unchanged"]()
    else:
        with pytest.raises(AssertionError, match="/app/article.md"):
            verifier["test_source_article_is_unchanged"]()
