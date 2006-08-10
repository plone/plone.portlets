from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility

from interfaces import IPortletContext
from interfaces import IPortletStorage
from interfaces import IPortletRetriever

class DefaultPortletRetriever(object):
    """Default implementation of the portlet retrieval algorithm.
    
    This obtains portlets from the default portlet storage.
    """
    
    implements(IPortletRetriever)
    adapts(IPortletContext)
    
    def __init__(self, context):
        self.context = context

    def getPortlets(self, manager):
        storage = getUtility(IPortletStorage)
        userPortlets = storage.getPortletAssignmentsForUser(manager, self.context.userId)
        groupPortlets = []
        for g in self.context.groupIds:
            groupPortlets.extend(storage.getPortletAssignmentsForGroup(manager, g))
        
        contextPortlets = storage.getPortletAssignmentsForContext(manager, self.context.uid)
        parent = self.context.parent
        while parent is not None:
            parentContext = IPortletContext(parent)
            contextPortlets.extend(storage.getPortletAssignmentsForContext(manager, parentContext.uid))
            parent = parent.parent
        
        # XXX: Port portlet composition-in-context algorithm from
        # PlonePortlets to here. This must rely on IPortletContext,
        # which can obtain a uid of a context, the current user id 
        # and a list of group ids for that user - see interfaces.py
        
        return contextPortlets + userPortlets + groupPortlets