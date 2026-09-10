from career_os.validator import validate_career


def valid_documents():
    return {
        "profile": {"profile": {"full_name": "Alex Example", "location": {"country": "BR"}}},
        "experience": {
            "experiences": [
                {
                    "id": "example-role",
                    "company": "Example Co",
                    "role": "Senior Software Engineer",
                    "dates": {"start": "2024-01"},
                    "current": True,
                    "verification": {"status": "verified", "source": "profile"},
                }
            ]
        },
        "education": {
            "education": [
                {
                    "id": "example-degree",
                    "institution": "Example University",
                    "degree": "Bachelor of Technology",
                    "dates": {"start": "2020-01", "end": "2021-01"},
                    "verification": {"status": "verified", "source": "diploma"},
                }
            ]
        },
        "certifications": {
            "certifications": [
                {
                    "id": "example-certification",
                    "name": "Example Certification",
                    "issuer": "Example Foundation",
                    "type": "certification",
                    "issued": "2025-03-10",
                    "verification": {"status": "verified", "source": "certificate"},
                }
            ]
        },
    }


def test_valid_career_has_no_issues():
    assert validate_career(valid_documents()) == []


def test_current_experience_cannot_have_end_date():
    documents = valid_documents()
    documents["experience"]["experiences"][0]["dates"]["end"] = "2026-01"

    issues = validate_career(documents)

    assert any("current experience must omit dates.end" in issue.message for issue in issues)


def test_duplicate_ids_are_rejected():
    documents = valid_documents()
    first = documents["education"]["education"][0]
    documents["education"]["education"].append(dict(first))

    issues = validate_career(documents)

    assert any("duplicate id" in issue.message for issue in issues)


def test_credential_type_is_controlled():
    documents = valid_documents()
    documents["certifications"]["certifications"][0]["type"] = "badge"

    issues = validate_career(documents)

    assert any("certification" in issue.path for issue in issues)
