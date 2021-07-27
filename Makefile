PYENV=env
PYTHON=$(PYENV)/bin/python3

.PHONY: all-tests tests install clean

tests: install
	$(PYTHON) -m pytest -s -m "not slow"

all-tests: install
	$(PYTHON) -m pytest -s

install: $(PYENV)/bin/activate
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/_restclient[develop]
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/nwis_client[develop]
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/caches[develop]
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/gcp_client[develop]
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/events[develop]
	$(PYTHON) -m pip install --use-feature=in-tree-build ./python/metrics[develop]

$(PYENV)/bin/activate:
	test -d $(PYENV) || python3 -m venv $(PYENV)
	$(PYTHON) -m pip install -U pip wheel setuptools build pytest
	touch $(PYENV)/bin/activate

clean:
	rm -rf $(PYENV)
