    #!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'requests',
]

test_requirements = [
    'requests-mock'
]

setup(
    name='pyactiviti',
    version='0.1.0',
    description="An SDK that helps with interacting with Activiti.",
    long_description=readme + '\n\n' + history,
    author="Stephane Wirtel",
    author_email='stephane@wirtel.be',
    url='https://github.com/matrixise/pyactiviti',
    packages=[
        'pyactiviti',
    ],
    package_dir={'pyactiviti':
                 'pyactiviti'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='pyactiviti',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
