import re
import sys
from pathlib import Path
from typing import Final

from analyzer import CodeAnalyzer
from diff_engine import DiffEngine
from git_utils import GitManager
from ollama_client import OllamaClient

# This script orchestrates the code review via Ollama.
# If the AI returns "LGTM", the script exits with code 0.
# If the AI rejects the code, it displays suggestions and a diff, exiting with code 1.


def extract_fixed_code(text: str) -> str | None:
    """Extracts the code and cleans potential markdown backticks."""
    pattern: Final[str] = r"\[FIXED_CODE\](.*?)\[/FIXED_CODE\]"
    match: re.Match[str] | None = re.search(pattern, text, re.DOTALL)
    if match:
        code: str = match.group(1).strip()
        code = re.sub(r"^```python\n|^```\n|```$", "", code, flags=re.MULTILINE)
        return code.strip()
    return None


def process_review(analyzer: CodeAnalyzer, filename: str, content: str) -> bool:
    """Analyzes a file and prints the feedback. Returns True on rejection."""
    review: str | None = analyzer.check_file(filename, content)

    if review and "REJECTED" in review.upper():
        print(f"\n\033[1m\033[91mREJECTED: {filename}\033[0m")

        parts: list[str] = review.split("[FIXED_CODE]")
        explanation: str = parts[0].replace("REJECTED:", "").strip()
        print(f"\033[93mReasons:\033[0m\n{explanation}")

        fixed_code: str | None = extract_fixed_code(review)
        if fixed_code:
            print(f"\n\033[1m\033[94m--- Suggested Diff for {filename} ---\033[0m")
            diff: str = DiffEngine.generate_colored_diff(content, fixed_code, filename)
            print(diff)
        else:
            print("\n\033[33m[!] AI failed to provide [FIXED_CODE] tags for a diff.\033[0m")
        return True

    print(f"\033[32m✓ {filename}: LGTM\033[0m")
    return False


def main() -> None:
    """Main orchestrator for the AI Code Reviewer."""
    # Strict path initialization using pathlib
    current_file_path: Final[Path] = Path(__file__).resolve()
    base_path: Final[Path] = current_file_path.parent.parent
    config_file: Final[Path] = base_path / "config" / "settings.yaml"
    prompt_file: Final[Path] = base_path / "config" / "system_prompt.txt"

    # Initialize Ollama Client
    client: Final[OllamaClient] = OllamaClient(str(config_file))

    # Connection check (for office/home portability)
    if not client.is_available():
        print("\033[93mOllama not found or offline; skipping AI review.\033[0m")
        sys.exit(0)

    # Load system prompt
    if not prompt_file.exists():
        print(f"Error: Prompt file not found at {prompt_file}")
        sys.exit(1)

    system_prompt: Final[str] = prompt_file.read_text(encoding="utf-8")
    analyzer: Final[CodeAnalyzer] = CodeAnalyzer(client, system_prompt)

    files_to_review: list[tuple[str, str]] = []

    # Case 1: Manual Mode (arguments passed to docker run)
    if len(sys.argv) > 1:
        print("--- Manual AI Review Mode ---")
        for file_arg in sys.argv[1:]:
            path: Path = Path("/repo") / file_arg
            if path.exists() and path.is_file():
                files_to_review.append((file_arg, path.read_text(encoding="utf-8")))
            else:
                print(f"\033[91mFile not found: {file_arg}\033[0m")

    # Case 2: Git Hook Mode (staged files)
    else:
        git: Final[GitManager] = GitManager()
        staged_files: list[str] = git.get_staged_files()
        if not staged_files:
            # No files staged, nothing to do
            sys.exit(0)

        print(f"--- Git Pre-commit AI Review ({len(staged_files)} files) ---")
        for f_name in staged_files:
            content: str | None = git.get_file_content(f_name)
            if content:
                files_to_review.append((f_name, content))

    # Execution of the reviews
    rejection_count: int = 0
    for f_name, f_content in files_to_review:
        is_rejected: bool = process_review(analyzer, f_name, f_content)
        if is_rejected:
            rejection_count += 1

    # Exit logic
    if rejection_count > 0:
        print(f"\n\033[91mFAILED: {rejection_count} file(s) did not pass the AI review.\033[0m")
        print("Use 'git commit --no-verify' to bypass if necessary.")
        sys.exit(1)

    print("\n\033[92mPASSED: All files are clean.\033[0m")
    sys.exit(0)


if __name__ == "__main__":
    main()
