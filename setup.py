from setuptools import setup
import os
import ast
HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='huey'):
    """Get version."""

    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()
    lines = data.split('\n')
    for line in lines:
        if line.startswith('VERSION_INFO'):
            version_tuple = ast.literal_eval(line.split('=')[-1].strip())
            version = '.'.join(map(str, version_tuple))
            break
    return version


setup(
    name='huey',
    version=get_version(),
    packages=['huey'],
    url='https://github.com/aerispaha/van-data-logging/',
    license='',
    author='Adam Erispaha',
    author_email='aerispaha@gmail.com',
    description='tools for data logging in the campervan'
)
