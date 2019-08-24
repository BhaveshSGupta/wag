import sys
import argparse
import os

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

	def __init__(self, path, force=False):
		self.worktree = path
		self.gitdir = os.path.join(path, ".git")


def repo_create(path):
	"""Create a new repository at path."""
	repo = GitRepository(path)
	if os.path.exists(repo.worktree): # We check whether there exsits a path of worktree
		if not os.path.isdir(repo.worktree):# if path exsits its a directory or not
			raise Exception("%s is not a directory!" % path)
		if os.listdir(repo.worktree):# if path exsits its empty or not
			raise Exception("%s is not empty!" % path)
	else:
		os.makedirs(repo.worktree) # Create directory as nothing exist with same path
