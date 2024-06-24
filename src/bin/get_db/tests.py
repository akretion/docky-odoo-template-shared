#!/usr/bin/env python


from . import get_db
from .get_db import get_a_spare, main_bs, parse_args, sanitize_branch_name


def test_sanitize_branch_name():
    # main cases
    assert sanitize_branch_name("14.0") == "14-0"
    assert sanitize_branch_name("14") == "14-0"

    # additionnal cases
    assert sanitize_branch_name("15.03") == "15-03"
    assert sanitize_branch_name("14.1234") == "14-1234"


def test_get_a_spare():
    list_db = (
        "proj_132",
        "proj_preprod-16-0",
        "proj_preprod-18-0",
        "proj_template",
        "proj_18-0_template",
    )
    assert get_a_spare(list_db, "proj") is False
    assert get_a_spare(list_db, "proj_18-0") is False

    list_db = (
        "proj_132",
        "proj_preprod-16-0",
        "proj_preprod-18-0",
        "proj_template",
        "proj_spare_01_template",
        "proj_18-0_template",
    )
    assert get_a_spare(list_db, "proj") == "proj_spare_01_template"
    assert get_a_spare(list_db, "proj_18-0") is False

    list_db = (
        "proj_132",
        "proj_preprod-16-0",
        "proj_preprod-18-0",
        "proj_template",
        "proj_18-0_spare_02_template",
        "proj_18-0_template",
    )
    assert get_a_spare(list_db, "proj") is False
    assert get_a_spare(list_db, "proj_18-0") == "proj_18-0_spare_02_template"


def test_main_bs():
    cr = None
    db_list = (
        "proj_132",
        "proj_preprod-16-0",
        "proj_preprod-18-0",
        "proj_template",
        "proj_18-0_spare_02_template",
        "proj_18-0_template",
        "proj_18-0_to_migrate_template",
    )

    # TEST1
    # a spare is present for the major branch (18)
    # we should take the spare
    args1 = {
        "db_name": "proj_123",
        "major_branch": "18.0",
        "project_name": "proj",
    }

    def test1_create_from_template(cr, db_name, template):
        assert False

    def test1_rename_spare(cr, db_name, template):
        assert db_name == "proj_123"
        assert template == "proj_18-0_spare_02_template"

    get_db.create_from_template = test1_create_from_template
    get_db.rename_spare = test1_rename_spare
    main_bs(cr, parse_args(args1.values()), db_list) is True

    # TEST2
    # there is no spare, we take the default branch
    args2 = {
        "db_name": "proj_123",
        "major_branch": "16.0",
        "project_name": "proj",
    }

    def test2_create_from_template(cr, db_name, template):
        assert db_name == "proj_123"
        assert template == "proj_template"

    def test2_rename_spare(cr, db_name, template):
        assert False

    get_db.create_from_template = test2_create_from_template
    get_db.rename_spare = test2_rename_spare
    main_bs(cr, parse_args(args2.values()), db_list) is True

    # TEST3
    # there is no spare, we take the default branch
    # it's counter intuitive, for 19.0

    args3 = {
        "db_name": "proj_123",
        "major_branch": "19.0",
        "project_name": "proj",
    }

    def test3_create_from_template(cr, db_name, template):
        assert db_name == "proj_123"
        # yes we take the default template because it exists
        assert template == "proj_template"

    def test3_rename_spare(cr, db_name, template):
        assert False

    get_db.create_from_template = test3_create_from_template
    get_db.rename_spare = test3_rename_spare
    main_bs(cr, parse_args(args3.values()), db_list)

    # TEST4
    # force an existing template
    args4 = {
        "db_name": "proj_123",
        "major_branch": "19.0",
        "project_name": "proj",
        "force_template": "proj_preprod-18-0",
    }

    def test4_create_from_template(cr, db_name, template):
        assert db_name == "proj_123"
        # yes we take the default template because it exists
        assert template == "proj_preprod-18-0"

    def test4_rename_spare(cr, db_name, template):
        assert False

    get_db.create_from_template = test4_create_from_template
    get_db.rename_spare = test4_rename_spare
    main_bs(cr, parse_args(args4.values()), db_list) is True

    # TEST5
    # force a not existing template
    args5 = {
        "db_name": "proj_123",
        "major_branch": "19.0",
        "project_name": "proj",
        "force_template": "proj_preprod-dontexist-0",
    }

    def test5_create_from_template(cr, db_name, template):
        assert False

    def test5_rename_spare(cr, db_name, template):
        assert False

    get_db.create_from_template = test5_create_from_template
    get_db.rename_spare = test5_rename_spare
    assert main_bs(cr, parse_args(args5.values()), db_list) is False

    # TEST6
    # test with a not existing migration
    args6 = {
        "db_name": "proj_123",
        "major_branch": "19.0",
        "project_name": "proj",
        "migration": "--migration",
    }

    def test6_create_from_template(cr, db_name, template):
        assert False

    def test6_rename_spare(cr, db_name, template):
        assert False

    get_db.create_from_template = test6_create_from_template
    get_db.rename_spare = test6_rename_spare
    assert main_bs(cr, parse_args(args6.values()), db_list) is False

    # TEST7
    # test with an existing migration
    args7 = {
        "db_name": "proj_123",
        "major_branch": "18.0",
        "project_name": "proj",
        "migration": "--migration",
    }

    def test7_create_from_template(cr, db_name, template):
        assert template == "proj_18-0_to_migrate_template"

    def test7_rename_spare(cr, db_name, template):
        assert False

    get_db.create_from_template = test7_create_from_template
    get_db.rename_spare = test7_rename_spare
    assert main_bs(cr, parse_args(args7.values()), db_list) is True
