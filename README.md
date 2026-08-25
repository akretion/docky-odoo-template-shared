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

# Features

## `pg_stat_statements` enabled in dev environment

`pg_stat_statements` allows to track statistics of SQL queries. It is very useful to
analyze the performance of SQL queries triggered by Odoo.

If not already, the extension needs to be enabled with:
```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

Then before triggering the Odoo feature you want to analyze, clear the stats:
```sql
SELECT pg_stat_statements_reset();
```

Launch the Odoo feature you want (e.g. a report, an SO validation...), and once it's finished, take a look on generated queries with a query such as:
```sql
SELECT queryid, substring(query, 1, 160) AS query,
      calls,
      round(total_exec_time::numeric, 2) AS total_time,
      round(mean_exec_time::numeric, 2) AS mean_time,
      round((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS percentage
FROM pg_stat_statements
WHERE dbid IN (SELECT oid FROM pg_database WHERE datname=current_database())
ORDER BY total_time DESC
LIMIT 10;
```

A high number of `calls` could be an issue on Odoo/Python side (e.g. search in a loop,
or missing cache), while a high `mean_time` could be a query badly written or a missing index.

For this last issue, check the full query with:
```sql
SELECT query FROM pg_stat_statements WHERE queryid={QUERYID};
```
If there are parameters, they will be replaced by placeholders, you'll have to guess from where this query is launched in Odoo, and what parameters are used when this query is executed.
Then launch your query prefixed with `EXPLAIN ANALYZE`:
```sql
EXPLAIN ANALYZE {QUERY}
```
This will tell you where the bottleneck could be, and up to you to find the right fix (e.g. missing index).

You could use a service like [explain.dalibo.com](https://explain.dalibo.com/) to visualize the result in a nice graph.

For best results, use `EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)`.
