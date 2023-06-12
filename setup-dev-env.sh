#!/bin/bash

CPU_TYPE=$(uname -m);
if [[ $CPU_TYPE != "x86"* ]]; then
  echo "It seems you're not using an x86 architecture (Intel chip for the unenligthened. Highly recommend
  you give up the ways of M1 chips and embrace Intel or AMD).";
  sleep 5;
fi

if [[ $OSTYPE == 'darwin'* ]]; then
  #check for MongoDB drivers
  if ! brew --version &> /dev/null; then
    echo "Homebrew not found. Installing homebrew";
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)";
  fi
  
  if ! poetry --version &> /dev/null; then
    echo "Poetry not found. Installing Poetry now";
    curl -sSL https://install.python-poetry.org | python3 -;
    export PATH="$HOME/.local/bin":$PATH;
  fi

  if ! mongosh --version &> /dev/null; then
    echo "MongoDB drivers not found. Installing MongoDB drivers for $(uname -a)";
    brew tap mongodb/brew;
    brew update;
    brew install mongodb-community@6.0;
  fi

  if ! gcloud --version &> /dev/null; then
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

  if ! docker --version &> /dev/null; then
    echo "Docker Desktop not found. Installing Docker Desktop for $(uname -a) arch $CPU_TYPE";
    if [[ $CPU_TYPE == "x86"* ]]; then
      wget "https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-amd64";
      echo "Go to the Downloads folder, and double click the Docker.dmg installer. This will launch the 
      setup wizard.";
    else 
      wget "https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64";
      "Go to the Downloads folder, and double click the Docker.dmg installer. This will launch the setup wizard";
    fi
  fi

else
  if ! poetry --version &> /dev/null; then
    echo "Poetry not found. Installing Poetry now";
    sudo aprt-get update;
    sudo apt-get install python3-poetry;
  fi

  if ! mongosh --version &> /dev/null; then
    echo "MongoDB drivers not found. Installing MongoDB drivers for $(uname -a) now.";
    sudo apt-get install gnupg;
    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
   --dearmor;
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list;
    sudo apt-get update;
    sudo apt-get install -y mongodb-org;
  fi

  if ! docker --version &> /dev/null; then
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

  if ! gcloud --version &> /dev/null; then
    curl -O "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-434.0.0-linux-x86_64.tar.gz";
    tar -xvf google-cloud-cli-434.0.0-linux-x86_64.tar.gz;
    ./google-cloud-sdk/install.sh;
    ./google-cloud-sdk/bin/gcloud init;
  fi
fi
