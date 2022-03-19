#
#
#

.PHONY: dummy cleanup test init_docs create_docs build_docs

dummy:
	@echo "make with no args is not supported!"
	@echo "try make {cleanup|test}"

cleanup:
	@echo "Cleaning..."
	rm -rf ./build
	rm -rf ./**/*.egg-info
	rm -rf ./**/*.dist-info
	zsh -c "rm -rf ./**/__pycache__"

init_docs:
	rm -rf docs
	mkdir docs
	sphinx-quickstart -q --no-batchfile \
		-p pip_init \
		-a Enchan1207 \
		-r v1.0.0 \
		-l ja \
		--extensions="sphinx.ext.autodoc,sphinx.ext.napoleon" \
		./docs

create_docs:
	sphinx-apidoc -e -f -o ./docs .

build_docs:
	sphinx-build ./docs/ ./docs/_build/

test:
	python3 -m unittest discover ./tests
