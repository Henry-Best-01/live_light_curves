


clean: clean-build clean-pyc

clean-build:
    rm -fr build/
    rm -fr dist/
    rm -fr *.egg-info
    rm -fr docs/_build


clean-pyc:
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '__pycache__' -exec rm -rf {} +


test:
    py.test

coverage:
    coverage run --source live_light_curves setup.py test
    coverage report -m
    coverage html
    open htmlcov/index.html

format:
    black .
    docformatter ./* -r --black --in-place

















