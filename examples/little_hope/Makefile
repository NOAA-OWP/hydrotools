# Workflow options
PYENV?=venv
PYTHON=$(PYENV)/bin/python3
JUPYTER=$(PYENV)/bin/jupyter
SCRIPT=little_hope.py
NOTEBOOK=little_hope.ipynb
OUTPUTS=peak_histogram.png streamflow.png nwisiv_cache.sqlite

.PHONY: clean

run: $(PYENV)/bin/activate
	$(PYTHON) $(SCRIPT)

notebook: $(PYENV)/bin/activate
	$(JUPYTER) notebook $(NOTEBOOK)

events: $(PYENV)/bin/activate
	$(JUPYTER) notebook little_hope.ipynb

$(PYENV)/bin/activate: requirements.txt
	test -d $(PYENV) || python3 -m venv $(PYENV)
	$(PYTHON) -m pip install -U pip wheel setuptools
	$(PYTHON) -m pip install -r requirements.txt
	touch $(PYENV)/bin/activate

clean:
	rm -rf $(PYENV) $(OUTPUTS)
