import pytest

from dotenv_diff.parser import DotenvParseError, parse_dotenv


def test_parse_basic_dotenv_values():
    result = parse_dotenv(
        """
        # Comment
        DATABASE_URL=postgres://localhost/app
        EMPTY=
        export DEBUG=true
        """
    )

    assert result == {
        "DATABASE_URL": "postgres://localhost/app",
        "EMPTY": "",
        "DEBUG": "true",
    }


def test_parse_quoted_values_and_comments():
    result = parse_dotenv(
        """
        SECRET="value # not a comment"
        TOKEN='abc#123'
        HOST=localhost # comment
        """
    )

    assert result == {
        "SECRET": "value # not a comment",
        "TOKEN": "abc#123",
        "HOST": "localhost",
    }


def test_rejects_line_without_assignment():
    with pytest.raises(DotenvParseError):
        parse_dotenv("DATABASE_URL")

