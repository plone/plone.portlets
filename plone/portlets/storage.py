from zope.interface import implements

from persistent import Persistent
from persistent.dict import PersistentDict

from plone.portlets.interfaces import IPortletStorage

class PortletStorage(Persistent):
    """A volatile default portlet storage.

    This will most likely need to be override to become persistent.
    """
    implements(IPortletStorage)

    def __init__(self):
        self.contextPortlets = PersistentDict()
        self.userPortlets = PersistentDict()
        self.groupPortlets = PersistentDict()

    def getPortletAssignmentsForContext(self, uid):
        return self.contextPortlets.get(uid, [])

    def setPortletAssignmentsForContext(self, uid, portletAssignments):
        self.contextPortlets[uid] = portletAssignments

    def getPortletAssignmentsForUser(self, userId):
        return self.userPortlets.get(userId, [])

    def setPortletAssignmentsForUser(self, userId, portletAssignments):
        self.userPortlets[userId] = portletAssignments

    def getPortletAssignmentsForGroup(self, groupId):
        return self.groupPortlets.get(groupId, [])

    def setPortletAssignmentsForGroup(self, groupId, portletAssignments):
        self.groupPortlets[groupId] = portletAssignments