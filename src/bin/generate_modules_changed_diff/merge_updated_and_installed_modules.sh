# In the list of installed modules, add the modules who will be updated by click odoo update
# Some modules like core, custom modules, or patched module do not increment their version number

# USAGE
#    merge_updated_and_installed_modules.sh modules_before modules_after modules_updated
#
# Example
#  modules_before:
#   base,18.0.1.0.0
#   module_not_installed,
#   module_1,18.0.1.0.1
#   module_2,18.0.1.1.0
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
#   base,18.0.1.0.0* silent update
#   module_not_installed,
#   module_1,18.0.1.0.1
#   module_2,18.0.2.0.0

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
if [ -n "$3" ]; then
    # test if file is readable
    if [ ! -f "$3" ] || [ ! -r "$3" ]; then
        echo "File '$3' do not exist or is unreadable." >&2
        exit 1
    fi
fi
MODULES_BEFORE="$1"
MODULES_AFTER="$2"
MODULES_UPDATED_FILE="$3"

gawk -F, '
    ARGIND == 1 { before[$1] = $2; next }
    ARGIND == 2 { updated[$1]; next }
    {
        # $1 nom du module
        # $2 version du module
        if ($1 in updated && $2 == before[$1]) {
            print $1 "," $2 "* silent update"
        } else {
            print $1 "," $2
        }
    }
' "${MODULES_BEFORE}" "${MODULES_UPDATED_FILE}" "${MODULES_AFTER}"
