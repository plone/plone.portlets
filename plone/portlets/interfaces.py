from zope.interface import Interface, Attribute
from zope import schema

from zope.app.container.interfaces import IContained
from zope.contentprovider.interfaces import IContentProvider
from zope.interface.common.mapping import IReadMapping

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

# Generic marker interface - a portlet may reference one of these

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

# Portlet assignment - new types of portlets may need one of these

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
    
# A content provider capable of rendering portlets - each type of portlet will
# need one of these
    
class IPortletRenderer(IContentProvider):
    """A special implementation of a content provider which is managed
    by an IPortletManager.
    
    Any object providing IPortletDataProvider should be adaptable to 
    IPortletRenderer in order to be renderable as a portlet. (In fact,
    the return value of IPortletAssignment.data needs to have such an
    adapter, regardless of whether it actually implements IPortletDataProvider)
    """
    
# Discovery of portlets

class IPortletRetriever(Interface):
    """A component capable of discovering portlets assigned to it for rendering.
    
    Typically, a content object and an IPortletManager will be multi-
    adapted to IPortletRetriever.
    """

    def getPortlet(id):
        """Get the IPortletAssignment with the specific id.
        
        Raises KeyError if the id cannot be found.
        """

    def getPortlets():
        """Return a list of IPortletAssignment's to be rendered
        """

# Management and storage of portlets relative to a context

class IPortletAssignable(Interface):
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
    
# A manager for portlets

class IPortletStorage(Interface):
    """A component for storing portlet assignments.
    """
        
    def getPortletAssignmentsForContext(uid):
        """Get the list of portlets assigned to the given context
        """
    
    def setPortletAssignmentsForContext(uid, portletAssignments):
        """Set the list of portlets assigned to the given context
        """
        
    def getPortletAssignmentsForUser(userId):
        """Get the list of portlets assigned to the given user id
        """
        
    def setPortletAssignmentsForUser(userId, portletAssignments):
        """Set the list of portlets assigned to the given user id
        """
        
    def getPortletAssignmentsForGroup(groupId):
        """Get the list of portlets assigned to the given group
        """
        
    def setPortletAssignmentsForGroup(groupId, portletAssignments):
        """Set the list of portlets assigned to the given group
        """

class IPortletManager(IPortletStorage, IContained):
    """A manager for portlets.
    
    This will typically adapt its context to IPortletRetriever and query it for 
    a list of IPortletRenderers to render.
    """
    
    def __call__(context, request, view):
        """Act as an adapter factory.
        
        When called, should return an IPortletManagerRenderer for rendering 
        this portlet manager and its portlets.
        
        The IPortletManager instance will be registered as a site-local
        adapter factory that the component architecture will use when it
        looks up adapters in the handler for a TAL provider: expression.
        
        See zope.contentprovider for more.
        """

class IPortletManagerRenderer(IContentProvider):
    """A content provider for rendering a portlet manager.
    """

    def filter(self, portlets):
        """Return a list of IPortletRenderer's to display that is a subset of
        the list of IPortletRenderer's passed in.
        """