import os
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "myApp v1.0.py"


def load_app_module():
    spec = importlib.util.spec_from_file_location("app", APP_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_process_command_url_map(monkeypatch):
    app = load_app_module()

    opened = {}

    def fake_open(url):
        opened["url"] = url
        return True

    monkeypatch.setattr(app.webbrowser, "open", fake_open)

    output, context = app.process_command("open google", [])

    assert "Opening open google" in output
    assert opened["url"] == "https://google.com"
    assert context[-1]["content"] == output


def test_ai_process_missing_key(monkeypatch):
    app = load_app_module()

    monkeypatch.setenv("GROQ_API_KEY", "")

    output = app.aiProcess("hello")
    assert "Missing GROQ_API_KEY" in output


def test_context_save_load(tmp_path):
    app = load_app_module()

    context = [{"role": "user", "content": "hello"}]
    file_path = tmp_path / "context.json"

    app.save_context_to_file(context, filename=file_path)
    loaded = app.load_context_from_file(filename=file_path)

    assert loaded == context
