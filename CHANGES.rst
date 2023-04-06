Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

3.0.0 (2023-04-06)
------------------

Breaking changes:


- Drop support for Plone 5.2 and Python 2.
  Only Plone 6.0 on Python 3.8+ is supported.
  [plone devs] (#9)


Internal:


- Update configuration files.
  [plone devs] (80cf330f)


2.3.3 (2023-03-14)
------------------

Bug fixes:


- Use `ZODB` as dependency rather than the deprecated `ZODB3`.
  [gforcada] (#1)
- Fix deprecation warnings (#5)


2.3.2 (2020-04-21)
------------------

Bug fixes:


- Minor packaging updates. (#1)


2.3.1 (2019-02-08)
------------------

Bug fixes:


- Fixed some deprecation warnings. Code style: black, isort Fix tests, also do
  not leave closed files. [jensens] (#4)


2.3 (2016-11-01)
----------------

New features:

- Support Python 3. [davisagli]


2.2.3 (2016-08-09)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


2.2.2 (2016-02-15)
------------------

Fixes:

- Rerelease to fix problem on test server.  [maurits]


2.2.1 (2016-02-12)
------------------

Fixes:

- Do not break in placeless portlet retriever if there is no underlying code
  available for existing portlet assignment.
  [vipod]

- Prevent possible unicode errors when creating portlet hashes.  [wichert]


2.2 (2012-10-01)
----------------

- Added an adapter and IBlockingPortletManager marker interface which portlet
  managers can provide to block parent contextual portlets by default.
  [elro]

- Delegate to ILocalPortletAssignmentManager for category blacklist retrieval.
  This allows a custom adapter to override the default blacklist settings per
  portlet manager.
  [elro]


2.1 (2012-07-02)
----------------

- Avoid some test dependencies.
  [hannosch]

- Graceful handling of portlets with missing implementation.
  [do3cc]

2.0.2 - 2011-04-21
------------------

- Add MANIFEST.in.
  [WouterVH]

2.0.1 - 2011-01-03
------------------

- Added a method to get unavailable portlets of of a manager.
  This refs http://dev.plone.org/plone/ticket/11343
  [thomasdesvenain]

2.0 - 2010-07-16
----------------

- Update license to GPL version 2 only.
  [hannosch]

- Make it possible to rely on the ``__portlet_metadata__`` of a portlet
  renderer to determine its availability. This closes
  http://dev.plone.org/plone/ticket/10742.
  [enriquepablo, hannosch]

2.0b3 - 2010-06-13
------------------

- Use the standard libraries doctest module.
  [hannosch]

- Use zope.browserpage if available.
  [hannosch]

2.0b2 - 2010-03-27
------------------

- Protect the exception logging against funky portlets. In error cases even
  doing a repr() on the portlet might cause an infinite recursion error.
  [hannosch]

2.0b1 - 2010-01-25
------------------

- Added ``__portlet_metadata__`` attribute to portlet renderers, to make it
  easier for a portlet to know how it was looked up (and thus reconstruct a URL
  to itself, for example).
  [optilude]

2.0a1 - 2009-11-14
------------------

- Avoid a variety of zope.app dependencies in favor of Zope Toolkit packages.
  [hannosch]

- Added support for showing/hiding of all portlets (PLIP #9286)
  [igbun]

1.2 - 2009-06-19
----------------

- Fixed 'SyntaxError: non-keyword arg after keyword arg' in unicode call.
  [maurits]

- Fix/workaround for http://dev.plone.org/plone/ticket/8128 (UnicodeDecodeError
  within _coerce() caused by external data with wrong encoding).
  [ajung]

- Moved test-only dependencies to a test extra requirement.
  [hannosch]

- Clarified license and copyright statements.
  [hannosch]

- Specify package dependencies.
  [hannosch]

- Replaced direct invocations of interfaces with queryAdapter calls. The
  former does a suboptimal getattr call internally.
  [hannosch]

1.1.0 - 2008-04-20
------------------

- Ensure the keys stored in a portlet assignment mapping are always
  unicode. This is necessary because an OOBTree will, once one unicode key
  has been added, force all keys to unicode. This can lead to unicode
  decode errors.
  Fixes http://dev.plone.org/plone/ticket/6100
  [optilude]

- Changed a type() comparison into a isinstance comparison.
  [hannosch]

- PLIPs 205 and 218: Allow registering portlet types to multiple portlet
  manager interfaces, require portlet types to be explicitly registered
  for portlet manager interfaces, enable modifying registrations through
  GenericSetup, and restrict most default Plone portlet types to left/
  right/dashboard columns.
  [sirgarr]

- PLIP207: Allow custom portlet managers, i.e., allow specifying an
  alternative portlet manager class through GenericSetup.
  [sirgarr]

1.0.6
-----

- Made tests run under Zope 2.11.
  [hannosch]

1.0.5
-----

- Added properties to keep track of the manager name, category name and
  key/name in portlet assignment mappings.
  [optilude]

1.0.1
-----

- Adjusted some tests, so they work on both Zope 2.10 and 2.11.
  [hannosch]

1.0
---

- Initial package structure.
  [zopeskel]
