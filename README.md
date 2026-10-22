# Student Task Tracker — CI/CD Practical

A small academic web app to demonstrate Jenkins, Docker Hub, and Kubernetes.

## Features
- View and add study tasks
- Mark a task complete or pending
- `/health` endpoint for Kubernetes health checks
- `/version` endpoint for demonstrating a code update

Tasks are stored in memory and reset when the app restarts. This is intentional to keep the project small and database-free.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000.

## Test
```bash
pytest -q
```

## Jenkins setup
- Jenkins and Docker must work on the Jenkins agent.
- Install Python 3, `venv`, `kubectl`, and Minikube as required.
- Make sure the Jenkins Linux user can use `kubectl` with a running Minikube cluster.
- In Jenkins, add a **Username with password** credential with ID `dockerhub-creds`. Use your Docker Hub username and an access token as the password. Never put secrets in the repository.
- Create a Pipeline job connected to this GitHub repository and its `Jenkinsfile`.
- Enable the GitHub webhook trigger if you want pushes to trigger builds.

Pipeline stages: checkout, tests, Docker build, Docker Hub push, and Kubernetes deployment.

For the redeployment demo, change the message returned by `/version` in `app.py`, commit and push, and show Jenkins building and deploying the updated image.
