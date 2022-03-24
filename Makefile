#
#
#

document_source_root="./doc_sources"
document_output_root="./docs/"

.PHONY: dummy cleanup test init_docs create_docs build_docs cleanup_docs release_test

dummy:
	@echo "make with no args is not supported!"
	@echo "try make {cleanup|test}"

cleanup:
	@./cleanup.sh

init_docs:
	rm -rf ${document_source_root} ${document_output_root}
	mkdir ${document_source_root} ${document_output_root}
	touch ${document_source_root}/.nojekyll
	sphinx-quickstart -q --no-batchfile \
		-p blueprintpy \
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
		./src/blueprintpy \
		"*internal_templates"
	@rm ${document_source_root}/modules.rst
	@rm ${document_source_root}/blueprintpy.rst


build_docs:
	sphinx-build ${document_source_root}/ ${document_output_root}

cleanup_docs:
	rm -rf ${document_output_root}
	mkdir ${document_output_root}
	touch ${document_output_root}/.nojekyll

release_test:
	python3 -m build && python3 -m twine upload --repository testpypi dist/*

test:
	python3 -m unittest discover ./tests
