from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='plone.portlets',
      version=version,
      description="An extension of zope.viewlet to support dynamic portlets",
      long_description="""\
""",
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='portlet viewlet',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.portlets',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
