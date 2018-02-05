from setuptools import setup


setup(
    name='tangods-training',
    version='0.1.0.dev0',
    packages=['training'],
    author='S',
    author_email='',
    license="GPLv3",
    description=('Dummy tango device from the tango training kits cafe'),
    install_requires=['pytango'],
    tests_require=['pytest',
                    'pytest-xdist'],
    setup_requires=['pytest-runner']
)
