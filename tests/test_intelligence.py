from career_os.intelligence import analyze_job, extract_skill_requirements


def _documents():
    return {
        "skills": {
            "skills": [
                {"id": "java", "name": "Java", "category": "backend", "aliases": []},
                {"id": "aws", "name": "AWS", "category": "cloud", "aliases": ["Amazon Web Services"]},
                {"id": "kubernetes", "name": "Kubernetes", "category": "platform", "aliases": ["K8s"]},
            ]
        },
        "experience": {
            "experiences": [
                {"id": "acme", "skills": ["Java", "AWS"]},
            ]
        },
    }


def test_extracts_canonical_skills_and_aliases():
    found = extract_skill_requirements(
        _documents(),
        "We need Java, Amazon Web Services and K8s experience.",
    )
    assert found == ["Java", "AWS", "Kubernetes"]


def test_analysis_separates_evidence_from_missing_requirements():
    analysis = analyze_job(
        _documents(),
        "Senior role using Java, AWS and Kubernetes.",
    )
    assert analysis.coverage == 2 / 3
    assert [item.skill for item in analysis.matched] == ["Java", "AWS"]
    assert [item.skill for item in analysis.missing] == ["Kubernetes"]
    assert analysis.matched[0].evidence_experience_ids == ("acme",)


def test_multiword_alias_does_not_match_inside_another_word():
    docs = _documents()
    assert extract_skill_requirements(docs, "Amazon Web ServicesNow is not a skill.") == []
    assert extract_skill_requirements(docs, "Experience with Amazon Web Services.") == ["AWS"]


def test_sentence_final_punctuation_does_not_hide_requirements():
    assert extract_skill_requirements(_documents(), "Java, AWS and Kubernetes.") == [
        "Java", "AWS", "Kubernetes"
    ]
