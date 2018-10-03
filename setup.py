# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def readme():
    with open('README.txt') as f:
        return f.read()


version = '1.3.1'


setup(
    name='django-recaptcha2',
    packages=find_packages(exclude=['samples']),
    # package_data={'': ['']},
    include_package_data=True,
    version=version,
    install_requires=[
        'requests'
    ],
    tests_require=(
        ['django-setuptest'],
    ),
    test_suite='setuptest.setuptest.SetupTestSuite',
    description='Django reCaptcha v2 field/widget',
    long_description=readme(),
    author='Andrea Briganti',
    author_email='kbytesys@gmail.com',
    url='https://github.com/kbytesys/django-recaptcha2',
    download_url='https://github.com/kbytesys/django-recaptcha2/tarball/v%s' % version,
    keywords=['django', 'recaptcha', 'recaptcha2'],
    license='GNU LGPL v2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
