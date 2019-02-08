from setuptools import find_packages
from setuptools import setup


version = '2.3.1'

setup(
    name='plone.portlets',
    version=version,
    description="An extension of zope.viewlet to support dynamic portlets",
    long_description=(
        open("README.rst").read() + "\n" + open("CHANGES.rst").read()
    ),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords='portlet viewlet',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.org/project/plone.portlets',
    license='GPL version 2',
    packages=find_packages(),
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            'zope.browserpage',
            'zope.configuration',
            'zope.location',
            'zope.security',
        ]
    ),
    install_requires=[
        'setuptools',
        'ZODB3',
        'plone.memoize',
        'zope.annotation',
        'zope.component',
        'zope.container',
        'zope.contentprovider',
        'zope.interface',
        'zope.publisher',
        'zope.schema',
        'zope.site',
    ],
)
