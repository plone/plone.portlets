from BTrees.OOBTree import OOBTree
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletCategoryMapping
from plone.portlets.interfaces import IPortletStorage
from zope.container.btree import BTreeContainer
from zope.container.contained import Contained
from zope.container.ordered import OrderedContainer
from zope.interface import implementer

import logging


LOG = logging.getLogger("portlets")


def _coerce(key):
    # XXX: We coerce all mapping keys (things like user and group ids)
    # to unicode, because the OOBTree that we store them in will fall over with
    # mixed encoded-str and unicode keys. It may be better to store byte strings
    # (and thus coerce the other way), especially to support things like Active
    # Directory where user ids are binary GUIDs. However, that's a problem for
    # another day, since it'll require more complex migration.
    if isinstance(key, bytes):
        try:
            key = str(key, encoding="utf-8")
        except UnicodeDecodeError:
            LOG.warn("Unable to convert %r to unicode" % key)
            return str(key, "utf-8", "ignore")

    return key


@implementer(IPortletStorage)
class PortletStorage(BTreeContainer):
    """The default portlet storage."""


@implementer(IPortletCategoryMapping)
class PortletCategoryMapping(BTreeContainer, Contained):
    """The default category/key mapping storage."""

    # We need to hack some stuff to make sure keys are unicode.
    # The shole BTreeContainer/SampleContainer mess is a pain in the backside

    def __getitem__(self, key):
        return super().__getitem__(_coerce(key))

    def get(self, key, default=None):
        """See interface `IReadContainer`"""
        return super().get(_coerce(key), default)

    def __contains__(self, key):
        """See interface `IReadContainer`"""
        return super().__contains__(_coerce(key))

    has_key = __contains__

    def __setitem__(self, key, object):
        """See interface `IWriteContainer`"""
        super().__setitem__(_coerce(key), object)

    def __delitem__(self, key):
        """See interface `IWriteContainer`"""
        super().__delitem__(_coerce(key))


@implementer(IPortletAssignmentMapping)
class PortletAssignmentMapping(OrderedContainer):
    """The default assignment mapping storage."""

    __manager__ = ""
    __category__ = ""
    __name__ = ""

    def __init__(self, manager="", category="", name=""):
        # XXX: This depends on implementation detail in OrderedContainer,
        # but it uses a PersistentDict, which sucks :-/
        OrderedContainer.__init__(self)
        self._data = OOBTree()

        self.__manager__ = manager
        self.__category__ = category
        self.__name__ = name
