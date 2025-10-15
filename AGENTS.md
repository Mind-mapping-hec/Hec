AGENTS.md
===========

Purpose
-------

This file documents the automated agents, bots, or service accounts used by the Mind Map Mini project and provides a template and guidelines for adding new agents.

When to add an agent
--------------------

- You have an automated process that performs repository operations (CI, formatting, deployment, backups).
- You want to run scheduled tasks that operate on project files.
- A third-party integration or service requires a dedicated, auditable identity.

Agent fields (recommended)
---------------------------

When you add an agent to this project, include at least the following information in the repository (for example, in this file or in a dedicated team doc):

- Name: short descriptive name (e.g. `format-bot`, `backup-agent`).
- Purpose: one-sentence summary of what it does.
- Owner / Contact: GitHub username or email of the person/team responsible.
- Entrypoint: path to the script, workflow, or service that runs the agent (e.g. `.github/workflows/ci.yml`, `scripts/backup.py`).
- Triggers: how the agent runs (push, schedule, manual, webhook).
- Scopes / Permissions: what the agent needs access to (repo read/write, deploy keys, cloud credentials). Prefer least privilege.
- Secrets / Config: environment variables, secret names (do NOT store secrets in this repo). Reference where secrets are stored (GitHub Actions secrets, vault, etc.).

Agent template
---------------

Copy and fill this template when registering a new agent:

```
Name: <short-name>
Purpose: <one-line description>
Owner: <github-user or team>
Entrypoint: <file path or workflow>
Triggers: <push|schedule|manual|webhook>
Permissions: <e.g., contents: read, actions: write>
Secrets: <list of secret names referenced>
Notes: <any additional info, rate limits, external services>
```

Example
-------

```
Name: autosave-pruner
Purpose: remove autosave files older than 90 days from the `autosave/` folder and commit an index update
Owner: @maintainer-team
Entrypoint: scripts/prune_autosaves.py
Triggers: schedule (daily)
Permissions: repo contents: write
Secrets: None
Notes: This script runs in GitHub Actions and uses a checkout token provided by the runner.
```

Security & best practices
-------------------------

- Keep secrets out of the repository. Use GitHub Actions secrets, environment vaults, or a secrets manager.
- Use least privilege for access tokens and service accounts.
- Document any scheduled agents and include revert/rollback instructions in case of faulty runs.
- Prefer idempotent agents that can be re-run safely.

Where to put agent code
------------------------

- Small helper scripts: `scripts/` or `tools/`
- Scheduled or CI workflows: `.github/workflows/`
- Long-running services: document in `AGENTS.md` and keep runtime configuration separate from code.

Keeping this file up to date
---------------------------

If you add, modify, or remove an agent, update this file with the new entry, the owner contact, and any changes to scopes or secrets.

Acknowledgements
----------------

This project prefers transparency for automated access. If you have questions about an agent or need to request access for a new one, open an issue or contact the repository owner.
