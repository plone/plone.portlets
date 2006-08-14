from zope.interface import implements
from zope.component import adapts

from plone.portlets.interfaces import IPortletAssignable
from plone.portlets.interfaces import IPortletContext
from plone.portlets.interfaces import IPortletManager

class ContextPortletAssignable(object):
    """Default implementation of a portlet assignable for contexts (content 
    objects).
    """

    implements(IPortletAssignable)
    adapts(IPortletContext, IPortletManager)

    def __init__(self, context, manager):
        self.context = context
        self.manager = manager

    def getPortletAssignments(self):
        return self.manager.getPortletAssignmentsForContext(self.context.uid)

    def setPortletAssignments(self, portletAssignments):
        self.manager.setPortletAssignmentsForContext(self.context.uid, portletAssignments)