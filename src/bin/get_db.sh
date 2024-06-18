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
# AK_TEMPLATE_DB is someproject_template or someproject_14_template

echo "get db"
echo "DB_NAME: ${DB_NAME}"
echo "AK_TEMPLATE_DB: ${AK_TEMPLATE_DB}"

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

if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='${AK_TEMPLATE_DB}_spare_01'" -d postgres )" == '1' ]
then
	echo "take spare_01"
	psql -c "ALTER DATABASE \"${AK_TEMPLATE_DB}_spare_01\" RENAME TO \"${DB_NAME}\"" -d postgres
	exit 0
fi

if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='${AK_TEMPLATE_DB}_spare_02'" -d postgres )" == '1' ]
then
	echo "take spare_01"
	psql -c "ALTER DATABASE \"${AK_TEMPLATE_DB}_spare_02\" RENAME TO \"${DB_NAME}\"" -d postgres
	exit 0
fi

echo "start from template"
# AK_TEMPLATE_DB = by default is CI_PROJECT_NAME_template
# but during a migration, it should be 
# CI_PROJECT_NAME_16-0_template
createdb ${DB_NAME} -T ${AK_TEMPLATE_DB}
exit 0
