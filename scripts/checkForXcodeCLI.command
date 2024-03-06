#!/bin/zsh
echo "Checking Command Line Tools for Xcode"
# Only run if the tools are not installed yet
# To check that try to print the SDK path
git &> /dev/null
if [ $? -ne 0 ]; then
REPAIR_GIT=1
fi

xcode-select -p &> /dev/null
if [ $REPAIR_GIT == 1 ]; then
  echo "Command Line Tools for Xcode not found. Installing from softwareupdate…"
# This temporary file prompts the 'softwareupdate' utility to list the Command Line Tools
  touch /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress;
  PROD=$(softwareupdate -l | grep "\*.*Command Line" | tail -n 1 | sed 's/^[^C]* //')
  softwareupdate -i "$PROD" --verbose;
else
  echo "Command Line Tools for Xcode have been installed."
fi
