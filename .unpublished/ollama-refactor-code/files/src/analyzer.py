from ollama_client import OllamaClient


class CodeAnalyzer:
    def __init__(self, client: OllamaClient, system_prompt: str) -> None:
        self.client: OllamaClient = client
        self.system_prompt: str = system_prompt

    def check_file(self, filename: str, content: str) -> str | None:
        """Triggers analysis for supported file extensions."""
        if not filename.endswith((".py", ".php", ".sh")):
            return None

        return self.client.analyze_code(self.system_prompt, content)
