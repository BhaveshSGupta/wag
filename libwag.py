import sys
import argparse
import os
import configparser

argparser = argparse.ArgumentParser(description="Another Content Tracker")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True
argsp = argsubparsers.add_parser(
    "init", help="Initialize a new, empty repository.")
argsp.add_argument("path", metavar="directory", nargs="?",
                   default=".", help="Where to create the repository.")


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    if args.command == "init":
        cmd_init(args)


def cmd_init(args):
    repo_create(args.path)


class GitRepository(object):
    """A git repository"""
    worktree = None
    gitdir = None

    def __init__(self, path):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")


def repo_create(path):
    """Create a new repository at path."""
    repo = GitRepository(path)
    # We check whether there exsits a path of worktree
    if os.path.exists(repo.worktree):
        # if path exsits its a directory or not
        if not os.path.isdir(repo.worktree):
            raise Exception("%s is not a directory!" % path)
        # if path exsits its empty or not
        if os.listdir(repo.worktree):
            raise Exception("%s is not empty!" % path)
    else:
        # Create directory as nothing exist with same path
        os.makedirs(repo.worktree)
        repo_path(repo, "branches")
    
    assert(repo_dir(repo, "branches", mkdir=True))
    assert(repo_dir(repo, "objects", mkdir=True))
    assert(repo_dir(repo, "refs", "tags", mkdir=True))
    assert(repo_dir(repo, "refs", "heads", mkdir=True))

    with open(repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")
    
    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)

def repo_dir(repo, *path, mkdir=False):
    # repo is for our repository object as we want to work with repository.
    # *path is the path we want to check
    # mkdir to specify whether we want to create directory or not.

    # this function would give us path we want to check if it exist or not
    path = repo_path(repo, *path)

    # This would check whether path exists and if it does then it would check if it is a direcoty or not
    if os.path.exists(path):
        if (os.path.isdir(path)):
            return path
        else:
            raise Exception("Not a directory %s" % path)

    # This would check if we need to create directory as it doesn't exsits
    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None


def repo_path(repo, *path):
    # This would return us path under repository git directory
    return os.path.join(repo.gitdir, *path)

def repo_file(repo, *path, mkdir=False):

    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)

def repo_default_config():
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")

    return ret