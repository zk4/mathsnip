
rm:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -type d -iname '*egg-info' -exec rm -rdf {} +
	rm -f .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	# rm -rf .py.egg-info
	rm -rf .pytest_cache
	rm -rf .hypothesis
	rm -rdf assets


install: uninstall
	pip3 install .

uninstall:
	pip3 uninstall  -y mathsnip

main:
	python3 main.py eat -c 2

run:
	python3 -m mathsnip eat -c 2

wrun:
	watchexec -ce py 'python3 -m mathsnip eat -c 2'

all: rm uninstall install run


pure-all: env-rm rm env install test run



upload-to-test: rm freeze
	python3 setup.py bdist_wheel --universal
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*


upload-to-prod: rm freeze
	python3 setup.py bdist_wheel --universal
	twine upload dist/*


freeze: auto_version
	# pipreqs will find the module the project really depneds
	# Don`t use this !
	pipreqs . --force

freeze-env: auto_version
	#  pip3 will find all the module not belong to standard  library
	pip3 freeze > requirements.txt


env-rm:
	rm -rdf venv

env-create:
	python3 -m venv venv

env: env-create
	pip3 install -r requirements.txt

source:
	echo "you need to manully source it"
	echo ". env/bin/activate"
	. venv/bin/activate

auto_version:
	# python version.py
	echo "hello"

dev:
	pip install -e .
key:
	python3 -m mathsnip


