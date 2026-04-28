#!/bin/bash
# generate a .diff with list of modules updated / installed
# no args
# create files in workdir

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# paths
WORKDIR=shared

# inputs
MODULES_BEFORE=modules_before.txt
MODULES_AFTER=modules_after.txt
MODULES_UPDATED=modules_updated.txt
MODULES_MISSING=modules_missing.txt
MODULES_WITH_UPDATES=modules_updates.txt
MODULES_WITH_UPDATES_WITH_MISSING="modules_updates_missings.txt"
CLICK_ODOO_UPDATE_LOG=click-odoo-update.log

# outputs
OUTPUT=modules_changed.diff
OUTPUT_NOCOLOR=modules_changed_nocolor.diff

cd $WORKDIR

# script

${DIR}/list_updated_modules.sh  ${CLICK_ODOO_UPDATE_LOG} > ${MODULES_UPDATED}
# modules_missing is comming from generate_code_quality
${DIR}/merge_updated_and_installed_modules.sh ${MODULES_BEFORE} ${MODULES_AFTER} ${MODULES_UPDATED} > ${MODULES_WITH_UPDATES}
${DIR}/merge_missing_and_installed_modules.sh ${MODULES_MISSING} ${MODULES_WITH_UPDATES} > ${MODULES_WITH_UPDATES_WITH_MISSING}

git diff --no-index --output ${OUTPUT} --color -- ${MODULES_BEFORE} ${MODULES_WITH_UPDATES_WITH_MISSING} || true
git diff --no-index --output ${OUTPUT_NOCOLOR} --no-color -- ${MODULES_BEFORE} ${MODULES_WITH_UPDATES_WITH_MISSING} || true
