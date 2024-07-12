#!/usr/bin/env python


from . import publish_db
from .publish_db import main_bs, parse_args, get_next_branch


def test_get_next_branch():
    # main cases
    assert get_next_branch("14.0") == "15-0"
    assert get_next_branch("14") == "15-0"

    # additionnal cases
    assert get_next_branch("15.03") == "16-0"
    assert get_next_branch("14.1234") == "15-0"


def test_main_bs():
    cr = None

    args1 = {
        "db_name": "proj_123",
        "major_branch": "18.0",
        "project_name": "proj",
    }

    def test1_create_from_template(cr, db_name, template):
        assert db_name == "proj_19-0_to_migrate_template"
        assert template == "proj_123"

    def test1_kill_existing_connexions(cr, db_name):
        assert db_name == "proj_123"

    def test1_drop_db_if_exists(cr, db_name):
        assert db_name == "proj_19-0_to_migrate_template"

    publish_db.create_from_template = test1_create_from_template
    publish_db.kill_existing_connexions = test1_kill_existing_connexions
    publish_db.drop_db_if_exists = test1_drop_db_if_exists
    main_bs(cr, parse_args(args1.values())) is True

