#!/bin/bash
set -eux -o pipefail

# compute the "newest" git tag of the current branch

# if multiples tags are found for the current commit
# the bigger is used
# ex 16.14.1 is bigger than 16.9.1

# if no tag found argument is used as default tag
# or fallback to 0.0.0

# version are stored as git tags

# requirements:
# git

# optionnal arguments:
# (0.0)
if [ -z ${1:-} ]; then
  # if no arg given, default to 0.0.0
  DEFAULT_TAG="0.0.0"
else
  DEFAULT_TAG=$1
fi;

# force fetch tags (especially in fetch startegy)
git fetch --tags

# it's a bit tricky here, because some may have tagged
# none or multiple time the same commit

set +e # disable error for git describe
# error will still be printed on stdout
LATEST_CANDIDATE=$(git describe --abbrev=0 --tags)
set -e
if [ -z $LATEST_CANDIDATE ]; then
  # print on stderr
  echo "No tag found, will fall back to DEFAULT_TAG" >&2
  LATEST_TAG=${DEFAULT_TAG}
else
  # if there is multiple tags on the same commit, keep the last one
  # sort -V gives 16.0.9 before 16.0.10
  # tail -n 1 gives the last line
  LATEST_TAG=$(git tag --points-at $LATEST_CANDIDATE | sort -V | tail -n 1)
fi;

# current version is latest tag or commit branch name (ie 16.0)
# for the moment branch name should follow semver
# name like "master" or "next" are not supported

# increment version number
echo $LATEST_TAG
