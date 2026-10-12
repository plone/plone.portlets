Overview
========

``plone.portlets`` contains the complete portlet implementation of Plone:

``plone.portlets``
    A generic infrastructure for managing portlets.
    Portlets are a bit like viewlets, except they can be manipulated at runtime,
    using local components.

``plone.app.portlets``
    The Plone-specific user interface for ``plone.portlets``,
    as well as the standard set of portlets that ship with Plone.

``plone.portlet.collection``
    A portlet that fetches results from a collection.

``plone.portlet.static``
    A portlet providing a rich-text field for more or less static text.

Until version 4.x these were four separate distributions.
Since version 5.0.0 (Plone 6.3) they are shipped together in this distribution,
see `PLIP 4137 <https://github.com/plone/Products.CMFPlone/issues/4137>`_.
The import paths did not change.
The distributions ``plone.app.portlets``, ``plone.portlet.collection`` and
``plone.portlet.static`` are kept on PyPI as empty packages that depend on
``plone.portlets``, so existing dependencies keep working.
The code for Plone 6.2 and earlier stays in the former repositories.


Call one portlet by URL
=======================

To call a portlet by its URL, for example, to update it via an AJAX call, use
the ``@@render-portlet`` view in your portlet renderer with ``portlethash`` as a
query parameter.

The following example shows how to construct a reload URL for a portlet::

    from plone.app.portlets.portlets.base import Renderer
    from Products.CMFPlone.utils import safe_unicode


    class BasePortletRenderer(Renderer):
        @property
        def hash(self):
            portlethash = self.request.form.get(
                "portlethash", getattr(self, "__portlet_metadata__", {}).get("hash", "")
            )
            return portlethash

        @property
        def reload_url(self):
            base_url = self.context.absolute_url()
            hash = safe_unicode(self.hash)
            return f"{base_url}/@@render-portlet?portlethash={hash}"


Git history
===========

All four former repositories were merged with their complete history.
The code was moved into ``src/`` shortly before the merge,
so to see the history of a package before that move,
pass the old path as well, for example::

    git log -- src/plone/app/portlets plone/app/portlets

``git log --follow`` (for single files) and ``git blame`` cross the move on their own.


Compatibility
=============

- ``plone.portlets`` 5.x is for Plone 6.3.
- Plone 6.2 uses ``plone.portlets`` 4.x, ``plone.app.portlets`` 7.x,
  ``plone.portlet.collection`` 5.x and ``plone.portlet.static`` 5.x.
