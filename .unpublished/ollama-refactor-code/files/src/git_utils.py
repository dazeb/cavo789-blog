import subprocess
from typing import Final


class GitManager:
    @staticmethod
    def setup_safe_directory() -> None:
        """Ensures the repository is recognized as safe by Git in the container."""
        subprocess.run(
            ["git", "config", "--global", "--add", "safe.directory", "/repo"], check=False
        )

    @staticmethod
    def get_staged_files() -> list[str]:
        """Returns the list of files currently in the Git staging area."""
        GitManager.setup_safe_directory()
        result: Final[subprocess.CompletedProcess[str]] = subprocess.run(
            ["git", "-C", "/repo", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=False,
        )
        files: list[str] = result.stdout.strip().split("\n")
        return [f for f in files if f]

    @staticmethod
    def get_file_content(filename: str) -> str:
        """Retrieves the content of a file from the staging area."""
        result: Final[subprocess.CompletedProcess[str]] = subprocess.run(
            ["git", "-C", "/repo", "show", f":{filename}"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout
