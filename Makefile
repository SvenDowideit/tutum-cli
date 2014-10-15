clean:
	rm -rf venv build dist tutum.egg-info
	rm -f *.tar.gz
	find . -name '*.pyc ' -delete

prepare:clean
	set -ex
	virtualenv venv
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install .

test:prepare
	venv/bin/pip install mock nose
	venv/bin/python setup.py nosetests

certs:
	curl http://ci.kennethreitz.org/job/ca-bundle/lastSuccessfulBuild/artifact/cacerts.pem -o cacert.pem

build_osx:prepare
	if [ ! -f cacert.pem ]; then make certs; fi
	venv/bin/pip install pyinstaller
	venv/bin/pyinstaller tutum.spec -y
	mv dist/tutum tutum
	tutum/tutum -v
	tar zcvf tutum-Darwin-x86_64.tar.gz tutum
	rm -rf tutum
	mv tutum-Darwin-x86_64.tar.gz dist/tutum-Darwin-x86_64.tar.gz
