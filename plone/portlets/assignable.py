from persistent.list import PersistentList
from persistent.dict import PersistentDict

from zope.interface import implements
from zope.component import adapts
from zope.annotation.interfaces import IAnnotations

from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.interfaces import IPortletManager

from plone.portlets.storage import PortletAssignmentMapping
from plone.portlets.constants import CONTEXT_ASSIGNMENT_KEY
from plone.portlets.constants import CONTEXT_BLACKLIST_STATUS_KEY

from BTrees.OOBTree import OOBTree

class LocalPortletAssignmentManager(PortletAssignmentMapping):
    """Default implementation of a portlet assignable for contexts (content 
    objects).
    """
    implements(ILocalPortletAssignmentManager)
    adapts(ILocalPortletAssignable, IPortletManager)

    __name__ = __parent__ = None

    def __init__(self, context, manager):
        self.context = context
        self.manager = manager
        
        PortletAssignmentMapping.__init__(self)

    def _newData(self):
        annotations = IAnnotations(self.context)
        local = annotations.get(CONTEXT_ASSIGNMENT_KEY, None)
        if local is None:
            local = annotations[CONTEXT_ASSIGNMENT_KEY] = OOBTree()
        portlets = local.get(self.manager.__name__, None)
        if portlets is None:
            portlets = local[self.manager.__name__] = PersistentList()
        return portlets
        
    def setBlacklistStatus(self, category, status):
        annotations = IAnnotations(self.context)
        local = annotations.get(CONTEXT_BLACKLIST_STATUS_KEY, None)
        if local is None:
            local = annotations[CONTEXT_BLACKLIST_STATUS_KEY] = PersistentDict()
        blacklist = local.get(self.manager.__name__, None)
        if blacklist is None:
            blacklist = local[self.manager.__name__] = PersistentDict()
        blacklist[category] = status
    
    def getBlacklistStatus(self, category):
        annotations = IAnnotations(self.context)
        local = annotations.get(CONTEXT_BLACKLIST_STATUS_KEY, None)
        if local is None:
            return None
        blacklist = local.get(self.manager.__name__, None)
        if blacklist is None:
            return None
        return blacklist.get(category, None)
        