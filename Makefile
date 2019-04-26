SRCPATH="src"

.PHONY: clean
clean: check-env
	cd $(SRCPATH) \
		&& rm -rf build package.zip

.PHONY: test
test: check-env
		pipenv install \
        && pipenv run python -m unittest discover -s src/

.PHONY: check-env
check-env:
	ifndef SRCPATH
		$(error SRCPATH is undefined)
	endif
		@if [ ! -d $(SRCPATH) ]; then \
			echo $(SRCPATH) does not exist; \
			exit 1; \
	fi
.PHONY: run-local
run-local:
	set -o allexport \
	&& python $(SRCPATH)/server.py \
	&& set +o allexport 