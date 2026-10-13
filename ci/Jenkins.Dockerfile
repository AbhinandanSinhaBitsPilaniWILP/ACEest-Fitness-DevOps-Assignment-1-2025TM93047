FROM jenkins/jenkins:lts-jdk21

USER root
RUN apt-get update \
    && apt-get install --yes --no-install-recommends docker-cli docker-buildx git python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
RUN command -v docker && docker --version

COPY ci/jenkins-init.groovy /usr/share/jenkins/ref/init.groovy.d/jenkins-init.groovy

USER jenkins
RUN jenkins-plugin-cli --plugins workflow-aggregator git pipeline-stage-view
