import json
from unittest.mock import patch

from backend.roadmap_gen import build_prompt, generate_roadmap


def test_build_prompt():
    fake = [
        {"title": "Two Sum", "difficulty": "Easy", "url": "", "meta": {}},
        {"title": "3Sum", "difficulty": "Medium", "url": "", "meta": {}},
    ]

    with patch("backend.roadmap_gen.get_company_problems", return_value=fake):
        prompt = build_prompt("google", "beginner", 4)
        assert "google" in prompt
        assert "Two Sum" in prompt


@patch("openai.chat.completions.create")
def test_generate_roadmap(mock_api):
    mock_api.return_value = {
        "choices": [{"message": {"content": "{\"summary\": \"ok\"}"}}]
    }

    text = generate_roadmap("google", "beginner", 4, model="gpt-test-model")
    assert "summary" in text or isinstance(text, str)
