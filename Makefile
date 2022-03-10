#
#
#

.PHONY: dummy cleanup test

dummy:
	@echo "make with no args is not supported!"
	@echo "try make {cleanup|test}"

cleanup:
	@echo "Cleaning..."
	rm -rf ./build
	rm -rf ./**/*.egg-info
	rm -rf ./**/*.dist-info
	rm -rf ./**/__pycache__

test:
	python3 -m unittest discover ./tests
