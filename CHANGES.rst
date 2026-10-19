Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

5.0.0a1 (2026-10-19)
--------------------

Breaking changes:


- Merge ``plone.app.portlets``, ``plone.portlet.collection`` and ``plone.portlet.static`` into this distribution, with their complete git history.
  Import paths do not change.
  The three former distributions are continued as empty packages that depend on ``plone.portlets``.
  See `PLIP 4137 <https://github.com/plone/Products.CMFPlone/issues/4137>`_.
  @jensens (#4137)


Internal:


- Move package metadata from ``setup.py`` to ``pyproject.toml``.
  [plone devs]


The changelog starts fresh with version 5.0.0, when ``plone.app.portlets``,
``plone.portlet.collection`` and ``plone.portlet.static`` were merged into this
distribution.
The changelogs of the four former distributions are kept in ``docs/archive/``.
