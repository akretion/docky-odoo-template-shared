#!/usr/bin/env python

from plumbum import local
from sys import stderr

DEFAULT_VERSION = "0.0.0"


def current_git_tag():
    bin = local.path("../last_git_tag.sh")
    if not bin.exists():
        print("Can't find current_git_tag.sh", file=stderr)
    return bin


def create_a_git_dir():
    # assume we are already in the dir
    local["git"]["init"]()


def git_touch_and_add(somefile):
    # touch and add a file
    local["touch"][somefile]()
    local["git"]["add", somefile]()
    local["git"]["commit", "-m", somefile]()


def git_tag(tagname):
    """add tag"""
    local["git"]["tag", tagname]()


def test_current_git_tag_empty():
    """in case no git tag yet on the project"""
    bin = current_git_tag()
    with local.tempdir() as tmpdir:
        with local.cwd(tmpdir):
            create_a_git_dir()
            git_touch_and_add("somefile")
            cmd = local[bin]
            ret = cmd()
            # strip \n
            assert ret.strip() == DEFAULT_VERSION

            # now provide a default arg
            cmd = local[bin]["16.0.0"]
            ret = cmd()
            assert ret.strip() == "16.0.0"


def test_current_git_tag_empty_other_branch():
    """in case no git tag yet on the current branch
    but present in another"""
    bin = current_git_tag()
    with local.tempdir() as tmpdir:
        with local.cwd(tmpdir):
            create_a_git_dir()
            git_touch_and_add("somefile")
            local["git"]["checkout", "-b", "current-branch"]()
            local["git"]["checkout", "-b", "some-other-branch"]()
            git_touch_and_add("someotherfile")
            git_tag("16.0.0")
            # go back in previous branch
            local["git"]["checkout", "current-branch"]()

            cmd = local[bin]
            ret = cmd()
            # strip \n
            assert ret.strip() == DEFAULT_VERSION


def test_current_git_tag_increment():
    bin = current_git_tag()
    with local.tempdir() as tmpdir:
        with local.cwd(tmpdir):
            create_a_git_dir()
            git_touch_and_add("somefile")
            git_tag("16.0.0")

            cmd = local[bin]
            ret = cmd()
            # strip \n
            assert ret.strip() == "16.0.0"

            git_touch_and_add("someotherfile")
            git_tag("16.0.1")

            cmd = local[bin]
            ret = cmd()
            # strip \n
            assert ret.strip() == "16.0.1"


def test_current_git_tag_mulitple():
    # ensure to always return the last tag
    # even if there are two tags on the same
    # commit
    bin = current_git_tag()
    with local.tempdir() as tmpdir:
        with local.cwd(tmpdir):
            create_a_git_dir()
            git_touch_and_add("somefile")
            git_tag("16.0.0")
            cmd = local[bin]
            ret = cmd()
            # strip \n
            assert ret.strip() == "16.0.0"

            git_tag("16.0.1")
            cmd = local[bin]
            ret = cmd()
            # strip \n
            assert ret.strip() == "16.0.1"

            # create tag in opposit order
            git_tag("16.0.4")
            cmd = local[bin]
            ret = cmd()
            # strip \n
            assert ret.strip() == "16.0.4"

            git_tag("16.0.3")
            cmd = local[bin]
            ret = cmd()
            # strip \n
            assert ret.strip() == "16.0.4"
