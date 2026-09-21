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


# KpiTen (optional)

Answer `yes` to the `kpiten` question to get [KpiTen](https://github.com/akretion/kpiten), the
dashboards and KPI on the data of the Odoo of the project (the rights of the user connected to Odoo
apply). It adds :

- `kpiten.dc.yml` : one service per front (Shiny :5000, NiceGUI :5001, marimo :5002), built from
  `kpiten/Dockerfile`, on http://PROJECT_NAME-shiny.localhost, `-nicegui`, `-marimo` (traefik) ;
  the fronts read Odoo through `/jsonrpc` (so `base` is a server-wide module of the dev stack) and
  Postgres directly ; their parquets are in `data/shared/kpiten` ;
- `.env.kpiten` : the environment of the fronts (tracked by git, no secret : the password of the
  Odoo account they use is `KPITEN_ODOO_PWD` of the `.env`, `admin` by default) ;
- `odoo/spec-kpiten.yaml` : the `kpiten` entry to copy in `odoo/spec.yaml` (the branch
  `odoo-multiversion` is one source for all the series, `scripts/downgrade.py` converts it).

The address of each front is a system parameter (`kpiten_<front>_service`). No
`server_environment_files` needed : the `data/neutralize.sql` of `kpiten_shiny`, `kpiten_nicegui`
and `kpiten_marimo` set it for the docky stack when the database is neutralized
(`odoo neutralize`, already the last step of `backup/load_db.sh`, which first sets `web.base.url`
to http://PROJECT_NAME.localhost). On a database that was not restored, run it by hand :
`docky run odoo neutralize`. For the other environments set the parameters as usual (the public
url of the front in `external_url`, `http://kpiten-<front>:<port>` in `internal_url`).
