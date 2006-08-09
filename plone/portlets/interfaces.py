from zope.interface import Interface, Attribute

from zope.contentprovider.interfaces import IContentProvider

from zope.viewlet.interfaces import IViewlet
from zope.viewlet.interfaces import IViewletManager

# Generic marker interface

class IPortletDataProvider(Interface):
    """A marker interface for objects providing portlet data.
    
    This can be used as a marker by implementations requiring a regular content 
    object to be able to be "switched on" as a portlet. Alternatively, a more
    specific sub-interface can provide the necessary information to render
    the portlet.
    
    An adapter should exist from the specific type of IPortletDataProvider to 
    an appropriate IPortletViewlet to render it.
    
    The data provider will also be referenced in an IPortletAssignment so that
    it can be retrieved on demand.
    """
    
# Special viewlet manager and viewlet to render portlets
    
class IPortletViewlet(IContentProvider):
    """A special implementation of a viewlet (content provider) which is managed
    by an IPortletViewletManager.
    
    Any object providing IPortletDataProvider should be adaptable to 
    IPortletViewlet in order to be renderable as a portlet.
    """

class IPortletViewletManager(IViewletManager):
    """A ViewletManager that looks up its viewlets runtime.
    
    This will typically adapt its context to IPortletRetrieval and query it for 
    a list of IPortletViewlets to render.
    """

# Discovery of portlets

class IPortletRetrieval(Interface):
    """A component capable of discovering portlets assigned to it.
    
    Typically, a content object will be adapted to IPortletRetriever. The
    implementation of getPortlets() will most likely query the IPortletStorage
    utility for the actual portlets to render.
    """

    def getPortlets(manager):
        """Return a list of IPortletViewlet's to be rendered in the context 
        for the given viewlet manager.
        """

# Assignment of portlets

class IPortletAssignment(Interface):
    """Assignment of a portlet to a given viewlet manager relative to a 
    context, user or group.
    
    Implementations of this interface will typically be persistent, stored in
    an IPortletStorage.
    
    The 'data' attribute may be implemented as a property that retrieves the
    data object on-demand.
    """
    
    data = Attribute(u'Portlet data object')

class IPortletManager(Interface):
    """A component capable of managing portlets.
    
    Typically, a content object, user or group would be adapted to allow 
    storage and retrieval of portlet assignments relative to this context.
    """

    def getPortletAssignments(manager):
        """Get a list of portlet assignments for the given viewlet manager
        for this specific context.
        """

    def setPortletAssignments(manager, portletAssignments):
        """Set the list of portlet assignments for the given viewlet manager
        for this specific context.
        """

class IPortletStorage(Interface):
    """A component for storing portlet assignments.
    
    Typically, this will be registered as a site-local utility.
    """
        
    def getPortletAssignmentsForContext(manager, context):
        """Get the list of portlets assigned to the given context for the given
        manager.
        """
    
    def setPortletAssignmentsForContext(manager, context, portletAssignments):
        """Set the list of portlets assigned to the given context for the given
        manager.
        """
        
    def getPortletAssignmentsForUser(manager, userId):
        """Get the list of portlets assigned to the given user id for the given
        manager.
        """
        
    def setPortletAssignmentsForUser(manager, userId, portletAssignments):
        """Set the list of portlets assigned to the given user id for the given
        manager.
        """
        
    def getPortletAssignmentsForGroup(manager, groupId):
        """Get the list of portlets assigned to the given context for the given
        manager.
        """
        
    def setPortletAssignmentsForGroup(manager, groupId, portletAssignments):
        """Set the list of portlets assigned to the given context for the given
        manager.
        """