# Git-Flow

This document briefly outlines the git workflow used to make additions, changes, and
deletions of content on this repo. In general we used a three step process:

1. Fork
2. Branch
3. Pull Request

The subsequent sections will outline these steps and discuss how to synchronize your
fork with the upstream repo.

## Getting Started

Begin by creating a fork of the repository ([official GitHub docs on
forking](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo)).
This is done by clicking the fork button in the upper right hand corner while on the
GitHub web ui. This will effectively create a copy of the repo under your user
account.

Next, navigate to your fork and create a local clone (copy) of the repo. This is done
on the command line.

```bash
git clone https://github.com/<your-username>/evaluation_tools
cd evaluation_tools
```

Next, if you haven't already, you'll need to configure `git` to know who you are. You
can either do this globally, meaning you do it once and these settings will be
default for all other `git` repos in the future, or locally meaning just change the
settings for this repo. Here we will do it globally.

```bash
git config --global user.name "<First Name> <Last Name>"
git config --global user.email "<your>@<email>"
```

Lastly, it will be helpful in the future to pull commits from the upstream
repository, in this case `NOAA-OWP/evaluation_tools`. Right now the local cloned
repository only knows about the remote fork under your username (you can check this
using `git remote --verbose`).
Add an upstream remote that points to `NOAA-OWP/evaluation_tools` using:

```bash
git remote add upstream git@github.com:NOAA-OWP/evaluation_tools.git
```

## Branching

Now that a local clone of your fork has been made, to commit changes, you'll want to
open a feature branch. To do so run:

```bash
git checkout -b <feature-branch-name>
```

It's important to note that when creating a branch, the starting point of the created
branch is the last commit from the branch you were last on. Diagrammatically:

```bash
      / <feature-branch-name> commit 3
main | commit 3
     | commit 2
     | commit 1
```

## Committing changes

Now that the feature branch has been created, its safe to make changes. Do so using:

```bash
git add <some-file-name>
git commit -m "<a human readable and meaningful commit message>"

# Push changes up to origin remote (aka your fork)
git push origin <feature-branch-name>
```

## Opening a Pull Request

Now that you've made changes to the feature branch and pushed them to your origin
remote (fork), its time to open a PR to start the process of adding your changes to
the official `NOAA-OWP/evaluation_tools` repo.

This step is done on the GitHub site, so open a browser and navigate to your fork.
Next, select _Pull requests_ from the ribbon, then _New pull request_. You should be
greeted with a dialog asking to compare changes. Simply this is asking, what changes
on your fork do you want to compare with the official `NOAA-OWP/evaluation_tools`. On
the right side, click the dropdown menu labeled _compare_ and find the feature branch
you pushed up to the origin. You should see a new dialog appear that looks similar to
a GitHub issue form. Fill out the information and click open pull request.

## Syncing your fork

Inevitably there will come a time when the `NOAA-OWP/evaluation_tools` `main` branch
is ahead of your forks main branch. That's okay, but this means that you wont have
the latest work on your fork. This is important because if you are to start new work,
**you should always base it off the newest work on main**.

To update your fork, from the command line do the following:

```bash
# switch to main branch on your fork
git checkout main # if you have any unstaged changes you will need to deal with those first. See `git stash`

# Fetch latest data from upstream remote
git fetch upstream

# Put those changes on top of your local main's using a rebase
git rebase upstream/main

```

## Cleanup

If you have local branches that are no longer needed (list all branches using `git branch`) once they have made their way into the remote tracked development branch,
you can remove them with `git branch -D <branch>`.
