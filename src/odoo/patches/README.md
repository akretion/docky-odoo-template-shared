## Apply patches

If you need to apply some code changes to existing modules,
you can use the patches intead of a fork, particulary if patch is not
meant to be published.


### How to move a custom module to a public repo

Let's say you want to publish local-src/custom_module_x
to OCA/some-repo/some_module.
You were the only implementation under the custom_module_x name
so it's not necessary to publish a migration script.


Steps
- 1) rename the module, clean the code, remove private data
- 2) create pre_init_hook to rename the module 
- 3) create a patch
- 4) publish the module (without the patch)
- 5) specify the patch in spec.yaml


#### Clean the code

Ensure you follow the code conventions of the destination repo (apply
pre-commit).
Also search for strings like the customer's name or anything related to 
the customer.

Search also for other modules who depends on the one you are moving.
Try to uninstall the module from odoo Applications page or search
depencies with `manifestoo`


#### Pre-init-hook

Always use openupgrade lib to rename module, fields, data, views...
Add a `pre_init_hook`, in `__manifest__.py` and import it in `__init__.py`

Take a look on `some-repo` folder


####  Create a patch

On the destination module, AFTER the commit you publish on OCA, add your specific changes,
and migration commit (but do not push).

Then `cd external-src/some-repo` then run `git format-patch 16.0 -o ../../patches/some-repo/`

#### Specify the patch in spec.yaml

In spec.yaml, use the long syntax and specify the directory of the patch with `git am`:

```
some-repo:
  modules:
    - some_module
  remotes:
    oca: https://github.com/oca/some-repo
  merges:
    - oca 16.0
  shell_command_after:
    - git am ../../patches/some-repo/*
```
