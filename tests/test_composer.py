from career_os.composer import compose_targeted_resume


def _documents():
    return {
        "skills": {"skills": [
            {"name": "Java", "aliases": []},
            {"name": "AWS", "aliases": ["Amazon Web Services"]},
            {"name": "Kubernetes", "aliases": ["K8s"]},
        ]},
        "experience": {"experiences": [
            {"id": "one", "skills": ["Java", "AWS"], "highlights": [
                "Mentored junior engineers.",
                "Built Java services on AWS.",
                "Implemented Java code reviews.",
                "Improved onboarding documentation.",
            ]},
            {"id": "two", "skills": ["Java"], "highlights": ["Improved team processes."]},
        ]},
        "target_profiles": {"platform": {
            "emphasis": {"primary": ["AWS"], "secondary": ["Java"]},
        }},
    }


def test_composer_ranks_verified_highlights_and_preserves_source():
    source = _documents()
    result, report = compose_targeted_resume(
        source, "Java and Amazon Web Services and Kubernetes.", "platform", 2
    )
    assert result["experience"]["experiences"][0]["highlights"] == [
        "Built Java services on AWS.",
        "Implemented Java code reviews.",
    ]
    assert result["experience"]["experiences"][1]["highlights"] == ["Improved team processes."]
    assert source["experience"]["experiences"][0]["highlights"][0] == "Mentored junior engineers."
    assert report["missing_evidence"] == ["Kubernetes"]
    assert report["selection"][0]["selected_highlight_indices"] == [1, 2]
    assert report["selection"][1]["fallback"] is True


def test_composer_rejects_invalid_limit():
    import pytest
    with pytest.raises(ValueError):
        compose_targeted_resume(_documents(), "Java", max_highlights=0)


def test_composer_without_detected_requirements_keeps_existing_claims():
    source = _documents()
    result, report = compose_targeted_resume(source, "Unknown vacancy requirements.", max_highlights=2)
    assert result["experience"]["experiences"][0]["highlights"] == source["experience"]["experiences"][0]["highlights"][:2]
    assert report["detected_requirements"] == []
