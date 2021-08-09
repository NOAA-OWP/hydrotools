# Adding subpackage to gh-pages deployment

## Getting started

1. Start by first creating a fork of the repo. This will create a personal clone of the
   repository under your username.
2. Make a local clone of your fork using `git clone https://github.com/<your-user-name>/hydrotools` on the command line.
3. Change directories your local copy using `cd hydrotools` from the command line.
   1. If you have not setup `git` before, you'll need to tell `git` your name and
      email. To set these options globally use `git config --global user.name "Your Name"`, then `git config --global user.email "your@email.com"`. You can do this locally instead using `git config --local`.
4. Create a new branch to add work to using `git checkout -b sphinx-docs`. Now we can move onto the installation.

## Installation

We recommend using a virtual environment. Use the virtual environment manager of
choice, here we will use anaconda.

### Required packages

- `Sphinx`
- `furo` this is the `sphinx` theme used.
- `hydrotools`

```python
# Create virtual environment
conda create --name hydrotools-sphinx-docs python=3.8 -y

# activate the virtual environment
conda activate hydrotools-sphinx-docs

# Install dependencies. This assumes you are in the hydrotools root directory
pip install .
pip install Sphinx furo
```

## Building the docs

To build the docs, it helpful to first know the process. All `hydrotools`
documentation is build using [`Sphinx`](https://www.sphinx-doc.org/en/master/). Its
helpful to note that `Sphinx` by default uses reStructured text its another markup
language like markdown. For `Sphinx` to _know_ about code we want to add to
gh-pages, its necessary to create bindings so `Sphinx` can go and create
documentation automagically. Lastly, before pushing any changes to the fork, a small
amount of house keeping is required to adjust the bindings `Sphinx` generated.

### Generating the bindings

Bindings are generated using `sphinx-apidoc`. The example below created bindings for
the `nwm_client` and outputs them in the `docs/` directory.

```python
# Create bindings without a table of contents (toc), include private modules (start with _)
# separate all modules into individual rst files, tell sphinx-apidoc that the
# package is a namespace style package, output the bindings in docs/, generate bindings
# for nwm_client, and ignore files that include the word test.
sphinx-apidoc --no-toc --private --separate --implicit-namespaces -o docs/ python/nwm_client/src/hydrotools "*test?*"
```

After running this, a few files should appear in the `docs/` directory. The one named
`hydrotools.nwm_client.rst` is the package level file, there should be other
appended with module names like `hydrotools.nwm_client.nwm.rst` for example. If
the subpackage only has one file, you may just see one new binding, that's okay.

Next, open the package level file, in this case `hydrotools.nwm_client.rst`.
The top should look something like the following:

```rst
evaluation\_tools.nwm\_client package
=====================================

Submodules
----------
```

All that is required is the word _package_ be replaced with _subpackage_, so
`evaluation\_tools.nwm\_client subpackage`.

Lastly, its required that the package level file be referenced in `docs/index.rst`. You do
this by simply adding the filename without the extension to list of other modules
under the `.. toctree:` header.

So, this:

```rst
.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: API:

   hydrotools.nwis_client
   hydrotools._restclient
```

Becomes this:

```rst
.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: API:

   hydrotools.nwis_client
   hydrotools._restclient
   hydrotools.nwm_client
```

## Verify that documentation was added properly

To check that the subpackage bindings were added to `Sphinx`, from the `docs/`
directory, run `make html`. This will build an `html` form of the documents. To view
them, navigate to and open `docs/_build/html/index.html` using your web browser of
choice.

## Push your changes to your fork

Run `git status` to see which files have been added/modified/deleted. Use `git add <filename>` to add each added/modified file to the staging area. Next, use `git commit -m "<type a human readable commit message>"` to add a commit message. Lastly,
use `git push origin <the-name-of-your-branch>` to push your changes to the remote.
From here, you can navigate to your fork on GitHub.com and open a pull request to
request your changes be pulled into official repository.
