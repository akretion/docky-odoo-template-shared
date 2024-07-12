#!/usr/bin/env python3
# get_db.py: create db

import argparse

try:
    import psycopg2
    from psycopg2 import sql
except ModuleNotFoundError:
    print("psycopg2 may be not found")
    # in tests, we don't need psycopg2
from sys import argv, stderr


def parse_args(args):
    # expose input from CLI
    parser = argparse.ArgumentParser(description="Get a db from a template or spare")

    # Required attributes
    # here with force
    parser.add_argument("db_name", type=str, help="Expected db_name (outcome)")

    parser.add_argument("major_branch", type=str, help="like 16.0")
    parser.add_argument(
        "project_name", type=str, help="The base name of the db (without ending _)"
    )
    # Switch
    parser.add_argument(
        "--migration",
        action="store_true",
        help="Is an open upgrade migration" "a %_to_migrate template will be used",
    )
    # optionnal
    parser.add_argument(
        "--force_template",
        type=str,
        nargs="?",
        help="Optionnal, use this template and exit",
    )
    return parser.parse_args(args)


def list_db(cr, project_name):
    query = sql.SQL("SELECT datname FROM pg_database WHERE datname ilike %s")
    cr.execute(query, (f"{project_name}%",))
    results = cr.fetchall()
    # fetchall returns a [('db1',),('db3',)]
    return [res[0] for res in results]


def rename_spare(cr, db_name, spare):
    query = sql.SQL("ALTER DATABASE {spare} RENAME TO {db_name};").format(
        db_name=sql.Identifier(db_name),
        spare=sql.Identifier(spare),
    )
    cr.execute(query)


def create_from_template(cr, db_name, template):
    query = sql.SQL("CREATE DATABASE {db_name} TEMPLATE {template};").format(
        db_name=sql.Identifier(db_name),
        template=sql.Identifier(template),
    )
    cr.execute(query)


def sanitize_branch_name(branch):
    """Replace dot by dash in branch name"""
    # we don't like dot in db names
    # 18.0 -> 18-0
    parts = branch.split(".")
    # we expect kind of semver
    # we retain only two first digits
    # 18.32.2 -> 18.32
    # 17.3 -> 17.3
    # 15 -> 15.0
    major = parts[0]
    minor = parts[1] if len(parts) > 1 else "0"
    return f"{major}-{minor}"


def get_a_spare(list_db, prefix):
    """Return name of a spare or False"""
    spare_candidates = [db for db in list_db if db.startswith(f"{prefix}_spare_")]
    # take de first one
    if spare_candidates and spare_candidates[0]:
        return spare_candidates[0]
    else:
        return False


def main_bs(cr, args, db_list):
    """Create a db from a template or rename from a spare

    Return False if no template found
    """
    force_template = args.force_template
    is_openupgrade_migration = args.migration
    version = sanitize_branch_name(args.major_branch)
    db_name = args.db_name
    proj_name = args.project_name
    proj_name_ver = f"{proj_name}_{version}"
    proj_name_ver_template = f"{proj_name_ver}_template"
    proj_name_def_template = f"{proj_name}_template"
    proj_name_ver_to_migrate_template = f"{proj_name_ver}_to_migrate_template"

    if force_template:
        # use force_template and exit
        create_from_template(cr, db_name, force_template)
        return True

    if is_openupgrade_migration:
        # template should be: project_name_major-to_migrate_template
        if proj_name_ver_to_migrate_template in db_list:
            create_from_template(cr, db_name, proj_name_ver_to_migrate_template)
            return True
        else:
            # we don't want to take a default branch here
            print(f"{proj_name_ver_to_migrate_template} not found", file=stderr)
            return False

    # does a spares exists ?
    # we assume the spare have major branch in the name
    spare = get_a_spare(db_list, proj_name_ver)
    if spare:
        rename_spare(cr, db_name, spare)
        return True

    if proj_name_ver_template in db_list:
        create_from_template(cr, db_name, proj_name_ver_template)
        return True

    # fallback to name without branch
    # = the version in production
    if proj_name_def_template in db_list:
        create_from_template(cr, db_name, proj_name_def_template)
        return True

    print(
        f"{proj_name_ver_template} or {proj_name_def_template} not found", file=stderr
    )
    return False


def main():
    args = parse_args(argv[1:])
    print(args)
    # we use environment variables like PGHOST, PGUSER...
    conn = psycopg2.connect(dbname="postgres")
    conn.autocommit = True
    try:
        with conn.cursor() as cr:
            db_list = list_db(cr, args.project_name)
            main_bs(cr, args, db_list)
        conn.close()
    except psycopg2.Error as err:
        # close connection explicitely
        # all exceptions ?
        conn.close()
        raise err
        # rethrow ?


main()
