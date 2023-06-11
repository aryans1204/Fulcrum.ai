#!/bin/bash

CPU_TYPE=$(uname -m);
if [[ $CPU_TYPE != "x86"* ]]; then
  echo "It seems you're not using an x86 architecture (Intel chip for the unenligthened. Highly recommend
  you give up the ways of M1 chips and embrace Intel or AMD).";
  sleep 5;
fi

if [[ $OSTYPE == 'darwin'* ]]; then
  #check for MongoDB drivers
  if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing homebrew";
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)";
  fi
  
  if ! command -v poetry &> /dev/null; then
    echo "Poetry not found. Installing Poetry now";
    curl -sSL https://install.python-poetry.org | python3 -;
    export PATH="$HOME/.local/bin":$PATH;

  if ! command -v mongodb &> /dev/null; then
    echo "MongoDB drivers not found. Installing MongoDB drivers for $(uname -a)";
    brew tap mongodb/brew;
    brew update;
    brew install mongodb-community@6.0;
  fi

  if ! command -v docker &> /dev/null; then
    echo "Docker Desktop not found. Installing Docker Desktop for $(uname -a) arch $CPU_TYPE";
    if [[ $CPU_TYPE == "x86"* ]]; then
      wget "https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-amd64";
      cd ~/Downloads;
      ./Docker.dmg;
    else 
      wget "https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64";
      cd ~/Downloads;
      ./Docker.dmg;
    fi
  fi

  if ! command -v gcloud &> /dev/null; then
    echo "GCloud SDK not found. Installing GCloud SDK for $(uname -a) arc $CPU_TYPE";
    if [[ $CPU_TYPE == "x86"* ]]; then
      wget "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-434.0.0-darwin-x86_64.tar.gz";
      tar -xvf google-cloud-cli*;
      ./google-cloud-sdk/install.sh;
      ./google-cloud-sdk/bin/gcloud init;
    
    else
      wget "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-434.0.0-darwin-arm.tar.gz";
      tar -xvf google-cloud-cli*;
      ./google-cloud-sdk/install.sh;
      ./google-cloud-sdk/bin/gcloud init;
    fi
  fi

else
  if ! command -v poetry &> /dev/null; then
    echo "Poetry not found. Installing Poetry now";
    curl -sSL https://install.python-poetry.org | python3 -;
    export PATH="$HOME/.local/bin":$PATH;
  fi

  if ! command -v mongodb &> /dev/null; then
    echo "MongoDB drivers not found. Installing MongoDB drivers for $(uname -a) now.";
    sudo apt-get install gnupg;
    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
   --dearmor;
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list;
    sudo apt-get update;
    sudo apt-get install -y mongodb-org;
  fi

  if ! command -v docker &> /dev/null; then
    echo "Docker not installed. Installing Docker engine for $(uname -a) now.";
    sudo apt-get update;  
    sudo apt-get install ca-certificates curl gnupg;

    sudo install -m 0755 -d /etc/apt/keyrings;
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg;
    sudo chmod a+r /etc/apt/keyrings/docker.gpg;
    
    echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    sudo apt-get update;
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin;

  fi

  if ! command -v gcloud &> /dev/null; then
    echo "Google Cloud CLI not installed. Installing Google Cloud CLI now.";
    sudo apt-get update;
    sudo apt-get install apt-transport-https ca-certificates gnupg curl sudo;
    echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list;
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.gpg;
    sudo apt-get update && sudo apt-get install google-cloud-cli;
  fi










