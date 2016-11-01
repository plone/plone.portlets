from setuptools import setup, find_packages

version = '2.3'

setup(
    name='plone.portlets',
    version=version,
    description="An extension of zope.viewlet to support dynamic portlets",
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
    ],
    keywords='portlet viewlet',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.python.org/pypi/plone.portlets',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            'zope.browserpage',
            'zope.configuration',
            'zope.location',
            'zope.security',
        ],
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
