FROM jenkins/jenkins:lts-jdk17

USER root

# Install required tools and Python with venv support
RUN apt-get update && apt-get install -y \
    postgresql-client \
    python3 \
    python3-venv \
    python3-pip \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Create a Python virtual environment and install required packages
ENV VENV_PATH=/opt/pyenv
RUN python3 -m venv $VENV_PATH && \
    $VENV_PATH/bin/pip install --no-cache-dir \
        pandas \
        matplotlib \
        plotly

# Optionally make the virtual environment's Python and pip the defaults
RUN ln -s $VENV_PATH/bin/python /usr/local/bin/python3 && \
    ln -s $VENV_PATH/bin/pip /usr/local/bin/pip3

# Create backup directory with Jenkins user ownership
RUN mkdir -p /opt/backups && \
    chown -R jenkins:jenkins /opt/backups

# Install Jenkins plugins
RUN jenkins-plugin-cli --plugins \
    configuration-as-code \
    job-dsl \
    workflow-aggregator \
    pipeline-utility-steps \
    email-ext \
    docker-workflow \
    blueocean \
    dashboard-view

USER jenkins
