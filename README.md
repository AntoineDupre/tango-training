Build
====


Build rpm package from jenkins
----
[Jenkins job](http://w-v-ci-0.maxiv.lu.se/job/dev-maxiv-tangotraining-testing)


Build using setup.py
----
python setup build



Test
====
Run with setup.py:
```bash
$ python3 setup.py test
```

Add extra test argument:
```bash
$ python3 setup.py --addopts "--verbose"
```

Installation
=======

Install from maxiv rpm repository
--------
```bash
$ sudo yum makecache --enablerepo=maxiv-testing
$ sudo yum install tangods-training --enablerepo=maxiv-testing
```


Install from sources in the user space:
----
```bash
$ python setup.py install --user
```
