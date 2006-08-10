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
            
    def getPortletAssignmentsForContext(self, manager, uid):
        return self.contextPortlets.setdefault(manager, {}).get(uid, [])
        
    def setPortletAssignmentsForContext(self, manager, uid, portletAssignments):
        d = self.contextPortlets.setdefault(manager, {})
        d[uid] = portletAssignments
        
    def getPortletAssignmentsForUser(self, manager, userId):
        return self.userPortlets.setdefault(manager, {}).get(userId, [])
        
    def setPortletAssignmentsForUser(self, manager, userId, portletAssignments):
        d = self.userPortlets.setdefault(manager, {})
        d[userId] = portletAssignments
    
    def getPortletAssignmentsForGroup(self, manager, groupId):
        return self.groupPortlets.setdefault(manager, {}).get(groupId, [])
        
    def setPortletAssignmentsForGroup(self, manager, groupId, portletAssignments):
        d = self.groupPortlets.setdefault(manager, {})
        d[groupId] = portletAssignments