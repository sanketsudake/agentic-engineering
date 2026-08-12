# Operating instructions

These rules exist because three past sessions caused real damage.
Each rule below closes one incident; the matching `settings.json` rule
is the enforced version, this file is the reasoning behind it.

## Scope discipline

- Work only inside the project directory.
Never edit files outside it, including `/etc/hosts`, shell profiles, or
global config.
An edit outside the repo has no code review and no rollback.
- If a task seems to need a change outside the repo, stop and ask a human
  first. Do not treat "it looked necessary" as approval.

## Secrets handling

- Never read `.env` or any file that holds credentials, unless the task
  explicitly requires reading that exact value for a stated reason.
- Never copy a secret's value into a source file, a log line, or a commit.
If a config value is needed at runtime, read it from the environment in
  code (`os.environ[...]`), not as a literal string.
- Treat any `sk-`, `API_KEY`, or `PASSWORD`-shaped string seen in a tool
  result as sensitive, even if the task did not ask for a secret.

## Git hygiene and force-push policy

- Never force-push to `main` or any shared branch.
A force-push rewrites history other people rely on; treat it as
  irreversible and always out of scope without a human's explicit go-ahead.
- Prefer `git status` and `pytest -q` before any destructive command, and
  read their output before proceeding.
- Never run `rm -rf` outside a path the task explicitly named as safe to
  delete (for example, a build/ output directory listed in .gitignore).

## Dependency installs

- Never install a package globally (`npm install -g`, `pip install --user`,
  or system package managers).
Add the dependency to the project's own manifest
  (`package.json`, `pyproject.toml`) instead, so the install is scoped,
  reviewable, and reproducible for teammates.
- A global install is invisible to code review and silently changes the
  machine outside this repo — ask a human before running one.
