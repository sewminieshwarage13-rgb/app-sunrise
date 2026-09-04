# Git and GitHub Workflow

## Local repository workflow

The project is prepared for a local Git repository with `.gitignore` excluding generated build output. The recommended progression is:

1. Create an initial commit for the base JSP/Servlet application.
2. Commit the MySQL migration, JDBC repository and SQL schema as a separate change.
3. Commit the Physical/Online appointment method, authenticated REST endpoint and tests as a separate change.
4. Commit the final assessment report and evidence after visual review.

Each commit should contain one coherent feature or documentation improvement. Before committing, run the automated test suite; after committing, use `git log --oneline --graph --decorate --all` to demonstrate the history.

## Public GitHub publication

GitHub publication requires the repository owner to be signed in to their own GitHub account. The following commands publish the already-created local history without exposing credentials in project files:

```powershell
git branch -M main
git remote add origin https://github.com/<your-github-user>/sunrise-dental-clinic.git
git push -u origin main
```

Create the remote repository as **Public** before the push. Once the push completes, replace the placeholder below in the submission report and README with the actual public URL:

```text
https://github.com/<your-github-user>/sunrise-dental-clinic
```

## Workflow used

Feature work is made on a short-lived branch, reviewed with `git diff main...feature-name`, tested, then merged into `main` using a fast-forward or merge commit as appropriate. This gives a visible audit trail, isolates changes to the appointment feature, and makes rollback possible with `git revert <commit>`.

This document intentionally does not claim that a GitHub remote has been published: no GitHub account or repository URL was supplied to the project workspace.
