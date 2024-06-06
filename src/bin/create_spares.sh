#!/bin/bash

# create few spares from a template

# A spare is db derived from a template, ready to be renamed and used
# It's quicker to rename a db than create a new one from a template
# At creation of the spare, we do not know the final name of the db
# so we create it with a suffix _spare_0n

# Arguments: $DB_NAME name of the final db like 'someproject'
# ${DB_NAME}_template should exist like someproject_template

# because it may take looong time to execute
# you can run this from docker compose run --detach
# in order to let the gitlab runner continue without expecting
# a result

echo "Generate spares"
echo $(date -u)

# DB_NAME is the target like someproject_1234
# CI_PROJECT_NAME is someproject

if ! command -v psql &> /dev/null
then
  echo "Command 'psql' could not be found"
  # A utility to be executed was not found.
  exit 127
fi

# ensure template exists
if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='${CI_PROJECT_NAME}_template'" -d postgres)" != '1' ]
then
	echo "Template do not exist" >> /dev/stderr
	exit 1
fi

# create a spare only if it doesn't exists
# we assume spare are deleted somewhere else when a new template is provisionned
if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='${CI_PROJECT_NAME}_spare_01'" -d postgres)" != '1' ]
then
	echo "Create spare_01"
	createdb ${CI_PROJECT_NAME}_spare_01 -T ${CI_PROJECT_NAME}_template;
fi

if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='${CI_PROJECT_NAME}_spare_02'" -d postgres )" != '1' ]
then
	echo "Create spare_02"
	createdb ${CI_PROJECT_NAME}_spare_02 -T ${CI_PROJECT_NAME}_template;
fi

echo "Spare generated"
echo $(date -u)