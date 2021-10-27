PYENV=env
PYTHON=$(PYENV)/bin/python3
NAMESPACE_DIR := ./python/

PACKAGE := hydrotools
SUBPACKAGES := _restclient[develop] nwis_client[develop] caches[develop] nwm_client_new[develop] events[develop] metrics[develop] nwm_client[gcp,develop]

# discard `extras_require` qualifies from subpackage names (e.g. [develop])
SUBPACKAGES_WITHOUT_EXTRA_REQUIRE = $(shell echo $(SUBPACKAGES) | sed 's|\[[^][]*\]||g')

# relative path to subpackages (e.g. ./python/nwis_client)
SUBPACKAGES_PATHS := $(addprefix $(NAMESPACE_DIR), $(SUBPACKAGES))

.PHONY: help all-tests tests install uninstall develop clean

help:
	    @echo "HydroTools makefile commands:"
	    @echo "  install : install all subpackages from local source code"
	    @echo "  develop : install all subpackages in editable mode (pip -e) from local source code"
	    @echo "  tests : run unit tests. exclude tests marked as slow"
	    @echo "  all-tests : run all unit tests"
	    @echo "  uninstall : uninstall all subpackages"
	    @echo "  clean : delete python virtual environment"
		@echo
		@echo "  utility requirements:"
		@echo "    pip > 21.1"
		@echo "    sed"

.DEFAULT_GOAL := help

tests: install
	$(PYTHON) -m pytest -s -m "not slow"

all-tests: install
	$(PYTHON) -m pytest -s

install: $(PYENV)/bin/activate
	$(PYTHON) -m pip install --use-feature=in-tree-build $(SUBPACKAGES_PATHS)

uninstall: $(PYENV)/bin/activate
	$(PYTHON) -m pip uninstall -y $(addprefix $(PACKAGE)., $(SUBPACKAGES_WITHOUT_EXTRA_REQUIRE))

develop: $(PYENV)/bin/activate
	$(PYTHON) -m pip install --use-feature=in-tree-build --editable $(SUBPACKAGES_PATHS)


$(PYENV)/bin/activate:
	test -d $(PYENV) || python3 -m venv $(PYENV)
	$(PYTHON) -m pip install -U pip wheel setuptools build pytest
	touch $(PYENV)/bin/activate

clean:
	rm -rf $(PYENV)
