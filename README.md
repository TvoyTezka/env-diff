# dotenv-diff

Compare dotenv files and find missing, extra, and empty variables.

## Install

Install from the repository:

```bash
python -m pip install git+https://github.com/bam0ny/dotenv-diff.git
```

For local development, install it in editable mode from the project directory:

```bash
python -m pip install -e ".[dev]"
```

## Usage

Compare the expected file with the actual file:

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

Show the installed version:

```bash
dotenv-diff --version
```

Create `.env.example` from `.env` with empty values:

```bash
dotenv-diff --init
```

When passing paths to `--init`, the order stays the same as comparison mode:
the example file comes first, then the actual file.

```bash
dotenv-diff --init .env.example .env
```

If `.env.example` already exists, use `--force` to overwrite it:

```bash
dotenv-diff --init --force
```

## Supported dotenv syntax

`dotenv-diff` supports common `.env` lines:

```dotenv
DATABASE_URL=postgres://localhost/app
EMPTY=
export DEBUG=true
SECRET="value # not a comment"
TOKEN='abc#123'
HOST=localhost # inline comment
```

Blank lines and full-line comments are ignored. Lines without `=` are treated
as parse errors so broken configuration fails loudly.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## License

MIT
