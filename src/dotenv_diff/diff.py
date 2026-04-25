from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EnvDiff:
    missing: list[str]
    extra: list[str]
    empty: list[str]

    @property
    def has_issues(self) -> bool:
        return bool(self.missing or self.extra or self.empty)

    def to_dict(self) -> dict[str, list[str]]:
        return {
            "missing": self.missing,
            "extra": self.extra,
            "empty": self.empty,
        }


def compare_envs(expected: dict[str, str], actual: dict[str, str]) -> EnvDiff:
    expected_keys = set(expected)
    actual_keys = set(actual)

    return EnvDiff(
        missing=sorted(expected_keys - actual_keys),
        extra=sorted(actual_keys - expected_keys),
        empty=sorted(key for key in expected_keys & actual_keys if actual[key] == ""),
    )

