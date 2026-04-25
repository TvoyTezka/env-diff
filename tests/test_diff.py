from dotenv_diff.diff import compare_envs


def test_compare_envs():
    diff = compare_envs(
        expected={"DATABASE_URL": "", "JWT_SECRET": "", "REDIS_URL": ""},
        actual={"DATABASE_URL": "postgres://localhost/app", "DEBUG_SQL": "true", "REDIS_URL": ""},
    )

    assert diff.missing == ["JWT_SECRET"]
    assert diff.extra == ["DEBUG_SQL"]
    assert diff.empty == ["REDIS_URL"]
    assert diff.has_issues is True


def test_compare_envs_without_issues():
    diff = compare_envs(expected={"DATABASE_URL": ""}, actual={"DATABASE_URL": "postgres"})

    assert diff.to_dict() == {
        "missing": [],
        "extra": [],
        "empty": [],
    }
    assert diff.has_issues is False

