from distutils.core import setup

setup(
    name='mongoprof',
    version='0.2.0',
    author='James Turk',
    author_email='jturk@sunlightfoundation.com',
    url='http://github.com/sunlightlabs/mongoprof',
    scripts=['mongoprof.py'],
    license='BSD',
    description='command line tool for watching mongodb queries',
    long_description=open('README.rst').read(),
    install_requires=['pymongo', 'termcolor'],
)
