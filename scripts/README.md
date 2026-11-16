# Profile automation

Two workflows keep new repositories from being forgotten and do the mechanical part of adding one.

## New repositories

`.github/workflows/new-repos.yml` runs every Monday and on demand. It lists the account's public repositories that are not forks, not archived and not linked from `README.md`, and keeps one open issue titled "Repositories missing from the profile page" up to date. It closes the issue when nothing is missing. Repositories that should stay off the page go in `scripts/ignore.txt`, one name per line.

## Draft a tool entry

`.github/workflows/draft-entry.yml` runs on demand with the repository name. It:

1. Clones the repository.
2. Reads the source for network and install behaviour (`audit.mjs`).
3. Runs the repository's own test script, if it has one.
4. Captures light and dark screenshots with external requests blocked (`shoot.py`, `frame.py`).
5. Inserts a draft featured entry into `README.md` and opens a draft pull request (`draft.py`).

Everything the scripts cannot know is written as `TODO` in the entry and listed in the pull request. That covers the main limit, the alt text and the Not checked column. A person replaces each one, or leaves the cell empty.

Run the tests and the audit locally with `node scripts/audit.mjs <repo-dir>`.

## Settings

- Actions must be enabled for the repository.
- Settings, Actions, General, Workflow permissions: allow read and write, and allow GitHub Actions to create pull requests.
- Issues must be enabled.
- Both workflows appear in the Actions tab once they are on the default branch.
