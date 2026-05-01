import sys
from typing import Any, Final

import requests
import yaml


class OllamaClient:
    def __init__(self, config_path: str) -> None:
        try:
            with open(config_path, encoding="utf-8") as f:
                self.config: Final[dict[str, Any]] = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

    def is_available(self) -> bool:
        """Checks if the Ollama service is reachable."""
        try:
            url: str = f"{self.config['ollama_url']}/api/tags"
            response: requests.Response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Connection check failed: {e}")
            return False

    def analyze_code(self, system_prompt: str, code_content: str) -> str:
        """Sends code to the LLM for analysis."""
        payload: Final[dict[str, Any]] = {
            "model": self.config["model"],
            "system": system_prompt,
            "prompt": f"Analyze this file content:\n\n{code_content}",
            "stream": False,
        }

        try:
            url: str = f"{self.config['ollama_url']}/api/generate"
            print(f"Sending request to Ollama (model: {self.config['model']})...")
            response: requests.Response = requests.post(
                url,
                json=payload,
                timeout=self.config["timeout"],
            )
            response.raise_for_status()
            result: dict[str, Any] = response.json()
            return str(result.get("response", ""))
        except Exception as e:
            return f"Error during AI analysis: {str(e)}"
