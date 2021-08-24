PYENV=env
PYTHON=$(PYENV)/bin/python3
NAMESPACE_DIR := ./python/

PACKAGE := hydrotools
SUBPACKAGES := _restclient[develop] nwis_client[develop] caches[develop] nwm_client[gcp,develop] events[develop] metrics[develop]

# discard `extras_require` qualifies from subpackage names (e.g. [develop])
SUBPACKAGES_WITHOUT_EXTRA_REQUIRE = $(shell echo $(SUBPACKAGES) | sed 's|\[[^][]*\]||g')

# relative path to subpackages (e.g. ./python/nwis_client)
SUBPACKAGES_PATHS := $(addprefix $(NAMESPACE_DIR), $(SUBPACKAGES))

.PHONY: all-tests tests install clean

tests: install
	$(PYTHON) -m pytest -s -m "not slow"

all-tests: install
	$(PYTHON) -m pytest -s

install: $(PYENV)/bin/activate
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/_restclient[develop]
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/nwis_client[develop]
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/caches[develop]
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/nwm_client[gcp,develop]
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/events[develop]
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/metrics[develop]

$(PYENV)/bin/activate:
	test -d $(PYENV) || python3 -m venv $(PYENV)
	$(PYTHON) -m pip install -U pip wheel setuptools build pytest
	touch $(PYENV)/bin/activate

clean:
	rm -rf $(PYENV)
