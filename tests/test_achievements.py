from career_os.intelligence import analyze_job
from career_os.achievements import rank_achievements


def _career():
    return {
        "skills": {"skills": [
            {"name": "Java", "aliases": []},
            {"name": "AWS", "aliases": ["Amazon Web Services"]},
            {"name": "Kubernetes", "aliases": ["K8s"]},
        ]},
        "experience": {"experiences": [
            {"id": "acme", "skills": ["Java", "AWS"],
             "highlights": [
                 "Designed Java processing services on AWS.",
                 "Improved the developer onboarding experience.",
                 "Led Java code reviews.",
             ]},
        ]},
        "target_profiles": {"platform": {"emphasis": {"primary": ["AWS"], "secondary": ["Java"]}}},
    }


def test_ranks_real_highlights_by_explicit_job_relevance():
    career = _career()
    analysis = analyze_job(career, "Java, AWS and Kubernetes")
    ranked = rank_achievements(career, analysis, "platform")
    assert [item.highlight_index for item in ranked] == [0, 2]
    assert ranked[0].matched_requirements == ("Java", "AWS")
    assert ranked[0].score == 5
    assert ranked[0].text == career["experience"]["experiences"][0]["highlights"][0]


def test_parent_experience_skills_do_not_fabricate_highlight_evidence():
    career = _career()
    analysis = analyze_job(career, "Kubernetes")
    assert rank_achievements(career, analysis) == []


def test_empty_requirements_yield_no_ranked_achievements():
    career = _career()
    assert rank_achievements(career, analyze_job(career, "No relevant terms")) == []
