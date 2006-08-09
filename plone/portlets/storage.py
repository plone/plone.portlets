from zope.interface import implements

from interfaces import IPortletStorage

class VolatilePortletStorage(object):
    """A volatile default portlet storage.
    
    This will most likely need to be override to become a site-local utility
    with better knowledge about contexts, users and groups.
    """
    implements(IPortletStorage)
    
    def __init__(self):
        self.contextPortlets = {}
        self.userPortlets = {}
        self.groupPortlets = {}
    
    def getPortletAssignmentsInContext(self, manager, context, userId, groupIds):
        portlets = self.contextPortlets[manager].get(context, []) + \
                   self.userPortlets[manager].get(userId, [])
        for groupId in groupIds:
            portlets += self.groupPortlets[manager].get(groupId, [])
        return portlets
        
    def getPortletAssignmentsForContext(self, manager, context):
        return self.contextPortlets.setdefault(manager, {}).get(context, [])
        
    def setPortletAssignmentsForContext(self, manager, context, portletAssignments):
        d = self.contextPortlets.setdefault(manager, {})
        d[context] = portletAssignments
        
    def getPortletAssignmentsForUser(self, manager, userId):
        return self.userPortlets.setdefault(manager, {}).get(userId, [])
        
    def setPortletAssignmentsForUser(manager, userId, portletAssignments):
        d = self.userPortlets.setdefault(manager, {})
        d[userId] = portletAssignments
    
    def getPortletAssignmentsForGroup(manager, groupId):
        return self.groupPortlets.setdefault(manager, {}).get(groupId, [])
        
    def setPortletAssignmentsForGroup(manager, groupId, portletAssignments):
        d = self.groupPortlets.setdefault(manager, {})
        d[groupId] = portletAssignments