#!/bin/bash

if [ "$1" != "" ]; then
  git add .;
  git commit -m "$@";

  # bitbucket
  git push -u origin master;

  # github
  git push -u github master;
fi
