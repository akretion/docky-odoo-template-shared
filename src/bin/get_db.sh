#!/bin/bash

# ensure a db is available
# provision a db from a spare if needed
# fallback to _template

# This should be run before or in

# A spare is db derived from a template, ready to be renamed and used
# It's quicker to rename a db than create a new one from a template
# At creation of the spare, we do not know the final name of the db
# so we create it with a suffix _spare_0n

# DB_NAME is the target like someproject_1234
# CI_PROJECT_NAME is someproject

echo "get db"
if ! command -v psql &> /dev/null
then
  echo "Command 'psql' could not be found"
  # A utility to be executed was not found.
  exit 127
fi

if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" -d postgres )" == '1' ]
then
	echo "${DB_NAME} already exist. Skipping"
	exit 0
fi

if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='${CI_PROJECT_NAME}_spare_01'" -d postgres )" == '1' ]
then
	echo "take spare_01"
	psql -c "ALTER DATABASE \"${CI_PROJECT_NAME}_spare_01\" RENAME TO \"${DB_NAME}\"" -d postgres
	exit 0
fi

if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname=\"${CI_PROJECT_NAME}_spare_02\"" -d postgres )" == '1' ]
then
	echo "take spare_01"
	psql -c "ALTER DATABASE \"${CI_PROJECT_NAME}_spare_02\" RENAME TO \"${DB_NAME}\"" -d postgres
	exit 0
fi

echo "start from template"
createdb ${DB_NAME} -T ${CI_PROJECT_NAME}_template
exit 0
