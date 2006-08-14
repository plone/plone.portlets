from zope.interface import implements
from zope.component import adapts

from plone.portlets.interfaces import IPortletContext
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPlacelessPortletManager
from plone.portlets.interfaces import IPortletRetriever

class PortletRetriever(object):
    """The default portlet retriever.

    This will aggregate contextual portlets, acquired up until the root 
    IPortletContext, then user portlets, then group portlets.
    """

    implements(IPortletRetriever)
    adapts(IPortletContext, IPortletManager)

    def __init__(self, context, storage):
        self.context = context
        self.storage = storage

    def getPortlets(self):
        # Get user portlets
        userPortlets = self.storage.getPortletAssignmentsForUser(self.context.userId)

        # Get group portlets and combine them into a single list
        groupPortlets = []
        for g in self.context.groupIds:
            groupPortlets.extend(self.storage.getPortletAssignmentsForGroup(g))

        # Get context portlets, including those for parents
        contextPortlets = []
        location = self.context
        while location is not None:
            parentContext = IPortletContext(location)
            contextPortlets.extend(self.storage.getPortletAssignmentsForContext(parentContext.uid))
            location = parentContext.parent

        return contextPortlets + userPortlets + groupPortlets
        
class PlacelessPortletRetriever(PortletRetriever):
    """A placeless portlet retriever.
    
    This will aggregate user portlets, then group portlets.
    """
    
    implements(IPortletRetriever)
    adapts(IPortletContext, IPlacelessPortletManager)
    
    def __init__(self, context, storage):
        self.context = context
        self.storage = storage
        
    def getPortlets(self):
        # Get user portlets
        userPortlets = self.storage.getPortletAssignmentsForUser(self.context.userId)
        
        # Get group portlets and combine them into a single list
        groupPortlets = []
        for g in self.context.groupIds:
            groupPortlets.extend(self.storage.getPortletAssignmentsForGroup(g))
        
        return userPortlets + groupPortlets