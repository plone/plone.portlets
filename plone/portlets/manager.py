from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility

from interfaces import IPortletManager
from interfaces import IPortletStorage
from interfaces import IPortletContext

class DefaultPortletManager(object):
    """Default implementation of a portlet manager that delegates to the
    portlet storage utility.
    """
    
    implements(IPortletManager)
    adapts(IPortletContext)

    def __init__(self, context):
        self.context = context

    def getPortletAssignments(self, manager):
        storage = getUtility(IPortletStorage)
        return storage.getPortletAssignmentsForContext(manager, self.context.uid)

    def setPortletAssignments(self, manager, portletAssignments):
        storage = getUtility(IPortletStorage)
        storage.setPortletAssignmentsForContext(manager, self.context.uid, portletAssignments)