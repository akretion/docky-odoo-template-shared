#!/usr/bin/env python3
# publish_db.py: create db for the next version
# we start from source_db

# create a db with a name like projet_17-0_to_migrate_template
# take care if the dest db already exist (drop if exits)
# and kill all connexions to source_db to allow the copy


import argparse

try:
    import psycopg2
    from psycopg2 import sql
except ModuleNotFoundError:
    print("psycopg2 may be not found")
    # in tests, we don't need psycopg2
from sys import argv


def parse_args(args):
    # expose input from CLI
    parser = argparse.ArgumentParser(description="Create a template for next version. Next version is guessed from major_branch.")

    # Required attributes
    # here with force
    parser.add_argument("source_db", type=str, help="The db to copy)")
    parser.add_argument("major_branch", type=str, help="like 16.0 - actual version")
    parser.add_argument(
        "project_name", type=str, help="The base name of the db (without ending _)"
    )
    return parser.parse_args(args)


def get_next_branch(branch):
    # we expect branch to be like 16.0
    # return 17.0
    parts = branch.split(".")
    # we expect kind of semver
    # we retain only two first digits
    # 18.32.2 -> 19-0
    # 17.3 -> 18-0
    # 15 -> 16-0
    major = str(int(parts[0]) + 1)
    return f"{major}-0"


def kill_existing_connexions(cr, db_name):
    # we can't copy if some already access the db
    # like pdbouncer !
    query = "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s"
    data = [db_name]
    # the syntax is a bit tricky
    # no '' and data should be a collection (like array)
    cr.execute(query, data)


def create_from_template(cr, db_name, template):
    query = sql.SQL("CREATE DATABASE {db_name} TEMPLATE {template};").format(
        db_name=sql.Identifier(db_name),
        template=sql.Identifier(template),
    )
    cr.execute(query)


def drop_db_if_exists(cr, db_name):
    query = sql.SQL("DROP DATABASE IF EXISTS {db_name};").format(
        db_name=sql.Identifier(db_name),
    )
    cr.execute(query)


def main_bs(cr, args):
    version = get_next_branch(args.major_branch)
    source_db = args.source_db
    proj_name = args.project_name
    proj_name_ver = f"{proj_name}_{version}"
    proj_name_ver_to_migrate_template = f"{proj_name_ver}_to_migrate_template"
    print(f"Will create {proj_name_ver_to_migrate_template} from {source_db}")
    kill_existing_connexions(cr, source_db)
    drop_db_if_exists(cr, proj_name_ver_to_migrate_template)
    create_from_template(cr, proj_name_ver_to_migrate_template, source_db)
    return True


def main():
    args = parse_args(argv[1:])
    print(args)
    # we use environment variables like PGHOST, PGUSER...
    conn = psycopg2.connect(dbname="postgres")
    conn.autocommit = True
    try:
        with conn.cursor() as cr:
            main_bs(cr, args)
        conn.close()
    except psycopg2.Error as err:
        # close connection explicitely
        # all exceptions ?
        conn.close()
        raise err
        # rethrow ?


if __name__ == '__main__':
    # run as a script, not imported as a module
    main()
