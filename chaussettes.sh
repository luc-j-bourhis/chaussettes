#!/bin/bash
# If the application is properly installed, package chaussettes will be found.
# On the contrary, if we want to run the development version, we need to
# tell Python where to find that package.
if [[ $1 == dev ]]; then
  cd "$( dirname "${BASH_SOURCE[0]}" )" 1> /dev/null
fi
exec /usr/bin/python3 -c 'from chaussettes import main; main.run()'
