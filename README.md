# dotenv-diff

Compare dotenv files and find missing, extra, and empty variables.

## Usage

```bash
dotenv-diff .env.example .env
```

Example output:

```text
Missing:
  DATABASE_URL
  JWT_SECRET

Extra:
  DEBUG_SQL

Empty:
  REDIS_URL
```

Use `--strict` in CI to return exit code `1` when differences are found:

```bash
dotenv-diff .env.example .env --strict
```

Use `--json` for machine-readable output:

```bash
dotenv-diff .env.example .env --json
```

Create `.env.example` from `.env` with empty values:

```bash
dotenv-diff --init
```

If `.env.example` already exists, use `--force` to overwrite it:

```bash
dotenv-diff --init --force
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## License

MIT
