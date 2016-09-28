INSTALL
=======

Install dependencies and copy or symlink executables into your $PATH

```
    $ pip3 install -r requirements.txt
    $ ln -s $PWD/git-phab ~/.local/bin/
```

Optionaly generate and copy or symlink manpage into your $MANPATH

```
  $ a2x --doctype manpage --format manpage git-phab.txt
  $ ln -s $PWD/git-phab.1 ~/.local/share/man/man1/
```

Optionaly enable bash completion:

```
  $ sudo activate-global-python-argcomplete3
```

And add this in your ~/.bash_completion:

```
  function _git_phab()
  {
    COMP_WORDS=(git-phab ${COMP_WORDS[@]:2})
    COMP_CWORD=$((COMP_CWORD - 1))
    COMP_LINE=${COMP_LINE/git phab/git-phab}
    _python_argcomplete_global git-phab
  }
```

REQUIREMENTS
============

See requirements.txt

DESCRIPTION
===========

Git subcommand to integrate with phabricator.

WORKFLOW EXAMPLE
================

First, specify a personal remote repository where to push WIP branches:

```
  $ git config phab.remote xclaesse
```

Make sure the fetch URL of the repository can be accessed by the reviewers. For example if your remote is called `github`:

```
  $ git remote show github | grep URL
    Fetch URL: git@github.com:NICK/PROJECT.git
    Push  URL: git@github.com:NICK/PROJECT.git
  $ git remote set-url github https://github.com/NICK/PROJECT.git
  $ git remote set-url --push github git@github.com:NICK/PROJECT.git
  $ git remote show github | grep URL
    Fetch URL: https://github.com/NICK/PROJECT.git
    Push  URL: git@github.com:NICK/PROJECT.git
```

Before starting your work, create a branch:

```
  $ git checkout -b fix-bugs origin/master
  Branch fix-bugs set up to track remote branch master from origin.
  Switched to a new branch 'fix-bugs'
```

Note that is it important to set the tracking remote branch, git-phab will use
it to set the default commit range to attach.

Now fix your bugs...

When the branch is ready for review, attach it (requesting the creation of a
new task):

```
  $ git phab attach --task
  Using revision range 'origin/master..'
  a3beba9 — Not attached — Truncate all_commits when filtering already proposed commits
  Attach above commits and create a new task? [yn] y
  (...)
  Push HEAD to xclaesse/wip/phab/T3436-fix-bugs? [yn] y
  Create and checkout a new branch called: T3436-fix-bugs? [yn] y

  Summary:
  New: task T3436
  New: 66b48b9 — D483 — Truncate all_commits when filtering already proposed commits
  Branch pushed to xclaesse/wip/phab/T3436-fix-bugs
  Branch T3436-fix-bugs created and checked out
```

Note that the current branch name wasn't starting with a task ID, so it proposed
to create a new one. If you already had a task for it, just pass `--task`
option. But it created a new branch prefixed with the task ID so future git-phab
commands will know which task this branch refers to:

```
  $ git branch
  * T3436-fix-bugs
    fix-bugs
    master
```

When your commits have been accepted, merge them:


```
  $ git checkout master
  $ git merge T3436-fix-bugs
  $ git phab land
  66b48b9 — D483 Accepted — Truncate all_commits when filtering already proposed commits
  Do you want to push above commits? [yn] y
  Do you want to close 'T3436'? [yn] y
```

You can now cleanup your branches:

```
  $ git phab clean
  Task 'T3436' has been closed, do you want to delete branch 'T3436-fix-bugs'? [yn] y
    -> Branch T3436-fix-bugs was deleted
  Task 'T3436' has been closed, do you want to delete branch 'xclaesse/wip/phab/T3436-fix-a-bug'? [yn] y
    -> Branch xclaesse/wip/phab/T3436-fix-a-bug was deleted
```
