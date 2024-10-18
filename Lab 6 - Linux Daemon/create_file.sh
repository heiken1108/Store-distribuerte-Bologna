#!/bin/bash

DIRECTORY="/path/to/monitored_directory"
FILENAME=$(date +"%Y-%m-%d_%H-%M-%S").txt
touch "$DIRECTORY/$FILENAME"
