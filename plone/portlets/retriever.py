from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility

from interfaces import IPortletContext
from interfaces import IPortletViewletManager
from interfaces import IPortletStorage
from interfaces import IPortletRetriever

class DefaultPortletRetriever(object):
    """Default implementation of the portlet retrieval algorithm.
    
    This obtains portlets from the default portlet storage.
    """
    
    implements(IPortletRetriever)
    adapts(IPortletContext, IPortletViewletManager)
    
    def __init__(self, context, manager):
        self.context = context
        self.manager = manager
        
    def getPortlet(self, id):
        portlets = [p for p in self.getPortlets() if p.id == id]
        if len(portlets) == 0:
            raise KeyError
        else:
            return portlets[0]
        
    def getPortlets(self):
        storage = getUtility(IPortletStorage)
        
        # Get user portlets
        userPortlets = storage.getPortletAssignmentsForUser(self.manager, self.context.userId)
        
        # Get group portlets and combine them into a single list
        groupPortlets = []
        for g in self.context.groupIds:
            groupPortlets.extend(storage.getPortletAssignmentsForGroup(self.manager, g))
        
        # Get context portlets, including those for parents
        contextPortlets = storage.getPortletAssignmentsForContext(self.manager, self.context.uid)
        parent = self.context.parent
        while parent is not None:
            parentContext = IPortletContext(parent)
            contextPortlets.extend(storage.getPortletAssignmentsForContext(self.manager, parentContext.uid))
            parent = parent.parent
        
        return contextPortlets + userPortlets + groupPortlets