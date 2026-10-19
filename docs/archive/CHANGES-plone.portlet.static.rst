Changelog
=========


.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

5.0.0 (2026-05-16)
------------------

Internal:


- Update configuration files.
  [plone devs]


5.0.0a1 (2025-11-19)
--------------------

Breaking changes:


- Replace ``pkg_resources`` namespace with PEP 420 native namespace.
  Support only Plone 6.2 and Python 3.10+. (#3928)


4.0.5 (2025-09-11)
------------------

Internal:


- Move distribution to src layout [gforcada] (#4217)


4.0.4 (2025-01-23)
------------------

Bug fixes:


- Fix DeprecationWarnings. [maurits] (#4090)


4.0.3 (2024-11-30)
------------------

Tests


- Fix removed `unittest.makeSuite` in python 3.13.
  [petschki] (#45)


4.0.2 (2024-01-22)
------------------

Internal:


- Update configuration files.
  [plone devs] (6e36bcc4, 7723aeaf)


4.0.1 (2023-03-21)
------------------

Internal:


- Update configuration files.
  [plone devs] (a533099d)


4.0.0 (2022-11-30)
------------------

Bug fixes:


- Remove six dependency.
  [gforcada] (#1)
- Final release.
  [gforcada] (#600)


4.0.0b1 (2022-06-23)
--------------------

Bug fixes:


- Test-only fix: normalize white space.
  [maurits] (#49)


4.0.0a1 (2021-04-20)
--------------------

Breaking changes:


- Update for Plone 6 with Bootstrap markup
  [petschki, agitator] (#22)


Bug fixes:


- Remove explicit required attribute on `omit_border` boolean
  [petschki] (#20)


3.1.6 (2020-09-21)
------------------

Bug fixes:


- Removed Plone 4 compatibility code.
  [maurits] (#19)
- Fixed invalid escape sequence.
  [maurits] (#3130)


3.1.5 (2020-09-07)
------------------

Bug fixes:


- Fixed startup warning for setDefaultRoles.
  [maurits] (#17)


3.1.4 (2020-04-21)
------------------

Bug fixes:


- Minor packaging updates. (#1)


3.1.3 (2018-09-28)
------------------

Bug fixes:

- Fix static portlet for py3
  [pbauer]


3.1.2 (2018-02-05)
------------------

Bug fixes:

- Fix test. Portletrenderer can't be wrapped in aq.
  [pbauer]

- Add Python 2 / 3 compatibility
  [vincero]


3.1.1 (2017-07-03)
------------------

Bug fixes:

- Remove unittest2 dependency
  [kakshay21]


3.1 (2016-09-07)
----------------

New:

- Attempt to use AutoExtensibleForm for as base for static portlet forms
  when Plone 4 site also has recent plone.app.widgets; this should be
  consistent in portlet with how TinyMCE is configured for Dexterity
  content.  This approach attempts to harmonize Plone 4 compatibillity
  work done previously by @thet and @cdw9 -- supporting Plone 4, either
  with/without plone.app.widgets, and with/without plone.app.contenttypes
  (provided recent plone.app.widgets is used).
  [seanupton]


3.0.2 (2016-02-14)
------------------

Fixes:

- Cleaned up test setup.
  [timo]

- Check that renderer has a '__portlet_metadata__' attribute
  and compute 'assignment context' only for 'context' portlet.
  [sverbois]

- Plone 4 compatibility.
  [thet]


3.0.1 (2014-10-23)
------------------

- Replace DL/DT/DD in portlet with more semantic markup (see PR #7).
  [khink]

- Fix the relative url transformation.
  The 'safe_html' transformation has to be called with 'assignment context'
  instead of 'display context'.
  [sverbois]


3.0.0 (2014-04-13)
------------------

- Use z3c.form for the portlet forms.
  [bosim, davisagli]


2.0.2 (2013-01-13)
------------------

- Check if instance is str before turning to unicode as Portal_tranform itself
  can return unicode
  [fafhrd91]

- Portlet title no longer required. If the title is empty, the css class
  "titleless" is added to the header.
  [rnix, thet]

- Adding constraint to validate white spaces
  Fix https://dev.plone.org/ticket/13130
  [hersonrodrigues]

- Add MANIFEST.in.
  [WouterVH]

- Add metadata.xml to profile.
  [WouterVH]


2.0.1 - 2011-01-03
------------------

- Add Site Administrator to the default roles for the
  "plone.portlet.static: Add static portlet" permission, for forward
  compatibility with Plone 4.1.
  [davisagli]


2.0 - 2010-07-18
----------------

- Removed the deprecated `hide` option form the portlet.
  [hannosch]

- Update license to GPL version 2 only.
  [hannosch]


2.0b2 - 2010-02-17
------------------

- Removed the transformation cache from the portlet renderer. Portal transforms
  doesn't actually work with the assignment class as a cache context.
  This closes http://dev.plone.org/plone/ticket/10167.
  [hannosch]


2.0b1 - 2009-12-02
------------------

- Removed Kupu as a testing dependency. In Plone 4 the tests work with the
  default TinyMCE transforms.
  [hannosch]


2.0a2 - 2009-11-18
------------------

- Removed reference to non-existent profile in plone.app.portlets.
  [hannosch]


2.0a1 - 2009-11-13
------------------

- Remove the "hide" option as this is now available to all portlets (PLIP 9286)
  [igbun]

- Adjusted test setup to Plone 5.
  [hannosch]

- Added the z3c.autoinclude entry point so this package is automatically loaded
  on Plone 3.3 and above.
  [hannosch]

- Declare test dependencies in an extra.
  [hannosch]

- Specify package dependencies.
  [hannosch]

- Added 'tile' CSS class to the links within dt.portletHeader and
  dd.portletFooter for static portlet's template
  [spliter]


1.2.1 - 2009-11-25
------------------

- Fixed a syntax error introduced in the last change.
  [hannosch]


1.2 - 2009-11-25
----------------

- Ensure that text output is passed through the safe-html transform to protect
  against malicious text. This also ensures the resolve uid behavior works when
  only TinyMCE and not Kupu is installed.
  [hannosch]

- Removed msgids in portlets.xml. There is no support for
  msgids in the import of portlets.xml implementation.
  This allows to extract translatable strings with i18ndude.
  [vincentfretin]

- Added transform to resolve uids.
  [lrowe]


1.2rc1 - 2009-03-27
-------------------

- The portlet was incorrectly using the 'Manage portlet' permission. It now
  uses a custom permission with the same default roles.
  Fixes http://dev.plone.org/plone/ticket/8403.
  [optilude]


1.1.5 - 2008-08-18
------------------

- Fixed a typo in CSS class name. This closes
  http://dev.plone.org/plone/ticket/8119.
  [hannosch]


1.1.2 -  2008-06-01
-------------------

- Added more i18n in the main python file as the i18n in portlets.xml
  is not used.  [maurits]

- Added option to (temporarily) hide the portlet without needing to
  delete it.  [maurits]


1.1.0 - 2008-04-20
------------------

- Unchanged from 1.1rc2


1.1rc2 - 2008-03-26
-------------------

- Use README.txt and HISTORY.txt as the package's long description and
  add missing history entries for all releases.
  [wichert]

- Fix the version restriction on the plone.app.form dependency.
  [wichert]


1.1rc1 - 2008-03-25
-------------------

- Add missing i18n support.
  [hannosch]

- Add a version restriction on the plone.app.form dependency.
  [optilude]


1.1.0a1 - 2008-03-09
--------------------

- Packaging cleanups
  [wichert]

- PLIP 184: make text editable using a rich text editor such as kupu
  [optilude]

- Add an 'omit border' option
  [optilude]


1.0b3 - 2007-08-27
-------------------

- Correct portlet styling to Plone standards
  [optilude]


1.0b2 - 2007-08-26
------------------

- Make header and footer configurable
  [optilude]


1.0b1 - 2007-08-26
------------------

- Added missing i18n markup to portlets.xml.
  [hannosch]

- Changed the i18n domain to `plone`.
  [hannosch]

- Initial release
  [optilude]
