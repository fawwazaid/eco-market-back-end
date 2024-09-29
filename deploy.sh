#!/bin/sh

# Check if zsh is available
if command -v zsh >/dev/null 2>&1; then
    echo "Using zsh to run the commands..."
    # If zsh is available, run the Docker commands in zsh
    exec zsh -c "
        docker build -t ecommerce .
        docker tag ecommerce dockerfawwazaid/ecommerce:final-14
        docker push dockerfawwazaid/ecommerce:final-14
    "
else
    # If zsh is not available, fall back to bash
    echo "zsh not found. Using bash instead..."
    exec bash -c "
        docker build -t ecommerce .
        docker tag ecommerce dockerfawwazaid/ecommerce:final-14
        docker push dockerfawwazaid/ecommerce:final-14
    "
fi  # End of the if block