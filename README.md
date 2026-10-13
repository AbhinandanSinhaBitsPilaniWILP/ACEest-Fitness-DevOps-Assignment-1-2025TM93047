# ACEest Fitness DevOps Assignment - 2025TM93047

Student ID: 2025TM93047  
Submission contact: 2025tm93047@wilp.bits-pilani.ac.in

This repository implements the ACEest Fitness & Gym assignment as a small Flask web application. It provides a login-protected dashboard for client registration, program generation, membership status, workout logging, and JSON API access. Pytest validates the application, Docker packages it, Jenkins performs the BUILD quality gate, and GitHub Actions runs the automated build-test-container workflow on every push and pull request.

## Source adaptation

The supplied code archive contains Tkinter desktop versions, with `Aceestver-3.2.4.py` as the most feature-rich version. This repository keeps those fitness-management concepts and adapts them to Flask because the assignment explicitly requires a Flask application and web-accessible CI/CD evidence.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:ADMIN_USERNAME = "admin"
$env:ADMIN_PASSWORD = "admin"
python app.py
```

Open `http://127.0.0.1:5000`. The default local-demo credentials are `admin` / `admin`; set `ADMIN_PASSWORD` before any shared deployment. The SQLite database is created under `instance/`.

## Test locally

```powershell
python -m pytest -q
```

The suite covers the health endpoint, authentication guard, client creation, duplicate validation, program generation, workout logging, and client detail API.

## Build and run with Docker

```powershell
docker build -t aceest-fitness-devops .
docker run --rm -p 5000:5000 `
  -e ADMIN_PASSWORD=change-me `
  -v aceest-data:/app/instance `
  aceest-fitness-devops
```

Verify `http://127.0.0.1:5000/healthz` returns `{"service":"aceest-fitness","status":"ok"}`. The image runs as a non-root user and includes a Docker health check.

## Jenkins BUILD job

Create a Pipeline job in Jenkins, point it at this GitHub repository, and select `Jenkinsfile` from SCM. The pipeline expects a Jenkins agent with Python, Docker, and permission to access the Docker daemon. It runs unit tests, builds the image, starts a container, checks `/healthz`, and always cleans up the smoke-test container and image.

For a GitHub webhook, configure the repository webhook to the Jenkins endpoint and enable the appropriate GitHub hook trigger in the job. Keep credentials in Jenkins credentials storage; do not commit tokens or passwords.

## GitHub Actions

`.github/workflows/main.yml` is triggered by both `push` and `pull_request`. It checks out the source, installs Python dependencies, runs Pytest, builds the Docker image, starts the container, and verifies `/healthz`.

## Evidence checklist for submission

Capture and upload the following screenshots to one Google Drive folder, then replace the placeholders in the final submission page with the real share links:

1. Local run: browser dashboard after login, with the address bar visible.
2. Docker run: terminal showing `docker build`, `docker run`, and the `/healthz` response, plus the app in the browser.
3. GitHub Actions: the workflow run summary with all steps green and the repository URL visible.
4. Jenkins: the pipeline stage view and successful console output showing tests, Docker build, and smoke test.
5. GitHub repository: public repository home page showing the README and required files.

## Suggested Git history

Use small, descriptive commits such as `feat: add client management flow`, `test: cover client and workout API`, `build: add Docker packaging`, and `ci: add Jenkins and GitHub Actions pipelines`. Use a feature branch and merge through a pull request so the pull-request workflow is evidenced.

