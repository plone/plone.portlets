from zope.interface import implements
from zope.component import adapts

from plone.portlets.interfaces import IPortletContext
from plone.portlets.interfaces import IPortletStorage
from plone.portlets.interfaces import IPortletRetriever

class DefaultPortletRetriever(object):
    """A volatile default portlet storage.
    
    This will most likely need to be override to become persistent.
    """
    
    implements(IPortletRetriever)
    adapts(IPortletContext, IPortletStorage)
    
    def __init__(self, context, storage):
        self.context = context
        self.storage = storage
        
    def getPortlet(self, id):
        portlets = [p for p in self.getPortlets() if p.id == id]
        if len(portlets) == 0:
            raise KeyError
        else:
            return portlets[0]
        
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
            contextPortlets.extend(self.storage.getPortletAssignmentsForContext(location.uid))
            location = location.parent
        
        return contextPortlets + userPortlets + groupPortlets