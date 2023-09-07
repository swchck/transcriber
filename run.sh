#!/bin/bash

run() {
    docker compose down
    docker compose up -d --force-recreate
}

if command -v docker-compose &> /dev/null; then
    echo "docker-compose is installed on your system."
else
    echo "docker-compose is not installed on your system."
    echo "installing homebrew (Usually you should type your password)"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install orbstack
fi
run