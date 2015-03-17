clean:
	rm -rf venv build dist tutum.egg-info python-tutum*
	rm -f *.tar.gz
	find . -name '*.pyc ' -delete

prepare:clean
	set -ex
	virtualenv venv
	export SDK_VER=$(shell cat requirements.txt | grep python-tutum | grep -o '[0-9.]*') && curl -0L https://github.com/tutumcloud/python-tutum/archive/v$${SDK_VER}.tar.gz | tar -zxv && venv/bin/pip install python-tutum-$${SDK_VER}/. && rm -rf python-tutum-$${SDK_VER}
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install .

test:prepare
	venv/bin/pip install mock nose
	venv/bin/python setup.py nosetests

retest:
	venv/bin/python setup.py nosetests

certs:
	curl http://ci.kennethreitz.org/job/ca-bundle/lastSuccessfulBuild/artifact/cacerts.pem -o cacert.pem

build-osx:prepare
	if [ ! -f cacert.pem ]; then make certs; fi
	venv/bin/pip install pyinstaller
	venv/bin/pyinstaller tutum.spec -y
	mv dist/tutum tutum
	tutum/tutum -v
	tar zcvf tutum-Darwin-x86_64.tar.gz tutum
	rm -rf tutum
	mv tutum-Darwin-x86_64.tar.gz dist/tutum-Darwin-x86_64.tar.gz

publish-osx:build-osx
	venv/bin/pip install awscli
	venv/bin/aws s3 cp dist/tutum-Darwin-x86_64.tar.gz s3://files.tutum.co/packages/tutum-cli/Darwin/x86_64/tutum-`cat tutumcli/__init__.py |grep version | grep -o "\'.*\'" | sed "s/'//g"`.tar.gz --acl public-read

publish-pypi:prepare
	python setup.py sdist upload
