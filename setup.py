from setuptools import setup, find_packages
import os
import uwsgiit

CLASSIFIERS = [
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    author="Riccardo Magliocchetti",
    author_email="riccardo.magliocchetti@gmail.com",
    name='uwsgiit-py',
    version=uwsgiit.__version__,
    description='Library for uwsgi.it api',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    url="https://github.com/xrmx/uwsgiit-py",
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'requests>=2',
    ],
    test_suite='uwsgiit.tests',
    packages=find_packages(exclude=["test_project", "example.*"]),
    include_package_data=True,
    zip_safe = False,
)
