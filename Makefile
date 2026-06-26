.PHONY: install demo serve clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

demo: install
	$(PYTHON) -m search index --docs ./sample_docs
	$(PYTHON) -m search query "distributed consensus algorithms"

serve: install
	$(PYTHON) -m search serve --port 8000

clean:
	rm -rf .venv index.json __pycache__ **/__pycache__
