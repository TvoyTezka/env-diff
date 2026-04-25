from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv_diff.diff import EnvDiff, compare_envs
from dotenv_diff.parser import DotenvParseError, parse_dotenv_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dotenv-diff",
        description="Compare dotenv files and find missing, extra, and empty variables.",
    )
    parser.add_argument("example", type=Path, help="Expected dotenv file, for example .env.example")
    parser.add_argument("actual", type=Path, help="Actual dotenv file, for example .env")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 1 when any differences are found.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Print machine-readable JSON output.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        expected = parse_dotenv_file(args.example)
        actual = parse_dotenv_file(args.actual)
    except OSError as error:
        print(f"dotenv-diff: {error}", file=sys.stderr)
        return 2
    except DotenvParseError as error:
        print(f"dotenv-diff: {error}", file=sys.stderr)
        return 2

    diff = compare_envs(expected, actual)

    if args.json_output:
        print(json.dumps(diff.to_dict(), indent=2))
    else:
        print_diff(diff)

    if args.strict and diff.has_issues:
        return 1

    return 0


def print_diff(diff: EnvDiff) -> None:
    if not diff.has_issues:
        print("No differences found.")
        return

    sections = [
        ("Missing", diff.missing),
        ("Extra", diff.extra),
        ("Empty", diff.empty),
    ]
    first = True

    for title, values in sections:
        if not values:
            continue

        if not first:
            print()

        print(f"{title}:")
        for value in values:
            print(f"  {value}")

        first = False


if __name__ == "__main__":
    raise SystemExit(main())

