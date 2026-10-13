# ACEest Evidence Plan

## What the assignment requires

The assignment document requires a Flask fitness-management application, local Git and GitHub version control, Pytest validation, a Docker image, a Jenkins BUILD job, and a GitHub Actions workflow triggered by push and pull request. It also expects a public GitHub repository containing the application, tests, Dockerfile, workflow YAML, and professional README.

The supplied code archive is reference application material rather than a ready submission: its versions are Tkinter desktop programs. The current repository adapts the fitness-management features to Flask so the application can be tested and opened in a browser.

## What the requested submission adds

The requested submission format adds a public repository link and evidence links hosted in one Google Drive folder. The evidence must show actual successful runs; a screenshot of configuration alone is not sufficient.

## Execution order

1. Create or sign in to the student-owned GitHub account using the institutional email. Keep the password, recovery information, email verification code, and any CAPTCHA under the account owner's control.
2. Create a public repository, push this project, and confirm the repository home page shows `app.py`, `tests/`, `Dockerfile`, `Jenkinsfile`, `.github/workflows/main.yml`, and `README.md`.
3. Open the repository's Actions tab and confirm the push workflow is green. Create a small feature branch and pull request, then capture the green pull-request workflow as the strongest CI evidence.
4. Install or start Docker Desktop and run the local image. Capture the build output, the running container, the `/healthz` response, and the browser dashboard.
5. Configure Jenkins with a Pipeline-from-SCM job pointing to the public repository and the `Jenkinsfile`. Give the Jenkins agent access to Python and Docker, run the job, and capture the stage view plus the successful console lines.
6. Create one Drive folder owned by the student account. Upload the evidence images and set the folder to the access level permitted by the submission instructions. Do not make the files editable unless required.
7. Create the one-page submission document with the repository URL and the four evidence URLs in the same order as the example PDF: local run, Docker run, GitHub Actions, and Jenkins. Add the repository file listing as a fifth link only if the evaluator benefits from it.
8. Open every shared link in a private/incognito window or a signed-out browser and verify that the evaluator can access it. Fix sharing before submission if any link requires the owner's login.

## Screenshot names and minimum proof

| File | Minimum visible proof |
| --- | --- |
| `01-local-run.png` | Browser address bar, ACEest dashboard, at least one client, and a generated program or logged workout |
| `02-docker-run.png` | Terminal with image build and container/health response, plus the app URL or browser view |
| `03-github-actions.png` | Public repository URL, workflow run, commit or pull request, and all required steps green |
| `04-jenkins.png` | Jenkins job name/build number, green stages, and console output for tests, Docker build, and smoke test |
| `05-repository.png` | Public repository page showing the expected files and README |

## Final quality gate

The final links are valid only when all four infrastructure claims are backed by real evidence: local Flask run, Docker build/run, GitHub Actions success, and Jenkins success. The repository and Drive links must be checked from a signed-out view before submission.

