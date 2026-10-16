from career_os.intelligence import analyze_job
from career_os.scoring import score_experiences


def test_profile_emphasis_prioritizes_relevant_evidence():
    documents = {
        "skills": {
            "skills": [
                {"id": "java", "name": "Java", "category": "backend"},
                {"id": "aws", "name": "AWS", "category": "cloud"},
            ]
        },
        "experience": {
            "experiences": [
                {"id": "older", "current": False, "skills": ["Java", "AWS"]},
                {"id": "current", "current": True, "skills": ["Java"]},
            ]
        },
        "target_profiles": {
            "platform": {
                "emphasis": {"primary": ["AWS"], "secondary": ["Java"]},
                "preferred_experience_order": ["current", "older"],
            }
        },
    }
    analysis = analyze_job(documents, "Need Java and AWS.")
    scores = score_experiences(documents, analysis, "platform")
    assert scores[0].experience_id == "older"
    assert scores[0].matched_skills == ("Java", "AWS")
    assert scores[0].score > scores[1].score
