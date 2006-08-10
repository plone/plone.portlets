from zope.interface import Interface, Attribute
from zope import schema

from zope.contentprovider.interfaces import IContentProvider

from zope.viewlet.interfaces import IViewlet
from zope.viewlet.interfaces import IViewletManager

# Context - the application layer must implement this

class IPortletContext(Interface):
    """A context in which portlets may be rendered.
    
    No default implementation exists for this interface - it must be provided
    by the application in order to tell the portlets infrastructure how to
    render portlets.
    """
    
    uid = schema.TextLine(title=u'A unique id for this context',
                          required=True,
                          readonly=True)
    
    parent = schema.Object(title=u'Parent of this context, should be adaptable to an IPortletContext', 
                           description=u'Should be None if there is no parent',
                           schema=Interface,
                           required=False,
                           readonly=True)
    
    userId = schema.TextLine(title=u'The id of the current user',
                             description=u'Should be None if there is no authenticated user',
                             required=False,
                             readonly=True)
                             
    groupIds = schema.Tuple(title=u'A list of group ids the current user is in',
                            description=u'Should be None if there is no authenticated user',
                            required=False,
                            readonly=True,
                            value_type=schema.TextLine())

# Portlet assignment - the application layer should implement a this

class IPortletAssignment(Interface):
    """Assignment of a portlet to a given viewlet manager relative to a 
    context, user or group.
    
    Implementations of this interface will typically be persistent, stored in
    an IPortletStorage.
    
    The 'data' attribute may be implemented as a property that retrieves the
    data object on-demand.
    """
    
    id = schema.TextLine(title=u'An id for this particular assignment',
                         description=u'This should be unique in the given viewlet manager and context',
                         required=True)
    
    data = Attribute(u'Portlet data object')

# Generic marker interface - the application layer may use this if desired

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
    
# Viewlets capable of rendering portlets - the application layer must implement
# adapters to these 
    
class IPortletViewlet(IContentProvider):
    """A special implementation of a viewlet (content provider) which is managed
    by an IPortletViewletManager.
    
    Any object providing IPortletDataProvider should be adaptable to 
    IPortletViewlet in order to be renderable as a portlet.
    """
    
# Special viewlet manager and viewlet to render portlets

class IPortletViewletManager(IViewletManager):
    """A ViewletManager that looks up its viewlets runtime.
    
    This will typically adapt its context to IPortletRetriever and query it for 
    a list of IPortletViewlets to render.
    """

# Discovery of portlets

class IPortletRetriever(Interface):
    """A component capable of discovering portlets assigned to it.
    
    Typically, a content object and an IPortletViewletManager will be multi-
    adapted to IPortletRetriever. The implementation of getPortlets() will most 
    likely query the IPortletStorage utility for the actual portlets to render.
    """

    def getPortlet(id):
        """Get the IPortletAssignment with the specific id.
        
        Raises KeyError if the id cannot be found.
        """

    def getPortlets():
        """Return a list of IPortletAssignment's to be rendered
        """

# Management and storage of portlets

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
        
    def getPortletAssignmentsForContext(manager, uid):
        """Get the list of portlets assigned to the given context for the given
        manager.
        """
    
    def setPortletAssignmentsForContext(manager, uid, portletAssignments):
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