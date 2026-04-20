# extract updated module from the click-odoo-update logs
# return a list, one module per line
#
# USAGE:
#    list_updated_modules.sh [FILE]
#
# if no FILE is given read standard input

if [ -n "$1" ]; then
    # test if file is readable
    if [ ! -f "$1" ] || [ ! -r "$1" ]; then
        echo "File '$1' do not exist or is unreadable." >&2
        exit 1
    fi
    INPUT_SOURCE="$1"
else
    # if stdin
    if [ -t 0 ]; then
        echo "No log in stdin." >&2
    fi
    INPUT_SOURCE="-" # stdin
fi

sed -ne "s/^.*click_odoo_contrib.update: Updating addons for their hash changed: //p" $INPUT_SOURCE  |  tr '.' ',' | sed 's/,/\n/g' | sort 
