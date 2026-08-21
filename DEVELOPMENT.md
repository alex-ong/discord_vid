# Development

Steps to set up a local development environment for `discord_vid`.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed
- Python 3.9 (uv can install this for you, see below)

## Setup

1. Clone the repo and `cd` into it.
2. Install Python 3.9 and pin it for this project:
   ```
   uv python install 3.9
   uv python pin 3.9
   ```
3. Install dependencies (creates `.venv` and installs from `uv.lock`):
   ```
   uv sync
   ```
4. Install the git pre-commit hook (runs `ruff format` on every commit):
   ```
   uv run pre-commit install
   ```

## Running the app

```
uv run python main.py 25MB_720p30 some_file.mp4
```

## Formatting / linting

```
uv run ruff format .
```

You can also run all pre-commit hooks manually against every file:
```
uv run pre-commit run --all-files
```

## Building the executable

Builds the app with PyInstaller using [main.spec](main.spec):
```
build.bat
```

## Managing dependencies

- Add a runtime dependency: `uv add <package>`
- Add a dev-only dependency: `uv add --dev <package>`
- Upgrade the lockfile: `uv lock --upgrade`
