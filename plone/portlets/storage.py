from zope.interface import implements

from zope.app.container.btree import BTreeContainer
from zope.app.container.contained import Contained, NameChooser
from zope.app.container.ordered import OrderedContainer

from plone.portlets.interfaces import IPortletStorage
from plone.portlets.interfaces import IPortletCategoryMapping
from plone.portlets.interfaces import IPortletAssignmentMapping

from BTrees.OOBTree import OOBTree

class PortletStorage(BTreeContainer):
    """The default portlet storage.
    """
    implements(IPortletStorage)
        
class PortletCategoryMapping(BTreeContainer, Contained):
    """The default category/key mapping storage.
    """
    implements(IPortletCategoryMapping)

class PortletAssignmentMapping(OrderedContainer):
    """The default assignment mapping storage.
    """
    implements(IPortletAssignmentMapping)
    
    def __init__(self):
        # XXX: This depends on implementation detail in OrderedContainer,
        # but it uses a PersistentDict, which sucks :-/
        OrderedContainer.__init__(self)
        self._data = OOBTree()