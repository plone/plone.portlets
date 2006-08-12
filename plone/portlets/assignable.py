from zope.interface import implements
from zope.component import adapts

from interfaces import IPortletAssignable
from interfaces import IPortletContext

class DefaultPortletAssignable(object):
    """Default implementation of a portlet assignable that delegates to a 
    specific portlet manager.
    """
    
    implements(IPortletAssignable)
    adapts(IPortletContext)

    def __init__(self, context):
        self.context = context

    def getPortletAssignments(self, manager):
        return manager.getPortletAssignmentsForContext(self.context.uid)

    def setPortletAssignments(self, manager, portletAssignments):
        manager.setPortletAssignmentsForContext(self.context.uid, portletAssignments)