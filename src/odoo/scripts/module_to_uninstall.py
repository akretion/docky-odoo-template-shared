# Fill the variable MODULE LIST with the module you want to uninstall
# Exemple : MODULE_LIST = ["custom_all"]
# or leave an empty list
# The modules will be uninstalled by start entrypoint script
MODULE_LIST = []
if MODULE_LIST:
    print(str(MODULE_LIST).replace("[", "(").replace("]", ")"))
