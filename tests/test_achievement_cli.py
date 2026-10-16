import json

from career_os.cli import analyze_job_command


def test_analyze_job_cli_achievement_json(tmp_path, monkeypatch, capsys):
    from career_os import cli
    documents = {
        "skills": {"skills": [{"name": "Java", "aliases": []}]},
        "experience": {"experiences": [{"id": "acme", "skills": ["Java"], "highlights": ["Built Java services."]}]},
        "target_profiles": {"platform": {"emphasis": {"primary": ["Java"]}}},
    }
    monkeypatch.setattr(cli, "_load_validated", lambda root: (documents, []))
    vacancy = tmp_path / "vacancy.txt"
    vacancy.write_text("Java required.", encoding="utf-8")
    assert analyze_job_command(tmp_path, vacancy, True, "platform", True) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["achievements"][0]["score"] == 3
    assert payload["achievements"][0]["text"] == "Built Java services."


def test_analyze_job_cli_unknown_profile(tmp_path, monkeypatch, capsys):
    from career_os import cli
    monkeypatch.setattr(cli, "_load_validated", lambda root: ({"target_profiles": {}}, []))
    vacancy = tmp_path / "vacancy.txt"
    vacancy.write_text("Java", encoding="utf-8")
    assert analyze_job_command(tmp_path, vacancy, False, "missing", True) == 2
    assert "Unknown target profile" in capsys.readouterr().err
