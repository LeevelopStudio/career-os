from career_os.validator import validate_career

def valid_documents():
    return {
        "profile":{"profile":{"full_name":"Alex Example","location":{"country":"BR"}}},
        "experience":{"experiences":[{"id":"example-role","company":"Example Co","role":"Senior Software Engineer","dates":{"start":"2024-01"},"current":True,"skills":["Java","Distributed Systems","AWS"],"verification":{"status":"verified","source":"profile"}}]},
        "education":{"education":[{"id":"example-degree","institution":"Example University","degree":"Bachelor of Technology","dates":{"start":"2020-01","end":"2021-01"},"verification":{"status":"verified","source":"diploma"}}]},
        "certifications":{"certifications":[{"id":"example-certification","name":"Example Certification","issuer":"Example Foundation","type":"certification","issued":"2025-03-10","verification":{"status":"verified","source":"certificate"}}]},
        "skills":{"skills":[{"id":"java","name":"Java","category":"backend"},{"id":"distributed-systems","name":"Distributed Systems","category":"architecture"},{"id":"aws","name":"AWS","category":"cloud"}]},
        "languages":{"languages":[]},
        "target_profiles":{"senior":{"id":"senior","preferred_experience_order":["example-role"]}},
    }

def test_valid_career_has_no_issues(): assert validate_career(valid_documents()) == []

def test_current_experience_cannot_have_end_date():
    d=valid_documents(); d["experience"]["experiences"][0]["dates"]["end"]="2026-01"
    assert any("current experience must omit dates.end" in i.message for i in validate_career(d))

def test_duplicate_ids_are_rejected():
    d=valid_documents(); first=d["education"]["education"][0]; d["education"]["education"].append(dict(first))
    assert any("duplicate id" in i.message for i in validate_career(d))

def test_credential_type_is_controlled():
    d=valid_documents(); d["certifications"]["certifications"][0]["type"]="badge"
    assert any("certification" in i.path for i in validate_career(d))

def test_experience_skills_cannot_have_duplicates():
    d=valid_documents(); d["experience"]["experiences"][0]["skills"]=["Java","Java"]
    assert any("duplicates" in i.message for i in validate_career(d))

def test_experience_skills_cannot_be_empty():
    d=valid_documents(); d["experience"]["experiences"][0]["skills"]=["Java","  "]
    assert any("empty strings" in i.message for i in validate_career(d))

def test_unknown_skill_is_rejected():
    d=valid_documents(); d["experience"]["experiences"][0]["skills"].append("Kotlin")
    assert any("unknown canonical skill 'Kotlin'" in i.message for i in validate_career(d))

def test_unknown_preferred_experience_is_rejected():
    d=valid_documents(); d["target_profiles"]["senior"]["preferred_experience_order"].append("missing")
    assert any("unknown experience id 'missing'" in i.message for i in validate_career(d))
