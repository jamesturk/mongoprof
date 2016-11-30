from distutils.core import setup

setup(
    name='mongoprof',
    version='0.3.0',
    author='James Turk',
    author_email='james.p.turk@gmail.com',
    url='http://github.com/jamesturk/mongoprof',
    scripts=['mongoprof.py'],
    license='BSD',
    description='command line tool for watching mongodb queries',
    long_description=open('README.md').read(),
    install_requires=['pymongo<3', 'termcolor'],
)
