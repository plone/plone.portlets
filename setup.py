from setuptools import setup, find_packages

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
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "Framework :: Zope3",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='portlet viewlet',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.portlets',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=[
              'zope.configuration',
              'zope.security',
              'zope.testing',
              'zope.app.component',
              'zope.app.content',
              'zope.app.folder',
              'zope.app.pagetemplate',
              'zope.app.security',
          ],
      ),
      install_requires=[
        'setuptools',
        'ZODB3',
        'plone.memoize',
        'zope.annotation',
        'zope.component',
        'zope.contentprovider',
        'zope.interface',
        'zope.publisher',
        'zope.schema',
        'zope.app.container',
      ],
      )
