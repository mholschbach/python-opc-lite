# install GNU make to run make
MAKE = make

help:
	@echo "make <OPTIONS>"
	@echo OPTIONS:
	@echo "  help"
	@echo "  test"
	@echo "  mypy"
	@echo "  docclean"
	@echo "  docapidoc"
	@echo "  dochtml"
	@echo "  clean"
	@echo "  setup"
	@echo "  build"
	@echo "  testupload"
	@echo "  upload"

.PHONY = help, test, docclean, docapidoc, dochtml, clean, setup, build, testupload, upload, tox

test:
	poetry run pytest --cov-report term-missing --cov-report html --cov-branch --cov src

mypy:
	poetry run mypy src

docclean:
	$(MAKE) -C docs clean

docapidoc:
	sphinx-apidoc -o ./docs/source -e ./src/opc
	$(MAKE) dochtml

dochtml:
	$(MAKE) docclean
	$(MAKE) -C docs html

clean:
	rm -rf "dist"
	rm -rf .tox

setup:
	pip install -e .[docs,tests,dists]
	pip uninstall -y python-opc-lite

build:
	$(MAKE) clean
	python -m build

testupload:
	twine upload -r testpypi dist/*

upload:
	twine upload dist/*

tox:
	$(MAKE) clean
	tox
