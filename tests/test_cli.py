from dotenv_diff.cli import main


def test_version(capsys):
    try:
        main(["--version"])
    except SystemExit as error:
        assert error.code == 0

    assert "dotenv-diff 0.1.0" in capsys.readouterr().out


def test_init_creates_example_from_env(tmp_path, capsys):
    actual = tmp_path / ".env"
    example = tmp_path / ".env.example"
    actual.write_text(
        """
        DATABASE_URL=postgres://localhost/app
        SECRET="hidden value"
        EMPTY=
        """,
        encoding="utf-8",
    )

    exit_code = main(["--init", str(example), str(actual)])

    assert exit_code == 0
    assert example.read_text(encoding="utf-8") == "DATABASE_URL=\nSECRET=\nEMPTY=\n"
    assert f"Created {example} from {actual}." in capsys.readouterr().out


def test_init_uses_default_paths(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("DATABASE_URL=postgres\nSECRET=hidden\n", encoding="utf-8")

    exit_code = main(["--init"])

    assert exit_code == 0
    assert (tmp_path / ".env.example").read_text(encoding="utf-8") == "DATABASE_URL=\nSECRET=\n"


def test_init_does_not_overwrite_existing_example_without_force(tmp_path, capsys):
    actual = tmp_path / ".env"
    example = tmp_path / ".env.example"
    actual.write_text("DATABASE_URL=postgres\n", encoding="utf-8")
    example.write_text("EXISTING=\n", encoding="utf-8")

    exit_code = main(["--init", str(example), str(actual)])

    assert exit_code == 2
    assert example.read_text(encoding="utf-8") == "EXISTING=\n"
    assert "already exists; use --force to overwrite" in capsys.readouterr().err


def test_init_overwrites_existing_example_with_force(tmp_path):
    actual = tmp_path / ".env"
    example = tmp_path / ".env.example"
    actual.write_text("DATABASE_URL=postgres\n", encoding="utf-8")
    example.write_text("EXISTING=\n", encoding="utf-8")

    exit_code = main(["--init", "--force", str(example), str(actual)])

    assert exit_code == 0
    assert example.read_text(encoding="utf-8") == "DATABASE_URL=\n"
