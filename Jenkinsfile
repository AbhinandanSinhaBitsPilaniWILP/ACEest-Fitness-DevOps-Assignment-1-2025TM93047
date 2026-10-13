pipeline {
    agent any

    environment {
        IMAGE_NAME = 'aceest-fitness-devops'
        CONTAINER_NAME = 'aceest-fitness-jenkins-smoke'
    }

    stages {
        stage('Install and Test') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/python -m pip install -r requirements.txt'
                sh '.venv/bin/python -m pytest -q tests'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build --tag ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Container Smoke Test') {
            steps {
                sh "docker run --detach --rm --name ${CONTAINER_NAME} --publish 5099:5000 ${IMAGE_NAME}:${BUILD_NUMBER}"
                sh '''for attempt in $(seq 1 20); do
                    if python3 -c 'import urllib.request; assert urllib.request.urlopen("http://127.0.0.1:5099/healthz").status == 200'; then
                        exit 0
                    fi
                    sleep 1
                done
                exit 1'''
            }
        }
    }

    post {
        always {
            sh "docker stop ${CONTAINER_NAME} || true"
            sh "docker image rm ${IMAGE_NAME}:${BUILD_NUMBER} || true"
        }
    }
}
