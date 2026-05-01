import difflib


class DiffEngine:
    @staticmethod
    def generate_colored_diff(old_code: str, new_code: str, filename: str) -> str:
        old_lines: list[str] = old_code.splitlines(keepends=True)
        new_lines: list[str] = new_code.splitlines(keepends=True)

        diff = difflib.unified_diff(
            old_lines, new_lines, fromfile=f"a/{filename}", tofile=f"b/{filename}"
        )

        colored_diff: list[str] = []
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                colored_diff.append(f"\033[32m{line}\033[0m")  # Vert
            elif line.startswith("-") and not line.startswith("---"):
                colored_diff.append(f"\033[31m{line}\033[0m")  # Rouge
            elif line.startswith("^"):
                colored_diff.append(f"\033[36m{line}\033[0m")  # Cyan
            else:
                colored_diff.append(line)

        return "".join(colored_diff)
