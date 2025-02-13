#!/bin/bash
set -euxo pipefail

# create few spares from a template

# A spare is db derived from a template, ready to be renamed and used
# It's quicker to rename a db than create a new one from a template
# At creation of the spare, we do not know the final name of the db
# so we create it with a suffix _spare_0n

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <DB_TEMPLATE>"
  exit 1
fi

echo "Generate spares for template $1"
echo $(date -u)

if ! command -v psql &> /dev/null
then
  echo "Command 'psql' could not be found"
  # A utility to be executed was not found.
  exit 127
fi

# ensure template exists
if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='$1'" -d postgres)" != '1' ]
then
  echo "Template do not exist" >> /dev/stderr
  echo "$1 = $1" >> /dev/stderr
  exit 1
fi

# create a spare only if it doesn't exists
# we assume spare are deleted somewhere else when a new template is provisionned
if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='$1_spare_01'" -d postgres)" != '1' ]
then
  echo "Create spare_01"
  createdb $1_spare_01 -T $1;
fi

if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='$1_spare_02'" -d postgres )" != '1' ]
then
  echo "Create spare_02"
  createdb $1_spare_02 -T $1;
fi

echo "Spare generated"
echo $(date -u)
