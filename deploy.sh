#!/bin/sh

# Check if zsh is available
if command -v zsh >/dev/null 2>&1; then
    echo "Using zsh to run the commands..."
    # If zsh is available, run the Docker commands in zsh
    exec zsh -c "
        docker build -t ecomarket .
        docker tag ecomarket dockerfawwazaid/ecomarket:latest
        docker push dockerfawwazaid/ecomarket:latest
    "
else
    # If zsh is not available, fall back to bash
    echo "zsh not found. Using bash instead..."
    exec bash -c "
        docker build -t ecomarket .
        docker tag ecomarket dockerfawwazaid/ecomarket:latest
        docker push dockerfawwazaid/ecomarket:latest
    "
fi  # End of the if block

# run
# chmod +x deploy.sh
# .deploy.sh