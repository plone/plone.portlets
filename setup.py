from setuptools import setup, find_packages
import sys, os

version = '1.1.0'

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
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='portlet viewlet',
      author='Martin Aspeli',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.portlets',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'plone.memoize',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
