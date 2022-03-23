#
#
#

document_source_root="./doc_sources"
document_output_root="./docs/"

.PHONY: dummy cleanup test init_docs create_docs build_docs

dummy:
	@echo "make with no args is not supported!"
	@echo "try make {cleanup|test}"

cleanup:
	@echo "Cleaning..."
	rm -rf ./build
	rm -rf ./**/*.egg-info
	rm -rf ./**/*.dist-info
	rm -rf ./dist
	zsh -c "rm -rf ./**/__pycache__"; exit 0

init_docs:
	rm -rf ${document_source_root} ${document_output_root}
	mkdir ${document_source_root} ${document_output_root}
	touch ${document_source_root}/.nojekyll
	sphinx-quickstart -q --no-batchfile \
		-p pip_init \
		-a Enchan1207 \
		-r v1.0.0 \
		-l ja \
		--extensions="sphinx.ext.autodoc,sphinx.ext.napoleon" \
		${document_source_root}

create_docs:
	@sphinx-apidoc \
		--force --module-first -d 1 \
		--templatedir="${document_source_root}/_templates" \
		-o ${document_source_root} \
		./src/ \
		"**/pip_init_internal_templates"
	@rm ${document_source_root}/modules.rst


build_docs:
	sphinx-build ${document_source_root}/ ${document_output_root}

release_test:
	python3 -m build && python3 -m twine upload --repository testpypi dist/*

test:
	python3 -m unittest discover ./tests
