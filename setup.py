import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-datatablesview',
    version='1.2.0',
    packages=['datatablesview'],
    include_package_data=True,
    license='MIT License',  # example license
    description='DataTablesView is a Django app that facilitates the creation of reports and tables with record listings.',
    long_description=README,
    url='https://pagtech.com.br/',
    author='Lucas Mendes',
    author_email='lucas.mendes@pagtech.com.br',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
