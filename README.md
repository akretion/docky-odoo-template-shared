# Basic Odoo project template used by [docky](https://github.com/akretion/docky)

This repo contains all the basic files needed to create an Odoo project from scratch using [ak](https://github.com/akretion/ak) command-line tool developed by [Akretion](https://akretion.com).

To start a new Odoo project, you don't need to download this repo.

1. First install to [docky](https://github.com/akretion/docky) (version > 8.0.0), [copier](https://github.com/copier-org/copier) and [ak](https://github.com/akretion/ak)


For that we deeply recommand you to install them with [pipx](https://github.com/pypa/pipx)

```
pipx install docky
pipx install copier
pipx install git+https://github.com/akretion/ak.git@master
```

2. Create an *empty folder* for your Odoo projet and run `copier copy` in it

```
copier copy https://github.com/akretion/docky-odoo-template-shared .
```

3. Create the ".env" file by running copier copy again but with a different template

```
copier copy https://github.com/akretion/docky-odoo-template-personal .
```

4. Download the Odoo source code and other external modules specified in the [spec.yaml](odoo/spec.yaml) `ak build` from the spec.yaml's folder

```
cd odoo
ak clone
ak build
```

> [ak](https://github.com/akretion/ak) use the [git-aggregator](https://github.com/acsone/git-aggregator) tool by [Acsone](https://www.acsone.eu/).
> More information on the [git-aggregator](https://github.com/acsone/git-aggregator) repo to understand how to fill the [spec.yaml](odoo/spec.yaml) file.


5. Once all the code is downloaded, go back to your project's root folder and launch `docky run`
```
cd ..
docky run
```

On the first `docky run`, docky will download the Odoo image referenced in the [DockerFile](odoo/Dockerfile) and run your different docker-compose files (basically docker-compose.yml, dev.docker-compose.yml or prod.docker-compose.yml) following the environment's variables registered in your **.env** file.

To reload the Odoo docker image or to update your docky after changing you environment variables, run `docky build`.

More information on : [docky](https://github.com/akretion/docky).


# Gitlab

On gitlab, mark the branch as protected


# Bump and Migration

From the gitlab pipeline, run the "publish" job to create an updated docker image
