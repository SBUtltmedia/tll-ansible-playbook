#!/bin/zsh

echo "Checking Command Line Tools for Xcode..."

# Check if the Xcode Command Line Tools are already installed by printing the developer path.
# The '||' (OR) operator is used to check the exit status.
# If 'xcode-select -p' succeeds (exit status 0), it means the tools are installed.
# If it fails (non-zero exit status), the 'else' block will be executed.
if xcode-select -p &>/dev/null; then
  echo "Command Line Tools for Xcode are already installed. Exiting."
  exit 0
else
  echo "Command Line Tools for Xcode not found. Installing now..."
fi

# The installation code should only run if the 'if' condition above is false.
# This temporary file prompts the 'softwareupdate' utility to list the Command Line Tools.
touch /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress;

# Find the latest Command Line Tools product ID and install it.
PROD=$(softwareupdate -l | grep "\*.*Command Line" | tail -n 1 | sed 's/^[^C]* //')
softwareupdate -i "$PROD" --verbose;

echo "Installation complete."