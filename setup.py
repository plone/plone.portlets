from setuptools import setup, find_packages

version = '2.0b3'

setup(name='plone.portlets',
      version=version,
      description="An extension of zope.viewlet to support dynamic portlets",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='portlet viewlet',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.portlets',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=[
              'zope.configuration',
              'zope.location',
              'zope.security',
              'zope.app.content',
              'zope.app.folder',
              'zope.app.pagetemplate',
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
