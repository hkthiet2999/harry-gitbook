from setuptools import setup, find_packages

VERSION = '1.0.1'

setup(
    name="mkdocs-gitbook",
    version=VERSION,
    url='https://github.com/smoothkt4951/harry-gitbook',
    license='Apache License, Version 2.0',
    description='Harry Gitbook using GitBook and Mkdocs',
    author='Harry Hoang',
    author_email='smoothkt4951@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'gitbook = mkdocs_gitbook',
        ]
    },
    zip_safe=False
)
