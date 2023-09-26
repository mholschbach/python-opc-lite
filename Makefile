# install GNU make to run make

help:
	@echo "make <OPTIONS>"
	@echo OPTIONS:
	@echo "  help"
	@echo "  test"

.PHONY = help, test

test:
	pytest -s -v  tests/
