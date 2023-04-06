from setuptools import find_packages
from setuptools import setup


version = "3.0.0"

setup(
    name="plone.portlets",
    version=version,
    description="An extension of zope.viewlet to support dynamic portlets",
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="portlet viewlet",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/plone.portlets",
    license="GPL version 2",
    packages=find_packages(),
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    extras_require=dict(
        test=[
            "zope.browserpage",
            "zope.configuration",
            "zope.location",
            "zope.security",
            "zope.testing",
        ]
    ),
    install_requires=[
        "BTrees",
        "setuptools",
        "ZODB",
        "plone.memoize",
        "persistent",
        "zope.annotation",
        "zope.component",
        "zope.container",
        "zope.contentprovider",
        "zope.interface",
        "zope.publisher",
        "zope.schema",
        "zope.site",
    ],
)
