pre-commit-init:
	pre-commit uninstall && \
	pre-commit install && \
	pre-commit autoupdate && \
	pre-commit install --hook-type commit-msg -f
start-test:
	coverage run -m pytest;coverage html;open htmlcov/index.html
