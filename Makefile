SRCPATH="src"

.PHONY: install
install:
	pipenv install --all

.PHONY: test
test:
	pipenv install \
	&& pipenv run python -m unittest discover -s src/ \
	&& pipenv uninstall --dev

.PHONY: run-local
run-local:
	set -o allexport \
	&& FLASK_APP='src:create_app()' FLASK_ENV=development pipenv run flask run \
	&& set +o allexport 