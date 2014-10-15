clean:
	rm -rf venv build dist tutum.egg-info
	find . -name '*.pyc ' -delete

test:clean
	set -x
	virtualenv venv
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install mock nose
	venv/bin/pip install .
	venv/bin/python setup.py nosetests
