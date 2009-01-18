from setuptools import setup, find_packages
import sys, os

version = '1.2'

setup(name='plone.portlets',
      version=version,
      description="An extension of zope.viewlet to support dynamic portlets",
      long_description="""\
plone.portlets provides a generic infrastructure for managing portlets. 
Portlets are a bit like viewlets, except they can be manipulated at runtime,
using local components. This package is used by plone.app.portlets to provide
Plone-specific portlets, but should be generic enough to work on other 
platforms. It should work in a "pure Zope 3" environment.
""",
      classifiers=[],
      keywords='portlet viewlet',
      author='Martin Aspeli',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.portlets',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'ZODB3',
        'plone.memoize',
        'zope.annotation',
        'zope.component',
        'zope.configuration',
        'zope.contentprovider',
        'zope.interface',
        'zope.publisher',
        'zope.schema',
        'zope.security',
        'zope.app.component',
        'zope.app.container',
        'zope.app.content',
        'zope.app.folder',
        'zope.app.pagetemplate',
        'zope.app.security',
      ],
      )
