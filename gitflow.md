# MaaS Git-Flow

## Getting Started

Begin by making a local copy of the repository
`git clone https://github.com/jarq6c/evaluation_tools`

Don't forget to ensure identity is set properly, by default, git doesn't configure e-mail addresses well!  You can set your machines global policy using

    git config --global user.name "Jane Doe"
    git config --global user.email "jane@doe.org"

If you only want to make name and e-mail changes for _this_ newly cloned repository then use

	cd evaluation_tools
    git config user.name "John Doe"
    git config user.email "john@doe.org"

Local development is left to developer preference, but all development should sync with the upstream development branch frequently.  This guide shows the process using local development “feature” branches, but ultimately, changes should end up on development, synced upstream, and then pushed to the development branch upstream with as much commit history as is meaningful (minimal merge commits).

## Synchronizing

To sync a single upstream branch and pull all the upstream changes into your working tree:

`git fetch <branch>; git checkout <branch>; git rebase origin/<branch>;`
OR
`git checkout <branch>; git pull --rebase`
OR
`git pull origin <branch> --rebase`

## Development
To get started with some feature development, create a local branch and check it out

	git checkout develop
    git branch featureA
    git checkout featureA
OR
`git checkout -b featureA develop`

Development work should commit frequently when changes are complete and meaningful.  If work requires modifying more than one file in the source, it is recommended to commit the changes independently to help avoid too large of conflicts if the occur.

### Commits

When changes are made to a file and ready for committing, then use these git commands

    git add <file>
    git commit -m “meaningful commit message here”
    
If multiple files need to be associated with a single commit (this should be rare) then you can add multiple files with
`git add <file1> <file2> <fileN>`

Use `git status` to see what files are modified but not committed.

### Rebasing

When work is ready to be shared upstream, it should be synced with the upstream development branch.  This should be done frequently, even if the work isn’t complete.  This will help minimize potential conflicts.  To prepare for moving work upstream, first make sure the local repository is synced (see above instructions for [Synchronizing](#synchronizing).)

Next we want to rebase the new work onto the development branch. To rebase local changes:

    git checkout featureA
    git rebase develop

OR 
`git rebase develop featureA`

Once the rebase is complete and conflicts are resolved, the develop branch can be fast forwarded to include all the local changes.  This is done by

	git checkout develop
	git merge featureA --ff

### Interactive rebasing

This is a good time to tidy up and clean up the local development work, and interactive rebasing is a good idea here.  Just use `git rebase -i` in place of the `git rebase` commands above (the other arguments stay the same.)

In interactive rebasing, you have the opportunity to drop commits, squash multiple together into a more logical patch, or even edit commits by splitting them up into multiple commits.  For more on the power of interactive rebasing, browse the internet.  A great place to get familiar with git flows and rebasing is [https://learngitbranching.js.org](https://learngitbranching.js.org/)

### Pushing Upstream

Once local work has been rebased onto the synchronized development branch, push those changes upstream to share the work.
`git push origin develop`

### Cleanup

If you have local branches that are no longer needed once they have made their way into the remote tracked development branch, you can remove them with
`git branch -d <branch>`

## General rebase reference

A quick synopsis of local rebasing to manage local branches is provided here

**Add commits from branch B to the end of branch A**
`git rebase A B`
To sync both to same commit, invert the rebase or merge
`git rebase B A` OR `git checkout A; git merge B`

**sync two branches very explicitly**

    git checkout B
    git rebase A
sync both to same commit:

    git checkout A
    git rebase B

OR `git merge B --ff`


> Written with [StackEdit](https://stackedit.io/).
