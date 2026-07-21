from __future__ import annotations

import os

from dotenv import load_dotenv


def test_dotenv_does_not_override_deployment_environment(tmp_path, monkeypatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("GROQ_API_KEY=local-key\nOPENAI_API_KEY=local-openai-key\n")
    monkeypatch.setenv("GROQ_API_KEY", "deployment-key")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    load_dotenv(env_file, override=False)

    assert os.environ["GROQ_API_KEY"] == "deployment-key"
    assert os.environ["OPENAI_API_KEY"] == "local-openai-key"
