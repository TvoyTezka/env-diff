from __future__ import annotations

from pathlib import Path


class DotenvParseError(ValueError):
    """Raised when a dotenv line cannot be parsed."""


def parse_dotenv_file(path: str | Path) -> dict[str, str]:
    return parse_dotenv(Path(path).read_text(encoding="utf-8"), source=str(path))


def parse_dotenv(content: str, source: str = "<string>") -> dict[str, str]:
    values: dict[str, str] = {}

    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("export "):
            line = line[len("export ") :].lstrip()

        if "=" not in line:
            raise DotenvParseError(f"{source}:{line_number}: expected KEY=VALUE")

        key, value = line.split("=", 1)
        key = key.strip()

        if not key:
            raise DotenvParseError(f"{source}:{line_number}: empty variable name")

        if any(char.isspace() for char in key):
            raise DotenvParseError(f"{source}:{line_number}: variable name contains whitespace")

        values[key] = _clean_value(value.strip())

    return values


def _clean_value(value: str) -> str:
    if not value:
        return ""

    quote = value[0]
    if quote in ("'", '"'):
        return _read_quoted_value(value, quote)

    return _strip_inline_comment(value).strip()


def _read_quoted_value(value: str, quote: str) -> str:
    result: list[str] = []
    escaped = False

    for char in value[1:]:
        if escaped:
            result.append(char)
            escaped = False
            continue

        if char == "\\" and quote == '"':
            escaped = True
            continue

        if char == quote:
            break

        result.append(char)

    return "".join(result)


def _strip_inline_comment(value: str) -> str:
    for index, char in enumerate(value):
        if char == "#" and (index == 0 or value[index - 1].isspace()):
            return value[:index]

    return value

