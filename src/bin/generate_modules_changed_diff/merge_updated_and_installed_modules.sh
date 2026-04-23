# In the list of installed modules, add the modules who will be updated by click odoo update
# Some modules like core, custom modules, or patched module do not increment their version number

# USAGE
#    merge_updated_and_installed_modules.sh modules_after modules_updated
#
# Example
#
#  modules_after:
#   base,18.0.1.0.0
#   module_not_installed,
#   module_1,18.0.1.0.1
#   module_2,18.0.2.0.0
#
#  modules_updated:
#   base
#   module_2
#
#  output:
#   base,18.0.1.0.0**
#   module_not_installed,
#   module_1,18.0.1.0.1
#   module_2,18.0.2.0.0**

if [ -n "$1" ]; then
    # test if file is readable
    if [ ! -f "$1" ] || [ ! -r "$1" ]; then
        echo "File '$1' do not exist or is unreadable." >&2
        exit 1
    fi
fi
if [ -n "$2" ]; then
    # test if file is readable
    if [ ! -f "$2" ] || [ ! -r "$2" ]; then
        echo "File '$2' do not exist or is unreadable." >&2
        exit 1
    fi
fi
MODULES_UPDATED_FILE="$1"
MODULES_AFTER="$2"

gawk -F, '
    ARGIND == 1 { updated[$1]; next }
    {
        # $1 nom du module
        # $2 version du module
        if ($1 in updated) {
            print $1 "," $2 "* silent update"
        } else {
            print $1 "," $2
        }
    }
' "${MODULES_UPDATED_FILE}" "${MODULES_AFTER}"
